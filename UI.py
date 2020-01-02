try:
    # for Python2
    from Tkinter import *
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import filedialog as fd
    from Tkinter import messagebox as ms

except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as fd
    from tkinter import messagebox as ms

# Libraries for document data extraction
import PIL 
from PIL import ImageTk, Image,ImageEnhance
import pandas as pd
import cv2
import os
import re
import json
import datetime
import time 
from computervision_OCR import *
import sys
sys.path.insert(1, 'preproceesing/')
from Document_digitization_preprocessing3jan import *
from invoice_extraction import *
import numpy as np
#from pdf2image import convert_from_path, convert_from_bytes
#import PyPDF2
import numpy as np
from alyn import Deskew
import math
from scipy.ndimage import rotate 
from scipy import ndimage
from scipy.ndimage.filters import rank_filter
import warnings
from sys import argv
warnings.filterwarnings("ignore")




class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("INTELLIGENT DATA EXTRACTION")

        self.master.geometry("1500x1000")
        self.c_size = (500,400)
        self.file = ""
        self.entryarray = []
        self.labelarray = []
        self.labeltextarray = []
        # self.confidencearray= []
        s = self.c_size
        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            

        self.Frame1 = Frame(master, bg="#ececec")
        self.Frame1.grid(row = 0, column = 3, rowspan = 6, columnspan = 2, sticky = W+E+N+S)
        

        for c in range(3):
            self.Frame1.columnconfigure(c, weight=1)


        self.Frame4 = Frame(master, bg="#ececec")
        self.Frame4.grid(row = 5, column = 3, rowspan = 2, columnspan = 2, sticky = W+E+N+S) 

        for c in range(3):
            self.Frame4.columnconfigure(c, weight=1)
        for c in range(3):
            self.Frame4.rowconfigure(c, weight=1)

        self.canvasLogo = Canvas(self.Frame4,height=280,width=280,bg='#ececec',bd=0, highlightthickness=0)
        self.canvasLogo.grid(row = 1, column = 1)

        eImg=Image.open("ey-logo.png").resize((280,200),Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(eImg)
        self.canvasLogo.delete(ALL)
        self.canvasLogo.create_image(280/2,280/2,
                anchor=CENTER,image=self.img2)
        self.canvasLogo.update()



        self.Frame2 = Frame(master, bg="#8a8a8a")
        self.Frame2.grid(row = 5, column = 0, rowspan = 2, columnspan = 3, sticky = W+E+N+S)


        self.loadimage = tk.PhotoImage(file="button png (1).png")

        self.openbutton = Button(self.Frame2,text='Open New Image'
            ,command=self.make_image,  highlightthickness = 0, image=self.loadimage, bd = -2,activebackground ="#8a8a8a",  bg="#8a8a8a",compound=CENTER,fg="#555555")
        self.openbutton.pack(side=LEFT, expand=YES)
        self.openbutton.pack_propagate(False)

        self.openbutton.config(font=("arial", 12))

        self.clearbutton = Button(self.Frame2,text='Reset'
            ,command=self.clearImage,  highlightthickness = 0, image=self.loadimage, bd = -2,activebackground ="#8a8a8a", bg="#8a8a8a", compound=CENTER,fg="#555555")
        self.clearbutton.pack(side=LEFT, expand=YES)
        self.clearbutton.config(state="disabled")
        self.clearbutton.config(font=("arial", 12))



        self.processbutton = Button(self.Frame2,text='Process'
            ,command=self.processing,  highlightthickness = 0, image=self.loadimage, bd = -2,activebackground ="#8a8a8a", bg="#8a8a8a", compound=CENTER,fg="#555555")
        self.processbutton.pack(side=LEFT, expand=YES)
        self.processbutton.config(state="disabled")
        self.processbutton.config(font=("arial", 12))


        self.Frame3 = Frame(master, bg="green")
        self.Frame3.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, sticky = W+E+N+S)

        self.canvas = Canvas(self.Frame3,height=500,width=500,bg='black',bd=40)
        self.canvas.pack(expand=YES, fill=BOTH)
        '''self.canvas.columnconfigure(0,weight=1)
        self.canvas.rowconfigure(0,weight=1)'''

        # inp = [{'Field':"", 'Confidence_Score(%)':"",'Values':""}, {'Field':"", 'Confidence_Score(%)':"",'Values':""}, {'Field':"", 'Confidence_Score(%)':"",'Values':""}]
        # data = pd.DataFrame(inp)
        # dfObj = pd.DataFrame(columns=['Confidence_Score(%)', 'Field', 'Values'])
        inp = [{'Field':"", 'Values':""}, {'Field':"", 'Values':""}, {'Field':"", 'Values':""}]
        data = pd.DataFrame(inp)
        dfObj = pd.DataFrame(columns=[ 'Field', 'Values'])
        
        
        self.resultsToForm(data)
        if dfObj.empty == True:
            self.submitbutton.destroy()
            
        self.canvas.update()

        textID = self.canvas.create_text(self.canvas.winfo_height()/2,self.canvas.winfo_width()/2, text="No Image Selected",font=('',30), anchor="nw", fill="white")


    # Function to set focus (cursor) 
    def focus(self,field,event): 
        # set focus on the course_field box 
        field.focus_set() 

    def set_text(self,e,text):
        e.delete("1.0",END)
        e.insert(INSERT,text)
        return

    def get_text(self,e):
        return e.get("1.0",END)

    
    def make_image(self):
        try:
            File = fd.askopenfilename()
            self.pilImage = Image.open(File)
            self.file = File

            print (File)
            #self.file =self.pilImage

            re=self.pilImage.resize(self.c_size,Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(re)
            self.canvas.delete(ALL)
            self.canvas.create_image(self.c_size[0]/2+10,self.c_size[1]/2+10,
                anchor=CENTER,image=self.img)

            self.processbutton.config(state="normal")
            #self.resetAll()
            self.openbutton.config(state='disabled')
            self.clearbutton.config(state="normal")


            print (5)
            
            
        except Exception as e:
            print (str(e))
            ms.showerror('Error!','File type is unsupported.')

# -------------------------------------------Code for document data extraction-------------------------------------------------------------------------


    def processing(self):
    
                start=datetime.datetime.now()
                document=''
                image_stream=open(self.file,"rb").read()
                print("**************************Image preprocessing starts**************************")            
                image_stream2=image_preprocessing(self.file,image_stream)
                print("**************************OCR process starts**********************************")
                OCR_result=OCR_v1(self.file,image_stream2)    # OCR extraction output
                textdata=OCR_result    
                print("**************************Entity extraction starts*****************************")         
                data=invoice_extraction(textdata)
                end_time=datetime.datetime.now()   
                print(data)          
                table=pd.DataFrame(list(data.items()),columns=['Field','Values'])     # Extracted data in list form
                # conf=list()
                # textconf=0.0
                # for i in range(int(int(table.size)/2)):
                #     if table['Values'][i]=='NA':
                #         conf.append("{0:.1f}".format(textconf))
                #     else:
                #         conf.append("{0:.6f}".format(textConfidence))

                # table['Confidence_Score(%)']=conf
                self.resultsToForm(table)                                            # Table is created based on extracted data 

#------------------------------------UI code--------------------------------------------------------------------------------------------------------------

      
     # Design for table containing extracted data            

    def resultsToForm(self,data):
        length = len(data)
        for r in range(length*4+1):
            self.Frame1.rowconfigure(r, weight=1) 


        self.label1 = Label(self.Frame1, text="Fields", bg="#8a8a8a",fg="white",width=20, highlightcolor="black", relief=GROOVE,bd=2)
        self.label1.grid(row=0, column=0, sticky="nsew") 
        self.label1.config(font=("arial", 10))
        self.label2 = Label(self.Frame1, text="Values", bg="#8a8a8a",fg="white",width=30, relief=GROOVE,bd=2)
        self.label2.grid(row=0, column=1, sticky="nsew") 
        self.label2.config(font=("arial", 10))
        # self.label3 = Label(self.Frame1, text="Confidence Score", bg="#8a8a8a",fg="white",width=20, relief=GROOVE,bd=2)
        # self.label3.grid(row=0, column=2, sticky="nsew") 
        # self.label3.config(font=("arial", 10))
        



        i=1
        for index, row in data.iterrows():
            if i%2!=0:
                bg1 = "#d8d8d8"
                bg2 = "#d8d8d8"
                bg3 = "#d8d8d8"
                fg1 = "black"
            else:
                bg1 = "#b1b1b1"
                bg2 = "#b1b1b1"
                bg3 = "#b1b1b1"
                fg1 = "black"

            label = Label(self.Frame1, text=row['Field'], bg=bg1,fg=fg1,width=20)
            label.grid(row=i, column=0, sticky="nsew")
            label.config(font=("arial", 10)) 

            self.labelarray.append(label)

            name_field = Text(self.Frame1,width=40,height=1,fg=fg1,wrap=WORD, bg=bg2,highlightthickness=0,bd=2,relief=FLAT)
            name_field.bind("<Return>", name_field.focus_set)
            name_field.config(font=("arial", 10))
            name_field.grid(row=i, column=1, sticky="nsew")

            self.entryarray.append(name_field)

            # label = Label(self.Frame1, text=row['Confidence_Score(%)'],fg=fg1, bg=bg3,width=20)
            # label.grid(row=i, column=2, sticky="nsew") 
            # label.config(font=("arial", 10))
            
            # self.confidencearray.append(label)

            
            
            self.labeltextarray.append(row['Field'])

            

            if (row['Values']==None) or (row['Values']==''):
                self.set_text(name_field,"")
            else:
                self.set_text(name_field,row['Values'])         

            i+=1

        self.submitbutton = Button(self.Frame1,text='Submit',command=self.submit,  highlightthickness = 0, image=self.loadimage, bd = -2,activebackground="#ececec", bg="#ececec", compound=CENTER,fg="#555555")
        self.submitbutton.config(font=("arial", 12))
        self.submitbutton.grid(row=15,column=1)

    def clearImage(self):

        self.openbutton.config(state="normal")
        self.resetAll()

    def submit(self):
        
        entry = ""
        for i in range(len(self.entryarray)):
            entry+=(self.labeltextarray[i]+":"+self.get_text(self.entryarray[i]).strip()+",")

        file = open("result.txt","a")
        file.write(entry + '\n')
        file.close()

        self.resetAll()

    def resetAll(self):
        
        self.canvas.delete(tk.ALL)

        self.canvas.update()
        textID = self.canvas.create_text(self.canvas.winfo_height()/2,self.canvas.winfo_width()/2, text="No Image Selected",font=('',30), anchor="nw", fill="white")



        if len(self.entryarray)>0:
            for i in range(len(self.entryarray)):
                self.entryarray[i].destroy()
                self.labelarray[i].destroy()
                # self.confidencearray[i].destroy()
            self.submitbutton.destroy()
            self.label1.destroy()
            self.label2.destroy()
           # self.label3.destroy()




        self.entryarray = []
        self.labeltextarray = []
        self.labelarray = []
        # self.confidencearray = []
        self.file = ""
        self.processbutton.config(state="disabled")
        self.openbutton.config(state="normal")
        self.clearbutton.config(state="disabled")

       # inp = [{'Field':"", 'Confidence_Score(%)':"",'Values':""}, {'Field':"", 'Confidence_Score(%)':"",'Values':""}, {'Field':"", 'Confidence_Score(%)':"",'Values':""}]
        
        inp = [{'Field':"", 'Values':""}, {'Field':"", 'Values':""}, {'Field':"", 'Values':""}]
        data = pd.DataFrame(inp)
        dfObj = pd.DataFrame(columns=[ 'Field', 'Values'])
        
        # dfObj = pd.DataFrame(columns=['Confidence_Score(%)', 'Field', 'Values'])
        
        self.resultsToForm(data)
        if dfObj.empty == True:
            self.submitbutton.destroy()

        self.canvas.update()

    def Remove1(self,duplicate): 
        final_names = [] 
        for num in duplicate: 
            if num not in final_names: 
                final_names.append(num) 
        return final_names




root = Tk()
root.state("zoomed")
root.geometry("400x200+200+200")
app = Application(master=root)
app.mainloop()