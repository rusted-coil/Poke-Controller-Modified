#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

# ハピナスレイド周回用
# リセットからスタート
class Reset(PythonCommand):
    NAME = 'レイド周回(SV)'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            for i in range(30):
                self.Loop()

    def Loop(self):
        self.press(Button.HOME, 0.05, 1.1)
        self.press(Button.X, 0.05, 0.3)
        self.press(Button.A, 0.05, 2.0)
        for i in range(10):
            self.press(Button.A, 0.05, 0.3)
        self.wait(20.0)
        self.press(Button.A, 0.05, 21.0)
        self.press(Button.A, 0.05, 2.0)
        self.press(Button.A, 0.05, 20.0) # 参加待ち
        self.press(Button.A, 0.05, 0.3)
        self.press(Button.A, 0.05, 2.0)
        self.press(Button.A, 0.05, 41.0) # レイド開始演出
        self.press(Button.A, 0.05, 1.0)
        self.press(Button.A, 0.05, 1.0)
        self.press(Button.A, 0.05, 11.0) # 攻撃中

    # デバッグ機能 整数秒待ってログでカウント
    def PrintWait(self, seconds):
        for i in range(seconds):
            self.wait(1.0)
            print('wait', i + 1, 'seconds')
