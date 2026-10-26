# F42MutBattery — fixture-level mutation of battery42 (kengaku r42, wave 2 FALSIFY, 2026-10-26)

Seat: F42MutBattery (leaf, mutation tester). Attacked: the landed C1 calibration claim
(`plans/round42_c1_verify.py` + `plans/battery42/`, 5 modules, 29 fixtures, 14 mutants) at lane tip
508434ad55c709337065611691c426f05875492d, via one single-edit mutant per fixture and per-fixture removal.
Lane clone: `/fast/scratch/hyaku/kengaku-r42/F42MutBattery/lane` @ 508434ad (plans/ identical to the landing
tip ff14d76d — the docs commit touched only LOG/SCORECARD/lessons/census/measure).

**Envelope (QUALITY Q32):** every counter run went through `receipt_run.sh` =
`/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 …/round42_c1_verify.py --lane …/lane --battery-dir … --work …/c1work --jobs 16`.
99 receipts in this dir (`receipt-<tag>.txt`: 97 case runs + baseline + treeprobe), each carrying ENVELOPE,
`START/END date +%T`, and `ls -A /home/vgpnk/.local/bin | sha256sum` before/after — identical on every run
(`77408cab9a10361a9f6025bab21f5f07933d94ce46e6a10b9117805d58811c11`). No pacman transaction; no tools installed.

**Baseline:** `receipt-baseline.txt` reproduces the landing measurement's C1 block: `PINS total=2 mismatched=0`,
29 `FIXTURE … ok` lines, 14 `MUTANT … killed by=…` lines, `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9
order=5/5`, `PREDICATE C1 pass`, exit 0 (3 s wall). Killer map: X1→a_route-x1-provenance-table, X3→a_route-x3-provenance-url,
X6→a_class-x6-sibling-digest, X7→a_class-x7-fabricated-token, X9→a_row-x9-short-no-token, X12→a_route-x12-slashless-toml,
X13→a_row-x13-staged-capture, X14→a_class-x14-uppercase-token, X15→a_row-x15-sibling-digest, XO1→o_clause-freeze-single,
XO3→o_clause-receipt-withdrawn, XO5→o_scan-xo5-post-receipt-verdicts, XO6→o_scan-xo6-pass-verdict-row,
XO7→o_scan-xo7-timeout-rows. Every mutant has exactly 2 hit fixtures (X7: 6).

**Method:** the REAL counter in dev mode (`--battery-dir` = scratch copy of all 5 battery modules with one
single edit; predicate line reads `n/a`, verdict lines identical in shape). One adversarial mutant per fixture
(the single edit most likely to slip through), plus controls: flip-expect on all 29, decisive-commit drops,
excuse-break, unborn-HEAD, receipt-constant byte, 29 single-fixture removals, 3 pair removals. All edits are in
`driver.py` (copied into this dir); per-case mutated batteries and results.tsv were built in scratch and wiped.

## Table 1 — the 29 fixture mutants (one adversarial single edit each)

All 29 rows: `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0` + `MUTANTS total=14 killed=14 survived=0
invalid=0 null_detected=0 unattributed=0` + exit 0, i.e. byte-identical verdict lines to baseline unless noted.

