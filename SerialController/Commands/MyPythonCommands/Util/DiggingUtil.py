#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DiggingImageProcessor:
    def __init__(self, preview):
        self.Preview = preview

    # Previewから現在のマスの硬さ[0-4]を取得します。
    # gridsは(x, y)のtupleのリストです。
    def GetGridsDurability(self, grids):
        for x,y in grids:
            pass

