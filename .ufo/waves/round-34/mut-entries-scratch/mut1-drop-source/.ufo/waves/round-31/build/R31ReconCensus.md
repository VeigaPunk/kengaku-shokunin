# R31ReconCensus — round-31 round-start census, frozen commands run verbatim

Seat: `L1Kengaku31.R31ReconCensus` (leaf: no spawns, no background jobs, no `ask`).
Read-only: nothing under the lane repo was created, edited or deleted except this file. Every
command was run from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (the lane root the census
block names). Scratch: `/tmp/r31-R31ReconCensus/` (`run.sh`, `manual-census.txt`, `validate.txt`,
`ids.txt`, `dups.txt`, `usedby.txt`, `r30-quoted.txt`, `r30-w04.txt`) — 24 KiB, nothing deleted
outside it.
**Tool installs/upgrades: none.** bash, gawk, grep, coreutils, git and python3 were already
present; PACMAN is paused host-wide and no `uv tool` / npx / binary install was needed.

## 0. State measured (before any wave seat wrote)

| item | reading |
|---|---|
| lane HEAD | `0883e72ef8474ca42ac1a54eb0273079f1507035` (`round-30 verifier spot-check (integrator, hyaku): non-author admit/reject`) |
| `corpus/SOURCES.md` vs HEAD | clean (`git status --porcelain -- corpus/SOURCES.md` prints nothing) |
| registry blob / sha256 / lines | `3407b78890f65c132a0c9471515f4513b2646d49` / `dec033bf982cce1fb8852703647ad38165c128b06fdab0ee2a56036162fcb5c3` / 142 |
| worktree drift present (siblings', not mine) | `M .ufo/waves/round-30/build/R30DraftGate.md`, `M …/R30RevLesson.md`, `M .ufo/waves/round-30/falsify/R30FxCoverageAxis.md`, `M …/R30FxEntryCompleteSet.md`, `M …/R30FxEntryQ4Q6.md`, `M plans/sources_adopt.py`; `?? .ufo/waves/round-31/`, `?? plans/round-31-claims.md`, `?? plans/round31_defects.py` |
| access date for this round | 2026-10-25 |

The census reads `corpus/SOURCES.md`, which is unmodified, so no sibling edit can move these numbers.
Re-read at `2026-10-25T08:55:04Z`, after sibling seats had begun writing: `git status --porcelain --
corpus/SOURCES.md` still prints nothing, sha256 still `dec033bf…fb5c3`, CMD1 still `88`, CMD3 still
`A=78 B=8 C=2`. Siblings had meanwhile added `M LOG.md`, `M corpus/lessons/round-30.md`,
`M corpus/knowledge/contamination-transparency-card.md`, `?? corpus/evidence/round31/` (C2's write
surface); none of it touches the registry or this census.

## 1. (a) The maintained census — `scripts/sources-census.sh validate`

Command, exactly as assigned (direct execution, shebang `#!/usr/bin/env bash`):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
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
EXIT=0
```

15 lines: 14 `W04` + 1 `ok`; no `E01`–`E12`, no `W01`–`W03`. Output digest
`sha256=2740b4a3ea034e761f1e487b7f6d47781b3ba2d6bca7956797b2f36154cf7899`.
**Byte-identical to the round-30 receipt**: `diff` of this capture against the block quoted at
`.ufo/waves/round-30/falsify/R30FxRowsCensus.md:46-61` (the 15 `kengaku…` lines) is empty.

## 2. (b) The frozen manual census block

`/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a shokunin learns" → §Census
(`CORPUS.md:131-152`) holds **seven** commands, not six. The assignment's count says "six" but its
own parenthetical enumerates seven (rows, malformed, tier histogram, status histogram, duplicate
ids, enum violations, mined used-by paths). All seven were run; nothing in the block was skipped.
Each was run through `bash -c` with the text copied from the block, from the lane root, capturing
stdout+stderr and the exit status of the pipeline as a plain shell reports it.

### CMD1 — rows (spacing-tolerant)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
88
EXIT=0
```

### CMD2 — malformed rows (11 columns means NF=13; must print 0)

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
EXIT=0
```

### CMD3 — tier histogram

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=78 B=8 C=2 
EXIT=0
```

(Trailing space is part of the frozen `printf`, reproduced above.)

### CMD4 — status histogram

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=76 queued=8 rejected=4 
EXIT=0
```

### CMD5 — duplicate ids (must print nothing)

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
EXIT=0
```

No output. Producer stages measured without the pipe: `awk` exit 0 over 88 ids, `sort | uniq -d`
exit 0 with 0 lines — silence is a pass, not a broken stage.

### CMD6 — enum violations and tier inflation (must print nothing)

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
EXIT=0
```

No output. 88 anchored rows satisfied `NF==13`, so the check was not vacuous.

### CMD7 — mined rows whose used-by paths do not exist (must print nothing)

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
EXIT=0
```

No output. Fed 120 path tokens from 76 `mined` rows with `used-by` ≠ `—`, 17 distinct; all 17
resolve on disk (`ok` ×17, no `missing:`). Silence is a pass over real paths, not an empty loop.

### Summary of (b)

| # | command (CORPUS.md:135-152 order) | output | exit |
|---|---|---|---|
| 1 | rows | `88` | 0 |
| 2 | malformed | `0` | 0 |
| 3 | tier histogram | `A=78 B=8 C=2 ` | 0 |
| 4 | status histogram | `mined=76 queued=8 rejected=4 ` | 0 |
| 5 | duplicate ids | *(nothing)* | 0 |
| 6 | enum violations / tier inflation | *(nothing)* | 0 |
| 7 | mined used-by paths missing | *(nothing)* | 0 |

## 3. Difference against the committed round-30 receipt — exactly one command

**CMD3 is the only command whose output differs.** It prints `A=78 B=8 C=2`; the committed
round-30 receipt records `A 79 / B 7 / C 2`:

- `.ufo/waves/round-30/falsify/R30FxRowsCensus.md:107` — `| tiers | **A 79 / B 7 / C 2** | cell 4 |`
- `.ufo/waves/round-30/falsify/R30FxEvidence.md:108` — `… baseline A 76 / B 4 / C 2 → now A 79 / B 7 / C 2; rows now 88`

Everything else matches the same receipt: rows 88 (`R30FxRowsCensus.md:104`), statuses
`mined 76 / queued 8 / rejected 4` (`:108`), duplicate ids 0 (`:105`), and the 14 `W04` census
lines (§1 above, byte-identical).

**Cause, observed in git — a stale receipt, not a registry change.** `corpus/SOURCES.md` is
identical at `0883e72` and at its parent, and both give `A=78 B=8 C=2`. Commit
`9af639c` ("round-30: S086 is not peer-reviewed (society stamp) — relabel and tier to B") changed
S086's tier cell `A` → `B` and touched `corpus/SOURCES.md` (`2 +-`). The two receipts above were
committed **before** it — `R30FxEvidence.md` at `623c1fc`, `R30FxRowsCensus.md` at `706ed3f`,
while `9af639c` is the later commit — and were not re-run after the relabel.

**Three independent readings agree with the frozen command, and the round-30 receipts are the
outliers:**

- maintained parser: `sources-census.sh census --file …/corpus/SOURCES.md` →
  `file tier.A 78` / `file tier.B 8` / `file tier.C 2` / `file rows 88`, `FLEET` the same, exit 0;
- `corpus/lessons/round-30.md:93` — "they enter `mined`, tier A 76 → 78, tier B 4 → 8";
- `SCORECARD.md:1022` (round-30 C1 row) — "Registry 82 → 88 rows (S081–S086, tier A 76→78, B 4→8)".

The six round-30 rows are `B,B,A,A,B,B` (`S081 B, S082 B, S083 A, S084 A, S085 B, S086 B`), and
`76+4+2 = 82` baseline rows → `A=78 B=8 C=2`, which sums to the 88 rows CMD1 prints. The receipt's
`A 79 / B 7` does not sum against its own per-row tier table either. **Number-drift class**, in
`.ufo/waves/round-30/falsify/` only: the registry itself is clean under CMD1/CMD2/CMD6, and
`A=78 B=8 C=2` is the correct reading of the tree the round started on.

## 4. Round-start baseline the three claims start from

| counter | round-start value | how |
|---|---|---|
| registry rows | 88 | CMD1 |
| knowledge files | 39 | `ls corpus/knowledge/*.md \| wc -l` |
| README index rows | 39 | anchored `knowledge/<name>.md` index rows in `corpus/README.md` (`grep -cE` over the row prefix) |
| census verdict | exit 0, 14 `W04`, 0 `E*` | §1 |
| ids ≥ S092 in registry | 0 (`grep -cE '^\|[[:space:]]*(S092\|S093\|S100)[[:space:]]*\|'` → `0`) | C1's three ids are free |
| those ids in the staged package | present, 3 rows | `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:22` S092, `:23` S093, `:30` S100 |
| staged package rows | 175 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on the append |
| round-31 expectation | `entries=[{path: corpus/knowledge/benchmark-verifier-execution-model.md, sources: [S092,S093,S100]}]`, `access_date 2026-10-25` | `.ufo/waves/round-31/adoption-expect.json` |

The C1 predicate's `cited_rows=3` therefore starts from a registry that holds none of the three
ids and a package that holds all three; `rows_present=3` is reachable only by appending them.
C2's and C3's counters read only round-30 bytes and were not touched by this census.

## 5. Not done (bounds)

No `plans/`, `corpus/`, `.ufo/state`, `MANIFEST.json`, `watchdog.log` or Git-index write; no
`git add/commit/checkout/reset/push`; no mutating `jj`; no write or campaign tool under
`/home/vgpnk/Projects/shokuknow`; no sibling lane touched; no subagent, background job or `ask`.
The five modified and three untracked paths in §0 were already there and were left exactly as found.

VERDICT: PASS — census validate exits 0 with the 14 `W04` warnings byte-identical to round 30, and of the seven frozen manual commands (rows `88`, malformed `0`, statuses `mined=76 queued=8 rejected=4`, duplicate ids, enum violations, mined used-by paths all silent, each exit 0) exactly one differs from the committed round-30 receipt: the tier histogram prints `A=78 B=8 C=2` where `.ufo/waves/round-30/falsify/R30FxRowsCensus.md:107` and `R30FxEvidence.md:108` say `A 79 / B 7 / C 2`, a stale receipt left behind by commit `9af639c`'s S086 A→B relabel and confirmed wrong by the maintained parser, `corpus/lessons/round-30.md:93` and `SCORECARD.md:1022` — the registry is clean.
