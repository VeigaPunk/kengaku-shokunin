# R30GateQuote — C3 operability: the adoption gate validates quotes

Seat: `L1Kengaku30.R30GateQuote` (leaf). Round 30, claim **C3** (`plans/round-30-claims.md`).
Deliverable: `/tmp/r30-GateQuote/sources_adopt.py` (sha256 `f26ed9bb…7b14609d`, 791 lines),
extended from the lane's `plans/sources_adopt.py` (sha256 `6fe6e762…f7ead2`, 478 lines).
The lane file is **unmodified**: `git status --porcelain` in the lane lists no `plans/sources_adopt.py`,
so the only lane write is this report.

## 1. What the new mode does

`--quote-file <rows.txt> --artifact <path-or-dir>` — for every supplied registry-shaped row, take the
quoted spans in its **anchor cell** (0-based column 5, the column the live registry uses, e.g. S078's
`§The locked protocol line 75: "The verifier never runs in the agent's sandbox." (8 words)`) and require
each span to be

1. at most **25 words** (`QUOTE_WORDS`, SOURCES contract v1 rule 1 / QUALITY Q3), counted with
   `words(text) = len(text.split())` — the same counter `plans/round30_defects.py` uses, so a word count
   this gate prints cannot disagree with one a round's defect receipt prints; and
2. a **byte substring** of the artifact bytes, decoded UTF-8 and newline-normalised on both sides
   (`\r\n`→`\n`, lone `\r`→`\n`), never a fuzzy or whitespace-insensitive match.

Exit codes, each separately reachable:

| code | meaning |
|---|---|
| 0 | every span located and inside the cap |
| 2 | artifact names no file/directory, or holds no UTF-8 text (same class as argparse usage errors; `--quote-file`/`--artifact` given alone is argparse 2) |
| 4 | structural: unparsable row, anchor cell with **no** quoted span, or an **unbalanced** `"` whose greedily paired half is present |
| 6 | a span exceeds the cap → `EXIT_QUOTE_TOO_LONG` |
| 7 | a span is absent from the artifact → `EXIT_QUOTE_ABSENT` |

First refusal in the order 2, 4, 6, 7 wins; **every** refused row is still named, so one run surfaces all
defects. Two design points that exist because the alternative greens a quote nobody wrote:

- the parity refusal: with three `"` in a cell, greedy pairing validates `alpha` between two unrelated
  marks — mutant `m5` below proves the case catches it;
- a separate `found` counter: an over-long span that *is* in the bytes reports `overlong=1 found=1`, so a
  reader can tell "too long" (edit the quote) from "not in the capture" (re-open the source). Those are
  not the same repair.

Artifact may be one file or a directory; a directory is every UTF-8 file under it in **sorted path
order**, and a file that does not decode as UTF-8 is skipped by name rather than byte-replaced — a
mangled capture must not locate a quote that is not in it. The receipt names the file a span was found in.

## 2. Acceptance run — `SELFTEST cases=14 failed=0`, exit 0

```
$ python3 /tmp/r30-GateQuote/sources_adopt.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
SELFTEST cases=14 failed=0
EXIT=0
```

The four new cases, in the existing `CASE <name> PASS` form, appended after case 10 so **no existing case
changed name or order**:

| case | fixture | verdict required |
|---|---|---|
| `quote-overlong-refused` | 26-word quote, **present** in the artifact | `EXIT_QUOTE_TOO_LONG`, `overlong=["S015"]`, `absent=[]`, `located=[]`, `found=["S015"]` — the refusal is length, not absence |
| `quote-absent-refused` | 20-word quote absent from a **directory** artifact; plus a cell with no span; plus a 3-quote cell whose paired half *is* present | `EXIT_QUOTE_ABSENT` + `absent=["S016"]` + `artifacts=["capture.txt","notes.md"]`; structural rows `S019:no-quote` and `S021:unbalanced-quote` → `EXIT_MALFORMED`, `found=[]` |
| `quote-located-accepted` | CRLF capture, two spans, both present; and a twin row with one absent span | `EXIT_OK`, `located=["S017","S017"]`, `spans=2`; twin `EXIT_QUOTE_ABSENT` with `located=["S020"]` and `found=["S020"]`; `locates()` on an LF quote, a CRLF quote and a widened paraphrase |
| `quote-boundary-25-accepted` | exactly 25 words, present | `EXIT_OK`, `located=["S018"]`, `cap=25`, and `words(edge)==25`, `words(edge+" x")==26` |

