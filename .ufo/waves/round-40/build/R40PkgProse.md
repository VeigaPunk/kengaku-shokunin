# R40PkgProse — C2 lane prose (PROVINCE / README / SKILL), round 40 wave 1

Seat: R40PkgProse (scribe, leaf). Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Task: draft paste-ready prose for C2 only — no lane file edited, no product code, no counter, no probe run.

## Behavior

I read the frozen claims (`plans/round-40-claims.md`, full), the frozen receipt
`corpus/evidence/round40/db-wal-probe.txt` (28 cases + 2 summary lines), the frozen dry table
`corpus/evidence/round40/db-wal-dry-cases-freeze.txt` (6 TAG lines + 28 CASE lines), the eight captures in
`corpus/evidence/round40/tb2-db-wal-recovery/` plus `SHA256SUMS`, the round-35..39 prose shapes in
`PROVINCE.md`, `corpus/README.md` and `SKILL.md`, and the V7 rule in `plans/round40_c2_verify.py` — then drafted
three paste-ready blocks. Nothing was executed against the lane; no clone was made, no git command was run, no
`TMPDIR` scratch tree was needed, and no tool was installed (`pacman` untouched, nothing filed).

## Artifacts

| what | path (relative to the lane root) |
|---|---|
| draft (a) PROVINCE round-40 paragraph | `.ufo/waves/round-40/build/R40PkgProse/province-round40.md` |
| draft (b) README sixth TB2 sub-bullet (+ optional §Open gaps chronology entry) | `.ufo/waves/round-40/build/R40PkgProse/readme-frontier-bullet.md` |
| draft (c) `SKILL.md` section "Database-recovery TB2 grader — round 40" | `.ufo/waves/round-40/build/R40PkgProse/skill-section-round40.md` |
| receipt: tag→label derivation (reproduces V7's `derive()`) | `.ufo/waves/round-40/build/R40PkgProse/receipt-tag-derivation.txt` |
| receipt: auditable case → tests-letters index | `.ufo/waves/round-40/build/R40PkgProse/receipt-case-index.txt` |
| this report | `.ufo/waves/round-40/build/R40PkgProse.md` |

## Evidence ledger

Every number that appears in the drafts:

1. `cases=28 observed_pass=8 observed_fail=20 mismatches=0` — `corpus/evidence/round40/db-wal-probe.txt:35`
   (read in full; 28 `CASE` lines at `:6-33`, `regrade cases=28 differ=0` at `:34`).
2. Frozen instruction lines per tag — `grep -n "TAG " corpus/evidence/round40/db-wal-dry-cases-freeze.txt` →
   `TAG fix-wal instruction.md:7`, `extract-all :8`, `json-at-path :9`, `record-format :12`, `sorted-by-id :13`,
   `eleven-records :13` (`:1-6`).
3. Label derivation (my reproduction of `derive()`, `plans/round40_c2_verify.py:209-214`), command
   `python3 - <<'PY' …` over the receipt, output (`receipt-tag-derivation.txt`):

   ```
   fix-wal        partly     pass=5  fail=18 total=23
   extract-all    partly     pass=4  fail=11 total=15
   json-at-path   enforced   pass=0  fail=5  total=5
   record-format  partly     pass=2  fail=6  total=8
   sorted-by-id   enforced   pass=0  fail=1  total=1
   eleven-records enforced   pass=0  fail=10 total=10
   cases 28 observed_pass 8 observed_fail 20
   ```

4. "22 of the 33 id/name/value cells" — `test_outputs.py:53-58` pins `len(data) == 11` and
   `ids == list(range(1, 12))` (11 id cells); `:64-67` pins the values of ids 1-2 (2); `:70-80` pins the names of
   ids 3-11 (9). 11 + 2 + 9 = 22 of 11 records × 3 fields.
5. Test letters per case — `receipt-case-index.txt` (generated from the receipt; every `receipt:N` cite in draft
   (c) was checked against this index).
6. Grader line map used in draft (c) — `grep -n "" corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py`:
   `exists :7-9`, `is_valid :12-18`, `structure :21-35` (`required_fields :27-32`, type checks `:33-35`),
   `sorted :38-44`, `completeness :47-80`, `no_duplicate :83-89`, `wal_was_decrypted :92-107`.
7. `test.sh:18-29` — `uvx … pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py` then
   `echo 1|0 > /logs/verifier/reward.txt` (`grep -n "" test.sh`).
8. `solve.sh:8` — `# Print current database content (read-only to avoid WAL interaction)`; the destructive-read
   trap's publish is this comment plus `:10`'s `file:/app/main.db?mode=ro`.
9. `task.toml:29` `docker_image = "alexgshaw/db-wal-recovery:20251031"`, `:34` `allow_internet = true`;
   `Dockerfile:3` `FROM ubuntu:24.04`, `:14-15` the two `COPY` lines.
10. Probe semantics cited in draft (c) — `plans/db_wal_probe.py:3-10` (modes), `:10-20` (sandbox shape, recipe
    error = exit 2), `:25-29` (ground truth computed from the captures under XOR 0x42), `:314-364` (exit-2
    setup paths).
11. Captures present: `ls corpus/evidence/round40/tb2-db-wal-recovery/` → `Dockerfile instruction.md main.db
    main.db-wal.encrypted solve.sh task.toml test.sh test_outputs.py SHA256SUMS` (8 captured + sums).

## Draft (a) — PROVINCE.md round-40 paragraph

Shape matches the round-38/39 blocks: **Core addition** (task, commit, entry + S119/S120, probe, receipt numbers),
the new graded-state class (one JSON export whose source of truth is a binary database file pair), the observed
lines with receipt cites, the "records how that captured grader answers those synthetic states only" clause, the
limits (host packages, unprivileged, image never pulled, published trap), the ordering disclosure
(`c2-stage-check.txt` → `stagecheck cases=28 failed=0`, grader never imported in stage mode), the adjacency
routing, and the narrowing sentence ("The round35/36/37/38/39 paragraphs above stay as written; this paragraph
narrows only their *remaining TB2 tasks* clause for this one task"). Remaining count stated as **83** (89 − 6).

Two deliberate wordings: the entry is described as claiming *a probed instance* of the destructive-read behaviour
(the oracle publishes it at `solve.sh:8`), never a discovery; and storage-repair doctrine is routed to the sibling
lanes that own it rather than stated here.

## Draft (b) — corpus/README.md

New sixth sub-bullet appended after the round-39 bullet (`corpus/README.md:265`), in the same five-part shape
(label with class, depth + date, entry/SOURCES/probe/receipt pointers, the "(6 of the 89 TB2 task graders; not
breadth, and no quality, validity, difficulty or gameability verdict)" parenthesis, the observed content, the
class sentence). The optional companion block drafts the matching *Open gaps → "Agentic benchmark task-spec
audits"* chronology entry (shape of `:309-321`, ending "narrowed for that one task only … (6 of 89 read)"); it is
marked optional so the L1 can drop it if the chronology stays one-entry-per-round.

## Draft (c) — SKILL.md section, 14 decision-table rows

Section shape follows round 38/39: citation gate (run the probe; exit 0/2 semantics; `--dry`/`--stage-check` are
not evidence; receipt summary + `regrade` line), the class difference, then
`### Decision table — what the grader reads, and what passes it` with columns
`what the grader actually reads | what passes | what a reviewer should check instead | cite`, then
"What a green means", the six-tag requirement-map paragraph with derived labels, the limits paragraph, and the
`A property of this capture at 2fd12b88; …` disclaimer.

Row inventory — every row cites at least one receipt case id:

| # | reads | cite |
|---|---|---|
| 1 | `os.path.exists` only | `truth-trailing-garbage` (receipt:26) |
| 2 | `json.load` + list + non-empty | `empty-list` (28), `truth-wrapped-object` (23) |
| 3 | `required_fields.issubset` | `truth-extra-field` (22) |
| 4 | `isinstance(int/str)` | `truth-bool-value-id5` (31), `truth-value-float-id1` (18), `truth-ids-as-floats` (25) |
| 5 | `ids == sorted(ids)` | `truth-reversed-order` (19), `truth-plus-duplicate-id11` (20) |
| 6 | `len == 11`, `ids == 1..11` | `literals-never-open-db` (15), `truth-drop-id11` (29), `empty-list` (28) |
| 7 | `len(ids) == len(set(ids))` | `truth-plus-duplicate-id11` (20), `truth-dup-id10-no-id11` (21) |
| 8 | values of ids 1-2 only | `truth-value-id3-wrong` (30), `literals-never-open-db` (15) |
| 9 | names of ids 3-11 only | `literals-names-1-2-wrong` (16), `literals-id3-name-wrong` (17) |
| 10 | `test_wal_was_decrypted` | `literals-never-open-db` (15), `truth-ids-as-strings` (24), `decrypt-in-place-no-json` (14) |
| 11 | nothing reads the WAL/db | `decrypt-in-place-no-json` (14) |
| 12 | wrong-key XOR | `xor-wrong-key` (11), `base-only-ro` (9) |
| 13 | plain read-write open | `plain-read-then-solve` (10) |
| 14 | baselines + oracle | `empty-app` (6), `untouched` (7), `oracle-solve-sh` (8), `decrypt-then-extract` (12), `decrypt-checkpoint-truncate` (13) |

## Findings (adjacency, observation-only)

1. **The seventh test is not a WAL test.** `test_wal_was_decrypted` (`:92-107`) asserts `len(data) > 5` and then
   re-reads two cells already pinned by `test_recovered_data_completeness` (id 1 value, id 6 name) behind `if`
   guards. `literals-never-open-db` passes it with the WAL untouched (receipt:15); `truth-ids-as-strings` passes
   it while failing tests 3-5 because the dict keys are strings, so `1 in id_to_item` is false (receipt:24,
   `PPFFFPP`) — the named-for-decryption test can pass on a state that skipped both re-reads.
2. **`test_no_duplicate_ids` cannot fail alone.** Both duplicate witnesses fail tests 5 and 6 together
   (`PPPPFFP`, receipt:20,21), because `len == 11` plus `ids == 1..11` already excludes duplicates. It is a
   redundant assertion over the same bytes.
3. **The pinning is asymmetric.** 22 of 33 cells: ids all 11, values only 1-2, names only 3-11. A hand-typed
   export with correct names and arbitrary integers for ids 3-11 passes 7/7 (receipt:15,30); wrong names for
   ids 1-2 pass 7/7 (receipt:16). Only id 3's name is sampled, not ids 1-2's.
4. **The graded state never includes the database.** A repaired WAL with no export is `FFFFFFF`
   (receipt:14); a hand-typed export with no repair is 7/7 (receipt:15). The instruction's first ask
   (`instruction.md:7`) therefore has zero assertions behind it; only its downstream symptom is graded.
5. **One open destroys the evidence, and the oracle then fails too.** `plain-read-then-solve` (receipt:10) is
   `PPPPFPF`: the same two tests that catch a 5-base-row state (receipt:9,11) fail after the task's own
   `solve.sh` runs on a database whose WAL a plain open already deleted. The behaviour is published by the
   oracle itself (`solve.sh:8`), so the prose claims a probed instance, not a discovery.
6. **Round-40 baselines differ in direction from round 39.** `empty-app` and `untouched` are both `FFFFFFF`
   (receipt:6,7) — the image ships no export, so the do-nothing floor is 0/7 rather than round-39's 4/5. The
   cheap pass here is hand-typed literals, not partial work.
7. **`sorted-by-id` rests on one case.** The frozen set has exactly one violating witness
   (`truth-reversed-order`, receipt:19), so its `enforced` label is V7-valid but thin; the prose says so.

## Conflicts and unverified brief claims

- The wave brief says "`regrade cases=28 differ=0`, second run byte-equal". The receipt does carry
  `regrade cases=28 differ=0` (`db-wal-probe.txt:34`), but `ls corpus/evidence/round40/` lists only
  `db-wal-dry-cases-freeze.txt`, `db-wal-probe.txt`, `tb2-db-wal-recovery` — no second-run artifact — so I did
  **not** assert the byte-equal second run in any draft and I did not rerun the probe to produce one. Verbatim
  observation: `ls corpus/evidence/round40/` → `db-wal-dry-cases-freeze.txt  db-wal-probe.txt
  tb2-db-wal-recovery`.
- Every other brief number checked out against the receipt without change: 28 cases, `observed_pass=8`,
  `observed_fail=20`, `mismatches=0`; 22-of-33 pinning; `literals-never-open-db` 7/7; `truth-bool-value-id5` 7/7;
  `truth-ids-as-floats` structure-only failure; `truth-extra-field` 7/7; `xor-wrong-key` 5 base rows;
  `plain-read-then-solve` two failures; `decrypt-in-place-no-json` 0/7.
- No contradiction found between `plans/round-40-claims.md` §C2 and the receipt.

## Gates

- I ran no lane verification (no counter, no probe, no gate, no battery). Draft (c) describes the probe's gate in
  the third person from `plans/db_wal_probe.py`'s docstring and exit paths, not from a run of my own.
- Drafts are unintegrated by design: `PROVINCE.md`, `corpus/README.md`, `SKILL.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/` and `.ufo/waves/round-40/claims/` were read, never written.
- Nothing in this report or in the drafts may be read as modifying the frozen contract, axes or judgment.

## Out of scope (for the L1 / sibling seats)

- The knowledge entry itself (`corpus/knowledge/tb2-db-wal-recovery-grader.md`) and its `## Requirement map`:
  V7 requires exactly the six tags in the counter's row shape, each with the frozen line and at least one cited
  violating case id. My derived labels are in `receipt-tag-derivation.txt`; if the entry seat drafts different
  labels, V7 fails (`plans/round40_c2_verify.py:217-253`).
- The README index row for the new entry (the table at `corpus/README.md:68-72`) and the PROVINCE placement
  point (after the round-39 block, before `## Open gaps`-style tail); S119/S120 already exist at
  `corpus/SOURCES.md:134-135` and were not touched.
- The C2 counter run, the gate rerun, and the `plans/pkg-spec-r40.json` admission are not mine; C1 prose is not
  mine.
- No evidence file, capture, claim or frozen digest was modified.

VERDICT: c2-prose-drafted-14-rows
