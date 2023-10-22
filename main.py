# Author      : OMAR ALFAROUK ALMOHAMAD

import re
import time
import platform
import subprocess
from colorama import Fore, Style
import uuid
import netifaces
from getmac import get_mac_address


# control if ip is valid because sometimes next to the interface unwanted data
def control_ip(ip):
    pattern = (r"^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4]["
               r"0-9]|25[0-5])$")

    if re.match(pattern, ip):
        return True
    else:
        return False


# use netifaces to get getway local ip address
def get_gateway_ip(interface_name):
    try:
        gateway_ip = None
        gateways = netifaces.gateways()
        
        #loop for get entered interface and find ip address
        for gateway in gateways:
            if gateway == "default":
                if gateways[gateway][netifaces.AF_INET][1] == interface_name and control_ip(
                        gateways[gateway][netifaces.AF_INET][0]):
                    gateway_ip = gateways[gateway][netifaces.AF_INET][0]
                    break
                else:
                    continue
            elif gateway != "default":
                #control interface and ip address is match
                if gateways[gateway][0][1] == interface_name and control_ip(gateways[gateway][0][0]):
                    gateway_ip = gateways[gateway][0][0]
                    break
                else:
                    continue
            else:
                continue

        return gateway_ip

    except Exception as e:
        print(f'Error: {e}')
        return None


def find_mac_address(interface_name):
    try:
        if platform.system() == "Darwin" or platform.system() == "Linux":
            try:
                default_gateway_ip = get_gateway_ip(interface_name)
                if default_gateway_ip:
                    arp_result = subprocess.check_output(["arp", "-a"]).decode("utf-8")
                    lines = arp_result.splitlines()

                    for line in lines:
                        #search for ip in lines and get mac address
                        if default_gateway_ip in line:
                            parts = line.split()
                            mac_address = parts[3]
                            return mac_address
                return None
            except subprocess.CalledProcessError:
                return None

        elif platform.system() == "Windows":
            if interface_name == " " or interface_name is None:
                mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                return mac_address
            else:
                result = subprocess.check_output(["getmac"], universal_newlines=True)
                lines = result.split("\n")
                for line in lines:
                    if interface_name in line:
                        mac_address = line.split()[0]
                        return mac_address
        else:
            raise Exception("This operating system is not support.")
    except Exception as e:
        print(f"Error: {e}")
        return None


# this function is get mac address faster then arp requesting
def get_mac_address_alternative(interface):
    router_ip = get_gateway_ip(interface)
    mac_address = get_mac_address(interface, router_ip)
    return mac_address


changed = False
method_type = None

orjinal_mac = input("Please enter the MAC address(00:11:22:33:44:55):\n")

interface_name = input("Please enter the interface name (etc. en0)\nPress enter for wlan0:")
if interface_name == "":
    interface_name = "wlan0"
    

while method_type != '1' and method_type != '2':
    method_type = input("Please select a method of tracker\n1.Scan with arp\n2.Scan with get-mac lab. (Faster)\n")

print(f"\n\nCurrent MAC address: {orjinal_mac}")

while True:
    try:
        current_mac = None
        if method_type == '1':
            current_mac = find_mac_address(interface_name)
        elif method_type == '2':
            current_mac = get_mac_address_alternative(interface_name)

        if current_mac != orjinal_mac:
            if current_mac is not None:
                print(Fore.RED + f"MAC address has changed: {orjinal_mac} -> {current_mac}" + Style.RESET_ALL)
                changed = True
                time.sleep(5)

        if current_mac == orjinal_mac and changed is True:
            print(Fore.BLUE + f"The MAC address is back to the original: {orjinal_mac}" + Style.RESET_ALL)
            changed = False
            time.sleep(5)

    except KeyboardInterrupt:
        break

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
