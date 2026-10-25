# R29a2RevCensus — census and index-parity conformance

Seat: reviewer (leaf). Round 29 attempt 2, 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: registry count under the census anchor, knowledge index parity in both directions, and the
five staged rows S077/S078/S079/S080/S090 from the package
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.

Read-only on the lane; scratch in `/tmp/r29a2-census-probe/` and `/tmp/r29a2-repro2/`. This seat
created, edited or deleted **no** production file. No tool installed or upgraded (none needed).

**Timing note that governs how to read this report.** Mid-review the lane advanced: the block
landed while I was measuring. The first measurement saw the pre-landing tree (**76** registry rows,
37 knowledge files); the tree now holds **81** rows and **38** files. Everything below is stated
twice where it matters: the *current* measurement (authoritative) and the *reconstructed
pre-landing baseline* (what the change was measured against). Where my earlier inference and the
landed facts disagree, §5 says so explicitly.

---

## 1. Registry count — current tree

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
→ 81
```

| Quantity | Value | Evidence |
|---|---|---|
| Registry rows under the 0–3-space anchor | **81** | command above |
| Pre-landing baseline (same anchor) | **76** | reconstructed by deleting the five landed rows: 76; also `gate-preappend.txt:1` `registry=76` |
| Distinct ids / duplicates | **81 / 0** | `sort \| uniq -c \| awk '$1>1'` → empty |
| id range | **S001–S080** then **S090**; max `S090` | id enumeration |
| Absent ids inside the range | **S081–S089** (9 ids) | `missing ids: S081,…,S089` |
| Malformed (≠11 cells) | **0** | `plans/round28_census.py` → `"malformed": 0` |
| Tier split | **A 75 / B 4 / C 2** (= 81) | same run |
| Status split | **mined 69 / queued 8 / rejected 4** (= 81) | same run |
| `## Registry` section | lines **19–100** (`## Paths` at 100) | `grep -n '^## ' corpus/SOURCES.md` |
| Landed rows | lines **100–104** | five rows, column 0 |

