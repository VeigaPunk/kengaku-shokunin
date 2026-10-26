# F40CritScorecard — round-40 SCORECARD/LOG self-assessment vs the receipts

Seat: critic, kengaku round 40 wave 2 (falsify), hyaku run 9, 2026-10-26. Judged on **calibration**.
Attack: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md` §Round 40 (lines 1450-1498) and
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/LOG.md` round-40 entry (lines 1190-1224) against the receipts:
`.ufo/waves/round-40/integrate/measure-final.txt`, `.ufo/waves/round-40/claims/*.txt`,
`corpus/evidence/round40/db-wal-probe.txt`, the wave-1 reports named in each cell, and the landed tree.

Lane tip read: `c9c793ca33fab1cdaf1127c06ba31685c7db1325`; the documents under audit landed at
`ec1005a2a28bc5cfdde7723374368ed4cc956eed`; the measurement they cite is of landing `ec17216844585d0fecde9f1d4c4be0b78a3bf76f`
(`measure-final.txt:1`). Scratch `/fast/scratch/hyaku/kengaku-r40/F40CritScorecard` (clone `--no-local`, checked out at
`ec1005a2…`, `rev-parse --show-toplevel` = scratch), removed at finish. Every instrument invocation ran in
`bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid
--die-with-parent`. No lane file, git index or jj state touched; no installs; no pacman. Receipts below are copied in
`falsify/F40CritScorecard/` (`round-close-repro.txt`, `registry-row-delta.txt`, `adv-cell-spans.txt`,
`noharm-and-adv-lines.txt`, `numbers-a.txt`, `numbers-b.txt`, `cells-and-frontier.txt`, `c1-before-cell.txt`).

## 1. Numbers that reproduce (checked, not assumed)

Each line was re-derived; the command is in the receipt named in the last column.

