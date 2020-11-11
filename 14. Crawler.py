#!/usr/bin/env python

import requests

targetURL = "http://10.0.2.14/mutillidae"

def getResponse(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

with open("/home/kali/Downloads/wordlist.txt", "r") as wordList:
    for line in wordList:
        word = line.strip()
        url = targetURL + "/" + word
        response = getResponse(url)
        if response:
            print("[+]Discovered subdomain -->" + str(url))
