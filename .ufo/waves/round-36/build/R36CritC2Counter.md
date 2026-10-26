# R36CritC2Counter — C2 counter falsified: a zero-knowledge package scores defects=0

Seat: critic (wave 1, round 36). Target: `plans/round36_c2_verify.py` (digest at scoring time
`983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120`), frozen claims
`plans/round-36-claims.md` (`3241b86`, Amendment 1 `acbda2f`).
Every number below was produced in a fixture clone
`D=$(mktemp -d /tmp/k36cc2-XXXX); git clone -q --no-checkout --shared <lane> $D/lane;
git -C $D/lane sparse-checkout set --no-cone /corpus /plans; git -C $D/lane checkout -q master`
(`git -C $D/lane rev-parse --show-toplevel` = `/tmp/k36cc2-x6Y0/lane`); fixture removed at the end.
Copies of every artefact: `.ufo/waves/round-36/build/R36CritC2Counter/`.

## Decisive counterexample

A package with **1 new 110-word file, 3 registry rows whose scope/anchor are the literal string
`x` and whose `teaches` cells are word salad, a 1-word README index description and a bare-path
coverage bullet** — and whose entry states **nothing at all about the grader** — scores:

```
$ python3 plans/round36_c2_verify.py --lane .      (fixture clone, master + the junk package)
W1 ok
W2 ok
W3 ok
W4 ok
W5 ok
W6 ok
checks=6 defects=0
PREDICATE C2 pass
exit=0
```
(`P1-zero-findings.txt`, reproduced at the end as `P1-frozen-final.txt` after the other variants.)

That is the acceptance bar in the ticket (`checks=6 defects=0` for a junk package) met with room to
spare: not one of the receipt's headline findings — leading-zero octets permitted, digit-adjacent
dates unobserved, 5/other-width years unobserved, month-length validity outside the expected set,
Feb 29 permitting side unobserved, and the literal-alternation shortcut that the probe *observed
passing* (`hardcoded-expected-dates`) — appears in the entry, and none is required to.

### Exact bytes of the cheapest package

Entry `corpus/knowledge/tb2-regex-log-grader.md` (110 words, sha256
`50f8c68fd81c1f2ad65d0552b7bcd3087e239c4326fe71395b7ff32687700b7c`, copy
`entry-P1-junk.md`):

```
source: S108 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py
source: S109 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh
source: S110 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md
verified-at: 2026-10-25
recheck: 30d

# regex-log grader

cases=24 observed_pass=8 observed_fail=16 mismatches=0

## Negative space

Something could falsify this.

## Located quotes

| n | quote | where |
|---|---|---|
| 1 | “Write a regex” | `instruction.md:1` |
| 2 | “a regex expression” | `instruction.md:1-2` |
| 3 | “regex expression that” | `instruction.md:1-3` |
| 4 | “expression that matches” | `instruction.md:1-4` |
| 5 | “that matches dates” | `instruction.md:1-5` |
| 6 | “matches dates in” | `instruction.md:1-6` |
| 7 | “dates in the” | `instruction.md:1-7` |
| 8 | “in the format” | `instruction.md:1-8` |
```

Registry rows (`junk-package.diff`):

```
| S108 | regex-log grader tests/test_outputs.py — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py | code | A | x | x | alpha beta gamma delta epsilon zeta eta theta | mined | 2026-10-25 | 30d | corpus/knowledge/tb2-regex-log-grader.md |
| S109 | regex-log runner tests/test.sh — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh | code | A | x | x | one two three four five six seven eight | mined | 2026-10-25 | 30d | corpus/knowledge/tb2-regex-log-grader.md |
| S110 | regex-log instruction — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md | docs | A | x | x | red orange yellow green blue indigo violet black | mined | 2026-10-25 | 30d | corpus/knowledge/tb2-regex-log-grader.md |
```

README: `| \`knowledge/tb2-regex-log-grader.md\` | x | S108, S109, S110 |` and a coverage-map
bullet that is only `- knowledge/tb2-regex-log-grader.md`.

### Variant: an entry that contradicts the executed receipt — also defects=0

`entry-P2.md` adds exactly two sentences, both false against the receipt
(`hardcoded-expected-dates … observed=pass`, `ip-leading-zeros-allowed … observed=pass`):

