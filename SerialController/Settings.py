#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, pickle
import tkinter as tk


class GuiSettings:
    SETTING_PATH = "./settings.poke"

    def __init__(self):
        # default values
        self.camera_id = tk.IntVar(value=0)
        self.com_port = tk.IntVar(value=0)
        self.fps = tk.StringVar(value='45')
        self.is_show_realtime = tk.BooleanVar(value=True)
        self.is_show_serial = tk.BooleanVar(value=False)
        self.is_use_keyboard = tk.BooleanVar(value=True)

    def load(self):
        if os.path.isfile(self.SETTING_PATH):
            load_settings = pickle.load(open(self.SETTING_PATH, 'rb'))

            # deserialize
            deserialized = {key: value[1](value=value[0]) for key, value in load_settings.items()}

            if self.__dict__.keys() != deserialized.keys():
                print('Setting items have been altered.')
                self.generate()
                self.load()
            else:
                self.__dict__ = deserialized
        else:
            print('No setting files can be found.')
            self.generate()
            self.load()

    def generate(self):
        self.save()
        print('A default settings file has been created.')

    def save(self, path=None):
        # Some preparations are needed because tkinter related objects are not serializable.
        data = {key: [value.get(), type(value)] for key, value in self.__dict__.items()}

        f = open(self.SETTING_PATH if path is None else path, 'wb')
        pickle.dump(data, f)


import numpy as np
import copy

H, W, K = map(int, input().split())
a = np.zeros((H, W), dtype=int)
print(a)

for i in range(H):
    s = input()
    for j in range(W):
        a[i, j] = 0 if s[j] == "." else 1
print(a)

_a = copy.deepcopy(a)
hls = []
wls = []
for i in range(2 ** H):
    hls.append(np.array(list(map(int, list(str((format(i, 'b')).zfill(H)))))))
    for j in range(2 ** W):
        wls.append(np.array(list(map(int, list(str(format(j, 'b').zfill(W)))))))

for i in range(len(hls)):
    for j in range(len(wls)):
        _a = copy.deepcopy(a)
        for k_ in range(H):
            _a[k_, :] = _a[k_, :] * wls[0]
        for l_ in range(W):
            _a[:, l_] = _a[:, l_] * hls[0]
        print(np.sum(_a))
