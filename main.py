import re
import time
import scapy.all as scapy
import platform
import subprocess
from colorama import Fore, Style
import nmap
import uuid
import socket
import netifaces
from getmac import get_mac_address


def get_gateway_ip():
    try:
        gateway_ip = None
        gateways = netifaces.gateways()
        if 'default' in gateways:
            gateway_ip = gateways['default'][netifaces.AF_INET][0]
        return gateway_ip

    except Exception as e:
        print(f'Hata oluştu: {e}')
        return None


def searchMacAddress(data):
    mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", data)
    if mac_address_search:
        return mac_address_search.group(0)
    return None


def findMacAddress(interfaceName):
    try:
        if platform.system() == "Darwin" or platform.system() == "Linux":
            try:
                default_gateway_ip = get_gateway_ip()
                if default_gateway_ip:
                    arp_result = subprocess.check_output(["arp", "-a"]).decode("utf-8")
                    lines = arp_result.splitlines()

                    for line in lines:
                        if default_gateway_ip in line:
                            parts = line.split()
                            mac_address = parts[3]
                            return mac_address
                return None
            except subprocess.CalledProcessError:
                return None

        elif platform.system() == "Windows":
            if interfaceName == " " or interfaceName is None:
                mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                return mac_address
            else:
                result = subprocess.check_output(["getmac"], universal_newlines=True)
                lines = result.split("\n")
                for line in lines:
                    if interfaceName in line:
                        mac_address = line.split()[0]
                        return mac_address
        else:
            raise Exception("Bu işletim sistemi desteklenmiyor.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None


def getMacAddressAlternative(interface):
    routerIp = get_gateway_ip()
    macAddress = get_mac_address(interface, routerIp)
    return macAddress


orjinal_mac = input("Please enter the MAC address(00:11:22:33:44:55):\n")
changed = False
interfaceName = None
if platform.system() == "Darwin" or platform.system() == "Linux":
    interfaceName = input("Please enter the interface name (etc. en0)\nPress enter for wlan0:")
    if interfaceName == "":
        interfaceName = "wlan0"

trackerType = None
while trackerType != '1' and trackerType != '2':
    trackerType = input("Please select a method of tracker\n1.Scan with arp\n2.Scan with get-mac lab.\n")

print(f"\n\nMevcut Wi-Fi MAC adresi: {orjinal_mac}")

while True:
    try:
        current_mac = None
        if trackerType == '1':
            current_mac = findMacAddress(interfaceName)
        elif trackerType == '2':
            current_mac = getMacAddressAlternative(interfaceName)

        if current_mac != orjinal_mac:
            if current_mac is not None:
                print(Fore.RED + f"Wi-Fi MAC adresi değişti: {orjinal_mac} -> {current_mac}" + Style.RESET_ALL)
                changed = True
                time.sleep(5)

        if current_mac == orjinal_mac and changed is True:
            print(Fore.BLUE + f"MAC adresi orjinale gecti: {orjinal_mac}" + Style.RESET_ALL)
            changed = False
            time.sleep(5)

    except KeyboardInterrupt:
        break

    except Exception as e:
        print(f"Hata oluştu: {e}")
        time.sleep(5)
