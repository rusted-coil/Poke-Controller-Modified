#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import PythonCommand

# クチバの縦ルート
class SodateFRLG(PythonCommand):
    TAG = 'FRLG'
    NAME = 'FRLG育て屋レベル上げ'

    def __init__(self):
        super().__init__()

    def do(self):
        while(True):
            self.hold(Direction.UP)
            self.wait(3.5)
            self.holdEnd(Direction.UP)
            self.hold(Direction.DOWN)
            self.wait(3.5)
            self.holdEnd(Direction.DOWN)
