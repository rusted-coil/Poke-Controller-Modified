#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Hat
from Commands.PythonCommandBase import PythonCommand

from Commands.CustomInput import g_CustomInput

from .Util.DayChanger import DayChanger

# 1日進める処理実装
class AdvanceDayRaidHole:
    @staticmethod
    def AdvanceDay(cmd):
        # レイドを始める
        cmd.press(Button.A, 0.05, 0.5)
        cmd.press(Button.A, 0.05, 3.0)

        # HOME画面に戻り設定をクリック
        cmd.press(Button.HOME, 0.05, 1.0)
        cmd.press(Hat.BTM, 0.05, 0.05)
        for i in range(5): # HOMEメニューの項目が増えたら変更する
            cmd.press(Hat.RIGHT, 0.05, 0.05)

        # 設定画面で本体の設定へ
        cmd.press(Button.A, 0.05, 0.05)
        cmd.press(Hat.BTM, 2.2, 0.05)
        cmd.press(Button.A, 0.05, 0.05)

        # 本体の設定で時刻変更へ
        for i in range(3):
            cmd.press(Hat.BTM, 0.05, 0.05)
        cmd.press(Hat.BTM, 0.3, 0.05)
        for i in range(2):
            cmd.press(Hat.BTM, 0.05, 0.05)
        cmd.press(Button.A, 0.05, 0.3)
        cmd.press(Hat.BTM, 0.05, 0.05)
        cmd.press(Hat.BTM, 0.05, 0.05)

        # 設定画面で+1日
        dayChanger = DayChanger(g_CustomInput.Model.Date)
        dayChanger.AdvanceDay(cmd)
        g_CustomInput.SetDate(dayChanger.CurrentDate)

        # ゲームに戻る
        cmd.press(Button.HOME, 0.05, 1.0)
        cmd.press(Button.A, 0.05, 0.5)

        # レイドをキャンセルしてワット受け取り
        cmd.press(Button.B, 0.05, 1.1)
        cmd.press(Button.A, 0.05, 4.0)
        cmd.press(Button.A, 0.05, 0.5)
        cmd.press(Button.A, 0.05, 0.5)
        cmd.press(Button.A, 0.05, 0.1)
        cmd.press(Button.A, 0.05, 0.1)
        cmd.press(Button.A, 0.05, 0.1)

class AdvanceDayRaidHoleOne(PythonCommand):
    NAME = '1日進める(RaidHole)'

    def __init__(self):
        super().__init__()

    def do(self):
        AdvanceDayRaidHole.AdvanceDay(self)

class AdvanceDayRaidHoleThree(PythonCommand):
    NAME = '3日進める(RaidHole)'

    def __init__(self):
        super().__init__()

    def do(self):
        for i in range(3):
            AdvanceDayRaidHole.AdvanceDay(self)

class AdvanceDayRaidHoleFour(PythonCommand):
    NAME = '4日進める(RaidHole)'

    def __init__(self):
        super().__init__()

    def do(self):
        for i in range(4):
            AdvanceDayRaidHole.AdvanceDay(self)
