# C1BatteriesR80 — independent battery replay

## Scope and measured revision

Axes: coverage (R80-C1) and calibration (R80-C2). Read the frozen claims in full before shell execution. No implementation, plan, gate, receipt, ledger, or external substrate was changed; this advisory report is the only persistent file written.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`.
Measured master and clean clone HEAD: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (advanced from freeze).

Setup commands (S was `/fast/scratch/hyaku/kengaku-r80/C1BatteriesR80`):

```sh
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
export HYAKU_SCRATCH="${HYAKU_SCRATCH:-/fast/scratch/hyaku}"
S="$HYAKU_SCRATCH/kengaku-r80/C1BatteriesR80"
mkdir -p "$S"
git -C "$LANE" rev-parse master
git -C "$S" clone --shared -q "$LANE" clone
git -C "$S/clone" rev-parse --show-toplevel
git -C "$S/clone" rev-parse HEAD
git -C "$S/clone" status --porcelain
python3 --version
git --version
```

Output:

```text
6669fe72e59718acc1a0f32a92849a544b0b2f1c
/fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/clone
6669fe72e59718acc1a0f32a92849a544b0b2f1c
[status --porcelain produced no lines]
Python 3.14.8
git version 2.56.0
```

Exactly one shared clone was created. No fixture git commits or other git mutations were performed. No tools were installed or updated.

## Results and comparison

All eight battery processes exited 0. All four controls retained `target_reached=False`. Every case count, failure tally, mutant killed/survived tally, and target flag matches the corresponding committed receipt. **Three receipt files nevertheless diverge in diagnostic codes or case details**, so the committed battery observations are not fully reproducible at this tip.

Wall times below are single observations, measured around each Python invocation using `date +%s%N`; all eight batteries ran concurrently, so these are contention-inclusive wall times, not isolated benchmarks.

| Battery | Wall ms | Exit | Comparison with committed receipt |
|---|---:|---:|---|
| C1 selftest | 643 | 0 | 16 cases, 14 red, 0 failures match; two CASE diagnostic lines diverge |
| C1 mutants | 264 | 0 | 6 real, 6 killed, 0 survived match; second-member diagnostic codes diverge |
| C1 flip-ledger-only | 76 | 0 | Exact battery stdout match; 138 defects; target false |
| C1 header-only | 74 | 0 | Exact battery stdout match; 126 defects; target false |
| C1 copy-observations | 74 | 0 | Exact battery stdout match; 2 defects; target false |
| C2 selftest | 126 | 0 | Exact battery stdout match; 9 cases, 8 red, 0 failures |
| C2 mutants | 65 | 0 | Exact battery stdout match; 4 real, 4 killed, 0 survived |
| C2 presence | 32 | 0 | Defects 19 → 18; INDEX-MISSING disappears; target remains false |

### Every divergent line: committed → fresh

`corpus/evidence/round80/c1-selftest.txt`:

```text
COMMITTED CASE observations-foreign expect=OBSERVATIONS-FOREIGN observed=DIVERGENCE-UNNOTED,OBSERVATIONS-FOREIGN,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
FRESH     CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
COMMITTED CASE second-member expect=RECEIPT-MEMBER-COUNT observed=DIVERGENCE-UNNOTED,OBSERVATIONS-FOREIGN,RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
FRESH     CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
```

`corpus/evidence/round80/c1-mutants.txt`:

```text
COMMITTED MUTANT second-member codes=DIVERGENCE-UNNOTED,OBSERVATIONS-FOREIGN,RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
FRESH     MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
```

`corpus/evidence/round80/c2-control-presence.txt`:

```text
COMMITTED CONTROL presence ids=6 closed=6 defects=19 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,INDEX-MISSING,SOURCE-LINE
FRESH     CONTROL presence ids=6 closed=6 defects=18 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,SOURCE-LINE
```

No other battery stdout differences were observed. Receipts contain no explicit exit-status stamp; observed process exit codes are all 0, consistent with their successful battery summaries, but no historical numeric exit code can be compared from these receipt bytes.

Additional frozen-prose discrepancy: C2's claims battery prose and its mutants function docstring say six data mutations, but the committed MUTANTS list and both committed/fresh receipt outputs contain **four**, all killed. This is not a fresh-versus-receipt tally divergence. No frozen rule was reopened or edited.

## Exact battery commands and retained fresh output

All commands ran with cwd `$S/clone`, using separate work directories. The timing wrapper was `t0=$(date +%s%N); <command>; rc=$?; t1=$(date +%s%N); echo "RC=$rc WALL_MS=$(( (t1-t0)/1000000 ))"`. The shell used `set -e`; every invocation succeeded and reached the timing print.

### C1 selftest

```sh
python3 plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c1-selftest
```

```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
RC=0 WALL_MS=643
```

### C1 mutants

```sh
python3 plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c1-mutants
```

```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
RC=0 WALL_MS=264
```

### C1 controls

```sh
python3 plans/round80_c1_located_replay.py --control-flip-ledger-only --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c1-ctl-flip
```

```text
CONTROL flip-ledger-only located=0 reproduced=0 defects=138 codes=COMMAND-TOOL,DIVERGENCE-UNNOTED,EXIT-NONZERO,LANE-TIP-INVALID,MINTED-BY,OBSERVATIONS-EMPTY,RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH,SOURCE-UNTRACKED,STAMP-MEMBER,STAMP-MISSING,SUBJECT-ABSENT,TOOL-MISMATCH,WORKTREE-DIRTY
CONTROL flip-ledger-only target_reached=False
RC=0 WALL_MS=76
```

```sh
python3 plans/round80_c1_located_replay.py --control-header-only --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c1-ctl-header
```

```text
CONTROL header-only located=0 reproduced=0 defects=126 codes=COMMAND-TOOL,DIVERGENCE-UNNOTED,EXIT-NONZERO,LANE-TIP-INVALID,MINTED-BY,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH,SOURCE-UNTRACKED,STAMP-MEMBER,STAMP-MISSING,TOOL-MISMATCH,WORKTREE-DIRTY
CONTROL header-only target_reached=False
RC=0 WALL_MS=74
```

```sh
python3 plans/round80_c1_located_replay.py --control-copy-observations --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c1-ctl-copy
```

```text
CONTROL copy-observations located=5 reproduced=5 defects=2 codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH
CONTROL copy-observations target_reached=False
RC=0 WALL_MS=74
```

### C2 selftest

```sh
python3 plans/round80_c2_spotcheck_debt.py --selftest --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c2-selftest
```

```text
CASE clean expect=pass observed=- ok
CASE unregistered expect=DEBT-UNREGISTERED observed=DEBT-UNREGISTERED ok
CASE trivial-check expect=CHECK-TRIVIAL observed=CHECK-TRIVIAL ok
CASE check-fails expect=CHECK-FAIL observed=CHECK-FAIL ok
CASE close-routing-file expect=CLOSE-NOT-REPAIR observed=CLOSE-NOT-REPAIR ok
CASE close-no-evidence expect=CLOSE-NOT-EVIDENCE observed=CHECK-FAIL,CLOSE-NOT-EVIDENCE ok
CASE source-line expect=SOURCE-LINE observed=SOURCE-LINE ok
CASE index-missing expect=INDEX-MISSING observed=INDEX-MISSING ok
CASE duplicate-row expect=DEBT-DUPLICATE observed=DEBT-DUPLICATE ok
SELFTEST cases=9 red=8 failures=0
RC=0 WALL_MS=126
```

### C2 mutants

```sh
python3 plans/round80_c2_spotcheck_debt.py --mutants --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c2-mutants
```

```text
MUTANT drop-one-row expect=DEBT-UNREGISTERED observed=DEBT-UNREGISTERED killed
MUTANT close-names-spotcheck expect=CLOSE-NOT-REPAIR observed=CLOSE-NOT-REPAIR killed
MUTANT check-made-trivial expect=CHECK-TRIVIAL observed=CHECK-TRIVIAL killed
MUTANT status-reopened expect=TARGET observed=- killed
MUTANTS real=4 killed=4 survived=0
RC=0 WALL_MS=65
```

### C2 control

```sh
python3 plans/round80_c2_spotcheck_debt.py --control-presence --work /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/work/c2-ctl
```

```text
CONTROL presence ids=6 closed=6 defects=18 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,SOURCE-LINE
CONTROL presence target_reached=False
RC=0 WALL_MS=32
```

## Committed-byte comparison provenance

The lane worktree reported 11 dirty status lines after replay; its master remained the measured hash. No dirty lane file was used to run a battery: execution was from the clean shared clone. To avoid treating possibly dirty lane receipt files as committed evidence, baseline bytes were also obtained directly from the clone's committed HEAD:

```sh
git -C /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/clone ls-files corpus/evidence/round80/c1-selftest.txt corpus/evidence/round80/c1-mutants.txt corpus/evidence/round80/c1-control-flip-ledger-only.txt corpus/evidence/round80/c1-control-header-only.txt corpus/evidence/round80/c1-control-copy-observations.txt corpus/evidence/round80/c2-selftest.txt corpus/evidence/round80/c2-mutants.txt corpus/evidence/round80/c2-control-presence.txt
```

Output: all eight paths above were listed (tracked).

```sh
git -C /fast/scratch/hyaku/kengaku-r80/C1BatteriesR80/clone show HEAD:corpus/evidence/round80/c1-selftest.txt HEAD:corpus/evidence/round80/c1-mutants.txt HEAD:corpus/evidence/round80/c1-control-flip-ledger-only.txt HEAD:corpus/evidence/round80/c1-control-header-only.txt HEAD:corpus/evidence/round80/c1-control-copy-observations.txt HEAD:corpus/evidence/round80/c2-selftest.txt HEAD:corpus/evidence/round80/c2-mutants.txt HEAD:corpus/evidence/round80/c2-control-presence.txt
```

Output contained the committed counterparts reproduced above for every differing line. All remaining emitted receipt lines matched the fresh stdout shown in the command blocks, excluding the added timing/RC lines. This comparison does not claim that the dirty lane worktree itself passes either claim.

## Host state, interpretation, and limits

- C1 batteries construct fixtures and execute the fixture Python probe using `sys.executable`; they need a working Python interpreter and writable scratch filesystem. The fixture branch bypasses the real population gate and ancestor git checks. These batteries do **not** independently replay the six real domain instruments or prove their host independence.
- C2 selftest/mutants run fixture checks through `bash -lc`; their commands invoke `grep`. Thus Bash, grep resolution through the login-shell PATH, and login-shell startup environment are ambient host dependencies. No alternate host or hermetic-environment experiment was performed. No network/tool installation is invoked by the inspected fixture battery paths.
- C2 presence additionally copies the measured lane's real spot-check and README. Its diagnostic count is therefore revision-dependent, not a fixed fixture-only value. At the measured clone, the README indexes `lessons/round-79-verifier-spotcheck.md` (read/search observed at line 927); the control source copies that README, explaining the disappearance of INDEX-MISSING and the count decrease from 19 to 18. This is content-state dependence, not evidence of host drift.
- C1 diagnostic changes are already reflected in the measured source: observations-foreign expects REPRODUCTION-MISMATCH and adds a non-observation line; second-member adds NOISE with the other member. The old extra codes are absent in fresh output. No predicate or kill rule was changed by this seat.
- No battery process failure, mutant survivor, or target-reaching cheap control was observed. The discrepancies are stale diagnostic receipts, plus the four-versus-six prose discrepancy; not a demonstrated target escape.
- No full claim counter, domain instrument replay, build, formatter, or unrelated test was run. L1 owns integration and post-integration gates. No blocker prevents delivery of these findings.

## Advisory self-evaluation

Accuracy 4/5: raw outputs and committed-byte provenance retained; no historical exit stamps exist to compare. Completeness 4/5: all eight assigned batteries and every target flag covered; host dependence assessed from source, not experimentally isolated. Clarity 4/5: divergence table separates unchanged tallies from changed codes, but full evidence makes the report long. Actionability 4/5: exact stale receipt lines identified; only L1 may integrate fixes. Conciseness 4/5: command/output evidence intentionally dominates. Mean 4.0/5. Highest-impact improvements: L1 can reconcile the three stale receipts without changing frozen predicates, and independently isolate Bash login-shell dependencies if stronger host-independence evidence is required. User-agreement self-check: the report distinguishes successful batteries from nonmatching committed diagnostics.
