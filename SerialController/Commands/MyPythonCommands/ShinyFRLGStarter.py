#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

# シンボル前でレポートした状態で話しかけられる所に立ってスタート
class ShinySV(CustomPythonCommand):
    NAME = 'FRLG御三家色厳選'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):        
        self.Reset()
        while True:
            for i in range(20): # ポケモンを貰う
                self.press(Button.A, 0.05, 0.2)
            for i in range(20): # ニックネームをつけない
                self.press(Button.B, 0.05, 0.2)
            self.wait(3.0)
            self.press(Button.X, 0.05, 0.5)
            self.press(Button.A, 0.05, 0.5)
            self.press(Button.A, 0.05, 0.5)
            self.press(Button.A, 0.05, 0.5)
            self.press(Button.A, 0.05, 0.5)
            self.wait(1.0)
            if self.CheckFrame():
                self.Reset()
            else:
                # 色違い
                break

    def CheckFrame(self):
        return self.Preview.RequestPixelColorMatch(
            parentCommand=self,
            x=124,
            y=45,
            expectedBGR=(240, 173, 207))
    
    def Reset(self):
        self.press(Button.A | Button.B | Button.PLUS | Button.MINUS)
        for i in range(20):
            self.press(Button.A, 0.05, 0.2)
        self.wait(1.8 + random.randint(0, 59) / 60)
        self.press(Button.A, 0.05, 1.0)
        self.press(Button.B, 0.05, 2.0) # あらすじスキップ
