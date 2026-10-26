# R36ConnAmendment — cross-lane precedent survey: is Amendment 1 a ratchet, a revision, or a rule change?

Seat: R36ConnAmendment (connector, wave 1, round 36). Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. All lane files read-only; no lane file was
written. Scratch: `.ufo/waves/round-36/build/R36ConnAmendment/`.
Nothing was appended to `.ufo/l0-questions.md`.

---

## 1. The question this seat answers

`plans/round-36-claims.md:123` opens:

> `## Amendment 1 (pre-scoring instrument repair, disclosed; recorded after freeze 3241b86c, before any seat dispatch)`

and ends (`:136-139`):

> `Whether a pre-scoring mechanical repair of a frozen instrument is a new revision or voids the claim is the open question already on the L0 queue (revenger | round-69); this round proceeds on the disclosed amendment and reports the verdict either way.`

The task asks for the common rule the five sibling precedents each applied, how each worded its
verdict, and a recommendation on the three-way label.

**Recommendation: `revision`** — specifically a *new pre-scoring revision* in revenger r69's own
formulation ("a NEW pre-scoring revision with a fresh red-before"), **not** a ratchet and **not** a
rule change. The reasoning and the two disclosure gaps that must accompany the label are in §5–§7.

---

## 2. The five sibling precedents, with file:line

### 2.1 The L0 question lines (all five, verbatim anchors)

| # | lane / round | L0 line | the ruling asked for |
|---|---|---|---|
| P1 | `tabi \| round-22` | `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:155` | "is a disclosed, value-neutral encoding revision admissible under the §9 clause 'a rule changed after any seat has scored is not the claim's rule', or must such a round republish the pre-revision rule and report 0?" |
| P2 | `revenger \| round-68` | `.ufo/l0-questions.md:156` | "May the next round replace marker-presence with behavioural legs and drop c7_v3_clean from HOLDS_OK_V6, or should the frozen instrument stay as-is and the gap remain a named limitation?" |
| P3 | `revenger \| round-69` | `.ufo/l0-questions.md:160` | "may the L1 land a mechanical counter repair … as a NEW pre-scoring revision with a fresh red-before, or must the claim stand falsified and the fix wait a round?" |
| P4 | `kumitate \| round-63` | `.ufo/l0-questions.md:167` | "Is that a ratchet within the declared rule, or a rule change that voids C1?" |
| P5 | `kumitate \| round-64` | `.ufo/l0-questions.md:170` | "accept this as a ratchet (A), or rule the claim must be re-frozen in a new round (B, costs a round)?" |

All five lines are still **unruled** (no `L0 ANSWER` marker on any of them; the only two `L0 ANSWER`
markers in the file, `.ufo/l0-questions.md:52` and `:53`, are kama/planner-taxonomy questions).

### 2.2 How each sibling report worded its verdict

**P1 — tabi round-22** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-22/tabi.md`)

- `:37-41` — "Receipt `.ufo/waves/round-22/expectation-revision.json`; note errata appended at
  `corpus/knowledge/webmcp-lifecycle-oracle-round-22.md` §Errata. **Value neutrality is measured, not
  asserted: 12 at the pre-revision oracle `e3cf4e0`, 12 at the post-revision oracle `47bfb5f`**."
- `:209-212` — "this round treats it as admissible *because* the value is identical before and after
  and nothing was narrowed".
- `:213` — "The round did not block on it."
- Note the strictness of the case: the L0 line says the revision was authored "after the data was
  observed **and** after this lane's own W2b seats had scored the pre-revision rule"
  (`.ufo/l0-questions.md:155`) — i.e. the §9 trigger *was* engaged — and tabi still treated it as
  admissible on the value-neutrality + nothing-narrowed grounds, while filing the question.

**P2 — revenger round-68** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-68/revenger.md`)

- `:139-142` — "Reported, not hidden: two critics show the predicate is satisfiable by a gate that
  does not detect drift. … the instrument gap is **routed rather than repaired after the wave** (the
  reviewed artifact stays the measured artifact)."
