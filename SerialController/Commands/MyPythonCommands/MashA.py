#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

class Mash_A(PythonCommand):
    NAME = 'A連打'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            self.wait(0.5)
            self.press(Button.A)
