# R29a2RevCensus — census and index-parity conformance

Seat: reviewer (leaf). Round 29 attempt 2, 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: registry count under the census anchor, knowledge index parity in both directions, and the
five staged rows S077/S078/S079/S080/S090 from the package
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.

Read-only on the lane; scratch in `/tmp/r29a2-repro2/`, `/tmp/r29a2-ind/`. This seat created, edited
or deleted **no** production file. No tool installed or upgraded (none needed).

## Measurement instant — read this first

The lane changed under this review three times. Every number below is pinned to one instant:

**2026-10-25 03:51:31**, with `corpus/SOURCES.md` mtime 03:50, `corpus/README.md` 03:51,
`corpus/lessons/round-29.md` 03:51, `plans/adoption_check.py` 03:50.

Observed trajectory of the registry during the review:

| Instant | Registry rows | Knowledge files | Note |
|---|---|---|---|
| first measurement | **76** | 37 | pre-landing; five rows still only in the package |
| mid-review | **81** | 38 | S077–S080, S090 + entry + index row landed |
| **final (03:51:31)** | **82** | **38** | **S091** landed at line 106; `plans/adoption_check.py` hardened |

Consequence: **six** findings that were live at some point during this review are now discharged on
the committed bytes (F1, F2, F3, F5, F6, F7), and two of them — F3 and F5 — were fixed while this
report was being written. §4 records each with the reproduction that proves it *was* real, so the
discharge is auditable rather than asserted, and §7 states what that costs in verification strength.
Two findings remain live: **F4** (a parser anchor) and **F11** (a stale count in the round lesson).

---

## 1. Registry count — final tree

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
→ 82
```

| Quantity | Value | Evidence |
|---|---|---|
| Registry rows under the 0–3-space anchor | **82** | command above |
| Distinct ids / duplicates | **82 / 0** | `sort \| uniq -c \| awk '$1>1'` → empty |
| id range | **S001–S080**, then **S090, S091** | id enumeration |
| Absent ids inside the range | **S081–S089** (9 ids) | `missing in range: S081,…,S089` |
| Malformed (≠11 cells) | **0** | `plans/round28_census.py` → `"malformed": 0` |
| Tier split | **A 76 / B 4 / C 2** (= 82) | same run |
| Status split | **mined 70 / queued 8 / rejected 4** (= 82) | same run |
| `## Registry` section | lines **19–107** (`## Paths` begins at 107) | `grep -n '^## ' corpus/SOURCES.md` |
| Landed rows | S077–S080 at **100–103**, S090 at **104**, S091 at **106**, all column 0 | row anchors |

