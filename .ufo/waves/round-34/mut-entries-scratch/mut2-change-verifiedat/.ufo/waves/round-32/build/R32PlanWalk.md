# R32 Plan Walk — pre-wave data-walk

Seat: L1Kengaku32.R32PlanWalk (leaf scout). Access date for every source opened this round:
2026-10-25. Installs: none (no tool added or updated).

Frozen claims file read first: `plans/round-32-claims.md` (freeze commit `0d32691d`, HEAD at
walk time `6084cd34`).

---

## (a) Registry row count; S093/S094/S097 presence

Command (cwd = lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

```
$ grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md
91
```

**Exact registry row count = 91** (matches claims line 4 "Registry 91 rows").

Presence command:

```
$ grep -nE '^\| *S(093|094|097) *\|' corpus/SOURCES.md
112:| S093 | SWE-bench Pro V2 task verifier files (tests/test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os | code | A | the executed grading code for one SWE-bench Pro V2 task at a pinned commit — the test-space reset it performs itself, the paths that reset skips, and the log-scan parser behind its PASSED set | commit 66f92766bba642462d4bbe5479e83f91f9211862, v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh:33 "Resetting test-space to base state (full test-code surface)..." (8 words); :71 `T) git checkout HEAD -- "$path"`; :214 "success = all_required <= passed_tests" (5 words) | the task restores its own test-code surface from the contai…
```

- `S093` **present** at line 112; full row read raw: `status=mined`, `opened=2026-10-25`,
  `recheck=180d`, `used-by=corpus/knowledge/benchmark-verifier-execution-model.md`.
