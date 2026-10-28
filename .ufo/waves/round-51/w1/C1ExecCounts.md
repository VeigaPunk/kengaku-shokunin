# C1ExecCounts — round 51 (hyaku run 11), seat executor

**Item:** re-derive every numeric claim the `PROVINCE.md` surface tables make, each with its
command. Feeds the C1 `NUMBER-DRIFT` repair. Read-only against the lane; no production file
touched.

## Axes named

- **Primary axis: freshness (8 → 9).** A surface row that states a number is a freshness claim;
  a stale numeral makes the row assert something false about today.
- **Secondary axis: operability.** Each claim is scored only if a command re-derives it, so the
  report names the exact command for every number.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

(Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`, `git status --porcelain`
shows only untracked `.ufo/waves/**`; no tracked file dirty. Stage-1 freeze is `e07f131`, the tip
is `4090c3d`, one commit later, and `corpus/SOURCES.md`, `PROVINCE.md` and `grader.py` are
unchanged between the two: `git diff --stat e07f131..4090c3d` touches exactly three files, all
wave scaffolding — `.ufo/waves/round-51/build_spec.py` (+151), `w1-dispatch.json` (+1003),
`w1-spec.json` (+589).)

All gate/instrument runs were made in a `git clone --shared` at
`/fast/scratch/hyaku/kengaku-r51/C1ExecCounts/lane` (top-level verified with
`git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r51/C1ExecCounts/lane`, HEAD
`4090c3db79d11279ab5e5121ba25e74aa316e6e7`), so no lane file was written by `grader.py`.

## Claim → command → observed → verdict

### 1. "25 rows" — `PROVINCE.md:112` (`### Core`, Public-literature registry)

Row text at `PROVINCE.md:112`:

```
| Public-literature registry | `test -e corpus/SOURCES.md` | present; 25 rows, contract-v1 census clean (`corpus/evidence/round24-census/after.txt`); receipts `corpus/evidence/round24-sources/gate.md` |
```

Command (the one the claims file and `plans/round24_census.sh:41` both use):

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```

Observed:

```
170
```

Independent re-derivation (same file, three ways):

```sh
grep -oE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md | wc -l   # 170
grep -cE '^[|]' corpus/SOURCES.md                                              # 172
python3 -c "import re,pathlib; t=pathlib.Path('corpus/SOURCES.md').read_text(); print(len(re.findall(r'^\|[ \t]*S[0-9]{3,}[ \t]*\|', t, flags=re.M)))"   # 170
```

Registry shape at this revision: 170 matches, 170 unique ids, **0 duplicates**, ids `S001`–`S177`,
not contiguous (7 ids absent inside the range); 224 lines total, 172 of them table rows (the two
non-`S` table rows are header/separator). No match occurs inside a fenced block (0 lines).

**Verdict: DISAGREES — 25 vs 170.** The `25` is the round-24 census value. `PROVINCE.md:119`
(round-25 correction, "holds 37") and `PROVINCE.md:175-190` (round-26 corrections R26-E3/E9/E10,
`rows=42`, `id_set=exact`) already supersede the cell as dated frozen populations; the live count
at `4090c3d` is **170**.

Counter confirmation at this revision (`python3 plans/round51_surfaces.py --lane .`, exit 1):

```
PROBES run=19 present=13 absent=6 errors=0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
```

The full counter output at `4090c3d` is **byte-identical to
`.ufo/waves/round-51/claims/c1-before.txt` after normalising only the `REV` line** (`diff` of the
two normalised files → no output, `IDENTICAL`). Nothing in the lane has drifted since the before
receipt; the `NUMBER-DRIFT 1` is still exactly SF14.

### 2. "733 checks" — `PROVINCE.md:19` (`## Surfaces`, In-repo gate)

Row text at `PROVINCE.md:19` asserts `python3 grader.py` → exit 0/1/2 and **733 checks** after the
round-14 analysis-byte pin.

Command (lane-root clone, no arguments):

```sh
python3 grader.py
```

Observed (verbatim tail, captured to a file so `$?` is grader's own):

```
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
GRADER_EXIT=0
```

Supporting numerics in the same row, same file:

| Row sub-claim | Command | Observed |
|---|---|---|
| "four probe trees (r8/r9/r11/r12)" | `grep -oE '"(r8|r9|r11|r12)_(jsonl|md|runlog)"' grader.py \| cut -d_ -f1 \| tr -d '"' \| sort -u` | `r11 r12 r8 r9` (4 trees) |
| "three r12 md5 pins" | `grep -cE '^ +"r12_[a-z]+": \("md5"' grader.py` | `3` (lines 1536-1538: `r12_jsonl`, `r12_runlog`, `r12_md`) |
| "`90c87c88…ae941f`" digest | `sha256sum grader.py` | `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f` |

**Verdict: AGREES — 733, 4 trees, 3 r12 md5 pins, digest pin all exact at `4090c3d`.**

### 3. "28 root receipt logs indexed in `corpus/README.md`" — `PROVINCE.md:109` (`### Core`, Own probe artifacts)

The index is the table under `corpus/README.md:182` ("Root-level receipt logs"), closed by the
`Round-24 additions` heading at `:216`.

Command:

```sh
awk '/^Root-level receipt logs/,/^Round-24 additions/' corpus/README.md \
  | grep -cE '^\| `(probe-r19|attrib-r2)[^`]*\.log`'
```

Observed:

```
28
```

Every indexed name resolves (command below prints one line per index row, then counts):

```sh
awk '/^Root-level receipt logs/,/^Round-24 additions/' corpus/README.md \
  | grep -oE '`(probe-r19|attrib-r2)[^`]*\.log`' | tr -d '`' \
  | while read f; do [ -f "corpus/evidence/$f" ] && echo OK || echo "MISSING $f"; done \
  | sort | uniq -c
```

```
     28 OK
```

Cross-check of the same block by a looser pattern (any `` `*.log` `` row between the two headings)
also returns **28**, so the count does not depend on the name prefixes.

**Verdict: AGREES on the count — 28 indexed, 28 resolve.** One prose caveat for the landing edit:
the files are **not** in the corpus root (`ls corpus/*.log` → 0 files); all 28 live at
`corpus/evidence/<name>.log`. "Root-level" in the README means root level of the `evidence/`
section. The row's number is right; its locator word is ambiguous.

### 4. "the twelve evidence dirs the Core row loops over" — `PROVINCE.md:109`

Command (the row's own loop, verbatim, run from the lane root):

```sh
for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing; do test -d corpus/evidence/$d || echo missing $d; done
```

Observed: **no output** (loop exit 0).

Count of names in the loop:

```sh
echo "round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing" | wc -w
```

```
12
```

Scope check of the enclosing directory:

```sh
ls -d corpus/evidence/*/ | wc -l
```

```
41
```

**Verdict: AGREES — twelve dirs named, twelve present, loop prints nothing.** The number is a
**subset**: `corpus/evidence/` holds 41 directories, so "all present" is true of the twelve named
and says nothing about the other 29 (not a defect of this row, but the reader should not read it
as an all-evidence census).

### 5. "S0–S7" — `PROVINCE.md:19` (`--selftest` claim)

Command:

```sh
python3 grader.py --selftest
```

Observed (verbatim, labels extracted):

```
[selftest] PASS S0 control (clean copies): exit 0, expected 0
[selftest] PASS S1 stored-ok flip (record layer): ...
[selftest] PASS S2 run.log SUMMARY edit (summary layer): ...
[selftest] PASS S3 raw-digit bump (re-parse layer): ...
[selftest] PASS S4 r11 stored-ok flip (record layer): ...
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): ...
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] PASS S7 r12 stats anchors (Page L / grade_seq / Brier-BSS / Newton): all known-value assertions hold
[selftest] ALL PASS
SELFTEST_EXIT=0
```

`grep -c '^\[selftest\] PASS'` → `8`; distinct labels → `S0 S1 S2 S3 S4 S5 S6 S7`.

**Verdict: AGREES — the printed selftest labels are exactly S0–S7 (8 cases), all PASS, exit 0.**
Note for the record: `grader.py` also contains `S0b/S0c/S0d/S0e` and `S0e` labels inside the
round-12 fixture-battery helper (lines ~5321-5368), which is **not** reached by `--selftest` and
prints nothing in the run above. The row's "S0–S7" is a statement about the `--selftest` output and
is correct as such; a reader who greps the source for `S0`-prefixed labels would over-count.

## Adjacent numerics in the same two tables (cheap, re-run; not in my named list)

| Row / cell | Command | Observed | Agrees? |
|---|---|---|---|
| `### Core`, interval re-verdict instrument: "4 unique samples, 92/92 correct, transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1" | `python3 plans/attrib_calibration.py --summary` (exit 0) | `unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 … transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0` | **agrees** (4 / 92 / 92 / 2 / 1 all present verbatim) |
| `### Core`, state-assertion check: "exit 0 / exit 0 on the landed tree (base `6180e4f`: exit 1, 10 mismatches)" | `python3 plans/state_check.py --summary` (exit 0) | `VERDICT: PASS — all comparable frozen assertions match`; the instrument's own supersession record carries `"receipt": ["10", "0"]` against `SCORECARD.md:757` | landed-tree half **agrees** (exit 0); the `6180e4f` half is **historical, not re-derived** here (would need the old tree + old instrument; out of this item) |
| `## Surfaces` gate row: "round-14 mutation test killed 4/4 fresh corruptions" | — | historical round-14 record; no command in the lane re-runs it | **not re-derived** (historical) |
| `## Surfaces` served-model row: "41 tokens, EXACT_MATCH", "`n_ctx=16384`", "7,226 lines" | — | endpoint/path absent (SF03 `absent`, SF04 `absent`); `/proc/1299/cmdline` and the telemetry file cannot be read at this revision | **not re-derived** (targets absent; the row already carries `ABSENT` markers) |