The **S081–S089 gap is expected, not a defect**: those ids are staged package rows the round
deliberately did not admit (`corpus/lessons/round-29.md:175`, Gate row "remaining 168 staged rows
and 64 staged entries | reject this round"). Do not read "81 rows" as "S001–S081"; the registry is
contiguous only over S001–S080.

Full census, three sub-gates green:

```
python3 plans/round28_census.py --revision live-check
→ sources: {"rows":81,"malformed":0,"statuses":{"mined":69,"queued":8,"rejected":4},
             "tiers":{"A":75,"B":4,"C":2}}
→ knowledge: {"files":38,"index_rows":38,"unindexed":[],"dangling":[],"duplicate_rows":[]}
→ c1_exit=0  c2_exit=0  state_exit=0

scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku-shokunin
→ kengaku-shokunin	ok	.../corpus/SOURCES.md        (exit 0; W04 duplicate-url warnings only)
```

---

## 2. Knowledge index parity — both directions

| Direction | Pre-landing | **Current** |
|---|---|---|
| Files on disk → has a `corpus/README.md` index row | 37 / 37 | **38 / 38** |
| README index rows → file exists on disk | 37 / 37 | **38 / 38** |
| Unindexed | none | **none** |
| Dangling | none | **none** |
| Duplicate index rows | 0 | **0** |
| Index rows at 1–3 leading spaces | 0 | **0** (all 38 at column 0) |

```
find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l   → 38
grep -cE '^ {0,3}\|[[:space:]]*`knowledge/' corpus/README.md      → 38
```

**Parity is exact in both directions.** The new entry's index row is `corpus/README.md:64`, at
column 0, in the canonical shape `| `knowledge/<name>.md` | … |` — it satisfies both index
predicates in play (see F8), and the frontier lines at `:240` and `:262` were updated in the same
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
pipe, so all four lane parsers (column-0, 0–3, `NF==13`, `body[1:-1].split("|")`) read them as 11
cells. Confirmed on the committed bytes:

```
line 100 S077 cells=11 literal/escaped pipe=False
line 101 S078 cells=11 ...
line 102 S079 cells=11 ...
line 103 S080 cells=11 ...
line 104 S090 cells=11 ...
```

### Landed cell content (all five conform)

| Row | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|
| S077 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S078 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S079 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S080 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |
| S090 | `A` | `mined` | `2026-10-25` | `2026-10-25` | `corpus/knowledge/benchmark-task-validity-checklist.md` |

### Package cell content (what a verbatim append would have carried)

All five carried `opened = 2026-10-23`, a prose `recheck`
`2026-10-23 — re-verify at the next upstream release (Gate S0NN)`, and S078 additionally named
`corpus/knowledge/judge-calibration-thresholds.md`. These are the substance of F1/F2 below.

---

## 4. Findings

Each finding states what is true **now**. Where a defect existed in the delivered package and is
resolved on the committed tree, it is marked **DISCHARGED** with the reproduction that proves it was
real — so that a later reader does not have to take the discharge on faith, and so the gate's value
is documented.

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

Why it fires: `symbolic()` is `^[A-Za-z][A-Za-z0-9 _-]*$`, so a cell beginning with a digit is
neither an ISO date nor `<N>d` nor symbolic. It was also an outlier: of the 76 baseline rows,
`recheck` was ISO 32 / `<N>d` 27 / symbolic 22 (`on-release`) / **prose 0**.

**Now:** landed `recheck = 2026-10-25` on all five; the live census validates `ok`, exit 0.

### F2 — DISCHARGED (was HIGH/blocking): S078's `used-by` named a non-existent entry

The package's S078 cell was `corpus/knowledge/benchmark-task-validity-checklist.md,
corpus/knowledge/judge-calibration-thresholds.md`; the second path has never existed in
`corpus/knowledge/` (the lane holds `llm-judge-calibration.md`, a different entry). On the
reconstructed verbatim append:

```
file	E11	S078 missing used-by corpus/knowledge/judge-calibration-thresholds.md
```

F1 and F2 were **independent** — normalizing only `recheck` still fails on `E11` alone:

| Variant | Result | Exit |
|---|---|---|
| V1 package bytes verbatim | `E09` ×5 **+** `E11` S078 | 1 |
| V2 `recheck` normalized only | `E11` S078 **only** | 1 |
| V3 `recheck` + `used-by` normalized | `ok` | 0 |

**Now:** landed `used-by` is exactly `corpus/knowledge/benchmark-task-validity-checklist.md`; `ok`.

### F3 — LIVE, MEDIUM: `plans/adoption_check.py` silently drops every indented registry row

`plans/adoption_check.py:33` matches a 0–3-space anchor but `:44` splits cells with
`raw.rstrip()[1:-1].split("|")`, which assumes column 0. For an indented row the first `[1:-1]`
slice consumes the indent instead of the leading `|`, yielding 12 cells and hitting the `continue`
at `:45`: matched, then discarded.

Reproduced against the **current** file, with only `S077` shifted one space left inside the live
registry:

```
python3 plans/adoption_check.py --lane /tmp/r29a2-census-probe/live-ind \
        --expect .ufo/waves/round-29/attempt2/adoption-expect.json
→ entries=1 indexed=1 cited_rows=5 rows_present=4 rows_mined=4 usedby_ok=1 verified_at=1 census=skipped
→ exit 1
```

The fleet census reads the same bytes as clean (81 rows, `validate ok`, exit 0). So the two
instruments disagree on identical input. It is fail-closed (under-counts; never a false green), and
the five landed rows are column 0 so C1 is unaffected — but `ROW_RE`'s 0–3 clause is not
load-bearing as written. `plans/sources_adopt.py:71,74` does this correctly
(`body = stripped.strip()` then `body[1:-1].split("|")`); that is the two-line fix.

### F4 — LIVE, MEDIUM: the "census parser's own 0–3 anchor" is not in `plans/round28_census.py`

`plans/round28_census.py:40` is `re.match(r"^\|\s*S[0-9]{3,}\s*\|", line)` — **column 0 only**. The
0–3 anchor lives in `plans/sources_adopt.py:33` and in `scripts/sources-census.sh`. Consequence on
the same one-space shift, current tree:

```
python3 plans/round28_census.py --root <1-space-indented copy> --revision probe  → rows=80 malformed=0
python3 plans/round28_census.py --revision probe (live tree)                    → rows=81
```

The row vanishes with **no** malformed-count increase — a silent under-count, not a rejected row.
Four parsers in the lane therefore hold four different notions of "a registry row"
(`round28_census.py` column 0; `sources_adopt.py` 0–3 correct; `adoption_check.py` 0–3 match with
column-0 split; `sources-census.sh` 0–3 with `NF==13`). They agree at 81 today only because every
row is column 0. If C2's justification cites "the census parser's own anchor", it must name
`sources_adopt.py` / `sources-census.sh`, not `round28_census.py`.

### F5 — LIVE, LOW: the frozen C1 target line omits the `verified_at=` field the tool prints

C1 (frozen, `plans/round-29-attempt2-claims.md`) requires `adoption_check.py` to print exactly

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

The live run prints one extra field:

```
python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
→ entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
→ exit 0
```

`.ufo/waves/round-29/attempt2/adoption-measured.txt` records exactly this longer line. A literal
diff against the frozen text fails on the inserted `verified_at=1 `. `verified_at` is a
*strengthening* (it is what proves each entry's `verified-at: 2026-10-25`), so the claim text is the
stale side: report the measured line and say the frozen line omits a field. Do not "fix" this by
deleting the counter's check.

### F6 — DISCHARGED (was LOW): an end-of-file append is `E12`-invalid

Appending the block at EOF instead of inside `## Registry` (lines 19–100) yields
`E12 S077 … S090 row outside Registry section` ×5, exit 1. The landed rows are at lines 100–104,
before `## Paths`: correct.

### F7 — DISCHARGED (was LOW): `opened` disagreed with the claimed access date

Package rows carried `opened = 2026-10-23` while C1 asserts 2026-10-25 re-grounding. Landed rows
carry `opened = 2026-10-25`, matching the entry's `verified-at: 2026-10-25`.

### F8 — INFO: two index predicates disagree on row shape; the landed row satisfies both

| Row shape | `round28_census.py:43` ``^\|\s*`(knowledge/…)`\s*\|`` | `adoption_check.py:76` substring ``| `knowledge/<name>` |`` |
|---|---|---|
| `\| \`knowledge/x.md\` \| … \|` | counts | counts |
| indented 2 spaces | does **not** count | counts |
| `\|\`knowledge/x.md\`\|` (no space) | counts | does **not** count |
| 2 spaces after the filename | counts | does **not** count |

`corpus/README.md:64` is the first shape, so both agree (verified: census `index_rows=38`, new entry
counted `True`; adoption substring `True`). The disagreement is fail-closed in both directions, so
it costs a diagnosis round rather than producing a false green. Keep authoring index rows in the
canonical shape.

### F9 — INFO: `plans/registry_check.py` cannot see any of this round's rows

`plans/registry_check.py:13` pins the population to `plans/fixtures/r28/registry/population.json`:
**13 source ids, S038–S060**, and **35** knowledge paths. `parse_registry` skips ids outside
`population["source_ids"]` (`:42`), and `check` only walks `population["knowledge_paths"]` (`:57`).
S077–S080, S090 and `benchmark-task-validity-checklist.md` are outside it by construction. So a
green `registry_check.py` is **not** evidence about this round's links — the fleet census (`E09`/
`E11`) is the only instrument that reads them. (This is also why the F1/F2 defects would not have
been caught by the lane's own frozen gate.)

### F10 — INFO: the five requested rows are not the only malformed rows in the package

Scoped to the five, nothing is malformed. For the record, the same 175-row package carries escaped
pipes that do break the 11-cell clause — a hazard only if a tool ever stages the whole file as one
block:

| Row | Package line | Raw parts | Cells | Escaped text |
|---|---|---|---|---|
| S093 | 23 | 14 | **12** | `fail_to_pass \| pass_to_pass` |
| S101 | 31 | 17 | **15** | `git apply … \|\| git apply --3way … \|\| patch --fuzz=3 …` |

`plans/sources_adopt.py`'s `split_cells` correctly refuses these (`escaped-pipe`; selftest
`CASE escaped-pipe-refused PASS`). `corpus/lessons/round-29.md:174` records the same two rows and
counts the 171 prose `recheck` cells they carry.