| # | fixture | kind | single edit | counter output | noticed |
|---|---------|------|-------------|----------------|---------|
| C01 | a_class-x6-sibling-digest | capture byte | x6-a/notes.txt `names`→`nameZ`; token is capture B's digest, A's bytes unreferenced | identical (X6 still `killed by=a_class-x6-sibling-digest attributed=L527`) | no |
| C02 | a_class-x6-stale-manifest | drop commit | drop commit 1; commit 2's `add -A` absorbs it | identical; HEAD tree byte-identical (tree probe) | no |
| C03 | a_class-x7-fabricated-token | capture byte | the row's own capture `names`→`nameZ`; token fabricated regardless | identical | no |
| C04 | a_class-x7-provenance-row | drop commit | drop commit 1; tree identical | identical | no |
| C05 | a_class-x14-uppercase-token | capture byte | outputs.txt body byte; row anchor and erratum correction both derive from the body literal | identical | no |
| C06 | a_class-x14-two-errata | drop commit | drop commit 1; tree identical | identical | no |
| C07 | a_route-x1-provenance-table | capture byte | registry.capture body byte; SHA256SUMS, provenance digest column and row anchor all recompute | identical | no |
| C08 | a_route-x1-two-row-registry | drop commit | drop the batch commit; tree identical | identical | no |
| C09 | a_route-x3-provenance-url | capture byte | capture.py body byte; all digests recompute | identical | no |
| C10 | a_route-x3-blob-url | capture byte | test_outputs.py body byte | identical | no |
| C11 | a_route-x12-slashless-toml | capture byte | test_outputs.py body byte | identical | no |
| C12 | a_route-x12-two-tomls | capture byte | lookup-circuit.txt body byte | identical | no |
| C13 | a_row-x9-short-no-token | capture byte | note.txt body byte; row carries no token, cell-count fires regardless | identical | no |
| C14 | a_row-x9-registry-short-valid | capture byte | alpha body byte; rows recompute from dig(body) | identical | no |
| C15 | a_row-x13-staged-capture | staged byte | staged cap.txt byte; HEAD verdict unchanged, mutant still resolves via index | identical | no |
| C16 | a_row-x13-url-staged | staged byte | staged test_outputs.py byte | identical | no |
| C17 | a_row-x15-sibling-digest | capture byte | fx-a body byte; token uncommitted regardless, correction is fx-b's digest | identical | no |
| C18 | a_row-x15-manifest-sibling | drop commit | drop the rows commit; tree identical | identical | no |
| C19 | o_clause-freeze-single | claims byte | claims header `run.`→`runX`; gate reads commit structure only | identical | no |
| C20 | o_clause-freeze-pair-edited-after | drop commit | drop the scaffold commit; tree identical, clause 1 unchanged | identical | no |
| C21 | o_clause-receipt-withdrawn | drop commit | drop the withdraw (rm+commit); freeze tree keeps receipt v1 → clause 1 fires instead of clause 2, rc still 1 | `MUTANT XO3 order rc-silence killed by=o_clause-receipt-side-line attributed=L188 hits=1` (by= shift), wrong=0, killed=14, exit 0 | no |
| C22 | o_clause-receipt-side-line | drop commit | drop the withdraw; same clause substitution on the side line | identical (second hit; killer untouched) | no |
| C23 | o_clause-clean-order | claims byte | claims header byte | identical | no |
| C24 | o_scan-xo5-post-receipt-verdicts | drop commit | drop the post-receipt verdicts commit; reference stops at the receipt commit | `MUTANT XO5 order rc-mirror killed by=o_scan-xo5-amended-claims-blob attributed=L117 hits=1` (by= shift), exit 0 | no |
| C25 | o_scan-xo5-amended-claims-blob | drop commit | drop the amend commit; freeze-time blob is clean | identical (killer untouched) | no |
| C26 | o_scan-xo6-pass-verdict-row | blob byte | `P10 PASS`→`P10 PASs`; neither reference nor widened alternation matches | `MUTANT XO6 order rc-mirror killed by=o_scan-xo6-echoed-pass-row attributed=L53 hits=1` (by= shift), exit 0 | no |
| C27 | o_scan-xo6-echoed-pass-row | blob byte | `gate: P10 PASS`→`PASs` | identical | no |
| C28 | o_scan-xo7-timeout-rows | blob byte | `observed=timeout`→`observed=timeouT`; reference matches any value, narrowed mutant still misses it | identical | no |
| C29 | o_scan-xo7-skipped-row-r38 | blob byte | `observed=skipped`→`observed=skippEd` | identical | no |

**Caught 0/29.** No `wrong`, no SURVIVED, no UNATTRIBUTED, no build failure, no sidechannel token, no tamper,
no null flip on any of the 29. Three rows (C21, C24, C26) shift only the `killed by=` attribution to the pair
partner — the mutant stays killed.

