#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
import datetime

#--------------------------------------------------------------
# Model
#--------------------------------------------------------------

class CustomInputModel:
    pass

#--------------------------------------------------------------
# View
#--------------------------------------------------------------

class CustomInputView:
    # Frameを生成します。
    def CreateFrame(self, master):
        self.Frame = ttk.Labelframe(master)

        ## 日付
        self.DateRow = ttk.Frame(self.Frame)

        self.DateLabel = ttk.Label(self.DateRow)
        self.DateLabel.config(text='日付:')
        self.DateLabel.pack(side = tk.LEFT)

        self.YearLabel = ttk.Label(self.DateRow)
        self.YearLabel.config(text='Year')
        self.YearLabel.pack(side = tk.LEFT)

        self.YearList = list(range(2000, 2100))
        self.YearBox = ttk.Combobox(self.DateRow, width=6, values=self.YearList)
        self.YearBox.set(2000)
        self.YearBox.pack(side = tk.LEFT)

        self.MonthLabel = ttk.Label(self.DateRow)
        self.MonthLabel.config(text='Month')
        self.MonthLabel.pack(side = tk.LEFT)

        self.MonthList = list(range(1, 13))
        self.MonthBox = ttk.Combobox(self.DateRow, width=4, values=self.MonthList)
        self.MonthBox.set(1)
        self.MonthBox.pack(side = tk.LEFT)

        self.DayLabel = ttk.Label(self.DateRow)
        self.DayLabel.config(text='Day')
        self.DayLabel.pack(side = tk.LEFT)

        self.DayList = list(range(1, 32))
        self.DayBox = ttk.Combobox(self.DateRow, width=4, values=self.DayList)
        self.DayBox.set(1)
        self.DayBox.pack(side = tk.LEFT)

        self.TodayButton = ttk.Button(self.DateRow)
        self.TodayButton.config(text='今日の日付', command=lambda: self.SetDate(datetime.date.today()))
        self.TodayButton.pack(side = tk.LEFT, padx='10')

        self.DateRow.pack(anchor = tk.W, padx='5', pady = '5')

        ## 数値1
        self.Int1Row = ttk.Frame(self.Frame)

        self.Int1Label = ttk.Label(self.Int1Row)
        self.Int1Label.config(text='数値1:')
        self.Int1Label.pack(side = tk.LEFT)

        self.Int1Entry = ttk.Entry(self.Int1Row)
        self.Int1Entry.pack(side = tk.LEFT)

        self.Int1Row.pack(anchor = tk.W, padx='5', pady = '5')

        self.Frame.config(height='200', text='Custom Input')
        return self.Frame

    # 日付
    def GetDate(self):
        return datetime.date(int(self.YearBox.get()), int(self.MonthBox.get()), int(self.DayBox.get()))
    def SetDate(self, date):
        self.YearBox.delete(0, tk.END)
        self.YearBox.insert(tk.END, date.year)
        self.MonthBox.delete(0, tk.END)
        self.MonthBox.insert(tk.END, date.month)
        self.DayBox.delete(0, tk.END)
        self.DayBox.insert(tk.END, date.day)

    # 数値1
    def GetInt1(self):
        return self.Int1Entry.getint(0)
    def SetInt1(self, value):
        self.Int1Entry.delete(0, tk.END)
        self.Int1Entry.insert(tk.END, value)

#--------------------------------------------------------------
# Controller
#--------------------------------------------------------------

class CustomInputController:
    Model = CustomInputModel()
    View = None 

    # ViewであるFrameを生成します。
    def CreateFrame(self, master):
        if self.View is None:
            self.View = CustomInputView()
            return self.View.CreateFrame(master)
        else:
            return self.View.Frame

    # Viewに入力されている内容をModelにロードします。
    def LoadFromView(self):
        self.Model.Date = self.View.GetDate()
        self.Model.Int1 = self.View.GetInt1()

    # 日付を反映します。
    def SetDate(self, date):
        self.Model.Date = date
        self.View.SetDate(date)

#--------------------------------------------------------------

g_CustomInput = CustomInputController()
