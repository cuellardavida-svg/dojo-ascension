# 🥋 Dojo Ascension: A Digital Ecology for Creators

[![Contributors](https://img.shields.io/badge/contributors-welcome-brightgreen.svg)](https://github.com/solarpunkopensourcelaboratory/dojo-ascension/graphs/contributors)

> *"The world is already at your fingertips. You are here to find your voice."*

Welcome to the Dojo. This is not just a codebase or a traditional programming class. This is a sanctuary for the curious, the artists, the philosophers, and the inner child eager to understand how the digital world works.

Whether you are a seasoned traveler recovering from a difficult learning journey, or someone stepping into a terminal for the very first time, you belong here. We do not learn code to feed the machine. We learn code so that you can apply these instruments to your **own** arts, hobbies, and passions.

Here, you will learn Python, Linux, and systems thinking through play, mentorship, and ecology. Your wings are yours to open. Let us provide the updraft.

---

## 🛤️ The 10-Minute Spark: Start Here

No prior experience is required. Follow these three steps to step onto the mat and begin your first mission.

### Step 1: Claim Your Space (Clone the Dojo)
Open your computer's terminal and copy-paste this command to bring the Dojo to your local machine:

```bash
git clone https://github.com/solarpunkopensourcelaboratory/dojo-ascension.git
cd dojo-ascension
```

### Step 2: Equip Your Gear (Install Requirements)

Every explorer needs the right tools. Run this command to unpack your gear securely:

```bash
pip install -r requirements.txt
```

### Step 3: Step Onto the Mat (Enter the Classroom)

You are ready. Awaken the engine and begin your journey:

```bash
python dojo_classroom.py
```

*(When the screen lights up and the Dojo welcomes you, take a breath. You have just taken your first step into a larger world.)*

---

## 🌱 Our Superobjective

Inspired by the greatest mentors—from the theatre stage to the realms of animation—our ultimate goal is to raise the next generation of formidable, responsible, and informed creators. We believe the strongest future is built by humans and machines intelligent enough to choose what they want, in harmony with the planet that sustains us.

---

## 🌻 Mission & Funding Snapshot

See the one-page public promise and measurable outcomes in [FUNDING_ONE_PAGER.md](FUNDING_ONE_PAGER.md).

Key outcomes we track:
- Learner retention (14-day return rate)
- Mission completion (median missions completed per active learner)
- Contributor growth (unique merged PR authors per month)

Why organizations adopt it:
- Lightweight browser + terminal delivery
- Shared mission schema instead of a heavyweight LMS rebuild
- Local-first learner data for low-resource environments
- Contributor pathways for educators, writers, reviewers, translators, and facilitators

---

## Frontends and Clients

The Dojo Ascension repo defines a data and logic layer for a learning game:

- **Missions are stored as JSON** (`missions.json` and `missions/*.json`)
- **Player progress and journal entries are stored as JSON** (save files)
- **Multiple frontends available**:
  - Terminal / VS Code experience written in Python (`dojo_classroom.py`)
  - Browser-based single-page app (`dojo_web.html`) — **NEW!**

We explicitly invite other frontends (RPG, mobile, desktop, etc.) that:
- Consume the same mission schema and skill/honor model
- Preserve the educational intent of each mission
- Respect the project license (see LICENSE)

If you are building a new frontend, open an issue to coordinate on data formats and progression so we stay interoperable.

---

*Use in fundraisers and ethical businesses*

We explicitly welcome:
- Non‑profits using Dojo‑derived games in fundraisers
- Ethical solarpunk businesses building commercial games or tools that teach with Dojo missions
- If you distribute software that incorporates Dojo code, you must follow the GPL‑3.0 license (keep derivative code open-source, provide source to users)
- If you want to discuss special arrangements or dual-licensing for a specific project, open an issue or contact the maintainers

---

## 🏫 Organizational Efficiency & Public Value

Dojo Ascension is designed as **mission-aligned digital literacy infrastructure**:

- **Low overhead** — no database or paid SaaS required for core use
- **Low resource** — browser edition works offline; terminal edition runs on basic Python setups
- **Reusable curriculum** — JSON missions can be expanded without a large engineering team
- **Interoperable** — multiple frontends can share the same learner and mission model
- **Local-first** — institutions can pilot cohorts without sending learner data to a third-party service

This makes the project useful for:
- libraries
- classrooms
- community technology labs
- mutual-aid networks
- small nonprofits and fellowships

---

## 🚀 Quick Start

### Option A: Play in Your Browser (Easiest)

No installation required. Just download and open:

```bash
# Clone the repo
git clone https://github.com/solarpunkopensourcelaboratory/dojo-ascension.git
cd dojo-ascension

# Open in your browser
open dojo_web.html
# or double-click dojo_web.html in your file explorer
```

**Features:**
- ✅ All 10 missions available
- ✅ Progress saves to browser storage (persists across sessions)
- ✅ Works offline
- ✅ Mobile responsive
- ✅ Zero dependencies

---

### Option B: Play in Terminal (Python)

For a deeper, reflective experience with optional journal entries:

**Prerequisites:**
- Python 3.8+
- Git
- 2GB free disk space

**Installation:**

```bash
# 1. Clone this repo
git clone https://github.com/solarpunkopensourcelaboratory/dojo-ascension
cd dojo-ascension

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Dojo
python dojo_classroom.py
```

**First Time Setup:**

When you run the game, you'll be prompted to enter your name. The system will:
1. Check your environment (Python version, Git installation, disk space)
2. Create a save file at `~/.dojo_save.json`
3. Optionally create a journal at `~/.dojo_journal_data.json`

**Shared Workstation Tip:**

On a shared machine, keep each participant's progress separate:

```bash
export DOJO_DATA_DIR="$HOME/.dojo-ascension/alice"
python dojo_classroom.py
```

---

## 📖 Curriculum (10 Core Missions)

| # | Mission | Skill | Philosophy |
|---|---------|-------|------------|
| 1 | System Grounding | Git | Wu Wei: Your tools become extensions of your mind |
| 2 | Variables & Data Lineage | Python | Genealogy: Tracing lineage reveals identity |
| 3 | JSON — Data Language | JSON | Cornel West: Justice is cooperation in code |
| 4 | Functions & Jeet Kune Do | Python | Bruce Lee: Maximum efficiency with minimum effort |
| 5 | Git — Journalistic Integrity | Git | Activism: Git is an immutable ledger of truth |
| 6 | Git — Branching & Merging | Git | Wing Chun: Deflect and redirect, don't oppose |
| 7 | APIs & Digital Journalism | Architecture | Freedom of Information: Query the source directly |
| 8 | File I/O — Institutional Memory | Python | Bushido: Legacy ensures society can learn |
| 9 | OOP — Sociological Modeling | Architecture | Theatre: Roles and Actors in a cooperative |
| 10 | Code Review — Gentle Art | Review | BJJ: Testing each other's code before production |

---

## 🎮 How to Play

### Main Menu Options

1. **Start Next Mission** — Play the next incomplete mission in sequence
2. **Choose Specific Mission** — Jump to any mission you want
3. **View Progress Dashboard** — See your skill levels and rank
4. **Reflection Journal** (Terminal only) — Review past journal entries and your practice chain
5. **VSCode Integration Guide** (Terminal only) — Learn how to pair missions with VSCode
6. **Save Progress** — Manually save your state
7. **Exit** — Quit (progress is auto-saved)

### Mission Flow

Each mission teaches a concept through:

1. **Philosophical Anchor** — Connect code to a real-world principle
2. **Economic Parallel** — Understand the "cost" and "value" of the pattern
3. **Technical Concept** — Learn the actual code syntax
4. **Challenge** — Answer a question or write code
5. **Reflection** (Terminal optional) — Answer Uta Hagen's 9 systems-thinking questions

### Progression System

- **Honor Points** — Earned by completing missions (20-30 per mission)
- **Ranks** — Initiate → Apprentice → Practitioner → Adept → Expert → Co-Architect
- **Skills** — Track mastery: Python, Git, JSON, Architecture, Code Review (0-5 levels each)
- **Practice Chain** — Consecutive days of journaling (rewards deliberate practice, not perfection)
- **Pathways** — Beginner confidence → Contributor readiness → Mission authoring → Facilitator readiness

---

## 💾 Progress Saves

Your progress is stored in JSON files (shared between both frontends):

### `~/.dojo_save.json` (Player State)
```json
{
  "name": "David",
  "honor": 150,
  "completed": ["git_system_grounding", "python_variables"],
  "skills": {
    "python": 2,
    "git": 3,
    "json": 1,
    "architecture": 0,
    "review": 0
  },
  "last_save": "2026-06-22T18:40:02Z"
}
```

### `~/.dojo_journal_data.json` (Reflection Entries — Terminal only)
```json
{
  "2026-06-22": {
    "timestamp": "2026-06-22T18:42:15Z",
    "mission_id": "python_variables",
    "mission_title": "Variables & Data Lineage",
    "player_rank": "Apprentice",
    "answers": {
      "Who am I in this circumstance?": "A programmer learning to think systematically...",
      "What do I want?": "To understand how data flows through systems..."
    }
  }
}
```

---

## 🔗 VSCode Integration (Terminal Version)

Pair each mission with VSCode for hands-on learning:

### One-Time Setup

1. Install [VSCode](https://code.visualstudio.com)
2. Install extensions:
   - **Python** (by Microsoft) — Run and debug Python code
   - **GitLens** — View Git history and blame
   - **Prettier** — Auto-format JSON
   - **Python Indent** — Smart indentation

### Workflow

```bash
# In VSCode terminal:
python dojo_classroom.py

# In another VSCode editor:
# 1. Complete a mission in the terminal
# 2. Open ~/dojo_demo.json or other files created by missions
# 3. Experiment and modify them
# 4. Run code with F5 to see results
```

### Official Tutorials to Pair With

- **Missions 1-4** → [Python Quick Start](https://code.visualstudio.com/docs/python/python-quick-start)
- **Missions 5-6** → [Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview)
- **Missions 7-8** → [Debugging](https://code.visualstudio.com/docs/python/debugging)
- **Missions 9-10** → [Testing](https://code.visualstudio.com/docs/python/testing)

---

## 📚 Architecture (v5.0)

### Data-Driven Missions

Missions are stored in `missions/missions.json` as pure data:

```json
{
  "id": "git_system_grounding",
  "number": 1,
  "title": "System Grounding",
  "philosophy": "Like Tai Chi...",
  "economics": "Infrastructure is...",
  "lesson": "The terminal...",
  "challenge": "Type the command to clone a repository.",
  "answer": "git clone",
  "answertype": "contains",
  "skill": "git",
  "honorreward": 20
}
```

This means:
- ✅ **Non-programmers can contribute missions** (educators, subject-matter experts)
- ✅ **Translators can localize content** without touching Python
- ✅ **Mission packs can be shared** and loaded dynamically
- ✅ **Save files are future-proof** (mission IDs never change)
- ✅ **Multiple frontends can coexist** (share the same mission/player data)

### Engine Architecture

**Terminal Version:**
- `dojo_classroom.py` — Main game loop, mission loading, player management (v5.0 Dynamic Engine)
- `missions/missions.json` — All mission data (externalized, data-driven)
- `~/.dojo_save.json` — Player progress (persistent)
- `~/.dojo_journal_data.json` — Reflection entries (persistent, optional)

**Browser Version:**
- `dojo_web.html` — Standalone single-page app (HTML/CSS/JavaScript)
- Mission data embedded inline (no external dependencies)
- Browser localStorage for persistent player progress

### Future Phases

- **Phase 1 (Current)** — 10 core Python/Git/JSON/CodeReview missions (Terminal + Browser)
- **Phase 2** — `dojo_ascension.py` — Advanced multi-week curriculum (Linux, security, quant)
- **Phase 3** — Mission packs: Journalism, Genealogy, Governance, AI Literacy
- **Phase 4** — Community: Shared mission packs, classroom dashboards, instructor tools

---

## 🧪 Development & Testing

### One-Command Contributor Onboarding

Use these exact commands:

```bash
python newcomer.py
python newcomer.py --play
```

- `python newcomer.py` installs dependencies, runs tests, and validates missions.
- `python newcomer.py --play` does the same and then launches the game.

### Validate Missions

```bash
python validate_missions.py
```

This checks for missing required fields, type mismatches, and schema issues.

### Run Tests

```bash
python -m unittest discover -s tests
```

### PR Merge Baseline (Required)

Every PR must pass:
- `python -m unittest discover -s tests`
- `python validate_missions.py`

For mission/content PRs, also complete the Definition of Done in [.github/pull_request_template.md](.github/pull_request_template.md).

### Generate Repo Bundle

If you want a single text file for sharing with collaborators or AI tools:

```bash
python refresh_repo_bundle.py
```

This regenerates [repo_bundle.txt](repo_bundle.txt) from the current repository contents.

### Pilot Reporting Utilities

For cohort reporting and grant evidence:

```bash
python export_learner_data.py --data-dir ~/.dojo_ascension --format json
python measure_retention.py --data-dir ~/.dojo_ascension
```

These commands aggregate anonymized learner outcomes from local save files.

---

## 🤝 Contributing

### For Mission Writers

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick start:

1. Fork the repo
2. Use `missions/mission_template.json` to draft a mission
3. Review with `missions/MISSION_REVIEW_RUBRIC.md`
4. Test locally: `python newcomer.py`
5. Add your mission(s) to `missions/missions.json`
6. Submit a pull request

Good first mission path for non-coders:
- Start with one recall/application mission
- Keep challenge and answer short
- Add one optional hint
- Ask for review using the mission rubric
- Use plain language and inclusive examples (see [docs/ACCESSIBILITY_BASELINE.md](docs/ACCESSIBILITY_BASELINE.md))

### Project Governance, Metrics, and Roadmap

- Governance and response times: [docs/GOVERNANCE.md](docs/GOVERNANCE.md)
- Public metrics: [docs/METRICS.md](docs/METRICS.md)
- Pilot program: [docs/PILOT_PROGRAM.md](docs/PILOT_PROGRAM.md)
- Funding kit: [docs/FUNDING_KIT.md](docs/FUNDING_KIT.md)
- Impact measurement: [docs/IMPACT_MEASUREMENT.md](docs/IMPACT_MEASUREMENT.md)
- Learner privacy: [docs/DATA_PRIVACY.md](docs/DATA_PRIVACY.md)
- Accessibility testing: [docs/ACCESSIBILITY_TESTING.md](docs/ACCESSIBILITY_TESTING.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Monthly updates: [CHANGELOG.md](CHANGELOG.md)

### For Frontend Developers

Want to build a new frontend (RPG, mobile, web framework, etc.)?

1. Load missions from `missions/missions.json` (or embed them)
2. Implement the same player state structure (see `~/.dojo_save.json` format)
3. Follow the answer validation logic (see `validate_answer()` in `dojo_classroom.py`)
4. Open an issue to discuss compatibility before building

### For Code Contributors

- Bug fixes and feature requests welcome
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup

---

## 📋 Project Status

**v5.0 (Current)**
- ✅ Dynamic mission engine (missions.json)
- ✅ Terminal frontend (Python)
- ✅ Browser frontend (HTML/JavaScript) — NEW!
- ✅ Competency-based ranking
- ✅ Uta Hagen reflection journal (Terminal only)
- ✅ Dashboard with skill specialization
- ✅ Persistent saves (JSON)
- 🔜 Mission packs (Journalism, Genealogy, Governance)
- 🔜 Classroom mode (instructor dashboard)
- 🔜 Mobile app (iOS/Android)

---

## 🔧 Maintenance & Sustainability

Dojo Ascension is intentionally small, legible, and inexpensive to maintain.

- **Minimal dependencies** — only small Python packages plus the standard library
- **No required cloud backend** — core use stays local-first
- **Transparent governance** — decisions, response times, and merge baselines are documented
- **Grant-ready evidence** — privacy, pilot, and impact docs are part of the repository
- **Community maintenance model** — contributors can help through code, curriculum, accessibility, documentation, facilitation, and translation

Funding primarily supports maintenance, accessibility, curriculum expansion, pilot operations, and community stewardship.

---

## 📖 License

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. https://fsf.org/

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

The GNU General Public License is a free, copileft license for software and other kinds of works.

When we use your software, we must adhere to the spirit of cooperation and transparency that defines the open-source community.

[Full GPL-3.0 text available at: https://www.gnu.org/licenses/gpl-3.0.txt]

---

## 🙏 Credits

Built by and for the SolarPunk community. Inspired by:
- **Uta Hagen's acting techniques** (systems thinking)
- **Cornel West's philosophy** (public justice)
- **Bruce Lee's martial philosophy** (efficiency)
- **Estonia's e-governance model** (resilience)
- **Brazilian Jiu-Jitsu** (collaborative learning)

---

## 🔗 Links

- [GitHub Repository](https://github.com/solarpunkopensourcelaboratory/dojo-ascension)
- [Contributing Guide](CONTRIBUTING.md)
- [Mission & Funding One-Pager](FUNDING_ONE_PAGER.md)
- [Governance](docs/GOVERNANCE.md)
- [Public Metrics](docs/METRICS.md)
- [SolarPunk Open Source Laboratory](https://github.com/solarpunkopensourcelaboratory)

---

**Let us never stop learning from Galileo.** — SolarPunk Opensource Laboratory
