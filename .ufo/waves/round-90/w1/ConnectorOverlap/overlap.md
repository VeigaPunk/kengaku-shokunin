# ConnectorOverlap — round 90 sibling-overlap scan (read-only, report only)

Seat: ConnectorOverlap-11 (leaf, read-only). No claims, no edits, no commits, no installs.
Reference instruments (kengaku at pin commit B `664435cf`): `plans/round90_burndown.py` (R90-C3
freeze gate), `plans/round90_counter_pin.py` + `plans/counter-pins-r90.json` (R90-C2), `plans/round90_c1_replay.py`
(R90-C1). Base `dcdd494e`.

## Method and scope

- Population: the 20 sibling lanes `/home/vgpnk/Projects/shokunin/<id>-shokunin` (kengaku excluded). The fleet
  root's `kumitate-shokinin/` (typo spelling) is not a lane repo and was not read.
- Read-only git only: `git -C <lane> grep -n -I -E …` and `git -C <lane> ls-files` / `show HEAD:<path>` over
  TRACKED content (`plans/`, `tools/`, `scripts/`, `corpus/`, `.ufo/`). Untracked files and `.scratch/` were not
  scanned. The kengaku instrument headers were read with `git show 664435cf:<path>`.
- Pattern sets: (A) routed-findings / burn-down / freeze-refusal; (B) sha/blob pin over counters or receipts;
  (C) TB2 grader offline replay. Raw hit lists: `receipts/raw-hits.txt` (114 lines, 36 A / 55 B / 23 C before
  manual triage) and `receipts/names.txt` (tracked filenames matching routed/grader/tb2/pins/freeze/burn).
- Dead commands (disclosed): one `sed: stream did not contain valid UTF-8` on a `git grep | sed` pipeline
  whose input was a sibling's tracked `.ufo/waves` text (rc not captured; the affected lines were re-read
  individually). One shell-syntax error (`pi-natives:command … col 804`, rc 2) in an early inline `printf`
  loop with no effect; re-run with a simpler command. A broad background grep (bg_3824) was superseded by
  the scoped scan; its output was discarded and no verdict uses it. All other `git` and `grep` calls exited 0.

## (a) routed-findings burn-down with a freeze-refusal gate

