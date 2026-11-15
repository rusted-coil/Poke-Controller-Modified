#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Hat
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

class LatiosZA(CustomPythonCommand):
    TAG = 'ZA'
    NAME = 'ZAラティオス色厳選'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        LatiosZA.DoReset(self)
        # タイトル画面～ゲーム開始まで待機
        for i in range(5):
            self.press(Button.A, 0.05, 0.35)
        self.wait(7.5)
        # ワープ床
        for i in range(5):
            self.press(Button.A, 0.05, 0.35)

    @staticmethod
    def DoReset(cmd):
        cmd.press(Button.HOME, 0.05, 1.1)
        cmd.press(Button.X, 0.05, 0.3)
        cmd.press(Button.A, 0.05, 2.0)
        for i in range(10):
            cmd.press(Button.A, 0.05, 0.3)
        # ソフト選択～タイトルまで待機
        cmd.wait(16.5)
