#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

from . import CommandBase
from .Keys import Button, Hat, KeyPress

# 複合ボタンを扱うコマンドクラス
class MultiCommand(CommandBase.Command):
    def __init__(self):
        super().__init__()

    def start(self, ser, postProcess=None):
        self.isRunning = True
        self.key = KeyPress(ser)

    def end(self, ser):
        pass

    def wait(self, wait):
        sleep(wait)

    def press(self, buttonList):
        self.key.input(buttonList)
        self.wait(0.1)
        self.key.inputEnd(buttonList)
        self.isRunning = False
        self.key = None

# バックアップデータをロード（SwSh）
class LoadBackupSwSh(MultiCommand):
    def __init__(self):
        super().__init__()

    def start(self, ser):
        super().start(ser)
        self.press([Hat.TOP, Button.B, Button.X])
