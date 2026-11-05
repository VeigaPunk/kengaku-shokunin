# ConnectorOverlap/report.md — copy of ../ConnectorOverlap.md

Canonical seat report: `.ufo/waves/round-94/w1/ConnectorOverlap.md` (the `Report:` trailer path).
Raw grep/query receipts live beside this file under `receipts/`. Content below is the report copy.

---

# ConnectorOverlap — sibling-overlap scan, kengaku round 94, wave 1

Seat: ConnectorOverlap-37 (leaf; read-only; no absorb). Judged at **T = 90c7677f0ba95d0930d93bda6a14aa50605ebe2e** via a
detached shared clone (`/fast/scratch/hyaku/kengaku-r94/ConnectorOverlap/lane`, removed at yield); sibling trees read at
their own working-tree HEADs, recorded per citation below. Lane master has since moved to d04e6664c4fc — none of the
cited kengaku-at-T files are re-read from the moving tree. Claims doc read in full first (plans/round-94-claims.md).
No installs (nothing beyond stock git/python needed; pacman pause respected). Scratch removed before yield.

Scope per item: every sibling lane `/home/vgpnk/Projects/shokunin/*-shokunin` (21 non-kengaku) **and** fleet `scripts/`;
plus a bonus sweep of the non-lane fleet dirs (counters/, reports/, research/, st2/, wt2/, exp-full/, history-recheck/,
tools/, templates/, kumitate-shokinin/) — zero TB2/freeze-gate signals there. Queries: `terminal.?bench`,
`write.?compressor|data\.comp`, `harbor-framework|2fd12b88`, `frozen.?instrument|--full-history|TREESAME|freeze.?integrity`,
`freeze_integrity|check-freeze|freeze-order|freeze_edited|counter_not_frozen`, `(?i)mutant`, `(?i)(ghidra|dewolf|decompil)`,
`-O3`, `null copy|cli.?path|copy of the (gate|counter)`. Raw excerpts in `receipts/`.

Headline: **(a) nobody else touches Terminal-Bench bytes; (b) kaidoku and mado own real tracked freeze-gate machinery
that is mechanism-adjacent to R94-C2 (complement, cite, never absorb); (c) the decomp -O3 vs grader plain-gcc divergence
is kengaku-owned and no sibling holds any part of it.** Nothing found flips R94-C1 or R94-C2.

## (a) TB2 grader replay / write-compressor / compression-codec / TB2 task bytes

**Verdict: no sibling owns or duplicates any of it. Kengaku is the fleet's sole TB2 grader owner — again.**

Every sibling hit is an echo of kengaku's own bytes, not an owned replay or capture:

- kaidoku-shokunin `.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601,19614` — reservation-time scan
  embedding the *KengakuR41* driver text (PIN `2fd12b88…`, `constraints-scheduling` capture paths). kaidoku's tracked
  tree holds zero TB2 bytes.
- kaidoku r69/r92/r93 and kake r71/r92/r93 connector/scope receipts (e.g. `kaidoku/.ufo/waves/round-69/w1/ConnectorCross/sweep/s4-receipt.txt:185-212`,
  `kake/.ufo/waves/round-92/w1/ConnectorScope/receipts/query-422.txt:74`, `kake/.ufo/waves/round-71/w1/ConnOverlap.md:29-32`
  — "…kengaku = Terminal-Bench…" in the S-homonym survey): all scans *about* kengaku, routed to kengaku.
- kagi-shokunin r30/r33 connector tables (`.ufo/waves/round-30/w1/ConnOverlap-report.md:64,228`, `round-33/build/ConnOverlap.md:73,114-115`):
  "OpenSSL key management **as a benchmark grader surface** (Terminal-Bench `openssl-selfsigned-cert` task)" — explicitly
  kengaku's ground, NO CLAIM/DEFER. Prior connector rounds already settled this adjacency identically.
- kumitate-shokunin `corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83` — a *paper capture* (S197) using
  Terminal-Bench as a benchmark name in MAS-topology research. Zero task bytes, zero graders. The only sibling tracked
  mention of the benchmark name.
- kumitate-shokunin `.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json:370-471` —
  kumitate r63 borrowed a copy of *kengaku's* round-35 dispatch as forgery-control material for its own gate. Wave
  history; kengaku bytes as attack fixtures; no TB2 claim.
- souji-shokunin `census/round-31/waves/w2/SwarmConnector28.md:21` — routes kengaku's TB2 git-leak ground to kengaku.
- game-dev-3d-shokunin `corpus/fixtures/r94vendor/three.core.js:29685,49752` — `data.compareFunction` false positives on
  the `data\.comp` regex. Not a hit.
- Compression/codec domain check: audio-shokunin's codec ground is media codecs (`corpus/live/r62-boundary/src/codec_desc.c`,
  Avid RGB "Packer"); kaidoku's is firmware extraction (binwalk/unblob carriers). Neither replays a compression/codec TB2
  task; `write.?compressor` over all tracked sibling trees matches nothing but the JS false positives. Fleet `scripts/`
  (shokunin-watchdog.sh, sources-census.sh, hyaku/, fixtures/): clean.

