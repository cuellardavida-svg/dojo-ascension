#!/usr/bin/env python3
"""Measure learner return rate from Dojo save files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from export_learner_data import load_learner_records, returned_within_days


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure 14-day learner return rate from Dojo save files."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing learner save files.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Return window in days. Defaults to 14.",
    )
    args = parser.parse_args()

    records = load_learner_records(args.data_dir)
    eligible = len(records)
    retained = sum(
        1
        for record in records
        if returned_within_days(record.get("session_log", []), args.days)
    )
    rate = round((retained / eligible) * 100, 2) if eligible else 0.0
    print(
        json.dumps(
            {
                "eligible_learners": eligible,
                "retained_within_window": retained,
                "window_days": args.days,
                "retention_rate_percent": rate,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
