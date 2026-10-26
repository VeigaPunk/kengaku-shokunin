# F37XMutP4 — extra P4 (quote-verbatim) mutants beyond M09–M12

Seat: critic, wave 2 (falsify), kengaku round 37.
Targets: `plans/battery37/p4.py` and clause `c_quote_verbatim` (P4) of `plans/pkg_gate.py`.
Harness: `.ufo/waves/round-37/falsify/F37XMutP4/harness.py` (reuses the counter's own machinery by
importing `plans/round37_c1_verify.py`: `load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`,
`run_gate`, `MUTANTS`), counterexample probe `.ufo/waves/round-37/falsify/F37XMutP4/probe.py`.
Receipts: `receipt.json`, `probe.json`, `counter-clone-full.txt`, `SHA256SUMS` (same dir).

## Setup / frozen state reproduced

```
$ S=/fast/scratch/hyaku/kengaku-r37/F37XMutP4
$ git clone -q --no-local /home/…/kengaku-shokunin "$S/fx/lane"
$ git -C "$S/fx/lane" rev-parse HEAD
357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ git -C "$S/fx/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r37/F37XMutP4/fx/lane
$ sha256sum "$S/fx/lane/plans/pkg_gate.py"
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41   (= counter GATE_SHA256)
```

Counter run on my clone (not the lane), full battery, before mutating anything
(`cd "$S/fx/lane"; python3 plans/round37_c1_verify.py --lane . --work "$S/c1work"`, 82.4 s):

