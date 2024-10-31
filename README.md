[![CodeFactor](https://www.codefactor.io/repository/github/0x414141411/portscout/badge)](https://www.codefactor.io/repository/github/0x414141411/portscout)
# PortScout

PortScout -- Fast and reliable port scanner written in Python

PortScout is a efficient port scanner designed to help identifying open ports on target systems.

## Features

- **Fast and Reliable**: Quickly identifies open ports on target systems.
- **Version Scan**: Perform version scans on open ports.
- **Specific Ports Scan**: Specify specific ports for scanning.
- **Port Range**: Specify a range of ports to scan (default is 1-1024).

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/0x414141411/Portscout

2. **Install Requirements**:
   ```sh
   pip3 install -r requirements.txt

3. **Run PortScout**
   ```sh
   python portscout.py <target>

## Flags
- **Version Scan**: ```(-v) - To scan version of the host```
- **Specific Ports Scan**: ```(-ps) - To specify specific ports for scanning, e.g., 80,443,8080```
- **Port Range**: ```(-p) - Default range is 1-1024```

## Examples
1. **Basic Scan**:
   ```sh
   python3 portscout.py <target>
2. **Version and Port Range scan**:
   ```sh
   python3 portscout.py -v -p 1-80 <target>
3. **Specific Ports Scan**:
   ```sh
   python3 portscout.py -ps 1, 80,443 <target>


