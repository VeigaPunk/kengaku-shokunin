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
`-O3`, `null copy|cli.?path|copy of the (gate|counter)`. Raw excerpts in `ConnectorOverlap/receipts/`.

Headline: **(a) nobody else touches Terminal-Bench bytes; (b) kaidoku and mado own real tracked freeze-gate machinery
that is mechanism-adjacent to R94-C2 (complement, cite, never absorb); (c) the decomp -O3 vs grader plain-gcc divergence
is kengaku-owned and no sibling holds any part of it.** Nothing found flips R94-C1 or R94-C2.

---

## (a) TB2 grader replay / write-compressor / compression-codec / TB2 task bytes

**Verdict: no sibling owns or duplicates any of it. Kengaku is the fleet's sole TB2 grader owner — again.**

Every sibling hit is an echo of kengaku's own bytes, not an owned replay or capture:

- kaidoku-shokunin `.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601,19614` — a reservation-time
  scan that embeds the *KengakuR41* driver text (PIN `2fd12b88…`, `constraints-scheduling` capture paths). It records
  kengaku's round-41 work inside kaidoku's wave history; kaidoku's tracked tree holds zero TB2 bytes.
- kaidoku r69/r92/r93 and kake r71/r92/r93 connector/scope receipts (e.g. `kaidoku/.ufo/waves/round-69/w1/ConnectorCross/sweep/s4-receipt.txt:185-212`,
  `kake/.ufo/waves/round-92/w1/ConnectorScope/receipts/query-422.txt:74`, `kake/.ufo/waves/round-71/w1/ConnOverlap.md:29-32`
  — "…kengaku = Terminal-Bench…" in the S-homonym survey): all scans *about* kengaku, routed to kengaku.
- kagi-shokunin r30/r33 connector tables (`.ufo/waves/round-30/w1/ConnOverlap-report.md:64,228`, `round-33/build/ConnOverlap.md:73,114-115`):
  "OpenSSL key management **as a benchmark grader surface** (Terminal-Bench `openssl-selfsigned-cert` task)" — explicitly
  classified as kengaku's ground, NO CLAIM/DEFER. Prior connector rounds already settled this adjacency the same way.
- kumitate-shokunin `corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83` — a *paper capture* (S197) that
  uses Terminal-Bench as an evaluated benchmark name in MAS-topology research. Knowledge about the benchmark, zero task
  bytes, zero graders. Closest thing to "Terminal-Bench" in any sibling's tracked corpus; not a duplication.
- kumitate-shokunin `.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json:370-471` —
  kumitate r63 borrowed a copy of *kengaku's* round-35 dispatch as **forgery-control material** for its own gate. Wave
  history, kengaku bytes used as attack fixtures, no TB2 claim.
- souji-shokunin `census/round-31/waves/w2/SwarmConnector28.md:21` — routes kengaku's TB2 git-leak ground to kengaku ("kengaku
  holds measured plain-git reflog/object-retention ground … (Terminal-Bench 2 git-leak grader)").
- game-dev-3d-shokunin `corpus/fixtures/r94vendor/three.core.js:29685,49752` — `data.compareFunction` false positives on
  my `data\.comp` regex. Not a hit.
- Compression/codec domain check: audio-shokunin's codec ground is media codecs (`corpus/live/r62-boundary/src/codec_desc.c`,
  Avid RGB "Packer"; r87 links table), kaidoku's is firmware extraction (binwalk/unblob carriers). Neither replays a
  compression/codec TB2 task; `write.?compressor` over all tracked sibling trees matches nothing but those JS false
  positives. Fleet `scripts/` (shokunin-watchdog.sh, sources-census.sh, hyaku/, fixtures/): clean.

## (b) Frozen-instrument-vs-freeze-commit gates / self-mutation through a CLI-path copy

**Verdict: two real owners — kaidoku (rich, tracked, mechanism-duplicate of R94-C2's class) and mado (tracked chronology
gate). Complements, not duplicates of kengaku's *object*. Route = cross-cite prior art; never absorb.**

