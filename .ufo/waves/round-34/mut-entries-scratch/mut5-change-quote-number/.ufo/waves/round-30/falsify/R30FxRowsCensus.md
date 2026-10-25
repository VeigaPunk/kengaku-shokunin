# R30FxRowsCensus — registry schema and census re-run on the landed rows S081–S086

Seat: `L1Kengaku30.R30FxRowsCensus-3` (leaf `scout`, round-30 falsify wave, hyaku run 6, 2026-10-25).
writer: L1Kengaku30.R30FxRowsCensus-3
Item: **re-run the fleet census both ways on the landed tree, then re-check the six new rows cell by
cell** — 11 cells, no literal or escaped `|`, tier defensible against SOURCES-CONTRACT-v1,
`status=mined`, `opened=2026-10-25`, `recheck=180d`, `used-by` exactly the admitted entry, no
duplicate URL inside scope.
Bounds honoured: no subagent, no background job, no lane edit (this report is the only lane write),
read-only on `shokuknow` and the fleet repo, PACMAN untouched.

Candidate path: `corpus/knowledge/contamination-transparency-card.md`

## 0. What was measured, and on which bytes

`corpus/SOURCES.md` moved **three times while this seat measured** (siblings are editing it live):

| snapshot | time (2026-10-25) | `corpus/SOURCES.md` sha256 | observed change |
|---|---|---|---|
| A | 07:36Z (first runs) | not captured before the first edit | output identical to the pinned run below |
| B | 07:41:12Z | `43d3e37ed669a1769cbc1c751f8c9b267c3430b5eea26acb02d17eac4bb94284` | S081 scope/teaches, S084 teaches, S086 CJK count |
| C | 07:42:05Z | `ffb4165b244823b570c2aadcb1d54434deb46505dee0fd86eb353943f089259c` | S082 source title |
| D (pinned) | 07:43:12Z | `094e5c1820575643290c5721616d5439603619f8b21f2e1631b1181b3a78e92b` | S083 anchor hyphen note |
| E (post-report check) | 07:47Z | `cf58f52b0affae3af9a875e5957e2135e857055aeb1e8072775f5641e39d99e1` | S085 anchor p.32 proviso ("crosses three typeset lines") |

Fourth move: after this report was drafted the file advanced to **E**. Re-running both census
commands on E produced output **byte-identical** to §1 (both exit 0), and a cell diff of S081–S086
between D and E touched exactly one cell — S085 `anchor`, which gained a locatability proviso and no
new cell, status or count. Every table in §3–§4 therefore holds on E as written.

Every count below is from **D** (`/tmp/r30fx-RowsCensus/final-snap.md`, copy byte-identical to the
lane file, sha re-checked before and after both runs), with the §3/§4 tables re-verified on **E**;
C/D were stable across the two census runs.
Consequence for the wave: sibling reports that pin `1be35142…` or `43d3e37…`
(e.g. `falsify/R30FxQuotes.md` §snapshots) now name bytes that no longer exist in the tree; their
per-row counts still hold on D and E (re-measured here, §3), but their hashes are stale.

Tools: `bash`, `gawk`, `python3`, `npx -y marked@18.1.1` (npm cache only, nothing added to `PATH`;
used for the GFM table-membership check in §5-F1), `curl`-free reads through the harness for the two
arXiv fetches. **Nothing was installed or upgraded.**

## 1. The two census runs, verbatim

Root-scoped run (lane discovered from `shokunin.conf`/`*-shokunin`):

```
$ sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
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
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
**EXIT=0**
```

File-scoped run on the exact file the claim cites:

```
$ sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
**EXIT=0**
```

Reading of the two runs (observed, not inferred):

- **Both exit 0.** No `E01`–`E12` and no `W01`–`W03` on any row; the only findings are 14 `W04`
  cross-scope duplicate URLs, all pre-existing rows (S040, S048, S057–S059, S064–S069, S071,
  S075–S076). W-codes do not change status by design (`scripts/sources-census.sh:17-18,31-33`).
- **None of the 14 warnings names S081–S086.** The six new rows emit no code at all in either run.
- Run A (pre-drift tree) produced byte-identical output to the pinned run D, so the drift in §0
  did not change any census verdict.