| # | Path:line (sibling) | Mechanism (one line) | Verdict vs kengaku | Action |
|---|---|---|---|---|
| A1 | tameshi `corpus/routed-defects.json` (108 rows: 74 fixed, 12 declined, 22 open; open ids R45.1 … R59) + `.ufo/evidence/round-50/c1/measure.py:1-14, 48, 58-60` | Routed-defect ledger judged against the tree per row (evidence line ranges + excerpts); rev-parametric counter. | SAME data surface and the SAME pathology (22 open rows, oldest opened round 45, ledger round 58). DIFFERENT gate: no freeze refusal, no supersede rows, no age rule. | keep |
| A2 | kumitate `scripts/routed-ledger.mjs:1-21, 223-226` + `corpus/routed-ledger.md:1-9, 13-75` | Ledger of every spot-check routed item; quote-bound; closed/wontfix rows bind an answer at path:line; `--rev` reads committed spot-checks. Append-only text rule at `routed-ledger.md:9`. | SAME surface (routed ledger, rev-parametric, append-only rule). DIFFERENT: `grep -c -i 'freeze\|oldest'` = 0 in the script; `open` rows carry no age and no freeze consequence (e.g. R55-V1, R57-V1 open). | keep |
| A3 | kaidoku `.ufo/waves/round-18/tools/routed-defects.py:1-25` (tracked) | git-object-only counter of six round-17 routed defects with `named` and `substance` check sets. | Same primitive (rev-pinned routed counter). DIFFERENT: fixed list, no ledger, no refusal. | keep |
| A4 | mori `tools/mori-routed-check.py:1-12`, `tools/mori-routed-r24.py:1-10`; PROVINCE.md:590-591 claims them | Per-round frozen routed items (R1–R4, D1–D5) re-derived from git objects. | Same ground at item level only. DIFFERENT: no ledger, no burn-down, no freeze gate. | keep |
| A5 | kotoba `verifiers/check_routed_repairs.py:1-12`, `check_routed_repairs_v2.py:1-3`; tsukuroi `tools/check-r74-routed-r75.py:1-6` (series r71–r75); kasegi `corpus/instruments/r44-routed-defects.py:1-6`, `r45-routed-defects.py`, `r47-routed-defects.py:1-6` | Per-round counters of routed repairs landed in committed bytes. | DIFFERENT: per-round closure counts, no standing ledger, no freeze consequence. | keep |
| A6 | kotodama `reports/round-14/routed-resolution.json`, `round-22/…`, `round-30/…` | Point-in-time resolution records (keys round/date/resolutions; round-30 has a counting command). | DIFFERENT: records, not a ledger; no gate. | keep |
| A7 | chousa `corpus/evidence/round40/routed-defect-dispositions.json:1-10` | Per-id disposition map for round-40 routed items. | DIFFERENT (static record). | keep |
| A8 | kaidoku `tools/round-84/freeze-precheck.py:1-8`; `tools/round-30/prefreeze-gate.py:1-12` | Prefreeze REFUSAL gates: a claim must name its counter; pins must bind. | The nearest freeze-refusal in the fleet. DIFFERENT refusal condition (claim-text / pin completeness, not routed-finding age). | keep |
| A9 | lore `corpus/tools/dependency_freeze.py:299, 303, 423, 437` | `--freeze refuses` on scope or pin conflicts. | DIFFERENT (dependency pins, no routed ledger). | keep |
| A10 | tameshi `plans/round-74.plan.md:163`, `corpus/lessons/round-84.md:13`, `round-85.md:15`, `round-87.md:20`; kumitate `corpus/lessons/round-37-verifier-spotcheck.md:205` | The word "burn-down": tameshi's considerthese idea 4 (assimilation backlog) was declined as unrelated; kumitate's "burn-down" is a ratchet concept in a lesson. | Name collision only; no instrument. | none |

Result for (a): no sibling source implements "refuse a freeze while routed findings older than N−2 remain
pending". `grep` of tracked `*.py *.mjs *.js *.sh *.json` for oldest-open/pending-routed or freeze-refusal logic
returned only dispatch prompts and lesson prose. kengaku's C3 gate remains the only instrument of that rule in
the fleet's tracked source.

## (b) external sha/blob pin ledgers over counters or receipts

