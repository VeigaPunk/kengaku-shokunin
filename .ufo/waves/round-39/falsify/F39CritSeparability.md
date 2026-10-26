# F39CritSeparability — round 39 wave 2 (falsify): does the §Separability sentence hold?

Seat: critic. Target: `plans/round-39-claims.md` §Separability (`:92-94`), attacked against the L1's correction in
`corpus/lessons/round-39.md:47`. Measured at the assigned tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch
master) on clean clones; the live lane moved to `acf4375` during the seat (4 dirty entries, none mine — I never wrote
in the lane). Receipts: `.ufo/waves/round-39/falsify/F39CritSeparability/` (`base-*`, `A-*`, `A2-*`, `B-*`, `B2-*`,
`C-*`, `D-*`, `E-*`, `F-*`, `G-*`, `H-*`, `mutations.txt`). Scratch `/fast/scratch/hyaku/kengaku-r39/F39CritSeparability`
held all ten clones and was removed; no lane file, index or jj state touched. Environment: Python 3.14.8, git 2.56.0.

The sentence under test (`plans/round-39-claims.md:92-94`):

> "C1 reads only the gate, the round-35 spec, the round-36/37 counters, batteries 37/38 and `plans/battery39`; C2 reads
> only its captures, spec, probe, receipt, entry, SOURCES and README. Neither counter reads the other's work product:
> C1 can pass with C2 absent and vice versa. The gate digest is shared and frozen for both."

The L1's substitute (`corpus/lessons/round-39.md:47`): "each claim passes with the other's work product wholly absent,
not partly present."

## Axes

- **calibration** — C1's 7/7 kill count and its stability under foreign edits (primary).
- **coverage** — C2's `checks=7 defects=0` and what actually moves it.
- **operability** — whether the frozen predicates reproduce from anything but a pristine clone.
- **claim precision** — whether §Separability describes the read surface it claims to.

## Measurements

Ten clean clones of `a6832f53`, one mutation each (`mutations.txt`), two counters. Every C1 run is
`python3 plans/round39_c1_verify.py --lane .` (~35–45 s); every C2 run `python3 plans/round39_c2_verify.py --lane .`
(~2 s); audit `python3 plans/round39_c1_audit.py --lane .` (~25 s).

| # | mutation | C1 stdout | C2 stdout |
|---|---|---|---|
| base | none | `PREDICATE C1 pass` (sha `c9108768…`) | `checks=7 defects=0` `PREDICATE C2 pass` (sha `8cbf8384…`) |
| **A** | whole C2 package: entry, S117+S118 rows, 4 README line groups, receipt | `PINS total=26 mismatched=0` / `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0` / `PREDICATE C1 pass`, **byte-identical** | `checks=7 defects=4` (V2, V3, V4, V7) `PREDICATE C2 fail` rc=1 |
| **A2** | A + `round39_c2_verify.py`, `git_leak_probe.py`, `pkg-spec-r39.json`, `corpus/evidence/round39/` | pass, **byte-identical** (`sha256 c9108768…`); `AUDIT C1 clean` | n/a (its counter is gone) |
| **B** | `rm -rf plans/battery39` | `BATTERY fixtures=86 …` / `MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0` (M02, M03, M04, M07 survive) / `PREDICATE C1 fail` rc=1 | `checks=7 defects=0` `PREDICATE C2 pass`, **byte-identical** |
| **B2** | B + battery37, battery38, `round36/37/39_c1_verify.py`, `round37_c1_attribution.py` | n/a | `checks=7 defects=0` `PREDICATE C2 pass`, **byte-identical** |
| **C** | only the README index row (`corpus/README.md:72`) | `fixtures=90 wrong=54 …` / `MUTANTS total=7 killed=6 survived=1` (M06 survives) / `PREDICATE C1 fail` | `checks=7 defects=1` (V2) `PREDICATE C2 fail` |
| **D** | only the receipt `corpus/evidence/round39/git-leak-probe.txt` | pass, **byte-identical** | `checks=7 defects=3` (V2, V4, V7) |
| **E** | only SOURCES rows S117/S118 | pass, **byte-identical** | `checks=7 defects=2` (V2, V3) |
| **F** | entry + README row, SOURCES rows kept | pass, **byte-identical** | `checks=7 defects=4` (V2, V4, V6, V7) |
| **G** | C2 entry content perturbed (`recheck: echo bogus-c2-entry-probe` appended), parity intact | pass, **byte-identical** | n/a |
| **H** | the *round-38* entry's README row (`tb2-build-pmars-grader`), nothing of C2 touched | `wrong=54` / `killed=6 survived=1` (M06) / `PREDICATE C1 fail` | `checks=7 defects=1` (V2) |

