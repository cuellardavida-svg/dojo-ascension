#!/usr/bin/env python3
"""
DOJO ASCENSION v5.0 — Dynamic Mission Engine + Reflection System
A terminal RPG that teaches Python, Git, and JSON for SolarPunk contributor qualification.
Missions are data-driven (missions.json). Learning is paired with Uta Hagen reflection.

Author: alucardzagreus-boop / SolarPunk HackNet
Pedagogical Model: Connectivism, Progressive Disclosure, Deliberate Practice
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

    class _Dummy:
        def __getattr__(self, name): return ""
    Fore = Style = Back = _Dummy()

# ─────────────────────────────────────────────
#  CONFIGURATION & PATHS
# ─────────────────────────────────────────────


def get_state_paths():
    """Resolve save and journal paths, allowing per-user overrides on shared machines."""
    data_dir = Path(
        os.environ.get(
            "DOJO_DATA_DIR", str(
                Path.home() / ".dojo_ascension"))).expanduser()
    data_dir.mkdir(parents=True, exist_ok=True)

    save_file = Path(
        os.environ.get(
            "DOJO_SAVE_FILE", str(
                data_dir / "dojo_save.json"))).expanduser()
    journal_file = Path(
        os.environ.get(
            "DOJO_JOURNAL_FILE", str(
                data_dir / "dojo_journal_data.json"))).expanduser()

    if not save_file.is_absolute():
        save_file = data_dir / save_file
    if not journal_file.is_absolute():
        journal_file = data_dir / journal_file

    save_file.parent.mkdir(parents=True, exist_ok=True)
    journal_file.parent.mkdir(parents=True, exist_ok=True)
    return save_file, journal_file


SAVE_FILE, JOURNAL_FILE = get_state_paths()
MISSIONS_FILE = Path(__file__).parent / "missions" / "missions.json"

UTA_HAGEN_QUESTIONS = [
    "Who am I in this circumstance?",
    "What are my circumstances?",
    "What do I want?",
    "Why do I want it?",
    "When is it?",
    "Where is it?",
    "What must I overcome?",
    "How will I accomplish my objective?",
    "What have I discovered?"
]


def iso_now():
    """Return an ISO timestamp for learner-state and impact metrics."""
    return datetime.now().isoformat()

# ─────────────────────────────────────────────
#  UI & FORMATTING
# ─────────────────────────────────────────────


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_slow(text, speed=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


def divider(char="─", width=60, color=Fore.CYAN):
    print(f"{color}{char * width}{Style.RESET_ALL}")


def header(title, color=Fore.CYAN):
    divider("═", 60, color)
    print(f"{color}{Style.BRIGHT}  {title}{Style.RESET_ALL}")
    divider("═", 60, color)


def lesson_box(text):
    lines = text.strip().split("\n")
    print(f"\n{Back.BLUE}{Fore.WHITE}{'  LESSON  ':^60}{Style.RESET_ALL}")
    for line in lines:
        print(f"  {Fore.CYAN}{line}{Style.RESET_ALL}")
    print()


def challenge_box(text):
    lines = text.strip().split("\n")
    print(f"\n{Back.GREEN}{Fore.BLACK}{'  CHALLENGE  ':^60}{Style.RESET_ALL}")
    for line in lines:
        print(f"  {Fore.GREEN}{line}{Style.RESET_ALL}")
    print()


def hint_box(text):
    print(f"\n  {Fore.YELLOW}💡 HINT: {text}{Style.RESET_ALL}\n")


def wait():
    input(f"\n{Fore.WHITE}[ Press ENTER to continue... ]{Style.RESET_ALL}")

# ─────────────────────────────────────────────
#  MISSION LOADING
# ─────────────────────────────────────────────


def load_missions():
    """Load missions from the mission index or fallback to the mission files folder."""
    mission_dir = MISSIONS_FILE.parent

    if MISSIONS_FILE.exists():
        try:
            with open(MISSIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('missions', [])
        except (OSError, json.JSONDecodeError) as e:
            print(f"{Fore.RED}Error loading missions: {e}{Style.RESET_ALL}")
            sys.exit(1)

    mission_files = sorted(mission_dir.glob("mission*.json"))
    if not mission_files:
        print(f"{Fore.RED}Error: no mission files found in {mission_dir}{Style.RESET_ALL}")
        sys.exit(1)

    missions = []
    for mission_path in mission_files:
        try:
            with open(mission_path, 'r', encoding='utf-8') as f:
                missions.append(json.load(f))
        except (OSError, json.JSONDecodeError) as e:
            print(f"{Fore.RED}Error loading mission file {mission_path}: {e}{Style.RESET_ALL}")
            sys.exit(1)

    return missions

# ─────────────────────────────────────────────
#  PLAYER CLASS
# ─────────────────────────────────────────────


class Player:
    RANK_THRESHOLDS = [
        (0, "Initiate"),
        (50, "Apprentice"),
        (150, "Practitioner"),
        (300, "Adept"),
        (600, "Expert"),
        (1000, "Co-Architect")
    ]

    def __init__(self, name, honor=0, completed=None, skills=None):
        self.name = name
        self.honor = honor
        self.completed = set(completed or [])
        self.skills = skills or {
            "python": 0,
            "git": 0,
            "json": 0,
            "architecture": 0,
            "review": 0
        }
        self.first_session_at = None
        self.last_session_at = None
        self.last_mission_at = None
        self.session_count = 0
        self.session_log = []
        self.load_state()
        self.start_session()

    def get_rank(self):
        """Competency-based rank"""
        for threshold, title in reversed(self.RANK_THRESHOLDS):
            if self.honor >= threshold:
                return title
        return "Initiate"

    def add_honor(self, points, skill=None):
        self.honor += points
        self.last_mission_at = iso_now()
        print(
            f"\n{Fore.YELLOW}⚡ +{points} HONOR POINTS | Total: {self.honor}{Style.RESET_ALL}")

        if skill and skill in self.skills:
            self.skills[skill] += 1
            print(
                f"{Fore.CYAN}↑ {skill.upper()} now Level "
                f"{self.skills[skill]}{Style.RESET_ALL}"
            )

        self.save_state()

    def save_state(self, quiet=False):
        """Persist player progress to JSON"""
        state = {
            "name": self.name,
            "honor": self.honor,
            "completed": list(self.completed),
            "skills": self.skills,
            "first_session_at": self.first_session_at,
            "last_session_at": self.last_session_at,
            "last_mission_at": self.last_mission_at,
            "session_count": self.session_count,
            "session_log": self.session_log,
            "last_save": iso_now()
        }
        try:
            SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            if not quiet:
                print(f"{Fore.GREEN}✓ Progress saved to {SAVE_FILE}{Style.RESET_ALL}")
        except OSError as e:
            print(f"{Fore.RED}Error saving progress: {e}{Style.RESET_ALL}")

    def load_state(self):
        """Load player progress from JSON"""
        if SAVE_FILE.exists():
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self.name = state.get("name", self.name)
                self.honor = state.get("honor", 0)
                self.completed = set(state.get("completed", []))
                self.skills = state.get("skills", self.skills)
                self.first_session_at = state.get("first_session_at")
                self.last_session_at = state.get("last_session_at")
                self.last_mission_at = state.get("last_mission_at")
                self.session_count = state.get("session_count", 0)
                self.session_log = state.get("session_log", [])
            except (OSError, json.JSONDecodeError):
                pass  # Default to new player if corrupted

    def start_session(self):
        """Record a learner session for retention and cohort reporting."""
        current = iso_now()
        if not self.first_session_at:
            self.first_session_at = current
        self.last_session_at = current
        self.session_count += 1
        # Keep a bounded recent log so cohort metrics stay useful without
        # allowing save files to grow forever on long-running installs.
        self.session_log = (self.session_log + [current])[-60:]
        self.save_state(quiet=True)

# ─────────────────────────────────────────────
#  UTA HAGEN JOURNAL SYSTEM
# ─────────────────────────────────────────────


def load_journal_data():
    """Load journal entries from JSON"""
    if JOURNAL_FILE.exists():
        try:
            return json.loads(JOURNAL_FILE.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def save_journal_data(data):
    """Persist journal to JSON"""
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')


def get_practice_chain(data):
    """Calculate consecutive practice days (replaces 'streak')"""
    chain = 0
    current = datetime.now().date()
    while current.strftime("%Y-%m-%d") in data:
        chain += 1
        current -= timedelta(days=1)
    return chain


def journal_reflection(mission_id, mission_title, player):
    """Optional post-mission reflection using Uta Hagen questions"""
    choice = input(
        f"\n{Fore.CYAN}Would you like to journal about this mission? "
        f"(y/n): {Style.RESET_ALL}"
    ).strip().lower()
    if choice != 'y':
        return

    data = load_journal_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if today in data:
        print(f"{Fore.YELLOW}You already journaled today.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.BLUE}{'─' * 60}")
    print("  UTA HAGEN SYSTEMS THINKING JOURNAL")
    print(f"  Mission: {mission_title}")
    print(f"{'─' * 60}{Style.RESET_ALL}\n")

    answers = {}
    for i, question in enumerate(UTA_HAGEN_QUESTIONS, 1):
        print(f"{Fore.WHITE}[{i}/9] {question}{Style.RESET_ALL}")
        answer = input(f"{Fore.GREEN}→ {Style.RESET_ALL}").strip()
        answers[question] = answer

    data[today] = {
        "timestamp": datetime.now().isoformat(),
        "mission_id": mission_id,
        "mission_title": mission_title,
        "player_rank": player.get_rank(),
        "answers": answers
    }
    save_journal_data(data)

    print(
        f"\n{Fore.GREEN}✓ Reflection saved to {JOURNAL_FILE}"
        f"{Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}Practice Chain: {get_practice_chain(data)} days{Style.RESET_ALL}")


def view_journal(data):
    """Display past journal entries"""
    if not data:
        print(
            f"\n{Fore.YELLOW}No journal entries yet. Start by journaling "
            f"after a mission!{Style.RESET_ALL}"
        )
        return

    clear_screen()
    header("REFLECTION JOURNAL — PAST ENTRIES", Fore.BLUE)

    print(
        f"{Fore.CYAN}Practice Chain: {get_practice_chain(data)} "
        f"consecutive days{Style.RESET_ALL}\n"
    )

    for date in sorted(data.keys(), reverse=True)[:10]:
        entry = data[date]
        print(
            f"{Fore.YELLOW}{date}{Style.RESET_ALL} — "
            f"{entry.get('mission_title', 'Unknown')}"
        )
        for question, answer in entry.get("answers", {}).items():
            print(f"  {Fore.WHITE}Q: {question}{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}A: {answer[:80]}...{Style.RESET_ALL}" if len(
                answer) > 80 else f"  {Fore.GREEN}A: {answer}{Style.RESET_ALL}")
        print()

    wait()

# ─────────────────────────────────────────────
#  MISSION EXECUTION
# ─────────────────────────────────────────────


def validate_answer(user_input, answer, answertype="exact"):
    """
    Validate user answer against expected answer(s).
    
    answertype can be:
    - "exact": exact match (case-insensitive, whitespace-normalized)
    - "contains": substring match (case-insensitive)
    - default: treat as contains
    """
    user = user_input.lower().strip()
    
    # Handle list of acceptable answers
    if isinstance(answer, list):
        for ans in answer:
            if validate_answer(user_input, ans, answertype):
                return True
        return False
    
    answer_str = str(answer).lower().strip()
    
    if answertype == "exact":
        return user == answer_str
    else:  # "contains" or default
        return answer_str in user


def run_code_challenge(prompt, answer, answertype="exact", hint=""):
    """Generic code challenge runner"""
    challenge_box(prompt)
    if hint:
        hint_box(hint)
    print(
        f"  {Fore.WHITE}TIP: Try this in VSCode — create a .py file and "
        f"run it there!{Style.RESET_ALL}"
    )
    print(
        f"\n  {Fore.YELLOW}→ Type your answer, 'hint', or 'skip':"
        f"{Style.RESET_ALL}\n"
    )

    attempts = 0
    while True:
        try:
            user_input = input(f"  {Fore.GREEN}>>> {Style.RESET_ALL}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to menu...")
            return False

        if user_input.lower() == 'skip':
            print(f"  {Fore.YELLOW}Skipped. Revisit anytime.{Style.RESET_ALL}")
            return False
        if user_input.lower() == 'hint':
            hint_box(hint or "Think about what the challenge is asking.")
            continue

        attempts += 1
        result = validate_answer(user_input, answer, answertype)

        if result is True:
            print(f"\n  {Fore.GREEN}{Style.BRIGHT}✓ CORRECT!{Style.RESET_ALL}")
            if attempts == 1:
                print(
                    f"  {Fore.YELLOW}Bonus: First try! +5 honor{Style.RESET_ALL}")
            return True
        else:
            print(
                f"\n  {Fore.RED}✗ Not quite. Try again.{Style.RESET_ALL}"
            )
            if attempts >= 3:
                print(
                    f"  {Fore.YELLOW}Hint (after 3 tries): {hint}"
                    f"{Style.RESET_ALL}"
                )


def execute_mission(mission_data, player, missions=None):
    """Execute a mission from the data structure"""
    mid = mission_data["id"]
    num = mission_data["number"]
    title = mission_data["title"]
    philosophy = mission_data["philosophy"]
    economics = mission_data["economics"]
    lesson = mission_data.get("lesson", mission_data.get("techconcept", ""))
    challenge = mission_data["challenge"]
    answer = mission_data["answer"]
    answertype = mission_data.get("answertype", "contains")
    skill = mission_data["skill"]
    honor_base = mission_data.get("honorreward", mission_data.get("honor_base", 20))
    hint = mission_data.get("hint", "")

    header(f"MISSION {num}: {title}", Fore.CYAN)

    print(f"{Fore.BLUE}📜 PHILOSOPHICAL ANCHOR:{Style.RESET_ALL}")
    print(f"  {philosophy}\n")

    print(f"{Fore.YELLOW}🌐 ECONOMIC PARALLEL:{Style.RESET_ALL}")
    print(f"  {economics}\n")

    print(f"{Fore.CYAN}💻 TECHNICAL CONCEPT:{Style.RESET_ALL}")
    print(f"  {lesson}\n")

    wait()

    won = run_code_challenge(
        challenge,
        answer,
        answertype,
        hint)

    if won:
        missions = missions or load_missions()
        first_completion = mid not in player.completed
        player.completed.add(mid)
        if first_completion:
            player.add_honor(honor_base, skill)
            print(f"\n{Fore.CYAN}✓ Mission {num} Complete!{Style.RESET_ALL}")
        else:
            player.last_mission_at = iso_now()
            player.save_state(quiet=True)
            print(
                f"\n{Fore.CYAN}✓ Mission {num} reviewed again."
                f"{Style.RESET_ALL}"
            )
            print(
                f"{Fore.YELLOW}Honor is only awarded on the first completion so "
                f"your progress stays trustworthy for pilots and cohorts."
                f"{Style.RESET_ALL}"
            )
        next_mission = get_next_mission(missions=missions, completed_ids=player.completed)
        if next_mission:
            print(
                f"{Fore.MAGENTA}Next step: Mission {next_mission['number']} — "
                f"{next_mission['title']}.{Style.RESET_ALL}"
            )
        print(
            f"{Fore.BLUE}Pathway track: {get_pathway_stage(player, missions)}"
            f"{Style.RESET_ALL}"
        )
        journal_reflection(mid, title, player)
        return True
    else:
        print(
            f"\n{Fore.YELLOW}Practice makes perfect. Return when you're ready."
            f"{Style.RESET_ALL}"
        )
        return False


def get_next_mission(missions, completed_ids):
    """Return the next unfinished mission in curriculum order."""
    return next((m for m in missions if m["id"] not in completed_ids), None)


def get_pathway_stage(player, missions):
    """Translate raw progress into a learner-facing pathway."""
    completed = len(player.completed)
    total = len(missions)
    if completed < min(3, total):
        return "Beginner confidence"
    if completed < min(6, total):
        return "Contributor readiness"
    if completed < total:
        return "Mission authoring"
    return "Facilitator readiness"

# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────


def show_dashboard(player, missions):
    """Display player progress and skill specialization"""
    clear_screen()
    header("DOJO ASCENSION — PROGRESS DASHBOARD", Fore.CYAN)

    print(
        f"\n{Fore.WHITE}Player    : {Style.BRIGHT}{player.name}"
        f"{Style.RESET_ALL}"
    )
    print(f"{Fore.WHITE}Rank      : {Fore.YELLOW}{player.get_rank()}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Honor     : {Fore.YELLOW}{player.honor} pts{Style.RESET_ALL}")

    divider()
    print(f"\n{Fore.CYAN}SKILL SPECIALIZATION:{Style.RESET_ALL}")
    for skill, level in sorted(player.skills.items(), key=lambda x: -x[1]):
        bar = "█" * level + "░" * (5 - level)
        print(f"  {skill.upper():<15} [{bar}] {level}/5")

    divider()
    print(f"\n{Fore.CYAN}MISSION PROGRESS:{Style.RESET_ALL}")
    print(f"  Completed: {len(player.completed)}/{len(missions)}")

    completed_skills = set()
    for m in missions:
        if m["id"] in player.completed:
            completed_skills.add(m["skill"])

    print(
        f"  Skills Mastered: {', '.join(sorted(completed_skills)) or 'None yet'}\n"
    )

    journal_data = load_journal_data()
    chain = get_practice_chain(journal_data)
    next_mission = get_next_mission(missions, player.completed)

    divider()
    print(f"\n{Fore.MAGENTA}MOMENTUM & PATHWAY:{Style.RESET_ALL}")
    print(f"  Pathway Track : {get_pathway_stage(player, missions)}")
    print(f"  Sessions Logged: {player.session_count}")
    print(f"  Practice Chain: {chain} day(s)")
    if next_mission:
        print(
            f"  Next Mission  : {next_mission['number']}. "
            f"{next_mission['title']} ({next_mission['skill']})"
        )
    else:
        print("  Next Mission  : Completed core pathway — mentor, document, or author a mission")
    if player.last_mission_at:
        print(f"  Last Win      : {player.last_mission_at}")
    print("  Cohort Prompt : Invite a peer or facilitator to join your next session")

    # Show next rank threshold
    next_thresholds = [
        t for t,
        _ in Player.RANK_THRESHOLDS if t > player.honor]
    if next_thresholds:
        next_t = next_thresholds[0]
        bar_width = 30
        filled = int((player.honor / next_t) * bar_width)
        print(f"{Fore.YELLOW}Next Rank Progress:{Style.RESET_ALL}")
        print(
            f"  [{'█' * filled}{'░' * (bar_width - filled)}] {player.honor}/{next_t} honor")

    wait()

# ─────────────────────────────────────────────
#  CHRONICLE TIPS
# ─────────────────────────────────────────────


def chronicle_tips(player, missions, journal_data):
    """Analyse session history and surface personalised practice tips."""
    clear_screen()
    header("CHRONICLE TIPS — PERSONALISED INSIGHTS", Fore.MAGENTA)

    tips = []

    # ── Journal / practice-chain analysis ──────────────────────────────────
    chain = get_practice_chain(journal_data)
    total_entries = len(journal_data)

    if total_entries == 0:
        tips.append((
            "📔 Start your reflection journal",
            "You haven't written any journal entries yet. After each mission "
            "choose 'y' to journal. Even one sentence per session compounds "
            "into powerful self-knowledge over time."
        ))
    elif chain == 0:
        tips.append((
            "🔄 Rebuild your practice chain",
            f"You have {total_entries} past journal entr"
            f"{'y' if total_entries == 1 else 'ies'} but your current chain "
            "is broken. Return daily — even a 5-minute session counts."
        ))
    elif chain < 3:
        tips.append((
            f"🌱 Chain growing: {chain} day(s) — keep going!",
            "Consistent micro-practice beats long irregular sessions. "
            "Aim to reach a 7-day chain to build a lasting habit."
        ))
    else:
        tips.append((
            f"🔥 Practice chain: {chain} day(s) — excellent consistency!",
            "You are showing up regularly. Now focus on depth: read your old "
            "journal entries and look for recurring blockers to work through."
        ))

    # ── Mission-completion analysis ─────────────────────────────────────────
    total_missions = len(missions)
    done = len(player.completed)
    remaining = [m for m in missions if m["id"] not in player.completed]

    if done == 0:
        tips.append((
            "🚀 Begin your first mission",
            "No missions completed yet — select option 1 from the menu to "
            "start with Mission 1: System Grounding."
        ))
    elif done == total_missions:
        tips.append((
            "🏆 All missions complete — go deeper",
            "You've finished every available mission. Re-read your journal "
            "entries, contribute a new mission JSON to the community, or "
            "mentor another practitioner."
        ))
    else:
        next_m = remaining[0]
        tips.append((
            f"⚔️  Next frontier: Mission {next_m['number']} — {next_m['title']}",
            f"You've completed {done}/{total_missions} missions. "
            f"Your next challenge focuses on the '{next_m['skill'].upper()}' "
            "skill — tackle it in your next session."
        ))

    # ── Skill-gap analysis ──────────────────────────────────────────────────
    skill_levels = player.skills
    if skill_levels:
        weakest_skill = min(skill_levels, key=lambda s: skill_levels[s])
        weakest_level = skill_levels[weakest_skill]
        strongest_skill = max(skill_levels, key=lambda s: skill_levels[s])
        strongest_level = skill_levels[strongest_skill]

        if weakest_level == 0:
            tips.append((
                f"📉 Untouched skill: {weakest_skill.upper()}",
                f"Your {weakest_skill.upper()} skill is at 0. Look for "
                f"missions tagged '{weakest_skill}' to start building it."
            ))
        elif strongest_level - weakest_level >= 2:
            tips.append((
                f"⚖️  Balance your skills: lift {weakest_skill.upper()} "
                f"(lvl {weakest_level}) toward {strongest_skill.upper()} "
                f"(lvl {strongest_level})",
                "A well-rounded practitioner avoids over-specialisation. "
                f"Seek out {weakest_skill.upper()}-tagged missions to close "
                "the gap."
            ))
        else:
            tips.append((
                f"✅ Skills are balanced (strongest: {strongest_skill.upper()} "
                f"lvl {strongest_level})",
                "Keep progressing evenly. Each new mission advances a "
                "specific skill — check the mission list to plan ahead."
            ))

    # ── Reflection-quality nudge (based on journal content length) ──────────
    if journal_data:
        short_entries = sum(
            1 for entry in journal_data.values()
            if all(len(a) < 20 for a in entry.get("answers", {}).values())
        )
        if short_entries > 0:
            tips.append((
                "✍️  Go deeper in your reflections",
                f"{short_entries} of your journal entr"
                f"{'y has' if short_entries == 1 else 'ies have'} very short "
                "answers. The Uta Hagen questions reward specificity — aim "
                "for at least one full sentence per question."
            ))

    # ── Honor-rank nudge ────────────────────────────────────────────────────
    next_thresholds = [
        (t, title)
        for t, title in Player.RANK_THRESHOLDS
        if t > player.honor
    ]
    if next_thresholds:
        next_t, next_title = next_thresholds[0]
        gap = next_t - player.honor
        tips.append((
            f"🎖️  {gap} honor until rank: {next_title}",
            f"You are at {player.honor} honor. Keep completing missions to "
            "reach the next rank and unlock new challenges."
        ))

    # ── Render ──────────────────────────────────────────────────────────────
    print(
        f"\n{Fore.CYAN}Session snapshot for {Style.BRIGHT}{player.name}"
        f"{Style.RESET_ALL}{Fore.CYAN} | "
        f"{done}/{total_missions} missions | "
        f"{total_entries} journal entr"
        f"{'y' if total_entries == 1 else 'ies'} | "
        f"chain {chain} day(s){Style.RESET_ALL}\n"
    )
    divider()

    for i, (headline, detail) in enumerate(tips, 1):
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}[{i}] {headline}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{detail}{Style.RESET_ALL}")

    divider()
    wait()


# ─────────────────────────────────────────────
#  VSCODE GUIDE
# ─────────────────────────────────────────────


def show_vscode_guide():
    """Display VSCode integration instructions"""
    clear_screen()
    header("VSCODE INTEGRATION GUIDE", Fore.GREEN)
    print("""
  SETUP (one-time):
  ─────────────────
  1. Install VSCode: https://code.visualstudio.com
  2. Extensions (Ctrl+Shift+X):
     • Python by Microsoft
     • GitLens (Git superpowers)
     • Prettier (JSON formatting)
     • Python Indent (auto-indentation)

  OFFICIAL TUTORIALS (pair with missions):
  ───────────────────────────────────────────
  Missions 1-4   → code.visualstudio.com/docs/python/python-quick-start
  Missions 5-6   → code.visualstudio.com/docs/sourcecontrol/overview
  Missions 7-8   → code.visualstudio.com/docs/python/debugging
  Missions 9-10  → code.visualstudio.com/docs/python/testing

  DAILY WORKFLOW:
  ───────────────
  1. Open dojo-ascension folder in VSCode
  2. Open terminal (Ctrl+`) → python dojo_classroom.py
  3. Complete a mission in the terminal
  4. Open ~/dojo_*.json files in VSCode
  5. Experiment and modify them

  KEY SHORTCUTS:
  ──────────────
  F5              → Run Python file
  F9              → Toggle breakpoint (debugger)
  Ctrl+`          → Open integrated terminal
  Ctrl+Shift+P    → Command palette
  Ctrl+Shift+G    → Git panel (view changes, commits)
  Ctrl+Shift+X    → Extensions marketplace
    """)
    wait()

# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────


def main_menu(player, missions):
    """Main menu interface"""
    clear_screen()
    header(f"DOJO OS v5.0 | {player.name} | {player.get_rank()}", Fore.CYAN)
    print(
        f"\n  {Fore.YELLOW}⚡ Honor: {player.honor}  |  Completed: "
        f"{len(player.completed)}/{len(missions)}{Style.RESET_ALL}\n"
    )
    next_mission = get_next_mission(missions, player.completed)
    print(
        f"  {Fore.MAGENTA}Pathway: {get_pathway_stage(player, missions)}"
        f"{Style.RESET_ALL}"
    )
    if next_mission:
        print(
            f"  {Fore.CYAN}Next recommended mission: {next_mission['number']}. "
            f"{next_mission['title']}{Style.RESET_ALL}\n"
        )
    print(f"  {Fore.WHITE}1. Start Next Mission{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}2. Choose Specific Mission{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}3. View Progress Dashboard{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}4. Reflection Journal{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}5. VSCode Integration Guide{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}6. Save Progress{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}7. Exit{Style.RESET_ALL}")
    print(
        f"\n  {Fore.MAGENTA}/chronicle tips{Fore.WHITE} — personalised tips "
        f"from your session history{Style.RESET_ALL}"
    )
    return input(f"\n  {Fore.GREEN}root@dojo:~# {Style.RESET_ALL}").strip()


def game_loop():
    """Main game loop"""
    global SAVE_FILE, JOURNAL_FILE
    SAVE_FILE, JOURNAL_FILE = get_state_paths()
    missions = load_missions()

    clear_screen()
    print_slow(
        f"{Fore.CYAN}{Style.BRIGHT}  DOJO ASCENSION v5.0{Style.RESET_ALL}", 0.03)
    print_slow(
        f"{Fore.WHITE}  Dynamic Mission Engine + Reflection System{Style.RESET_ALL}", 0.02)
    print_slow(
        f"{Fore.YELLOW}  Python | Git | JSON | Code Review{Style.RESET_ALL}", 0.02)
    print()

    if SAVE_FILE.exists():
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        player = Player(
            saved["name"],
            saved["honor"],
            saved.get(
                "completed",
                []),
            saved.get("skills"))
        print(
            f"{Fore.CYAN}✓ Save found! Welcome back, {player.get_rank()} "
            f"{player.name}.{Style.RESET_ALL}"
        )
    else:
        name = input(
            f"\n  {Fore.GREEN}Enter your name, Initiate: {Style.RESET_ALL}"
        ).strip() or "Initiate"
        player = Player(name)

    wait()

    while True:
        choice = main_menu(player, missions)

        if choice == '1':
            # Find next unfinished mission
            next_mission = None
            for m in missions:
                if m["id"] not in player.completed:
                    next_mission = m
                    break

            if next_mission:
                execute_mission(next_mission, player, missions)
            else:
                print(
                    f"\n{Fore.GREEN}✓ All missions complete! You are a Co-Architect!{Style.RESET_ALL}")
                time.sleep(2)

        elif choice == '2':
            clear_screen()
            print(f"\n{Fore.CYAN}Available Missions:{Style.RESET_ALL}\n")
            for m in missions:
                status = "✓" if m["id"] in player.completed else " "
                print(f"  [{status}] {m['number']}. {m['title']}")

            try:
                num = int(
                    input(
                        f"\n{Fore.GREEN}Choose mission number: "
                        f"{Style.RESET_ALL}"
                    )
                )
                mission = next(
                    (m for m in missions if m["number"] == num), None)
                if mission:
                    execute_mission(mission, player, missions)
                else:
                    print(f"{Fore.RED}Mission not found.{Style.RESET_ALL}")
                    time.sleep(2)
            except ValueError:
                pass

        elif choice == '3':
            show_dashboard(player, missions)

        elif choice == '4':
            journal_data = load_journal_data()
            view_journal(journal_data)

        elif choice == '5':
            show_vscode_guide()

        elif choice == '6':
            player.save_state()
            time.sleep(1)

        elif choice == '7':
            player.save_state()
            print_slow(
                f"\n{Fore.CYAN}Disconnecting from Dojo OS... Progress saved."
                f"{Style.RESET_ALL}"
            )
            sys.exit(0)

        elif choice.lower() in ('/chronicle tips', '/chronicle'):
            journal_data = load_journal_data()
            chronicle_tips(player, missions, journal_data)


if __name__ == "__main__":
    try:
        game_loop()
    except KeyboardInterrupt:
        print(
            f"\n{Fore.BLUE}The Dojo remains. Return when ready."
            f"{Style.RESET_ALL}"
        )
        sys.exit(0)