- `:289` — the L0 line is quoted in full in the report; `:291` — "The round does not block on it."
- The C7 instrument and every V-label were left exactly as they were.

**P3 — revenger round-69** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-69/revenger.md`)

- `:24-25` — "**Verdict: FALSIFIED** — its frozen predicate reads four counter labels that the pinned
  instrument cannot print; **the instrument defect is reported, not repaired after scoring**."
- `:105-108` — "The diagnostic column is one mechanical relocation of the pinned counter (`def run`
  hoisted above its first use, +67 bytes of layout, helper bytes unchanged) … it is disclosed in
  `reports/round-69/measure-after.log` and is **not the claim's measurement**. **C2 FALSIFIED as
  declared**."
- `:203-206` — the round-68 question "stands unanswered and is not pre-empted"; a second question is
  filed asking whether a frozen instrument's crash "may be repaired in-revision when the claim is
  otherwise unevaluable".

**P4 — kumitate round-63** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-63/kumitate.md`)

- `:15` — "**Gate ratchet (declared in the plan before data)**: … selftest 25 → 69 cases; controls
  14 → 75 (`.ufo/waves/round-63/controls/CHANGES-AFTER-FREEZE.md`, committed `05b31769`, `144f11f5`)."
- `:51` — "**the operator rules on the control-set changes** and on the counters' known holes."
- `:70` — "the post-freeze control changes are **disclosed rather than hidden**."
- The disclosed file `kumitate-shokunin/.ufo/waves/round-63/controls/CHANGES-AFTER-FREEZE.md:12`:
  "`probe/inline63-probe.mjs`, `probe/topology63-probe.mjs` and the C2 controls are **NOT changed**.
  Known counter holes found by wave 1 are **reported, not patched**."

