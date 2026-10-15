---
status: draft
sensitivity: public
created_by: fixture-author
synthetic: true
created: '2026-10-15'
updated: '2026-10-15'
id: cand-demo
type: candidate
title: Synthetic expression
hypothesis: hyp-demo
source: src-demo
family: demo-response
expression: rank(ts_delta(close, 5))
settings:
  region: USA
  universe: TOP3000
  delay: 1
  neutralization: INDUSTRY
  decay: 5
  truncation: 0.08
  pasteurization: 'ON'
  nan_handling: 'OFF'
expected_effect: untested illustrative relation
static_checks:
  fields: unverified
research_state: draft
parent_candidate: null
repair_experiment: null
notes: Illustrative syntax only; field availability is unverified.
---

Synthetic research fixture. Not investment evidence.
