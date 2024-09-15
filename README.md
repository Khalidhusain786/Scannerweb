# Scannerweb

Vulnerability Scanner written in python3, It Fuzzes All URLs of target website & then scan them for scanner web

# Screeenshot 

![CAPTURE 1](https://github.com/Khalidhusain786/Scannerweb/blob/main/Screenshot_2023-10-15_22_39_36.png)
![CAPTURE 1](https://github.com/Khalidhusain786/Scannerweb/blob/main/Screenshot_2023-10-15_22_40_00.png)

# Navigate to the /opt directory (optional)
```bash
cd /opt/
```

# Clone this repository
```bash

 git clone https://github.com/Khalidhusain786/Scannerweb.git
```

# Navigate to scannerweb folder
```bash
 cd Scannerweb
```

# Installing dependencies
```bash

 sudo apt install python3-pip 

 pip3 install -r requirements.txt

```

# Installing GoBuster (For More Installation Method, Visit: https://github.com/OJ/gobuster)
# NOTE: GoBuster Tool is Only Required for using --fuzz-scan flag
# PS: You need at least go 1.16.0 to compile gobuster.

```bash
 go install github.com/OJ/gobuster/v3@latest

```

# Help Menu

```bash
 chmod +x scannerweb.py

 python3 scannerweb.py --help
```

# Scanning Single URL
```bash

 python3 scannerweb.py https://example.com/admin/dashboard.php
```
 
# Scanning Multiple URLs
```bash

 python3 scannerweb.py -uL url_list.txt
```

# Automatically FUZZ URLs and Scan Them for web 
```bash
sudo apt install gobuster

python3 scannerweb.py -f -u https://www.example.com -w wrordlst.txt
```
