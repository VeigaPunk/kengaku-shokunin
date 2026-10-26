# R36MutC2W2W3 — mutation test of C2 checks W2/W3 (`plans/round36_c2_verify.py`)

Seat: R36MutC2W2W3 (mutation-tester, wave 1). Scope: W2 (SOURCES rows S108–S110) and W3 (entry
triad/negative-space/located-quotes) of the frozen C2 counter. Fixture-only work; no lane file
outside `.ufo/waves/round-36/build/R36MutC2W2W3*` was written.

## Instrument under test

`python3 plans/round36_c2_verify.py --lane .` (fixture copy of tip `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd`,
identical bytes to the live lane; `PROBE_SHA256` carries Amendment 1, `d58194c8…`). W6 runs the fleet
census in `--file` mode against the fixture registry, so a mutant can also be caught by census
E-codes — recorded below per mutant.

## Fixture (per the fixture rule)

```
D=$(mktemp -d /tmp/k36-XXXX)                      # → /tmp/k36-TgST
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/corpus/' '/plans/'
git -C "$D/lane" checkout -q master
git -C "$D/lane" rev-parse --show-toplevel        # → /tmp/k36-TgST/lane  (verified before any write)
```

Passing package installed on the committed tip:

- `corpus/SOURCES.md`: the three peer-drafted rows (`.ufo/waves/round-36/build/R36RowsDraft/rows-S108-S110.md`)
  inserted before `## Paths` (Registry section, after S107).
- `corpus/knowledge/tb2-regex-log-grader.md`: peer draft `.ufo/waves/round-36/build/R36EntryDraft/entry.md`.
- `corpus/README.md`: one index row `| \`knowledge/tb2-regex-log-grader.md\` | … (S108, S109, S110) |`
  after the round-35 TB2 row, one coverage-map bullet after the round-35 TB2 bullet (keeps
  knowledge-files == index rows at 43 ≥ 43; committed state was 42/42).
- `corpus/evidence/round36/` and `plans/` needed no copy: everything committed at `f9efce3`
  (`git -C <lane> status --porcelain` shows only `.ufo/waves/round-36/*` untracked).

Baseline (detector on pristine bytes, required green before any mutant):

```
W1 ok / W2 ok / W3 ok / W4 ok / W5 ok / W6 ok
checks=6 defects=0
PREDICATE C2 pass          exit=0
```

Harness: `mutate.py` (archived beside this report). Every replacement asserts `count(old)==1`; every
application is pre-sha ↔ post-sha checked against the pristine snapshot, so restoration is verified
per mutant, not assumed. Detector run after each restore and once at the end.

Pristine (package-installed) sha256:

```
6db92cbd827562b19ae22acdcdd07946d718d77e33b372d25c1d9b016f5b564e  corpus/SOURCES.md
9520b238dc176ad0f90af4713c82a0a51f26fc14d940d78b27efc0b85b3d2edd  corpus/knowledge/tb2-regex-log-grader.md
948d91743b2867f6e5082079f03f5e7f70b7c9cad7999e9758999a26028302dc  corpus/README.md
```

## Mutants

21 valid applications: the 20 tasked mutants (mutant 9 in its tasked form, 9a) plus one sharpening
variant (9b). Every "expected" below is the check the frozen claims' W2/W3 definitions imply.

