#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

# SVでタマゴ受け取り自動化
# 現在はタマゴパワーLv2をつけた後に30分間5分おきにタマゴを受け取るだけ
class ReceiveEggSV(PythonCommand):
    NAME = 'タマゴ受け取りSV'

    def __init__(self):
        super().__init__()

    def do(self):
        for _ in range(10):            
            self.wait(180.0)
            # 20秒ぐらいA連打
            for _ in range(170):
                self.press(Button.A, 0.05, 0.05)
            self.wait(0.5)
            # メッセージウィンドウを閉じるためB連打
            for _ in range(15):
                self.press(Button.B, 0.05, 0.5)
