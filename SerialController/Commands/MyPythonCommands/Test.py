#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

#import AdvanceDays

# Mash a button A
# A連打
class Mash_A(PythonCommand):
    NAME = 'テスト1'

    def __init__(self):
        super().__init__()

    def do(self):
        self.press(Button.X, 0.1, 1.0)
        self.press(Button.B, 0.1, 1.0)