---

## 5. Observations that are documented decisions, not findings

Stated here because a reviewer scanning the numbers will otherwise ask about them.

**S090 tier `B` → `A`.** The package graded S090 `B` with an in-cell reason ("tier B because the
page carries no visible publication date"). Landed is `A`. This is **documented and reasoned** at
`corpus/lessons/round-29.md` §Attempt 2, Cell transitions (`:194-197`):

> S090 enters tier **A**, not the package's B: SOURCES-contract tier B is "strong secondary", and a
> first-party release announcement is a maintainer statement (tier A). The package's stated reason
> — no visible publication date — is page-scoped only, because the publisher's own index dates the
> post. … Registry 76 → 81 rows; tiers A 70 → 75, B 4 → 4, C 2 → 2.

That prediction matches measurement exactly (A 75 / B 4 / C 2, 81 rows), and the landed anchor cell
carries the supporting evidence ("the publisher's news index dates this post 2025-11-07"). **My own
earlier inference was wrong here**: extrapolating from the package's tier cells I predicted
A 74 / B 5 / C 2. The promotion is the correct reading, not a silent cell edit — but it is only
correct *because* the date objection was falsified, so a later reader should check the anchor cell's
date claim, not just the tier letter. Whether an index-page date suffices for tier A is a judgment
for the claim critic, not this seat.

**`adopt-block.md` is not what landed, for 3 of 5 rows.** `.ufo/waves/round-29/attempt2/adopt-block.md`
matches the committed rows byte-for-byte for S077 and S078, and differs for S079/S080/S090 — in the
`anchor` cell only (line-number corrections, quote re-boundaries). Cause is recorded as M97 at
`corpus/lessons/round-29.md:166`: `build_block` rewrites only `status`/`recheck`/`used-by`/`opened`, so
entry-side corrections did not propagate; the round's own rule is "correct the entry first, then
rebuild the block". The registry is the authoritative surface; the block file is a pre-correction
snapshot. Re-running the gate against the package now correctly reports the ids as collisions
(`gate-postappend-rerun.txt`: `registry=81 collisions=5`), which is the gate working as designed.

**`build-validation.txt` is 0 bytes.** `.ufo/waves/round-29/attempt2/build-validation.txt` is empty
(0 bytes, mtime 03:40) and is referenced by no `*.json` receipt in that directory. The build's
validation evidence lives in `corpus/evidence/round29-attempt2/` instead. An empty file whose name
promises validation is a trap for a later reader; delete it or fill it.

---

## 6. Reproduction

Every number above is reproducible from the current tree with no lane writes. This script was run
end-to-end; the outputs quoted in §3–§4 come from it.

```bash
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
P=/tmp/r29a2-repro2; rm -rf "$P"; mkdir -p "$P"

# A. census + parity + counter (current tree)
cd "$LANE"
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md          # 81
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
```

The F3/F4 parser probes are separate and smaller — shift one landed row by a single leading space
(still inside the 0–3 census clause) and compare the three instruments on identical bytes:

```bash
P=/tmp/r29a2-ind; rm -rf $P; mkdir -p $P/corpus
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
cp corpus/SOURCES.md corpus/README.md $P/corpus/; cp -r corpus/knowledge corpus/lessons plans $P/corpus/
python3 - "$P/corpus/SOURCES.md" <<'PY3'
import re,sys
p=sys.argv[1]; out=[]
for l in open(p).read().splitlines():
    if re.match(r"^\|\s*S077\s*\|", l): l=" "+l      # one leading space
    out.append(l)
open(p,'w').write("\n".join(out)+"\n")
PY3
python3 plans/adoption_check.py  --lane $P --expect .ufo/waves/round-29/attempt2/adoption-expect.json
python3 plans/round28_census.py  --root $P --revision ind
scripts/sources-census.sh census --file $P/corpus/SOURCES.md
# adoption_check → rows_present=4, exit 1   (F3)
# round28_census → rows=80 malformed=0      (F4)
# fleet census   → rows=81, exit 0          (neither parser's behaviour)
```

Two measurement traps this exercise hit, recorded so the next seat does not repeat them:

1. **Filter on `E[0-9][0-9]`, not `E0[0-9]`.** `E11` does not match `E0[0-9]`; a `E0[0-9]` filter
   hides the dangling-`used-by` finding entirely. My first pass did exactly that and briefly
   reported an unfiltered absence.
2. **`--file` derives the lane root from the file's own location.** Copying `SOURCES.md` to a bare
   `/tmp/x.txt` makes every `used-by` path resolve against `/tmp` and fabricates ~100 `E11`s. Keep
   the file at `<root>/corpus/SOURCES.md` with `corpus/knowledge` and `corpus/lessons` present.

---

## 7. Residual risk and verification gaps

- **The 76-row baseline no longer exists in the lane.** §4's F1/F2/F6/F7 evidence is from a
  *reconstruction* (delete five rows, re-insert package bytes). It is faithful to the package bytes
  and to `gate-preappend.txt:1` (`registry=76`), but it is a reconstruction, not the historical tree.
- **I did not verify the five rows' located quotes or digests.** Source re-openings, quote
  boundaries and sha256s are other seats' scope; I verified cell structure, index parity and census
  conformance only. The ≤25-word quote claims in `corpus/lessons/round-29.md` §Sources opened are
  unverified by this seat.
- **`census=ok` on the live tree was measured through the counter** (`--census`, exit 0) and
  independently via `sources-census.sh validate` (exit 0). Both agree. I did not exercise the counter
  against a deliberately broken census.
- **F3/F4 indentation probes use a /tmp copy** with one row shifted; they demonstrate the parsers'
  disagreement, and they do not assert that any indented row exists on the live tree (none does —
  all 81 rows are column 0).
- No `lsp` semantic queries were used: the scope is Markdown tables and Python string parsing, where
  the authoritative evidence is the reproduced parser output above.

---

## 8. Bottom line for the L1

- Registry **81** rows under the census anchor, **81 unique**, **0 malformed**; ids S001–S080 then
  S090, with S081–S089 deliberately unadmitted. Tiers **A75/B4/C2**, statuses **mined69/queued8/rejected4**.
- Knowledge parity **38/38 in both directions**; zero unindexed, zero dangling, zero duplicate rows;
  the new index row is `corpus/README.md:64` in canonical shape.
- All five staged rows parse as **exactly 11 cells** with **no literal or escaped pipe** — nothing to
  flag on the cell-count axis, as delivered or as landed.
- The two cells that were blocking **are discharged on the committed bytes**: `recheck` prose
  (`E09` ×5) and S078's dangling `judge-calibration-thresholds.md` `used-by` (`E11`) both reproduce
  on the package bytes and both read clean once normalized — proven independent (§4 F1/F2).
- Frozen C1 target is met; the measured line carries one extra field, `verified_at=1`, that the
  frozen text omits (§4 F5). Quote the measured line.
- Two parser defects remain live and are worth a round-30 row: `adoption_check.py`'s indented-row
  drop (§4 F3) and `round28_census.py`'s column-0-only anchor (§4 F4). Both under-count silently;
  neither can produce a false green today.
