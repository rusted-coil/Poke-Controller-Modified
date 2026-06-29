#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

# シンボル前でレポートした状態で話しかけられる所に立ってスタート
class ShinyFRLGStarter(CustomPythonCommand):
    TAG = 'FRLG'
    NAME = 'FRLG伝説色厳選'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        fs = 0
        f1 = 0
        while True:
            f2 = fs - f1
            self.Reset(f1)
            self.wait(f2 / 60.0)
            for i in range(10): # エンカウント
                self.press(Button.A, 0.05, 0.2)
            self.wait(12.0)
            if self.CheckFrame():
                print('f1: ' + str(f1) + ' / f2: ' + str(f2))
                f1 += 1
                if f1 > fs:
                    fs += 1
                    f1 = 0
            else:
                print('f1: ' + str(f1) + ' / f2: ' + str(f2))
                # 色違い
                break

    def CheckFrame(self):
        return self.Preview.RequestPixelColorMatch(
            parentCommand=self,
            x=450,
            y=51,
            expectedBGR=(73, 134, 255))
    
    def Reset(self, f1):
        self.press(Button.A | Button.B | Button.PLUS | Button.MINUS)
        self.wait(4.0)
        self.press(Button.A)
        self.wait(2.0)
        self.press(Button.A)
        self.wait(2.0 + f1 / 60.0) # タイトル画面で待機
        self.press(Button.A, 0.05, 3.0)
        self.press(Button.A, 0.05, 1.0)
        self.press(Button.B, 0.05, 2.0) # あらすじスキップ
