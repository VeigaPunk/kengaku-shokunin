# C1RevRerun — independent re-run of the frozen C1 command at the stage-1 freeze

Seat: `C1RevRerun` (reviewer), round 51, hyaku run 11, 2026-10-28.
Item: re-run `python3 plans/round51_surfaces.py --lane .` in a **clean clone** of the stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c` and byte-diff its output against the committed receipt
`.ufo/waves/round-51/claims/c1-before.txt`, reporting byte-level differences and the exit code,
**without reading the receipt before my own run** (the first run below preceded any read of it).

## Axes named

- **A1 — freshness / reproducibility of the C1 before-receipt**: can an independent seat, from a
  clean clone at the freeze, reproduce the recorded before-measurement of `PROVINCE.md`'s declared
  surfaces?
- **A2 — revision attestation**: does the counter's `REV` line name the tree that was measured?
- **A3 — instrument determinism**: is the counter stable run-to-run and does its own selftest hold?

Judged axis of this seat: **freshness**. No production file was edited; this seat is read-only
against the lane apart from this report.

## Scratch and clean-clone discipline

- Scratch root `/fast/scratch/hyaku/kengaku-r51/C1RevRerun`, `TMPDIR` exported to it.
  `df -h /fast` at start: `/dev/nvme1n1p2 804G 249G 555G 31% /fast`.
- Clone used for the measured run: `git clone --shared <LANE> <scratch>/lane` then
  `git -C <scratch>/lane checkout e07f131…`; `git -C lane rev-parse --show-toplevel` printed
  `/fast/scratch/hyaku/kengaku-r51/C1RevRerun/lane`, `git -C lane status --porcelain` printed
  nothing (clean tree) before the measured run.
- `lane2` and `lane3` are fixture clones, each verified with `rev-parse --show-toplevel` equal to
  its own path before any ref write. Their only writes were local `update-ref refs/heads/master`
  pins inside scratch, used to isolate the `REV` line (see F1).
- Scratch tree removed before yielding (see §Scratch cleanup at the end).

## Commands run and observed output

### 1. The frozen command, clean clone at the freeze (measured run, first run, receipt unread)

```
cd /fast/scratch/hyaku/kengaku-r51/C1RevRerun/lane
python3 plans/round51_surfaces.py --lane .   # EXIT=1
```

Verbatim stdout (stderr empty):

```
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
```

Every headline number in `plans/round-51-claims.md` §C1 **Before** is reproduced exactly:
`ANCHORS 19/19`, `ROWS 9+10`, `PROBES present=13 absent=6`, `DRIFT 3` (SF01/SF02/SF03),
`UNVERDICTED 1` (SF04), `NUMBER-DRIFT 1` (SF14 25 vs 170), `RESOLVE 13/13 met`,
`PREDICATE R51-C1 fail`, **exit 1**.

### 2. Byte-diff against the committed receipt

```
wc -lc receipt ->  21 940   receipt
wc -lc run1.txt -> 21 940   run1.txt
sha256 receipt  = 6f862e3cbd13759875c822391c2f2d0c743e756abcfac986556aaa9c977c7624
sha256 run1.txt = bd8a01de70a900d62aa8d059c8251a5c616c4171ce954d84dcde4392c0f06733
cmp receipt run1.txt -> differ: char 5, line 1   (CMP_EXIT=1)
diff -u receipt run1.txt:
-REV 297e17927ba9342a87ba27a48cc5270a001de7cb
+REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

**Byte-level result: exactly one differing line out of 21 — line 1, the `REV` line.** The other 20
lines (including all three `DETAIL DRIFT` texts, the `DETAIL UNVERDICTED`, the `DETAIL NUMBER-DRIFT`
text, every zero counter, `RESOLVE`, and the final `PREDICATE R51-C1 fail`) are byte-identical.
Both files are 21 lines / 940 bytes; the byte counts coincide only because both revisions are
40-hex hashes, so `wc` equality is not evidence of equality — `cmp`/`diff` is.

### 3. Why the `REV` line differs (A2)

`tip_rev()` runs `git -C <lane> rev-parse master` — the *branch ref of the clone*, not the
checked-out commit. In the measured clone: `git -C lane rev-parse master` =
`4090c3db79d11279ab5e5121ba25e74aa316e6e7`, `git -C lane rev-parse origin/master` = same,
`git -C lane rev-parse HEAD` = `e07f131cf7037e58a21db6e1f3986cf401ad257c` (detached at the freeze).
The lane's `master` advanced after the freeze:

```
4090c3d round-51: v2 wave spec (64 seats) + validated dispatch payload
e07f131 round-51: stage-1 freeze — C1 surface-truth counter+manifest, C2 routing counter, claims, before receipts
297e179 round-50: receipt notes — the scratch FENCE path is not load-bearing, the committed digests are
```

Two isolating fixtures (scratch clones only):

- `lane2`: tree at `e07f131`, `refs/heads/master` pinned to `e07f131` → output identical to run 1
  except `REV e07f131…`. So the `REV` value is a pure function of the branch ref.
- `lane3`: tree at `e07f131`, `refs/heads/master` pinned to the base tip `297e179…` →
  `cmp receipt run_freezetree_baseREV.txt` **CMP_EXIT=0**, sha256 **identical**
  (`6f862e3c…c7624` for both). This is the decisive control: the receipt's *measurement* is exactly
  reproducible from the freeze tree, and the sole byte difference is the ref-derived `REV` line.

- `lane2` with a mutated copy of `PROVINCE.md` passed via `--province` (clone tree untouched,
  `git status --porcelain` empty): `REV e07f131…` **unchanged** while
  `ANCHORS total=19 dup=0 missing=1`, `ANCHOR-MISSING 1`
  (`SF01 anchor not found: | Research notes (SSOT for eval craft) |`), `UNCOVERED 1`
  (`## Surfaces row line 12 has no manifest entry`). So `REV` does not bind the measured content.

### 4. Determinism and selftest (A3)

Three consecutive runs at fixed host state: sha256 `bd8a01de…f06733` for all of `run1/run2/run3`,
`EXIT=1` each, `diff` between them empty (`IDENTICAL_1_2`, `IDENTICAL_1_3`).

`python3 plans/round51_surfaces.py --selftest` → `[selftest] cases=9 failures=0`,
`[selftest] ALL PASS`, `SELFTEST_EXIT=0`. The selftest's own runs print `REV unknown` (its tmpdir is
not a repo), consistent with the `tip_rev` fallback.

### 5. Base-tip reproducibility of the *claims' wording* (A1)

```
git -C lane3 cat-file -e 297e179…:plans/round51_surfaces.py
  -> fatal: path 'plans/round51_surfaces.py' does not exist in '297e179…'
git -C lane3 ls-tree --name-only 297e179… plans/ | grep round51  -> (no round51 files)
python3 plans/round51_surfaces.py --lane .   # clean checkout of 297e179…, EXIT=2
  stderr: python3: can't open file '…/lane3/plans/round51_surfaces.py': [Errno 2] No such file or directory
```

`PROVINCE.md` is byte-identical across the two commits
(`git rev-parse 297e179…:PROVINCE.md` = `git rev-parse e07f131…:PROVINCE.md` = `a1492cdd46c2…`),
and the stage-1 commit adds only the instruments, manifest, claims and receipts
(`git diff --stat 297e179… e07f131…` → 6 files, 1063 insertions, `PROVINCE.md` untouched).

### 6. Probe scope census (A1, residual risk)

Manifest census (`plans/round51-surfaces.json`, 19 entries, `resolve_floor` 13,
sections `## Surfaces` / `### Core`), probe kinds `paths=13 http=1 sha256=3 count=1 port=1`:

- **host-global, outside the clone (8/19):** SF01, SF02, SF04, SF05, SF06 (`$HOME` paths),
  SF03 (`http://127.0.0.1:34113/health`), SF15 (`sha256 ~/.local/share/ds-flash-shim/shim.py`),
  SF16 (`port 8791`).
- **tree-relative (11/19):** SF07–SF14, SF17–SF19.

Zero-interference demonstration (no host port touched, no sibling measurement disturbed): with
`HOME=<scratch>/fakehome` populated with the five `$HOME` targets and without the shim:

```
HOME=<scratch>/fakehome python3 plans/round51_surfaces.py --lane .   # EXIT=1
PROBES run=19 present=17 absent=2 errors=0
STALE 6
  DETAIL STALE SF01 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF02 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF04 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF05 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF06 probe=present state=absent (all 1 targets resolve)
  DETAIL STALE SF15 probe=absent state=present (missing file ~/.local/share/ds-flash-shim/shim.py)
RESOLVE observed_present=17 floor=13 verdict=met
```

Tree and `REV` unchanged; only host-visible inputs moved. (I deliberately did **not** bind
`:34113` to test SF03 — sibling seats are probing that port concurrently and a listener would
corrupt their measurements.)

### 7. Dead diagnostic

`grep -n errors plans/round51_surfaces.py` → line 190 `present = absent = errors = 0`, line 209
prints it; **no increment anywhere**. `PROBES … errors=0` can never be nonzero: an unknown probe
kind raises `SystemExit`, and every `http`/`port` failure is folded into `absent`. The field is not
evidence.

