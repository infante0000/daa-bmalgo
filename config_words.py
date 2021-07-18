from openpyxl import load_workbook
from tkinter import messagebox


def add(word):
    filename = "swear_words.xlsx"
    wb = load_workbook(filename)
    ws = wb['Sheet1']

    try:
        if not word:
            raise ValueError
        else:
            ws.append([word])
            wb.save(filename)
            messagebox.showinfo("Censoring Tool", "Word has been added successfully!")
    except ValueError:
        messagebox.showerror("Censoring Tool", "Adding the word failed.")
        pass
