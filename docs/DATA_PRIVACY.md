# Learner Data & Privacy

Dojo Ascension is designed to support low-overhead educational use without requiring a central tracking service.

## What data is stored

### Terminal edition
- learner name
- honor, completed missions, and skill levels
- session timestamps for retention reporting
- optional reflection journal entries

### Browser edition
- the same learner progress fields stored in browser local storage
- no automatic server sync

## What is *not* required
- no hosted database
- no third-party analytics SDK
- no mandatory account creation
- no centralized learner surveillance for core use

## Storage locations
- Terminal save: `~/.dojo_ascension/dojo_save.json` by default
- Terminal journal: `~/.dojo_ascension/dojo_journal_data.json` by default
- Browser save: local browser storage

Environment overrides (`DOJO_DATA_DIR`, `DOJO_SAVE_FILE`, `DOJO_JOURNAL_FILE`) can isolate learners on shared machines.

## Classroom / nonprofit guidance
- Prefer one save directory per learner on shared machines.
- Explain clearly to learners what is stored and why.
- Export only anonymized cohort aggregates when reporting pilot outcomes.
- Treat reflection journals as optional and potentially sensitive.

## Export and deletion
- Learners can delete local files directly.
- Browser learners can clear local storage in the browser.
- Facilitators can export anonymized progress summaries with:

```bash
python export_learner_data.py --data-dir <dir> --format json
```

## FERPA-compatible posture
This repository is structured to make privacy-preserving classroom use feasible:
- local-first data storage
- no required cloud account
- no default third-party telemetry
- optional reflective writing instead of mandatory behavioral surveillance

Organizations remain responsible for their own policies, consent practices, and compliance reviews.
