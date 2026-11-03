# Round 65 w1 — seat LessonDraft (lesson skeleton + README index rows)

Seat: `LessonDraft`, leaf member (no subagent dispatch). Scope: draft only — the L1 integrates.
Claims of record: `plans/round-65-claims.md`, read in full (base `12a6255170bcc466029bf82037885fd69e20370f`).
Tools installed or upgraded: **none** (no pacman, no uv install, no binary download; every tool needed
was already present: `gcc`/`gcov` 16.2.1, `bwrap` 0.13.1, `/usr/bin/python3` 3.14.8, `sqlite3` 3.54.0).
Network opened: **none** by this seat (read-only over committed bytes; the two named opens belong to
`GraderRecon`). No port bound. No git mutation (read-only `log`/`show`/`ls-files`-grade reads only).

## Files written

| path | what it is |
|---|---|
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/LessonDraft/round-65.md` | the lesson the L1 lands at `corpus/lessons/round-65.md` (skeleton: H1 + status block, `## Gate`, `## Mistakes`, `## Carried → closed / open`, `## Assimilation`) |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/LessonDraft/readme-index-rows.md` | the exact index rows to append to `corpus/README.md` (lesson row + knowledge row, with placement, a byte-exact alternative for the knowledge row, and optional round-65 evidence bullets) |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/LessonDraft/verification-receipt.txt` | the observed command/output receipt backing every quoted value in the two files above |

Scratch dir `/fast/scratch/hyaku/kengaku-r65/LessonDraft/` was created and removed; no receipt lived
only there.

## Behaviour (what the two files contain)

**`round-65.md`** — H1 `# Round 65 — <one-line thesis filled by the L1>`; a status block naming the
round, the date 2026-11-03, the base `12a62551`, the freeze `b5032ff8`, the claims-doc pointer
`plans/round-65-claims.md`, the 12-seat wave shape, and the two claims with their axes.

`## Gate` records, for EACH of S232 / S233 / S234, the URL, the access date 2026-11-03, and a ≤25-word
located quote with its location; then the four R65-C2 correction artifacts; then admitted/rejected
subsections with reasons; then the `spot-check result: (pending outside verifier)` placeholder; then a
no-bind observation and the host facts re-measured at this seat.

`## Mistakes` is a one-line instruction placeholder for the L1 in the four-cell shape
`class . evidence pointer . captured-by . fix`, with the instruction that a defect no seat observed is
not a row. `## Carried → closed / open` and `## Assimilation` are L1 placeholders (the L0 questions to
carry are named in the placeholder text so the L1 does not have to re-derive them).

**`readme-index-rows.md`** — one lesson row (2-cell form, matching the existing round-64 lesson row's
shape in the `## Round29 supporting artifacts` table) and one knowledge row (3-cell form matching the
`## What's here` table header, with the source/probe/receipt cell). The knowledge row is offered in
two byte-exact forms with an explicit "choose ONE, not both" instruction: the 3-cell form matching the
table header and 59 of the 63 knowledge rows, or the 2-cell form matching the two most recent rows
(round-63, round-64). Two optional round-65 evidence bullets mirror the round-64 landing's
`### Round-63 evidence` bullets, with lane-root-based paths (the form QUALITY Q47 requires).

## The Gate quote lines (the values the L1 must be able to verify)

```
S232  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-with-gcov/tests/test_outputs.py   accessed 2026-11-03
      "No .gcda files found, gcov instrumentation may not be enabled"   (line 51, 10 words)
      "sqlite3 not found in PATH"                                        (line 25,  5 words)
S233  https://sqlite.org/2026/sqlite-amalgamation-3540100.zip            accessed 2026-11-03
      "sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h"                      (unzip -l, 4 words)
S234  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py   accessed 2026-11-03
      assert result == 0, f"Port {port} is not listening - no real gRPC server is running"   (line 96, 16 words)
```

Every quote is corroborated at this seat against committed bytes: the S232 fragments appear in
`corpus/evidence/round65/g2-capture.txt` (`sqlite3 not found in PATH`), `g4-capture.txt`
(`No .gcno files found`) and `g5-capture.txt` (`No .gcda files found`); the S233 four-file layout in
`unzip -l` of the wave's zip; the S234 f-string at line 96 of the committed kv-store-grpc capture.
Shas re-verified: grader `b165f850…2993b` (S232), zip `0a9c8e34…ad1f9` (S233), kv-store grader
`115de2e9…b1b0e` (S234).

