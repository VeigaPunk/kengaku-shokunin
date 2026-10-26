# R36GateC — C1 hardened gate candidate (wave 1)

Seat: R36GateC (executor). Deliverable: `.ufo/waves/round-36/build/R36GateC/pkg_gate.py`
(399 lines, stdlib only: argparse, hashlib, json, os, pathlib, re, subprocess, sys).
sha256 `2cafbe190f7e99e4d4ead66fa4519d139afd0d616d782bd4af7b5dc006d7e786`.
No lane file was written; no git mutation ran outside a mktemp clone; nothing installed (uv 0.13.0
and biopython 1.85 were already cached).

## Battery (target met)

Fixture clone (`mktemp -d`, `git clone --shared --no-checkout`, sparse
`/corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build`,
`checkout master`, toplevel verified, counter files copied, gate installed as `plans/pkg_gate.py`,
index-only `git add -A`), then `python3 plans/round36_c1_verify.py --lane .`:

```
FIXTURE P0 expect=accept observed=accept ok -- genuine round-35 package
FIXTURE P1 expect=reject observed=reject ok -- 8 one-word quotes
FIXTURE P2 expect=reject observed=reject ok -- 8 copies of one quote
FIXTURE P3 expect=reject observed=reject ok -- an unparsed quote row beside the genuine rows
FIXTURE P4 expect=reject observed=reject ok -- junk teaches cells
FIXTURE P5 expect=reject observed=reject ok -- stub probe printing the receipt
FIXTURE P6 expect=reject observed=reject ok -- untracked leftover file
FIXTURE P7 expect=reject observed=reject ok -- cheapest package: one-word quotes + junk teaches + stub probe + stray file
FIXTURE L1 expect=accept observed=accept ok -- D4 genuine correction line
FIXTURE L2 expect=reject observed=reject ok -- D4 line with the two file:line citations swapped
FIXTURE L3 expect=reject observed=reject ok -- D4 line without the harness token
FIXTURE L4 expect=accept observed=accept ok -- D5 genuine erratum line
FIXTURE L5 expect=reject observed=reject ok -- D5 erratum saying the quote is not present
FIXTURE L6 expect=reject observed=reject ok -- D5 genuine line over an altered (quote-injected) capture
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=open observed=pass agree=NO fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0
R35-D2 status=open observed=pass agree=NO untracked_anywhere=0 line_fixtures_wrong=0/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=2 mismatches=2
PREDICATE C1 fail
EXIT=1
```

The `FIXTURES` line is the frozen target. The two `mismatches` are ledger bookkeeping for the L1, not
gate behaviour: R35-D1 and R35-D2 now *pass* while their rows still say `open` (close them,
`closed_round: 36`). R35-D3 (21 committed round-34 nested paths at `master`) and R35-D4
(`corpus/lessons/round-36.md` absent) are the other seats' surfaces and remain red here, as the wave
context predicted.

## Real lane

```
python3 .../build/R36GateC/pkg_gate.py package --root /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --rerun --spec .../plans/pkg-spec-r35.json
P1 ok frozen_instruments=3
P2 ok receipt sha256=2359d9067906 cases=18 observed_pass=5 observed_fail=13 mismatches=0
P3 ok sources=S105,S106,S107 verified-at=2026-10-25
P4 ok negative_space_words=136 falsifier=yes
P5 ok rows=22 distinct_quotes=22 distinct_lines=22
P6 ok rows=3 cells=11 teaches_min=23w
P7 ok pinned_captures=6 manifest=SHA256SUMS
P8 ok index_rows=42 knowledge_files=42
P9 ok not-requested
P10 ok rerun exit 0 bytes=3399
defects=0
EXIT=0
```

`--require-clean-tree` was omitted (the lane holds untracked wave dirs). The probe ran with
`PYTHONDONTWRITEBYTECODE=1`; `git status --porcelain` after every run is unchanged
(`?? .ufo/waves/round-36/{assimilation,build,build.ready,build.ready.dispatched,integrate}`) and no
`__pycache__` was written under `corpus/evidence/round35`.

## What each battery fixture dies of (first DEFECT line, measured)

| Fixture | rc | Killing clause |
|---|---|---|
| P0 genuine | 0 | — |
| P1 one-word quotes | 1 | `P5 DEFECT 8 quote(s) outside 3..25 words` |
| P2 8 copies of one quote | 1 | `P5 DEFECT distinct_quotes=1 distinct_lines=1 (want >= 8)` |
| P3 unparsed quote row | 1 | `P5 DEFECT unparsed_rows=1 of 23` |
| P4 junk teaches cells | 1 | `P6 DEFECT cells under 8 words: S105/S106/S107.teaches=1w` |
| P5 stub probe | 1 | `P1 DEFECT frozen_instruments=3 changed=plans/tb2_grader_probe.py=72fac5461bde` |
| P6 untracked leftover | 1 | `P9 DEFECT untracked=1 e.g. plans/round35_scratch.py` |
| P7 cheapest all-junk | 1 | P1 + P5 + P6 + P9 (four independent clauses) |
| L1 D4 genuine | 0 | — |
| L2 D4 citations swapped | 1 | `D4 DEFECT directional pattern absent near its citation: R34C2CounterDraft\.md:8…records…SELFTEST cases=10 failed=0` |
| L3 D4 harness token gone | 1 | `D4 DEFECT directional pattern absent near its citation: R34MutC2Harness\.md:12…SELFTEST green failed` |
| L4 D5 genuine | 0 | — |
| L5 D5 "not present" | 1 | `D5 DEFECT erratum lacks 'is present'` |
| L6 D5 over injected capture | 1 | `D5 DEFECT capture sha256=030d85ccf8ae manifest=b60af7757074` |

