#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

# Mash a button A
# A連打
class Mash_A(PythonCommand):
    NAME = 'テスト'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            self.wait(1.0)
            self.press(Button.X)
            self.wait(1.0)
            self.press(Button.B)
