# R44RoutedPackage — routed package rows re-checked and drafted (kengaku round 44, wave 1)

Seat: scribe, leaf. Scope: the nine routed rows that hang off the `circuit-fibsqrt` package —
`R42-R3-02/05/06/07/08/09` (from `.ufo/waves/round-42/falsify/F42RevC2Package.md`) and `R42-R3-38/39/40`
(from `.ufo/waves/round-42/falsify/F42EntryQuotes.md`). Nothing frozen was touched: no tool, counter, probe,
spec, gate, dry table, capture, receipt or claims file was edited, and no lane file was written by this seat.

Every measurement is on a scratch clone of the committed tip. Drafts were applied **only inside that clone**
(`/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage/lane`), never in the lane; the lane's
`corpus/routed-findings.jsonl` is untouched and the drafted rows live in a separate file
(`R44RoutedPackage/draft-ledger-rows.jsonl`).

## 1. Identity and environment

- `git -C $S/lane rev-parse HEAD` → `5e3d3aa06c6b7000929ac3e62563a39159c4501f`; lane HEAD → the same;
  `git -C $S/lane status --porcelain` → 0 entries before any draft edit.
- Lane worktree (read-only to this seat) carried 4 untracked round-44 paths only at measurement time:
  `.ufo/waves/round-44/integrate/`, `wave.ready`, `wave.ready.partial`, `wave/` — no tracked file modified, so the
  clone equals the lane's committed state. After this seat's last run the lane gained `plans/battery44/` and
  `wave.ready.dispatched` from other seats' work; no tracked file is modified and none of it is this seat's.
- Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage`, `TMPDIR=$S`; receipts in
  `.ufo/waves/round-44/wave/R44RoutedPackage/` beside this report. Tools installed: none.

## 2. Baseline — all nine current `check`s run at the tip

Command: each row's `check` verbatim from `corpus/routed-findings.jsonl`, `cwd=$S/lane`.

| Row | current `check` (verbatim) | rc | baseline state |
|---|---|---|---|
| R42-R3-02 | `grep -q ':238' SKILL.md` | 1 | red; no `:238` anywhere in `SKILL.md` |
| R42-R3-05 | `grep -qF 'test_outputs.py:26-53' corpus/knowledge/tb2-circuit-fibsqrt-grader.md` | 1 | red; entry still says `:26-52` at `:350` |
| R42-R3-06 | `grep -qE 'S128 \((OpenAgents\|TB2\.1 issue\|issue)' corpus/README.md` | 1 | red; index row `:75` still files S128 as a TB2 artefact |
| R42-R3-07 | `! grep -qF 'equal to the receipt row' SKILL.md` | 1 | red; sentence at `SKILL.md:699` |
| R42-R3-08 | `! grep -qF 'biopython==1.85' plans/pkg_gate.py` | 1 | red; `plans/pkg_gate.py:276` |
| R42-R3-09 | *(none)* | n/a | uncheckable by construction (row says so) |
| R42-R3-38 | `grep -qE '^## Errata \(round 43' … && grep -qF ':297' …` | 1 | first clause 0, second 1 |
| R42-R3-39 | same shape, `:311` | 1 | first clause 0, second 1 |
| R42-R3-40 | same shape, `:431` | 1 | first clause 0, second 1 |

Ledger self-consistency at the tip (`python3 plans/routed_open.py --lane $S/lane --observe`, envelope §8):
`OBSERVE rows=60 mismatched=0`, `ROWS total=60 open=38 blocked=1 closed=21 refused=0`, `routed_open=39`.
The nine rows print `observed=fail self=open` (or `observed=n/a` for 09).

## 3. Each row re-checked against the tip and its entry rows

| Row | Claim at the tip | Evidence (measured this seat) |
|---|---|---|
| 02 | `SKILL.md:600` cites `(:178-184)` for both V4's and V7's `receipt or entry absent` | `def v4` at `plans/round42_c2_verify.py:178` (string `:184`), `def v7` at `:231` (string `:238`). Citation incomplete — claim holds |
| 05 | entry `:350` cites the helpers as `test_outputs.py:26-52` | capture: `def fibonacci` at `:26`, `isqrt`'s last statement `x = x_new` at `:53`, `:54` blank → span is `:26-53`; `SKILL.md:1205` already cites `:26-53` — claim holds |
| 06 | `README.md:75` sources cell = "S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)" | `corpus/SOURCES.md:143` S128 = "OpenAgents issue #9645 …", tier B; convention row `README.md:70` separates prior art ("; S114 (TB2.1 issue #133, prior report)"); README:272 and `PROVINCE.md:539` both label S128 prior art — claim holds |
| 07 | `SKILL.md:699` says V9 requires the case table "equal to the receipt row by row" | V9(a) matches `CASE_ROW` at `:84` over `(id, letters, observed)` and compares at `:298`; description cells differ (receipt:16 "padded with blank lines to 32000 lines (sim ignores blanks; the size test counts them)" vs entry:231 "padded to 32000 lines: the size test counts blanks") — claim holds |
| 08 | P10's fallback pins `biopython==1.85` though the probe is stdlib-only | `plans/pkg_gate.py:276`; `grep -n Bio plans/fibsqrt_probe.py` → no import (its only `pytest` mentions are prose at `:18`, `:19`, `:44`); `plans/pkg-spec-r44.json` `frozen_instruments` pins `plans/pkg_gate.py` `ea638822…` — claim holds, and the file is frozen this round |
| 09 | `:328` credits "pytest's cache" for writes the probe never makes | probe harness calls the three captured functions directly; no pytest import — claim holds |
| 38 | entry `:297` still reads "maximum, 48401 = 220²+1, is the only reach above 2^15" | unchanged in place (errata never edits the sentence, by the round-43 R1 rule) |
| 39 | entry `:311` still puts `stdin` on `/dev/null` "(probe docstring …)" | unchanged in place |
| 40 | entry `:431` still says both padded rows "too pass only because …" | unchanged in place |

## 4. What the round-43 errata already fixed — and why three checks stayed red

Measured, not inferred: the round-43 errata section exists (`entry:451`, `## Errata (round 43, closure R1 …)`),
and each of E1/E2/E3/E4 quotes the right sentence, but the headers cite **spans**:

