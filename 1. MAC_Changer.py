#!/usr/bin/env python

import subprocess
import optparse
import re


def user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Input Interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Input MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Input Interface")
    elif not options.new_mac:
        parser.error("[-] Input MAC")
    return options


def change_mac(interface, new_mac):
    print("[+} Changing MAC address")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    mac_changer = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_res)
    if mac_changer:
        print(mac_changer.group(0))
    else:
        print("[-] MAC address not found")


options = user_input()
ifconfig_res = subprocess.check_output(["ifconfig", options.interface])
#print(ifconfig_res)
current_mac = get_current_mac(options.interface)
change_mac(options.interface, options.new_mac)
print(str(current_mac))
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Changed Successfully")
else:
    print("[-] MAC not changed")

