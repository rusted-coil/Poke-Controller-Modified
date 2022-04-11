#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class CustomInputData:
    def SetDate(self, year, month, day):
        self.Date = datetime.date(year, month, day)
    pass

g_CustomInputData = CustomInputData()
