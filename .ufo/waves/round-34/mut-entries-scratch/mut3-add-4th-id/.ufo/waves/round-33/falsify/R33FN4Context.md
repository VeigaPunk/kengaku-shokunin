# R33FN4Context — N4 closure hash context (falsify seat, mutation probe)

Seat: `KengakuR33.R33FN4Context` (mutation-tester), round 33 / hyaku run 7, 2026-10-25.
Target claim (frozen, `plans/round-33-claims.md` §C2): **N4** — the fleet report
`.ufo/reports/round-32/kengaku.md` contains the round-32 closure tip `112091c`
(append-only addendum). Counter: `plans/round33_defects.py`, `check_n4`
(lines 114–121), `CLOSURE_TIP = "112091c"` (line 47).

## Attack

In a fresh `/tmp` fixture, retain the required N4 text but place `112091c` only in an
unrelated appendix sentence — i.e. the hash is present, but never named as the
round-32 closure tip in an addendum. If `check_n4` still passes, unrelated presence
passes and the check binds no context.

## Instrument / fixture provenance (all bytes in `/tmp/r33-fn4context/`, no lane or fleet write, no git anywhere)

- `plans/round33_defects.py` copied to the sandbox, sha256
  `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6` (identical to the
  lane file before and after the run).
- Live fleet report read-only-copied as `r32-live.md`, sha256
  `b71dc9a62eb69f983b86452c29f3bad102baf450256c74bab9cc3b9af03c4faf`.
- **P (pristine baseline)** = live report bytes with the `## Addendum (round 33 …)`
  block cut, i.e. the filed report retaining all required N4 text and no closure tip
  (asserted: `112091c not in P`); sha256 `2e388493f7a4c45a39bf710450c467c1154db6f013f969911da07cec3ac925bf`.
- **M (mutant)** = P verbatim (`M.startswith(P)` asserted) + appendix section whose
  only `112091c` occurrence (asserted count == 1) is an unrelated housekeeping
  sentence: `label `112091c` was reused for a discarded draft archive; the label is
  unrelated to this report's subject matter and to any version-control state.`
  sha256 `9a13b117ea8b7616283375e151a4dc240fa2643e9471fc6d79588450b5765ac3`.
- **R (restoration control)** = byte copy of P.

Probe invoked the module's own public predicate exactly as its selftest does
(`round33_defects.py:196-199`), importing the byte-identical copy:
`check_n4(<sandbox>, <fixture>)`; `check_n4` never reads its `lane` argument.

## Expected detector (context-bound counter)

`check_n4(M)` should return the red reason — the hash is present but the report does
not name it as the round-32 closure tip in an append-only addendum, and no addendum
was appended to the mutant beyond an unrelated register.

## Observed output (verbatim)

```
P sha256: 2e388493f7a4c45a39bf710450c467c1154db6f013f969911da07cec3ac925bf
M sha256: 9a13b117ea8b7616283375e151a4dc240fa2643e9471fc6d79588450b5765ac3
R sha256: 2e388493f7a4c45a39bf710450c467c1154db6f013f969911da07cec3ac925bf | R bytes == P bytes: True
CLOSURE_TIP constant: 112091c
check_n4(P) -> 'the round-32 report does not name the round-32 closure tip 112091c'
check_n4(M) -> ''
check_n4(R) -> 'the round-32 report does not name the round-32 closure tip 112091c'
M occurrence @ line 67: label `112091c` was reused for a discarded draft archive; the label is unrelated
```

## Verdict: **caught? NO — uncaught (mutant SURVIVES / GAMED)**

- Baseline sanity: `check_n4(P)` reddens with the exact frozen reason string, so the
  detector works on this fixture class and the result is conclusive (not a
  false-negative of the harness).
- Mutant: `check_n4(M)` returns `''` (green). **Unrelated presence passes**: any
  sentence in the report — however unrelated to closure — satisfies N4. `check_n4` is
  a bare substring test (`CLOSURE_TIP not in read(r32_report)`): no closure-tip
  context binding, no addendum/append-only verification, no word boundaries (it also
  matches inside the full 40-char hash `112091c2d9077e…`, as the live addendum does).
- This independently reproduces build-wave `R33CounterAttack.md` §3 row E4 ("GAMED —
  bare substring test, no commit/tip context bound") and blind-spot B4, on a fixture
  derived from the real report bytes rather than synthetic text.
- Coverage finding only: the frozen claim's predicate is a presence test; the
  contract forbids changing the instrument. No lane/fleet byte was mutated; the
  module copy was imported, never edited.

## Restoration evidence

- `fixture-restored.md` bytes == `fixture-pristine.md` bytes (sha256
  `2e388493…` both, `R bytes == P bytes: True`); detector red again on R.
- Lane instrument unchanged across the run:
  `plans/round33_defects.py` sha256 `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`
  before and after. Fleet report `r32-live.md` read-only (sha
  `b71dc9a6…` unchanged; the live file was never opened for writing).
- No git/jj command was run in any repo; sandbox `/tmp/r33-fn4context/` only.
  No tools installed.

## Limitation

`check_n4` ignores `--lane` and defaults to the absolute fleet path (build finding B6;
`R33ExecDefsBefore.md` §6), so the aggregate `--lane .` counter reads the live fleet
report regardless of any lane tree. The probe therefore exercises `check_n4`'s
predicate directly via its explicit `r32_report` parameter — the same interface the
counter's selftest uses — which is the exact predicate the aggregate run applies to
the real file.
