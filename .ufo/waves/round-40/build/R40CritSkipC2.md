# R40CritSkipC2 — post-first-run skip controls for C2 (round 40 wave 1, critic)

Scope: `plans/round40_c2_verify.py` (V1–V7), `plans/pkg_gate.py` (P1–P10, digest `ea638822…`), the frozen
package they gate, at lane HEAD `3077adbc7145726519f60f01426a5d03381ad444` (`git -C <lane> rev-parse HEAD`;
freeze `bbb1095`, first recorded probe run `055748f`). Nothing frozen was edited; every hash re-checked
unchanged: `sha256sum plans/pkg_gate.py plans/pkg-spec-r40.json plans/db_wal_probe.py
corpus/evidence/round40/db-wal-dry-cases-freeze.txt` → `ea638822…`, `4af78f4f…`, `69af65df…`, `688f3475…`
(`frozen-digests-observed.txt`), i.e. the counter's `GATE_SHA256`/`SPEC_SHA256`/`PROBE_SHA256`/`DRY_SHA256`.

All writes were in scratch clones under `/fast/scratch/hyaku/kengaku-r40/R40CritSkipC2/` (`lane_a`,
`lane_b`, `lane_c`, `lane_d`, `lane_e`, `lane_f`, `lane_g`, each `git -C … rev-parse --show-toplevel` = that
clone, every write committed to the index only) and in this report dir. The lane was never written: the two
`git` calls on it are read-only (`rev-parse`, `diff`, `show`). Scratch removed at the end.

One package builder, `mkpkg40.py` (kept here), writes a filler entry (`## Summary`, 13 verbatim quotes from
`test_outputs.py`/`instruction.md`, `## Requirement map` derived from a receipt, `## Negative space`), a
README index row + coverage bullet, and the receipt named by `--receipt` (`real`, `typed-literal`,
`typed-format`, `typed-derived`). Rows S119/S120 are **not** in the clone at HEAD (see §F); every control
below copies the two registry rows from the lane worktree (`rows-S119-S120.txt`, sha256 `ab23548c…`) so the
controls isolate the receipt/prose question instead of re-testing a missing row.

## A. Literal `--dry` copy with `observed=predicted`: red at V2, and only V2

Receipt typed from the frozen dry table in the dry table's line shape with the summary converted
(`cases=28 observed_pass=8 observed_fail=20 mismatches=0`), 4841 bytes; the probe was never run to make it.

```
$ python3 plans/round40_c2_verify.py --lane "$S/lane_a" --work "$S/w_a"
V1 ok listed=8 bad=0 extra=0
    gate: … P6 ok rows=2 … P9 ok untracked=0 …
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 ok … V4 ok cases=28 mismatches_named=0/0 bad=0 … V5 ok … V6 ok … V7 ok rows=6 tags=6 bad=0
checks=7 defects=1
PREDICATE C2 fail
```

**Which V: V2 only** (P10, `plans/pkg_gate.py:284`). V4 accepts the typed CASE lines and the typed summary;
V3/V5/V6/V7 are green on filler prose (`ctrl-a-counter.txt`).

## B. Probe copy predicting `PPPPPPP` everywhere: `mismatches=20`

`plans/db_wal_probe.py` copied to `plans/db_wal_probe_allp.py` with `re.subn(r'"([PF]{7})"', '"PPPPPPP"', …)`
→ `replacements 28`; nothing else changed.

```
$ python3 "$S/lane_b/plans/db_wal_probe_allp.py" --lane "$S/lane_b" --work "$S/w_b"
cases=28 observed_pass=8 observed_fail=20 mismatches=20
exit 0
```

Twenty `match=NO` ids (`ctrl-b-match-no-ids.txt`): `empty-app`, `untouched`, `base-only-ro`,
`plain-read-then-solve`, `xor-wrong-key`, `decrypt-in-place-no-json`, `literals-id3-name-wrong`,
`truth-value-float-id1`, `truth-reversed-order`, `truth-plus-duplicate-id11`, `truth-dup-id10-no-id11`,
`truth-wrapped-object`, `truth-ids-as-strings`, `truth-ids-as-floats`, `truth-trailing-garbage`,
`truth-wrong-path`, `empty-list`, `truth-drop-id11`, `truth-name-null-id1`, `truth-value-string-id4`. The
frozen prediction table is falsifiable: believing every case passes costs 20 detections. (The probe exits 0
on mismatches by design; only the receipt line counts.)

