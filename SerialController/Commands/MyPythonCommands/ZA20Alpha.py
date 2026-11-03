#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat, Direction
from Commands.PythonCommandBase import PythonCommand

# ZA20番ワイルドゾーンのオヤブン色違い自動厳選
# ベンチを調べてスタート
class ZA20Alpha(PythonCommand):
    NAME = 'ZA20番オヤブン'

    def __init__(self):
        super().__init__()

    def do(self):
        self.hold(Direction.DOWN_RIGHT)
        self.hold(Direction.R_UP_LEFT)
        while(True):
            self.wait(0.1)
            self.press(Button.A)
