#!/usr/bin/env python
import argparse
import scapy.all as scapy

def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Input Target IP/IP Range")
    options = parser.parse_args()
    return options



def scan(ip):
    arp_scanner = scapy.ARP(pdst=ip)
    broadcaster = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_scanner_broadcaster = broadcaster/arp_scanner
    client_list = []
    for i in arp_scanner_broadcaster:
        client_dict = {"ip": i[0].psrc, "mac": i[0].hwsrc}
        client_list.append(client_dict)
        return client_list



def output(scan_result):
    print("IP \t\t\t MAC \n ------------------------------")
    for i in scan_result:
        print(i["ip"] + "\t\t" + i["mac"])


options = input_args()
scan_result = scan(options.target)
output(scan_result)
