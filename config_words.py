from openpyxl import load_workbook
from tkinter import *
from tkinter import messagebox, Toplevel


def add(text):
    filename = "swear_words.xlsx"

    wb_wordList = load_workbook(filename)
    ws_wordList = wb_wordList.worksheets[0]

    ctr = 1
    cell_val = ''
    while cell_val != '':
        cell_val = ws_wordList['A' + ctr].value
        ctr += 1

    ws_wordList['A' + str(ctr)] = text.lower()
    wb_wordList.save(filename)
    # messagebox.showinfo("DAA Speech Recognition", "Word has been added successfully!")
