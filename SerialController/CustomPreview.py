#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading
import time
import tkinter as tk
from tracemalloc import start
import cv2
from time import sleep

from PIL import Image, ImageTk, ImageDraw

from ImageProcessRequest import ScreenshotRequest, TemplateExistRequest, TemplatePositionRequest

class CancelRequest():
    pass

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
        self.Request = None
        self.RequestBuffer = None

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
            if not self.RequestBuffer is None:
                self.Request = self.RequestBuffer if not type(self.RequestBuffer) is CancelRequest else None
                self.RequestBuffer = None

            frame = self.Camera.readFrame()

            # frameに対する処理
            frame = cv2.resize(frame, (640, 360))
            if not self.Request is None:
                frame = self.Request.Process(frame)
                if self.Request.IsFinished:
                    self.Request = None

            frameTk = self.CvImageToTk(frame)
            self.DisplayBufferImage = lastFrameTk # リソースが開放されないようにselfで持つ
            self.DisplayBuffer['image'] = self.DisplayBufferImage
            self.DisplayImage = frameTk
            self.Display['image'] = self.DisplayImage
            lastFrameTk = frameTk

        # リソースを解放
        self.DisplayBufferImage = None
        self.DisplayImage = None

    # リクエストを処理します。
    def RequestImpl(self, parentCommand, request, timeout):
        startTime = time.perf_counter()
        self.RequestBuffer = request
        # 結果待ちループ
        while not request.IsFinished:
            if not parentCommand.alive:
                self.RequestBuffer = CancelRequest()
                return False
            # 時間切れ
            elif time.perf_counter() - startTime >= timeout:
                self.RequestBuffer = CancelRequest()
                return False
            sleep(0.1)
        return request.Result

    # スクリーンショットを保存するリクエストを作成します。
    def RequestScreenshot(self, parentCommand, savePath, targetRect=None, isUseGrayScale=True, timeout=1.0):
        return self.RequestImpl(parentCommand, ScreenshotRequest(savePath, targetRect, isUseGrayScale), timeout)

    # テンプレートマッチングを行い、テンプレートが存在するかどうかを返すリクエストを実行します。
    def RequestTemplateExist(self, parentCommand, templatePath, targetRect=None, isUseGrayScale=True, threshold=0.7, timeout=1.0):
        return self.RequestImpl(parentCommand, TemplateExistRequest(templatePath, targetRect, isUseGrayScale, threshold), timeout)

    # テンプレートマッチングを行い、最も類似度の高い中心座標を返すリクエストを実行します。
    def RequestTemplatePosition(self, parentCommand, templatePath, targetRect=None, isUseGrayScale=True, threshold=0.7, timeout=1.0):
        return self.RequestImpl(parentCommand, TemplatePositionRequest(templatePath, targetRect, isUseGrayScale, threshold), timeout)
