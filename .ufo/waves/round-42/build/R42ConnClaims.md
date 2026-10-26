# R42ConnClaims — cross-document consistency check (kengaku round 42, wave 1)

Seat: R42ConnClaims (connector, leaf). Scope: every number and hash in
`plans/round-42-claims.md`, the `plans/round42_c1_verify.py` / `plans/round42_c2_verify.py`
docstrings, `.ufo/waves/round-42/claims/*.txt`, `.ufo/waves/round-42/first-run/`, checked
against each other and against `git -C …/kengaku-shokunin log`. Read-only seat: no lane file
was touched; all hashes recomputed on disk.

## Method (commands)

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -15` and
  `git log -1 --format='%H %s' <rev>` for the freeze / receipt / baseline hashes.
- `sha256sum <frozen files>` vs `.ufo/waves/round-42/claims/frozen-digests.txt`.
- `sha256sum -c SHA256SUMS` in `corpus/evidence/round42/tb2-circuit-fibsqrt/`.
- `grep`/`sed` reads of all 13 `.txt` receipts in `.ufo/waves/round-42/claims/`, the
  `envelope.sh`, both control patches, the MUTANTS table
  (`plans/round42_c1_verify.py:145-216`), both counter docstrings (lines 1-93 / 1-63),
  the dry table, the probe receipt, `test_outputs.py`, `sim.c`, `instruction.md`,
  `plans/pkg-spec-r42.json`, `SCORECARD.md` (`### Planned (round 42) — corrected`),
  and a Python case-by-case diff of dry table vs receipt.

## Checked numbers/hashes — all agree (location A vs location B)

1. **Freeze hash** `bc856d803576e182b6c3c12afc6b23f392071c25` — seat spec vs
   `git log -1 bc856d8` → `bc856d803576e182b6c3c12afc6b23f392071c25 round-42: freeze — …`.
   Its stat shows it contains the claims, both counters, probe, spec, dry table, 9
   captures + SHA256SUMS, all controls and witness modules — and NOT the receipt.
2. **Receipt hash** `523b27806be0df26d2235089d845265a29f8cedf` — seat spec vs
   `git log -1 523b278` → matches; commit adds exactly
   `corpus/evidence/round42/fibsqrt-probe.txt` + `.ufo/waves/round-42/first-run/run-log.txt`,
   i.e. after the freeze, matching `round-42-claims.md` §C2 "Receipt (first recorded run,
   committed after this file)". Commit order `d69452c → bc856d8 → 523b278 → fda71ae` is linear.
3. **Baseline tip** `d69452cfa4ea8f95a43caf3727a7c797ba390b6c` — claims.md header vs
   `git log -1 d69452c` → matches.
4. **Frozen digests** — all 12 entries of `claims/frozen-digests.txt` recomputed on disk:
   claims.md `2c4a5e04…`, c1 counter `559fca0c…`, c2 counter `270097fd…`, probe
   `fc58bf3f…`, spec `e836c425…`, gate `ea638822…`, anchor tool `11bb2cad…`, order tool
   `948d5e1d…` (the two truncated digests quoted in claims.md §C1 Surface match these
   prefixes), dry table `9ee60af6…`, SHA256SUMS `36b15d5b…`, `w_anchor.py 8ef62333…`,
   `w_order.py 2da4c12d…`. **0 mismatches.**
