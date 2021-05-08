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


def multiContainTemplate(self, path, templates, threshold=0.95):
    img = self.camera.readFrame()  # キャプチャーを取得
    img = np.asarray(img)  # num.pyが読み込めるndarryに変換
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # グレースケールに変換
    template_length = len(templates)  # テンプレートの数を数える
    result = []
    for i in range(template_length):  # テンプレートそれぞれに対して以下の処理を順番に実行
        template = cv2.imread(path + templates[i], 0)  # テンプレートをグレースケールで読み込み
        h, w = template.shape[:2]  # テンプレートの縦横の大きさを取得
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # imgとキャプチャの一致度合いをヒートマップで取得
        max_val = 1  # 以降の処理を最低１回は実行するためのダミー
        while max_val > threshold:  # 一致度が閾値を超える場所がなくなるまで以下を実行
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > threshold:
                res[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w] = 0  # 一致した場所を0でマスク
                result.append((i, max_loc))

                # ↓必要なければ当然消しても良い。iは０枚目から始まることに注意
                print(i, '枚目のテンプレートが一致した箇所は', max_loc)
        print
    return result


class ScreenShot(ImageProcPythonCommand):
    NAME = 'ポケモンHOMEのポケモンリスト化'

    def __init__(self, cam):
        super().__init__(cam)
        self.ls_type = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice",
                        "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
                        "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
        self.moves = None
        self.HP = np.zeros((3, 10))
        self.Atk = np.zeros((3, 10))
        self.SpAtk = np.zeros((3, 10))
        self.Def = np.zeros((3, 10))
        self.SpDef = np.zeros((3, 10))
        self.Spd = np.zeros((3, 10))
        self.Dex = np.zeros((3, 10))
        self.stats_temp = [[] for i in range(6)]
        self.dex = []
        self.ls_dex = []
        self.statistics = []
        self.stat_array = None

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

    def StatsCheck(self, stt, path, idx, use_gray=True, show_value=False, img=None, single_match=True):
        ret, loc, wh, res = self.isContainTemplate(path,
                                                   use_gray=use_gray,
                                                   threshold=0.75,
                                                   show_value=show_value,
                                                   img=img,
                                                   ret="match",
                                                   single_match=single_match
                                                   )
        print(wh)
        if loc[0] is not None:
            # num = [-1, -1, -1]
            for pt in zip(*loc[::-1]):
                isExist = [False, -1]
                for i, loc_ in enumerate(self.stats_temp[stt]):
                    x = loc_[0]
                    y = loc_[1]
                    d = (pt[0] + wh[0] - x) ** 2 + (pt[1] + wh[1] - y) ** 2
                    if d < 30:
                        isExist = [True, i]

                # if pt[0] in [i for i in range(0, 11)]:
                #     x_ = 5
                # elif pt[0] in [i for i in range(15, 26)]:
                #     x_ = 20
                # elif pt[0] in [i for i in range(30, 41)]:
                #     x_ = 35
                # else:
                #     x_ = pt[0]

                if not isExist[0] and ret:
                    self.stats_temp[stt].append([pt[0] + wh[0], pt[1] + wh[1], int(path[18]), res[pt[1], pt[0]]])
                elif isExist and ret and isExist[1] != -1 \
                        and self.stats_temp[stt][isExist[1]][2] == int(path[18]) \
                        and self.stats_temp[stt][isExist[1]][3] < res[pt[1], pt[0]]:
                    # self.stats[stt].append([pt[0], pt[1], int(path[18]), res[pt[1], pt[0]]])
                    self.stats_temp[stt][isExist[1]] = [pt[0] + wh[0], pt[1] + wh[1], int(path[18]), res[pt[1], pt[0]]]
                elif isExist and ret and isExist[1] != -1 and self.stats_temp[stt][isExist[1]][3] < res[pt[1], pt[0]]:
                    self.stats_temp[stt].append([pt[0] + wh[0], pt[1] + wh[1], int(path[18]), res[pt[1], pt[0]]])
                    # self.stats[stt][isExist[1]] = [pt[0], pt[1], int(path[18]), res[pt[1], pt[0]]]
        # if ret:
        #     self.stats[stt].append(pts)

    def DexCheck(self, n, path, idx, use_gray=True, show_value=False, img=None, single_match=True):
        ret, loc, wh, res = self.isContainTemplate(path,
                                                   use_gray=use_gray,
                                                   threshold=0.84,
                                                   show_value=show_value,
                                                   img=img,
                                                   ret="match",
                                                   single_match=single_match
                                                   )
        if loc[0] is not None:
            for pt in zip(*loc[::-1]):
                isExist = False
                for loc_ in self.dex:
                    x = loc_[0]
                    y = loc_[1]
                    d = (pt[0] - x) ** 2 + (pt[1] - y) ** 2
                    if d < 30:
                        isExist = True
                if not isExist and ret:
                    self.dex.append([pt[0] + wh[0], pt[1] + wh[1], int(path[18]), res[pt[1], pt[0]]])

    def crop(self, img):
        # 画像の読み込み
        # Grayscale に変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray', gray)

        # 色空間を二値化
        img2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow('img2', img2)

        # 輪郭を抽出
        contours = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        # print(contours)

        # 輪郭の座標をリストに代入していく
        x1 = []  # x座標の最小値
        y1 = []  # y座標の最小値
        x2 = []  # x座標の最大値
        y2 = []  # y座標の最大値
        for i in range(1, len(contours)):  # i = 1 は画像全体の外枠になるのでカウントに入れない
            ret = cv2.boundingRect(contours[i])
            x1.append(ret[0])
            y1.append(ret[1])
            x2.append(ret[0] + ret[2])
            y2.append(ret[1] + ret[3])
        print("###", x1, flush=True)
        # 輪郭の一番外枠を切り抜き
        x1_min = min(x1)
        y1_min = min(y1)
        x2_max = max(x2)
        y2_max = max(y2)
        # cv2.rectangle(img, (x1_min, y1_min), (x2_max, y2_max), (0, 255, 0), 3)

        crop_img = img[:, x1_min:x2_max]
        # cv2.imshow('crop_img', crop_img)
        cv2.imwrite(str(img)[:10] + ".png", crop_img)

        return crop_img

    def do(self):
        # Hexagon.png
        # 148, 216 ~ 367,464
        # moves
        # 1: 554-599, 236-281
        # 2: 294-339
        # 3: 351-396
        # 4: 409-454
        # q1 = queue.Queue()
        # q2 = queue.Queue()
        # q3 = queue.Queue()
        # q4 = queue.Queue()

        poke_num = 0
        while True:
            self.press(Button.R, wait=0.1, ifPrint=False)
            poke_num += 1
            self.moves = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
            self.stats_temp = [[] for i in range(7)]
            self.statistics = [[[-1] * 4 for i in range(3)] for i in range(7)]
            self.HP = np.zeros((3, 10))
            self.Atk = np.zeros((3, 10))
            self.SpAtk = np.zeros((3, 10))
            self.Def = np.zeros((3, 10))
            self.SpDef = np.zeros((3, 10))
            self.Spd = np.zeros((3, 10))
            self.Dex = np.zeros((3, 10))
            self.stat_array = [self.HP, self.Atk, self.Def, self.SpAtk, self.SpDef, self.Spd, self.Dex]
            _img = self.camera.image_bgr

            # q1.put(_img)
            # q2.put(_img)
            # q3.put(_img)
            # q4.put(_img)

            for i in range(18):
                t1 = threading.Thread(target=self.TypeCheck,
                                      args=(0, f"ListupPoke/type/{self.ls_type[i]}.png", i),
                                      kwargs={"use_gray": False,
                                              "show_value": False,
                                              "img": _img[236:281, 554:599]}
                                      )
                t1.start()
                t2 = threading.Thread(target=self.TypeCheck,
                                      args=(1, f"ListupPoke/type/{self.ls_type[i]}.png", i),
                                      kwargs={"use_gray": False,
                                              "show_value": False,
                                              "img": _img[294:339, 554:599]}
                                      )
                t2.start()
                t3 = threading.Thread(target=self.TypeCheck,
                                      args=(2, f"ListupPoke/type/{self.ls_type[i]}.png", i),
                                      kwargs={"use_gray": False,
                                              "show_value": False,
                                              "img": _img[351:396, 554:599]}
                                      )
                t3.start()
                t4 = threading.Thread(target=self.TypeCheck,
                                      args=(3, f"ListupPoke/type/{self.ls_type[i]}.png", i),
                                      kwargs={"use_gray": False,
                                              "show_value": False,
                                              "img": _img[409:454, 554:599]}
                                      )
                t4.start()
            for i in range(10):
                # 235~280 ,195~215
                s1 = threading.Thread(target=self.StatsCheck,
                                      args=(0, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[190:220, 230:285]),
                                              "single_match": False
                                              }
                                      )
                s1.start()
                s2 = threading.Thread(target=self.StatsCheck,
                                      args=(1, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[280:305, 395:445]),
                                              "single_match": False
                                              }
                                      )
                s2.start()
                s3 = threading.Thread(target=self.StatsCheck,
                                      args=(2, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[433:457, 395:445]),
                                              "single_match": False
                                              }
                                      )
                s3.start()
                s4 = threading.Thread(target=self.StatsCheck,
                                      args=(3, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[280:305, 70:120]),
                                              "single_match": False
                                              }
                                      )
                s4.start()
                s5 = threading.Thread(target=self.StatsCheck,
                                      args=(4, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[433:457, 70:120]),
                                              "single_match": False
                                              }
                                      )
                s5.start()
                s6 = threading.Thread(target=self.StatsCheck,
                                      args=(5, f"ListupPoke/number/{i}.png", i),
                                      kwargs={"use_gray": True,
                                              "show_value": False,
                                              "img": self.crop(_img[465:490, 230:290]),
                                              "single_match": False
                                              }
                                      )
                s6.start()
                dex = threading.Thread(target=self.StatsCheck,
                                       args=(6, f"ListupPoke/number/{i}.png", i),
                                       kwargs={"use_gray": True,
                                               "show_value": False,
                                               "img": cv2.bitwise_not(_img[175:210, 570:625]),
                                               "single_match": False
                                               }
                                       )
                dex.start()
                s1.join()
                s2.join()
                s3.join()
                s4.join()
                s5.join()
                s6.join()
                dex.join()

            t1.join()
            t2.join()
            t3.join()
            t4.join()
            # for l in self.moves:
            #     if l[0] != -1:
            #         pass
            #         print(self.ls_type[l[1]],round(l[0],4),end="")
            #         print(self.ls_type[l[1]]
            #         , end=","
            #         )
            #     else:
            #         print("")
            #         pass
            # print(self.stats_temp)
            # print(self.statistics[0][-1][0])
            for i in range(7):
                self.stats_temp[i] = sorted(self.stats_temp[i], key=lambda x: (x[3]))
                self.stats_temp[i] = sorted(self.stats_temp[i], key=lambda x: (x[0]), reverse=True)
                # print(self.stats_temp)
                # pos = 2
                # for j in self.stats_temp[i]:
                #     # print(j)
                #     if self.statistics[i][pos][0] == -1:
                #         self.statistics[i][pos] = j
                #     elif self.statistics[i][pos][0] != -1 and \
                #             abs(self.statistics[i][pos][0] - j[0]) <= 7 and \
                #             self.statistics[i][pos][3] < j[3]:
                #         print("###", self.statistics[i][pos][0])
                #         self.statistics[i][pos] = j
                #     elif abs(self.statistics[i][pos][0] - j[0]) > 7:
                #         print("%%%", self.statistics[i][pos][0] - j[0])
                #         pos -= 1
                for k, s in enumerate(self.stats_temp[i]):
                    # print(k)
                    self.stat_array[i][(-k - 1) % 3, s[2]] = s[3]
            # for i in range(7):
            #     for j in range(3):
            #         if self.statistics[i][j][0] == -1:
            #             self.statistics[i][j][2] = 0
            # print(self.stat_array)
            print(self.stats_temp)
            # for n in range(7):
            #     self.statistics[n] = self.statistics[n][0][2] * 100 + \
            #                          self.statistics[n][1][2] * 10 + \
            #                          self.statistics[n][2][2] * 1
            # self.stats[i] = self.stats[i][0][2] * 100 + self.stats[i][1][2] * 10 + self.stats[i][2][2] * 1

            print("statistics", self.statistics)
            self.dex = []
            self.checkIfAlive()
            # break
