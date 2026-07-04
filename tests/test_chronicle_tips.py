"""Unit tests for the /chronicle tips feature in dojo_classroom.py."""
import io
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import dojo_classroom
from dojo_classroom import Player, chronicle_tips, get_practice_chain


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _make_player(honor=0, completed=None, skills=None):
    """Return a Player with no disk I/O side-effects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["DOJO_DATA_DIR"] = tmpdir
        os.environ["DOJO_SAVE_FILE"] = str(Path(tmpdir) / "save.json")
        os.environ["DOJO_JOURNAL_FILE"] = str(Path(tmpdir) / "journal.json")
        dojo_classroom.SAVE_FILE, dojo_classroom.JOURNAL_FILE = \
            dojo_classroom.get_state_paths()
        p = Player("Tester", honor=honor, completed=completed, skills=skills)
    return p


def _minimal_missions(n=3):
    """Return *n* lightweight mission dicts."""
    skills = ["git", "python", "json"]
    return [
        {
            "id": f"mission_{i}",
            "number": i + 1,
            "title": f"Mission {i + 1}",
            "skill": skills[i % len(skills)],
        }
        for i in range(n)
    ]


def _journal_with_entries(dates):
    """Return journal data dict keyed by date strings."""
    return {
        date: {
            "timestamp": f"{date}T10:00:00",
            "mission_id": "demo",
            "mission_title": "Demo",
            "player_rank": "Initiate",
            "answers": {"Q1": "An answer", "Q2": "Another answer"},
        }
        for date in dates
    }


def _capture_chronicle_tips(player, missions, journal_data):
    """Run chronicle_tips and return printed output as a string."""
    buf = io.StringIO()
    # Suppress clear_screen, header, divider, wait for unit testing
    with patch("dojo_classroom.clear_screen"), \
         patch("dojo_classroom.header"), \
         patch("dojo_classroom.divider"), \
         patch("dojo_classroom.wait"), \
         patch("sys.stdout", buf):
        chronicle_tips(player, missions, journal_data)
    return buf.getvalue()


# ─────────────────────────────────────────────
#  Tests: journal-related tips
# ─────────────────────────────────────────────

class TestChronicleJournalTips(unittest.TestCase):

    def test_no_journal_entries_surfaces_start_journal_tip(self):
        player = _make_player()
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("Start your reflection journal", output)

    def test_zero_chain_but_past_entries_surfaces_rebuild_tip(self):
        # Entry from 3 days ago — no entry yesterday/today → chain = 0
        old_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        journal = _journal_with_entries([old_date])
        player = _make_player()
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, journal)
        self.assertIn("Rebuild your practice chain", output)

    def test_active_chain_surfaces_chain_length(self):
        # Entries for today and yesterday → chain = 2
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        journal = _journal_with_entries([today, yesterday])
        player = _make_player()
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, journal)
        self.assertIn("2 day", output)

    def test_short_reflection_answers_surfaces_depth_nudge(self):
        today = datetime.now().strftime("%Y-%m-%d")
        journal = {
            today: {
                "timestamp": f"{today}T10:00:00",
                "mission_id": "demo",
                "mission_title": "Demo",
                "player_rank": "Initiate",
                "answers": {"Q1": "ok", "Q2": "yes"},   # very short
            }
        }
        player = _make_player()
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, journal)
        self.assertIn("deeper in your reflections", output)


# ─────────────────────────────────────────────
#  Tests: mission-completion tips
# ─────────────────────────────────────────────

class TestChronicleMissionTips(unittest.TestCase):

    def test_no_completed_missions_surfaces_begin_tip(self):
        player = _make_player()
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("Begin your first mission", output)

    def test_all_missions_complete_surfaces_go_deeper_tip(self):
        missions = _minimal_missions(3)
        completed_ids = [m["id"] for m in missions]
        player = _make_player(honor=100, completed=completed_ids)
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("All missions complete", output)

    def test_partial_completion_surfaces_next_mission(self):
        missions = _minimal_missions(3)
        # Complete only the first mission
        player = _make_player(honor=20, completed=[missions[0]["id"]])
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("Mission 2", output)


# ─────────────────────────────────────────────
#  Tests: skill-gap tips
# ─────────────────────────────────────────────

class TestChronicleSkillTips(unittest.TestCase):

    def test_zero_skill_surfaces_untouched_tip(self):
        skills = {"git": 0, "python": 3, "json": 2, "architecture": 1, "review": 1}
        player = _make_player(skills=skills)
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("Untouched skill", output)
        self.assertIn("GIT", output)

    def test_large_skill_gap_surfaces_balance_tip(self):
        skills = {"git": 1, "python": 4, "json": 1, "architecture": 1, "review": 1}
        player = _make_player(skills=skills)
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("Balance your skills", output)

    def test_balanced_skills_surfaces_balanced_tip(self):
        skills = {"git": 3, "python": 3, "json": 3, "architecture": 3, "review": 3}
        player = _make_player(skills=skills)
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("balanced", output)


# ─────────────────────────────────────────────
#  Tests: honor/rank tips
# ─────────────────────────────────────────────

class TestChronicleHonorTips(unittest.TestCase):

    def test_honor_gap_surfaces_rank_progress_tip(self):
        player = _make_player(honor=10)
        missions = _minimal_missions()
        output = _capture_chronicle_tips(player, missions, {})
        self.assertIn("honor until rank", output)

    def test_max_honor_no_rank_tip(self):
        # 1000+ honor → Co-Architect, no next rank
        player = _make_player(honor=1001)
        missions = _minimal_missions(3)
        completed_ids = [m["id"] for m in missions]
        player.completed = set(completed_ids)
        missions_all_done = missions
        output = _capture_chronicle_tips(player, missions_all_done, {})
        self.assertNotIn("honor until rank", output)


# ─────────────────────────────────────────────
#  Tests: slash-command routing in game_loop
# ─────────────────────────────────────────────

class TestChronicleMenuDispatch(unittest.TestCase):
    """Verify that /chronicle tips and /chronicle are dispatched correctly."""

    def _run_one_loop_iteration(self, menu_input):
        """
        Patch main_menu to return *menu_input* once then '7' to exit.
        Assert chronicle_tips is called exactly once.
        """
        missions = _minimal_missions()

        call_count = {"n": 0}

        def fake_chronicle_tips(p, m, j):
            call_count["n"] += 1

        menu_responses = iter([menu_input, '7'])

        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "save.json"
            journal_path = Path(tmpdir) / "journal.json"
            save_path.write_text(
                '{"name":"Tester","honor":10,"completed":[],'
                '"skills":{"git":1,"python":1,"json":1,'
                '"architecture":0,"review":0}}',
                encoding="utf-8"
            )

            with patch("dojo_classroom.load_missions", return_value=missions), \
                 patch("dojo_classroom.get_state_paths",
                       return_value=(save_path, journal_path)), \
                 patch("dojo_classroom.SAVE_FILE", save_path), \
                 patch("dojo_classroom.JOURNAL_FILE", journal_path), \
                 patch("dojo_classroom.load_journal_data", return_value={}), \
                 patch("dojo_classroom.chronicle_tips",
                       side_effect=fake_chronicle_tips), \
                 patch("dojo_classroom.main_menu",
                       side_effect=lambda p, m: next(menu_responses)), \
                 patch("dojo_classroom.clear_screen"), \
                 patch("dojo_classroom.print_slow"), \
                 patch("dojo_classroom.wait"), \
                 self.assertRaises(SystemExit):
                dojo_classroom.game_loop()

        return call_count["n"]

    def test_slash_chronicle_tips_dispatches(self):
        n = self._run_one_loop_iteration('/chronicle tips')
        self.assertEqual(n, 1)

    def test_slash_chronicle_alone_dispatches(self):
        n = self._run_one_loop_iteration('/chronicle')
        self.assertEqual(n, 1)

    def test_slash_chronicle_tips_case_insensitive(self):
        n = self._run_one_loop_iteration('/Chronicle Tips')
        self.assertEqual(n, 1)


if __name__ == "__main__":
    unittest.main()
