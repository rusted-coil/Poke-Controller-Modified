#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading
import tkinter as tk
import cv2

from PIL import Image, ImageTk, ImageDraw

class CustomPreview(tk.Frame):
    @staticmethod
    def CvImageToTk(image):
        split = cv2.split(image)
        if len(split) == 3:
            blue,green,red = split
            image = cv2.merge((red,green,blue))
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image=image)        

    def __init__(self, camera, master=None):
        super().__init__(master, width=640, height=360)

        self.Camera = camera

        self.IsRunning = False

        # 描画用のDisplayとちらつき防止のDisplayBufferを作成
        self.DisplayBuffer = tk.Label(self)
        self.Display = tk.Label(self)
        self.DisplayBuffer.grid(row=0, column=0, sticky=tk.NSEW)
        self.Display.grid(row=0, column=0, sticky=tk.NSEW)

        # DisableのPhotoImageを作成し、リソースが開放されないようにselfで持つ
        self.DisabledImage = self.CvImageToTk(cv2.imread("../Images/disabled.png", cv2.IMREAD_GRAYSCALE))

        self.DisplayBuffer['image'] = self.DisabledImage
        self.Display['image'] = self.DisabledImage

    # プレビューが有効かどうかをセットします。
    def UpdateRunning(self, isRunning):
        if isRunning != self.IsRunning:
            self.IsRunning = isRunning
            if self.IsRunning:
                self.StartPreview()

    # プレビューを開始します。
    def StartPreview(self):
        self.CaptureThread = threading.Thread(target = self.PreviewLoop)
        self.CaptureThread.daemon = True
        self.CaptureThread.start()

    # プレビューのタスクです。
    def PreviewLoop(self):
        lastFrameTk = None
        while self.IsRunning:
            frame = self.Camera.readFrame()

            # frameに対する処理
            frame = cv2.resize(frame, (640, 360))

            frameTk = self.CvImageToTk(frame)
            self.DisplayBufferImage = lastFrameTk # リソースが開放されないようにselfで持つ
            self.DisplayBuffer['image'] = self.DisplayBufferImage
            self.DisplayImage = frameTk
            self.Display['image'] = self.DisplayImage
            lastFrameTk = frameTk

        # リソースを解放
        self.DisplayBufferImage = None
        self.DisplayImage = None