5. **14 mutants, 9 anchor + 5 order** — `MUTANTS` table (`round42_c1_verify.py:145-216`):
   X1 X3 X6 X7 X9 X12 X13 X14 X15 + XO1 XO3 XO5 XO6 XO7; `TOTAL = 14`,
   `FLOORS = {"anchor": 9, "order": 5}`; identical lists in claims.md §C1 and in the task
   spec. Confirmed by `MUTANTS total=14`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5` in
   `claims/witness-run.txt`, `control-c1-nothing.txt`, `control-c1-no-mutants.txt`,
   `control-c1-attribution.txt`, `control-c1-tool-edited.txt`,
   `control-c1-direction-mislabel.txt`, `control-c1-witness-as-battery.txt`.
6. **13 direct + 1 indirect (XO6)** — `adv_kind` column of the MUTANTS table (only XO6 is
   `indirect`) vs `ADVERTISED direct=13 indirect=1 none=0` in `witness-run.txt` and all
   control receipts, and claims.md "13 `direct`, 1 `indirect`: XO6".
7. **XO5/XO6 are rc-mirror** — table directions vs `witness-run.txt` (`XO5 order rc-mirror`,
   `XO6 order rc-mirror`) vs claims.md; and `control-c1-direction-mislabel.txt` shows both
   `SURVIVED` under the round-40 `rc-silence` label with `exhibits=0>1,rc-mirror` exactly as
   claims.md quotes.
8. **14 freeze fixtures** — `BATTERY fixtures=14` in `witness-run.txt` (14 `FIXTURE w-…`
   lines: 9 `tool=anchor`, 5 `tool=order`) and in the no-mutants / attribution / tool-edited
   / direction-mislabel / witness-as-battery receipts.
9. **Witness result** — claims.md "14/14 killed, attributed" vs `witness-run.txt`
   `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`,
   every mutant line `killed by=… attributed=L…` (`PREDICATE C1 n/a` is correct: the
   run used `--battery-dir …/witness`).
10. **C1 controls** — claims.md descriptions byte-match the receipts:
    `control-c1-nothing.txt` (`fixtures=0`, `killed=0 survived=14`, `anchor=0/9 order=0/5`,
    `PREDICATE C1 fail`, exit 1); `control-c1-witness-as-battery.txt` (`PREDICATE C1 pass`);
    `control-c1-no-mutants.txt` + `.patch` (`MUTANTS = []`, `total=0`, fail);
    `control-c1-attribution.txt` + `.patch` (span forced to `{1}`, `killed=0 unattributed=14`,
    all lines `span=L1-L1`, fail); `control-c1-tool-edited.txt`
    (`PINS … mismatched=1 first=plans/anchor_digest_check.py`, 9 anchor `invalid`,
    `PINS-AFTER mismatched=1`, fail); `control-c1-hostile-escape.txt`
    (`SETUP fixture 'h-esc42-relative-escape' of battery42/h_esc42.py breaks the contract`,
    exit 2). Envelope lines on all of them carry start/end `date +%T` and
    `local_bin_listing_before=763032563d3739aa after=763032563d3739aa unchanged`, matching the
    Q32 description of `claims/envelope.sh` (script read: it prints exactly those fields).
11. **C2 counts** — claims.md vs `control-c2-nothing.txt`: `checks=9 defects=6` with V2 V3 V4
    V7 V8 V9 DEFECT and V1/V5/V6 ok; `V1 ok listed=9 bad=0 extra=0`; gate `P2 …
    receipt unreadable: corpus/evidence/round42/fibsqrt-probe.txt` and `P10 DEFECT receipt
    unreadable` as claims.md states. `c2-stage-check.txt` tail `stagecheck cases=16 failed=0`
    matches claims.md §"Order of operations".
12. **16 cases, 7/9 split, 0 mismatches, regrade clean** — dry table summary
    `cases=16 predicted_pass=7 predicted_fail=9`; receipt tail
    `cases=16 observed_pass=7 observed_fail=9 mismatches=0` and
    `regrade cases=16 differ=0`; 16 `CASE` lines in each (programmatic count: 16/16, same
    order, every `predicted`/`tests`/`violates=` cell equal, every `match=yes regrade=same`;
    output: "drifts: NONE").
13. **9 captures** — `ls` of `corpus/evidence/round42/tb2-circuit-fibsqrt/` = Dockerfile,
    README.md, gates.txt, instruction.md, sim.c, solve.sh, task.toml, test.sh,
    test_outputs.py (+ SHA256SUMS); `sha256sum -c SHA256SUMS` → 9 × `OK`; the c2 counter
    `CAPTURES` dict (9 entries) carries the same 9 digests; claims.md "9 files + SHA256SUMS"
    and the counter docstring "the nine captures" agree.
14. **Spec rows S125/S126/S127** — `plans/pkg-spec-r42.json` rows: S125 `test_outputs.py`
    sha256 `6117b8ed…0438`, S126 `instruction.md` `a7f50026…b9ea`, S127 `sim.c`
    `700645ac…6173`, `raw_base` pinned at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
    `row_opened 2026-10-26` — equal to the CAPTURES dict, SHA256SUMS, the receipt header
    comment lines, and the truncated hashes quoted in claims.md §C2 Surface. The "17:08 -03"
    opening time in claims.md:69 is corroborated by `.ufo/waves/round-42/build/R42PkgRows.md:158-160`
    (three cmp-identical re-fetches); the first-run probe at 17:11:12 is a later, different
    event (`first-run/run-log.txt`: `start 17:11:12 lane=bc856d8…`, `rc=0 end 17:12:06`).
15. **Grader facts** — `test_outputs.py`: test 1 asserts `/app/gates.txt` exists (`:7-11`);
    test 2 counts every line and asserts `line_count < 32000` (`:21-23`); test 3 runs
    `gcc -O3 /tests/sim.c -o sim` (`:66`) then `/app/sim N` (`:119`). The N table evaluates
    to exactly 28 values, max 48401 (Python `eval` of the list). `sim.c` reads
    `parse_gates("gates.txt")` cwd-relative (`:319`), takes the value from `argv[1]`
    (`:324`), loops 32000 steps (`:335`), and prints the 32 highest-indexed signals
    (`values[num_signals - 32 + i]`, `:340-347`). `instruction.md:8` says the first 32 lines
    come "from … stdin" and `:9` says "the last 32 lines are converted to an integer" —
    matching the receipt's `violates=` tags and the task spec's grader facts. Dry-table
    `TAG` lines: 7 tags (line-form, last-32-lines, gates-file, line-limit, output-function,
    example-208, example-20000) all occur in receipt `violates=` sets.
16. **Receipt headlines** — the spec's per-case claims match the receipt rows: `lookup-28`
    gates_lines=1195 tests=PPP with `violates=…example-208,example-20000`; 31999→PPP,
    32000→PFP ("fails only the size test"), comment-lines/reversed-lines/crlf→PPP,
    trailing-space→PPF, fake-sim-script→PPF, gates-is-directory→PFF.
17. **Frozen predicates verbatim** — C1 predicate sentence in claims.md equals
    `round42_c1_verify.py:9-14` word for word; C2 predicate sentence equals
    `round42_c2_verify.py:8-10`. C2 counter is "V1–V8 re-pointed + V9" per both docstrings.
18. **Carried axis numbers** — claims.md "calibration 8, coverage 7 (capped by … round-33),
    novelty 7, depth 9, operability 8, freshness 8, adjacency 8; lowest non-retired: coverage
    7 tied with novelty 7" equals `SCORECARD.md` `### Planned (round 42) — corrected`
    verbatim; "8 of 89" narrows round-41's recorded "7 of 89" consistently.
