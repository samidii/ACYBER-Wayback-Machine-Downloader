import subprocess
import sys
import importlib
import time
import random
import os
import socket

# Required packages
required_packages = ["requests", "colorama"]

# Check and install missing packages
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"[INFO] Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import requests
from colorama import Fore, Style, init

init(autoreset=True)

# Show ASCII banner
BANNER = r"""
 ______    ______  __      __  _______   ________  _______  
/      \  /      \|  \    /  \|       \ |        \|       \ 
|  $$$$$$\|  $$$$$$\\$$\  /  $$| $$$$$$$\| $$$$$$$$| $$$$$$$\
| $$__| $$| $$   \$$ \$$\/  $$ | $$__/ $$| $$__    | $$__| $$
| $$    $$| $$        \$$  $$  | $$    $$| $$  \   | $$    $$
| $$$$$$$$| $$   __    \$$$$   | $$$$$$$\| $$$$$   | $$$$$$$\
| $$  | $$| $$__/  \   | $$    | $$__/ $$| $$_____ | $$  | $$
| $$  | $$ \$$    $$   | $$    | $$    $$| $$     \| $$  | $$
 \$$   \$$  \$$$$$$     \$$     \$$$$$$$  \$$$$$$$$ \$$   \$$
                                                             
                                                             
"""
print(Fore.CYAN + BANNER)
print(Fore.YELLOW + "[INFO] ACYBER downloader starting...\nVersion : 2025-08-30 1.0.0\n@mrmtwoj at Github")

# Global settings
TIMEOUT = 15
RETRIES = 3
DELAY = 2
RETRY_DELAY = 10

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
]

def get_random_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

# Proxy handling
def check_open_ports(start, end, host="127.0.0.1"):
    open_ports = []
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        try:
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            s.close()
    return open_ports

available_ports = []

def get_random_proxy():
    if available_ports: 
        port = random.choice(available_ports)
        return {"http": f"socks5://127.0.0.1:{port}", "https": f"socks5://127.0.0.1:{port}"}
    return None 

# Fetch snapshots from Wayback Machine
def fetch_snapshots(domain):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=timestamp,original&collapse=digest"
    try:
        resp = requests.get(url, timeout=TIMEOUT, proxies=get_random_proxy(), headers=get_random_headers())
        resp.raise_for_status()
        data = resp.json()
        return data[1:] if len(data) > 1 else []
    except Exception:
        print(Fore.RED + "[ERROR] Failed to fetch snapshots from Wayback Machine")
        return []

# Download a single file
def download_file(archive_url, filepath):
    for attempt in range(RETRIES):
        try:
            r = requests.get(archive_url, timeout=TIMEOUT, proxies=get_random_proxy(), headers=get_random_headers())
            if r.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(r.content)
                print(Fore.GREEN + f"[OK] {os.path.basename(filepath)}")
                return True
            else:
                print(Fore.YELLOW + f"[FAIL] {os.path.basename(filepath)} ({r.status_code})")
        except Exception:
            print(Fore.MAGENTA + f"[WARNING] Network issue for {os.path.basename(filepath)}. Waiting {RETRY_DELAY}s before retry...")
            time.sleep(RETRY_DELAY)
        time.sleep(DELAY)
    print(Fore.RED + f"[ERROR] Failed to download {os.path.basename(filepath)} after {RETRIES} attempts")
    return False

# Download multiple files
def download_files(snapshots, ftype):
    for ts, original in snapshots:
        if not original.lower().endswith(f".{ftype}"):
            continue
        archive_url = f"https://web.archive.org/web/{ts}/{original}"
        filename = f"{ts}_{os.path.basename(original)}"
        filepath = os.path.join(os.getcwd(), filename)

        if os.path.exists(filepath):
            print(Fore.CYAN + f"[SKIP] {filename}")
            continue

        print(Fore.BLUE + f"[DL] {archive_url}")
        download_file(archive_url, filepath)
        time.sleep(DELAY)

# Main
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="acyber.ir security redteam at iran - Download historical files from Wayback Machine"
    )
    parser.add_argument("-url", required=True, help="Domain or URL (e.g., example.com)")
    parser.add_argument("-type", required=True, help="File type to download (e.g., pdf, jpg, png)")
    parser.add_argument("-proxyport", help="Proxy port range, e.g., 1080-1090", default=None)
    args = parser.parse_args()

    global available_ports
    if args.proxyport:
        try:
            start, end = map(int, args.proxyport.split("-"))
            available_ports = check_open_ports(start, end)
            print(Fore.CYAN + f"Available proxy ports: {available_ports}")
        except:
            print(Fore.RED + "[ERROR] Invalid proxyport format. Use start-end, e.g., 1080-1090")
            available_ports = []

    snapshots = fetch_snapshots(args.url)
    print(Fore.CYAN + f"Found {len(snapshots)} snapshots for {args.url}")

    download_files(snapshots, args.type)

if __name__ == "__main__":
    main()
