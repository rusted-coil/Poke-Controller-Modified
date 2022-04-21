#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# 画像処理のリクエストを表す基底クラスです。
class RequestBase:
    def __init__(self, targetRect):
        self.TargetRect = targetRect
        self.IsFinished = False

    def Process(self, frame):
        if not self.TargetRect is None:
            cv2.rectangle(frame, self.TargetRect.TopLeft, self.TargetRect.BottomRight, (0, 0, 255), 1)
        return frame

# スクリーンショットを保存するリクエスト
class ScreenshotRequest(RequestBase):
    def __init__(self, targetRect):
        self.TargetRect = targetRect

    def Process(self, frame):
        self.IsFinished = True
        return frame

# パターンマッチングのリクエスト
class PatternMatchingRequest(RequestBase):
    def __init__(self, targetRect):
        super().__init__(targetRect)

    def Process(self, frame):
        return super().Process(frame)

