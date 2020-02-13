#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick


# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class raid_search(ImageProcPythonCommand):  # ワット回収済みレイドの前から
    NAME = 'レイド探し'

    def __init__(self, cam):
        def __init__(self, name, cam):
            super().__init__(name, cam)

        def do(self):
            searchfor = 'shandera.png'  # Silhouette
            print('Start searching {}'.format(searchfor))
            s = time.time()
            j = 1
            while self.checkIfAlive():
                self.wait(1)
                print('{}周目'.format(j), end="")
                for i in range(3):
                    i += 1
                    print('{}日目'.format(i))
                    self.press(Button.A, wait=2.0)
                    # self.loopwhileImage('minnade.png', 100)
                    self.press(Button.A, wait=3)  # レイド開始

                    self.press(Button.HOME, wait=1)
                    self.press(Direction.DOWN)
                    self.press(Direction.RIGHT)
                    self.press(Direction.RIGHT)
                    self.press(Direction.RIGHT)
                    self.press(Direction.RIGHT)
                    self.press(Button.A, wait=1.5)  # 設定選択
                    # self.press(Direction.DOWN, duration=2, wait=0.5)
                    self.hold(Direction.DOWN)
                    self.loopwhileImage('hontai.png', 100)
                    self.holdEnd(Direction.DOWN)

                    self.press(Button.A, wait=0.3)  # 設定 > 本体
                    self.press(Direction.DOWN)
                    self.press(Direction.DOWN)
                    self.press(Direction.DOWN)
                    self.press(Direction.DOWN, wait=0.3)
                    self.press(Button.A, wait=0.3)  # 日付と時刻 選択
                    # self.press(Button.A, wait=0.4)

                    self.press(Direction.DOWN, wait=0.2)
                    self.press(Direction.DOWN, wait=0.2)
                    self.press(Button.A, wait=0.2)
                    self.press(Direction.UP, wait=0.2)
                    self.press(Direction.RIGHT, wait=0.1)
                    self.press(Direction.RIGHT, wait=0.1)
                    self.press(Direction.RIGHT, wait=0.1)
                    self.press(Direction.RIGHT, wait=0.1)
                    self.press(Direction.RIGHT, wait=0.1)
                    self.press(Button.A, wait=0.5)
                    self.press(Button.HOME, wait=1)  # ゲームに戻る
                    self.press(Button.HOME, wait=2)

                    self.press(Button.B, wait=1)
                    self.press(Button.A)  # レイドをやめる
                    self.loopwhileImage('Network_Offline.png', 100)
                    self.wait(0.5)
                    self.press(Button.A, wait=1.5)
                    self.press(Button.A, wait=1.5)  # 2000W
                    if not self.checkIfAlive(): return

                self.press(Button.A, wait=3)
                if self.isContainTemplate(searchfor, 0.8):
                    print('found in {}.'.format(s - time.time()))
                    self.finish()
                else:
                    print('Not found.')
                    self.press(Button.HOME, wait=0.6)  # EXIT Game
                    self.press(Button.X, wait=0.6)
                    self.press(Button.A, wait=2.5)  # closed
                    j += 1
                    if j % 10 == 0:
                        self.press(Direction.DOWN)
                        self.press(Direction.RIGHT)
                        self.press(Direction.RIGHT)
                        self.press(Direction.RIGHT)
                        self.press(Direction.RIGHT)
                        self.press(Button.A, wait=1.5)  # 設定選択
                        # self.press(Direction.DOWN, duration=2, wait=0.5)
                        self.hold(Direction.DOWN)
                        t = 0
                        self.loopwhileImage('hontai.png', 100)
                        self.holdEnd(Direction.DOWN)

                        self.press(Button.A, wait=0.3)  # 設定 > 本体
                        self.press(Direction.DOWN)
                        self.press(Direction.DOWN)
                        self.press(Direction.DOWN)
                        self.press(Direction.DOWN, wait=0.3)
                        self.press(Button.A, wait=0.2)  # 日付と時刻 選択
                        # self.press(Button.A, wait=0.4)

                        self.press(Direction.DOWN, wait=0.2)
                        self.press(Direction.DOWN, wait=0.2)
                        self.press(Button.A, wait=0.2)
                        self.press(Direction.DOWN, duration=6.5, wait=0.2)
                        self.press(Direction.RIGHT, wait=0.1)
                        self.press(Direction.RIGHT, wait=0.1)
                        self.press(Direction.RIGHT, wait=0.1)
                        self.press(Direction.RIGHT, wait=0.1)
                        self.press(Direction.RIGHT, wait=0.1)
                        self.press(Button.A, wait=0.5)
                        self.press(Button.HOME, wait=1)  # ゲームに戻る
                    self.press(Button.A, wait=2.0)  # Choose game
                    # self.press(Button.A, wait=18.0)  # User selection
                    self.press(Button.A)  # User selection
                    self.loopwhileImage('OP.png', 500)
                    self.press(Button.A, wait=7.0)  # load save-data