## (b) Frozen-instrument-vs-freeze-commit gates / self-mutation through a CLI-path copy

**Verdict: two real owners — kaidoku (rich, tracked, mechanism-duplicate of R94-C2's class) and mado (tracked chronology
gate). Complements, not duplicates of kengaku's *object*. Route = cross-cite prior art; never absorb.**

Kengaku's objects for comparison (all at T): gate v2 `plans/round94_freeze_integrity.py` — sha256 table, bytes at freeze
**and** at rev must match the row, `rev-list --full-history` touched-count (:131), TREESAME-side discarded edits count as
breach and an edit-then-revert is still a breach (:19-22), exactly one ```frozen-instruments block (:48, :94-96),
duplicate rows refused (:100-102), 15-case in-process battery; counter `plans/round94_c2_counter.py` — W1 history census,
W2 twelve fixture repos, W3 SELFTEST echo, W4 single-add-commit freeze selector, **W5 seven CLI-path mutants K1–K7**
(:59-70) each killed at its designated fixture, null copy keeps all green.

1. **kaidoku-shokunin @ c19d57cd2e65 — tracked counter family, same mechanism class** (complement; strongest overlap):
   - `tools/round-44/c2-counter.py:595-598` — `freeze_integrity(...)`: "A changed frozen path is exit 2, never a pass."
   - `tools/round-49/c2-mismatch.py:67-70,699-703` — `frozen_path_changed` plus `counter_not_frozen` (own bytes vs FREEZE blob).
   - `tools/round-50/c1-counter.py:156-159,1574-1579` — `receipt_fresh` via `git log -m --full-history --diff-filter=A`
     because "the default simplified history hid a pre-freeze add behind a TREESAME merge in round 49".
   - `tools/round-50/c2-record.py:34-38,96-99,1294-1297` — `git -c core.quotePath=false log --full-history -m --no-renames
     --name-status -z` + blob-and-mode compare ("renames, quoted names, mode changes, added files and touch-and-restore").
   - **Mutation-through-a-copied-CLI precedent (kengaku W5's class):** `tools/round-50/c2-record.py:1591-1595` battery
     runs the counter from an alt path (`counter=alt`) expecting `counter_not_frozen`;
     `tools/round-50/selftest-r49-c2.py:28-49,125-128,378-382` grafts a mutant counter blob into synthetic FREEZE/BASE
     commits "so the mutant passes its own counter_not_frozen guard" (fixtures `x-counter-bytes`, `x-frozen-edit`,
     `x-frozen-add`, `x-frozen-plan`).
   - Disclosures: `corpus/lessons/round-49.md:52` (TREESAME-merge-add blindness; "three constant mutants are invisible");
     `plans/round-49-claims.md:43` ("refs/replace, grafts and squashes are invisible"); `plans/round-50-claims.md:46`.
   - Relationship: **duplicate in mechanism, complementary in object.** kaidoku guards kaidoku's round-48/49/50 frozen
     paths and counters; kengaku v2 guards kengaku's claims-table instruments (one-block/duplicate-row grammar,
     breach-on-revert, in-process battery, W4 single-add selector — v2-unique). Convergent evolution: kaidoku mined
     TREESAME at r49 and fixed at r50; kengaku mined W-2/W-3/W-6 at r93 and closed them in v2.
2. **mado-shokunin @ 24ba2a9ddac2 — tracked standing freeze-order gate** (complement):
   - `quality/check-freeze-order.py:1-14,120-124` — derives the FREEZE commit (first-parent `--full-history` walk;
     freeze = commit where every freeze-file blob first equals its REV blob), detects `freeze_edited:<file>`, verdicts
     freeze-committer-time strictly before wave-launch createdAt.
   - **Contradiction, stated not smoothed:** mado reads "an edit … later reverted" as OK (:13); kengaku v2 counts it a
     breach (`round94_freeze_integrity.py:21-22`); kaidoku's walk sees touch-and-restore as a breach. Three lanes, three
     predicates, each with declared limits (mado also discloses committer-date backdating). Genuine semantic fork in the
     fleet's freeze-integrity family — one line for the round-95 lesson, not a repair.
3. Practice-level (wave-history receipts, no standing tracked gate): chousa r31 F2-1
   (`.ufo/waves/round-31/build/ReviewClaimsDesign31.md:15`), r46 F2 (`.ufo/waves/round-46/w1/ExecCounterRun.md:141-144`),
   r48 `VerifyFrozenClaim.md:8`, r49 `ReviewFreezeEq.md`, r50 `R50CritErratum.md`; kotoba r82
   (`corpus/lessons/round-82.md:91`, `plans/round-82-addendum-1.md:13`); kotodama
   (`reports/round-14/fix-runner-hash.md:31-33,87-91`); kake (`corpus/lessons/round-43.md:1`); souji (`SCORECARD.md:1589`).
4. Plumbing-only: kumitate `scripts/plan-before-ready.sh:154-157,181-183` (plan-before-ready gating; kumitate also
   mutation-batters its own ledger probe — round-69 artifact "7/20 mutants wrong"); mori
   `tools/mori-sources-appendonly.py:236-237` (append-only registry ancestry, different predicate).
5. Mutation-culture adjacency (technique): audio's revert-the-fix mutants/forges of its own driver in scratch trees
   (`corpus/live/r89-reverify/mut.py:2-26`, `battery-mut.sh:2-5`, `r79-critic/forge1-measure_audio.py`;
   `r94-simplifier/r94s_evidence_arm_entailment.txt:28-29` "equivalent mutant"). No sibling copies a *gate's* CLI entry
   and redirects main the way kengaku W5 does; kaidoku's alt-path counter copy is the nearest prior instance.

## (c) decomp -O3 vs grader plain-gcc divergence (`corpus/evidence/round94/decomp-opt-divergence.txt:1-4` at T)

**Verdict: kengaku-owned; no sibling owns or duplicates it.**

"decomp" is the task's *decompressor source*, not decompilation. Nearest lanes:

- **revenger @ 9ddd38ac8bae** owns decompiler ground truth (S054–S113; `ghidra-headless-recon`, SCORECARD.md:168) —
  decompiler output quality, not grader rebuild flags.
- **tsukuroi @ 64f45b790f2d** — `tools/check-adjacency-anchors.py:120` "decomp/recomp interest" demand-context only.
- **tameshi @ f256302b394a** — zero ghidra/dewolf/decompil hits in tracked trees.
- Prior art, none the same claim: kaidoku `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md:16-27` (-O0/-O1/-O2
  corpora); audio `reports/round-68/r68-boundary.md:209-212`, `reports/round-95/r95-scout.md:62,306-307`
  (uninitialized-stack mechanism class); game-dev-2d `reports/round-72/r72-critic.md:218` (-O0 probe builds).

## Routed notes for round 95 (report-only; no verdict flips)

- **R-N1 (info).** kaidoku discloses refs/replace/graft/squash invisibility (`plans/round-49-claims.md:43`); kengaku gate
  v2 declares no equivalent limit while `resolve()`/`blob()` honor replace refs silently. Non-flipping at T (linear lane
  history; counter-owned plain fixture clones). Declared-limit candidate for a future gate revision.
- **R-N2 (info).** Revert-semantics fork (mado OK vs kengaku breach vs kaidoku seen-breach) deserves one explicit
  sentence wherever the freeze-integrity family is next documented.
- **R-N3 (info).** Round-95 lesson can cite kaidoku r49→r50 TREESAME lineage and mado's freeze-order gate as independent
  prior art for v2's W-2/W-3/W-6 closures — cross-lane convergence strengthens calibration without changing bytes.

## Hygiene

- Fleet-root stray `kumitate-shokinin/` (typo dir outside every lane) holds a nested copy
  `kumitate-shokunin/.ufo/waves/round-69/w1/K69ExecBaseCounter.md`. Untouched by this seat; route to fleet owner.
- Tool note: grep tool glob-path form (`…/*-shokunin`) silently returns no results (demonstrated false negative);
  use explicit `;`-joined lane paths. Filed to the harness issue channel.
- No tool installs or upgrades; no sibling tree, lane index, jj state, or fleet root mutated.

## FINDINGS

- FINDING F1 info (a): no sibling replays TB2 graders, write-compressor, or any compression/codec task, and none
  captures TB2 task bytes — all sibling hits are echoes/routings of kengaku's own bytes; kengaku remains sole owner.
- FINDING F2 info (b): kaidoku owns the mechanism-duplicate family (freeze_integrity, counter_not_frozen, TREESAME-aware
  --full-history walks, mutant-counter copies through an alt CLI path) — complement in object; cross-cite, never absorb.
- FINDING F3 info (b): mado owns a standing freeze-order chronology gate; it deliberately reads a revert-restored freeze
  edit as OK while kengaku gate v2 counts any touched commit as breach — explicit semantic fork, state it, don't smooth it.
- FINDING F4 info (c): the decomp -O3 vs grader plain-gcc divergence is owned by kengaku's R94-C1 surface; no sibling
  (revenger/tsukuroi/tameshi included) owns any part; nearest prior art is kaidoku -O-level corpora, audio
  uninitialized-stack reports, revenger decompiler literature.
- FINDING F5 minor: fleet-root stray dir `kumitate-shokinin/` (nested kumitate round-69 artifact) sits outside all lanes;
  route to the fleet owner for cleanup.
- FINDING F6 minor: grep glob-path form false-negatives (documented above, filed) — overlap seats must use explicit paths.
- FINDING R-N1 info: kaidoku discloses refs/replace/graft/squash invisibility; kengaku gate v2 declares no equivalent
  limit — one-line declared-limit candidate for a future gate revision (non-flipping at T).