| # | Mutant (target file) | Expected detector | Actual output (counter, exit) | Verdict |
|---|---|---|---|---|
| M01 | S108 row with 10 cells (recheck cell removed) | W2 cell count | `W2 DEFECT S108 has 10 cells` + `W6 DEFECT census exit 1` (E01), defects=2, exit 1 | killed |
| M02 | `\|` escaped inside S108 teaches cell (`… function \| single`) | W2 cell count | `W2 DEFECT S108 has 12 cells` + census E01, defects=2, exit 1 | killed |
| M03 | `/tasks/` segment in S108 URL | W2 exact pinned URL | `W2 DEFECT S108 source URL […/tasks/regex-log/tests/test_outputs.py'] != …/regex-log/tests/test_outputs.py`, defects=1, exit 1 | killed |
| M04 | `#L87` fragment appended to S108 URL | W2 exact pinned URL | `W2 DEFECT S108 source URL […test_outputs.py#L87'] != …test_outputs.py`, defects=1, exit 1 | killed |
| M05 | tier A→B on S108 | W2 tier/status | `W2 DEFECT S108 tier/status/opened = B/mined/2026-10-25`, defects=1, exit 1 | killed |
| M06 | status mined→queued on S108 | W2 tier/status | `W2 DEFECT S108 tier/status/opened = A/queued/2026-10-25`, defects=1, exit 1 | killed |
| M07 | used-by gains second existing path (`, corpus/knowledge/benchmark-grader-semantics.md`) | W2 used-by == entry exactly | `W2 DEFECT S108 used-by 'corpus/knowledge/tb2-regex-log-grader.md, corpus/knowledge/benchmark-grader-semantics.md'`, defects=1, exit 1 | killed |
| M08 | duplicate S108 row (verbatim copy, adjacent) | W2 presence count | `W2 DEFECT S108 present 2 times` + census E03, defects=2, exit 1 | killed |
| M09a | S108 row indented 4 spaces (only copy) | row invisible to census regex → W2 must defect via absence | `W2 DEFECT S108 present 0 times`, defects=1, exit 1; `ROW_RE sees indented row: False` | killed (by absence) |
| M09b | genuine S108 row + additional 4-space indented duplicate | (sharpening: does any check see the shadow copy?) | no defect line, `checks=6 defects=0`, exit 0 | **SURVIVED** |
| M10 | S109 teaches cell set to S108's teaches text | W2 pairwise-distinct teaches | `W2 DEFECT S109 teaches duplicates another row`, defects=1, exit 1 | killed |
| M11 | S110 teaches → 7 words (`four operating rules beyond matching: last date`) | W2 ≥8 words | `W2 DEFECT S110 teaches has 7 words`, defects=1, exit 1 | killed |
| M12 | quote citation off by one line (`test.sh:26`→`test.sh:27` for the echo-1 quote) | W3 verbatim-on-cited-line | `W3 DEFECT quote not on test.sh:27-27: echo 1 > /logs/verifier/reward.txt`, defects=1, exit 1 | killed |
| M13 | one changed char in quote (`echo 1`→`echo 2`, same cited line) | W3 verbatim | `W3 DEFECT quote not on test.sh:26-26: echo 2 > /logs/verifier/reward.txt`, defects=1, exit 1 | killed |
| M14 | quote exceeding the 25-word cap (spanning `test_outputs.py:10-11`) | W3 word cap | `W3 DEFECT quote of 30 words: Test that the agent created a file with`, defects=1, exit 1 | killed |
| M15 | 2-word quote (`“echo 1”` at `test.sh:26`) | W3 ≥3 words | `W3 DEFECT quote of 2 words: echo 1`, defects=1, exit 1 | killed |
| M16 | straight-quoted row (`"…"` instead of `“…”`) | W3 row must parse | `W3 DEFECT unparsed quote row: \| pass writes reward 1 \| "echo 1 > /logs/verifier/reward.txt`, defects=1, exit 1 | killed |
| M17 | all 29 quote rows replaced by copies of one quote | W3 ≥8 distinct quotes/locations | `W3 DEFECT rows=29 distinct_quotes=1 distinct_locations=1 (want >=8 each)`, defects=1, exit 1 | killed |
| M18 | falsifier removed (`Falsifier…falsified` → `Refuter…refuted`; section retains other text) | W3 negative-space falsifier | `W3 DEFECT negative space absent or has no falsifier`, defects=1, exit 1 | killed |
| M19 | `recheck:` without date/cadence (`180d` → `periodically`) | W3 recheck grammar | `W3 DEFECT line 5 recheck lacks date/cadence`, defects=1, exit 1 | killed |
| M20 | entry source lines 2 and 3 swapped (S109 ↔ S110) | W3 ordered source triad | `W3 DEFECT line 2 is not the S109 source line with its pinned URL`, defects=1, exit 1 | killed |

