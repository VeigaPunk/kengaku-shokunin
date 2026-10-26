# R40ConnFrontier — frontier/coverage check (kengaku r40 wave 1, 2026-10-26)

Axes named: **coverage** (is the C2 ground new vs the five admitted TB2 graders), **calibration**
(self-assessment denominators in SCORECARD/SHONEN/README vs repo state), **index parity** (README
inventory vs committed bytes). No lane files touched; investigation is read-only. No scratch needed
(no clones/fixtures built).

Repo state at this seat's run (wave 1, all paths `git ls-files`-verified committed):
`corpus/evidence/round40/` = 10 tracked files (receipt, dry table, 8 captures);
`corpus/SOURCES.md` rows S119/S120 at :134-135; `corpus/knowledge/` = 46 entries of which **5**
`tb2-*-grader.md`; **no** `tb2-db-wal-recovery-grader.md`, no README/PROVINCE round-40 text yet
(wave-2/L1 integration, drafts at `.ufo/waves/round-40/build/R40PkgEntry/`).

## 1. Is "binary database file pair → JSON export" ground the lane did not hold? — YES, new

Graded-artefact classes of the five admitted TB2 graders (corpus/README.md:265 and its four
predecessor bullets; entry files in corpus/knowledge/):

| Round | Task | Graded artefact / state |
|---|---|---|
| 35 | protein-assembly | agent-written sequence file vs in-test literals (no reference inputs read) |
| 36 | regex-log | agent-authored regex file, executed in-grader against a fixed in-test log |
| 37 | configure-git-webserver | two live HTTP responses from a lane-built service |
| 38 | build-pmars | a built executable + source tree on disk |
| 39 | git-leak-recovery | git object store/refs + one flag file |

Round 40's `db-wal-recovery` is a sixth class, new on three axes at once:

1. **Source of truth the grader never opens.** All seven tests open only `/app/recovered.json`
   (draft entry cites `test_outputs.py:9,14,23,40,49,85,94`); the SQLite `main.db` and the
   XOR-encrypted WAL are read by no test. No prior admitted grader had a *binary database file pair*
   as the ground state behind the graded artefact.
2. **Destructive-read trap on the ground state itself.** A plain read-write `sqlite3` open first
   destroys the undecryptable WAL, after which the task's own oracle fails 2 tests
   (receipt case `plain-read-then-solve … tests=PPPPFPF`, `corpus/evidence/round40/db-wal-probe.txt`).
   Prior classes' ground states (files, services, repos) were at worst mutable, never
   self-destructing on observation.
3. **Recovery step unobserved / hand-typed export passes.** "Fix the WAL file"
   (`instruction.md:7`, S120) is graded only through export rows: `literals-never-open-db`
   (database never opened) passes 7/7; only 22 of 33 id/name/value cells are pinned; `True` passes
   as an int value; float ids `1.0..11.0` fail only the structure test; an extra field passes
   (receipt cases `literals-never-open-db`, `truth-bool-value-id5`, `truth-ids-as-floats`,
   `truth-extra-field`, all `match=yes regrade=same`).

Probe evidence (frozen, committed):
- `cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS` → 8/8 `OK`
  (Dockerfile, instruction.md, main.db, main.db-wal.encrypted, solve.sh, task.toml, test.sh,
  test_outputs.py).