## Gates

- **Write scope respected.** Only the seat dir `.ufo/waves/round-65/w1/LessonDraft/` (three files)
  and the scratch dir were written; `corpus/README.md`, `corpus/lessons/`, `corpus/SOURCES.md`,
  `SCORECARD.md` and `corpus/QUALITY.md` were read only. No `git add/commit/stash/checkout/reset/pull/push/fetch`,
  no mutating `jj`. No fleet-root tracked file touched. No `.scratch/`, `MANIFEST.json`,
  `.ufo/state/`, `.ufo/watchdog.log` or `shokuknow` access.
- **Frozen claims untouched.** No predicate, counter, kill rule, frozen vector or control was changed;
  the claims doc was read, not edited. The lesson quotes the frozen vectors and the frozen C2 counters
  verbatim from it.
- **No port bound; no model passed; no `ask` tool; no polling** (every command was a single bounded
  read).
- **Network** — none opened by this seat; the two named opens belong to `GraderRecon`, whose receipts
  are consistent with the shas re-verified here.

## Findings (for the L1 and the judge)

1. **The two most recent knowledge index rows are 2-cell in a 3-column table.** `corpus/README.md`
   lines 90 and 91 (`knowledge/tb2-network-service-offline-grader.md`,
   `knowledge/tb2-kv-store-grpc-offline.md`) carry only `| Entry | Covers |`, while the `## What's here`
   table header is `| Entry | Covers | Primary source |` and 59 of the 63 knowledge rows use all three
   cells. The lesson row for round 64 (line 552) is likewise 2-cell inside the `## Round29 supporting
   artifacts` table, whose header is `| Path | Covers |`. This seat does not repair either (append-only
   rule, and it is the L1's file); it hands the L1 both byte-exact forms of the new knowledge row and
   states that exactly one is to be appended. Flagging it because the same 2-cell drift is what the
   round-64 lesson's own Gate rows are graded against.
2. **The C2 counters are uneven at the freeze tip.** Observed at `b5032ff8` (the freeze landing):
   `grep -c 'supersedes S230' corpus/SOURCES.md` → **1** (S234 already landed at the freeze, exactly as
   the claims doc states), while `R64-ERRATUM-65` → 0, `addendum-classified` → 0, `Q47 —` → 0. The
   claims doc's own red-before receipt records all four at 0 at base `12a62551`. The three remaining
   counters are what the round-65 wave must move; the first is already satisfied by the freeze and must
   NOT be double-counted as a wave deliverable. Recorded in the seat receipt.
3. **The lesson skeleton deliberately asserts no predicate verdict.** The knowledge index row states
   the frozen vectors and the three captured fragments (both already frozen or already measured) and
   leaves the measured predicate string for the L1 to paste, mirroring how the round-64 row carries
   `PREDICATE R64-C1 pass`. The lesson's H1, verdict clause, `## Mistakes` rows, `## Carried → closed / open`
   and `## Assimilation` are all explicit L1 placeholders — a draft, not a claim of completion.
4. **A path-base convention is already fixed by the round-64 closure.** QUALITY Q47 (a round-65
   deliverable) requires wave-evidence paths to be lane-root-based; the optional round-65 evidence
   bullets this seat drafted use `corpus/…` and `.ufo/…` (lane-root-relative) form, and the index rows
   use the same form. The lane-root base is stated, per Q47's alternative.

## Out of scope (not done by this seat, deliberately)

- Landing `corpus/lessons/round-65.md`, the README rows, the S232/S233 status flip, the SCORECARD
  block and the QUALITY Q47 criterion — all are the L1's writes; this seat produced drafts only.
- Any edit to the frozen claims doc, the captures, the registry or the scoreboard.
- Any `## Mistakes` row content: mined from wave outcomes no seat has reported yet.
- Tooling installs: none needed, none performed (per the tooling authorization, no upgrade was
  required for this drafting task).