Identity receipts (`sha256sum`, full hashes in `mutations.txt` sibling files): C1 = `c9108768d6447024379851d0914ff618172d2b302c8bab8c572ca716d2558311`
for base, A, A2, D, E, F, G; C2 = `8cbf83841a2756543b10da500a250acb9e2ce0148d64b57392b8a812690e65a4` for base, B, B2.

## Findings

**S1 — the predicate-level claim is confirmed, exactly.** C1 with the whole C2 package absent (A) and with every C2
artefact including its counter, probe and spec absent (A2) prints the *same 101 lines*, `PREDICATE C1 pass`. C2 with
`plans/battery39` absent (B) and with all three C1 counters, both older batteries and the attribution audit absent
(B2) prints the same 20 lines, `PREDICATE C2 pass`. "C1 can pass with C2 absent and vice versa" is true as measured,
not merely plausible.

**S2 — "C1 reads only …" (claims:92) is false: C1's fixtures copy the live corpus.** `plans/round36_c1_verify.py:57`
copies `spec["entry"], spec["receipt"], spec["sources"], spec["readme"]` from the lane worktree, `:64` copies *every*
`corpus/knowledge/*.md` and `:67` every `corpus/lessons/*.md`. Consequence in C: deleting C2's one README index row —
a C2 work product — moves C1 to `wrong=54`, `killed=6 survived=1`. All 54 wrong fixtures carry defect `P8` and none
lacks it (`grep -c P8` over the 54 `WRONG` lines → 54; wrong without P8 → 0). C1's read surface therefore includes
`corpus/README.md`, `corpus/knowledge/` and `corpus/lessons/`, which §Separability does not list at all.

