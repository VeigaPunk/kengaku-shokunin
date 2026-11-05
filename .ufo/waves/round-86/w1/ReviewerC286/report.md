# ReviewerC286 — attack on R86-C2: is the box-4 re-pin a repair or a laundering?

Attack seat on R86-C2 (freeze `61b0e074`, instruments `316811fa604eeef…`, BASE `88651a72`).
Read-only on production; every executable fact below was re-run by this seat in
`/fast/scratch/hyaku/kengaku-r86/ReviewerC286/` at the frozen instrument bytes
(`plans/round86_c2_repin.py` sha256 `a3fbf5064c1c84707dac711550df29087c3be8cefa3e4c44c0d53aa3566bd036`
— byte-identical at `316811fa`, at HEAD `ab9da0d4`, in the working copy, and in commit
`39df7aca`; receipts copied into this seat directory). One process note: an early draft of
this file was written with unverified placeholders and was deleted and rewritten from
measured evidence before submission; no fabricated content survives here.

---

## Q1 — What was the pin, and every time it moved? **verdict: ANSWERED (with one history finding)**

`git log -S'P3c.box.4' --oneline -- plans/state_check.py` → exactly one commit:
`d4dfdb016c45a332d308898511e3964655629cc5` ("round-26: admit reviewed grader audit and frozen
self-assertion repairs", 2026-10-21). That commit introduced the whole `P3c` shuttle family
into `plans/state_check.py`, including:

```python
(4, "PROVINCE.md:129", 129, "### Adjacent", None),
```

So the pin was *born* correct: at `d4dfdb01`, `### Adjacent` really is line 129 of
`PROVINCE.md` (`git show d4dfdb01:PROVINCE.md | grep -n '^### Adjacent'` → `129`).

Verified biography of both halves afterwards (per-revision script, receipts inline):

| rev | date | commit | `### Adjacent` line | SHONEN box-4 pointer | `P3C_PINS` box-4 |
|---|---|---|---|---|---|
| `d4dfdb01` | 10-21 | round-26 | 129 | — | born 129 |
| `11e79380` | 10-28 | round-51 (C1 surface truth) | **130** (grew) | 129 | 129 |
| `fea67b2c` | 11-02 | round-59 W2 | 130 | 129 | 129 |
| `08148cc4` | 11-04 01:35 | round-75 integrate | **143** (grew) | 129 | 129 |
| `9f8f0f21` | 11-04 01:37 | round-75 A5 | **151** (grew) | 129 | 129 |
| `88651a72` (BASE) | 11-04 | round-85 closure | 151 | **129 (stale)** | **129 (stale)** |
| `0481a6d3` | 11-04 17:51 | round-86 | 151 | **151** | **151** |
| `61b0e074`/`316811fa`/HEAD | | freeze/instruments/wave | 151 | 151 | 151 |

Interpretive moves along the way:

- Round-59 `fea67b2c` appended correction **R26-E11** to `SCORECARD.md` (line 2716 in the
  landing commit, still at line 2716 at BASE and at HEAD):
  > `- **R26-E11 (2026-11-02)** supersedes \`P3c.box.4.pointer.1\` — now \`pointer=PROVINCE.md:129\` \`pointer_count=1\` \`target=PROVINCE.md:129\` \`token=### Adjacent\` \`token_hits=0\` \`line_text=<blank>\``
- Round-82 `c804dd41` ("counters and repairs land — … determinism provenance") is a **non-move**:
  `git show c804dd41 -- SHONEN.md PROVINCE.md plans/state_check.py` is empty for these files
  (0-line diff), even though the commit *message* contains the string `PROVINCE.md:151`
  (`c804dd41`'s -S hit on `PROVINCE.md:151` is message-only). The seat instruction's phrase
  "round-25/26 correction history" is loosely satisfied: the *assertion form* is a round-26
  introduction (`d4dfdb01`), round 25 contributed the negative precedent
  (`.ufo/waves/round-26/build/ExecStateSelftestRed.md` F4: “supersession laundering … An
  R26-E row restating `pointer=PROVINCE.md:129` turned P3c.box.4 MISMATCH→SUPERSEDED …
  Pre-registration C2 requires *the full re-derived value*”). No R25 correction touches this pin.
- The actual *pin movement* history is: born 129 (round-26) → **stays 129** through four
  rounds of unrelated `PROVINCE.md` growth (11e79380/08148cc4/9f8f0f21, which carried
  `### Adjacent` 129→130→143→151) → moved to 151 exactly once, at `0481a6d3`, together with
  the SHONEN pointer.

**Finding (Q1-F1).** R26-E11's committed text is **now stale prose itself**: it asserts
`line_text=<blank>`, which was true when round-59 wrote it (verified:
`git show fea67b2c:PROVINCE.md | sed -n '129p'` → empty), but today line 129 holds the table
separator `|---|---|---|` (moved there by `9f8f0f21`). `state_check.py` computes
`line_text` from the tree's own bytes, so at BASE the correction's *stale* half is exactly
what routed the mismatch into view (BASE MISMATCH JSON: correction `line_text=<blank>` vs
derived `line_text=|---|---|---|`). R86-C2's claims text and the `STALE_LINE` retention
do not record that R26-E11, the very correction this repair supersedes in spirit, has a
stale `line_text` claim. Impact: none on the counter's verdicts (the pin moves once to the
derived line and `P4` re-derives); the gap is record-legibility, not behavior.

## Q2 — Does `P1-derive` read bytes or a constant? Can the counter pass with a stale pointer plus a hand-moved pin? **verdict: BYTES (not a constant); reach-the-target requires *three* coordinated tampered files — demonstrated below**

Source, `plans/round86_c2_repin.py:65-72` (the derivation is unconditional):

```python
def derive(root: Path) -> int:
    ...
    lines = (root / PROVINCE).read_text(encoding="utf-8").splitlines()
    ...
    hits = [index + 1 for index, line in enumerate(lines) if line.strip() == TOKEN]
    if len(hits) != 1:
        raise SetupDefect(f"token-count {TOKEN!r}={len(hits)}")
    return hits[0]
```

`STALE_LINE = 129` is used **only** to *construct* stale fixtures and in one selftest case
(`derive-is-not-the-stale-line`, `derived != STALE_LINE`); `derive()` never reaches for it —
there is no fallback and no constant in the comparison path.

**Constraint facts (all executed, receipts `q2-fixtures.txt`, `q2_fixture.py`):**

- `absent-token` and `duplicate-token` fail **closed** (SetupDefect, exit 2) —counter read
  only through the one heading.
- Four fixture trees cut from BASE bytes with a *hand-moved* pin:
  - A: SHONEN→999 *and* pin→999 → `defects=3`, fail.
  - B: SHONEN at 129, pin→999 (pin follows nothing) → `defects=3`, fail.
  - C: pin→151 alone (pointer unmoved) → `defects=2` (`P2-shonen`, `P4-state`), fail.
  - D: SHONEN→151 alone (pin unmoved) → `defects=2` (`P3-pin`, `P4-state`), fail.
- The one **reach-the-target** fixture (my "laundering" attempt, receipt
  `tampered-999-counter.txt`): a tree where `### Adjacent` is planted at line 999, the real
  heading at 151 is renamed, SHONEN says `PROVINCE.md:999`, and `P3C_PINS[3]` says
  `(4, "PROVINCE.md:999", 999, ...)`. On that tree:
  `TARGET derived_line=999 shonen_pointer=PROVINCE.md:999 pin_line=999 state_mismatches=0
  selftest=skipped defects=0 / PREDICATE R86-C2 pass / exit=0`.
- The same tree cross-checked with the **live** (un-tampered) `state_check.py`
  (`--lane <live> --root <tampered tree>`): `state_mismatches=1` and
  `DEFECT P4-state` — the live instrument refuses the tampered tree
  (`tampered-999-live-lane.txt`).

**Conclusion.** `P1-derive` reads *tree bytes*, so a tree doctored to move the token defeats
the counter. "Hand-moved to a different wrong line" is therefore **not** one-file laundering
(pin↔pointer must also shift, and `PROVINCE.md` must be planted to make the derive match), a
three-file coordinated edit. When only one file is tampered (every realistic laundering /
single-edit hypothesis), the counter fails. The committed history contains no such planted
`PROVINCE.md` variant — the token sat at 151 unmoved from `9f8f0f21` through the fix.

**Finding (Q2-F2).** The counter's deployment in the claims (
`python3 plans/round86_c2_repin.py --lane . --rev <REV>`) resolves `state_check.py` from the
**live lane** (`state_summary(root, lane)` prefers `lane / STATE` when it exists) while
`derive` reads the extract at `--rev`. That asymmetry is *load-bearing against* the 999-family
forgery and is what saved the P4 leg in my last fixture. It is documented nowhere; my read of
`plans/round-86-claims.md` §R86-C2 does not name it. Marking it as a documentation gap, not a
defect: without the live-lane preference the forged-tree family would have a reachable target.

