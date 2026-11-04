# MutTesterR85 — independent mutation battery on the two new counters

2026-11-04. Leaf seat, round 85 wave 1. Read-only on production; every mutant and fixture lived
under `/fast/scratch/hyaku/kengaku-r85/MutTesterR85` (deleted before yield).

Pinned measured revisions (the lane master moved three times while this seat ran; the battery is
pinned by commit, never by branch name):

| tag | revision | `plans/round85_c1_replay.py` | `plans/round85_c2_debt.py` | `plans/round85_sqlite_truncate_probe.py` |
|---|---|---|---|---|
| PIN | `217910c5` | `9f1e59449aba2c3b951b67c04edd3ce7decaaf9f7e112255ab2357f23a834456` | `7ef98e4b3ec94304fa63b15d440685b8afe30794e2eafaf6b145af962a4ed389` | `d00868acbfe8c398a4703860b39c101734799aeb8cc5de8f2f3d3e05ccb0582f` |
| HEAD-1 | `35b1e4e0` | `095d5ed7c83fbc8011acfcb2825e9f6df0d49285fe827f979fe2898d120c785f` | `2283cada0d7239efd62a9df458846845eb663b3fd21d73be68b09b2b62356c7f` | `04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538` |
| HEAD-2 (report time) | `def5d0ea` | `3f4945ba5b7774489f215623644ee28f6ce60ab6aa0bc6e233797db1d5748e2d` | `7622c250327cc5eaaa4bbbee6fde18034874fb914f5817acb43d5af9dc83ae5d` | `04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538` |

Frozen inputs (`plans/round85-cases.json` `bd98794b…`, `plans/round85-defects.json` `c046535c…`)
and the receipt were read from the measured tree, never from the worktree. Host: Python 3.14.8,
`/usr/bin/bwrap` present. Baselines: C1 `TARGET members=1 cases=8 legs=16 mismatches=0 located=1
executed=1 defects=0` / `PREDICATE R85-C1 pass` and C2 `TARGET ids=8 closed=8 checks_passed=8
indexed=yes defects=0` / `PREDICATE R85-C2 pass` at PIN, HEAD-1 and HEAD-2.

Eight mutants, each one exact textual edit (`if False:`, a widened allow-list, or a constant
`True`) of the committed counter, plus the fixture the removed guard should let through. Method per
mutant: build a fixture copy, run the **pristine** counter on it (must reject, with the named
defect), run the **mutated** counter on the same bytes (must reach the target), then classify.

## Results at PIN `217910c5`