| claim (file:line) | receipt | reproduce |
|---|---|---|
| baseline `d3a6277f…`, freeze `bbb10950…`, first run `055748f7…`, landing `ec172168…` (SCORECARD:1452-1453) | `git cat-file -e <h>^{commit}` ×4 | yes, all four objects exist (`numbers-a.txt` §A) |
| C1 landing: `PINS total=3 mismatched=0`, `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (SCORECARD:1460) | `measure-final.txt:4,47-51` | yes |
| C1 before: `fixtures=0`, `killed=0 survived=21`, `PREDICATE C1 fail`, exit 1 (SCORECARD:1460; LOG:1199) | `claims/control-c1-nothing.txt:23-27` | the *stated control* prints exactly this; see M1 for why it is not the before |
| C2 before: `checks=7 defects=4` (V2, V3, V4, V7), exit 1; after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (SCORECARD:1461) | `claims/control-c2-nothing.txt:13-21`; `measure-final.txt:65-73` | yes, exactly those four V-codes |
| probe `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0` (SCORECARD:1461,1473; LOG:1204) | `corpus/evidence/round40/db-wal-probe.txt` tail; `measure-final.txt:642` | yes, byte-equal re-run (`P10 probe_rerun=byte-equal bytes=8257`) |
| SOURCES 111→114, knowledge 46→47, index rows 46→47 (SCORECARD:1461,1482) | `git show <c>:corpus/SOURCES.md \| grep -c '^\| *S[0-9]{3}'`; `ls-tree` knowledge | 111/46 at baseline and freeze → 114/47 at landing; index_rows=47 (`numbers-b.txt` §H) |
| tier A +2, tier B +1 (SCORECARD:1482) | S119 `A`, S120 `A`, S121 `B` (`corpus/SOURCES.md:134-136`) | yes (`numbers-b.txt` §I) |
| "6 of 89" (SCORECARD:1461) | `grep -o '6 of the 89 TB2 task graders' corpus/README.md` | yes (`cells-and-frontier.txt` §J) |
| "22 of 33 cells pinned; nine wrong values pass 7/7" (LOG:1205-1207; entry:31,84) | captured grader assertions; `CASE literals-never-open-db … tests=PPPPPPP` | yes: 11 structural ids + 2 values + 9 names = 22; nine value cells unpinned (`cells-and-frontier.txt` §K) |
| advertised 17 = 13 direct + 4 indirect of 21; 17→0 (SCORECARD:1460; LOG:1203) | `R40CritClaims.md:18` table, `:225` (D4) | yes |
| pytest 8.4.1 28/28; independent 28/28; older SQLite same verdicts (LOG:1209) | `R40CritPytest.md:60`, `R40CritIndep.md:72`, `R40CritSqlite.md:11-15,19-24` (3.40.1/3.45.1/3.54.0) | yes |
| regrade sweep 5 graders, 15 states, 0 flips, 2 graders mutate (SCORECARD:1481-1482; LOG:1215) | `R40RegradeSweep.md:3,57,65-83` (MUT markers only on configure-git-webserver and git-leak-recovery) | yes |
| collisions 37, admit-candidates 2 deferred (LOG:1216) | `R40MergeRescreen.md:30,85` | yes |
| four SOURCES rows re-opened, two locator notes (LOG:1222) | `R40SourcesRecheck.md:11-12,43-44,50` (`VERDICT: sources-rechecked-4-changes-2`) | yes |
| no-harm: round-39 C1 `killed=7`, round-38 C2, round-37 C1 `killed=55`, round-37 C2, round-36 C2 `checks=6`, anchor `rows=114 tokens=21 defects=0`, ledger `mismatches=0`, census exit 0, both frozen-digest runs OK, order_check 38/39/40 = 1/0/0 (SCORECARD:1463-1466) | `measure-final.txt:196-197,218,332-333,354,479-480,501,511,515,573,535-558,79-94` | yes (round-38 C1 is red as landed; see M4) |
| planned numbers: 51 killed/53 survived of 104; `main()` 2 of 32; 71 routed vs 5 ledger rows; `cases=16 … mismatches=2`, oracle 3/3, nop 0/3; PR #245 (SCORECARD:1487-1493) | `R40PlanNext.md:18,29,35,91,239,323` | yes |
| L0 cap question open (SCORECARD:1455) | `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:163` (`kengaku \| round-33` decision packet) | yes |
| capability `round-close-check` verdicts 38→1, 40→0 (SCORECARD:1474) | re-run in the envelope at a clean clone | reproduce **only** with `SHOKUNIN_ROOT` or `--census`; see M5 |

## 2. Mismatches

### M1 — the C1 "before" cell is the empty-battery control, while the same row says every direction was witnessed before freeze

**Attacks:** SCORECARD.md:1460 (C1 row, score cell) and LOG.md:1199 ("Freeze `killed=0 survived=21`").

**Counterexample.** The row's before is `BATTERY fixtures=0`, `MUTANTS total=21 killed=0 survived=21`
(`claims/control-c1-nothing.txt:23-24`) and the row's own title says "every direction witnessed **before freeze**"
(SCORECARD.md:1460). The freeze commit `bbb1095` commits a witness battery that kills 7 of the 21:
`.ufo/waves/round-40/claims/witness-run.txt` (36 lines, committed in `bbb1095` with `claims/witness/w_{anchor,ledger,order}.py`)
ends `MUTANTS total=21 killed=7 survived=14 invalid=0 null_detected=0`. So the pre-round state was not 21-undemonstrated;
the `fixtures=0` control is vacuous by the counter's own kill rule (no fixtures ⇒ nothing can kill).

**Evidence.**

```
$ git -C <lane> show --stat --oneline bbb1095 | grep -E 'claims/(witness|witness-run)'
 .ufo/waves/round-40/claims/witness-run.txt         |  36 ++
 .ufo/waves/round-40/claims/witness/w_anchor.py     |  32 ++
 .ufo/waves/round-40/claims/witness/w_ledger.py     |  25 +
 .ufo/waves/round-40/claims/witness/w_order.py      |  39 ++
$ tail -4 .ufo/waves/round-40/claims/witness-run.txt
MUTANTS total=21 killed=7 survived=14 invalid=0 null_detected=0
$ grep -E 'BATTERY fixtures|MUTANTS total' .ufo/waves/round-40/claims/control-c1-nothing.txt
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=0 survived=21 invalid=0 null_detected=0
```

Receipt: `F40CritScorecard/c1-before-cell.txt`. Wave 1 filed this defect before the landing and it was not incorporated:
`R40CritClaims.md:222` (D1) "7 of 21 are killed by the freeze's own committed witness fixtures; reproduced
`killed=7 survived=14`", `:223` (D2) "the named C1 do-nothing control is vacuous as a before".

**Impacted axes:** calibration (the row's own before→after, and the advertised-count sentence "17 → 0"), and the
SCORECARD's credibility as a state description. Not the frozen predicate, which is correctly quoted.

**Smallest safe correction.** Keep `control-c1-nothing.txt` but label it what it is — the empty-battery non-vacuity
control — and state the before on the committed witness battery: `killed=7 survived=14` (`witness-run.txt`), with the
landing as `killed=21`. In LOG, replace "Freeze `killed=0 survived=21`" with "freeze witness battery `killed=7
survived=14`; do-nothing control `killed=0`". If the calibration count is meant as "the lane's own counter", say so in
the same cell and drop the unqualified "17 → 0".

### M2 — R1's registry-row enumeration names 7 instruments; 5 rows landed

**Attacks:** SCORECARD.md:1476-1477 — "round-39 closure R1 (registry rows for `order_check.py`,
`round39_c1_audit.py` and the five round-40 instruments)".

**Counterexample.** The landing commit added exactly five gate/probe rows and removed none:
`order-check`, `round39-c1-audit`, `round40-c1-mutants`, `round40-c2`, `db-wal-probe`
(`git diff ec17216^ ec17216 -- SKILL.md`). `round_close.py` has no registry row at all
(`grep -cE '^\| \`round-close' SKILL.md` → 0; its only SKILL.md appearance is prose in the round-40 addendum, line 633),
and the `tip-receipts` row pre-existed the landing (`git show ec17216^:SKILL.md | grep -c tip-receipts` → 1). Wave 1's
own list is the same five (`R40RegistryRows.md:9-11,17-31`).

**Evidence.** `F40CritScorecard/registry-row-delta.txt`:

```
  + order-check
  + round39-c1-audit
  + round40-c1-mutants
  + round40-c2
  + db-wal-probe