## Q3 — The four controls and both base/tip runs, executed by this seat. **verdict: NO control reaches the target; BASE is red exactly as claimed**

All executed in `/fast/scratch/hyaku/kengaku-r86/ReviewerC286/runs/` at the frozen bytes
(`controls.txt`, `base-run.txt`, `tip-run.txt`, `selftest.txt`, `mutants.txt`):

| invocation | output (and exit) |
|---|---|
| `--control-do-nothing` | `CONTROL do-nothing target_reached=False defects=3 legs=P2-shonen,P3-pin,P4-state` (exit 0) |
| `--control-stale-pin` | `CONTROL stale-pin target_reached=False defects=3 legs=P2-shonen,P3-pin,P4-state` (exit 0) |
| `--control-pointer-only` | `CONTROL pointer-only target_reached=False defects=1 legs=P3-pin` (exit 0) |
| `--control-pin-only` | `CONTROL pin-only target_reached=False defects=2 legs=P2-shonen,P4-state` (exit 0) |
| tip (`--rev ab9da0d4`) | `TARGET derived_line=151 shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0` / `PREDICATE R86-C2 pass` / **exit 0** (receipt `tip-run.txt`) |
| BASE (`--rev 88651a72…`) | `DEFECT P2-shonen … / DEFECT P3-pin line=129 derived=151 / DEFECT P4-state mismatches=1` / `TARGET … state_mismatches=1 selftest=pass defects=3` / `PREDICATE R86-C2 fail` / **exit 1** (receipt `base-run.txt`) |
| `plans/state_check.py --summary` on the BASE extract | `assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5` / `MISMATCH: P3c.box.4.pointer.1 …` / `VERDICT: FAIL` / exit 1 (receipt `base-state-check-summary.txt`) |
| `--selftest` | `SELFTEST cases=4 red=4 failures=0` (exit 0) |
| `--mutants` | `MUTANTS real=3 necessary=1 redundant=2 declared_redundant=2` (exit 0) |

