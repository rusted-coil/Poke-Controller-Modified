#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from Commands.Keys import Button, Hat

class DayChanger:
    def __init__(self, date):
        self.CurrentDate = date
        self.IsFromRight = False # 初期状態では日時変更メニューのカーソルは左から始まる

    # 日時変更メニューのカーソルを左端から右端に設定します。
    def CursorLeftToRight(self, cmd):
        cmd.press(Button.A, 0.05, 0.3)
        cmd.press(Hat.RIGHT, 2.0, 0.05)
        cmd.press(Button.A, 0.05, 0.3)
        self.IsFromRight = True

    # 現在の日付から設定画面で1日進めます。
    def AdvanceDay(self, cmd):
        tomorrow = self.CurrentDate + timedelta(days=1)
        updateCount = 1
        if tomorrow.year - self.CurrentDate.year == 1:
            updateCount = 3
        elif tomorrow.month - self.CurrentDate.month == 1:
            updateCount = 2

        cmd.press(Button.A, 0.05, 0.3) # 日時変更画面へ

        if self.IsFromRight:
            cmd.press(Hat.LEFT, 0.05, 0.05)
            cmd.press(Hat.LEFT, 0.05, 0.05)
            cmd.press(Hat.LEFT, 0.05, 0.05)
        else:
            cmd.press(Hat.RIGHT, 0.05, 0.05)
            cmd.press(Hat.RIGHT, 0.05, 0.05)

        for i in range(updateCount): # Day, Month, Yearを1加算
            cmd.press(Hat.TOP, 0.05, 0.05)
            if i != updateCount - 1:
                cmd.press(Hat.LEFT, 0.05, 0.05)
        
        for i in range(updateCount + 3): # 完了
            cmd.press(Button.A, 0.05, 0.05)

        self.CurrentDate = tomorrow
        self.IsFromRight = True        
