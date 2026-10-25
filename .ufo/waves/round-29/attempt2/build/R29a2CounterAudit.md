# R29a2CounterAudit — can `plans/adoption_check.py` counters disagree?

Seat: `L1Kengaku29.R29a2CounterAudit` (leaf). Date: 2026-10-25. Lane: `kengaku-shokunin`.
Scope: adversarial fixture probe of `plans/adoption_check.py`. Findings only — no production edit was made; all
fixtures under `/tmp/r29a2-CounterAudit/`. No tool installed or upgraded. No subagent dispatched.

**The counter was edited twice while I measured it.** Every number below names its revision; a conclusion that depends on
the revision says so.

## 0. Revisions

| label | bytes | sha256 | provenance |
|---|---|---|---|
| **R1** | 4262 | `6f7656fea11f0ceda8533eef42ee51de5044aa6c5e971194fdff310bca6e28a1` | `git show 8c14a5d:plans/adoption_check.py` — the **committed** baseline |
| **R2** | 4312 | `704b6544a334117e529428d5f93c5360fcb26c3dc37ca80f83b86706fbd84d56` | worktree at 06:46:10Z; adds only the census `-shokunin` suffix strip |
| **R3** | 4549 | `ee34914c847879fc4354fc965ec82294c9b0c6985da7fe466db784543a9fab25` | worktree at 06:47:54Z; **current**, `git status` = `M plans/adoption_check.py` |

R3's `git diff -U2` against `8c14a5d`, beyond R2's suffix strip: `required = sum(len(entry["sources"]))`, the assertions
`len(cited) == required` / `rows_present == required` / `rows_mined == required` (`:116-118`), `usedby_ok` rewritten from
per-entry-with-`break` to all-of (`:86-92`), `verified_at` dropped from the printed line (`:109-111`) while remaining a gate
(`:120`), and `registry_rows` using `raw.strip()` instead of `raw.rstrip()`.

Live-lane snapshots (sibling seats were writing the corpus throughout):

| UTC | entry sha256 | SOURCES sha256 | README sha256 | counter |
|---|---|---|---|---|
| 06:45:49Z | `a4c8f7ed…110be1` | `d81683f2…b32c6a` | `7c4d4da2…64c3171` | R2: `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` exit 1 |
| 06:46:04Z | `80fd49f6…c03b45` | `ffb73d5a…c3c08c` | `119c99b6…5e9386` | R2: `entries=1 indexed=1 … census=skipped` exit 0; **with `--census` from lane root: `census=fail` exit 1** |
| 06:48Z | same corpus | same corpus | same corpus | R3: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` **exit 0** (lane root, `--census`) |

## 1. Method

Fixtures are copies of the lane's corpus layout (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/…`) plus the
**frozen** `.ufo/waves/round-29/attempt2/adoption-expect.json` (copied verbatim: one entry,
`corpus/knowledge/benchmark-task-validity-checklist.md`, five sources S077/S078/S079/S080/S090, `access_date` 2026-10-25).
Five registry rows were appended with `status=mined` and `used-by` naming the citing entry, and one
`` | `knowledge/benchmark-task-validity-checklist.md` | `` README index row.

Every defect fixture is the **green base** with exactly one field changed, so a moved counter is attributable to that field.
The README used in fixtures is the live README **with every line naming the entry removed**, plus the single fixture index
row — otherwise defect (b) is unreproducible once the real README indexes the entry (measured: a first rebuild left the
live index row in place and (b) falsely passed).

Two families: **minimal** (`/tmp/r29a2-CounterAudit/rebuild/{base,a_*,…,o_*}`) and **census-probeable**
(`/tmp/r29a2-CounterAudit/croot/`: a fleet root with `shokunin.conf` + a **full** corpus copy, rows inserted inside
`## Registry`).

Reproduce: `python3 /tmp/r29a2-CounterAudit/rebuild.py <dir>` (validated — it regenerates the matrix below), then

```
PY=<lane>/plans/adoption_check.py
python3 $PY --lane <fixture> --expect <fixture>/expect.json            # minimal matrix
cd /tmp/r29a2-CounterAudit/croot && python3 $PY --lane <v> --expect <v>/expect.json --census
```

## 2. Green control (both revisions)

`base` → R1 `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` exit 0;
R3 `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped` exit 0. With `--census` from
cwd `croot`, both print `census=ok` exit 0. The fixtures can reach the target line, so a non-movement below is a finding.

## 3. The four assigned defects

