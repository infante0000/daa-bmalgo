# USE SCRATCH.PY TO TEST OUT CODE THEN TRANSFER TO MAIN.PY IF IT IS WORKING. THANKS!
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font
import speech_recognition as sr
import pyttsx3
from pygame import mixer
from pydub import AudioSegment
from tkinter import messagebox
from functools import partial
import time
import censor, config_words

# root application
root = Tk()
root.title("Censoring Tool")
root.iconbitmap('img/favicon.ico')

# style of root
style = ttk.Style()
style.theme_use('winnative')

photo = PhotoImage(file='img/microphone.png').subsample(25, 25)


def progressBar():
    transWin = Toplevel(root)
    transWin.title("Censoring Tool")
    transWin.geometry("500x200")
    transWin.iconbitmap('img/favicon.ico')

    labelProg = Label(transWin, text="Transcribing your file. Please Wait...", font=("Helvetica", 12))
    labelProg.pack(pady=20)
    progress = ttk.Progressbar(transWin, orient=HORIZONTAL, length=200, mode='determinate')
    progress.pack(pady=10)
    size = 100
    complete = 0
    speed = 10
    while complete < size:
        time.sleep(0.30)
        progress['value'] += (speed / size) * 100
        complete += speed
        transWin.update_idletasks()
    if complete == size:
        transWin.destroy()


def speakBtn():
    mixer.init()
    mixer.music.load('audio/chime.mp3')
    mixer.music.play()
    clearBtn()

    r = sr.Recognizer()

    # run print to check which mic is to be used
    # print(sr.Microphone.list_microphone_names())

    engine = pyttsx3.init()

    # change number depending on which mic is used
    with sr.Microphone() as source:
        engine.say("Speak Now")
        print("Speak Now")
        engine.runAndWait()

        # adjust threshold
        r.energy_threshold = 3500
        audio = r.listen(source)

        try:
            text = str(r.recognize_google(audio, language="fil-PH")).lower()
            mixer.music.load('audio/chime-end.mp3')
            mixer.music.play()

            ogText.delete(1.0, END)
            ogText.insert(1.0, text)
            print(text)
        except:
            messagebox.showerror("Error", "Sorry I can't recognize the audio. Please try again!")
            print("Sorry. I Don't Recognize The Audio")


def transcribeBtn():
    ogText.delete(1.0, END)
    r = sr.Recognizer()

    audfile = inputAudio.get()

    if ogText.get(1.0, END) == '\n' and len(audfile) == 0:
        messagebox.showerror("Error", "There is no input to be transcribed.")

    else:
        if audfile.endswith('.wav'):
            with sr.AudioFile(audfile) as source:
                audio = r.listen(source)

                try:
                    print('Transcribing...')
                    text = str(r.recognize_google(audio, language="fil-PH")).lower()

                    progressBar()
                    print(text)
                    ogText.insert(1.0, text)

                except:
                    messagebox.showerror("Error", "Sorry I can't recognize the audio. Please make sure the audio is "
                                                  "audible.")
                    print("Sorry. I cannot recognize the audio")

        else:
            convert = messagebox.askyesno("Error", "The file uploaded is not supported. Do you want to convert file?")
            if convert == 1:
                src = audfile
                dst = "audio/converted.wav"

                # convert wav to mp3
                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")
                messagebox.showinfo("WAV Converter", "Conversion completed and is ready to be transcribed.")
                inputAudio.delete(0, END)
                inputAudio.insert(0, str(dst))
            else:
                pass


def uploadBtn():
    root.filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Audio Files", "*.wav .mp3 .aac .m4a .midi"), ("All Files", "*.*")))
    inputAudio.delete(0, END)
    inputAudio.insert(0, str(root.filename))


def clearBtn():
    ogText.delete(1.0, END)
    inputAudio.delete(0, END)
    censorText.delete(1.0, END)


