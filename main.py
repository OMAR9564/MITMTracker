import re
import time
import scapy.all as scapy
import platform
import subprocess
from colorama import Fore, Style
import nmap
import uuid


def get_gateway_ip():
    try:
        output = subprocess.check_output(['netstat', '-s'], universal_newlines=True)

        for line in output.split('\n'):
            if 'default' in line:
                router_ip = line.split()[1]
                return router_ip

        return None
    except Exception as e:
        print(f'Hata oluştu: {e}')
        return None

def searchMacAddress(data):
    mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", data)
    if mac_address_search:
        return mac_address_search.group(0)
    return None

def findMacAddress(ipAddress, interfaceName):
    try:
        if platform.system() == "Darwin" or platform.system() == "Linux":
            result = subprocess.check_output(["ifconfig", interfaceName], universal_newlines=True)
            interfaces = re.findall(r"(\S+):", result)

            for interface in interfaces:
                if interfaceName in interface:
                    mac_address = searchMacAddress(result)
                    if mac_address:
                        return mac_address
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


orjinal_mac = input("Please enter the MAC address(00:11:22:33:44:55):\n")
print(f"Mevcut Wi-Fi MAC adresi: {orjinal_mac}")
changed = False
interfaceName = None
if platform.system() == "Darwin" or platform.system() == "Linux":
    interfaceName = input("Please enter the interface name (etc. en0)\nPress enter for wlan0:")
    if interfaceName == "":
        interfaceName = "wlan0"

while True:
    try:
        gateway_ip = get_gateway_ip()
        current_mac = findMacAddress(gateway_ip, interfaceName)

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
