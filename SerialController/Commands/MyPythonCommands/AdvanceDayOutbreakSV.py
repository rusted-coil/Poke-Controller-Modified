#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

class AdvanceDayOutbreakSV(PythonCommand):
    NAME = 'SV大量発生厳選'

    def __init__(self):
        super().__init__()

    def do(self):
        # HOME画面に戻り設定をクリック
        self.press(Button.HOME, 0.05, 1.0)
        self.press(Hat.BTM, 0.05, 0.05)
        for i in range(5): # HOMEメニューの項目が増えたら変更する
            self.press(Hat.RIGHT, 0.05, 0.05)

        # 設定画面で本体の設定へ
        self.press(Button.A, 0.05, 0.05)
        self.press(Hat.BTM, 2.2, 0.05)
        self.press(Button.A, 0.05, 0.05)

        # 本体の設定で時刻変更へ
        for i in range(3):
            self.press(Hat.BTM, 0.05, 0.05)
        self.press(Hat.BTM, 0.3, 0.05)
        for i in range(2):
            self.press(Hat.BTM, 0.05, 0.05)
        self.press(Button.A, 0.05, 0.3)
        self.press(Hat.BTM, 0.05, 0.05)
        self.press(Hat.BTM, 0.05, 0.05)

        # 設定画面を開いて閉じる
        self.press(Button.A, 0.05, 0.3) # 日時変更画面へ
        for i in range(6): # 完了
            self.press(Button.A, 0.05, 0.05)

        # ゲームに戻る
        self.press(Button.HOME, 0.05, 1.0)
        self.press(Button.A, 0.05, 0.5)
