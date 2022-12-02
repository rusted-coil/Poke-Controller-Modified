#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat, Direction
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
        self.press(Button.A, 0.15, 1.0)
        self.press(Hat.TOP, 0.15, 0.2)
        self.press(Hat.TOP, 0.15, 0.1)
        self.press(Button.A, 0.15, 2.0) # メニュー選択
        self.press(Button.A, 0.15, 0.1) # ライドフォルムにしますか→はい
        self.press(Button.A, 0.15, 0.1)
        self.press(Button.A, 0.15, 0.1)
        self.press(Button.A, 0.15, 0.1)
        self.wait(3.0)
        self.press(Button.A, 0.15, 0.5) # ライドフォルムになった

        # バトルチームを開く
        self.press(Hat.RIGHT, 0.15, 0.1)
        self.press(Hat.BTM, 0.15, 0.2)
        self.press(Hat.BTM, 0.15, 0.1)
        self.press(Button.A, 0.15, 3.0)
        self.press(Button.X, 0.3, 0.2)
        self.press(Button.X, 0.3, 0.2)
        self.press(Button.L, 0.15, 0.5)

        # 道具を預かる
        self.press(Button.A, 0.15, 1.0)
        self.press(Hat.BTM, 0.15, 0.1)
        self.press(Hat.BTM, 0.15, 0.1)
        self.press(Hat.BTM, 0.15, 0.1)
        self.press(Button.A, 0.15, 1.0)

        # 戻る
        self.press(Button.B, 0.15, 2.5)
        self.press(Hat.LEFT, 0.15, 0.5)

    # はまり防止
    def recovery(self):
        for i in range(10):
            self.press(Button.B, 0.15, 0.1)
        self.press(Direction.UP, 0.2, 1.0)
        self.press(Button.X, 0.15, 1.0)
        self.press(Hat.RIGHT, 0.15, 0.5)
        self.press(Hat.LEFT, 0.15, 0.5)
        self.press(Hat.TOP, 2.0, 0.6)
        self.press(Hat.BTM, 0.15, 0.5)
