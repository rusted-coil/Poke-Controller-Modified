#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Auto league
# 自動リーグ周回(画像認識なし)
class Seed_Consume(PythonCommand):
	NAME = 'シード消費'

	def __init__(self):
		super().__init__()

	def change_day(self):
		self.press(Button.A, duration=0.05, wait=0.15)
		self.press(Direction.LEFT, duration=0.05, wait=0.05)
		self.press(Direction.LEFT, duration=0.05, wait=0.05)
		self.press(Direction.LEFT, duration=0.05, wait=0.01)
		self.press(Direction.UP, duration=0.05, wait=0.01)  # increment a day
		# self.press(Direction.RIGHT, wait=0.05)
		# self.press(Direction.RIGHT, wait=0.05)
		# self.press(Direction.RIGHT, wait=0.05)
		self.press(Button.A, duration=0.05, wait=0.05)
		self.press(Button.A, duration=0.05, wait=0.05)
		self.press(Button.A, duration=0.05, wait=0.05)
		self.press(Button.A, duration=0.05, wait=0.15)


	def do(self):
		self.wait(1)
		loops = int(input("input how many loops\n"))
		# loops = MyDialog.input_value(self, "Loops")
		print('Now to start {} loops for consuming seed'.format(loops))
		ndiv = loops // 30
		ndiv_ = loops - ndiv * 30
		print('LOOPS: ', loops)
		for i in range(ndiv):
			for j in range(30):
				print('Now : Frame {}'.format(i * 30 + j + 1))  # 1~31
				self.change_day()
				if not self.checkIfAlive(): return
			self.change_day()
			if not self.checkIfAlive(): return
		for k in range(ndiv_):
			print('Now : Frame {}'.format(ndiv * 30 + k + 1))
			self.change_day()
			if not self.checkIfAlive(): return

		self.finish()
