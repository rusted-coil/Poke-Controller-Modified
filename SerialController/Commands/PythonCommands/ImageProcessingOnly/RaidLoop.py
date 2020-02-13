#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class raid_loop(ImageProcPythonCommand):
	NAME = 'レイド配布周回'

	def __init__(self, name, cam):
		super().__init__(name, cam)

	def do(self):
		print('Start loop')
		s = time.time()
		j = 1
		while True:
			self.wait(1)
			print('{}周目'.format(j), end="")
			self.loopwhileImage('Network_Offline.png', 10)
			self.press(Button.Y)  # YY-COMMUNICATION
			self.loopwhileImage('internet.png', 10)
			self.press(Button.PLUS, wait=10)  # Internet
			self.loopwhileImage('dialogue.png', 10)
			self.press(Button.B, wait=1)
			self.press(Button.B)  # back to wild-area
			self.loopwhileImage('Network_Online.png', 10)  # online check
			self.wait(0.5)
			self.press(Button.A, wait=5)  # open raid
			self.press(Button.A, wait=1)  # open raid
			self.loopwhileImage('change_pokemon.png', 10)  # timing check
			self.press(Direction.UP, wait=0.5)  # 準備完了
			self.press(Button.A, wait=0.5)  # 準備完了
			if self.isContainTemplate('start_battle.png'):
				t = 0
				while t < 160:  # wait for 180 sec
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
			self.press(Button.A, wait=1.0)  # Choose game
			self.press(Button.A)  # User selection
			self.loopwhileImage('OP.png', 30)  # recognize Opening
			self.press(Button.A, wait=7.0)  # load save-data
			print('{} s 経過'.format(time.time() - s))
# if not self.checkIfAlive(): return
