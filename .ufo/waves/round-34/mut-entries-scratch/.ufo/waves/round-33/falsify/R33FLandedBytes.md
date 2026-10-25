# R33FLandedBytes — C1 staged quote bytes versus landed source-row identity

Seat: `KengakuR33.R33FLandedBytes` (leaf; no subagents spawned). Wave 36, round 33
(hyaku run 7), 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

Target: `.ufo/waves/round-33/assimilation/append-rows.md` S103/S104 rows vs
`corpus/SOURCES.md` S103/S104 rows. Question: are all gate-relevant
source/anchor/status/date/recheck/used-by cells byte-equivalent?

No tools installed (no installs/updates performed; `python3` present). No lane/fleet
files mutated; reads only. Report written to this path.

## Verdict

**NO — not all gate-relevant cells are byte-equivalent.** `source`, `kind`, `tier`,
`scope`, `status`, `opened`, `recheck`, `used-by` are byte-identical for both rows.
The **anchor** and **teaches** cells differ in both S103 and S104 (raw byte comparison,
below). The divergence is an annotation/gloss condensation, not a change to the located
quote substrings: every quoted substring is byte-identical (5/5 for S103, 3/3 for
S104), so the C1 kill-rule quote payload survives; the semantic claims are preserved in
condensed form.

## Evidence (exact commands and outputs)

### 1. Cell-by-cell byte comparison (raw, no whitespace normalization)

Command (lane root):

```
python3 - <<'EOF'
import re
def get_rows(path, ids):
    out={}
    for ln,line in enumerate(open(path,encoding='utf-8'),1):
        m=re.match(r'^\s*\| (S\d{3}) \|',line)
        if m and m.group(1) in ids: out[m.group(1)]=(ln,line.rstrip('\n'))
    return out
staged=get_rows('.ufo/waves/round-33/assimilation/append-rows.md',{'S103','S104'})
landed=get_rows('corpus/SOURCES.md',{'S103','S104'})
for rid in ('S103','S104'):
    sl=staged[rid][1]; ll=landed[rid][1]
    print(rid,'whole-line identical:', sl==ll, '| staged',len(sl.encode()),'landed',len(ll.encode()))
    sc=sl.split('|')[1:-1]; lc=ll.split('|')[1:-1]
    for h,a,b in zip(['id','source','kind','tier','scope','anchor','teaches','status','opened','recheck','used-by'],sc,lc):
        if a!=b: print('  RAW-DIFF',h,'| staged',len(a),'landed',len(b))
EOF
```

Output:

```
S103 whole-line identical: False | staged 1851 landed 1475
   RAW-DIFF anchor | staged 726 landed 515
   RAW-DIFF teaches | staged 441 landed 278
S104 whole-line identical: False | staged 1250 landed 1050
   RAW-DIFF anchor | staged 474 landed 428
   RAW-DIFF teaches | staged 331 landed 177
```

Cells verified byte-identical at raw level for both rows: id, source (269 chars S103 /
105 chars S104), kind, tier, scope (299 / 225), status (`mined`), opened
(`2026-10-25`), recheck (`180d`), used-by (`corpus/knowledge/benchmark-grader-semantics.md`,
46 chars).

### 2. Quote-substring preservation

All quoted strings in the anchors are byte-identical between staged and landed
(output: `quotes staged==landed: True | n staged 5 landed 5` for S103; `3/3` for S104).
The quoted strings therefore keep the ≤25-word property (the gate counts whitespace
tokens on the quote string itself; identical strings give identical counts).

### 3. What differs (S103 anchor)

Staged (724 chars in cell, 726 raw): `…main.py:58 "def validate_record_data(…)" (11
words; signature default, not executed); :279 "# Validate with 0.05% tolerance" (5 words)
and :280 "validate_record_data(…)" (3 words; the only call, so 0.05 is the executed
tolerance); :218 "return True  # Don't fail evaluation if we can't check logs" (11 words;
caught exceptions fail open); :234 "if not check_abtesting_logging_bucket_clean(…)" (4
words; absent credentials fall through to implicit None, which fails the task)`.

Landed (513 chars in cell, 515 raw): `…main.py:58 "def validate_record_data(…)" (11
words); :279 "# Validate with 0.05% tolerance" (5); :280 "validate_record_data(…)" (3);
:218 "return True  # Don't fail evaluation if we can't check logs" (11); :234 "if not
check_abtesting_logging_bucket_clean(…)" (4)`.

S103 teaches: staged `the benchmark scores by comparing a produced artefact against a
ground-truth artefact under a numeric tolerance fixed at the call site — 0.05 percentage
points per scenario, not the 0.1 signature default — so a grader's operative threshold
must be read from its invocation and not its declaration, and the same task's log-bucket
check fails open on caught exceptions while absent credentials fall through to implicit
None and fail the task` vs landed `scores a produced artifact against a ground-truth
artifact at a tolerance fixed at the call site — 0.05 percentage points per scenario, not
the 0.1 signature default; caught log-check exceptions fail open, while absent credentials
fall through to implicit None and fail closed`.

