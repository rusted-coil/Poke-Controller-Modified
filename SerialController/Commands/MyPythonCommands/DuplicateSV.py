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
            # ライドフォルムに戻す
            self.press(Button.A)
            self.wait(0.3)
            self.press(Hat.TOP)
            self.press(Hat.TOP)
            self.press(Button.A)
            self.wait(1.5)
            self.press(Button.A)
            self.wait(0.3)
            self.press(Button.A)
            self.wait(2.5)
            self.press(Button.A)
            self.wait(0.5)

            # バトルチームを開く
            self.press(Hat.RIGHT)
            self.wait(0.1)
            self.press(Hat.BTM)
            self.wait(0.1)
            self.press(Hat.BTM)
            self.wait(0.1)
            self.press(Button.A)
            self.wait(2.5)
            self.press(Button.X)
            self.press(Button.X)
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
