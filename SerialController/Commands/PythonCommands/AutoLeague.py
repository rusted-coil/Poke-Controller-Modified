#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction, Stick
from Commands.PythonCommandBase import PythonCommand


# Auto league
# Automatic League Loop (No Image Recognition)
class AutoLeague(PythonCommand):
    NAME = 'Automatic League Loop'

    def __init__(self):
        super().__init__()

    def do(self):
        self.hold(Direction(Stick.LEFT, 70))

        while True:
            for _ in range(0, 10):
                self.press(Button.A, wait=0.5)

            self.press(Button.B)
