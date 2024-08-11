#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

# シンボル前でレポートした状態で話しかけられる所に立ってスタート
class ShinySV(CustomPythonCommand):
    NAME = 'BDSP色違い厳選'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        while True:
            for i in range(10): # エンカウントイベント用ボタン連打
                self.press(Button.A, 0.05, 0.2)                
            self.wait(19.5) # エンカウントイベント～戦闘開始までの待機時間　色違い演出(2秒)が入るとギリギリ足りないラインを狙う

            if self.CheckBattleIcon(): # この時間でたたかうマークがあったら色違いじゃない
                self.Reset()
            else:
                # 色違い
                break

    def CheckBattleIcon(self):
        return self.Preview.RequestTemplateExist(
            parentCommand=self,
            templatePath="../Images/BattleIconBDSP.png",
            targetRect=Rect(575, 200, 60, 50),
            timeout=0.0)
    
    def Reset(self):
        self.press(Hat.TOP, 0.1, 0.3)
        self.press(Button.A, 0.1, 5.0)
        self.press(Button.A, 0.1, 1.0)
        self.press(Direction.DOWN, 4.0, 0.5)
        self.press(Direction.UP, 4.0, 0.5)