- `E01` requires `NF==13` (= 11 cells) and silently `continue`s on a short row; `E09` accepts
  `^[0-9]+d$`; `E11` checks each `used-by` path exists under the lane. All six rows clear those
  three by construction of the checks in §3.

## 2. Registry census numbers on snapshot D

| quantity | value | how |
|---|---|---|
| rows in `## Registry` | **88** | `^\| S[0-9]{3,} \|` over the file |
| distinct ids / duplicate ids | 88 / **0** | set vs count |
| id range, with gaps | S001–S086 plus S090–S091; **S087–S089 absent**, and physical order is S001…S080, S090, S091, **S081–S086** | line map §5-F1 |
| tiers | **A 79 / B 7 / C 2** | cell 4 |
| statuses | **mined 76 / queued 8 / rejected 4** | cell 8 |
| duplicate-URL groups (any scope) | 13 non-empty groups, all pre-existing; **0** involving S081–S086 | independent re-implementation of the census `url_of()` (strip fragment, trailing `/`, scheme; lowercase host) |

The claim "88 rows total" is true of the file; it is **not** a contiguous S001–S088 — see F1/F2.

## 3. Per-row cell table (snapshot D, lines 107–112)

`cells` = 11 and `|`-free were checked on the raw line (`"\\|" in line` false; splitting on `|`
yields exactly 13 fields, so no literal pipe can hide inside a cell). `dup URL` uses the census
normalisation against **all 88 rows** (W04-wide, stricter than the assigned within-scope check).

| id | cells | pipe-free | kind | tier | status | opened | recheck | used-by | dup URL | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| S081 | 11 | yes | paper | B | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS (tier note T1, scope clause F3) |
| S082 | 11 | yes | paper | B | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS (tier note T1, anchor tail F3b) |
| S083 | 11 | yes | paper | A | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS |
| S084 | 11 | yes | docs | A | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS (pin note F4) |
| S085 | 11 | yes | docs | B | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS (tier note T2) |
| S086 | 11 | yes | paper | A | mined | 2026-10-25 | 180d | `corpus/knowledge/contamination-transparency-card.md` | none | PASS |

Every assigned predicate is satisfied: 11 cells, no literal or escaped pipe, `status=mined` for all
six, `opened=2026-10-25` (not future → E08 silent), `recheck=180d` (cadence form → E09 silent and
`overdue` would due them 2027-04-23), `used-by` is exactly the one admitted entry (not a list, no
em-dash → E11 and W03 silent), and each row's URL is unique across the registry.

Anchor quote widths on the landed bytes (the staged S081 30-word quote that
`build/R30RevRows.md` blocked is **repaired**):

| id | quoted spans (whitespace words / CJK tokens) | over 25? |
|---|---|---|
| S081 | 22 · 6 · 18 | no |
| S082 | 11 · 17 | no |
| S083 | 14 · 19 | no |
| S084 | 3 · 7 · 1 (CJK; 1 token = one 23-character sentence) | no |
| S085 | 3 · 1 (CJK, inner quotes fullwidth, pairing intact) | no |
| S086 | 3 tokens (title) + 1 token / 30 CJK characters (caveat) | no |

Identity check against the staged package (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`
lines 11–16): **same six titles and URLs**, same tiers (B, B, A, A, B, A), same `kind`. The landed
rows differ only where the gate normalises — `opened` 2026-10-23 → 2026-10-25, prose `recheck` →
`180d`, `used-by` two paths → the one admitted entry — plus this round's content repairs (S081
scope/teaches, S082 title, S083 hyphen note). No tier cell was re-derived this round; all six are
inherited from the 2026-10-23 stage (see T1/T2).

## 4. Tier against the contract

Contract text (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-30`, restated
in `corpus/SOURCES.md:11-15`): **A** = primary or authoritative *for that scope* (spec, official docs,
source code, original paper, maintainer statement, own gate output); **B** = strong secondary
(expert write-up with reproducible detail, survey, textbook); **C** = lead only; `community` never A;
tier is scoped, never global.