rows added: 5   rows removed: 0
round-close registry row at tip: 0
tip-receipts row already present at ec17216^: 1
```

**Impacted axes:** operability (registry coverage) and calibration (a routed item reported as more complete than landed).

**Smallest safe correction.** "round-39 closure R1 (five registry rows: `order-check`, `round39-c1-audit`,
`round40-c1-mutants`, `round40-c2`, `db-wal-probe`); `round_close.py` and the tip-receipts derived mapping are
documented in the round-40 addendum prose, not as rows".

### M3 — "each `adv` cell quoting the tool's docstring" is true for 20 of 21 cells

**Attacks:** LOG.md:1198-1199 ("each `adv` cell quoting the tool's docstring at file:line"). The same sentence is in the
landed SKILL.md round-40 addendum (`SKILL.md:626`), so fixing LOG alone leaves a second authority carrying it.

**Counterexample.** L14's `adv` cell quotes `plans/ledger_tip.py:228 '# a crash is an observed failure, never a pass'`
(`measure-final.txt:41`; `plans/round40_c1_verify.py:191-193`). The module docstring is lines 2-63 (`ast.body[0]`);
line 228 is a trailing comment on an `except` clause (`plans/ledger_tip.py:227-228`). Classified mechanically against
all three docstring spans, 20/21 cells are inside the docstring, 1/21 (`L14`) is not:

```
# module docstring plans/anchor_digest_check.py: lines 2-136 ; ledger_tip.py: 2-63 ; order_check.py: 2-42
adv cells inside the tool docstring: 20/21; outside: 1/21 [('L14', 'ledger_tip', 228)]
```

**Evidence.** `F40CritScorecard/adv-cell-spans.txt` (one line per MUTANT with its classified span); wave 1's
`R40CritClaims.md:225` (D4) also records "L14/L15 quote code, not docstrings" (my span check puts L15's `:20-21`
inside the docstring, so only L14 is a code quote).

**Impacted axes:** calibration (the counter's own description of its advertised surface).

**Smallest safe correction.** "20 of the 21 `adv` cells quote the tool's docstring; L14 quotes an inline comment at
`plans/ledger_tip.py:228` (its behaviour is a code comment, not a docstring sentence)" — in LOG and in `SKILL.md:626`.

### M4 — "every no-harm instrument green at the landing tip" contradicts the measurement it cites

**Attacks:** LOG.md:1223 ("every no-harm instrument green at the landing tip (`integrate/measure-final.txt`)"). Same
boilerplate at LOG.md:1145 (round 38) and :1179 (round 39).

**Counterexample.** The cited receipt runs `plans/round38_c1_verify.py` and ends `PREDICATE C1 fail`, `exit=1`:
`measure-final.txt:221` (command), `:330` `MUTANT N21 D5 silence SURVIVED`, `:333` `PREDICATE C1 fail`, `:334` `exit=1`.
The SCORECARD words the same instrument correctly — "round-38 C1 `killed=21 survived=1` as landed"
(SCORECARD.md:1464) — so the LOG sentence drops a qualifier its own source keeps.

**Evidence.** `F40CritScorecard/noharm-and-adv-lines.txt` §a-b.

**Impacted axes:** freshness / calibration (a green/red verdict stated where the receipt says red).

**Smallest safe correction.** "every no-harm instrument is unchanged at the landing tip; round-38 C1 is red as landed
(`MUTANT N21 SURVIVED`, `PREDICATE C1 fail`, exit 1), the rest green".

### M5 — the `round-close-check` evidence command does not run as printed

**Attacks:** SCORECARD.md:1474 — "`python3 plans/round_close.py --lane . --round 38` → exit 1; `--round 40` → exit 0
(wave-1 `R40CloseCheck`)".

**Counterexample.** On a clean clone of the tip with the environment cleared, the printed command exits **2 for both
rounds** (no census script found); the 1/0 verdicts reproduce only with the env var or `--census` — which is how wave 1
recorded it (`R40CloseCheck.md:71`: `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 plans/round_close.py --lane .
--round <N>`, receipt `run-clone-38-39-40.txt`).

**Evidence.** `F40CritScorecard/round-close-repro.txt`, clean `--no-local` clone at `ec1005a2…`, in the bwrap envelope:

```
$ env -u SHOKUNIN_ROOT python3 plans/round_close.py --lane . --round 38
ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH
ROUND-CLOSE RESULT ERROR
exit=2
$ env -u SHOKUNIN_ROOT python3 plans/round_close.py --lane . --round 40
ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH
exit=2
$ SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 plans/round_close.py --lane . --round 38   -> exit=1
$ … --round 39 -> exit=0 ; … --round 40 -> exit=0
$ env -u SHOKUNIN_ROOT … --round 38 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh -> exit=1
$ env -u SHOKUNIN_ROOT … --round 40 --census …                                                        -> exit=0
```

`find_census` (`plans/round_close.py:138-151`) resolves `--census`, else `$SHOKUNIN_ROOT`, else up to six lane parents;
a clone outside the fleet root has no `scripts/sources-census.sh` above it.

**Impacted axes:** calibration (the rubric requires every row's pointer to re-run) and operability.

**Smallest safe correction.** Print the command with its precondition:
`SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 plans/round_close.py --lane . --round N` (or add
`--census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), as `R40CloseCheck.md:71` already does.

