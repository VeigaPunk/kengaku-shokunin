# R53ScribeScoreLog2 — scribe, kengaku round 53 wave 3

Axes: calibration, operability. Leaf member — no subagent dispatch. No files were written outside this seat's
directory and the seat's scratch; nothing was committed, pushed, stashed, checked-out, reset or pulled in the lane or
the fleet repo; no fixture repository was created; no tool was installed or upgraded.

## What I did

Drafted the three round-53 text artifacts the L1 lands, in the shape of the round-52 sections, from
`.ufo/waves/round-53/facts.md` and the committed receipts, plus two fresh measurements of my own at the lane's current
HEAD:

1. `scorecard-section.md` — a `## Round 53` section for `SCORECARD.md`: claim table with the frozen counting
   commands, the base-tip before receipts and the measured after-state; verdicts; axis state carried; a
   `### Round-53 capabilities` table (no row enters — the facts do not support one yet); `### Planned (round 54)`.
2. `log-entry.md` — a `LOG.md` round-53 entry in the shape of the round-52 entry (motivating evidence, outcome,
   evidence pointers).
3. `readme-rows.md` — the `corpus/README.md` index row for the round's new knowledge entry plus the
   `### Round-53 evidence` bullets and the cross-checks behind them.
4. Two fresh receipts at the lane's current HEAD (below), copied into this seat's directory.

No verdict the facts do not support is written: prior art, the C2 re-execution leg and every wave-3 attack are left as
`[pending: …]`; coverage stays 7 and is not claimed (the open L0 questions `kengaku | round-25`, `round-33`, `round-51`
are unanswered); no score change is set.

## Lane tip

The lane advanced under this seat, as the assignment warned.

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` at seat start → `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`
  (commit `hyaku run12: remove stale round-53 w2.ready …`).
- `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53ScribeScoreLog2/lane`
  then `git -C …/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r53/R53ScribeScoreLog2/lane` (the required
  path) and `git -C …/lane rev-parse HEAD` → `9ead4476bf55b1ea6490d0204b668195db4a4d1d`
  (`round-53: confirmations integrated (20 tasks, five wave-2 readers), wave-3 spec+dispatch evidence`).
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin branch -v` → `master 9ead4476 …`; `git merge-base --is-ancestor
  b1f79a54 9ead4476` → true. **All measurements below are at `9ead4476`.**

## Fresh measurements (this seat)

### 1. C1 frozen counting command at `9ead4476`

```
$ cd /fast/scratch/hyaku/kengaku-r53/R53ScribeScoreLog2/lane
$ TMPDIR=/fast/scratch/hyaku/kengaku-r53/R53ScribeScoreLog2/tmp timeout 900 python3 plans/round53_c1_triage.py --lane .
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3
PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 fail
EXIT=1
```

