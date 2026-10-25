# F35Census — kengaku round 35 wave 2 (falsify) seat report

Seat: F35Census (executor, leaf). Target: sources census of the landed lane tip
`dfee6fff631ebc5f623ba4506e5c7992a215401c` (branch master; `git rev-parse HEAD`
in the lane = `dfee6fff631ebc5f623ba4506e5c7992a215401c`, so the worktree is at
the landed tip).

## 1. `sources-census.sh validate` — command, output, exit

Command:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

Output (full):

```
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
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

Exit code: **0** (appended `echo "EXIT=$?"` → `EXIT=0`).

Reading: no E-code findings (E01–E12 all absent); only W04 warnings (same normalized
URL across scopes without a supersedes row), which by the contract never change a
clean lane's status. The registry validates clean.

## 2. Row counts before/after

Commands (read-only `git show` of the committed blobs):

```
git -C <lane> show 58a19f37312e1b22fd2a7957bdfc6bb7832aadd0:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
git -C <lane> show dfee6fff631ebc5f623ba4506e5c7992a215401c:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
```

Output: `BEFORE=97`, `AFTER=100`.

ID diff (same blob extraction, ids sorted, `comm`):

```
== ADDED between before and after:
105
106
107
== REMOVED between before and after:
(empty)
== COUNT before=97 after=100
```

Round 35 therefore added exactly rows **S105, S106, S107** and removed none. All
three are the Terminal-Bench 2.0 protein-assembly rows (C1 coverage): S105
`tests/test_outputs.py` grader, S106 `tests/test.sh` verifier runner, S107
`instruction.md` task instruction — each mined, tier A, used-by
`corpus/knowledge/tb2-protein-assembly-grader.md`, matching the frozen C1 claim.

## 3. Tier/status histograms

Awk over the committed `corpus/SOURCES.md` at each commit (field split on `|`,
id-matching rows only; NF!=13 rows counted separately):

Before (58a19f3): rows=97, tiers A=82 B=13 C=2, status mined=81 queued=8 rejected=8.
After (dfee6fff): rows=100, tiers A=85 B=13 C=2, status mined=84 queued=8 rejected=8.

Histogram check (after):

```
TIER: A 85, B 13, C 2
STATUS: mined 84, queued 8, rejected 8
NF!=13 rows: 0
```

Cross-check with the census mode of the same script:

```
kengaku	rows	100
kengaku	tier.A	85
kengaku	tier.B	13
kengaku	tier.C	2
kengaku	status.mined	84
kengaku	status.queued	8
kengaku	status.rejected	8
FLEET	rows	100
FLEET	tier.A	85
FLEET	tier.B	13
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	84
FLEET	status.rejected	8
FLEET	status.invalid	0
FLEET	missing	0
CENSUS_EXIT=0
```

The awk histograms and the script's own census agree exactly. The only change
across the round is +3 mined tier-A rows (S105–S107); queued/rejected/tier-B/C
counts unchanged.

## 4. NF==13 for every row

Awk `NF != 13` count over blob rows: **0 bad at before, 0 bad at after**
(every row in the registry table has exactly 13 pipe-delimited fields). The
validate run's absent E01 (malformed row) independently confirms this.

## 5. Every mined row's used-by paths exist

Extracted used-by (column 12, trimmed, `—`/empty skipped) for all 84 mined rows
at dfee6fff, deduplicated, and checked `-f` relative to the lane root:

- mined rows total: 84
- unique used-by paths examined: all exist — `OK` for every path, **0 MISSING**.

No dangling used-by paths. (Validate's E11 check was also absent.)

## 6. Falsify verdict

Nothing falsified: validate exit 0 clean (W04-only), rows 97 → 100 with exactly
S105/S106/S107 added, 0 rows removed, NF==13 on every row at both commits, tier/status
histograms consistent between independent awk and the script's census mode, and all
84 mined rows' used-by paths present on disk.

Evidence that would have shown disagreement (all tried, none occurred): any E-code
(E01–E12) with exit 1; row counts other than 97/100; added/removed ids other than
S105/S106/S107; `NF != 13` > 0; any mined used-by path missing (`MISSING`); or a
tier/status histogram drift beyond +3 mined tier-A rows (the census-mode output is
the independent cross-check).

Tooling: no tools installed or updated (none were needed; RULES.md read).

VERDICT: census-0-rows-97-100
