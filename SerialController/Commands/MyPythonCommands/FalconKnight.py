#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Hat, Direction
from Commands.PythonCommandBase import PythonCommand

class Mash_A(PythonCommand):
    NAME = 'ファルコン法無限消費'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            self.hold(Direction.DOWN_RIGHT)
            self.wait(0.5)
            self.holdEnd(Direction.DOWN_RIGHT)
            self.hold(Direction.UP_LEFT)
            self.wait(0.5)
            self.holdEnd(Direction.UP_LEFT)
#            self.press(Hat.RIGHT, 0.06, 0.06)
#            self.press(Hat.BTM, 0.06, 0.06)
#            self.press(Hat.TOP, 0.06, 0.06)
#            self.press(Hat.LEFT, 0.06, 0.06)