| # | mutant | leg removed | fixture | unmutated | mutant | verdict |
|---|---|---|---|---|---|---|
| 1 | `worktree-dirty` | `RECEIPT-WORKTREE` (`if stamp.get("WORKTREE") != "clean"` → `if False`) | receipt `WORKTREE clean` → `WORKTREE dirty` | rc 1, `DEFECT RECEIPT-WORKTREE dirty` | rc 0, `PREDICATE R85-C1 pass` | **necessary** |
| 2 | `exit-weak` | `RECEIPT-EXIT` (`!= "0"` → `not in {"0","1","3"}`) | receipt `EXIT 0` → `EXIT 3` | rc 1, `DEFECT RECEIPT-EXIT 3` | rc 0, `PREDICATE R85-C1 pass` | **necessary** |
| 3 | `table-member` | `TABLE-MEMBER` (`if doc.get("member") != MEMBER` → `if False`) | table `member` → `sqlite-db-truncate-legacy`, receipt `CASE_TABLE_SHA` rebound to the new bytes | rc 1, `TABLE-MEMBER 'sqlite-db-truncate-legacy'` **and** `REPRODUCE-MISMATCH rc=2 no observation block` | rc 1, `REPRODUCE-MISMATCH` only | redundant |
| 4 | `freeze-anchor` | the R84-V2 freeze anchor (`git cat-file -e FREEZE_REV:rel` → `if False`) | complete replay tree inside a `git init` repo with no commit, so `FREEZE_REV` resolves nowhere | rc **2**, `DEFECT SETUP frozen-input-missing plans/round85-cases.json@1a45aeb5e870` | rc 0, `PREDICATE R85-C1 pass` | **necessary** |
| 5 | `predicate-absent` | `PREDICATE-LINE` (`!= "pass"` → `== "fail"`, accepting an absent line) | receipt's `PREDICATE R85-PROBE pass` line deleted | rc 1, `PREDICATE-LINE absent` **and** `REPRODUCE-MISMATCH rc=0 block differs` | rc 1, `REPRODUCE-MISMATCH` only | redundant |
| 6 | `table-subject` | `TABLE-SUBJECT` (`if doc.get("subject_sha") != SUBJECT_SHA` → `if False`) | table `subject_sha` last nibble changed, receipt `CASE_TABLE_SHA` rebound | rc 1, `TABLE-SUBJECT 8f5bc11018687d8c` **and** `REPRODUCE-MISMATCH rc=2` | rc 1, `REPRODUCE-MISMATCH` only | redundant |
| 7 | `indexed-always` | C2 `indexed()` → `return True` | fixture git repo at the measured revision, both round-85 README index lines deleted and committed | rc 1, all eight checks `ok`, `TARGET … indexed=no`, `PREDICATE R85-C2 fail` | rc 0, `TARGET … indexed=yes`, `PREDICATE R85-C2 pass` | **necessary** |
| 8 | `v8-ignores-exit` | v8 exit code (`ok = proc.returncode == 0 and …` → `ok = "PREDICATE R82-C1 pass" in text`) | committed `plans/round82_c1_plans_registry.py` whose `__main__` prints `DEFECT POSTCHECK ledger-row-unreadable` after `main()` (which printed `PREDICATE R82-C1 pass`) and exits 1 | rc 1, `CHECK v8 DEFECT rc=1 … PREDICATE R82-C1 pass; DEFECT POSTCHECK …` | rc 0, `CHECK v8 ok rc=1 …` | **necessary** |

Counts at PIN: **necessary 5, redundant 3, inconclusive 0**.

### Why the three redundant mutants are redundant (defence in depth, not failure)

C1's REPRODUCE leg is a single choke point over the same bytes. The counter re-runs
`plans/round85_sqlite_truncate_probe.py` from the measured tree and requires its observation block
to equal the receipt's. The probe independently refuses any table whose sha ≠
`FROZEN_TABLE_SHA` (`load_inputs`, `wrong-table sha=…`, exit 2) and re-derives every `CASE` line
from a sandboxed execution (`bwrap`, real `test_json_data`, real set arithmetic). Consequently:

- `table-member` and `table-subject` are caught with `REPRODUCE-MISMATCH rc=2 no observation block`:
  the probe's own table pin fires before any table-field leg could matter.
- `predicate-absent` is caught with `REPRODUCE-MISMATCH rc=0 block differs`: the fresh block
  carries the `PREDICATE R85-PROBE pass` line the receipt dropped.
- This extends the counter's own comment at PIN (the dropped `no-receipt-table-sha` mutant): not
  only the receipt's `CASE_TABLE_SHA` binding but also `TABLE-MEMBER`, `TABLE-SUBJECT` and
  `PREDICATE-LINE` are redundant with REPRODUCE. Their value is diagnosis and exit-code
  specificity, not independent detection.

The five necessary legs are exactly the ones the probe cannot see: receipt-level claims
(`WORKTREE`, `EXIT`), the pre-execution freeze anchor, C2's `indexed()` population-ledger mark, and
the v8 gate exit code at PIN.

## Drift snapshot at HEAD-1 `35b1e4e0` and HEAD-2 `def5d0ea`

Same battery, counters re-read from each commit; fixtures re-extracted from the same commit.

- HEAD-1: necessary 4 (`worktree-dirty`, `exit-weak`, `freeze-anchor`, `indexed-always`),
  redundant 3 (same three), **`v8-ignores-exit` not applicable** — the needle
  `ok = proc.returncode == 0 and "PREDICATE R82-C1 pass" in text` is gone from `v8`.
- HEAD-2: identical outcome (4 / 3 / 1 not applicable); C1's needle set still present, C2's v8
  still does not read the gate exit code.

