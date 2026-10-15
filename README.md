# LLM Wiki Alpha Brain Research

A project-local research-memory skill and Obsidian-compatible starter for
WorldQuant BRAIN. Preserve the chain from source claim to hypothesis,
expression, observed experiment and reusable lesson, including failed ideas.

## Install and try

Requirements: Python 3.11 or later and PyYAML in the project virtual environment. From this repository:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
mkdir -p research
.venv/bin/python skills/llm-wiki-alpha-brain-research/scripts/brain_wiki.py init --wiki research/wiki
.venv/bin/python skills/llm-wiki-alpha-brain-research/scripts/brain_wiki.py lint --wiki research/wiki
```

Windows: use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.
Additional offline CLI operations (capture stores bytes; typed research notes
are authored using the referenced contract):

```bash
.venv/bin/python skills/llm-wiki-alpha-brain-research/scripts/brain_wiki.py capture --wiki research/wiki --file README.md
.venv/bin/python skills/llm-wiki-alpha-brain-research/scripts/brain_wiki.py index --wiki research/wiki
.venv/bin/python skills/llm-wiki-alpha-brain-research/scripts/brain_wiki.py handoff --wiki research/wiki --output research/handoff
```

Replace the capture input with an accessible local source file. Open research/wiki as an Obsidian vault if desired. Obsidian is optional.
The synthetic example contains five records and no actual platform result.

Install the entire skills/llm-wiki-alpha-brain-research directory in your
host's documented skill location, or explicitly provide its SKILL.md to the
host. Keep scripts, references and assets beside it. Installation discovery
varies by host; manual invocation is the portable fallback.

Example requests: “Capture this paper into the project wiki”, “Show evidence
behind this candidate”, “Record this failed simulation”, and “Find prior
failures before proposing another variant”. The host skill orchestrates
research; the CLI only initializes, captures local bytes, validates typed
records, rebuilds navigation and exports a manual handoff.

## Evidence and privacy

Actual research lives under ignored research/ by default. Framework files
and synthetic examples are distributable; project sources/results are not
part of the package. Do not commit credentials or account exports. Gitignore
does not remove already tracked files; review the staged file list.

A clean lint result checks structure and provenance fields, not financial
validity. The package has no live BRAIN client, backtester, automatic alpha
submission, fixed platform thresholds, dashboard or web crawler. Existing
research tools can supply candidates and artifacts through the documented
handoff. Never infer current field access or program eligibility from examples.

## Development

This local MVP assumes a single writer; concurrent writes are unsupported.
Host behavior remains pending and unverified until the manual behavioral
cases are executed.

Run the offline suite above. Run manual cases in tests/behavioral-cases.md
before advertising host support. The maintainer exports skill assets from
a private canonical source using scripts/export_skill.py; contributors edit
their checkout and submit a diff that is applied to the canonical source
before regeneration. No private vault path is required to use this package.

Read docs/provenance.md for architectural attribution. This project is an
independent implementation and is not affiliated with WorldQuant.
