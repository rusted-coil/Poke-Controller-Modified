#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class CustomInputData:
    SetDateCallback = None

    # Dateに日付をセットします。
    def SetDate(self, year, month, day, isCallback):
        self.Date = datetime.date(year, month, day)
        if isCallback and self.SetDateCallback != None:
            self.SetDateCallback()

g_CustomInputData = CustomInputData()
