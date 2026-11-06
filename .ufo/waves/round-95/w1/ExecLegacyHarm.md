# ExecLegacyHarm — harm and conformance at T afe9c229 (round 95, W1)

Full evidence: `.ufo/waves/round-95/w1/ExecLegacyHarm/report.md` (raw receipts in `.ufo/waves/round-95/w1/ExecLegacyHarm/receipts/`).
BASE 4524072d vs T afe9c229, both measured in `--shared` clones; no lane mutation; no tool installed or updated.

## Legacy gate (round79 population ledger)
- BASE: `DEFECTS n=14`, `PREDICATE R79-C1 fail`, rc 1 (matches L1 receipt exactly).
- T: `DEFECTS n=0`, `PREDICATE R79-C1 pass`, rc 0.
- Each of the 14 BASE defects maps to one C-commit edit: 3 RECEIPT-UNTRACKED and 1 SUBJECT-MISMATCH (ledger rows) plus 10 CLASS-K-MISMATCH (SKILL.md class cells).
- Every C-commit ledger subject and verdict is supported by its receipt header and CASE/PREDICATE lines (§1a of report.md). SKILL.md non-count text is unchanged.

## Standing gates (BASE and T, both green)
grader.py (733 checks), state_check (318 match, 0 mismatch), round68 (n=0), round91 (live=0), anchor_line_check (live=0; rows 294 -> 301 with S303-S309), sources-census explicit-dir validate at BASE and T (rc 0, identical W04 list). The `--root /home/vgpnk/Projects/shokunin kengaku` form reads the fleet worktree at ea19299d, not T.

## Findings
FINDING H1 major round-87 counter flips PASS->FAIL at T: `DEFECT L7-ledger row {... "subject": "tb2-header" ...}`, `TARGET executed_rows=39 ... defects=1`, `PREDICATE R87-C1 fail`, rc 1 (BASE: `defects=0`, `PREDICATE R87-C1 pass`). Cause: the C commit's correct subject fix (tb2-result-file -> tb2-header, the only shape the round-79 gate accepts) against the round-87 counter's stale frozen `LEDGER_SUBJECT`. Route R96: re-pin the counter; do not repair in round.
FINDING H2 minor round-94 counter flips PASS->FAIL at T: `DEFECT L7 ledger member=executed round=94 executed_total=39`, `PREDICATE R94-C1 fail` (EXECUTED_AFTER=38 pinned to its own tip; the round-95 flip adds a member). Round-90..93 counters are already red at BASE with the same pinned-total pattern (92: `executed_total=38`, 93: `executed_total=38`, both fail at BASE). Route R96: key L7 totals to the member set, not an absolute count.
FINDING I1 info SKILL.md class cells lack round-95 attribution text (count cells correct).
FINDING I2 info round92 receipt uses `PREDICATE R92-PROBE pass`; verdict `cases` is correct under the frozen shape rule.
FINDING none for the legacy gate (14 -> 0, exactly mapped), grader, state_check, round68, round91, anchor_line_check, sources-census (explicit dirs).
