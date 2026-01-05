import sys
import time
import os
import json
# We now import external tools (dependencies)
from colorama import init, Fore, Style

# Initialize colorama. 'autoreset=True' means the color resets 
# back to white automatically after each print statement.
init(autoreset=True)

# --- THE CURRICULUM DATA ---
CURRICULUM = {
    "Phase 1": {
        "Theme": "Foundations & Style",
        "Weeks": [
            {"week": 1, "task": "Linux Grounding & Mindset", "status": "Locked"},
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
    },
    "Phase 3": {
        "Theme": "Originality & Light",
        "Weeks": [
            {"week": 9, "task": "Flagship Design", "status": "Locked"},
            {"week": 10, "task": "The Unified Theme", "status": "Locked"},
            {"week": 11, "task": "Polishing the Temple", "status": "Locked"},
            {"week": 12, "task": "Final Ascension", "status": "Locked"}
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

    def choose_path(self):
        print(f"\n{Style.BRIGHT}{Fore.MAGENTA}=== THE CROSSROADS ==={Style.RESET_ALL}")
        print("At Level 5, you must choose your discipline:")
        print(f"{Fore.GREEN}[1] Path of Earth (Automation){Style.RESET_ALL} - The Builder")
        print(f"{Fore.RED}[2] Path of Fire (Security){Style.RESET_ALL}   - The Guardian")
        print(f"{Fore.BLUE}[3] Path of Water (Quant){Style.RESET_ALL}      - The Oracle")
        
        choice = input(f"\n{Fore.CYAN}Select your destiny (1-3): {Style.RESET_ALL}")
        if choice == '1': self.path = "Automator"
        elif choice == '2': self.path = "Guardian"
        elif choice == '3': self.path = "Oracle"
        else: self.path = "Ronin"
        
        print(f"\nYou have chosen the path of the {Style.BRIGHT}{self.path}.")
        time.sleep(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def main_menu():
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.CYAN}")
    print("╔════════════════════════════════════════╗")
    print("║     DOJO OS: THE ASQ ASCENSION         ║")
    print("║   build_v3.1 | Status: ONLINE          ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Current Objective: Build the Inner Temple")
    
    print("1. Enter the Dojo (Start Curriculum)")
    print("2. View ASQ Map")
    print("3. Check Mental State (Shadow/Honor)")
    print("4. Exit")
    
    return input(f"\n{Fore.GREEN}root@dojo:~# {Style.RESET_ALL}")

def view_map(player):
    clear_screen()
    print(f"{Style.BRIGHT}{Fore.MAGENTA}=== THE 12-WEEK ASCENSION MAP ===")
    for phase, data in CURRICULUM.items():
        print(f"\n{Style.BRIGHT}{phase}: {data['Theme']}")
        for week in data['Weeks']:
            status_icon = "🔒" if week['status'] == "Locked" else "✅"
            if player.level == week['week']: status_icon = "📍"
            print(f"  {status_icon} Week {week['week']}: {week['task']}")
    input(f"\n{Fore.CYAN}[Press Enter to Return]")

def game_loop():
    clear_screen()
    print_slow("Initializing Neural Link...")
    player_name = input("Identify yourself, Initiate: ")
    player = Player(player_name)
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            print(f"\nLoading Module for Week {player.level}...")
            print_slow(f"{Fore.YELLOW}Subject: Linux Grounding & Mindset")
            print_slow("Mission: Clean the server logs using 'grep' and 'rm'...")
            time.sleep(2)
            
        elif choice == '2':
            view_map(player)
            
        elif choice == '3':
            print(f"\n{Style.BRIGHT}--- {player.name.upper()}'S SOUL ---")
            print(f"Class:  {player.path if player.path else 'Initiate'}")
            print(f"Honor:  {player.honor}/100 (Bushido)")
            print(f"Shadow: {player.shadow}/100 (Jungian Risk)")
            input("\n[Press Enter]")
            
        elif choice == '4':
            print(f"{Fore.RED}Disconnecting...")
            sys.exit()

if __name__ == "__main__":
    game_loop()
