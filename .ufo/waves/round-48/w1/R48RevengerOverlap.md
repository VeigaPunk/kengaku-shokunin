# R48RevengerOverlap — reverse-engineered C1/C2 attack surface over all 64 wave items

**Axes named:** calibration (R48-C1) and coverage (R48-C2). This seat makes no admission judgment, no
score, and no scored measurement.

**Revision inspected:** `REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze; inspection only) and
`REV bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (lane tip, presence check only). No counter, probe, fence,
gate or mutant was executed; no receipt was produced, so the REV lines above name inspected trees, not
measured ones.

**Freeze check (basis for making no scored run).** The stage-1 freeze exists in the committed lane tree:
`plans/round-48-claims.md` at `a543d920` hashes `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672`,
identical to the worktree copy, and no commit after `a543d920` touches it
(`git log --oneline a543d920..HEAD -- plans/round-48-claims.md` → empty). Stage 2 — the counter files, the
frozen populations, the literals `<P> <H> <S> <B> <M>` / `<V> <N>` and the before-control receipts — is
absent: `git ls-tree -r --name-only a543d920 plans/ | grep -c round48` → `0`, and the same filter at `bf783c1`
prints nothing. `.ufo/waves/round-48/claims/` holds only `README.txt` and `freshness-r48.txt`; there are no
control receipts. Because the claims date stage 2 *after* wave 1 returns and before any claimed work is
scored, every item whose named output is a measurement is unfreezable in this wave. That is finding **S1**,
not a local excuse.

## Command log (exact; cwd is the fleet root unless stated)

```text
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48RevengerOverlap ; export TMPDIR=<that dir>
git -C <lane> log --oneline -3        → bf783c1, 453ddfd, a543d92
git -C <lane> cat-file -t a543d920…   → commit
git -C <lane> merge-base --is-ancestor a543d920… HEAD → exit 0 (stage-1 is an ancestor of tip)
git -C <lane> log --oneline a543d920..HEAD -- plans/round-48-claims.md → (empty)
git -C <lane> show a543d920:plans/round-48-claims.md | sha256sum
  → 87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672
sha256sum <lane>/plans/round-48-claims.md → same digest
git -C <lane> ls-tree -r --name-only a543d920 plans/ | grep -c round48 → 0
git -C <lane> ls-tree -r --name-only HEAD plans/ | grep round48       → (no output)
git -C <lane> log -1 --format='%H %ci %s' a543d920
  → a543d920… 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 … and C2 … claims
ls <lane>/plans/refusals46 | wc -l → 20      ls <lane>/plans/sealed46 | wc -l → 12
find plans/battery42|43|44 -maxdepth 1 -type f | wc -l → 5 + 7 + 10 = 22 module files
git -C <lane> show a543d920:plans/fixture_fence.py | sha256sum
  → 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
git -C <lane> show a543d920:plans/round46_c1_verify.py | grep -nE 'print\(f?"(PINS|REFUSALS|SEALED|HONEST|BENIGN|CALIBRATION|PREDICATE)'
  → lines 492, 590, 595, 603, 606, 627 (no BENIGN print exists: delta (b) has no output line in the frozen predicate)
git -C <lane> show a543d920:plans/round46_c1_verify.py | grep -nE 'FLOOR|HONEST_TOTAL|contradicted'
  → 190 REFUSAL_FLOOR = 20, 191 SEALED_FLOOR = 12, 192 HONEST_TOTAL = 104,
    605 contradicted = rleaked + rread + rhung + rbuild + sleaked + sread + shung + sbuild
git -C <lane> show a543d920:plans/round46_c3_verify.py | sed -n '1,130p'
  → legs V1–V13, SUBSTANTIVE = ("V3","V4","V7","V9","V10","V12"), DRY_SHA256 pin for V5, V11 hardening
python3 (scratch) load w1-spec.json → 64 items; per-item `# Item` text extracted and grepped
grep on the 64 item texts: io_uring → 0 ; census → 1 (report census only) ; predictor → 0 ; advertis → 0 ;
  strace → 0 ; hostile → 0 ; 'BASE fence' → 1 (ExecHonest only) ; 'landed fence' → 1 (HoMount only)