## Controls — what the counter DOES catch (the sensitivity boundary)

| probe | edit | counter line | noticed |
|-------|------|--------------|---------|
| F01–F29 | flip `expect` on each fixture (29 runs) | `FIXTURE <fid> tool=… expect=… declared=… observed_rc=… observed=… WRONG` + `BATTERY … wrong=1`, exit 1 — 29/29 (e.g. F07: `FIXTURE a_route-x1-provenance-table tool=anchor expect=reject declared=- observed_rc=0 observed=- WRONG`) | yes |
| P02 | x6-stale-manifest: drop the commit carrying the bad row | identical to baseline — the row survives uncommitted in the worktree; the tool reads `corpus/SOURCES.md` from the working tree (`anchor_digest_check.py:398`) | no |
| P04 | x7-provenance-row: drop the commit carrying the defective row | identical (same worktree-rows mechanism) | no |
| P06 | x14-two-errata: drop the commit carrying the wrong-case erratum | `FIXTURE a_class-x14-two-errata … observed_rc=0 observed=- WRONG` — lessons are read from the worktree only for paths committed at HEAD (`anchor_digest_check.py:106-107`), so the uncommitted erratum vanishes and the verdict flips green | yes |
| P13 | x9-short-no-token: drop the only commit | `FIXTURE a_row-x9-short-no-token … observed_rc=2 observed=- WRONG` (unborn HEAD → usage error) + `MUTANT X9 … killed by=a_row-x9-registry-short-valid` by= shift | yes |
| P26 | xo6-pass-verdict-row: `receipt unreadable`→`receipt unreadablE` | `FIXTURE o_scan-xo6-pass-verdict-row tool=order expect=accept declared=- observed_rc=1 observed=- WRONG` (the P10 excuse breaks, the gate line becomes a hit) | yes |
| RC1/RC2 | receipt-body constant byte (`cases=16`→`cases=15`), 11 order fixtures at once | identical — the order gate never reads receipt bytes (commit structure only) | no |

## Why the 29 primaries are invisible — four mechanisms, all verified

1. **Tree-identical commit drops** (C02, C04, C06, C08, C18, C20, C21, C22): the surviving commit's `add -A`
   absorbs the dropped one. Tree probe (`receipt-treeprobe.txt`, built through the counter's own
   `--build-module` child in the same bwrap shape): mutated HEAD^{tree} == pristine HEAD^{tree} for every
   fixture of every probed module, e.g. `C02 a_class-x6-stale-manifest TREE-EQUAL pris=84f0613045e3 mut=84f0613045e3`.
   The counter fingerprints the built tree and reads no build history, so a tree-identical build is invisible
   by construction. For C21/C22 the *history* does change (clause 1 fires instead of clause 2) but the exit
   code and class set do not, and `defects` is empty for order fixtures — nothing for `wrong` to see.
2. **Digest-derivation consistency** (C05, C07–C12, C14, C15, C16): every digest reference is computed from the
   same body literal at build time, so a one-byte capture edit propagates consistently into SHA256SUMS,
   provenance digest columns and row anchors; the tool still accepts (or still rejects with the same class).