## 3. Red receipt — the same cases fail on the pre-change body

The cases are run against the lane's pre-change bytes by `/tmp/r30-GateQuote/red_probe.py`
(sha256 `5921a0b9…d991033`), which loads a body as a module with every gate symbol resolved through it:

```
$ python3 red_probe.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py
CASE quote-overlong-refused FAIL
  AttributeError: body has no quote_check
CASE quote-absent-refused FAIL
  AttributeError: body has no quote_check
CASE quote-located-accepted FAIL
  AttributeError: body has no quote_check
CASE quote-boundary-25-accepted FAIL
  AttributeError: body has no quote_check
SELFTEST cases=4 failed=4
EXIT=1
```

Same probe, same case bodies, against the round-30 body:

```
$ python3 red_probe.py /tmp/r30-GateQuote/sources_adopt.py
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
SELFTEST cases=4 failed=0
EXIT=0
```

The claim's control line, verbatim — the pre-change bytes cannot reach the target at all:

```
$ python3 plans/sources_adopt.py --quote-file /tmp/r30-GateQuote/real/quotes-accept.txt \
      --artifact corpus/evidence/round25-calibration/attrib-calibration-summary.txt
usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]
                        [--package PACKAGE] [--admit-ids ADMIT_IDS]
                        [--entries ENTRIES] [--access-date ACCESS_DATE]
                        [--recheck RECHECK] [--out OUT] [--attest-opened]
                        [--scope-to-admit]
sources_adopt.py: error: unrecognized arguments: --quote-file /tmp/r30-GateQuote/real/quotes-accept.txt --artifact corpus/evidence/round25-calibration/attrib-calibration-summary.txt
EXIT=2
```

An absent API is a weak red on its own, so failure-capability is also proved by mutation (next section)
and by the pre-change selftest tally (section 5).

## 4. Mutation matrix — every new case is failure-capable, not vacuously true

Each mutant is the round-30 body with one semantic edit (`sed -E` on a `/tmp` copy); `grep FAIL|SELFTEST`
of `--selftest`:

```
=== m0-accepts-everything ===        (the three refusal branches replaced by `if False:`)
CASE quote-overlong-refused FAIL
CASE quote-absent-refused FAIL
CASE quote-located-accepted FAIL
SELFTEST cases=14 failed=3
=== m1-cap-exclusive ===             (`count > cap` → `count >= cap`)
CASE quote-boundary-25-accepted FAIL
SELFTEST cases=14 failed=1
=== m2-cap-off-by-two ===            (`count > cap` → `count > cap + 2`)
CASE quote-overlong-refused FAIL
SELFTEST cases=14 failed=1
=== m3-substring-disabled ===        (`locates` returns the first artifact name)
CASE quote-absent-refused FAIL
CASE quote-located-accepted FAIL
SELFTEST cases=14 failed=2
=== m4-normalise-identity ===        (`normalize_text` returns its input)
CASE quote-located-accepted FAIL
SELFTEST cases=14 failed=1
=== m5-parity-dropped ===            (`cell.count('"') % 2` short-circuited off)
CASE quote-absent-refused FAIL
SELFTEST cases=14 failed=1
=== m6-quote-side-unormed ===        (`needle = quote`, artifact still normalised)
CASE quote-located-accepted FAIL
SELFTEST cases=14 failed=1
=== m7-cap-ignored ===               (cap branch never taken)
CASE quote-overlong-refused FAIL
SELFTEST cases=14 failed=1
```

Each of the four cases dies to at least one semantic mutant: overlong ← m0/m2/m7, absent ← m0/m3/m5,
located ← m0/m3/m4/m6, boundary ← m0/m1. No mutant survives the suite.

## 5. Existing surface unchanged — old vs new on every existing invocation

