#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from Commands.Keys import Button
from Commands.PythonCommandBase import ImageProcPythonCommand, PythonCommand

class Reset(ImageProcPythonCommand):
    NAME = 'テスト'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("Source bgr:")
        print(id(self.camera.image_bgr))
        print("Copied bgr:")
        self.src = self.camera.image_bgr.copy()
        print(id(self.src))
