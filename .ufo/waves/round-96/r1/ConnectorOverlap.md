# ConnectorOverlap — R96 sibling-overlap scan (scoped findings)

Seat `ConnectorOverlapR` (leaf). Measured tip `T = 09717e49ff46fad5b255619d671aaaae52dfc180`;
BASE `45740a61`. Read-only; one fixture clone at T under
`/fast/scratch/hyaku/kengaku-r96/ConnectorOverlap/` (toplevel asserted). Full evidence:
`.ufo/waves/round-96/r1/ConnectorOverlap/report.md` and `.../receipts/`.

## (a) TB2 grader replays / parquet-pandas graders

- `multi-source-data-merger`, `merged_users`, `merged_users.parquet`: **0 sibling files**.
  `conflicts.json`: 5 sibling files, all unrelated (`p1-conflicts.json`, `pairwise_conflicts.json`).
- `tb2-*` knowledge entries: **31, all kengaku**. No sibling lane replays a TB2 grader.
- 84 sibling files name `Terminal-Bench`: 81 `.ufo/` connector/report receipts, 2 kumitate
  `corpus/` (a published study's benchmark use), 1 souji census note — citations only.
- Overlaps: chousa r63 `ConnSiblingOverlap.md:69-70` and r55 `R55ConnSiblings.md:67` cite kengaku
  TB2 entries; tameshi r58 `narrow-60.json:14` cites kengaku receipt bytes; kaidoku r90
  `ConnectorOverlap/receipts/kengaku.json` reads `constraints_probe.py:1-45` for isolation.
  All **complement**; no duplicate, no conflict.
- Round-96 capture vs round-52 capture: `tests/test_outputs.py` `a070888930cf…` and
  `tests/test.sh` `d5a00e64413c…` **byte-identical**; round-96 adds solve.sh/Dockerfile/data/
  instruction/task.toml. The r79 blocker detector reads the same grader bytes the replay ran.
- **PROVINCE holds**: five sibling PROVINCE lines assign LLM eval here (chousa:11, kasegi:50,
  kama:42, game-dev-3d:77, kumitate:25); no sibling claims the surface.

## (b) Absolute totals vs member sets; standing battery; bite/grow

- Repaired: r87 `LEDGER_SUBJECT` `tb2-result-file` → `tb2-header` (`round87_c1_replay.py:48`);
  r90–r95 L7 `exec_total == N` → `rev_set >= base_set | {MEMBER}` and cells `>=`
  (`round90:61,281`; `round91:47,227`; `round92:46,247`; `round93:55,229-230`; `round94:235`;
  `round95:243`). The old `EXECUTED_AFTER` constants remain as message-only values.
- Battery controls are two-sided and sound: `c1-only` red 7; `delete-l7` green 14/bites 0;
  `repin-abs` green 14/grows 0; `full` and `c2-only` pass.
- **CO-2 (minor)**: the 12 bites / 6 grows are **8 distinct forgery inputs** —
  `others[0] = build-pmars` for all six counters, `unexecuted[0] = adaptive-rejection-sampler`
  for all six (`round96_standing_battery.py:187-199`). Counts true, independence overstated.
- **CO-3 (minor)**: the set-keyed repair removes the last absolute-total cross-check; the
  compensating r79 bound is never composed with the grow forgery. Verified: r79 **pass** at T
  (`DEFECTS n=0`, `replayed=40`) and **fail** on the same grow commit
  (`DEFECT RECEIPT-UNTRACKED adaptive-rejection-sampler round96-grow-fixture`, `DEFECTS n=5`,
  rc 1). Receipts `c-r79-at-T.txt`, `c-r79-grow-forgery.txt`.
- **CO-7 (minor)**: the battery discards a failed grow leg's counter output
  (`round96_standing_battery.py:204-208`; `run_counter` `finally` at `:107-117`), so the one r91
  grow failure at T is unattributable. I re-ran all six counters at the same forged commit:
  **6/6 pass** (`executed_rows=41`, `defects=0`; `c-grow-r90.txt` … `c-grow-r95.txt`), matching
  the L1's isolated and 6× parallel diagnostics — 13 passes against 1 failure. Flake, not a
  counter defect; the diagnostic gap is the finding.
- **CO-6 (major)**: r80 (`round80_c1_located_replay.py:335-351`, `executed == 24`) and r81
  (`round81_c1_new_members.py:390-414`, `executed == 26`) still pin the r79 gate's absolute
  executed count, **worktree-only**; at T the gate prints `executed=40`. Both are SCORECARD-met
  C1 counters (`SCORECARD.md:3760,3832`). The round-96 population excludes them, so the frozen
  predicate is unaffected, but the absolute-pin class is not fully repaired and the battery's
  `--rev` invocation cannot see them.
- Sibling primitives are complements, not duplicates: kumitate `receipt-evidence.mjs:14-24`
  (reproduction), tabi `check-measurement-binding.mjs:3-22` (counter-bytes binding — would flag
  the repair by design, `[INFERENCE]`), kama `round72-receipt-tip-binding.py:1-14`, mori
  `mori-retention-reconcile.py:1-3`, kotodama `check-evidence-coupling.py:1-10`. **0 sibling
  hits** for `STANDING total=` / `BITES checked=` / `GROWS checked=` / `set_contains_base`.

## Cross-axis pattern

Coverage growth is the adversarial input to calibration: each executed member added since round 90
broke every earlier absolute pin (at BASE r90–r94 red against 34–38; C1's +1 would break r95 too,
`c1-only` red 7). C2's repair makes the pins growth-tolerant by construction — and therefore
accepts any executed superset, including the ledger-only grow forgery. The compensating bound
(r79's receipt/subject/verdict validation) exists and rejects that forgery, but the battery never
composes the two. Two counters of the same class (r80/r81) survive behind worktree-only legs the
battery cannot reach. Contract surface: the seven repaired counters are post-freeze edits of
rounds 87/90–95 instruments, so r93/r94/r95 freeze-integrity gates flip PASS→FAIL at T (ExecHarm
`ExecHarm.md:57-90`; gate `round94_freeze_integrity.py:1-20`). Under the byte-replace repair,
R96-C2 pass and those gates' pass are **mutually exclusive**; additive supersession would decouple
them.

## Proposed move (round 97; not in-round)

Compose the grow forgery with r79: add a leg that runs `round79_c1_population_ledger.py` against
the existing ledger-only grow commit, requires `PREDICATE R79-C1 fail` rc 1 **with**
`DEFECT RECEIPT-UNTRACKED <member>` (attributed, not any failure), and requires pass at the
unmodified tip. Affected axes: calibration improved (tolerance becomes bounded and measured);
coverage unchanged (C1's growth is receipt-backed); contract unchanged (CO-4/CO-6 need their own
decisions). Risks: r79's receipt checks are shape-based (proves unreceipted growth is caught, not
fabricated growth); the grow commit must stay ledger-only; the leg needs its own freeze and
controls; it does not repair r80/r81 or the freeze contradiction. Verification is the two receipts
above.

## Findings

- CO-1 info — no sibling replay; PROVINCE holds.
- CO-2 minor — 8 distinct forgery inputs, not 18.
- CO-3 minor — tolerance bound not composed; r79 verified to catch the grow forgery.
- CO-4 major — seven repaired counters are post-freeze edits; r93/r94/r95 freeze gates PASS→FAIL
  at T; contract-surface contradiction, true positive under the gate's definition.
- CO-5 info — fleet-root `.pytest_cache` (23:15:12) names the round-96 grader tests; a same-round
  pytest invocation used the fleet root as rootdir (cwd not established); untracked, no git state
  change.
- CO-6 major — r80/r81 still pin absolute executed totals (24/26) behind worktree-only legs; at T
  the gate prints 40; outside the round-96 population, so the frozen predicate is unaffected.
- CO-7 minor — the battery discards a failed grow leg's counter output; the one r91 grow failure
  at T is unattributable (my rerun of the same forged commit: 6/6 pass, 13 passes vs 1 failure
  including the L1 diagnostics). Flake, not a counter defect.
