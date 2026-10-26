# R39ConnFrontier — frontier/coverage check (kengaku r39 wave 1, connector)

Seat: R39ConnFrontier (connector, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` read-only; no lane file edited, staged or committed. Evidence gathered from committed repo state at lane tip `7504738` (round-39 wave-1 dispatch), freeze `088f7c3`, first recorded probe run `6a1eb5e`.

## 1. Is "repository-history state" ground the lane did not hold?

**Yes — frontier-new.** The four admitted TB2 grader entries' graded-state classes, each read from its own entry:

| Admitted entry (round) | Graded state / artefact class | Location |
|---|---|---|
| `tb2-protein-assembly-grader.md` (35) | one pytest fn over an agent-authored **gBlock file** — "the five expected subproteins are amino-acid **literals** in the test file"; probe output is a synthetic gBlock string | `corpus/knowledge/tb2-protein-assembly-grader.md:10-16` |
| `tb2-regex-log-grader.md` (36) | "The graded artefact is not a data string the agent writes: it is a **regex pattern file**" | `corpus/knowledge/tb2-regex-log-grader.md:11` |
| `tb2-git-webserver-grader.md` (37) | "the graded state is two HTTP responses"; table row: "the graded state need not come from a repository, a hook or a push" | `corpus/knowledge/tb2-git-webserver-grader.md:39,149` |
| `tb2-build-pmars-grader.md` (38) | built executable + source tree: file presence, `ldd` string scan, dir shape, stdout prefix; "Two different objects are graded under the name `pmars`" | `corpus/knowledge/tb2-build-pmars-grader.md:82`; `PROVINCE.md:293-295` |

None of the four reads a git repository's object store, refs, reflog, dangling objects or work-tree checksum. The round-39 claim's class is new to the executed sample:

- "Edge class new to the lane: the graded state is a git repository's object store and refs plus one flag file, checked by `git log --all` greps, `git fsck` dangling objects and a work-tree checksum" (`plans/round-39-claims.md:70-71`).
- Confirmed against the captured grader: `test_outputs.py` asserts via `git log --all --grep/-S`, `git fsck --no-reflogs` and a work-tree checksum (receipt `corpus/evidence/round39/git-leak-probe.txt` CASE lines; captures `corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py` sha256 `dc7b01c1…`, captured at pin `2fd12b88`). `cases=25 observed_pass=13 observed_fail=12 mismatches=0`; first-run record `.ufo/waves/round-39/first-run/first-run.txt`: `rc1=0 rc2=0; cmp run1 run2 -> byte-equal`, run1 sha256 `d7f3a465…` equals committed receipt sha256.

Adjacent ground checked and ruled not-holding: `knowledge/benchmark-verifier-execution-model.md` (r31) describes SWE-bench Pro V2's own *git-based test-space reset* as harness-restore behaviour, not a graded-artefact class; the lane's own `plans/pkg_gate.py` reads git history as an internal instrument, not benchmark-grader ground. No other corpus entry executes a grader over repository history.

## 2. Which exact frontier clause narrows, and what it should read after

Clause: `corpus/README.md` §Frontier → **Agentic benchmark task-spec audits** bullet → round-38 sub-bullet tail (lines 301-305):

> "The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (4 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane)."

After the round-39 admission this should read (following the per-round convention of a new sub-bullet + count bump in the tail):

- A new `*Partly discharged round 39 (2026-10-26):*` sub-bullet after line 305: reads/executes the fifth pinned TB2 grader `git-leak-recovery/tests/test_outputs.py` + `instruction.md` @ `2fd12b88` (rows S117/S118), probe `plans/git_leak_probe.py`, receipt `corpus/evidence/round39/git-leak-probe.txt` (`cases=25 observed_pass=13 observed_fail=12 mismatches=0`, second run byte-equal), entry `corpus/knowledge/tb2-git-leak-recovery-grader.md`; state the new edge class (repository-history state: git object store + refs + flag file, `git log --all` greps, `git fsck` dangling objects, work-tree checksum) and that the clause stays open for the remaining TB2 task graders **(5 of 89 read)**, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (refused).
- The round-38 tail at lines 302-303 should be updated from "(4 of 89 read)" to "(5 of 89 read)" — the round-37 bullet (line 290) already shows this pattern of bumping the count in the chronologically newest tail.

Mirror landing updates required (same admission): one coverage-map bullet (a "fifth task, repository-history-state class" bullet mirroring line 263's "fourth task" bullet), one PROVINCE "Round39 partial frontier admission" paragraph after `PROVINCE.md:309`, SCORECARD round-39 row (knowledge rows 45→46, SOURCES 109→111 per the C2 claim), and a `Round-39 evidence` README section (captures/receipt already exist at `corpus/evidence/round39/`, unindexed).

## 3. Self-assessment line mismatches (calibration denominator outside C1)

Counted by scanning SCORECARD.md, SHONEN.md, README.md and corpus/README.md against the committed repo state.

**Mismatch count: 1.**

1. `corpus/README.md:101` — "### `lessons/` — round lessons and audits (index)" claims the table is the lessons index, but 20 committed lesson files are absent from it (verified via `grep -oE 'lessons/[A-Za-z0-9._-]+\.md' corpus/README.md | sort -u` vs `ls corpus/lessons/*.md | xargs -n1 basename | sort -u`; all are `git ls-files`-tracked): `round-29-verifier-spotcheck.md`, and for rounds 30-38 each `round-NN.md` + `round-NN-verifier-spotcheck.md`. (`round-28.md`/`round-29.md` are referenced in the per-round supporting-artifact tables at lines 364/393, so they are not counted; rounds 30-38 have no such reference anywhere.) These are all committed (e.g. `round-38.md` landed at `a022ae6`/`ef2fba0`), so the index claim mismatches the repo state.

Checked and **not** mismatches:
- `SHONEN.md` (12 lines): generic promotion checklist, no countable repo-state assertions.
- `README.md` (14 lines, lane root): no countable claims.
- `SCORECARD.md`: round-38 section's counts re-verified against disk — SOURCES `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 109 (row claims 107→109); knowledge entries 45 files = 45 README rows (row claims 44/44→45/45); TB2 count claims are per-round historic records ("4 of the 89", line 263) and are true of the current 4 admitted entries. "Planned (round 39)" bullet (lines 1372-1373) matches the frozen claims; `first-run.txt` confirms "first recorded probe run before any --rerun control".
- The historical "unopened leads" phrasing (`PROVINCE.md:123-125`, `corpus/README.md:284`) is kept verbatim by the lane's append-only convention with per-round narrowing paragraphs; not mismatches under that stated convention.
- S117/S118 rows not yet in SOURCES is the freeze's planned landing state, not a mismatch; the L0 cap question `kengaku | round-33` exists at fleet root `.ufo/l0-questions.md:163`.
- `corpus/lessons/round-39.md` exists only as an untracked wave-1 draft (git status `??`); excluded from the count.

## 4. Risks / notes for the L1

- If the round-39 landing adds the lessons index rows for rounds 30-38, the mismatch count above drops to 0; the count is a pre-landing snapshot (wave 1).
- The new grader class wording should mirror the round-38 entry's discipline: "not breadth, and no quality, validity, difficulty or gameability verdict" — the 5-of-89 count is cumulative, not a class claim.

## Evidence commands

- `git log --oneline -5` → tip `7504738`, freeze `088f7c3`, first probe run `6a1eb5e`.
- `grep -oE 'lessons/[A-Za-z0-9._-]+\.md' corpus/README.md | sed 's|lessons/||' | LC_ALL=C sort -u` (33) vs `ls corpus/lessons/*.md | xargs -n1 basename | LC_ALL=C sort -u` (53) → 20 unindexed committed lesson files.
- `git ls-files corpus/lessons/ | grep -E 'round-(29|3[0-9])'` → all 20 tracked.
- `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 109; `ls corpus/knowledge | wc -l` → 45.
- `cat .ufo/waves/round-39/first-run/first-run.txt` → `rc1=0 rc2=0; cmp run1 run2 -> byte-equal`; `sha256sum corpus/evidence/round39/git-leak-probe.txt` → `d7f3a465…` (matches first-run run1).

VERDICT: frontier-new-mismatches-1
