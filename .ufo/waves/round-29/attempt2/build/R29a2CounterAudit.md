# R29a2CounterAudit — can `plans/adoption_check.py` counters disagree?

Seat: `L1Kengaku29.R29a2CounterAudit` (leaf). Date: 2026-10-25. Lane: `kengaku-shokunin`.
Scope: adversarial fixture probe of `plans/adoption_check.py`. Findings only — no production edit was made;
all fixtures live under `/tmp/r29a2-CounterAudit/`. No tool was installed or upgraded. No subagent was dispatched.

## 0. Pinned revisions (the file moved under me mid-run)

| label | bytes | sha256 | provenance |
|---|---|---|---|
| **R_old** | 4262 | `6f7656fea11f0ceda8533eef42ee51de5044aa6c5e971194fdff310bca6e28a1` | `git show 8c14a5d:plans/adoption_check.py` (committed baseline) |
| **R_new** | 4312 | `704b6544a334117e529428d5f93c5360fcb26c3dc37ca80f83b86706fbd84d56` | working tree, mtime `2026-10-25T06:46:10Z`, `git status` = `M plans/adoption_check.py` |

Sole difference (`git diff -U3`): R_new adds `lane_name = lane.name[: -len("-shokunin")] if lane.name.endswith("-shokunin") else lane.name`
at line 94 and passes it to the census subprocess instead of `lane.name`. Every non-census counter is byte-identical in
behaviour: the full fixture matrix below was run on both revisions and diffed — **identical** (`diff results-all.txt results-all-newrev.txt` → no output).

Live lane snapshots (the round was being edited by sibling seats while I measured):

| UTC | entry sha256 | SOURCES sha256 | README sha256 | counter (no `--census`) |
|---|---|---|---|---|
| 06:45:49Z | `a4c8f7ed…110be1` | `d81683f2…b32c6a` | `7c4d4da2…64c3171` | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` exit 1 |
| 06:46:04Z | `80fd49f6…c03b45` | `ffb73d5a…c3c08c` | `119c99b6…5e9386` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` exit 0 |

## 1. Method

Fixtures are copies of the lane's corpus layout (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/…`) plus the
**frozen** expectation file `.ufo/waves/round-29/attempt2/adoption-expect.json` (copied verbatim; one entry, five sources
S077/S078/S079/S080/S090, `access_date` 2026-10-25). Five registry rows were appended for those ids with `status=mined` and
`used-by` naming the citing entry, and one `| \`knowledge/benchmark-task-validity-checklist.md\` |` README index row.

Each defect fixture is the **green base** with exactly one field changed, so a moved counter is attributable to that field.
Two fixture families:

- **minimal** — `/tmp/r29a2-CounterAudit/{base,a_*,…,m_*}`: lane tables + the single entry (census not exercisable there).
- **census-probeable** — `/tmp/r29a2-CounterAudit/croot/`: a fleet root (`shokunin.conf`) with a **full** corpus copy
  (`corpus/knowledge/`, `corpus/lessons/`) so census E11 has no missing `used-by` paths, and rows inserted **inside**
  `## Registry`.

Commands (revision-independent unless flagged):

```
PY=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/adoption_check.py
python3 $PY --lane <fixture> --expect <fixture>/expect.json          # minimal matrix
cd /tmp/r29a2-CounterAudit/croot && python3 $PY --lane <v> --expect <v>/expect.json --census
```

## 2. Green control

`base` → `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` **exit 0**.
With `--census` from cwd `croot`: `… census=ok` **exit 0**. The fixtures are therefore capable of reaching the frozen
target line, which is the precondition for calling any non-movement below a finding.

## 3. The four assigned defects

Green base: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1`

| # | defect | printed line | field that moved | exit |
|---|---|---|---|---|
| (a) | entry file absent | `entries=0 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=0 census=skipped` | `entries` 1→0, `cited_rows` 5→0, `verified_at` 1→0 (`indexed`, `usedby_ok` unchanged) | **1** |
| (b) | entry present, **not indexed** in README | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` | `indexed` 1→0 only | **1** |
| (c) | cited row `status=queued` (S079) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped` | `rows_mined` 5→4 only | **1** |
| (d) | cited row's `used-by` missing the entry (S090) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` | **none** | **0** |