```
The grader rejects a literal alternation of the nine expected dates, and it rejects
IPv4 octets that carry leading zeros. Neither claim is true of the executed probe.
```

`P2-contradicts-receipt.txt`: `checks=6 defects=0` / `PREDICATE C2 pass` / `exit=0`.
W5 compares bytes to a fresh probe run and then checks **only** that the entry contains the
summary string; it never reads the entry's claims. An admitted entry may therefore assert the
negation of its own instrument's output.

## W5's `match=NO` naming rule is dead code for this claim, and weak even if it fired

1. **Vacuous today.** The frozen receipt has zero lines matching the rule.
   `W5.num_matchNO_lines_in_receipt = 0 | cases flagged: []` (rule
   `re.match(r"case=(\S+) .* match=NO ", l)` applied to every line of
   `corpus/evidence/round36/regex-log-probe.txt`). With `mismatches=0` and a byte-pinned,
   deterministic probe, no case can ever need naming, so the rule cannot fail C2 — the
   "honest reporting" clause is unenforced. P1 exploits precisely this: it names no case.
2. **Trailing-space literal.** `match=NO ` (with the space) skips a line whose text ends at
   `match=NO`: rule applied to `case=y predicted=pass observed=fail match=NO` → `None`, while
   `… match=NO assertion='-' …` → `y`. The frozen probe always appends
   `assertion=…` (`plans/regex_log_probe.py:157`), so this hole is latent, not live — but it is
   one probe edit away from silently disabling the rule, and the probe is the thing whose digest
   is pinned, so nobody would re-read the rule.
3. **Containment anywhere.** The check is `name not in et` over the whole entry. A bare comma list
   (`invalid-regex, regex-file-absent`) satisfies it; so does pasting the receipt. There is no
   requirement that the name sit next to an observation or a verdict.

## W3's "≥8 distinct located lines" is actually "≥8 distinct `(file, start, end)` triples"

