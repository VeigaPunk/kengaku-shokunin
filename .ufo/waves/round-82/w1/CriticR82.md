# CriticR82 — round-82 three-claim critique (adversarial, read-only over the lane)

Measured 2026-11-04. Lane master = freeze commit `12f1029a45cf0097a3afd030d757bf93b87f8018`; BASE = `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`.
Method: shared clone in `$HYAKU_SCRATCH/kengaku-r82/CriticR82/clone` (HEAD = `12f1029a`, verified `rev-parse --show-toplevel`), all BASE reads via `git show`/`git cat-file`/`git grep` at `a3a03ac`; the lane itself only `stat`ed/`test -e`d, never written. Scratch deleted before yield.
Claims text: `plans/round-82-claims.md` read in full before any command. No tools installed or upgraded (none needed); pacman untouched.

At measurement time the round's three counters (`plans/round82_c1_plans_registry.py`, `plans/round82_c2_closure_debt.py`, `plans/round82_c3_sweep.py`) and the receipt `corpus/evidence/round82/sweep.txt` do **not exist** at the tip (`git cat-file -e 12f1029a:…` → fatal for all four; the freeze commit carries only `plans/round82-sweep-map.json` and the two evidence files). Several findings below are therefore statements about the frozen text + BASE bytes; where a counter must exist to test a sentence, I say so as *unconfirmed*, never *passed*.

---

## Item 1 — Causal separability: **CONFIRM** (two couplings named)

Commands and outputs:

```
$ git diff --stat a3a03ac..HEAD -- plans/
 plans/round-82-claims.md     | 185 ++++++++++++++++
 plans/round82-sweep-map.json | 504 ++++++++++++++++++++++++++++++++++++
 2 files changed, 689 insertions(+)
```
No `plans/*.py` instrument byte changed BASE→HEAD, so a C3 run's inputs are identical whether C1/C2 have landed or not (for bytes; see coupling 2 for filesystem state).

```
$ git grep -lE "SKILL\.md|SCORECARD\.md|corpus/lessons|SOURCES\.md|routed-findings|corpus/README" a3a03ac -- <the 26 map instruments>
  (no output — none of the 26 instruments reads any document C1's rows or C2's repairs touch)
```

Read/write matrix over committed bytes:

- C1's universe is pinned to BASE (`git show` of SCORECARD.md, LOG.md, corpus/README.md, SKILL.md, `ls-tree` at `a3a03ac`) → C2's new `corpus/routed-findings.jsonl` rows and `corpus/README.md` index line at the tip are invisible to it; C3 writes nothing C1 reads. C1 would pass with C2/C3 unlanded (modulo its own rows).
- C2's universe is the newest `corpus/lessons/round-*-verifier-spotcheck.md` + its own rows + repair artifacts; neither C1 nor C3 writes any of those (C1 writes SKILL.md rows; C3 writes `sweep.txt`; no overlap).
- C3 reads `plans/grader-population-ledger.json` (untouched by C1/C2 — verified in the BASE..HEAD diff), the frozen map (committed in the freeze commit, before any counter existed), and its own receipt. None of the 26 instruments is one of C1's four row targets (`plans/log_appendonly.py`, `plans/round37_c1_attribution.py`, `plans/round66_registry_check.py`, `plans/round80_c1_remint.py` — none appears in the map's instrument set), and V4's edit target `plans/round81_c2_spotcheck_debt.py` is not a sweep instrument. So no claim **writes bytes another claim's universe runs or reads**.

Two couplings the frozen text does not name:

