# R35CritC2 — calibration critique of C2 (persistent routed-defect ledger)

Seat: `R35CritC2` (critic). Scope: attack C2 as a calibration claim per the frozen
`plans/round-35-claims.md` C2 section. All evidence was produced read-only against the lane
(`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `11d64530179b78e33ba6074fc77d63d36ee7ac31`)
or inside throwaway `/tmp/k35-exp-*` fixture clones (sparse, `--shared`, verified toplevel,
deleted after each run). Nothing in the lane was written; no git state was mutated.

## 1. Do-nothing and flip-only controls cannot reach the target

Both are already scored at freeze and printed:

- `controls/control-c2-nothing.txt`: `rows=5 closed=0 observed_pass=0 mismatches=0` → `PREDICATE C2 fail`, exit=1.
- `controls/control-c2-flip.txt`: `rows=5 closed=5 observed_pass=1 mismatches=4` → `PREDICATE C2 fail`, exit=1.

Neither prints the frozen success line, so neither reaches the target. The flip control's single
green row is D1 (`agree=yes untracked=0`) purely because a fresh clone has no untracked files —
this is itself the D1 vacuity finding (§3).

## 2. D4 can be passed by a correction line that says the opposite of the truth

The check `r34_d4` requires exactly one SCORECARD line starting `- **D4 correction (round 34 C2):**`
containing the four substrings `R34C2CounterDraft.md:8`, `cases=10 failed=0`,
`R34MutC2Harness.md:12`, `SELFTEST green failed`. It is pure token co-occurrence: direction is
never asserted. Counterexample (EXP1, isolated fixture): appended

```
- **D4 correction (round 34 C2):** the counter draft's selftest was red (SELFTEST green failed at R34C2CounterDraft.md:8, cases=10 failed=0 at R34MutC2Harness.md:12)
```

and flipped row `R34-D4` to `closed`. The checker reports:

```
R34-D4 status=closed observed=pass agree=yes correction_lines=1
```

The line contains every required token but asserts the exact opposite of the true record (the
draft selftest is green at `R34C2CounterDraft.md:8`; the harness selftest is red at
`R34MutC2Harness.md:12` — verified in HEAD bytes: draft line 8 `SELFTEST cases=10 failed=0`,
harness lines 12–13 `SELFTEST green failed (1)`). So a *labelled-correctly, false* self-assessment
certifies the closure. The D4 defect (misattribution) would remain textually unfixed while the
check passes.

## 3. D5 can be passed by an erratum that says the quote is absent

`r34_d5` requires one line starting `Erratum (round 35):` containing `nec-s091-reopen.html` and
the substring `present` (plus an S091 row in `round-35.md` §Mistakes). `"present"` matches inside
`"not present"`. Counterexample (EXP2): appended

```
Erratum (round 35): the staged S091 quote is not present in nec-s091-reopen.html
```

plus a §Mistakes S091 row; flipped `R34-D5` to `closed`. Output:

```
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
```

The erratum states the refusal reason was correct (quote absent) — the negation of the defect
closure — and the check certifies it. The observation itself is genuine (`quote_present_at_HEAD=True`
per tag-strip + whitespace normalization of HEAD capture bytes), so the *honest* line also passes
(EXP4: `is present` → pass); the hole is that the false line passes too. Secondary gap: the
observation source `nec-s091-reopen.html` is writable lane content with no pin — injecting the
quote into the capture would also manufacture a pass.

## 4. D1 is not re-derivable from committed bytes; it is vacuous in any clean checkout

`r34_d1` runs `git ls-files --others --exclude-standard` (working tree), not repo bytes — directly
contradicting the checker docstring's claim that "each row's check compares the lane's self-assessment
with an observation computed from repo bytes". Evidence:

- EXP3: in a pristine fixture clone, flipping only D1 to `closed` yields `R34-D1 status=closed observed=pass agree=yes untracked=0` — no mismatch, zero repair.
- This matches the freeze flip control (`untracked=0`, agree=yes) while the live lane at freeze held `untracked=1425` (control-c2-nothing.txt) and holds 657 today.

So D1 certifies only "the workspace this checker ran in has no untracked files under three paths +
the round-34 wave tree". It cannot certify the defect class from the repository, and its "re-runs
at every tip" property is not meaningful for it. The check is only non-vacuous if the landing run
executes in the live lane workspace *and* the repair truly cleans it. Scope note: at freeze the D1
scope did not cover the new round-35 build art (657 untracked today), so a future recurrence of the
same class under the current round would be invisible to the persisted ledger.

## 5. D2: tip-state closure does not verify the routed prescription

`r34_d2` counts committed paths under the three mirror roots at `refs/heads/master` (109413 at
HEAD, `committed_mirror_paths=109413`). Deleting the roots at the tip passes it, but:

- History keeps all 109413 paths / 1692.9 MiB logical (`git ls-tree -r -l HEAD` sum), so "recursive self-mirrors" remain in the object store. Unique-object cost is small (`git count-objects -vH`: count 6909, size-pack 1.14 MiB) because the mirrors deduplicate and compress, but the 109k-path tree remains an operational drag.
- The routed defect's own wording ("mutants must run in a temp clone outside the repo … record a lesson and a guard") has a process half; the check has no clause for the guard or the lesson. Deleting at tip alone is therefore accepted while the "commit only receipts" rule stays unverified.

So the answer to "deleting mirrors from the tip honestly answers the defect?" is: it closes the
present-state symptom, but the check cannot tell a tip-only deletion from a repair that also records
the lesson/guard; the anti-recurrence half is unmeasured.

## 6. D3 is the soundest check; one hardening available

`r34_d3` is byte-grounded (`hashlib.sha256` per listed file, requires both evaluator entries) and a
text-only edit cannot pass it. Optional hardening: compare the evaluator digests against the frozen
external hashes (`44a05a24…`, `9ede4664…`) rather than self-consistency, protecting against
rewriting the capture files to match a wrong manifest.

## 7. Smallest safe corrections (all preserve the frozen predicate: same printed line, same exit semantics)

1. **D4**: replace bare co-occurrence with ordered clause regexes, e.g. require
   `R34C2CounterDraft\.md:8` … (same line) `cases=10 failed=0` **and**
   `R34MutC2Harness\.md:12` … `SELFTEST green failed` (each citation immediately before its own
   token). The false line fails both orders; the honest line passes.
2. **D5**: require token `is present` (or reject `not present`) in the erratum line, and pin the
   capture's authenticity — compare the tip blob sha256 of `nec-s091-reopen.html` against the
   committed `quarantine-SHA256SUMS` entry (or a frozen constant) before trusting the observation.
3. **D1**: keep the row, but (a) run the landing verification (`--lane .`) in the live lane
   workspace so D1 is non-vacuous, and (b) broaden the untracked roots to the current wave tree +
   `plans/roundNN_*` leftovers generically so the class is caught next round too; document that D1
   is a workspace check, not a repo-bytes check.
4. **D2**: inside `r34_d2`, require in addition that a round-35 lesson line records the temp-clone
   rule (e.g. contains `temp clone`), so the prescription half is verified alongside the tip count.

## 8. Impacted axes

- **calibration** (primary): false-positive closures demonstrated for D4 and D5; D1 not verifiable from committed bytes.
- **operability**: honest repair is fully scriptable today (observations for D1/D4/D5 already hold at HEAD; D2/D3 are plain deletes/manifest appends); the counterexamples only show the checks cannot distinguish truthful from false text.
- **depth**: counter semantics are token-level, not directional; no claim on the repair's honesty is warranted (the in-flight live edits — SCORECARD D4 line, round-34 erratum, round-35.md, tb2-eval manifest — are consistent with the honest path).

**VERDICT: c2-critic-1-findings**
