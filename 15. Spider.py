#!/usr/bin/env python

import re
import urlparse
import requests

targetURL = "http://10.0.2.14/mutillidae/"
targetList = []

def getResponse(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawl(targetURL):
    hreflink = getResponse(targetURL)
    for link in hreflink:
        link = urlparse.urljoin(targetURL, link)
        if "#" in link:
            link = link.split("#")[0]
        if targetURL in link and link not in targetList:
            targetList.append(link)
            print(link)
            crawl(link)

crawl(targetURL)