The **S081–S089 gap is expected, not a defect**: those ids are staged package rows the round
deliberately did not admit (`corpus/lessons/round-29.md:181`, Gate row "remaining 168 staged rows
and 64 staged entries | reject this round"). Do not read "82 rows" as "S001–S082"; the registry is
contiguous only over S001–S080.

Full census, three sub-gates green:

```
python3 plans/round28_census.py --revision final
→ sources: {"rows":82,"malformed":0,"statuses":{"mined":70,"queued":8,"rejected":4},
             "tiers":{"A":76,"B":4,"C":2}}
→ knowledge: {"files":38,"index_rows":38,"unindexed":[],"dangling":[],"duplicate_rows":[]}
→ c1_exit=0  c2_exit=0  state_exit=0

scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin
→ kengaku-shokunin	ok	.../corpus/SOURCES.md        (exit 0; 14 W04 duplicate-url warnings only)
```

---

## 2. Knowledge index parity — both directions

| Direction | Pre-landing | **Final** |
|---|---|---|
| Files on disk → has a `corpus/README.md` index row | 37 / 37 | **38 / 38** |
| README index rows → file exists on disk | 37 / 37 | **38 / 38** |
| Unindexed | none | **none** |
| Dangling | none | **none** |
| Duplicate index rows | 0 | **0** |
| Index rows at 1–3 leading spaces | 0 | **0** (`index=38`, `index_col0=38`) |

```
find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l   → 38
grep -cE '^ {0,3}\|[[:space:]]*`knowledge/' corpus/README.md      → 38
grep -cE '^\| `knowledge/' corpus/README.md                       → 38   (all column 0)
```

**Parity is exact in both directions.** The new entry's index row is `corpus/README.md:64`, at
column 0, in the canonical ``| `knowledge/<name>.md` | … |`` shape — it satisfies both index
predicates in play (§4 F8), and the frontier lines at `:249` and `:271` were updated in the same
change.

---

## 3. The five rows — cell counts

Method: split on `|`; cells = `NF - 2` (13 raw `-F'|'` fields = leading empty + 11 cells + trailing
empty). Checked both as **delivered in the package** and as **landed**.

| Row | Package line | Landed line | Indent | Raw parts | **Cells** | Literal `\|` in cell | Escaped `\|\|` | Parses as 11? |
|---|---|---|---|---|---|---|---|---|
| S077 | 7 | 100 | 0 | 13 | **11** | no | no | **yes** |
| S078 | 8 | 101 | 0 | 13 | **11** | no | no | **yes** |
| S079 | 9 | 102 | 0 | 13 | **11** | no | no | **yes** |
| S080 | 10 | 103 | 0 | 13 | **11** | no | no | **yes** |
| S090 | 20 | 104 | 0 | 13 | **11** | no | no | **yes** |

**Nothing to flag on the cell-count axis.** All five are at column 0 and carry no literal or escaped
pipe, so every lane parser (column-0, 0–3, `NF==13`, `body[1:-1].split("|")`) reads them as 11 cells.

```
line 100 S077 cells=11   line 101 S078 cells=11   line 102 S079 cells=11
line 103 S080 cells=11   line 104 S090 cells=11   (no literal/escaped pipe in any)
```

The sibling row S091 (line 106) also checks out at 11 cells, `tier=A`, `status=mined`,
`opened=2026-10-25`, `recheck=180d`, `used-by corpus/lessons/round-29.md`.

### Landed cell content — all five conform

| Row | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|
| S077 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S078 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S079 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S080 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S090 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |

### Package cell content — what a verbatim append would have carried

All five carried `opened = 2026-10-23`, a prose `recheck`
`2026-10-23 — re-verify at the next upstream release (Gate S0NN)`, and S078 additionally named
`corpus/knowledge/judge-calibration-thresholds.md`. That is the substance of F1/F2.

---

## 4. Findings

Severity is current. **DISCHARGED** marks a defect that was real in the reviewed bytes and is fixed
on the final tree — the reproduction is kept so the discharge can be audited and so the gate's value
is documented rather than assumed.

### F1 — DISCHARGED (was HIGH/blocking): prose `recheck` made the append `E09`-invalid

Reproduced by reconstructing the 76-row baseline from current bytes (delete the five landed rows)
and inserting the package rows verbatim inside `## Registry`:

```
scripts/sources-census.sh validate --file $P/base/corpus/SOURCES.md --today 2026-10-25
file	E09	S077 recheck=2026-10-23 — re-verify at the next upstream release (Gate S077)
file	E09	S078 recheck=2026-10-23 — re-verify at the next upstream release (Gate S078)
file	E09	S079 recheck=2026-10-23 — re-verify at the next upstream release (Gate S079)
file	E09	S080 recheck=2026-10-23 — re-verify at the next upstream release (Gate S080)
file	E09	S090 recheck=2026-10-23 — re-verify at the next upstream release (Gate S090)
EXIT=1
```

Why it fires: `symbolic()` is `^[A-Za-z][A-Za-z0-9 _-]*$`, so a cell starting with a digit is
neither an ISO date, nor `<N>d`, nor symbolic. It was also an outlier — of the 76 baseline rows,
`recheck` was ISO 32 / `<N>d` 27 / symbolic 22 (`on-release`) / **prose 0**.

**Final tree:** `recheck = 2026-10-25` on all five; live census `ok`, exit 0.

### F2 — DISCHARGED (was HIGH/blocking): S078's `used-by` named a non-existent entry

The package's S078 cell was `corpus/knowledge/benchmark-task-validity-checklist.md,
corpus/knowledge/judge-calibration-thresholds.md`; the second path has never existed in
`corpus/knowledge/` (the lane holds `llm-judge-calibration.md`, a different entry).

```
file	E11	S078 missing used-by corpus/knowledge/judge-calibration-thresholds.md
```

F1 and F2 were **independent** — normalizing only `recheck` still fails on `E11` alone:

| Variant | Result | Exit |
|---|---|---|
| V1 package bytes verbatim | `E09` ×5 **+** `E11` S078 | 1 |
| V2 `recheck` normalized only | `E11` S078 **only** | 1 |
| V3 `recheck` + `used-by` normalized | `ok` | 0 |

**Final tree:** `used-by` is exactly `corpus/knowledge/benchmark-task-validity-checklist.md`; `ok`.

### F3 — DISCHARGED (was MEDIUM): `adoption_check.py` silently dropped indented registry rows

At the revision I first read, `plans/adoption_check.py:44` split cells with
`raw.rstrip()[1:-1].split("|")` while its `ROW_RE` accepted a 0–3-space anchor. For an indented row
the `[1:-1]` slice consumed the indent instead of the leading `|`, yielding 12 cells and hitting the
`continue` at `:45` — matched, then discarded.

Observed against that revision, with only `S077` shifted one space left:

```
entries=1 indexed=1 cited_rows=5 rows_present=4 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped
exit 1
```

while the fleet census read the same bytes as `81 rows`, `validate ok`, exit 0.

**Final tree:** the same probe now reports `rows_present=5`. The fix is `plans/adoption_check.py:44`
→ `body = raw.strip()` before the split, exactly the shape `plans/sources_adopt.py:71,74` already
used. The `exit 1` in that probe is now correct-by-design and unrelated:
`:99` sets `census_code = 1  # an unrun census is not a pass`, so the counter refuses to pass without
`--census`.

### F4 — LIVE, MEDIUM: the "census parser's own 0–3 anchor" is not in `plans/round28_census.py`

`plans/round28_census.py:40` is `re.match(r"^\|\s*S[0-9]{3,}\s*\|", line)` — **column 0 only**
(file unchanged since 2026-10-21 11:05). The 0–3 anchor lives in `plans/sources_adopt.py:33` and in
`scripts/sources-census.sh`. On a copy of the **final** tree with one landed row shifted a single
leading space (still inside the 0–3 census clause):

```
python3 plans/round28_census.py --root <indented copy> --revision ind  → rows=81 malformed=0
python3 plans/round28_census.py --revision live                        → rows=82
```

The row vanishes with **no** malformed-count increase — a silent under-count, not a rejected row.
So the lane holds four notions of "a registry row": `round28_census.py` column 0;
`sources_adopt.py` 0–3 with a correct split; `adoption_check.py` 0–3 with a now-correct split;
`sources-census.sh` 0–3 with `NF==13`. They agree at 82 today only because every row is column 0.
If C2's justification cites "the census parser's own anchor", it should name `sources_adopt.py` /
`sources-census.sh`, not `round28_census.py` — or `round28_census.py:40` should accept ` {0,3}`.

### F5 — DISCHARGED (was LOW): the frozen C1 target line did not match the counter's output

C1 (frozen) requires exactly

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

At the revision I first read, the counter printed an extra `verified_at=1 ` field before `census=`.
**Final tree:** the printed line matches the frozen text **verbatim** —

```
python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
→ entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
→ exit 0
```

— and this is a display change only, not a weakening: `verified_at_ok == len(entries)` is still
enforced in the pass condition (`plans/adoption_check.py:124`). The counter's checks also got
stricter in the same edit (`:83,:120,:124`):

- `required = sum(len(entry["sources"]))` and `len(cited) == required` — an entry citing *more* ids
  than it declares now fails;
- `usedby_ok` is an **all-of** test per entry (every declared source must name the entry), replacing
  the earlier any-of `break`;
- an empty expectation returns 1 (`:83-85`), not a vacuous pass;
- `indexed` is now an anchored `^\| \`knowledge/<name>\` \|` regex, and `verified_at` an anchored
  line match, instead of bare substrings.

### F6 — DISCHARGED (was LOW): an end-of-file append is `E12`-invalid

Appending the block at EOF instead of inside `## Registry` yields
`E12 S077 … S090 row outside Registry section` ×5, exit 1. The landed rows are at lines 100–104
(and S091 at 106), inside the section that runs 19–107: correct.

### F7 — DISCHARGED (was LOW): `opened` disagreed with the claimed access date

Package rows carried `opened = 2026-10-23` while C1 asserts 2026-10-25 re-grounding. Landed rows
carry `opened = 2026-10-25`, matching the entry's `verified-at: 2026-10-25`.

### F11 — LIVE, LOW: the attempt-2 lesson's own transition accounting is stale by one row

`corpus/lessons/round-29.md:205` states:

> Registry 76 → 81 rows; tiers A 70 → 75, B 4 → 4, C 2 → 2.

Measured on the final tree: **82 rows**, tiers **A 76 / B 4 / C 2**, statuses
mined 70 / queued 8 / rejected 4. The gap is S091, which landed at line 106 (tier `A`, `mined`,
`recheck=180d`, `used-by corpus/lessons/round-29.md`) after that paragraph was written — the Gate
table itself already carries the S091 decision at `:182`, so the paragraph, not the decision, is
what drifted. Same class as M94 (count units) which this round already logged: the prose count and
the registry disagree, and only the registry is authoritative. Fix: amend the sentence to
"76 → 82 rows; tiers A 70 → 76, B 4 → 4, C 2 → 2" and say S091 entered as a second, separately
justified row.

### F8 — INFO: the two index predicates agree on the dangerous shapes and still differ on spacing

| Row shape | `round28_census.py:43` ``^\|\s*`(knowledge/…)`\s*\|`` | `adoption_check.py:77` ``^\| `knowledge/<name>` \|`` |
|---|---|---|
| ``\| `knowledge/x.md` \| … \|`` (canonical) | counts | counts |
| indented 2 spaces | does **not** count | does **not** count |
| ``\|\`knowledge/x.md\`\|`` (no space) | counts | does **not** count |
| 2 spaces after the filename | counts | does **not** count |
| a `\| \`knowledge/x.md\` \|` mention inside a comment | does **not** count | does **not** count |

Both now reject indentation and in-comment mentions (both were live divergences earlier in this
review), so the fail-open cases are gone. What remains is spacing tolerance: a row the census counts
could still be uncounted by the counter, which fails closed (exit 1 with `indexed=0`) and is caught
immediately. `corpus/README.md:64` is canonical, so both agree on the real entry.

### F9 — INFO: `plans/registry_check.py` cannot see any of this round's rows

`plans/registry_check.py:13` pins the population to `plans/fixtures/r28/registry/population.json`:
**13 source ids, S038–S060**, and **35** knowledge paths. `parse_registry` skips ids outside
`population["source_ids"]` (`:42`), and `check` only walks `population["knowledge_paths"]` (`:57`).
S077–S080, S090, S091 and `benchmark-task-validity-checklist.md` are outside it by construction. A
green `registry_check.py` is **not** evidence about this round's links; the fleet census (`E09`/
`E11`) is the only instrument that reads them — which is exactly why F1/F2 would not have been
caught by the lane's own pre-existing gate.

