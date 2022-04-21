#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.CustomPythonCommandBase import CustomPythonCommand
from CustomPreview import Rect

class Mash_A(CustomPythonCommand):
    NAME = '画像処理テスト'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        print('ここにきたよ')
        while True:
            self.Preview.RequestPatternMatching(None, targetRect=Rect(100, 100, 50, 50))
            self.wait(0.5)
            self.Preview.RequestPatternMatching(None, targetRect=Rect(200, 200, 50, 50))
            self.wait(0.5)
