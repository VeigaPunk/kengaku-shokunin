# F37XMutP910 — critic, wave 2 (falsify), kengaku round 37

Target: `plans/battery37/p910.py` (clause P9/P10 fixtures for frozen M39/M41/M42/M43) and, through it,
the C1 calibration claim of `plans/round-37-claims.md`.
Lane clone: `/fast/scratch/hyaku/kengaku-r37/F37XMutP910/fx/lane` at `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`;
`sha256sum plans/pkg_gate.py` = `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (freeze digest).
Every number below comes from a run in that clone; no lane file was written.

## Method

1. Reused the counter as a module (`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`, `run_gate`),
   built the 64 fixtures once and measured the reference plus each non-frozen gate variant against the
   same fixture directories — the counter's own kill semantics (`(exit code, DEFECT set)` differs on any
   fixture). Harness: `F37XMutP910/harness.py`, output `F37XMutP910/harness.txt`.
2. Isolation matrix for the four p910 fixtures plus one out-of-battery positive control:
   `F37XMutP910/isolation_matrix.py`, output `isolation_matrix.txt`.
3. Feasibility of the corrections proposed below: `F37XMutP910/correction_check.py`,
   output `correction_check.txt`.
4. Fixture-docstring claims checked against the gate text (`c_receipt` L117-121, `c_instruments` L112-115,
   `spec.frozen_instruments`, `spec.probe_cmd`) and by a counterfactual on the staged `.gitignore`
   (`F37XMutP910/positive_control.py`, output `positive_control.txt`).

Reference health at the tip (harness run): `BATTERY fixtures=64 wrong=0` — every fixture, p910 included,
prints exactly its declared clause set. Baseline kill map for the frozen neighbours, from
`python3 plans/round37_c1_verify.py --lane . --only M39,M40,M41,M42,M43`: `M39 → p910-not-a-git-repo`,
`M40 → r36-P6`, `M41 → p910-receipt-deleted`, `M42 → p910-probe-exits-1`, `M43 → p910-receipt-one-byte`,
`BATTERY fixtures=64 wrong=0 renamed_disagree=0`.

## Finding 1 — four new non-frozen P9/P10 mutants, all killed (4/4)

Each is one exact `old -> new` replacement that occurs exactly once in the frozen gate; each compiles;
each is distinct from M39-M43 in mechanism, not just in bytes.

| id | clause | weakening | result | killing fixture(s) |
|---|---|---|---|---|
| X1 | P9 | `return not left, ...` → `return len(left) < 2, ...` — one untracked file counts as clean (off-by-one threshold) | killed | `r36-P6`, `r36-P7` |
| X2 | P9 | `if r.returncode != 0:` → `if r.returncode not in (0, 128):` with its `root is not a readable git worktree` return — git's fatal "not a repository" status exempted (guard loosened) | killed | `p910-not-a-git-repo` |
| X3 | P10 | `if r.returncode != 0:` → `if r.returncode < 0:` with its `fresh probe exit=` return — only a signal counts as failure | killed | `p910-probe-exits-1` |
| X4 | P9 | `left = [x for x in r.stdout.splitlines() if x]` → `... if x and not x.endswith(".py")` — an untracked `*.py` counts as clean (over-broad exclusion) | killed | `r36-P6`, `r36-P7` |

`MUTANTS total=7 killed=4 survived=3 invalid=0` (`harness.txt`). X3 is killed by the p910 probe-exit
fixture precisely because its output stays byte-equal while the status is 1 — the fixture's design does
discriminate an exit-status weakening from a byte-equality weakening, which M42 alone did not show.

Caveat on attribution, not on the kills: both P9 kills come from **round-36** fixtures, so p910's own P9
coverage is only the not-a-repository branch. The untracked branch's strength across the whole battery
rests on one file name: `(d / "plans/round35_scratch.py").write_text(...)` in
`plans/round36_c1_verify.py:156`. X4 survives the moment that stray file stops ending in `.py`.

## Finding 2 — three survivors: limits of the battery, all cheaply killable

| id | clause | weakening | result |
|---|---|---|---|
| L1 | P10 | `r.stdout != want` → `r.stdout.rstrip() != want.rstrip()` (trailing-whitespace tolerance) | SURVIVED |
| L2 | P10 | `return True, f"probe_rerun=byte-equal ..."` → `return False, ...` — P10 rejects even the byte-equal success path | SURVIVED |
| L3 | P10 | `r.stdout != want` → `r.stdout.splitlines()[:1] != want.splitlines()[:1]` — first output line only | SURVIVED |

These are not gate defects and not violations of the frozen predicate: C1 is one-directional (each
advertised class must be *demonstrated*), and over-firing or under-comparing on an unexercised path
leaves it green. They are limits of what the battery demonstrates, and the single fact behind all three
is measured, not argued:

```
P10-exercised fixtures=3 p910-receipt-deleted,p910-probe-exits-1,p910-receipt-one-byte
P10-passing fixtures=0 -
```

All 64 fixtures never see P10 return `ok`: no fixture combines `--rerun` with an unmodified package.
Consequently (a) a gate that always rejects `--rerun` is indistinguishable, and (b) the only
byte-difference fixture, `p910-receipt-one-byte`, flips a byte at `receipt.index(b"biopython=")`, i.e. on
output line 1 of 21, so line-1-only comparison is indistinguishable from full comparison.

Smallest safe correction, demonstrated feasible (`correction_check.txt`):

```
REF A genuine+rerun      rc=0 defects=-
REF B byte-off-line5     rc=1 defects=P10,P2
REF C trailing-space     rc=1 defects=P1,P10
MUT L1 flips=C trailing-space
MUT L2 flips=A genuine+rerun
MUT L3 flips=B byte-off-line5,C trailing-space
```

* add a fifth fixture to a battery module: genuine package + `--rerun`, `expect: accept`, `defects: []`
  (reference run: `P10 ok probe_rerun=byte-equal bytes=3399`, exit 0 — `positive_control.txt`) → kills L2;
* move (or add) the one-byte flip to a line other than 1 → kills L3;
* edit the probe to append one trailing space to byte-identical output → kills L1 (P1 fires as well, as
  for `p910-probe-exits-1`).

None of this is applied here; the frozen claim, the battery and `p910.py` are untouched.

## Finding 3 — do the p910 fixtures isolate one defect, as the docstring says?

Docstring claim (`plans/battery37/p910.py:1`): "one single-defect fixture per frozen mutant M39, M41, M42,
M43"; and `:8-10` "P2 fires as well and that is unavoidable: `spec["receipt"]` is the single input to
both P2's digest pin and P10's re-run baseline."

Isolation matrix (`isolation_matrix.txt`), per fixture, which frozen mutants of the declared clauses flip it:

```
REF p910-not-a-git-repo          rc=1 defects=P9         M39 only
REF p910-receipt-deleted         rc=1 defects=P10,P2     M02 (P2 unreadable), M41 (P10 unreadable)
REF p910-probe-exits-1           rc=1 defects=P1,P10     M01 (P1 digest), M42 (P10 exit)
REF p910-receipt-one-byte        rc=1 defects=P10,P2     M03 (P2 digest), M43 (P10 bytes)
REF genuine-rerun(DIAG)          rc=0 defects=-         (not in the battery)
MUT M40 P9  flips=-   -- untracked file present
```

Verdict per fixture:

* **p910-not-a-git-repo — yes, isolated.** One defect (no worktree), one clause (P9), and it reacts only to
  M39; M40 does not flip it, so the untracked branch is provably not in play.
* **p910-receipt-deleted — isolated as a defect, not as a clause.** One defect (delete the receipt) with two
  declared consequences; it reacts to exactly one mutant per declared clause (M02, M41) and to no other.
  The "unavoidable" sentence is grounded in code: `c_receipt` hashes `spec["receipt"]` (`pkg_gate.py:118`)
  and `c_rerun` reads the same path (`pkg_gate.py:268`).
* **p910-probe-exits-1 — isolated as a defect, not as a clause.** It reacts to M01 and M42 only, and P1 is
  forced because the edited file is a pinned instrument: `frozen_instruments` pins
  `plans/tb2_grader_probe.py` at `acd7d38d…` (`pkg-spec-r35.json`), so any behavioural edit of the probe
  changes its digest. The docstring's second clause set is exact.
* **p910-receipt-one-byte — isolated as a defect, but it does not discriminate the strength of the branch
  it names.** Its single byte flip lands on line 1, so L3 (line-1-only comparison) fires identically; the
  fixture proves "some difference is detected", not "the whole stream is compared". See Finding 2.

Two supporting checks on the fixtures' own scaffolding:

* The `.gitignore` claim is true, not decorative. Counterfactual (`positive_control.txt`): after one gate
  run the fixture contains `corpus/evidence/round35/tb2-eval/__pycache__/test_outputs.cpython-313.pyc`; with
  the staged `.gitignore` removed, the same bytes give
  `P9 DEFECT untracked=1 first=corpus/evidence/round35/tb2-eval/__pycache__/test_outputs.cpython-313.pyc`.
  The fixtures stay P9-clean only because of that staged file, so the p910 P10 fixtures are one run-order
  accident away from reporting P9 instead of P10.
* No fixture masks its target clause by short-circuiting: `run_checks` (`pkg_gate.py:293-302`) runs every
  requested clause and only counts defects, so a co-firing clause cannot hide a later one.

## Impacted axes

C1 calibration only. C2 coverage and the frontier are untouched by this seat. The frozen predicate
(`killed=55/55`) remains true; what is overstated is the battery's demonstrated rejection surface, not the
count of demonstrated classes.

## Verdict

The four extra mutants are killed, so p910's P9/P10 clauses are calibrated beyond the frozen set in the
direction the counter tests. The seat's real finding is one-directional coverage: p910 supplies the only
fixtures that ever reach P10 and not one of them lets P10 pass, which leaves three surviving weakenings,
each killable by a two-line fixture whose acceptance is already measured.

VERDICT: extra-mutants-p910-killed-4/4
