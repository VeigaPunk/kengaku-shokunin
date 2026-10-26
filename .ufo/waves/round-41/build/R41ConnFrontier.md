# R41ConnFrontier — frontier/coverage check (wave 1, 2026-10-26)

Seat: R41ConnFrontier (connector, leaf). Lane: kengaku-shokunin @ HEAD `fc79f2a49be0221e138b3885fa0d83bc43b31a42` (freeze commit `8ef8b4fc…` for `plans/round-41-claims.md`; first recorded probe run `f774a87a…`). Evidence below measured on the current tree.

## 1. Is "a grader that embeds its own scheduling model over pinned inputs, reading ICS by regex" ground the lane did not hold (vs the six TB2 graders admitted)?

**Yes — new ground.** The six admitted TB2 graders and their graded artefacts (corpus/README.md:262–267):

| # | After (round) | Graded artefact | How the verdict is computed |
|---|---|---|---|
| 1 | protein-assembly (35) | gBlock composition | literal expected subproteins/order/FLAG-SNAP/linker/GC-window equality |
| 2 | regex-log (36) | agent-authored `regex.txt` | exact `re.findall(...)` equality vs a literal nine-date list over a fixed in-test log |
| 3 | configure-git-webserver (37) | two HTTP responses | one substring assertion (`TEST PASSED`) on helper stdout |
| 4 | build-pmars (38) | built binary + source tree | file presence + `ldd` string scan + regex over program stdout |
| 5 | git-leak-recovery (39) | git repo state | five assertions over refs, dangling objects, flag file, work-tree checksum |
| 6 | db-wal-recovery (40) | `recovered.json` export | seven assertions over one JSON export (DB/WAL pair as source of truth) |

None embeds a domain/scheduling model, none reads ICS, none grades a submission semantically against multiple pinned input files. The `constraints-scheduling` grader (claim §C2) computes its verdict via an embedded scheduling model — `_hard_ok`, `_overlap`, a minute-granularity earliest-slot scan — over three sha256-pinned input calendars, and reads the graded ICS artefact with regexes, not an ICS parser. That is an executed-sample edge class the lane had not held; the claim's own framing confirms it ("a seventh grader class (an embedded scheduling model)", `plans/round-41-claims.md:79`; "Edge class new to the lane", `:84-87`).

## 2. Which frontier clause narrows, and how should it read?

The clause is the "Terminal-Bench 2.0's" scoring-code clause inside the **Agentic benchmark task-spec audits** bullet of `corpus/README.md` §Frontier. Its round-40 sub-bullet currently ends:

- `corpus/README.md:337` — "it stays open for the remaining TB2 task graders (6 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity".
- `PROVINCE.md:445` — "or speak for the remaining 83 TB2 task graders (89 carry `tests/test.sh`; 6 are read)".

After this admission the paragraph narrows **only the "remaining TB2 tasks" count tokens**: 6 → 7 read of 89, remaining 83 → 82, keeping the template wording "narrowed for that one task only / inverse ground stays as written". The coverage map (`corpus/README.md` rows 262–267) gains a seventh bullet for `tb2-constraints-scheduling-grader.md` (S122 `tests/test_outputs.py`, S123 `instruction.md`; S124 = TB2.1 PR #245, tier B, opened in wave 1); PROVINCE gains a Round41 paragraph. One wording note for L1: this is the first admitted grader whose verdict is *semantic* (constraint satisfaction over pinned calendars), so the new bullet should carry the "one new executed edge class" tag used for rounds 37–40, plus the class sentence from the claim (§C2) — not a "same ground" bare clone.

## 3. Self-assessment lines in SCORECARD/SHONEN/README mismatching repo state — count

**0 fresh mismatches.** Evidence:

- `python3 plans/state_check.py --summary` (run from lane root, TMPDIR=scratch) → `VERDICT: PASS — all comparable frozen assertions match`, exit 0 (frozen P2/P3/P4 populations; only informational `OUT_OF_POPULATION` lines for `lessons/round-34…40*.md`).
- Independent counts vs the scorecard's round-40 claims (SCORECARD.md:1450,1461,1482):
  - knowledge files 47 = knowledge index rows 47 (matches "knowledge 46 → 47");
  - SOURCES S-rows 114, max id S121 (matches "SOURCES 111→114"); S122/S123 not yet present — L1 opens them this wave;
  - `tb2-*-grader.md` files = 6 (matches "a sixth TB2 grader executed", "(6 of 89)").
- Root README.md (14 lines) and SHONEN.md (12 lines) carry no numeric repo-state claims; SHONEN pointers resolve.
- Stale *history* cells (e.g. SCORECARD.md:557 `sources-registry` census "rows 25"; :558/:559 selftest counts) are explicitly superseded by recorded errata (R25-E1/E9/E10, R26-E1–E8); state_check emits `SUPERSEDED` for them and the lane's append-only convention treats them as corrected, not fresh mismatches — reported here as not counted.

Neighboring debt (not a self-assessment line, flagged for L1): 23 files under `corpus/lessons/` (rounds 29–40 lessons + spotchecks, incl. `round-29-verifier-spotcheck.md`) are unindexed in `corpus/README.md`'s lessons tables (33 index rows vs 56 files). state_check flags them `OUT_OF_POPULATION`; no line in the three files asserts lessons parity today, so it is a latent coverage gap, not a mismatch count.

## Calibration denominator outside C1

0 (self-assessment mismatch count); caves: 23 unindexed lessons files, and the superseded-history cells above (recorded, not fresh).

VERDICT: frontier-new-mismatches-0
