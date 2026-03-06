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
    # Generate Frame.
    def CreateFrame(self, master):
        self.Frame = ttk.Labelframe(master)

        ## Date
        self.DateRow = ttk.Frame(self.Frame)

        self.DateLabel = ttk.Label(self.DateRow)
        self.DateLabel.config(text='Date:')
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
        self.TodayButton.config(text='Today\'s Date', command=lambda: self.SetDate(datetime.date.today()))
        self.TodayButton.pack(side = tk.LEFT, padx='10')

        self.DateRow.pack(anchor = tk.W, padx='5', pady = '5')

        ## Number 1
        self.Int1Row = ttk.Frame(self.Frame)

        self.Int1Label = ttk.Label(self.Int1Row)
        self.Int1Label.config(text='Number 1:')
        self.Int1Label.pack(side = tk.LEFT)

        self.Int1Entry = ttk.Entry(self.Int1Row)
        self.Int1Entry.setvar('0')
        self.Int1Entry.pack(side = tk.LEFT)

        self.Int1Row.pack(anchor = tk.W, padx='5', pady = '5')

        self.Frame.config(height='200', text='Custom Input')
        return self.Frame

    # Date
    def GetDate(self):
        return datetime.date(int(self.YearBox.get()), int(self.MonthBox.get()), int(self.DayBox.get()))
    def SetDate(self, date):
        self.YearBox.delete(0, tk.END)
        self.YearBox.insert(tk.END, date.year)
        self.MonthBox.delete(0, tk.END)
        self.MonthBox.insert(tk.END, date.month)
        self.DayBox.delete(0, tk.END)
        self.DayBox.insert(tk.END, date.day)

    # Number 1
    def GetInt1(self):
        try:
            return int(self.Int1Entry.get())
        except ValueError:
            print('Int1 value is invalid')
            return 0        
    def SetInt1(self, value):
        self.Int1Entry.delete(0, tk.END)
        self.Int1Entry.insert(tk.END, value)

#--------------------------------------------------------------
# Controller
#--------------------------------------------------------------

class CustomInputController:
    Model = CustomInputModel()
    View = None 

    # Generate the Frame that is the View.
    def CreateFrame(self, master):
        if self.View is None:
            self.View = CustomInputView()
            return self.View.CreateFrame(master)
        else:
            return self.View.Frame

    # Load the content entered in the View into the Model.
    def LoadFromView(self):
        self.Model.Date = self.View.GetDate()
        self.Model.Int1 = self.View.GetInt1()

    # Reflect the date.
    def SetDate(self, date):
        self.Model.Date = date
        self.View.SetDate(date)

    # Reflect Int1.
    def SetInt1(self, value):
        self.Model.Int1 = value
        self.View.SetInt1(value)

#--------------------------------------------------------------

g_CustomInput = CustomInputController()
