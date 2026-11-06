# Receipt (b) — gates judged through mutants/forgeries: sibling overlaps, round 95

## kaidoku @ b0a7bb8c — freeze family byte-stable since r94; round-100 adds its own forgery controls

Tracked diff c19d57cd2e65 (r94 pin) → b0a7bb8c (current HEAD) over `tools/ plans/`:
only two commits, both round-100 (a610671d7 `round-100: C1 candidate
tools/round-100/upx-pe-repair.py`, 8e24c29a3 `round-100: freeze — plan, C1 battery + red
fixtures, C2 counter + controls, S327 copy, census-start`). The r94-cited freeze family is
unchanged; re-verified at the new HEAD:

- `tools/round-44/c2-counter.py:595-597` — `freeze_integrity(...)` "A changed frozen path is
  exit 2, never a pass." (identical bytes)
- `tools/round-50/selftest-r49-c2.py:28-49` — `--mutant-counter PATH`: "the counter file at
  PATH replaces the frozen one (its blob is grafted into synthetic FREEZE/BASE commits in the
  fixture clone only, so it passes its own counter_not_frozen guard) and the same expected file
  is applied. Exit 1 = the self-test caught the mutant" — battery-DRIVEN-RED precedent for
  kengaku W3 (`plans/round95_c2_counter.py` BATTERY_PROBES), not just W5.

New in round 100 (mechanism-duplicate of R95-C2's class, different object — kaidoku's
SKILL.md/registry + UPX repair tool):

- `.ufo/waves/round-100/pre/c2-forgery-controls.txt` — forgeries F-drop 241573e9, F-tool
  b4b0c4fd, F-dup 3ef454b3 (forged SKILL.md copies, forged `upx-field-value-repair.py`) each
  `met False`, `rc=1` against kaidoku's C2 counter — kaidoku's counter discriminates its
  forgeries, the same polarity kengaku's census asserts (14 → 0).
- `tools/round-100/forgeries/h0-identity.py` … `h6-exec-only.py` (7 generated forgeries,
  `gen-forgeries.py`), `.ufo/waves/round-100/pre/forgery/F-{drop,dup,tool}.*` fixtures.
- Note: `census-start.txt` in the same commit is a fleet *sources* census run (W04 rows,
  rc=0) — the "census" word there is the SOURCES census, not a forgery census.

Dispositions: complement in object, duplicate in mechanism (counter + forgery battery +
red expectation). Cross-cite as convergent evolution; never absorb (F-rule also forbids
instrument swapping in-round).

## mado @ 24ba2a9d — unchanged since the r94 pin

Same HEAD as round 94's report (`24ba2a9ddac2`); `quality/check-freeze-order.py` docstring
re-read (lines 1-14): first-parent full-history FREEZE-commit derivation, "Reads git objects
only", revert-restored-freeze-edit-reads-OK stance intact. The three-lane semantic fork
(mado OK vs kengaku v2 breach `plans/round94_freeze_integrity.py` vs kaidoku sees
touch-and-restore) carries over verbatim — documentation debt, not a defect.

## chousa @ 378fda82 — practice-level freeze discipline and the inverse-direction lineage

- Per-seat `freeze_integrity` receipt convention (no standing gate): r60 wave seats embed a
  `freeze_integrity` field in their result JSONs
  (`.ufo/waves/round-60/w1-results.json:10,64,184,340`), r60 had a genuine claim-SHA mismatch
  block (09d8053f vs 65721569, `ReviewFreeze.md:1-3`), r65 `ReviewFreeze/freeze-integrity.txt`.
- `corpus/lessons/round-53-verifier-spotcheck.md:27` — `forge-c1.py` "passes 8/8 on six runs
  while canning REAL and string-stubbing --selftest; committed as controls/forge-c1.py";
  `:83` — "Frozen-counter forgeability streak (RW-1, 5 rounds) … a forged REAL leg still
  passes". `corpus/lessons/round-54.md:21` — r54 standalone forge receipts
  (`controls/c1-forge.txt`, `controls/c2-forge` family).
- Label discipline: `:25`,`:81` — "tool-file sha256" (`32628bbc…`) vs fixtures digest, a
  report-label rule.

chousa forges *counters* that pass its own gate; kengaku forges *gates* that pass its own
counter. Inverse directions of the same calibration question — complement; the RW-1 streak is
prior art for treating counter-forgery as a standing measurable.

## kama @ 9b4c7af1 — nearest `--tool-file` primitive

`tools/round64-c1-counter.py:1727-1734` — `def tool_files(repo, tip, work)`: "Write the tip's
tool + dependency to work/tip. Returns tool path or None". The counter materializes a *tip's*
tool blob and runs it — the closest sibling mechanism to kengaku's census running an arbitrary
`--tool-file` gate blob through the counter (`plans/round95_false_gate_census.py:117-122`
writes `work/gate-<gid>.py` from `git show rev:path`). Same words, different semantics
(tip-pinned, single tool vs adversarial population); complement.

## Mutation-culture adjacency (technique, not gate self-mutation)

- audio @ f9da7ee9 — new r96/r97 mutation trees since r94:
  `corpus/live/r96-critic/measure_audio.r96critic.fixtures-copy.py`,
  `corpus/live/r97-verifier/mut/{min-getreg,min-nop,min-sha,min-stim}/corpus/fixtures/measure_audio.py`
  (revert-class mutants of its own driver, fixtures-copy variant).
- game-dev-2d @ 1e033ef0 — `reports/round-100/r100-critic.md:85-88` — "dead-allowlist mutant
  battery" (sole false gate `r100_expected_errors_all_matched`), "drop-mutant battery"
  (vacuity check: 491 rows all-PASS over zero rows), "pin mutants" m_clip/m_focus/m_seq.
- Neither mutates a *gate* through a copied CLI path; kaidoku's r49/r50 alt-path counter copy
  remains the nearest prior instance of kengaku's W5 class.

## Verdict (b)

Three sibling mechanisms touch the class — kaidoku (standing tracked counter family + new r100
forgery controls), mado (standing freeze-order gate), chousa (per-seat freeze-integrity
practice + forged-counter lineage) — all complements in object; none duplicates kengaku's
object (the round-94 gate v2 + the 14-gate false population + the W1-W5 counter + the census).
PROVINCE holds: nothing absorbed; every overlap is routed as prior art.
