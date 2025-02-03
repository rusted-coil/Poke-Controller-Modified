#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Direction, Button, Stick
from Commands.CustomPythonCommandBase import CustomPythonCommand

# 
class TOGfhouchi(CustomPythonCommand):
    NAME = 'TOGfマグロ丼放置'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        stickInput = Direction(Stick.LEFT, -90, showName='DOWN_LEFT')
        self.hold(Button.B)
        while True:
            self.hold(Direction.DOWN)
            for i in range(4):
                self.press(Button.A)
            self.holdEnd(Direction.DOWN)
            self.hold(Direction.UP_LEFT)
            for i in range(2):
                self.press(Button.A)
            self.holdEnd(Direction.UP_LEFT)