Same invocation, both bodies, stdout+stderr+exit compared (`cmp`), run from the lane root;
`PKG=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read-only):

```
strict-package             IDENTICAL exit=3
scoped-package             DIFFERS old_exit=2 new_exit=2
admit-build                IDENTICAL exit=5
self-collision             IDENTICAL exit=3
usage-no-package           DIFFERS old_exit=2 new_exit=2
admit-ids-no-date          IDENTICAL exit=3
help                       DIFFERS old_exit=0 new_exit=0
```

- `strict-package` = `--registry corpus/SOURCES.md --package $PKG`
- `scoped-package` = `… --scope-to-admit --admit-ids S081,S082,S083,S084,S085,S086`
- `admit-build` = the scoped run plus `--access-date 2026-10-25 --entries corpus/knowledge/contamination-transparency-card.md`
- `admit-ids-no-date` = `--admit-ids S081` without `--access-date` (the parser.error path)

The three `DIFFERS` are **stdout-identical and exit-identical**; the only difference is argparse's usage
synopsis, which must enumerate the two new options:

```
--- stderr diff (scoped-package; identical shape for usage-no-package and help)
<                         [--recheck RECHECK] [--out OUT] [--attest-opened]
<                         [--scope-to-admit]
>                         [--recheck RECHECK] [--out OUT]
>                         [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
>                         [--attest-opened] [--scope-to-admit]
```

Selftest tally before/after — the only intended change: 10 → 14, cases 1–10 byte-identical.

```
11c11,15
< SELFTEST cases=10 failed=0
---
> CASE quote-overlong-refused PASS
> CASE quote-absent-refused PASS
> CASE quote-located-accepted PASS
> CASE quote-boundary-25-accepted PASS
> SELFTEST cases=14 failed=0
```

## 6. The mode on real lane bytes (not fixtures)

Artifacts are committed lane files read in place; the quote files under `/tmp/r30-GateQuote/real/` were
generated from those same bytes (`assert quote in text` before writing, so nothing is paraphrased):

```
=== 1 accept (file artifact) ===
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=attrib-calibration-summary.txt
  ok S901 words=5 at attrib-calibration-summary.txt quote="correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0"
EXIT=0

=== 2 accept (directory artifact) ===
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=attrib-calibration-selftest-v2.txt,attrib-calibration-selftest.txt,attrib-calibration-summary-v2.txt,attrib-calibration-summary.txt,attrib-oracle-intervals.txt,revert-test.txt,round25-census-after.txt,round25-census-before-6180e4f.txt,state-check-after-v2.txt,state-check-after.txt,state-check-before-6180e4f-v2.txt,state-check-before-6180e4f.txt,state-check-selftest-v2.txt,state-check-selftest.txt
  ok S901 words=5 at attrib-calibration-summary.txt quote="correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0"
EXIT=0

=== 3 over-long (26 words, present in bytes) ===
QUOTE rows=1 spans=1 located=0 found=1 overlong=1 absent=0 malformed=0 cap=25 artifacts=r12-report-final.md
  REFUSED S902 overlong words=26 cap=25 at r12-report-final.md quote="Committed gate at the pre-round HEAD `f09ff1f`: **1711 lines**, `python3 grader.py` → `CHECKS n=280 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0; `--selftest` → 7 scenarios S0–S6 `ALL"
EXIT=6

=== 4 absent from artifact ===
QUOTE rows=1 spans=1 located=0 found=0 overlong=0 absent=1 malformed=0 cap=25 artifacts=attrib-calibration-summary.txt
  REFUSED S903 absent words=5 quote="correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0Z"
EXIT=7

=== 5 mixed: 6 wins over 7 ===
QUOTE rows=2 spans=2 located=0 found=1 overlong=1 absent=1 malformed=0 cap=25 artifacts=r12-report-final.md
  REFUSED S902 overlong words=26 cap=25 at r12-report-final.md quote="Committed gate at the pre-round HEAD `f09ff1f`: **1711 lines**, `python3 grader.py` → `CHECKS n=280 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0; `--selftest` → 7 scenarios S0–S6 `ALL"
  REFUSED S903 absent words=10 quote="a paraphrase that the capture does not contain at all"
EXIT=6

=== 6 unreadable artifact ===
QUOTE cap=25 problem=--artifact names no file or directory: /tmp/r30-GateQuote/nope.txt
EXIT=2

=== 7 only --quote-file ===
usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]
                        [--package PACKAGE] [--admit-ids ADMIT_IDS]
                        [--entries ENTRIES] [--access-date ACCESS_DATE]
                        [--recheck RECHECK] [--out OUT]
                        [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
                        [--attest-opened] [--scope-to-admit]
sources_adopt.py: error: --quote-file and --artifact must be given together
EXIT=2
```

Run 3 is the important one: `found=1 located=0 overlong=1` prints `at r12-report-final.md`, i.e. the
refusal names the reason a reader must fix.

A live anchor cell, extracted from `corpus/SOURCES.md` and run with `SOURCES.md` as the artifact —
a **cell-shape receipt only** (self-referential, so it proves the parser meets the registry's real
format, not that S078's source says what the row claims):

```
QUOTE rows=1 spans=2 located=2 found=2 overlong=0 absent=0 malformed=0 cap=25 artifacts=SOURCES.md
  ok S078 words=8 at SOURCES.md quote="731 -> 642 tasks: 89 dropped after review."
  ok S078 words=8 at SOURCES.md quote="The verifier never runs in the agent's sandbox."
EXIT=0
```

Both spans count **8 words**, matching the lane's own `(8 words)` annotations in that cell and the pricing
D3 re-derives — the counter agrees with the corpus on a real row.

## 7. Risks and limits (stated, not hidden)

- **A green here is presence, not truth.** The gate proves bytes occur in the artifact it is handed. If a
  caller points `--artifact` at a lane receipt instead of the fetched source, the gate greens the lane's
  own copy — the laundering loop QUALITY Q5 forbids. The mode cannot detect that; the report line prints
  the artifact name (`at SOURCES.md` above) so a reviewer can see where the bytes came from. Section 6's
  run 8 is labelled a shape receipt for exactly this reason.
- **The cap is per span, not per row.** An anchor cell carrying three quotes has three checks; there is no
  aggregate word budget, which is what the contract states and what the live S078 cell needs.
- **Multi-span rows report one row id per span** (`located=["S017","S017"]`), so `spans` and
  `len(located)` agree; a caller counting rows should use `rows=`.
- **Word splitting is whitespace only** (tabs, NBSP, em-dash all part of tokens). `731 -> 642` counts as 8
  words including the arrow, consistent with `round30_defects.words`; a stricter linguistic counter would
  move counts the lane has already priced in receipts.
- **The lane file is untouched**: this round's C3 predicate runs `python3 plans/sources_adopt.py
  --selftest`; that command prints `cases=10` on the live lane until the parent integrates
  `/tmp/r30-GateQuote/sources_adopt.py` over it. Deliberate — my bound is scratch-only plus this report.
- Tool installs: none needed (python3 3.x stdlib only); no pacman transaction attempted.

## 8. Files

| path | role |
|---|---|
| `/tmp/r30-GateQuote/sources_adopt.py` | the extended gate (deliverable), sha256 `f26ed9bb94086e9e9a7c3d7812608870e3fd1de441d5fe10fcff380f7b14609d` |
| `/tmp/r30-GateQuote/red_probe.py` | runs the four new cases against any body, sha256 `5921a0b9bfe2d923a2d420c47ff19e34da96cffa58cf4bc7b26a9ba99d991033` |
| `/tmp/r30-GateQuote/mut/m*.py` | the eight mutants of section 4 |
| `/tmp/r30-GateQuote/real/quotes-*.txt` | quote files built from committed lane bytes (section 6) |
| `.ufo/waves/round-30/build/R30GateQuote.md` | this report (only lane write) |

Checks the parent should run after integration: `python3 plans/sources_adopt.py --selftest`
(expect `cases=14 failed=0`, exit 0), `python3 /tmp/r30-GateQuote/red_probe.py plans/sources_adopt.py`
(expect 0 failures), and one quote-mode invocation over a real capture to confirm the artifact path
resolves from the lane root.
