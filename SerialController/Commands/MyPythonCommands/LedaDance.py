#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import PythonCommand

# 踊りレベル上げ
class SodateFRLG(PythonCommand):
    TAG = 'FEFW'
    NAME = 'レダ踊り稼ぎ'

    def __init__(self):
        super().__init__()

    def do(self):
        while(True):
            self.press(Direction.RIGHT)
            self.press(Button.A)
            self.press(Button.A)
            self.press(Direction.UP)
            self.press(Button.A)
            # 待機
            self.press(Direction.LEFT)
            self.press(Button.A)
            self.press(Button.A)
            self.press(Direction.DOWN)
            self.press(Direction.DOWN)
            self.press(Button.A)
            self.press(Button.A)
            self.press(Button.A)
            # 踊る
            for i in range(20):
                self.press(Button.B)
            self.press(Button.A)
            self.press(Direction.UP)
            self.press(Button.A)
            # ターン終了
            for i in range(15):
                self.press(Button.B)
