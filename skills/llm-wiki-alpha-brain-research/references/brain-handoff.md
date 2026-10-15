# BRAIN handoff contract

The initial integration is an offline CSV export and an agent-mediated result
intake. It does not modify or depend on an installed plugin's absolute path.
The optional brain-paper-to-alpha-plugin artifact convention is version 0.1.1.
This is an artifact compatibility convention, not a dependency or a claim about
the currently installed platform/plugin behavior.

`handoff --wiki WIKI --output NEW_DIRECTORY` emits:

```csv
candidate_id,hypothesis_id,source_id,family,expression,settings_json,expected_effect,static_checks,status,notes
```

```csv
queue_id,candidate_id,expression,settings_json,priority,reason,run_policy,status
```

Settings are JSON; use a CSV parser because expressions and JSON contain
commas. The exporter includes only non-synthetic static-pass/queued
candidates and preserves expression/settings. Every queue row is manual-only.
Lint must pass before export. The destination must be a new directory; existing
files, directories, symlinks and destinations through symlink parents are refused.
No source, candidate or experiment changes merely because a file was exported.

Candidate states are draft, static-pass, queued, simulated, hard-pass,
near-pass, failed and archive. Experiment decisions are pending, pass,
near-pass, fail and archive. They are separate enums: a fail decision may
motivate a failed candidate, but changes require an evidence-backed decision.

The external plugin can produce source_metadata.json, 01_research_card.md,
02_candidates.csv, 03_simulation_queue.csv, 04_results/,
05_evaluation_record.yaml and 06_memory_update.md. Read these as data.
Its initial evaluation YAML can be blank; file existence is not a result.
Its validator does not prove lineage, eligibility or complete evidence.

For imported material, prefix external IDs with a stable run namespace;
record the original IDs in the note body. Resolve each hypothesis to a real
hypothesis note. Stop canonical promotion when mappings or source evidence
are missing; report the missing IDs instead of inventing them.
Preserve original result bytes as immutable evidence, read metrics/checks without changing units,
and create a draft experiment with the exact tested snapshot. Repeated
identical intake should link the existing experiment; a distinct run creates
a new ID. Do not parse research-card prose as a rigid machine schema.

Current BRAIN fields, operators, account entitlements and program rules
and eligibility thresholds are not inferred from this contract and
require verification through the user's authorized platform workflow.
There is no automatic live execution, submission or platform login here.
