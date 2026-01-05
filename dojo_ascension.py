import sys
import time
import os
import json
import platform # New Tool: To detect the OS
import shutil   # New Tool: To check disk space
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
    },
    "Phase 2": {
        "Theme": "Systems & Depth",
        "Weeks": [
            {"week": 5, "task": "Unit Testing & Robustness", "status": "Locked"},
            {"week": 6, "task": "Secure Coding (OWASP)", "status": "Locked"},
            {"week": 7, "task": "VPS Deployment", "status": "Locked"},
            {"week": 8, "task": "Risk Metrics Dashboard", "status": "Locked"}
        ]
    }
}

class Player:
    def __init__(self, name):
        self.name = name
        self.path = None
        self.honor = 50
        self.shadow = 0
        self.level = 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# --- MISSION LOGIC ---
def execute_week1():
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.YELLOW}=== MISSION 1: THE GROUNDING ==={Style.RESET_ALL}")
    print_slow("Objective: Verify the integrity of the Dojo environment.")
    print("Scanning system parameters...\n")
    time.sleep(1)

    # Check 1: Operating System
    system_os = platform.system()
    print(f"Checking OS... {Fore.CYAN}{system_os}{Style.RESET_ALL}")
    
    if system_os == "Linux":
        print(f"{Fore.GREEN}[PASS] The soil is fertile.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[WARNING] Non-Linux environment detected.{Style.RESET_ALL}")
        print("We will proceed, but true power requires Linux.")
    
    time.sleep(1)

    # Check 2: Disk Space
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    print(f"\nChecking Floor Space... {Fore.CYAN}{free_gb} GB Free{Style.RESET_ALL}")

    if free_gb > 5:
        print(f"{Fore.GREEN}[PASS] The Dojo has room to grow.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[FAIL] The Dojo is cluttered. Clean your disk.{Style.RESET_ALL}")

    print(f"\n{Style.BRIGHT}Mission Complete. +10 Honor gained.{Style.RESET_ALL}")
    input("\n[Press Enter to return to Meditate]")
    return 10 # Return XP/Honor

# --- MAIN LOOP ---
def main_menu():
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.CYAN}")
    print("╔════════════════════════════════════════╗")
    print("║     DOJO OS: THE ASQ ASCENSION         ║")
    print("║   build_v3.2 | Status: ONLINE          ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")
    
    print("1. Enter the Dojo (Current Mission)")
    print("2. View ASQ Map")
    print("3. Check Mental State")
    print("4. Exit")
    
    return input(f"\n{Fore.GREEN}root@dojo:~# {Style.RESET_ALL}")

def game_loop():
    clear_screen()
    player_name = input("Identify yourself, Initiate: ")
    player = Player(player_name)
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            if player.level == 1:
                xp = execute_week1()
                player.honor += xp
            else:
                print("Module locked or under construction.")
                time.sleep(2)
            
        elif choice == '2':
            # Simplified map view for brevity
            print(f"\n{Fore.MAGENTA}Current Phase: {CURRICULUM['Phase 1']['Theme']}")
            input("[Enter]")
            
        elif choice == '3':
            print(f"\n{Style.BRIGHT}--- {player.name.upper()} ---")
            print(f"Honor:  {player.honor}")
            input("[Enter]")
            
        elif choice == '4':
            print(f"{Fore.RED}Disconnecting...")
            sys.exit()

if __name__ == "__main__":
    game_loop()
