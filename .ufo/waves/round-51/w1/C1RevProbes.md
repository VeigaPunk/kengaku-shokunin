# C1RevProbes — independent re-probe of all 19 declared C1 surfaces

Seat: `C1RevProbes` (reviewer), kengaku round 51, hyaku run 11, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Read-only against the lane; the only
lane file written is this report.

## Axes named

- **Primary axis: freshness (C1, 8 → 9)** — "every surface `PROVINCE.md` declares is
  machine-checked". The frontier coordinates I walk are the five C1 sub-counters
  (`STALE`, `DRIFT`, `UNVERDICTED`, `NUMBER-DRIFT`, `RESOLVE`) plus one coordinate the
  predicate does **not** print: whether the counter's verdicts survive a *different
  measurement primitive* on the same tree.
- **Secondary axis: adjacency (C2)** — untouched by this seat (no `corpus/routed-findings.jsonl`
  read or write). Named only so the L1 knows the C2 axis is unmeasured here.
- **Not an axis, measured anyway: instrument operability** — whether the frozen C1 command
  returns the same verdict for the same tree. This is a freshness *truth* question (a counter
  whose verdict depends on CWD cannot certify the tip), not a separate axis move.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

`git rev-parse master` == `HEAD` == `4090c3d` ("round-51: v2 wave spec (64 seats) + validated
dispatch payload"). `git status --porcelain` = 9 untracked `.ufo/waves/...` entries;
`git status --porcelain -- PROVINCE.md corpus/SOURCES.md plans/round51-surfaces.json
plans/round51_surfaces.py grader.py` = **0**, so every file I measured is byte-identical to
commit `4090c3d`. All measurements are of the lane tree at that revision.

## Frozen instruments read first

- `plans/round-51-claims.md` (read in full).
- `plans/round51_surfaces.py` (whole file, incl. `probe()` and `check()`).
- `plans/round51-surfaces.json` (19 entries, 2 sections, `resolve_floor` 13).
- `PROVINCE.md` `## Surfaces` (lines 8–21) and `### Core` (lines 102–119).

Baseline reproduced with the frozen command, from the lane root:

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round51_surfaces.py --lane .
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

This is the recorded before receipt (`.ufo/waves/round-51/claims/c1-before.txt`, `REV 297e179…`)
except the `REV` line — verified, not eyeballed:

```
$ diff <(grep -v '^REV ' tip.txt) <(grep -v '^REV ' .ufo/waves/round-51/claims/c1-before.txt)
IDENTICAL_APART_FROM_REV
```

The before receipt was taken at base tip `297e1792`; the tip has since advanced to `4090c3d`, and
**no surface verdict changed** between the two revisions (`present=13 absent=6`, `DRIFT 3`,
`UNVERDICTED 1`, `NUMBER-DRIFT 1`, exit 1).

## Primitive map — what the counter uses vs what I used

| Probe kind | Entries | Counter primitive (`round51_surfaces.py`) | My independent primitive(s) |
|---|---|---|---|
| `paths` | SF01,02,04,05,06,07,08,09,11,13,17,18,19 (13) | `pathlib.Path.exists()` (via `expand()`) | `stat -c '%n \| %F \| %s bytes'` **and** `ls -d`; plus `stat` type check (`directory`/`regular file`) |
| `sha256` | SF10,12,15 (3) | `hashlib.sha256(f.read_bytes()).hexdigest()` + 8-char `startswith(pin)` | `sha256sum` **and** `openssl dgst -sha256` (full 64 hex), plus `b2sum` as a third digest family |
| `port` | SF16 (1) | Python `socket.connect(("127.0.0.1", 8791))` | `ss -ltn 'sport = :8791'` **and** `nc -z -w2`; `getent ahosts 127.0.0.1` for name resolution |
| `http` | SF03 (1) | `urllib.request.urlopen(...).status == 200` on `/health` only | `curl -sS -o /dev/null -w '%{http_code}'` on **all three** endpoints the row declares |
| `count` | SF14 (1) | `len(re.findall(r'^\|\s*S[0-9]{3,}\s*\|', text, re.M))` | `grep -cE`, `awk -F'\|'` field-2 match, `wc -l`, and a Python id-set census (distinct ids, min/max, gaps, dups) |

Total: 19/19 entries re-probed, every one with at least one primitive outside the counter's.

## Result — 19 rows, both outputs

`state` = the manifest's recorded state; `C` = counter verdict; `M` = my verdict.

| id | target | state | C | M | my verbatim output |
|---|---|---|---|---|---|
| SF01 | `~/Projects/webzites/repos/llm-wiki` | absent | absent | absent | `ABSENT  /home/vgpnk/Projects/webzites/repos/llm-wiki` (stat); `ls: cannot access '…/llm-wiki': No such file or directory` |
| SF02 | `~/archive/bench-arena` | absent | absent | absent | `ABSENT  /home/vgpnk/archive/bench-arena`; `ls: cannot access '…/bench-arena': No such file or directory` |
| SF03 | `http://127.0.0.1:34113/health` | absent | absent | absent | `curl: (7) Failed to connect to 127.0.0.1:34113 after 0 ms: Could not connect to server` → `000` (exit 7) |
| SF04 | `~/Projects/bounties/ledger/telemetry.jsonl` | absent | absent | absent | `ABSENT  /home/vgpnk/Projects/bounties/ledger/telemetry.jsonl`; parent tree also absent |
| SF05 | `~/.bailian/telemetry.jsonl` | absent | absent | absent | `ABSENT  /home/vgpnk/.bailian/telemetry.jsonl`; `~/.bailian` itself absent |
| SF06 | `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` | absent | absent | absent | `ABSENT  …/models/index.md`; `models.jsonl` also absent |
| SF07 | 5 evidence dirs | present | present | present | `PRESENT corpus/evidence/round8-horizon \| directory \| 94 bytes` (+4 more, all `directory`) |
| SF08 | `grader.py` | present | present | present | `PRESENT grader.py \| regular file \| 274855 bytes` |
| SF09 | `corpus/knowledge/eval-prior-art-calibration.md` | present | present | present | `PRESENT corpus/knowledge/eval-prior-art-calibration.md \| regular file \| 8619 bytes` |
| SF10 | `grader.py` pin `90c87c88` | present | present | present | `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f  grader.py` (sha256sum) / `SHA2-256(grader.py)= 90c87c88…ae941f` (openssl) |
| SF11 | 7 evidence dirs | present | present | present | `PRESENT corpus/evidence/round9-fleet \| directory \| 504 bytes` (+6 more, all `directory`) |
| SF12 | `plans/attrib_probe.py` pin `489f938a` | present | present | present | `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b  plans/attrib_probe.py` / `SHA2-256(plans/attrib_probe.py)= 489f938a…16e06b` |
| SF13 | `corpus/QUALITY.md` | present | present | present | `PRESENT corpus/QUALITY.md \| regular file \| 108725 bytes` |
| SF14 | `count` on `corpus/SOURCES.md`, claim 25 | present | present / NUMBER-DRIFT 1 | present, count **170** | see §F3: `grep -cE` 170, `awk` 170, Python `re` 170, distinct ids 170 |
| SF15 | `~/.local/share/ds-flash-shim/shim.py` pin `42d86d99` | present | present | present | `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  /home/vgpnk/.local/share/ds-flash-shim/shim.py` / `SHA2-256(…)= 42d86d99…15a386` |
| SF16 | port 8791 | present | present | present | `LISTEN 0 512 127.0.0.1:8791 0.0.0.0:*` (ss); `Connection to 127.0.0.1 8791 port [tcp/*] succeeded!` (nc, exit 0) |
| SF17 | 2 knowledge files | present | present | present | `PRESENT corpus/knowledge/eval-prior-art-calibration.md \| regular file`; `PRESENT corpus/knowledge/attrib-prior-art-r21.md \| regular file \| 14608 bytes` |
| SF18 | `plans/attrib_calibration.py` | present | present | present (row command run) | `TOTAL files=9 … correct=92 incorrect=0 … mismatches=0` / `EXIT=0` (see §F4c) |
| SF19 | `plans/state_check.py` | present | present | present (row command run) | `VERDICT: PASS — all comparable frozen assertions match` / `EXIT=0` (see §F4c) |

**Primitive disagreement on the 19 recorded states: 0.** Every one of the 19 manifest `state`
values is confirmed by an independent primitive (13 `present`, 6 `absent`). The counter's
`STALE 0` is therefore not an artifact of its own primitive choice: `stat`/`ls -d`,
`sha256sum`/`openssl`, `ss`/`nc -z`, `curl` and `grep`/`awk` all agree with it on this tree.

Two extras that strengthen rather than change the verdict:

- `sha256sum` and `openssl dgst -sha256` agree to all 64 hex on all three pinned files, and the
  full digests match the tails `PROVINCE.md` prints (`90c87c88…ae941f`, `489f938a…16e06b`,
  `42d86d99…15a386`). The counter's 8-char `startswith` pin is not hiding a suffix mismatch.
- SF16's row asserts the listener is `ds-flash-shim` on `127.0.0.1:8791`; `ss -ltnp` attributes
  `127.0.0.1:8791` to `python3` pid 1515 and `tr '\0' ' ' </proc/1515/cmdline` prints
  `/usr/bin/python3 /home/vgpnk/.local/share/ds-flash-shim/shim.py`, and `curl :8791/` → `200`.

## Findings

### F1 — HIGH — the counter's `paths`/`sha256` probes resolve against process CWD, not `--lane`; the predicate is not CWD-invariant

`probe()` joins `lane` for `count` only:

```python
if kind == "paths":
    missing = [t for t in p["targets"] if not expand(t).exists()]     # CWD, not lane
...
if kind == "sha256":
    f = expand(p["target"])                                            # CWD, not lane
...
if kind == "count":
    f = lane / p["target"] if not os.path.isabs(p["target"]) else Path(p["target"])   # lane-joined
```

10 of the 19 entries carry lane-relative targets (`corpus/…`, `plans/…`, `grader.py`). Run the
same script on the same tree from any other CWD and the counter flips 10 entries to `absent`:

```
$ cd /home/vgpnk/Projects/shokunin && python3 kengaku-shokunin/plans/round51_surfaces.py --lane kengaku-shokunin
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
PROBES run=19 present=3 absent=16 errors=0
DRIFT 3
STALE 10
  DETAIL STALE SF07 probe=absent state=present (missing: corpus/evidence/round8-horizon, …)
  DETAIL STALE SF08 probe=absent state=present (missing: grader.py)
  DETAIL STALE SF09 probe=absent state=present (missing: corpus/knowledge/eval-prior-art-calibration.md)
  DETAIL STALE SF10 probe=absent state=present (missing file grader.py)
  DETAIL STALE SF11 probe=absent state=present (missing: corpus/evidence/round9-fleet, …)
  DETAIL STALE SF12 probe=absent state=present (missing file plans/attrib_probe.py)
  DETAIL STALE SF13 probe=absent state=present (missing: corpus/QUALITY.md)
  DETAIL STALE SF17 probe=absent state=present (missing: corpus/knowledge/eval-prior-art-calibration.md, …)
  DETAIL STALE SF18 probe=absent state=present (missing: plans/attrib_calibration.py)
  DETAIL STALE SF19 probe=absent state=present (missing: plans/state_check.py)
EXIT_FROM_FLEET_ROOT=1

$ cd / && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round51_surfaces.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
PROBES run=19 present=3 absent=16 errors=0
STALE 10
RESOLVE observed_present=3 floor=13 verdict=violated
PREDICATE R51-C1 fail
EXIT_FROM_ROOT=1
```

Why this matters to the claim, not just to style: the claim's after target is "measured at the
landing tip **in a clean clone**", and the predicate it certifies is `exit 0` + final line
`pass`. With this bug, `present` ranges over `3 … 13` for one fixed tree depending only on the
caller's CWD, and `RESOLVE` can read `violated` on a perfect tree. A reviewer who runs the
documented `--lane <clone>` from anywhere but the clone root records a false fail; worse, a
landing that "fixes" a fail by `cd`-ing is indistinguishable from a real correction. The fix is
one line per kind (`expand` → `lane / expand` for relative targets) and it does not change the
frozen verdict at the lane root. **The frozen command `--lane .` from the lane root is correct
today; the flag does not do what its name implies.** Recommend the L1 either fix the join or
state in the claims that the command is only valid with `cwd == lane`.

### F2 — HIGH — `NUMBER-DRIFT` compares the manifest to the file, never the row to the file; `NUMBER-DRIFT 0` is reachable while the anchored row still lies

`check()` compares `count_claim` with the number in the *probe detail*, and the row text is
never parsed for a number:

```python
if "count_claim" in e:
    m = re.search(r"(\d+)", detail)
    if not m or int(m.group(1)) != int(e["count_claim"]):
        problems["NUMBER-DRIFT"].append("%s row claims %s, probe says %s" % (e["id"], e["count_claim"], detail))
```

Demonstrated on the live tree with a scratch copy of the manifest (lane untouched):

```
$ python3 plans/round51_surfaces.py --lane . --manifest /fast/scratch/…/m-170.json
DRIFT 3
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
$ sed -n '112p' PROVINCE.md | grep -o '25 rows'
25 rows
```

`NUMBER-DRIFT` went to `0` while `PROVINCE.md:112` still says "25 rows". So the C1 predicate
cannot distinguish "the row was corrected" from "the manifest's `count_claim` was edited to
match the file". Consequences the L1 must handle at landing:

- The kill rule's `NUMBER-DRIFT 0` is satisfiable without touching the row. To make the claim
  honest, the landing must (a) record the row's *current* number in `count_claim`, (b) date the
  `:112` cell append-only, and (c) show in the receipt that both moved together. A receipt that
  prints `NUMBER-DRIFT 0` alone is not evidence that the row was corrected.
- Conversely, leaving `count_claim=25` and appending a correction that says 170 will keep
  `NUMBER-DRIFT 1` forever, because the counter reads the row line only. There is no
  append-only path to `NUMBER-DRIFT 0` unless `count_claim` is re-recorded.

### F3 — MEDIUM — the number itself: `corpus/SOURCES.md` holds **170** rows at `4090c3d`; every number `PROVINCE.md` records for it is stale (25 → 37 → 42 → 170)

Four independent primitives on the same file:

```
$ wc -l corpus/SOURCES.md
224 corpus/SOURCES.md
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
170
$ grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md          # the correction's own command
170
$ awk -F'|' '/^\|/ { g=$2; gsub(/^[ \t]+|[ \t]+$/,"",g); if (g ~ /^S[0-9][0-9][0-9]+$/) n++ } END { print n+0 }' corpus/SOURCES.md
170
$ python3 -c "…re.findall(r'^\|\s*S[0-9]{3,}\s*\|', …)"      # the counter's own primitive
170
```

Id census (different primitive again — distinct-set arithmetic, not a line count):

```
row_count=170 distinct=170 min=1 max=177
missing_ids=7 ['S087', 'S088', 'S089', 'S095', 'S096', 'S098', 'S099']
duplicate_ids=0 []
```

Undercount check: `grep -oE 'S[0-9]{3,}' corpus/SOURCES.md | sort -u | wc -l` → `171`; the only
extra token is `S0950268810000385` (an arXiv id inside a quote), i.e. **no registry row hides in
a non-standard shape** — the four row-count primitives are not all missing the same rows.

The document's recorded numbers are therefore all wrong at the tip:

| where | recorded | truth at `4090c3d` |
|---|---|---|
| `PROVINCE.md:112` (SF14 anchor row) | "25 rows" | 170 |
| `PROVINCE.md:119` (round-25 correction) | "holds 37 after round 25" | 170 |
| `PROVINCE.md:189-190` (R26-E9/E10) | "now `rows=42` `id_set=exact`" | 170, id set has 7 gaps |

Note that `plans/state_check.py --summary` already treats `:112` as **SUPERSEDED** (its own
output, run in the scratch clone):

```
SUPERSEDED: P3b.province.public-literature-registry.rows:112 — {… "claim": ["25"]}
SUPERSEDED: P3b.province.round25-correction.rows:119 — {… "claim": ["37"]}
```

so the lane's state machine says "superseded" while the C1 manifest says "NUMBER-DRIFT" and the
document's own latest correction says 42. Three records, three numbers, none of them 170. The
C1 landing must not re-state 42 as current: `SOURCES.md` grew by 128 rows after `f11bffbf`
(history: `822f3b7` "round-50: … git-doc sources S173-S177" is the latest touch). This is a
`## Surfaces`/`### Core` truth defect the manifest sees only as a count; it is also the strongest
single piece of evidence that freshness 8 is the right band.

### F4 — MEDIUM — four probe specs answer a narrower question than the row they anchor (agreement that proves less than it looks)

None of these changes a `state` today; each is a place where a `present`/`absent` verdict is
weaker than the row's assertion. I re-probed the wider assertion for each:

- **(a) SF03 — one endpoint of three.** The row declares `http://127.0.0.1:34113` with
  `/v1/models`, `/health`, `/v1/chat/completions`; the manifest probes `/health` only. `curl` on
  all three: `000` / exit 7 each. Same verdict, and now covering the row.
- **(b) SF07 / SF11 — partial directory sets, one cross-wired dir.** The `## Surfaces` "Own probe
  artifacts" row lists 10 dirs; SF07 probes 5 of them (`round8-horizon`, `round9-replication`,
  `round12-ladder`, `round14-fleet`, **`round13-coverage`** — the last is not in that row; it
  belongs to the `### Core` row). The Core row lists 12 dirs; SF11 probes 7. I `stat`ed all 12:
  every one is a `directory`, all present, so both verdicts hold. The cross-wiring is harmless
  today but means SF07's `present` is partly about a row it does not anchor.