## C. The round-39 informed-filler shape: `checks=7 defects=0` again

Frozen receipt untouched, `--prose false --cites one`:

```
$ python3 plans/round40_c2_verify.py --lane "$S/lane_c" --work "$S/w_c"
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
V1 … V7 all ok … checks=7 defects=0
PREDICATE C2 pass
```

The accepted entry (`ctrl-c-filler-entry.md`) says, in `## Summary`:

> "The 28-case probe found that every case passes: 28 pass, 0 fail."

against `cases=28 observed_pass=8 observed_fail=20 mismatches=0` in the receipt one directory away
(`corpus/evidence/round40/db-wal-probe.txt:35`). **No check compares the two.** V4's one load-bearing clause,
`mismatches_named=0/0` (`plans/round40_c2_verify.py:191`), has no subject on a landable receipt: this package
carries `mismatches=0`. Its requirement map cites one violator per tag (`fix-wal`, `extract-all`,
`record-format` are `partly` and are witnessed only by a single case), and V7's `derive` is satisfied by that.

## D. Sharpening A: the format-perfect typed receipt is red by exactly six lines

Typing the receipt in the probe's exact line shape (adding `predicted_tests=`, `match=yes`, `regrade=same`,
headers from `PINS`, both footers) but without the exception suffixes gives 6648 bytes; the frozen receipt is
8257: `ctrl-d-vs-frozen.diff` differs on **6 CASE lines** and nothing else. Counter: identical transcript to
A — `V2 DEFECT`, `checks=7 defects=1`, exit 1. So P10's barrier is the exception cell only.

## E. The derived receipt: P10 has zero information content on this package