def addBtn():
    # new window app
    addWindow = Toplevel(root)
    addWindow.geometry("500x300")
    addWindow.title("Add Words")
    addWindow.iconbitmap('img/favicon.ico')

    #define widgets for addWindow
    lblCaption = Label(addWindow, text="You may add the words you wish to be censored.\n Only input one word at a time.", font="Helvetica 12 bold")
    inputWord = Entry(addWindow, width=35, font="Helvetica 14")
    btnAddWords = Button(addWindow, text="Add to List", font="Helvetica 12", command=lambda: config_words.add(inputWord.get()))
    btnExit = Button(addWindow, text="Exit Window", font="Helvetica 12" , command=addWindow.destroy)

    #display in addWindow
    lblCaption.pack(pady=10)
    inputWord.pack(pady=10)
    btnAddWords.pack(pady=10)
    btnExit.pack(pady=10)


def censorBtn():
    if ogText.get(1.0, END) == '\n':
        messagebox.showerror("Error", "There is no input to be censored.")
    else:
        censorText.delete(1.0, END)
        censor.list_pattern.clear()
        redacted = censor.censorFile(ogText.get(1.0, END))
        censorText.insert(1.0, redacted)

        showCensoredWin = Toplevel(root)
        showCensoredWin.title("Censoring Tool")
        showCensoredWin.geometry("500x300")
        showCensoredWin.iconbitmap('img/favicon.ico')

        labelframe1 = LabelFrame(showCensoredWin, text="Censored Words")
        labelframe1.pack(fill="both", expand="yes")

        toplabel = Label(labelframe1, text="Words censored using Boyer Moore Algorithm", font="Helvetica 12 bold")
        toplabel.pack(pady=10)

        patternLabel = Label(labelframe1, text="\nPatterns Found:", font="Helvetica 12 underline")
        patternLabel.pack(padx=3)

        for p in range(len(censor.list_pattern)):
            patlistLabel = Label(labelframe1, text=str(censor.list_pattern[p]), font="Helvetica 12")
            patlistLabel.pack(padx=3)

        indexLabel = Label(labelframe1, text="\nMatch at Indexes:", font="Helvetica 12 underline")
        indexLabel.pack(padx=3)

        indexlistlabel = Label(labelframe1, text=", ".join(censor.final_index), font="Helvetica 12")
        indexlistlabel.pack(padx=3)


fontLabel = Font(family="Helvetica", size=12, weight="normal", underline=1)
fontButton = Font(family="Helvetica", size=10, weight="bold")

# define labels
label1 = ttk.Label(root, text='Original Text', font=fontLabel)
label1.grid(row=2, column=0, padx=10, sticky=W)
label2 = ttk.Label(root, text='Censored Text', font=fontLabel)
label2.grid(row=4, column=0, padx=10, sticky=W)

# define textbox
ogText = Text(root, width=75, padx=3, height=10, font=("Helvetica", 12))
ogText.grid(row=3, column=0, padx=10, pady=10)
censorText = Text(root, width=75, padx=3, height=10, font=("Helvetica", 12))
censorText.grid(row=5, column=0, padx=10, pady=10)

# define entry
inputAudio = Entry(root, width=35, borderwidth=5, font=("Helvetica", 12))
inputAudio.grid(row=0, column=0, columnspan=3, padx=110, pady=12)

# define buttons
btnSpeak = Button(root, image=photo, command=speakBtn, bd=0, activebackground='#c1bfbf', overrelief='groove',
                  relief='sunken')
btnUpload = Button(root, text="Upload a File", font=fontButton, command=uploadBtn)
btnTranscribe = Button(root, text="Transcribe the File", font=fontButton, padx=35, command=transcribeBtn)
btnAdd = Button(root, text="Add your own words", font=fontButton, padx=25, command=addBtn)
btnCensor = Button(root, text="Censor", font=fontButton, padx=62, command=censorBtn)
btnClear = Button(root, text="Clear", font=fontButton, padx=63, command=clearBtn)
btnQuit = Button(root, text="Exit Application", font=fontButton, padx=39, command=root.quit)

# show the buttons
btnSpeak.grid(row=0, column=0, padx=50, sticky=W)
btnUpload.grid(row=0, column=0, padx=75, pady=5, columnspan=50, sticky=W)
btnTranscribe.grid(row=6, column=0, columnspan=2, pady=5)
btnAdd.grid(row=7, column=0, columnspan=2, pady=5)
btnCensor.grid(row=8, column=0, columnspan=2, pady=5)
btnClear.grid(row=9, column=0, pady=5, padx=15, sticky=W)
btnQuit.grid(row=9, column=0, pady=5, padx=15, sticky=E)

root.mainloop()