| Row | Defect sentence | Round-43 handler | Header span | Check wants | Substance | Check |
|---|---|---|---|---|---|---|
| 38 | `:297` | E1 | `:296-298` | `:297` | fixed | red |
| 39 | `:311` | E2 | `:309-312` | `:311` | fixed | red |
| 40 | `:431` | E3 | `:430-432` | `:431` | fixed | red |
| — | `:433-434` | E4 | `:433-434` | `:433-434` | fixed | green (R42-R3-41 closed) |
| 05 | `:350` | none | — | `test_outputs.py:26-53` | **not fixed** | red |
| 09 | `:328` | none | — | none | **not fixed** | n/a |
| 02 | `SKILL.md:600` | none | — | `:238` | **not fixed** | red |
| 06 | `README.md:75` | none | — | `S128 (…)` | **not fixed** | red |
| 07 | `SKILL.md:699` | none | — | not "equal to the receipt row" | **not fixed** | red |
| 08 | `plans/pkg_gate.py:276` | none (frozen) | — | no `biopython==1.85` | **cannot fix under the freeze** | red |

Twin rows closed in round 43 with lenient checks, all three re-measured `rc=0` here:
`R42-R3-01` (`grep -qE '43680|43681'`), `R42-R3-04` (`grep -qF 'fibsqrt_probe.py:201'`), `R42-R3-41` (`:433-434`).
So the errata landed; only rows whose check demands a **single-line anchor** that the errata stated as a span are
red. That is one defect class, not three content defects (finding F1).

## 5. Draft (applied and measured in the scratch clone only)

Three lane-surface edits plus one ledger draft. Diff: `R44RoutedPackage/package-draft.diff`, 4 hunks, 3 files,
`+28 −4`; application target is the landing commit (L1 substitutes its hash in the `close` cells).

**(a) `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` — appended section (22 lines), nothing above edited:**

