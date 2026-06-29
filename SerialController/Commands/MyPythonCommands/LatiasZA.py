#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

class LatiasZA(CustomPythonCommand):
    TAG = 'ZA'
    NAME = 'ZAラティアス色厳選'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        # 左スティックの上と下を一定秒数ごと、指定回数繰り返す
        for i in range(25):
            self.hold(Direction.UP)
            self.press(Button.B, 0.05, 0.2)
            self.wait(3.6)
            self.holdEnd(Direction.UP)
            self.wait(1.0)

            self.hold(Direction.DOWN)
            self.press(Button.B, 0.05, 0.2)
            self.wait(3.5)
            self.holdEnd(Direction.DOWN)
            self.wait(1.0)
