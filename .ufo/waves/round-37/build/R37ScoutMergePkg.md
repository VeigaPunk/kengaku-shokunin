# R37ScoutMergePkg — merge/kengaku re-screen (round 37, wave 1)

Seat: scout, read-only. Source `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was read only. Nothing adopted. No lane file edited. Only writes: this report and the wave scratch lists in `.ufo/waves/round-37/assimilation/` (new dir, requested). No scratch clone was needed (no fixture ran).

Axes: (a) did the package change since round 36; (b) id-space collision with S111–S113; (c) fit to C2 (pinned TB2 `configure-git-webserver`, a service/state grader read through a shell verifier) and to PROVINCE; (d) duplication against held ground.

## 1. Did the package change? No.

```
$ stat -c '%y %n' SOURCES.append.md MERGE-REPORT.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
2026-10-24 23:33:20 … (all four, one second apart)
```
All four mtimes precede the round-36 screen (2026-10-25). `staged-ids` is byte-equal to the round-36 list (`diff .ufo/waves/round-36/assimilation/staged-ids .ufo/waves/round-37/assimilation/staged-ids` → no output, then `staged-same-as-r36`). Digests now: `SOURCES.append.md` a46458851f93…, `grader-predicate-input-types.md` 350e2677f920… (full values: `sha256sum` output in §6). The round-36 report recorded no staged-file digest, so equality rests on mtime and the id list, not on a digest comparison [INFERENCE: unchanged].

## 2. §10 id extraction (0–3 leading spaces)

Anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (the round-36 `id-collision-check.sh` contract; `sh …/round-36/assimilation/id-collision-check.sh --selftest` → `SELFTEST guard-ok`). Commands (run from the lane root):

```
grep -oE "$ANCH" corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > .ufo/waves/round-37/assimilation/reg-ids
grep -oE "$ANCH" /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md | … > …/staged-ids
comm -12 reg-ids staged-ids > collisions ;  printf 'S111\nS112\nS113\n' > c2-ids ;  comm -12 c2-ids staged-ids > c2-collisions
```
Result (`wc -l`): reg-ids 103 (S001–S110), staged-ids 175 (S077–S251), collisions **27**, c2-collisions **3**.

- Registry vs staged: 27 shared ids = S077–S086, S090–S094, S097, S100–S110. Round 36 had 24; the three new ones (S108, S109, S110) are round 36's own TB2 regex-log rows. Many are the same document as the lane row (S077, S079, S092, S093, S100 share URL; titles differ slightly), others are different documents under the same id: lane S107 is TB2 protein-assembly `instruction.md`, staged S107 is Toolathlon `deploy_containers.sh`; lane S110 is TB2 regex-log `instruction.md`, staged S110 is GENIAC phase-2 detail; lane S101/S102 are rejection markers (`REJECTED: duplicate id; flip: a future candidate must use a new id`).
- **C2 ids S111–S113 collide with staged rows** (`cat c2-collisions` → S111 S112 S113): staged S111 and S112 are GENIAC rows, S113 is a post-5G phase-2 compilation. The lane registry does not hold S111–S113 yet (`grep -c "S11[123]" corpus/SOURCES.md` → 0), so C2's landing creates no registry collision, but any later adoption of staged rows must renumber past **S113**, not past S110 as the round-36 flip said.
- Consequence for C2 landing: none. The staged package is never appended wholesale; C2's rows are lane-authored.

## 3. Fit to C2 / PROVINCE

C2 is one pinned TB2 grader whose verdict comes from a shell script probing a live HTTP service (`plans/round-37-claims.md:62-68`). I searched the staged rows and entries for `terminal-bench|tb2|verify.sh|test_outputs|test.sh|webserver|nginx|bubblewrap|harbor|service|configure-git` (`grep -n -i …` over `SOURCES.append.md`; `grep -l -i …` over `knowledge/`). Result:

- No staged row or entry mentions `configure-git-webserver`, a git-served web root, `verify.sh`, an HTTP/port probe, or a sandboxed executed offline TB2 probe. The only Terminal-Bench rows are S077, S079, S090, S092, S100 (all already held by the lane, same ids) and the only entries mentioning TB are the three round-1/2 entries the lane already holds under the same names (§4) plus `terminal-bench-release-identity.md`.
- Service/process graders appear only as Toolathlon harness architecture: staged S102 (Toolathlon `EVAL_SERVICE_README.md`/`evaluator.py`) and S107 (`deploy_containers.sh`), cited by `benchmark-grader-integrity-models-2026-10-23.md`. That is the *harness* service (where the grader runs), not a grader that probes a service; it does not supply any C2 fact.
- PROVINCE: the round-36 section scopes admission to one grader's offline behaviour (spot-check "adjacency | unchanged"). The Toolathlon packages are a second benchmark; none is shaped like C2.

Conclusion: nothing staged fits C2. No C2 input is missing from the package; C2 stays self-sourced (S111–S113 opened this round).

## 4. Verdict per candidate (packages with grader / verifier content)

| # | Package entry (staged rows) | Verdict | Reason (observed) | Flip condition |
|---|---|---|---|---|
| 1 | `grader-predicate-input-types.md` (S143, S144) | **HOLD** (admit-candidate, unchanged) | Package bytes unchanged since round 36 (§1). The three round-36 defects are still in the text: the claim "never bare strings" is still S143's row cell (`SOURCES.append.md` S143 row); denominator `23 of 38` still at entry line 11 while the round-36 recount is 13+23+1 = 37 for the S130 package (same Toolathlon denominator family); `compare_rating` narrative still at entry lines 16 and 24 (unreproduced by the lane). S144 is own-work, locator `lanes/kengaku/round7/…` (not in this lane; `grep -c shokuknow corpus/SOURCES.md` → 0). Round-37 claims are frozen to C1 and C2 and name no Toolathlon candidate (`grep -n "S143\|predicate-input" plans/round-37-claims.md` → no hit); the claims' own assimilation candidate is `considerthese/2026-10-25.md` 2(a). §10 forbids widening a frozen target. | A later-round claim that re-opens S143/S144; the three text defects repaired; S144's probe re-homed in-lane with an in-lane receipt; rows renumbered past **S113**; landed as a dated amendment. |
| 2 | `benchmark-grader-integrity-models-2026-10-23.md` (S101, S102, S107) | **HOLD** | Fits PROVINCE's grader-coverage theme and is the nearest TB2 relevance (M1 shared-environment verification applies to TB2's `verify.sh`), but its sources are staged ids the lane already burned: lane S101/S102 are `REJECTED: duplicate id` markers whose own flip says a future candidate "must use a new id and pass the source gate"; lane S107 is a different document. No lane entry carries an M1/M2/M3 model split (`ls corpus/knowledge \| grep integrity` → none). Its M1 half overlaps the held `benchmark-verifier-execution-model.md` (S092). Not opened by this lane. No claim names it. | A claim that opens the Harbor/SWE-bench Pro/Toolathlon sources at pins in-lane, re-ids rows past S113, and reconciles M1 with the held verifier-model entry. |
| 3 | `benchmark-grader-integrity-models-2026-10-23b.md` (S108) | **HOLD** | Same family; amends #2 and depends on it ("This amends … round-3 entry"). Its S108 collides with the lane's S108 (`tests/test_outputs.py`, TB2 regex-log). Predicate/tolerance axes are task-parameterised facts about Toolathlon tasks the lane never opened. | Same as #2 and only after #2 lands. |
| 4 | `toolathlon-grader-contract-2026-10-23.md` (S114) | **REFUSE** | Sole source S114 is own-work `lanes/kengaku/round5/toolathlon-grader-tabulation.md` in shokuknow; §10 forbids campaign tools, so the 108-grader tabulation cannot be re-run from the lane. Same ground as the round-36 refusal of S130. | An in-lane re-derivation of the denominator from the pinned tree with the lane's own receipt. |
| 5 | `toolathlon-grader-behaviour-probe-2026-10-23.md` (S130) | **REFUSE** (unchanged from round 36) | Own-work locator; denominator 38 against rows 13+23+1 = 37 (round-36 erratum, `corpus/lessons/round-36.md:28`). | As round 36: in-lane probe re-run at `9be8d8fe` with the lane's receipt and the denominator corrected. |
| 6 | `grader-fixture-probe-stage3.md` (S170, S171) | **REFUSE** (unchanged) | Superseded interim state of the lineage; its stage-4 successor says all four spreadsheet graders discriminate (round-36 spot-check §3 agrees). | Only as a folded history paragraph in a reconciled amendment of #1. |
| 7 | `grader-fixture-coverage.md` (S155) | **REFUSE** (unchanged) | Sole source is own-work, no in-lane receipt. | In-lane re-run of the stage-2 probe with the lane's receipt. |
| 8 | `spreadsheet-grader-fixtures.md` (S180–S182), `grader-sheet-checks-real-pandas-r16.md` (S245–S247), `grader-candidate-coverage{,-r13,-r14,-r15}.md` (S189, S212, S232, S240), `grader-candidate-reconstruction.md` (S197) | **REFUSE** (family; none new) | First line of each file's sources (`grep -m3 "^source:"`) is own-work in shokuknow (`lanes/kengaku/round10…16`), no in-lane receipts; Toolathlon-only, no TB2 or service-grader fact. Round-36 already refused the stage-3/4 lineage on the same ground. | In-lane re-runs with in-lane receipts, per entry. |
| 9 | `terminal-bench-release-identity.md` (S100, S092) | **REFUSE** (unchanged) | Cites S100 and S092, both held (`used-by` = `corpus/knowledge/benchmark-verifier-execution-model.md`); adds no ground. | A release-identity fact no admitted entry states, with a located quote at the pin. |
| 10 | `benchmark-verifier-execution-model.md`, `benchmark-grader-semantics.md`, `benchmark-task-validity-checklist.md` (round 1–2) | **REFUSE** (duplicate path) | The lane holds same-named files (`diff -q` → differ; `wc -l` staged vs lane: 87 vs 175, 95 vs 174, 73 vs 139), so the staged copies are the older, shorter forms [INFERENCE: the lane files are supersets; I did not line-diff content]. Adopting would overwrite or fork held entries. | A staged section the held file lacks, shown by a section-level diff. |

Other staged entries (cjk-*, card-*, post5g-*, osf-*, judge-*, contamination-*, maintainer-*, disclosure-*, geniac-*, eastern-*, japanese-*, benchmark-card-*, per-benchmark-*, preregistration-*, author-approved-*, programme-side-*): out of PROVINCE for C2 and not a service/process/shell-grader candidate; not screened line by line (the title list in `MERGE-REPORT.md` is the evidence). No verdict given; none is in this seat's scope.

Totals over the 10 verdict rows: 0 admit, 7 refuse (#4–#10), 3 hold (#1–#3).

## 5. What changed for the L1 compared with round 36

1. Flip floor for any later adoption moves from "past S110" to "past **S113**" (C2 reserves S111–S113; staged S111–S113 are GENIAC/post-5G rows).
2. Collision count 24 → 27 (S108–S110 landed in round 36); the guard script is unchanged and its selftest still passes.
3. New hold: the integrity-models pair (#2, #3). Round 36 did not give them a verdict row; they are adjacent to C2 through M1, but the lane's rejection markers on S101/S102 require new ids.
4. Nothing to land from the package this round.

## 6. Evidence

```
$ sha256sum .ufo/waves/round-37/assimilation/*
34a28f6889a73c7ba7b68f9dfd2d9dfcb75e38de50d254f20fa8b7e80d4e4730  c2-collisions (= c2-ids: S111 S112 S113)
bf615ce26dfbcc080fe1621dde2111520e0188b3701454f086d29971e6bd6cbc  collisions (27 ids)
fd96aa9008e7897807f77930b7edc207e29c67e1a5765e56022d925ed3be14d3  reg-ids (103)
2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c  staged-ids (175; equals round-36 staged-ids)
$ cd /home/vgpnk/Projects/shokuknow/merge/kengaku && sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  knowledge/corpus/knowledge/grader-predicate-input-types.md
```
Scratch lists: `.ufo/waves/round-37/assimilation/{reg-ids,staged-ids,collisions,c2-ids,c2-collisions}`. Tooling installed: none.

VERDICT: package-0-admit-7-refuse-3-hold
