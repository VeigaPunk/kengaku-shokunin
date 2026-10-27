# R45DistillRouted — routed-ledger dedupe (round 45, wave 1, scout)

Read-only on the lane. Clone `/fast/scratch/hyaku/kengaku-r45/R45DistillRouted/lane` (`git rev-parse --show-toplevel` = that path),
HEAD `52d7486a8caf930855cd1f748032ac21648303f5`. Receipts in `R45DistillRouted/`: `observe.txt` (sha256 `51e464da…3ae8`, 3.5 KB),
`groups.json` (sha256 `682e4705…db6b22`), `proposed-fence-rows.jsonl` (sha256 `1a65d703…bbaa1`).

```
ENVELOPE start 23:26:23 cwd=/fast/scratch/hyaku/kengaku-r45/R45DistillRouted/lane
ENVELOPE end 23:26:26 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

## 1. State

```
python3 plans/routed_open.py --lane . --list      → ROWS total=60 open=23 blocked=1 closed=34 refused=2 / routed_open=24 oldest_round=39
python3 plans/routed_open.py --lane $S/lane --observe (envelope) → OBSERVE rows=60 mismatched=0
```

Identical to the round-44 closing state (`corpus/lessons/round-44.md:109-110`). No round-45 seat has touched the ledger. The round-44
rider patches (`.ufo/waves/round-44/wave/R44RoutedRiders/*.patch`) are still unlanded: `python3 plans/scratch_guard.py --selftest` →
`SELFTEST ok=36/36` (rider needs 37), and `plans/carried_direction_diff.py`, `plans/sources_appendonly.py`, `plans/source_state.py` do not exist.

## 2. The fence findings are NOT in the ledger — finding that changes the closure line

The task expected V1–V3 and LaneInclude to cluster with older fence rows. Measured:

```
grep -ciE 'fence|argv_shape|lane_breach|include' corpus/routed-findings.jsonl  → 2, both false hits
  (R39-R2 "git_leak_probe" file name; R42-R3-35 "plan-missing-refusals")
grep -c 'R44SentinelFences\|LaneInclude\|V11' corpus/routed-findings.jsonl     → 0
```

They live only as prose at `corpus/lessons/round-44-verifier-spotcheck.md:115-119` (§4 "Routed defects the lane must fix next round")
and in `plans/round-45-claims.md:7`. The round-44 burn-down (`round-44.md:106-110`) therefore never counted them, and C1's
`PREDICATE C1 pass` closes **no existing ledger row**. There is no older fence row to cluster with; the fence class is one new cluster of 4
findings, one root cause: *a fence whose verdict depends on git reads that can touch, or fail to describe, a path outside d*.

### G0 — the fence class (4 findings, 0 ledger rows) · high confidence · closed by C1 itself

| finding | where recorded | root-cause leg | refusal module that proves it |
|---|---|---|---|
| `R44SentinelFences` V1 (HIGH) | `round-44-verifier-spotcheck.md:115`; `.ufo/waves/round-44/wave/R44SentinelFences.md:33` | `.git/commondir` delegates the store | `plans/refusals45/f7_commondir.py` |
| `R44SentinelFences` V2 (MED) | same `:115`; report `:104` | second config `.git/config.worktree` include | `f8_worktreecfg.py` |
| `R44SentinelFences` V3 (LOW/MED) | same `:115`; report `:146` | `rc != 0` read as "clean" | `f9_nodescribe.py` |
| `R44LabratLaneInclude` | `:118`; `.ufo/waves/round-44/wave/R44LabratLaneInclude.md` | parent-side `lane_breach` opens include before refusal | `f10_laneinclude.py` |

All four are the legs the frozen round-45 C1 contract lists (pure-filesystem legs first; `rc != 0` = breach; any `.git/config*` include)
and all four have a frozen red module whose round-44 verdict is `ADMIT`/`BREACH opens=4` in
`.ufo/waves/round-45/claims/control-c1-fence-r44.txt:3,10-15`. The older F1–F6 rows (`f1`–`f6`) are round-43 findings already closed in round 44
and are not ledger rows either (`grep` above: 0).

**Closure line (draft):** file the four as rows, class prefix `fence-`, each with
`check = python3 plans/round45_c1_verify.py --lane . 2>&1 | grep -q '^PREDICATE C1 pass'` (`proposed-fence-rows.jsonl`), status
`open` at the freeze, closed together by the C1 pass in one field change. Cost: 4 rows born and closed in one round; benefit: the
round-45 burn-down line counts them, and a failed C1 leaves them visible instead of leaving only prose. (I have not run this check: `plans/fixture_fence.py`
is wave-1 build output and absent at the tip.)

`R44CritV11` (memorizable V11) is the same story: unledgered, closed by the hardened V11 in `plans/round45_c2_verify.py` (a different
class — the C2 grader surface; do not merge with G0). The `check` for it would be the C2 counter's V11 pass line.

## 3. Open ledger rows: 24 rows → 9 groups

The ledger is byte-identical in state to the one `R44DistillRouted` grouped (`.ufo/waves/round-44/wave/R44DistillRouted.md` §3, verdict
`routed-groups-9-from-38` before the 15-row closure patch). I re-read all 24 open/blocked rows' `note`/`check` and re-measured rather than
copy: every group below still holds, and every row has exactly one group (`groups.json`: `open=24 flat=24 missing=∅ extra=∅ dupes=0`).
None is closed by round 45's frozen C1/C2.

| group | rows | one fix | closeable in round 45? |
|---|---|---|---|
| **G1** rider patch set | `R39-R2`, `R42-R3-26`, `R42-R3-27`, `R42-R6` | apply `01`,`01b`,`02`,`03` from `R44RoutedRiders/` + rewrite the `SKILL.md` "not edited" sentence; `git_leak_probe.py`/`scratch_guard.py` are `plans/` files, **not in the frozen set** | yes — files are unfrozen this round (frozen list: counters r44/r45, probe, spec, `pkg_gate.py`, refusals45, battery42-44) |
| **G2** carried-residuals register | `R39-R4`, `R40-R5`, `R42-R5` | one register section naming each F39 residual + one check; retire the 3 bundle rows. Keep `mutant_direction_check.py` (refuses non-round-38 list, exit 2) and `order_check.py` fail-open as named items | partial: register yes; `order_check.py` repair no (pinned by round-42 PINS, → G8) |
| **G3** negative proof for repairs a–c | `R42-R1` | one receipt proving "both tools execute no fixture code" or a red module for a reachable repair | yes, docs/receipt only. Adjacent to G0 (sandbox/fence family) but a different artefact: it proves repairs a–c of the *round-42 counter*, not the round-45 fence |
| **G4** survivor-calibration controls | `R42-R3-34`, `R42-R3-35` | restore control + red modules for `b-xo1-receipt-is-directory`, `b-xo3-emptied-directory`, `b-x13-staged-manifest` | no — `grep -nE 'xo1\|xo3\|x13' plans/round45_c1_verify.py` → 0 hits; C1 covers the ten refusals45 shapes only. `R42-R3-35` is the **only ledger row with a "refusal" in its class** and it is *not* a fence row — do not close it with G0 |
| **G5** plan rows superseded by round-44 freeze | `R42-R3-33`, `R42-R3-37` | swap checks to the round-44 witness run, close with evidence | yes, ledger-only |
| **G6** land the two QUALITY tools with `--lane` | `R42-R3-18`, `R42-R3-19` | land `plans/carried_direction_diff.py` + `plans/sources_appendonly.py` accepting `--lane`, or rewrite both Check lines to the draft path | yes |
| **G7** misdescribed-but-measured-true, one correction pass | `R42-R3-02`, `-05`, `-06`, `-07`, `-09`, `-32` | six one-token text edits (SKILL.md:600 add `:238`; entry `:26-53`; README.md:75 move S128; SKILL.md "equal to the receipt row" → triple; entry clause; lesson E8 naming `measure-final.txt:938`) | yes — corpus/SKILL text, none frozen (note: R42-R3-07's own line cite `:684-685` is stale; locate by the sentence) |
| **G8** freeze-held repairs | `R42-R3-08`, `R39-R3` | schedule a round where `plans/pkg_gate.py` (frozen again this round) and `corpus/defects.jsonl` (pinned by `ledger_tip.py`) are editable | no — both pins still hold; the `blocked` status on `R39-R3` is correct |
| **G9** source-surface state reader | `R42-R3`, `R42-R3-36` | `plans/source_state.py`-style reader of tier-B state + one dated prior-art receipt under `corpus/evidence/` | no wave-1 owner; round-45 C2's S149–S156 are all tier A, so `R42-R3`'s precondition ("a package with a tier-B row") is not met |

Cheapest-first class closures this round (rows removed per artefact): G7 (6 rows / 1 commit), G1 (4 rows / 4 patches already written
and red→green receipted), G6 (2/1), G5 (2/1 ledger edit), G2-register (3/1). That is up to 17 of 24 rows closeable from unfrozen files
alone; G3 adds 1 more.

## 4. Arithmetic

| axis | rows | groups |
|---|---|---|
| ledger rows open or blocked | 24 | 9 (G1–G9) |
| unledgered fence findings (G0) | 0 → 4 proposed | 1 |
| rows/fix-unit | 2.7 (24 / 9) | — |
| rows closeable by C1 or C2 as frozen | 0 | — |

## 5. What I did not merge

- **G0 with `R42-R3-35`/G4**: the only fence-adjacent ledger text; it is about *order-tool substitute fixtures*, and the round-45 counter
  has no leg for them (grep above). Merging would close it falsely.
- **G0 with G3 (`R42-R1`)**: both talk about hostile modules and sandbox repairs, but G3's repairs a–c belong to `plans/round42_c1_verify.py`.
- **`R44CritV11` into G0**: different surface (C2 predictor lint vs C1 fence); a C1 failure must not leave a C2-class row open and vice versa.
- **G1 and G2's `mutant_direction_check.py`**: both touch "the F39 carried items" only by name; one is a tool-contract patch set, the other a register.

## 6. Limits

`--observe` re-runs each row's own check; 6 rows report `observed=n/a` (no check: `R40-R5`, `R42-R3-09`, `-33`, `-34`, `-35`, `-37`) so
their grouping rests on reading, not on a red/green. The proposed fence rows' check was not executed (counter instrument not yet
runnable end-to-end at the tip). Group map was built from this seat's reading plus the round-44 report; if G9 should be split
(weakest merge: two artefacts, one commit), it separates without affecting any other group.

VERDICT: routed-groups-9-from-24