`mkpkg40.py --receipt typed-derived` builds the receipt from three public frozen artifacts and never opens
the receipt file: the dry table (`CASE … predicted= observed= tests= violates= -- …`), `PINS` and the two
footer lines from `plans/db_wal_probe.py`, and a six-row table of exception classes read off
`test_outputs.py` (`open()` → `FileNotFoundError`, `json.load()` → `JSONDecodeError`, `item["id"]` over the
wrapped dict's string keys → `TypeError`).

```
$ cmp "$S/ctrl-e-typed-derived.txt" corpus/evidence/round40/db-wal-probe.txt && echo DERIVED-BYTE-EQUAL
DERIVED-BYTE-EQUAL
$ python3 plans/round40_c2_verify.py --lane "$S/lane_e" --work "$S/w_e"
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
checks=7 defects=0
PREDICATE C2 pass
```

The receipt is 35 lines: 1 title + 4 capture digests + 28 CASE lines + `regrade cases=28 differ=0` +
the summary. Every cell except **32 error tokens in 6 lines** (24 `FileNotFoundError`, 6 `JSONDecodeError`,
2 `TypeError`; `grep -o 'error=[A-Za-z]*' … | sort | uniq -c`) is already printed by `--dry`; those 32 tokens
name three classes readable from the grader's three exception sites, and `regrade=same` is the determinism
claim the rider asserts. Honest limit: I had seen the receipt's `error=` tokens in a grep before writing the
table, so this construction shows derivability, not that a reader derives it blind.

## F. Composite: derived receipt beside a false entry also passes (no run, false summary)

```
$ python3 plans/round40_c2_verify.py --lane "$S/lane_f" --work "$S/w_f"
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
checks=7 defects=0
PREDICATE C2 pass
```

`ctrl-f-derived-false-entry.md` carries the same false `## Summary` as C. So a package whose receipt no run
produced, whose prose contradicts the receipt it cites, and whose map cites one convenient violator satisfies
the frozen predicate. The counter does execute the probe (P10 reruns it and byte-compares) and the dry table
(V5), so green does establish **reproducibility on this host**, not execution before the entry.

## G. Integration blocker found while isolating the controls: S119/S120 are not at HEAD

A clean clone of `3077adb` has no registry rows: `git -C lane_a show HEAD:corpus/SOURCES.md | grep -c S119`
→ `0`; `grep -cE '^\| S11[9]'` on the lane worktree → `1`. The lane worktree carries them uncommitted
(`git -C <lane> diff --stat corpus/SOURCES.md` → `2 ++`, exactly the two rows). On such a clone the package
is red at **two** checks for the wrong reason:

```
$ python3 plans/round40_c2_verify.py --lane "$S/lane_g" --work "$S/w_g"
    gate: P6 DEFECT rows=2 bad=2 first=S119: rows=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=1
V2 DEFECT … V3 DEFECT rows=2 bad=['S119:row', 'S120:row']
checks=7 defects=2
PREDICATE C2 fail
```

The L1 must land the two rows with the entry; the predicate is measured on a clean clone of the landing tip.

## Impacted axes

- **calibration (8):** the answers are (a) red at V2 only, (b) `mismatches=20`, (c) green — `checks=7
  defects=0` again (C), and green even with a wholly derived receipt and a false summary (E, F). The claim's
  sentence "authenticity rests on P10, the fresh probe run byte-compared to the receipt"
  (`plans/round40_c2_verify.py:19`) is false as written on this package: P10 reruns the probe, so it buys
  reproducibility; the 8257 receipt bytes contain no observation the dry table lacks except three exception
  classes and one determinism claim. Relative to round 39 (where one exception suffix escaped the typist,
  `R39CritSkipC2.md` §D), round 40 is strictly weaker: all 28 predictions already match, so `observed=` is a
  copy of `predicted=`.
- **coverage:** unchanged and still capped at 7 by the open L0 question `kengaku | round-33`; the capture,
  probe and P10 keep their value (B shows the prediction table is falsifiable), so no coverage move is claimed
  or lost.
- **operability:** each counter run completes in ≈2.4 s wall (tool wall time, `--work` under NVMe scratch) with
  `gate_exit=0/1` as expected and `V6 census_exit=0` on the patched clones.

## Smallest safe correction (routed, not applied: V1–V7 are frozen this round)

1. **R40-D1, V4 ↔ entry summary.** Require the entry to carry the receipt's summary verdict verbatim in a
   fixed shape (`receipt: cases=<n> observed_pass=<p> observed_fail=<f>`) and reject any other
   `observed_pass=`/`<n> pass` statement for the package. C and F say "28 pass, 0 fail" against
   `observed_pass=8`; an honest entry pays one line, and the frozen receipt already carries it.
2. **R40-D2, P10 wording.** Weaken `plans/round40_c2_verify.py:19` to "reproducibility rests on P10;
   authenticity rests on the order gate and non-author review" — or give the receipt one cell `--dry` cannot
   print (E shows none exists today).
3. **R40-D3, V7 citation width.** Where a tag has both an observed-pass and an observed-fail violator, require
   the row to cite one of each (`fix-wal`, `extract-all`, `record-format` do); the one-witness map of C/E/F dies.
4. All three change the frozen checks. This round cannot take them: the claims froze "no check added or
   relaxed" (`plans/round-40-claims.md:81`) and "Kill rule: predicate not met at landing → not admitted"
   (`:86`). They belong to round 41 as routed items.

## Limits of these controls

- Controls C/E/F reuse or derive a receipt that is on disk before the entry is written; P10 cannot distinguish
  "copied the real run" from "the real run happened", and neither can this critic. The order question is
  `plans/order_check.py`, not V1–V7.
- I did not run the counter on the real lane (the reviewer's call); the lane digests above are read-only checks.
- Host python3 3.13/sqlite3 3.54.0/bwrap stand in for the image's Ubuntu 24.04 packages, as the probe
  docstring says. No tool was installed (pacman paused; `uv` already present and used only by the gate).

## Evidence (this directory)

`mkpkg40.py`; `ctrl-a-typed-literal.txt`, `ctrl-a-counter.txt`; `ctrl-b-probe-allppppp.txt`,
`ctrl-b-match-no-ids.txt`, `ctrl-b-stderr.txt` (0 bytes); `ctrl-c-counter.txt`, `ctrl-c-filler-entry.md`;
`ctrl-d-typed-format.txt`, `ctrl-d-vs-frozen.diff`, `ctrl-d-counter.txt`; `ctrl-e-typed-derived.txt`,
`ctrl-e-counter.txt`, `ctrl-e-derived-entry.md`; `ctrl-f-counter.txt`, `ctrl-f-derived-false-entry.md`;
`ctrl-g-rows-absent-at-head.txt`; `rows-S119-S120.txt`; `frozen-digests-observed.txt`.

VERDICT: c2-skip-controls-red-2/3
