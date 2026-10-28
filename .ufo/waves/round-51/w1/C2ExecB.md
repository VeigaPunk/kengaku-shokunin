# C2ExecB — attribution of `corpus/routed-findings.jsonl` rows 10–18 (0-based 9..17)

Seat C2ExecB (executor), kengaku round 51 (hyaku run 11), one v2 build-and-attack wave.
Item: for each of the nine rows, decide `owner` (fleet lane or `unowned:integrator`),
`disposition`, author a check where the row has none, and **run** every check.
Fragment (sibling file, written): `.ufo/waves/round-51/w1/C2ExecB.jsonl` — 9 complete row
objects, one per line, every original field preserved, `owner` + `disposition` added.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

That is the lane tip (`round-51: v2 wave spec (64 seats) + validated dispatch payload`), read
from a `git clone --shared` of the lane into my scratch. Stage-1 freeze commit
`e07f131cf7037e58a21db6e1f3986cf401ad257c` is present (`git cat-file -t` → `commit`).
I measured in the clone, not in the live tree, because the live tree was being rewritten
under me mid-session (§5 D-E).

## 1. Axes named

1. **adjacency (8 → 9)** — the axis the item is scored on: every routed finding names its owner
   lane and its disposition. Instrument: `plans/round51_routing.py` (frozen, read in full).
2. **within that axis, the operability of the evidence** — a `fixed-verified` disposition is only
   true if the row's own `check` re-derives the finding *inside the execution context the frozen
   counter actually uses*. That sub-axis is where the window turned out to be broken (§5 D-A), and
   it is why five rows are `fixed-verified` and four are `accepted-risk` rather than nine and zero.

## 2. Commands run (exact)

```sh
# stable base
git clone --shared --no-hardlinks <LANE> /fast/scratch/hyaku/kengaku-r51/C2ExecB/lane
git -C .../lane checkout -q 4090c3db79d11279ab5e5121ba25e74aa316e6e7
git -C .../lane rev-parse HEAD                      # 4090c3db79d11279ab5e5121ba25e74aa316e6e7

# before-state, reproduced against the receipt
cd .../lane && python3 plans/round51_routing.py --lane .        # exit 1

# instrument soundness
cd .../lane && python3 plans/round51_routing.py --selftest      # exit 0

# per-row check, run exactly as plans/round51_routing.py:118-125 runs it
#   bash -lc "<check>", cwd=<scratch work>, env TMPDIR=<scratch work> LANE=<lane abs path>
python3 /fast/scratch/hyaku/kengaku-r51/C2ExecB/run_checks.py     # unrooted
python3 /fast/scratch/hyaku/kengaku-r51/C2ExecB/run_rooted.py     # same command, cd "$LANE" && prefixed

# whole-ledger scan of every check that exists (61 of 71)
python3 /fast/scratch/hyaku/kengaku-r51/C2ExecB/scan_all.py

# the fragment, evaluated alone by the frozen counter with --run-checks
cp <fragment> .../lane/corpus/routed-findings.jsonl
cd .../lane && python3 plans/round51_routing.py --lane . --run-checks   # exit 0
cp .../ledger-full.jsonl .../lane/corpus/routed-findings.jsonl          # clone restored: status empty

# owner evidence
awk 'NR>=563 && NR<=612 {...}' SKILL.md        # registry `owner` column, lines 563-609
grep -n '^- \*\*R[0-9]\*\*' corpus/lessons/round-40-verifier-spotcheck.md corpus/lessons/round-41-verifier-spotcheck.md
cd .../lane && python3 plans/routed_open.py --lane . --observe
cd .../lane && python3 plans/routed_open.py --lane . --list
```

Every `source` pointer was read at its exact line. Verified line numbers:
`round-40-verifier-spotcheck.md:92` = `- **R1** C1 counter soundness (frozen, gameable)…`,
`:101` = `- **R5** Carried: R3-from-r39 (order class into a separately frozen ledger), …`;
`round-41-verifier-spotcheck.md:105` = `- **R1** C1 counter soundness residuals …`,
`:110` = `- **R2** Scratch hygiene (D1) …`, `:114` = `- **R3** C2 filler admission …`,
`:116` = `- **R4** SOURCES rule 2 (D2) …`, `:117` = `- **R5** Carried: 14 round_close.py/tip_receipts.py
residuals …`; `SKILL.md:562` = the gate-registry table header.

