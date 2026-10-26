# R39CritSkipC2 — post-first-run skip controls for C2 (round 39 wave 1, critic)

Scope: `plans/round39_c2_verify.py` (V1–V7), `plans/pkg_gate.py` (P1–P10) and the frozen package they
gate, at lane tip `750473847af9c7a461487ba3a589b5519fac5ed8` (the claims' baseline is `b2bdd425`; the
lane has landed later round-39 commits). The first recorded probe run
`6a1eb5e1da4a435940b821e28530c31f3411549c` has landed, so `--rerun` is legal for these controls.

Nothing frozen was edited. All writes were in scratch clones under
`/fast/scratch/hyaku/kengaku-r39/R39CritSkipC2/` (`lane_a`, `lane_b`, `lane_c`, `lane_d`; each
`git -C … rev-parse --show-toplevel` = that clone) and in
`.ufo/waves/round-39/build/R39CritSkipC2/`. The lane's frozen inputs still hash to their pins:
`sha256sum plans/git_leak_probe.py plans/pkg_gate.py plans/pkg-spec-r39.json
corpus/evidence/round39/git-leak-dry-cases-freeze.txt` →
`4961a50f…`, `ea638822…`, `f62163ce…`, `e92a5d6d…` (the counter's `PROBE_SHA256`, `GATE_SHA256`,
`SPEC_SHA256`, `DRY_SHA256`).

Every control reuses one package builder, `mkpkg.py` (kept here), which writes a filler entry,
registry rows S117/S118 with the *correct* anchor digests, a README index row + coverage bullet, and
either the frozen receipt (`--receipt real`) or a typed one (`--receipt handtyped`); D starts from
`--receipt real` and then overwrites the receipt with the typed exact-format file. All four
controls therefore differ only in the receipt and in the requirement map's citation width.

## A. Literal `--dry` copy, typed with `observed=predicted`: red at V2 (P10)

Receipt typed from the frozen dry table in the dry table's own line shape
(`CASE <id> predicted=<p> observed=<p> tests=<L> violates=… -- …`), 5009 bytes
(`ctrl-a-typed-receipt.txt`); the probe was never run to produce it.

```
$ python3 plans/round39_c2_verify.py --lane "$S/lane_a" --work "$S/w_a"
V1 ok listed=7 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=12 distinct_quotes=12 distinct_lines=12 out_of_word_range=0
    gate: P4 ok checked=12 bad=0 first=0
    gate: P5 ok manifest_entries=7 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=46 knowledge_files=46 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=1
PREDICATE C2 fail
exit 1
```

**Which V: V2 only.** Every other check is green on junk prose: V3 accepts the correct anchors, V4
accepts the typed CASE lines and the typed summary (`mismatches_named=0/0`), V6 the census, V7 the
mechanically derived map. The single defender is the gate's P10 byte comparison reached through V2.

## B. Probe copy with every prediction `PPPPP`: `mismatches=12`

`plans/git_leak_probe_allp.py` in `lane_b` is the frozen probe with all 25 `Case(... "PPPPP" …)`
predictions rewritten (`re.subn(r'"(?:[PF]{5})"', '"PPPPP"', …)` → `n=25`); nothing else changed.

```
$ python3 "$S/lane_b/plans/git_leak_probe_allp.py" --lane "$S/lane_b" --work "$S/w_b"
cases=25 observed_pass=13 observed_fail=12 mismatches=12
exit 0
```

The twelve `match=NO` ids (`ctrl-b-probe-allppppp.txt`): `empty-app`, `untouched`,
`dangling-secret-blob`, `dangling-secret-commit`, `branch-keeps-leak`, `commit-message-secret`,
`notes-secret`, `untracked-file-secret`, `readme-edited`, `flag-extra-text`, `flag-is-directory`,
`flag-in-repo-only`. The prediction table is falsifiable: believing every case passes costs 12
detections. (The probe still exits 0 on mismatches by design; only a receipt line counts.)

## C. The round-38 informed-filler shape: `checks=7 defects=0` again

Package with the *frozen* receipt (never touched), the same false-prose entry, and a requirement map
citing one convenient violator per tag — the round-38 `R38CritC2Counter` §1 shape.

```
$ python3 plans/round39_c2_verify.py --lane "$S/lane_c" --work "$S/w_c"
V1 ok listed=7 bad=0 extra=0
    gate: … P3 ok rows=12 … P4 ok checked=12 … P8 ok index_rows=46 knowledge_files=46 …
    gate: P10 ok probe_rerun=byte-equal bytes=5867
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit 0
```

The accepted entry (`ctrl-c-filler-entry.md`) states, in `## Summary`:

> "The 25-case probe found no passing case at all: 0 pass, 25 fail"

while the receipt one directory away says `cases=25 observed_pass=13 observed_fail=12
mismatches=0` (`corpus/evidence/round39/git-leak-probe.txt:30`). No check compares the two.

Its twelve quote rows carry verbatim quotes under false claims, for example (claim 1 of 12, all
`ctrl-c-filler-entry.md`):

- claim *"the grader rebuilds the repository from a Debian source package and diffs it"* on quote
  `["git", "-C", "/app/repo", "log", "--all", "-p", "-S", "secret["],` (`test_outputs.py:41`) — the
  capture has no build line at all: `grep -cE 'make|dpkg|gcc|[Dd]ebian'
  corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py` → `0`.