**P5 — kumitate round-64** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-64/kumitate.md`)

- `:31` — "Post-freeze ratchet changes are disclosed in `.ufo/waves/round-64/controls/CHANGES-AFTER-FREEZE.md`:
  **no counter, threshold or pin changed**; controls grew 16 → 50, the tool v1 → v3, the demo v1 → v3.
  The freeze's own P2 floor was unreachable and was met by the declared ratchet, which the operator may
  rule on (L0 question appended)."
- `kumitate-shokunin/.ufo/waves/round-64/controls/CHANGES-AFTER-FREEZE.md:4-7` — "The **plan's declared
  ratchet** (C1, J64) allows exactly this kind of change: a lie a wave seat finds that the tool accepts
  becomes a control with its `expect`, and the tool is fixed — a strengthening, never a relaxation.
  **No frozen counter, no frozen probe check, no threshold and no pin changed**: … are byte-identical
  to the freeze (`node scripts/counter-pins.mjs` → CLEAN)."
- The plan clauses that make the label available: `kumitate-shokunin/.ufo/waves/round-64/plan.md:53`
  ("Wave seats are asked to find cheaper lies (ratchet)") and `:86` ("the same no-retroactive-change
  rule and the same **monotone ratchet** (a forgery found by a seat becomes a control and a fix, never
  a relaxation) apply"); `round-63/plan.md:64` carries the same ratchet clause.

### 2.3 The consolidating rule the sibling lanes already wrote down

`kumitate-shokunin/corpus/knowledge/counter-amendment-discipline.md` is the lane's own admitted
doctrine on this exact question, and it is the rule all five precedents are instances of:

- `:28-31` **C4** — "A control that reads the predicate on unfinished work forces an amendment. …
  and it was found **before any candidate score existed**."
- `:32-34` **C5** — "The amendment is named and **carries its own failing run**."
- `:35-37` **C6** — "**Strictness only, before data.** An amendment may add a clause that makes the
  predicate harder to satisfy; **it may never relax one**, and it lands in the same commit family as
  the candidate, **before the first candidate score**."
- `:38-40` **C7** — "**Every control re-scores under the amended predicate.** A control that was killed
  before the amendment is run again and must still be killed; a control that now passes is an amendment
  defect, not a control win."
- `:66-69` **C14** — "**Nothing changes after the first candidate score.** … a rule rewritten after a
  seat scored is not the claim's rule (the round-42 precedent), whatever it passes afterwards."
- `:70` **C16** — "**The origin case is the lane's own r42 counter amendment.** A kill rule widened
  after build seats had already scored the frozen ids is not the claim's rule."

---

## 3. The common rule, stated once

> **A frozen instrument may be amended only where the amendment leaves the claim's *rule* intact —
> its predicate sentence, its check definitions, its metric, target, population, thresholds and pins.
> A change that moves any of those is a rule change: it voids the claim and must wait a round.
> A change that only strengthens the adversarial surface (new controls, a repaired gate arm, a
> re-encoded expectation carrying the same value) is a **ratchet**, and it is a ratchet *within the
> declared rule* only when the plan declared the ratchet before data **and** the frozen
> counter/probe/threshold/pin bytes stayed identical. An amendment that is not predeclared is a
> **new revision**, and it is admissible only when it lands before any seat has scored, is disclosed
> in a named artifact, and is shown **value-neutral by measurement, not asserted**. The operator
> rules on the class; the round never blocks on the question; an instrument defect found *after*
> scoring is reported as falsified and routed, never repaired.**

Three discriminators fall out of it, and each is what the precedents actually applied:

| discriminator | tabi r22 | revenger r68 | revenger r69 | kumitate r63 | kumitate r64 |
|---|---|---|---|---|---|
| timing vs first score | **after** (W2b seats had scored) | after (wave had scored) | after (wave had scored) | after (wave 1 had scored) | after (wave 1 had scored) |
| rule moved? | no (value identical, nothing narrowed) | no (gap left in place) | no (crash left in place) | no (rule text unchanged) | no (counter/threshold/pin unchanged) |
| class used | disclosed value-neutral revision | named limitation, routed | falsified + routed | **ratchet (plan-declared)** | **ratchet (plan-declared)** |
| red-before re-scored? | measured 12/12 both sides | n/a | crash shown, not repaired | controls 14→75 disclosed | controls 16→50, pins proven byte-identical |

The one thing kumitate had and kengaku round-36 does not have is the plan clause. kumitate's two
"ratchet" verdicts rest on `plan.md:53`/`:86` (and `round-63/plan.md:64`) — a ratchet **declared in
the plan before data**.

---

## 4. Amendment 1 measured against the rule

### 4.1 What actually changed (2 lines, 2 files)

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show acbda2f -- plans/regex_log_probe.py plans/round36_c2_verify.py`:

```
plans/regex_log_probe.py
  @@ -124,7 +124,7 @@ def run_grader(mod_path, regex, mode):
  -            first = (str(e).splitlines() or ["AssertionError"])[0]
  +            first = (str(e).splitlines() or ["AssertionError"])[0].replace(d, "<tmp>")

plans/round36_c2_verify.py
  @@ -38,7 +38,7 @@ ENTRY = "corpus/knowledge/tb2-regex-log-grader.md"
  -PROBE_SHA256 = "34ab5dfd6d1c3fb972cb698a1d44db07a1670ee206521d7c3177a9e0f729561b"
  +PROBE_SHA256 = "d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc"  # Amendment 1 (claims file)
```

The commit also added `corpus/evidence/round36/{regex-log-dry-cases-freeze.txt,
regex-log-probe-first-run.txt, regex-log-probe.txt}` and the `## Amendment 1` section
(`plans/round-36-claims.md:123-139`). No other file was touched.

### 4.2 Timing — pre-scoring, proven three ways

