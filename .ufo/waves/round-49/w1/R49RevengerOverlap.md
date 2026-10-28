# R49RevengerOverlap — attack-surface reconstruction, duplicate measurement and unattacked-leg audit

seat: R49RevengerOverlap (revenger, calibration+coverage)
round: kengaku 49, hyaku run 10, wave w1 (v2), 2026-10-28
claims served: R49-C1 (calibration), R49-C2 (coverage) — audit only; no admission claimed
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
Axes named: **calibration** (C1 fence/over-refusal), **coverage** (C2 TB2 grader admission). This seat scores neither axis; it measures whether each axis' frozen legs are actually measured, once.

## 0. Freeze precondition (checked before anything else; no scored run was made)

| check | command | observed |
|---|---|---|
| freeze exists in committed lane tree | `git -C <clone> log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93` | `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims` |
| freeze is an ancestor of the wave tip | `git merge-base --is-ancestor 9d2900a af88aab && echo …` | `9d2900a IS ancestor of af88aab` (`af88aab 2026-10-28 09:18:20 -0300 round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)`) |
| clone state measured | `git status --porcelain`; `git rev-parse HEAD`; `git rev-parse --show-toplevel` | `porcelain-lines=0`; `HEAD=9d2900af41e4d1fc6022eff99010436fde6dbd93`; toplevel = my scratch lane clone |
| stage-2 artifacts do not exist yet (expected) | `git ls-tree -d --name-only af88aab -- plans/honest49 plans/sealed49 plans/mutants49 …` | only `plans/battery42|43|44`, `plans/refusals46`, `plans/sealed46` exist; `honest49/sealed49/mutants49` absent; `plans/round49_c1_verify.py`, `plans/round49_c2_verify.py`, `plans/pkg-spec-r49.json` absent at the tip |

**Ordering note (not a blocker, but a provenance defect for the L1).** `corpus/lessons/round-48.md`-style provenance in `plans/round-49-claims.md` says the run launched at `2026-10-28T08:59:38-03:00` (verified in `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1823` — `launch kengaku round=49 pgid=3953023 driver=hyaku-inline attempt=1`). The stage-1 freeze commit is `09:14:40`, i.e. **~15 minutes after the launch line**, and the wave spec that seats are dispatched from is `09:18:20`. So the freeze predates every possible seat measurement (dispatch cannot precede the spec commit), but does **not** predate the run launch. The claims' own header — "Freeze shape (declared now, before any data)" — is true for data (measurements) and false for launch; a closure reviewer reading the watchdog line first can reasonably read this as a post-launch freeze. `[INFERENCE]` on "no seat measured before 09:18:20": dispatch is generated from `w1-spec.json`, committed at 09:18:20, so no earlier dispatch existed. Recommend the L1 state the two timestamps explicitly rather than the present "no earlier attempt exists" sentence.

## 1. Method

1. Read `plans/round-49-claims.md` in full (every C1/C2 predicate line, control list and kill rule) and `corpus/lessons/round-48-verifier-spotcheck.md` (routed defects 1–4).
2. Enumerated the 64 dispatched seats from `.ufo/waves/round-49/w1-spec.json` @ `af88aab` (keys: `name, role, item, axes, milestone`; role census: `critic 15, mutation-tester 14, executor 11, reviewer 11, scribe 4, connector 4, scout 3, sentinel 1, revenger 1`).
3. Extracted each seat's `# Item` body verbatim (the `# Target` / `# Evidence and boundaries` preamble is identical boilerplate for every seat and is excluded so it cannot pollute the scan) and ran a per-leg regex scan over the 64 bodies. Leg vocabulary was taken from the claims text and from `plans/round46_c3_verify.py:25-56` (V1…V13 are defined there; V14/V15 are new in round 49) and `plans/round46_c1_verify.py:22-45,73-81` (PINS/REFUSALS/SEALED/HONEST/CALIBRATION, floors).
4. Verified frozen populations at the base: `plans/refusals46/*.py`=20, `plans/sealed46/*.py`=12, batteries 42/43/44 = 5+7+10 modules (=104 fixtures, matching `HONEST_TOTAL = 104` at `plans/round46_c1_verify.py:192`), and `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/`=16 — the population the claim's `<H>` extends.
5. Cross-checked each claimed leg against the seat that **produces** it and the seat(s) that **attack** it. A leg is "attacked" only where a seat's item asks for a measurement that can falsify that line; mere mention of the counter is not counted.