v8 was rewritten during the wave (`da463cbd`, `35b1e4e0`): its pass condition is now the presence
of four literal flags in `plans/round83_c2_debt.py` bytes, and the round-82 gate's `ROW … defects=`
value is appended as detail only. Measured consequence, fixture commit `b050935a` (registry prints
`DEFECT R82-C1 registry-row-missing` / `PREDICATE R82-C1 fail`, exits 1):

```
PIN 217910c5 : CHECK v8 DEFECT rc=1 DEFECT R82-C1 registry-row-missing; PREDICATE R82-C1 fail     (rc 1)
HEAD-1/HEAD-2: CHECK v8 ok literal_flags=4/4                                                     (rc 0)
HEAD-2 full  : TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0 / PREDICATE R85-C2 pass
```

That means the executable form no longer enforces the frozen R84-V8 row ("`round82_c1_plans_registry.py
--lane .` → `PREDICATE R82-C1 pass`, exit 0") at the measured revision. **Finding F1:
frozen-check divergence (calibration).** It overlaps an already routed limitation:
`corpus/lessons/round-85.md` ("V8's base sensitivity is therefore established at
the byte level … and the gate's green verdict is recorded as the after-state only. Routed to the
round-82 gate owner; not fixed here", commit `da463cbd`) already records the weakening. This
measurement is the concrete before/after the routing lacked; the L1 should treat v8 as
detail-only at HEAD and re-establish the frozen predicate or keep the routing open.

## Coverage boundary recorded, not claimed as a defect

The receipt stamp's `LANE_TIP`, `HOST_PYTHON` and `HOST_OPENSSL` are required-present but
unconstrained by any leg (REPRODUCE compares the observation block only), so a receipt may carry
arbitrary values in those three fields and still pass. The frozen predicate requires only that the
stamp carry them, so this is inside the contract; it is listed so the independent closure does not
read "all twelve stamp fields present" as "all twelve checked".

## Restoration and cleanup evidence

- Production never edited: counters, probe, case table, defect list, receipt, ledger and docs were
  read with `git show <rev>:<path>` into scratch; every mutant and fixture lived under
  `/fast/scratch/hyaku/kengaku-r85/MutTesterR85`. Nothing was staged, committed, checked out or
  reset in the lane or fleet repos; no `pacman`/tool installs occurred.
- Worktree hashes moved during the window (e.g. `plans/round85_c1_replay.py` `7c524a51…` →
  `3f4945ba…`) because sibling seats were landing commits/edits concurrently (master advanced
  `217910c5` → `35b1e4e0` → `def5d0ea` inside this seat's run). None of those writes are this
  seat's: this seat only read, and its counter processes ran with `-I -B` on scratch copies.
- Pristine counters re-run after the battery: C1 pass and C2 pass at PIN and at HEAD-1/HEAD-2
  (`final-c1-pin.txt`, `final-c2-pin.txt`, `final-c1-head.txt`, `final-c2-head.txt`).
- Fixture repos were created exactly as `mktemp -d` + `git init`, with
  `git -C <D> rev-parse --show-toplevel` asserted equal to `<D>` before every mutating call, and
  every commit made inside `<D>` with `-c user.name/-c user.email` on the command line only.
- Scratch tree deleted before yield; this file, `results.json`, `results-head.json`,
  `results-head2.json`, the baseline logs and the driver were copied into
  `.ufo/waves/round-85/w1/MutTesterR85/evidence/` first.

## Reproduction

```
BATTERY_PIN=<rev> BATTERY_PRISTINE=<dir with c1.py c2.py> \
BATTERY_TIP=<git archive of that rev: plans, corpus/evidence/round52/graders/sqlite-db-truncate,
            corpus/evidence/round85, SKILL.md> \
BATTERY_MUTANTS=<out> BATTERY_FIXTURES=<out> BATTERY_WORK=<out> BATTERY_OUT=<json> \
python3 -I -B run_battery.py
```

Fixture construction and each mutation's unified diff are embedded per mutant in
`evidence/results*.json` (`mutations.diff`), together with the exact pristine/mutated stdout for
both sides of every comparison.
