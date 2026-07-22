# Public Metrics

Track these monthly in `CHANGELOG.md`.

## Core metrics
- Active contributors (unique merged PR authors)
- Merged mission/content PRs
- Learner progression signals (mission completion and return rate)

## Decision metrics for funders and pilot partners
- **14-day learner return rate** — % of learners with a second session within 14 days
- **Median missions completed per active learner** — program momentum
- **Confidence / belonging signal** — short post-session self-report from learners
- **Contribution behavior** — issues opened, PRs opened, or missions authored by pilot participants
- **Inclusion signal** — whether learners felt welcomed, confused, included, or excluded

## Data capture (manual baseline)
- GitHub PR activity for contributor and merge counts
- Optional anonymized learner snapshots from pilot cohorts
- Local save-file exports with `python export_learner_data.py --data-dir <dir>`
- Retention rollups with `python measure_retention.py --data-dir <dir>`
- Post-session facilitator notes using the pilot feedback template

## Reporting format
Use one monthly entry with:
- Metrics table (current month vs previous month)
- What improved
- What regressed
- Next experiment

## Minimum monthly evidence bundle
- `CHANGELOG.md` metrics entry
- At least one pilot or cohort note when a cohort is active
- One contributor/community signal (new mission author, new reviewer, translation help, accessibility feedback, etc.)