## 2. Reconstructed attack surface — C1 (31 seats: items 01–31; 21 of them attack roles)

| C1 surface (frozen line / rule) | producer seat | attacking seat(s) | notes |
|---|---|---|---|
| `PINS total=<P> mismatched=0` | 01 ExecCounter (leg), 04 ExecHonest (digests) | 24 MutCounterPins | single attacker; no seat recomputes `<P>` for the stage-2 dir set (see G8) |
| `REFUSALS total=20 clean=20 …` | r46 frozen (`plans/refusals46`), no new producer | 02 FenceA, 03 FenceB, 11 Rerun, 30 RevNoHarm | well covered |
| `SEALED total=<S> clean=<S> …` | **none for `plans/sealed49/`** (01 only renames the path) | 02 (the 12 `sealed46` only), 03, 30 | **producer missing — G1** |
| `HONEST fixtures=<H> admitted=<H> refused=0` | 04 ExecHonest (authoritative), 10 ScoutPop (survey), 13 Overrefusal (author), 18 HoMount (mount class) | 02, 03, 11, 12 HonestInv, 29 CritPop | 9 seats touch it — proportionate (this is the claim's core), but three authors overlap — D3 |
| `BENIGN total=<B>` (informational, never in the kill rule) | 01 | 14 HoArgv, 15 HoPaths, 16 HoStore, 17 HoConfig | 4 attack seats on a non-kill leg |
| `MUTANTS total=<M> caught=<k> floor=<M>/2` | 26 MutBattery (≥14 mutants), 01 (leg) | 11 (all fields), 31 RevClaim | floor arithmetic verified only by 11/31 — acceptable |
| `CALIBRATION advertised=<20+S> contradicted=0` | 01 | **none** | **G5** |
| 6 controls (no fence; base @3a548330; r45 keyed; admit-all; refuse-all; name-keyed) | 05 ExecControls runs all six | 28 CritBase (= control #2), 27 PredCounter (= control #3/#6 family) | no-fence, admit-all, refuse-all have exactly one runner; the duplicated ones are the already-answered ones — D1, D2 |

## 3. Reconstructed attack surface — C2 (29 seats: items 32–60; 17 attack roles)

| C2 leg (from `plans/round46_c3_verify.py:25-56` + claims a–f) | producer seat | attacking seat(s) | notes |
|---|---|---|---|
| V1 capture manifest (8 files) | — | **none by name**; indirect only via 36 ExecMutBattery's `capture` target | G6 |
| V2 package gate / P10-disabled wrapper | 37 ExecSpec | 35 ExecControls, 45 PreReceipt, 50 MutOrder | covered |
| V3 anchor digests | 34/37 (rows/spec) | 36, 46 PosControl, 51 (spec tamper) | covered |
| V4 receipt | 33/34 (receipt content) | 43 Rerun, 53 MutReceipt, 48 Echo, 54 MutDup | covered (2 overlap — D8) |
| V5 frozen probe + `--dry` byte-equality | 33 ExecProbe (repair), 34 (CASES) | 51 (probe tamper), 43 | see G7: nobody stage-checks the **merged** probe |
| V6 census (`scripts/sources-census.sh validate`) | — | **none** (only 62 RevReport cites the census for the report) | **G4** |
| V7 requirement map / 7 tags | 34 ExecCases (author), 39 ScribeEntry (draft) | 44 TagInv, 58 RevAdmission, 49 MutTags | 44 and 58 are the same enumeration — D7 |
| V8 order (`first-commit == stage-3` descendant of stage-2) | 32 ExecCounter (rule), 37/35 (order_check) | 45 PreReceipt, 50 MutOrder, 58 (order half) | well covered |
| V9 content consistency / case inventory | 34 | 54 MutDup, 53 | covered |
| V10 mechanism (DECISIVE line per case) | 39 (entry rows) | **none by name**; indirect via receipt/entry mutations (36, 53) | G6 |
| V11 held-out predictor + r46 refusal lint | **none** ("retained" from r46) | **none** | **G2** |
| V12 anchor-line rule | 39 | **none by name**; indirect via 36 `spec` target | G6 |
| V13 filler package | r46 frozen `plans/filler46/` | 47 Filler **and** 35 ExecControls (control #2) | exact duplicate — D4 |
| V14 mutation floor (`<N>/2`) | 36 ExecMutBattery (≥14) | 43, 52 MutVerdict, plus 49/50/51/53/54 component mutants | most-attacked leg (7 seats); proportionate to a new kill leg |
| V15 preconditions ("missing/tamper-pinned input is a DEFECT of that leg") | 32 ExecCounter (leg) | **none** for missing/unparseable inputs; 51 covers *tamper* only | **G3** |
| 3 controls: base tree / filler / echo | 35 ExecControls runs all three | 57 CritDoNothing (= base), 47 (= filler), 48 (= echo) | every control is re-measured once — D4–D6 |
| `--stage-check` gate on the stage-2 probe revision | 33 ExecProbe | **33 only** | G7 |
| S166 reopen (claim's §2b basis) | 55 SourceReopen, 38 ScribeGate | — | fine (independent reopen + scribe record) |

## 4. Measurements attacked twice without need

Each row names the **same** artifact and the **same** expected output measured by two seats. "Added discrimination" = what the second seat can learn that the first cannot.

| id | measurement | seats | added discrimination | verdict |
|---|---|---|---|---|
| D1 | base fence `@3a548330` vs the v3 counter ("do-nothing") | 05 ExecControls control #2, 28 CritBase ("run the cheapest do-nothing control") | none — 05 already runs exactly `base fence @3a548330`; r48 already measured the outcome (`HONEST fixtures=120 admitted=112 refused=8`, `PREDICATE R48-C1 fail`, `w1/R48C1ExecCounter.md`), so 28's "if it reaches target" question is answered by a committed receipt | **redundant** — retire 28 or re-point it at a control that has no second runner (admit-all / refuse-all) |
| D2 | keyed fence cannot pass v3 | 05 controls #3 (r45 keyed) and #6 (name-keyed), 27 PredCounter ("keyed or path-keyed fence") | a third key shape only | **partly redundant** — keep 27 only if pinned to *path*-keyed (distinct key source from the name-keyed control); otherwise it repeats control #3 |
| D3 | new honest classes beyond the frozen set | 04 ExecHonest (authoritative author: "replace refs, shallow partial clone state, …"), 10 ScoutPop (survey: "stash entries, .gitmodules, replace refs, grafts, shallow files, …"), 13 Overrefusal (author: "replace refs, shallow clone, packed-refs with peeled tags, stash, .gitmodules") | 10 ranks by git-doc evidence (distinct); 13 re-authors ≥4 of the same classes 04 owns | **redundant authoring** — two independent class sets both claim to be "novel honest", which makes `<H>` ambiguous for 12 HonestInv. Fix: 13 keeps its classes *out* of `plans/honest49/` (verification-only held-out), so the denominator stays single-owner |
| D4 | filler package under the v4 counter (V13) | 35 ExecControls control #2, 47 Filler | none — 47's item ("whether a committed filler package with plausible rows/entry can clear the v4 counter") *is* the control | **redundant** — 47 should either be retired or be strengthened into a *pass* attempt (a filler that survives V13's ≥3-substantive-defect rule), which is the open risk from r37 |
| D5 | echo receipt (dry table copied as receipt) | 35 ExecControls control #3, 48 Echo | none as worded | **redundant** — keep 48 only if it forges a receipt whose digest matches the pinned receipt byte for byte (a strictly stronger artifact than the verbatim copy) |
| D6 | base tree, no `plans/polyglot_c_py_probe.py` | 35 ExecControls control #1, 57 CritDoNothing | none — both expect `PREDICATE R49-C2 fail` with the same content defects | **redundant** — retire one; the receipt is already a frozen stage-2 control |
| D7 | V7: every frozen tag has a violating case | 44 TagInv ("enumerate every frozen tag and map it to its violating case … fail any tag lacking an executable violation"), 58 RevAdmission ("independently adjudicate whether every frozen tag has a violating case and the order proof holds") | 58's *order* half only | **redundant on V7** — 44 is the canonical V7 answer (it is the routed-defect-3 fix). Restrict 58 to the V8 order proof, or drop 44 |
| D8 | receipt-byte tamper detection | 51 MutPins ("one digest-pinned component at a time (capture/probe/spec/receipt/dry table)"), 53 MutReceipt ("modify receipt bytes … while preserving case labels") | 53's label-preservation variant is strictly stronger in the receipt dimension | **partly redundant** — remove `receipt` from 51's sweep |
| D9 | causal separability of C1 vs C2 | 31 RevClaim ("flag any dependence on C2 artifacts"), 41 ConnCross ("hidden shared inputs or counter dependencies that would break causal separability") | none — the property is symmetric and both seats read the same `## Separability` paragraph | **redundant** — one seat suffices (41, which has both counters in view) |

Explicitly **not** flagged, because they are adjacent but measure different things: 12 HonestInv (admission expectations per fixture) vs 29 CritPop (denominator exclusions/duplicates); 45 PreReceipt (constructs a bypass) vs 50 MutOrder (mutates the gate); 46 PosControl (pass without executing the probe) vs 57 (plain no-package control).

## 5. Frozen legs no seat attacks

Severity is against the claims' own kill rules: a leg that can alone flip `PREDICATE … fail` and has no attacker is the expensive case.

| id | leg | evidence of absence | severity |
|---|---|---|---|
| **G1** | **C1 `SEALED` second half: "the wave-1 held-out hostile modules authored against the landed fence candidate, committed at stage 2 under `plans/sealed49/` (count `<S>` pinned at stage 2)"** (claims, delta (e)) | scan of all 64 `# Item` bodies: `held-out|novel hostile|hostile module` → **0 seats**; `sealed` → only 01 ExecCounter, which merely renames `SEALED_REL`; 02/03 measure the frozen 12 only; 30 RevNoHarm reasons about a leak without authoring a module | **blocking.** `<S>` cannot be filled as written. Stage 2 "may fill literals and pins; it may not change a predicate line", so the only honest outcomes are `<S>=12` with the (e) sentence unmet, or a wave-2 seat. Note the precedent: `plans/round46_c1_verify.py:29-31` records SEALED as "hostile modules authored in wave 1 by critic seats" — round 46 had that producer, round 49 has no equivalent item. Also note the structural wrinkle: an authoring seat must read a wave-1 repair candidate, and L1 may land a *different* variant (A vs B), so "authored against the landed fence candidate" is not satisfiable by construction for the losing variant — the honest wording is "authored against a wave-1 candidate and not used to fit the landed one" |
| **G2** | C2 **V11** "held-out predictors retained with the round-46 refusal lint" (claims, delta (f)); V11 counts in `<V>` | scan `predictor|predict\(` → **0 seats**; 42 ScoutEntry reads the entry against captures but not the predictor; 58 adjudicates tags/order only | **high** — a stale r46 predictor (trained on the r46 case table, which is being amended) can DEFECT the attempt while no seat measures it before the receipt. The claim calls V11 "retained", but retention without an attack is exactly the r48 failure mode (a leg nobody executed) |
| **G3** | C2 **V15** "every frozen input digest resolves and every leg's frozen table parses before any leg scores; a missing/tamper-pinned input is a DEFECT of that leg, not a crash" (new, routed-defect-3 answer) | scan `precondition|V15|missing|parses` over bodies → 1 hit, 47 Filler, unrelated; 51 tampers digests (mismatch), which is not *missing* and not *unparseable* | **high** — the leg that is supposed to fail the freeze *before* scoring is itself unscored |
| **G4** | C2 **V6** census | scan `census|SOURCES\.md` → 62 RevReport (report structure) and 38 ScribeGate (lesson text); neither runs `scripts/sources-census.sh validate` against the package | medium-low (external, stable script; but V6 is in `defects=`) |
| **G5** | C1 `CALIBRATION advertised=<20+S> contradicted=0` | scan `advertis|contradicted` → 01 (builds the line) and 08 ConnOverlap (unrelated context); no seat re-derives it | low (derived arithmetic; a distinct-module miscount would hide here) |
| **G6** | C2 **V1**, **V10**, **V12** attacked only indirectly | no seat body names the capture manifest, the `## Mechanism` DECISIVE-line rule, or the re-implemented anchor-line rule (`anchor` → 09 ConnPattern, comparing `anchor_line_check.py` as a pattern, not running V12) | low — 36's declared targets (`capture, entry, receipt, dry table, spec, probe`) plausibly flip V1/V10/V12, but the mutant set is authored by 36 and never audited against the V-leg list |
| **G7** | `--stage-check` on the **merged** stage-2 probe | 33 ExecProbe repairs hardening and stage-checks *its* copy; 34 ExecCases amends `CASES` in *a scratch copy*; the frozen stage-2 precondition is "the amended probe revision passes `--stage-check`", i.e. the merge of both edits. No seat's item covers the merge | **high** — this is a frozen precondition for the stage-2 commit itself, and it is the one measurement two producers each believe a different seat owns |
| **G8** | evaluation of the **assembled** stage-2 tree (counter × `honest49` × `sealed49` × `mutants49` for C1; counter × spec × dry table × receipt × mutants for C2) | 11 C1Rerun runs "on the exact committed base and on each submitted fence variant" — never on a tree with the new populations/mutants present; 24 mutates pins but does not re-derive `<P>`; C2 is better off because 43 Rerun names "the staged candidate tree" | **medium-high, asymmetric** — C1 has no assembled-tree run at all, so `PINS total=<P>` can be stale/partial (e.g. `<H>`=124 modules but `<P>` still pinning 16) and no seat would catch it. C2's 43 partially covers this; assign an explicit assembled-tree rerun to one seat per claim (or state it as an L1 stage-2 duty in the freeze) |

## 6. Misallocation summary (the one number that matters)

40 attack seats (critic 15 + mutation-tester 14 + reviewer 11) spread over 32 C1/C2 surfaces, but the distribution is inverted against risk:

- 4 seats (14, 15, 16, 17) attack `BENIGN`, which the frozen predicate labels "(informational)" and which no kill rule keys on.
- 9 seats re-measure the three C2 controls (base/filler/echo) or the C1 base fence — all four of which are already-answered "fails trivially" measurements (D1, D4, D5, D6).
- 0 seats attack V11, V15, the `sealed49` producer, or the merged-probe stage-check — the three fresh legs added this round precisely because round 46/48 froze legs nobody executed.

`R49C1ScoutPop` (10) vs `R49C1Overrefusal` (13) is the clearest same-axis duplication: both enumerate "ordinary `git init` states the frozen population lacks", and their class lists intersect on `replace refs`, `shallow`, `.gitmodules`, `stash` — the same four classes 04 ExecHonest is asked to author.

## 7. Limits and inferences

- Every seat's attack surface is reconstructed from its **item text** in `w1-spec.json` @ `af88aab`; no seat output is being judged (the wave is in flight, and `w1/` contains only `swarm-registry.json`). A seat may do more than its item says; it cannot be *credited* with attacking a leg its item never names, which is why the gap table is about ownership, not effort.
- The `# Evidence and boundaries` boilerplate ("capture URL, access date…") is excluded from scans; `# Target` is excluded too, because every C1 item contains "serving R49-C1 (calibration)" and every C2 item "serving R49-C2 (coverage)", which otherwise match every leg scan (observed: a full-text scan returned 35/64 and 64/64 hits for unrelated legs).
- V-leg semantics are taken from the digest-pinned `plans/round46_c3_verify.py` docstring (lines 25–56) plus the r49 deltas in the claims; V14/V15 numbering is the claims' own.
- `[INFERENCE]` G1's blocking severity assumes the L1 will not hand-author `sealed49` modules at stage 2. The claims do permit the L1 to land the fence; authoring hostile modules there would be new work, not a literal/pin fill, and would sit inside the integrator's own measurement.
- `[INFERENCE]` D-table "added discrimination = none" is a judgment about information content given the frozen expected outputs (each control's expected output is fixed in the claims), not a claim that re-running is worthless as an independence check.
- No external source was opened by this seat (no web fetch, no URL, no capture); all evidence is lane-tree bytes at `REV 9d2900af…`. No scored counter/probe run was made; no production file, plan, corpus file, counter, probe or wave artifact other than this report was written.
- Tooling: nothing installed, nothing upgraded, no pacman transaction attempted.

## 8. Scratch

Scratch `/fast/scratch/hyaku/kengaku-r49/R49RevengerOverlap/` (one `git clone --shared` of the lane, detached at `9d2900af…`, `git status --porcelain` empty) contained only the clone and two derived text files (`seats.txt`, `items.txt`) regenerated from the committed `w1-spec.json`. It is removed before this seat yields; nothing citable lives there — every citation above resolves inside `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (`plans/…`, `.ufo/waves/round-4{6,8}/…`, `.ufo/waves/round-49/w1-spec.json` @ `af88aab`).

VERDICT: **surface reconstructed; 9 duplicate measurements (5 redundant, 4 partly redundant, each with a named narrowing); 8 frozen surfaces with no attacker, of which 3 are blocking/high — G1 C1 `sealed49` held-out producer (absent from all 64 items; `<S>` unfillable as written), G2 C2 V11 predictor, G3 C2 V15 preconditions, plus G7 merged-probe `--stage-check` and G8 assembled-tree run (asymmetric: C1 has none, C2's 43 covers it). No scored run, no production edit, no admission.**
