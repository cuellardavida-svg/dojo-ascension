import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import dojo_classroom
from dojo_classroom import Player, execute_mission
from export_learner_data import aggregate, load_learner_records


class ImpactMetricTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        tmp = Path(self.tempdir.name)
        os.environ["DOJO_DATA_DIR"] = str(tmp)
        os.environ["DOJO_SAVE_FILE"] = str(tmp / "dojo_save.json")
        os.environ["DOJO_JOURNAL_FILE"] = str(tmp / "dojo_journal_data.json")
        self.addCleanup(os.environ.pop, "DOJO_DATA_DIR", None)
        self.addCleanup(os.environ.pop, "DOJO_SAVE_FILE", None)
        self.addCleanup(os.environ.pop, "DOJO_JOURNAL_FILE", None)
        dojo_classroom.SAVE_FILE, dojo_classroom.JOURNAL_FILE = dojo_classroom.get_state_paths()

    def test_player_state_tracks_sessions_for_retention(self):
        first = Player("Tester")
        first_count = first.session_count
        first_log_length = len(first.session_log)

        second = Player("Tester")

        self.assertGreaterEqual(first_count, 1)
        self.assertEqual(first_log_length, first_count)
        self.assertEqual(second.session_count, first_count + 1)
        self.assertEqual(len(second.session_log), second.session_count)
        self.assertIsNotNone(second.first_session_at)
        self.assertIsNotNone(second.last_session_at)

    def test_replaying_mission_does_not_double_award_honor(self):
        mission = {
            "id": "mission_one",
            "number": 1,
            "title": "Mission One",
            "philosophy": "Anchor",
            "economics": "Economics",
            "lesson": "Lesson",
            "challenge": "Challenge",
            "answer": "ok",
            "skill": "python",
            "honor_base": 20,
        }
        player = Player("Tester")

        with patch("dojo_classroom.wait"), \
             patch("dojo_classroom.run_code_challenge", return_value=True), \
             patch("dojo_classroom.journal_reflection"), \
             patch("dojo_classroom.load_missions", return_value=[mission]):
            execute_mission(mission, player, [mission])
            honor_after_first = player.honor
            execute_mission(mission, player, [mission])

        self.assertEqual(honor_after_first, 20)
        self.assertEqual(player.honor, honor_after_first)
        self.assertEqual(player.skills["python"], 1)
        self.assertEqual(len(player.completed), 1)

    def test_export_learner_data_reports_retention(self):
        save_path = Path(self.tempdir.name) / "cohort" / "dojo_save.json"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        start = datetime(2026, 7, 1, 12, 0, 0)
        return_visit = start + timedelta(days=5)
        save_path.write_text(
            json.dumps(
                {
                    "name": "Learner",
                    "honor": 40,
                    "completed": ["m1", "m2"],
                    "skills": {"python": 1, "git": 1, "json": 0, "architecture": 0, "review": 0},
                    "first_session_at": start.isoformat(),
                    "last_session_at": return_visit.isoformat(),
                    "last_mission_at": return_visit.isoformat(),
                    "session_count": 2,
                    "session_log": [start.isoformat(), return_visit.isoformat()],
                }
            ),
            encoding="utf-8",
        )

        records = load_learner_records(Path(self.tempdir.name))
        summary = aggregate(records)

        self.assertEqual(len(records), 1)
        self.assertTrue(records[0]["returned_within_14_days"])
        self.assertEqual(summary["learner_count"], 1)
        self.assertEqual(summary["retention_rate_percent"], 100.0)


if __name__ == "__main__":
    unittest.main()
