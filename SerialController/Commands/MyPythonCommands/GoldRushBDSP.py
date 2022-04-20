#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction, Hat
from Commands.PythonCommandBase import PythonCommand

# BDSPにおいてマダムとジェントルマンを狩って金を稼ぎます。
# ・マダムの上1右3のマスから徒歩で開始
# ・便利ボタンにはバトルサーチャーのみ登録
# ・手持ちはLv100ルージュラ、技はこなゆきorねんりき（ポイントアップでPP40）
# ・他の手持ちは無しorLv100のみ（レベルアップのメッセージ送りをなくすため）
class GoldRush_BDSP(PythonCommand):
    NAME = '金稼ぎ(BDSP)'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            # バトルサーチャーの充電
            for i in range(5):
                self.press(Direction.LEFT, 1.4, 0.05)
                self.press(Direction.RIGHT, 1.4, 0.05)

            # バトルサーチャーを使う
            self.press(Button.PLUS, 0.05, 2.0)
            for i in range(3):
                self.press(Button.A, 0.05, 0.5)

            # マダム
            for i in range(3):
                self.press(Hat.LEFT, 0.2, 0.2)
            self.press(Hat.BTM, 0.05, 0.05)
            for i in range(70):
                self.press(Button.A, 0.05, 0.5)
            self.press(Button.B, 0.05, 0.05)
            self.press(Button.B, 0.05, 0.05)

            # ジェントルマン
            for i in range(3):
                self.press(Hat.LEFT, 0.2, 0.2)
            self.press(Hat.BTM, 0.05, 0.05)
            for i in range(70):
                self.press(Button.A, 0.05, 0.5)
            self.press(Button.B, 0.05, 0.05)
            self.press(Button.B, 0.05, 0.05)

            # 戻る
            self.press(Direction.RIGHT, 1.0, 0.05)
