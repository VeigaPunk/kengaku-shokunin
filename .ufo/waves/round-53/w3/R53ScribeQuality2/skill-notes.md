# SKILL.md lines to add — round 53 (seat `R53ScribeQuality2`)

Draft text only; the L1 integrates. Every path and number below is committed at lane HEAD
`9ead4476bf55b1ea6490d0204b668195db4a4d1d`; every command is one that exists in the tree and was
run at that tip. Nothing here invents a command.

Two additions are proposed:

* **(1)** a new section `## Presence-only grader triage` with a short decision table — where to put
  it and what it says;
* **(2)** one new entry in the existing error-pattern list (`## Benchmark anti-patterns`,
  `SKILL.md:60`, items 1–19) covering the three error classes round 53 named.

---

## (1) `## Presence-only grader triage` — proposed section

**Placement.** After `## Constant-compare TB2 grader — round 44` (the file ends at `SKILL.md:1370`)
and before `## Cited local sources` would break the file's order; the file's per-round sections run
`## TB2 regex-log grader — round 36` … `## Constant-compare TB2 grader — round 44` in
`SKILL.md:858-1370`. The new section is a *round-53* section about an instrument rather than one
grader, so the least surprising placement is **at the end of the file, after the round-44 section**
(`SKILL.md:1370`), matching how each round's section was appended in the rounds 36–44 series. The
alternative the L1 may prefer is to place it next to `## Gate/probe registry` (`SKILL.md:560`),
because the section's subject is the registry row `round53-c1` (`SKILL.md:639`). Both are
append-only insertions into `SKILL.md`; neither edits an existing line.

**Proposed text (verbatim, ready to append):**

```markdown
## Presence-only grader triage — round 53

A Terminal-Bench 2.0 grader's test is **presence-only** when it passes in every state in which the
filesystem paths it names merely exist: creating the named files and directories (`touch`, `mkdir`,
an empty file) satisfies every assertion the test can reach. The definition is frozen in
`.ufo/waves/round-53/p1-spec.md`; the classifier that implements it is
`plans/round53_c1_classify.py` (`classify_source(src) -> {test key: 'P1' | 'P0'}`, standard library
only, no network, no filesystem access), and the counter that grades the triage against blind labels
is `plans/round53_c1_triage.py` (registry row `round53-c1`, `SKILL.md:639`).

### Decision table — what a grader's assertion reads, and what that means for the triage

| what the reachable assertion reads | class | what it means | cite |
|---|---|---|---|
| only the existence or type of a path (`.exists()`, `.is_file()`, `os.path.exists`, a name in a directory listing) | `P1` | the test passes on an empty artefact; it cannot distinguish "present" from "correct" | `plans/round53_c1_classify.py` docstring, rule 3; `.ufo/waves/round-53/p1-spec.md` Y.2 |
| file content, a size, a count, a command's output, a return value | `P0` | the assertion constrains something beyond presence | `plans/round53_c1_classify.py` docstring, rules 2–3; `.ufo/waves/round-53/p1-spec.md` Y.3 |
| no assertion is reachable at all | `P0` | the test asserts nothing | `.ufo/waves/round-53/p1-spec.md` N |
| the verdict depends on code that is not in the captured files | `U`, mapped to `P0` | the captured bytes cannot decide it | `.ufo/waves/round-53/p1-spec.md` U |

Reach follows same-file helpers, `self.` methods, requested same-file fixtures and referenced
constants transitively; a violation anywhere in the reachable code makes the test `P0`.

### Decision table — what to read in a triage result before citing it

| the result says | what it does *not* say | what to check instead | cite |
|---|---|---|---|
| a task's grader holds a `P1` test | that the task is graded by presence alone | the other tests in the same grader — round 52 found no task graded by presence alone, so a `P1` test is a weak test inside a stronger grader | `corpus/knowledge/tb2-grader-vacuity-triage.md` §Summary |
| the oracle agrees with the classifier | that the classifier is right | the oracle is eight blind label seats over pinned shards; agreement is a result to attack, not a verdict | `.ufo/waves/round-53/claims/c1-after-oracle.txt`; `plans/round53-c1-triage.py` `leg_freeze` |
| a task is "never-read" | that no earlier round examined it | round 52's machine receipt carries per-test classes for the same tasks; "never-read" means "not named in the base-tip lane texts and not confirmed in round 52" | `plans/round-53-claims.md` §Amendments A1 "Not changed"; `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` |
| the counter prints `PREDICATE R53-C1 pass` | that the triage instrument is sound | the counter's own selftest is the falsifier: `python3 plans/round53_c1_triage.py --selftest` prints `SELFTEST cases=47 failures=0` and each case is a forged-but-complete world | `.ufo/waves/round-53/claims/c1-selftest.txt` |

Limits: a presence-only test inside a larger grader is a *presence-only test*, never a whole-grader
weakness; the classifier is a static reading of the captured bytes at pin `2fd12b88` and says nothing
about a task's validity, difficulty or gameability. Measured at this tip: 305 tests over 88 tasks,
`P1=52 P0=253`, `P1` in 41 of 88 tasks (`.ufo/waves/round-53/w1/C1ExecClassifier/fix-round-receipt.txt`).
```

