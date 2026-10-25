# R29a2CounterAudit — can `plans/adoption_check.py` counters disagree?

Seat: `L1Kengaku29.R29a2CounterAudit` (leaf). Date: 2026-10-25. Lane: `kengaku-shokunin`.
Scope: adversarial fixture probe of `plans/adoption_check.py`. Findings only — no production edit was made; all fixtures
under `/tmp/r29a2-CounterAudit/`. No tool installed or upgraded. No subagent dispatched.

**The counter was rewritten three times while I measured it (R1 → R2 → R3 → R4).** Every number names its revision.
R1 (committed) and R4 (current) were both measured on the **same rebuilt fixtures**, so their columns are comparable.

## 0. Revisions

| label | bytes | sha256 | provenance |
|---|---|---|---|
| **R1** | 4262 | `6f7656fea11f0ceda8533eef42ee51de5044aa6c5e971194fdff310bca6e28a1` | `git show 8c14a5d:plans/adoption_check.py` — the **committed** baseline |
| **R2** | 4312 | `704b6544a334117e529428d5f93c5360fcb26c3dc37ca80f83b86706fbd84d56` | worktree 06:46:10Z — adds only the census `-shokunin` suffix strip |
| **R3** | 4549 | `ee34914c847879fc4354fc965ec82294c9b0c6985da7fe466db784543a9fab25` | worktree 06:47:54Z — `required`, all-of `usedby_ok`, `verified_at` unprinted |
| **R4** | 4875 | `949c367d79aaff26deffbea66fead2982fabe13e527c01076aa2193dd5032414` | worktree 06:50:37Z; **current**, `git status` = `M plans/adoption_check.py` |

Deltas beyond R2's suffix strip, from `git diff` against `8c14a5d`:

- **R3**: `required = sum(len(entry["sources"]))`; assertions `len(cited) == required`, `rows_present == required`,
  `rows_mined == required`; `usedby_ok` rewritten from per-entry-with-`break` to all-of; `verified_at` dropped from the
  printed line while staying a gate; `registry_rows` uses `raw.strip()`.
- **R4** on top: `indexed` and `verified_at` become **anchored regexes** (`^| \`knowledge/<name>\` |` at line start;
  `^verified-at: <date>$`), an empty-expectation guard, and **`census_code = 1` by default** — "an unrun census is not a
  pass".

Live-lane snapshots (sibling seats were writing the corpus throughout):

| UTC | entry sha256 | counter line | exit |
|---|---|---|---|
| 06:45:49Z | `a4c8f7ed…110be1` | R2 `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` | 1 |
| 06:46:04Z | `80fd49f6…c03b45` | R2 `entries=1 indexed=1 … census=skipped` | 0; **with `--census` from lane root: `census=fail`, exit 1** |
| 06:50:51Z | `fc29e7f2…ed0fbf9` | R4 `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | **0** |

## 1. Method

Fixtures copy the lane's corpus layout (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/…`) plus the **frozen**
`.ufo/waves/round-29/attempt2/adoption-expect.json` (verbatim: one entry,
`corpus/knowledge/benchmark-task-validity-checklist.md`, five sources S077/S078/S079/S080/S090, `access_date` 2026-10-25).
Five registry rows were appended with `status=mined` and `used-by` naming the citing entry, plus one
`` | `knowledge/benchmark-task-validity-checklist.md` | `` README index row.

Every defect fixture is the **green base** with exactly one field changed, so a moved counter is attributable to that field.
Two fixture families:

- **minimal** `/tmp/r29a2-CounterAudit/rebuild/{base,a_*,…,o_*}` — lane tables + one entry; census not exercisable
  (~90 spurious `E11` for pre-existing rows whose targets the copy lacks).
- **census-clean** `/tmp/r29a2-CounterAudit/croot/` — a fleet root (`shokunin.conf`) with a **full** corpus copy
  (`corpus/knowledge/`, `corpus/lessons/`) and rows inserted **inside** `## Registry`, so `census=ok` is reachable and the
  census column becomes meaningful.

