#--- Notepy - The Python-made Notepad - by Nik ---
#--- Author: Nikos-Nikitas ---
#--- GitHub: nikosnikitas ---

#--- importing our notepy class ---
from notepy import Notepy, NotepyGr
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
import os
import webbrowser

#--- function that changes the app's language ---
def changeLang(l=""):
    global lang
    lang = l
    return lang

app = ""

if __name__ == '__main__':
    langWin = Tk()
    langWin.title("Notepy - The Python-made Notepad")
    langWin.geometry("640x480")
    langWin.resizable(True, True)
    lang = changeLang("")
    lbl = Label(langWin, text="Select Language - Επιλογή Γλώσσας")
    lbl.pack()
    enBtn = Button(langWin, text="English", command = lambda:changeLang("en"))
    enBtn.pack()
    grBtn = Button(langWin, text="Ελληνικά", command = lambda:changeLang("gr"))
    grBtn.pack()
    lbl2 = Label(langWin, text="After selection click X to close this window. \n Μετά την επιλογή πατήστε στο Χ για να κλείσετε αυτό το παράθυρο.")
    lbl2.pack()
    langWin.mainloop()

    if lang == "en":
        langWin.destroy
        app = Notepy()
    if lang == "gr":
        langWin.destroy
        app = NotepyGr()