Base: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1` (+`verified_at=1` under R1).

| # | defect | R1 printed line | R3 printed line | field moved | R1 exit | R3 exit |
|---|---|---|---|---|---|---|
| (a) | entry file absent | `entries=0 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=0 census=skipped` | `entries=0 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 census=skipped` | `entries` 1→0, `cited_rows` 5→0 (R1 also `verified_at` 1→0) | **1** | **1** |
| (b) | entry present, not indexed in README | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped` | `indexed` 1→0 only | **1** | **1** |
| (c) | cited row `status=queued` (S079) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=4 usedby_ok=1 census=skipped` | `rows_mined` 5→4 only | **1** | **1** |
| (d) | cited row's `used-by` missing the entry (S090) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=0 census=skipped` | **R1: none. R3: `usedby_ok` 1→0** | **0** | **1** |

### (a) Entry absent — caught, but two conjuncts go vacuous (both revisions)
`present` counts non-empty text (`R1 :73-74`, `R3 :74-75`), so an absent entry also empties `cited`; `rows_present` and
`rows_mined` fall to 0 and, under R1, satisfied `rows_present == len(cited)` / `rows_mined == len(cited)` by `0 == 0`
(`R1 :112-113`). R1's exit 1 came from `entries`, `verified_at` and (not) the row counters. R3 closes this with
`required = sum(len(entry["sources"]))` (`R3 :82`) compared at `:116-118`, so the empty citation set now fails on its own.

### (b) Not indexed — clean single-field move (both revisions)
Only `indexed` moved. The check is an exact substring: `` f"| `knowledge/{name}` |" in readme `` (`R3 :76-77`). Brittleness in §5.

### (c) `queued` — clean single-field move (both revisions)
Only `rows_mined` moved; it reads `registry[row_id][7]`, the status column, matching the header
`corpus/SOURCES.md:21` (`… | status | opened | recheck | used-by |`, index 7). The fleet census is blind to this defect: my
`v_queued` fixture's census output carries only the 14 pre-existing `W04` warnings — no `E07` (E07 tests the enum, and
`queued` is legal).

### (d) `used-by` missing the entry — R1 green, R3 red
R1 (`:83-90`) counted `usedby_ok` **per entry** and `break`ed on the first row naming the entry, so with S077–S080 correct,
S090's missing `used-by` was never examined: **no counter moved, exit 0** on a five-row entry with one unlinked row. That is
the assigned defect passing the gate. R3 replaces it with all-of over `entry["sources"]` (`:86-92`) → `usedby_ok=0`, exit 1.
The residual hole is the match itself: `rel in registry[row_id][10]` is a **substring** test (see (h)).

## 4. Further disagreement probes

Same green base, one change each; no `--census`.

