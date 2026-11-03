# ErrataBuild — R65-C2 correction artifacts (round 65, w1)

Seat ErrataBuild. Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; every path below is
lane-root-based (`kengaku-shokunin/...`) per Q47. No lane file was edited, no git mutation, no port,
no server, no network, no model, no install.

## Deliverables (in `.ufo/waves/round-65/w1/ErrataBuild/`)

| file | bytes | sha256 | shape |
|---|---|---|---|
| `erratum-round64-lesson.md` | 743 | `601f241f…4580f45` | `## Erratum (round 65)` block, token `R64-ERRATUM-65` once, dated 2026-11-03, 9 lines (limit 15) |
| `scorecard-correction.md` | 685 | `fbd9a1d2…3e5e051` | `### Round-64 correction (round 65, routed defect 2)`, addendum-classified wording, 8 lines (limit 12) |
| `quality-q47.md` | 700 | `7cee976d…383c2a` | `## Round65 criterion` + one bold `Q47 —` lead line + 4 supporting lines, lesson §7.3 |
| `kvstore-entry-addendum.md` | 577 | `c3daed6e…6759ded` | `## Citation addendum (round 65)`, S230 → S234 re-point, entry bytes above unchanged |

Receipts: `before-counters.txt` (red-before at base `12a62551`), `s234-checks.txt` (S234 validated at
HEAD `b5032ff8`), `landing-dryrun.txt` (append simulation + prefix checks + placement control),
`landing-notes.md` (append recipe and findings).

## Counter table (commands and observed values)

| frozen counter | target | before @ `12a62551` | after (dry-run append) |
|---|---|---|---|
| `git show <base>:corpus/SOURCES.md \| grep -c 'supersedes S230'` | 1 | 0 (rc 1) | 1 |
| `git show <base>:corpus/lessons/round-64.md \| grep -c 'R64-ERRATUM-65'` | 1 | 0 (rc 1) | 1 |
| `git show <base>:SCORECARD.md \| grep -c 'addendum-classified'` | ≥1 | 0 (rc 1) | 2 |
| `git show <base>:corpus/QUALITY.md \| grep -c 'Q47 —'` | 1 | 0 (rc 1) | 1 |

Base blob evidence: SOURCES `2f618fc9` 192299 B, round-64 lesson `a609c040` 13548 B, SCORECARD
`d118ebf5` 344735 B, QUALITY `5a2e88fd` 115160 B, kv-store entry 15034 B (all end 0x0A).
Dry-run prefix: the four files this seat appends keep the base bytes as an identical prefix
(`cmp -n <size>` rc 0). No filed byte is rewritten.

## S234 validation (`s234-checks.txt`, HEAD `b5032ff8`)

One S234 row, `NF=13` (11 census columns, no pipe inside cells), kind `code`, tier `A`, `teaches`
22 words, opens `supersedes S230 —`, anchor cell carries the verbatim line-96 f-string, status
`mined`, used-by `corpus/knowledge/tb2-kv-store-grpc-offline.md`; S230 row byte-identical from base
to HEAD; grader sha `115de2e9…` matches `SHA256SUMS` line 80. `PREDICATE S234-ROW pass`.

## Findings for the L1 (reported, not repaired)

1. **SCORECARD placement conflict.** The seat spec's "after the round-64 section, before the Planned
   (round 65) block" is an insertion at byte 343957 (line 2864) and breaks the frozen clause
   "SCORECARD.md keeps its base bytes as a byte-prefix" (`landing-dryrun.txt`, insertion control,
   `cmp` rc 1). EOF append is the only placement satisfying the frozen byte-prefix clause; the block
   heading keeps it findable. The L1 decides; this seat applied neither.
2. **SOURCES.md freeze insertion.** At HEAD the S232/S233/S234 rows are 3 insertions at byte 181788
   (line 248), before the trailing `## Paths` footer — 0 deletions, no filed byte rewritten, but the
   strict `12a62551` byte-prefix reading already fails at the freeze tip. Under the per-landing
   reading (base = freeze tip) SOURCES.md is untouched by the C2 repair and prefix-clean. The four
   counter targets are unaffected.
3. **No stitch risk from my artifacts:** all four are EOF appends after a 0x0A terminator, so the
   dry-run reproduces the landed after-values exactly.

## Risks / blockers

- The two findings above are L1 decisions, not seat edits; the C2 predicate's byte-prefix clause is
  the one clause this seat cannot make true for SCORECARD.md under the insertion placement and for
  SOURCES.md under the strict round-base reading.
- Nothing else blocked. Scratch `/fast/scratch/hyaku/kengaku-r65/ErrataBuild` removed after the
  receipts were copied into the seat dir.
