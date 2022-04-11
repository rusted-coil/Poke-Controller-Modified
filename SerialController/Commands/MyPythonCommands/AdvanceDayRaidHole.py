#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

from Commands.CustomInputData import g_CustomInputData

from .Util.DayChanger import DayChanger

class AdvanceDayRaidHole(PythonCommand):
    NAME = '1日進める(RaidHole)'

    def __init__(self):
        super().__init__()

    def do(self):
        dayChanger = DayChanger(g_CustomInputData.Date)
        dayChanger.CursorLeftToRight(self)
        dayChanger.AdvanceDay(self)
        g_CustomInputData.SetDate(dayChanger.CurrentDate.year, dayChanger.CurrentDate.month, dayChanger.CurrentDate.day, True)