- **(c) SF18 / SF19 — existence probed, exit status asserted.** Both rows assert a command
  (`python3 plans/attrib_calibration.py --summary` / `plans/state_check.py --summary` → exit 0),
  while the manifest probes only `is_file()`. I ran both commands in a `git clone --shared`
  scratch clone at `4090c3d` (`git rev-parse --show-toplevel` == the clone, `git status
  --porcelain` = 0 after the runs): `attrib_calibration.py --summary` → `TOTAL files=9
  scored_files=5 … unique_samples=4 … correct=92 incorrect=0 … mismatches=0`, `EXIT=0`;
  `state_check.py --summary` → `VERDICT: PASS — all comparable frozen assertions match`,
  `EXIT=0`. Both rows are truthful, but the counter would not notice if they stopped exiting 0.
- **(d) SF08 / SF10 — the row's "733 checks" is not probed.** SF08 asserts `python3 grader.py`
  runs offline and SF10 pins the digest; the manifest pins the digest only. Ran in the clone:
  `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully
  re-derives offline` / `EXIT=0`, and `--selftest` → `[selftest] ALL PASS` / `EXIT=0`. The row's
  733 is exact at the tip.

### F5 — LOW — `paths` does not assert type; today no false `present` is hiding there

The counter's `paths` probe accepts any existing inode. `stat -c '%F'` shows every evidence
target is a `directory` and every file target is a `regular file`, so the type-blind probe
agrees with a type-checking one on all 13 `paths` entries. A future file-for-directory swap
would read `present` silently.