## What this means for the C1 `NUMBER-DRIFT` repair

1. **The only numeral the counter binds today is SF14's, and it must become 170.** `NUMBER-DRIFT 0`
   requires `count_claim == probed count`, and the probe reads the live file
   (`{"kind":"count","target":"corpus/SOURCES.md","pattern":"^\\|\\s*S[0-9]{3,}\\s*\\|"}` → 170 at
   `4090c3d`). Setting `count_claim: 170` clears `NUMBER-DRIFT` without touching any other key.
2. **Counter gap (freshness truth, worth an attack row):** the counter compares `count_claim` to the
   probe only — it never parses the numeral out of the row. A manifest with `count_claim: 170`
   passes `NUMBER-DRIFT 0` even if `PROVINCE.md:112` still reads "25 rows". So `NUMBER-DRIFT 0` is
   **not** evidence that the row's own number is true; the row edit and the manifest edit are two
   independent obligations and only the manifest half is machine-checked.
3. **Append-only wording constraint:** `PROVINCE.md:190` (R26-E9/E10) pins `rows=42` `id_set=exact`
   as a **frozen round-25 population** ("count `SOURCES.md` ids ≤42, not future additions"), and
   `plans/state_check.py` carries that as a live supersession (`claim ["25"]` → correction tokens
   `rows=42`). A landing correction must therefore date a **new** live count (170 at 2026-10-28)
   rather than rewrite 42 or 25; 42 is a frozen-population fact and stays true.
