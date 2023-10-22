# MITMTracker
**README.md**

## MAC Address Tracker

This is a simple Python script to track the MAC address of an interface. It can be used to detect MAC address spoofing attacks, or to simply monitor the MAC address of an interface over time.

## Usage

To use the script, first install the required Python packages:

```
pip install re netifaces getmac colorama
```

Then, run the script and enter the MAC address of the interface you want to track:

```
python mac_address_tracker.py
Please enter the MAC address(00:11:22:33:44:55): 00:11:22:33:44:55
Please enter the interface name (etc. en0)
Press enter for wlan0:
Please select a method of tracker
1.Scan with arp
2.Scan with get-mac lab. (Faster)
2
```

The script will then start tracking the MAC address of the interface. If the MAC address changes, the script will print a message to the console.

To stop tracking the MAC address, simply press `Ctrl`+`C`.

## Notes

* The script uses two different methods to track the MAC address of the interface:
    * **Method 1:** Uses the `arp` command to find the MAC address of the default gateway.
    * **Method 2:** Uses the `getmac` command to find the MAC address of the interface.

Method 2 is faster than method 1

## Example Output

```
Current MAC address: 00:11:22:33:44:55

MAC address has changed: 00:11:22:33:44:55 -> 00:22:33:44:55:66

The MAC address is back to the original: 00:11:22:33:44:55
```