The frozen claims sentence (and the counter's docstring, W3) says *distinct located lines*. The
code collects `locs.add((fname, a, b))`. Evidence, on P1's entry:

```
rows 8 distinct_quotes 8 distinct_triples 8 distinct_lines 1 word_counts [3]
```

i.e. all eight quotes are three-word fragments of **instruction.md line 1**, and the eight
"locations" are `:1`, `:1-2`, …, `:1-8`. Control: collapsing the eight rows onto the identical
triple `instruction.md:1` fails —
`W3 DEFECT rows=8 distinct_quotes=8 distinct_locations=1 (want >=8 each)` (`C2-same-location.txt`).
So the token the code counts is the range end, not the line; an entry can quote one agent-facing
line of boilerplate eight times and pass a clause written to force eight locations. Note also that
nothing requires a single quote from `test_outputs.py` or `test.sh` — the two `code` rows — so an
entry can be built entirely from `instruction.md` and still pass W2/W3.

## Axes that DO hold (controls, so the finding is narrow)

| probe | result | file |
|---|---|---|
| capture byte-tampered, SHA256SUMS untouched | `W1 DEFECT listed digest mismatch or missing file: instruction.md` | in-report |
| capture tampered **and** SHA256SUMS rewritten to match | `W1 DEFECT instruction.md not listed at pinned digest` | in-report |
| summary line deleted from the entry | `W5 DEFECT entry does not carry the receipt summary line verbatim` | `C1-no-summary.txt` |
| 2-word quote | `W3 DEFECT quote of 2 words: the format` | `C3-two-word-quote.txt` |
| unparsed quote row | `W3 DEFECT unparsed quote row: …` | `C4-unparsed-row.txt` |
| `teaches` of 7 words | `W2 DEFECT S108 teaches has 7 words` | `C5-teaches-7-words.txt` |
| index row removed | `W4 DEFECT index row absent or missing S108/S109/S110` | `C7-no-index-row.txt` |

W1 and W5 defend the *bytes* (instrument, capture, receipt); W2/W3/W4 and W5's entry clause
defend only *shape*. Nothing defends the *knowledge*. This is the round-35 D1 failure mode
reappearing in the counter that was supposed to close it: the package is admitted for having the
right rows, not for having done the reading.

The frozen skip-control could not find this, and that is the sharpest part of the finding:
`claims/control-c2-skip.txt` reports `W2 teaches has 1 words`, `W3 quote of 1 words`,
`W5 fresh probe output differs from receipt`, `W6 census exit 1` — four *shape/byte* defects. It
was hardened along the axes it already failed. Raise every one of those four to a passing shape
(8-word filler teaches, 3-word fragments, the real probe, 43 index rows) and the control turns
green; the semantic axis was never probed.

## Smallest safe correction

**Do not patch the counter for this round.** `plans/round36_c2_verify.py` is a frozen instrument,
its digest is listed in the freeze block (`plans/round-36-claims.md:103`) and already drifted from
its frozen value (corroborating `R36RowsDraft`/`R36SkillDraft`: file is `983ed65c…`, block says
`f70e6d3a…`); editing it now repeats the Amendment-1 question the L0 queue already holds. The
correct wave-1 action is to record the limit: C2's predicate is a **shape validator**, and the
"frontier → core is covered" move rests on a package whose knowledge the instrument does not read.

For round 37, four clauses close it, in cost order (all satisfiable by the genuine package —
demonstrated, below):

1. **Findings must be stated.** For every receipt line with `observed=pass`, require the entry to
   name the case *and* contain its `requirement=…` text verbatim (8 cases at the frozen receipt;
   the receipt supplies the bytes, so the entry copies rather than invents). This is the clause
   that kills P1 and P2 and is the real content requirement: a permitting side observed by the
   probe is a finding, and the receipt's `mismatches=0` must not be the reason none is reported.
2. **Lines, not ranges.** Key W3 locations on `(file, first_line)` — implement the frozen sentence.
3. **`teaches` must touch its own source.** Require ≥2 distinct ≥4-char word tokens shared with
   that row's capture file, and the pinned commit sha in the `anchor` cell. Measured on the real
   capture text: `alpha beta gamma …` 0/7, `one two three four …` 0/5, `red orange yellow …` 0/7;
   a true sentence scores 6/9 (`the regex must select the last date on each IPv4-bearing log`).
4. **Prose floors.** README index description and coverage bullet ≥8 words besides the path
   (P1 uses `x` and a bare path).

Draft implementation and proof: `.ufo/waves/round-36/build/R36CritC2Counter/proposed_c2_addendum.py`
(imports the frozen counter, adds D1/D2/D3, touches no lane file).

```
P1 junk entry        : frozen checks=6 defects=0 | addendum D1+D2+D3 DEFECT, addendum_exit=1
P2 contradicting     : frozen checks=6 defects=0 | addendum 3 DEFECT, addendum_exit=1
P3 genuine-shaped    : frozen checks=6 defects=0 | addendum defects=0, exit=0
```
(`P1-addendum.txt`, `P2-addendum.txt`, `P3-frozen.txt`, `P3-addendum.txt`, entry copies
`entry-P1-junk.md`, `entry-P2.md`, `entry-P3-genuine-shaped.md`.) P3 is P1's shape with the eight
`observed=pass` requirement strings quoted, eight quotes on eight distinct capture lines, real
`teaches` cells and pin-bearing anchors — i.e. the correction costs the genuine entry nothing but
the transfer it is supposed to make.

## Impacted axes

- **Calibration** (the C2 claim's own axis): the frozen predicate is satisfiable without the work;
  P1 and P2 both give `defects=0`. The wave-1 C2 package can land green while a wave-2 mutation
  seat turns the entry into filler and still sees green.
- **Coverage**: "frontier → core" is asserted on an entry that may contain no claim about the
  grader. The counter cannot distinguish coverage from its row shell.
- **Provenance (minor, corroborative)**: the freeze block's digest for the counter
  (`f70e6d3a…`, `plans/round-36-claims.md:103`) does not match the file (`983ed65c…`); Amendment 1
  discloses the constant move but not that the instrument's own pin is now stale, so no check can
  tell a later tamper from the disclosed repair.

## What a judge should take from this

Not "the entry is wrong" — no entry exists yet at the tip (`corpus/knowledge/tb2-regex-log-grader.md`
absent; `grep -c "S10[89]\|S110" corpus/SOURCES.md` = 0). The finding is that *whatever* entry the
L1 lands, `defects=0` is not evidence that it carries the receipt's findings, that its quotes are
located on distinct lines, or that its `teaches` cells mean anything. The C2 predicate as frozen is
a green light for a shell.

VERDICT: cheapest-junk-c2-0-defects
