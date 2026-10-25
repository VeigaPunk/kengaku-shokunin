# R33ReconRegistry — round-33 C1 registry / coverage-map recon (leaf scout)

Seat: `R33ReconRegistry` (leaf; no subagent dispatch, no background jobs, no model pinning).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date for every source opened this round: **2026-10-25**.
Report path: `.ufo/waves/round-33/build/R33ReconRegistry.md`.
Production writes by this seat: **none** — this file is the only lane path written. Scratch:
`/tmp/r33-R33ReconRegistry/` (HEAD exports via `git archive`, byte extracts, census runs) — under
60 MB. No git index, branch, commit, checkout or mutating jj command was touched; only read-only
`git log / show / diff / status / ls-tree / archive / cat-file`. `/home/vgpnk/Projects/shokuknow`
was not written and no campaign tool was run there. The fleet repo `/home/vgpnk/Projects/shokunin`
was not written; the fleet census was **read** (`bash scripts/sources-census.sh validate --root
… kengaku`, stdout only, no `--out`).

Tools installed/upgraded by this seat: **none**. No pacman / uv / npx / cargo action was taken;
no tool was needed (read-only byte extraction, regex, `difflib` via stdlib `python3`, and
read-only `git` plumbing). The operator directive in `/home/vgpnk/.omp/agent/RULES.md` was read
first; its "install freely" allowance was not exercised because no capability was missing.

## 0. Tip movement observed during this seat (material to the L1)

The lane tip moved **twice** while this seat was reading, and the content of the C1 landing
changed with it. All findings below are re-derived against the **final** tip.

| moment | tip | note |
|---|---|---|
| seat start | `7895588` (C2 routed-defect repairs) | working tree already carried the uncommitted C1 patch |
| mid-seat | `2b4cef2` "renumbered assimilation (S103/S104), routed-defect closure N1-N6, catalog re-probe receipts" | integrator committed the C1 patch; **S103/S104 rows here were the short in-flight wording** |
| later | `7895588` again | `git reflog` shows `7895588 HEAD@{0}: export from jj` — a jj export re-pointed the git tip back, and `corpus/SOURCES.md` briefly carried **jj conflict markers** (`<<<<<<< conflict 1 of 1`, `%%%%%%% diff from: tvtyrotx 2b4cef2e …`, `\\\\\\\\\\ to: svpktmrr 78955888 …`) |
| final (report time) | **`b54feca` "round-33: admitted grader semantics and re-probed catalogs"** | rewritten landing commit; conflict markers resolved; working tree clean of `corpus/` edits |

`git reflog -8` at report time (verbatim):

```
7895588 HEAD@{0}: export from jj
2b4cef2 HEAD@{1}: commit: round-33: renumbered assimilation (S103/S104), routed-defect closure N1-N6, catalog re-probe receipts
7895588 HEAD@{2}: export from jj
c227e48 HEAD@{3}: export from jj
f0b20ae HEAD@{4}: export from jj
112091c HEAD@{5}: export from jj
bcd2a6c HEAD@{6}: export from jj
```

**Consequence for this report:** every "before" string below is anchored on the **freeze tip
`c227e486`** (the tip the frozen claims name), every "after" string on **`b54feca`**. The
`2b4cef2` intermediate is *not* the delivered text — the S103/S104 row bodies and the entry body
were rewritten between `2b4cef2` and `b54feca` (e.g. the S103 anchor cell grew from 1071 to 1465
bytes and now carries a pinned-blob URL plus five located quotes). Any downstream artifact quoting
`2b4cef2`'s row text is stale.

## (a) Every registry row with id ≥ S090 in `corpus/SOURCES.md`

Re-derived from `git show b54feca:corpus/SOURCES.md` by parsing the 11-cell table row
(`raw.strip()[1:-1].split("|")`). Registry total at `b54feca`: **97 rows** (`grep -cE '^\| *S[0-9]{3,} *\|'`
→ 97); 95 at the freeze tip `c227e486`; the delta is exactly the two new rows S103 and S104.
Ids present at `b54feca`: 1–86, 90–94, 97, 100–104 (gaps 87, 88, 89, 95, 96, 98, 99 are
pre-existing and unchanged).