- claim *"the work-tree checksum skips the repository directory entirely"* on
  `"find /app/repo -type f -not -path '*/\.*' "` (`test_outputs.py:101`) — it is a `find` over
  `/app/repo`.
- claim *"the whole score is one comparison with a compiled binary"* — the capture defines five
  tests (`grep -c '^def test_' …` → `5`).

Its requirement map, mechanically derived from the receipt and the dry table and citing the
first violator only:

```
| `instruction.md:3` | `recover-secret` | enforced | `empty-app` |
| `instruction.md:4` | `secret-gone` | partly | `untouched` |
| `instruction.md:5` | `files-untouched` | enforced | `empty-app` |
| `instruction.md:5` | `messages-untouched` | partly | `empty-app` |
```

Three of the four tags are witnessed by the do-nothing control, which is the same
"label from one convenient witness" shape round-37 closure D2 called a defect, now legal in the
`cases` column. `## Negative space` is satisfied by its own negation: *"no falsifier is offered for
the summary above"* — the gate only searches for `falsifi(?:er|ed|es|ability)`.

**So yes: the carried round-38 limit reproduces exactly on this package.** V4's
`mismatches_named=0/0` has no subject on a landable receipt (P10 forces `mismatches=0`), so the one
clause that could make the frozen predictions load-bearing is vacuous by construction again.

## D. Sharpening A: a format-perfect typed receipt is still red — by 58 bytes on one line

Typing the receipt from the frozen dry table in the probe's *exact* line shape (adding
`predicted_tests=<L>` and `match=yes`, assuming `observed=predicted`) gives 5809 bytes; the frozen
receipt is 5867:

```
$ diff typed-receipt-exact-format.txt corpus/evidence/round39/git-leak-probe.txt
28c28
< CASE flag-is-directory … match=yes violates=recover-secret -- cleanup + …
---
> CASE flag-is-directory … match=yes violates=recover-secret test_flag_file_exists_and_correct:error=IsADirectoryError -- cleanup + …
```

Counter on that receipt: same transcript as A — `checks=7 defects=1`, `V2 DEFECT`, exit 1. The one
thing a typed receipt cannot invent is the exception suffix, which only a real run produces. That is
P10's whole information content here: one line out of 29. Independent confirmation that the probe
output *is* deterministic on this host: a direct run in `lane_a` is byte-identical to the frozen
receipt (`ctrl-probe-direct.out`, 5867 bytes, `cmp` clean).

## Impacted axes

- **calibration (8):** the frozen C2 predicate (`claims` §C2: `checks=7 defects=0` + `PREDICATE C2
  pass`) still admits a package whose entry contradicts the receipt it cites, whose twelve quote
  claims are unsupported by the capture, and whose map cites the do-nothing case for three tags.
  Green here is evidence about eleven anchors and eight word-counts, not about the reading or the run
  (parts A–C). Under the assignment's own scoring this is 2 of 3 skip controls red.
- **coverage:** unchanged and still capped at 7 by the open L0 question; the capture, probe and P10
  keep their value (B shows the prediction table is falsifiable; A/D show the receipt cannot simply be
  typed).
- **operability:** the whole counter runs in ~1.4–2.8 s on this host, `gate_exit=0/1` as expected,
  census clean (`V6 ok census_exit=0`) with the two new registry rows.

## Smallest safe correction

One clause, local, receipt-checkable: **bind the entry to the receipt's own summary.** In V4, require
the entry to contain the receipt's `SUMMARY` line's verdict pair verbatim (e.g. a line
`receipt: cases=<n> observed_pass=<p> observed_fail=<f>`), and reject the entry if any other
`observed_pass=<n>`/`<n> pass` statement for this package appears. My filler dies on it (its Summary
says `0 pass, 25 fail` against `observed_pass=13 observed_fail=12`); the frozen receipt already
carries that line (`corpus/evidence/round39/git-leak-probe.txt:30`), so an honest entry pays nothing.
~6 lines, no new input, no relaxation.

Second (only if the round-38 §8.2 item is wanted in this round): require each requirement-map row to
cite one observed-`pass` and one observed-`fail` violator where both exist — `secret-gone` and
`messages-untouched` each have both, so the `empty-app`-only citations fail.

## Limits of these controls

- Controls C/D reuse the frozen receipt, which is on disk before the entry is written; P10 cannot
  distinguish "copied the real run" from "the real run happened", and neither can this critic. The
  order-of-operations question is the separate R3 gate, not V1–V7.
- I did not run the counter on the real lane (that is the reviewer's call); the lane digests above are
  read-only checks, and the lane was never written (no git or jj command ran there).
- Host git 2.56.0/bash stand in for the image's Ubuntu git/dash, as the probe docstring says.

## Evidence

`mkpkg.py` (package builder), `ctrl-a-counter.txt`, `ctrl-a-typed-receipt.txt`,
`ctrl-b-probe-allppppp.txt`, `ctrl-c-counter.txt`, `ctrl-c-filler-entry.md`, `ctrl-d-counter.txt`,
`ctrl-d-typed-receipt.txt`, `ctrl-d-typed-vs-frozen.diff`, `ctrl-probe-direct.out` — all under
`.ufo/waves/round-39/build/R39CritSkipC2/`. Scratch `/fast/scratch/hyaku/kengaku-r39/R39CritSkipC2/`
removed after the receipts were copied.

VERDICT: c2-skip-controls-red-2/3
