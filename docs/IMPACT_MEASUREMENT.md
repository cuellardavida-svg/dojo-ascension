# Impact Measurement

This document turns the public metrics into a repeatable reporting workflow for pilots, grants, fellowships, and nonprofit adoption.

## Core questions
- Are learners returning?
- Are learners completing missions?
- Are learners gaining confidence and belonging?
- Are learners becoming contributors, authors, or facilitators?

## Quantitative metrics

### 1. 14-day learner return rate
Definition: percent of learners with a second logged session within 14 days.

```bash
python measure_retention.py --data-dir <dir>
```

### 2. Median missions completed per active learner
Definition: middle value of mission completions across learners in a cohort.

```bash
python export_learner_data.py --data-dir <dir> --format json
```

### 3. Contributor growth
Definition: unique merged PR authors per month.

Source:
- GitHub PR activity
- `CHANGELOG.md`

## Qualitative metrics
- learner confidence after each session
- whether learners felt included or excluded
- facilitator notes about where support was required
- examples of non-code contribution: mission writing, translation, accessibility review, documentation, facilitation

## Recommended cohort evidence bundle
- anonymized export from local save files
- retention rollup
- 2-3 short learner quotations
- 1 facilitator summary
- 1 note on what changed in docs or missions after feedback

## Suggested reporting cadence
- per session: learner/facilitator notes
- per cohort: short pilot summary
- monthly: `CHANGELOG.md` metrics update

## Minimal public summary template
- cohort size
- missions started and completed
- 14-day return rate
- median missions completed
- confidence / belonging themes
- contribution outcomes
- next experiment