grep -l -iE 'BLOCKED|INCONCLUSIVE' .ufo/waves/round-48/w1/*.md → 11 of 30 landed reports
```

No `lsp` device is mounted in this seat's inventory (`read xd://lsp` → "No such tool"), so references/
definition queries were unavailable; the leg definitions cited below were read directly from the committed
counter sources and the fence, not inferred from names.

## Reconstructed attack surface

Surfaces are the measurable units the two frozen predicates and kill rules actually bind: 16 for C1 and 19
for C2. A seat counts for a surface only when its own `# Item` names that measurement. Seat prefixes are
elided (`ExecFenceA` = `R48C1ExecFenceA`).

### C1 — 16 surfaces (claims §C1 predicate, deltas (a)–(e), envelope B1/B3/B4/B5/B6, kill rule)

| surface | seats | seats naming it |
|---|---|---|
| PIN — pin integrity (`PINS total=<P> mismatched=0`) | 1 | MutCounterPins |
| REF — 20 refusals refused, zero traced outside | 6 | ExecFenceA, ExecFenceB, MutGit, MutBoundary, ExecControls, Rerun |
| SEA — 12 sealed + new held-out, refused | 3 | ExecFenceA, ExecFenceB, RevNoHarm |
| HON — honest population admitted, `refused=0` | 13 | ExecFenceA, ExecFenceB, ExecHonest, HonestInv, CritPop, ScoutPop, Rerun, Overrefusal, HoArgv, HoPaths, HoStore, HoConfig, HoMount |
| BEN — `BENIGN-ADMIT` classification (delta b) | 4 | HoArgv, HoPaths, HoStore, HoConfig |
| CAL — `CALIBRATION advertised=<20+S> contradicted=0` | **0** | — |
| B1 — strace log integrity | **0** | — |
| B3 — whole-scratch-root touch scope | 2 | MutBoundary, HoPaths |
| B4 — verdict channel (exit status) | 1 | MutExit |
| B5 — stat/readlink/access channel | **0** | — |
| B6 — blocked/pending calls | 1 | MutPending |
| Q39 — name hiding | 1 | MutNames |
| MUT — fence-mutant floor (≥12 mutants, floor `M/2`) | 3 | MutGit, MutBoundary, MutPending |
| PRV — authoring provenance (base-fence description) | **0** | — |
| LIM — named limits (host paths outside scratch root, untraced channels) | **0** | — |
| SEP — falsifiability / separability | 1 | RevClaim |

### C2 — 19 surfaces (inherited V1–V13, frozen deltas (a)–(e), predicate `checks=<V> defects=0`)

| surface | seats | seats naming it |
|---|---|---|
| V1 — capture manifest (8 files, digests) | 1 | MutPins |
| V2 — package gate (spec+gate pins, `--rerun` accept) | 6 | ExecProbe, PosControl, Filler, Echo, ExecControls, MutPins |
| V3 — anchor digests / 11-cell registry rows | 5 | MutPins, MutNames, MutDup, Filler, Echo |
| V4 — receipt vs dry table, summary, `match=` lines | 5 | MutReceipt, MutDup, MutNames, Filler, Echo |
| V5 — probe digest + `--dry` byte-equality | 3 | ExecCases, ExecProbe, MutPins |
| V6 — `sources-census.sh validate` | **0** | — |
| V7 — requirement map + all-tag violating cases | 4 | ExecCases, TagInv, RevAdmission, MutTags |
| V8 — order proof / pre-receipt P10 | 5 | ExecCounter, ExecProbe, ExecControls, PreReceipt, MutOrder |
| V9 — content consistency (table, rows, PROVINCE, frontier) | 7 | ScribeEntry, ScoutEntry, MutReceipt, MutNames, MutDup, Filler, Echo |
| V10 — mechanism rows quoting DECISIVE lines | **0** | — |
| V11 — held-out predictors + round-45 refusal lint | **0** | — |
| V12 — anchor-line rule (line N, range, word count) | 2 | SourceReopen (one row), Filler (indirect) |
| V13 — filler control | 2 | Filler, ExecControls |
| V14 — package-mutant battery (`<N>/2` floor) | 6 | ExecMutBattery, MutTags, MutPins, MutReceipt, MutNames, MutDup |
| V15 — preconditions dry-run (a leg never scores on a bad input) | 2 | ExecCounter, MutPins |
| VCNT — `checks=<V>` leg-count literal | **0** | — |
| CTL3 — three before-controls (base, filler, echo) | 4 | ExecControls, CritDoNothing, Filler, Echo |
| ORD — stage-2 ordering, P10 disabled | 5 | ExecControls, PreReceipt, MutOrder, ExecProbe, ExecCounter |
| SEP — separability (cross-claim) | 2 | ConnCross, RevClaim |

Density: 35 surfaces, 95 seat-attacks, but **9 surfaces have zero attackers** and 6 more have exactly one.
C1 spends 13 of 30 seats on one line (`HONEST`); C2 spends 7 on V9 and 5–6 each on V2/V3/V4/V8/V14, while V6,
V10, V11 and the leg-count literal are unowned.

## Measurements attacked twice without need

Judgment rule used: a repeat adds information only when (i) a seat could *pass* where another failed, (ii)
the second seat re-executes a **scored** result (Q22 independence), or (iii) it mutates in a different
direction from a property measurement. Controls whose expected outcome is already committed failing
evidence, single-URL provenance artifacts, and static text properties fail that test.

| id | measurement | seats | disposition |
|---|---|---|---|
| D1 | C1 base-fence do-nothing control (one control in claims §Do-nothing) | CritBase, ExecControls (#2), Rerun (base leg) | **fold** — ExecControls owns the control receipt; CritBase's guard is already committed (`control-c1-base-fence.txt`, r46); Rerun keeps only the landing-tip re-run |
| D2 | C1 keyed / path-keyed fence bypass | PredCounter (constructs), ExecControls (#6 "name-keyed variant") | **fold + freeze** — the 6th control is **not in the frozen five**; and the r45 keyed fence *was* name/path-keyed (`/refusals45-` in the path), so #3 and #6 duplicate each other inside one seat |
| D3 | C1 `HONEST … refused=0` disposition line | 13 seats; 7 author fixtures (ExecHonest, Overrefusal, HoArgv, HoPaths, HoStore, HoConfig, HoMount), 6 re-measure | **partial fold** — keep ExecHonest (population), Overrefusal (independent/held-out authoring), HonestInv (audit), HoMount (frozen mount obligation); fold HoArgv/HoPaths/HoStore/HoConfig into one class-expansion seat (each re-measures the same line; HoArgv also re-covers the 2 frozen r46 argv held-outs) |
| D4 | C1 counter re-execution | Rerun, ExecFenceA, ExecFenceB, ExecControls | **keep** — A/B are candidate receipts, ExecControls the controls, Rerun the non-author re-run |
| D5 | C2 base (no-package) control | CritDoNothing, ExecControls | **fold** |
| D6 | C2 filler control | Filler, ExecControls (V13 leg) | **fold** — one execution of the filler package, per-leg table produced by that run |
| D7 | C2 echo control | Echo, ExecControls | **fold** |
| D8 | C2 V7 tag→violating-case map | TagInv, RevAdmission | **merge** — both enumerate the same committed bytes. Worse, both are **stale by construction**: TagInv's own receipt measures the pre-amendment table (`5/7`, `both-print`/`toolchain` empty), i.e. the r46 state, not the r48 fix |
| D9 | C2 V8 / P10 ordering property | PreReceipt, MutOrder, ExecControls, (+2 implementers) | **keep** PreReceipt (property) and MutOrder (sensitivity); ExecControls' ordering pin is the receipt; drop the duplicate design work (D13) |
| D10 | S166 re-open (URL + date + ≤25-word quote) | SourceReopen, ScribeGate | **fold** — claims §2b requires "a wave seat"; the artifact is one quote |
| D11 | PROVINCE ownership boundary | ConnPrior, Scope | **fold** — Scope is a narrower framing of the same question |
| D12 | causal separability | RevClaim, ConnCross | **fold to ConnCross**; RevClaim should spend its budget on the kill rule's cheap pass (S8) |
| D13 | P10-disabled gate mechanism | ExecProbe ("design the P10-disabled gate mode"), ExecCounter (V8 leg) | **conflict, not just duplicate** — two executors own one design decision that the frozen text does not name |
| D14 | mutant kill recording | ExecMutBattery executes the mutants that MutTags/MutPins/MutReceipt/MutNames/MutDup also execute and score | **merge** — producers author + declare the expected flip; the battery is the single executor/receipt owner |

## Frozen legs no seat attacks

| id | unmeasured surface | frozen text it leaves unmeasured | why it matters |
|---|---|---|---|
| U1 | **CAL `advertised/contradicted`** | "`CALIBRATION advertised=<20+S> contradicted=0`" | see S3: the contradicted numerator (counter line 605) cannot express delta (b) |
| U2 | **B1 log integrity** | "the strace envelope B1/B3/B4/B5/B6 legs retained" | a fence that truncates/unlinks the strace log passes; r46's B1 exists precisely to count that as READ, and no mutant targets it |
| U3 | **B5 stat/readlink channel** | same | a fence that only *stats* outside paths escapes an opens-only witness; HoStore/HoPaths touch it only incidentally |
| U4 | **PRV authoring provenance** | "each authored against the *base* fence description, not against any repaired fence" | only ExecHonest's item carries the constraint; 6 other authoring seats may lawfully author against a candidate fence, contaminating H |
| U5 | **LIM named limits** | r46 counter: host paths outside the scratch root are uncounted; `io_uring` SQE opens emit no traced syscall | delta (b) makes *traced* access the only LEAK, so these limits become the cheapest way to admit a hostile module without a kill |
| U6 | **SEA growth** | "plus the wave-1 held-out hostile modules authored against the landed fence (count `<S>` pinned at stage 2)" | `hostile` appears in **zero** of the 64 items; no seat authors one (see S2) |
| U7 | **V6 census** | "V6 census: `scripts/sources-census.sh validate --file …/corpus/SOURCES.md` exits 0" | SOURCES rows S166–S172 are part of the claimed package; a stale/duplicate row is unmeasured |
| U8 | **V10 mechanism** | "V10 mechanism: `## Mechanism` rows per receipt case citing a frozen DECISIVE line" | V14 requires a mutant that flips V10, but no seat owns V10 at all |
| U9 | **V11 predictors + lint** | "V11 held-out predictors retained with the round-46 refusal lint" | r45 fielded `R45CritV11Bypass`; r48 fields no V11 adversary — the only leg that executes arbitrary entry-supplied code is un-attacked |
| U10 | **VCNT leg count** | "`<V>` and `<N>` fixed at stage 2 (`<V>` must count every leg above including V14 and V15)" | `checks=len(which)` is self-reported; a counter that omits V11 prints `checks=14 defects=0` |
| U11 | V1 set completeness; V15 "never a crash" semantics; V12 line-N/range/word-count edges | "lists exactly the eight captured files"; "a missing/tamper-pinned input is a DEFECT of that leg, not a crash" | extra capture file, precondition-failure behaviour and off-by-one line refs have no adversary |

## Structural defects in the frozen attack surface (found before any scoring)

- **S1 — temporal inversion.** The round is one batch ("ONE v2 build-and-attack wave"; `counts.spawn=64`), yet
  stage 2 lands only "after wave 1 returns". **36 of 64 items** have a measured outcome as their named
  deliverable (19 of 30 C1, 17 of 30 C2); their subject does not exist when they run. Landed evidence agrees:
  11 of 30 reports already end BLOCKED/INCONCLUSIVE (`R48C1CritBase`, `R48C1MutBoundary`, `R48C1MutNames`,
  `R48C1Rerun`, `R48C1PredCounter`, `R48C2Filler`, `R48C2MutDup`, `R48C2MutTags`, `R48C2MutVerdict`,
  `R48C1ConnPattern`, `R48C1ConnOverlap`). Both kill rules depend on wave-1-authored mutants
  ("`<M>` fresh mutants of the landed fence", "`<N>` fresh mutants of committed package bytes"), and the
  landed fence is chosen *after* wave 1 — so neither floor can be evidenced this round.
- **S2 — SEALED is de-held-out and may not grow.** r46 sealed modules were "hostile modules authored in wave 1
  by critic seats that no fence-writing seat reads". r48 tells the fence authors to satisfy them ("while all
  20 refusals46 + 12 sealed46 modules remain refused"), and no seat authors new held-out modules against the
  landed fence. With `S=12`, `advertised=20+S=32` is exactly the r46 number: C1 can be admitted having never
  faced a hostile module its author did not see.
- **S3 — delta (b) cannot be expressed in the frozen predicate lines.** The r46 `SEALED` rollup is
  `clean | LEAKED (a fixture admitted) | READ | HUNG`, and `contradicted` sums `leaked+read+hung+build` over
  both hostile legs. Delta (b) redefines LEAK as traced access only and says an admitted `touches=0` fixture is
  "reported as `BENIGN-ADMIT` and counted separately" — but the frozen lines have no BENIGN column and adding
  one would change a predicate line, which stage 2 may not do. Read one way, an admitted hostile module with
  no trace prints `SEALED … leaked=0` and `contradicted=0` (kill rule blind). No seat measures either reading.
- **S4 — honest population authorship is unfrozen and internally contradictory.** Delta (a) builds H from the
  104 battery fixtures, the 9 r46 classes, and "the novel honest classes authored by **wave-1 critic seats**",
  while the seat that authors the new classes is an **executor** (ExecHonest, "author 6+ NEW novel honest
  classes"); Overrefusal is required to author "beyond the frozen set", yet under delta (a) critic-authored
  classes *are* the frozen set. There is no honest held-out registry, unlike SEALED for hostile modules, so a
  representativeness test has no defined population to be held out from.
- **S5 — literal conflicts with the item texts.** `<N>` is unfrozen at stage 2, but ExecMutBattery hardcodes
  "the 13-mutant battery … `>= floor(13/2)` killed"; `<V>` is unfrozen while `checks=<V>` is the pass line;
  `<S>` growth would require editing `SEALED_FLOOR = 12  #… exact, not a floor` in the imported counter, which
  no frozen delta names.
- **S6 — the V7 fix breaks inherited V5.** V5 requires the probe's `--dry` output to be byte-equal to the
  frozen dry table *at its pinned digest* (`DRY_SHA256`), while ExecCases must amend that same 18-case table.
  v4 must therefore re-pin and re-mean V5, which the frozen deltas (a)–(e) do not authorize. Two C2 seats own
  one artifact with incompatible requirements.
- **S7 — design collision on P10-disable** (D13): the one mechanism V8's fix depends on is claimed by both an
  executor that owns the counter and an executor that owns the probe.
- **S8 — the cheapest pass is unreviewed.** C1's kill rule fires only on HONEST refusal, traced hostile
  admission, or a sub-floor mutant catch rate; C2's only on a V defect or a sub-floor battery. With S2, S3 and
  U5–U6 unfilled, both claims have a pass path that no seat in this wave attacks. RevClaim is the only seat
  aimed at it, and it is also asked to carry separability (D12).
- **S9 — claim author as sole post-freeze measurer.** After stage 2, the only actor that can run the scored
  predicates is the L1 (single integrator), because there is no second wave. R48-C1 exists to repair a
  *self-assessment* defect; at round level it reproduces one: the fence's judge is written in the wave that
  writes the fence, and the measurement has no adversarial seat.

## Confidence

- High (read directly from committed bytes): the freeze state and digests, the 64 item texts, the leg lists of
  `plans/round46_c1_verify.py` / `plans/round46_c3_verify.py`, the `contradicted` formula, the floors, the
  zero-attacker surfaces U1–U3/U7–U10, and duplicate groups D1–D14.
- Medium: the measurement-dependence count (36/64) — classification of each item's named output; borderline
  items (`ExecFenceA/B` receipts, `PreReceipt`, `Sandbox`) are marked A only because a candidate/dry path exists.
- Inference (marked): that no second wave exists in round 48 — inferred from the spec's "ONE v2 build-and-attack
  wave", `counts.spawn=64`, and the absence of any w2 item set; if the L1 opens a stage-2 measurement pass, S1
  and S9 weaken and the U-list becomes the pass's required agenda.
- Inference: severity ordering of duplicates assumes the L1 wants one receipt per frozen control; if the L1
  wants two independent witnesses per control, D1/D5–D7 become warranted and only D8/D10–D13/D14 survive.

## Limits

No scored counter/probe/gate/fence/mutant execution was run and none was warranted: stage 2 is absent, so a
measured run would either use an unfrozen detector or a stale one. No claim admission is asserted. I did not
open the external terminal-bench URL; no external source was fetched. Absence findings (U-list) are absences of
a named target in the 64 item texts, read literally, plus the absence of a `hostile`/`predictor`/`census`/
`advertis` target anywhere in them — not proof that a seat cannot improvise one. Scratch
`/fast/scratch/hyaku/kengaku-r48/R48RevengerOverlap` was created, used only for the item-text extraction, and
removed before this report was filed; no lane production file was touched, nothing was staged or committed, no
pacman/uv/npx install occurred.

## Sources opened (all local; access date 2026-10-27 unless noted; ≤25-word located quotes)

1. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — “Stage 2 (one amendment
   commit, after wave 1 returns and BEFORE any claimed work is scored)” (15 words).
2. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` —
   “wave-2 reports count 3 admitted held-outs (2 argv, 1 paths)” (10 words).
3. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md` — “fence mutants 2/13 caught” (4 words;
   round-46 wave-2 C1 row).
4. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1-spec.json` — “ONE v2
   build-and-attack wave” (5 words); 64 items enumerated.
5. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1-dispatch.json` — “`"spawn":
   64`” (counts block; one batched task call).
6. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` @ `a543d920` — “hostile
   modules authored in wave 1 by critic seats that no fence-writing seat reads” (15 words).
7. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c3_verify.py` @ `a543d920` — “a fixed
   public state set is memorizable three ways” (9 words; V11 hardening).
8. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` @ `a543d920` (sha256
   `05d5fe03…`) — “admit only a fixture whose git store, discovered repos and argv stay inside” (12 words).
9. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1CritBase.md` —
   “STAGE2_C1_UNAVAILABLE” (control seat's blocker marker).
10. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2TagInv.md` — “5/7 tags
    have at least one executable violating case” (8 words; shows the pre-amendment table was measured).
11. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1PredCounter.md` — “keys
    on the counter's fixture path prints the same pass” (10 words; r45 keyed-control identity).
12. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2ConnCross.md` —
    “The counters share no input” (5 words).
13. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2MutTags.md` — “no
    scored counter/probe execution and no mutations” (8 words).
14. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1MutBoundary.md` —
    “no mutants scored” (3 words).

VERDICT: **attack surface reconstructed and defective.** C1: 16 surfaces, 5 unowned (CAL, B1, B5, PRV, LIM),
13 seats piled on one line, and the claim's own repair (delta b) makes the kill rule's witness narrower than
the advertisement it checks. C2: 19 surfaces, 4 unowned (V6, V10, V11, VCNT), V7/V8 attacked by 4–5 seats
each while the leg whose removal would hide a defect (V11) has no adversary. 14 duplicate groups, 8 of them
foldable without losing information. 9 structural defects, of which S1 (36 measurement seats behind a freeze
that lifts after the wave), S2 (SEALED grown by nobody and de-held-out), S3 (BENIGN admissions invisible to
`contradicted`) and S4 (no honest held-out registry) leave **both frozen predicates passable without ever
facing the failure they were written to catch**; the L1 must fix the stage-2 text (S5–S7) before pinning, not
after. No scored run was made; no admission claimed.
