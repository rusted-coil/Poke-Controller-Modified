
import cv2
from Commands.PythonCommandBase import PythonCommand
from CustomPreview import Rect
from ImageProcessRequest import ScreenshotRequest

# ScreenshotRequestが正常に動くかテストします。
class ScreenshotTest(PythonCommand):
    NAME = 'スクリーンショットテスト'

    def __init__(self):
        super().__init__()

    def do(self):
        frame = cv2.imread("../Images/template3.png", cv2.IMREAD_COLOR)
        request = ScreenshotRequest("../Images/template3.png", Rect(5,5,20,20))
        request.Process(frame)
        if request.IsFinished and request.Result:
            print("テスト成功")
        else:
            print("テスト失敗")
