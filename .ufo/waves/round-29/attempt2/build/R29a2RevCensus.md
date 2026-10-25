# R29a2RevCensus — census and index-parity conformance

Seat: reviewer (leaf). Round 29 attempt 2, 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: registry count under the census anchor, knowledge index parity both directions, and the
five staged rows S077/S078/S079/S080/S090 from the package
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.
Read-only on the lane; all scratch in `/tmp/r29a2-census-probe/`. No production file was created,
edited or deleted by this seat. No tool installed or upgraded (nothing was needed).

---

## 1. Registry count

Command (as specified):

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
→ 76
```

| Quantity | Value | Evidence |
|---|---|---|
| Registry rows under the 0–3-space anchor | **76** | command above |
| Contiguous id range | **S001 … S076** (no gaps) | list of ids from the same anchor; first `S001`, last `S076` |
| Distinct ids | **76** (`sort -u` = 76; zero duplicates) | `sort \| uniq -c \| awk '$1>1'` → empty |
| `## Registry` section bounds | lines **19–100** (`## Paths` starts at 100) | `grep -n '^## ' corpus/SOURCES.md` |
| Row lines | **23–98** (76 lines) | anchor line list |
| Malformed (≠11 cells) | **0** | `plans/round28_census.py` → `"malformed": 0` |
| Tier split | A 70 / B 4 / C 2 | same run |
| Status split | mined 64 / queued 8 / rejected 4 | same run |

Cross-check with the lane census instrument:

```
python3 plans/round28_census.py --revision test-census
→ sources: {"rows": 76, "malformed": 0, "statuses": {"mined":64,"queued":8,"rejected":4},
             "tiers": {"A":70,"B":4,"C":2}}
→ exit 0
```

Caveat on the wording "the census parser's own anchor": the 0–3-leading-space anchor is **not**
in `plans/round28_census.py`. That file uses column-0 only (finding F4). The 0–3 anchor lives in
`plans/sources_adopt.py:33` and in the fleet census. On the current tree all four parsers agree on
**76** because every registry row is at column 0.

---

## 2. Knowledge index parity — both directions

```
find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l                → 37
grep -cE '^ {0,3}\|[[:space:]]*`knowledge/' corpus/README.md                  → 37
```

Set comparison (not only counts), `comm` over sorted lists:

| Direction | Count | Entries |
|---|---|---|
| On disk → has a `corpus/README.md` index row | **37 / 37** | none unindexed |
| In `corpus/README.md` index → file exists on disk | **37 / 37** | none dangling |
| Duplicate index rows | **0** | — |
| Index rows at 1–3 leading spaces | **0** (all 37 at column 0) | `grep -cE '^ {1,3}\| \`knowledge/'` → 0 |

Census verdict:

```
python3 plans/round28_census.py --revision test-census
→ knowledge: {"files":37,"index_rows":37,"unindexed":[],"dangling":[],"duplicate_rows":[]}
```

**Parity is exact in both directions on the frozen tree.** 37 index rows are distributed as
29–63 (the `What's here` table, 35 rows) plus 331 and 358 (the round28/round29 admitted-knowledge
tables).

### Post-admission parity (predicted, not asserted)

Admitting `corpus/knowledge/benchmark-task-validity-checklist.md` with its index row makes the
pair **38 / 38**. Verified by simulation on a `/tmp` copy carrying the normalized rows plus the
entry and its README row:

```
python3 plans/round28_census.py --root /tmp/r29a2-census-probe/simfix --revision simfix
→ sources: {"rows": 81, "malformed": 0, "statuses":{"mined":69,"queued":8,"rejected":4},
             "tiers":{"A":74,"B":5,"C":2}}
→ knowledge: {"files":38,"index_rows":38,"unindexed":[],"dangling":[],"duplicate_rows":[]}
```

76 + 5 = 81 rows and 37 + 1 = 38 entries, with the three status counts and tier counts each
summing to 81.

