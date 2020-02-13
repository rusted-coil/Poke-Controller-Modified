#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class Auto_raid(ImageProcPythonCommand):
	NAME = 'レイド周回'

	def __init__(self, name, cam):
		super().__init__(name, cam)

	def do(self):
		loop = 1
		while True:
			print(f"loop : {loop}")
			self.wait(1.0)
			print("Go Solo Raid battle.")
			while not self.isContainTemplate("raid_menu.png", 0.9):
				self.press(Button.A, wait=1.5)
			self.press(Direction.DOWN, duration=0.07, wait=1.0)
			self.press(Button.A, wait=1.5)
			self.press(Button.A, wait=1.5)
			print("Raid battle start.")
			while not self.isContainTemplate("catch_or_not.png", 0.7):
				if self.isContainTemplate('fight.png') or self.isContainTemplate("cheers.png", 0.8):  # press A
					for i in range(8):
						self.press(Button.A, wait=0.5)
				if self.isContainTemplate("Network_Offline.png", 0.8):
					break
			print("Raid Battle Finish")
			if self.isContainTemplate("catch_or_not.png", 0.7):
				self.press(Direction.DOWN, duration=0.07, wait=1.0)
			while not self.isContainTemplate("Network_Offline.png", 0.8):
				self.press(Button.A, wait=1.0)
			loop += 1
			# self.press(Direction.UP, duration=0.07, wait=1.0)