# CONTEXT: AI and Contributor Onboarding

Dojo Ascension is a lightweight, mission-driven learning project designed to teach Python, Git, JSON, and code review through practical prompts and reflection. The repository is intentionally structured so that non-programmers, educators, and engineers can collaborate on a shared curriculum without needing a heavy platform or external services.

At a high level, there are two active frontends that share the same pedagogical model: a terminal experience in `dojo_classroom.py` and a browser experience in `dojo_web.html`. The terminal path includes optional reflective journaling and local JSON persistence for progress tracking. Core mission data is stored in `missions/missions.json`, with companion mission files in `missions/` for structured, schema-rich authoring workflows.

If you are trying to understand the project quickly, read in this order:
1. `README.md` for project intent, workflows, and contributor entry points.
2. `missions/missions.json` for the canonical mission sequence consumed by the runtime.
3. `CONTRIBUTING.md` and `missions/MISSION_REVIEW_RUBRIC.md` for writing standards.
4. `docs/` materials for governance, metrics, privacy, and accessibility constraints.

Continuous integration currently validates quality with tests and mission validation. Existing checks live in `.github/workflows/validate.yml` and run unit tests plus mission schema checks on pushes and pull requests. A dedicated workflow, `.github/workflows/refresh-repo-bundle.yml`, now keeps `repo_bundle.txt` refreshed on pushes to `main`, using only `GITHUB_TOKEN` for bot-authenticated commits when bundle content changes.

The plain-text bundle pipeline is maintained by `repo_text_export.py` and `refresh_repo_bundle.py`. The exporter intentionally excludes generated bundle artifacts to avoid recursive self-ingestion and unnecessary churn. This keeps AI-facing snapshots stable and useful for rapid analysis.

To verify local changes, run:
- `python -m unittest discover -s tests`
- `python validate_missions.py`
- `python refresh_repo_bundle.py`

Project tone matters as much as syntax. Preferred contributions are clear, inclusive, and practical. The style favors plain language, respectful review, and system-level thinking over gatekeeping or jargon-heavy explanations. Keep changes focused, preserve interoperability between frontends, and avoid introducing hidden infrastructure dependencies.

For AI tools and fast repository ingestion, use `llms.txt` and `repo_bundle.txt` as the first loading surfaces, then drill into specific files relevant to the task.
