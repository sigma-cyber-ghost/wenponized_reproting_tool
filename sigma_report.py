import requests
import threading
import random
import time
import os
import sys
import re
import argparse
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ANSI color codes - Black Hat Hacker Style
BLACK = "\033[0;30m"
DARK_GREY = "\033[1;30m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)

def create_session():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=100, pool_maxsize=100)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# Enhanced Black Hat Hacker Banner
BANNER = f"""
{BLUE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣄⠀⠐⣶⣶⣶⣶⣶⡖⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⠆⠀⠀⢀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢢⢒⡡⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀{MAGENTA}SIGMA_CYBER_GHOST{BLUE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠡⠚⡐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠡⠀⠁⠀⠠⠁⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{RESET}
{GREEN}╔══════════════════════════════════════════════════════════════════════╗
║{CYAN}    SIGMA CYBER GHOST - WEAPONIZED REPORTING TOOL [Version 2.1]       {GREEN}║
║{CYAN}                         [Proxy-Free Mode]                            {GREEN}║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
{GREEN}╔══════════════════════════════════════════════════════════════════════╗
║{CYAN}    Author: @sigma_cyber_ghost      GitHub: github.com/sigma-cyber    {GREEN}║
║{CYAN}    Instagram: @safderkhan0800_     Telegram: t.me/sigma_cyber_ghost  {GREEN}║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
"""

