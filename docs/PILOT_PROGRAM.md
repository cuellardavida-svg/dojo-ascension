# Tiny Pilot Program

## Goal
Run one short pilot (2-4 weeks) with a small cohort to validate onboarding, mission clarity, and contributor flow.

## Cohort
- 8-20 learners
- 1-3 facilitators
- Mix of coders and non-coders

## What to collect
- Completion data: started vs completed missions
- Retention signal: return within 14 days
- Contributor signal: pilot participants opening issues/PRs
- Qualitative feedback: confusion points, motivation, accessibility blockers
- Confidence and belonging signal: short learner self-report after each session
- Facilitator effort: how much support was needed per learner/session

## Feedback instrument (minimum)
After each session, ask:
1. What was clear?
2. What was confusing?
3. What made you feel included or excluded?
4. What should we improve before inviting more learners?

## Publishable outcome target
Aim for a simple before/after story that a grant reviewer can understand:
- cohort size
- learner completion count
- 14-day return rate
- confidence/belonging summary
- contribution behavior (issues, PRs, or mission drafts)
- 2-3 short learner/facilitator quotations

Use:
- `python export_learner_data.py --data-dir <dir>`
- `python measure_retention.py --data-dir <dir>`
- `.github/ISSUE_TEMPLATE/pilot_feedback.md`

## Closeout
Publish a short pilot summary in `CHANGELOG.md` and update:
- onboarding docs
- mission author guidance
- roadmap priorities
