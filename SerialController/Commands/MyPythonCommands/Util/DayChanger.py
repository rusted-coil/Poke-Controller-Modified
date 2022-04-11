#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from Commands.Keys import Button, Direction

class DayChanger:
    def __init__(self, date):
        self.CurrentDate = date
        self.IsFromRight = False # 初期状態では日時変更メニューのカーソルは左から始まる

    # 日時変更メニューのカーソルを左端から右端に設定します。
    def CursorLeftToRight(self, cmd):
        cmd.press(Button.A, 0.05, 0.3)
        cmd.press(Direction.RIGHT, 2.0, 0.04)
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
            cmd.press(Direction.LEFT, 0.05, 0.04)
            cmd.press(Direction.LEFT, 0.05, 0.04)
            cmd.press(Direction.LEFT, 0.05, 0.04)
        else:
            cmd.press(Direction.RIGHT, 0.05, 0.04)
            cmd.press(Direction.RIGHT, 0.05, 0.04)

        for i in range(updateCount): # Day, Month, Yearを1加算
            cmd.press(Direction.UP, 0.05, 0.04)
            if i != updateCount - 1:
                cmd.press(Direction.LEFT, 0.05, 0.04)
        
        for i in range(updateCount + 3): # 完了
            cmd.press(Button.A, 0.05, 0.04)

        self.CurrentDate = tomorrow
        self.IsFromRight = True        