## 3. Attribution — summary table

`owner` is `kengaku` for all nine. That is not a default: every row's subject is a lane-owned
artifact, and the lane's own registry names the owner in a committed column
(`SKILL.md:563-609`, every row `owner= kengaku`, including `order-check` :590,
`mutant-direction-check` :585, `round42-c1-mutants` :599, `round42-c2` :600,
`sources-adopt` :573, `scratch-root-guard` :608).

| idx | id | status | owner | disposition | owner evidence (quoted) | check, counter cwd | check, rooted `cd "$LANE" &&` |
|---|---|---|---|---|---|---|---|
| 9 | R40-R5 | open | kengaku | **accepted-risk** | source `r40:101` "Carried: … `F39OrderGateMut` fail-open"; subject `plans/order_check.py` → registry `order-check` owner=kengaku (`SKILL.md:590`); `mutant_direction_check.py` → `SKILL.md:585` | authored (was empty) | **1** (residual open) |
| 10 | R42-R1 | open | kengaku | **accepted-risk** | source `r41:105` "the round-42 counter must carry the five `F41C1Hardened` repairs frozen … pin that assumption in the counter's PINS or fixture"; subject `plans/round42_c1_verify.py` → `round42-c1-mutants` owner=kengaku (`:599`) | 2 (`grep: plans/round42_c1_verify.py: No such file or directory`) | **1** (clause 5, the uv pin) |
| 11 | R42-R2 | closed | kengaku | **fixed-verified** | source `r41:110` "give the round root a guard the seats cannot remove"; subject `plans/scratch_guard.py` → `scratch-root-guard` owner=kengaku (`:608`) | 1 (`python3: can't open file '…/work/plans/routed_open.py'`) | **0** |
| 12 | R42-R3 | open | kengaku | **accepted-risk** | source `r41:114` "a check that reads S124-style tier-B PR rows' live state word"; subject `plans/round42_c2_verify.py` → `round42-c2` owner=kengaku (`:600`) | 2 (`grep: .ufo/waves/round-42/claims/control-c2-filler.txt: No such file`) | **1** (clause 3, the state-word detector) |
| 13 | R42-R4 | closed | kengaku | **fixed-verified** | source `r41:116` "correct a non-mutable cell by a new row opening `supersedes S0NN —`, never in place"; subject `corpus/SOURCES.md` + Q34 in-lane (`corpus/QUALITY.md:759`) → `sources-adopt` owner=kengaku (`:573`) | 2 (`error: Could not access 'd69452cf..HEAD'`) | **0** |
| 14 | R42-R5 | open | kengaku | **accepted-risk** | source `r41:117` "… `F39OrderGateMut` fail-open (**no owner this round**)"; the bullet's own words are the unruled overlap — the registry row `order-check` (`:590`, owner=kengaku) resolves it from committed bytes | 2 (`python3: can't open file '…/work/plans/mutant_direction_check.py'`) | **2** (SETUP, see §4) |
| 15 | R40-R1.1 | closed | kengaku | **fixed-verified** | source `r40:92` "R1 C1 counter soundness (frozen, gameable)"; subject `plans/round42_c1_verify.py` → `:599` owner=kengaku | 2 (`grep: plans/round42_c1_verify.py: No such file or directory`) | **0** |
| 16 | R42-R2.1 | closed | kengaku | **fixed-verified** | source `r41:110`; subject `plans/scratch_guard.py` → `scratch-root-guard` owner=kengaku (`:608`) | 1 (silent) | **0** |
| 17 | R42-R2.2 | closed | kengaku | **fixed-verified** | source `SKILL.md:562` (registry header); subject is the registry row itself → `scratch-root-guard` owner=kengaku (`:608`) | 2 (silent) | **0** |

Disposition reasoning, per the claims doc's rules (`plans/round-51-claims.md:84-91`):

- **fixed-verified ×5** (R42-R2, R42-R4, R40-R1.1, R42-R2.1, R42-R2.2) — the finding is closed in
  the row, and its own check exits 0 in this run once the row is anchored at the lane.
  `fixed-historical` would also be legal for R42-R2.1 (`close` starts with `plans/scratch_guard.py`,
  which resolves) and R42-R2.2 (`close` starts with `77ea425a`, a real commit), but both checks do
  prove the state *now*, so the stronger value is the true one. It is also the **only** legal value
  for R42-R2 and R42-R4: their `close` fields start with `children` and `corpus/QUALITY.md:759`
  respectively, neither of which resolves as a commit or as a lane-relative path, so
  `fixed-historical` would print `CLOSE_REF missing` (§5 D-G).
- **accepted-risk ×4** (R40-R5, R42-R1, R42-R3, R42-R5) — the row is open, the owner is this lane,
  and no other lane owns any part of it, so `routed`/`referral` would be a false attribution and
  `refused-out-of-scope` a false refusal. `accepted-risk` is the enum's only value that means
  "named, owned, knowingly carried". Each is evidenced by the failing clause that the row's own
  note names (§4).
- **No `next` field anywhere in the fragment**: the counter requires it only for
  `routed`/`referral` rows (`plans/round51_routing.py:126-130`), and no row in this window names a
  non-kengaku artifact. I did not manufacture a routed row to exercise that branch — control 3
  (`absorbed-routed`) therefore has no witness in my fragment.

## 4. Measurements — the checks actually run

Exit codes as measured (0 = the row's finding is resolved; nonzero = still open). This one
convention is uniform across all nine rows: **check exits 0 iff the finding is resolved.** The
frozen counter consumes exit 0 only for `fixed-verified` rows (`plans/round51_routing.py:118-131`),
so the nonzero exits on the four `accepted-risk` rows are legal and are themselves the
re-derivation of the open state.

Failing clause isolated for each `accepted-risk` row (each check was split and run clause by clause
at the lane):

```text
R42-R1  exit=0  grep -q -- '--unshare-ipc' plans/round42_c1_verify.py
        exit=0  grep -q -- '--ro-bind-data' plans/round42_c1_verify.py
        exit=0  grep -q 'def path_ok' plans/round42_c1_verify.py
        exit=0  grep -q 'unattributed' plans/round42_c1_verify.py
        exit=1  grep -rqs 'command -v uv\|/usr/local/bin/uv' plans/battery42/     <-- the open item