```markdown
## Errata (round 44, package rows R42-R3-05/09/38/39/40; appended 2026-10-26, nothing above edited)

Three items. The first is a locator appendix for the round-43 errata: routed rows R42-R3-38/39/40 name one entry line
each, while E1–E3 state a span. E8 and E9 correct two sentences no earlier errata reached.

- **Locator appendix to E1–E4.** The sentence E1 quotes is `:297` (E1's span is `:296-298`); E2's is `:311` (span
  `:309-312`); E3's is `:431` (span `:430-432`); E4's is `:433-434` as written. Each of the four corrections stands
  as worded; this item adds the single-line anchors and changes no sentence above.

- **E8 `:350` — the helper span.** Quote: "the captured grader's own helpers (`test_outputs.py:26-52`)". **Locator
  wrong by one line.** `fibonacci` starts at `:26` and `isqrt`'s last statement is `:53` (`x = x_new`; `:52` is its
  `return x`; `:54` is blank), so the helper span is `test_outputs.py:26-53`, the same span the SKILL decision table
  cites (`SKILL.md:1205`). Correction: "the captured grader's own helpers (`test_outputs.py:26-53`)". Nothing else in
  the bullet moves.

- **E9 `:328` — the vacuous pytest-cache clause.** Quote: "this grader writes nothing outside its own `./sim` and
  pytest's cache". **Unsupported for this probe.** The probe never runs pytest: its harness imports the captured
  module and calls the three functions itself (`plans/fibsqrt_probe.py`; the file's only `pytest` mentions are prose
  about `test.sh`, `:18`, `:19`, `:44`), so no pytest cache exists in the sandbox the Regrade section describes.
  Correction: "this grader writes nothing outside its own `./sim`". The Regrade section's conclusion — a second call
  over unchanged files cannot differ — stands on the file reads, not on this clause.
```

**(b) `SKILL.md:600`** — V4/V7 citation: `(`:178-184`)` → `(`:184` in V4, `:238` in V7)`.

**(c) `SKILL.md:699`** — V9 content: "the entry's `## Case table` equal to the receipt row by row" → "the entry's
`## Case table` rows equal on the three graded fields — case id, the three test letters and the observed verdict
(`plans/round42_c2_verify.py:84`, `:298`); the description cells are prose and are never compared".

**(d) `corpus/README.md:75`** — sources cell: `S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)` →
`S125, S126, S127 (terminal-bench-2 @ 2fd12b88); S128 (OpenAgents issue #9645, prior art)`.

**(e) Ledger draft** (`R44RoutedPackage/draft-ledger-rows.jsonl`, the nine rows only; validates under
`routed_open --list`, 60 rows, rc 0):

- `R42-R3-02/05/06/07/09/38/39/40` → `status=closed`, `close` naming the edit (L1 substitutes the commit).
- `R42-R3-09` also gains its first check:
  `grep -qF ':328' corpus/knowledge/tb2-circuit-fibsqrt-grader.md && grep -qF 'no pytest cache exists' …`.
- `R42-R3-08` → `status=blocked`, `close=null`, blocker: "`plans/pkg_gate.py` is a frozen instrument:
  `plans/round-43-claims.md` §C2 froze it and `plans/pkg-spec-r44.json` pins it at `ea638822…` in
  `frozen_instruments`, so the row's check … cannot close until a round freezes a different gate; the cold-cache
  failure it names is measured this round". Check unchanged. (Precedent for the status: `R39-R3`, blocker =
  "`corpus/defects.jsonl` is pinned …".)

**Measured after the draft** (all nine checks re-run verbatim in the patched clone): `rc=0` for 02, 05, 06, 07, 09,
38, 39, 40; `rc=1` for 08 only. `routed_open --observe` over the drafted rows, envelope §8:
`OBSERVE R42-R3-08 rc=1 observed=fail self=blocked` and the other eight `rc=0 observed=pass self=closed`;
`OBSERVE rows=60 mismatched=0`; `ROWS total=60 open=29 blocked=2 closed=29 refused=0`; `routed_open=31`.

## 6. Non-regression: the round-42 C2 counter on the patched clone

`python3 plans/round42_c2_verify.py --lane $S/lane --work $S/c2w` under the round-44 envelope:

```
V1 ok listed=9 bad=0 extra=0        V6 ok census_exit=0
V2 ok spec=frozen gate=frozen gate_exit=0     V7 ok rows=7 tags=7 bad=0
V3 ok rows=3 bad=0                  V8 ok order_exit=0 result=PASS
V4 ok cases=16 mismatches_named=0/0 bad=0     V9 ok case_rows=16/16 bad=0
V5 ok probe=frozen dry_byte_equal=True        checks=9 defects=0 / PREDICATE C2 pass
gate: P10 ok probe_rerun=byte-equal bytes=4212
```
So appending the errata section, the two SKILL edits and the README cell leave `round42-c2` quoted and derived
content intact (`V9 case_rows=16/16`, `P7`/`P4` inside `gate_exit=0`). Lane clone after the run:
`git status --porcelain` = the three drafted files only (no stray writes).

## 7. Findings

