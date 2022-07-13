#Credits to david for 50% of all this mess

# Script to send email with optional 
# attachments using gmail
#
import os
import re
import smtplib
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from textwrap import dedent
from typing import List
from tkinter import *
from tkinter import filedialog
import getpass
import socket
import pathlib
import requests
import json

def send_mail(
    send_from:str, send_to:str,
    username:str, password:str,
    subject:str, message:str, files:List[str],
    server:str="smtp.gmail.com", port:int=587, use_tls=True
):
    global spacing
    spacing.configure(text="Mail has been sent")

    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)
    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
        exit()
    data = response.json()
    
    "Compose and send email with provided info and attachments."
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(message + "\n"  + str(getpass.getuser()) + "\n" + str(data['ip'])))
    ##############################################################################################
    #here you can remove the IP and other things if you like, its just there because i don't want#
    #any ignorant person to abuse it, tho it still can happen pretty easely                      #
    #since it happened before                                                                    #
    ##############################################################################################
    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
          'Content-Disposition',
          'attachment; filename={}'.format(pathlib.Path(path).name))
        msg.attach(part)
    try:
      smtp = smtplib.SMTP('smtp.gmail.com', port)
      smtp.ehlo()
      if use_tls: smtp.starttls()
      smtp.login(username, password)
    except smtplib.SMTPAuthenticationError as err:
      code = err.args[0]
      subcode = ""
      mesg = err.args[1].decode("utf-8")
      ERR_REGEX = re.compile(
          r"(^|\n)(?P<subcode>\d(?:\.\d+)*)\s+", re.DOTALL
      )
      m = ERR_REGEX.search(mesg)
      if m:
          subcode = m.group("subcode")
          mesg = ERR_REGEX.sub("\\1", mesg)
      print("\x1b[1;41;37m", end="")
      print(f"Error code {code} - server rejected authentication", end="")
      print("\x1b[0;1;31m")
      print(mesg, end="")
      print("\x1b[0m")
      if code == 534 and subcode == "5.7.9":
          print(dedent("""
          NOTE: Steps to generate app-specific password
            • Log in to your Google account
            • Go to My Account > Sign-in & Security > App Passwords
            • Scroll down to Select App (in the Password & sign-in method box)
            • Choose 'Other (custom name)'
            • Give this app password a name, e.g. "mymailer"
            • Choose Generate
            • Copy the long generated password and paste it into your script."""
          ))
      return err
    result = smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    
    return result

################################################################################

def makeInterface():
    global allFiles
    global spacing
    allFiles = []
    window = Tk()
    space = Label(window, height = 3, width = 5)
    space.grid(row = 0, column = 0)
    WrittenText = Label(window, text = "Subject:")
    WrittenText.grid(row = 1, column = 1)
    Subject = Entry(window)
    Subject.grid(row = 1, column = 2)
    WrittenTextTwo = Label(window, text = "Content:")
    WrittenTextTwo.grid(row = 2, column = 1)
    Mailcontent = Text(window, bg = "Grey", fg = "White", font=("calibri", 20), height = 12, width = 50)
    Mailcontent.grid(row = 2, column = 2)
    spacing = Label(window, height = 3)
    spacing.grid(row = 3, column = 2)
    appendFiles = Button(window, text="Add files", command=openSelector, width = 50, height = 3, bg = "Blue")
    appendFiles.grid(row = 4, column = 2)
    sendButton = Button(window, text="Send mail", height = 5, width = 100, bg="Green", command=lambda Subject = Subject,
                        Mailcontent = Mailcontent:
                        sendMail(Subject.get(), Mailcontent.get("1.0", "end-1c")))
    sendButton.grid(row = 5, column = 1, columnspan = 2)
    window.title("Mail sender")
    window.geometry("800x700")
    window.mainloop()

def openSelector():
    global allFiles
    global spacing
    allFilesShown = ""
    FilePathOne = filedialog.askopenfilename(title="Select a file", filetypes=(("text files","*.txt"), ("all files","*.*")))
    pathHere = os.getcwd()
    shutil.copy(FilePathOne, pathHere)
    allFiles.append(FilePathOne.split("\\")[-1])
    for everyFile in allFiles:
        allFilesShown += everyFile + "\n"
    spacing.configure(text=allFilesShown)

def sendMail(Messsubject, Messmessage):
    global allFiles
    send_mail(
    "thepascalfromnowhere@gmail.com",  # your gmail address
    "issuepascal@gmail.com",  # Target
    username='thepascalfromnowhere@gmail.com',
    password='uxscdawtbdpklblc',
    subject=Messsubject,
    message=Messmessage,
    files=allFiles)

    allFiles = []
   

makeInterface()





#Credits to david for 50% of all this mess





    