R42-R3  exit=0  grep -q 'CONTROL-C2-FILLER red-as-required' .ufo/waves/round-42/claims/control-c2-filler.txt
        exit=0  grep -q '"V9"' plans/round42_c2_verify.py
        exit=1  grep -rqs 'pulls/\|state=closed' plans/*.py                      <-- the open item
R42-R5  exit=2  python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py
        SETUP counter plans/round42_c1_verify.py is not a round-38-list counter:
        missing=R37_REL,battery38_fixtures,attributed,FAMILY non_6_tuple_rows=14; this check reads
        the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only
R40-R5  exit=1  authored: test -n "$(git log --format=%h 34158b0..HEAD -- plans/order_check.py)"
        && python3 plans/mutant_direction_check.py …      # git log is empty: order_check.py
        # unedited since 34158b0, so the F39OrderGateMut fail-open item stands
```

Authored check (idx 9, the only empty `check` in this window):

```sh
cd "$LANE" && test -n "$(git log --format=%h 34158b0..HEAD -- plans/order_check.py)" && python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py >/dev/null 2>&1
```

It re-derives two of the row's four named items (F39OrderGateMut unedited since `34158b0`;
F39MutDirection still SETUP-failing). It does **not** cover `F39LedgerTip` D1 or the W04 census
line — declared as a limit, not hidden.

**The fragment, evaluated alone by the frozen counter** (clone ledger replaced by the fragment,
`--run-checks`, then restored; clone `git status --porcelain` empty afterwards):

```text
LEDGER corpus/routed-findings.jsonl rows=9
FIELDS complete=9 incomplete=0
OWNERS attributed=9 unattributed=0
DISPOSITIONS set=9 bad=0
SOURCES resolved=9 missing=0
CHECKS present=9 absent=0
VERIFIED ran=5 passed=5 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
FRAGMENT-ONLY EXIT=0
```

**Before-state reproduced** at REV 4090c3d, matching `.ufo/waves/round-51/claims/c2-before.txt`
line for line, exit 1:

```text
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```

**Instrument selftest**: `cases=11 failures=0`, `[selftest] ALL PASS`, exit 0.

**Whole-ledger check scan** (all 61 rows that have a `check`, both execution contexts):

```text
unrooted (counter cwd, LANE in env): total=61 exit0=6  nonzero=55
  unrooted exit0 ids: R39-R2, R39-R5, R42-R3-03, R42-R3-07, R42-R3-08, R42-R3-26
rooted (cd "$LANE" && …):            total=61 exit0=43 nonzero=18
  rooted nonzero ids: R39-R2=1, R39-R3=1, R39-R4=2, R42-R1=1, R42-R3=1, R42-R5=2, R42-R6=1,
    R42-R3-02=1, R42-R3-05=1, R42-R3-06=1, R42-R3-07=1, R42-R3-08=1, R42-R3-18=1, R42-R3-19=1,
    R42-R3-26=1, R42-R3-27=1, R42-R3-32=1, R42-R3-36=1
```

`CHECKS absent=10` = `R40-R5`, `R42-R3-09`, `R42-R3-33/34/35/37`, `R45-S5-7b/c/d/e`; my fragment
fills `R40-R5`, leaving 9 for the seats that own them.

## 5. Defects and rulings for the L1

**D-A (blocks the C2 after-target; systemic).** Every pre-existing `check` in the ledger is
cwd-relative, and the frozen counter runs checks with `cwd=<scratch tmp>`
(`plans/round51_routing.py:118-125`, `bash -lc`, `LANE` supplied in env). Measured: **6/61** exit 0
as the counter runs them, **43/61** once `cd "$LANE" && ` is prefixed — so **41 checks are
cwd-dependent** (fail as the counter runs them, pass anchored), **14 fail in both** contexts, and
**4 flip** (pass unrooted, fail rooted). Consequence: no row can be
`fixed-verified` at landing unless its check is `$LANE`-anchored, so `CHECK_FAILED 0` is
unreachable without a mechanical re-root of the ledger's checks. My nine rows carry the prefix
(original command verbatim, prefix added); the other 52 rows in the ledger are other seats'
windows. **Suggested ruling:** state the `$LANE`-anchor requirement in the claims/lesson, because
`LANE` in the environment is the counter's only signal that checks must be lane-anchored.

**D-B.** Re-rooting is not a universal fix: 4 checks flip the other way (pass unrooted, fail
rooted — `R39-R2`, `R42-R3-07`, `R42-R3-08`, `R42-R3-26`), and 18 remain nonzero when rooted. Only
three of those 18 are in my window and all three are the open residuals I marked `accepted-risk`;
the other 15 must not be marked `fixed-verified` by their owners without a read.

**D-C.** `R42-R2.2`'s source anchor `SKILL.md:562` is the gate-registry **table header**; the row it
records as missing exists at `SKILL.md:608` (`| scratch-root-guard | gate | … | kengaku |`).
The counter splits `source` on `:` and only tests file existence, so the pointer passes while being
46 lines stale. The row's note ("no SKILL.md registry row") is a historical statement; the check
now exits 0.

**D-D.** `R40-R1.1`'s note claims "the tally still counts R40-R1 open". Measured at 4090c3d:
`plans/routed_open.py --lane . --observe` → `ROWS total=71 open=27 blocked=1 closed=41 refused=2`,
`routed_open=28 oldest_round=39`; `--list` → `ROW R40-R1 status=closed`. The base row was closed, so
the transition-row note needs an append-only correction at landing.

**D-E (measurement hazard in the live tree).** While I was reading the live lane, three production
files showed as `M` with identical content: `git diff --summary` →
`mode change 100755 => 100644` for `plans/round42_c1_verify.py`, `plans/routed_open.py`,
`plans/scratch_guard.py`; `git diff --stat` → 3 files changed, 0 insertions, 0 deletions. At
15:20 `ls -l` reported them as **0 bytes**; two minutes later `stat -c%s` reported
35983 / 10877 / 25643, equal to `git cat-file -s HEAD:<path>`. So the live tree passed through a
0-byte window on three counters. No evidence of mine depends on the live tree — I measured in a
`--shared` clone at 4090c3d — but any seat reading the live tree during that window would measure a
hollow file.

**D-F (ruling gap).** The claims doc specifies check exit-0 semantics only for `fixed-verified`
rows. I applied one convention uniformly (§4: exit 0 iff resolved) so a red check on an
`accepted-risk` row reads as "still open", not as a defect. Freeze that sentence, or a reader
cannot distinguish the two.

**D-G.** `R42-R2` and `R42-R4` cannot be `fixed-historical`: their `close` fields start with
`children` and `corpus/QUALITY.md:759`, neither of which resolves as a commit (hex 7-40) or as a
lane-relative path (`plans/round51_routing.py:132-147`). If the L1 prefers `fixed-historical` for
those two, `close` must gain a resolvable first token (`5e3d3aa` and a commit/path respectively) —
that is an edit to a preserved field, so I left it to the L1 and used `fixed-verified`, which their
checks prove in this run.

**Overlaps named, not absorbed (the axis's own signal).** None of these changes an owner in my
fragment; they are rulings for the L1.

1. `R42-R4` — rule 2's canonical text lives **outside** the lane at
   `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118` (read-only for this lane), and
   `shokunin.conf` gives `aggregator` "cross-lane quality, mint and dormancy calls, corpus review".
   kengaku owns the in-lane mirror (`corpus/QUALITY.md:759`, Q34) and its seats' drafting discipline;
   the fleet-side home of the rule is aggregator's. A fleet-side referral would be a **new** row.
2. `R42-R1` — the residual pins a host fact (`uv` absent from `/usr/local/bin`, quoted from
   `F41RevBatCtl.md:89`). `tsukuroi` owns "host operability and repair"; kengaku owns the pin in its
   own counter PINS. Owner stays kengaku; the host fact, if the L1 wants it owned, is a tsukuroi row.
3. `R42-R5` — its source bullet records `(no owner this round)` for `F39OrderGateMut` fail-open.
   That is the axis's "unruled overlap" in the lane's own words; `SKILL.md:590`
   (`order-check`, owner=kengaku) resolves it from committed bytes, which is why I could attribute
   it rather than route it.

## 6. Limits

- I read and attributed **only** rows idx 9..17. The other 62 rows are other seats' windows; the
  whole-ledger scan in §4 is reported as context, not as attribution.
- All nine owners are `kengaku` because every row's subject is a lane-owned artifact. I did not
  invent a `routed`/`referral` row, so the `next` branch and control 3 have no witness here.
- Measurements are at REV 4090c3d in a shared clone. `R42-R4`'s check is `HEAD`-dependent
  (`git diff d69452cf..HEAD -- corpus/SOURCES.md` with zero removed lines); it stays 0 while no line
  is removed from `corpus/SOURCES.md`, and a landing edit that removes one flips it red.
- Checks ran with a 60 s timeout and no network, per the claims' own declared limit; a
  network-dependent check counts as failed.
- `R40-R5`'s authored check covers two of its four named items (declared in §4).
- I did not re-run the C1 counter (`plans/round51_surfaces.py`) — it is outside my item — and I did
  not run `--run-checks` against the live tree, only against the clone.

## 7. Tool installs

None. No install or upgrade was needed for this item; the PACMAN guard was not touched.

## 8. Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C2ExecB` (`TMPDIR` exported there; one `--shared`
clone at `<scratch>/lane`). Removed before yield; the fragment and this report live in the wave dir,
and every number above is quoted inline from the commands in §2, so nothing citable lives in `/tmp`
or in the scratch tree.

VERDICT: 9/9 rows attributed (`owner=kengaku`, evidenced from the lane's own registry owner column
and each row's source bullet) with 5 `fixed-verified` (all checks exit 0 under the frozen counter
once `$LANE`-anchored) and 4 `accepted-risk` (each failing clause isolated and quoted); the fragment
alone makes the frozen C2 predicate print `PREDICATE R51-C2 pass`, exit 0; before-state reproduced
at REV 4090c3d; the systemic defect that blocks the after-target is that 41 of 61 existing checks
are cwd-dependent (fail under the frozen counter's scratch cwd, pass when `$LANE`-anchored) and 14
fail in both contexts, so the L1 must re-root and re-read the ledger's checks before any row can be
`fixed-verified`.
