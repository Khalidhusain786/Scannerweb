import requests
import urllib3
import concurrent.futures
from colorama import init, Fore, Back, Style
import argparse
import pyfiglet
import sys
import os
import platform

# Correctly disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init()

class scannerweb:
    def __init__(self):
        self.vulnerable_urls = []
        self.progress = []
        self.errors = []
        self.total = 0

    def get_arguments(self):
        # Banner with your custom title
        banner = pyfiglet.figlet_format("      scannerweb")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        
        parser = argparse.ArgumentParser(description=f'{Fore.RED}Scannerweb v1.0 {Fore.YELLOW}[Author: {Fore.GREEN}Khalid Husain{Fore.YELLOW}] [{Fore.GREEN}https://github.com/Khalidhusain786{Fore.YELLOW}]')
        parser._optionals.title = f"{Fore.GREEN}Optional Arguments{Fore.YELLOW}"
        
        parser.add_argument("-u", "--url", dest="url", help=f"Scan Single URL for Khalid")
        parser.add_argument("-uL", "--url-list", dest="file_containing_urls", help=f"Provide a File Containing URLs")
        parser.add_argument("-f", "--fuzz-scan", dest="fuzz_and_scan", help=f"Fuzz domain using GoBuster then scan")
        parser.add_argument("-w", "--wordlist", dest="wordlist", help=f"Wordlist for fuzzing", default='content_discovery_all.txt')
        parser.add_argument("-t", "--timeout", dest="timeout", help=f"HTTP Timeout (default: 60)", default=60, type=int)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", help=f"Parallel Threads (default: 100)", default=100, type=int)
        parser.add_argument("-c", "--content-length", dest="ContentLength", help=f"Content Length for EAR Confirmation", default=200, type=int)
        parser.add_argument("-o", "--output", dest="output", help=f"Output filename", default='vulnerable.txt')

        return parser.parse_args()

    def start(self):
        self.arguments = self.get_arguments()
        print(f"{Fore.YELLOW}           [Author: {Fore.GREEN}Khalid Husain{Fore.YELLOW}] [{Fore.GREEN}https://github.com/Khalidhusain786{Fore.YELLOW}]\n\n{Style.RESET_ALL}")
        
        self.ThreadNumber = self.arguments.ThreadNumber
        self.timeout = self.arguments.timeout
        self.content_length = self.arguments.ContentLength

        if self.arguments.url:
            self.check_ear(self.arguments.url)
            
        elif self.arguments.file_containing_urls:
            if not os.path.exists(self.arguments.file_containing_urls):
                print(f"{Fore.RED}[!] File not found!{Style.RESET_ALL}")
                return
            
            with open(self.arguments.file_containing_urls, 'r') as f:
                final_url_list = [line.strip() for line in f if line.strip()]

            self.total = len(final_url_list)
            print("="*85)
            print(f'{Fore.YELLOW}[*] Initiating Execution After Redirect (Webscan) Scanner...{Style.RESET_ALL}')
            print("="*85)

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber) as executor:
                executor.map(self.check_ear, final_url_list)

        elif self.arguments.fuzz_and_scan:
            print("="*85)
            print(f'{Fore.YELLOW}[*] Fuzzing URLs using GoBuster Tool...{Style.RESET_ALL}')
            print("="*85)
            binary = "gobuster.exe" if platform.system() == 'Windows' else "gobuster"
            command = f'{binary} dir -w {self.arguments.wordlist} -t {self.timeout} -x php,asp,aspx,jsp -u {self.arguments.fuzz_and_scan} -o urls_list.txt -q -e'
            
            os.system(command)

            if os.path.exists('urls_list.txt'):
                with open('urls_list.txt', 'r') as f:
                    final_url_list = [line.split(' ')[0].strip() for line in f if line.strip()]
                
                self.total = len(final_url_list)
                print("="*85)
                print(f'{Fore.YELLOW}[*] Initiating Scannerweb Vulnerability Scanner...{Style.RESET_ALL}')
                print("="*85)
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber) as executor:
                    executor.map(self.check_ear, final_url_list)
        else:
            print(f"{Fore.RED}[!] Please Provide a URL or File. Use --help for more.{Style.RESET_ALL}")
            sys.exit()

        # Save results
        if self.vulnerable_urls:
            with open(self.arguments.output, 'w') as f:
                for vuln in self.vulnerable_urls:
                    f.write(vuln + "\n")
            print(f'\n\n{Fore.GREEN}[+] Results saved to: {self.arguments.output}{Style.RESET_ALL}')

    def check_ear(self, url):
        try:
            # allow_redirects=False is required to detect EAR
            response = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=False)
            
            if response.status_code == 302:
                if 'Location' in response.headers:
                    response_length = len(response.text)
                    if response_length >= self.content_length:
                        status = f"{Fore.GREEN}100% Vulnerable"
                    else:
                        status = f"{Fore.YELLOW}Might Be Vulnerable"
                    
                    self.vulnerable_urls.append(url)
                    if self.arguments.url:
                        print(f'{Fore.GREEN}[+] [302] {Fore.WHITE}{url} {Fore.YELLOW}[Location: {Fore.GREEN}{response.headers["Location"]}{Fore.WHITE}] [Status: {status}{Fore.YELLOW}]{Style.RESET_ALL}')
            
            elif self.arguments.url:
                print(f'{Fore.YELLOW}[-] [{response.status_code}] {Fore.WHITE}{url}{Fore.YELLOW} ... not vulnerable!{Style.RESET_ALL}')

            if not self.arguments.url:
                self.progress.append(1)
                print(f'\r{Fore.YELLOW}[*] ProgressBar: {Fore.WHITE}{len(self.progress)}/{self.total} {Fore.YELLOW}[Errors: {Fore.RED}{len(self.errors)}{Fore.YELLOW}] [Vulnerable: {Fore.GREEN}{len(self.vulnerable_urls)}{Fore.YELLOW}] ... {Style.RESET_ALL}', end="")
        
        except Exception:
            self.errors.append(1)
            if not self.arguments.url:
                self.progress.append(1)

if __name__ == '__main__':
    test = scannerweb()
    test.start()