Two fixture-hygiene facts I had to correct mid-run, both worth knowing for reuse:

1. The fixture README must have **every line naming the entry stripped** before the single fixture index row is appended —
   once the live README indexes the entry, defect (b) becomes unreproducible.
2. A "wrong `used-by`" mutation must replace the **whole cell of a real row line**; my first attempt string-replaced the
   entry path inside a template that never contained it, producing a silent no-op fixture that read as a false green.

Reproduce: `python3 /tmp/r29a2-CounterAudit/rebuild.py <dir>` (validated — regenerates the minimal matrix), then

```
PY=<lane>/plans/adoption_check.py
python3 $PY --lane <fixture> --expect <fixture>/expect.json                    # minimal matrix
cd /tmp/r29a2-CounterAudit/croot && python3 $PY --lane <v> --expect <v>/expect.json --census   # census-clean matrix
```

## 2. Green control

| revision | minimal (`base`) | census-clean (`croot/base`, `--census`) |
|---|---|---|
| R1 | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` **exit 0** | same but `census=ok`, **exit 0** |
| R4 | same line without `verified_at`, `census=skipped`, **exit 1** | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` **exit 0** |

R4 cannot exit 0 without `--census` (`census_code = 1` default), so **under R4 the exit code alone no longer discriminates
anything in the unflagged mode** — the printed line does. The frozen do-nothing control receipt
(`control.nothing.txt`, R1-era, run without `--census`) therefore still carries its evidence in the line (`entries=0 …`), not
in its exit 1.

## 3. The four assigned defects

Base line: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1`.

| # | defect | R1 printed line / exit | R4 printed line / exit | field moved |
|---|---|---|---|---|
| (a) | entry file absent | `entries=0 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 verified_at=0 census=skipped` / **1** | `entries=0 indexed=1 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=1 census=skipped` / **1** | `entries` 1→0, `cited_rows` 5→0 (R1 also `verified_at`) |
| (b) | entry present, not indexed in README | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` / **1** | `entries=1 indexed=0 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped` / **1** | `indexed` 1→0 only |
| (c) | cited row `status=queued` (S079) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped` / **1** | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=4 usedby_ok=1 census=skipped` / **1** | `rows_mined` 5→4 only |
| (d) | cited row's `used-by` missing the entry (S090) | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped` / **0** | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=0 census=skipped` / **1** | **R1: none. R4: `usedby_ok` 1→0** |

Census-clean confirmation of (d) — full corpus, `--census`, the wrong `used-by` naming an entry that **exists on disk**:

```
v_usedby_wrong_existing   R1  entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok   exit 0
                          R4  entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=0 census=ok                exit 1
census codes for that fixture: 14 W04, no E-code
```

So R1 passed a five-row entry with one unlinked row while the fleet census also passed it. R4 catches it; the census still
does not.

### (a) Entry absent — caught, but two conjuncts go vacuous under R1
`present` counts non-empty text (`R1 :73-74`, `R4 :74-75`), so an absent entry also empties `cited`; `rows_present` and
`rows_mined` fall to 0 and R1 satisfied `rows_present == len(cited)` / `rows_mined == len(cited)` by `0 == 0`
(`R1 :112-113`). R1's exit 1 came from `entries` and `verified_at`. R3/R4 close this via `required` (`R4 :83-85` with the
empty-expectation guard) compared at the `ok` conjunction.

### (b) Not indexed — clean single-field move
Only `indexed` moved in both revisions. The check is exact/anchored text matching (`R1 :75-76` substring;
`R4 :77` `^| \`knowledge/<name>\` |`); brittleness in §5.

