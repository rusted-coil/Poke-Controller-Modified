#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from Commands.Keys import Button
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect

class DiggingStarter(CustomPythonCommand):
    NAME = 'スクリーンショット保存'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        self.Preview.RequestScreenshot(
            parentCommand=self,
            savePath=datetime.datetime.now().strftime('../Screenshot/%Y%m%d_%H%M%S.png'),
            isUseGrayScale=False)
