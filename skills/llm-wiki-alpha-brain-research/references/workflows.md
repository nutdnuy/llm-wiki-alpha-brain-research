# Research workflows

## Intake and evidence

Read the home page, search existing note IDs/titles/source origins, and inspect
related failures before creating research. Prefer a primary paper, official
dataset description or owner-supplied export. Record inaccessible or partial
evidence as a gap; never reconstruct missing tables or outcomes.

Capture the original local file with `capture --wiki WIKI --file FILE`.
Store its returned path and SHA-256 in a Source Note. The CLI does not fetch
URLs or extract PDFs. Use the host's appropriate retrieval tool first; retain
both original and extracted evidence when extraction changes the material.
Record origin, capture time, conversion method and completeness. Duplicate
bytes reuse one raw object; each distinct source identity gets its own note.

Give claims stable IDs such as claim-01 and precise page/section/table/row
locators. For every claim distinguish fact, interpretation or question and
pending, verified or contradicted. An independent check must read the actual
cited bytes/section before changing verification to verified.

## Hypothesis and candidate

Search the wiki before proposing a new family. Cite source ID, claim ID and
locator. State the economic mechanism, direction, horizon, required data,
point-in-time timing, leakage threats and an observable kill condition.
Source findings and proposed executable translations are different claims.

Use the selected backend's research workflow when available to design a small,
thesis-preserving candidate family. Read `backends.md` before implementing
a candidate or importing a result. Otherwise produce a clearly untested
research card. Do not invent available fields, operators or measured scores.
Set candidate state draft until static checks are recorded. Static checks
may support static-pass only; they cannot establish observed performance. Record all
reproduction settings; absent platform choices remain a stated blocker.

A repair creates a new candidate with both parent_candidate and
repair_experiment on the same backend. Cross-backend implementations share
the hypothesis instead. Record the changed axis and why the observed failure
motivates it in notes. Keep the original candidate and experiment unchanged.

## Result and memory

Capture the original result artifact before summarizing it. Create a new
experiment per attempt; match its expression/settings to its candidate.
Preserve units, dates, actual IS/OOS coverage, missing metrics as null and
numeric zero as zero. Never infer OOS performance from an IS panel.
Distinguish untested, offline_proxy, live_brain and local_backtest. Mark demonstrations
synthetic even when their schema resembles an actual export.

Record all reported failures and warnings, unavailable checks, diagnosis,
decision, reason and next action. A pass decision requires real artifacts,
the complete applicable check set, a dated backend evaluation policy reference
and review of the actual result. BRAIN checks need current platform evidence;
Python checks follow the predeclared project plan. This package embeds no
universal performance thresholds.
Submission state belongs to the external platform workflow.

## Query and synthesis

First search exact terms and stable IDs using rg. Read candidate/hypothesis
links and prior experiments; follow source claims to raw evidence. For an
answer about observed performance, inspect the experiment's artifact and
scope. Answer with traceable links and state gaps explicitly. Search outside
the project only when authorized by the request.

Create a synthesis only when comparison adds reusable insight. Include
supporting source claims, experiment IDs, failed alternatives, limits and
open questions. Preserve contradictory results; do not average them away.

## Review and logging

An independent reviewer checks source fidelity, claim locators, economic
logic, timing, reproduction settings and evidence/state consistency. Record
reviewed_by and review_evidence before reviewed status. For conflicted
evidence, preserve both sides and explicitly mark status conflicted.

After research writes, run `lint`, fix clear structural errors, run `index`,
and append one log entry with timestamp, operation, affected IDs and checks
actually performed. A query or health check is read-only except for a
requested report; ask for
additional input only when a substantive correction cannot be supported.
