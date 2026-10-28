# R50FRExecCensus — before census (kengaku r50, hyaku 11, wave w1)

Seat: executor, leaf. Item: **before census** — `sources-census.sh validate` + the frozen CORPUS.md census
snippets, measured at the stage-1 freeze. Read-only against the lane; no production file touched; no commit,
no git mutation anywhere outside my own scratch clone.

Axes named (per assignment): **novelty** (C1 — this census is the `corpus/SOURCES.md` before-state that the
round's frontier step, claims §2b "census before→after", is measured against) and **calibration** (C2 — the
census artefacts it fixes are the frozen pointers C2 audits; I measured neither claim's predicate, and this
report claims **no** R50-C1/R50-C2 admission).

```
REV lane-tip-at-measurement   d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78   (lane checkout advanced d6f2fce→d45c5bb during this seat's run; not used for any number below)
REV freeze-commit             3b02d573d58cc6d2e0d27ef92ac0815354912252   (measured revision; every census number below is from this commit)
REV base-tip-per-assignment   71f5f5f77591d8c3d19297ee9785436da45209e4
REV clone                     /fast/scratch/hyaku/kengaku-r50/R50FRExecCensus/root/kengaku-shokunin @ 3b02d57 (git clone --shared, clean: 0 status entries)
REV sources-blob-at-freeze    256a5dd90a3377b9c49783b5b6d209bed13c4e43
REV sources-sha256-at-freeze  09b1c39d6c13f1f7b6ba74729381e4e156a10154ce9c45913b8cb31d164136a6   (219 lines)
SHA256 census-script          3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ENV  git 2.56.0 · GNU Awk 5.4.1 · 32 cores · /fast NVMe free 505G
```

## 1. Freeze verification (before any measurement)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD ; echo rc=$?
rc=0                                   # freeze IS an ancestor of the live lane tip
$ git merge-base --is-ancestor 71f5f5f77591d8c3d19297ee9785436da45209e4 3b02d573d58cc6d2e0d27ef92ac0815354912252 ; echo rc=$?
rc=0                                   # the named base tip IS an ancestor of the freeze
$ git rev-list --count 71f5f5f..3b02d57
2                                      # the freeze is 2 commits past the named base tip
$ git log -1 --format='%H %ci %s' 3b02d573d58cc6d2e0d27ef92ac0815354912252
3b02d573d58cc6d2e0d27ef92ac0815354912252 2026-10-28 14:18:09 -0300 round-50: C1 four-control receipts and C2 before/selftest receipts (pre-data)
```

Note for the L1: the freeze is **not** an ancestor of `71f5f5f` (rc=1 for that direction) — it is a
descendant of it. The assignment's "before any measurement verify the freeze commit is an ancestor of the lane
tip" is satisfied against the live tip (rc=0) and against the named base tip in the correct direction.

The live lane's `corpus/SOURCES.md` is **not** the frozen one: at the end of this seat the live working tree
equals live HEAD (`d45c5bb`), 224 lines, git blob `6a6f4954b1a90e55bb67d624b5bc9e0bf2af7350`, sha256
`8a1ba15597360ea21b2c9b184c26be7827a49d9e0f50d7abae23d9957da2f4eb`; the freeze is 219 lines, blob
`256a5dd90a3377b9c49783b5b6d209bed13c4e43`, sha256 `09b1c39d…` — the round's S173–S177 git-doc rows already
landed at `822f3b7`. Therefore every number in §2 (A), §3–§5 is taken
from a `git clone --shared` checked out at the freeze, never from the live working tree.

## 2. `sources-census.sh validate`

### A. Freeze-pinned (evidence of record)

Root wrapper: a scratch `shokunin.conf` whose only row is the fleet's own mapping
(`kengaku|kengaku-shokunin|…`, fleet-root `shokunin.conf:47`), so the script resolves lane `kengaku` to the
clone's `corpus/SOURCES.md`. Same script binary, same lane id, same mode; only `--root` points at the frozen
clone instead of the live checkout.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /fast/scratch/hyaku/kengaku-r50/R50FRExecCensus/root kengaku ; echo EXIT=$?

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
kengaku	ok	/fast/scratch/hyaku/kengaku-r50/R50FRExecCensus/root/kengaku-shokunin/corpus/SOURCES.md
EXIT=0
(stderr: empty)
```

15 × `W04` (duplicate URL across scopes — warning class, does not affect lane status), 1 × `ok`, **no E-codes**
(E01–E12), exit **0**.

### B. Literal as-issued form (live fleet root)

