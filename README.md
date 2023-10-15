# Scannerweb

Vulnerability Scanner written in python3, It Fuzzes All URLs of target website & then scan them for scanner web

# Navigate to the /opt directory (optional)
$ cd /opt/

# Clone this repository
$ git clone https://github.com/PushpenderIndia/EARScanner.git

# Navigate to EARScanner folder
$ cd EARScanner

# Installing dependencies
$ sudo apt install python3-pip 
$ pip3 install -r requirements.txt

# Installing GoBuster (For More Installation Method, Visit: https://github.com/OJ/gobuster)
# NOTE: GoBuster Tool is Only Required for using --fuzz-scan flag
# PS: You need at least go 1.16.0 to compile gobuster.
$ go install github.com/OJ/gobuster/v3@latest

# Help Menu
$ chmod +x scannerweb.py
$ python3 scannerweb.py --help

# Scanning Single URL
$ python3 scannerweb.py -u https://example.com/admin/dashboard.php

# Scanning Multiple URLs
$ python3 scannerweb.py -uL url_list.txt

# Automatically FUZZ URLs and Scan Them for EAR 
$ python3 scannerweb.py -f https://www.example.com