| id | tier | contract reading | defensible? |
|---|---|---|---|
| S081 | B | scope is "the preprint's own argument" — the paper's own text, i.e. the contract's *original paper*/primary clause | **Conservatively defensible, not the letter.** It is one of only **two arXiv rows at B**; the other **21** arXiv rows are A (S002, S003, S004, S007, S008, S009, S010, S012, S013, S015, S016, S018, S019, S020, S021, S022, S035, S040, S044, S057, S091). No inflation (Q2 satisfied), so no admission harm. |
| S082 | B | same construction, scope even says "not peer reviewed" | same as S081: conservative, off-precedent |
| S083 | A | peer-reviewed paper for its own design claim (Findings of EACL 2026) | **yes** |
| S084 | A | vendor's official docs for its own two documented procedures | **yes** |
| S085 | B | B requires "reproducible detail"; the scope itself says "no document number, measurements or data release" | **weakest of the six.** Neither clause fits cleanly: A would need treating a sponsoring body's self-description as a maintainer statement; B claims a property the row simultaneously denies. No inflation. |
| S086 | A | peer-reviewed proceedings paper for its own method and caveat | **yes** |

T1 — the six tier cells are **staged values carried through unchanged**; the round's own lesson
records them as Q2 support (`corpus/lessons/round-30.md:42-43`) without noting the inheritance. In a
registry where 21 arXiv rows sit at A, two arXiv preprints at B is a curation choice a later seat
must not silently "fix" upward without re-reading them; either way it is not a defect that refuses a
row.

## 5. Findings (ordered by what a later seat must act on)

**F1 — the six rows are not inside the rendered registry table (shape defect, census-invisible).**
The registry is split by two blank lines that pre-exist this append (identical at HEAD,
`git show HEAD:corpus/SOURCES.md` sha `e18b32d9…`):

```
98  row S076      ← last row of the only real table
99  BLANK
100 row S077   101 S078   102 S079   103 S080   104 S090
105 BLANK
106 row S091      ← round 29
107 row S081   108 S082   109 S083   110 S084   111 S085   112 S086   ← this append
113 ## Paths
```

Rendered with `marked@18.1.1`: **one `<table>`, 76 `<td>` ids, S001–S076**. S077–S080, S090, S091
and all six new rows render as **paragraphs**, not table rows (a GFM table needs a header row plus a
delimiter row; block C at line 106 has neither). Neither checker sees this: the census keeps
`in_registry` true across blank lines and only counts cells (`sources-census.sh:611-636`), and
`plans/sources_adopt.py` checks id collision and cell schema only (`:10-27`). So "registry schema
passes" is true textually and false visually; the file has 7 of its 88 rows outside its table.
Fix is one line (delete the blank lines at 99 and 105) or landing the block before line 99. Severity:
documentation, not predicate — C1 and the census are unaffected.

**F2 — S081–S086 are reserved staged ids, not "the next unused".** Contract: `id` — "the next
unused; never reused" (`SOURCES-CONTRACT-v1.md:22`); the next unused after S091 is **S092**. The six
ids are the stage's own allocation for this candidate (`SOURCES.append.md:11-16`) and were named in
round 29's Gate row `contamination-transparency-card.md (S081–S086) | reject this round`
(`corpus/lessons/round-29.md:180`), with S087–S089 still reserved for the refused CJK-eval rows
(`SOURCES.append.md:17-19`). Because the identity is the *same six sources*, this is **not id reuse**
— the append is correct and the frozen claim mandates these ids — but `build/R30RevRows.md:43`
("S081–S086 are the next unused ids") is the wrong grounding: a later round applying the contract
literally would allocate S092+ and skip the reserved block. The right rule is "resume the staged
block, or max(live)+1, whichever the freeze names", and it should be written where ids are allocated.

**F3 — two landed cell clauses are falsified by this round's own fetches.**
1. S081 `scope` tail: "its JSON schema, validator and regeneration field sit in the full text, not
   on the cited abstract page". The cited abs page (`https://arxiv.org/abs/2608.29463`, fetched
   2026-10-25) reads: *"We operationalize it as a four-field disclosure protocol in which "unknown"
   is a valid entry, released under CC BY 4.0 with a JSON Schema, a validator, and worked
   examples."* The **schema and validator are on the cited page**; only the regeneration field is
   absent. The repaired sentence over-corrects the staged 30-word defect.
2. S082 `anchor` tail: "the abs page for 2607.01254 carries neither phrase". The abs text carries the
   first phrase as a mid-sentence clause: *"…while item-level transparency and procedural
   transparency have opposite effects on benchmark validity."* Only the sentence-initial capital
   (and the second, §8.2 phrasing) is absent. The anchor's two quotes themselves do resolve where it
   says: §7.3 is headed "Governance Design: Protected Items and Procedural Transparency" with the
   quoted sentence verbatim, §8.2 is "Mandatory Transparency in Benchmark Design and Deployment"
   with the second quote verbatim (both fetched 2026-10-25).