| # | probe | R1 | R3 | verdict |
|---|---|---|---|---|
| (e) | all five ids on **one** `source:` line (the lane's dominant convention) | `cited_rows=1 rows_present=1 rows_mined=1` **exit 0** | `cited_rows=1 rows_present=1 rows_mined=1` **exit 1** | R1 false green, R3 false **red** |
| (f) | no `source:` line at all | `cited_rows=0 rows_present=0 rows_mined=0` **exit 0** | `…=0` **exit 1** | fixed in R3 |
| (g) | 4 of 5 rows' `used-by` wrong, 1 correct | `usedby_ok=1` **exit 0** | `usedby_ok=0` **exit 1** | fixed in R3 |
| (h) | `used-by` names `…-checklist.md.bak` | `usedby_ok=1` **exit 0** | `usedby_ok=1` **exit 0** | **still a false green** |
| (i) | entry file contains a single space | `entries=1` `verified_at=0` exit 1 | `entries=1 cited_rows=0` exit 1 | caught (R1 on `verified_at`, R3 on `required`) |
| (j) | `verified-at: 2026-10-24` | `verified_at=0` exit 1 | exit 1, **field not printed** | still a gate; now invisible in the line |
| (k) | cites `S091`, no registry row | `rows_present=4 rows_mined=4` exit 1 | same, exit 1 | caught |
| (l) | all five `used-by` wrong | `usedby_ok=0` exit 1 | `usedby_ok=0` exit 1 | caught |
| (m) | S080's line replaced by a duplicate `S077` cite | `cited_rows=4 rows_present=4 rows_mined=4` **exit 0** | `…=4` **exit 1** | fixed in R3 |
| (n) | five expected ids **plus** an extra `source: S001` line | n/a | `cited_rows=6 rows_present=6 rows_mined=6` **exit 1** | R3 strictness: `sources` is an exact set |
| (o) | README index cell written without the space before `\|` | n/a | `indexed=0` **exit 1** | R3 false red on formatting |

**(e) is the sharpest result.** `SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)` (`:34`) is
line-anchored with one capture group, so it returns only the **first** id per line. Verified directly:
`R.findall("source: S077 — a; S078 — b; S079 — c; S080 — d; S090 — e")` → `['S077']`. This is not a corner case: 10 of the
38 `corpus/knowledge/*.md` entries put more than one id on one `source:` line (`attribution-interval-calibration.md` 9,
`extraction-policy-comparison.md` 10, `webarena-task-spec-audit.md` 7, …), and **only the new round-29 entry uses one
`source:` line per id** (5 lines / 5 ids; every other entry has exactly one `source:` line). R1 therefore accepted a
corpus-conventional entry while silently skipping four cited rows' `status` and `used-by`; R3 now **rejects** that same
conventional entry (`len(cited)=1 != required=5`). Both are wrong in opposite directions; the round's entry passes R3 only
because it was written in a shape no other entry uses.

## 5. Counters that cannot be made to disagree (current R3)

| counter | status | why |
|---|---|---|
| `entries` | moves (a, i), but `present` is truthiness | a one-space file counts as present (`R3 :74-75`) |
| `indexed` | moves (b), **whitespace-bound, not section-bound** | exact substring `\| \`knowledge/x.md\` \|` (`:76-77`): (o) a table cell written `\`knowledge/x.md\`\|` reads 0; conversely any occurrence of that exact cell anywhere in README reads 1, with no binding to the index table |
| `cited_rows` | moves (e, m) **only because R3 compares to `required`** | the value itself is still first-id-per-line (`:34`): a conventional entry reports `cited_rows=1` for five citations |
| `rows_present` | moves (k); **cannot see an uncited row** | aggregate over `cited`; with `len(cited) == required` (`:116`) an empty/partial set now also fails, but there is no per-row binding |
| `rows_mined` | moves (c); same aggregate shape | a citation the regex cannot see is a row whose `status` is never checked (e) |
| `usedby_ok` | moves (d, g, l); **substring, so not exact** | `rel in registry[row_id][10]` (`:90`) accepts `…-checklist.md.bak` (h) and would accept any superset string; it is per entry, not per row, so its values are 0/1 only |
| `verified_at` | moves (j) but **is no longer printed** | gated at `:120`, absent from the line (`:109-111`); an operator reading the line cannot tell it was checked — the docstring at `:15-22` also does not list it |
| `census` | **not a corpus-byte counter** | see the census subsection below |

### The census counter is a cwd/roster probe

1. **R1/R2 could not reach `census=ok` from the documented invocation.** The claims' target command is
   `python3 plans/adoption_check.py --expect … --census` (cwd = lane root). At 06:46:04Z R2 printed `census=fail` **exit 1**
   from lane root and `census=ok` from fleet root, on identical bytes. Mechanism: R1/R2 passed `lane.name`
   (`kengaku-shokunin`); `scripts/sources-census.sh:518` matches the **roster** name (`kengaku`, from `rel%-shokunin` at
   `:480`), and the fallback `elif [ -d "$arg" ]` (`:521`) is cwd-relative, so the arg resolved only when cwd was the fleet
   root. R3's strip (`:97`) fixes the real lane: R3 prints `census=ok` exit 0 from lane root, from fleet root, and from
   `/tmp` with an absolute `--lane` (all three measured).
2. **A fixture / non-roster lane is still cwd-dependent.** R3, identical tree: cwd `croot` → `census=ok` exit 0; cwd `/tmp`
   → `census=fail` exit 1. Only cwd changed.
3. **Census is blind to both row-level defects.** `v_queued` and `v_usedby_wrong_existing` produce no `E07`/`E11`, only
   `W04`. E07 tests the status enum (`queued|mined|rejected`); E11 tests only that the `used-by` path exists on disk
   (`scripts/sources-census.sh:657-659,567`).
4. **`census=ok` requires rows inside `## Registry`.** My first census-probeable fixtures appended rows at end of file →
   5×`E12 row outside Registry section` and `census=fail` while every other counter was green. In the live
   `corpus/SOURCES.md` the table runs from `## Registry` (line 19) to `## Paths` (line 106); the round-29 rows landed at
   100–104 — **inside**, which is why the live census shows no E12 for S077–S090 (census output has no line matching
   `S077|S078|S079|S080|S090|task-validity`). Without `--census` the counter cannot see placement at all: fixture
   `croot/v_outside_registry` (all five rows appended after `## Leads`) prints the **full target line, exit 0**, and only
   `--census` turns it red (`census=fail` exit 1). `registry_rows` parses every `| S### |` row in the file, wherever it sits
   (`R3 :40-49`), so section membership is enforced by the census alone.
5. **Census needs a full corpus.** A minimal copy yields ~90 spurious `E11 missing used-by` rows for pre-existing rows whose
   targets are absent from the copy.

## 6. Consequence for the frozen C1 target

Frozen target line: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0.

- The **committed** baseline could never print it: R1 printed an eighth field (`verified_at=1`) and never `census=ok` from
  lane root. Two independent reasons.
- **R3 prints it, exit 0, from the documented invocation** (measured 06:48Z on the live tree). R3 is **uncommitted**.
  If the round commits corpus bytes without `plans/adoption_check.py`, the frozen target regresses to `census=fail`, exit 1,
  on a fully correct lane — a false negative against a landed round.
- Even under R3, exit 0 is not proof the frozen expectation holds: (h) exits 0 with a wrong `used-by`, and (e)/(o) show the
  converse (exit 1 on correct bytes). The counter's polarity is wrong in both directions on real edge shapes.

Advisory only (production edits are outside this seat's authority):

1. Citation extraction: take **all** ids on every `source:` line (`\bS[0-9]{3,}\b` over the line), keeping R3's
   `len(cited) == required`. This fixes (e) without reopening (f)/(m).
2. `usedby_ok`: compare the parsed path list of the `used-by` cell for **equality** (or at least a component-wise match),
   not `rel in cell`, and count per (entry, source) pair. Acceptance: (h) must exit 1, (d)/(g) stay 1.
3. `indexed`: tolerate optional spaces around the cell (`` re.search(r"\| *`knowledge/name` *\|", readme) ``) and bind the
   match to the index table. Acceptance: (o) must exit 0, (b) must stay 1.
4. Census: keep R3's suffix strip **and** pass `cwd=lane.parent` to `subprocess.run`, so the verdict is cwd-independent.
   Acceptance: the `croot` tree yields the same `census=` from `croot`, `/tmp`, and the fleet root.
5. Keep `verified_at` gated, and state in the diff/claims that it is a silent gate so nobody reads the seven printed fields as
   the whole assertion set.
6. Record the invocation contract next to the target line in the claims: cwd, `--lane`, and that `census=ok` needs the fleet
   roster reachable from `lane.parent`.

## 7. Evidence

Artifacts (scratch; the report body is the durable locus):
`/tmp/r29a2-CounterAudit/` — `rebuild.py` (validated fixture builder), `rebuild/` (fixtures used for the per-revision table),
`results-by-revision.txt` (R1 vs R3, identical fixtures), `results-all.txt` (R1, original fixtures),
`results-census.txt`, `results-croot.txt`, `live-census.out`, `adoption_check.committed.py` (R1).

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census   # R3
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok        exit=0
$ python3 /tmp/r29a2-CounterAudit/adoption_check.committed.py --expect .ufo/waves/…/adoption-expect.json --census   # R1
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=fail   exit=1
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin \
    | grep -oE '\b[EW][0-9]{2}\b' | sort | uniq -c
     14 W04        # no E-codes: S077–S090 sit inside ## Registry
$ cd /tmp && python3 …/plans/adoption_check.py --lane /tmp/r29a2-CounterAudit/croot/base --expect … --census
… census=fail   exit=1
$ cd /tmp/r29a2-CounterAudit/croot && python3 …/plans/adoption_check.py --lane base --expect base/expect.json --census
… census=ok     exit=0
```

## 8. Blockers / risks

- No blocker. The counter moved twice during the audit (R1 → R2 06:46:10Z, R2 → R3 06:47:54Z); R1 and R3 were both measured
  on the **same rebuilt fixtures**, so the per-revision table is comparable, and every claim above names its revision.
- Risk to the round: R3 is uncommitted. The frozen target is unreachable at the committed baseline for two independent
  reasons (§6), so the commit that closes C2 must include `plans/adoption_check.py` (with `plans/sources_adopt.py`).
- Risk to future fixture work: any `census=` number is meaningless without its cwd; and fixture READMEs must strip the live
  entry's index row or defect (b) is unreproducible.
