import requests
import threading
import random
import time
import os
import sys
import re
from datetime import datetime

# ANSI color codes for hacker aesthetic
RED = "\033[1;31m"
DARK_RED = "\033[31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPLE = "\033[1;35m"
CYAN = "\033[1;36m"
DARK_GREY = "\033[1;90m"
RESET = "\033[0m"

# Banner and social media links
BANNER = f"""{RED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣄⠀⠐⣶⣶⣶⣶⣶⡖⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⠆⠀⠀⢀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡏⢅⠄⡀⠉⢛⡙⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢄⡆⡀⠀⢀⣠⣤⣾⣿⣿⣿⡃⠀⠀⢸
⠀⡀⠀⠀⠂⠀⠀⠀⠈⢀⠀⠀⢠⣷⡏⣲⡀⣀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡐⠌⣘⣲⡄⣿⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀
⣿⢕⠀⠀⠀⠀⠀⠐⠀⠋⠀⠀⢸⡟⡜⢣⣹⣿⣿⣶⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡚⠃⠀⠉⢿⡧⠘⠉⠁⠈⢻⢿⣿⠆⠀⠀⠀
⡵⡾⠀⠀⠀⠀⠿⠛⠁⠀⠀⠀⠈⠀⠀⣤⣶⣶⣶⣶⣤⣀⢠⠀⠀⡀⢀⠀⡀⠀⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢀⣀⣠⣾⣇⠀⠀⠀⠀⠀⠈⠹⡃⠀⠀⠀
⣦⠁⠀⠀⢘⣦⡀⠀⠤⠒⠈⠀⠀⠀⠀⠀⢠⡀⣄⡀⣀⠀⠀⠈⠀⠉⠈⠘⠒⠛⠂⠀⠀⠀⠀⠴⣤⢢⣄⠀⠀⣄⣀⠘⠻⢿⡗⠀⠀⠀⠀⠀⠀⠀⡅⠀⠀⠀
⣟⣧⠀⠀⠼⠛⣥⡃⠄⡀⠀⠀⠀⠀⠀⠀⣮⣽⣿⣿⣿⣻⡖⣶⣼⣦⣴⣀⢀⠀⢠⠠⠄⡀⢀⠀⠀⠀⠀⠈⠉⠈⠀⠙⠀⠄⠈⠀⠀⠀⢀⣴⣶⣶⠆⠀⠀⠀
⣿⣿⡀⠀⠀⠀⣿⡹⢎⠔⠀⡀⠀⠀⠀⠴⠺⣿⣿⣿⠃⠁⠈⠈⠉⠛⠻⡹⣞⡂⢅⡊⠴⡐⢏⡟⣼⣿⣿⢦⣦⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⢸⣿⣿⡃⠀⠀⠀
⣿⣿⡆⢰⣤⡀⠙⡸⢌⡚⠄⠀⠀⠀⠀⣠⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠘⢆⠱⠀⠨⠑⠉⠀⠀⠀⠀⠀⠉⣾⠀⠀⠀⠀⠀⢰⣠⣶⣷⣾⡟⣿⣿⠇⠀⠀⠈
⣿⣿⡇⠫⣿⣿⠀⠀⠃⠜⡄⠀⠀⠀⠀⣽⣿⣿⠏⠃⠀⠀⠀⠀⠀⠀⠀⡀⡈⣔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡄⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣻⣿⡇⠀⠀⠀
⣿⣿⣀⣤⣿⣿⣇⠀⠀⢰⡀⠀⠈⠄⠀⣿⣿⣿⠦⣁⠒⣶⣴⣴⡶⢼⢭⣇⠞⠁⠀⠘⡤⣀⠀⠀⠀⠀⠀⢦⣹⡇⠀⠀⠀⡜⠀⣿⡿⠛⣵⣿⣿⣿⡆⠀⠀⠀
⣿⣿⣿⣅⠀⠚⣿⡆⠀⠢⠄⠀⠀⢂⠀⣿⣿⣿⢰⢩⡙⣾⣿⣿⢯⣯⣿⠇⠀⠀⠀⠀⢰⢩⣿⠇⠀⣀⠉⠢⢵⡇⠀⠀⡘⠄⠐⠋⣠⣾⣿⣿⣿⣿⠆⠀⠀⠀
⣿⣿⣿⣿⣧⣠⣼⣿⠀⢀⠂⠀⠀⠀⢂⠙⢍⠣⣋⢧⣝⣾⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢨⣹⢎⠀⢦⠑⢢⡙⡼⠀⠀⡐⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⡇⠀⠀⢈
⣿⣿⣿⣿⣿⣿⣧⠥⢭⣤⣤⠀⠀⠀⠢⠀⠀⠀⠀⠜⣿⣿⣿⡏⣿⣿⠟⣀⠠⢢⠄⡀⢤⣛⡎⠜⠢⠉⠂⠁⠀⠀⠐⠀⠀⡀⣿⣿⣿⣿⣿⣿⣿⣿⡷⡇⠀⠀
⣿⣿⣿⣿⣿⣿⢱⢃⠀⠉⠃⠀⠀⠀⠀⡃⠀⠀⠀⠀⠾⣿⣿⢱⡧⡇⠀⡣⠘⡁⠂⠴⢸⣟⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣱⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠀⠀
⣿⣿⣿⣿⣿⣿⣎⢧⠂⠀⠀⠀⠀⠀⠀⠰⠁⠀⠀⠀⠀⣯⢋⡎⡑⣁⢐⡑⣀⠃⡘⠠⣻⠍⠀⠀⠀⠀⢠⣶⣶⡖⠀⣀⣤⣛⠻⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣯⡣⡅⡀⠀⠀⠱⣀⠀⠑⠀⠀⠀⠀⠀⡇⢨⠀⠃⠈⠃⠘⠐⠂⠂⠒⠀⠀⠀⠀⠀⠀⢻⣿⠀⢼⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⡃⠀⠀⢀
⠙⣿⠿⡿⢿⣿⣿⣿⣷⣜⠡⣆⡀⠀⠀⠈⠄⠠⠀⠀⠀⠀⡏⡔⠰⠀⠆⡄⢀⠀⡘⠐⠀⠀⠀⠀⠀⠀⠠⣌⢿⠀⣼⣿⣿⣿⣿⣿⠿⢸⣿⣿⣿⣿⠄⠀⠀⠀
⠀⠀⠀⠃⢫⣿⣿⣿⣿⣿⣷⠆⠹⢤⡀⠀⠀⠀⠈⠀⠃⠄⠀⠁⠀⠘⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠌⠎⢀⣿⣿⣿⣿⠟⣡⣾⣿⣿⣿⣿⣿⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠙⠿⢿⣿⣿⣾⢁⠀⠉⠣⠄⠀⠀⠀⠀⠆⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡿⠛⠰⠿⠁⠀⠉⢹⣿⣿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠫⣭⣓⠏⠤⢠⡊⠑⣠⡀⠀⠀⠀⠁⠀⠰⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠂⠄⠀⠀⠀⠀⠉⠋⠁⠀⠀⠀⠀⠀⠀⠈⢟⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠐⡠⠀⠀⠈⠛⢿⣶⣬⡖⠁⠄⠳⠆⣀⠀⠀⠀⠀⠀⠀⠈⠀⠀⡐⠀⠡⠀⠀⠀⠠⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠐
⠀⠀⠀⠀⠀⠀⠀⠀⡑⠬⢠⠀⠀⠀⠈⠀⠏⠀⠈⢀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠀⠀⠀⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡁⠎⠤⡀⠀⠀⠀⠀⠀⠀⠂⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢢⢒⡡⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀SIGMA_CYBER_GHOST⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠡⠚⡐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠡⠀⠁⠀⠠⠁⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{RESET}"""

SOCIAL_MEDIA = {
    "Telegram": f"{YELLOW}https://web.telegram.org/k/#@Sigma_Cyber_Ghost{RESET}",
    "GitHub": f"{YELLOW}https://github.com/sigma-cyber-ghost{RESET}"
}

# Supported platforms and their report endpoints
PLATFORMS = {
    "instagram": {
        "url": "https://www.instagram.com/report",
        "validation": r"^[a-zA-Z0-9_.]{1,30}$",
        "profile": "https://www.instagram.com/{username}/"
    },
    "whatsapp": {
        "url": "https://www.whatsapp.com/report",
        "validation": r"^(\+\d{1,3})?\d{8,15}$",
        "profile": None
    },
    "twitter": {
        "url": "https://api.twitter.com/report",
        "validation": r"^[a-zA-Z0-9_]{1,15}$",
        "profile": "https://twitter.com/{username}"
    },
    "facebook": {
        "url": "https://www.facebook.com/report",
        "validation": r"^[a-zA-Z0-9.]{5,50}$",
        "profile": "https://www.facebook.com/{username}"
    },
    "tiktok": {
        "url": "https://www.tiktok.com/report",
        "validation": r"^[a-zA-Z0-9_.]{3,24}$",
        "profile": "https://www.tiktok.com/@{username}"
    },
    "reddit": {
        "url": "https://www.reddit.com/report",
        "validation": r"^[a-zA-Z0-9_-]{3,20}$",
        "profile": "https://www.reddit.com/user/{username}"
    },
    "discord": {
        "url": "https://discord.com/report",
        "validation": r"^.{3,32}#[0-9]{4}$",
        "profile": None
    }
}

# Common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15"
]