---

## 3. The five staged rows — cell counts

`awk -F'|'` / Python split on `|` over the exact package lines
(`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`):

| Row | Package line | Indent | Raw split parts | **Cells** | Literal `\|` in cell | Escaped `\|\|` | Parses as 11? |
|---|---|---|---|---|---|---|---|
| S077 | 7 | 0 | 13 | **11** | no | no | **yes** |
| S078 | 8 | 0 | 13 | **11** | no | no | **yes** |
| S079 | 9 | 0 | 13 | **11** | no | no | **yes** |
| S080 | 10 | 0 | 13 | **11** | no | no | **yes** |
| S090 | 20 | 0 | 13 | **11** | no | no | **yes** |

Method note: 13 raw `-F'|'` fields = 1 empty field before the leading `|` + 1 empty field after
the trailing `|` + 11 cells. Cell count = `NF - 2`.

**None of the five requested rows is flagged.** All five are at column 0 and carry no literal or
escaped pipe, so every parser in the lane (column-0, 0–3, and the fleet census's `NF==13` check)
reads them as 11 cells.

### Cell content that the gates do reject (same five rows)

| Row | status (cell 8) | opened (cell 9) | recheck (cell 10) | used-by (cell 11) |
|---|---|---|---|---|
| S077 | `mined` | `2026-10-23` | `2026-10-23 — re-verify at the next upstream release (Gate S077)` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S078 | `mined` | `2026-10-23` | `2026-10-23 — re-verify at the next upstream release (Gate S078)` | `corpus/knowledge/benchmark-task-validity-checklist.md, corpus/knowledge/judge-calibration-thresholds.md` |
| S079 | `mined` | `2026-10-23` | `2026-10-23 — re-verify at the next upstream release (Gate S079)` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S080 | `mined` | `2026-10-23` | `2026-10-23 — re-verify at the next upstream release (Gate S080)` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S090 | `mined` | `2026-10-23` | `2026-10-23 — re-verify at the next upstream release (Gate S090)` | `corpus/knowledge/benchmark-task-validity-checklist.md` |

Rows parse; two cells per row do not conform. See F1 and F2 — both are blocking for C1's
`census=ok`.

---

## 4. Findings by severity

### F1 — HIGH, blocking C1: prose `recheck` on all five rows is `E09`-invalid

The package `recheck` cells begin with an ISO date but are prose, not an ISO date, not `<N>d`,
and not a symbolic cadence (`symbolic()` is `^[A-Za-z][A-Za-z0-9 _-]*$`, so a leading digit
fails). The fleet census is the instrument behind `adoption_check.py`'s `census=` field.

Reproduced by appending the package bytes verbatim inside the `## Registry` section of a
`/tmp` copy of the lane registry and validating:

```
scripts/sources-census.sh validate --file /tmp/r29a2-census-probe/simlane/corpus/SOURCES.md --today 2026-10-25
file	E09	S077 recheck=2026-10-23 — re-verify at the next upstream release (Gate S077)
file	E09	S078 recheck=2026-10-23 — re-verify at the next upstream release (Gate S078)
file	E09	S079 recheck=2026-10-23 — re-verify at the next upstream release (Gate S079)
file	E09	S080 recheck=2026-10-23 — re-verify at the next upstream release (Gate S080)
file	E09	S090 recheck=2026-10-23 — re-verify at the next upstream release (Gate S090)
EXIT=1
```

This is also an outlier against the lane's own convention: of the 76 live rows, `recheck` is
ISO 32 / `<N>d` 27 / symbolic 22 (`on-release`) / **PROSE 0**. A prose `recheck` has never been
admitted here.

Remedy is already the C2 contract (`plans/sources_adopt.py`, requirement 3: prose `recheck`
normalized to the frozen access date). With `recheck = 2026-10-25` substituted, validation is
clean (see F2 for the second, independent blocker):

```
scripts/sources-census.sh validate --file /tmp/r29a2-census-probe/simfix/corpus/SOURCES.md --today 2026-10-25
file	ok	/tmp/r29a2-census-probe/simfix/corpus/SOURCES.md
EXIT=0     (census rows = 81)
```

### F2 — HIGH, blocking C1: S078's `used-by` names an entry that does not exist in the lane

`S078` `used-by` = `corpus/knowledge/benchmark-task-validity-checklist.md,
corpus/knowledge/judge-calibration-thresholds.md`. The second path is absent from
`corpus/knowledge/` (disk listing has `llm-judge-calibration.md`, not
`judge-calibration-thresholds.md`), and it is not an entry C1 admits. On the same verbatim append:

```
file	E11	S078 missing used-by corpus/knowledge/judge-calibration-thresholds.md
```

`E11` alone forces exit 1 → `census=fail` → the frozen C1 target line is unreachable. C2
requirement 3 ("`used-by` is rewritten to exactly the admitted entries citing the row") is what
must strip this; if the gate is run with `--entries corpus/knowledge/benchmark-task-validity-checklist.md`
it should emit a single-entry `used-by`. If the append is done by hand instead, this cell must be
edited — otherwise the round fails on a strawman.

Note the ordering hazard: `E09` and `E11` are both present, so fixing only the `recheck`
normalization still leaves `census=fail`.

### F3 — MEDIUM: `plans/adoption_check.py` silently drops every 0–3-indented registry row

`plans/adoption_check.py:33` matches a 0–3-space anchor, but `:44` splits cells with
`raw.rstrip()[1:-1].split("|")`, which assumes the row starts at column 0. For an indented row the
first `[1:-1]` slice consumes the indent space instead of the leading `|`, producing 12 cells and
hitting the `continue` at `:45` — the row is matched and then discarded.

Repro on the `/tmp` copy with **only** `S077` shifted by one leading space inside the `## Registry`
section:

```
python3 plans/adoption_check.py --lane /tmp/r29a2-census-probe/simind1 --expect ...
→ entries=1 indexed=1 cited_rows=5 rows_present=4 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped
→ exit 1

scripts/sources-census.sh census --file /tmp/r29a2-census-probe/simind1/corpus/SOURCES.md
→ file rows 81 ; FLEET rows 81 ; exit 0
```

The two instruments disagree on the same bytes. It is fail-closed (under-counts, never
false-greens), and the five staged rows are at column 0 so C1 is not currently affected — but the
`0–3` in `ROW_RE` is not load-bearing as written, and the "" claim that this parser follows the
census anchor does not hold. `plans/sources_adopt.py:69-76` does this correctly
(`body = stripped.strip()` then `body[1:-1].split("|")`), which is the shape `adoption_check.py`
should adopt.

### F4 — MEDIUM: the "census parser's own 0–3 anchor" is not in `plans/round28_census.py`

`plans/round28_census.py:40` uses `re.match(r"^\|\s*S[0-9]{3,}\s*\|", line)` — column 0 only.
The 0–3 anchor is in `plans/sources_adopt.py:33`. Consequence on the same 1-space-shifted copy:

```
python3 plans/round28_census.py --root /tmp/r29a2-census-probe/simind1 --revision simind1
→ rows=80 malformed=0 knowledge=38 38      # the indented row vanishes, no warning
```

So the lane holds four different registries-with-different-anchors: `round28_census.py` (column 0),
`sources_adopt.py` (0–3, correct split), `adoption_check.py` (0–3 match, column-0 split), and
`sources-census.sh` (0–3, `NF==13`). They agree at 76 today only because every row is at column 0.
Any future indented row produces a silent, differently-sized count per instrument. If the C2
justification line leans on "the census parser's own anchor", it should name
`scripts/sources-census.sh` / `plans/sources_adopt.py`, not `round28_census.py`.

### F5 — MEDIUM: the frozen C1 target line omits `verified_at=`, which the tool now prints

C1 (frozen) requires `adoption_check.py` to print **exactly**

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

The implemented `plans/adoption_check.py:104-108` prints

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
```

Observed on the `/tmp` simulation (`census=skipped` there only because the fleet census resolves a
lane by name under `--root`; the lane-side `validate` on the same file exits 0):

```
python3 plans/adoption_check.py --lane /tmp/r29a2-census-probe/simfix --expect /tmp/r29a2-census-probe/expect.json
→ entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=skipped
→ exit 0
```

A literal diff against the frozen line fails on the inserted `verified_at=1 `. Either the report
must present the actual line (honest, with the extra field noted) or the field order must match the
frozen text. This is a reporting contract mismatch, not a behaviour defect — `verified_at` is a
strengthening (it proves the re-grounding duty), so the claim text is the thing that is stale.

### F6 — LOW: an append at end-of-file is `E12`-invalid

Appending the block to the end of `corpus/SOURCES.md` (rather than before line 100, `## Paths`)
produces:

```
file	E12	S077 row outside Registry section
file	E12	S078 row outside Registry section
file	E12	S079 row outside Registry section
file	E12	S080 row outside Registry section
file	E12	S090 row outside Registry section
EXIT=1
```

The `## Registry` section is lines 19–100 and the table ends at line 98. The five rows must be
inserted at line 99 (after `S076`), not at EOF.

### F7 — LOW: `opened` stays `2026-10-23` while the entry claims 2026-10-25 access

All five rows carry `opened = 2026-10-23` (package line 7–20). C1's re-grounding duty requires the
entry and its Gate block to carry `2026-10-25`; it does not literally require the `opened` cell to
be rewritten, and `E08` passes because `2026-10-23` is a past date. The result is a row whose
`opened` and whose entry `verified-at` name different days for the same opening claim. Recommend
setting `opened = 2026-10-25` for the five rows so the registry and the counter agree; if the
package's 2026-10-23 opening is meant to be preserved, the entry must say so rather than imply a
single access date.

### F8 — INFO: index-row shape must be column 0 with a pipe immediately after the closing backtick

Two different index predicates are in play, and they disagree on two of four shapes:

| Row shape | `round28_census.py:43` `^\|\s*\`(knowledge/…)\`\s*\|` | `adoption_check.py:76` substring ``| `knowledge/<name>` |`` |
|---|---|---|
| `\| \`knowledge/x.md\` \| … \|` | counts | counts |
| `  \| \`knowledge/x.md\` \| … \|` (2-space indent) | **does not count** | counts |
| `\|\`knowledge/x.md\`\|…\|` (no space) | counts | **does not count** |
| `\| \`knowledge/x.md\`  \| … \|` (2 spaces after) | counts | **does not count** |

All 37 existing rows are the first shape. Author the new row in that exact shape or the pair of
gates will disagree. The disagreement is fail-closed in both directions for C1 (`census` cross-check
catches the indent case; `indexed` catches the no-space case), so it costs a diagnosis round, not a
false green.

### F9 — INFO: `plans/registry_check.py` cannot see the new rows

`plans/registry_check.py:13` pins the population to
`plans/fixtures/r28/registry/population.json` (`base_revision` frozen): 13 source ids, **S038–S060**,
and 35 knowledge paths. `parse_registry` skips any id outside `population["source_ids"]` (`:40`),
and `check` only walks `population["knowledge_paths"]` (`:57`). Therefore S077/S078/S079/S080/S090
and the pending `benchmark-task-validity-checklist.md` are outside its scope by construction, and
**the dangling `judge-calibration-thresholds.md` used-by (F2) is invisible to `registry_check.py`**.
The fleet census (`E11`) is the only instrument that catches it. Do not read a green
`registry_check.py` as evidence that the adopted rows' links are sound.

### F10 — INFO: the requested five rows are not the only malformed rows in the package

The task scopes the cell check to the five requested rows, and all five pass. For completeness, the
same 175-row package contains escaped pipes that *do* break the 11-cell clause — outside this
seat's five, but a hazard if any tool ever stages the whole `SOURCES.append.md` as one block:

| Row | Package line | Raw split parts | Cells | Escaped text |
|---|---|---|---|---|
| S093 | 23 | 14 | **12** | `fail_to_pass \| pass_to_pass` |
| S101 | 31 | 17 | **15** | `git apply --verbose … \|\| git apply --3way … \|\| patch --fuzz=3 -p…` |

Both are the accepted-but-silent `\|\|` inside a cell that `plans/sources_adopt.py`'s
`split_cells` correctly refuses (`escaped-pipe`, selftest `CASE escaped-pipe-refused PASS`). If the
adopt gate is invoked with `--package` on the whole file, the `check` stage will report them and
exit non-zero — the correct behaviour, but it means the gate cannot be run "clean" against the
package as delivered; only per-id staging is clean.

---

## 5. Gate state observed (context for the above)

```
python3 plans/sources_adopt.py --selftest
CASE collision-zero-indent PASS    CASE collision-one-space PASS   CASE collision-three-space PASS
CASE four-space-not-a-row PASS     CASE escaped-pipe-refused PASS  CASE prose-recheck-normalized PASS
CASE usedby-projected PASS         CASE duplicate-staged-id PASS   CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=0        exit=0
```

```
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin
→ 13 × W04 duplicate-url warnings, then  kengaku-shokunin  ok  .../corpus/SOURCES.md  ; exit=0
```

The baseline tree is clean (warnings only). C2's ten cases exist and pass; the `0–3` anchor is
demonstrably load-bearing in `sources_adopt.py` (`collision-one-space` / `collision-three-space`
vs `four-space-not-a-row`).

---

## 6. Residual risk and verification gaps

- The post-admission numbers (81 rows, 38/38 parity, tier A74/B5/C2, status mined 69) are
  **simulated** on a `/tmp` copy, not measured on the lane. They will hold only if the landed block
  is exactly the five normalized rows plus one column-0 README row.
- `census=ok` was verified for the lane-side `validate` on the simulated registry, not through
  `adoption_check.py --census` (the fleet script resolves a lane by name under `--root`, so a
  `/tmp/simfix` lane cannot resolve without a `shokunin.conf` entry). The real `--census` run must
  be executed on the lane itself after landing.
- F1/F2 are demonstrated by reproducing the package bytes; they are not a claim about whether the
  L1 will normalize. If the L1 lands the rows via `sources_adopt.py --out` with
  `--access-date 2026-10-25 --entries corpus/knowledge/benchmark-task-validity-checklist.md`, both
  are expected to clear — that expectation is `[INFERENCE]` from reading `build_block`, not run.
- The five rows' located quotes and source re-openings are other seats' scope; this seat verified
  only cell structure, index parity, and census conformance.
- No `lsp` semantic queries were used: this scope is Markdown/registry data and Python string
  parsing, where the authoritative evidence is the parser output reproduced above.

## 7. Bottom line for the L1

- Registry **76**, contiguous `S001–S076`, zero duplicates, zero malformed.
- Knowledge parity **37/37 both directions**, zero unindexed, zero dangling, zero duplicate rows.
- All **five staged rows parse as exactly 11 cells** with no literal or escaped pipe — **nothing to
  flag on the cell-count axis**.
- Two cells per row nevertheless block the round: prose `recheck` (`E09` ×5, F1) and S078's
  dangling `judge-calibration-thresholds.md` `used-by` (`E11`, F2). Verbatim append → `census=fail`.
- Normalized append (recheck → `2026-10-25`, used-by → admitted entry only), inserted at line 99
  inside `## Registry` → `ok`, 81 rows, exit 0.
- The frozen C1 target line is missing the `verified_at=1` field the tool prints (F5); report the
  actual line.
