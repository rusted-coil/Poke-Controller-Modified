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

# Base class representing image processing requests.
class RequestBase:
    def __init__(self, targetRect):
        self.TargetRect = targetRect
        self.IsFinished = False

    def Process(self, frame):
        if not self.TargetRect is None:
            cv2.rectangle(frame, self.TargetRect.TopLeft(), self.TargetRect.BottomRight(), (0, 0, 255), 1)
        return frame

# Request to save a screenshot
class ScreenshotRequest(RequestBase):
    def __init__(self, savePath, targetRect = None, isUseGrayScale=True):
        super().__init__(targetRect)
        self.Path = savePath
        self.IsUseGrayScale = isUseGrayScale

    def Process(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if self.IsUseGrayScale else src
        # Save as image
        cv2.imwrite(self.Path, src)
        self.IsFinished = True
        self.Result = True        
        return frame

# Base class for template matching requests
class TemplateMatchingRequestBase(RequestBase):
    def __init__(self, templatePath, targetRect=None, isUseGrayScale=True):
        super().__init__(targetRect)
        self.Template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE if isUseGrayScale else cv2.IMREAD_COLOR)
        self.IsUseGrayScale = isUseGrayScale

    def Matching(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if self.IsUseGrayScale else src
        return cv2.matchTemplate(src, self.Template, cv2.TM_CCOEFF_NORMED)

# Request to perform template matching and check for existence
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

# Request to perform template matching and get the center coordinates with the highest similarity
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

# Request to determine if the pixel at the specified coordinates is a specific color
class PixelColorMatchRequest(RequestBase):
    """
    Determines if the pixel color at the specified coordinates (x, y) matches the expected color (BGR).
    You can specify the tolerance for each channel (default: 10).

    Usage example:
        # Check if the coordinates (100, 200) are red (BGR: 0, 0, 255) with tolerance 15
        req = PixelColorMatchRequest(
            x=100, y=200,
            expectedBGR=(0, 0, 255),
            tolerance=15
        )
    """
    def __init__(self, x, y, expectedBGR, tolerance=10, targetRect=None):
        """
        Args:
            x (int): X coordinate to check (relative to targetRect if specified)
            y (int): Y coordinate to check (relative to targetRect if specified)
            expectedBGR (tuple): Expected color as (B, G, R) tuple
            tolerance (int): Tolerance for each channel (0 for exact match only)
            targetRect (Rect|None): Target area. If None, checks the entire frame
        """
        super().__init__(targetRect)
        self.X = x
        self.Y = y
        self.ExpectedBGR = np.array(expectedBGR, dtype=np.int16)
        self.Tolerance = tolerance

    def Process(self, frame):
        src = self.TargetRect.SliceFrame(frame) if not self.TargetRect is None else frame

        # Check if coordinates are within frame bounds
        h, w = src.shape[:2]
        if 0 <= self.X < w and 0 <= self.Y < h:
            pixel = np.array(src[self.Y, self.X], dtype=np.int16)
            diff = np.abs(pixel - self.ExpectedBGR)
            matched = bool(np.all(diff <= self.Tolerance))

            # Debug: Display coordinates, actual color, expected color, difference, and result
#            print(f"[PixelColorMatch] pos=({self.X}, {self.Y}) "
#                  f"actual_BGR=({pixel[0]}, {pixel[1]}, {pixel[2]}) "
#                  f"expected_BGR=({self.ExpectedBGR[0]}, {self.ExpectedBGR[1]}, {self.ExpectedBGR[2]}) "
#                  f"diff=({diff[0]}, {diff[1]}, {diff[2]}) "
#                  f"tolerance={self.Tolerance} "
#                  f"matched={matched}")

            self.IsFinished = True
            self.Result = matched
        else:
            # If coordinates are out of bounds, consider it not matched and complete
#            print(f"[PixelColorMatch] pos=({self.X}, {self.Y}) is out of bounds "
#                  f"(frame size: {w}x{h})")
            self.IsFinished = True
            self.Result = False

        return super().Process(frame)
    