Kengaku's objects for comparison (all at T): gate v2 `plans/round94_freeze_integrity.py` — sha256 table, bytes at
freeze **and** at rev must match the row, `rev-list --full-history` touched-count (:131), TREESAME-side discarded edits
count as breach and an edit-then-revert is still a breach (:19-21 docstring), exactly one ```frozen-instruments block
(:48, :94-96), duplicate rows refused (:100-102), 15-case in-process battery; counter `plans/round94_c2_counter.py` —
W1 history census, W2 twelve fixture repos, W3 SELFTEST echo, W4 single-add-commit freeze selector, **W5 seven CLI-path
mutants K1–K7** (:59-70: `evaluate`/`parse_table` copied as `*_cli`, one mutation each, `main` redirected, battery left
honest) each killed at its designated fixture, null copy keeps all green.

1. **kaidoku-shokunin @ c19d57cd2e65 — tracked counter family with the same mechanism class** (complement; strongest overlap):
   - `tools/round-44/c2-counter.py:595-598` — `freeze_integrity(root, freeze, rev, frozen_spec, declared, frozen_dirs)`:
     "A changed frozen path is exit 2, never a pass."
   - `tools/round-49/c2-mismatch.py:67-70,699-703` — `frozen_path_changed` plus `counter_not_frozen`: the counter exits 2
     when **its own bytes differ from its blob at FREEZE** (self-frozen guard, digest pair recorded).
   - `tools/round-50/c1-counter.py:156-159,1574-1579` — `receipt_fresh` requires `git log -m --full-history
     --diff-filter=A` because "the default simplified history hid a pre-freeze add behind a TREESAME merge in round 49".
   - `tools/round-50/c2-record.py:34-38,96-99,1294-1297` — frozen-path walk `git -c core.quotePath=false log --full-history
     -m --no-renames --name-status -z` + blob-and-mode compare "sees renames, quoted names, mode changes, added files and
     touch-and-restore"; `counter_not_frozen` self-check.
   - **Mutation-through-a-copied-CLI precedent (kengaku W5's class):** `tools/round-50/c2-record.py:1591-1595` battery
     writes the counter to an alt path and runs it (`counter=alt`) expecting `counter_not_frozen`;
     `tools/round-50/selftest-r49-c2.py:28-49,125-128,378-382` grafts a *mutant counter blob* into synthetic FREEZE/BASE
     commits "so the mutant passes its own counter_not_frozen guard" and asks whether the battery notices
     (fixtures `x-counter-bytes`, `x-frozen-edit`, `x-frozen-add`, `x-frozen-plan`).
   - Disclosure: `corpus/lessons/round-49.md:52` — TREESAME-merge-add blindness and "three constant mutants are
     invisible", frozen-reported-not-patched; `plans/round-49-claims.md:43` — declared limits "refs/replace, grafts and
     squashes are invisible"; `plans/round-50-claims.md:46` — `counter_not_frozen`; `--full-history` as landed clauses.
   - Relationship: **duplicate in mechanism, complementary in object.** kaidoku guards kaidoku's own round-48/49/50
     frozen paths and counters; kengaku v2 guards kengaku's claims-table instruments. Neither can serve as the other's
     tabled instrument (and the F-rule forbids swapping instruments in-round). v2's unique bits: the one-block/duplicate-row
     table grammar, breach-on-revert semantics, in-process battery, W4 single-add freeze selector. kaidoku's unique bits
     vs v2: rename/quoted-name/mode visibility (`-z --no-renames`), merge-aware `-m` walk, the disclosed
     refs/replace-graft-squash limit (see Routed note below). Convergent evolution is itself calibration evidence:
     kaidoku mined TREESAME blindness at r49 and fixed it at r50; kengaku mined W-2/W-3/W-6 at r93 and closed them in v2.
2. **mado-shokunin @ 24ba2a9ddac2 — tracked standing freeze-order gate** (complement):
   - `quality/check-freeze-order.py:1-14,120-124` — derives the FREEZE commit (first-parent `--full-history` walk over
     the freeze paths; freeze = the commit where every freeze-file blob first equals its REV blob), detects
     `freeze_edited:<file>`, and verdicts freeze-committer-time strictly before the wave's `swarm-registry.json` createdAt.
     Read-only git objects only; selftest builds scratch repos.
   - **Contradiction, stated not smoothed:** mado's docstring declares "an edit to a freeze file that is later reverted
     leaves the blob equal and reads OK" (:13) — kengaku v2 asserts the opposite ("An edit later reverted is still a
     breach", `round94_freeze_integrity.py:21-22`); kaidoku's walk *sees* touch-and-restore as a breach. Three lanes,
     three predicates; each is honest about its own declared limits (mado also discloses committer-date backdating).
     This is a genuine semantic fork in the fleet's freeze-integrity family — worth one line in the round-95 lesson, not
     a repair.
3. Practice-level (recurring seat work, wave-history receipts, no standing tracked gate): chousa r31 F2-1
   (`.ufo/waves/round-31/build/ReviewClaimsDesign31.md:15`), r46 F2 (`.ufo/waves/round-46/w1/ExecCounterRun.md:141-144`),
   r48 `VerifyFrozenClaim.md:8` (`git show FREEZE:claims.md | sha256sum` vs on-disk + `git diff FREEZE..HEAD -- tool`),
   r49 `ReviewFreezeEq.md`, r50 `R50CritErratum.md`; kotoba r82 freeze-ordering lesson (`corpus/lessons/round-82.md:91`
   — mines a Q65 freeze-ordering defect and *plans* "a pre-freeze gate that refuses the plan", `plans/round-82-addendum-1.md:13`);
   kotodama runner-hash binding (`reports/round-14/fix-runner-hash.md:31-33,87-91`); kake r43 freeze-order lesson
   (`corpus/lessons/round-43.md:1`); souji r61 erratum (`SCORECARD.md:1589`, freeze attribution via
   `git log --diff-filter=A --no-renames --full-history`). None is an instrument; all routed internally already.
4. Plumbing-only overlaps: kumitate `scripts/plan-before-ready.sh:154-157,181-183` (`--full-history --diff-filter=A`
   oldest-add mapping for plan-before-ready gating; kumitate also mutation-batters its own ledger probe — see the
   round-69 artifact at `kumitate-shokunin/.ufo/waves/round-69/`, "7/20 mutants wrong"); mori's append-only gate
   (`tools/mori-sources-appendonly.py:236-237`, `--full-history` parent-carrying walk for registry supersede timing) —
   same git plumbing, different predicate (append-only registry ancestry, not instrument freeze).
5. Mutation-culture adjacency (technique, not gate-self-mutation-through-CLI-copy): audio's revert-the-fix mutants and
   forges of its own driver run in scratch trees (`corpus/live/r89-reverify/mut.py:2-26`, `battery-mut.sh:2-5`,
   `r79-critic/forge1-measure_audio.py`; and the r94 receipt `r94s_evidence_arm_entailment.txt:28-29` "A mutation tester
   would score the dropped arm an equivalent mutant"). No sibling generates mutants of a *gate* by copying its CLI entry
   and redirecting main the way kengaku W5 does; kaidoku's alt-path counter copy is the nearest prior instance.

## (c) decomp -O3 vs grader plain-gcc divergence (`corpus/evidence/round94/decomp-opt-divergence.txt:1-4` at T)

**Verdict: kengaku-owned; no sibling owns or duplicates it. Keep it; nothing to route out.**

The observation is kengaku's own, committed at T, self-labelled "host observation (not a claim leg)": the write-compressor
task image builds `/app/decomp` with `gcc -O3` while the grader rebuilds `decomp2` with plain gcc, and `decomp.c`'s
`printf("%s")` over an uninitialised stack buffer makes trailing bytes codegen-dependent (d_o3 4870 B differs; d_o0 4868 B
identical). Important disambiguation: "decomp" here is the task's *decompressor source*, not decompilation — the lane
names that sound similar own different things:

- **revenger-shokunin @ 9ddd38ac8bae** owns decompiler ground truth (SOURCES S054–S113: Ghidra/IDA/LLM4Decompile/SAILR…;
  capability `ghidra-headless-recon`, SCORECARD.md:168) — about decompiler output quality, not grader rebuild flags.
- **tsukuroi-shokunin @ 64f45b790f2d** mentions "decomp/recomp interest" only as demand context
  (`tools/check-adjacency-anchors.py:120`). No ownership.
- **tameshi-shokunin @ f256302b394a**: zero hits on ghidra/dewolf/decompil in tracked trees.
- Nearest prior art, none of it the same claim: kaidoku compiles its corpus binaries at -O0/-O1/-O2 as extraction
  inputs (`corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md:16-27`, per-key -O-level table); audio documents the
  uninitialized-stack mechanism class in its own driver domain (`reports/round-68/r68-boundary.md:209-212`,
  `reports/round-95/r95-scout.md:62,306-307`); game-dev-2d builds probes at -O0 (`reports/round-72/r72-critic.md:218`).
  The TB2 grader-vs-image rebuild divergence rides with kengaku's TB2 coverage ground (see (a)).

## Routed notes for round 95 (report-only; no verdict flips; no in-round repairs)

- **R-N1 (info).** kaidoku's counters disclose that `refs/replace`, grafts and squashes are invisible to their freeze
  walks (`kaidoku/plans/round-49-claims.md:43`). Kengaku gate v2's docstring declares no equivalent limit; `resolve()`
  uses `rev-parse --verify` and `blob()` uses `git show`, both of which honor replace refs silently. Non-flipping today
  (lane history is linear, W2 fixtures are counter-owned plain clones), but it is a one-line declared-limit candidate for
  a future gate revision — the exact disclosure pattern kaidoku used.
- **R-N2 (info).** The revert-semantics fork (mado OK vs kengaku breach vs kaidoku seen-breach) deserves one explicit
  sentence wherever the freeze-integrity family is next documented, so a future reader does not read mado's green as
  contradicting v2's red.
- **R-N3 (info).** Round-95 lesson can cite kaidoku r49→r50 TREESAME lineage and mado's freeze-order instrument as
  independent prior art for v2's W-2/W-3/W-6 closures — convergence across three lanes strengthens the calibration claim
  without changing any byte.

## Hygiene

- **Fleet-root stray:** `kumitate-shokinin/` (typo dir outside every lane) contains a nested copy
  `kumitate-shokunin/.ufo/waves/round-69/w1/K69ExecBaseCounter.md` (a kumitate r69 seat report with its ledger-probe
  mutation results). Untouched by this seat; fleet owner should delete or adopt it.
- **Tool note for future overlap seats:** the grep tool silently returns "No matches found" when `path` is a glob form
  (`…/*-shokunin`) even over directories containing the pattern; pass explicit `;`-joined lane paths (demonstrated:
  `terminal` over the glob form → 0 hits, over explicit paths → 30+ hits). Filed to the harness issue channel.
- No tool installs or upgrades were made. No sibling tree, the lane index, jj state, or fleet root was mutated.

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

Paths written: `.ufo/waves/round-94/w1/ConnectorOverlap.md` (this report),
`.ufo/waves/round-94/w1/ConnectorOverlap/report.md` (copy), `.ufo/waves/round-94/w1/ConnectorOverlap/receipts/a-tb2-scan.md`,
`.ufo/waves/round-94/w1/ConnectorOverlap/receipts/b-freeze-gates.md`,
`.ufo/waves/round-94/w1/ConnectorOverlap/receipts/c-decomp-opt.md`,
`.ufo/waves/round-94/w1/ConnectorOverlap/receipts/method-and-tool-notes.md`.
