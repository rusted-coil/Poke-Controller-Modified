#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick
import numpy as np
import cv2
from PIL import Image
import time
import datetime
import os
import glob
import csv


class SeriesOfBattles(ImageProcPythonCommand):
    NAME = '戦闘エンジン改(交代対応)'

    def __init__(self, cam):
        super().__init__(cam)
        self.CaptureArea = None
        self.cam = cam

    def do(self):
        waza_position = 0  # 技のカーソル位置 上から0,1,2,3
        cum_elapsed_turn = 0  # 累計経過ターン数
        cum_output_time = 0  # 累計経過時間
        start_time = time.time()
        PATH = '/BattleEngine/'
        elapsed_turn = 0
        self.waitForImageRecognized(PATH + 'Tatakau.png')
        while True:
            self.checkIfAlive()
            battle_start_time = time.time()
            print('たたかうを認識')
            elapsed_turn += 1
            img = self.camera.readFrame()
            HP = self.containHPbar(img, 979, 63, 1244, 73)
            PokeName = self.RaidName(img)
            single = True
            if single:  # 現在はシングルバトル専用
                enemy_HP = self.containHPbar(img, 979, 63, 1244, 73)
            isWild = True

            if isWild:  # 対野生
                print('残り体力…{}　{}ターン目'.format(HP, elapsed_turn))
                if elapsed_turn == 1:
                    self.press(Direction.DOWN)
                    self.press(Button.A)
                    command_num = self.BattleEngine()
                    self.press(Button.B, wait=2)
                    self.press(Direction.UP)
                    self.wait(0.5)
            else:  # 相手の残りポケモン数取得(対トレーナー戦）　未実装
                print('相手の残りポケモン数…{}　相手の残り体力…{}　{}ターン目'.format(PokeName, HP, elapsed_turn))

            # Todo 相手の残り所持ポケモン数によって挙動を変える。
            # 具体的には、相手のポケモンが変わったときにだけこの処理を行う

            self.press(Button.A, wait=1.5)

            move = command_num - waza_position
            move_abs = abs(move)
            if move > 0:
                for i in range(move_abs):
                    self.press(Direction.DOWN)
                    waza_position += 1
                    self.wait(0.1)
            elif move < 0:
                for i in range(move_abs):
                    self.press(Direction.UP)
                    waza_position += 1
                    self.wait(0.1)
            else:
                pass

            self.press(Button.A, wait=1)
            self.press(Button.A, wait=8)  # たたかう
            while True:
                if self.isContainTemplate(PATH + 'Tatakau.png'):
                    print('たたかうを認識')
                    elapsed_turn += 1
                    img = self.camera.readFrame()
                    HP = self.containHPbar(img, 979, 63, 1244, 73)
                    print('相手の残り体力…{}　{}ターン目'.format(HP, elapsed_turn))
                    self.press(Button.A, wait=1)
                    self.press(Button.A, wait=1)
                    self.press(Button.A, wait=3)  # たたかう

                    if self.isContainTemplate(PATH + 'WazaSetumei.png'):  # PP切れや金縛り時
                        self.press(Direction.DOWN)
                        self.wait(1)
                        self.press(Button.A, wait=1)
                        self.press(Button.A, wait=1)

                elif self.isContainTemplate('Battle_end.png', 0.7, False):
                # self.isContainTemplate('dialogue.png', 0.7, False, True) or
                    print('戦闘終了(?)')

                    print('かかったターン数は{}'.format(elapsed_turn))
                    output_time = time.time() - battle_start_time
                    cum_output_time += output_time
                    print('かかった時間は{:.10}'.format(str(datetime.timedelta(seconds=output_time))))
                    while not (self.isContainTemplate("Network_offline.png", 0.9) or self.isContainTemplate(
                            "Network_online.png", 0.9)):
                        self.press(Button.B, wait=1)
                    waza_position = 0
                    break
                else:
                    self.wait(0.25)


    def BattleEngine(self):
        # while True:
        TEMPLATEPATH = './Template/BattleEngine/'
        template_path = ['kouka_batugun1.png', 'kouka_batugun2.png', 'kouka_batugun3.png',
                         'kouka_ari1.png', 'kouka_ari2.png', 'kouka_ari3.png',
                         'imahitotu1.png', 'imahitotu2.png', 'imahitotu3.png',
                         'kouka_nasi1.png', 'kouka_nasi2.png', 'kouka_nasi3.png']
        output_temp_list = ['効果抜群', '効果有り', '今一つ', '効果なし']
        output_list = ['変化技', '変化技', '変化技', '変化技']  # 書き換えが発生しなかった時は変化技を出力する
        while not self.isContainTemplate('BattleEngine/' + 'Sentaku.png'):
            self.wait(0.2)
        # print('画像認識 start')
        img = self.camera.readFrame()
        img = np.asarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img2 = img[0:400, 500:1280]
        data = [[3, 1, 0], [3, 1, 1], [3, 1, 2], [3, 1, 3]]  # 技の通り、タイプ一致、技のINDEX。ソート用の配列
        template_length = len(template_path)  # テンプレートの数だけ画像認識を実行する
        for i in range(template_length):
            template = cv2.imread(TEMPLATEPATH + template_path[i], 0)
            h, w = template.shape[:2]
            # 画像認識の閾値
            threshold = 0.93
            res = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
            max_val = 1
            while max_val > threshold:
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > threshold:
                    res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1, max_loc[0] - w:max_loc[0] + w] = 0
                    num = round((max_loc[1] - 120) / 90) % 4  # 画像の座標を技の位置に変換
                    output_list[num] = output_temp_list[int(i / 3)]
                    data[num][0] = int(i / 3)
        # ここからタイプの認識
        output_type_list = ['認識失敗', '認識失敗', '認識失敗', '認識失敗']  # 書き換えが発生しなかった時は認識失敗を出力する
        template_type_path = ['Normal.png', 'Fire.png', 'Water.png', 'Electric.png', 'Grass.png', 'Ice.png',
                              'Fighting.png', 'Poison.png', 'Ground.png', 'Flying.png', 'Psychic.png', 'Bug.png',
                              'Rock.png', 'Ghost.png', 'Dragon.png', 'Dark.png', 'Steal.png', 'Fairly.png']
        output_type_temp_list = ['ノーマル', 'ほのお', 'みず', 'でんき', 'くさ', 'こおり',
                                 'かくとう', 'どく', 'じめん', 'ひこう', 'エスパー', 'むし',
                                 'いわ', 'ゴースト', 'ドラゴン', 'あく', 'はがね', 'フェアリー']
        your_type = []
        template_length = len(template_type_path)  # テンプレートの数だけ画像認識を実行する
        for i in range(template_length):
            template = cv2.imread(TEMPLATEPATH + template_type_path[i], 0)
            h, w = template.shape[:2]
            # 画像認識の閾値
            threshold = 0.9
            res = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
            max_val = 1
            while max_val > threshold:
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > threshold:
                    res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1, max_loc[0] - w:max_loc[0] + w] = 0
                    print(output_type_temp_list[int(i)], '…', max_loc)
                    if max_loc[1] < 100:
                        your_type.append(output_type_temp_list[int(i)])
                    else:
                        num = round((max_loc[1] - 130) / 70) % 4  # 画像の座標を技の位置に変換
                        output_type_list[num] = output_type_temp_list[int(i)]

        # ここまでタイプの処理

        print('ポケモンのタイプは{}'.format(your_type))
        print('技のタイプは{}'.format(output_type_list))
        print('技の通りは{}'.format(output_list))

        for a in range(len(your_type)):
            for b in range(len(output_type_list)):
                if output_type_list[b] == your_type[a]:
                    data[b][1] = 0  # タイプ一致

        sorted_data = sorted(data, key=lambda x: (x[0], x[1], x[2]))

        print('選ぶべき技は', sorted_data[0][2] + 1, '個目の技')

        return sorted_data[0][2]


    def containHPbar(self, img, x1=461, y1=89, x2=819, y2=90):
        img2 = img[y1:y2, x1:x2]  # HPバーのみを切り取り
        cv2.imwrite('HPcolor.png', img2), print('capture succeeded: ')  # 正しく切り取れているか念の為保存
        img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # グレースケールに変換
        img4 = cv2.threshold(img3, 120, 255, cv2.THRESH_BINARY)  # 画像を二値化。閾値は２つ目の引数。0が黒、255が白
        binary_list = img4[-1][img4[-1].shape[0] // 2 - 1]  # img4の縦方向中央(行)の色情報を格納
        HP = np.argmin(binary_list) - 1  # binary_listのなかで最小値（つまり０）のインデックスから１を引いたものがHPバーの長さ
        if np.all(HP==0):
            HP = 0
        elif HP == -1:  # HPmaxの時だけこの処理
            HP = img2.shape[1]  # つまり100％
        result = str(int(HP * 100 / img2.shape[1])) + '%'
        return result


    def RaidName(self, img, x1=480, y1=0, x2=800, y2=78, cnt=0):  # レイドのポケモンを認識します
        # テンプレートマッチングではなく単純な加算のみで画像の判別を行うことで高速化しています。
        img2 = img[y1:y2, x1:x2]
        img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # Grayscale に変換
        img4 = cv2.threshold(img3, 254, 255, cv2.THRESH_BINARY)[1]  # 二値化。黒背景白文字
        img5 = cv2.threshold(img4, 254, 255, cv2.THRESH_BINARY_INV)[1]  # 色空間を二値化(かつ白黒反転)白背景黒文字
        images = glob.glob('./Template/BattleEngine/NameList/*.png')
        for i, fname in enumerate(images):
            mask = cv2.imdecode(np.fromfile(fname, dtype=np.uint8),
                                cv2.IMREAD_GRAYSCALE)  # imreadと同等だが、cv2が日本語パスを読み込まないためにnumpyで読み込んでいる。
            dst = mask + img4  # ２つの画像を重ね合わせる。正しいマスク画像ならばほとんど真っ白な画像が生成される。
            if np.count_nonzero(dst == 0) < 30:  # 閾値。黒いピクセルの数が少ないほど一致度が高い。
                # print('テンプレートとの差…'+str(np.count_nonzero(dst == 0)))
                PokeName = os.path.splitext(os.path.basename(fname))[0]  # 画像の名前を取得
                return PokeName
        '''
        #メモ
        print(all([all(img[i] == 255) for i in range(len(img))]))#img6の全要素が255の時にTrue。使いにくかったので採用せず。
        '''
        if cnt <= 1:  # 再検索をかける回数
            cnt += 1
            # print('認識失敗または該当なし。再検索します')
            new_img = self.camera.readFrame()
            return self.RaidName(img=new_img, cnt=cnt)
        else:
            cv2.imwrite('./Template/BattleEngine/NameList/img' + str(
                len(glob.glob('./Template/RaidName/templatelist/*')) + 1) + '.png', img5)
            return '該当なし'
