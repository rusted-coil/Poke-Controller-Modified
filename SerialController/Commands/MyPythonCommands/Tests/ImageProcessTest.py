from socket import timeout
import cv2
from Commands.CustomPythonCommandBase import CustomPythonCommand
from ImageProcessRequest import Rect, ScreenshotRequest

# ScreenshotRequestが正常に動くかテストします。
class ScreenshotTest(CustomPythonCommand):
    NAME = 'ImageProcessテスト'

    def __init__(self, preview):
        super().__init__(preview)

    def do(self):
        self.Preview.RequestTemplateExist(
            parentCommand=self, 
            templatePath="../Images/template1.png",
            targetRect=Rect(50, 50, 50, 50),
            timeout=10.0)