Restoration: every application's post-sha equals its pre-sha (harness asserts; 21/21 `restored=YES`).
Final restored run: `checks=6 defects=0`, `PREDICATE C2 pass`, exit 0; all three file sha256 equal the
pristine values above (verified after the last mutant and again after the M11 re-run, below).

## The survivor (false-green finding, coverage limit only)

**M09b — a second S108 row indented 4 spaces survives the whole counter (exit 0).**

- Mechanism: `ROW_RE = ^ {0,3}\|\s*(S\d{3,})\s*\|` (counter, line 47) sees only 0–3-space rows; the
  4-space copy is invisible to W2's presence census, so `len(got) == 1` still holds. W6 is blind to it
  too: the fleet census gawk only processes lines matching `^ {0,3}\|` (`sources-census.sh`, "0–3
  leading ASCII spaces …; 4 or more spaces are indented code and ignored"). Row count is unchanged:
  `sources-census.sh census --file` → `rows 103` on pristine and `rows 103` with the indented
  duplicate (exit 0 both). No E12 either — the outside-Registry scan runs after the same `^ {0,3}\|`
  filter.
- Interpretation: mechanically a survivor, but it does **not** violate the invariant under the
  fleet's *declared* parsing convention — an indented copy is indented code, not a registry row, in
  both the counter and the census contract (the convention is documented in the census script header,
  and exercised by its selftest at indent widths 0–3). It is a coverage finding for wave 2: a mutant
  cannot smuggle a second *census-visible* row (M08 proves that), but nothing counts raw S-lines, so
  an indented shadow row is green. Attackers should aim there; per the round rules this is reported
  as a limit, not repaired.
- Boundary note: a 1–3-space indent stays visible (M09a's complement); only ≥4 spaces vanishes.

## Disclosures (inconclusive first attempts, superseded)

- M11 was first applied with a mis-built replacement (`…last date wins` = 8 words) and passed green —
  that application tested nothing (the mutant did not violate ≥8 words) and is excluded from the
  tally; the corrected 7-word mutant kills (`W2 DEFECT S110 teaches has 7 words`). One restore slip in
  that manual re-run wrote a hex string into the fixture file; it was repaired by rebuilding the
  package deterministically and the sha256 re-verified equal to the pristine snapshot
  (`6db92cbd…`) with the counter green again before anything else was concluded.
- M14's harness label says "26-word"; the applied quote measures 30 words by the counter's own
  `len(quote.split())` (my hand count was wrong, the >25 violation class is what was exercised). The
  killed verdict is unaffected.

## Defense-in-depth notes (which layer caught what)

- W2's exact string equality on the pinned URL catches M03/M04; the census normalizes URLs
  (`url_of` strips fragments/trailing slash) and only compares within-lane duplicates, so census is
  fragment-blind — W2 is the load-bearing check there.
- M01/M02/M08 are double-covered (W2 message + census E01/E03); all other W2 mutants are caught by
  W2 alone (census accepts tier B/queued as enum-valid, and a used-by second path that exists on disk
  passes E11).
- Every W3 mutant is caught by W3 alone; the entry file is outside the census's surface.

## Cleanup

Fixture and harness lived under `/tmp/k36-TgST` (mktemp rule); `mutate.py` archived to
`.ufo/waves/round-36/build/R36MutC2W2W3/mutate.py`; fixture removed with `rm -rf /tmp/k36-TgST` after
the final restoration proof. No lane file outside this report and the seat scratch dir was written.

VERDICT: w2w3-mutants-20/21