- **F1 `routed-check-token-vs-errata-span` (root cause of 38/39/40).** A routed check that greps for one entry line
  is satisfiable only if the correction carries that line. E1–E3 state spans (`:296-298`, `:309-312`, `:430-432`),
  E4 states the exact pair the check greps — so `R42-R3-41` closed and 38/39/40 did not, on identical work. Draft
  rule for the lane: an errata item that closes a routed row leads with the row's line in backticks.
- **F2 duplicate rows (01/38, 04/39).** The same defect was filed twice (one row from each review seat) with
  different checks; round 43 closed the lenient twin and left the strict one red, so the burn-down counts the same
  defect twice and overstates open work by 2 until both close. Draft closes both and keeps the pair visible.
- **F3 `R42-R3-09`'s "no check" is falsified once the correction exists.** The row's note ("no stable text property
  separates a correction from the original clause") is true of the original sentence only; after an appended
  correction a two-token check is stable (measured green, §5). Its `check=null` was a consequence of the
  append-only rule, not of the text.
- **F4 `R42-R3-08` is unreachable as filed.** Its check needs an edit to `plans/pkg_gate.py`, which round 43 froze and
  `plans/pkg-spec-r44.json` re-pins (`ea638822…`). Drafted as `blocked`, not silently dropped. The cold-cache
  failure F42RevC2Package inferred (D8) is **half measured**: on a cold `~/.cache` overlay the fallback ran under
  `uv` with network and fetched 143 MB into the overlay, and P10 still passed (§6) — the offline-cold failure stays
  inferred, no offline host was available.
- **F5 nit in the row's own note.** `R42-R3-06`'s note cites the coverage bullet at `README.md:271`; at this tip it is
  `:272` (line drift since round 42). Its PROVINCE clause is right: `PROVINCE.md:539` reads "(S125, S126, S127; S128
  prior art)", and `README.md:272` reads "(+ S128, tier B prior art)".

## 8. Envelopes (QUALITY Q32)

All three runs used `.ufo/waves/round-44/claims/envelope.sh "$S/env"`; `~/.local/bin` content digest unchanged in
each.

```
# baseline observe
ENVELOPE start 20:36:41 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage/lane
ENVELOPE end   20:36:43 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
# round-42 C2 counter on the patched clone
ENVELOPE start 20:38:19 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage/lane
ENVELOPE end   20:39:20 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
# observe over the drafted rows (re-run after the appendix's item-count wording fix)
ENVELOPE start 20:41:07 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage/lane
ENVELOPE end   20:41:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
The nine per-row `grep`/`test` checks write nothing and were first run bare (§2), then re-run inside the envelope
through `routed_open --observe` (§2, §5) — both report the same nine results.

## 9. Limits

- Drafts were measured in the scratch clone only; the lane's ledger, entry, SKILL and README are unmodified, so
  `routed_open --observe` on the lane still reads `open=38` and the same nine red rows until L1 lands the patch.
- The `close` cells in the drafted rows name the edit, not a commit; L1 must substitute the landing hash before the
  rows are honest (a closed row without a commit id would be a self-close).
- `round42-c2` was run once, on this host, under host python 3.14 with network; the probe's gcc/pytest parity
  limits are the entry's own (§What the probe does not show) and were not re-measured.
- No row outside the nine was re-checked; `R42-R3-01/04/41` were only run to show the twin asymmetry (§4).
- `plans/pkg_gate.py` was read, never edited; the `biopython` fallback was exercised only through the counter run.

## 10. Receipts (`R44RoutedPackage/`, sha256 prefix)

| file | sha256[0:16] | content |
|---|---|---|
| `package-draft.diff` | `75592098d9dca3b1` | the three-file draft patch (4 hunks, +28 −4) |
| `draft-ledger-rows.jsonl` | `35d483dac4e5dda2` | the nine drafted rows |
| `entry-appendix-only.txt` | `4d383462a49bc26d` | the appendix block alone (22 lines, with the blank separator line) |
| `observe-baseline.txt` | `fc4206c29bfb62e2` | `routed_open --observe` at the tip (envelope) |
| `observe-after-draft.txt` | `6c18f9a403f7265c` | `--observe --file draft` (envelope) |
| `c2-patched-counter.txt` | `3c1f7a92c70396b2` | `round42_c2_verify.py` on the patched clone (envelope) |
| `ledger-list-baseline.txt` | `54beb34a3dabcb3a` | `routed_open --list` at the tip |

Scratch `/fast/scratch/hyaku/kengaku-r44/R44RoutedPackage` removed with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44RoutedPackage "$S"` after the receipts
above were copied here.

VERDICT: package-defects-fixed-8-of-9
