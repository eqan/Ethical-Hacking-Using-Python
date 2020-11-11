#!/usr/bin/env python
import scapy.all as scapy
import time

def getMAC(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    answered = scapy.srp(arp_r_b, verbose=False, timeout=1)[0]
    return answered[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process)

def process(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        real_mac = getMAC(packet[scapy.ARP].psrc)
        response_mac = getMAC(packet[scapy.ARP].hwsrc)
        try:
            if real_mac != response_mac:
                print("[+] You are under attack")
        except IndexError:
            pass

sniff("eth0")
