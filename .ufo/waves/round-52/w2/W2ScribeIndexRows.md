# W2ScribeIndexRows — round 52, wave 2 (falsify), scribe seat

Lane `kengaku-shokunin`, HEAD `87301bacca90c03fa915716fbe6d7023762c5ab3` (`git rev-parse --show-toplevel` = lane root). Axis: coverage. Leaf seat; no subagent dispatch; no lane-tree edit.

## Result

- **Index rows drafted** at `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeIndexRows/index-rows.md` (copy: `.ufo/waves/round-52/w2/W2ScribeIndexRows/receipts/index-rows.md`). Four artefact groups are pasteable now (two counters, the population manifest, the claims file, the `corpus/evidence/round52/graders/` dir). The knowledge row, lesson row, coverage bullet and frontier bullet are **conditional**: their files are not on disk, and the capability they index is admitted only if `PREDICATE R52-C1` passes.
- **Frontier clause advanced:** `corpus/README.md` `## Frontier`, bullet **Agentic benchmark task-spec audits** (line 329). The open part advanced is the *graders* leg for Terminal-Bench 2.0. Contamination and runtime task validity are not advanced.
- **Attack landed?** This seat attacked nothing; it measured the index inputs. Two measured findings matter to the integrator (below).

## Measurements (commands run read-only, `TMPDIR` in scratch)

```
python3 plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin   # exit 1
python3 plans/round52_c2_registry.py     --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin   # exit 0
python3 plans/round52_c1_grader_audit.py --selftest                                              # exit 0
python3 plans/round52_c2_registry.py     --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --selftest   # exit 0
```

R52-C1 (literal):
- `TASKS total=89 records=89 classified=88`
- `CAPTURES expected=184 present=183 mismatched=0`
- `CLASS V1=2 V4=0 V2=53 V3=31 V0=3`
- `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`
- `CANDIDATES total=29`; `CONFIRMED new=0 []`; `PRIOR-ART ok=False urls=0`; `LABELS agree=0 of 0`
- `PREDICATE R52-C1 fail` (exit 1)
- A5: `CAPTURES present+pinned_excluded=184 of 184`; `TASKS classified+excluded=89 of 89`; `PREDICATE R52-C1-A5 fail`

R52-C2:
- `ADVERTISED total=72`; `REGISTERED total=72 rows=74`
- `MISSING 0`; `INCOMPLETE 0`; `ENTRY-MISSING 0`; `SELFTEST-UNBACKED 0`
- `PREDICATE R52-C2 pass` (exit 0)

Selftests: R52-C1 `cases=6 failures=0` (exit 0); R52-C2 `cases=3 failures=0` (exit 0).

Tree counts: `corpus/evidence/round52/graders/` holds 89 task directories, 185 files (183 captures, `SHA256SUMS` with 184 lines, `EXCLUDED.md`). Population `plans/round52-tasks.json`: `task_count=89`, `capture_file_count=184`, `sha256 0230b68c…`. `plans/round52_c1_grader_audit.py` `sha256 0b1d4213…` (429 lines); `plans/round52_c2_registry.py` `sha256 b9ce9439…` (199 lines).

## Findings for the integrator

1. **Stale receipts in `.ufo/waves/round-52/claims/`.** `c1-after.txt` shows `CAPTURES present=89` and `c2-after.txt` shows `MISSING 28`. At HEAD `87301ba` the same counters give `present=183` and `MISSING 0`. Neither file is the after-run. Regenerate the after-run receipt at the landing revision before citing any number from them.
2. **Knowledge entry, lesson, `confirmations.json`, `prior-art.md`, `labels.json` are not on disk.** The planned entry name `corpus/knowledge/tb2-grader-vacuity-triage.md` comes from the wave-2 spec; the lesson is `corpus/lessons/round-52.md`. `W2ExecEntryDraft` and `W2ExecLessonDraft` had written no draft files at measurement. Their index rows stay drafts until the files land.
3. **Literal C1 is `fail` and A5 is `fail`.** The A5 line adds the pinned-absent capture and the 89th classified task; it does not add the missing `CONFIRMED` or `PRIOR-ART` legs, so `R52-C1-A5` fails too. The index therefore records the capability as landed-not-admitted. Variant B of the frontier bullet is the one to use at the present measurement.
4. **SOURCES ids.** The registry's highest id at HEAD is `S178`; `S179` (the TB2 population row drafted by the wave-1 scribe) is not in `corpus/SOURCES.md` yet. The knowledge row cites `S179` and must be checked against the registry at landing.
5. **`corpus/README.md` is a messy append-log.** The round-52 rows go into four anchors (plans table; knowledge table; lessons table; coverage map and frontier). The draft gives content anchors, not line numbers, because the tree moves during integration.

## Frontier clause

`corpus/README.md:329` — **Agentic benchmark task-spec audits**: "the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately". Round 52 advances the grader leg for Terminal-Bench 2.0 at the population level (bytes-level triage of all 89 graders). It does not advance: hand-read depth (12 of 89 TB2 graders stay hand-read unless confirmations land); scoring code for the other 77; SWE-bench Pro V2 and Toolathlon; contamination; runtime task validity (which `PROVINCE.md` refuses to this lane).

## Commands run by this seat (all read-only on the lane)

- `git rev-parse --show-toplevel`, `git log -1`, `git status --short -- plans corpus` (0 lines — plans and corpus clean)
- the four counter invocations above
- `sha256sum` of the three round-52 plan artefacts; `wc -l` of the two `.py`
- `find corpus/evidence/round52/graders -type f | wc -l` (185); `wc -l …/SHA256SUMS` (184)
- `grep` / `awk` / `sed -n` reads of `corpus/README.md` anchors, `corpus/SOURCES.md` ids, `plans/round-52-claims.md` A1–A5, `.ufo/waves/round-52/claims/*.txt`
- `df -h /fast` (538 G free at 34 % use)

## Files produced (absolute paths)

- `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeIndexRows/index-rows.md` — the draft (kept: the item names this path)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeIndexRows.md` — this report
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeIndexRows/report.md` — same content
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeIndexRows/receipts/` — `c1-now.txt`, `c2-now.txt`, `c1-selftest-now.txt`, `c2-selftest-now.txt`, `index-rows.md`

## Tooling

No tools installed or upgraded. The seat used `bash`, `python3` (already present), `sha256sum`, `wc`, `awk`, `grep`, `git` (read-only subcommands only). No pacman, no `uv`, no network fetch.

## Scratch

Removed everything in `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeIndexRows/` except `index-rows.md`, which the item names as the draft path; the copy in the report dir is the kept receipt.