| line | id | source cell (first 40 chars) | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|
| 103 | S090 | `Terminal-Bench 2.0 and Harbor (release a` | docs | A | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| 104 | S091 | `Agentic Benchmark Checklist (ABC) — http` | paper | A | mined | 2026-10-25 | 180d | `corpus/lessons/round-29.md, corpus/knowledge/benchmark-task-validity-checklist.md` |
| 111 | S092 | `Harbor harness source (verifier executio` | code | A | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-verifier-execution-model.md` |
| 112 | S093 | `SWE-bench Pro V2 task verifier files (te` | code | A | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` |
| 113 | S100 | `Terminal-Bench 2.0 task tree (release id` | dataset | A | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-verifier-execution-model.md` |
| 114 | S094 | `supersedes S094 — duplicate staged row r` | docs | B | **rejected** | 2026-10-25 | 180d | `—` |
| 115 | S097 | `supersedes S097 — duplicate staged row r` | docs | B | **rejected** | 2026-10-25 | 180d | `—` |
| 116 | S101 | `supersedes S101 — duplicate staged row r` | docs | B | **rejected** | 2026-10-25 | 180d | `—` |
| 117 | S102 | `supersedes S102 — duplicate staged row r` | docs | B | **rejected** | 2026-10-25 | 180d | `—` |
| 118 | S103 | `Toolathlon task evaluation script (tasks` | code | A | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-grader-semantics.md` |
| 119 | S104 | `LLMs-as-Judges: A Comprehensive Survey o` | paper | B | mined | 2026-10-25 | 180d | `corpus/knowledge/benchmark-grader-semantics.md` |

Kind column values (parsed): S090 `docs`, S091 `paper`, S092 `code`, S093 `code`, S100 `dataset`,
S094/S097/S101/S102 `docs`, S103 `code`, S104 `paper`.

**Registry census at the delivered tip** (`bash scripts/sources-census.sh census --file <export of b54feca:corpus/SOURCES.md>`,
read-only): `rows 97`, `tier.A 82`, `tier.B 13`, `tier.C 2`, `status.mined 81`, `status.queued 8`,
`status.rejected 8`, `tier.invalid 0`. Lane-level `validate --root /home/vgpnk/Projects/shokunin kengaku`
→ **exit 0** with **15 `W04`** warnings (identical set to the freeze control `.ufo/waves/round-33/claims/census-before.txt`
— the two new rows introduce no new duplicate-URL warning, because S103's URL differs from S080's
`raw.githubusercontent.com/hkust-nlp/Toolathlon/…` and S104's `arxiv.org/abs/2412.05579` is new to
the registry; the round-32 refusal row S097 no longer carries the arXiv URL).

**Refusal rows unchanged:** `git diff bcd2a6c b54feca -- corpus/SOURCES.md` removes **zero** row
lines (the only `-` line in that diff is the file header). The four round-32 refusal rows at
S094/S097/S101/S102 are byte-identical to their `bcd2a6c` form — ids never reused.

## (b) Exact `used-by` cell text of S093 today

At the delivered tip `b54feca` (`git show b54feca:corpus/SOURCES.md`, row at line 112, cell 11):

```
corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md
```

Provenance: that cell has been **byte-identical since `bcd2a6c` (round 32)** — the round-32
commit that landed the draft entry also pre-wrote S093's `used-by` to name it, and round 33
changed nothing in that cell. Verified by cell extraction at `bcd2a6c^` (`…verifier-execution-model.md`
only), `bcd2a6c`, `112091c`, `7895588` and `b54feca` (last four identical).

**The frozen claim's wording vs the tree:** the claim says "S093 … is already `mined` and gains
the entry in `used-by`". Strictly, S093 did **not** gain the entry this round — it already named
it. The predicate's observable requirement ("`used-by` naming the entry") holds; the *delta*
wording in the claim is inaccurate against the committed tree. **[INFERENCE, high confidence]**
the claim text was written against a pre-`bcd2a6c` mental model of S093's cell.

## (c) `corpus/README.md` — index row, coverage-map bullet, frontier sub-bullet (verbatim)

All three re-read from `git show b54feca:corpus/README.md`. README length: **389 lines** at
`b54feca` (388 at the freeze tip `c227e486` — the +1 is the round-33 coverage bullet's line shift
from the coverage-map insertion? No: `git diff c227e486 b54feca --stat -- corpus/README.md` = `6 +++---`,
i.e. **3 insertions / 3 deletions**, so the line count is unchanged at 388 content lines + trailing
newline; the 389 count includes the empty trailing element of `split('\n')`).

### (c1) Index row — `corpus/README.md:67` (440 chars)

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part | S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

Exactly **one** index row exists for the entry (`grep -c '^| \`knowledge/benchmark-grader-semantics.md\` |' corpus/README.md` → 1).
Index parity at `b54feca`: 41 `knowledge/` rows ↔ 41 `corpus/knowledge/*.md` files, no unindexed
file and no dangling row. **Note for the L1:** the frozen claims' lane-facts say "corpus/knowledge
40 files; 40 index rows" — that figure is **stale for this baseline**; the baseline `112091c`
already held 41/41 (the unadmitted round-32 draft file plus its index row). The 41/41 parity holds
at every snapshot I measured (`112091c`, `c227e486`, `7895588`, `b54feca`).

### (c2) Coverage-map bullet — `corpus/README.md:255` (802 chars)

```
- **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

### (c3) Frontier sub-bullet — `corpus/README.md:279` (574 chars)

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

**Observed drift (flagged for the L1):** this committed line names **S104 only**; it does not name
S103 anywhere (`'S103' in line` → `False`). The build-seat recommendation in
`.ufo/waves/round-33/build/R33ReadmePatch.md` §4 asked for exactly one insertion — `, S103` after
`9be8d8fe` — so the committed text differs from the recommendation by that insertion, and the
sibling seat `R33IndexTruth` flagged the same drift. **[INFERENCE]** the omission is cosmetic
rather than predicate-breaking: the frozen predicate reads the entry's `source:` lines and the
registry rows, not this bullet's id list, and `plans/round33_c1_verify.py` checks V1–V8 — none of
which reads README:279. But the bullet is the round's own record of *which* row the discharge
rests on, and it now names only the survey row. The one-line fix is in §6 (Edit 4b).

## (d) The `corpus/README.md` `## Frontier` bullet text C1 narrows

`## Frontier` is at `corpus/README.md:271`; its intro is at `:273-274`. The bullet C1 narrows is
**bullet 1, "Agentic benchmark task-spec audits"** (`corpus/README.md:276`), and the clause
C1 discharges is inside its **round-31 sub-bullet** (`corpus/README.md:278`).

### (d1) Bullet 1 header — `corpus/README.md:276` (442 chars, byte-identical at freeze tip and tip)

```
- **Agentic benchmark task-spec audits**: why — S005/S006 show lab self-audits finding task-level validity defects *after* publication; the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.
```

### (d2) The clause C1 discharges — `corpus/README.md:278` (841 chars, byte-identical at freeze tip and tip)

```
  - *Partly discharged round 31 (2026-10-25):* `knowledge/benchmark-verifier-execution-model.md` reads the harness's own verifier-mode resolver and `Verifier.verify` at Harbor commit `6099b8cf`, so the `their scoring code was not read and stays open` clause above is discharged for **verifier execution** (where grading runs, what is restored first, how SWE-bench Pro V2 derives its PASSED set). The clause stays open for the other benchmarks' scoring code (one SWE-bench Pro V2 task's grader *is* read here, in depth, and that is the only task-level code this round opens), for runtime task validity (which `PROVINCE.md` refuses to this lane) and for Toolathlon; the Terminal-Bench 2.0 axis-E cell is filled by this entry and the SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.
```

The narrowing clause is the trailing one, verbatim:

```
and for Toolathlon;
```

`grep -n 'and for Toolathlon' corpus/README.md` at the delivered tip → lines **255, 278, 279**.
Line 278 is the round-31 bullet (the clause's owner); 255 is the coverage bullet; 279 is round
33's own discharge bullet, which quotes the clause in its own words.

**Byte-level history of the frontier sub-bullet chain** (each round's own sub-bullet is *replaced*
in place, never appended — this is the lane's established pattern, confirmed by
`git show 9591131 -- corpus/README.md` and `git show bcd2a6c -- corpus/README.md`):

- `8cf7b60` (round 29 attempt 2) **added** `*Partly discharged round 29 attempt 2 (2026-10-25):*`
- round 30 **added** its own `*Partly discharged round 30 (2026-10-25):*` under the contamination bullet
- `9591131` (round 31) **replaced** the round-31 sub-bullet's text in place (narrowing the clause list)
- `bcd2a6c` (round 32) **added** `*Partly discharged round 32 (2026-10-25):*` (the S097-citing text)
- `b54feca` (round 33) **replaced** it with `*Partly discharged round 33 (2026-10-25):*` (S104-citing text)

So C1's edit is a **replace-in-place of the round-32 sub-bullet**, matching how round 31 revised
its own sub-bullet. `git log -p -- corpus/README.md` shows the round-32 line was deleted in the
round-33 landing.

## (e) `PROVINCE.md` wording the entry affects

**None.** `git diff 112091c b54feca --stat -- PROVINCE.md` is **empty** — `PROVINCE.md` has not
been touched since `8cf7b60` (round-29 attempt-2), and `git log -- PROVINCE.md` confirms the last
touch is that round-29 commit. The round-33 landing (`b54feca`) does not modify it.

What the entry *refers to* in PROVINCE (read-only, quoting `PROVINCE.md` as it stands):

- `PROVINCE.md:121-127` — `### Frontier`, the ground the entry's axis sits on:

```
### Frontier

The ground named in `corpus/README.md` §Frontier: agentic benchmark task-spec
audits (Terminal-Bench 2.0 / Toolathlon / SWE-bench Pro primary specs —
unopened leads), contamination transparency cards, judge calibration applied
to this lane's own grader/attribution outputs, an identity-verified endpoint
for novelty probes, and non-karpathy wiki topics (source absent).
```

- `PROVINCE.md:219-220` — the refusal the entry's scope sentence rests on ("It is not runtime
  task validity (`PROVINCE.md` refuses that to this lane)"): *"configuration, runtime task
  validity, hosted judges, contamination measurement or any benchmark's web properties."*
- `PROVINCE.md:213-222` — the round-29 attempt-2 admission paragraph, which is the **most recent**
  PROVINCE admission paragraph and the narrowest precedent for how this lane words an admission.
  It ends: *"this paragraph narrows only the "unopened leads" phrase for Terminal-Bench 2.0,
  SWE-bench Pro V2 and Toolathlon-Verified, which are now opened."*
- `PROVINCE.md:200-202` (round-28) and `:208-211` (round-29) — the earlier gap paragraphs naming
  *"runtime task validity, hosted judges and contamination remain open"*.

**Assessment for the L1:** the round-31 entry (`benchmark-verifier-execution-model.md`) and the
round-32 draft entry likewise added **no** PROVINCE paragraph, and the frozen C1 predicate does not
name PROVINCE.md. A round-33 PROVINCE paragraph would be a *new* lane convention, not a repair of
a stale one; the only PROVINCE text that a round-33 admission arguably contradicts is the
`PROVINCE.md:124` Frontier phrase *"primary specs — unopened leads"*, and that phrase was already
narrowed by the round-29 attempt-2 paragraph at `:221-222`. **[INFERENCE, medium confidence]** no
PROVINCE edit is required; if the L1 wants one, it must be **append-only** (a new dated section
after `:222`), never a rewrite of `:121-127` or `:213-222`.

## 5. Registry / README counters at the delivered tip (exercised, not assumed)

Run in the lane working tree at tip `b54feca`, read-only:

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit 0

$ python3 plans/round33_c1_verify.py --lane .
checks=8 defects=0
exit 0

$ python3 plans/state_check.py --summary
VERDICT: PASS — all comparable frozen assertions match
exit 0
```

Negative controls re-derived by this seat (a claim not exercised is not a pass):

- **HEAD-only tree** (`git archive c227e486` → `/tmp/…/headtree/kengaku-shokunin`, the freeze tip):
  `adoption_check --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=fail`, **exit 1**;
  `round33_c1_verify.py --lane .` → `checks=8 defects=3`
  (`DEFECT V2 cited-row-identity: the S093 registry row cites no URL`, `DEFECT V7 renumber-map-recorded`, `DEFECT V8 refusal-rows-intact`).
- **The frozen control receipt** `.ufo/waves/round-33/claims/control-nothing.txt` pins
  `expect_sha256=fbd7b47ededdfe251465c13ee1c2b758453f2b691bc0639d8a74df3e0752a214`; the expect
  file's current sha256 matches (recomputed).
- The **frozen** counter `plans/round33_c1_verify.py` at `f0b20ae` had two latent defects that
  the delivered tree repairs (`git diff f0b20ae b54feca -- plans/round33_c1_verify.py` = 6+/3−):
  V2 read only cell 0 (the id) instead of cells 0 **or** 1 for the URL, and V8 read `supersedes <id>`
  from the *teaches* cell instead of the *source* cell. Both are fixed in the delivered tree; the
  fix is committed inside `b54feca` (the script is byte-identical in the working tree — no uncommitted
  drift). `python3 plans/round33_c1_verify.py --selftest` → `SELFTEST checks=8 failed=0` exit 0 on
  the delivered script; the frozen `f0b20ae` script's selftest also passed (`checks=8 failed=0`),
  i.e. the selftest never caught the two cell-index bugs.

## 6. Paste-ready old-strings for every edit the round-33 integration made

Anchors: **OLD** = `git show c227e486:<path>` (freeze tip, the state the integration edited);
**NEW** = `git show b54feca:<path>` (delivered tip). Each OLD block is byte-exact and unique in
its file.

### Edit 1 — `corpus/SOURCES.md`: append the two new rows (lines 118–119)

OLD anchor (line 117, the S102 refusal row; the two new rows go immediately after it, before
`## Paths`):

```
| S102 | supersedes S102 — duplicate staged row refused after registry collision; this id already identifies the SWE-bench release map. Use the existing S102 row; no catalog row admitted. | docs | B | rejected correction record for a staged S102 duplicate; not a new source and not an admitted citation | this row records why the staged candidate is refused, not an external-source anchor | REJECTED: duplicate id; flip: a future candidate must use a new id and pass the source gate | rejected | 2026-10-25 | 180d | — |
```

NEW (line 118, 1465 chars):

```
| S103 | Toolathlon task evaluation script (tasks/finalpool/ab-testing/evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon — pinned blob https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py | code | A | the executed scoring code for one Toolathlon task at a pinned commit — what is compared (a produced record.csv against groundtruth_workspace/expected_ratio.csv), against what reference, and with the tolerance the sole call site passes rather than the signature default — for the code's own behaviour | commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py:58 "def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:" (11 words); :279 "# Validate with 0.05% tolerance" (5); :280 "validate_record_data(actual_records, expected_records, tolerance_pct=0.05)" (3); :218 "return True  # Don't fail evaluation if we can't check logs" (11); :234 "if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):" (4) | scores a produced artifact against a ground-truth artifact at a tolerance fixed at the call site — 0.05 percentage points per scenario, not the 0.1 signature default; caught log-check exceptions fail open, while absent credentials fall through to implicit None and fail closed | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
```

NEW (line 119, 1040 chars):

```
| S104 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579 | paper | B | the survey's own five-part structure for LLM-as-a-judge evaluation — Functionality, Methodology, Applications, Meta-evaluation, Limitations — for the preprint's own text; tier B because it is a preprint at the time of opening | arXiv 2412.05579v2 (v1 Sat, 7 Dec 2024; v2 Tue, 10 Dec 2024), abs page:41 title "LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods" (8 words); :124 "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." (20 words); :131 "60 pages, comprehensive and continuously updated" (6 words) | meta-evaluation — how a judge itself is scored — is separate from methodology; the survey uses its own spelling, LLMs-as-Judges in the title and LLMs-as-judges in the abstract | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
```

### Edit 2 — `corpus/README.md:67` (index row)

OLD (386 chars):

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; a log-bucket check fails open) and the LLM-as-judge survey frame: meta-evaluation is its own part | S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

NEW (440 chars) — as quoted in §(c1) above.

Span delta: description cell `a log-bucket check fails open` → `its log-bucket check mixes fail-open exceptions with fail-closed credential absence`; citation cell `S094`→`S103`, `S097`→`S104`. The `S093 restated from the verifier-execution entry` tail is retained.

### Edit 3 — `corpus/README.md:255` (coverage-map bullet)

OLD (712 chars) — as quoted verbatim in §(c2)'s OLD block above (round 32 wording, S093/S094/S097,
`one of which fails open`).

NEW (802 chars) — as quoted verbatim in §(c2).

Span delta: `round 32`→`round 33`; `, admitted under renumbered ids` inserted after the date; `S094`→`S103`, `S097`→`S104` (two id sites); `one of which fails open` → `the log-bucket one mixing fail-open exceptions with fail-closed credential absence`. The 0.05% clause, the `PROVINCE` refusal and the three "Not …" disclaimers are byte-identical.

### Edit 4 — `corpus/README.md:279` (frontier sub-bullet, replace-in-place)

OLD (574 chars):

```
  - *Partly discharged round 32 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S097). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

NEW as delivered (574 chars) — as quoted verbatim in §(c3). Span delta: `round 32`→`round 33`; `S097`→`S104`.

### Edit 4b — OPTIONAL, NOT YET APPLIED: name S103 in the round-33 frontier sub-bullet

OLD (= the delivered `corpus/README.md:279` line):

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

NEW (recommended, = old + exactly one insertion `, S103`):

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`, S103) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