1. **Shared surface:** `.ufo/waves/round-82/w1-results.json` is read by C2's V6 check and written by the wave integration (L1), not by any counter. Absent today (`ls` → `No such file`). Not a claim→claim edge, but it is the one file two round artifacts touch.
2. **Ordering:** C3 runs instruments in the lane worktree; C2's V5 repair deletes `--lane/`, which **exists right now** (`stat` → `--lane mtime=2026-11-04 01:58:44`, exactly the spot-check's V5 stamp). A C3 receipt minted before the deletion and re-checked after it is measured against a different filesystem at the same tip. `--verify-at-tip` re-runs "at the measured tree" — if the tree changes between mint and verify, `reproduced` vs `diverged` can flip for reasons outside C3. No instrument greps as reading/writing `--lane/`, so the risk is bounded but not excluded. Smallest safe correction: the gate should mint and verify the receipt at one integrated tip (state the ordering constraint in the gate's docstring; the frozen "one measured tip" sentence already implies it).

## Item 2 — Do-nothing control: **CONFIRM** — every number re-derived, none overstated

C1, from BASE bytes (scratch script; all via `git show a3a03ac:…`):

```
DOC SCORECARD.md: 136 literal plans/*.py refs
DOC LOG.md: 78 literal plans/*.py refs
DOC corpus/README.md: 83 literal plans/*.py refs
UNIVERSE files=295 referenced=144 intersection=133      # matches the target's rows=<133+4> anchor
universe=133 registry-names=134 table-rows=134           # at tip; 134 = 1 header row + 133 data rows
universe NOT in registry: ['plans/fixture_fence.py', 'plans/log_appendonly.py',
 'plans/policy_cases.py', 'plans/round37_c1_attribution.py', 'plans/round66_registry_check.py',
 'plans/round80_c1_remint.py']
```
CLI split from file bytes at BASE: `fixture_fence.py argparse=False __main__=False`, `policy_cases.py argparse=False __main__=False` → the 2 `UNCLASSIFIED` (support-module exclusions); the other four `argparse=True __main__=True` → the 4 `MISSING` (a CLI cannot be a support module). `rows=<133+4>`: 133 data rows at tip + 4 = consistent (134 table lines include the `| name | kind | entry | … |` header).

C2, from BASE bytes:

```
$ git show a3a03ac:corpus/routed-findings.jsonl | wc -l        → 117
$ git show a3a03ac:corpus/routed-findings.jsonl | grep -c R81-V → 0
$ grep -c '\*\*V[0-9]' round-81-verifier-spotcheck.md §5        → 7 bullets (lesson lines 195,200,205,208,211,213,218)
```

C3 absences, from BASE bytes:

```
$ git cat-file -e a3a03ac:plans/round82_c3_sweep.py             → fatal, absent
$ git cat-file -e a3a03ac:plans/round82-sweep-map.json          → fatal, absent
$ git cat-file -e a3a03ac:corpus/evidence/round82/sweep.txt     → fatal, absent
```
(plus both C1/C2 counters absent at BASE). All 13 numbers of `freeze-controls.txt` reproduce exactly. **Nothing to contest.**

## Item 3 — C3 target reachability: **CONTEST**

**(a) The three-places sentence cannot be quoted from committed bytes.** The claims freeze: *"each predicate sentence below is the same sentence in the counter's code and in the round's receipts."* Today:
- Predicate (exists): claims file, R82-C3: "`Target (after): TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=0`, `PREDICATE R82-C3 pass`, exit 0."
- Counter: `plans/round82_c3_sweep.py` — absent at tip (fatal). **Cannot quote `histogram_total=26` in code.**
- Receipt: `corpus/evidence/round82/sweep.txt` — absent at tip. **Cannot quote it in the receipt.**
Sentence identity is *unconfirmed*, not established. Expected mid-wave; the claim as frozen is currently a promise about bytes that do not exist.

**(b) The `--check` target is hand-satisfiable; the runtime tripwires are described twice, differently.** `--check` is specified as "verdict over committed bytes". Anchor evidence: **0 of the 26 committed member receipts carry an `EXIT` or `COMMAND` line** (script over the map's receipts: `receipts with EXIT line: 0/26 ; with COMMAND line: 0/26`). So a receipt's per-member `exit=`/`secs=` are self-asserted; nothing committed anchors them to a run. Construction: for each of the 26 members take the map's `argv` (which `--check` itself reconstructs for the COMMAND-MISMATCH leg), copy the committed receipt's projected observation lines (identical instrument bytes BASE↔tip, verified in item 1), stamp `status=reproduced`, choose any `exit=`/`secs=`, sum the histogram to 26 — an internally consistent, hand-written `sweep.txt` is indistinguishable from a run-produced one to any committed-bytes check.

The frozen text then assigns `--verify-at-tip` two different jobs:
- "`--verify-at-tip` re-runs its own `--selftest` battery at the measured tree (round-80 plan item 4)" — selftest only, instruments not re-run → the fabricated receipt survives everything;
- "The capability enters the SCORECARD capabilities table only when `--check` exits 0 at the tip **and `--verify-at-tip` reproduces the receipt's classification**" — instruments re-run → fabrication caught wherever a member genuinely diverges at the tip.

Smallest safe correction: implement `--verify-at-tip` as the second sentence (re-run all members, diff classifications) and state in the gate that `--check` alone cannot certify authenticity. Until the counter lands, this is the one un-closable hole in the claim's own text.

## Item 4 — Projection laundering: **CONTEST** (three findings, one concrete member)

**(a) "reused unchanged" is false.** round-80-claims.md:49 keeps `^CASE `, `^case=`, `^cases=`, `^MISMATCH `, `^OBSERVED-U `, `^VECTOR `; round-81-claims.md:52 keeps `^case=`, `^cases=`, `^MISMATCH `, `^OBSERVED-U `, `^VECTOR `. R82-C3 keeps `^(CASE |case=|TEST |VECTOR |LEG |regrade )` — it **stops keeping `MISMATCH ` and `OBSERVED-U `** and adds `TEST / LEG / regrade `. Consequently the frozen drop-clause "lines starting `OBSERVED-U `" is dead by construction: the keep-pattern can never match such a line.

**(b) Concrete laundering channel — three instruments emit the dropped signal.**

```
a3a03ac:plans/round58_c2_kl_probe.py:396:        lines.append(f"MISMATCH {name} " + "; ".join(bad))
a3a03ac:plans/round59_c1_openssl_probe.py:363:   lines.append(f"MISMATCH {name} " + "; ".join(bad))
a3a03ac:plans/round61_c1_cancel_probe.py:483:    lines.append(f"MISMATCH {name} " + "; ".join(bad))
```
A replay of these members that drifts into emitting/changing `MISMATCH` lines with an unchanged exit classifies `reproduced` under R82's projection; under the round-80/81 projection the same drift is `diverged:<n>`. The committed receipts show 0 `MISMATCH` lines today (no drift at BASE) — the hole opens exactly when the sweep's target event occurs, contradicting "nothing is laundered into `reproduced`".

**(c) Dropped-line census per member, derived from the 26 committed receipts** (keep-pattern → drop `cases=`, drop `CASE|case=` lines whose `predicted=` contains `U`):
- `cases=` lines: **0 in all 26 receipts** — the drop clause is vacuous over every committed receipt.
- `predicted=U` CASE lines: **only `largest-eigenval`** (instrument `plans/round57_c2_eigen_probe.py`, which prints `OBSERVED-U …` at :324): 2 CASE lines with `predicted=U` + 1 `OBSERVED-U` line = 3 of its 41 receipt lines hidden; kept=24, residual=22. A divergence confined to those 2 lines' `observed=`/`tests=` fields or the OBSERVED-U payload, exit unchanged, is invisible. `largest-eigenval` is the member whose divergence the drops would hide.
- No member has residual=0 (fully-laundered); smallest visible surfaces: `pypi-server` residual=4 of 17 lines, `torch-tensor-parallelism` 10 of 47.
Since the projection text is frozen, the smallest safe correction is at landing time: either keep `^MISMATCH ` in the receipt's compared projection and document the deviation from the frozen sentence, or raise an L0 question before the gate lands — silently implementing the false "reused unchanged" sentence bakes the channel in.

## Item 5 — C2 discharge quality, V1…V7 (restatement trap → does the planned artifact clear it?)

BASE bytes confirm every defect first: `c2-after.txt:3` = `WORKTREE dirty (1 paths)` (LANE_TIP `604be350…`); `tb2-file-artifact-replay-classes.md` opens with a thesis paragraph, no `source:/verified-at:/recheck:`; `round81_c2_spotcheck_debt.py:384` "Six attributed data mutations" vs `real=4`; `--lane/` present (mtime matches the spot-check to the minute); `determinism.txt` carries only two `rc=/sha256=` lines, no COMMAND/REV; the two word-miscounts re-derived below.

- **V1 — clears, with a named trap.** Repair = re-mint from a clean tree + dated lesson correction. Trap: the spot-check's own alternative leg ("make the C2 paragraph cite `gates-clean.txt@39bbe9a4`") is a restatement — re-anchoring prose, not repairing the receipt. The planned artifact takes the re-mint leg → clears iff the check re-derives the stamp from the re-minted receipt and fails on BASE's dirty stamp (sensitivity leg as frozen).
- **V2 — strongest documentation repair; I reproduced the defect myself.** Quote 1: "Write a CSV file /app/summary.csv with the following structure (including the header):" → whitespace-split = **12** words (lesson says 14). Quote 2: "The goal is to extract this secret key and save it to `/app/results.txt`." → **13** words (lesson says 17). The check recomputes mechanically, so the corrected constants are enforced and revert-sensitive. Clears.
- **V3 — weak predicate, real restatement trap.** The frozen check only demands the trio *opens with* `source:`, `verified-at:`, `recheck:` — presence, not content. A vacuous trio (source: itself, any date, `recheck: none`) passes. The lesson prescribes real values (S260/S261, tip, counter command). Clears only if the counter pins the values, which cannot be confirmed until it lands.
- **V4 — the claim blesses a restatement leg.** Docstring says six mutants, battery prints `real=4`: correcting the docstring blesses a battery that lost two mutants without asking where they went; adding the two mutants is the repair. The frozen text allows both ("fix the docstring (or add the two missing mutants)"). Either passes the recomputing check. Quality undecidable until the wave's bytes say which leg it took.
- **V5 — strongest of the seven.** `test ! -e ./--lane` tests the filesystem; deletion is the repair; the lesson note is garnish. Cannot be restated away. Clears (the directory still exists now, so the repair is pending, not fake).
- **V6 — weakest discharge, two flags.** (i) The repair artifact is `.ufo/waves/round-82/w1-results.json` — the wave's own bookkeeping about itself; the check reads a file the satisfied party writes (self-referential). It is absent today, so V6 cannot have passed yet. (ii) Provenance: the live mutation-tester seat in the roster is **`R78MutC1`**, a round-78-prefixed seat, not an r82 seat. If the attack-share numerator rests on a carry-over seat, the "live `mutation-tester` seat" leg needs the L1 to record why it counts; otherwise the discharge inherits the exact defect V6 routed (round 81 counted a sentinel as its fourth attack seat).
- **V7 — clears only against the stamped hashes, and there is a live contradiction to resolve.** The spot-check itself reports its replay hashing `4ca4c612…`/`5fb7aa35…` while the receipt stamps `43a8c276…`/`8d3471f9f6238c63` — the receipt's hashes are **not** reproduced by the spot-checker's own plain replay. Pasting a COMMAND+REV therefore clears only if that command's replay reproduces the *stamped* hashes; if it reproduces the spot-check's instead, the repair must re-stamp the hashes (re-measure), not just paste. The frozen sentence ("so its two hashes are re-derivable") implies the check re-runs the command — restatement trap = paste an invocation that was never the producer.

---

## What I could not break
- C1's 4 MISSING / 2 UNCLASSIFIED / 133-universe arithmetic and every number in `freeze-controls.txt` (item 2).
- The separability of the three counters' read/write sets over committed bytes (item 1) — no claim writes bytes another claim's universe reads or runs; the two couplings named are ordering/bookkeeping, not read collisions.
- All 26 map instruments exist at BASE; none reads a C1/C2-touched document; instrument bytes identical BASE↔freeze.
- `largest-eigenval`'s residual is 22 lines — the U-drop hides a bounded slice (3 lines), not a whole member; no member's projection is empty.

## Unattacked / unconfirmed (counters absent at tip)
- Whether `--check`'s printed `TARGET …` sentence equals the counter's code string and the receipt's line (item 3a) — cannot be tested until `plans/round82_c3_sweep.py` and `sweep.txt` are committed; my item-3(b) construction is the standing test to run against them.
- Whether the C2 counter's V3 leg pins the trio's values and which V4 leg the wave took — both need the landed bytes.
