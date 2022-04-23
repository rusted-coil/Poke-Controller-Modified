#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from .Util.DiggingUtil import DiggingImageProcessor

class DiggingStarter(CustomPythonCommand):
    NAME = '化石掘り開始'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        gridList = [
                ( 2, 2), (5, 2), (8, 2), (11, 2),
                (11, 5), (8, 5), (5, 5), ( 2, 5),
                (2, 8), (5, 8), (8, 8), (11, 8),
            ]
        self.press(Direction.UP, 1.0, 0.05)
        result = DiggingImageProcessor.GetGridsDurability(self, self.Preview, gridList)
        (px, py) = (6, 0)
        count = 0
        for x, y in gridList:
            if x < px:
                for i in range(px - x):
                    self.press(Hat.LEFT, 0.05, 0.05)
            if x > px:
                for i in range(x - px):
                    self.press(Hat.RIGHT, 0.05, 0.05)
            if y < py:
                for i in range(py - y):
                    self.press(Hat.TOP, 0.05, 0.05)
            if y > py:
                for i in range(y - py):
                    self.press(Hat.BTM, 0.05, 0.05)
            for i in range(result[count]):
                self.press(Button.A, 0.05, 0.1)
            px = x
            py = y
            count = count + 1
        print(result)
        