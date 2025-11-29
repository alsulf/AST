import threading
import socket
import random
import time
import hashlib
import os
import sys
from datetime import datetime

# color
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    C_RED = Fore.RED
    C_GREEN = Fore.GREEN
    C_YELLOW = Fore.YELLOW
    C_CYAN = Fore.CYAN
    C_RESET = Style.RESET_ALL
except Exception:
    C_RED = C_GREEN = C_YELLOW = C_CYAN = C_RESET = ""

# Utility functions
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def safe_private_ip(ip):
    """Return True if IP is in a private IP range."""        
    try:
        parts = [int(p) for p in ip.split('.')]
        if len(parts) != 4:
            return False
        a, b, c, d = parts
        # 10.0.0.0/8
        if a == 10:
            return True
        # 172.16.0.0/12
        if a == 172 and 16 <= b <= 31:
            return True
        # 192.168.0.0/16
        if a == 192 and b == 168:
            return True
        return False
    except Exception:
        return False
    
def progress_bar(prefix, total=100, speed=0.02):
    for i in range(total + 1):
        bar = ('#' * (i // 2)).ljust(50)
        print(f"{C_GREEN}{prefix} [{bar}] {i}%{C_RESET}", end='\r')
        time.sleep(speed * (0.8 + random.random() * 0.4))
    print()

# Visual Effects
def matrix_rain(duration=6):
    chars = "01"
    end = time.time() + duration    
    try:
        while time.time() < end:
            line = "".join(random.choice(chars) for _ in range(123))
            print(line)
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass

def scanning(nodes_min=1, nodes_max=8, duration=4):
    start = time.time()
    nodes = 0
    while time.time() - start < duration:
        nodes = random.randint(nodes_min, nodes_max)
        pct = int((time.time() - start) / duration * 100)
        sys.stdout.write(f"{C_CYAN}[SCANNING]{C_RESET} Progress: {pct}% | Nodes found: {nodes} \r")
        sys.stdout.flush()
        time.sleep(0.04)
    print()

def ascii_radar(scan_ip_list, sweep_duration=6):
    rows, cols = 20, 40
    center_r, center_c = rows // 2, cols // 2
    def ip_to_pos(ip):
        seed = sum(int(x) for x in ip.split('.'))
        random.seed(seed)
        return random.randint(1, rows - 2), random.randint(1, cols - 2)
    ip_positions = {ip: ip_to_pos(ip) for ip in scan_ip_list}
    end = time.time() + sweep_duration
    try:
        while time.time() < end:
            angle = random.randint(0, 359)
            clear()
            print(f"{C_YELLOW}=== IP RADAR ==={C_RESET}")
            for r in range(rows):
                line = ''
                for c in range(cols):
                    ch = '.'
                    for ip, (pr, pc) in ip_positions.items():
                        if pr == r and pc == c:
                            ch = '*'
                    if r == center_r and c == center_c:
                        ch = '0'
                    line += ch
                print(line)
            time.sleep(0.12)
    except KeyboardInterrupt:
        pass

# Network Tools
COMMON_PORTS = [22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389]

def scan_port(ip, port, timeout=0.3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            res = s.connect_ex((ip, port))
            if res == 0:
                return True
    except Exception:
        pass
    return False

def port_scan_ip(ip, ports=None, max_threads=50):
    if ports is None:
        ports = COMMON_PORTS
    open_ports = []

    if not safe_private_ip(ip):
        print(f"{C_RED}Target {ip} is not a private IP. Scan aborted (safety).{C_RESET}")
        return open_ports
    threads = []
    results_lock = threading.Lock()
    def worker(p):
        if scan_port(ip, p):
            with results_lock:
                open_ports.append(p)
    for p in ports:
        t = threading.Thread(target=worker, args=(p,))
        t.start()
        threads.append(t)
        if len(threads) >= max_threads:
            for th in threads:
                th.join()
            threads = []
    for th in threads:
        th.join()
    return sorted(open_ports)

def scan_ip_range(prefix, start=1, end=20, timeout=0.2):
    active_hosts = []
    threads = []
    lock = threading.Lock()
    def worker(i):
        ip = f"{prefix}{i}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                res = s.connect_ex((ip, 80))
                if res == 0:
                    with lock:
                        active_hosts.append(ip)
        except Exception:
            pass
    for i in range(start, end + 1):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return sorted(active_hosts)

# Hashing & Cracker
HASH_ALGS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
}

def hash_text(text, algo='sha256'):
    algo = algo.lower()
    if algo not in HASH_ALGS:
        raise ValueError('Unsupportted algorithm')
    h = HASH_ALGS[algo](text.encode('utf-8')).hexdigest()
    return h

def cracker(target_hash, algo='sha256', duration=6):
    print(f"{C_YELLOW}Starting cracking...{C_RESET}")
    start = time.time()
    candidates = 0
    while time.time() - start < duration:
        candidates += random.randint(100, 500)
        pct = int((time.time() - start) / duration * 100)
        sys.stdout.write(f"Triying... {candidates} candidates | {pct}%\r")
        sys.stdout.flush()
        time.sleep(0.05 + random.random() * 0.05)
    print()
    cracked = random.random() < 0.35
    if cracked:
        sample = '4L5ULF89:)'
        print(f"{C_GREEN}Cracked! -> {sample} {C_RESET}")
        return sample
    else:
        print(f"{C_RED}Failed to crack (x).{C_RESET}")
        return None

# Packet Log
def packet_log(duration=6, ips=None):
    if ips is None:
        ips = [f"192.168.1.{i}" for i in range(2, 10)]
    end = time.time() + duration
    try:
        while time.time() < end:
            src = random.choice(ips)
            dst = random.choice(ips)
            proto = random.choice(['TCP', 'UDP','ICMP'])
            sport = random.randint(1024, 65535)
            dport = random.choice(COMMON_PORTS)
            size = random.randint(40, 1500)
            ts = datetime.now().strftime('%H:%M:%S')
            print(f"{C_GREEN}[PACKET] {ts} {src} -> {dst} | {proto} | {dport} | {size} bytes{C_RESET}")
            time.sleep(0.12 + random.random() * 0.18)
    except KeyboardInterrupt:
        pass

# UI & Menu
def banner():
    print(C_CYAN + r"""
   _____      __          _________   ___    ___    __           ________
  /     \    |  |        /  ______/   |  |   |  |  |  |         |  _____/
 /  ___  \   |  |        \  \ ____    |  |   |  |  |  |         |  |_____
|  |___|  |  |  |         \____   \   |  |   |  |  |  |         |  _____/
|  _____  |  |  |              \   \  |  |   |  |  |  |         |  |
|  |   |  |  |  |______   _____/   /  |  |___|  |  |  |______   |  |
|__|   |__|  |_________|  \_______/   \_________/  |_________|  |__|      v.2025.11.0a1

""" + C_RESET)
    print(C_YELLOW + "Tools Basic of Termux" + C_RESET)
    print()

def main_menu():
    while True:
        clear()
        banner()
        print("1. Matrix rain")
        print("2. Scan + Radar")
        print("3. Network scan")
        print("4. Port scan")
        print("5. Packet log")
        print("6. Hash tool")
        print("7. All tools")
        print("0. Exit")
        print()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            clear(); print(f"{C_RED}Matrix rain (Ctrl+C to stop).{C_RESET}")
            matrix_rain(30); input("press enter to return...")
        elif choice == '2':
            clear(); scanning(); sample_ips = [f"192.168.{i}" for i in range(2, 10)]
            ascii_radar(sample_ips, sweep_duration=6)
            input("press enter to return...")
        elif choice == '3':
            clear(); 
            prefix = input("Enter IP prefix (e.g. 192.168.1.): ").strip()
            if not prefix.endswith('.'):
                prefix += '.'
            test_ip = prefix + '1'
            if not safe_private_ip(test_ip):
                print(f"{C_RED}Prefix {prefix} is not private. Aborted for safety.{C_RESET}")
                input("Enter to return...")
                continue
            start = int(input("Start (1-254): ").strip() or '1')
            end = int(input("End (start-254): ").strip() or str(min(start+19, 254)))
            print("Scanning range...")
            hosts = scan_ip_range(prefix, start=start, end=end, timeout=0.15)
            print(f"Active hosts: {hosts}")
            input("Enter to return...")
        elif choice == '4':
            clear(); ip = input("Enter target IP : ").strip()
            if not safe_private_ip(ip):
                print(f"{C_RED}Target {ip} is not private. Aborted for safety.{C_RESET}")
                input("Enetr to teturn...")
                continue
            print(f"{C_YELLOW}Running port scan...{C_RESET}")
            progress = threading.Thread(target=progress_bar, args=("Port scan", 100, 0.59))
            progress.start()
            opens = port_scan_ip(ip, ports=COMMON_PORTS)
            progress.join()
            print(f"Open ports on {ip}: {opens}")
            input("Enter to return...")
        elif choice == '5':
            clear(); print("Packet log (Ctrl+C to stop)")
            packet_log(60)
            input("enter to return...")
        elif choice == '6':
            clear(); t = input("Enter text to hash: ").strip()
            algo = input("Algorithm (md5/sha1/sha256) [sha256]: ").strip() or 'sha256'
            try:
                h = hash_text(t, algo=algo)
                print(f"{algo} -> {h}")
            except Exception as e:
                print(f"Error: {e}")
                input("Enter to return...")
                continue
            c = input(f"{C_GREEN}Run cracker on this hash? (y/N): {C_RESET}").strip().lower()
            if c == 'y':
                cracker(h, algo=algo, duration=6)
            input("Enter to return...")
        elif choice == '7':
            clear(); print("Starting All tools...")
            t1 = threading.Thread(target=matrix_rain, args=(6,))
            t2 = threading.Thread(target=scanning, args=(1, 12, 5))
            t1.start(); t2.start()
            t1.join(); t2.join()
            ascii_radar([f"192.168.1.{i}" for i in range(2, 16)], sweep_duration=5)
            print("Now showing packet logs:")
            packet_log(5)
            print(f"{C_GREEN}complete #{C_RESET}")
            input("Enter on return...")
            
        elif choice == '0':
            print(f"{C_GREEN}Thanks & Goodbye.{C_RESET}")
            break
        else:
            print("Unknown option.")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting...')