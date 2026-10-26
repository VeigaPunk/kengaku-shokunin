# F39CritC1Count — recount of C1's calibration denominator

Seat: critic, round-39 wave 2 (FALSIFY). Lane `kengaku-shokunin` read at tip
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`; every file I quote was hashed in a
`git clone -q --no-local` of that tip whose `rev-parse --show-toplevel` is the clone, and
compared to the lane working tree: `diff` empty, so the numbers below are tip-bound
(receipts `falsify/F39CritC1Count/{recount,anchors,before-after,digests}.txt`). Scratch
`/fast/scratch/hyaku/kengaku-r39/F39CritC1Count` (`TMPDIR` there), removed at exit. No lane
file, index, git or jj state written; no tool installed (pacman paused host-wide, nothing
needed); no predicate re-run — the C1/C2 counters are wave-1/L1 surfaces, and the numbers I
check are the ones the lane committed.

Question: does the round-39 landing report the right advertised-behaviour denominator and the
right before/after mismatch counts? Answer in one line: **the before/after pair is right, the
denominator is not.** On the declared surface that C1's own freeze names, 5 of the 7 mutants
have a reaching advertising sentence, not 4 — and the landed text reaches 4 only by silently
switching from "what the gate advertises" to "what the `adv` cell cites", a standard it never
states.

---

## 1. The declared surface, as the freeze defines it

`plans/round-39-claims.md:24-26` names exactly four anchors: "what the lane advertises about
it — the gate docstring, `corpus/QUALITY.md` Q24/Q27, the SCORECARD capability row
`package-gate`". Located (`anchors.txt`):

| anchor | line | quoted fragment (≤25 words) |
|---|---|---|
| gate docstring | `plans/pkg_gate.py:7` | "exit 0 = accept, 1 = reject, 2 = usage/setup (an unexpected crash never maps onto 0 or 1)." |
| gate docstring | `plans/pkg_gate.py:9-10` | "Every clause is spec-driven: paths, digests, row ids, tier, status, quote bounds, labels and directional tokens come from --spec." |
| gate docstring | `plans/pkg_gate.py:13` | "a quote not verbatim on its cited line … are defects." |
| Q24 | `corpus/QUALITY.md:300` | "the genuine package must be accepted, every single-property junk mutant must be rejected" |
| Q27 | `corpus/QUALITY.md:409-410` | "a gate's advertised defect class counts as held only when a single-defect fixture kills that class's silence mutant" |
| SCORECARD row | `SCORECARD.md:564` | "the labelled D4/D5 correction lines against a spec of pinned digests"; "a stub probe dies on its digest pin"; "Exit 0 accept / 1 reject / 2 setup" |

Two things follow from the surface definition and are not negotiable by the counter: Q24's
"genuine package" sentence and SCORECARD's class sentences are *advertising* whether or not a
given `adv` cell happens to quote them. The cell is metadata about the mutant; the denominator
is a property of the advertised surface.

## 2. Per-mutant tier, measured against those four files

Tiering method is wave 1's own (`R39CritClaims` §1): **C** = a sentence states the property in
the mutant's direction; **K** = a component noun or a general class sentence covers it; **N** =
no sentence on the surface reaches it, or the sentence it names is satisfied by both the
reference and the mutant.

| M | behaviour the mutant silences | what the cell cites | citation reaches? (measured) | any surface sentence reaches? | tier |
|---|---|---|---|---|---|
| M01 D5 mirror | a D5 capture pinned on a non-first manifest row is accepted | Q24 `QUALITY.md:300` | **no**: `quarantine-SHA256SUMS` row 1 *is* the capture digest (`b60af775…`), so `[:1]` is a no-op on the accepted state | **yes, K**: `SCORECARD.md:564` "the labelled D4/D5 correction lines against a spec of pinned digests" — a digest on row 2 is still pinned in the manifest | **K** |
| M02 P1 silence | every frozen instrument is checked, not only the first | SCORECARD:564 fragment "… a stub probe dies on its digest pin" | **K only**: the named pin (the probe) is `frozen_instruments[0]`, the pin the mutant retains; cover comes from the plurals "frozen instruments" / "a spec of pinned digests" | yes (same sentence) | **K** |
| M03 P3 silence | a quote one word above the spec's upper word bound is a defect | `pkg_gate.py:9-10` | **K only**: provenance of the bound, not that exceeding it rejects; the defect list (`:13`) omits word bounds; Q24's example (`QUALITY.md:305`) is the *lower* bound | yes (same sentence) | **K** |
| M04 P7 silence | a row's second `source:` line is not compared | SCORECARD:564 "SOURCES rows …" | **no**: wrong artefact — that names the registry P6 reads (`pkg_gate.py:184-209`), the mutant is in the entry's `source:` lines (`:211-232`); Q1 (`QUALITY.md:15-19`) says what a line carries, not how many | **no** | **N** |
| M05 RUN rc-silence | a package with a DEFECT clause exits 1 | `pkg_gate.py:7` + SCORECARD exit clause | yes | yes | **C** |
| M06 MAIN rc-mirror | the genuine package exits 0 | `pkg_gate.py:7` + Q24 | yes | yes | **C** |
| M07 D5 mirror | a quote whose span carries markup is found (tag strip on) | Q24 `QUALITY.md:300` | **no**: the genuine quote is contiguous in the **raw** capture (`quote in raw = True`, `recount.txt`), so the strip never changes the accepted state | **no**: nothing advertises tag tolerance; `pkg_gate.py:13` advertises the opposite (strict "verbatim") | **N** |

Recount: **C 2 (M05, M06) / K 3 (M01, M02, M03) / N 2 (M04, M07)** → advertised = C+K = **5/7**.

The three uncited-by-the-cell mutants remain M01, M04, M07 — that part of wave 1 is right and
I reproduce it. What is wrong is the step from "the cell cites the wrong sentence" to "the
gate does not advertise the behaviour", taken for M01 only. Wave 1 itself never took that step:
`build/R39CritClaims.md:35` says "A covering class sentence does exist at `SCORECARD.md:564`
… but the cell does not name it", and `build/R39AdvErrata.md:148` says the same and calls M01
"*uncitable*", reserving "*unreachable by any sentence*" for M07 (`:149`).

## 3. The two landed statements, and where they break

| statement | text | against the recount |
|---|---|---|
| `corpus/lessons/round-39.md:46` | "the advertised-behaviour count is reported as 4 (M02, M03, M05, M06): before 2 undemonstrated (M02, M03) → after 0" | **denominator wrong** (5, not 4); **before/after right** under 5 too (M01 was already killed at the freeze) |
| `SCORECARD.md:1385` | "Advertised-only recount (M02, M03, M05, M06 reach a sentence; M01, M04, M07 do not — `R39CritClaims` §1): 2 → 0" | **membership claim false for M01** and misattributed to `R39CritClaims` §1, which says the opposite; "2 → 0" holds |

Verified before/after, from the committed control and the landing measurement
(`before-after.txt`):

- freeze control `.ufo/waves/round-39/claims/control-c1-nothing.txt`: survivors **M02, M03,
  M04, M07**, killed M01, M05, M06 (`MUTANTS total=7 killed=3 survived=4`).
- landing `integrate/measure-final.txt`: `MUTANTS total=7 killed=7 survived=0`, no survivor line.
- Among {M02, M03, M05, M06} → before **2** (M02, M03) → after **0**. ✓
- Among {M01, M02, M03, M05, M06} → before **2** (M01 is killed at the freeze by the
  `mirror` relabel of `d5m-n21-manifest-row-2`; the round-38 block in the same file still reads
  `MUTANT N21 D5 silence SURVIVED`) → after **0**. ✓

So the number that moves is identical under 4 and under 5. The defect is not the arithmetic; it
is that the membership sentence is false and its provenance citation points at a report that
contradicts it.

## 4. Why the pair (4, 2 → 0) is not derivable from one standard

Four self-consistent readings of "advertised", computed mechanically from the committed
control:

| standard | advertised | before-undemonstrated | after |
|---|---|---|---|
| C only (a sentence states the property) | **2/7** (M05, M06) | 0 | 0 |
| C+K, the cell's own citation credited | **4/7** (M02, M03, M05, M06) | 2 (M02, M03) | 0 |
| C+K, any declared-surface sentence | **5/7** (M01, M02, M03, M05, M06) | 2 (M02, M03) | 0 |
| Q27's own unit — the advertised *class* (D5, P1, P3, P7, RUN, MAIN are all named) | **7/7** | 4 (M02, M03, M04, M07) | 0 |

The landed (4, 2 → 0) is row 2. Row 2 is a legitimate thing to measure — how good are the seven
`adv` cells — but it is not "the advertised-behaviour count", and it is not the unit Q27 makes
load-bearing ("a gate's *advertised defect class*"). Rows 3 and 4 also report 2 → 0 without
being derivable from row 2's list. A reader given only lesson:46 cannot tell which of the four
the lane means, and row 1 shows what happens if the reader takes the label literally: the
round's improvement disappears (0 → 0), because M05/M06 were already killed at the freeze.

## 5. One further advertising imprecision (not part of the count)

The M01 cover is K, not C, for a second reason worth recording: SCORECARD:564 says "against a
**spec** of pinned digests", but the D5 path pins nothing in the spec — measured, neither the
capture digest nor the manifest digest appears anywhere in `plans/pkg-spec-r35.json`
(`recount.txt`: `spec string contains capture digest = False`, `… manifest digest = False`); the
manifest is read from the same capture directory it vouches for (`pkg_gate.py:346`). So the D5
half of that sentence is imprecise about where the pins live. This does not move the count (the
sentence still names the correction line and digest pinning), but a reader who insists the
sentence be literally true would get 4/7 for a *different* reason — and with a different repair
(fix the row, or pin the manifest) — not because M01 has no sentence.

## 6. What this does and does not falsify

- Does not falsify C1's predicate or its landing: `PINS total=26 mismatched=0`, `BATTERY
  fixtures=90 … wrong=0`, `MUTANTS total=7 killed=7 survived=0`, `PREDICATE C1 pass`
  (`integrate/measure-final.txt`) are untouched by a denominator relabel.
- Does not change the axis: 2 → 0 holds at 4 and at 5, so calibration 8 → 8 held stands.
- Does falsify the claim that M01 "does not reach a sentence" (SCORECARD:1385) and the count 4
  as "the advertised-behaviour count" (lesson:46), and it shows the landed SCORECARD row
  misattributes that claim to `R39CritClaims` §1.
- M04 and M07 stay N on independent measurement (artefact misnaming; quote contiguous raw), so
  this is a one-mutant correction, not a re-run of wave 1's argument.
- Recorded, not a defect here: the list of seven is not a census of the gate's advertised
  behaviours (wave 1 §2), so the denominator is a count over this list, never over the surface.

## 7. Smallest safe correction (text only; nothing frozen)

- `corpus/lessons/round-39.md:46` → "the advertised-behaviour count is **5 (M01, M02, M03, M05,
  M06)** on the declared surface; crediting only the sentence each `adv` cell actually cites
  gives 4 (M01's cell cites Q24, which the genuine manifest's row-1 capture digest satisfies);
  before 2 undemonstrated (M02, M03) → after 0 under either reading."
- `SCORECARD.md:1385` → replace the parenthetical with "Advertised-only recount: 5 reach a
  sentence on the declared surface (M01 via `SCORECARD.md:564`; M02, M03, M05, M06) and 4 are
  also cited correctly by their cell (M01's cites Q24, a no-op on the accepted state); M04 and
  M07 reach none — `R39CritClaims` §1, `R39AdvErrata` F-C/F-D. 2 → 0."

## Receipts

- `falsify/F39CritC1Count/recount.txt` — frozen-instrument order (`tb2_grader_probe.py` first),
  genuine D5 capture/`quarantine-SHA256SUMS` digest and two rows, row-1-is-capture,
  all-rows vs row-1-only pinned, quote contiguous in raw and tag-stripped, spec pins neither
  digest.
- `falsify/F39CritC1Count/anchors.txt` — `grep -n` of every quoted fragment (docstring 7/9/13,
  Q24 300/305, Q27 409-410, SCORECARD 564/1385, lesson 46, claims 25/27/62,
  `R39CritClaims.md:35,300-307`, `R39AdvErrata.md:148-149,156-158`).
- `falsify/F39CritC1Count/before-after.txt` — survivors parsed from the freeze control and the
  landing measurement; the four standards' counts; the note that `measure-final.txt`
  concatenates runs.
- `falsify/F39CritC1Count/digests.txt` — sha256 of every file measured, identical in clone and
  lane.

VERDICT: c1-advertised-5/7-stated-count-wrong
