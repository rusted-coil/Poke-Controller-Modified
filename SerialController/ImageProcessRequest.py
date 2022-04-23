#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

class Rect:
    def __init__(self, left, top, width, height):
        self.Left = left
        self.Top = top
        self.Width = width
        self.Height = height

    def SliceFrame(self, frame):
        return frame[self.Top : self.Top+self.Height, self.Left : self.Left + self.Width]

    def TopLeft(self):
        return (self.Left, self.Top)

    def BottomRight(self):
        return (self.Left + self.Width, self.Top + self.Height)

# 画像処理のリクエストを表す基底クラスです。
class RequestBase:
    def __init__(self, targetRect):
        self.TargetRect = targetRect
        self.IsFinished = False

    def Process(self, frame):
        if not self.TargetRect is None:
            cv2.rectangle(frame, self.TargetRect.TopLeft(), self.TargetRect.BottomRight(), (0, 0, 255), 1)
        return frame

# スクリーンショットを保存するリクエスト
class ScreenshotRequest(RequestBase):
    def __init__(self, savePath, targetRect = None, isUseGrayScale=True):
        super().__init__(targetRect)
        self.Path = savePath
        self.IsUseGrayScale = isUseGrayScale

    def Process(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if self.IsUseGrayScale else src
        # 画像として保存する
        cv2.imwrite(self.Path, src)
        self.IsFinished = True
        self.Result = True        
        return frame

# テンプレートマッチングを行うリクエストの基底
class TemplateMatchingRequestBase(RequestBase):
    def __init__(self, templatePath, targetRect=None, isUseGrayScale=True):
        super().__init__(targetRect)
        self.Template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE if isUseGrayScale else cv2.IMREAD_COLOR)
        self.IsUseGrayScale = isUseGrayScale

    def Matching(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if self.IsUseGrayScale else src
        return cv2.matchTemplate(src, self.Template, cv2.TM_CCOEFF_NORMED)

# テンプレートマッチングを行い、存在をチェックするリクエスト
class TemplateExistRequest(TemplateMatchingRequestBase):
    def __init__(self, templatePath, targetRect=None, isUseGrayScale=True, threshold=0.7):
        super().__init__(templatePath, targetRect, isUseGrayScale)
        self.Threshold = threshold

    def Process(self, frame):
        result = super().Matching(frame)        
        ys, xs = np.where(result >= self.Threshold)
        if len(ys) > 0:
            self.IsFinished = True
            self.Result = True
        return super().Process(frame)

# テンプレートマッチングを行い、最も類似度の高い中心座標を取得するリクエスト
class TemplatePositionRequest(TemplateMatchingRequestBase):
    def __init__(self, templatePath, targetRect=None, isUseGrayScale=True, threshold=0.7):
        super().__init__(templatePath, targetRect, isUseGrayScale)
        self.Threshold = threshold

    def Process(self, frame):
        result = super().Matching(frame)        
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        if maxVal >= self.Threshold:
            self.IsFinished = True
            self.Result = maxLoc
        return super().Process(frame)
