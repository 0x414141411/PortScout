import pyfiglet
import sys
import socket
import os
import time
import shlex
import threading
import psutil
from colorama import Fore, Back, Style
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

ascii_banner = pyfiglet.figlet_format("PORTSCOUT")
print(ascii_banner)
print("© 2024 PORTSCOUT")

if "--help" in sys.argv:
    print("Usage: python3 portscout.py <target>")
    print("Additional options:")
    print("Version (-v) - To perform version scan")
    print("Port (-p) - To specify the range for scan, default is 1-1024")
    print("Specific ports (-ps) - To specify specific ports for scanning, e.g., 80,443,8080")
    sys.exit()

version_scan = "-v" in sys.argv
port_scan = "-p" in sys.argv
specific_ports_scan = "-ps" in sys.argv
target = None
port_range = (1, 1024)
specific_ports = []

for arg in sys.argv[1:]:
    if arg.startswith("-"):
        if arg == "--target":
            target = sys.argv[sys.argv.index(arg) + 1]
        elif arg in ("-p"):
            try:
                port_range = tuple(map(int, sys.argv[sys.argv.index(arg) + 1].split("-")))
            except (ValueError, IndexError):
                print("Please give a valid port range")
                sys.exit()
        elif arg in ("-ps"):
            try:
                specific_ports = list(map(int, sys.argv[sys.argv.index(arg) + 1].split(",")))
            except (ValueError, IndexError):
                print("Please give a valid list of ports")
                sys.exit()
    else:
        target = arg

if target is None:
    print("Target is not specified, see --help")
    sys.exit()

print(f"Scanning Target: {target}")
if specific_ports:
    print(f"Specific Ports: {specific_ports}")
else:
    print(f"Port Range: {port_range[0]}-{port_range[1]}")
print(f"Scanning started at: {datetime.now()}")

open_ports = []

def scan_port(port, target):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                if version_scan:
                    try:
                        s.send(b'HEAD / HTTP/1.1\r\n\r\n')
                        banner = s.recv(1024).decode(errors='ignore').strip()
                        if banner:
                            print(f"Port {port}: {banner}")
                        else:
                            s.send(b'GET / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
                            banner = s.recv(1024).decode(errors='ignore').strip()
                            print(f"Port {port}: {banner}")
                    except UnicodeDecodeError as e:
                        print(f"Error decoding banner for port {port}: {e}")
                    except socket.timeout as e:
                        print(f"Timeout retrieving banner for port {port}: {e}")
                    except socket.error as e:
                        print(f"Socket error retrieving banner for port {port}: {e}")
                    except Exception as e:
                        print(f"Error retrieving banner for port {port}: {e}")
    except socket.gaierror as e:
        print(f"Error resolving hostname {target}: {e}")
    except socket.timeout as e:
        print(f"Timeout error on port {port}: {e}")
    except socket.error as e:
        print(f"Socket error on port {port}: {e}")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def safe_ping(target):
    if os.name == 'nt':
        command = f"ping -n 1 {shlex.quote(target)}"
    else:
        command = f"ping -c 1 {shlex.quote(target)}"

    response = os.system(command)
    return response == 0

if safe_ping(target):
    print(f"[{Fore.LIGHTCYAN_EX + '^' + Style.RESET_ALL}][{Fore.YELLOW + target + Style.RESET_ALL}][{Fore.GREEN + 'is UP' + Style.RESET_ALL}]")
else:
    print(f"[{Fore.LIGHTCYAN_EX + 'X' + Style.RESET_ALL}][{Fore.YELLOW + target + Style.RESET_ALL}][{Fore.RED + 'is DOWN' + Style.RESET_ALL}]")
    sys.exit()

def scan_ports(target, port_range, specific_ports):
    with ThreadPoolExecutor(max_workers=100) as executor:
        if specific_ports:
            futures = [executor.submit(scan_port, port, target) for port in specific_ports]
        else:
            futures = [executor.submit(scan_port, port, target) for port in range(port_range[0], port_range[1] + 1)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Exception in thread: {e}")

scan_ports(target, port_range, specific_ports)

if open_ports:
    print(f"Open Ports: {open_ports}")
else:
    print("No open ports found.")