## Findings for the L1 (production files are yours to land; I edited nothing)

**F1 — MEDIUM, revision attestation (A2).** `tip_rev()` uses `git rev-parse master`, so the `REV`
line names a branch ref, not the measured tree. Consequences, all fixture-proven above:
(a) a clean clone at `e07f131` prints `REV 4090c3d…`, a post-freeze commit whose tree was never
measured; (b) the line stays fixed while the measured content changes; (c) the receipt reproduces
byte-identically only when `master` is pinned to the base tip. The C1 **after** measurement at the
landing tip is therefore self-attesting only if `master == HEAD` at run time — true if you commit to
`master` before measuring, false in a detached worktree or if `master` lags the measured commit.
Suggested (your call): print both, e.g. `REV <HEAD> ref=<branch-tip>`, and state the measured
commit hash explicitly in the after-receipt narrative.

**F2 — MEDIUM, claims wording vs reproducibility (A1).** `plans/round-51-claims.md` §C1 says the
before was "measured with this command at the base tip". At commit `297e179` the instrument and
manifest do not exist in the tree: a clean checkout yields `EXIT=2`, `python3: can't open file
'…/plans/round51_surfaces.py'`. The before is reproducible only from the stage-1 freeze tree
`e07f131` (or from an uncommitted working tree at the base tip, which is evidently how it was
produced). The measurement itself is unaffected — `PROVINCE.md` is blob-identical across the two
commits, and the freeze tree reproduces the receipt byte-for-byte (§3). Tighten the sentence at
landing: "measured at the base tip's `PROVINCE.md`, committed as receipt in the stage-1 freeze".

**F3 — MEDIUM/LOW, point-in-time probes (A1).** 8 of 19 entries are decided by host state outside
the lane clone (§6), so "measured at the landing tip in a clean clone" reproduces only 11/19 probes.
`plans/round-51-claims.md` §Limits declares point-in-time behaviour for *endpoints* only; the five
`$HOME` path rows and the `ds-flash-shim` digest carry the same property undeclared. Residual risk
for the after measurement: a `STALE` caused by `~/.local/share/ds-flash-shim/shim.py` being edited,
`~/archive/bench-arena` moving, or `~/.bailian/*` appearing — none of which is a C1 defect, but any
of which fails the predicate. Record the host fingerprint (or re-probe the same 8 immediately before
landing) in the after-receipt.

**F4 — none, positive.** The counter is deterministic (3/3 identical runs), its selftest passes
9/9, and its before-receipt is honest: the freeze tree reproduces it byte-for-byte with the ref
pinned. The recorded exit code is correct (1).

**F5 — LOW, dead diagnostic.** `errors` (§7) is always 0 and cannot fail. Either increment it on
probe exceptions or drop it from the `PROBES` line so the line stays evidence.

## Limits of this seat

- I did **not** audit the `prose` readings of the 19 rows against `PROVINCE.md` (that is the prose
  seats' item), nor the manifest's `state` choices, nor the SF14 count pattern's correctness.
- I did not measure the C1 **after** state (nothing has landed) and did not touch C2.
- `--run-checks`/`round51_routing.py` untouched.
- Only three fixture clones in scratch; the base-tip pin in `lane3` is a local ref write inside
  scratch, disclosed in §Scratch and §3.
- No tool was installed or upgraded in this seat (no package manager invoked; `python3` and `git`
  were already present).

## Scratch cleanup

`/fast/scratch/hyaku/kengaku-r51/C1RevRerun` was removed after this report was written; all
evidence it held is transcribed verbatim above. `ls` of the scratch root after cleanup is recorded
in the seat's yield. No scratch tree left on disk.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c (tree measured; counter printed `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` from the clone's `master` ref — see F1)

VERDICT: REPRODUCED — the frozen C1 before-measurement reproduces at the stage-1 freeze in a clean clone with exit 1 and 20/21 lines byte-identical to the committed receipt; the single differing line is the ref-derived `REV` line (`4090c3d…` from the clone's `master` vs the receipt's `297e179…`), eliminated to a byte-identical sha256 by pinning `master` to the base tip, which proves the difference is attestation (F1), not measurement. F2 (claims' "at the base tip" wording is not reproducible from that commit — the instrument does not exist there), F3 (8/19 probes are host-global, so the after measurement can go STALE for reasons unrelated to the claim) and F5 (dead `errors` field) are routed to the L1 for landing; none of them changes the recorded before-numbers or the exit code.
