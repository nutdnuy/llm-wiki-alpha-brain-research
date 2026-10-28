---
status: draft
sensitivity: public
created_by: fixture-author
synthetic: true
created: '2026-10-15'
updated: '2026-10-15'
id: exp-demo-python
type: experiment
title: Synthetic planned Python experiment
candidate: cand-demo-python
evidence_kind: untested
observed_at: null
expression: synthetic_five_session_change
settings:
  engine: qlib
  engine_version: synthetic-demo
  code_revision: synthetic-code-manifest
  data_snapshot: synthetic-data-manifest
  universe: synthetic demonstration only
  sample_start: '2020-01-01'
  sample_end: '2021-12-31'
  signal_lag_bars: 1
  execution_lag_bars: 1
  rebalance: daily
  execution_price: next open
  portfolio: synthetic equal weights
  costs:
    commission_bps: 1
    slippage_bps: 2
    borrow_bps_per_year: 100
artifacts: []
metrics: {}
checks: {}
decision: pending
reason: ''
next_action: Obtain authorized result
test_scope: not run
brain_alpha_id: null
backend: python
---

Synthetic research fixture. Not investment evidence.