Both are single-clause accuracy defects in `scope`/`anchor`; neither touches a quoted span, so
neither trips C1's kill rule. They must be corrected as new text (no id change) because a later seat
will re-use that clause as a location claim.

**F4 — S084 is the registry's only floating pin, and it is tier A.** `doc.opencompass.org.cn/zh_CN/latest/…`
— the sole `/latest/` URL among 88 rows; every other row carries a version, commit, date path or DOI.
Its anchor leans on raw html line numbers (344, 397, 315) that will move when 0.4.0 is superseded;
"OpenCompass 0.4.0" appears in the title and scope but not in the URL. The contract's anchor clause
("exact section/page/line plus revision … never a bare homepage") is satisfied only through the
title, and the 180d recheck will re-measure a different page. Not a census failure and not a refusal;
recorded so the recheck seat pins a versioned URL next.

**F5 — `used-by` is exact per the gate and C1, incomplete per the contract.** All six cells name
exactly `corpus/knowledge/contamination-transparency-card.md` (the assigned check passes:
`entries=1` semantics, no dangling path, W03 silent). But the contract defines `used-by` as "the
knowledge entries **or lessons** citing the row" (`SOURCES-CONTRACT-v1.md:40`), and `corpus/lessons/round-30.md:67-72` cites all
six; S005/S006/S076/S091 already list lessons there. So the cells satisfy the gate's rule 3
("rewritten to exactly the admitted entries") and the frozen predicate while omitting
`corpus/lessons/round-30.md`. This is a real contract/gate tension, not a row error — the gate wins
while the predicate is frozen; the contract sentence should say so.

**F6 — live-tree drift during the audit.** Three writes in 93 seconds (§0). S082's source **title
changed under this seat** (staged "…Evaluation Economics and Benchmark Governance" → landed
"…Evaluation Scarcity, and the Political Economy of AI Capability Measurement"); the landed title is
confirmed correct against the arXiv API and the HTML `<title>`, so the change was a repair. Sibling
falsify reports pinning `1be35142…`/`43d3e37…` are now describing superseded bytes; the six-row
counts in `R30FxQuotes.md` still reproduce on D.

## 6. What this seat did not verify

- Quote relocation for S083–S086: read from landed cells only. The fresh fetches I made are S081
  (all three spans present) and S082 (§7.3 and §8.2 sentences present, headings confirmed). Per-source
  re-read seats `R30FxSrcS083`–`R30FxSrcS086` own the other four.
- The `html line 344/397/315` and `§7.3 line 855 / §8.2 line 901` **line numbers**: the harness
  reader returns extracted text, whose line numbering differs from the raw HTML (S082's §7.3
  sentence landed at artifact line 378). The section anchors are confirmed; the integers are not
  reproducible through this reader.
- Whether the S084/S085/S086 hosts answer 200 today: not fetched here (S085's CAICT host was
  reported HTTP 000 on a first fetch in round 29 and was re-opened by another seat this round).
- Nothing in `plans/round30_defects.py` or `plans/sources_adopt.py` was executed by this seat; C2/C3
  are other items. This report adds no state to the lane beyond itself.

## 7. Verdict

No row among S081–S086 should have been withheld: each satisfies every assigned census/cell
predicate on snapshot `094e5c18…`, each is the same source the round-29 Gate reserved under that id,
each URL is unique in the registry, and the landed quote widths are within the ≤25-word bar. The
append's defects are **placement** (F1: six rows, with S077–S080/S090/S091, sit outside the rendered
table), **one stale id rationale** (F2), **two falsified single clauses** (F3: S081 `scope`, S082
`anchor`), and **three weaker tier/pin cells** (S081/S082 B off-precedent, S085's B unsupported by
its own scope prose, S084's `/latest/` pin) that are curation calls rather than failures.

VERDICT: PASS — S081–S086 all pass the registry/census cell audit (11 cells, pipe-free, mined, opened 2026-10-25, recheck 180d, used-by exact, no duplicate URL); defects F1–F5 are cell/shape-level and refuse no row
