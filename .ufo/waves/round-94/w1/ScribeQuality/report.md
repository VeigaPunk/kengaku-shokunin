# ScribeQuality — round 94, wave 1 (leaf scribe)

Seat ScribeQuality (scribe). Item: draft three texts (a `corpus/QUALITY.md` criterion, the
round-94 lesson `## Gate` block for S297–S302, and the `SKILL.md` gate-registry row for the
freeze-integrity gate) for the L1 to integrate. No subagents, no commits, no pushes, no lane
mutation.

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`. Read-only against the
lane throughout: `git rev-parse` / `log` / `show` / `cat-file` / `ls-tree` / `diff` /
`merge-base` only. Every execution ran from a scratch clone
(`/fast/scratch/hyaku/kengaku-r94/ScribeQuality/lane`, `git clone --shared`, detached at
`242b3669`; `git -C <clone> rev-parse --show-toplevel` equals that clone) or from a throwaway
fixture repo created with `mktemp -d` + `git init -q`, each committed with
`-c user.name=fixture -c user.email=fixture@invalid` after asserting
`git rev-parse --show-toplevel` prints the fixture dir. No tool installed or upgraded (pacman
is paused host-wide; nothing needed installing). No host sysctl touched.

## Deliverables (all under this seat's wave dir)

| file | what it is |
|---|---|
| `quality-criterion.md` | draft of a new `corpus/QUALITY.md` criterion (Q75) with the file's own style check and the measurements behind it |
| `lesson-gate.md` | draft of the round-94 lesson `## Gate` block for S297–S302, with the per-row source check |
| `skill-registry-row.md` | draft of the `SKILL.md` gate-registry row for freeze-integrity v2, column by column, with the sibling-overlap review of the L1's existing uncommitted row |
| `receipts/` | eight raw receipts (below) |

## What I verified (each receipt is a transcript of a real run)

1. **Gate v2 at the measured tip T.** `python3 plans/round94_freeze_integrity.py --lane . --freeze
   844c504e… --rev 90c7677f… --claims plans/round-94-claims.md --work DIR` → `SELFTEST cases=15
   ok=15`, `FREEZE-INTEGRITY instruments=11 intact=11 broken=0`, `PREDICATE freeze-integrity pass`,
   rc 0. (`receipts/receipt-gate-v2-at-T.txt`)
2. **The round-94 C2 counter at T.** `python3 plans/round94_c2_counter.py --lane . --rev
   90c7677f… --work DIR` → `W1 pass … W5 pass`, `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2
   pass`, rc 0; `W5 null ok fixtures_ok=12 of 12` and `W5 pass mutants=7 killed=7`. Matches the
   L1's committed `.ufo/waves/round-94/L1/c2-tip.txt` byte for byte on the lines that matter.
   (`receipts/receipt-c2-at-T.txt`)
3. **The five known false gates at T** (the three round-93 seat forgeries and the two surviving
   round-93 mutants), each run through the round-94 counter via `--tool-file`: every one ends
   `PREDICATE R94-C2 fail`, rc 1, and every one is RED at its own designated fixture. This is
   the "5 → 0" the claims file asserts, re-measured at the tip rather than at P1.
   (`receipts/receipt-false-gates-at-T.txt`)
4. **All six new SOURCES rows against the lane capture.** sha256, byte count, cited line, word
   count and quote-substring for each of S297–S302. All match except one word count — see
   SQ-1. (`receipts/receipt-sources-s297-s302.txt`)
5. **Every rc-2 path of gate v2**, twelve of them, each reproduced with its printed
   `DEFECT SETUP` line and exit code. (`receipts/receipt-rc2-causes.txt`)
6. **The `--work`-inside-the-lane behaviour** of gate v2, and that `--selftest` is not a flag
   it has. (`receipts/receipt-inlane-workdir.txt`)

## Findings

**SQ-1 (major, verdict-flipping for a standing lane gate — not for R94-C1/C2).** SOURCES row
S299's `(9 words)` cell is wrong; its quote has 10 whitespace tokens. The lane's own
anchor-line gate is therefore **red at the tip**: `python3 plans/anchor_line_check.py --lane .`
prints `ROW S299 state=live defects=words:1` and `ANCHORLINE … live=1 cells=1`, rc 1, where at
BASE (`0cbb9279`) it printed `live=0 cells=0`, rc 0. The admitted counter
`plans/round91_f1_counter.py --lane . --work DIR` flips with it: `PREDICATE R91-F1 pass`, rc 0
at BASE → `DEFECT FULL-CHECK rc=1 … live=1 cells=1`, `PREDICATE R91-F1 fail`, rc 1 at the tip.
The defect entered with this round's C commit `90c7677f`, which added S297–S302.
Exact commands and outputs are in `receipts/receipt-s299-wordcount.txt`.
**Effect on a verdict: neither R94-C1 nor R94-C2 is flipped.** Neither round-94 counter reads
`corpus/SOURCES.md` (`grep -n SOURCES plans/round94_{c1_replay,c2_counter,compressor_probe,freeze_integrity}.py`
→ no match), the defect is in no tabled instrument (the round-94 `frozen-instruments` table
lists only `plans/` instruments and the six `corpus/evidence/round94/graders/write-compressor/`
captures), and the fleet census `scripts/sources-census.sh validate` on the lane's registry
exits 0 (only the 30 pre-existing W04 duplicate-url warnings). Both counters were re-run at T
and pass. What is red is a standing lane gate and an admitted counter of record — a lane-hygiene
regression at the tip, and one the round's own source-verification obligation should have
caught before the C commit. The repair the lane's rules require is a **new superseding row**
(CORPUS rule 2; QUALITY Q34), not an in-place edit; I verified that path end-to-end in a scratch
clone — one row `S303` whose `teaches` cell opens `supersedes S299 —`, carrying the identical
quote with the count corrected to 10, takes the gate to `ROW S299 state=repaired by=S303`,
`live=0 cells=0`, rc 0 (`receipts/receipt-s299-supersede-repair.txt`). The lane has in-place
precedents (round-92 M1 at `d1ccf56d`; round-93 W-7), both of which are recorded as
corrections of the round's own rows; **the L1 decides, this seat does not repair.** Under the
frozen rule the correction lands in round 95, since no tabled instrument changes after F.

**SQ-2 (minor, sibling overlap).** The lane's working tree already carries an **uncommitted**
`freeze-integrity` row at `SKILL.md:698` and an uncommitted `freeze-integrity gate` capabilities
row in `SCORECARD.md` — written at 19:04:37, right after the w1 dispatch commit `d04e6664`
(19:04:13). The L1 is writing the SKILL.md registry row itself (the round-93 closure's carried
conformance items 1 and 2). My third deliverable is therefore a **review** of that row rather
than a competing draft; `skill-registry-row.md` lists five measured differences, of which the
substantive ones are (a) "printed on every run" is not literally true — the two rc-2 paths that
return before the battery print no `SELFTEST` line — and (b) the rc-2 cause list omits five
causes the code raises (`claims file … absent at freeze`, `malformed table row`, `no paths
given`, `duplicate --paths`, `rev-list failed`, plus argparse's usage exit). Neither changes a
verdict; both change what a reader of the registry is told the tool does. I did not touch
`SKILL.md` or `SCORECARD.md`.

**SQ-3 (minor, latent).** Gate v2 does not refuse a `--work` directory **inside** the lane,
unlike several other lane counters (e.g. `round38-c1`, `round42-c1`, whose registry rows say
"refused inside the lane"). Measured: `--work ./inlane` inside a lane clone runs green and
leaves an empty `inlane/` directory behind; `git status --porcelain` stays clean, so no tracked
byte changes. The registry row's write-scope cell should say so rather than claim "none in the
lane" unconditionally. (`receipts/receipt-inlane-workdir.txt`)

**SQ-4 (info).** The lesson `## Gate` block for S297–S302 has no home yet:
`corpus/lessons/round-94.md` does not exist at the tip. The L1 creates it; my draft is the
block to paste in.

## Out of scope for this seat

- No instrument was edited and no verdict was re-litigated. The C1/C2 claims are the L1's;
  this seat re-ran them only to check that SQ-1 does not touch them.
- The wave's other seats' areas (probe portability, mutation testing, the freeze census, the
  history census, the sibling-lane overlap survey) were not mine to duplicate.
- The round-92 gate defects the claims file carries forward (override vacuity
  `plans/round92_burndown.py:306-329`, the planted-marker skip at `:445`/`:558`, the unpinned
  round-92 counters, the unguarded `cost_model_for_tests.py`) are untouched and still open.
- `corpus/lessons/round-94.md` is the L1's to write.

## Honest limits of this seat's evidence

- The source checks are against the lane's **capture** (`corpus/evidence/round94/graders/write-compressor/`),
  whose sha256 values match the SOURCES rows and the frozen table. I did not re-fetch the six
  URLs from raw.githubusercontent.com; the rows' HTTP-200 access claims are the L1's, and my
  check confirms only that the captured bytes are what the rows say they are.
- The QUALITY criterion I draft asserts what a counter must show; it does not assert that any
  particular round's counter satisfies it. The round-94 counter does satisfy it as measured
  (SQ receipts 2 and 3), but the criterion is written to bind the next round's counter too.
- The `SKILL.md` row draft was reviewed against the committed file at `d04e6664`; the L1's
  uncommitted row may still change, and its final placement is the L1's call.
- SQ-1's severity depends on a judgement the L1 owns: whether a red `anchor-line-check` and a
  red `round91_f1_counter` at the tip count as a round-94 defect. I report the measurements;
  I do not assign the round's verdict.