```
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANT M09 P4 killed by=p23-p3-heading-renamed -- no parsed quote
MUTANT M10 P4 killed by=p4-capture-unreadable -- quote cites an unreadable capture
MUTANT M11 P4 killed by=p4-line-outside -- quote line range outside the capture
MUTANT M12 P4 killed by=p4-one-char-off -- quote not verbatim on its cited line
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

So the battery under attack is the frozen one, and my harness builds the same 64-fixture world
(`harness.py` prints `FIXTURES 64`, `NULL null_detected=0`). No lane file was written; every git call
named `-C "$S/fx/lane"`; scratch removed at the end.

## New mutants (non-frozen, same clause), each anchored exactly once

`for each: gate_src.count(old) == 1` (harness prints `anchor_count`), `py_compile` clean, run over all 64
fixtures; killed iff some fixture's `(exit code, DEFECT id set)` differs from the reference.

| id | kind | `old -> new` | status | killed by |
|---|---|---|---|---|
| X1 | off-by-one threshold (`>`→`>=`) | `elif q.start > q.end or q.end > len(lines):` → `elif q.start >= q.end or q.end > len(lines):` | killed, 42/64 fixtures differ | `r36-P0` (accept → `rc1{P4}`) + 41 |
| X2 | check applied to the first quote only | `    for q in p.quotes:` → `    for q in p.quotes[:1]:` | **SURVIVED** 0/64 | — |
| X3 | branch reordered so the range check shadows the unreadable branch | `if lines is None: bad.append(unreadable)` / `elif q.start > q.end or q.end > len(lines):` → `if q.start > q.end or q.end > len(lines):` | **SURVIVED** 0/64 (equivalent, see F4) | — |
| X4 | check loosened: whole capture instead of the cited lines | `elif q.text not in "\n".join(lines[q.start - 1:q.end]):` → `elif q.text not in "\n".join(lines):` | **SURVIVED** 0/64 | — |
| X5 | loosened to case-insensitive (extra) | same anchor → `elif q.text.lower() not in "\n".join(lines[q.start - 1:q.end]).lower():` | **SURVIVED** 0/64 | — |
| X6 | off-by-one (`>`→ lax `+1`) (extra) | `q.end > len(lines):` → `q.end > len(lines) + 1:` | **SURVIVED** 0/64 | — |

Harness output: `NEWMUTANTS killed=1 survived=5 invalid=0`.

## F1 (strongest) — the battery is blind to every quote after the first

X2 survived all 64 fixtures. Cause: every P4-defect injection in `plans/battery37/` targets the first
data row — `p4.py` routes all three defect builders through `_first_row` (lines 57, 66, 75), and `p5.py`
stops at the first parsable row (`for i, row in enumerate(rows): … return new`, line 184). `p23.py` does
touch rows 4/6/14 but for P3 shape defects, not P4.

Counterexample fixture (mine, scratch only), second data row citing `9999`:

```
PROBE probe-second-row-outside X2 ref=rc1/{P4} mut=rc0/{} DIFFERS
```

The gate checks 22 quotes (`P4 DEFECT checked=22 bad=1`); the battery defaces quote 1 in all four p4
fixtures. A weakening that skips quotes 2..22 is undemonstrated.

## F2 — verbatim-on-the-cited-lines is not demonstrated, only verbatim-somewhere

X4 (search the whole capture) survived: no fixture has a quote that is verbatim elsewhere in its capture
but not on its cited lines. Minimal killer fixture: cite lines `1-2` of `test_outputs.py` for the row whose
text lives on line 13 —

```
PROBE probe-first-row-off-line X4 ref=rc1/{P4} mut=rc0/{} DIFFERS
```

X5 (case-only) and X6 (one line past the end) likewise survive and have 6-line killers:

```
PROBE probe-first-row-case-only   X5 ref=rc1/{P4} mut=rc0/{} DIFFERS
PROBE probe-first-row-one-past-end X6 ref=rc1/{P4} mut=rc0/{} DIFFERS
```

`p4-one-char-off` cannot see X5 (it substitutes one alphanumeric character, so a case-insensitive compare
still mismatches) and `p4-line-outside` cannot see X6 (9999 is past `len+1` too).

## F3 — X1 is killed, but by no P4 fixture

X1 (`start >= end`, i.e. single-line quotes are "outside the capture") rejects the genuine package: all 22
genuine rows are single-line (`start == end`, e.g. `test_outputs.py:13..:23`). It is killed because
`r36-P0` (the accept fixture) flips `rc0{}` → `rc1{P4}`; **`p4-*` appear in none of the 42 differing
fixtures** — every p4 fixture already prints P4 DEFECT, so a P4 mutant that keeps it DEFECT is invisible to
them. The clause's range semantics are therefore certified by the genuine-accept fixture, not by the P4
module. (Also: the kill is broad — 42/64 — a hint that X1 is a *stricter* mutant, not a silenced check.)

## F4 — X3 is an equivalent mutant at clause granularity, not a battery gap

Reordering the `lines is None` branch behind the range check makes the clause raise
`TypeError: object of type 'NoneType' has no len()` on `p4-capture-unreadable`. `run_checks` catches it and
prints P4 DEFECT, so the observable `(rc=1, {P4,P5})` is identical:

```
ref    : P4 DEFECT checked=22 bad=1 first=no-such-capture-37.py: unreadable capture
mutant : P4 DEFECT clause error TypeError: object of type 'NoneType' has no len()
```

No fixture can distinguish this: an unreadable capture always makes the reference P4 fail as well, and the
gate's documented contract is accept/reject per clause (it maps a clause crash onto DEFECT by design). This
is a limit of the counter's observable (clause id set, not the note), not a defect the battery could fix
without changing the frozen predicate. Note M10 proves the branch is *effective* (removing it flips P4 to
ok on that fixture); X3 only regresses the reason.

## F5 — p4.py isolation audit: 2 of 4 fixtures isolate one defect, not 4 of 4

Killing frozen mutants per p4 fixture (all 55 mutants x the 4 p4 fixtures, `receipt.json`):

| fixture | declared defects | observed (reference) | frozen mutants that change it | isolates one defect? |
|---|---|---|---|---|
| `p4-no-quote-row` | P3,P4 | `rc1{P3,P4}` | M09 only (P4) | **no**: two clauses declared, one demonstrated; no P3 mutant touches it |
| `p4-capture-unreadable` | P4,P5 | `rc1{P4,P5}` | M10 (P4), M18 (P5) | **no**: two clauses really move |
| `p4-line-outside` | P4 | `rc1{P4}` | M11 (P4) | yes |
| `p4-one-char-off` | P4 | `rc1{P4}` | M12 (P4) | yes |

The module docstring already concedes the P3+P4 coupling for `p4-no-quote-row`, but the header line
"single-defect fixtures" and the declaration `["P3","P4"]` overstate it: the P3 member is *unfalsified* on
that fixture, because silencing any P3 branch leaves `rc1{P3,P4}` unchanged (M04–M08 absent from the
killing set). Nothing is over-declared on `p4-capture-unreadable` (both members move via M10/M18), so its
two-clause declaration is honest. Unrelated-clause contamination is absent: no non-P4/P5 mutant kills any
p4 fixture.

Reference observables match the declarations exactly (counter: `wrong=0`, and my run prints
`p4-no-quote-row=rc1/{P3,P4} p4-capture-unreadable=rc1/{P4,P5} p4-line-outside=rc1/{P4}
p4-one-char-off=rc1/{P4}`), so the declared sets are not wrong — only coarser than "one defect".

## Impacted axes

- **C1 calibration (frozen claim stands)**: the predicate still prints 55/55 on the tip; nothing here
  contradicts it. The findings are *beyond the frozen mutant set*, i.e. limits of the advertised clause
  coverage, not a landing regression.
- **P4 coverage claim** (gate docstring "a quote not verbatim on its cited line … are defects";
  `QUALITY.md` Q24 / SCORECARD `package-gate` row): demonstrated only for quote #1, and the "cited line"
  half of the verbatim predicate is not demonstrated at all (F1, F2).
- **battery37/p4.py docstring accuracy**: "single-defect fixtures" is false for 2 of 4 entries (F5).

## Smallest safe corrections (for wave 3 / owner; not applied by me)

1. Add to `plans/battery37/p4.py`, reusing `_apply`/`rewrite_quotes`, each ~6 lines:
   - `p4-second-quote-outside` — inject the out-of-range line into `rows[1]` instead of `_first_row` →
     kills X2 (declared `["P4"]`, verified `rc1{P4}` on my probe).
   - `p4-first-quote-off-line` — cite `1-2` for a row whose text lives on a later line → kills X4.
   - `p4-first-quote-case-only` — case-only text change → kills X5.
   - `p4-first-quote-one-past-end` — `end = len(capture)+1` → kills X6.
   Each is P4-only on my probe (`ref=rc1/{P4}`, mutant `rc0/{}`), so the declarations stay exact.
2. Fix the p4.py header to say "fixtures that declare the exact clause set the unmodified gate prints",
   and either drop P3 from `p4-no-quote-row`'s declaration or add a P3-distinguishing fixture; currently
   the P3 member there is untested.
3. Leave X3 alone in the gate; if the owner wants branch-level fidelity, that is a counter-contract change
   (observable = clause ids only, by design), not a battery fix.

## Scratch

`/fast/scratch/hyaku/kengaku-r37/F37XMutP4` (clone, fixture builds, gate copies) — removed before
finishing; receipts copied into this directory first (`SHA256SUMS`). No tool installs, no upgrades, no
mutating git command in the lane.

VERDICT: extra-mutants-p4-killed-1/4
