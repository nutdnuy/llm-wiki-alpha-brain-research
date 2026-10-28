# Data contract v1 — BRAIN and Python extension

Markdown frontmatter is parsed using yaml.safe_load. Notes live under
02-Wiki/{Sources,Hypotheses,Candidates,Experiments,Syntheses}/ID.md.
Each ID is globally unique within one project. Use run-prefixed IDs when
importing another system. The filename must equal the stable ID.

Common fields: id, type, title, status, sensitivity, created_by, synthetic,
created and updated. Use quoted ISO dates/timestamps. Status is draft,
reviewed or conflicted. Sensitivity is public, personal, confidential or
restricted. reviewed requires reviewed_by different from created_by and
review_evidence identifying the review and the evidence checked.

| Type | Additional required fields |
| --- | --- |
| source | origin, captured_at, raw_path, raw_sha256, capture_method, capture_completeness, claims |
| hypothesis | sources, mechanism, expected_sign, horizon, data_requirements, leakage_checks, kill_criteria |
| candidate | hypothesis, source, family, expression, settings, expected_effect, static_checks, research_state, parent_candidate, repair_experiment, notes |
| experiment | candidate, evidence_kind, observed_at, expression, settings, artifacts, metrics, checks, decision, reason, next_action, test_scope, brain_alpha_id |
| synthesis | sources, experiments, limitations |

Source claims contain id, text, locator, kind and verification. kind is fact,
interpretation or question; verification is pending, verified or contradicted.
Source capture_completeness is complete, partial or unknown. Each citation
in sources contains source, claim and locator. Claim IDs must exist in the
referenced source; a precise locator remains subject to semantic review.

New candidates and experiments declare backend: brain or python. Legacy
records with no backend are treated as brain. Sources/hypotheses/syntheses
are shared; backend identity is part of the tested snapshot. See
`backends.md` for Python settings and execution evidence.

BRAIN settings contain region, universe, delay, neutralization, decay, truncation,
pasteurization and nan_handling; retain extra actual platform settings too.
These are artifact-convention keys, not a platform API contract. Never fill
missing settings by guessing. Field/operator existence is checked externally.

research_state is draft, static-pass, queued, simulated, backtested, hard-pass, near-pass,
failed or archive. parent_candidate and repair_experiment are both null for
a seed or both set for a repair. Never mutate a tested candidate snapshot.
Create another candidate for any expression/settings change. The motivating
repair experiment must reference the parent candidate on the same backend; parent chains cannot
cycle. A candidate source must belong to its hypothesis sources.

Synthetic ancestry cannot be relabeled as real: candidate sources, hypotheses,
all hypothesis citations (including mixed real/synthetic sources), and every
parent candidate and its sources/hypothesis are included. Experiments cannot
be real when their candidate is synthetic. Preserve the synthetic label rather
than treating illustrative records as empirical evidence.

evidence_kind is untested, offline_proxy, live_brain (BRAIN only), or
local_backtest (Python only). Python experiments keep brain_alpha_id null.
artifacts is a list
of mappings with path and sha256; paths must stay inside the wiki and cannot
use symlinks. metrics and checks are mappings. Preserve units in metric
values, for example turnover: {value: 0.12, unit: fraction}. Null and zero
differ. decision is pending, pass, near-pass, fail or archive.

An untested experiment has empty metrics/checks, null observed_at and
brain_alpha_id, and a pending decision. Observed results require artifacts,
observation time and test_scope. pass additionally requires non-synthetic
matching-backend evidence and checks with required_checks_complete: true, items mapping
every applicable named check to PASS, policy_source and as_of.

simulated (BRAIN), backtested (Python) and near-pass candidate states require
matching non-synthetic live_brain or local_backtest artifacts; hard-pass
additionally requires a matching pass decision. A Python pass means the
predeclared research policy passed, not BRAIN eligibility or trading approval.
The experiment expression and complete settings mapping must exactly match
its candidate snapshot, including extra settings. A reviewer
verifies that the listed checks are actually complete for that dated policy.

Lint verifies structure, references, hashes and selected evidence/state
invariants. It does not verify source truth, mathematical validity, current
platform rules, completeness of a declared check set or future returns.
Only typed references are mechanically resolved; freeform prose links and
claim locators require review. Generated navigation uses full wiki-relative paths including each type and ID.