- `tail -5 corpus/evidence/round40/db-wal-probe.txt` → `regrade cases=28 differ=0` then
  `cases=28 observed_pass=8 observed_fail=20 mismatches=0` (matches the freeze's headline numbers).
- `grep -n cases= corpus/evidence/round40/db-wal-dry-cases-freeze.txt:35` →
  `cases=28 predicted_pass=8 predicted_fail=20` (predictions frozen pre-probe).

The drafter's own headline agrees: the draft entry names "one edge class new to the lane's
**executed** grader sample: the graded artefact is a **JSON export whose source of truth is a
binary database file pair**" (`.ufo/waves/round-40/build/R40PkgEntry/entry.md`, Summary).

## 2. Which frontier clause narrows, and what it should read after

The narrowing clause is the **round-39 §Frontier sub-bullet** of the "Agentic benchmark task-spec
audits" item, `corpus/README.md:308-321` — specifically :320:

> "it stays open for the remaining TB2 task graders (5 of 89 read)"

Per the rounds 35–39 convention (each round appends a new sub-bullet and leaves predecessors
byte-identical), admission should:

- append a `*Partly discharged round 40 (2026-10-26):*` sub-bullet for
  `knowledge/tb2-db-wal-recovery-grader.md` (S119, S120; probe `plans/db_wal_probe.py`; receipt
  `corpus/evidence/round40/db-wal-probe.txt`) naming the new class and the 28-case result; and
- carry the open-tail sentence forward as "**(6 of 89 read)**", keeping the unchanged riders
  ("for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which
  PROVINCE.md refuses to this lane)").

Sibling lines the same integration pass must touch (not in the asked set, recorded for the L1):
- coverage map, `corpus/README.md:265` — a sixth bullet after the "(fifth task,
  repository-history class)" one; the sibling draft already proves the wording
  (`.ufo/waves/round-40/build/R40PkgEntry/readme.md` §1-§2, gate clause P8 verified);
- `## What's here` index row for the new entry (draft §1);
- evidence inventory after `corpus/README.md:472` — a "### Round-40 evidence" section;
- `PROVINCE.md` round-39 paragraph tail: "the remaining **84** TB2 task graders (89 carry
  `tests/test.sh`; **5** are read)" → 83 / 6 are read.

## 3. Self-assessment mismatch census (SCORECARD / SHONEN / README vs repo state)

Mismatches found: **2** (both are wave-1 integration lags, scheduled for the same landing; no line
states a number the repo contradicts).

1. `corpus/README.md:472-475` — the evidence inventory ends at "### Round-39 evidence" while
   `corpus/evidence/round40/` is committed (`git ls-files corpus/evidence/round40/` → 10 files:
   receipt, dry table, 8 captures). The inventory claims to list committed evidence dirs; it omits
   the round's frozen receipt and captures. Index-parity mismatch, resolves with the C2 landing.
2. `corpus/README.md:320` — the frontier tail "(5 of 89 read)" under-reports the repo state: the
   sixth grader's bytes are committed (S119/S120 registered, captures 8/8 `sha256sum -c` OK) and
   probe-executed with a committed receipt (`cases=28 … mismatches=0`, `regrade … differ=0`). This
   is the freeze-scheduled narrowing line (C2 surface names "one §Frontier TB2 sub-bullet narrowed
   by one task"), so it is a pending-narrowing stale denominator, not an error to correct in place.

Lines checked and found **consistent** (not counted):
- `corpus/README.md:265` — "5 of the 89 TB2 task graders": an *admitted-entry* count; `ls corpus/knowledge/ | grep -c '^tb2-.*grader.md$'` → 5. Accurate until admission.
- `SCORECARD.md:729-730` — latest re-derived axis state (novelty 7 · calibration 8 · depth 9 · coverage 7 (capped) · operability 8 · freshness 8 · adjacency 8); carried unchanged by the round-40 freeze. No round-40 axis row exists to contradict.
- `SCORECARD.md` "### Planned (round 40)" — forward-looking and materialized as frozen: planned "TB2 db-wal-recovery @ 2fd12b88"; repo now holds exactly that package. The plan's pilot expectations (oracle 7/7, nop 7/7 fails, byte-equal reruns) match receipt cases `oracle-solve-sh PPPPPPP`, `untouched FFFFFFF`, `regrade cases=28 differ=0`.
- `SHONEN.md` (12 lines) — no TB2/coverage denominators; the "No cross-domain bleed (PROVINCE.md still accurate)" box holds against the admitted-entry state.
- `PROVINCE.md` round-39 paragraph — "84 … 5 are read" matches today's 5 admitted entries (it narrows at landing; outside the asked file set, flagged in §2).

## 4. Boundaries

Read-only seat: no lane file edited, no clone/fixture built, no scratch consumed (nothing to clean).
Evidence commands and outputs are quoted inline; captures verified against their own
`SHA256SUMS` on this host. Judgment of admission stays with the C2 counter
(`plans/round40_c2_verify.py`) and the L1; this seat priced coverage only.

VERDICT: frontier-new-mismatches-2
