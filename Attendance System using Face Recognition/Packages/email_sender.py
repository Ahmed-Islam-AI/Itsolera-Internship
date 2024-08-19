#Importing SMTPLIB TO Generate Email
import smtplib
from smtplib import SMTPServerDisconnected

#Taking Input parameters
sender_email=input("Please Input Sender Email :\n")
reciever_email=input("Please Input Reciever Email :\n")
subject=input("PLease Enter Subject\n")
message=input("PLease Enter Mail\n")
text=f"Subject:{subject}\n\n{message}"
pass_key=input("PLease Enter Your Pass Ky")
#Starting a SMTPLIB server
server = smtplib.SMTP('smtp.gmail.com', 587)
try:
      #Passing Through all the security layers
      server.starttls()
      #LOgin into my account , the second parameter is the pass key which is different for each account
      server.login(sender_email,"wykn uaph kpju cmbu")
      #Send a email to reciever mail
      server.sendmail(sender_email,reciever_email, text)
      print("Successfully Sent")
except SMTPServerDisconnected as e:
      print(f"Error: {e}")
finally:
      server.quit() 