4. **The other four numerics in my item are inside rows whose manifest probe cannot see them.**
   `733`, `28`, `12` and `S0–S7` sit in `PROVINCE.md:19` and `:109`, covered by
   `paths: grader.py` (SF08), `sha256: grader.py` (SF10) and a 7-path subset probe (SF11). The
   counter has no probe kind that runs a subprocess, so `733 checks` is not machine-checkable with
   the frozen kinds at all; `28` and `S0–S7` would need a `count` probe over a file (the README
   table / a captured selftest receipt). All four re-derive correctly **by hand today**, so they are
   true-but-unchecked, not false.
5. **SF11's twelve dirs are covered by two entries, not one.** SF07 probes
   `round8-horizon, round9-replication, round12-ladder, round14-fleet, round13-coverage` and SF11
   probes the remaining seven; union = exactly the loop's twelve, no overlap, no gap. The loop
   command itself is never executed by the counter — it is emulated by path probes. That is sound
   for `test -d`, and worth stating in the landing note so a reviewer does not go looking for the
   missing execution.

## Limits

- Point-in-time: every count is at `4090c3d`. `SOURCES.md` grows by design, so 170 is a snapshot,
  not a constant; the counter's live-file probe means the landing must measure 170 again at the
  landing tip before pinning `count_claim`.