Clauses with **no** battery fixture (a calibration gap the wave-2 mutation seat should attack):
P2 (receipt pin), P3 (provenance trio), P4 (negative space), P7 (capture manifest), P8 (README
parity), P10 (`--rerun`). Each was shown able to fail below; P10 is additionally exercised at the tip
inside ledger row R35-D1 (`tip_package_rc=0`) and by the real-lane run above.

## Extra falsifiers, one per uncovered clause (built from the counter's own genuine fixture)

| Mutation on a fresh copy of genuine P0 | rc | Observed line |
|---|---|---|
| A receipt gains a trailing byte | 1 | `P2 DEFECT receipt sha256=ec901166854b pinned=2359d9067906` |
| B extra capture file `extra-capture.py` (unpinned) | 1 | `P7 DEFECT capture defects=unpinned:extra-capture.py` |
| C first quote re-cited one line down (`:13` → `:14`) | 1 | `P5 DEFECT quote not on test_outputs.py:14-14` |
| D every `falsif…` line deleted from `## Negative space` | 1 | `P4 DEFECT negative space carries no falsifier` |
| E README index row for the entry deleted | 1 | `P8 DEFECT index rows for knowledge/tb2-protein-assembly-grader.md = 0` |
| F S106 teaches cell → `short` | 1 | `P6 DEFECT cells under 8 words: S106.teaches=1w` |
| G S107 row appended a second time | 1 | `P6 DEFECT S107 present 2 times` |

## Not fixture recognition (attacked by construction)

The gate reads only spec-named paths and never the caller's path, so relabelling is inert. Measured on
the counter's own fixtures, moved to deliberately misleading paths:

```
relocated_genuine rc=0 defects=[]        # P0 moved to .../P7-junk-cheapest-all-mutant
relocated_junk    rc=1 defects=['P5 DEFECT 8 quote(s) outside 3..25 words: 'gblock_path'=1w,…']
                                         # P1 moved to .../P0-genuine-round-35-package
```

## Exit-code contract (measured)

| Invocation | Exit |
|---|---|
| `package` on genuine | 0 |
| `package` on any junk | 1 |
| `package --root /tmp/does-not-exist-xyz` | 2 (`GATE setup error: root not a directory`) |
| `package` with a spec lacking `rows` | 2 (`GATE setup error: spec lacks 'rows'`) |
| `package --root .` (no `--spec`) | 2 (argparse) |
| `d4-line --file /tmp/nope.txt` | 1 (`D4 DEFECT file absent`) — absent evidence is a reject, not a crash |
| unexpected exception | 2 (`GATE error <type>`) |

## Gate semantics as built (short)

P1 frozen-instrument sha256 pins · P2 receipt sha256 pin + exactly one green `cases=` summary line
that the entry quotes verbatim · P3 first three lines are `source: S105|S106|S107 ` with the pinned
URL, then `verified-at:` and a `recheck:` date/cadence · P4 `## Negative space` carrying `falsif…` ·
P5 the `## Located quotes` table parsed row by row (an unparsed row is a defect, never skipped), every
quote 3..25 words and verbatim on its cited capture line(s), every cited capture one of the spec's
capture names, ≥8 distinct quotes at ≥8 distinct `(file,line)` pairs · P6 S105–S107 once each, 11
cells, pinned URL, tier A, status mined, opened date, used-by = entry, scope and teaches cells ≥8
words, teaches pairwise distinct · P7 `SHA256SUMS` parses, every listed byte matches, no captured
regular file is unpinned, and each spec row's digest equals its manifest entry · P8 one README index
row naming all three rows, a `## Coverage map` bullet, knowledge files == index rows · P9
`git -C ROOT ls-files --others --exclude-standard` empty · P10 the spec's probe command reproduces the
receipt byte for byte (direct interpreter first, then the `uv --with biopython==1.85` toolchain the
captured `test.sh:21` pins).

## Limits named

- Six of the ten package clauses have no frozen battery fixture; the extra-falsifier table is the only
  evidence they can fail. A wave-2 mutant aimed at P2/P3/P7/P8 (~e.g. a correctly re-pinned but
  semantically wrong receipt) is not covered by the frozen battery and would need the mutant reported,
  not a battery change (claims' kill rule).
- P5 applies 3..25 words to **every** row. The genuine entry's shortest quotes are exactly 3 words
  (`gblock_path = Path("/app/gblock.txt")`, `flag_aa = "DYKDDDDK"`), so the rule is tight against a
  shorter rounding; a future package with a 2-word claim quote would be rejected by design.
- P6's distinctness is on the teaches cell only (scope cells are word-counted, not de-duplicated).
- P8's parity is dynamic (files vs index rows), not the literal 42, so a new knowledge file without a
  README row fails — intended.
- P9 needs `git` and a repository root; without one it is a DEFECT, not a skip.
- P10's fallback (`uv run --no-project --with biopython==1.85`) can need a network fetch on a cold uv
  cache; a cold/offline cache yields `P10 DEFECT` (reject), never a green. cwd is the root, so the
  receipt's relative paths are reproducible from any clone.
- The gate never inspects the git index or HEAD (only P9 asks git for untracked paths), so a package
  cannot be admitted by being committed.

## Ledger note for the L1

Close R35-D1 and R35-D2 with `closed_round: 36` once the gate lands and R35-D3/D4 are fixed by their
own seats; the fixture clone already shows `observed_pass=2 … mismatches=2` with the gate in place.
VERDICT: gateC-false_green-0-false_red-0-unevaluated-0
