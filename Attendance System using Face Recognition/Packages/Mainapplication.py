#Imporrting necessory libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
import mysql.connector as mc
import json
import cv2
import numpy as np
from registeration import Registeration
from PIL import Image,ImageTk
import datetime
from time import strftime
import os
import smtplib
from smtplib import SMTPServerDisconnected
from attend import process_attendance
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import pathlib
import face_recognition

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''MAIN CLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Define a Main Class
class MainApplication:
    #Define a main Constructor
    def __init__(self,root):
        ''' Main Application'''
        self.root=root
        self.root.title("ATTENDANCE MANAGEMENT SYSTEM USING FACE RECOGNITION")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(0,0)
        ''' Main Application'''
        
        ##MainFrame
        self.main_frame=Frame(self.root,bg="lightgray")
        self.main_frame.pack(fill=BOTH,expand=True)
        
        ##AttendenceFrame
        self.attendence_frame=Frame(self.main_frame,relief=RIDGE,bd=4,background="white")
        self.attendence_frame.place(x=850,y=130,width=400,height=500)
        
        #FaceIcon
        img=Image.open("D:\\Student_Attendance_System_using_face_recognition\\UIimages\\face-scan.png")
        img=img.resize((100,100))
        self.photo_image=ImageTk.PhotoImage(img)
        lbl_img1=Label(self.main_frame,image=self.photo_image)
        lbl_img1.place(x=1000,y=90)
        
        #ItsoleraIcon
        img1=Image.open("D:\\Student_Attendance_System_using_face_recognition\\UIimages\\ki.jpg")
        img1=img1.resize((200,200))
        self.photo_image1=ImageTk.PhotoImage(img1)
        lbl_img2=Label(self.main_frame,image=self.photo_image1)
        lbl_img2.place(x=20,y=20,width=200,height=70)

        #MainLabel
        self.label=Label(self.main_frame,text="Attendance Management System\nUsing Face Recognition !",background="lightgray",font=("calibri",30,'bold'))
        self.label.place(x=70,y=130)
        
        #Define a timeStamp
        self.time_label = Label(self.main_frame, font=('calibri', 30, 'bold'), background='lightgray', foreground='black')
        self.time_label.pack(anchor='center')
        self.update_time()
        
        #Define a Database Frame
        self.dt_frame=Frame(self.main_frame,bd=4,relief=RIDGE,bg="white")
        self.dt_frame.place(x=70,y=280,width=600,height=350)
        
        ''''''''''''''''''''''''''''''''''''''''''' Scrollbar'''''''''''''''''''''''''''''''''''''''''''''''''
        #Attach a Y scroll bar to frame
        scroll_y=ttk.Scrollbar(self.dt_frame,orient=VERTICAL)

        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=45,
                             fieldbackground="white")
        self.style.map('Treeview',
                       background=[('selected','lightgreen')],
                       foreground=[('selected','black')],
                       )
        #Treeview to access dataframe
        self.tr_view=ttk.Treeview(self.dt_frame,columns=(
                                                          "ID",
                                                          "student Name",
                                                          "Time",
                                                          "Date",
                                                          "Marked"
        ),yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.tr_view.yview)
        
        #SHOW HEADINGS
        self.tr_view.heading("ID",text="Student ID")
        self.tr_view.heading("student Name",text="Student Name")
        self.tr_view.heading("Date",text="Date")
        self.tr_view.heading("Time",text="Time")
        self.tr_view.heading("Marked",text="Marked")
        
        #SET COLUMNS WIDTH
        self.tr_view['show']='headings'
        self.tr_view.column("Marked",width=50,anchor="center")
        self.tr_view.column("ID",width=50,anchor="center")
        self.tr_view.column("Date",width=50,anchor="center")
        self.tr_view.column("Time",width=50,anchor="center")
        self.tr_view.column("student Name",width=50,anchor="center")
        self.tr_view.pack(fill=BOTH,expand=True)
        self.fetch_from_database()

        ##Buttons for different functioality

        #Button for attendance start
        self.Start_attendance=Button(self.attendence_frame,text="Start Attendance",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.attendance)
        self.Start_attendance.place(x=75,y=230,width=250,height=50)
        
        #Button for registeration
        self.Register_bnt=Button(self.attendence_frame,text="Register New Student",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.register_func)
        self.Register_bnt.place(x=75,y=130,width=250,height=50)

        #BUtton for final report generation
        self.report=Button(self.attendence_frame,text="Final Report",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.final_report_func)
        self.report.place(x=75,y=330,width=250,height=50)
        
    ''''''''''''''''''''''''''''''''''''''''''' Functionality'''''''''''''''''''''''''''''''''''''''''''''''''
    #Fetching data from database
    def fetch_from_database(self):

        try:
            #Make a connection to centralized database
            connecton=mc.connect(host="localhost",username="root",password="Arham1234@",database="centralized_hub")
            #Cursor to execute queries of Sql
            cursor=connecton.cursor()
            #Fetching all the data from attendance frame
            cursor.execute("select ID,student_name,time,date,marked from attendance")
            rows=cursor.fetchall()
            #Insering the data into tree view
            if len(rows)!=0:
                self.tr_view.delete(*self.tr_view.get_children())
                for i in rows:
                    self.tr_view.insert("",END,values=i)
                #Connection commit
                connecton.commit()
            #Connection close    
            connecton.close()
        except Exception as e:
            ms.showerror("Error",{e})

    def update_time(self):
        time_string = strftime('%H:%M:%S %p')  # Format: Hours:Minutes:Seconds AM/PM
    # Update the label with the current time
        self.time_label.config(text=time_string)
    # Call this function again after 1000 milliseconds (1 second)
        self.time_label.after(1000, self.update_time)
    
    #Register Function to call a new class
    def register_func(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)
    
    #Final Report function to call final report window
    def final_report_func(self):
        self.new_window=Toplevel(self.root)
        self.app=FinalReport(self.new_window)
    
    #Calling process attendance from attend Package
    def attendance(self):
        process_attendance()
        self.fetch_from_database()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''MAIN CLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''REGISTERCLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1200x600+80+50")
        self.root.resizable(0,0)

        self.bg=Image.open("D:\\Student_Attendance_System_using_face_recognition\\UIimages\\it2.jpg")
        self.bg=self.bg.resize((1200,600))
        self.phto_img=ImageTk.PhotoImage(self.bg)
        labl1=Label(self.root,image=self.phto_img)
        labl1.place(x=0,y=0,relheight=1,relwidth=1)

        ##AttendenceFrame
        self.register_frame=Frame(self.root,relief=RIDGE,bd=4,background="white")
        self.register_frame.place(x=50,y=30,width=400,height=540)

        self.bg2=Image.open("D:\\Student_Attendance_System_using_face_recognition\\UIimages\\register.jpg")
        self.bg2=self.bg2.resize((50,50))
        self.phto_img2=ImageTk.PhotoImage(self.bg2)
        labl1=Label(self.register_frame,image=self.phto_img2)
        labl1.place(x=170,y=30)

        self.label(self.register_frame,20,100,"Student Id")
        self.id=StringVar()
        self.st_id=Entry(self.register_frame,textvariable=self.id,bd=4,relief=RIDGE)
        self.st_id.place(x=20,y=120,width=300,height=30)

        self.label(self.register_frame,20,160,"Student Name")
        self.name=StringVar()
        self.st_name=Entry(self.register_frame,textvariable=self.name,bd=4,relief=RIDGE)
        self.st_name.place(x=20,y=180,width=300,height=30)

        self.label(self.register_frame,20,220,"Email")
        self.email=StringVar()
        self.st_email=Entry(self.register_frame,textvariable=self.email,bd=4,relief=RIDGE)
        self.st_email.place(x=20,y=240,width=300,height=30)

        self.label(self.register_frame,20,280,"Contact")
        self.contact=StringVar()
        self.st_contact=Entry(self.register_frame,textvariable=self.contact,bd=4,relief=RIDGE)
        self.st_contact.place(x=20,y=300,width=300,height=30)

        self.label(self.register_frame,20,340,"Department")
        self.department=StringVar()
        self.st_dep=Entry(self.register_frame,textvariable=self.department,bd=4,relief=RIDGE)
        self.st_dep.place(x=20,y=360,width=300,height=30)

         #Define a Database Frame
        self.dt_frame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        self.dt_frame1.place(x=465,y=30,width=700,height=540)
        
        ''''''''''''''''''''''''''''''''''''''''''' Scrollbar'''''''''''''''''''''''''''''''''''''''''''''''''
        #Attach a Y scroll bar to frame
        scroll_y1=ttk.Scrollbar(self.dt_frame1,orient=VERTICAL)

        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=45,
                             fieldbackground="white")
        self.style.map('Treeview',
                       background=[('selected','lightgreen')])
        #Treeview to access dataframe
        self.tr_view1=ttk.Treeview(self.dt_frame1,columns=(
                                                          "ID",
                                                          "student Name",
                                                          "Contact",
                                                          "Email",
                                                          "Department"
        ),yscrollcommand=scroll_y1.set)
        scroll_y1.pack(side=RIGHT,fill=Y)
        scroll_y1.config(command=self.tr_view1.yview)

        self.tr_view1.heading("ID",text="Student ID")
        self.tr_view1.heading("student Name",text="Student Name")
        self.tr_view1.heading("Contact",text="Contact")
        self.tr_view1.heading("Email",text="Email")
        self.tr_view1.heading("Department",text="Department")

        self.tr_view1['show']='headings'
        self.tr_view1.column("Contact",width=100,anchor="center")
        self.tr_view1.column("ID",width=50,anchor="center")
        self.tr_view1.column("Email",width=100,anchor="center")
        self.tr_view1.column("Department",width=100,anchor="center")
        self.tr_view1.column("student Name",width=100,anchor="center")
        self.tr_view1.pack(fill=BOTH,expand=True)
        self.fetch_from_database1()

        self.insertion=Button(self.register_frame,text="Insert",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.insert)
        self.insertion.place(x=20,y=400,width=150,height=50)
        self.click_picture=Button(self.register_frame,text="Take Picture",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.take_picture)
        self.click_picture.place(x=180,y=400,width=150,height=50)
        self.click_picture.config(state=DISABLED)
        self.clear_field=Button(self.register_frame,text="Clear",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.clear)
        self.clear_field.place(x=20,y=460,width=150,height=50)
        self.delete_record=Button(self.register_frame,text="Delete",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.delete)
        self.delete_record.place(x=180,y=460,width=150,height=50)
        self.tr_view1.bind("<ButtonRelease-1>",self.get_cursor)
    def btn(self,text,frame,x,y,command):
        button=Button(frame,text=text,bd=5,relief=RIDGE,bg="cyan",fg="black",command=command)
        button.place(x=x,y=y,width=150,height=50)

    def label(self,frame,x,y,text):
        label=Label(frame,text=text,background="white")
        label.place(x=x,y=y)

    def entry(self,frame,x,y,type):
        var=IntVar if type=='int' else StringVar
        entry=Entry(frame,textvariable=var,bd=4,relief=RIDGE)
        entry.place(x=x,y=y,width=300,height=30)
        return var
    
    def clear(self):
        self.st_contact.config(state=NORMAL)
        self.st_id.config(state=NORMAL)
        self.st_email.config(state=NORMAL)
        self.st_name.config(state=NORMAL)
        self.st_dep.config(state=NORMAL)
        self.insertion.config(state=NORMAL)
        self.delete_record.config(state=NORMAL)
        self.st_email.delete(0,END)
        self.st_contact.delete(0,END)
        self.st_dep.delete(0,END)
        self.st_id.delete(0,END)
        self.st_name.delete(0,END)

    def fetch_from_database1(self):
        try:
          #Make a connection to centralized database
          connecton=mc.connect(host="localhost",username="root",password="Arham1234@",database="centralized_hub")
          #Cursor to execute queries of Sql
          cursor=connecton.cursor()
          #Fetching all the data from attendance frame
          cursor.execute("select ID,name,PHONE,Email,dep_name from student_info")
          rows=cursor.fetchall()
          #Insering the data into tree view
          if len(rows)!=0:
            self.tr_view1.delete(*self.tr_view1.get_children())
            for i in rows:
                self.tr_view1.insert("",END,values=i)
            #Connection commit
            connecton.commit()
        #Connection close    
          connecton.close()
        except Exception as e:
            ms.showerror("Error","Connection Interrupt")

    def take_picture(self):
        id=self.id.get()
        name=self.name.get()
        Registeration(name,str(id))
        self.insertion.config(state=NORMAL)
        self.delete_record.config(state=NORMAL)
        self.clear_field.config(state=NORMAL)
        self.click_picture.config(state=DISABLED)
        self.clear()
        
    def insert(self):
        if self.id.get() == "" or self.name.get()=="" or self.department.get()=="" or self.contact.get()=="" or self.email.get()=="":
            ms.showerror("Empty Error","All fields are required")
            self.clear()
        else:
            try:
                float(self.id.get())
                id=self.id.get()
                name=self.name.get()
                contact=self.contact.get()
                email=self.email.get()
                department=self.department.get()
                try:
                     #Make a connection to centralized database
                     connecton=mc.connect(host="localhost",username="root",password="Arham1234@",database="centralized_hub")
                     #Cursor to execute queries of Sql
                     cursor=connecton.cursor()
                     cursor.execute("insert into student_info values(%s,%s,%s,%s,%s)",(
                                                                                        id,
                                                                                        name,
                                                                                        contact,
                                                                                        email,
                                                                                        department
                     ))
                     connecton.commit()
                     connecton.close()
                     self.fetch_from_database1()
                     server = smtplib.SMTP('smtp.gmail.com', 587)
                     subject="Student Registered Successfully"
                     message=f"{name} is successfully registered in our database with corresponding ID:{id}\n\nID:{id}\nName:{name}\nEmail:{email}\nContact:{contact}\nDepartment:{department}"
                     text=f"Subject:{subject}\n\n{message}"
                     
                    #Passing Through all the security layers
                     server.starttls()
                    #LOgin into my account , the second parameter is the pass key which is different for each account
                     server.login("ak06598909@gmail.com","wykn uaph kpju cmbu")
                           #Send a email to reciever mail
                     server.sendmail("ak065989092Gmail.com",email,text )
    
                     server.quit() 
                     self.insertion.config(state=DISABLED)
                     self.delete_record.config(state=DISABLED)
                     self.clear_field.config(state=DISABLED)
                     self.click_picture.config(state=NORMAL)

                except Exception as e:
                    ms.showerror("Duplicate Id","Try different Id")
                    self.insertion.config(state=NORMAL)
                    self.delete_record.config(state=NORMAL)
                    self.clear_field.config(state=NORMAL)
                    self.click_picture.config(state=DISABLED)
                    self.clear()
            except ValueError:
                ms.showerror("Wrong type","Please Input Integer value in ID",)
            
    def delete(self):
        self.st_id.config(state="normal")
        self.st_name.config(state="normal")
        if self.id.get()=="" or self.name.get()=='':
            ms.showerror("Empty","Please input id and name")
        else:
            try:
                id=self.id.get()
                name=self.name.get()
            
                connecton=mc.connect(host="localhost",username="root",password="Arham1234@",database="centralized_hub")
                #Cursor to execute queries of Sql
                cursor=connecton.cursor()
                cursor.execute("delete from student_info where ID=%s",(id,))
                cursor.execute("delete from attendance where ID=%s",(id,))
                connecton.commit()
                connecton.close()
                self.fetch_from_database1()
                self.clear()
                image_path=f"D:\\Student_Attendance_System_using_face_recognition\\images\\{id}.jpg"
                path="D:\\Student_Attendance_System_using_face_recognition\\JsonData\\member_ids.json"
                data_dic={}
                with open(path, 'r') as f:
                   data_dic = json.load(f)
                data_dic.pop(str(id))
                with open(path, 'w') as f:
                    json.dump(data_dic, f)
                os.remove(image_path)
                # ms.showinfo("Deleted",f"The data corresponds to {name} and id :{id} is deleted successfully")
            except Exception as e:
                ms.showerror("Error Encounter",e)  

        
        

    def get_cursor(self,event=""):
        cursor_row=self.tr_view1.focus()
        content=self.tr_view1.item(cursor_row)
        row=content['values']

        self.id.set(row[0])
        self.name.set(row[1])
        self.contact.set(row[2])
        self.email.set(row[3])
        self.department.set(row[4])

        self.st_contact.config(state="disabled")
        self.st_id.config(state="disabled")
        self.st_email.config(state="disabled")
        self.st_name.config(state="disabled")
        self.st_dep.config(state="disabled")
        self.insertion.config(state=DISABLED)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''REGISTERCLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''FINALCLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class FinalReport:

    def __init__(self,root):
        
        self.db = mc.connect(
           host="localhost",
           user="root",  # Replace with your MySQL username
           password="Arham1234@",  # Replace with your MySQL password
           database="centralized_hub"
           )
        
        self.cursor = self.db.cursor()
        self.root=root
        self.root.title("Final Report Of Student")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(0,0)

        self.main_frame=Frame(self.root,bg="lightgray")
        self.main_frame.pack(fill=BOTH,expand=True)

        self.credentials_frame=Frame(self.main_frame,relief=RIDGE,bd=4,background="white")
        self.credentials_frame.place(x=50,y=60,width=400,height=540)
        
        self.bg=Image.open("D:\\Student_Attendance_System_using_face_recognition\\UIimages\\report.jpg")
        self.bg=self.bg.resize((120,120))
        self.phto_img=ImageTk.PhotoImage(self.bg)
        labl1=Label(self.main_frame,image=self.phto_img)
        labl1.place(x=190,y=80)

        label=Label(self.credentials_frame,text="Student ID",background="white")
        label.place(x=20,y=170)

        self.ID=IntVar()
        self.st_id=Entry(self.credentials_frame,textvariable=self.ID,bd=4,relief=RIDGE)
        self.st_id.place(x=20,y=190,width=300,height=30)

        self.generate_report1=Button(self.credentials_frame,text="Generate Report",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.generate_report)
        self.generate_report1.place(x=20,y=250,width=250,height=50)

        self.Mail=Button(self.credentials_frame,text="Mail",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.mail)
        self.Mail.place(x=20,y=350,width=250,height=50)
        self.Mail.config(state=DISABLED)

        self.Clear=Button(self.credentials_frame,text="Clear",bd=5,relief=RIDGE,bg="cyan",fg="black",command=self.clear)
        self.Clear.place(x=20,y=450,width=250,height=50)
        print()
       
    def student_present_count(self,student_id):
          self.cursor.execute("SELECT count(*) FROM attendance where ID=%s",(student_id,))
          return self.cursor.fetchone()
    
    def total_days_institute_open(self):
         self.cursor.execute("SELECT DATEDIFF(MAX(DATE),MIN(DATE)) FROM attendance")
         return self.cursor.fetchone()
    
    def fetch_student_data_from_base(self,student_id):
        self.cursor.execute("Select * from student_info where ID = %s ",(student_id,))
        return self.cursor.fetchone()
    
    def fetch_student_attendance_data(self,student_id):
        self.cursor.execute("select * from attendance where ID = %s",(student_id,))
        return self.cursor.fetchall()

    def calculate_attendance(self,attendance_data,student_data):
        total_days = attendance_data
        present_days = student_data

        percentage = (present_days / total_days) * 100 if total_days else 0
        return percentage,total_days,present_days

        
    def generate_report(self):
        if self.ID.get()=="":
            ms.showerror("Empty","All fields are required")
            self.st_id.delete(0,END) 
        else: 
            try:
               float(self.ID.get())          
               self.student_data_from_main = self.fetch_student_data_from_base((self.ID.get()))
               if not self.student_data_from_main:
                  ms.showerror("Error", "User is not found")
                  return
               self.student_present_days= self.student_present_count(self.ID.get())
               self.total_day=self.total_days_institute_open()
               self.total_day=self.total_day[0]+1
               self.student_attendance_data=self.fetch_student_attendance_data(self.ID.get())

               if not self.student_attendance_data:
                  ms.showerror("Error", "No attendance data found for this student")
                  return
               self.percentage ,self.total_day,self.present_days= self.calculate_attendance(self.total_day,self.student_present_days[0])

               self.id=self.student_data_from_main[0]
               self.name=self.student_data_from_main[1]
               self.contact=self.student_data_from_main[2]
               self.email=self.student_data_from_main[3]
               self.department=self.student_data_from_main[4]

               self.final_frame=Frame(self.main_frame,bd=4,relief=RIDGE,bg="white")
               self.final_frame.place(x=500,y=60,width=700,height=540)

               self.final_label=Label(self.final_frame,text="Attendance Report",font=("calibri",40,'bold'),bd=5,relief=GROOVE,bg="lightgreen",fg="black")
               self.final_label.pack(side=TOP,fill=X)
               
               self.final_report=Text(self.final_frame,bd=4,relief=RIDGE,bg="white",font=("calibri",15,'bold'))
               self.final_report.place(x=5,y=80,width=680,height=450)

               self.text=f"STUDENT ID :  {self.id}\nSTUDENT NAME :  {self.name}\nSTUDENT CONTACT :  {self.contact}\nSTUDENT EMAIL :  {self.email}\nSTUDENT DEPARTMENT :  {self.department}\n\nTOTAL DAYS INSTITUTE OPEN : {self.total_day}\nSTUDENT PRESENT DAYS : {self.present_days} \nATTENDANCE PERCENTAGE : {self.percentage}"
               self.final_report.insert(1.0,self.text)

               for record in self.student_attendance_data:
                   self.final_report.insert("end-1c",f"\n\nDate: {record[2]}, Time: {record[1]}, Marked: {record[3]}")
               self.generate_report1.config(state=DISABLED)
               self.Mail.config(state=NORMAL)
               
            except Exception as e:
                ms.showerror("Exception",f"{e}")

    def mail(self):
        self.mail_data=self.final_report.get(1.0,END)
        self.subject = "ATTENDANCE REPORT"
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'ak06598909@gmail.com'
        try:
            msg = MIMEMultipart()
            msg['From'] = formataddr(('Attendance System', smtp_user))
            msg['To'] = self.email  # Email of the student
            msg['Subject'] = self.subject

            msg.attach(MIMEText(self.mail_data, 'plain'))
                                    
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, "wykn uaph kpju cmbu")
                server.send_message(msg)
                self.Mail.config(state=DISABLED)
                self.clear()
            print(f"Attendance email sent to {self.email}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")

    def clear(self):
        self.st_id.delete(0,END)
        self.generate_report1.config(state=NORMAL)
        self.Mail.config(state=DISABLED)
        self.final_frame.destroy()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''FINALCLASS'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



if __name__ == "__main__":
    root=Tk()
    obj=MainApplication(root)
    root.mainloop()
    