### 4. What differs (S104 anchor)

Staged: `…abs page:41 title "LLMs-as-Judges: …" (8 words; the survey's own spelling,
three Ls); :124 "This paper presents …" (20 words); :131 comments "60 pages, comprehensive
and continuously updated" (6 words)`.

Landed: `…abs page:41 title "LLMs-as-Judges: …" (8 words); :124 "This paper presents …"
(20 words); :131 "60 pages, comprehensive and continuously updated" (6 words)`.

S104 teaches: staged `the field's own survey separates meta-evaluation — how a judge
itself is scored — from methodology, so judge-based scoring owns a validation protocol a
deterministic grader does not need; the parts are quoted in the survey's own spelling
(LLMs-as-Judges in the title, LLMs-as-judges in the abstract), not the staged single-L
typo` vs landed `meta-evaluation — how a judge itself is scored — is separate from
methodology; the survey uses its own spelling, LLMs-as-Judges in the title and
LLMs-as-judges in the abstract`.

### 5. Provenance

- `append-rows.md` (2 lines) is committed; working tree equals the committed bytes
  (`diff` empty). It entered at `2b4cef2` (round-33 renumbered assimilation) and was
  re-committed at `b54feca` ("round-33: admitted grader semantics and re-probed
  catalogs") with `+2` lines.
- Landed `corpus/SOURCES.md:118-119` rows are identical from `b54feca` through `HEAD`
  (`git show HEAD:corpus/SOURCES.md | sed -n '118,119p'` == `git show
  b54feca:corpus/SOURCES.md | sed -n '118,119p'`).
- The staged and landed artifacts therefore disagree at the committed tip; no
  byte-level pin ties them.

## Findings by severity

1. **HIGH — staged ↔ landed byte identity is broken for both rows (anchor + teaches),
   and no counter/gate checks it.** The append step's own artifact
   (`append-rows.md`) is not the bytes that landed in `corpus/SOURCES.md`. The C1
   counters (`adoption_check.py`, `round33_c1_verify.py`) check registry cells against
   the entry and the expect file — not staged-vs-landed row equality — so this delta is
   uncaught by construction. Any future audit or tooling that compares the two artifacts
   (e.g., a re-run of the append against the committed staged rows) will observe the
   mismatch. Consequence: the landing is not byte-reproducible from the committed staged
   artifact; the edit was applied at integration (before/at `2b4cef2`/`b54feca`)
   without leaving a diff record.
2. **MEDIUM — the edited cells are exactly the gate-relevant cells the task names.**
   `anchor` is the kill-rule quote carrier and `teaches` is the cell the second counter
   intends to read (`R33C1Counter.md` finding 2: `round33_c1_verify.py:168` reads
   `row[5]`, i.e. **anchor**, not `row[6]` teaches). Because the landing rewrote both
   cells, a counter or verifier expecting the staged bytes would fail on them; because
   the counter reads the wrong index anyway, neither the staged nor the landed teaches
   text is actually verified.
3. **LOW — content preserved.** The located quote substrings are byte-identical
   (5/5, 3/3), so the C1 kill-rule quote payload and word counts are unaffected; the
   semantic claims (executed tolerance 0.05 vs signature default 0.1; fail-open vs
   fail-closed; meta-evaluation as a separate part; survey spelling `LLMs-as-Judges`)
   survive in condensed form. The frozen C1 predicate (entry file citations, rows
   present/mined, opened/used-by cells, index row, counter prints) is not falsified by
   these text deltas.

## Residual risk and verification gaps

- The exact commit where the anchor/teaches text was changed was not isolated (the
  working-tree rows already differed at `2b4cef2`; no intermediate artifact records the
  edit). The edit is observable only as staged-vs-landed divergence.
- `R33GateMutants.md` row 3 observed that re-running the quote gate against the *landed*
  rows exits 8 with the committed `url-map.json` while `append-rows.md` passed; that
  finding concerns source-cell URL granularity and is independent of — and consistent
  with — this byte divergence. (The landed S103 source cell at `HEAD` cites both repo
  root and pinned blob.)
- No counter reads `append-rows.md` against `corpus/SOURCES.md`, so staged bytes can
  drift indefinitely without any check failing.

## Verdict

`VERDICT: difference-found (anchor/teaches diverge; source/status/date/recheck/used-by
byte-identical; quotes preserved)` — the reported acceptance question ("are all
gate-relevant source/anchor/status/date/recheck/used-by cells byte-equivalent?") answers
**no**, scoped to anchor (and teaches) on both rows; consequence stated above.

## L1 integration resolution

After this seat's snapshot, the canonical `.ufo/waves/round-33/assimilation/append-rows.md` was synchronized to the exact landed S103/S104 rows (blob-only Toolathlon URL, version-pinned arXiv URL, final anchor/teaches cells). `append-block.md` was regenerated from those rows; `cmp` confirms append-rows, landed-rows, append-block are byte-identical, and the final gate receipt re-runs the quote check on the final rows (8/8 located, bound, exit 0). The earlier difference-found verdict describes the pre-synchronization state and is resolved at final integration.
