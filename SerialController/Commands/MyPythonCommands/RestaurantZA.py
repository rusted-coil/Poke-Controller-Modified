#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

# レストランのカウンター前で話しかけられる所に立ってスタート
class RestaurantZA(CustomPythonCommand):
    NAME = 'ZAレストラン周回'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        while True:
            self.hold(Button.ZL)
            for i in range(10):
                self.press(Button.A)
            self.holdEnd(Button.ZL)
            self.wait(0.5)
