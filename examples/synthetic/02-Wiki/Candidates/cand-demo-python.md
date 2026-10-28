---
status: draft
sensitivity: public
created_by: fixture-author
synthetic: true
created: '2026-10-15'
updated: '2026-10-15'
id: cand-demo-python
type: candidate
title: Synthetic Python implementation
hypothesis: hyp-demo
source: src-demo
family: demo-response
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
expected_effect: untested illustrative relation
static_checks:
  fields: unverified
research_state: draft
parent_candidate: null
repair_experiment: null
notes: Synthetic counterpart of cand-demo; no code or market-data backtest was run.
backend: python
---

Synthetic research fixture. Not investment evidence.
