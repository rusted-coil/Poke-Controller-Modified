#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand
from Commands.PythonCommandBase import ImageProcPythonCommand


class LineSample(ImageProcPythonCommand):
    NAME = 'LINE notification sample'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        self.LINE_text("This is a notification to the default token")
        self.LINE_text("This is a text notification to another token", token='token_2')
        self.LINE_image("This is a text + image notification to another token", token='token_2')