### (c) `queued` — clean single-field move
Only `rows_mined` moved. It reads `registry[row_id][7]`, the status column, matching the header
`corpus/SOURCES.md:21` (`… | status | opened | recheck | used-by |`, index 7). The census is blind: `v_queued` produces no
`E07` (E07 tests the enum and `queued` is legal). This is the counter's unique coverage — nothing else checks that a cited
row was actually mined.

### (d) `used-by` missing — R1 green, R4 red (the assignment's target finding)
R1 (`:83-90`) counted `usedby_ok` **per entry** and `break`ed on the first row naming the entry: with S077–S080 correct,
S090's missing `used-by` was never examined — **no counter moved, exit 0**. R3/R4 use all-of over `entry["sources"]`
(`R4 :90-96`) → `usedby_ok=0`, exit 1. The residual hole is the match operator: `rel in registry[row_id][10]` is a
**substring** test (see (h)).

## 4. Further disagreement probes

Minimal family, no `--census` (R4's exits there are all 1 by construction, so the R4 column reports the line's verdict).

| # | probe | R1 line / exit | R4 line / exit | verdict |
|---|---|---|---|---|
| (e) | all five ids on **one** `source:` line (the lane's dominant convention) | `cited_rows=1 rows_present=1 rows_mined=1` / **0** | `cited_rows=1 …` / **1** | R1 false green → R4 false **red** |
| (f) | no `source:` line at all | `cited_rows=0 …` / **0** | `cited_rows=0 …` / **1** | fixed in R3/R4 |
| (g) | 4 of 5 rows' `used-by` wrong, 1 correct | `usedby_ok=1` / **0** | `usedby_ok=0` / **1** | fixed in R3/R4 |
| (h) | `used-by` names `…-checklist.md.bak` | `usedby_ok=1` / **0** (census-clean: 1, via `E11`) | `usedby_ok=1` / **1** (census `E11`) | **counter field still green**; caught only because `.bak` does not exist |
| (i) | entry file contains a single space | `entries=1 verified_at=0` / 1 | `entries=1 cited_rows=0` / 1 | caught (R1 on `verified_at`, R4 on `required`) |
| (j) | `verified-at: 2026-10-25  (annotation)` | `verified_at=1` / **0** (substring accepted) | gate fails / **1** | R4 rejects the corpus's own annotated style — see below |
| (k) | cites `S091`, no registry row | `rows_present=4 rows_mined=4` / 1 | same / 1 | caught |
| (l) | all five `used-by` wrong | `usedby_ok=0` / 1 | `usedby_ok=0` / 1 | caught |
| (m) | S080's line replaced by a duplicate `S077` cite | `cited_rows=4 …` / **0** | `cited_rows=4 …` / **1** | fixed in R3/R4 |
| (n) | five expected ids **plus** an extra `source: S001` line | n/a | `cited_rows=6 rows_present=6` / 1 | R4 strictness: `sources` is an exact set |
| (o) | README index cell written `…md`\|` (no space before the pipe) | n/a | `indexed=0` / 1 | R4 false red on formatting |

**(e) is the sharpest result.** `SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)` (`:34`) is
line-anchored with one capture group, so it returns only the **first** id per line. Verified directly:
`R.findall("source: S077 — a; S078 — b; S079 — c; S080 — d; S090 — e")` → `['S077']`. Not a corner case: 10 of the 38
`corpus/knowledge/*.md` entries put more than one id on one `source:` line (`attribution-interval-calibration.md` 9,
`extraction-policy-comparison.md` 10, `webarena-task-spec-audit.md` 7, …), and **only the new round-29 entry uses one
`source:` line per id** (5 lines / 5 ids; every other entry has exactly one `source:` line). R1 accepted a
corpus-conventional entry while silently skipping four cited rows' `status` and `used-by`; R3/R4 **reject** that same
conventional entry (`len(cited)=1 != required=5`). The round's entry passes only because it was written in a shape no other
entry uses.

**(j) is R4's own false red, grounded in the lane's corpus.** R4 anchors `^verified-at: <date>$`, but two committed entries
annotate that line — `corpus/knowledge/extraction-policy-comparison.md:2` and
`corpus/knowledge/grader-perturbation-audit.md:2` (`verified-at: 2026-10-21 (source openings …)`). Such an entry would be
refused by the gate. The precise fix is a word boundary, not end-of-line: `^verified-at: <date>\b` — it rejects
`2026-10-251` while accepting the annotated form.

## 5. Counters that cannot be made to disagree (current R4)

| counter | status | why |
|---|---|---|
| `entries` | moves (a, i); `present` is truthiness | a one-space file counts as present (`R4 :74-75`) |
| `indexed` | moves (b); **whitespace-bound** | anchored `^\| \`knowledge/<name>\` \|` (`R4 :77`): `…md`\|` reads 0 (o). It is now line-anchored (R4), so a mention inside prose no longer counts — that half is fixed |
| `cited_rows` | moves (e, m) **only via `required`** | the number itself is still first-id-per-line (`:34`): a conventional five-cite entry reports `cited_rows=1` |
| `rows_present` | moves (k); **no per-row binding** | aggregate over `cited`; an uncited row is invisible; empty set now fails via `required` |
| `rows_mined` | moves (c), unique coverage | same aggregate shape — a citation the regex cannot see is a row whose `status` is never checked (e) |
| `usedby_ok` | moves (d, g, l); **substring, all-or-nothing per entry** | `rel in registry[row_id][10]` (`R4 :94`) accepts `…-checklist.md.bak`; values are 0/1 |
| `verified_at` | moves (j), **not printed in R3/R4** | gated, absent from the line; the docstring's counter list (`:15-22`) does not mention it either, so a reader cannot tell it was checked |
| `census` | **not a corpus-byte counter** | below |

### The census counter is a cwd/roster probe

1. **R1/R2 could not reach `census=ok` from the documented invocation.** The claims' target command is
   `python3 plans/adoption_check.py --expect … --census` (cwd = lane root). At 06:46:04Z R2 printed `census=fail` **exit 1**
   from lane root and `census=ok` from the fleet root on identical bytes. Mechanism: R1/R2 passed `lane.name`
   (`kengaku-shokunin`); `scripts/sources-census.sh:518` matches the **roster** name (`kengaku`, from `rel%-shokunin` at
   `:480`), and the fallback `elif [ -d "$arg" ]` (`:521`) is cwd-relative, so the arg resolved only from the fleet root.
   R3/R4's suffix strip (`R4 :101`) fixes the real lane: `census=ok` exit 0 from lane root, fleet root, and `/tmp` with an
   absolute `--lane` (all three measured on the live tree).
2. **A fixture / non-roster lane is still cwd-dependent.** R4, identical tree: cwd `croot` → `census=ok` exit 0; cwd `/tmp`
   → `census=fail` exit 1. Only cwd changed.
3. **Census is blind to both row-level defects.** `v_queued` and `v_usedby_wrong_existing` produce 14 `W04` and **no**
   `E07`/`E11`. E07 tests the status enum (`queued|mined|rejected`); E11 tests only that each `used-by` path exists on disk
   (`scripts/sources-census.sh:657-659,567`) — so a `used-by` naming the *wrong but existing* entry passes the census.
4. **`census=ok` requires rows inside `## Registry`.** Rows appended at end of file → 5×`E12 row outside Registry section`,
   `census=fail`, every other counter green (fixture `croot/v_outside_registry`: without `--census` it prints the **full
   target line, exit 0** under R3; under R4 the exit is 1 only because the census is unrun). `registry_rows` parses any
   `| S### |` row anywhere in the file (`R4 :38-49`), so section placement is enforced by the census alone. In the live
   `corpus/SOURCES.md` the table runs `## Registry` (line 19) → `## Paths` (line 106) and the round-29 rows landed at
   100–104 — **inside**; the live census has no line matching `S077|S078|S079|S080|S090|task-validity`.
5. **Census needs a full corpus** — a minimal copy yields ~90 spurious `E11` for pre-existing rows.

**Residual hole neither layer closes** `[code]`: a `used-by` cell that names the entry **and** another path that exists
(e.g. `X.md, X.md.bak` with both files present) satisfies the counter's substring test (`R4 :94`) and the census's
path-existence test (`:567`) at once.

## 6. Consequence for the frozen C1 target

Frozen target: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0.

- The **committed** baseline could never print it, for two independent reasons: R1 printed an eighth field
  (`verified_at=1`) and never `census=ok` from the lane root.
- **R4 prints it, exit 0, from the documented invocation** (measured 06:50:51Z on the live tree).
- R4 is **uncommitted** (`M plans/adoption_check.py`). If the round commits corpus bytes without it, the frozen target
  regresses to `census=fail` exit 1 on a fully correct lane — a false negative against a landed round.
- Even under R4, exit 0 is not proof: (h) can still print `usedby_ok=1` with a superset `used-by` (caught here only because
  `.bak` is absent). And R4 rejects correct bytes in two measured shapes — (e) the corpus's dominant citation form and
  (o) a table cell written without the extra space.

Advisory only (production edits are outside this seat's authority):

1. **Citations**: take all ids on each `source:` line (`\bS[0-9]{3,}\b` over the line), keeping `required`. Fixes (e)
   without reopening (f)/(m).
2. **`usedby_ok`**: parse the `used-by` cell into paths and test membership/equality per (entry, source) pair instead of
   `rel in cell`. Acceptance: (h) must fail even when the `.bak` file exists.
3. **`indexed`**: allow optional spaces (`` r"^\| *`knowledge/" + name + "` *\|" ``). Acceptance: (o) must exit 0, (b) stays 1.
4. **`verified_at`**: replace the `$` anchor with `\b` so the corpus's annotated form passes while `2026-10-251` still fails.
   Acceptance: `corpus/knowledge/extraction-policy-comparison.md:2` style must pass; (j) with a trailing digit must fail.
5. **Census**: keep the suffix strip and pass `cwd=lane.parent`, so the verdict is cwd-independent. Acceptance: the `croot`
   tree yields the same `census=` from `croot`, `/tmp` and the fleet root.
6. Record the invocation contract beside the target line: cwd, `--lane`, `--census` (mandatory in R4), and that
   `census=ok` needs the fleet roster reachable from `lane.parent`.

## 7. Evidence

Artifacts (scratch; the report body is the durable locus): `/tmp/r29a2-CounterAudit/` — `rebuild.py` (validated builder),
`rebuild/` (minimal fixtures), `croot/` (census-clean fixtures), `results-by-revision.txt` (R1 vs R3),
`results-all.txt` (R1 minimal), `results-r4.txt` (R4 minimal), `results-r4-croot.txt`, `results-r1-vs-r4-croot.txt`,
`live-census.out`, `adoption_check.committed.py` (R1).

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && date -u +%FT%TZ   # 2026-10-25T06:50:51Z
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census   # R4
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok      exit=0
$ python3 /tmp/r29a2-CounterAudit/adoption_check.committed.py --expect .ufo/waves/…/adoption-expect.json --census  # R1
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

- No blocker. The counter changed three times during the audit (06:46:10Z, 06:47:54Z, 06:50:37Z); R1 and R4 were measured
  on the same fixtures, and every claim names its revision. If R4 moves again, re-run
  `rebuild.py` + `results-r4*.txt` commands — the fixtures are content-addressed by the frozen expect file.
- Risk to the round: R4 is uncommitted, and the frozen target is unreachable at the committed baseline for two independent
  reasons (§6). The commit closing C2 must include `plans/adoption_check.py` alongside `plans/sources_adopt.py`.
- Risk to future work: any `census=` number is meaningless without its cwd; and fixtures must strip the live entry's index
  row, and mutate whole table rows rather than path substrings, or defects silently become no-ops.