### F6 — LOW — `--selftest` prints intentional `PREDICATE R51-C1 fail` lines to stdout

In a scratch clone at `4090c3d`:

```
$ python3 plans/round51_surfaces.py --selftest
PREDICATE R51-C1 fail          <- from the last intentional-fail case, not the selftest verdict
[selftest] cases=9 failures=0
[selftest] ALL PASS
EXIT=0
```

The selftest is honest (9 cases, 0 failures) but any harness that greps the last `PREDICATE` line
over a selftest transcript reads `fail`. The counter's own selftest therefore cannot be used as a
C1 control receipt as-is; capture `[selftest] ALL PASS` and `EXIT=0` instead.

### F7 — LOW (frontier note, not a counter defect) — `:8793` is live, and the SF16 row says it was not probed

`ss -ltnp` at measurement: `127.0.0.1:8793` is `LISTEN`, `users:(("python3",pid=1516,…))`, and
`/proc/1516/cmdline` is `/usr/bin/python3 /home/vgpnk/.local/share/glm-flash-shim/shim.py`. The
SF16 row records "`:8793` not probed this round". Not scored by C1 (undeclared), reported because
the claim's after target adds "one new declared surface (the live served endpoint found this
round)": `:8793` is a shim listener, and the live model servers on this host are on other ports
(`llama-server` on `127.0.0.1:1234`, `127.0.0.1:37323`, `127.0.0.1:45669`), none of which is
`:34113`. Whatever endpoint the landing declares, it should be one of those measured listeners,
and its port must be probed with `ss`/`nc` and its identity with `/proc/<pid>/cmdline` — the
socket primitive alone cannot tell a shim from a model server.

