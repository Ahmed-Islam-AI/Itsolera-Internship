#Importing necessory libraries
import tensorflow as tf
from tensorflow import keras
import pickle as pkl
import cv2
import numpy as np
import transformers
import pathlib
import PIL 
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
from PIL import Image,ImageTk
import backend as bs

#loading saved artifects from backend
bs.load_saved_artifects()

class Main:
    def __init__(self,root):
        self.root=root
        self.root.title("Content Moderation System")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(0,0)

        self.main_frame=Frame(self.root,bg="#FFDF00")
        self.main_frame.pack(fill=BOTH,expand=True)

        self.main_label=Label(self.main_frame,bg="#87CEEB",text="Content Moderation System",bd=10,relief=GROOVE,font=("Times new roman",40,'bold'),fg="black")
        self.main_label.pack(side=TOP,fill=X)

        self.main_label2=Label(self.main_frame,bg="#87CEEB",text="Team Epsilon Deep Learning Project",bd=10,relief=GROOVE,font=("Times new roman",40,'bold'),fg="black")
        self.main_label2.pack(side=BOTTOM,fill=X)

        self.image_moderation=Frame(self.main_frame,bg="#FFDF00",bd=10,relief=GROOVE)
        self.image_moderation.place(x=0,y=90,height=520,width=675)

        self.text_moderation=Frame(self.main_frame,bg="#FFDF00",bd=10,relief=GROOVE)
        self.text_moderation.place(x=675,y=90,height=520,width=675)

        self.text_label=Button(self.text_moderation,font=("times new roman",20,'bold'),bd=5,relief=GROOVE,bg="lightgreen",fg="black",text="Enter Your Text",activebackground="#87CEEB")
        self.text_label.place(x=200,y=20,width=240,height=60)

        self.entry1=Text(self.text_moderation,font=("times new roman",20,'bold'),relief=GROOVE,bd=5)
        self.entry1.place(x=20,y=90,width=610,height=200)
        
        self.classify_text=Button(self.text_moderation,font=("times new roman",20,'bold'),bd=8,relief=RIDGE,bg="lightgreen",fg="black",text="Classify",
                                  activebackground="#87CEEB",command=self.classify_text_func)
        self.classify_text.place(x=480,y=300,width=150,height=60)

        self.clear_text=Button(self.text_moderation,font=("times new roman",20,'bold'),bd=8,relief=RIDGE,bg="lightgreen",fg="black",text="Clear",
                                  activebackground="#87CEEB",command=self.clear_text_func)
        self.clear_text.place(x=480,y=390,width=150,height=60)

        self.image_label=Button(self.image_moderation,font=("times new roman",20,'bold'),bd=5,relief=GROOVE,bg="lightgreen",fg="black",text="Enter Your Image Path",activebackground="#87CEEB")
        self.image_label.place(x=180,y=20,width=300,height=60)
        
        self.path=StringVar()
        self.entry2=Entry(self.image_moderation,font=("times new roman",20,'bold'),relief=GROOVE,bd=5,textvariable=self.path)
        self.entry2.place(x=20,y=90,width=610,height=70)

        self.classify_img=Button(self.image_moderation,font=("times new roman",20,'bold'),bd=8,relief=RIDGE,bg="lightgreen",fg="black",text="Classify",
                                  activebackground="#87CEEB",command=self.classify_img)
        self.classify_img.place(x=480,y=300,width=150,height=60)

        self.clear_img=Button(self.image_moderation,font=("times new roman",20,'bold'),bd=8,relief=RIDGE,bg="lightgreen",fg="black",text="Clear",
                                  activebackground="#87CEEB",command=self.clear_img)
        self.clear_img.place(x=480,y=390,width=150,height=60)

    def clear_text_func(self):
        self.entry1.delete(1.0,END)
        self.label.destroy()

    def classify_text_func(self):

        if self.entry1.get(1.0,END) == " ":
            msg.showerror("Empty Error","Please Input Some Text")
        else:
             try:
                 text=str(self.entry1.get(1.0,END))
                 output,preds=bs.text_moderation(text)
                 
                 self.label=Text(self.text_moderation,font=("times new roman",15,'bold'),background="#87CEEB",fg="black",bd=8,relief=GROOVE)
                 final=f"Text : {text} \n {output}",
                 self.label.place(x=20,y=300,height=180,width=400)
                 self.label.insert(1.0,final)

             except TypeError:
                 msg.showerror("Wrong Input","Please Input String Value")       

    def classify_img(self):

        path=self.path.get()
        path=pathlib.Path(path)
        img=Image.open(str(path))
        img1=img.resize((300,300))
        self.photo_1=ImageTk.PhotoImage(img1)
        self.lb2=Label(self.image_moderation,image=self.photo_1)
        self.lb2.place(x=0,y=200,width=300,height=270)


        prediction=bs.image_moderation(str(path))
        
        self.label1=Text(self.image_moderation,font=("times new roman",20,'bold'),background="#87CEEB",fg="black",bd=8,relief=GROOVE)
        self.label1.place(x=320,y=170,height=70,width=310)
        self.label1.insert(1.0,prediction)


    def clear_img(self):
        self.entry2.delete(0,END)
        self.lb2.destroy()
        self.label1.destroy()



if __name__ == "__main__":
    root=Tk()
    ob=Main(root)
    root.mainloop()