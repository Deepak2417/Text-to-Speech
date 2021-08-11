#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[32]:






# header files


from gtts import gTTS
from IPython.display import Audio
import pyttsx3
import PyPDF2
import random as rn
import requests
import gtts
import shutil
from playsound import playsound
from nltk.tokenize import word_tokenize
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


# In[33]:


#backend



def msgBox(msg):
    msgbox= Toplevel();
    msgbox.title("Error")
    errmsg= Label(msgbox, text=msg)
    errmsg.grid(row=0,column=0)


def setFilepath(path):
    path= path[:-3]+"mp3"
    print(path)
    return path
    
    
#to convert text to speech in offline mode
def offlineText(text):
    speaker = pyttsx3.init()
    speaker.setProperty("rate", 100)
    speaker.say(text)
    speaker.runAndWait()

#to convert pdf to speech in offline mode
def offlinePdf(path, startPage, endPage):
    new_path="r'"+path+"'"
    book = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    #print(pages)
    speaker = pyttsx3.init()
    for currentPage in range(startPage, endPage+1):
        page = pdfReader.getPage(currentPage)
        text = page.extractText()
        #print(text)
        speaker.setProperty("rate", 100)
        speaker.say(text)
        speaker.runAndWait()
        currentPage = currentPage + 1
        

#to convert text to speech in online mode
def onlineText(text):
    tts = gTTS(text)
    count = rn.randrange(0,1000000)
    tts.save(f'{count}.mp3')
    sound_file = f'{count}.mp3'
    return sound_file

#to convert pdf to speech in online mode
def onlinePdf(path, startPage, endPage):
    book = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    #print(pages)
    string = ''
    for currentPage in range(startPage, endPage+1):
        page = pdfReader.getPage(currentPage)
        text = page.extractText()
        sttg = word_tokenize(text)
        for t in range(0,len(sttg)):
            string+=(sttg[t]+' ')

        #print(string)
        tts = gTTS(string)
        count = rn.randrange(0,1000000)
        tts.save(f'{count}.mp3')
        sound_file = f'{count}.mp3'
        currentPage = currentPage + 1
        
    return sound_file


# In[36]:


#making user window

# from tkinter import *
# from tkinter import messagebox
# from tkinter import filedialog

# import requests
# from db import Database



#to display window component for PDF tab
def switchOptions():
    pdf_text.set("")
    dis_text.set("")
    txt_label = Label(app, text='Enter Text:', font=('bold', 14), pady=20, padx=10)
    txt_label.grid(row=0, column=0, sticky=W)
    pdf_entry = Entry(app, text="...", textvariable=pdf_text, width=60)
    pdf_entry.grid(row=0, column=1)
    pdf_browse.grid_forget()
    pdf_startLabel.grid_forget()
    pdf_start.grid_forget()
    pdf_endLabel.grid_forget()
    pdf_end.grid_forget()
    

#event to select pdf files
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", 
                                          filetypes = (("PDF files","*.pdf"),("all files", "*.*")))
    #pdf_entry.delete(0,END)
    pdf_text.set(filename)
    

#to display window component for Text tab
def txtOptions():
    pdf_text.set("")
    dis_text.set("")
    pdf_label = Label(app, text='Select file:', font=('bold', 14), pady=20, padx=10)
    pdf_label.grid(row=0, column=0, sticky=W)
    pdf_entry = Entry(app, text="...", textvariable=pdf_text, width=60)
    pdf_entry.grid(row=0, column=1)
    pdf_browse.grid(row=0,column=3, padx=20)
    pdf_startLabel.grid(row=2, column=0, sticky=E, padx=2)
    pdf_start.grid(row=2, column=1, sticky=W, padx=5)
    pdf_endLabel.grid(row=2, column=1, sticky=E)
    pdf_end.grid(row=2, column=2, sticky=W, padx=2)
        
    
   
    
#to perform network check
def networkCheck():
    url = "https://www.redhat.com/"
    dis_text.set("")
    timeout = 5.0
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False
        

#event for convert button click and to call conversion methods
def convertText():
    
    try:
        raise gTTSError()
        if networkCheck()==True:
            if bool(pdf_browse.winfo_ismapped())==True:
                aud_file=onlinePdf(pdf_text.get(), pdf_startPage.get(), pdf_endPage.get())
                playsound(aud_file)
                dis_text.set(f'Audio file saved at {setFilepath(pdf_text.get())}')
                shutil.move(aud_file, setFilepath(pdf_text.get()))
            else:
                #dis_text.set("online Text")
                aud_file=onlineText(pdf_text.get())
                playsound(aud_file)
                dis_text.set(f'Audio file saved at Desktop/{aud_file}')
                shutil.move(aud_file, f'Desktop/{aud_file}')
        else:
            if bool(pdf_browse.winfo_ismapped())==True:
                offlinePdf(pdf_text.get(), pdf_startPage.get(), pdf_endPage.get())
                dis_text.set("Your task is processed in offline mode")
            else:
                offlineText(pdf_text.get())
                dis_text.set("Your task is processed in offline mode")
    except TclError:
        msgBox("Invalid input type")
    except FileNotFoundError:
        msgBox("No such file!")
    except ValueError:
        msgBox("Please enter some value")
    except IndexError:
        msgBox("Enter valid Page number")
    except AssertionError:
        msgBox("No text to speak!")
    except PyPDF2.utils.PdfReadError:
        msgBox("Improper file format! Select PDF files only")
    except gtts.tts.gTTSError:
        msgBox("Sever taking too long to response!\r\nCheck your connection once.")

    

    

    
    
    
    
#to initiate the window
app = Tk()

#string variable for entry component
pdf_text=StringVar()

#string variable for display_spk label component
dis_text= StringVar()

pdf_startPage= IntVar()
pdf_endPage= IntVar()

#Browse button
pdf_browse = Button(app, text="Browse",command=browseFiles)
pdf_browse.grid(row=0,column=3, sticky=E)

pdf_startLabel = Label(app, text='Start Page:', font=('bold', 12), pady=20)
pdf_startLabel.grid(row=2, column=0, sticky=E, padx=2)
pdf_start = Entry(app, text="...", textvariable=pdf_startPage, width=5)


pdf_endLabel = Label(app, text='End Page:', font=('bold', 12), pady=20, padx=2)
pdf_endLabel.grid(row=2, column=1, sticky=E)
pdf_end = Entry(app, text="...", textvariable=pdf_endPage, width=5)

switchOptions()

#Convert button
convert_spk = Button(app, text="Convert", command=lambda: convertText())
convert_spk.grid(row=5, columnspan=4, pady=20)

#Label to display mode
display_spk = Label(app, text="....", textvariable=dis_text)
display_spk.grid(row=7, columnspan=4)

#code to switch between Text and PDF tab
toolbar = Menu(app)
toolbar.add_command(label="Text", command=switchOptions)
toolbar.add_command(label="PDF", command=txtOptions)

#to display title 
app.title('Text-to-Speech')

#define window size
app.geometry('600x300')

#configure and display window
app.config(menu=toolbar)
app.mainloop()


# In[ ]:




