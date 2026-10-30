# S5Connections — seat report (round 55, wave 1)

**Seat:** `S5Connections` — connector/scribe, leaf member, no subagent dispatch.
**Assignment:** draft the chess entry's **connections** and **limits** sections against the held
corpus, for seat `E7KnowledgeEntry` to consume.
**Date:** 2026-10-30. **Lane:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
base tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 freeze commit; base `798f5e9e`).

## Outcome

Delivered. The deliverable is
`.ufo/waves/round-55/w1/S5Connections/connections-and-limits.md` — three sections
(**connections**, **limits**, **class-boundary paragraph**), every claim tied to a named held
file in this lane repo. Nothing else in the lane was written by this seat; the lane tree was
read only, and **no mutating git/jj command was run anywhere**.

## What I ran (all read-only against the lane; exit codes as observed)

| command | exit | result |
|---|---|---|
| `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/{test_outputs.py,test.sh}` | 0 | `a540714e…b8f286` / `4770437e…6c334` — equal to the frozen pins in `plans/round-55-claims.md` §R55-C3 |
| `cmp corpus/evidence/round52/graders/chess-best-move/tests/test.sh corpus/evidence/round52/graders/regex-log/tests/test.sh` | 0 | **identical** — the runner-identity fact behind Amendment A1 and the S109 citation |
| `(cd .ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census && sha256sum -c SHA256SUMS)` | 0 | 107 lines, all `OK`; the 9 chess lines re-checked separately → all `OK` |
| `sha256sum …/f1-census/chess-best-move/{instruction.md,task.toml}` | 0 | `6ba25be4…19ce7a`, `d8f01d3c…2f9e` — the **same digests E14 fetched upstream** this round |
| `python3 -c "import importlib.util; …; round52_c1_grader_audit.classify(<chess capture>)"` | 0 | file class **V3** (content-check), single test **P3** (content/value) |
| `python3 .ufo/waves/round-55/w1/S5Connections/semdiff-class-boundary.py` | 0 | 16/16 r55 predictions reproduced; the r45-shape and r55-real shapes **disagree on 7 of 16** states; two incomparability witnesses printed |
| probe-module check: import `plans/round55_c3_chess_probe.py`, call its own `run_in_sandbox` on a missing-file and an empty-file case | 0 | missing → `('SETUP', 1)` (`FileNotFoundError`); empty → `('F', 1)` (`AssertionError`) |
| `sed -n`/`grep -n` citation sweeps over every file:line cited in the deliverable | 0 | all cited lines re-read and confirmed (see "Citation audit" below) |