3. **Insensitive capture bytes** (C01, C03, C13, C17): the edited capture is not the token source (the token is
   a sibling's committed digest, a fabricated digest, or there is no token), so the declared class is unchanged.
4. **Content the tools never read** (C19, C23, RC1, RC2): the order gate reads commit structure only — claims
   and receipt bytes are never parsed; the anchor tool never sees order fixtures.

When an edit *does* remove a killing behaviour (C21, C24, C26 lose the killer's exhibit), the pair partner
still exhibits and attributes, so the mutant stays killed — the two-fixture-per-mutant design absorbs it.

## Table 2 — redundancy: single-fixture removal (29 counter runs)

Every removal: `BATTERY fixtures=28 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0
invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, exit 0. **All 29 fixtures
are individually redundant at the verdict level.**

| group | fixtures | what changes |
|-------|----------|--------------|
| fully line-identical (15) | R02 R04 R06 R08 R10 R12 R14 R16 R18 R20 R22 **R23 (o_clause-clean-order)** R25 R27 R29 — the 14 second-hit fixtures + the pass-path fixture | nothing but `fixtures=29→28` |
| by=-shift only (14) | R01 R03 R05 R07 R09 R11 R13 R15 R17 R19 R21 R24 R26 R28 — the 14 primary killers | `killed by=` moves to the pair partner, e.g. R01: `MUTANT X6 anchor silence killed by=a_class-x6-stale-manifest attributed=L527 hits=1`; every mutant stays killed |

**Pair removals (joint necessity):** removing both members of any hit pair flips that mutant —
PR1 `MUTANT X1 anchor rc-mirror SURVIVED exhibits=none` (killed=13 survived=1, exit 1), PR2 `XO5 … SURVIVED`,
PR3 `X6 … SURVIVED`. The battery's detection power lives in the 14 pairs (+ clean_order as the pass-path
witness); each single fixture is a backup for its partner, not independently load-bearing. Note the predicate
does not bind the fixture count: `good` in `main()` checks kills/wrong/tamper/sidechannel/null, not `fixtures=<n>`.

## Findings for the L1

1. **The counter's fixture-level detection envelope is exactly**: declaration-vs-observed (`wrong`), kill-set or
   attribution change (SURVIVED/UNATTRIBUTED), build failure (SETUP), sidechannel token scan, tamper
   fingerprint, null nondeterminism. Every behaviour-preserving single edit is invisible: **0/29 adversarial
   fixture mutants noticed** (the declaration-flip control is noticed 29/29; decisive breaks P06/P13/P26 3/3).
2. **battery42 modules are not digest-pinned** — `.ufo/waves/round-42/claims/frozen-digests.txt` pins the two
   tools, the claims file, the counters, the probe, pkg files and the two witness modules, but no battery
   module — and the counter reads the battery from the lane at run time. Nothing structural detects a
   battery-module edit. What still defends C1: a single edit cannot remove a killing behaviour from both
   members of a pair, and removing/mutating both flips the mutant to SURVIVED (PR1–3). So single-edit fixture
   corruption cannot silently break C1's calibration counts; it CAN silently change which shape demonstrates
   what (the "second way" shapes, the two-commit histories, the pass-path witness). That is precisely the
   territory the frozen claims already reserve: "admission of C1 rests on the counter AND a non-author review
   that battery42 demonstrates the advertised behaviours honestly" — this experiment shows that clause is
   load-bearing, not decorative.
3. **The `wrong` channel inherits the anchor tool's read asymmetry**: rows from the worktree
   (`anchor_digest_check.py:398`), captures from HEAD blobs, lessons gated on HEAD-committed paths (lines
   106-107). Shown by P02/P04 (unnoticed) vs P06 (caught): dropping a decisive *row's* commit is invisible,
   dropping a decisive *erratum's* commit is caught. A fixture whose defect lives only in uncommitted worktree
   rows is indistinguishable from its committed shape.
4. **Redundancy**: 29/29 fixtures individually removable with the predicate intact (15 with no line change at
   all, 14 moving only `killed by=`); no single fixture is load-bearing, every pair is. If the L1 wants
   per-fixture load-bearing-ness, the counter would need to bind fixture identities (e.g. pin per-fixture
   fingerprints or require each mutant's `by=`), which it currently does not.

Receipts: `receipt-baseline.txt`, `receipt-C01..C29.txt`, `receipt-P02/P04/P06/P13/P26.txt`,
`receipt-PR1..3.txt`, `receipt-RC1/RC2.txt`, `receipt-F01..F29.txt`, `receipt-R01..R29.txt`,
`receipt-treeprobe.txt` — all in this dir, all ≤ 8 KiB. Reproduction: `driver.py` (CASES table = every edit),
`tree_probe.py`, `receipt_run.sh`, `results.tsv` copied into this dir; scratch
`/fast/scratch/hyaku/kengaku-r42/F42MutBattery` wiped after the run.

VERDICT: fixture-mutants-caught-0/29-redundant-29
