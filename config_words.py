from openpyxl import load_workbook
from tkinter import *
from tkinter import messagebox

addWindow = Toplevel()
addWindow.geometry("500x200")
addWindow.title("Add Words")
addWindow.iconbitmap('img/favicon.ico')

def add():
    stringAdd = inputWord.get()
    filename = "trial.xlsx"

    wb_wordList = load_workbook(filename)
    ws_wordList = wb_wordList.worksheets[0]

    ctr = 1
    cell_val = ''
    while cell_val != '':
        cell_val = ws_wordList['A' + ctr].value
        ctr += 1

    try:
        ws_wordList['A' + str(ctr)] = stringAdd.lower()
        wb_wordList.save(filename)
        messagebox.showinfo("DAA Speech Recognition", "Word has been added successfully!")
    except:
        messagebox.showerror("DAA Speech Recognition", "Adding the word failed.")


lblCaption = Label(addWindow, text="You may add the words you wish to be censored.")
inputWord = Entry(addWindow, width=35, borderwidth=5)
btnAddWords = Button(addWindow, text="Add to List")
btnExit = Button(addWindow, text="Exit Window", command=addWindow.destroy)

lblCaption.pack(pady=10)
inputWord.pack(pady=10)
btnAddWords.pack(pady=10)
btnExit.pack(pady=10)
