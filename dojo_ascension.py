import sys
import time
import os
import platform 
import shutil   
import requests # New Tool: The Messenger
from colorama import init, Fore, Style

init(autoreset=True)

# --- CONFIGURATION ---
CURRICULUM = {
    "Phase 1": {
        "Theme": "Foundations & Style",
        "Weeks": [
            {"week": 1, "task": "Linux Grounding & Mindset", "status": "Unlocked"},
            {"week": 2, "task": "Automation v1 & Data Fetch", "status": "Locked"},
            {"week": 3, "task": "Security Toolkit v1", "status": "Locked"},
            {"week": 4, "task": "Quant Backtester v1", "status": "Locked"}
        ]
    }
}

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1 # Starts at Week 1
        self.honor = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# --- MISSIONS ---
def execute_week1():
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.YELLOW}=== MISSION 1: THE GROUNDING ==={Style.RESET_ALL}")
    print("Scanning system parameters...")
    time.sleep(1)

    # Check OS
    if platform.system() == "Linux":
        print(f"{Fore.GREEN}[PASS] Linux Kernel detected.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[WARNING] Non-Linux environment.{Style.RESET_ALL}")
    
    # Check Space
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb > 5:
        print(f"{Fore.GREEN}[PASS] Storage Check: {free_gb}GB Free.{Style.RESET_ALL}")
    
    input("\n[Mission Complete. Press Enter]")
    return 1 # Returns Level increment

def execute_week2():
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.BLUE}=== MISSION 2: THE DATA LINK ==={Style.RESET_ALL}")
    print_slow("Objective: Establish a link to the CoinGecko Financial Grid.")
    time.sleep(1)
    
    target_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    print(f"\nTargeting: {Fore.CYAN}{target_url}{Style.RESET_ALL}")
    print("Sending Request...")
    
    try:
        # The Magic Spell (Request)
        response = requests.get(target_url)
        
        # Check if the door opened (Status Code 200 = OK)
        if response.status_code == 200:
            data = response.json()
            price = data['bitcoin']['usd']
            print(f"\n{Fore.GREEN}[SUCCESS] Connection Established!{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}>> BTC Price: ${price}{Style.RESET_ALL}")
            print_slow("\n\"The Oracle sees all flows.\"")
            input("\n[Mission Complete. Press Enter]")
            return 1
        else:
            print(f"{Fore.RED}[FAIL] Server rejected us. Code: {response.status_code}{Style.RESET_ALL}")
            input("[Press Enter]")
            return 0
            
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Connection Failed: {e}{Style.RESET_ALL}")
        input("[Press Enter]")
        return 0

# --- MAIN LOOP ---
def main_menu(player):
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.CYAN}DOJO OS v3.3 | Level: {player.level}{Style.RESET_ALL}")
    print(f"1. Start Next Mission (Week {player.level})")
    print("2. Exit")
    return input(f"\n{Fore.GREEN}root@dojo:~# {Style.RESET_ALL}")

def game_loop():
    clear_screen()
    player = Player("Initiate")
    
    while True:
        choice = main_menu(player)
        
        if choice == '1':
            if player.level == 1:
                level_up = execute_week1()
                player.level += level_up
            elif player.level == 2:
                level_up = execute_week2()
                player.level += level_up
            else:
                print("Content under construction. You have reached the edge of the known world.")
                time.sleep(3)
                
        elif choice == '2':
            print("Disconnecting...")
            sys.exit()

if __name__ == "__main__":
    game_loop()
