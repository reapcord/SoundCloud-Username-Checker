import requests
import json
import os
import time
import random
from colorama import Fore, Back, Style, init
from datetime import datetime

init()

VERSION = "@demiourgia v1.0"
CONFIG_FILE = "config.json"

THEMES = {
    "Demiourgia": {
        "primary": Fore.YELLOW,
        "secondary": Fore.LIGHTYELLOW_EX,
        "success": Fore.LIGHTGREEN_EX,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "info": Fore.LIGHTCYAN_EX,
        "text": Fore.LIGHTWHITE_EX,
        "highlight": Fore.WHITE,
        "accent": Style.BRIGHT + Fore.YELLOW,
        "banner": Style.BRIGHT + Fore.YELLOW  
    },
    "Dystopia": {
        "primary": Fore.LIGHTMAGENTA_EX,
        "secondary": Fore.LIGHTRED_EX,
        "success": Fore.LIGHTGREEN_EX,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "info": Fore.LIGHTCYAN_EX,
        "text": Fore.LIGHTWHITE_EX,
        "highlight": Fore.LIGHTMAGENTA_EX,
        "accent": Style.BRIGHT + Fore.LIGHTMAGENTA_EX,
        "banner": Style.BRIGHT + Fore.LIGHTMAGENTA_EX 
    },
    "Utopia": {
        "primary": Fore.LIGHTCYAN_EX,
        "secondary": Fore.LIGHTBLUE_EX,
        "success": Fore.LIGHTGREEN_EX,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "info": Fore.LIGHTMAGENTA_EX,
        "text": Fore.LIGHTWHITE_EX,
        "highlight": Fore.LIGHTCYAN_EX,
        "accent": Style.BRIGHT + Fore.LIGHTCYAN_EX,
        "banner": Style.BRIGHT + Fore.LIGHTCYAN_EX  
    }
}

settings = {
    "webhook": "",
    "webhook_name": "SC Checker",
    "webhook_pfp": "",
    "theme": "Demiourgia"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                saved = json.load(f)
                settings.update(saved)
        except:
            pass

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f)

def get_theme():
    return THEMES[settings["theme"]]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    theme = get_theme()
    clear()
    
    banner = f"""
{theme['banner']}
______ ________  ________ _____ _   _______ _____ _____  ___  
|  _  \  ___|  \/  |_   _|  _  | | | | ___ \  __ \_   _|/ _ \ 
| | | | |__ | .  . | | | | | | | | | | |_/ / |  \/ | | / /_\ \\
| | | |  __|| |\/| | | | | | | | | | |    /| | __  | | |  _  |
| |/ /| |___| |  | |_| |_\ \_/ / |_| | |\ \| |_\ \_| |_| | | |
|___/ \____/\_|  |_/\___/ \___/ \___/\_| \_|\____/\___/\_| |_/
{Style.RESET_ALL}"""
    
    print(banner)
    title = f"{theme['accent']}   {theme['text']}{VERSION}"
    print("\n" + " " * 15 + title + Style.RESET_ALL)
    print(" " * 20 + f"{theme['text']}{theme['secondary']}@unburdening{Style.RESET_ALL}\n")

def print_header(text):
    theme = get_theme()
    print(f"\n{theme['primary']}               {text}               {Style.RESET_ALL}\n")

def print_menu_item(number, text):
    theme = get_theme()
    print(f"  {theme['primary']}[{number}] {theme['text']}{text}{Style.RESET_ALL}")

def print_status(text, status="info"):
    theme = get_theme()
    icons = {
        "info": "i",
        "success": "✓",
        "error": "✗",
        "warning": "⚠"
    }
    color = theme.get(status, theme["text"])
    print(f"  {color}{icons.get(status, '')} {theme['text']}{text}{Style.RESET_ALL}")

def setup_webhook():
    theme = get_theme()
    show_banner()
    print_header("Webhook Configuration")
    
    print_status("Leave blank to skip webhook setup", "info")
    
    webhook = input(f"\n  {theme['secondary']}➜ Discord Webhook URL: {theme['highlight']}")
    
    if webhook:
        settings["webhook"] = webhook
        name = input(f"  {theme['secondary']}➜ Webhook Name (default: SC Checker): {theme['highlight']}")
        settings["webhook_name"] = name if name else "SC Checker"
        
        pfp = input(f"  {theme['secondary']}➜ Webhook Avatar URL: {theme['highlight']}")
        settings["webhook_pfp"] = pfp if pfp else ""
        
        print_status("Webhook configured successfully!", "success")
    else:
        settings["webhook"] = ""
        print_status("Skipping webhook setup", "info")
    
    time.sleep(1.5)
    save_config()

