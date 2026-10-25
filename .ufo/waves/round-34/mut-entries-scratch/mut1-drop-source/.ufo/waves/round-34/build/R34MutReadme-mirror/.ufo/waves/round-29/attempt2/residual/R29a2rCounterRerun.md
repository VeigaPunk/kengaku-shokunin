# Round 29 attempt 2 — residual seat: frozen-counter re-run on the landed tree

Seat: `L1Kengaku29.R29a2rCounterRerun` (residual verification, leaf, read-only outside the residual dir).
Host date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
All commands below were executed from that lane root.

## Revision state (this matters — see F1)

```
$ git rev-parse HEAD
4b82ff7acb73e548f9af71b25e3218ae4c839b88
$ git rev-parse master
4b82ff7acb73e548f9af71b25e3218ae4c839b88
$ git merge-base --is-ancestor ff476d0 4b82ff7 ; echo $?
0
```

The assignment names `ff476d017107ec5ee3df735a16713c5967592b71` as the landing commit. At the start of
this seat `git rev-parse master` printed exactly `ff476d017107ec5ee3df735a16713c5967592b71`; during the
seat `master` advanced to `4b82ff7` ("round-29: remove entry widenings, tighten used-by and census
gating, widen census row anchor"). **Every result below was reproduced under BOTH revisions with
identical output and identical exit codes** — the sealed `ff476d0:plans/adoption_check.py` blob
(`7b43f97d…`) was extracted with `git show` and run separately from the HEAD blob (`20726fc0…`).

Instrument identity at final state (worktree == HEAD):

| instrument | worktree blob | HEAD blob |
|---|---|---|
| `plans/adoption_check.py` | `20726fc0bd1cc9765b2b88bec0e202c0617348e3` | `20726fc0bd1cc9765b2b88bec0e202c0617348e3` |
| `plans/sources_adopt.py` | `e496ff93f2963dfd99b0298f89b93615648cfb98` | `e496ff93f2963dfd99b0298f89b93615648cfb98` |
| `plans/round28_census.py` | `c73cdd427520b5b14494435748e7a92fa4dd0dcf` | `c73cdd427520b5b14494435748e7a92fa4dd0dcf` |

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` is unmodified in its own repo
(`git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/sources-census.sh` → empty, exit 0);
sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.

## CMD1 — adoption check with `--census`

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
EXIT=0
```

Byte-identity against the frozen C1 target line (target written with `printf '%s\n'`, i.e. the line plus
its newline):

```
$ printf '%s\n' 'entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok' > target.txt
$ cmp target.txt c1.out ; echo $?
0
$ wc -c target.txt c1.out
 83 target.txt
 83 c1.out
$ sha256sum target.txt c1.out
810c54e0a3e668d1aa4cc51613a8e1e869bc4d95af1a8d44728e54591f76d1cb  target.txt
810c54e0a3e668d1aa4cc51613a8e1e869bc4d95af1a8d44728e54591f76d1cb  c1.out
```

Determinism: three consecutive runs printed the identical line with `EXIT=0` each time.

## CMD2 — adoption check WITHOUT `--census`

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped
EXIT=1
```

## CMD3 — `sources_adopt.py --selftest`

```
$ python3 plans/sources_adopt.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
SELFTEST cases=10 failed=0
EXIT=0
```

## CMD4 — fleet census `validate` for the kengaku lane

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

14 duplicate-URL warnings, all W04 and all for rows `S040`–`S076`; none names a round-29 row
(`S077`–`S090`). Warnings are non-fatal: the trailing `ok` line plus exit 0.

This subprocess is exactly what `--census` runs: `adoption_check.py` invokes
`CENSUS validate --root <lane.parent> <lane-name-without-'-shokunin'>`
(`plans/adoption_check.py`, census block), so CMD1's `census=ok` and CMD4's exit 0 are one measurement,
not two independent ones.

## CMD5 — read-only git state

```
$ git rev-parse master
4b82ff7acb73e548f9af71b25e3218ae4c839b88
EXIT=0

$ git status --porcelain
 M .ufo/waves/round-29/attempt2/build/R29a2CounterAudit.md
 M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
 M .ufo/waves/round-29/attempt2/build/R29a2EntryDraft.md
 M .ufo/waves/round-29/attempt2/build/R29a2RevCensus.md
 M .ufo/waves/round-29/attempt2/build/R29a2SimpGate.md
?? .ufo/waves/round-29/attempt2/build/R29a2GateBlock.md
?? .ufo/waves/round-29/attempt2/build/R29a2RevQuality.md
EXIT=0
```

All seven entries are sibling wave report files under `.ufo/waves/round-29/attempt2/build/`.
`git diff HEAD --stat -- plans/ corpus/` prints nothing (0 lines): every counter instrument and every
counted corpus byte is at HEAD.

## Verdict on the frozen C1 line

Frozen target: `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`

- **Byte-for-byte match: YES.** CMD1's stdout is 83 bytes, `cmp` exit 0, sha256
  `810c54e0a3e668d1aa4cc51613a8e1e869bc4d95af1a8d44728e54591f76d1cb` on both sides. The seven fields
  are the complete print statement — `verified_at` is computed but gated silently, so it cannot leak
  into the line.
- **Exit code 0: YES.** `EXIT=0` under the sealed `ff476d0` blob and under the HEAD `4b82ff7` blob.

The frozen line is the `--census` invocation's output. The un-flagged invocation (CMD2) prints
`census=skipped` and exits 1 — see F3.

## Findings

### F1 — MEDIUM — the named landing commit is no longer `master`'s tip (state moved under the seat)

`master` was `ff476d0…` when this seat started and is `4b82ff7…` now; `ff476d0` is an ancestor
(`merge-base --is-ancestor` → 0). `4b82ff7` rewrote the counter this seat verifies
(`plans/adoption_check.py`, +7/−1 region: `verified-at` regex gains `\b`, `used-by` becomes comma-token
exact, and `and args.census` is added to the `ok` conjunction) plus
`corpus/knowledge/benchmark-task-validity-checklist.md` (+20/−10) and `plans/round28_census.py`.

Consequence for the wave: a report that pins its evidence to `ff476d0` describes a tree that is no
longer the branch tip. The C1 contract itself is unaffected — both revisions print the frozen line
byte-identically and exit 0 — but any claim of the form "at the landing commit" must name which one.

Evidence that the counted bytes are untouched by the newer commit:

```
$ git diff ff476d0 4b82ff7 -- corpus/knowledge/benchmark-task-validity-checklist.md | grep -E '^[+-](source:|verified-at)'
COUNTED_LINE_DELTA_GREP_EXIT=1
```

No `source:` or `verified-at:` line changed in the entry; `corpus/SOURCES.md` and `corpus/README.md` are
not in `4b82ff7` at all (`git diff HEAD --name-only -- corpus/SOURCES.md corpus/README.md` → empty).
That is why the counters are revision-invariant here.

### F2 — MEDIUM — the committed measurement receipt records a line the landed counter cannot print

`.ufo/waves/round-29/attempt2/adoption-measured.txt` is committed (blob `62fa0d85…`, introduced in
`8cf7b60`, untouched by `4b82ff7`) and contains an **eight**-field line:

```
fields=8 :: entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
fields=7 :: entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

The first line is the file's content; the second is the counter's actual output at HEAD. The landed
`print()` emits exactly the seven frozen fields and never `verified_at`, so the receipt cannot have been
produced by the committed instrument — it predates the field removal. Anyone diffing the frozen target
against the recorded receipt sees a spurious mismatch at field 7.

### F3 — LOW — the no-flag invocation exits 1, twice by design

CMD2 prints `census=skipped` and exits 1 at both revisions: `census_code = 1  # an unrun census is not a
pass` in `ff476d0`, plus `and args.census` in the `ok` conjunction at `4b82ff7`. This is intended, but
an operator running the bare command sees a non-zero exit and a line that differs from the frozen target
only in the last field.

### F4 — LOW — `used-by` linkage is single-token, and the five rows satisfy the stricter form

Under the stricter HEAD logic (`rel in [part.strip() for part in cell.split(",")]`), all five rows pass
with the entry path as the cell's only token:

```
S077 status=mined usedby token exact=True | raw cell= corpus/knowledge/benchmark-task-validity-checklist.md
S078 status=mined usedby token exact=True | raw cell= corpus/knowledge/benchmark-task-validity-checklist.md
S079 status=mined usedby token exact=True | raw cell= corpus/knowledge/benchmark-task-validity-checklist.md
S080 status=mined usedby token exact=True | raw cell= corpus/knowledge/benchmark-task-validity-checklist.md
S090 status=mined usedby token exact=True | raw cell= corpus/knowledge/benchmark-task-validity-checklist.md
```

`usedby_ok=1` is therefore not an artifact of substring matching. Residual: the check is exact-token, so
a future entry listing this file alongside a second consumer must comma-separate, not space-separate.

### F5 — INFORMATIONAL — mid-seat the worktree briefly held dirty instruments and corpus

Between two status snapshots this seat observed `plans/adoption_check.py` at 4962 bytes
(mtime `2026-10-25 03:53:15`), plus modified `plans/round28_census.py`,
`corpus/knowledge/benchmark-task-validity-checklist.md`, `corpus/lessons/round-29.md` and
`corpus/evidence/round29-attempt2/census-after.txt`; those are now committed as `4b82ff7`. No counter
output in this report was disturbed: the same line and exit code were produced before, during, and
after that window, and under the sealed `ff476d0` blob run from `/tmp`.

## Residual risk and verification gaps

- **Single-entry scope.** `adoption-expect.json` carries one entry and five sources. `entries=1
  indexed=1` and `usedby_ok=1` are all-of checks over a single element; a two-entry expectation is not
  exercised by any command here.
- **`verified_at_ok` is unobservable from outside.** It gates `ok` but is not printed, so a counter whose
  access-date check silently stops matching would still emit the frozen seven-field line — with
  `EXIT=1`. Only the exit code distinguishes; the printed line cannot. CMD1's exit 0 is the sole
  evidence that the date gate fired.
- **Census is one measurement, not two.** CMD1's `census=ok` and CMD4's exit 0 run the same script with
  the same arguments; agreement is by construction.
- **Duplicate-URL warnings are cumulative and unfixed.** 14 W04 rows share URLs across scopes, including
  three distinct rows pointing at `docs.python.org/3/library/json.html`. The census tolerates them
  (exit 0), so the gate cannot regress on this and no command here would notice a new duplicate.
- **F1 means the wave's commit pins need re-reading** before any report states "measured at ff476d0".
- Not run, by scope: `plans/round28_census.py`, the gate/controls scripts, and any census of sibling
  lanes.

No installs were performed (none needed).

Report: `.ufo/waves/round-29/attempt2/residual/R29a2rCounterRerun.md`
