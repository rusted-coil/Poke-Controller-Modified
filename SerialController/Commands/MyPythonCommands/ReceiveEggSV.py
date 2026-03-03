#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat, Direction
from Commands.PythonCommandBase import PythonCommand

# SVでタマゴ受け取り自動化
# カラフシティ西にそらをとぶした時点からスタート
class ReceiveEggSV(PythonCommand):
    NAME = 'タマゴ受け取りSV'

    def __init__(self):
        super().__init__()

    def do(self):
        for setIndex in range(9): # 回数は適当に設定する
            print(str(setIndex + 1) + " セット目開始")
            # カラフシティ西で食事
            self.press(Direction.LEFT, duration=3.1)
            self.press(Direction.UP, duration=4.9)
            self.press(Direction.LEFT, duration=2.8)
            self.press(Direction.UP, duration=2.0)
            self.press(Direction.RIGHT, duration=0.1)
            self.press(Direction.UP, duration=0.4)
            self.press(Direction.LEFT, duration=0.1)
            self.press(Direction.UP, duration=0.4, wait=3.0)
            self.press(Button.A, wait=2.0)
            self.press(Hat.BTM, wait=1.0)
            self.press(Button.A, wait=1.5)
            self.press(Button.A, wait=2.0)
            self.press(Button.A, wait=23.0)
            self.press(Button.A, wait=1.0)
            self.press(Button.A, wait=2.0)
            # マップを開いてそらをとぶ
            self.press(Button.Y, wait=2.2)
            self.press(Direction.DOWN, wait=0.5)
            self.press(Button.A)
            self.press(Button.A, wait=1.0)
            self.press(Button.A, wait=5.0)
            # キャンプを開く
            self.press(Direction.DOWN, duration=4.0)
            self.press(Button.X, wait=0.5)
            self.press(Hat.TOP, duration=1.5)
            self.press(Hat.BTM, wait=0.5)
            self.press(Hat.BTM, wait=0.5)
            self.press(Button.A, wait=9.0)
            self.press(Direction.LEFT, duration=0.5)
            self.press(Direction.DOWN, duration=0.5)
            self.press(Direction.RIGHT, duration=0.4)
            for loopIndex in range(10):            
                self.wait(180.0)
                # 20秒ぐらいA連打
                for _ in range(170):
                    self.press(Button.A, 0.05, 0.05)
                self.wait(0.5)
                # メッセージウィンドウを閉じるためB連打
                for _ in range(15):
                    self.press(Button.B, 0.05, 0.5)
                print(str(loopIndex + 1) + " / 10 完了")
            self.wait(1.0)
            # キャンプを閉じる
            self.press(Button.Y)
            self.press(Button.B, wait=0.2)
            self.press(Button.Y, wait=0.8)
            self.press(Button.A, wait=3.0)
            # マップを開いてそらをとぶ
            self.press(Button.Y, wait=2.2)
            self.press(Direction.RIGHT, duration=0.08, wait=0.5)
            self.press(Button.A)
            self.press(Button.A, wait=1.0)
            self.press(Button.A, wait=5.0)
