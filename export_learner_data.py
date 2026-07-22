#!/usr/bin/env python3
"""Aggregate anonymized learner metrics from Dojo save files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def iter_candidate_files(data_dir: Path):
    for path in sorted(data_dir.rglob("*.json")):
        if path.name == "dojo_journal_data.json":
            continue
        yield path


def load_learner_records(data_dir: Path) -> list[dict]:
    records = []
    for path in iter_candidate_files(data_dir):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        if not isinstance(payload, dict):
            continue
        if "completed" not in payload or "skills" not in payload:
            continue

        completed = payload.get("completed", [])
        skills = payload.get("skills", {})
        stable_identity = f"{payload.get('name', '')}|{payload.get('first_session_at', '')}"
        learner_id = hashlib.sha256(stable_identity.encode("utf-8")).hexdigest()[:12]
        session_log = payload.get("session_log", [])

        records.append(
            {
                "learner_id": learner_id,
                "missions_completed": len(completed),
                "honor": payload.get("honor", 0),
                "skills_mastered": len([k for k, v in skills.items() if v > 0]),
                "pathway_stage": infer_pathway_stage(len(completed)),
                "first_session_at": payload.get("first_session_at"),
                "last_session_at": payload.get("last_session_at"),
                "last_mission_at": payload.get("last_mission_at"),
                "session_count": payload.get("session_count", len(session_log)),
                "session_log_count": len(session_log),
                "session_log": session_log,
                "returned_within_14_days": returned_within_days(session_log, 14),
            }
        )
    return records


def infer_pathway_stage(completed: int) -> str:
    if completed < 3:
        return "beginner_confidence"
    if completed < 6:
        return "contributor_readiness"
    if completed < 10:
        return "mission_authoring"
    return "facilitator_readiness"


def returned_within_days(session_log: list[str], days: int) -> bool:
    parsed = [parse_iso(item) for item in session_log]
    parsed = [item for item in parsed if item is not None]
    if len(parsed) < 2:
        return False

    start = parsed[0]
    for item in parsed[1:]:
        if (item - start).days <= days:
            return True
    return False


def aggregate(records: list[dict]) -> dict:
    learner_count = len(records)
    if learner_count == 0:
        return {
            "learner_count": 0,
            "median_missions_completed": 0,
            "retained_within_14_days": 0,
            "average_sessions": 0,
        }

    mission_counts = sorted(record["missions_completed"] for record in records)
    mid = learner_count // 2
    if learner_count % 2:
        median = mission_counts[mid]
    else:
        median = (mission_counts[mid - 1] + mission_counts[mid]) / 2

    retained = sum(1 for record in records if record["returned_within_14_days"])
    average_sessions = round(
        sum(record["session_count"] for record in records) / learner_count, 2
    )
    return {
        "learner_count": learner_count,
        "median_missions_completed": median,
        "retained_within_14_days": retained,
        "retention_rate_percent": round((retained / learner_count) * 100, 2),
        "average_sessions": average_sessions,
    }


def export_json(output: Path, summary: dict, records: list[dict]) -> None:
    output.write_text(
        json.dumps({"summary": summary, "learners": records}, indent=2),
        encoding="utf-8",
    )


def export_csv(output: Path, records: list[dict]) -> None:
    fieldnames = [
        "learner_id",
        "missions_completed",
        "honor",
        "skills_mastered",
        "pathway_stage",
        "first_session_at",
        "last_session_at",
        "last_mission_at",
        "session_count",
        "session_log_count",
        "returned_within_14_days",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export anonymized learner metrics from Dojo save files."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing learner save files.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format for learner metrics.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file. Defaults to learner_metrics.{json,csv}.",
    )
    args = parser.parse_args()

    records = load_learner_records(args.data_dir)
    summary = aggregate(records)
    output = args.output or Path(f"learner_metrics.{args.format}")

    if args.format == "json":
        export_json(output, summary, records)
    else:
        export_csv(output, records)

    print(json.dumps(summary, indent=2))
    print(f"Saved {len(records)} learner records to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