| # | Path:line (sibling) | Mechanism (one line) | Verdict vs kengaku | Action |
|---|---|---|---|---|
| B1 | kumitate `scripts/counter-pins.mjs:1-41, 62` + `.ufo/pins/counter-pins.json:1-3` (45 pins, rounds 53–84; 7 under `scripts/`, 38 under `.ufo/`, 0 under `plans/`) | Registry of `{round,name,path,sha256}` over frozen counters; absent / path-escape / symlink = DRIFT; duplicate names FAIL-CLOSED; empty = DRIFT; 11-case selftest. | SAME class as R90-C2's checker (sha256 registry, fail-closed absence, selftest). DIFFERENT: working tree only (usage line 13 has `--registry` only; `grep -c -- '--rev'` = 0); no git-blob arm; registry lives in the lane tree (the self-pin residual C2 discloses). | keep |
| B2 | tameshi `.ufo/evidence/round-50/freeze.json:1-9` (schema tameshi-r50-freeze-v1, sha256 map of counter and contract bytes); `.ufo/evidence/round-37/counter-pin.json:1-8` (counter_sha256 + tool_sha256); `.ufo/evidence/round-25/c1-pins.py:1-12` (P1 sha256 of counter and gate bytes at clone HEAD) | Per-round in-tree sha pins over counters, checked at a revision. | SAME class. DIFFERENT: per-round, in-tree, no external ledger, no blob-at-anchor arm. | keep |
| B3 | kaidoku `tools/round-29/freeze-gate.py:28, 89-94, 102-103` | `INSTRUMENT_PIN_MISMATCH` = recorded sha256 != blob at freeze; reads `git show <freeze>:<claims>` and `<measured>:<claims>`; `cat-file -t` blob check. | CLOSEST rev-binding primitive in the fleet to C2's record-table blob arm (pin vs git blob at the anchor). DIFFERENT: pins are self-recorded inside each claims container and anchored at the freeze commit, not an external ledger. | keep |
| B4 | kaidoku `tools/round-74/freeze-pins.py:1-12` | Computes producer pins mechanically from freeze bytes before the freeze commit. | DIFFERENT: pin generator, not a ledger. | keep |
| B5 | tabi `scripts/check-release-pins.mjs:2-5, 13-14, 19-46` | Release-pinned source freshness: reads `git show <rev>:<path>` only and sha256s the bytes. | Same primitive, different ground (SOURCES freshness, not counters). | keep |
| B6 | revenger `reports/round-89/instrument-pins.log` (3 lines), `reports/round-90/instrument-pins.log` (18 lines); cited as "match" in `.ufo/waves/round-89/w1/CriticR89Claims.md:19, 61` | Plain sha256 listing of instruments. No checker in the tracked tree verifies it. | Same data, no mechanical verifier: DIFFERENT. | keep; route-out (see R-O4) |
| B7 | kama `tools/round75-interpretation-pins.py`, `registry/engine-pins.tsv`; kake `corpus/knowledge/freshness-pins.json`; kotoba `verifiers/check_substrate_pins.py`; kasegi `corpus/instruments/freeze-check.py`; mado `quality/check-freeze-order.py`; mori `tools/mori-freeze-order.py` | Name-only hits; not read in full. | Presumed different ground by name (interpretation pins, engine/substrate pins, freeze ordering). Not verified. | keep |

Result for (b): sha pins over counters are common in the fleet (kumitate, tameshi, kaidoku, revenger). None
combines all three of C2's arms: an external pin ledger, a check at an arbitrary `--rev`, and a git-blob pin
of a record table at its creating commit. kaidoku's freeze-gate (B3) is the nearest rev-binding analogue.

## (c) TB2 grader offline replay over synthetic fixtures

- No sibling executes a Terminal-Bench 2.0 grader in tracked source. `git grep` of tracked `*.py *.mjs *.js
  *.sh *.json` outside `.ufo/waves/` for `test_outputs|terminal-bench-2|Terminal-Bench 2` returns one hit:
  `souji-shokunin census/round-5/seat-32.json:11` (the JSON key `directly_contradicted_prior_test_outputs`; false positive).
- Tracked names matching `tb2*`, `*terminal-bench*`, `*grader*`, `graders/**`, `test_outputs.py`: none in any sibling.
  `git log --all -- 'tb2*' '*terminal-bench*'` in tabi returns nothing; tabi tracks no `tb2-*` knowledge file.
- kengaku is the only lane that tracks TB2 grader knowledge (31 `corpus/knowledge/tb2-*.md`).
- Non-tool mentions are kengaku text copied into sibling wave directories. They are NOT sibling instruments:
  - tabi `.ufo/waves/round-62/w1/R62Exec1/context-6.stdout:1` begins `# kengaku-shokunin — Province`; its TB2
    grader claims at lines 256, 267, 290, 312, 395, 444, 495, 561, 594, 666–670 cite
    `corpus/knowledge/tb2-*-grader.md` and `plans/tb2_grader_probe.py`, neither tracked in tabi. Dangling attribution.
  - kake `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-422.txt:74`, `query-stale.txt:234`,
    `.ufo/waves/round-93/w1/ConnectorScope/receipts/sibling-scan.txt:22` quote kengaku SOURCES and knowledge rows (S126, S241, S144).
  - kaidoku `.ufo/waves/round-69/w1/ConnectorCross/sweep/s4-receipt.txt:185–215` quotes kengaku SKILL.md gate rows.
  - mado `.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:32` and kotoba `.ufo/waves/round-71/receipts/census-after.txt:28`
    record the fleet census W04 for kengaku S100 (terminal-bench-2 URL) duplicated across scopes.
  - chousa `.ufo/waves/round-73/w1/R73S03/.ufo__l0-questions.md.txt:206` quotes kengaku L0 question 203 (TB2 capture push-protection).

