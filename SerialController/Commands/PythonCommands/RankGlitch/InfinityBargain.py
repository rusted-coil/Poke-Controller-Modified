#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# using RankBattle glitch
# Auto cafe battles
# 無限カフェ(ランクマッチ使用)
class InfinityBargain(ImageProcPythonCommand):
	NAME = '無限掘り出し物'

	def __init__(self, cam):
		super().__init__(cam)

	def do(self):
		while True:
			while not self.isContainTemplate('bargain_0.png'):
				self.press(Button.A, wait=1.0)
			while not self.isContainTemplate('Network_Offline.png', 0.85):
				self.press(Button.B, wait=1.0)

			self.timeLeap()