```
$ git -C …/kengaku-shokunin log -1 --format='%h %cI %s' 3241b86
3241b86 2026-10-25T22:02:37-03:00 round-36: freeze claims, counters, probe, spec, ledger rows, controls
$ git -C …/kengaku-shokunin log -1 --format='%h %cI %s' acbda2f
acbda2f 2026-10-25T22:04:21-03:00 round-36: amendment 1 (probe temp-path normalisation), first probe run, receipt
$ git -C …/kengaku-shokunin log -1 --format='%h %cI %s' f9efce3
f9efce3 2026-10-25T22:08:34-03:00 round-36: wave-1 spec and dispatch (40 seats)
$ git merge-base --is-ancestor 3241b86… acbda2f && echo "freeze IS ancestor of amend (exit 0)"
freeze IS ancestor of amend (exit 0)
$ git merge-base --is-ancestor acbda2f… f9efce3 && echo "amend IS ancestor of wave1 dispatch (exit 0)"
amend IS ancestor of wave1 dispatch (exit 0)
$ git ls-tree -r --name-only acbda2f -- .ufo/waves/round-36/ | wc -l   # 9 — the freeze claims/controls only
$ git ls-tree -r --name-only 3241b86 -- .ufo/waves/round-36/ | wc -l  # 9
```

No seat report existed at `acbda2f`; the wave-1 dispatch commit is a descendant of the amendment.
**No seat had scored when Amendment 1 landed**, so §9's trigger ("a rule changed after any seat has
scored is not the claim's rule") is not engaged — the strictest case in the five precedents (tabi
r22) is not this case.

### 4.3 Value-neutrality — measured, not asserted (tabi r22's test)

Measured in a `mktemp` fixture clone per the lane fixture rule (sparse shared clone, `master`,
`rev-parse --show-toplevel` verified before any write, `rm -rf` at the end); scratch outputs in
`.ufo/waves/round-36/build/R36ConnAmendment/`.

```
=== A: freeze-commit probe --dry  vs  amended probe --dry ===
freeze-dry exit=0
amended-dry exit=0
DRY IDENTICAL freeze vs amended
DRY == committed dry-cases-freeze.txt          (corpus/evidence/round36/regex-log-dry-cases-freeze.txt)
=== B: amended probe full run x2, byte-compare ===
run1 exit=0 / run2 exit=0
TWO RUNS BYTE-IDENTICAL
=== C: amended run vs committed receipt ===
RUN == COMMITTED RECEIPT                        (corpus/evidence/round36/regex-log-probe.txt)
=== D: first-run receipt vs amended run ===
21,22c21,22
< case=invalid-regex … assertion='Regex in /tmp/tmp68j2v92s/regex.txt is invalid: …'
< case=regex-file-absent … assertion='Regex file /tmp/tmp7c39pj0f/absent-regex.txt does not exist'
---
> case=invalid-regex … assertion='Regex in <tmp>/regex.txt is invalid: …'
> case=regex-file-absent … assertion='Regex file <tmp>/absent-regex.txt does not exist'
```

The first-run→amended diff is **exactly the two `mkdtemp` paths and nothing else**: all 24
predicted/observed verdicts are identical (`mismatches=0` in both receipts), so the amendment changed
the printed *form* of two assertion texts and the digest that pins them, and no verdict.

### 4.4 The rule did not move

`plans/round36_c2_verify.py`'s docstring (`:4-31`) still states the frozen predicate and W1–W6
verbatim; the kill rule and target in `plans/round-36-claims.md:75-79` are untouched; the diff above
shows only a printed-string normalisation and one digest constant.

### 4.5 Is it a ratchet? **No** — kengaku's plan declares no ratchet

```
$ grep -cn "ratchet" plans/round-36-claims.md
0
```

There is no declared ratchet clause for Amendment 1 to be "within". Compare kumitate, where the
ratchet label was earned by `plan.md:53`/`:86` **and** by leaving the frozen counter/probe/pin bytes
identical (`round-64/controls/CHANGES-AFTER-FREEZE.md:5-7`). Amendment 1 changed the frozen probe's
bytes and moved the counter's `PROBE_SHA256` pin, so it also fails kumitate's "no pin changed" test.
Calling it a ratchet would assert a declaration that does not exist.

### 4.6 Is it a rule change? **No** — the rule moved nowhere

Predicate sentence, checks, metric, target, population, thresholds and all 24 verdicts are identical
(§4.3, §4.4). It is not the tabi r22 case where the pinned *expectation encoding* was re-written
(`errors: []`→`null`) — that changed a pinned input; here the pinned input (the 24 cases, their
regexes, their predictions) is byte-identical.

### 4.7 Therefore: a **new pre-scoring revision**