def change_theme():
    theme = get_theme()
    show_banner()
    print_header("Theme Selection")
    
    print(f"\n  {theme['text']}Current theme: {theme['accent']}{settings['theme']}{Style.RESET_ALL}\n")
    
    for i, name in enumerate(THEMES.keys(), 1):
        print_menu_item(i, name)
    
    print_menu_item(0, "Go back")
    
    try:
        choice = input(f"\n  {theme['secondary']}➜ Select theme: {theme['highlight']}")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(THEMES):
                theme_name = list(THEMES.keys())[choice-1]
                settings["theme"] = theme_name
                save_config()
                print_status(f"Theme changed to {theme_name}!", "success")
            elif choice != 0:
                print_status("Invalid selection", "error")
    except:
        print_status("Please enter a number", "error")
    
    time.sleep(1)

def send_webhook(username, stats):
    if not settings["webhook"]:
        return
    
    theme = get_theme()
    color = 0xFFD700 if settings["theme"] == "Demiourgia" else 0x9B59B6 if settings["theme"] == "Dystopia" else 0x3498DB
    
    embed = {
        "title": "✅ Available SoundCloud Username",
        "description": f"```\n{username}\n```\n[Profile Link](https://soundcloud.com/{username})",
        "color": color,
        "fields": [
            {"name": "Total Checked", "value": f"`{stats['total']}`", "inline": True},
            {"name": "Available", "value": f"`{stats['available']}`", "inline": True},
            {"name": "Taken", "value": f"`{stats['taken']}`", "inline": True}
        ],
        "footer": {
            "text": f"{VERSION} • {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}"
        }
    }
    
    payload = {
        "embeds": [embed],
        "username": settings["webhook_name"],
        "avatar_url": settings["webhook_pfp"] or None
    }
    
    try:
        requests.post(settings["webhook"], json=payload, timeout=10)
    except:
        pass

def check_username(username, stats):
    theme = get_theme()
    url = f"https://soundcloud.com/{username}"
    
    try:
        time.sleep(random.uniform(0.3, 1.2))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 404:
            stats["available"] += 1
            print(f"  {theme['success']}✓ {theme['text']}{url.ljust(40)} {theme['success']}AVAILABLE{Style.RESET_ALL}")
            with open("available.txt", "a") as f:
                f.write(f"{url}\n")
            send_webhook(username, stats)
        elif r.status_code == 200:
            stats["taken"] += 1
            print(f"  {theme['error']}✗ {theme['text']}{url.ljust(40)} {theme['error']}TAKEN{Style.RESET_ALL}")
        else:
            stats["taken"] += 1
            print(f"  {theme['warning']}⚠ {theme['text']}{url.ljust(40)} {theme['warning']}UNKNOWN ({r.status_code}){Style.RESET_ALL}")
            
    except Exception as e:
        stats["taken"] += 1
        print(f"  {theme['error']}⚠ {theme['text']}{url.ljust(40)} {theme['error']}ERROR ({str(e)}){Style.RESET_ALL}")

def start_checking():
    theme = get_theme()
    stats = {"total": 0, "available": 0, "taken": 0}
    
    show_banner()
    print_header("Username Checker")
    
    if not os.path.exists("wordlist.txt"):
        print_status("wordlist.txt not found!", "error")
        time.sleep(2)
        return
    
    with open("wordlist.txt", "r") as f:
        usernames = [line.strip() for line in f if line.strip()]
    
    if not usernames:
        print_status("No usernames found in wordlist.txt", "error")
        time.sleep(2)
        return
    
    stats["total"] = len(usernames)
    
    print(f"\n  {theme['text']}Loaded {theme['accent']}{stats['total']} {theme['text']}usernames")
    print(f"  {theme['info']}ℹ Press CTRL+C to stop\n{Style.RESET_ALL}")
    
    try:
        for username in usernames:
            check_username(username, stats)
    except KeyboardInterrupt:
        print(f"\n  {theme['warning']}⚠ Stopped by user{Style.RESET_ALL}")
    
    print_header("Results")
    print(f"\n  {theme['text']}Total Checked: {theme['accent']}{stats['total']}")
    print(f"  {theme['success']}✓ Available: {stats['available']}")
    print(f"  {theme['error']}✗ Taken: {stats['taken']}{Style.RESET_ALL}")
    
    if stats["available"] > 0:
        print(f"\n  {theme['info']}ℹ Available usernames saved to {theme['accent']}available.txt{Style.RESET_ALL}")
    
    input(f"\n  {theme['secondary']}➜ Press Enter to continue...{Style.RESET_ALL}")

def main_menu():
    load_config()
    
    while True:
        theme = get_theme()
        show_banner()
        print_header("Main Menu")
        
        print_menu_item(1, "Start Checking Usernames")
        print_menu_item(2, "Setup Discord Webhook")
        print_menu_item(3, "Change Theme")
        print_menu_item(4, "Exit")
        
        choice = input(f"\n  {theme['secondary']}➜ Select option: {theme['highlight']}")
        
        if choice == "1":
            start_checking()
        elif choice == "2":
            setup_webhook()
        elif choice == "3":
            change_theme()
        elif choice == "4":
            clear()
            print(f"\n  {get_theme()['primary']}@unburdening{Style.RESET_ALL}")
            time.sleep(1)
            exit()
        else:
            print_status("Invalid choice", "error")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()