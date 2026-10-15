# Contract

Each note is Markdown with YAML frontmatter. Name it after its stable ID in
the folder for its type: Sources, Hypotheses, Candidates, Experiments or Syntheses.
Required common keys are id, type, title, status, sensitivity, created_by,
synthetic, created and updated. IDs use lowercase letters, digits and hyphens.
Review status is draft, reviewed or conflicted; it is independent of research state.
Sensitivity is public, personal, confidential or restricted.

Use the installed skill's references/data-contract.md for the complete field
list and examples/synthetic for a complete synthetic research chain. Source
and experiment artifacts are relative paths plus SHA-256 hashes. A source
citation names a source ID, claim ID and locator. Repairs retain both parent
candidate and motivating experiment. Record missing observations as unknown,
not invented values. Public distribution includes framework and synthetic
examples only; actual project research remains local.