**Commands used above (all exist and were run at `9ead4476`):**

```
python3 plans/round53_c1_triage.py --lane .          # PINS/FREEZE/ORACLE/ORACLE-CONTROL/CONFIRM/PRIOR-ART; exit 1
python3 plans/round53_c1_triage.py --selftest         # SELFTEST cases=47 failures=0
python3 plans/round53_c1_triage.py --lane . --candidates   # CANDIDATES never_read_tasks=28
python3 plans/round53_c1_classify.py --selftest       # cases=83 failures=0
python3 plans/round53_c1_classify.py <file>... [--why]  # per-file P1/P0 histogram + TOTAL P1=.. P0=..
```

The last two are the classifier's own CLI (`plans/round53_c1_classify.py:1649-1655`), not a registry
row; they are quoted here because the section's reader needs a way to check one grader by hand.

---

## (2) One new entry in the error-pattern list

**Placement.** `SKILL.md:60` `## Benchmark anti-patterns`, items 1–19 (`SKILL.md:62-177`, item 19
ends at `SKILL.md:177`, immediately before `## Research-note structure` at `SKILL.md:179`). The new
entry is **item 20**, appended after item 19 — the list is append-only in practice (item 19 was added
at commit `0c16a79e`, round 14; no earlier item was renumbered).

The list's items are written as a bolded claim, the concrete failure, and a `(`cite`)` in parentheses.
The proposed item 20 keeps that shape and covers the three error classes round 53 named —
**classifier-vs-oracle**, **forged-complete controls**, **ledger tip-state** — because all three are
the same mistake at different surfaces: *the instrument is trusted because it agrees with something
the lane wrote*. (The L1 may prefer three separate items 20/21/22; the text below is written so each
of the three clauses can be lifted into its own item.)

**Proposed text (verbatim, to append as item 20):**

```markdown
20. **An instrument that is only as independent as the things it reads.** Round 53's two counters
    were frozen before any seat scored and then attacked before the data landed; every attack
    landed. The C1 counter printed `PREDICATE R53-C1 pass` on a fixture whose "classifier" was an
    all-`P1` stand-in, whose labels were that stand-in's own output, and whose confirmations and
    prior art were forged
    (`.ufo/waves/round-53/w1/C1CritCounterReach/results/composite-fixture.txt`). The C2 counter
    printed `PREDICATE R53-C2 pass` on a ledger that declared every row green, on zero registry
    rows, and on a renamed heading (`.ufo/waves/round-53/w1/C2CritLedgerReach/out/SUMMARY.txt`).
    Three recurring shapes: **(classifier-vs-oracle)** a label set copied from the classifier agrees
    with it perfectly and measures nothing — independence of labellers is a protocol property
    recorded in the seat reports, not something the counter can prove
    (`plans/round-53-claims.md` §Amendments A1, "Not changed"); **(forged-complete controls)** a
    control that only fails on a blank proves the counter rejects nothing — the control must be
    complete and well-formed but wrong, and it must fail *on the leg it names*
    (`.ufo/waves/round-53/claims/c1-selftest.txt`, `c2-selftest.txt`: `cases=47` and `cases=52`,
    every forged case red); **(ledger tip-state)** a registry cell states what its instrument
    returned *at that instrument's landing tree*, so the tip-state is a separate, executed fact per
    row, declared in `plans/round53-tipstate.json` and re-executed by
    `plans/round53_c2_tipstate.py` — a green ledger row can still be a gate that cannot fail, and
    the counter compares declaration against observation, not the strength of the instrument
    (`plans/round-53-claims.md` §Amendments A1, "Not changed";
    `.ufo/waves/round-53/claims/c2-run1.txt`: `mismatched=18`). Freeze the control before the data
    and re-run it after every amendment to the counter.
```

**Cites used above** (all committed at `9ead4476`):

| cite | what it is |
|---|---|
| `.ufo/waves/round-53/w1/C1CritCounterReach/results/composite-fixture.txt` | the all-`P1` + copied-labels + forged-evidence fixture that printed `PREDICATE R53-C1 pass` |
| `.ufo/waves/round-53/w1/C2CritLedgerReach/out/SUMMARY.txt` | the per-route one-line summary of the C2 attacks (`LANDED … pred=pass` lines) |
| `plans/round-53-claims.md` §Amendments A1 | the dated amendment that closed the routes, including its explicit "Not changed" note on labeller independence and on a gate that cannot fail |
| `.ufo/waves/round-53/claims/c1-selftest.txt` | `SELFTEST cases=47 failures=0` — the C1 forged-complete battery |
| `.ufo/waves/round-53/claims/c2-selftest.txt` | `SELFTEST cases=52 failures=0` — the C2 forged-complete battery |
| `.ufo/waves/round-53/claims/c2-run1.txt` | `RUN executed=77 timeout=0 mismatched=18 evidence_missing=1`, `PREDICATE R53-C2 fail` |

**Note for the L1.** The proposed text quotes no more than 25 words from any captured source and
contains no credential-shaped string; `SECRET`, `TOKEN` and the like appear nowhere in it. The two
registry rows the section's readers need (`round53-c1`, `round53-c2`) are already in
`SKILL.md:639-640`, so no registry row is added by this note — only prose.