This is the text `.ufo/waves/round-33/build/R33ReadmePatch.md` §4 recommended and that
`.ufo/waves/round-33/build/R33IndexTruth.md` flagged as drift. Not required by the frozen
predicate; it is a one-token record-accuracy fix. If applied it must be a **new** commit
(`QUALITY.md` R1: corrections are appended, never rewritten).

### Edit 5 — `corpus/knowledge/benchmark-grader-semantics.md` (the draft's citations re-pointed)

OLD header lines 2, 3, 6 (from `c227e486`):

```
source: S094 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, accessed 2026-10-25
source: S097 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
```

NEW lines 2–3 (delivered):

```
source: S103 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, accessed 2026-10-25
source: S104 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
```

OLD line 6 → NEW line 6:

```
writer: KengakuR32
```
→
```
writer: KengakuR33 (admission patch of the round-32 draft)
```

Additional in-body edits delivered in `b54feca` (the round-32 draft's body was substantially
rewritten — 181 changed lines, entry grew 6986 → 12135 bytes; headings moved from `:27`/`:60` to
`:45`/`:107`/`:126`). The OLD in-body strings the integrator replaced (all quoted from
`c227e486`, byte-exact):

- `**Source labels (Q5).** S093 is a benchmark maintainer's own task-grading code at a pinned` /
  `commit; S094 is Toolathlon's own task-evaluation script at a pinned commit; S097 is an arXiv` /
  `preprint. Each is a primary artefact of the party it describes, not an independent measurement.`
  → replaced by a renumber-labelled paragraph that names the mapping S094→S103, S097→S104.