**S3 — the lesson's substitute boundary ("not partly present") is the wrong rule.** D, E, F and G are all *partial*
states and all leave C1 byte-identical to base. G is the sharpest: a garbage `recheck:` line appended to C2's entry —
the exact shape of the round-38 incident — is invisible to C1. What moves C1 is not partial presence but a specific
shared invariant: the gate's P8, `index rows == knowledge files` (C read: `r36-P0 expect=accept … observed_defects=P8
WRONG`). Parity-preserving partial removals: invisible. Parity-breaking ones: red.

**S4 — the coupling is not C1←C2 at all; it is both←corpus parity.** H removes a *third* entry's README row
(`tb2-build-pmars-grader`, round 38) and reproduces C's numbers exactly — C1 `wrong=54`, `killed=6`, M06 survives; C2
`defects=1` (V2, the live-tree gate run). Since the touched file belongs to neither C1's nor C2's work product, the
sentence's framing ("neither reads the other's") is not the coupling that exists: both counters read one shared corpus
shape, and that shape is what a partial state can break.

**S5 — calibration cost of the parity channel: one README line deletes a kill.** In C and H, M06 (`MAIN rc-mirror`,
"the genuine package exits 0, not 1") survives because the reference fixture `r36-P0` now rejects (`observed_rc=1
observed_defects=P8`), so a mutant that turns accept into reject is no longer distinguishable. `killed=7` → `6`. The
L1's added audit does not restore it (A2: `AUDIT C1 clean`, and it is green in both configurations tested). The frozen
C1 predicate is reproduced only from a clone whose corpus parity is intact — the claims and lesson both *require* a
clean clone, but for the wrong reason ("partly present"), so the next seat that breaches parity for a legitimate
reason (a half-landed entry) will read the resulting `killed=6` as a counter defect.

**S6 — controls reproduced exactly, so the deltas above are attributable.** B prints the frozen do-nothing control of
`plans/round-39-claims.md:47-48` verbatim (`BATTERY fixtures=86 …`, `MUTANTS total=7 killed=3 survived=4`): battery39
is C1's only round-39 delta. A prints the frozen C2 do-nothing control of `plans/round-39-claims.md:81-82` verbatim
(`checks=7 defects=4` (V2, V3, V4, V7)): C2's predicate moves exactly by its own package. The shared gate digest clause
is also confirmed: both counters pin `ea638822…` (`plans/round39_c1_verify.py:72`, `plans/round39_c2_verify.py:60`).

## Impacted axes

- **calibration** — S5: a foreign README row removes a kill and reproduces a red C1; the 7/7 count is predicated on
  corpus parity, not on C1's own files. Claim as stated overstates isolation.
- **coverage** — S1/B2: C2's predicate is genuinely independent of every C1 artefact, including the counters themselves.
  No coverage claim needs to move.
- **operability** — S3/S5: "measure on a clean clone" is load-bearing; the stated reason is wrong, so the precondition
  will be carried for the wrong reason next round.
- **claim precision** — S2: the read enumeration at `plans/round-39-claims.md:92-93` omits `corpus/README.md`,
  `corpus/knowledge/`, `corpus/lessons/` and the `corpus/SOURCES.md` rows of other packages.

## Smallest safe correction

1. Replace §Separability (`plans/round-39-claims.md:92-94`) with, in substance:
   "Each counter passes with the other's work product *wholly* absent — measured byte-identical (`c9108768…` C1 with
   the C2 package, its counter, probe and spec gone; `8cbf8384…` C2 with battery37/38/39, the three C1 counters and the
   attribution audit gone). Beyond that, both counters read one shared surface that is neither's work product: the live
   corpus index parity the gate enforces (`corpus/README.md` index rows == `corpus/knowledge/*.md`, P8, copies at
   `plans/round36_c1_verify.py:57-68`) and the frozen gate digest. A partial state that breaks that parity reds both
   (C1 `wrong=54`, `killed=6`; C2 `V2`), whatever the file belongs to."
2. Correct `corpus/lessons/round-39.md:47` from "not partly present" to "not when a partial state breaks the shared
   README↔knowledge parity (P8); parity-preserving partial removals are invisible (receipts D/E/F/G)". Keep the row's
   `wrong=51`/`wrong=54` distinction: the magnitude tracks how many fixtures ride the genuine package, not the size of
   the deletion.
3. Engineering (round 40, not this round): make `plans/round36_c1_verify.py:55-68` read those corpus bytes from the
   freeze commit (`git show 088f7c36:<path>`) instead of `lane / rel`, so C1's predicate stops moving on worktree
   corpus edits and the parity channel cannot delete a kill.

## Limits

- One host, one interpreter (`Python 3.14.8`), git 2.56.0; the gate's arms that depend on the interpreter/environment
  are untouched by this seat.
- C1 runs are ~35–45 s each; ten were run (base, A, A2, B, C, D, E, F, G, H) and two audits (base, A2). C2 is ~2 s;
  nine were run (base, A, B, B2, C, D, E, F, H).
- The lane tip advanced to `acf4375` mid-seat; everything here is measured at `a6832f53` as assigned, in clones whose
  `rev-parse --show-toplevel` was verified to be the clone root before every write.

VERDICT: separable-partly