The item names the command with `--root /home/vgpnk/Projects/shokunin`; run exactly as issued it reads the live
lane **working tree**, not a commit. Recorded for fidelity only — this is not the freeze measurement:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin kengaku ; echo EXIT=$?
… identical 15 × W04 lines (S040 S048 S057 S058 S059 S064 S065 S066 S067 S068 S069 S071 S075 S076 S100) …
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
EXIT=0
(stderr: empty)
```

Observation worth carrying to the L1: the *finding set* is identical on the frozen tree and on the live tree
that already carries S173–S177, so the round's row additions add no new W04 and no new E-code. The count
totals differ (§5 cross-check is the frozen one).

## 3. Frozen CORPUS.md census snippets (freeze clone, cwd = clone root)

The block at fleet `CORPUS.md:131-150` (`### Census — run from the lane root`) contains **seven** snippets;
the assignment names five of them ("rows, malformed rows, tier histogram, status histogram, duplicate ids")
and calls them "four". All seven were run so the named five are covered unambiguously and the block is
exercised whole. Every snippet ran with `cwd` = the clone root (`corpus/SOURCES.md` relative path) at
`REV 3b02d57`.

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
SOURCES_SHA256 09b1c39d6c13f1f7b6ba74729381e4e156a10154ce9c45913b8cb31d164136a6

### snippet 1: rows
165
EXIT=0

### snippet 2: malformed rows (must print 0)
0
EXIT=0

### snippet 3: tier histogram
A=141 B=22 C=2 
EXIT=0

### snippet 4: status histogram
mined=149 queued=8 rejected=8 
EXIT=0

### snippet 5: duplicate ids (must print nothing)
EXIT=0

### snippet 6: enum violations and tier inflation (must print nothing)
EXIT=0

### snippet 7: mined rows whose used-by paths do not exist (must print nothing)
EXIT=0
```

Verbatim commands (exactly the frozen block, only the path prefix unchanged):

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {…enum…}' corpus/SOURCES.md      # snippet 6
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {…used-by…}' corpus/SOURCES.md   # snippet 7
```

Before-state table (frozen, 3b02d57):

| metric | value |
|---|---|
| registry rows | **165** |
| malformed rows (NF≠13) | 0 |
| tier histogram | **A=141 B=22 C=2** (invalid 0) |
| status histogram | **mined=149 queued=8 rejected=8** (invalid 0) |
| duplicate ids | none |
| kind/status/tier enum violations, community-at-A | none |
| mined rows with missing used-by path | none |

## 4. Maintained-parser cross-check (freeze clone)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root …/root kengaku ; echo EXIT=$?
kengaku	rows	165
kengaku	tier.A	141
kengaku	tier.B	22
kengaku	tier.C	2
kengaku	status.mined	149
kengaku	status.queued	8
kengaku	status.rejected	8
FLEET	rows	165
FLEET	tier.A	141
FLEET	tier.B	22
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	149
FLEET	status.rejected	8
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```

Independent parser agrees with the frozen awk snippets on all five named metrics (`missing 0` also confirms
snippet 7's silence from the other side).

## 5. Sensitivity checks on the "165"

The frozen snippets anchor at column 0 (`^\|`); the maintained parser tolerates 0–3 leading spaces. A row
indented 1–3 spaces would be invisible to a frozen snippet and visible to the parser — so agreement was
tested rather than assumed:

```
col0 rows:          165
0-3 space rows:     165      # no indentation drift; the frozen and maintained counts coincide by measurement
table lines (0-3):  167      # 165 rows + header + separator
NF!=13 (0-3):       0
distinct ids:       165
first/last id:      S001 / S172   # gaps in the sequence, no reuse, no duplicate
```

## Limits

- **One revision only.** Everything in §2A and §3–§5 is `3b02d57`. The live lane advanced twice during the
  seat (`d6f2fce` → `d45c5bb`); §2B records the live-tree reading at the moment of that invocation and is not
  a substitute for the L1's after census.
- **`W04` is warning-class by contract** (exit unchanged, "W-codes never change status"); 15 warnings are the
  frozen before-state, not a defect introduced here and not something this seat may remediate (production
  files are out of scope).
- **The census reads `corpus/SOURCES.md` plus filesystem existence of `used-by` paths.** It says nothing about
  whether those paths' content is truthful, nor about tiers being correct beyond the enum/community-at-A rules.
  The `E11` check resolves inside the clone, so "missing 0" is a statement about the freeze tree's file set.
- **Snippet-count discrepancy in the assignment** ("four … (rows, malformed rows, tier histogram, status
  histogram, duplicate ids)") is recorded, not silently resolved: five were named, seven exist and all seven
  were run.
- **No harness verification of the instrument.** The script's own `--selftest` was not run (not in the item;
  the script is a fleet-root file outside the lane and outside my write scope).
- Receipts are embedded verbatim in this file rather than written as sibling files, to keep to the
  one-file lane write scope. Scratch tree
  `/fast/scratch/hyaku/kengaku-r50/R50FRExecCensus` (clone `--shared` at 3b02d57 + conf wrapper + captured
  stdout/stderr) was removed before yield — no scratch left on disk, nothing outside the clone was written.

## VERDICT

**PASS — before census captured at the freeze.** `sources-census.sh validate` at
`REV 3b02d573d58cc6d2e0d27ef92ac0815354912252`: exit **0**, `ok`, 15 warning-class `W04`, **no E-findings**.
Frozen population: **165 rows; tier A=141 B=22 C=2; status mined=149 queued=8 rejected=8; malformed 0;
duplicate ids 0; enum/community violations 0; missing used-by 0** — confirmed by both the frozen awk snippets
and the maintained parser. No R50-C1/R50-C2 admission claimed; no SCORECARD/LOG/corpus write; no commit.