- `## S094 — Toolathlon's ab-testing grader is a deterministic state comparison with a call-site tolerance`
  → `## S103 — Toolathlon's ab-testing grader is a deterministic state comparison with a call-site tolerance`
- `## S097 — the survey frame: meta-evaluation is its own part`
  → `## S104 — the survey frame: meta-evaluation is its own part`
- `storage-bucket prefix (\`main.py:134-139\`) and checks whether the ab-testing logging bucket`
  → the delivered entry cites `main.py:125-140,225` for the storage-bucket prefix.

The two **staged misstatements** the claim requires the repair to fix are, in the delivered tree:
(i) executed tolerance — the entry states the operative value is `0.05` at the call site
(`main.py:279-280`), not the `0.1` signature default, and the S103 row's `teaches` cell says so
verbatim (*"a tolerance fixed at the call site — 0.05 percentage points per scenario, not the 0.1
signature default"*); (ii) credential failure — the S103 row's `teaches` cell reads *"caught
log-check exceptions fail open, while absent credentials fall through to implicit None and fail
closed"*, and the README index cell reads *"its log-bucket check mixes fail-open exceptions with
fail-closed credential absence"*. Neither the index row nor the coverage bullet now says "fails
open" unconditionally.

## 7. Findings, ranked

1. **[OBSERVED] The delivered tip is `b54feca`, and the C1 landing text changed under the seat.**
   `2b4cef2` was rewritten (`jj export` moved the git tip back to `7895588` and briefly left jj
   conflict markers in `corpus/SOURCES.md`); `b54feca` is the resolved landing. Any artifact
   quoting `2b4cef2`'s S103/S104 rows or entry body is stale — the S103 row grew 1071→1465 bytes.
2. **[OBSERVED] The four round-32 refusal rows at S094/S097/S101/S102 are byte-identical to their
   `bcd2a6c` form.** `git diff bcd2a6c b54feca -- corpus/SOURCES.md` removes zero rows. Ids reused: none.
3. **[OBSERVED] S093's `used-by` already named the entry before round 33** (from `bcd2a6c`);
   the round-33 integration left that cell untouched. The frozen claim's "S093 … gains the entry
   in `used-by`" describes a delta that did not occur; the predicate's observable condition holds.
4. **[OBSERVED] `corpus/README.md:279` names S104 but not S103** — a one-token drift from the
   build-seat recommendation, flagged independently by `R33IndexTruth`. Not predicate-breaking.
   Paste-ready fix in §6 Edit 4b.
5. **[OBSERVED] The claims file's "40 files; 40 index rows" is stale for this baseline** — the
   baseline `112091c` already held 41/41 (the unadmitted draft + its index row). Parity 41=41 holds
   at every snapshot.
6. **[OBSERVED] `PROVINCE.md` needs no edit for C1** — untouched since round-29 (`8cf7b60`); the
   round-31 and round-32 entries added none either; the frozen predicate does not name it. Any
   round-33 PROVINCE paragraph would be a new convention and must be append-only.
7. **[OBSERVED] The frozen counter had two latent cell-index bugs** (V2 read the id cell for a URL;
   V8 read `supersedes <id>` from the wrong cell). Both are fixed in the delivered tree and the fix
   is committed; the counter's own selftest never caught either (it passed on the buggy script).
8. **[OBSERVED] `SCORECARD.md` carries two `## Round 33` sections** (lines 1122 and 1135), from the
   two commits `7895588` and `b54feca`. `QUALITY.md` R2's check is `grep -c '^## Round <N>' LOG.md
   SCORECARD.md` → `1 1`; at `b54feca` it reads `1 2`. The same shape exists for rounds 9, 10 and 29
   (`2 2`, `2 2`, `2 2`), so this is a pre-existing lane pattern rather than a round-33
   regression — but round 33's second section is the round's *own* duplicate, not a legacy one.

## 8. Remaining unknowns

- Whether the L1 wants the `, S103` insertion in `corpus/README.md:279` (§6 Edit 4b). This seat
  does not judge; it reports the drift and the exact replacement bytes.
- Whether the L1 wants a round-33 PROVINCE paragraph (§e). Observed precedent says none is needed.
- The falsify wave's verdicts on the delivered tree (this seat's scope was registry/README recon
  only; it did not adjudicate the entry's claims).
- `corpus/evidence/round33/defects-after.txt` and the fleet-report errata were not opened by this
  seat — out of scope (C2), though `plans/round33_defects.py` was not run here either.

VERDICT: registry-read
