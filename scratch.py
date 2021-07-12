# USE SCRATCH.PY TO TEST OUT CODE THEN TRANSFER TO MAIN.PY IF IT IS WORKING. THANKS!
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
from pygame import mixer

import censor
import config_words

# root application
root = Tk()
root.title("DAA Speech Recognition")
root.iconbitmap('img/favicon.ico')

# style of root
style = ttk.Style()
style.theme_use('winnative')

photo = PhotoImage(file='img/microphone.png').subsample(25, 25)


def progressBar():
    transWin = Toplevel(root)
    transWin.title("DAA Speech Recognition")
    transWin.iconbitmap('img/favicon.ico')

    labelProg = Label(transWin, text="Transcribing your file. Please Wait...")
    labelProg.pack(pady=10)
    progress = ttk.Progressbar(transWin, orient=HORIZONTAL, length=200, mode='determinate')
    progress.pack(pady=10)
    size = 100
    complete = 0
    speed = 10
    while complete < size:
        time.sleep(0.07)
        progress['value'] += (speed / size) * 100
        complete += speed
        transWin.update_idletasks()
    if complete == size:
        transWin.destroy()


def speakBtn():
    mixer.init()
    mixer.music.load('audio/chime.mp3')
    mixer.music.play()

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

            ogText.focus()
            ogText.delete(1.0, END)
            censorText.delete(1.0, END)
            ogText.insert(1.0, text)
            print(text)
            ogText.configure(state='disabled')
        except:
            messagebox.showerror("Error", "Sorry I can't recognize the audio. Please try again!")
            print("Sorry. I Don't Recognize The Audio")


def transcribeBtn():
    ogText.delete(1.0, END)
    r = sr.Recognizer()
    audfile = inputAudio.get()

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
        initialdir="C:\\Users\\John\\PycharmProjects\\daa-speech-recognition\\audio",
        title="Select a File",
        filetypes=(("Audio Files", "*.wav .mp3 .aac .m4a .midi"), ("All Files", "*.*")))
    inputAudio.delete(0, END)
    ogText.delete(1.0, END)
    censorText.delete(1.0, END)
    inputAudio.insert(0, str(root.filename))


def clearBtn():
    inputAudio.delete(0, END)
    ogText.delete(1.0, END)
    censorText.delete(1.0, END)


def addBtn():
    addWindow = Toplevel(root)
    addWindow.geometry("500x200")
    addWindow.title("Add Words")
    addWindow.iconbitmap('img/favicon.ico')

    lblCaption = Label(addWindow, text="You may add the words you wish to be censored.\nOnly input ONE WORD to be "
                                       "added in the list")
    inputWord = Entry(addWindow, width=35, borderwidth=5)
    btnAddWords = Button(addWindow, text="Add to List", command=config_words.add(inputWord.get()))
    btnRemoveWords = Button(addWindow, text="Remove from List")
    #btnExit = Button(addWindow, text="Exit Window", command=addWindow.destroy())
    lblCaption.pack()
    inputWord.pack()
    btnAddWords.pack()
    #btnExit.pack()


def censorBtn():
    redacted = censor.censorFile(ogText.get(1.0, END))
    censorText.insert(1.0, redacted)


# define labels
label1 = ttk.Label(root, text='Original Text')
label1.grid(row=2, column=0, sticky=W)
label2 = ttk.Label(root, text='Censored Text')
label2.grid(row=4, column=0, sticky=W)

# define textbox
ogText = Text(root, width=50, height=10)
ogText.grid(row=3, column=0, pady=10)
censorText = Text(root, width=50, height=10)
censorText.grid(row=5, column=0, pady=10)

# define entry
inputAudio = Entry(root, width=35, borderwidth=5)
inputAudio.grid(row=0, column=0, columnspan=3, padx=110, pady=10)

# define buttons
btnSpeak = Button(root, image=photo, command=speakBtn, bd=0, activebackground='#c1bfbf', overrelief='groove',
                  relief='sunken')
btnUpload = Button(root, text="Upload a File", command=uploadBtn)
btnTranscribe = Button(root, text="Transcribe the File", padx=35, command=transcribeBtn)
btnAdd = Button(root, text="Add your own words", padx=25, command=addBtn)
btnCensor = Button(root, text="Censor", padx=62, command=censorBtn)
btnClear = Button(root, text="Clear", padx=63, command=clearBtn)
btnQuit = Button(root, text="Exit Application", padx=39, command=root.quit)

# show the buttons
btnSpeak.grid(row=0, column=0, sticky=W)
btnUpload.grid(row=0, column=0, padx=25, pady=5, columnspan=50, sticky=W)
btnTranscribe.grid(row=6, column=0, columnspan=2, pady=5)
btnAdd.grid(row=7, column=0, columnspan=2, pady=5)
btnCensor.grid(row=8, column=0, columnspan=2, pady=5)
btnClear.grid(row=9, column=0, pady=5, padx=5, sticky=W)
btnQuit.grid(row=9, column=0, pady=5, sticky=E)

root.mainloop()
