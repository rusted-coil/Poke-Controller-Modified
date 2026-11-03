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

# 指定した座標のピクセルが特定の色であるかを判定するリクエスト
class PixelColorMatchRequest(RequestBase):
    """
    指定座標 (x, y) のピクセル色が、期待する色 (BGR) と一致するかを判定します。
    tolerance で各チャンネルの許容誤差を指定できます（デフォルト: 10）。

    使用例:
        # (100, 200) の座標が赤色 (BGR: 0, 0, 255) かどうかを許容誤差 15 で判定
        req = PixelColorMatchRequest(
            x=100, y=200,
            expectedBGR=(0, 0, 255),
            tolerance=15
        )
    """
    def __init__(self, x, y, expectedBGR, tolerance=10, targetRect=None):
        """
        Args:
            x (int): 判定対象の X 座標（targetRect が指定されている場合はその領域内の相対座標）
            y (int): 判定対象の Y 座標（targetRect が指定されている場合はその領域内の相対座標）
            expectedBGR (tuple): 期待する色を (B, G, R) のタプルで指定
            tolerance (int): 各チャンネルの許容誤差（0 なら完全一致のみ）
            targetRect (Rect|None): 判定対象の領域。None の場合はフレーム全体を対象とする
        """
        super().__init__(targetRect)
        self.X = x
        self.Y = y
        self.ExpectedBGR = np.array(expectedBGR, dtype=np.int16)
        self.Tolerance = tolerance

    def Process(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame

        # 座標がフレーム範囲内かチェック
        h, w = src.shape[:2]
        if 0 <= self.X < w and 0 <= self.Y < h:
            pixel = np.array(src[self.Y, self.X], dtype=np.int16)
            diff = np.abs(pixel - self.ExpectedBGR)
            matched = bool(np.all(diff <= self.Tolerance))

            # デバッグ用: 座標・実際の色・期待色・差分・判定結果を表示
#            print(f"[PixelColorMatch] pos=({self.X}, {self.Y}) "
#                  f"actual_BGR=({pixel[0]}, {pixel[1]}, {pixel[2]}) "
#                  f"expected_BGR=({self.ExpectedBGR[0]}, {self.ExpectedBGR[1]}, {self.ExpectedBGR[2]}) "
#                  f"diff=({diff[0]}, {diff[1]}, {diff[2]}) "
#                  f"tolerance={self.Tolerance} "
#                  f"matched={matched}")

            self.IsFinished = True
            self.Result = matched
        else:
            # 座標が範囲外の場合は一致として完了
#            print(f"[PixelColorMatch] pos=({self.X}, {self.Y}) is out of bounds "
#                  f"(frame size: {w}x{h})")
            self.IsFinished = True
            self.Result = False

        return super().Process(frame)
    