# F37RevScorecardLog — round-37 wave-2 (falsify): SCORECARD.md §Round 37 + LOG.md §Round 37 @ `357deceb`

Seat: reviewer (leaf). Reviewed tip: `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` (branch master, pushed).
Lane working tree sat at `dc90676b` (dirty, 2 modified files), so **every lane read was `git show 357dece:<path>`** — no working-tree file was trusted for review content. Scratch `/fast/scratch/hyaku/kengaku-r37/F37RevScorecardLog` (clone at the tip + counter re-runs; removed at the end; reproduction receipts copied to `.ufo/waves/round-37/falsify/F37RevScorecardLog/{c1,c2,census}.out`). No lane file was edited; no mutating git/jj command was run in the lane.

## Assignment checks

### 1. Counting commands verbatim from the claims file — PASS
- SCORECARD C1 row (line 1277): `python3 plans/round37_c1_verify.py --lane .` — byte-identical to the claims predicate (`plans/round-37-claims.md` §C1). Quoted output strings match the claims word-for-word: before `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1; after `…killed=55 survived=0…`, `PREDICATE C1 pass`, exit 0.
- SCORECARD C2 row (line 1278): `python3 plans/round37_c2_verify.py --lane .` — byte-identical to the claims predicate; before `checks=7 defects=4` (V2, V3, V4, V7), after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 — matches claims §C2 verbatim.
- LOG names the same counters (`plans/round37_c1_verify.py`, probe, `plans/ledger_tip.py`, `plans/anchor_digest_check.py`); every number it quotes is reproduced below.

### 2. Before/after values equal the committed receipts — PASS (all values, all receipts committed at the tip)
| value in SCORECARD/LOG | committed receipt | match | my independent check |
|---|---|---|---|
| C1 before `fixtures=14 … killed=5 survived=50 … fail`, exit 1 | `.ufo/waves/round-37/claims/control-c1-nothing.txt` | exact | — |
| same, "also on committed bytes at `44b7298a`" | `claims/measure-before-committed.txt` (TIP line `44b7298ae1e0…` = commit `44b7298`, verified in history) | exact | — |
| C1 after `fixtures=64 … killed=55 survived=0 … pass`, exit 0 | `integrate/measure-final.txt` | exact | **re-ran on my clean clone at 357dece: identical lines, exit 0** |
| C2 before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 | `claims/control-c2-nothing.txt` | exact | — |
| C2 after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 | `integrate/measure-final.txt` | exact | **re-ran on my clone: V1–V7 ok, identical, exit 0** |
| probe `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | `corpus/evidence/round37/git-webserver-probe.txt:49` | exact | — |
| registry 103 → 107 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on `git show` at `3ea9a1d9` → 103, at `357dece` → 107; `measure-final.txt` `registry_rows=107` | exact | re-ran both greps |
| knowledge/index 43/43 → 44/44 | `control-c2-nothing.txt` gate P8 `index_rows=43 knowledge_files=43`; `measure-final.txt` P8 `44/44 bad=0`; index file is `corpus/README.md` (`integrate/measure.sh:24`) | exact | my clone C2 run: V2 ok (gate green ⇒ P8 44/44) |
| census exit 0 before and after | `claims/census-before.txt` exit=0 (15 W04); `measure-final.txt` census exit=0 | exact | my clone: exit 0, 15 W04 |
| anchor `rows=103 tokens=11 defects=5` at `3ea9a1d9` → `rows=107 tokens=15 defects=0` | `build/R37AnchorSweep/fixture-receipt.txt:8` (see D1) + `corpus/lessons/round-37.md:40`; after: `measure-final.txt` | exact | my clone: `rows=107 tokens=15 defects=0`, exit 0 |
| ledger `rows=9 closed=9 observed_pass=9 mismatches=0` | `measure-final.txt` `ledger_tip.py` block | exact | — |
| freeze digests (`ea638822…` gate, `4c61d103…` spec, `63cb75cf…` probe, both counters) | `claims/frozen-digests.txt` | exact | `git show 357dece:<file> \| sha256sum` → all five equal; gate digest also equal at baseline `3ea9a1d9` (gate unedited ✓) |

Named commits all exist: `ca790460` (freeze, 01:30), `5c7b34e9` (first recorded probe run, 01:32), `44b7298a` (01:36), `a3163e67` (battery, 01:47). Freeze tree at `ca79046` contains claims, both counters, the dry-case table, the six tb2-git-webserver captures + SHA256SUMS, and the red controls — matching LOG's freeze description.

### 3. Capability rows carry a demonstration command — PASS
- `gate-mutation-harness` (SCORECARD:566): `python3 plans/round37_c1_verify.py --lane .` on a clean clone → quoted outputs match `measure-final.txt`; freeze control `killed=5` cited with the claims path. First-working round 37.
- `service-grader-probe` (SCORECARD:567): `python3 plans/git_webserver_probe.py --lane .` → `cases=22 observed_pass=9 observed_fail=13 mismatches=0` matches the probe receipt; "read the summary line, not `$?`" caveat; re-run byte-equal backed by `measure-final.txt` P10 `probe_rerun=byte-equal bytes=8443`. First-working round 37.
- Table note ("rows enter only through a round that demonstrates the capability running") is honored by both rows.