# Updated platform configurations with improved validation
PLATFORMS = {
    "instagram": {
        "validation": r"^[a-zA-Z0-9_.]{1,30}$",
        "url": "https://www.instagram.com/report/user/",
        "profile": "https://www.instagram.com/{username}/",
        "existence_check": "content"
    },
    "twitter": {
        "validation": r"^[a-zA-Z0-9_]{1,15}$",
        "url": "https://api.twitter.com/1.1/report_user.json",
        "profile": "https://twitter.com/{username}",
        "existence_check": "status"
    },
    "facebook": {
        "validation": r"^[a-zA-Z0-9.]{5,50}$",
        "url": "https://www.facebook.com/api/graphql/",
        "profile": "https://www.facebook.com/{username}",
        "existence_check": "redirect"
    },
    "tiktok": {
        "validation": r"^[a-zA-Z0-9_.]{2,24}$",
        "url": "https://www.tiktok.com/api/report/aweme/",
        "profile": "https://www.tiktok.com/@{username}",
        "existence_check": "status"
    },
    "reddit": {
        "validation": r"^[a-zA-Z0-9_-]{3,20}$",
        "url": "https://www.reddit.com/api/report",
        "profile": "https://www.reddit.com/user/{username}",
        "existence_check": "status"
    },
    "discord": {
        "validation": r"^.{3,32}#[0-9]{4}$",
        "url": "https://discord.com/api/v9/report",
        "profile": None,
        "existence_check": None
    },
    "youtube": {
        "validation": r"^[a-zA-Z0-9_-]{3,30}$",
        "url": "https://www.youtube.com/report",
        "profile": "https://www.youtube.com/user/{username}",
        "existence_check": "status"
    },
    "twitch": {
        "validation": r"^[a-zA-Z0-9_]{4,25}$",
        "url": "https://www.twitch.tv/report",
        "profile": "https://www.twitch.tv/{username}",
        "existence_check": "status"
    }
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    clear_screen()
    print(BANNER)

def validate_username(username, platform):
    pattern = PLATFORMS[platform]["validation"]
    return re.match(pattern, username) is not None

def check_existence(username, platform):
    platform_data = PLATFORMS[platform]
    profile_url = platform_data.get("profile")
    if not profile_url:
        return None
        
    url = profile_url.format(username=username)
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    
    for attempt in range(3):
        try:
            session = create_session()
            response = session.get(
                url, 
                headers=headers,
                timeout=15,
                allow_redirects=True
            )
            
            # Enhanced platform-specific existence checks
            if platform == "instagram":
                # Instagram returns 200 for both existing and non-existing accounts
                # Check for specific content patterns
                page_text = response.text.lower()
                if "page not found" in page_text or "sorry, this page isn't available" in page_text:
                    return False
                if "login" in response.url or "accounts/login" in response.url:
                    return None  # Redirected to login page
                return True  # Account exists
                
            elif platform == "facebook":
                # Facebook redirects to login for non-existing profiles
                return response.status_code == 200 and "facebook.com/login" not in response.url
                
            elif platform == "twitter":
                # Twitter returns 200 for existing accounts, 404 for non-existing
                return response.status_code == 200
                
            elif platform == "tiktok":
                # TikTok returns 200 for existing accounts
                return response.status_code == 200
                
            elif platform == "reddit":
                # Reddit returns 200 for existing accounts
                return response.status_code == 200
                
            elif platform == "youtube":
                # YouTube returns 200 for existing accounts
                return response.status_code == 200
                
            elif platform == "twitch":
                # Twitch returns 200 for existing accounts
                return response.status_code == 200
                
            else:
                return response.status_code == 200
                
        except Exception as e:
            print(f"{RED}[DEBUG] Error checking {platform}: {str(e)[:60]}{RESET}")
            continue
            
    return None  # Couldn't determine after 3 attempts

def flag(account, platform):
    platform_url = PLATFORMS[platform]["url"]
    
    try:
        session = create_session()
        
        for i in range(25):  # Increased report attempts
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }
            
            payload = {
                "username": account,
                "reason": random.choice([
                    "hate_speech", "harassment", "impersonation", 
                    "terrorism", "child_endangerment", "bullying",
                    "self_harm", "graphic_violence", "non-consensual_intimate_imagery"
                ]),
                "details": "User is consistently violating community guidelines with harmful content targeting multiple users",
                "source": "web_report"
            }
            
            try:
                start_time = time.time()
                response = session.post(
                    platform_url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                elapsed = time.time() - start_time
                
                if response.status_code in (200, 201, 202):
                    print(f"{GREEN}[✓] {time.strftime('%H:%M:%S')} REPORT {i+1}/25 | {platform.upper()} | Status: {response.status_code} | Time: {elapsed:.2f}s{RESET}")
                else:
                    print(f"{YELLOW}[!] {time.strftime('%H:%M:%S')} REPORT {i+1}/25 | {platform.upper()} | Status: {response.status_code} | Time: {elapsed:.2f}s{RESET}")
                
            except Exception as e:
                print(f"{RED}[✗] {time.strftime('%H:%M:%S')} ERROR | {platform.upper()} | {str(e)[:60]}{RESET}")
            
            time.sleep(random.uniform(0.2, 0.8))  # Reduced sleep time
            
    except Exception as e:
        print(f"{RED}[✗] CRITICAL ERROR IN {platform.upper()} THREAD: {str(e)[:60]}{RESET}")

def purge(account, selected_platforms):
    threads = []
    print(f"\n{GREEN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{CYAN} TARGET ACQUISITION: {RED}{account}{RESET}{' '*(42-len(account))}{GREEN}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    
    for platform in selected_platforms:
        t = threading.Thread(target=flag, args=(account, platform))
        t.daemon = True
        t.start()
        threads.append(t)
        print(f"{MAGENTA}[~] {CYAN}DEPLOYING {RESET}| {YELLOW}{platform.upper()} {RESET}| {RED}Thread Activated{RESET}")
        time.sleep(0.05)
    
    start_time = time.time()
    while any(t.is_alive() for t in threads):
        if time.time() - start_time > 300:  # Increased timeout
            print(f"{RED}[!] THREAD EXECUTION TIMEOUT REACHED{RESET}")
            break
        time.sleep(1)
    
    print(f"\n{GREEN}[✓] {RED}WAVE OPERATIONS COMPLETED{RESET}")

def main():
    show_banner()
    
    print_slow(f"{GREEN}┌──({RESET}{CYAN}sigma@cyberghost{GREEN})-[{RESET}{YELLOW}~/target_acquisition{GREEN}]{RESET}")
    victim = input(f"{GREEN}└─${RESET} Target username: ").strip()
    
    if not victim:
        print(f"{RED}[✘] INVALID TARGET IDENTIFIER{RESET}")
        return
    
    print(f"\n{GREEN}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   AVAILABLE PLATFORMS:{RESET}")
    platforms = list(PLATFORMS.keys())
    for i, platform in enumerate(platforms, 1):
        print(f"   {RED}{i}. {platform.upper()}{RESET}")
    print(f"{GREEN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    choices = input(f"{GREEN}┌──({RESET}{CYAN}sigma@cyberghost{GREEN})-[{RESET}{YELLOW}~/platform_selection{GREEN}]{RESET}\n{GREEN}└─${RESET} Select platforms (comma separated, 'all' for all): ").strip().lower()
    
    if choices == 'all':
        selected_platforms = platforms
    else:
        selected_platforms = []
        for choice in choices.split(','):
            choice = choice.strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(platforms):
                    selected_platforms.append(platforms[index])
            elif choice in platforms:
                selected_platforms.append(choice)
    
    if not selected_platforms:
        print(f"{RED}[✘] NO VALID PLATFORMS SELECTED{RESET}")
        return
    
    print(f"\n{GREEN}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
    print(f"{YELLOW}   USERNAME VALIDATION:{RESET}")
    
    valid_platforms = []
    for platform in selected_platforms:
        is_valid = validate_username(victim, platform)
        status = f"{GREEN}VALID{RESET}" if is_valid else f"{RED}INVALID{RESET}"
        print(f"   {CYAN}{platform.upper()}:{RESET} {status}")
        
        if is_valid:
            valid_platforms.append(platform)
            
    print(f"{GREEN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    if not valid_platforms:
        print(f"{RED}[✘] NO VALID PLATFORMS FOR THIS USERNAME{RESET}")
        return
    
    print(f"\n{GREEN}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
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
                # For unknown status, we still try to attack the account
                existing_platforms.append(platform)
            print(f"   {CYAN}{platform.upper()}:{RESET} {status}")
        else:
            print(f"   {CYAN}{platform.upper()}:{RESET} {DARK_GREY}Check not supported{RESET}")
            existing_platforms.append(platform)
            
    print(f"{GREEN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}\n")
    
    if not existing_platforms:
        print(f"{RED}[✘] NO VALID ACCOUNTS FOUND{RESET}")
        return
    
    print(f"{GREEN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{YELLOW} TARGETING: {RED}{', '.join(existing_platforms).upper()}{RESET}{' '*(50-len(', '.join(existing_platforms)))}{GREEN}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    confirm = input(f"{GREEN}┌──({RESET}{CYAN}sigma@cyberghost{GREEN})-[{RESET}{YELLOW}~/confirmation{GREEN}]{RESET}\n{GREEN}└─${RESET} Confirm operation? (y/n): ").strip().lower()
    if confirm != 'y':
        print(f"{YELLOW}[*] OPERATION ABORTED{RESET}")
        return
    
    print(f"\n{GREEN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{RED} INITIATING WEAPONIZED REPORTING SEQUENCE                   {GREEN}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    
    for wave in range(1, 6):
        print(f"\n{GREEN}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
        print(f"{GREEN}   [🚀] {RED}WAVE {wave}/5 IN PROGRESS... {DARK_GREY}[{time.strftime('%H:%M:%S')}]{RESET}")
        print(f"{GREEN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}")
        purge(victim, existing_platforms)
        if wave < 5:
            delay = random.uniform(1, 3)
            print(f"\n{RED}[*] RECALIBRATING SYSTEMS - Next wave in {delay:.1f} seconds{RESET}")
            time.sleep(delay)
    
    print(f"\n{GREEN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{RED} OPERATION COMPLETED - 5 WAVES EXECUTED SUCCESSFULLY        {GREEN}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{DARK_GREY}Report summary generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[✘] OPERATION TERMINATED BY USER{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[✘] CRITICAL SYSTEM FAILURE: {str(e)}{RESET}")
        sys.exit(1)
