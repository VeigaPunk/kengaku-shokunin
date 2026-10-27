# R44SimplifyCounters — YAGNI review of the per-round C2 counters (report only, no edits)

Seat: simplifier, round-44 wave item `R44SimplifyCounters`. Target: `plans/round3*_c2_verify.py` …
`plans/round44_c2_verify.py` and considerthese/2026-10-26.md proposal 2 ("one standing TB2 admission
counter"). **No lane file was edited, no counter/battery/probe/fixture was executed**, so no envelope block
applies (the host-safety envelope binds runs that can write; every command below is read-only over lane files
plus writes inside my scratch dir `/fast/scratch/hyaku/kengaku-r44/R44SimplifyCounters` and this seat's
subdir). Scratch was removed at the end (`plans/scratch_guard.py safe-rm`).

## 1. Size of the target surface

```
$ cd kengaku-shokunin/plans && wc -l round3*_c2_verify.py round44_c2_verify.py
  234 round36  232 round37  280 round38  282 round39  284 round40
  309 round41  342 round42  410 round43  554 round44        (2927 total, 9 files)
```

Legs grow by exactly one per round since r41 — `def v1..v7` (r37–r40) → `+v8` (r41) → `+v9` (r42) → `+v10`
(r43) → `+v11` (r44):

```
$ for f in round3[6-9]_c2_verify.py round4[0-4]_c2_verify.py; do grep -oE '^def v[0-9]+' $f; done
round37..round40: v1..v7      round41: +v8   round42: +v9   round43: +v10   round44: +v11
```

## 2. Duplication measured three ways

**(a) Raw `diff` line counts (task's asked-for number).** Per-round literals (digests, `roundNN`, task
name, dates) replaced by placeholders first, so a pin rotation does not count as a change.

```
$ for a in 42 43; do diff round$a_c2_verify.py round$((a+1))_c2_verify.py | grep -c '^[<>]'; done
42->43: -57 +125   (410 lines)     43->44: -78 +222   (554 lines)      # raw
42->43:  299/410 carried = 72.9%   43->44:  350/554 carried = 63.2%     # normalized
$ python3 - <<'…' (difflib.SequenceMatcher on normalized lines)
r36->r37 20.3%  r37->38 56.1%  r38->39 94.0%  r39->40 94.4%
r40->r41 86.1%  r41->42 79.2%  r42->43 72.9%  r43->44 63.2%   ratio(r43,r44)=0.7261
```

The carried share falls only because each round appends a *new* leg (r41–r44: +1 leg each); the reusable
body itself never shrinks.

**(b) Whole-chain union.** All nine files normalized, counted as a set:

```
2927 lines total, 869 distinct normalized lines -> 70.3% duplication
(2590 non-blank / 868 distinct -> 66.5%; the top duplicate is `def main():`, x9)
```

**(c) What is actually round-specific in r44.** AST split of the 554 lines:

| part | lines | nature |
|---|---|---|
| docstring | 45 | 27 rule lines (fixed) + **18** round-specific |
| top-level `def` bodies | 355 | **98 new** (V11: `constants`, `states`, `sandboxed`, `v11`), 221 byte-identical to r43, 36 changed (`v2`/`main`) |
| module-level assignments | 83 | **40 per-round** (paths 11 + `CAPTURES` 13 + `DECISIVE` 16), 42 fixed (regexes, `GRADE_PY`, `PREDICT_PY`, sandbox env) |
| imports / blanks / `__main__` | 71 | fixed |

Round-specific total ≈ 40 + 18 = **58 of 554 lines = 10.5%** — i.e. ~89% of the newest counter is
copy-carried standing logic. Function-level identity (bodies, literals normalized):

```
r44 has 22 top-level defs: 16 byte-identical to r43, 3 changed (v2, main, docstring), 4 new
12 of them have identical bodies in r42, r43 AND r44: derive dry receipt_cases rows sha256 spec v1 v3 v4 v5 v6 v8
```

## 3. The cost the proposal is actually about: drift, not bytes

Copies are not merely redundant, they fork silently. Two legs were *fixed* in a new copy and the old copy
kept the bug (its digest was already frozen, so nothing re-runs it):

```
$ diff <(funcs r42 v7) <(funcs r43 v7)      # cited-case-id charset
-        cited = re.findall(r"`([a-z0-9-]+)`", rest)
+        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
$ diff <(funcs r42 v9) <(funcs r43 v9)      # test-letter cardinality
-        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]{3}) ", l)
+        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]) ", l)
```

`plans/round42_c2_verify.py` still carries the pre-fix `v7`/`v9` and no instrument in the lane can re-measure
round 42 with the corrected legs. Second cost: `SKILL.md` carries one registry row per round's counter
(7 `roundNN-c2` gate rows, 7,942 chars; round 44's row is not written yet) which restates the check count,
controls and pinned digests — a hand-copied spec that has to track every leg addition.

## 4. Smallest standing counter that relaxes no leg

**Shape.** One file `plans/tb2_admit.py`, one data file per round `plans/c2-round-NN.json`.

- 554 − 40 per-round assignment lines + ~18-line loader (`--lane`, `--round`, digest-check the data file
  against the round's `frozen-digests.txt` entry) ≈ **532 lines, written once**.
- Legs are untouched. Every leg reads its round constants from a pure-literal module global, assigned once and
  never stored elsewhere, so the whole change is a substitution at **30 load sites**:
  `CAP 5, CAPTURES 5, DRY_REL 4, SPEC_REL 2, DRY_SHA256 2, GATE_REL 2, PROBE_REL 2, TASK 2, DECISIVE 2,
  SPEC_SHA256 1, GATE_SHA256 1, PROBE_SHA256 1, CLAIMS_REL 1` (`ORDER_REL`, `CENSUS`, the five regexes,
  `STATE_KINDS`, `BWRAP/PATH/SANDBOX_ENV`, `GRADE_PY`, `PREDICT_PY` stay module-level — they are the same every round).
- Verified no per-round global is mutated anywhere: 14 store sites, all module-level `Assign` literals.
- Output contract must stay byte-identical: `Vn ok|DEFECT <note>`, `checks=N defects=0`, `PREDICATE C2 pass`,
  exit 0/1 (every `SKILL.md` gate row promises this shape).
- Data file draft for round 44 (built from the frozen literals, no new content):
  `.ufo/waves/round-44/wave/R44SimplifyCounters/c2-round-44.json` — **149 lines / 3,271 bytes**,
  sha256 `5f4f6af3e3966082b22a04b849a12ed8eb4ce9fd3689607a44fd56eafb9a42ae`. Payload counted line by line:
  15 lines carry a 64-hex digest (11 captures + spec/gate/probe/dry), 9 carry a path, 14 are `DECISIVE` case→line
  rows, 8 are predictor parameters (`class`, `grep`, `seed`, `states`, `min_pass`, `min_fail`, `kinds` over two
  lines) plus `round`/`task`; the remaining ~100 lines are JSON brace/key structure of the indent=1 dump
  (a compact dump renders the same 48 payload items in well under 60 lines).

Per-round authoring therefore drops from 554 lines of reviewed Python to ~149 lines of data, and leg logic is
re-reviewed **zero** times. After a second task of an *existing* class arrives, V11 costs 6 data lines instead
of 98 new code lines.

## 5. What must stay per-round (cannot be promoted to the standing file)

| item | why it stays | size |
|---|---|---|
| `DECISIVE` (V10) | the L1's freeze reading of the captures; the *content* leg, not derivable. Already cross-checked against the pinned dry table's case ids (`sorted(DECISIVE) == sorted(frozen_ids)`). | 16 lines |
| capture manifest + spec/gate/probe/dry digests, `CAP`, `TASK`, entry/receipt/readme/claims paths | digest pins are per-round by definition (V1/V2/V5/V9) | 40 lines |
| expected check count `N` + the predicate sentence | the frozen predicate text is per-round (`claims` doc); it grows when a leg is added | 1–2 lines |
| V11 class selection (seed, state count, ≥8/≥8, `kinds`) | data when the class recurs; a **new graded-state class** (module-import, service, repo-history) is a new ~60-line harness in the registry — the one legitimate code addition, added once | 6 lines |
| per-round controls (`control-c2-nothing`, `control-c2-predictor`) | round evidence receipts | — |

**Deliberate duplicates that must NOT be merged** (recorded so a later seat doesn't "clean" them):
`CAPTURES` overlaps `pkg-spec-r44.json` `rows[].capture/sha256` on 9 of 11 files — keeping both is defence in
depth, so V1 does not inherit a tampered spec. The counter's own digest pin
(`frozen-digests.txt`: `plans/round44_c2_verify.py` = `334ce2da…`) stays in its current shape.

**Provenance, never deleted:** the nine counter files themselves, the `SCORECARD.md` rows (12 `c2_verify`
mentions) and `corpus/lessons/*` that cite `plans/roundNN_c2_verify.py` as the instrument of a past round.
Also note `plans/anchor_digest_check.py:31` documents its census shape as "`plans/round37_c2_verify.py`
`SOURCE_ROW`" — that tool is C1-pinned this round (`11bb2cad…`), so a migration would leave a dangling doc
pointer that can only be corrected in a later round; the standing counter must keep the identical `SOURCE_ROW`
regex on a line a future edit can point at.

## 6. Verdict on the proposal (YAGNI)

**Do not build it in round 44.** The r44 counter is frozen and digest-pinned; the migration is r45+ work, and
for a single round a copy is cheaper than the migration. It pays at the first of:

1. the next round that reuses a graded-state class already in the registry (then the round's C2 diff is data
   only, ~149 lines, 0 lines of leg logic — today it is 222 added lines of which ~350 are carried text);
2. the first time an earlier round's C2 must be re-measured at the tip (today impossible: the fixed `v7`/`v9`
   live only in r43+, and re-running a frozen copy re-runs its bugs);
3. a twelfth leg: adding it once beats hand-porting it into a new 554-line copy.

Cost to build: one mechanical pass (30 substitutions + loader + digest-check), plus extracting 9 data files
from the existing counters. Keep every old counter file — they are the pinned instruments of rounds 36–44.

Tradeoffs to name if it is built: one point of failure for every admitted grader; a leg fix then reaches every
round at once (the drift gain and the regression risk are the same property); the predicate sentence per round
changes shape (`--round plans/c2-round-NN.json`) and `frozen-digests.txt` pins the shared counter + the data
file instead of one file; and it fixes *none* of the named content limits (V10's readable key, the counter that
admitted an informed filler — `corpus/lessons/round-43.md:14`). Those are content legs, and a filler control
that must stay red (proposal 2's second half) is a new V12, not a simplification.

## 7. Limits of this report

Read-only static analysis; the counter was not executed, so "no leg relaxed" is proved structurally (pure
literal globals, 30 substitution sites, unchanged output shape), not by a green run. No mutation test of the
standing design was made (that would be a battery, and out of this seat's scope). The 149-line data draft is a
sketch for size, not a landed file.

VERDICT: c2-counter-duplication-70
