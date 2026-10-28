# From research question to next experiment

Use this route for an end-to-end research request. A narrow ingest, query or
result-recording request stays narrow. Do not require a fixed source count
or candidate batch size; continue while the next action resolves a material
evidence gap within the requested scope.

## Establish the research brief

Use supplied papers, market/universe, horizon, data access, backend and budget.
Resolve what is already present in project files before asking. If backend is
unspecified, keep the hypothesis backend-neutral until implementation matters.
When both backends are requested, share evidence and hypotheses but create
separate candidates. Unknown settings do not become defaults.

For a research write, save a concise `03-Logs/Research/<run-id>.md` with:

- Question and why the proposed mechanism could predict returns.
- Known scope, assumptions, evidence needed and missing inputs.
- Current stage and linked Source/Hypothesis/Candidate/Experiment IDs.
- Testable contrary explanation and a measurable kill condition.
- Next experiment, expected information gained and stopping condition.

This is an operational brief, outside typed `02-Wiki` records. Use a unique
run ID and record its path in the operation log. It is not a measured result.

## Evidence before translation

Search existing sources, hypotheses, failed candidates and syntheses. A topic
or research request can justify relevant primary-source discovery; a
wiki-only query does not silently expand into external research.

Capture accessible original evidence and usable extraction, if needed. Keep
the paper's sample, universe, frequency, publication date, method, costs,
reported IS/OOS scope and limitations. An abstract can support only claims
actually present in the abstract; mark partial capture. Never reconstruct a
missing result table from a secondary summary.

Write source claims separately from the proposed tradable translation. A
paper's reported association is not an observed result for our implementation.
Claims begin pending. Preserve citations at page, table, equation or row level.

## Hypothesis and implementation

Create the smallest useful set of hypotheses supported by the evidence. Each
has mechanism, expected direction, horizon, data requirements, competing
explanation, leakage threats and a falsifiable kill condition. A draft may
contain uncertain evidence if uncertainty is explicit; it is not reviewed.

For each backend, use `backends.md` to determine whether an executable
candidate can be specified. A missing field mapping, timestamp convention,
cost model or reproduction setting blocks candidate creation, not the whole
research brief. Record the gap and a concrete action to resolve it.

Start with an interpretable baseline. Add only motivated variants that test
a distinct question. A small batch is usually easier to diagnose than many
unrelated expressions. Record each tried variant, including failed attempts.

## Predeclare a discriminating experiment

Before inspecting the deciding result, record:

- Point-in-time availability: release/revision lag, feature cutoff, universe
  membership, corporate actions and survivorship handling.
- Training, selection/validation and final test windows; label horizons and
  required separation where overlapping labels would leak across splits.
- Signal lag, execution convention, portfolio construction and cost model.
- Primary metric, units, uncertainty method and relevant baseline/negative
  control. Do not invent unavailable platform diagnostics.
- Regime/universe checks, parameter sensitivity and incremental value versus
  known exposures, where data allow.
- Trial/selection history and what would stop further tuning. Once a holdout
  is used to choose a variant it is selection evidence, not a fresh final test.
- Named acceptance criteria and the policy/brief version defining them.

For BRAIN, capture what the platform actually exposes and verify its current
checks through the authorized workflow. For Python/Qlib, preserve code and
data identity, exact configuration and logs. A local proxy for a BRAIN factor
does not inherit platform eligibility.

## Learn from the result

If execution was requested and the engine/data are available, use the chosen
execution workflow and ingest its artifacts. Otherwise deliver the untested
candidate and experiment plan. Do not fabricate metrics to complete the chain.

Create one experiment per distinct attempt. Classify the failure before a
repair: unavailable/invalid data, implementation/timing defect, unsupported
economic mechanism, excessive costs/turnover, unstable result or redundant
exposure. Record alternative diagnoses when evidence cannot distinguish them.

A repair is a new candidate linked to its parent and motivating experiment.
Change one interpretable axis when feasible. A cross-backend translation is a
sibling under the shared hypothesis, not a repair. Keep tested snapshots intact.

Compare only compatible metrics, periods, universes and cost assumptions.
Document differences instead of ranking incomparable Sharpe values. A
synthesis cites supporting and contradicting experiments, what remains
unknown, and the next test most likely to resolve the uncertainty.

## Deliver

Return the current evidence verdict, linked research records, the best next
experiment and the exact remaining gaps. Explain whether the outcome is an
untested plan, observed backtest, reviewed research decision or BRAIN check
result. None of these establishes future profitability. Apply the main
skill's lint/index/log completion steps only after writes.
