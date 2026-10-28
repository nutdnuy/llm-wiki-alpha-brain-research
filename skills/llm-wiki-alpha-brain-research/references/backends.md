# Shared research, separate execution records

`backend` is `brain` or `python` on candidates and experiments. Explicitly set
it on new records. Missing backend on an old v0.1 record means `brain`.
The existing `.brain-wiki.json` marker remains valid; no data rewrite is needed.
Older skill releases do not support Python records and must not write a mixed wiki.

Sources and hypotheses have no execution backend. Use one hypothesis ID for
the same economic claim; BRAIN and Python implementations get different
candidate IDs. Repairs stay within one backend. Cross-backend correspondence
belongs in the note body, with each implementation's approximation disclosed.

## BRAIN

Use `settings` keys region, universe, delay, neutralization, decay, truncation,
pasteurization and nan_handling, plus all actual extra platform settings.
Values must come from the requested configuration or observed export. Field
and operator availability needs current platform evidence.

`expression` is the exact tested expression. Actual platform results use
`evidence_kind: live_brain`; candidate execution state is `simulated`.
`handoff` exports only eligible BRAIN records to its existing manual CSV queue.
It never exports Python candidates.

## Python / Qlib

Use `backend: python`; `settings.engine` distinguishes `python`, `qlib` or
another identified runner. `expression` records the formula or precise code
entrypoint plus implementation identity. It is never executed by this CLI.

Required settings:

| Key | Meaning |
| --- | --- |
| engine, engine_version | Actual runner and installed version |
| code_revision | Git commit and dirty-diff identity, or immutable code hash |
| data_snapshot | Dataset version/hash or a captured manifest identifying it |
| universe | Actual membership rule; point-in-time limitations are explicit |
| sample_start, sample_end | ISO sample dates; actual splits go in test_scope |
| signal_lag_bars, execution_lag_bars | Nonnegative integer lags; timestamp semantics explained in the body |
| rebalance | Rebalance frequency/convention |
| execution_price | Observed/assumed execution convention |
| portfolio | Weighting, constraints, neutralization and sizing specification |
| costs | commission_bps, slippage_bps, borrow_bps_per_year; finite nonnegative numbers |

Use quoted strings for dates. Retain extra configuration, random seeds,
calendar, data frequency and package versions when relevant. Cost units are
per traded notional for commission/slippage and annualized for borrow; state
how the runner applies them. An explicit zero is an assumption requiring a
reason, not a substitute for an unknown cost. Missing required inputs stay in
the brief; no placeholder candidate is promoted just to satisfy the schema.

Executed local results use `evidence_kind: local_backtest` and candidate state
`backtested`. `brain_alpha_id` stays null. Capture the result manifest/log and
metrics as immutable artifacts; link code/data manifests without duplicating
large or licensed datasets. Record actual IS/validation/OOS coverage in
`test_scope`. An unavailable OOS metric remains null.

## Decisions and execution boundaries

`offline_proxy` means an approximation and cannot qualify for a pass decision
or an executed candidate state in either backend. It can guide the next test.
Synthetic fixtures stay synthetic even if code was executed on them.

A `pass` requires non-synthetic artifacts from the matching backend, all
applicable checks recorded as PASS, a true required_checks_complete flag,
policy_source and as_of date. For BRAIN the policy is the current relevant
platform check set. For Python it is the predeclared project evaluation plan,
including its OOS/cost/leakage requirements. A Python pass is only a pass of
that research plan. Neither kind authorizes deployment, submission or trading.

When the owner requests execution, prefer the installed backend specialist
if applicable: BRAIN research workflows or `qlib-quant-backtest-infra`.
Discover its actual tools and instructions then. If unavailable, provide the
concrete handoff/configuration and say which dependency is missing. Do not
install a platform, launch a long job or consume paid compute merely because
a memory record contains a queue entry.