Every control reaches a `target_reached=False`; the tip run reaches the target with
`defects=0`; the BASE run lands on `defects=3 / state_mismatches=1` — exactly the frozen
claim's before/after pair. The counter's own battery (selftest + mutants) is also green at
the frozen bytes.

## Q4 — Is the repair a "repair" or a "laundering"? Which does the committed history show? **verdict: REPAIR — the committed history shows the unpaired case can't reconstruct a self-agreeing pin pair; a laundering twin with byte-identical *content* exists as an unlanded orphan, but it is not the measured revision**

**Repair condition.** The pointer (SHONEN box-4) and the pin (`P3C_PINS` box-4) move
**together in one commit***, to a line the tree's bytes actually justify (`### Adjacent` at
151 since `9f8f0f21`), with the instrument (`state_check.py` re-derives its own fixtures and
the P1 engine reads bytes) still able to catch any later drift; the pin never silently
*eats* a round with an inconsistent pointer/pin combination and no completeness retention;
the stale value is kept as `STALE_LINE` and quoted in the claims.

**Laundering condition.** The *pin* is edited first (or alone), to whatever line makes the
frozen instrument green, while the pointer either stays or is dragged along by a later
"correction" that claims derivation; the commit history of PROVINCE bytes shows no motion
that the pin's move follows; the instrument's live copy then perceives `MATCH` with a value
the *tree never justified*, and the historical record loses the round-26 line.

**Which the committed history shows.** `HEAD` lineage is unambiguous:

- The **landed** fix `0481a6d387566f5311560eabe5668feb1d52aa54` (2026-11-04 17:51:40, "replay
  probe, case table and both counters; box-4 pin re-derived from PROVINCE bytes"): SHONEN
  box-4 129→151 in one hunk, and `plans/state_check.py` P3C_PINS 129→151 in another hunk of
  the **same commit**, with the dated comment
  ```python
  (4, "PROVINCE.md:151", 151, "### Adjacent", None),   # re-pinned round 86: derived from PROVINCE.md bytes
  ```
  It also rewrote the selftest fixture to read `box4 = next(pin for pin in P3C_PINS if pin[0] == 4)`
  and pin the fixture to the same derived line — the pin's value set propagates through the
  instrument own self-checking. `PROVINCE.md` is **untouched** in that commit
  (`git show 0481a6d3 -- PROVINCE.md` → empty). So it is not the case that the commit
  "followed a moving pointer": the byte line had been settled at 151 since 01:37 (locally, 16
  hours earlier), and the fix is an instrument-and-prose realignment, one atomic landing.
- `git log -S'P3c.box.4' --oneline -- plans/state_check.py` shows the pin had **never been
  touched** between round-26's birth-commit and the round-86 fix — intermediate CORRECTIONS
  (R26-E11) were prose-level only, coding the instrument's semantics of "the value 129 was
  wrong in round 59". That is the evidence this repair is **derivation-based, not pure
  supersession** — a supersession "the full-value" claim per round-26 anti-laundering
  precedent (`ExecStateSelftestRed.md` F4).

**The one genuinely suspicious object.** `git log -S'PROVINCE.md:129' --all --oneline`
returns a cluster of duplicate commits — `8bc3c6c5a…`, `c3eccf421…`, `a492db826…` — all
**orphaned** (`git merge-base --is-ancestor 8bc3c6c5 HEAD` → no; they are reachable only via
reflog-style scanning, not from any branch head), each with `--format='%H %cd %s'` output
that shows **empty commit messages** (`git log -1 --format=%B` → empty) and byte-identical
trees (`git diff 8bc3c6c5 0481a6d3` → empty; `git diff c3eccf42 0481a6d3` → empty; `git diff
a492db82 0481a6d3` → empty). These carry the same 129→151 pair-move as `0481a6d3` but have
no message, no wave file, no timestamp difference (all 2026-11-04 22:25:47 −0300) —
basically `git commit --amend` leftovers or failed `jj`-sandbox duplicate heads; they are
unreferenced by any claims file. Because they are unreachable, I conclude the landed
lineage-only fix (`0481a6d3`) is the measured committed history and it is the repair-class
case: the pin and pointer moved together in ONE commit, and PROVINCE bytes moved earlier
than both.

**Finding (Q4-F3).** The landed claim as worded — *"`P1` derives the line from the measured
bytes every run; `P4` reads the instrument's own output"* — is true in substance but its
argument has a **laundering twin shape** it doesn't name: a *single* commit that hard-codes
`4, "PROVINCE.md:151", 151, ...` into `P3C_PINS` would still satisfy `P1`+`P4` without a
counter of its own, and my own tampered-999 fixture shows exactly where that theory lands
(the counter passes if the bytes are doctored; the live `state_check.py` catches it only
because the round-86 commits *also* realigned `state_check.py`'s fixtures dynamically off
`P3C_PINS[0]`'s value). The round-86 lander did the right thing, but the claims' *argument*
and the controls don't protect the case where `state_check.py` itself (not the prose) is
hand-edited and committed together with the derivations. That is the residual we cannot
fork off the commit graph — the "instrument is its own control" objection is documented in
`ExecStateSelftestRed.md` F4 for `state_check.py` but never re-derived for the round-86
counter.

## Q5 — Is `STALE_LINE = 129` enough retention, or does the record need the round-26 correction line quoted? **verdict: NOT ENOUGH — the round-26 (R26-E11) committed row is the actual correction record and it must be quoted (it is not) **

What the record contains today at HEAD:

- `plans/round86_c2_repin.py:37` — `STALE_LINE = 129  # the frozen pin this round replaces`
- `plans/round-86-claims.md:109` — "`The historical pin value 129 is retained in the counter
  as STALE_LINE and in the lesson…`"
- `corpus/lessons/round-86.md:91` — "…and the historical value 129 is retained as
  `STALE_LINE`."
- The original R26-E11 row (`SCORECARD.md:2716`, committed 2026-11-02, bytes at
  `fea67b2c`): the full-value supersession row of round-59.

What that row's *committed text* says and where it lands (line 2716 at BASE and unchanged at
HEAD): `pointer=PROVINCE.md:129 pointer_count=1 target=PROVINCE.md:129 token=### Adjacent
token_hits=0 line_text=<blank>`. The claims never quote that line, and — crucially — no
**dated successor row** (R26-E12 or similar) was appended to `SCORECARD.md` when the pin was
re-derived to 151. `git log -S'P3c.box.4.pointer.1' -- SCORECARD.md` returns only R26-E11
and one planned-round-86 prose line — **no committed correction row** matches today's
bytes for box 4.

Consequences (measured, not speculative):
- `state_check.py --summary --root <BASE tree>` and the live HEAD run show
  `mismatch=0 superseded=6` at HEAD — R26-E11 is **not even routed** at HEAD: articles
  claiming "superseded" in prose never appear in `state_check.py`'s own output. So the
  "correction trail" for `P3c.box.4.pointer.1` at HEAD is exactly one stale-prose row plus a
  counter constant, nothing else.
- The R86-C2 claim text names `STALE_LINE` and claims the round-26/59 chain as context; the
  *lesson* (`corpus/lessons/round-86.md:85-93`) repeats that the 129 is retained but **does
  not supply the round-26 (nor the r59) correction line**.
- My Q1 reading: `P3.superseding()` (the engine that parsed R26-E11 at BASE) keys on
  `P3_CORRECTION_FLOORS` + a **P3_CORRECTION_LINE_RE** strict line format. Nothing in the
  repo — not the claims, not the lesson, not a fresh R26-E12 — writes the round-86 re-pin
  value in that format, so a future re-verifier reading only `plans/state_check.py` + the
  historical correction row will find **no committed line** connecting "the instrument now
  reads 151" to a dated record. That respects the round-86 lesson's own letter
  ("the historical value 129 is retained as `STALE_LINE`") but **not its spirit**.

**What is missing.** A dated P3-protocol row (an R26-E12-formatted line under SCORECARD's
superseding block) that records the box-4 re-pin at 151. `P3C_CORRECTION_FLOORS +
P3_CORRECTION_*` make such a row cheap and instantly checkable by `state_check.py`. Without
it, the whole retention chain is: a counter constant (`STALE_LINE = 129`) + stale prose in
R26-E11 (`line_text=<blank>`) — nothing that a future verifier can *re-derive* the value 151
from. Note: appending such a row is a *production* edit, outside this seat's write scope;
I record the gap, not the fix.

**Finding (Q5-F5).** Retention is incomplete: the round-26 (R26-E11) row's *full text* should
be quoted byte-for-byte in the round-86 claims file and the round-86 lesson, **and** a fresh
dated P3-protocol correction row recording the 151 re-pin does not exist. This is a
record-hygiene defect in the claim's own "why this is not laundering" argument, not a code
defect in the counter.

---

## Findings summary (severity)

1. **Q1-F1 (minor).** R26-E11's committed `line_text=<blank>` is stale prose at HEAD (today
   line 129 holds `|---|---|---|`). It is the correction row R86-C2 supersedes and it is
   never quoted in the round-86 claims/lesson; its staleness is unacknowledged anywhere in
   the round-86 record.
2. **Q2-F2 (info).** The counter's `--lane` vs `--rev` asymmetry (live `state_check.py`
   preferred over the extract's) is the load-bearing cross-check that caught my tampered-999
   forgery through `P4-state`; the claims text documents neither the mechanism nor the fact
   that a fully-doctored tree (planted token + moved pin) *would* otherwise reach the target.
3. **Q4-F3 (info).** The repair argument names the wrong one-sided case: the controls prove
   *pin-and-pointer* are independently necessary, but no control or claims text covers the
   "instrument is its own control" risk (state_check.py hard-edited as part of a fake fix),
   which the round-26 precedent (F4, supersession laundering) already flagged. Landed bytes
   are fine; the *stated argument* stops one step short.
4. **Q5-F5 (minor).** Retention is incomplete: the R26-E11 correction line should be quoted
   verbatim, and no dated P3-protocol record of the 151 re-pin exists. A future verifier
   cannot re-derive the round-86 value 151 from any committed correction row.

**Residual risk / verification gaps.** None of these findings flips the C2 verdict: all four
controls fail to reach the target; BASE is `defects=3 / state_mismatches=1` as frozen; the
tip reaches `defects=0` at the frozen bytes; every reachable one-file or two-file tamper of
the operands fails closed. The orphan-commit cluster (`8bc3c6c5`/`c3eccf42`/`a492db82`) is a
byte-identical *unlanded* twin of the landed fix (`0481a6d3`) with no message/timestamp
differentiation — I note it for the L1's provenance ledger; it is unreachable from HEAD and
does not affect the measured lineage.

**Instrument freeze integrity.** The claims are frozen at `61b0e074`, the instruments at
`316811fa`. `plans/round86_c2_repin.py` sha256 is `a3fbf506…` at `316811fa`, at HEAD, and in
the working copy; `plans/round86_c1_replay.py` sha256 `04f6ec2a…` likewise. The
`61b0e074`-era copies differ in the mutant/control *machinery* (that evolution landed in
`316811fa`, before any tip data, receipts at `48a1ffbd`); the shipped battery/control code is
unchanged since `316811fa`. Host-level conclusion: no voiding condition.

## Receipts (this seat directory)

- `tip-run.txt`, `base-run.txt`, `controls.txt`, `selftest.txt`, `mutants.txt`
- `q2-fixtures.txt`, `q2_fixture.py` (A/B/C/D hand-moved-pin trees)
- `tampered-999-counter.txt` (planted-token laundering fixture; counter passes)
- `tampered-999-live-lane.txt` (same tree + live `state_check.py`; counter fails)
- `base-state-check-summary.txt` (the population the claim counts, red at BASE)