- `S094` and `S097` **absent**: no line matches under the same anchor (grep exit 1 when only
  S093's line is matched, no S094/S097 lines exist). No other S094/S097 occurrences anywhere in
  the file (searched via `grep -n 'S094'` / `grep -n 'S097'` — the only hits are this row's
  absence; zero matches).
- Registry ends at `S100` (last row line 113); `S101`/`S102` absent (exit 1) — C3's rows are
  not yet open, as expected pre-wave.

## (b) README frontier bullet-1 (lines 274–276) and coverage-map row

Exact text, `corpus/README.md` lines 274–276 (raw read):

> Line 274: `- **Agentic benchmark task-spec audits**: why — S005/S006 show lab self-audits finding task-level validity defects *after* publication; the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.`
>
> Line 275: `  - *Partly discharged round 29 attempt 2 (2026-10-25):* `knowledge/benchmark-task-validity-checklist.md` builds the per-benchmark task-validity checklist from the primary maintainer artefacts of Terminal-Bench 2.0, SWE-bench Pro V2 and Toolathlon-Verified. It supersedes the `primary specs` half of the `unopened leads` phrase for those three sources — their scoring code was not read and stays open; contamination-transparency cards, runtime task validity and hosted judges remain open.`
>
> Line 276: `  - *Partly discharged round 31 (2026-10-25):* `knowledge/benchmark-verifier-execution-model.md` reads the harness's own verifier-mode resolver and `Verifier.verify` at Harbor commit `6099b8cf`, so the `their scoring code was not read and stays open` clause above is discharged for **verifier execution** (where grading runs, what is restored first, how SWE-bench Pro V2 derives its PASSED set). The clause stays open for the other benchmarks' scoring code (one SWE-bench Pro V2 task's grader *is* read here, in depth, and that is the only task-level code this round opens), for runtime task validity (which `PROVINCE.md` refuses to this lane) and for Toolathlon; the Terminal-Bench 2.0 axis-E cell is filled by this entry and the SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.`

**Coverage-map row that will need the sub-bullet**: `corpus/README.md:253` — the **"Benchmark
verifier execution model"** coverage row:

> `- **Benchmark verifier execution model**: covered at source-code depth (round 31, 2026-10-25) — knowledge/benchmark-verifier-execution-model.md; S092, S093, S100. Discharges the round-29 frontier clause "their scoring code was not read and stays open" for verifier execution only: ...`

C1's grader-semantics entry "extends the round-31 verifier-execution entry rather than repeating
it" (claims §C1), i.e. it extends this same row (which is the only coverage-map row citing S093),
so line 253 is the row that gains the new sub-bullet / source-list entry (S094, S097) when the
entry lands.

## (c) S094/S097 collision check under the 0-3-space anchor

Command and output (cwd = lane root):

```
$ grep -nE '^\| {0,3}S(094|097) *\|' corpus/SOURCES.md
(no output)
$ echo $?
1
```

No registry row matches `S094` or `S097` even allowing 0–3 spaces after the leading pipe — **no
collision under the 0-3-space anchor**. Cross-check with the star anchor used in (a) (spaces
0+), narrowing to an id boundary so `S097` cannot false-match inside a longer id:

```
$ grep -nE '^\| *S(094|097)[^0-9]' corpus/SOURCES.md
(no output)
$ echo $?
1
```

Independent confirmation: wave artifact `.ufo/waves/round-32/assimilation/reg-ids` lists the 91
registered ids (S001–S086, S090–S093, S100); it contains neither S094 nor S097, and S100 is the
maximum registered id. `collisions` (15 ids: S077–S086, S090–S093, S100) likewise contains
neither.

## (d) Census line

As written in the assignment, from the lane root:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
bash: scripts/sources-census.sh: No such file or directory
$ echo $?
127
```

The lane has **no `scripts/` directory** (`test -d scripts` → exit 1). The tool is fleet-canonical
at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (this path hazard was already
recorded in round-25 finding F6, `ConnSoujiKaidoku.md`). Canonical run:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
$ echo $?
0
```

Tail: 15 `W04` warnings (S040, S048, S057, S058, S059, S064, S065, S066, S067, S068, S069,
S071, S075, S076, S100), then `kengaku	ok	…/corpus/SOURCES.md`, **exit 0**. Matches claims
line 4 "census exit 0 with 15 W04".

## (e) Frozen claims vs observed

Consistent with `plans/round-32-claims.md`:

| Claim fact | Observed |
|---|---|
| Registry 91 rows | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` = **91** ✓ |
| `corpus/knowledge/` 40 files | `find corpus/knowledge -maxdepth 1 -type f \| wc -l` = **40** ✓ |
| 40 index rows | `grep -cE '^\| `knowledge/' corpus/README.md` = **40** ✓ |
| Census exit 0 with 15 W04 | canonical run above: 15 W04, `ok`, exit 0 ✓ |
| S093 already held (mined, opened 2026-10-25, used-by will gain entry) | S093 row: `mined`, `opened=2026-10-25`, `used-by=corpus/knowledge/benchmark-verifier-execution-model.md` ✓ |
| S094/S097 new rows this round | absent from registry ✓ |
| C1 control: `adoption-expect.json` (entry `benchmark-grader-semantics.md`, sources S093/S094/S097); `control-nothing.txt` prints `entries=0 …` exits 1 | both files exist at `.ufo/waves/round-32/claims/`; adoption-expect.json content matches predicate; control-nothing.txt: `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, `exit=1` ✓ |
| C2 control: `defects-before.txt` | exists; `checks=7 defects=7`, `exit=1`, R1–R7 lines match the freeze predicate ✓ |
| C3 control: `catalogs-before.txt` | exists; `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale`, `exit=1` ✓ |
| C3 surface: README index row "probed 2026-09-28" | `corpus/README.md:40`: `… probed 2026-09-28` ✓ |
| Counter scripts | `plans/adoption_check.py`, `plans/catalog_probe.py`, `plans/round32_defects.py`, `plans/round32_c1_verify.py` all present ✓ |
| Entry not yet admitted | `corpus/knowledge/benchmark-grader-semantics.md` absent in lane (staged only under read-only `shokuknow/merge/kengaku/`) ✓ |

Observations / deltas (not predicate violations):

1. **Baseline tip moved after freeze.** Claims: "Baseline: lane branch tip
   `f20a1097af900dc4595e0da0fa5e12e673f9ce7e` (local = remote, ahead=0)". Observed: `HEAD` =
   `6084cd3492c6aef10fd66afc36ffc00e79ace94a` (detached, "round-32: freeze-commit gate receipt
   (Q20 out-of-band)"); `f20a1097` exists locally and is an ancestor (`git merge-base
   --is-ancestor f20a1097… HEAD` → exit 0). Two post-baseline round-32 commits: `0d32691`
   ("frozen claims, counters, freeze controls") and `6084cd3`. `local = remote / ahead=0` could
   not be re-checked offline (no remote fetch); the local HEAD advancing past the frozen baseline
   is the expected freeze progression, not a claim change. Working tree also has one untracked
   wave artifact: `.ufo/waves/round-32/assimilation/`.
2. **Census path hazard (documented).** The as-written `scripts/sources-census.sh` command fails
   from the lane root (no lane `scripts/`); the canonical fleet path works and is what all prior
   round receipts use (round-25 F6 already recorded this).

---

## VERDICT: consistent