Exit 1. The four non-prior-art legs hold; the **PRIOR-ART leg holds no rows** (`rows=0 tasks_covered=0/20`), so the
frozen predicate fails. This is the seat's own observation, not the L1's scored verdict; the prior-art pricing is
wave-3 work in flight (`C1PriceScoutA`–`E`), so the round's final C1 verdict is left `[pending: …]` in the drafts.
Receipt: `.ufo/waves/round-53/w3/R53ScribeScoreLog2/c1-counter-at-9ead4476.txt`.
(The counter's main path only prints — `plans/round53_c1_triage.py:784-795` — so the run wrote nothing into the repo.)

### 2. C2 static legs at `9ead4476`

```
$ TMPDIR=… timeout 600 python3 plans/round53_c2_tipstate.py --lane . --source . --dry
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=74 selftest=4 help=0 help_limit=7.8
DRY static legs only: no predicate
EXIT=0
```

`--dry` runs the static legs only and prints no predicate; the re-execution leg (`RUN executed=… mismatched=…`) is the
wave-3 re-measurement's job and is left `[pending: …]`. Receipt:
`.ufo/waves/round-53/w3/R53ScribeScoreLog2/c2-dry-at-9ead4476.txt`.

### 3. Counts quoted in the drafts (each with its command)

- Confirmations: `python3 -c "import json,glob; …"` over `.ufo/waves/round-53/w2/C1ConfRead*/confirmations-part.json` →
  5 files (A, B, C, D, G), 4 rows each, all `confirmed: true`, **20 rows / 20 distinct tasks**; readers
  `C1ConfReadA`, `C1ConfReadB`, `C1ConfReadC`, `C1ConfReadD`, `C1ConfReadG` (4 each). The dispatched seats
  `C1ConfReadE` (directory present, empty) and `C1ConfReadF` (no directory) left no report.
- Integrated receipt: `corpus/evidence/round53/confirmations.json` → 20 rows, 20 distinct tasks, all `confirmed: true`,
  each with `report` + `report_sha256`; `git log --oneline -1 -- corpus/evidence/round53/confirmations.json` →
  `9ead4476 round-53: confirmations integrated (20 tasks, five wave-2 readers), wave-3 spec+dispatch evidence`.
- Ledger: `python3 -c "import json,collections;d=json.load(open('plans/round53-tipstate.json'));…"` → **78 rows**,
  kinds `entry=74, selftest=4`, states `green=66, red=12`.
- Classifier digest: `sha256sum plans/round53_c1_classify.py` → `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6`
  — equal to `classifier_sha256` in `plans/round53-c1-freeze.json` (the counter's FREEZE leg reports
  `classifier_sha=ok`) and to the digest named in `plans/round-53-claims.md`. The freeze file also pins the eight
  label-seat files (`label_sha256`), the eight shards (`shard_sha256`) and `author_seats =
  ['C1ExecClassifier', 'C1ExecClassifierAlt', 'C1ExecAdvCases', 'KengakuR53']`.
- Corpus index: `grep -c '^\| \`knowledge/' corpus/README.md` → 56; `ls corpus/knowledge | wc -l` → 56 (so the new
  knowledge entry adds one row and one file together).
- SOURCES: `grep -c '^\| S[0-9]' corpus/SOURCES.md` → 186.
- Registry rows: `grep -n '^\| \`round53\|^\| \`stage-scan' SKILL.md` → 3 rows (`round53-c1`, `round53-c2`, `stage-scan`);
  75 frozen + 3 = 78, matching the counter's `registry=78 … row_set_pinned=ok`.
- Seat counts: `python3 -c "import json;print(len(json.load(open('.ufo/waves/round-53/w1-spec.json'))['items']))"` → 35;
  `w2-spec.json` → 42; `w3-spec.json` → 32.
- Wave-1 receipts quoted: `c1-before.txt`, `c1-after-oracle.txt`, `c1-candidates.txt`, `c1-selftest.txt`
  (`cases=47 failures=0`), `c2-before-head.txt` (3 lines: `ROWS registry=75 ledger=0 missing=75 …` + two `MISSING` rows),
  `c2-before-manual-probe.txt` (73 rows parsed, 60 runnable as written: 38 exit 0, 22 exit non-zero, 13 placeholder),
  `c2-run1.txt` (`RUN executed=77 timeout=0 mismatched=18 evidence_missing=1`,
  `TIPSTATE declared_green=49 declared_red=28 observed_green=63 observed_red=14`, `PREDICATE R53-C2 fail`, exit 1),
  `c2-selftest.txt` (`cases=52 failures=0`), `c2-a3-redbefore.txt`.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2/scorecard-section.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2/log-entry.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2/readme-rows.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2/c1-counter-at-9ead4476.txt`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2/c2-dry-at-9ead4476.txt`
- this report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeScoreLog2.md`

Scratch (`/fast/scratch/hyaku/kengaku-r53/R53ScribeScoreLog2/`, the shared clone and the two receipts) was removed
before this report was written.

## Out of scope / not done

- The L1 owns the landed `SCORECARD.md`, `LOG.md` and `corpus/README.md` text; this seat drafted the text and did not
  edit those tracked files (the lane's `git status --porcelain` shows only `.ufo/waves/round-53/w3/` and
  `.ufo/waves/round-53/w3.ready.dispatched` as untracked).
- The C2 re-execution leg was **not** run by this seat (it is the wave-3 measurement seats' work; `--dry` was used
  because the full run is heavy and the L1 reconciles it).
- The census was not re-run by this seat (`scripts/sources-census.sh` may write into `corpus/`); the round-start
  census figures are quoted from `facts.md` and the round-end re-run is the L1's.
- No prior-art pricing, touch-run, blind re-label or wave-3 attack result is asserted anywhere in the drafts; each is
  `[pending: …]`.

## Findings for the L1

1. **The C1 counter at `9ead4476` fails on exactly one leg — PRIOR-ART (`rows=0 tasks_covered=0/20`)** — and the
   CONFIRM leg now passes with `new_confirmed=20 rejected=0`. The drafts therefore say "not admitted at the measured
   revision, novelty stays 8 pending the prior-art pricing", not "admitted".
2. **The C2 static legs hold at `9ead4476` (78 = 78, pinned row set, `bad_decl=0 bad_reason=0`)**; the committed
   ledger declares 66 green / 12 red after the L1's run-1 correction (`58746180`). The drafts do not claim the
   re-execution leg.
3. **The drafts' `### Planned (round 54)` lists the eleven named red causes** as repair work and the seven
   `corpus/knowledge` files / 56 index rows as an index-pair obligation.

Tool anomalies: none. Tool installs: none (`uv`, `git`, `python3`, `bwrap` were already present; `bwrap` was located
but not needed — the C1 counter ran without a sandbox and opened no network service).

Report: .ufo/waves/round-53/w3/R53ScribeScoreLog2.md