Result for (c): the offline TB2 grader replay ground is held by kengaku alone in the fleet's tracked source.
No sibling hit is a same-verdict match for C1's replay surface.

## Province check (root PROVINCE.md at HEAD, all 20 siblings)

- No sibling PROVINCE.md claims TB2-grader replay ground. The root PROVINCE.md of every sibling returns zero hits
  for `terminal-bench|TB2|grader` in the TB2 sense.
- Routed ground: mori PROVINCE.md:590-591 claims `tools/mori-routed-check.py` and `tools/mori-routed-r24.py` as
  gates (per-round item rechecks). That is a claim on routed-recheck ground, not on a burn-down ledger or freeze
  gate. kaidoku PROVINCE.md:553 names "the previous round's non-author routed-defect list" as an input population
  for its record audit (adjacent, not a claim on the ledger). kama PROVINCE.md:175 names `pin-watch` (routed
  defect R41A10-9), a source-tag pin instrument, not a counter pin.
- No sibling PROVINCE.md claims a routed-findings freeze gate or a counter-pin ledger. kumitate's root
  PROVINCE.md uses "routed" only for one kimi-census item (line 39) and "pin" only for a map-origin pin
  (line 37); neither is the ledger or counter-pin ground. tameshi's root PROVINCE.md has no hit.

## Keep / absorb / route-out, per hit

Absorb: none. No sibling instrument duplicates R90-C1, C2 or C3 in mechanism, so there is nothing to absorb.
The nearest analogues (kaidoku freeze-gate B3, kumitate counter-pins B1, tameshi freeze digests B2) stay with their lanes.

- A1 keep · A2 keep · A3 keep · A4 keep · A5 keep · A6 keep · A7 keep · A8 keep · A9 keep · A10 none
- B1 keep · B2 keep · B3 keep · B4 keep · B5 keep · B6 keep (route-out R-O4) · B7 keep (unverified)
- C-hits (kengaku text copies in tabi, kake, kaidoku, mado, kotoba, chousa wave dirs): keep (not instruments); route-out R-O2.

## Route-out notes (report only; no action in kengaku)

- R-O1 tameshi: 22 open routed rows dating to round 45 with no freeze consequence (`corpus/routed-defects.json`). The same
  pathology kengaku's C3 addresses; route to tameshi's own L0.
- R-O2 fleet orchestrator: kengaku `corpus/knowledge` and `SOURCES`/SKILL text is copied into sibling wave
  directories (tabi `round-62/w1/R62Exec1/context-6.stdout`, kake `round-92/w1/ConnectorScope/receipts/`, kaidoku
  `round-69/w1/ConnectorCross/sweep/`). The TB2 attributions in tabi's copy are not tabi's; route as provenance hygiene.
- R-O3 fleet orchestrator: kaidoku-shokunin tracks `.ufo/waves/round-90/w1/ConnectorOverlap/` (kaidoku's own item:
  UPX / packed ELF). Same directory name as this seat, different lane and item; no write collision (this seat writes
  only under kengaku's wave dir).
- R-O4 revenger: `reports/round-89|90/instrument-pins.log` is a sha listing verified by critic seats by hand; no tracked checker.
- R-O5 kumitate: `scripts/counter-pins.mjs` has no `--rev` and no blob arm (informational only; R90-C2 keeps its own checker).

## Frozen-element observation

Nothing in the frozen claims or the three instruments looked wrong within this scan's scope. The scan did not
evaluate the ledger state, the counters, or the C2/C3 verdicts. Those belong to the other seats.

## Receipts

- `receipts/raw-hits.txt` — raw `git grep` hits, prefixed A/B/C and lane.
- `receipts/names.txt` — tracked filename hits (routed, grader, tb2, pins, freeze, burn).
- Scratch `/fast/scratch/hyaku/kengaku-r90/ConnectorOverlap` removed after copying the receipts above.
