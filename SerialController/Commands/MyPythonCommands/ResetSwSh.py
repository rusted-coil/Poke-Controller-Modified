#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

class Reset(PythonCommand):
    NAME = 'リセット(SwSh)'

    def __init__(self):
        super().__init__()

    def do(self):
        self.press(Button.HOME, 0.05, 1.1)
        self.press(Button.X, 0.05, 0.3)
        self.press(Button.A, 0.05, 2.0)
        for i in range(10):
            self.press(Button.A, 0.05, 0.3)
        self.wait(16.0)
        self.press(Button.A, 0.05, 9.0)
        self.press(Button.A, 0.05, 0.05)

class CampReset(PythonCommand):
    NAME = 'キャンプリセット(SwSh)'

    def __init__(self):
        super().__init__()

    def do(self):
        self.press(Button.HOME, 0.05, 1.1)
        self.press(Button.X, 0.05, 0.3)
        self.press(Button.A, 0.05, 2.0)
        for i in range(10):
            self.press(Button.A, 0.05, 0.3)
        self.wait(14.0)
        self.press([Button.X, Button.B, Hat.TOP], 0.05, 3.5)
        self.press(Button.A, 0.05, 1.0)
        self.press(Button.A, 0.05, 9.0)
        self.press(Button.A, 0.05, 0.05)
