#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class three_day_after_raid_loop(ImageProcPythonCommand):
	NAME = '3日後レイド周回'

	def __init__(self, name, cam):
		super().__init__(name, cam)

	def do(self):
		print('Start loop')
		s = time.time()
		j = 1
		while True:
			self.wait(1)
			print('{}周目'.format(j), end="")
			for i in range(3):
				i += 1
				print('{}日目'.format(i))
				self.press(Button.A, wait=3.0)
				self.press(Button.A, wait=3.0)  # レイド開始

				self.timeLeap(False)

				self.press(Button.B, wait=1)
				self.press(Button.A)  # レイドをやめる
				while not self.isContainTemplate('Network_Offline.png', 0.8):
					self.wait(0.5)
				self.wait(0.5)
				self.press(Button.A, wait=1.5)
				self.press(Button.A, wait=1.5)  # 2000W
				if not self.checkIfAlive(): return

			self.wait(2.0)
			self.press(Button.A, wait=3)
			self.press(Button.B, wait=1)
			self.press(Button.B, wait=1)
			self.press(Button.B, wait=1)
			while not self.isContainTemplate('Network_Offline.png', 0.8):
				self.wait(0.5)
			self.timeLeap()
			self.wait(0.5)
			self.press(Button.Y)  # YY-COMMUNICATION
			while not self.isContainTemplate('internet.png', 0.8):
				self.wait(0.5)
			self.press(Button.PLUS, wait=10)  # Internet
			while not self.isContainTemplate('dialogue.png', 0.8):
				self.wait(0.5)
			self.press(Button.B, wait=1)
			self.press(Button.B)  # back to wild-area
			while not self.isContainTemplate('Network_Online.png', 0.8):  # online check
				self.wait(0.5)
			self.wait(0.5)
			self.press(Button.A, wait=5)  # open raid
			self.press(Button.A, wait=1)  # open raid
			while not self.isContainTemplate('change_pokemon.png', 0.8):  # timing check
				self.wait(0.5)
			self.press(Direction.UP, wait=0.5)  # 準備完了
			self.press(Button.A, wait=0.5)  # 準備完了
			if self.isContainTemplate('start_battle.png'):
				t = 0
				while t < 160:  # wait for 160 sec
					t += 1
					if self.isContainTemplate('4check.png', 0.85):
						self.press(Button.A)  # start if there are 4 people checked
					elif self.isContainTemplate('fight.png'):  # In case Starting manually
						break
					else:
						self.wait(1.0)
			if not self.isContainTemplate("lonely.png", 0.9):
				for i in range(10):
					self.press(Button.A, wait=0.8)
				while not self.isContainTemplate('catch_or_not.png'):  # To quit game
					if self.isContainTemplate('fight.png') or self.isContainTemplate('cheers.png'):  # press A
						for i in range(8):
							self.press(Button.A, wait=0.5)
				j += 1
			self.press(Button.HOME, wait=2)  # EXIT Game
			self.press(Button.X, wait=0.6)
			self.press(Button.A, wait=2.5)  # closed
			self.press(Button.A, wait=2.0)  # Choose game
			self.press(Button.A)  # User selection
			while not self.isContainTemplate('OP.png', 0.7):  # recognize Opening
				self.wait(1)
			self.press(Button.A, wait=7.0)  # load save-data
			print('{} s 経過'.format(time.time() - s))
# if not self.checkIfAlive(): return
