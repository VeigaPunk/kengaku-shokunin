# R5LedgerStatic — DEFECTS

Review: `.ufo/waves/round-54/w1/R5LedgerStatic/review.md` (full defect rows pasted).
Reproducer: `.ufo/waves/round-54/w1/R5LedgerStatic/static-audit.py` (executed, exit 0).

High: `scratch-root-guard` declares exit 2 but its reason and canonical CHECK-red branch require exit 1.
Medium: twelve red reasons merely restate nonzero exit; `round53-c2`, `sources-adopt`, `stage-scan` falsely label lane-dot argvs as bare; `round53-c2` reason falsely says the registry omits --source/--work, which SKILL.md:640 explicitly names.

Static checks: 78/78 registry identity, strict duplicate-free JSON, exact fields, canonical entry_mode_ok/script matches, 74/74 r53-entry argv matches, no green noise, all reason/evidence size bounds pass. No gate execution performed. LSP device unavailable. No installation or scratch artifacts.

Self-evaluation: accuracy 4/5 (static evidence, no execution); completeness 5/5 (all requested schema/reason/provenance checks and pasted rows); clarity 4/5 (full-row appendix is lengthy but required); actionability 5/5 (row-specific corrections and canonical source locations); conciseness 4/5 (appendix repeats common reason). Overall 4.4/5. Highest-impact remaining verification: independently reconcile the scratch-root-guard observed exit against its recorded evidence. Assessment is bounded to static review, not a runtime verdict.
