
import cv2
import numpy as np
from Commands.PythonCommandBase import PythonCommand
from CustomPreview import Rect
from ImageProcessRequest import ScreenshotRequest

# DiggingUtilが正常に動くかテストします。
class DiggingUtilTest(PythonCommand):
    NAME = '化石掘りテスト'

    def __init__(self):
        super().__init__()

    def do(self):
        frame = cv2.imread("../Images/out.png", cv2.IMREAD_GRAYSCALE)
        templates = [
            cv2.imread("../Images/template1.png", cv2.IMREAD_GRAYSCALE),
            cv2.imread("../Images/template2.png", cv2.IMREAD_GRAYSCALE),
            cv2.imread("../Images/template3.png", cv2.IMREAD_GRAYSCALE),
        ]
        gridTypes = []
        for y in range(6):
            gridTypesLine = []
            for x in range(6):
                grid = frame[y*30:y*30+30, x*30:x*30+30]
                match = 0
                for i in range(3):
                    result = cv2.matchTemplate(grid, templates[i], cv2.TM_CCOEFF_NORMED)
                    ys, xs = np.where(result >= 0.7)
                    if len(ys) > 0:
                        match = i + 1
                        break
                gridTypesLine.append(match)
            gridTypes.append(gridTypesLine)
        print(gridTypes)
                
