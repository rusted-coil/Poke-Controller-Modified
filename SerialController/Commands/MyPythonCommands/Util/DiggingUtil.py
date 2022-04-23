#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ImageProcessRequest import Rect

class DiggingImageProcessor:
    # previewから現在のマスの硬さ[0-4]を取得します。
    # gridsは(x, y)のtupleのリストです。左上を(0,0)とします。
    @ staticmethod
    def GetGridsDurability(parentCommand, preview, grids):
        pathList = ["../Images/template1.png", "../Images/template2.png", "../Images/template3.png"]
        gridTypes = []
        for x,y in grids:
            match = 0
            for i in range(len(pathList)):
                result = preview.RequestTemplateExist(
                    parentCommand=parentCommand, 
                    templatePath=pathList[i],
                    targetRect=Rect(88 + x*30, 44 + y*30, 30, 30),
                    timeout=0.1) # 掘る領域左上は88, 1マスは30x30
                if result:
                    match = i + 1
                    break
            gridTypes.append(match)
        return gridTypes