It satisfies both halves of revenger r69's proposed test (`l0-questions.md:160`): a *mechanical*
repair (two lines, one of them a digest constant) landed *pre-scoring*, with value-neutrality
measured. It is not a ratchet (no declared clause, a pin moved) and not a rule change (nothing in the
rule moved).

---

## 5. Two disclosure gaps the L1 must close before this label stands

### 5.1 The freeze digest block is stale for two rows and the counter's new digest is absent

`plans/round-36-claims.md:98-106` is headed "## Frozen digests (sha256, at freeze)" and still lists:

```
101: 34ab5dfd6d1c3fb972cb698a1d44db07a1670ee206521d7c3177a9e0f729561b  plans/regex_log_probe.py
103: f70e6d3a97bc8a755820cb12ab51f22f9eda684d4c2b40ceb8c92e11d48ad150  plans/round36_c2_verify.py
```

Measured at the tip (`sha256sum`):

```
d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc  plans/regex_log_probe.py
983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120  plans/round36_c2_verify.py
```

Rows 101 and 103 are superseded, and **the amended counter's own digest `983ed65c…` appears nowhere
in the claims file** — the Amendment 1 text (`:134-135`) names only the amended *probe* digest and
says the counter's constant "moves from `34ab5dfd…` to it (one line)". The two unchanged rows
(`round36_c1_verify.py` = `d7c3687c…`, `pkg-spec-r35.json` = `e085b435…`,
`toolathlon-package.md` = `00132ab0…`) still match the block exactly — verified by `sha256sum`.

This is the mirror of kumitate r64's discipline (`CHANGES-AFTER-FREEZE.md:5-7`: unchanged pins proven
byte-identical to the freeze). For a revision the mirror is: **enumerate every changed byte *and*
every unchanged pin, with digests.** Independent corroboration that this gap is already visible:
`.ufo/waves/round-36/build/R36CritC2Counter.md:161-165` and `:205-208`.

### 5.2 The amendment asserts byte-identity but commits no receipt for it; and the two C2 control receipts are not the receipts of the amended pair

`plans/round-36-claims.md:130-133` asserts a `cmp` of the freeze-commit probe's `--dry` against the
amended `--dry`, both equal to `regex-log-dry-cases-freeze.txt`, and that "two amended runs are
byte-equal". **No receipt file for either assertion is committed** — `corpus/evidence/round36/`
contains only `regex-log-dry-cases-freeze.txt`, `regex-log-probe-first-run.txt`,
`regex-log-probe.txt`, `tb2-regex-log/`, `toolathlon-package.md`. My §4.3 measurements confirm both
assertions are true, but they live in my scratch, not in the lane.

C7 of the doctrine (`counter-amendment-discipline.md:38-40`) requires every control to re-score under
the amended predicate. Re-running the freeze control harness at the tip
(`.ufo/waves/round-36/claims/make-controls.sh`, output to a `mktemp` dir):

```
$ diff <tip re-score> .ufo/waves/round-36/claims/control-c2-nothing.txt
6c6
< W5 DEFECT entry absent
---
> W5 DEFECT probe receipt absent
c2-nothing CHANGED
$ diff <tip re-score> .ufo/waves/round-36/claims/control-c2-skip.txt
c2-skip IDENTICAL
```

Both controls are **still red** under the amended pair (`checks=6 defects=4`, `PREDICATE C2 fail`,
exit 1), so C7's substance holds — no control was turned green. But the reason string moved, and the
cause is worth naming precisely: at the freeze commit the receipt file
`corpus/evidence/round36/regex-log-probe.txt` did not exist, so W5 stopped at "probe receipt absent";
at the tip the receipt exists, so W5 advances and stops at "entry absent" (the knowledge entry is not
in the tree during wave 1). The instrument's semantics did not change — the tree did.

Verification that the freeze receipt *is* reproducible at the freeze commit (so the drift is
amendment-time, not a fabrication), done in a fixture clone with the freeze-commit versions of both
amended files restored (`sha256sum` confirmed `34ab5dfd…` / `f70e6d3a…`) and the receipt removed:

```
W1 ok / W2 DEFECT S108 present 0 times / W3 DEFECT entry absent /
W4 DEFECT index row absent or missing S108/S109/S110 /
W5 DEFECT probe receipt absent / W6 ok
checks=6 defects=4 / PREDICATE C2 fail
$ diff <that output> .ufo/waves/round-36/claims/control-c2-nothing.txt
0a1
> # control control-c2-nothing — python3 plans/round36_c2_verify.py --lane .
8a10
> exit=1
```

i.e. the committed freeze receipt is byte-reproducible at the freeze commit modulo the two harness
wrapper lines `make-controls.sh` adds (`# control …` header, `exit=` trailer).

---

## 6. Risks if the L1 words it wrongly

| risk | who already said it | consequence |
|---|---|---|
| calling Amendment 1 a "ratchet within the declared rule" | `grep -c ratchet plans/round-36-claims.md` = 0; kumitate r63 `plan.md:64` / r64 `plan.md:53,:86` | a wave-2 critic can show there is no declared ratchet to be "within", and that a frozen pin moved (`CHANGES-AFTER-FREEZE.md:5-7` test) |
| calling it a "rule change that voids C2" | tabi r22 `round-22/tabi.md:209-212`; revenger r69 `round-69/revenger.md:24` | over-punishes a change that moved no rule and landed pre-scoring; the honest label is `revision` |
| leaving the stale digest rows | `R36CritC2Counter.md:161-165,205-208` | any reader who re-derives the frozen counter from `plans/round-36-claims.md:103` gets `f70e6d3a…` and may read the amendment as an undisclosed instrument change — the exact attack revenger r69 was routed for |
| shipping the claim without a committed byte-identity receipt | `plans/round-36-claims.md:130-133` asserts `cmp`/two-run equality with no receipt file | the amendment's own strongest evidence is unreceipted; tabi r22's standard is "value neutrality is **measured**, not asserted" (`round-22/tabi.md:39`) |
| citing the wave-1 control receipts as the amended pair's red-before | §5.2 above | the receipts are the freeze pair's; re-scored, both are still red but the W5 reason differs |

A fourth, smaller point: after normalisation the receipt no longer shows the grader's literal
assertion text (the real `mkdtemp` path is not recoverable from it). That is a disclosed cost of the
repair, not a defect — no entry row, quote or negative-space statement depends on it — but it should
be stated rather than left implicit.

---

## 7. Recommended wording for the kengaku report (L1's §Work performed / amendment paragraph)

> **Amendment 1 is a new pre-scoring revision of the frozen C2 instrument pair — not a ratchet and
> not a rule change.** It landed at `acbda2f` (22:04:21) after the freeze `3241b86c` (22:02:37) and
> before the wave-1 dispatch `f9efce3` (22:08:34), with no seat report in the tree at `acbda2f`, so
> §9's trigger ("a rule changed after any seat has scored") is not engaged. The claim's rule is
> untouched: the predicate sentence, checks W1–W6, the kill rule, the target and all 24 case verdicts
> are unchanged (`mismatches=0` before and after). Value-neutrality is measured, not asserted: the
> freeze-commit probe's `--dry` output and the amended probe's `--dry` output are byte-identical and
> both equal `corpus/evidence/round36/regex-log-dry-cases-freeze.txt`; two amended full runs are
> byte-identical; the amended run equals the committed receipt byte-for-byte; and the first-run →
> amended diff is exactly the two `mkdtemp` paths in the `invalid-regex` and `regex-file-absent`
> assertion texts. It is **not** a ratchet: round 36's claims file declares no ratchet clause
> (`grep -c ratchet plans/round-36-claims.md` = 0, against kumitate's plan-declared ratchet at
> `.ufo/waves/round-64/plan.md:53,:86`), and the amendment moved a frozen pin, which is the test
> kumitate's own ratchet verdicts had to pass (`round-64/controls/CHANGES-AFTER-FREEZE.md:5-7`).
> It is **not** a rule change: nothing in the rule moved. It is the shape revenger's round-69
> question asked about — a mechanical, pre-scoring repair landing as a new revision — with the
> fresh red-before still owed: both C2 controls re-score red under the amended pair
> (`checks=6 defects=4`, `PREDICATE C2 fail`, exit 1), but the committed freeze receipts are the
> freeze pair's, and the byte-identity assertions above are not yet receipted in the lane. The
> operator ruling requested by `revenger | round-69` (`.ufo/l0-questions.md:160`) is still open and
> this round does not block on it; the verdict is reported either way.