## What I did not measure (limits)

- I did not audit the 19 `prose` readings row by row beyond the subpath/endpoint widening in
  §F4 — that is the critic seats' assignment; I only checked that no `state` value disagrees
  with an independent primitive.
- Endpoint/port probes are point-in-time single shots at `4090c3d`; `:34113` was absent under
  three primitives and may return, which would legitimately flip SF03 to `STALE` (the claims
  call this intended behaviour).
- I did not run `--run-checks` or touch `corpus/routed-findings.jsonl` (C2 belongs to other
  seats), did not edit any production file, and did not run any mutating git command. The
  scratch clone was `git clone --shared` and stayed `dirty=0`.
- `wc -l` on `corpus/SOURCES.md` (224) is a file-shape datum, not a row count; the row count is
  the four agreeing primitives in §F3.
- No tool was installed or upgraded for this seat (nothing was needed; PACMAN guard untouched).

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C1RevProbes` (`TMPDIR` exported there, free space
seen at start: `804G total, 249G used, 555G avail, 31% on /fast`) held one `git clone --shared`
lane, two id-set files and one manifest copy. Removed before yield; the removal is verified in
the transcript and no citable evidence lives in it — every output above is quoted inline.

VERDICT: C1 re-probe — 19/19 surfaces independently confirmed, 0 primitive disagreements; the
frozen predicate's before-state reproduces exactly (`DRIFT 3`, `UNVERDICTED 1`, `NUMBER-DRIFT 1`,
`STALE 0`, `RESOLVE 13/13`, exit 1). Two instrument defects block a trustworthy *after*
measurement and must be fixed or disclosed by the L1: (F1) lane-relative targets resolve against
CWD, so the same tree reads `present=3 … 13` and `RESOLVE violated` off the lane root; (F2)
`NUMBER-DRIFT` never reads the row, so `NUMBER-DRIFT 0` is reachable while `PROVINCE.md:112`
still says "25 rows" (demonstrated: `count_claim=170` → `NUMBER-DRIFT 0`, row unchanged).
Freshness truth at the tip: `corpus/SOURCES.md` = 170 rows (S001–S177, 7 ids missing, 0
duplicates) against recorded 25/37/42 — three stale records, none current. Recommend: fix the
lane join, re-record `count_claim` with the row edit in the same receipt, and widen SF03/SF07/
SF11 probe specs to the rows they anchor.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
