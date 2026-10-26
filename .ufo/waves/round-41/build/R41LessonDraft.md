# R41LessonDraft — draft `corpus/lessons/round-41.md` (kengaku round 41, wave 1, scribe)

Seat: leaf scribe, no subagents, no background jobs. Lane repo read-only; nothing written outside this report dir.
No tool installed or upgraded (no `pacman`, `uv`, `npm`, no `~/.local/bin` write); no scratch needed — every check
below is a read of committed bytes. No lane file, Git index, jj state, corpus/, plans/ or frozen artefact was touched.

Paste-ready draft: `.ufo/waves/round-41/build/R41LessonDraft/round-41.md` (14 063 B). Its `<L1 fill>` markers are the
numbers this seat cannot observe (wave-1 battery not yet installed; census-after not yet run).

## 1. Inputs read (all in full or at the cited ranges)

| input | what was taken |
|---|---|
| `plans/round-41-claims.md` (whole) | freeze commit `8ef8b4f`, first run `f774a87`; C1 23 mutants/13-10 floors; C2 25 cases; §Frontier mined mistake at `:118-121`; rider at `:122-123`; routed R1-R5 at `:124-129` |
| `corpus/lessons/round-40.md` (whole) | section order, table shape, error/errata style |
| `corpus/lessons/round-40-verifier-spotcheck.md` (whole) | §5 R1-R5, verbatim items |
| `.ufo/waves/round-41/claims/` — `control-c1-nothing.txt`, `control-c1-no-mutants.txt` (+ patch), `control-c1-tool-edited.txt`, `control-c1-hostile.txt`, `witness-run.txt`, `s10_equivalence.txt`/`.py`, `census-before.txt` | control outputs, exit codes, the S10 equivalence line, 15 `W04` |
| `plans/round41_c1_verify.py:1-123,500-651` | docstring rule, `TOTAL`/`FLOORS` (`:123-124`), `floors_ok` (`:640`), `--work` creation |
| `plans/round41_c2_verify.py` (grep `V8|order|--work|W04|mkdir`) | V8 exists; `--work` created (`:44-45,290`) |
| `corpus/evidence/round41/constraints-probe.txt` (whole) | `regrade cases=25 differ=0` (`:32`), `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (`:33`) |
| captures `test_outputs.py:1-113`, `instruction.md:1-30`, `SHA256SUMS` | located quotes, line numbers, digests |
| wave-1 build reports `R41PkgRows.md` (+`pr245-body.md`), `R41CritPytest.md`+`table.md`+`full-run{1,2}.txt`, `R41CritIndep/compare-out.txt`, `R41BatRcvCtl.md`, `R41BatSrcExit.md`, `R41BatRcvRun.md`, `R41SourcesRecheck.md`, `R41MergeRescreen.md`, `R41RegistryRows.md` | S124 live state, pytest parity, independent agreement, module declarations, assimilation id counts, drafted registry rows and the second-seat counter runs |
| `plans/round-40/falsify/F40CritPlanNext.md:1-40` | run A (`:30-33`), the four-line patch (`:36`) |

## 2. Behaviour — what the draft contains

- **`## Mistakes`** — four rows, each with class · evidence pointer · captured-by · fix, and an explicit statement of
  whether the fix is *shown able to fail*:
  1. **vacuous predicate** (the freeze's own mined mistake): round-40 run A `MUTANTS total=0 … PREDICATE C1 pass`,
     `exit=0` (`F40CritPlanNext.md:30-33`); captured-by none (`plans/round-41-claims.md:120`); fix = `TOTAL`/`FLOORS`
     binding, shown able to fail by `control-c1-no-mutants.txt` (`MUTANTS total=0`, `PREDICATE C1 fail`, `exit=1`,
     `BATTERY fixtures=22`). Noted that this control leaves `TOTAL = 23`, unlike round-40's attack which reset it.
  2. **S10 withdrawn as rc-equivalent** (`ref_rc=5 mut_rc=5 EQUIVALENT-BY-RC`), captured by the pre-freeze witness
     rule; the equivalence driver prints the pair, so the withdrawal is measured.
  3. **S124 "published" without its state** — the freeze calls PR #245 published; live `gh api` in wave 1 returns
     `state=closed merged=false closed_at=2026-10-08T19:02:36Z comments=0`, body `:7` "local draft only". Fix is
     wording only; **no counter reads the state word** — flagged as not machine-checked.
  4. **witness-as-battery loophole** — `control-c1-witness-as-battery.txt` passes the predicate with copied witness
     modules, so a kill counts a result difference, not authorship; fix is rule + review, no automated check.
- **`## Gate`** — seven rows. S122 and S123 admitted (mined, tier A) with the L1's open time 15:19 -03 and the
  15:36:45 cmp-identical re-fetch; S124 admitted (mined, tier B) **as a closed, unmerged proposal** — the assignment's
  "S124 pending" is superseded by the wave-1 live open at 15:37 -03; captures (solve.sh, test.sh, task.toml,
  Dockerfile, README.md, three calendars, SHA256SUMS) recorded as captured-not-rows; PR #245's 55-case adversarial
  suite refused as a row (no capture, no executed count); the `merge/kengaku` re-screen recorded as nothing adopted
  (collisions 38, S122-S124 already staged); the four drift-risk SOURCES rows re-opened with no status change. Every
  row carries a flip condition.
- **`## Routed`** — R1-R5 from round-40 §5, each with this round's disposition: R1 addressed by the new counter
  (bindings, sandbox, hostile control), predicate still unmeasured at draft; R2 landed as rule + enforced; R3 **drafted**
  by `R41RegistryRows` (four rows + addendum, not applied; the 6-defect/8-mutant pricing explicitly deferred by that
  seat as falsify-wave work); R4 adopted (`ADVERTISED direct=21 indirect=2 none=0`); R5 split per item, including the
  three residuals with no owner (F39LedgerTip D1, F39MutDirection, F39OrderGateMut fail-open), the `--work` fix in the
  round-41 counters only, and `round_close.py --round 41` green at tip. One new round-42 item proposed: a schema check
  that a tier-B PR row carries its live state word, because S124's state is prose today.
- **`## Census`** — command, before-state (exit 0, `kengaku ok`, 15 `W04`), and the E11 coupling: rows S122-S124
  cannot be green until the knowledge entry lands, so entry + rows must be one commit (`R41PkgRows.md` §4a).
- **`## Falsifiers run in wave 1`** — the two outside checks on C2: real pytest parity `75/75` per test on 25/25
  cases with two identical passes and a negative control, and the independent slot model `AGREE 25/25 disagree=0`
  plus three extra cases. Labelled as other seats' reports, not re-run by this seat.

## 3. Quotes used (≤25 words, located)

| row | location | quote | words |
|---|---|---|---|
| S122 | `test_outputs.py:143` | `assert not any(_overlap(s, e, cal) for cal in (A, B, C))` | 11 (the `sources_adopt` counter's own count, `R41PkgRows.md` §4b) |
| S123 | `instruction.md:18` | `Any modification will cause the tests to fail.` | 8 (same counter) |
| S124 | `pr245-body.md:11` | `the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar` | 14 (same counter) |
| refused row | `pr245-body.md:30` | `The patch adds 55 adversarial calendar fixtures, each of which runs all three native verifier checks.` | 16 (counted here) |

Evidence commands: `grep -n …` on the captures for the line numbers; `cat SHA256SUMS` →
`1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1  test_outputs.py`,
`342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6  instruction.md` (`cmp`-identical re-fetch and
the live PR state are `R41PkgRows.md` §2/§3, not this seat's runs).

## 4. Findings this seat adds (beyond assembling the freeze)

1. **S124's state is the freeze's one factual correction.** `plans/round-41-claims.md:21-22,105` call the decoy
   finding "published (TB2.1 PR #245)"; the PR is closed, unmerged, 0 comments, and its body says "local draft only;
   do not submit without owner authorization" (`pr245-body.md:7`). The draft's Gate row states "closed unmerged
   proposal" and forbids the entry from reading it as a landed fix. This is a wording class no check catches.
2. **The no-mutants control is stronger than the round-40 attack it answers.** `control-c1-no-mutants.patch` appends
   only `MUTANTS = []` and leaves `TOTAL = 23`; the failure therefore comes from `len(MUTANTS) == TOTAL` /
   `floors_ok` / `killed == TOTAL` (`plans/round41_c1_verify.py:640`), not from a re-set literal. A counter whose
   literal can be edited alongside the list is still visible to the closure through the counter's own digest
   (docstring, non-vacuity paragraph), but this control shows the cheap edit does not green it.
3. **The predicate's own reachability control documents a loophole.** `control-c1-witness-as-battery.txt` reaches
   `PREDICATE C1 pass` with the pre-freeze witness modules in `plans/battery41`, so the battery rule and non-author
   review are load-bearing, not decorative. Recorded as a mistake row with "no automated check".
4. **The frozen predicate still does not bind the fixture count** (`BATTERY fixtures=<n>`). That is defensible (the
   binding that matters is per-mutant floors), but it means a future battery can shrink without a red line; noted in
   the draft only as part of the loophole row's reasoning, not as a defect claim.
5. **The C2 rows also collide with the assimilation staging.** `R41MergeRescreen` measured `collisions=38`
   (round-40: 37; the addition is S121), and the staged package already holds S122/S123/S124, so landing the three
   C2 rows raises collisions to 41 and gives the staged card entry `benchmark-card-field-schema-2026-10-23` three
   colliding ids. The lesson's Gate records this as the assimilation row and states the floor: any later staged-row
   adoption renumbers past S124. `R41MergeRescreen` adopted nothing and the package is byte-identical to round 40.
6. **Draft-time dispositions are now measured where a seat landed.** `R41RegistryRows` (written at 15:44, after this
   seat's first read of the dir) confirms the C1 before-state a second time (`fixtures=0`, `survived=23`, exit 1) and
   shows the C2 counter's four defects are entry-shaped (`P3/P4/P7`, `P6`, `P8`) with the probe leg green
   (`P10 ok probe_rerun=byte-equal bytes=5775`). The draft cites those, and still leaves `killed=23` and the
   census-after numbers to the L1, because no battery exists in the lane.

## 5. Touched surfaces

| path | action |
|---|---|
| `.ufo/waves/round-41/build/R41LessonDraft/round-41.md` | created — the draft lesson (paste-ready, `<L1 fill>` markers) |
| `.ufo/waves/round-41/build/R41LessonDraft.md` | created — this report |
| `/fast/scratch/hyaku/kengaku-r41/R41LessonDraft/` | not created (no clone, no fixture; read-only seat) |

Nothing written to `corpus/lessons/`, `corpus/SOURCES.md`, `README.md`, `SKILL.md`, `plans/`, any frozen artefact, the
lane's Git index or jj state, the fleet root, `~/.local/bin`, `/usr`, `/etc`, `$HOME`, or `/tmp`.

## 6. Out of scope

- Not editing `corpus/lessons/round-41.md` itself — the L1 integrates.
- Not running the C1 counter, the C2 counter or any battery (no verification is this seat's job; also
  `plans/battery41` does not exist yet).
- Not opening S122/S123/S124 (done by the L1 and `R41PkgRows`); not re-running the probe or the pytest parity seat.
- Not filling numbers that require wave-1 or wave-2 runs: battery fixture count, `killed=23` line, census-after
  (`W04` count and registry-row count), README index/coverage numbers, PROVINCE paragraph.

## 7. Known limits of this draft

- Quotes are copied from the captures and their word counts from `sources_adopt.py`'s `QUOTE` lines (S122/S123/S124)
  or counted here (the 55-case line); this seat did not re-run `sources_adopt.py`.
- S124's live state is cited from `R41PkgRows.md` §3 (the seat's `gh api` output), not fetched again by this seat; the
  body capture header (`pr245-body.md:3`) matches it.
- The draft's pytest-parity and independent-model numbers are other seats' receipts; a re-run inside the wave-2 scope
  would be the place to confirm them.
- `corpus/lessons/round-40.md` uses an `## Errata` section for wave-2; the draft leaves that to the L1 (marker
  present in `## Mistakes`).

VERDICT: lesson-drafted