Two additions the L1 should make in the same paragraph, so the label is self-supporting:

1. **Digest disclosure.** State that `plans/regex_log_probe.py` moves `34ab5dfd…` → `d58194c8…` and
   `plans/round36_c2_verify.py` moves `f70e6d3a…` → `983ed65c…`, and that rows 101 and 103 of
   `plans/round-36-claims.md:98-106` are superseded by Amendment 1 (the three unchanged rows still
   match). Disclose the counter's new digest — the Amendment 1 text currently names only the probe's.
2. **Receipt disclosure.** Commit the byte-identity receipts the paragraph relies on, and re-land the
   two C2 control receipts as the amended pair's (or state plainly that the committed ones are the
   freeze pair's and cite the re-score output).

---

## 8. Verification performed by this seat (all commands reproducible)

Every command below was run read-only against the lane, or in a `mktemp` fixture clone built per the
lane fixture rule (`git clone -q --no-checkout --shared`, `sparse-checkout set --no-cone`,
`checkout -q master`, `rev-parse --show-toplevel` verified before any write, `rm -rf "$D"` at the
end). No lane file was written; no git/jj mutating command was run in the lane.

| # | command | result |
|---|---|---|
| V1 | `git -C … log -1 --format='%h %cI %s'` on `3241b86`, `acbda2f`, `f9efce3` | 22:02:37 → 22:04:21 → 22:08:34 |
| V2 | `git merge-base --is-ancestor` (freeze→amend, amend→dispatch) | both exit 0 |
| V3 | `git ls-tree -r --name-only acbda2f -- .ufo/waves/round-36/ \| wc -l` | 9 (freeze claims/controls only; no seat report) |
| V4 | `git show acbda2f -- plans/regex_log_probe.py plans/round36_c2_verify.py` | 2 changed lines (the `.replace(d, "<tmp>")` and the `PROBE_SHA256` constant) |
| V5 | `sha256sum` of the 5 rows of `plans/round-36-claims.md:98-106` vs the tip files | rows 101 and 103 stale; rows 102, 104, 105 match |
| V6 | `grep -cn "ratchet" plans/round-36-claims.md` | 0 |
| V7 | freeze-commit probe `--dry` vs amended probe `--dry` vs `regex-log-dry-cases-freeze.txt` | all three byte-identical |
| V8 | two amended full probe runs | byte-identical, both exit 0 |
| V9 | amended run vs committed `regex-log-probe.txt` | byte-identical |
| V10 | `diff` first-run receipt vs amended run | exactly 2 lines (the `mkdtemp` paths); all 24 verdicts identical |
| V11 | `bash .ufo/waves/round-36/claims/make-controls.sh <lane> <mktemp>` at the tip, then `diff` vs the two committed C2 receipts | `control-c2-nothing` W5 reason moved (`probe receipt absent` → `entry absent`), still `checks=6 defects=4` exit 1; `control-c2-skip` byte-identical |
| V12 | same harness on a fixture clone with the freeze-commit versions of both amended files restored | the committed freeze receipt is reproduced byte-for-byte modulo the harness's `# control …` / `exit=` wrapper lines |

Scratch artifacts (mine, under the permitted build dir):
`.ufo/waves/round-36/build/R36ConnAmendment/{dry-freeze.txt,dry-amended.txt,run1.txt,run2.txt,freeze-tree-c2-nothing.txt}`.

**Tool installs:** none. No pacman, uv, npx or cargo transaction; the host-wide pacman pause was
respected. Only python3 / git / coreutils were used.

---

VERDICT: amendment-precedents-5-recommend-revision
