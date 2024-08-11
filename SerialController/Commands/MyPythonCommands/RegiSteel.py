#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat, Stick, Direction
from Commands.PythonCommandBase import PythonCommand

# レジスチル周回用
# レジロック、アイス、スチル色違い厳選のための周回、色違いが出たらそのままハマって停止
# レジ3種同様に可能（要微調整）
#
# 初期条件は以下の通り
# 1. 先頭を、自爆技を1番上の技に持つポケモン（癒しの願い推奨、置き土産はクリアボディのため不可）、確実に逃げるためにけむり玉を持たせる
# 2. その他、捕獲要因やボールを用意
# 3. フィールドの切り替わり初回のみロードが長いことがあるので、ソフト起動してから1回は遺跡入り口を出入り
# 　　（遺跡外でセーブ推奨、その場合は遺跡に入るだけでOK）
# 4. レジ3種それぞれの遺跡、床は光らせずに部屋の左上へ
# 5. マイコンを挿して周回スタート、ソフトリセットした場合は3からやり直し

class RegiSteel(PythonCommand):
    NAME = 'レジスチル色厳選'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            self.SolveSteel()
            self.RegiBattle()
            self.RegiReset()

    # 左上スタートで仕掛けを解いて石像の前に
    def SolveSteel(self):
        self.press(Direction.UP_LEFT, 4.5, 0.05) # 左上に進み続けてぶつかる
        # 仕掛け(レジ系ごとに個別)
        self.press(Direction.DOWN, 0.865, 0.05)
        self.press(Direction.RIGHT, 4.0, 0.05)
        self.press(Direction.DOWN, 0.535, 0.05)
        self.press(Direction.LEFT, 4.0, 0.05)
        self.press(Direction.DOWN, 0.535, 0.05)
        self.press(Direction.RIGHT, 4.0, 0.05)

        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Direction.RIGHT, 2.0, 0.05) # 右→右上→左上で石像まで行く
        self.press(Direction.UP_RIGHT, 4.5, 0.05) # 右→右上→左上で石像まで行く
        self.press(Direction.UP_LEFT, 2.0, 0.05) # 右→右上→左上で石像まで行く

    # 戦闘(共通)
    def RegiBattle(self):
        self.press(Button.B, 0.1, 0.4)
        self.press(Button.B, 0.1, 0.4)
        self.press(Hat.TOP, 1.5, 0.05)
        self.press(Button.A, 0.1, 1.0)
        self.press(Button.A, 0.1, 1.0)
        self.press(Button.A, 0.1, 0.05)
        # タイミング調整
        self.wait(15.5)
        self.press(Hat.TOP, 0.1, 1.0)
        self.press(Button.A, 0.1, 0.8)
        self.press(Button.B, 0.1, 0.4)
        self.press(Button.B, 0.1, 0.4)
        self.press(Hat.TOP, 1.5, 0.05)
        self.press(Button.A, 0.1, 0.8)
        self.press(Button.A, 0.1, 0.8)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)

    # リセット(共通)
    def RegiReset(self):
        self.press(Direction.DOWN, 7.0, 0.05)
        self.press(Direction(Stick.LEFT, 150, showName='UP_LEFT_LEFT'), 2.0, 0.05)