## 3. Checked, no mismatch (recorded so wave-2 seats do not re-file or copy an error)

- **`22 of 33 cells are pinned` is correct** (LOG:1207, entry:31,84, `corpus/README.md:73`): 11 `id` cells
  (`ids == expected_ids`), 2 value cells (`id_to_item[1]["value"] == 150`, `[2] == 250`), 9 name cells (ids 3-11) =
  22; unpinned = names 1-2 + values 3-11 = 11 (`cells-and-frontier.txt` §K). Wave-1 `R40CritClaims.md:198-203` §6 item 5
  calls the number "inverted" and says the entry's statement is "22 of 33 unpinned / 11 pinned", but the entry says the
  opposite and the item's own arithmetic (names 1-2 = 2 cells, values 3-11 = 9 cells) yields 11 unpinned. That item is a
  wave-1 report error; do not carry it as a round-40 finding.
- **The claims' witness split "14 by R39PlanNext / 7 here" is off** (R40CritClaims D8: 16 harness / 5 here, L01/L11
  double), but SCORECARD/LOG state only "every direction witnessed before freeze", which holds either way.
- **The measurement is of `ec172168…`** (the SCORECARD's landing hash), not of the docs tip `ec1005a2…`. Re-running the
  cheap no-harm legs at `ec1005a2…` in the envelope shows no drift: `rows=114 tokens=21 defects=0` (anchor, exit 0),
  `rows=9 closed=9 observed_pass=9 mismatches=0` (ledger, exit 0), round_close 40→0 / 39→0 / 38→1. No listed number
  changes.
- **Axis state and held scores** are consistent with the round-39 section (calibration 8, coverage 7, novelty 7,
  depth 9, operability 8, freshness 8, adjacency 8; round-39 C1 cell "8 → 8 held", C2 "7 → 7 held"), and the L0 cap
  question `kengaku | round-33` is open in the fleet queue. No "held" score is contradicted by the repo state.
- **The conformance-incident facts** (shared `~/.local/bin` shim, both attack modules neutralized) check out: both
  modules now `raise SystemExit(...)` at import
  (`.ufo/waves/round-40/build/R40CritC1Counter/crit_git_shim.py:10-12`, `crit_ledger_selfread.py:10-12`).

## 4. Verdict

Five mismatches, one of them substantive (M1: the C1 before/after is presented as 0→21 while the freeze's own committed
witness battery had 7 killed and the row simultaneously says every direction was witnessed before freeze; wave-1 D1/D2
filed it and the landing kept the vacuous control). Three are provenance/count defects (M2, M3, M5) and one is a
green/red wording defect against the cited receipt (M4). None touches a frozen predicate value: C1's landing numbers,
C2's `checks=7 defects=0`, the probe's 28/8/20, and the 111→114 / 46→47 counts all reproduce.

VERDICT: scorecard-mismatches-5
