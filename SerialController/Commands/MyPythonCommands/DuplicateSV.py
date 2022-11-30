#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

class DuplicateSV(PythonCommand):
    NAME = 'SV増殖'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            for i in range(30):
                self.duplicate()
            self.recovery()

    # 道具を1個増やす
    # * 2匹目をバグミライドンにし、カーソルを合わせた状態でスタート
    # * ボックスは1から始まるようにしておく
    def duplicate(self):
        # ライドフォルムに戻す
        self.press(Button.A)
        self.wait(0.8)
        self.press(Hat.TOP)
        self.wait(0.1)
        self.press(Hat.TOP)
        self.wait(0.1)
        self.press(Button.A) # メニュー選択
        self.wait(2.0)
        self.press(Button.A) # ライドフォルムにしますか→はい
        self.wait(0.2)
        self.press(Button.A)
        self.wait(0.2)
        self.press(Button.A)
        self.wait(0.2)
        self.press(Button.A)
        self.wait(3.0)
        self.press(Button.A) # ライドフォルムになった
        self.wait(0.5)

        # バトルチームを開く
        self.press(Hat.RIGHT)
        self.wait(0.1)
        self.press(Hat.BTM)
        self.wait(0.1)
        self.press(Hat.BTM)
        self.wait(0.1)
        self.press(Button.A)
        self.wait(3.0)
        self.press(Button.X)
        self.wait(0.3)
        self.press(Button.X)
        self.wait(0.3)
        self.press(Button.L)
        self.wait(0.5)

        # 道具を預かる
        self.press(Button.A)
        self.wait(1.0)
        self.press(Hat.BTM)
        self.wait(0.1)
        self.press(Hat.BTM)
        self.wait(0.1)
        self.press(Hat.BTM)
        self.wait(0.1)
        self.press(Button.A)
        self.wait(0.5)

        # 戻る
        self.press(Button.B)
        self.wait(2.5)
        self.press(Hat.LEFT)
        self.wait(0.5)

    # はまり防止
    def recovery(self):
        for i in range(10):
            self.press(Button.B)
            self.wait(0.1)
        self.press(Button.X)
        self.wait(1.0)
        self.press(Hat.RIGHT)
        self.wait(0.5)
        self.press(Hat.LEFT)
        self.wait(0.5)
        self.press(Hat.TOP, 2.0, 0.6)
        self.press(Hat.BTM)
        self.wait(0.5)