Environment observed: `python3` 3.14.8, `bubblewrap` 0.13.1, lane `git status --porcelain`
= 14 lines (the wave's own in-flight files; **not** mine — I wrote only inside my wave dir).

## Files written

- `.ufo/waves/round-55/w1/S5Connections/connections-and-limits.md` — the deliverable
  (connections §1, limits §2, class boundary §3, open items §4, evidence table).
- `.ufo/waves/round-55/w1/S5Connections/semdiff-class-boundary.py` — the class-boundary probe
  (transcribes both graders' predicates from the committed captures; compares the two shapes
  over 16 byte-level states; reports the whitespace-separator set, the folding (non-)behaviour,
  the multiplicity semantics and the two witnesses).
- `.ufo/waves/round-55/w1/S5Connections/semdiff-class-boundary.out` — its output.
- `.ufo/waves/round-55/w1/S5Connections.md` — this report (Report: trailer path).
- `.ufo/waves/round-55/w1/S5Connections/report.md` — the contract's per-seat report path
  (same content).

## What the deliverable says (summary for the L1)

**Connections (§1)** — five one-line connections, each naming what the chess entry *extends* and
what it *never overwrites*, plus three "prior ground already held" items:

- r45 (`tb2-password-recovery-grader.md`) — same artefact kind, **different comparison relation**;
  r45's Predictor, receipt and its "second exemplar of the F1 constant-compare family" wording
  stay as written.
- r46 (`tb2-polyglot-c-py-grader.md`) — exemplar count 12→13; r46's dual-runtime class claim and
  its round-46 Errata (2 items) untouched; the chess grader executes nothing.
- `benchmark-verifier-execution-model.md` — runner semantics only, by citation of S109; the
  shared-mode / `/tests`-upload / log-scan readings are not re-derived or overwritten.
- `tb2-grader-vacuity-triage.md` (r52) — one of the 89 additionally read and executed; the
  triage's counts and its `not admitted` verdict untouched; the chess grader is **not** among
  the 29 candidates nor the 30 blind labels.
- `tb2-feal-linear-cryptanalysis-grader.md` (r44) — a contrast case, with a definitional
  overlap flagged for the L1 (§4 item 1).
- Prior ground: `.ufo/waves/round-44/wave/R44LabratF1Leak/receipts/chess-derive.txt` already
  derived `['e2e4','g2g4']` as the mating set; the round-45 attempt-1 tree already holds the
  whole chess task tree (digest-verified) incl. `instruction.md` at the S202 digest; the
  round-45 census spec already names `decide_lines: [25]` and the token pair.

**Limits (§2)** — the PROVINCE round-37-style refusal list (no Terminal-Bench run, no task
image, no harness run, no real submission, no task validation, no contamination, no model
behaviour, and the remaining TB2 graders), plus four entry-specific limits: no chess
correctness established; host python3 stands in for the image's python and pytest is not run;
the 12 frozen cases never exercise an absent or non-regular `/app/move.txt`; the probe is
offline and synthetic.

**Class boundary (§3)** — r45 line-split membership vs r55 full-multiset equality, on the four
named axes: **partial credit** (r45 grants it via `in`; r55 grants none), **order** (free in
both but purchased differently — r45's order-freedom also buys freedom over count, extras and
duplicates), **duplicates** (invisible to r45's membership; fatal to r55's sorted-list
equality), **normalization** (r45 tokenizes by line on `U+000A` after universal-newline
translation; r55 tokenizes by whitespace run over all 29 Unicode whitespace code points;
neither applies case, digit-width or Unicode folding). Consequence, measured: the two relations
are **incomparable** — neither implies the other.

## Defects found (reported, not fixed — all are other seats' or the L1's files)

0. **E7's entry landed independently while this seat was drafting, and it covers a strict
   subset of this draft.** `corpus/knowledge/tb2-chess-best-move-grader.md` (writer
   `E7KnowledgeEntry`) does not reference this seat's file. It is correct on everything it does
   cover — the two `## Connections` it names (benchmark-verifier-execution-model, r45), its
   5-property `## Mechanism` (all four boundary axes against the receipt rows), its 7-bullet
   `## Negative space`, and its `## Class note (the r45 distinction)`. **This seat did not and
   will not edit E7's file.** The per-item coverage delta is tabulated in the deliverable's §5.
   The four substantive gaps, for the L1 to decide on before admission:
   (a) no connection to **r46** (`tb2-polyglot-c-py-grader.md`) — nothing says the entry extends
   the executed-exemplar count 12→13 or leaves r46's dual-runtime class and its 2-item round-46
   Errata untouched (`grep -c polyglot` = 0);
   (b) no connection to the **r52 vacuity triage** — the entry does not record that its task is
   one of the triage's 89, is **not** among the 29 candidates nor the 30 blind labels, and
   carries the committed classifier's **V3 / P3** class, i.e. is not a presence-only grader
   (`grep -c triage\|vacuity` = 0);
   (c) no **prior ground** cited — the r44 derivation receipt that already computed
   `['e2e4','g2g4']`, the round-45 attempt-1 tree that already holds the whole chess task tree
   (digest-verified, `instruction.md` at the S202 digest), and the round-45 census spec that
   already names `decide_lines: [25]` (`grep -c R44LabratF1Leak\|attempt1\|f1-census` = 0);
   (d) no **limits item on the absent-file `SETUP` gap** — the only hit for
   `absent|missing|nop|FileNotFound|setup` in the entry is the word "missing" in the multiset
   sense; there is no `## Limits` section at all.
   Also absent from the entry: the **incomparability** consequence of the class boundary
   (neither relation implies the other) and the exact separator-set difference as a *named*
   difference. The refusal count (13 of 89 read) is correct in the entry's positive form.
1. **The seat brief's refusal count is stale.** It asked for "86 graders still unread", which
   is round 37's figure (`PROVINCE.md:277`: "remaining 86 … 3 are read"). At the round-55
   landing revision the correct figure is **76 remaining, 13 of 89 read** (`corpus/README.md:445`;
   the claim narrows "12 of 89 read" → "13 of 89"). The deliverable uses 76/13 and flags the
   discrepancy in its §4 item 3. (E7's landed entry independently got this right.)
2. **F1-family definitional overlap (ruling wanted).** r44 names the family "a constant compare
   that cannot tell how the constant was obtained" (`tb2-feal-linear-cryptanalysis-grader.md:78-80`)
   and r45 calls itself the family's *second* exemplar (`:17-18`). The chess grader also compares
   against embedded literals, but by exact multiset. The round-55 claim calls it a "graded
   artefact class new to this lane" and the landed README row calls it "distinct from round 45's
   line-split membership" (`corpus/README.md:84`). Under r44's own wording the chess grader is
   arguably F1-adjacent. The entry must state which reading it takes and must not silently
   reclassify r44 or r45. **I did not rule on this** — it is the L1's.
3. **Citation status of the round-45 attempt-1 tree.** It is git-tracked (113 files) and its
   digests verify (`sha256sum -c` → exit 0), but `corpus/lessons/round-45.md:4` designates
   `.ufo/waves/round-45/attempt1-unclaimed/` as *"discarded drafts"* from the aborted round-45
   attempt 1. Whether it is citable ground is an L1 decision; the deliverable says so and does
   not treat it as admitted.
4. **Case-table gap: an absent `/app/move.txt` is a probe SETUP, not a verdict.** The chess
   grader reads `/app/move.txt` at `tests/test_outputs.py:23` with no existence check of its
   own, so an absent file raises `FileNotFoundError` (a directory → `IsADirectoryError`); the
   frozen probe's classifier maps any nonzero exit without `AssertionError` to `SETUP`
   (`plans/round55_c3_chess_probe.py:126-130`), aborting the whole run with exit 2. Verified
   against the committed probe module: missing → `('SETUP', 1)`; empty → `('F', 1)`. The frozen
   12-case table has `empty-file` but **no** absent-file case, so r45's `nop` analogue does not
   exist in this round's evidence. If the L1 wants that case, the frozen table must be amended
   as data **before** the after-run.
5. **Two corrections I made to my own draft before landing** (recorded for audit): the receipt
   line for the joined-token state was mis-cited as `:11` — that state is not in the frozen
   table at all and is measured only in my own probe; and the probe classifier's line range was
   corrected from `:119-127` to `:126-130`.

## Citation audit

Every `file:line` in the deliverable was re-read after writing. Confirmed: r45 capture `:14`
and `:18`; chess capture `:23` and `:25`; chess `test.sh` `:25-28`; regex-log capture `:90`;
db-wal capture `:44` and `:89`; r45 entry `:17-18`; r44 entry `:78-80`; r46 entry's Errata
(2 items) and r45 entry's Errata (5 items); `PROVINCE.md:277`; `corpus/README.md:84` and `:445`;
`corpus/lessons/round-45.md:4`; `plans/round55_c3_chess_probe.py:7-16`, `:54-79`, `:126-130`;
`corpus/evidence/round55/chess-best-move-probe.txt:1-12`; the round-52 receipt's counts; the
chess `task.toml:29` and `:34`; `environment/make.py:118`.

## Dead ends

- The chess `instruction.md` is **not** in `corpus/evidence/round52/graders/chess-best-move/`
  (only `tests/test_outputs.py` and `tests/test.sh` are) — it is in the round-45 attempt-1 tree
  and upstream (E14 fetched it). Not a defect; noted in the deliverable.
- `.ufo/waves/round-44/wave/R44LabratF1Leak/der/derive_chess.py` is **not** in the tree (only
  its receipt is), so the derivation cannot be re-run from committed bytes; the receipt is cited
  as-is and the entry is told not to restate it as its own finding.

## Tooling

**No installs, no upgrades.** Everything used (`python3` 3.14.8, `bubblewrap` 0.13.1, `sha256sum`,
`cmp`, `grep`, `sed`) was already present. No network calls were made by this seat (the upstream
digests I cite are E14's and the round-52 capture's, both already recorded in the lane).

## Scratch

`/fast/scratch/hyaku/kengaku-r55/S5Connections/` was created for the two probes and **removed**
after the receipts were copied into `.ufo/waves/round-55/w1/S5Connections/`. Nothing of mine
remains outside my wave directory.
