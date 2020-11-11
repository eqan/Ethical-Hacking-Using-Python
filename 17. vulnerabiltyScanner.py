#!/usr/bin/env python

import requests
import re
import urlparse
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignoreLink):
        self.session = requests.Session()
        self.targetURL = url
        self.targetLinks = []
        self.ignoreLinks = ignoreLink

    def extractLinks(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawl(self, url= None):
        if url == None:
            url = self.targetURL
        hrefLinks = self.extractLinks(url)
        for link in hrefLinks:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.targetURL in link and link not in self.targetLinks and link not in self.ignoreLinks:
                self.targetLinks.append(link)
                print(link)
                self.crawl(link)

    def extractForm(self, url):
        response = self.session.get(url)
        parsedHTML = BeautifulSoup(response.content, features="html.parser" )
        return parsedHTML.findAll("form")

    def submitForm(self, form, value, url):
        action = form.get("action")
        postURL = urlparse.urljoin(url, action)
        method = form.get("method")
        inputList = form.findAll("input")
        postData = {}
        for input in inputList:
            inputName = input.get("name")
            inputType = input.get("type")
            inputValue  = input.get("value")
            if inputType == "text":
                inputValue = value
            postData[inputName] = inputValue
        if method == "post":
            return requests.post(postURL, data=postData)
        return self.session.get(postURL, params=postData)

    def runScanner(self):
        for link in self.targetLinks:
            forms = self.extractForm(link)
            for form in forms:
                print("[+] Testing form in " + link)
                isVulnerableToXSS = self.testXSSinForm(form, link)
                if isVulnerableToXSS:
                    print("\n\n[+++] XSS discovered in" + link + " in the following form")
                    print(form)

            if "=" in link:
                print("[+] Testing" + link)
                isVulnerableToXSS = self.testXSSinLink(link)
                if isVulnerableToXSS:
                    print("[***] XSS discovered in" + link)

    def testXSSinForm(self, form, url):
        xssTestScript = "<sCript>alert('test')</scriPt>"
        response = self.submitForm(form, xssTestScript, url)
        return xssTestScript in response.content
            #return True
    def testXSSinLink(self, url):
        xssTestScript = "<sCript>alert('test')</scRipt>"
        url = url.replace("=", "=" + xssTestScript)
        response = self.session.get(url)
        return xssTestScript  in response.content
            #return True

targetURL = "http://10.0.2.14/dvwa/"
ignoreLink = "http://10.0.2.14/dvwa/logout.php"
dataDict = {"username": "admin", "password": "password", "Login": "submit"}
vulnerability = Scanner.Scanner(targetURL, ignoreLink)
vulnerability.session.post("http://10.0.2.14/dvwa/login.php", data=dataDict)
vulnerability.crawl()
vulnerability.runScanner()
