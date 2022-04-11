#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

from Commands.CustomInputData import g_CustomInputData

class AdvanceDayRaidHole(PythonCommand):
    NAME = '1日進める(RaidHole)'

    def __init__(self):
        super().__init__()

    def do(self):
        print(g_CustomInputData.test)
