# MVP verification and release handoff

Recorded 2026-10-15. This is a local acceptance record. All nine tasks received spec and quality approval. The final guard fix also passed both reviews, and the independent final reviewer approved commit `47d5fda`. The implementation was fast-forwarded into local `main`; the 45-test suite, 14-resource export check and example lint passed again in that checkout. No remote repository was created and no push or remote CI execution occurred.

## Evidence actually observed

| Check | Result and scope |
| --- | --- |
| Portable offline suite | 45 tests passed with Python 3.14.8 and PyYAML 6.0.3. |
| Skill export | `export_skill.py --check` returned 14; allowlisted resources and recorded hashes match the canonical source. |
| Synthetic example | A fresh physical temporary build using `tests/build_example.py` reproduced all 12 checked-in example files byte-for-byte; lint returned zero structural errors. |
| Scoped implementation reviews | Tasks 1–9 received scoped approval. The final independent review approved the integrated implementation after the symlink regression fix. |
| Directed manual behavior | Ten fresh Codex subagents manually loaded the installed skill; all ten cases assessed PASS after parent artifact inspection. See [observed evidence](behavioral-evidence.md). |
| Registration | Local registration commit `30a08f28046bbec914886b68bd6d051493b92df2`; both configured runtime symlinks resolve to the canonical skill. |
| Catalog audit | Before/after: 43 errors, 17 warnings, 6 informational findings. Stable finding fields were identical, excluding line movement; no finding refers to this skill. Existing unrelated catalog errors remain. |
| Dirty-workspace preservation | Registration used a HEAD-derived three-file patch; preexisting metadata changes remained unstaged, working bytes were checked, and the index was empty afterward. |

The registration commit contains only the new manifest record, generated inventory row and dated changelog entry, plus manifest date/count updates. It makes no behavioral or financial claim.

## Final symlink regression check

Final review found a P1 mismatch: lint skipped a symlinked research directory while handoff traversed it, allowing a record outside the validated note set into an export. The pre-fix reproduction returned lint errors `[]` and exported `1` candidate. The guard fix rejects research-directory symlinks, and handoff now uses the validated in-memory records. The same reproduction is rejected before any output directory is created. Two regression tests increased the portable suite from 43 to 45 passing tests; the final export check still matched 14 resources and example lint returned zero errors. The repository fix is `2fe3c2dc1438d5d93c11d2eb35a09ed15d423f15`; its canonical counterpart is `90bc4a6b`.

The ten manual prompts ran before this guard-only change and were not rerun afterward. SKILL.md and reference instructions did not change. The parent re-linted all ten resulting case wikis with the final guard code: every case had zero structural errors. The local post-fix check record identifies the repository fix above; original report hashes in the behavioral evidence remain unchanged. These final structural checks do not constitute new manual behavioral executions.

## Reproduce portable checks

Set `$PYTHON` to the project virtual-environment interpreter and `$SKILL_DIR` to `skills/llm-wiki-alpha-brain-research`. From the repository root:

```bash
$PYTHON -m unittest discover -s tests -p 'test_*.py' -v
$PYTHON "$SKILL_DIR/scripts/brain_wiki.py" lint --wiki examples/synthetic
```

Maintainers with an authorized canonical source can also run:

```bash
$PYTHON scripts/export_skill.py --source "$CANONICAL_SKILL_DIR" --destination "$SKILL_DIR" --check
```

The private canonical source is not needed for ordinary installation or use. [Manual case definitions](../tests/behavioral-cases.md) describe the intended observations; unit success alone does not satisfy them.

## Limits and unverified claims

The MVP assumes one writer; concurrent modifications are unsupported. Lint validates structure, references, hashes and typed provenance constraints. It cannot establish source truth, causal validity, correct interpretation, economic performance, current field/operator access, program eligibility, or complete policy applicability. Independent evidence review remains necessary.

Observed host behavior is limited to directed manual Codex skill loading on synthetic fixtures. Cases 03 and 05 recovered after initially guessing incorrect Home paths. Case 08 exposed stale synthesis prose without treating lint as a semantic repair. Case 09 checked an empty eligible queue; nonempty manual CSV rows were exercised by unit tests. These observations do not establish robustness against all prompt injections or all user requests.

Claude installation links resolve, but Claude behavior has not been tested. Automatic discovery on either host is unverified. Desktop app version was unavailable. The configured Python 3.11/3.13 CI matrix has not run remotely or locally; actual local execution used Python 3.14.8. There was no live BRAIN request, simulation, submission, account validation, or measured financial result.

## Concrete publication handoff

Proposed repository name: `llm-wiki-alpha-brain-research`; proposed visibility: public. Independently authored materials use the MIT license in `LICENSE`. The repository owner remains unselected. The tracked local package includes the approved implementation and acceptance documentation, integrated into local `main`. This statement concerns the release tracked set, not the cleanliness of another checkout. No remote exists for this release, and no publication action has been taken.

Review these release contents:

- `README.md`, `LICENSE`, `requirements.txt`, `.gitignore`.
- `skills/llm-wiki-alpha-brain-research/`: SKILL.md, references, starter assets, Python CLI modules, and distribution manifest.
- `examples/synthetic/`: the 12-file illustrative evidence chain, explicitly synthetic and untested.
- `tests/`: portable tests, fixture builder, support utilities and manual case definitions.
- `scripts/export_skill.py` and `.github/workflows/test.yml`.
- `docs/provenance.md`, `docs/verification.md`, and `docs/behavioral-evidence.md`.

Actual project research, account exports, credentials, canonical configuration and local raw behavioral reports are excluded. Before a future authorized publication, inspect the committed file list and staged diff, choose the owner/destination, and create a remote only within that authorization. This record does not claim those later steps have occurred.