PROXY_LIST = [
    "185.199.229.156:7492",
    "185.199.228.220:7300",
    "188.74.210.207:6286",
    "188.74.183.10:8279",
    "45.155.68.129:8133"
]

def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.01):
    """Print text with hacker-like typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    """Display banner and social media links with hacker style"""
    clear_screen()
    print(BANNER)
    print(f"{RED}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{DARK_GREY}                    SIGMA CYBER GHOST - WEAPONIZED REPORTING TOOL             {RED}║")
    print(f"║{DARK_GREY}                         [Version 1.2] - [Validation Enhanced]                {RED}║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
    
    print(f"\n{RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   SOCIAL MEDIA LINKS:{RESET}")
    for platform, url in SOCIAL_MEDIA.items():
        print(f"   {GREEN}• {platform}:{RESET} {url}")
    print(f"{RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")

def validate_username(username, platform):
    """Validate username format for specific platform"""
    pattern = PLATFORMS[platform]["validation"]
    return re.match(pattern, username) is not None

def check_existence(username, platform):
    """Check if username exists on platform with enhanced validation"""
    platform_data = PLATFORMS[platform]
    profile_url = platform_data.get("profile")
    if not profile_url:
        return None  # Platform doesn't support public profile checks
        
    url = profile_url.format(username=username)
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        proxies = {
            "http": f"http://{random.choice(PROXY_LIST)}",
            "https": f"http://{random.choice(PROXY_LIST)}"
        }
        
        response = requests.get(
            url, 
            headers=headers, 
            timeout=10,
            proxies=proxies,
            allow_redirects=False
        )
        
        # Platform-specific validation
        if platform == "instagram":
            # Instagram returns 200 for valid profiles, 404 for invalid
            return response.status_code == 200
        elif platform == "twitter":
            # Twitter returns 200 for valid, 404 for invalid
            return response.status_code == 200
        elif platform == "facebook":
            # Facebook might redirect to login for invalid profiles
            return response.status_code == 200 and "login" not in response.url
        elif platform == "tiktok":
            # TikTok returns 200 for valid, 404 for invalid
            return response.status_code == 200
        elif platform == "reddit":
            # Reddit returns 200 for valid, 404 for invalid
            return response.status_code == 200
        else:
            # Generic validation for other platforms
            return response.status_code == 200
            
    except Exception:
        return None  # Error occurred

def flag(account, platform):
    """Send report requests to a specific platform"""
    platform_url = PLATFORMS[platform]["url"]
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    
    proxies = {
        "http": f"http://{random.choice(PROXY_LIST)}",
        "https": f"http://{random.choice(PROXY_LIST)}"
    }
    
    payload = {
        "username": account,
        "reason": "hate_speech",
        "details": "User is inciting violence and hate against minorities.",
        "source": "web_report",
        "timestamp": int(time.time())
    }
    
    try:
        for i in range(10):  # Send 10 rapid-fire flags
            start_time = time.time()
            response = requests.post(
                platform_url,
                json=payload,
                headers=headers,
                timeout=8,
                proxies=proxies
            )
            elapsed = time.time() - start_time
            
            if response.status_code in (200, 201, 202):
                print(f"{GREEN}[✓] {DARK_GREY}{time.strftime('%H:%M:%S')} {YELLOW}REPORT {i+1}/10 {RESET}| {CYAN}{platform.upper()} {RESET}| {GREEN}Status: {response.status_code} {RESET}| {DARK_GREY}Time: {elapsed:.2f}s{RESET}")
            else:
                print(f"{RED}[✗] {DARK_GREY}{time.strftime('%H:%M:%S')} {YELLOW}REPORT {i+1}/10 {RESET}| {CYAN}{platform.upper()} {RESET}| {RED}Status: {response.status_code} {RESET}| {DARK_GREY}Time: {elapsed:.2f}s{RESET}")
            
            time.sleep(random.uniform(0.2, 1.0))
    except Exception as e:
        print(f"{RED}[!] {DARK_GREY}{time.strftime('%H:%M:%S')} {RED}ERROR {RESET}| {CYAN}{platform.upper()} {RESET}| {RED}{str(e)[:60]}{RESET}")

def purge(account, selected_platforms):
    """Handle multi-threaded flagging operations"""
    threads = []
    print(f"\n{RED}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{YELLOW} TARGET ACQUISITION: {GREEN}{account}{RESET}{' '*(42-len(account))}{RED}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    
    for platform in selected_platforms:
        t = threading.Thread(target=flag, args=(account, platform))
        t.daemon = True
        t.start()
        threads.append(t)
        print(f"{PURPLE}[~] {DARK_GREY}DEPLOYING {RESET}| {CYAN}{platform.upper()} {RESET}| {YELLOW}Thread Activated{RESET}")
        time.sleep(0.1)
    
    # Monitor threads
    while any(t.is_alive() for t in threads):
        time.sleep(0.5)
    
    print(f"\n{GREEN}[✓] {YELLOW}ALL OPERATIONS COMPLETED FOR CURRENT WAVE{RESET}")

def main():
    """Main program interface"""
    show_banner()
    
    # Get target username
    print_slow(f"{RED}┌──({RESET}{GREEN}sigma@cyberghost{RED})-[{RESET}{YELLOW}~/target_acquisition{RED}]{RESET}")
    victim = input(f"{RED}└─{GREEN}${RESET} Target username: ").strip()
    
    if not victim:
        print(f"{RED}[✘] INVALID TARGET IDENTIFIER{RESET}")
        return
    
    # Platform selection
    print(f"\n{RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   AVAILABLE PLATFORMS:{RESET}")
    for i, platform in enumerate(PLATFORMS.keys(), 1):
        print(f"   {GREEN}{i}. {platform.upper()}{RESET}")
    print(f"{RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    choices = input(f"{RED}┌──({RESET}{GREEN}sigma@cyberghost{RED})-[{RESET}{YELLOW}~/platform_selection{RED}]{RESET}\n{RED}└─{GREEN}${RESET} Select platforms (comma separated, 'all' for all): ").strip().lower()
    
    if choices == 'all':
        selected_platforms = list(PLATFORMS.keys())
    else:
        selected_platforms = []
        for choice in choices.split(','):
            choice = choice.strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(PLATFORMS):
                    selected_platforms.append(list(PLATFORMS.keys())[index])
            elif choice in PLATFORMS:
                selected_platforms.append(choice)
    
    if not selected_platforms:
        print(f"{RED}[✘] NO VALID PLATFORMS SELECTED{RESET}")
        return
    
    # Validate usernames for each platform
    print(f"\n{RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   USERNAME VALIDATION:{RESET}")
    
    valid_platforms = []
    for platform in selected_platforms:
        is_valid = validate_username(victim, platform)
        status = f"{GREEN}VALID{RESET}" if is_valid else f"{RED}INVALID{RESET}"
        print(f"   {CYAN}{platform.upper()}:{RESET} {status}")
        
        if is_valid:
            valid_platforms.append(platform)
            
    print(f"{RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    if not valid_platforms:
        print(f"{RED}[✘] NO VALID PLATFORMS FOR THIS USERNAME{RESET}")
        return
    
    # Check account existence
    print(f"\n{RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   ACCOUNT EXISTENCE CHECK:{RESET}")
    
    existing_platforms = []
    for platform in valid_platforms:
        if PLATFORMS[platform].get("profile"):
            exists = check_existence(victim, platform)
            if exists is True:
                status = f"{GREEN}EXISTS{RESET}"
                existing_platforms.append(platform)
            elif exists is False:
                status = f"{RED}NOT FOUND{RESET}"
            else:
                status = f"{YELLOW}UNKNOWN{RESET}"
                existing_platforms.append(platform)  # Proceed if unknown
            print(f"   {CYAN}{platform.upper()}:{RESET} {status}")
        else:
            print(f"   {CYAN}{platform.upper()}:{RESET} {DARK_GREY}Check not supported{RESET}")
            existing_platforms.append(platform)  # Always include platforms without profile check
            
    print(f"{RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    if not existing_platforms:
        print(f"{RED}[✘] NO VALID ACCOUNTS FOUND{RESET}")
        return
    
    # Confirmation
    print(f"{RED}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{YELLOW} TARGETING: {GREEN}{', '.join(existing_platforms).upper()}{RESET}{' '*(50-len(', '.join(existing_platforms)))}{RED}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    confirm = input(f"{RED}┌──({RESET}{GREEN}sigma@cyberghost{RED})-[{RESET}{YELLOW}~/confirmation{RED}]{RESET}\n{RED}└─{GREEN}${RESET} Confirm operation? (y/n): ").strip().lower()
    if confirm != 'y':
        print(f"{YELLOW}[*] OPERATION ABORTED{RESET}")
        return
    
    # Start attack waves
    print(f"\n{RED}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{YELLOW} INITIATING WEAPONIZED REPORTING SEQUENCE                   {RED}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    
    for wave in range(1, 6):  # Five waves
        print(f"\n{RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
        print(f"{RED}   [🚀] {YELLOW}WAVE {wave}/5 IN PROGRESS... {DARK_GREY}[{time.strftime('%H:%M:%S')}]{RESET}")
        print(f"{RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}")
        purge(victim, existing_platforms)
        if wave < 5:
            delay = random.uniform(1, 3)
            print(f"\n{YELLOW}[*] RECALIBRATING SYSTEMS - Next wave in {delay:.1f} seconds{RESET}")
            time.sleep(delay)
    
    print(f"\n{RED}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{GREEN} OPERATION COMPLETED - 5 WAVES EXECUTED SUCCESSFULLY        {RED}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{DARK_GREY}Report summary generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[✘] OPERATION TERMINATED BY USER{RESET}")
    except Exception as e:
        print(f"\n{RED}[✘] CRITICAL SYSTEM FAILURE: {str(e)}{RESET}")