19. **Round-41 cross-references** — claims.md's "20 battery40 survivors
    `MUTANTS total=20 killed=0 survived=20`" equals
    `.ufo/waves/round-41/build/R41PlanNext/near40_survivors_only.txt`
    (`MUTANTS total=20 killed=0 survived=20 invalid=0 null_detected=0`); the disclosed prior
    observation (nop 2/3 = PPF, oracle 3/3 = PPP, lookup 3/3 = PPP) matches the receipt's
    own observed rows; "34 unpriced advertised rows" and "XL1–XL6" appear identically in
    claims.md and the counter docstring.
20. **Census** — `claims/census-before.txt` ends `census_rc=0`, consistent with
    `control-c2-nothing.txt` `V6 ok census_exit=0`.

## Drift list

None. Every number, hash, mutant id/direction/kind, case count, control result and
timestamp cited across `plans/round-42-claims.md`, both counter docstrings, all 13
`claims/*.txt` receipts (+ envelope.sh + both patches), `first-run/run-log.txt` and the
on-disk evidence files agrees with `git log` and with recomputed sha256 digests.
Observation (not a drift): the freeze commit does not contain the receipt and
`first-run/run-log.txt` names the freeze lane hash with `rc=0` — both consistent with
"receipt committed after the claims file".

VERDICT: drift-0
