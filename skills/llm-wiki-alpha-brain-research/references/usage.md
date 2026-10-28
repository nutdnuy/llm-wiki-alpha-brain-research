# Invocation examples

The skill keeps its installed identifier `$llm-wiki-alpha-brain-research`.
Its display name is Alpha Research Wiki. BRAIN and Python/Qlib records share
one `<project>/research/wiki`; no second vault is needed.

- `Use $llm-wiki-alpha-brain-research to research post-earnings drift in this
  project. Share the evidence across BRAIN and Python/Qlib. Produce a
  falsifiable hypothesis and test plans; use only verified settings.`
- `Use $llm-wiki-alpha-brain-research to ingest this paper into the project
  wiki. Separate reported findings from our proposed alpha translation.`
- `Use $llm-wiki-alpha-brain-research to record this Qlib run and compare it
  with the linked BRAIN experiment, explaining scope differences.`
- `Use $llm-wiki-alpha-brain-research to retrieve prior failures in this
  family and propose the next experiment.`
- `Use $llm-wiki-alpha-brain-research to report what changed since the last
  review, citing the evidence. Keep existing research records unchanged.`
- `Use $llm-wiki-alpha-brain-research to health-check this wiki read-only.`

The only bundled CLI commands are:

```bash
"$BRAIN_WIKI_PYTHON" "$SKILL_DIR/scripts/brain_wiki.py" init --wiki "$WIKI"
"$BRAIN_WIKI_PYTHON" "$SKILL_DIR/scripts/brain_wiki.py" capture --wiki "$WIKI" --file "$SOURCE"
"$BRAIN_WIKI_PYTHON" "$SKILL_DIR/scripts/brain_wiki.py" lint --wiki "$WIKI"
"$BRAIN_WIKI_PYTHON" "$SKILL_DIR/scripts/brain_wiki.py" index --wiki "$WIKI"
"$BRAIN_WIKI_PYTHON" "$SKILL_DIR/scripts/brain_wiki.py" handoff --wiki "$WIKI" --output "$NEW_HANDOFF_DIR"
```

Use absolute paths. The historical script/marker names are retained for
compatibility. Handoff is BRAIN-only; Python uses its own runner configuration
and preserves output artifacts through `capture` and experiment notes.

For a fresh project environment, use Python >= 3.11 to create a virtual
environment and install `requirements.txt` from this skill. Qlib and BRAIN
clients are not memory-layer dependencies.

Maintainer verification (offline, disposable fixtures):

```bash
"$BRAIN_WIKI_PYTHON" -m unittest discover -s "$SKILL_DIR/tests" -v
```
