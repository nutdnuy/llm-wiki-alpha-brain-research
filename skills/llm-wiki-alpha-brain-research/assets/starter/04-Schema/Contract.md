# Contract

Each note is Markdown with YAML frontmatter. Name it after its stable ID in
the folder for its type: Sources, Hypotheses, Candidates, Experiments or Syntheses.
Required common keys are id, type, title, status, sensitivity, created_by,
synthetic, created and updated. IDs use lowercase letters, digits and hyphens.
Review status is draft, reviewed or conflicted; it is independent of research state.
Sensitivity is public, personal, confidential or restricted.

Use the installed skill's references/data-contract.md for the complete field
list and `04-Schema/Templates/` for note scaffolds. Source
and experiment artifacts are relative paths plus SHA-256 hashes. A source
citation names a source ID, claim ID and locator. Repairs retain both parent
candidate and motivating experiment. Record missing observations as unknown,
not invented values. Public distribution includes framework and synthetic
examples only; actual project research remains local.

New candidates and experiments declare backend: brain or python. Legacy
records without backend mean brain. See the skill's references/backends.md
for reproduction settings. BRAIN live results use live_brain and simulated;
Python/Qlib results use local_backtest and backtested. A proxy is offline_proxy
and cannot establish a pass. Repairs stay on the same backend. Cross-backend
implementations share a hypothesis and cite each other in their bodies.

Templates intentionally contain missing values. Fill them from evidence;
never save unresolved candidates just to produce a complete-looking chain.