### F10 — INFO: the five requested rows are not the only malformed rows in the package

Scoped to the five, nothing is malformed. For the record, the same 175-row package carries escaped
pipes that do break the 11-cell clause — a hazard only if a tool ever stages the whole file as one
block:

| Row | Package line | Raw parts | Cells | Escaped text |
|---|---|---|---|---|
| S093 | 23 | 14 | **12** | `fail_to_pass \| pass_to_pass` |
| S101 | 31 | 17 | **15** | `git apply … \|\| git apply --3way … \|\| patch --fuzz=3 …` |

`plans/sources_adopt.py`'s `split_cells` correctly refuses these (`escaped-pipe`; selftest
`CASE escaped-pipe-refused PASS`). `corpus/lessons/round-29.md:181` records the same two rows and
the 171 prose `recheck` cells they carry.

---

## 5. Observations that are documented decisions, not findings

Recorded so a reviewer scanning the numbers does not re-litigate them.

**S090 tier `B` → `A`.** The package graded S090 `B` with an in-cell reason ("tier B because the
page carries no visible publication date"). Landed is `A`. This is **documented and reasoned** at
`corpus/lessons/round-29.md:199-205`:

> S090 enters tier **A**, not the package's B: SOURCES-contract tier B is "strong secondary", and a
> first-party release announcement is a maintainer statement (tier A). The package's stated reason
> — no visible publication date — is page-scoped only, because the publisher's own index dates the
> post.

The landed anchor cell carries the supporting evidence ("the publisher's news index dates this post
2025-11-07"), so the promotion rests on a falsified objection rather than a preference. **My own
earlier inference was wrong here**: extrapolating from the package's tier cells I predicted
A 74 / B 5 / C 2 for a five-row append; the actual five-row state was A 75 / B 4 / C 2. The
promotion is the correct reading. Whether an index-page date suffices for tier A is a judgment for
the claim critic, not this seat — but a later reader should check that date claim, not just the tier
letter.

**`adopt-block.md` is not what landed, for 3 of 5 rows.**
`.ufo/waves/round-29/attempt2/adopt-block.md` matches the committed rows byte-for-byte for S077 and
S078 and differs for S079/S080/S090 — in the `anchor` cell only (line-number corrections and
quote re-boundaries). Cause is recorded as M97 at `corpus/lessons/round-29.md:166`: `build_block`
rewrites only `status`/`recheck`/`used-by`/`opened`, so entry-side corrections did not propagate;
the round's own rule is "correct the entry first, then rebuild the block". The registry is the
authoritative surface; the block file is a pre-correction snapshot. Re-running the gate against the
package now correctly reports the ids as collisions (`gate-postappend-rerun.txt`: `registry=81
collisions=5 S077 S078 S079 S080 S090`), which is the gate working as designed.

**`build-validation.txt` is 0 bytes.** `.ufo/waves/round-29/attempt2/build-validation.txt` is empty
(0 bytes, mtime 03:40) and referenced by no `*.json` receipt in that directory. The build's
validation evidence lives in `corpus/evidence/round29-attempt2/`. An empty file whose name promises
validation is a trap for a later reader; delete it or fill it.

---

## 6. Reproduction

Every number above is reproducible from the final tree with no lane writes. This was run
end-to-end; the outputs quoted in §3–§4 come from it.

```bash
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
P=/tmp/r29a2-repro2; rm -rf "$P"; mkdir -p "$P"

# A. census + parity + counter (final tree)
cd "$LANE"
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md          # 82
find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l        # 38
grep -cE '^ {0,3}\|[[:space:]]*`knowledge/' corpus/README.md          # 38
python3 plans/round28_census.py --revision repro
python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census

# B. reconstruct the 76-row pre-landing baseline (delete the five landed rows)
mkdir -p "$P/base/corpus"; cp corpus/SOURCES.md corpus/README.md "$P/base/corpus/"
cp -r corpus/knowledge corpus/lessons "$P/base/corpus/"
python3 - "$P/base/corpus/SOURCES.md" <<'PY'
import re,sys
p=sys.argv[1]; want={"S077","S078","S079","S080","S090"}
keep=[l for l in open(p).read().splitlines()
      if not ((m:=re.match(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|", l)) and m.group(2) in want)]
open(p,'w').write("\n".join(keep)+"\n")
PY

# C. insert package bytes verbatim, inside ## Registry
python3 - "$PKG" "$P/base/corpus/SOURCES.md" <<'PY'
import re,sys
pkg=open(sys.argv[1]).read().splitlines(); dst=sys.argv[2]; want={"S077","S078","S079","S080","S090"}
raw=[l for l in pkg if (m:=re.match(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|", l)) and m.group(2) in want]
lines=open(dst).read().splitlines()
last=max(i for i,l in enumerate(lines) if re.match(r"^\|\s*S[0-9]{3,}\s*\|", l))
open(dst,'w').write("\n".join(lines[:last+1]+raw+lines[last+1:])+"\n")
PY
"$CENSUS" validate --file "$P/base/corpus/SOURCES.md" --today 2026-10-25 \
  | grep -E '	E[0-9][0-9]	|	ok	'          # E09 x5 + E11 S078, exit 1

# D. normalize recheck and used-by independently: V2 = recheck only, V3 = recheck + used-by
for variant in v2 norm; do
  cp -r "$P/base" "$P/$variant"
  NORMALIZE_USEDBY=$([ "$variant" = norm ] && echo 1 || echo 0) \
  python3 - "$P/$variant/corpus/SOURCES.md" <<'PY2'
import os,re,sys
p=sys.argv[1]; want={"S077","S078","S079","S080","S090"}
norm_usedby = os.environ["NORMALIZE_USEDBY"] == "1"
out=[]
for l in open(p).read().splitlines():
    m=re.match(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|", l)
    if m and m.group(2) in want:
        c=[x.strip() for x in l.rstrip()[1:-1].split("|")]
        c[9]="2026-10-25"
        if norm_usedby: c[10]="corpus/knowledge/benchmark-task-validity-checklist.md"
        l="| "+" | ".join(c)+" |"
    out.append(l)
open(p,'w').write("\n".join(out)+"\n")
PY2
  echo "--- $variant"
  "$CENSUS" validate --file "$P/$variant/corpus/SOURCES.md" --today 2026-10-25 \
    | grep -E '	E[0-9][0-9]	|	ok	'
  echo "EXIT=${PIPESTATUS[0]}"
done
# expect: v2 -> E11 S078 only, exit 1 ;  norm -> ok, exit 0
```

The F3/F4 parser probes are separate and smaller — shift one landed row by a single leading space
(still inside the 0–3 census clause) and compare the instruments on identical bytes:

```bash
P=/tmp/r29a2-ind; rm -rf $P; mkdir -p $P/corpus
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
cp corpus/SOURCES.md corpus/README.md $P/corpus/; cp -r corpus/knowledge corpus/lessons $P/corpus/
cp -r plans $P/
python3 - "$P/corpus/SOURCES.md" <<'PY3'
import re,sys
p=sys.argv[1]; out=[]
for l in open(p).read().splitlines():
    if re.match(r"^\|\s*S077\s*\|", l): l=" "+l      # one leading space
    out.append(l)
open(p,'w').write("\n".join(out)+"\n")
PY3
python3 plans/adoption_check.py --lane $P --expect .ufo/waves/round-29/attempt2/adoption-expect.json
python3 plans/round28_census.py --root $P --revision ind
"$CENSUS" census --file $P/corpus/SOURCES.md
# adoption_check → rows_present=5 (fixed; exit 1 only because --census was not run)
# round28_census → rows=81 malformed=0   vs live 82      (F4, silent under-count)
# fleet census   → rows=82, exit 0
```

Three measurement traps this exercise hit, recorded so the next seat does not repeat them:

1. **Filter on `E[0-9][0-9]`, not `E0[0-9]`.** `E11` does not match `E0[0-9]`; an `E0[0-9]` filter
   hides the dangling-`used-by` finding entirely. My first pass did exactly that and briefly
   recorded an absence that was a filter artifact.
2. **`--file` derives the lane root from the file's own location.** Copying `SOURCES.md` to a bare
   `/tmp/x.txt` makes every `used-by` path resolve against `/tmp` and fabricates ~100 `E11`s. Keep
   the file at `<root>/corpus/SOURCES.md` with `corpus/knowledge` and `corpus/lessons` present.
3. **Re-read the instrument, not just the tree.** `plans/adoption_check.py` changed at 03:50 while
   this review was running; a finding carried forward from a 20-minute-old read would have been
   reported as live when it was already fixed. Timestamps of every cited file are in the
   measurement-instant table at the top.

---

## 7. Residual risk and verification gaps

- **The 76-row baseline no longer exists in the lane.** §4's F1/F2/F6/F7 evidence is from a
  *reconstruction* (delete five rows, re-insert package bytes). It is faithful to the package bytes
  and to `gate-preappend.txt:1` (`registry=76`), but it is a reconstruction, not the historical tree.
- **Two findings were fixed mid-review (F3, F5) and I did not observe the change being authored.**
  I observed the *before* state (my probes against the earlier revision, quoted verbatim) and the
  *after* state (final tree). I cannot state who fixed them or that the fix was reviewed. If a
  reviewer disputes the before-state, the byte-level evidence is the probe output quoted in F3/F5,
  not a sha of the old file — the old file version is gone.
- **This report is pinned to 03:51:31 and the tree is moving.** S091 landed between two of my own
  measurements; if a reader runs §1 and sees 83, that is a new row, not a contradiction. Re-run §6
  step A and compare against the mtimes in §0.
- **I did not verify the five rows' located quotes, word counts, or digests.** Source re-openings
  are other seats' scope; I verified cell structure, index parity and census conformance only. The
  ≤25-word quote claims in `corpus/lessons/round-29.md` §Sources opened are unverified by this seat.
- **`census=ok` was measured through the counter** (`--census`, exit 0) and independently via
  `sources-census.sh validate` (exit 0). Both agree. I did not exercise the counter against a
  deliberately broken census, so its `census` field is verified only in the passing direction.
- **F4's probe uses a `/tmp` copy** with one row shifted; it demonstrates the parsers' disagreement
  and does not assert that any indented row exists on the live tree (none does — all 82 are column 0).
- No `lsp` semantic queries were used: the scope is Markdown tables and Python string parsing, where
  the authoritative evidence is the reproduced parser output above.

---

## 8. Bottom line for the L1

- Registry **82** rows under the census anchor, **82 unique**, **0 malformed**; ids S001–S080 then
  S090–S091, with S081–S089 deliberately unadmitted. Tiers **A76/B4/C2**, statuses
  **mined70/queued8/rejected4**.
- Knowledge parity **38/38 in both directions**; zero unindexed, zero dangling, zero duplicate rows;
  the new index row is `corpus/README.md:64` in canonical column-0 shape.
- All five staged rows parse as **exactly 11 cells** with **no literal or escaped pipe** — nothing to
  flag on the cell-count axis, as delivered or as landed.
- Both blocking cells are **discharged on the committed bytes**: the prose `recheck` (`E09` ×5) and
  S078's dangling `judge-calibration-thresholds.md` `used-by` (`E11`) each reproduce on the package
  bytes and are independent of one another (§4 F1/F2). The `E12` EOF hazard and the `opened`-date
  disagreement are also discharged.
- The frozen C1 target is met **verbatim**:
  `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0 —
  and the counter's internal checks got stricter, not weaker (F5).
- **Two items remain live and are worth a round-30 row:** `round28_census.py:40` still uses a
  column-0-only anchor and silently under-counts an indented row (F4, reproduced on the final tree),
  and the attempt-2 lesson's transition sentence still says 81 rows / A 75 against a measured
  82 / A 76 (F11, `corpus/lessons/round-29.md:205`). Neither can produce a false green today.
