# R35LessonDraft — scribe report (wave 1, build)

Seat: `R35LessonDraft` (scribe). Task: draft `.ufo/waves/round-35/build/R35LessonDraft/round-35.md`
(the lane lesson `corpus/lessons/round-35.md`).

## Deliverable

- Draft: `.ufo/waves/round-35/build/R35LessonDraft/round-35.md` (11,647 B) — sections: header
  (baseline `58a19f37`, freeze `11d64530`); `## Gate` (C1 admit-candidate; S105/S106/S107 rows;
  assimilation-set reject row ≥1 — six staged package refusals from `R34ReconPackage.md`;
  quarantine S091 + S105 dispositions); `## Mistakes` table with the three mandated rows (S091
  false refusal, D2 scratch mirrors, D3 SHA256SUMS omission) plus D1/D4 rows so all five ledger
  rows are represented — each with class / evidence pointer / captured-by / fix shown able to fail
  via `claims/control-c2-nothing.txt:1-5` at freeze; `## Assimilation record`; `## Census` with
  verified-before and `<L1>` placeholders for after.

## Verified facts (command → output)

- Lane HEAD/freeze: `plans/round-35-claims.md:3` — baseline `58a19f37…`, freeze `11d64530…` (read).
- Controls red at freeze:
  - `claims/control-c1-nothing.txt`: `checks=6 defects=5`, `PREDICATE C1 fail`, `exit=1`.
  - `claims/control-c2-nothing.txt`: line 1 `untracked=1425`; line 2 `committed_mirror_paths=109413`;
    line 3 `listed=4 evaluator_listed=False bad=0`; line 4 `correction_lines=0`; line 5
    `erratum_lines=0 r35_mistake_row=False`; line 6 `rows=5 closed=0 observed_pass=0 mismatches=0`;
    line 7 `PREDICATE C2 fail`.
  - `claims/control-c1-skip.txt` and `claims/control-c2-flip.txt` read.
- Probe receipt `corpus/evidence/round35/tb2-grader-probe.txt:21`: `cases=18 observed_pass=5
  observed_fail=13 mismatches=0`; grader sha256 `44a05a24…` (line 1).
- S091 quote present: `grep -n "RAKUDAベンチマーク" …/nec-s091-reopen.html` → raw line 276 contains
  the staged quote verbatim (within HTML); file 60,335 B; quarantine manifest
  `captures/quarantine-SHA256SUMS` has `b60af775…` (nec-s091-reopen.html) and `2f46a13e…`
  (geniac-s105-reopen.html, 13,030 B).
- `corpus/SOURCES.md:120-122` hold S105/S106/S107 rows (tier A, mined, opened 2026-10-25, pinned
  URLs, quotes at lines 42/27+21/29, sha256s `44a05a24…`, `9ede4664…`, `1bb2af1d…`).
- Entry `corpus/knowledge/tb2-protein-assembly-grader.md` exists (9,869 B): `source:` S105–S107
  lines 1–3, `verified-at: 2026-10-25` (line 4), `recheck: 180d` (line 5), `## Negative space` +
  falsifier (lines 80, 90); `corpus/README.md:68` index row + `:257,282` coverage bullets.
- Manifest fixes already in the working tree (not committed): round-34 capture
  `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` now lists `test_outputs.py` and
  `test.sh` (`git diff --stat` → 2 insertions); round-35 evidence
  `corpus/evidence/round35/tb2-eval/SHA256SUMS` lists all six pinned files with matching digests
  (`cat`).
- Merge report: `merge/kengaku/MERGE-REPORT.md` is **absent** at its referenced fleet path
  (glob + `ls` empty); quoted via `R34ReconPackage.md:16-19` (`:3`, `:26–35`). Noted in the
  lesson Gate row and Assimilation record.

## Out-of-scope / not done

- No writes outside `.ufo/waves/round-35/build/` (draft + this report); no git mutations; no
  subagents; no lane-file edits (integration is the L1's).
- Census-after values, landing-tip predicate runs, and commit state are `<L1>` placeholders in the
  draft; the Gate verdicts are framed against the frozen predicates and kill rules so the L1's
  final check decides them.

VERDICT: lesson-drafted