### (a) Entry absent — moves, but two conjuncts become vacuous
`present` counts non-empty text (`plans/adoption_check.py:73-75`), so an absent file also empties `cited`; `rows_present`
and `rows_mined` fall to 0 (`:81-82`) and their assertions `rows_present == len(cited)` / `rows_mined == len(cited)`
(`:112-113`) are satisfied by `0 == 0`. The exit-1 comes from `entries`, `verified_at` and `usedby_ok`… actually
`usedby_ok` stays 1 because `:83-90` walks `entry["sources"]`, not the entry bytes. The failure is caught, but not by
the row counters.

### (b) Not indexed — clean single-field move
Isolated: only `indexed` moved. This is the counter working as advertised.

### (c) `queued` — clean single-field move
Only `rows_mined` moved (`:82` reads `registry[row_id][7]`, the status column — confirmed against
`corpus/SOURCES.md:21` header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`,
index 7 = `status`). The fleet census is **blind** to this defect: `v_queued` census output contains only `W04`, no `E07`
(E07 checks the enum, and `queued` is a legal value) — verified in §5.

### (d) `used-by` missing the entry — **no counter moves, exits 0** ← finding
Cause, `plans/adoption_check.py:83-90`:

```python
usedby_ok = 0
for entry in entries:
    rel = entry["path"]
    for row_id in entry["sources"]:
        cells = registry.get(row_id)
        if cells and rel in cells[10]:
            usedby_ok += 1
            break
```

`usedby_ok` is **per entry, not per row**, and `break`s on the first hit. With S077–S080 still naming the entry, S090's
missing `used-by` is never examined. The frozen target prints `usedby_ok=1` for five cited rows, so at most one row is
ever checked. The census is also blind here: `v_usedby_wrong_existing` (S090 pointing at another entry that exists on disk)
→ census `ok`, counter exit 0.

## 4. Further disagreement probes (beyond the assigned four)

All rows below are the green base with one change, minimal family, no `--census`.

| # | probe | printed line | exit |
|---|---|---|---|
| (e) | entry cites all five ids on **one** `source:` line (the corpus's own convention) | `entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 verified_at=1` | **0** |
| (f) | entry with **no** `source:` line | `entries=1 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=1` | **0** |
| (g) | 4 of 5 rows' `used-by` wrong, 1 correct | `… cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 …` | **0** |
| (h) | `used-by` names `…-checklist.md.bak` (suffix only) | `… usedby_ok=1 …` | **0** |
| (i) | entry file contains a single space | `entries=1 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=0` | **1** |
| (j) | `verified-at: 2026-10-24` (stale) | `… verified_at=0 …` | **1** |
| (k) | entry cites `S091`, which has no registry row | `… cited_rows=5 rows_present=4 rows_mined=4 …` | **1** |
| (l) | **all five** rows' `used-by` wrong | `… usedby_ok=0 …` | **1** |
| (m) | S080's line replaced by a **duplicate** `S077` cite | `… cited_rows=4 rows_present=4 rows_mined=4 …` | **0** |

**(e) is a false green with consequences.** `SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)`
(`:34`) is line-anchored with a single `findall` group, so it returns only the **first** id per line. Verified directly:
`R.findall("source: S077 — a; S078 — b; S079 — c; S080 — d; S090 — e")` → `['S077']`.
This is not a corner case: 10 of the 38 `corpus/knowledge/*.md` entries cite more than one id on one `source:` line
(e.g. `attribution-interval-calibration.md` 9 ids, `extraction-policy-comparison.md` 10, `webarena-task-spec-audit.md` 7),
and **only the new round-29 entry uses one `source:` line per id** (`benchmark-task-validity-checklist.md`: 5 lines / 5 ids;
every other entry has exactly 1 `source:` line). So the frozen `cited_rows=5` is reachable only by a citation shape no
other corpus entry uses, and a corpus-conventional entry scores `cited_rows=1` while the counter exits 0 — four cited
rows, including their `status` and `used-by`, are never checked.

**(m) shows `cited_rows` is not bound to the expectation.** The expectation declares `"sources": [S077,S078,S079,S080,S090]`,
but that list is only consumed by the `usedby_ok` loop (`:83-90`). The citation set is compared solely to
`len(cited)` (`:112-113`), so dropping or duplicating a citation keeps every assertion true.

**(i)** shows `present` is truthiness, not content: a one-space entry counts as present (`:74-75`) and the exit-1 comes from
`verified_at`, not from the entry being empty.

## 5. Counters that cannot be made to disagree

| counter | can it be made to disagree? | why |
|---|---|---|
| `entries` | yes, but weakly | whitespace-only file counts as present (i) |
| `indexed` | yes, cleanly (b) | exact substring `\| \`knowledge/<name>.md\` \|` |
| `cited_rows` | **only downward, and never against the frozen list** | first-id-per-line regex (e); duplicates/subset stay green (m); empty set green (f) |
| `rows_present` | **not per row** | aggregate vs `len(cited)`; vacuously 0==0 (a, f); cannot see an uncited row |
| `rows_mined` | yes (c), but **not per row** | same aggregate form; a duplicate/unseen cite hides a queued row |
| `usedby_ok` | **not per row** — only all-or-nothing | per-entry with `break` (d, g); substring match accepts `…md.bak` (h); 0 only when *every* row misses (l) |
| `verified_at` | yes (j), undocumented | printed at `:107`, checked at `:115`, **absent from the docstring's "Counters printed" list** (`:15-22`) |
| `census` | **not by corpus bytes at all** | see below |

### The census counter is not a corpus-byte counter

It is a subprocess side-channel whose state is decided by **lane resolution and cwd**, plus census rules that are blind to
the two defects C1 cares about (`status`, `used-by` targeting). Measured facts:

1. **R_old cannot reach `census=ok` from the documented invocation.** The claims' target command is
   `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`, i.e. cwd = lane
   root. On the landed tree at 06:46:04Z, R_old printed
   `entries=1 indexed=1 … census=fail` **exit 1**, while the same bytes with cwd = fleet root printed `census=ok`.
   Mechanism: R_old passed `lane.name` (`kengaku-shokunin`); `scripts/sources-census.sh:518` matches the **roster** lane
   name (`kengaku`, from `rel%-shokunin` at `:480`), and the fallback `elif [ -d "$arg" ]` at `:521` is cwd-relative — so
   the arg resolved only when cwd was the fleet root. R_new's suffix strip (`:94`) fixes this: R_new prints
   `census=ok` exit 0 from lane root, fleet root, **and** `/tmp` with an absolute `--lane` (all three verified).
2. **A fixture lane is still cwd-dependent.** Same R_new, same tree: `croot`, cwd `/tmp` → `census=fail` exit 1;
   cwd `croot` → `census=ok` exit 0. Only cwd changed. So on any tree where the lane name is not in the fleet roster, the
   census counter is a cwd probe, not a content probe.
3. **Census is blind to both row-level defects.** `census validate --root … ` on `v_queued` and on
   `v_usedby_wrong_existing` reports only the 14 pre-existing `W04` warnings — no `E07`, no `E11`. E07 tests the status
   enum (`queued|mined|rejected`), E11 tests only that the `used-by` path *exists on disk*
   (`scripts/sources-census.sh:657-659,567`). Neither can see `queued` or a wrong-but-existing `used-by`.
4. **`census=ok` requires rows inside `## Registry`.** My first census-probeable fixtures appended rows at end of file and
   got 5×`E12 row outside Registry section` + `census=fail`, with every other counter green. This is a live trap for the
   row append: in the real `corpus/SOURCES.md` the Registry table runs from `## Registry` (line 19) to `## Paths`
   (line 106); the round-29 rows landed at lines 100–104 — **correctly inside**, which is why the live census has no E12
   for S077–S090 (verified: census output has no line matching `S077|S078|S079|S080|S090|task-validity`).
5. **Census needs a full corpus.** A minimal copy yields ~90 spurious `E11 missing used-by` rows because the copied
   registry names files absent from the copy; census can only be exercised on a full-corpus clone (§1 `croot`).

## 6. Consequence for the frozen C1 target

The target line

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

is produced **by R_new only**, and R_new is **uncommitted** (`M plans/adoption_check.py`). If the round commits corpus
bytes without this edit, the documented command from the lane root prints `census=fail` and exits 1 on a fully correct
lane — a false negative against a landed round. Conversely, the counter's exit 0 is **not** evidence that the frozen
expectation holds: fixtures (d), (e), (f), (g), (h), (m) all exit 0 with real defects present. The do-nothing control
(`control.nothing.txt`, exit 1) and a landed round (exit 0) do differ, so the round is not inert — but the green line is
weaker than it reads.

Advisory only (production edits are outside this seat's authority):

1. `usedby_ok`: count **per (entry, source) pair** — drop the `break`, require every id in `entry["sources"]` to be named,
   and compare the cell's parsed path list for equality rather than `rel in cells[10]`. Acceptance: fixture (d) and (g)
   must exit 1, (h) must exit 1, (l) stays 1.
2. `cited_rows`: match **all** ids on a `source:` line (`findall` over the whole line, or `re.findall(r"\bS[0-9]{3,}\b", line)`)
   and assert `cited == set(entry["sources"])`. Acceptance: (e) prints `cited_rows=5`, (f) and (m) exit 1.
3. Vacuous conjunctions: require `len(cited) == sum(len(e["sources"]) for e in entries)` before comparing `rows_*`, so an
   empty or partial citation set cannot satisfy them.
4. Census: keep R_new's suffix strip **and** pass `cwd=lane.parent` to `subprocess.run`, so the counter's verdict does not
   depend on the operator's cwd. Acceptance: the same tree yields the same `census=` from lane root, fleet root and `/tmp`.
5. Docstring: add `verified_at` to the "Counters printed" list (`:15-22`), or drop it from the printed line and the `ok`
   conjunction (`:107,115`).
6. State the invocation contract in the claims/README next to the target line: cwd, `--lane`, and that `census=ok`
   requires the fleet roster (`shokunin.conf`) to be reachable from `lane.parent`.

## 7. Evidence

Artifacts (scratch, outside the lane): `/tmp/r29a2-CounterAudit/`
`results-all.txt`, `results-all-newrev.txt`, `results-census.txt`, `results-croot.txt`, `live-census.out`,
`adoption_check.committed.py` (R_old), and the fixture trees `base/`, `a_*`…`m_*`, `croot/`.

Key commands and observed output:

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census   # R_new
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
exit=0
$ python3 /tmp/r29a2-CounterAudit/adoption_check.committed.py --expect .ufo/…/adoption-expect.json --census  # R_old
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=fail
exit=1
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin \
    | grep -oE '\b[EW][0-9]{2}\b' | sort | uniq -c
     14 W04          # no E-codes: S077–S090 land inside ## Registry
$ cd /tmp && python3 …/plans/adoption_check.py --lane /tmp/r29a2-CounterAudit/croot/base --expect … --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=fail   exit=1
$ cd /tmp/r29a2-CounterAudit/croot && python3 …/plans/adoption_check.py --lane base --expect base/expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok     exit=0
```

## 8. Blockers / risks

- None blocking. The counter file was edited by a sibling seat during measurement (R_old → R_new at 06:46:10Z); both
  revisions were measured and the non-census matrix is identical across them, so no conclusion depends on the race.
- Risk to the round: R_new is uncommitted; the frozen target is unreachable without it (finding 6.1). The L1 should
  confirm `plans/adoption_check.py` is part of the commit that closes C2, together with `plans/sources_adopt.py`.
- Risk to any future fixture work: census verdicts are only meaningful from cwd = the fleet root (or a fixture root whose
  lane name the roster resolves); report the cwd with every `census=` number.