- `grader.py` and both instruments were executed only inside the scratch clone. I did not run them
  against the lane working tree (the lane is read-only for me); the clone is `--shared` off the same
  commit and its `rev-parse HEAD` was verified equal.
- The two historical cells (`4/4` mutation, `41 tokens` / `7,226 lines` / `6180e4f: 10 mismatches`)
  are declared **not re-derived**, not "wrong": no command in this item re-runs them and two of
  their targets are absent at this revision.
- I did not audit `prose` readings or the C2 ledger; that is other seats' items.

## Commands run (exhaustive list, lane-root unless noted)

```
git rev-parse HEAD ; git status --porcelain ; git log --oneline -3 ; git cat-file -t e07f131…
grep -n '^## Surfaces\|^### Core\|^##' PROVINCE.md
grep -n 'for d in round8-horizon' PROVINCE.md
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
grep -oE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md | wc -l
grep -cE '^[|]' corpus/SOURCES.md ; wc -l corpus/SOURCES.md
python3 -c '…re.findall S-row census, id set, duplicates…' corpus/SOURCES.md
sha256sum grader.py
awk '/^Root-level receipt logs/,/^Round-24 additions/' corpus/README.md | grep -cE '^\| `(probe-r19|attrib-r2)[^`]*\.log`'
awk '…same block…' corpus/README.md | grep -oE '`(probe-r19|attrib-r2)[^`]*\.log`' | … [ -f corpus/evidence/$f ] … | sort | uniq -c
for d in round8-horizon … round18-kimi-routing; do test -d corpus/evidence/$d || echo missing $d; done
ls -d corpus/evidence/*/ | wc -l
grep -oE '"(r8|r9|r11|r12)_(jsonl|md|runlog)"' grader.py | cut -d_ -f1 | tr -d '"' | sort -u
grep -cE '^ +"r12_[a-z]+": \("md5"' grader.py
grep -n 'SOURCES' plans/round24_census.sh
grep -n 'holds 37\|25 rows' PROVINCE.md
# scratch clone: /fast/scratch/hyaku/kengaku-r51/C1ExecCounts/lane (rev-parse --show-toplevel verified)
python3 grader.py                    # CHECKS n=733 … exit 0
python3 grader.py --selftest         # 8× PASS S0–S7, ALL PASS, exit 0
python3 plans/round51_surfaces.py --lane .      # PREDICATE R51-C1 fail, exit 1
python3 plans/attrib_calibration.py --summary   # exit 0
python3 plans/state_check.py --summary          # exit 0
diff <(sed 's/^REV .*/REV X/' claims/c1-before.txt) <(sed 's/^REV .*/REV X/' tip c1 output)   # IDENTICAL
```

## Scratch

`/fast/scratch/hyaku/kengaku-r51/C1ExecCounts` (the clone plus captured outputs) is **removed**
before yield; nothing citable was left there — every number in this report is a command a reader
can re-run from the lane root or a clone, and the outputs are quoted above verbatim.

VERDICT: PASS — of the five named numerics, four re-derive exactly at `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (733 checks + exit 0; 28 indexed receipt logs, all 28 resolving; 12 evidence dirs present; selftest labels exactly S0–S7) and one **disagrees**: `PROVINCE.md:112` says "25 rows" while `corpus/SOURCES.md` holds **170** S-rows (unique, S001–S177, 0 duplicates) — the `NUMBER-DRIFT 1` the frozen counter still reports, byte-identical to `c1-before.txt` apart from the `REV` line; the repair is `count_claim: 170` **plus** a dated append-only row correction, and `NUMBER-DRIFT 0` alone will not prove the row's numeral because the counter never parses the row.
