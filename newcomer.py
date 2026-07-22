#!/usr/bin/env python3
"""One-command onboarding for contributors."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def run_step(command: list[str], label: str) -> None:
    print(f"\n==> {label}")
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Dojo contributor onboarding checks.")
    parser.add_argument(
        "--play",
        action="store_true",
        help="Launch dojo_classroom.py after setup and checks.",
    )
    args = parser.parse_args()

    try:
        run_step([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrade pip")
        run_step([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], "Install dependencies")
        run_step([sys.executable, "-m", "unittest", "discover", "-s", "tests"], "Run tests")
        run_step([sys.executable, "validate_missions.py"], "Validate missions")

        if args.play:
            run_step([sys.executable, "dojo_classroom.py"], "Launch Dojo classroom")
        else:
            print("\n✅ Onboarding checks passed. Run: python newcomer.py --play")

    except subprocess.CalledProcessError as exc:
        print(f"\n❌ Failed during: {exc}")
        return exc.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
