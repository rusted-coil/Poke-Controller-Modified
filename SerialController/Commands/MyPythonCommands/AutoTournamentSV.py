#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

class AutoTournamentSV(PythonCommand):
    NAME = 'SV大会'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            for i in range(4):
                self.wait(0.3)
                self.press(Button.A)
            for i in range(2):
                self.wait(0.3)
                self.press(Button.B)
