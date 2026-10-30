# C10AmendmentDiscipline — round-55 w1 freeze-integrity audit

Seat: C10AmendmentDiscipline (freeze-integrity audit). Lane: kengaku-shokunin.
Freeze commit: `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`. Base tip: `798f5e9ef30ef39291295565209b65a17343c00e`.
Scratch: `/fast/scratch/hyaku/kengaku-r55/C10AmendmentDiscipline/` (deleted at exit).
No installs. No mutating git/jj commands (clone was `--shared --no-checkout`; base/freeze trees extracted with read-only `git archive`).

## 1. Freeze commit file list

`git -C <lane> show 80afa613… --stat` → exactly 7 files, 413 insertions, 0 deletions:

- `plans/round-55-claims.md` (+151)
- `plans/round55_c2_controls.py` (+199)
- `.ufo/waves/round-55/claims/c1-before.txt` (+13)
- `.ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt` (+12)
- `.ufo/waves/round-55/claims/c2-before-uv-decoy-script.txt` (+12)
- `.ufo/waves/round-55/claims/c3-before.txt` (+10)
- `.ufo/waves/round-55/claims/census-before.txt` (+16)

Matches the spec exactly: the two plans files + 5 files under `.ufo/waves/round-55/claims/` (4 before-receipts + census). No drift. `git merge-base --is-ancestor 80afa613 HEAD` → 0 (freeze is on master; HEAD == 80afa613 at audit time; wave work since sits uncommitted/untracked in the tree, which is the seats' own outputs, not rule drift).

## 2. Frozen before-commands re-run and diffed

Trees: base tree extracted via `git archive 798f5e9e` (for c1/c3); freeze tree via `git archive 80afa613` (for c2 — the controls builder is a freeze-commit file and does not exist at base; the r54 counter it loads is byte-identical between base and freeze since the freeze commit touched neither it nor any other plans file). Evidence files alongside this report (`*-rerun.txt`).

**R55-C1** — `python3 plans/round52_c2_registry.py --lane <base-tree>`: ADVERTISED total=79, REGISTERED total=77 rows=79, MISSING 2 (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), INCOMPLETE 0, ENTRY-MISSING 0, SELFTEST-UNBACKED 0, DUPLICATE 0, PREDICATE R52-C2 fail, exit 1. Byte-for-byte match with committed `c1-before.txt` (only the receipt's BASE/COMMAND banner lines differ, as expected). No drift.

**R55-C2** — `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r54` and `--case uv-decoy-script --against r54` (each exit 0):
- abbreviated-selftest: ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1; RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0; TIPSTATE green=1/red=0 observed green=1/red=0; PREDICATE R54-C2 pass; COUNTER EXIT 0; TRUE REGISTRY ENTRY exit=1; ROUTE laundering demonstrated. Matches committed receipt line-for-line.
- uv-decoy-script: same shape, matches committed receipt line-for-line.
- Sole difference both cases: `SOURCE rev` is the laundering fixture repo's own commit hash (fresh `git init`+commit per run, timestamp-seeded): observed `88b1942620…` / `7b8758d603…` vs committed `82c5279743…` / `8d00e0a207…`. Expected nondeterminism of the instrument, not rule drift; `clean=yes lane_rev_equal=yes` and every predicate-bearing line are identical. No drift.

**R55-C3** — three absence checks at base tree: `test -e corpus/evidence/round55/chess-best-move-probe.txt` → exit 1 (absent); `grep -c "thirteenth" PROVINCE.md` → 0, exit 1; `grep -c "chess-best-move" corpus/README.md corpus/SOURCES.md` → `corpus/README.md:0` / `corpus/SOURCES.md:0`, exit 1. Matches committed `c3-before.txt`. No drift.

## 3. Frozen rules file bytes

- `git hash-object plans/round-55-claims.md` (working tree) = `8b2997ce3d44ccab3fed4843fbc895e4a7ea35e7`; committed blob `80afa613:plans/round-55-claims.md` = `8b2997ce3d44ccab3fed4843fbc895e4a7ea35e7`. **Identical — no unstated working-tree edit.**
- Amendment A1 is IN the committed bytes: `git show 80afa613:plans/round-55-claims.md | grep -n "Amendment A1"` → line 121 (`Amendment A1 (2026-10-30, pre-dispatch, no seat has scored): the third planned row (verifier runner) is DROPPED …`).
- Bonus (same freeze batch): `plans/round55_c2_controls.py` working-tree hash `85813b1da6aa4f9cc51174f612b5b048e197282b` == committed blob. Identical.

## Drift named exactly

None. The only deltas observed anywhere in this audit are (a) receipt banner/header lines recording the run's own clone path, and (b) the per-run fixture-repo commit hash inside the two c2 `SOURCE rev` lines — both expected instrument nondeterminism, neither a rule, predicate, counter, kill-rule or control change.

## Dead ends

- First c2 attempt ran the controls script from the base tree and failed with exit 2 (file absent at base, as it must be — it is a freeze-commit instrument). Re-ran from the freeze tree; reported above. Not a defect.
- Census receipt (`census-before.txt`) was read for completeness; it is a W04 duplicate-url census of `corpus/SOURCES.md`, not a before-command of the three claims, and was not re-executed (its generator is outside this seat's named checks).
