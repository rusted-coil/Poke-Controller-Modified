#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import KeyPress, Button, Direction, Stick
from Commands.PythonCommandBase import ImageProcPythonCommand
import time
import threading
import queue
import numpy as np
import cv2
from PIL import Image
import pyocr
import pyocr.builders
from PIL import Image, ImageOps
import pandas as pd
import re


def cv2pil(image):
    """ OpenCV型 -> PIL型 """
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    new_image.resize((new_image.width * 2, new_image.height * 2))
    return new_image


def pil2cv(image):
    """ PIL型 -> OpenCV型 """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        new_image.resize((new_image.width * 3, new_image.height * 3))
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        new_image.resize((new_image.width * 3, new_image.height * 3))
    return new_image


class HomeOCR(ImageProcPythonCommand):
    NAME = 'ポケモンHOME_OCR'

    def __init__(self, cam):
        super().__init__(cam)
        self.nature_up = [[325, 355], [60, 80], [80, 100]]
        self.nature_down = [[180, 200], [70, 90], [70, 90]]
        self.ls_type = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice",
                        "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
                        "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
        self.moves = None
        self.HP = -1
        self.Atk = -1
        self.SpAtk = -1
        self.Def = -1
        self.SpDef = -1
        self.Spd = -1
        self.Dex = -1
        self.stats_temp = [-1] * 7
        self.dex = []
        self.ls_dex = []
        self.statistics = []
        self.stat_array = None
        self.tools = pyocr.get_available_tools()
        if len(self.tools) == 0:
            print('ocrできません')
            self.finish()
        self.tool = self.tools[0]

    def TypeCheck(self, move, path, idx, use_gray=True, show_value=False, img=None, single_match=True):
        # print(single_match)
        ret, value = self.isContainTemplate(path,
                                            use_gray=use_gray,
                                            threshold=0.90,
                                            show_value=show_value,
                                            img=img,
                                            ret="match",
                                            single_match=single_match
                                            )
        if ret and self.moves[move][0] < value:
            self.moves[move] = [value, idx]

    def StatsOCR(self, id1, id2, img):
        num = self.tool.image_to_string(
            img,
            lang='eng',
            builder=pyocr.builders.DigitBuilder(tesseract_layout=8)
            # builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )

        num = re.sub(r'\D', '', num)
        self.statistics[id1][id2] = num

    def isContainColorHSV(self, img, H_d, S_d, V_d, H_u, S_u, V_u, idx, poke_num):
        # 色基準で2値化する。
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # hsv2 = copy.copy(hsv)
        # print(H_d,flush=True)
        # 色の範囲を指定する
        lower_color_d = np.array([H_d[0] / 2, S_d[0] * 255 / 100, V_d[0] * 255 / 100])
        upper_color_d = np.array([H_d[1] / 2, H_d[1] * 255 / 100, H_d[1] * 255 / 100])
        lower_color_u = np.array([H_u[0] / 2, S_u[0] * 255 / 100, V_u[0] * 255 / 100])
        upper_color_u = np.array([H_u[1] / 2, S_u[1] * 255 / 100, V_u[1] * 255 / 100])

        # 指定した色に基づいたマスク画像の生成
        mask = cv2.inRange(hsv, lower_color_d, upper_color_d)
        mask2 = cv2.inRange(hsv, lower_color_u, upper_color_u)
        output = cv2.bitwise_and(hsv, hsv, mask=mask)
        output2 = cv2.bitwise_and(hsv, hsv, mask=mask2)

        if np.count_nonzero(output2 > 0) > 1:
            self.statistics[poke_num][7][0] = idx
        if np.count_nonzero(output > 0) > 1:
            self.statistics[poke_num][7][1] = idx
        return output

    def do(self):
        # Hexagon.png
        # 148, 216 ~ 367,464
        # moves
        # 1: 554-599, 236-281
        # 2: 294-339
        # 3: 351-396
        # 4: 409-454

        count_n = 10

        poke_num = 0
        for i in range(count_n):
            _img = self.camera.image_bgr
            self.statistics.append([-1] * 8)
            self.statistics[-1][7] = [0, 0]
            self.press(Button.R, wait=0.1, ifPrint=False)
            self.moves = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
            self.stat_array = [self.HP, self.Atk, self.Def, self.SpAtk, self.SpDef, self.Spd, self.Dex]
            ret, _img2 = cv2.threshold(_img, 170, 255, cv2.THRESH_BINARY)

            # for i in range(18):
            #     t1 = threading.Thread(target=self.TypeCheck,
            #                           args=(0, f"ListupPoke/type/{self.ls_type[i]}.png", i),
            #                           kwargs={"use_gray": False,
            #                                   "show_value": False,
            #                                   "img": _img[236:281, 554:599]}
            #                           )
            #     t1.start()
            #     t2 = threading.Thread(target=self.TypeCheck,
            #                           args=(1, f"ListupPoke/type/{self.ls_type[i]}.png", i),
            #                           kwargs={"use_gray": False,
            #                                   "show_value": False,
            #                                   "img": _img[294:339, 554:599]}
            #                           )
            #     t2.start()
            #     t3 = threading.Thread(target=self.TypeCheck,
            #                           args=(2, f"ListupPoke/type/{self.ls_type[i]}.png", i),
            #                           kwargs={"use_gray": False,
            #                                   "show_value": False,
            #                                   "img": _img[351:396, 554:599]}
            #                           )
            #     t3.start()
            #     t4 = threading.Thread(target=self.TypeCheck,
            #                           args=(3, f"ListupPoke/type/{self.ls_type[i]}.png", i),
            #                           kwargs={"use_gray": False,
            #                                   "show_value": False,
            #                                   "img": _img[409:454, 554:599]}
            #                           )
            #     t4.start()
            #
            # t1.join()
            # t2.join()
            # t3.join()
            # t4.join()

            DEX = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 0, cv2pil(_img2[175:210, 570:625]))
            )
            DEX.start()
            H = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 1, cv2pil(_img2[190:220, 230:285]))
            )
            H.start()
            A = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 2, cv2pil(_img2[280:305, 395:445]))
            )
            A.start()
            B = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 3, cv2pil(_img2[433:457, 395:445]))
            )
            B.start()
            C = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 4, cv2pil(_img2[280:305, 70:120]))
            )
            C.start()
            D = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 5, cv2pil(_img2[433:457, 70:120]))
            )
            D.start()
            S = threading.Thread(
                target=self.StatsOCR,
                args=(poke_num, 6, cv2pil(_img2[464:490, 230:285]))
            )
            S.start()

            # print("H", self.StatsOCR(cv2pil(_img2[190:220, 230:285])))
            # print("A", self.StatsOCR(cv2pil(_img2[280:305, 395:445])))
            # print("B", self.StatsOCR(cv2pil(_img2[433:457, 395:445])))
            # print("C", self.StatsOCR(cv2pil(_img2[280:305, 70:120])))
            # print("D", self.StatsOCR(cv2pil(_img2[433:457, 70:120])))
            # print("S", self.StatsOCR(cv2pil(_img2[465:490, 230:290])))
            # print("Dex", self.StatsOCR(cv2pil(_img2[175:210, 570:625])))

            # Nature_H = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[150:200, 230:280], *self.nature_down, *self.nature_up, 0, poke_num)
            # )
            # Nature_H.start()
            # Nature_A = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[230:280, 370:470], *self.nature_down, *self.nature_up, 1, poke_num)
            # )
            # Nature_A.start()
            # Nature_B = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[390:440, 370:470], *self.nature_down, *self.nature_up, 2, poke_num)
            # )
            # Nature_B.start()
            # Nature_C = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[230:280, 40:150], *self.nature_down, *self.nature_up, 3, poke_num)
            # )
            # Nature_C.start()
            # Nature_D = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[390:440, 40:150], *self.nature_down, *self.nature_up, 4, poke_num)
            # )
            # Nature_D.start()
            # Nature_S = threading.Thread(
            #     target=self.isContainColorHSV,
            #     args=(_img[490:530, 200:300], *self.nature_down, *self.nature_up, 5, poke_num)
            # )
            # Nature_S.start()
            time.sleep(0.28)
            _img3 = self.camera.image_bgr
            self.isContainColorHSV(_img3[150:200, 230:280], *self.nature_down, *self.nature_up, 0, poke_num)
            self.isContainColorHSV(_img3[230:280, 370:470], *self.nature_down, *self.nature_up, 1, poke_num)
            self.isContainColorHSV(_img3[390:440, 370:470], *self.nature_down, *self.nature_up, 2, poke_num)
            self.isContainColorHSV(_img3[230:280, 40:150], *self.nature_down, *self.nature_up, 3, poke_num)
            self.isContainColorHSV(_img3[390:440, 40:150], *self.nature_down, *self.nature_up, 4, poke_num)
            self.isContainColorHSV(_img3[490:530, 200:300], *self.nature_down, *self.nature_up, 5, poke_num)

            # self.isContainColorHSV(_img[230:280, 40:150], *self.nature_down)
            # self.isContainColorHSV(_img[230:280, 40:150], *self.nature_up)

            # for l in self.moves:
            #     if l[0] != -1:
            #         pass
            #         # print(self.ls_type[l[1]], round(l[0], 4), end="")
            #         print(self.ls_type[l[1]]
            #               # , end=","
            #               )
            #     else:
            #         print("")
            #         pass
            # H.join()

            poke_num += 1
            self.checkIfAlive()
            # break
        DEX.join()
        H.join()
        A.join()
        B.join()
        C.join()
        D.join()
        S.join()
        # Nature_H.join()
        # Nature_A.join()
        # Nature_B.join()
        # Nature_C.join()
        # Nature_D.join()
        # Nature_S.join()
        df = pd.DataFrame(self.statistics,
                          columns=['DEX', 'HP', 'Atk', 'Def', 'Sp.Atk', 'Sp.Def', 'Speed', 'Nature'])
        print(df)