### 4. No score raised beyond the rubric — PASS
- C1 row: "**8 → 8 held**"; C2 row: "**7 → 7 held** (L0 cap)"; "Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8" — identical to the claims' frozen axis selection. No axis moved, so the rubric's "±1 per axis-move" is not stressed. Before-values truthful: round-36 close row says calibration "**8 → 8 held**"; round-25 row holds coverage at 7 ("cap unchanged"); round-24 declaration basis "novelty 7 / calibration 8".
- Both rows carry explicit no-raise rationales that match the claims' named limits (C1: denominator is the lane's own mutant list, demonstration observational; C2: counter admits an informed filler package / spec template not digest-pinned — verified true of `plans/round37_c2_verify.py` (reads `SPEC_REL` from the tree, pins only `receipt_sha256`), with wave-1 variants v1/v4/v5 reaching `checks=7 defects=0` in `build/R37CritC2Counter.md`).

### 5. Coverage cap stated — PASS
- "Coverage stays capped at 7 by the open L0 question (`.ufo/l0-questions.md`, `kengaku | round-33`)" (SCORECARD §Round 37) and "(L0 cap)" in the C2 row. Pointer resolves: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:163` carries the `kengaku | round-33` line (fleet-root-relative path — the convention since rounds 25/33; `R33L0Packet.md` cites the same file:163). The line shows the cap question still open, consistent with 7 held.

## Findings

**D1 (low) — wave-1 `build/` receipts cited by the SCORECARD/LOG round-37 sections are not committed at the reviewed tip.** `git ls-tree -r --name-only 357dece .ufo/waves/round-37/build/ | wc -l` → **0**, yet the sections cite `build/R37CritC1Battery.md`, `build/R37CritC1Battery/receipts/attr-honest.txt`, `build/R37CritCases.md` §2.1, `build/R37CritC2Counter.md` (v1, v4), `build/R37DockerOracle.md` (SCORECARD limits) and `build/R37IndepVerdicts.md`, `build/R37TipSweep.md`, `build/R37ScoutMergePkg.md`, `build/R37ReopenPins` (LOG), and `corpus/lessons/round-37.md` cites `build/R37AnchorSweep/*`. At `357dece` a clean clone cannot re-run those pointers — the lane's own rubric anchor "every row's pointer re-runs" is satisfied only from the next commit `dc90676b` (close commit; 290 build files committed there; all ten cited paths present). Mitigation, verified: every number quoted from those reports matches the working-tree copies I read (`INDEP agree=22/22 extra=3/3`; sweep "Baseline table (25/25 green)" incl. `grader.py` rows 1–2; "Totals over the 10 verdict rows: 0 admit, 7 refuse, 3 hold"; image `alexgshaw/configure-git-webserver:20251031` pulled and `rmi`'d; 6/6 identical, `main` at the pin; `UNATTRIBUTED=0` / hostile `6/55 UNATTRIBUTED=49`; CritCases `VERDICT: cases-22-confounded-4-uncovered-extra-4/4` backing "four case labels"; `bubblewrap 0.13.1` in `R37ProbeRerun.md:20`) — and the value-bearing predicate receipts (`claims/` 13 files, `integrate/` 7 files) **are** committed at `357dece`. Citation-sequencing defect, no fabrication found.

**D2 (low) — LOG freshness sentence attributes `grader.py` green to the landing tip via a receipt that does not contain it.** LOG §Round 37: "the round-36 counters, `grader.py` and every registry gate stayed green on the pre-landing sweep (`build/R37TipSweep.md`, 25/25) and at the landing tip (`integrate/measure-final.txt`)." `measure-final.txt` contains no `grader.py` invocation (`measure.sh` runs the two r37 counters, anchor check, r36 C1/C2 counters, census, sha256sum, `ledger_tip.py`; no counter invokes `grader.py` — grep over all four counters: none). `grader.py` green is receipt-backed only for the pre-landing sweep (TipSweep rows 1–2). The round-36-counter and registry-gate halves are receipt-backed at the tip (measure-final: `round36_c1_verify` pass, `round36_c2_verify` 6/6, census exit 0, V3/P6 ok). Fix: scope `grader.py` to the sweep or re-run it at the tip.

## Residual risk / verification gaps
- `measure-final.txt`'s TIP line is `5c7d5d75…` (the pre-docs landing commit), not `357dece`. The commits between (`aa3d6ea`, `188a265`, `357dece`) touch no counter-readable file (diffstat: falsify dispatch/spec, SCORECARD +8, lessons +1, `plans/round37_c1_attribution.py` + attribution receipts) — and I reproduced C1/C2/anchor/census at `357dece` with identical values, closing the gap. Not counted as a defect.
- I did not re-run the 22-case probe, the hostile battery, or the docker/oracle run myself; those rest on the committed probe receipt plus wave-1/wave-2 replications quoted above (all cross-checked against the cited reports' contents).
- "No other installs" (LOG tool-use bullet) is a negative claim over 36 wave-1 seats not fully repo-verifiable; the two named tools are receipt-backed (`pkg_gate.py:276` pins `biopython==1.85` for the P10 re-run; bwrap version in `R37ProbeRerun.md`).
- Probe exit semantics ("read the summary line, not `$?`") not independently exercised by this seat.

Reproduction receipts: `.ufo/waves/round-37/falsify/F37RevScorecardLog/{c1,c2,census}.out` (my clean-clone runs at `357dece`).

VERDICT: scorecard-log-2-defects
