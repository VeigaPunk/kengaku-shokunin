# R48C1ExecCounter — v3 counter candidate for R48-C1 (calibration)

Seat `R48C1ExecCounter` (executor). Claim served: **R48-C1**. I do not claim C1 or C2 admission; this seat delivers
the measuring instrument, its measured selftests, and the one measured deviation the stage-2 amendment must
reconcile.

## Axes named

Primary: **calibration**. Instrument axes iterated (cheap, in parallel; a move was kept only if it improved one
axis and harmed none):

| # | axis | move | measured effect |
|---|---|---|---|
| 1 | honest-leg faithfulness | cut the leg over to the population seat `R48C1ExecHonest` delivered (16 novel module files + 104 battery), pinned by digest, and deleted my earlier 9 embedded reconstructions | `PINS total=82`, `HONEST fixtures=120`, `HONEST-POP battery=104 novel=16` |
| 2 | classification correctness | `kind_of()` per fixture (LEAK / BENIGN-ADMIT / READ / HUNG / ERROR), `module_rollup()` per module, `HONEST_NOVEL_EXPECTED` binding the novel half | admit-all prints `clean=0`, not `clean=20` |
| 3 | envelope retention (B1/B3/B4/B5/B6) | call the round-46 counter's `run_fence`/`analyse`/`build_module` instead of copying them | peeking stubs produce `read=20` / `leaked=20`, `contradicted=32` |
| 4 | pin / non-vacuity | pin the round-46 contract by digest, every hostile input, every novel honest module; fatal on unpinned or missing population | three tamper/unpinned probes and a novel-count literal all fire |
| 5 | satisfiability of the pass line | a probe fence that decides entirely inside `d` | `PREDICATE R48-C1 pass`, exit 0, clean clone |

Rejected moves (tested, not kept): folding hostile BENIGN-ADMITs into `clean` (makes an admit-all fence print
the frozen line — measured, see the reading note); counting `ERROR` as `leaked` (mislabels; it is kept out of
LEAK and READ and is fatal on its own `ERRORS` line); keeping my 9 embedded honest classes alongside the
delivered 16 (two populations can reach `novel=16` mixed, so one of them would have to be silently trusted —
deleted instead).

## Freeze check (before any measurement)

- Stage-1 freeze is in the committed tree: `git ls-tree -r --name-only a543d920 plans/` lists
  `plans/round-48-claims.md`; `git show a543d920:plans/round-48-claims.md | sha256sum` =
  `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672` = working copy; `git log --oneline
  a543d920..HEAD -- plans/` is empty.
- Stage 2 does **not** exist yet: `plans/round48_c1_verify.py`, `plans/honest48/`, `plans/sealed48/` are not in
  the lane, and no stage-2 amendment commit exists. **No scored counter/probe execution was made on claimed
  work**, and none is reported. Every run below is a selftest on a `git clone --shared` of the frozen base
  `a543d920`, some with a scratch fence via the testing-only `--fence` override. No run is a receipt for R48-C1.
- Measurement revisions are named by each run's `REV` line: `abb08e2…` (candidate + 16-module population
  committed, base fence), `128b533…` (same + probe fence committed, default mode). Both are scratch-clone
  revisions, not lane revisions, and are not offered as lane revisions.

## Deliverable

`plans/round48_c1_verify.py` — **433 lines, sha256
`8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`** (full text in Appendix A; the bytes must
survive this seat's scratch cleanup, which is why the appendix exists). Scratch path while alive:
`/fast/scratch/hyaku/kengaku-r48/R48C1ExecCounter/cand/round48_c1_verify.py`; a read-only copy went to the
controls seat at `/fast/scratch/hyaku/kengaku-r48/R48C1ExecControls/inbox/round48_c1_verify.v2.py`.

Stage-2 literals already filled and measured (not placeholders):

| literal | value | meaning |
|---|---|---|
| `REFUSAL_FLOOR` | 20 | frozen `plans/refusals46/` modules, exact |
| `SEALED_FLOOR` | 12 | frozen `plans/sealed46/` modules; must grow by `len(plans/sealed48/*.py)` at stage 2 |
| `HONEST_BATTERY` | 104 | the standing batteries |
| `HONEST_NOVEL_EXPECTED` | 16 | novel fixtures: 9 `r46novel` (n01-n09) + 7 `novel48` (n10-n16) |
| `HONEST_TOTAL` | 120 | `<H>` = 104 + 16 |
| `PINS_EXTRA` | 16 entries | `plans/honest48/<name>.py` digests, verified against seat R48C1ExecHonest's `modules.sha256` |
| `PINS total` | 82 | 65 round-46 pins + the round-46 counter itself + the 16 novel modules |
| `advertised` | 32 | 20 + 12 |

Contract compliance against `plans/round-48-claims.md` §C1: imports `plans/round46_c1_verify.py` with
`R46_PIN = ef19380e…` verified **before** the module executes (a mismatch is `SETUP … exit 2`); (a) honest leg as
above; (b) BENIGN-ADMIT classification; (c) Q39 name hiding retained by calling `k46.build_module` (per-run
tokens, `PAD=24`, shuffled build and run order); (d) B1/B3/B4/B5/B6 retained by calling `k46.run_fence`; (e)
REFUSALS 20 / SEALED 12 + extras; `REV` first line; `--literals` prints the stage-2 paste block.

### Frozen-line reading (recorded, never re-frozen)

`BENIGN-ADMIT` classifies a fixture; it is not a bucket in the four frozen counts. A hostile module is `clean`
only when every fixture it claims was **refused with zero traced outside access**, so a BENIGN-ADMIT on a hostile
leg leaves `clean<total` and the frozen line cannot print, even though it is never counted in `leaked`. This is
forced by the predicate itself: if benign admits were folded into `clean`, an admit-all fence would print
`REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0` and `CALIBRATION … contradicted=0` and pass —
measured false (`admit_all` below prints `clean=0`). The frozen kill rule ("any SEALED module with traced outside
access admitted → not admitted") is therefore a necessary condition and the predicate line stricter; the counter
is stricter than the kill rule and never looser. `ERROR` is neither LEAK nor READ: it is reported on
`ERRORS total=<n>` and is fatal. `BENIGN total` counts fixtures over all three legs (a passing run has
`BENIGN total=120`, all of them honest admissions).

## Exact commands and observed outputs (verbatim)

Setup per clone: `export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1ExecCounter`;
`git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`;
`git checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`; clone top level asserted with
`git -C "$D" rev-parse --show-toplevel` = `$D` before every fixture commit; then in the clone
`cp <candidate> plans/round48_c1_verify.py`, `mkdir -p plans/honest48`, and
`cp …/w1/R48C1ExecHonest/modules/r46novel/*.py …/modules/novel48/*.py plans/honest48/` (16 files).
Run form: `cd <clone> && python3 plans/round48_c1_verify.py --lane . [--fence <stub>]`.
Each run builds 66 modules (20 refusal + 12 sealed + 38 honest) and makes 169 fence runs in 8–14 s (`--jobs 8`).

### 1. Base fence (the before value), default mode, REV `abb08e2`, TREE clean

```
REV abb08e283a0eba0eb469fbc8d2f4d7cb2f49c359
TREE clean
PINS total=82 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=16 expected_novel=16 novel_modules=16
BENIGN total=112
CALIBRATION advertised=32 contradicted=0
REASON honest-not-admitted
PREDICATE R48-C1 fail
```
exit 1. The eight honest refusals, verbatim:

```
FENCE-RUN honest honest48/n03_detached_head.py n03-detached-head BREACH clean touches=0 calls=444 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest honest48/n07_reflog_gc.py n07-reflog-gc BREACH clean touches=0 calls=465 -- BREACH repo/.git/info/refs is not git's exclude file
FENCE-RUN honest honest48/n08_tag_detached.py n08-tag-detached BREACH clean touches=0 calls=444 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest honest48/n12_local_config_user.py n12-local-config-user BREACH clean touches=0 calls=445 -- BREACH repo/.git/config section [user] is not allowlisted
FENCE-RUN honest honest48/n13_remote_origin.py n13-remote-origin BREACH clean touches=0 calls=445 -- BREACH repo/.git/config section header b'[remote "origin"]' is not plain
FENCE-RUN honest honest48/n14_stash_entry.py n14-stash-entry BREACH clean touches=0 calls=472 -- BREACH refs/stash has a name git does not write
FENCE-RUN honest honest48/n15_commit_graph.py n15-commit-graph BREACH clean touches=0 calls=494 -- BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
FENCE-RUN honest honest48/n16_notes_ref.py n16-notes-ref BREACH clean touches=0 calls=470 -- BREACH refs/notes has a name git does not write
```

### 2. The frozen "must fail" controls (all `--fence`, REV `abb08e2`)

```
-- admit-all (def breach(d, argv, tool): return None) --
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
BENIGN total=169
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean
PREDICATE R48-C1 fail
-- refuse-all --
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=120 read=0 hung=0 build_errors=0
BENIGN total=0
CALIBRATION advertised=32 contradicted=0
REASON honest-not-admitted
PREDICATE R48-C1 fail
-- no fence (--fence at a missing path; every fixture ERROR, touches=0) --
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=0 read=0 hung=0 build_errors=0
ERRORS total=152
REASON refusals-not-clean,sealed-not-clean,honest-not-admitted,errors=152
PREDICATE R48-C1 fail
```

### 3. Envelope legs (B3 whole-root scope, B5 stat channel, B4 verdict channel)

Stubs `os.listdir`/`stat` `d.parent` (inside the counted scratch root, outside `d`) before deciding:

```
-- peek_refuse.py (peeks, then refuses) --
REFUSALS total=20 clean=0 leaked=0 read=20 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=12 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=120 read=120 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=32
REASON refusals-not-clean,sealed-not-clean,honest-not-admitted,contradicted=32
PREDICATE R48-C1 fail
-- peek_admit.py (peeks, then admits) --
REFUSALS total=20 clean=0 leaked=20 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=12 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=0 read=120 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=32
REASON refusals-not-clean,sealed-not-clean,honest-not-admitted,contradicted=32
PREDICATE R48-C1 fail
```

### 4. Satisfiability of the frozen pass line

(a) Probe with the three GC/HEAD shapes only: `HONEST fixtures=120 admitted=116 refused=4` — refusals
`n12 (config section not allowlisted)`, `n13 (config section)`, `n14 (refs entry)`, `n16 (refs entry)`, i.e. the
config/refs shapes the base and the three-shape probe both refuse.

(b) Probe v2 (adds `[user]`, `[remote "<n>"]`/`[branch "<n>"]`, `refs/notes/**`, `refs/stash`), **default mode
with the probe committed**, REV `128b533`, TREE clean:

```
REV 128b5331a075c27263c51c4b3021e23de2ee33e7
TREE clean
PINS total=82 mismatched=0
FENCE source=…/landD/plans/fixture_fence.py sha256=1e04fa75f1584c9b58df0c5e61d7eadafb27bc442faa1b1b4c37b2d89b8d8953
COPY f1_gitfile.py ok            (… ten COPY rows ok …)
MODULES refusal total=20
MODULES sealed total=12
MODULES honest total=38
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=16 expected_novel=16 novel_modules=16
BENIGN total=120
CALIBRATION advertised=32 contradicted=0
REASON -
PREDICATE R48-C1 pass
```
exit 0, with `touches=0` on all 169 fence runs. The probe starts no git child and names nothing outside `d`; it is
**not** a landing candidate (Appendix B). Independently, seat `R48C1ExecFenceA` reports its own variant admits
all 120 population fixtures with `touches=0`, refusals 34/34 fixtures, sealed 15/15 (peer message, not verified by
me).

### 5. Pin and non-vacuity probes (default mode, REV `abb08e2`)

```
-- an extra file dropped into plans/honest48/ --
PINS total=82 mismatched=1 first=plans/honest48/n99_extra.py:unpinned
HONEST fixtures=121 admitted=113 refused=8 read=0 hung=0 build_errors=0
REASON pins=1,tree-dirty=1,honest-novel=17!=16,honest-fixtures=121!=120,honest-not-admitted
PREDICATE R48-C1 fail
-- one line appended to a pinned novel module --
PINS total=82 mismatched=1 first=plans/honest48/n12_local_config_user.py
REASON pins=1,tree-dirty=1,honest-not-admitted
PREDICATE R48-C1 fail
-- (earlier build) one line appended to plans/round46_c1_verify.py --
SETUP plans/round46_c1_verify.py sha256=aa2ceaa7… is not the pinned ef19380e…, exit 2, no build, no fence run
```
and the stage-2 helper, with the 16 modules present:

```
PINS total=82 mismatched=0
LITERALS refusals=20 sealed_frozen=12 sealed_extra=0 honest_battery_modules=22 honest_battery_fixtures=104 honest_novel_modules=16 pins_extra=16
LITERALS-TO-PASTE REFUSAL_FLOOR=20 SEALED_FLOOR=12 HONEST_TOTAL=120
PIN "plans/honest48/n01_packed_refs.py" "9e1a2058e326781e0fb7007f041c2f13caa21b93fbd9cea6f668eb3765dac853"
… (16 PIN lines) …
```

## Deviation the stage-2 amendment must reconcile

The round-46 seat reported 9/9 novel honest classes refused by the base fence (`R46W2C1HoHonest.md`: "Thus
**9/9 were refused**, with no outside touches."). **That is not reproducible from the `w2` prose**, and both
independent reconstructions agree on that: seat `R48C1ExecHonest`'s delivered `r46novel` half is refused 3/9 by
the base fence (`n03`, `n07`, `n08`), and my own earlier rebuild (4/9, cut over and deleted) refused the same
family plus `n01`. Only that seat's counter output survived; its modules and builds did not. Combined with the
seven round-48 classes, the measured before value on the frozen 120-fixture population is:

**`HONEST fixtures=120 admitted=112 refused=8`** — the whole base-fence over-refusal, and it is narrower than the
`w2` text: 40-hex detached `HEAD`, `.git/info/refs` (written by `pack-refs`/`gc`), `objects/info/commit-graph`,
`[user]`, `[remote "<n>"]`, `refs/stash`, `refs/notes`.

Consequence for the frozen do-nothing control, which says the base-fence receipt should show "`HONEST …
refused=9` minimum": the *requirement* (the base fence must print `PREDICATE R48-C1 fail` on the honest leg) holds
— measured, §1 — but the `refused=9` literal does not. The L1 must, inside the stage-2 amendment window and
before any scored run, record the measured `refused=8` as the before value (a population/literal record), not
re-word the predicate, the kill rule or the control's requirement. I have told the controls seat to expect
`refused=8` and to report it rather than reproduce 9.

## Stage-2 handoff (mechanical)

1. `git add plans/round48_c1_verify.py` (Appendix A bytes; verify sha256 `8726e99b…`).
2. `mkdir plans/honest48 && cp …/w1/R48C1ExecHonest/modules/r46novel/*.py …/modules/novel48/*.py plans/honest48/`
   — the 16 digests already in `PINS_EXTRA` were taken from exactly those files and each matches
   `modules.sha256`; run `--literals` and require `PINS total=82 mismatched=0`.
3. `plans/sealed48/`: add the wave-1 held-out hostile modules, then set
   `SEALED_FLOOR = 12 + len(plans/sealed48/*.py)` and paste their `PIN` lines into `PINS_EXTRA`
   (`PINS total` becomes `82 + n`); `--literals` prints both.
4. Only after 1–3 are committed: run `python3 plans/round48_c1_verify.py --lane .` on a clean clone of the landing
   tip (the predicate is bound to a clean tree; a dirty tree fails in frozen mode).
5. Ordering (Q30): no scored run before the stage-2 commit; `--fence`, `--honest`, `--refusals`, `--sealed`,
   `--seed` runs are testing only and never a receipt for R48-C1.

## Limits (named)

1. `--literals` is a *helper*, not a predicate: it prints what the tree holds, so a stage-2 amendment that pastes
   its own numbers cannot be distinguished from a correct one by the counter — the controls seat and a critic must
   read the stage-2 diff (this file has exactly one editable block, `REFUSAL_FLOOR`/`SEALED_FLOOR`/`HONEST_*`/
   `PINS_EXTRA`; nothing else in it is literal).
2. Inherited envelope: `io_uring` SQE opens/reads emit no traced syscall; host paths outside the scratch root are
   not counted (a fence may still read `/etc`, `/proc`, `/sys`); a directory `stat`'s `st_nlink` channel is nulled
   by `PAD` padding, not measured; a module that builds no fixture is a `build_errors` module, never clean.
3. `BENIGN total` is a fixture count; module granularity is on `BENIGN-MODULES`. `CALIBRATION contradicted`
   keeps the round-46 formula (leaked+read+hung+build_errors over both hostile legs) and does not include benign
   admits — those are caught by `clean<total`.
4. Honest-leg `refused` counts every BREACH and `read` counts every fixture with any outside touch, so the two
   overlap for a refused-but-peeking fence (round-46 semantics retained).
5. The honest population's battery half (104 fixtures) is pinned only through the round-46 pin table; its novel
   half is pinned in `PINS_EXTRA`. `HONEST_NOVEL_EXPECTED` binds the novel fixture count, `HONEST_TOTAL` the sum.
6. Known flake in a frozen fixture: `plans/refusals46/f16_objects_hardlink_out.py` hardlinks every file under
   `objects/`, so a git maintenance lock appearing mid-build can fail it (`BUILD-ERROR … maintenance.lock …`,
   `build_errors=1` on the refusal leg). Observed once in ten selftest runs today; it fails loudly (never a pass). Retry
   once at stage 2 rather than editing the frozen module.

## Risks / blockers

- **Population provenance is settled, the control literal is not.** `plans/honest48/` content comes from a wave-1
  seat's deliverable, so the L1 is committing another seat's bytes: the `PINS_EXTRA` digests are my verification
  of that handoff, not an endorsement of its class authorship (critic seats `R48C1Ho*` own that).
- **Cross-seat observation, not verified here:** `R48C1ExecFenceA` reports its variant refuses fixtures that
  cross a mount boundary. The frozen C1 text says an honest fixture whose store sits on a mount boundary inside
  `d` is admitted iff every byte the decision reads is inside `d`. If that variant lands unchanged, an honest
  mount-boundary fixture would be refused and the HONEST leg would fail — worth a critic check before landing.
- **`plans/sealed48/` is empty**, so `<S> = 12` today; the frozen `<S>` must include the wave-1 hostile modules
  authored against the landed fence, or the sealed leg under-reports.
- Selftest only: nothing here measures the landing tip and nothing here admits or refuses R48-C1.

## Sources opened (local; this seat opened no network source)

| source | sha256 (16) | accessed | located quote (≤25 words) |
|---|---|---|---|
| `plans/round-48-claims.md` | `87e6075ff2c0748b` | 2026-10-27 | "(a) **honest population frozen at stage 2** = the 104 fixtures of `plans/battery42\|43\|44` + the 9 round-46 novel honest classes" |
| `corpus/lessons/round-46-verifier-spotcheck.md` | `130035fe1e5a7d1f` | 2026-10-27 | "repair over-refusal (9/9 novel honest controls refused) and broaden positive controls" |
| `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` | `7590690ae18bef92` | 2026-10-27 | "Thus **9/9 were refused**, with no outside touches." |
| `plans/round46_c1_verify.py` | `ef19380e862e0a6d` | 2026-10-27 | "must all be ADMITTED with no outside touch" |
| `plans/round44_c1_verify.py` | `6cf05323bafa9cdb` | 2026-10-27 | "for k, fx in enumerate(getattr(mod, \"FIXTURES\", []))" |
| `plans/fixture_fence.py` | `05d5fe03aa3be6b7` | 2026-10-27 | "the shape a plain `git init` + commits writes inside `d`" |
| `plans/battery42/a_class.py` | `eef02b5df0a8b5e7` | 2026-10-27 | "\"fid\", \"tool\", \"expect\", \"defects\", \"build\"" |
| `.ufo/waves/round-48/w1/R48C1ExecHonest/modules.sha256` | `51bfcfc4c9e6b664` | 2026-10-27 | "9e1a2058…  r46novel/n01_packed_refs.py" (digest rows, cross-checked by me) |
| `.ufo/waves/round-48/w1/R48C1ExecHonest/population.txt` | `70804edeaaf7bc29` | 2026-10-27 | "columns: HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>" |
| `.ufo/waves/round-46/w2/` listing | — | 2026-10-27 | directory listing only |

Lane state was read, never written: no lane file, `plans/*`, `corpus/*`, `SCORECARD.md`, `LOG.md`, `MANIFEST.json`,
`.ufo/state` or sibling repo was modified; no commit, push, or mutating git/jj ran outside my scratch clones, and
every fixture git call ran inside a clone with `git -C "$D"` after asserting its top level.

## Scratch

`/fast/scratch/hyaku/kengaku-r48/R48C1ExecCounter` (clones `lane`, `landA`-`landD`; `cand/`, `stubs/`, `out/`) is
**removed before this seat yields**, after the receipts above were transcribed here and the two source files were
embedded as Appendix A/B.

VERDICT: v3 counter candidate delivered — 433 lines, sha256 `8726e99b…`, stage-1 freeze verified, zero scored runs
on claimed work. On the frozen 120-fixture population (104 battery + seat R48C1ExecHonest's 16 novel modules,
digest-pinned) it prints `PINS total=82 mismatched=0`, `REFUSALS 20/20 clean`, `SEALED 12/12 clean`,
`HONEST fixtures=120 admitted=112 refused=8`, `CALIBRATION advertised=32 contradicted=0` and
`PREDICATE R48-C1 fail` on the base fence; every frozen must-fail control (no fence, admit-all, refuse-all,
peeking refuse/admit) fails; unpinned and tampered population files fail; and a probe fence that admits exactly
the nine ordinary store shapes prints `PREDICATE R48-C1 pass`, exit 0, on a clean clone. One measured deviation is
routed to stage 2: the base fence refuses 8 of 120, not the `w2` 9/9, so the do-nothing control's `refused=9`
literal must be recorded as `refused=8` in the amendment window.

---

## Appendix A — `plans/round48_c1_verify.py` (candidate; sha256 `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`)

````python
#!/usr/bin/env python3
"""Round-48 C1 counter (calibration, v3): the fixture fence is admitted only when it admits every fixture of a
frozen honest population without touching a byte outside `d`, refuses every frozen hostile module without
touching a byte outside `d`, and every admission that touched nothing outside `d` is reported as BENIGN-ADMIT
instead of being counted as a leak.

Contract. `plans/round-48-claims.md` §C1 (stage-1 commit a543d920) freezes this counter as
`plans/round46_c1_verify.py` (digest-pinned below, imported unchanged) plus five deltas, restated here with the
code that implements each:

  (a) HONEST POPULATION frozen at stage 2 = the 104 fixtures of `plans/battery42`, `plans/battery43`,
      `plans/battery44` plus the 16 novel honest modules committed at stage 2 under `plans/honest48/` and pinned
      below by digest: the nine round-46 novel classes rebuilt from their `w2` report description (`n01`-`n09`,
      authored against the *base* fence description, never against a repaired fence) and the seven classes
      authored in round 48 (`n10`-`n16`). `HONEST_TOTAL` is the stage-2 literal <H> and
      `HONEST_NOVEL_EXPECTED` the literal number of novel fixtures, so a population that loses or mixes its
      novel half cannot pass on the 104 battery fixtures alone.
  (b) BEHAVIOURAL CLASSIFICATION. Per fixture: `LEAK` = admitted AND traced opens/reads outside `d` observed;
      `BENIGN-ADMIT` = admitted with zero traced outside access; `READ` = refused but traced outside access
      observed; `HUNG`; `ERROR` = the harness exit status carried neither decision. Only LEAK counts as `leaked`;
      BENIGN-ADMIT is counted on its own `BENIGN` line and is never a leak. The kill rule keys on hostile
      behaviour: a hostile fixture admitted with outside access is a LEAK. A module is `clean` only when every
      fixture it builds was refused with zero outside access, so a BENIGN-ADMIT in a hostile leg leaves
      `clean<total` and the frozen line below cannot print (this counter is stricter than the kill rule, which
      names only outside-access admissions; it is never looser). An ERROR module is never clean: it is reported
      on `ERRORS` and keeps the frozen line from printing, with LEAK/READ keeping their strict meanings.
  (c) NAME HIDING (Q39) retained: fixture dirs, build dirs, fixture parents and module copies are named by a
      per-run `secrets` token, every parent is padded to `PAD` decoy children, and build and fence order are
      shuffled — all of it inherited from the round-46 counter's `build_module`/main ordering, which this file
      calls rather than copies.
  (d) STRACE ENVELOPE B1/B3/B4/B5/B6 retained by importing the round-46 counter's `run_fence`/`analyse`
      unchanged: the log lives outside the read-only sandbox, the whole scratch root is in scope, the
      stat/access/exec/write families count, `<unfinished ...>`/`<... resumed>` are decoded, and the verdict
      travels as the harness exit status (10 BREACH, 11 ADMIT, 12 error), never as parsed stdout.
  (e) REFUSALS = the 20 frozen `plans/refusals46/` modules; SEALED = the 12 frozen `plans/sealed46/` modules
      plus the wave-1 held-out hostile modules authored against the *landed* fence, committed at stage 2 under
      `plans/sealed48/` and pinned by digest. `SEALED_FLOOR` is the stage-2 literal <S>.

Frozen predicate (same lines as `plans/round-48-claims.md` §C1; the L1 fills `<P>`, `<S>`, `<H>` at the stage-2
amendment, together with the pins of `plans/sealed48/` and the 16 novel honest modules under `plans/honest48/`):
  C1 passes iff `python3 plans/round48_c1_verify.py --lane .` prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0`, then `BENIGN total=<B>`, then
  `CALIBRATION advertised=<20+S> contradicted=0`, then `PREDICATE R48-C1 pass`, exit 0, on a clean clone of the
  landing tip.

Receipts (Q22): the first line this counter prints is `REV <40-hex>` of the tree it measured; a dirty tree is
reported as `TREE dirty=<n>` and fails the predicate in the frozen (default) mode, because the predicate is
bound to a clean clone.

ORDERING (Q30). This counter scores the *landed* fence. It must not be run as a pass/fail receipt on any tree
before the stage-2 amendment commit exists: wave-1 candidates are only selftested, with `--fence`, on scratch
clones of the base, and the predicate they print is the predicate of the whole lane that happens to be checked
out, never an admission of R48-C1.

Limits, named: io_uring SQE opens/reads emit no traced syscall (B7, not exploited; `io_uring_*` is not blocked);
host paths outside the scratch root are not counted, so a fence may still read `/etc`, `/proc` and `/sys` while
deciding; a directory stat's `st_nlink` channel is nulled by padding, not measured; a module that fails to
build contributes no fixtures and is reported per leg; `BENIGN total=` counts fixtures (not modules) across all
three legs, and per-leg module counts are printed on `BENIGN-MODULES`; the novel honest population is lane
files pinned in `PINS_EXTRA`, so a missing, extra or edited novel module is a `PINS` mismatch rather than a
silent narrowing of the honest leg, and `HONEST_NOVEL_EXPECTED` binds the novel count from the other side;
`--refusals`, `--sealed`, `--honest`, `--fence` and `--seed` are testing overrides, and the predicate they print
is the predicate of the inputs they name (never a receipt for the frozen run).

  --lane DIR       lane (or clone) to measure; default `.`
  --work DIR       scratch parent (must lie outside the lane; default $TMPDIR)
  --jobs N         parallel fence runs (default 8)
  --refusals DIR   testing only: refusal modules from DIR
  --sealed DIR     testing only: sealed modules from DIR
  --honest DIR     testing only: extra honest modules from DIR
  --fence PATH     testing only: run the fence at PATH instead of plans/fixture_fence.py
  --seed HEX       testing only: fix the per-run token seed (names stay opaque; receipts reproduce)
  --literals       print the measured population counts and the PIN lines a stage-2 amendment must paste
                   in; build and trace nothing; exit 0

Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import secrets
import shutil
import subprocess
import sys
import tempfile

K44_REL = "plans/round44_c1_verify.py"
R46_REL = "plans/round46_c1_verify.py"
R46_PIN = "ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508"   # plans/round46_c1_verify.py @ a543d920
FENCE_REL = "plans/fixture_fence.py"
REFUSAL_REL = "plans/refusals46"
SEALED_REL = "plans/sealed46"
REFUSAL_SOURCE_REL = "plans/refusals45"
HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
HONEST_EXTRA_REL = "plans/honest48"     # stage 2: the 16 novel honest modules, pinned below
SEALED_EXTRA_REL = "plans/sealed48"     # stage 2: wave-1 held-out hostile modules, pinned below
# STAGE-2 LITERALS. `--literals` measures the population the committed tree actually holds; the amendment
# copies the numbers and the PIN lines back into this block. Nothing else in this file may change at stage 2.
REFUSAL_FLOOR = 20                       # <R>, frozen exact
SEALED_FLOOR = 12                        # <S>: 12 + len(plans/sealed48/*.py)
HONEST_BATTERY = 104                     # the standing batteries, pinned by the round-46 table
HONEST_NOVEL_EXPECTED = 16               # novel fixtures: 9 r46novel (n01-n09) + 7 novel48 (n10-n16)
HONEST_TOTAL = 120                       # <H>: HONEST_BATTERY + HONEST_NOVEL_EXPECTED
# The 16 novel honest modules exactly as delivered by `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/`
# (verified against that seat's `modules.sha256`); the stage-2 amendment commits them under `plans/honest48/`
# at these digests. A file there that is not listed, or a listed file whose bytes moved, is a PINS mismatch.
PINS_EXTRA: dict[str, str] = {
    "plans/honest48/n10_empty_repo.py": "04919778ef5f75a081517149d8bc84582622971a9a1e24da7df883446e737e3f",
    "plans/honest48/n11_multibranch.py": "72c2433ec8bb4898b7e7949a443f6fdc3c69aa9f1b3496366de50eba98116bb0",
    "plans/honest48/n12_local_config_user.py": "6c501b23fed7a8e3b1f9c20e3e45bc8707a087938c79ad9cdb78df8b425af952",
    "plans/honest48/n13_remote_origin.py": "34b2ca158cf3ce4d82484db06a065d88458064ae29fb4321e039d8a54e835d9d",
    "plans/honest48/n14_stash_entry.py": "3e288c6d5786520a101313e19f148bf79c6130470f753b911c6ba83409d3db92",
    "plans/honest48/n15_commit_graph.py": "4f34a149fa7e4018727cea5c1f421107dd1fda747b0c4de2cead45723be3f4c0",
    "plans/honest48/n16_notes_ref.py": "fabcc598e6117e469532e3f6bb1b297468eb27c3878f6f7faa5668a98a2a4ae6",
    "plans/honest48/n01_packed_refs.py": "9e1a2058e326781e0fb7007f041c2f13caa21b93fbd9cea6f668eb3765dac853",
    "plans/honest48/n02_annotated_tag.py": "9eda83c41d1442e14a25b48e17aa2024981d8d4b127d1507f714b911ecc10c16",
    "plans/honest48/n03_detached_head.py": "e9bd62d3341d645f34c2372b9076b92dfdefd5a3caf7d669119426edaae71e7a",
    "plans/honest48/n04_merge_commit.py": "ae6eed2fc058ebc9602b43daa9b04655bdc327d6d6d4f769adc22f3f56386daf",
    "plans/honest48/n05_gitignore.py": "59de03481bee3763087e2f2b2a92c64966952e9cdba8b11c1ed579f40cce8d24",
    "plans/honest48/n06_linear_30.py": "98035b8f551bc1818be09e3a987ef1fcf46356d90135ed3724e23b3879bad011",
    "plans/honest48/n07_reflog_gc.py": "8afa31c42b5075ea64cb53b18fc1d17af0dcb98330f521989fbb61e659c16f51",
    "plans/honest48/n08_tag_detached.py": "66eacd43caa995748677687ad4218ce1049ebc114a087e8405bec8f3c53c0f98",
    "plans/honest48/n09_ignored_untracked.py": "94fe3220722e18b02354e505ff4f7f51c4f3c2214fc9f91b81094150f8214c1b",
}

KINDS = ("clean", "benign", "leak", "read", "hung", "error")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_r46(lane):
    """Import the round-46 counter only when its bytes match the stage-1 pin."""
    got = sha256(lane / R46_REL)
    if got != R46_PIN:
        print(f"SETUP {R46_REL} sha256={got} is not the pinned {R46_PIN}", file=sys.stderr)
        return None
    return load(lane / R46_REL, "kengaku_r46_counter")


def rev(lane):
    """(40-hex HEAD or 40 zeros, dirty count or -1). `--no-optional-locks` keeps the measurement read-only."""
    head = subprocess.run(["git", "--no-optional-locks", "-C", str(lane), "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    st = subprocess.run(["git", "--no-optional-locks", "-C", str(lane), "status", "--porcelain"],
                        capture_output=True, text=True)
    if head.returncode != 0 or st.returncode != 0:
        return "0" * 40, -1
    return head.stdout.strip() or "0" * 40, len([l for l in st.stdout.splitlines() if l.strip()])


def kind_of(verdict, hits):
    """Delta (b): the four hostile buckets, BENIGN-ADMIT, and ERROR kept out of both leak and read."""
    if verdict == "HUNG":
        return "hung"
    if verdict == "ERROR":
        return "error"
    if verdict == "ADMIT":
        return "leak" if hits else "benign"
    return "read" if hits else "clean"


def module_rollup(rows):
    """One hostile module -> one of the frozen buckets. Not clean unless every fixture it claims was refused
    untouched; a module that built no fixture at all did not produce the module it claims, so it is a build
    error and never clean."""
    if not rows:
        return "build_errors"
    kinds = {r["kind"] for r in rows}
    for k in ("leak", "error", "hung", "benign", "read"):
        if k in kinds:
            return k
    return "clean"


def pin_issues(lane, k46, extra_dirs, default_mode):
    """Every pinned file at its digest, and (default mode) every file of a frozen population pinned — an
    unpinned input cannot print `mismatched=0`."""
    pins = dict(k46.PINS)
    pins[R46_REL] = R46_PIN
    issues = [rel for rel, dig in pins.items() if sha256(lane / rel) != dig]
    if default_mode:
        for d in extra_dirs:
            if not d.is_dir():
                continue
            for f in sorted(d.glob("*.py")):
                rel = f.relative_to(lane).as_posix()
                if rel not in PINS_EXTRA:
                    issues.append(rel + ":unpinned")
        for rel, dig in PINS_EXTRA.items():
            if sha256(lane / rel) != dig:
                issues.append(rel)
    return pins, issues


def module_files(d):
    return sorted(d.glob("*.py")) if d.is_dir() else []


def literal_report(lane, refdir, sealdir, honest_extra, sealed_extra):
    """Measure the population the tree holds and print what the stage-2 amendment must paste."""
    refusal = module_files(refdir)
    sealed_frozen = module_files(sealdir)
    sealed_extra_files = module_files(sealed_extra)
    honest_battery = [f for rel in HONEST_RELS for f in module_files(lane / rel)]
    honest_novel = module_files(honest_extra)
    print(f"LITERALS refusals={len(refusal)} sealed_frozen={len(sealed_frozen)}"
          f" sealed_extra={len(sealed_extra_files)} honest_battery_modules={len(honest_battery)}"
          f" honest_battery_fixtures={HONEST_BATTERY} honest_novel_modules={len(honest_novel)}"
          f" pins_extra={len(PINS_EXTRA)}")
    print(f'LITERALS-TO-PASTE REFUSAL_FLOOR={len(refusal)}'
          f" SEALED_FLOOR={len(sealed_frozen) + len(sealed_extra_files)}"
          f" HONEST_TOTAL={HONEST_BATTERY + len(honest_novel)}")
    for f in sealed_extra_files + honest_novel:
        print(f'PIN "{f.relative_to(lane).as_posix()}" "{sha256(f)}"')
    print("REV " + rev(lane)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--refusals", default=None, help="testing only: refusal module dir")
    ap.add_argument("--sealed", default=None, help="testing only: sealed module dir")
    ap.add_argument("--honest", default=None, help="testing only: extra honest module dir")
    ap.add_argument("--fence", default=None, help="testing only: fence file under test")
    ap.add_argument("--seed", default=None, help="testing only: fixed token seed")
    ap.add_argument("--literals", action="store_true", help="print the stage-2 literals and pins; run nothing")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rng = secrets.SystemRandom() if a.seed is None else random.Random(int(a.seed, 16))
    default_mode = (a.refusals is None and a.sealed is None and a.honest is None and a.fence is None
                    and a.seed is None and not a.literals)
    refdir = pathlib.Path(a.refusals).resolve() if a.refusals else lane / REFUSAL_REL
    sealdir = pathlib.Path(a.sealed).resolve() if a.sealed else lane / SEALED_REL
    hon_dir = pathlib.Path(a.honest).resolve() if a.honest else lane / HONEST_EXTRA_REL
    seal_extra = lane / SEALED_EXTRA_REL
    fence_src = pathlib.Path(a.fence).resolve() if a.fence else lane / FENCE_REL
    head, dirty = rev(lane)
    print(f"REV {head}")
    print("TREE clean" if dirty == 0 else f"TREE dirty={dirty}" + ("" if default_mode else " (override)"))
    k46 = load_r46(lane)
    if k46 is None:
        return 2
    pins, issues = pin_issues(lane, k46, (hon_dir, seal_extra), default_mode)
    print(f"PINS total={len(pins) + len(PINS_EXTRA)} mismatched={len(issues)}"
          + (f" first={issues[0]}" if issues else ""))
    for rel in issues[1:]:
        print(f"PIN-MISMATCH {rel}")
    if a.literals:
        literal_report(lane, refdir, sealdir, hon_dir, seal_extra)
        return 0
    if R46_REL in issues:
        print("SETUP the round-46 counter (contract) is not at its pinned digest", file=sys.stderr)
        return 2
    for exe in ("/usr/bin/bwrap", "/usr/bin/python3", k46.STRACE):
        if not os.access(exe, os.X_OK):
            print(f"SETUP {exe} is required", file=sys.stderr)
            return 2
    k44 = load(lane / K44_REL, "kengaku_r44_counter")

    if a.work:
        if pathlib.Path(a.work).resolve().is_relative_to(lane):
            print("SETUP --work must not lie inside the lane", file=sys.stderr)
            return 2
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k48-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    empty = pathlib.Path(tempfile.mkdtemp(prefix=root.name + "-empty-", dir=root.parent))
    try:
        ctl = root / "ctl"
        ctl.mkdir()
        (ctl / "harness.py").write_text(k46.HARNESS)
        fence_copy = ctl / "fence.py"
        if not fence_src.is_file():
            print(f"FENCE {fence_src} absent")
            fence_copy.write_text("def breach(d, argv, tool):\n    raise RuntimeError('fence absent')\n")
        else:
            fence_copy.write_bytes(fence_src.read_bytes())
            print(f"FENCE source={fence_src} sha256={sha256(fence_copy)}")
        honest_battery = [f for rel in HONEST_RELS for f in module_files(lane / rel)]
        honest_novel = module_files(hon_dir)
        groups = {
            "refusal": module_files(refdir),
            "sealed": module_files(sealdir) + (module_files(seal_extra) if sealdir == lane / SEALED_REL else []),
            "honest": honest_battery + honest_novel,
        }
        # (a): the honest leg's two halves are counted apart, so `HONEST_NOVEL_EXPECTED` can bind the novel
        # half on its own and a battery-only population cannot print the frozen line.
        pop = {("honest", f): "battery" for f in honest_battery}
        pop.update({("honest", f): "novel" for f in honest_novel})
        print(f"LITERALS refusals={REFUSAL_FLOOR} sealed={SEALED_FLOOR} honest={HONEST_TOTAL}")
        print(f"LAYOUT refusals={refdir} sealed={sealdir} honest_extra={hon_dir} sealed_extra={seal_extra}"
              f" novel={len(honest_novel)} pad={k46.PAD} jobs={a.jobs}")
        if default_mode:
            cp_bad = k46.copy_rows(refdir, lane) if refdir.is_dir() else []
        else:
            cp_bad = []
            print("COPY-CHECK skipped (refusals dir overridden for testing)")
        for g in ("refusal", "sealed", "honest"):
            print(f"MODULES {g} total={len(groups[g])}"
                  + ("" if groups[g] else " (directory absent or empty)"))
        built: dict[str, list] = {g: [] for g in groups}
        build_errors = {g: 0 for g in groups}
        order = [(g, f) for g in groups for f in groups[g]]
        rng.shuffle(order)                                 # (c): build order carries no signal
        for g, f in order:
            try:
                built[g].append((f, k46.build_module(k44, lane, root, empty, f, rng, ctl)))
            except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                    subprocess.TimeoutExpired) as e:
                build_errors[g] += 1
                print(f"BUILD-ERROR {g} {f.name} {str(e)[:160]}")
        jobs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
        rng.shuffle(jobs)                                  # (c): run order carries no signal
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            res = list(ex.map(lambda t: k46.run_fence(k44, lane, root, ctl, empty, fence_copy, t[1][2], t[0]),
                              enumerate(jobs)))
        per: dict[tuple[str, pathlib.Path], list] = {}
        for (g, f, fx), (verdict, why, hits, calls) in zip(jobs, res):
            kind = kind_of(verdict, len(hits))
            per.setdefault((g, f), []).append({"fx": fx, "verdict": verdict, "why": why, "hits": hits,
                                               "calls": calls, "kind": kind})
            head_hit = f"{hits[0][0]}:{hits[0][1]}" if hits else ""
            print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} {kind} touches={len(hits)}"
                  f" calls={calls}" + (f" first={head_hit}" if head_hit else "")
                  + (f" -- {why}" if why else ""))

        def hostile_leg(g):
            tally = {k: 0 for k in ("clean", "leak", "read", "hung", "build_errors", "benign", "error")}
            for f, fxs in built[g]:
                rows = per.get((g, f), [])
                bucket = module_rollup(rows)
                tally[bucket] += 1
                print(f"{g.upper()} {f.name} {bucket.upper()} fixtures={len(rows)}"
                      f" admitted={sum(r['verdict'] == 'ADMIT' for r in rows)}"
                      f" hung={sum(r['verdict'] == 'HUNG' for r in rows)}"
                      f" touches={sum(len(r['hits']) for r in rows)}")
            tally["build_errors"] += build_errors[g] + (len(cp_bad) if g == "refusal" else 0)
            return tally, len(groups[g])

        rt, rtotal = hostile_leg("refusal")
        print(f"REFUSALS total={rtotal} clean={rt['clean']} leaked={rt['leak']} read={rt['read']}"
              f" hung={rt['hung']} build_errors={rt['build_errors']}")
        st, stotal = hostile_leg("sealed")
        print(f"SEALED total={stotal} clean={st['clean']} leaked={st['leak']} read={st['read']}"
              f" hung={st['hung']} build_errors={st['build_errors']}")
        hrows = [r for (g, _f), rows in per.items() if g == "honest" for r in rows]
        h_adm = sum(r["kind"] == "benign" for r in hrows)
        h_ref = sum(r["kind"] in ("clean", "read") for r in hrows)
        h_read = sum(bool(r["hits"]) for r in hrows)
        h_hung = sum(r["kind"] == "hung" for r in hrows)
        hbuild = build_errors["honest"]
        print(f"HONEST fixtures={len(hrows)} admitted={h_adm} refused={h_ref} read={h_read} hung={h_hung}"
              f" build_errors={hbuild}")
        novel_rows = [r for (g, f), rows in per.items() if pop.get((g, f)) == "novel" for r in rows]
        print(f"HONEST-POP battery={sum(len(r) for (g, f), r in per.items() if pop.get((g, f)) == 'battery')}"
              f" novel={len(novel_rows)} expected_novel={HONEST_NOVEL_EXPECTED}"
              f" novel_modules={len(honest_novel)}")
        benign = {g: 0 for g in groups}
        for (g, _f), rows in per.items():
            benign[g] += sum(r["kind"] == "benign" for r in rows)
        benign_fx = sum(benign.values())
        print(f"BENIGN total={benign_fx}")
        print(f"BENIGN-MODULES refusals={benign['refusal']} sealed={benign['sealed']} honest={benign['honest']}")
        errors = rt["error"] + st["error"] + sum(r["kind"] == "error" for r in hrows)
        if errors:
            print(f"ERRORS total={errors}")
        contradicted = rt["leak"] + rt["read"] + rt["hung"] + st["leak"] + st["read"] + st["hung"]
        print(f"CALIBRATION advertised={rtotal + stotal} contradicted={contradicted}")
        after = [rel for rel, dig in pins.items() if sha256(lane / rel) != dig]
        fails = []
        if issues:
            fails.append(f"pins={len(issues)}")
        if after:
            fails.append(f"pins-after={len(after)}")
        if default_mode and dirty != 0:
            fails.append(f"tree-dirty={dirty}")
        if rtotal != REFUSAL_FLOOR:
            fails.append(f"refusals-total={rtotal}!={REFUSAL_FLOOR}")
        if (rt["clean"] != rtotal or rt["leak"] or rt["read"] or rt["hung"] or rt["build_errors"]
                or rt["benign"] or rt["error"]):
            fails.append("refusals-not-clean")
        if stotal != SEALED_FLOOR:
            fails.append(f"sealed-total={stotal}!={SEALED_FLOOR}")
        if (st["clean"] != stotal or st["leak"] or st["read"] or st["hung"] or st["build_errors"]
                or st["benign"] or st["error"]):
            fails.append("sealed-not-clean")
        if len(novel_rows) != HONEST_NOVEL_EXPECTED:
            fails.append(f"honest-novel={len(novel_rows)}!={HONEST_NOVEL_EXPECTED}")
        if len(hrows) != HONEST_TOTAL:
            fails.append(f"honest-fixtures={len(hrows)}!={HONEST_TOTAL}")
        if h_adm != HONEST_TOTAL or h_ref or h_read or h_hung or hbuild:
            fails.append("honest-not-admitted")
        if errors:
            fails.append(f"errors={errors}")
        if contradicted:
            fails.append(f"contradicted={contradicted}")
        good = not fails
        print("REASON " + (",".join(fails) if fails else "-"))
        print(f"PREDICATE R48-C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(empty, ignore_errors=True)
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
````

## Appendix B — `probe_fence_v2.py` (SATISFIABILITY PROBE ONLY; not a landing candidate; sha256 `1e04fa75f1584c9b58df0c5e61d7eadafb27bc442faa1b1b4c37b2d89b8d8953`)

````python
"""SATISFIABILITY PROBE ONLY — not a landing candidate, not claimed by any seat.

Decides whether the round-48 v3 counter's *pass* path is reachable: it admits a fixture iff the store is a
plain `git init`/commit shape that a correct repair would admit (`info/refs` and a detached HEAD allowed,
because `pack-refs` and `git checkout --detach` write them), and refuses symlinks, special files, hard links,
`.git` files, `commondir`, `alternates`, `modules`, `worktrees`, non-allowlisted config sections/keys, and argv
that leaves `d`. It starts no git child and names nothing outside `d`.
"""
import os
import pathlib
import re
import stat

ALLOW_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
             "logs", "objects", "refs", "packed-refs"}
CORE_KEYS = {"repositoryformatversion", "filemode", "bare", "logallrefupdates", "ignorecase",
             "precomposeunicode", "symlinks"}
INERT_KEYS = {("user", "name"), ("user", "email"), ("remote", "url"), ("remote", "fetch"),
              ("branch", "remote"), ("branch", "merge")}
SHA = re.compile(r"\A[0-9a-f]{40}\Z")
REFHEAD = re.compile(r"\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\Z")


def _bad_argv(d, argv, tool):
    vals = {}
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ("--lane", "--claims", "--receipt"):
            return "argv shape"
        vals = {"--lane": argv[1], "--claims": argv[3], "--receipt": argv[5]}
    elif tool == "anchor":
        k = 0
        while k < len(argv):
            if argv[k] not in ("--lane", "--evidence-ref", "--verbose"):
                return "argv token"
            if argv[k] == "--verbose":
                k += 1
                continue
            if k + 1 >= len(argv):
                return "argv value"
            vals[argv[k]] = argv[k + 1]
            k += 2
    else:
        return "tool"
    for s in vals.values():
        if "\x00" in s or "\n" in s or "\r" in s:
            return "argv bytes"
        p = os.path.normpath(s if s.startswith("/") else os.path.join(str(d), s))
        if p != str(d) and not p.startswith(str(d) + os.sep):
            return "argv outside"
    return vals


def _config(p):
    try:
        raw = pathlib.Path(p).read_bytes()
    except OSError:
        return "config unreadable"
    if b"\r" in raw or any(b >= 0x80 for b in raw):
        return "config bytes"
    sect = ""
    sub = ""
    for line in raw.split(b"\n"):
        s = line.strip()
        if not s or s[:1] in (b"#", b";"):
            continue
        if s.startswith(b"["):
            m = re.fullmatch(rb'\[([A-Za-z][A-Za-z0-9.-]*)(?: "([A-Za-z0-9_][A-Za-z0-9._-]*)")?\]', s)
            if m is None:
                return "config section"
            sect = m.group(1).decode().lower()
            sub = m.group(2).decode() if m.group(2) else ""
            if sect not in ("core", "user", "remote", "branch"):
                return "config section not allowlisted"
            if sect in ("remote", "branch") and not sub:
                return "config section without a name"
            if sect in ("core", "user") and sub:
                return "config section with a name"
            continue
        m = re.fullmatch(rb"([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*([ -~]*))?", s)
        if m is None:
            return "config line"
        key = m.group(1).decode().lower()
        val = m.group(2)
        if sect == "core":
            if key not in CORE_KEYS:
                return "config key not allowlisted"
            if val is not None and key == "bare" and val.decode().lower() not in ("false", "no", "off", "0"):
                return "config bare"
            continue
        # `user.name`/`user.email` and `remote.<n>.{url,fetch}`, `branch.<n>.{remote,merge}` name no path the
        # decision reads: they are inert strings a plain clone-less repository carries. Any other key in those
        # sections stays refused.
        if (sect, key) not in INERT_KEYS:
            return "config key not allowlisted"
        if val is None:
            return "config key without a value"
    return None


def _store(gd):
    try:
        ents = sorted(os.scandir(gd), key=lambda e: e.name)
    except OSError:
        return "store unreadable"
    have = set()
    for e in ents:
        st = e.stat(follow_symlinks=False)
        if e.name not in ALLOW_TOP:
            return "store entry not plain"
        have.add(e.name)
        if stat.S_ISLNK(st.st_mode) or stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
            return "store entry link"
        if e.name in ("hooks", "info", "logs", "objects", "refs"):
            if not stat.S_ISDIR(st.st_mode):
                return "store dir"
            continue
        if not stat.S_ISREG(st.st_mode):
            return "store file"
        if e.name == "HEAD":
            body = pathlib.Path(e.path).read_bytes()[:200].decode("ascii", "replace").strip()
            if not (SHA.match(body) or REFHEAD.match(body)):
                return "HEAD"
        if e.name == "config":
            why = _config(e.path)
            if why:
                return why
    for req in ("HEAD", "config", "objects", "refs"):
        if req not in have:
            return "store missing " + req
    if "info" in have:
        for e in os.scandir(os.path.join(gd, "info")):
            st = e.stat(follow_symlinks=False)
            if not stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode):
                return "info entry"
    if "objects" in have:
        for e in os.scandir(os.path.join(gd, "objects")):
            st = e.stat(follow_symlinks=False)
            if not stat.S_ISDIR(st.st_mode):
                return "objects entry"
            if e.name == "info":
                # `git gc`/`repack` write objects/info/packs and (optionally) objects/info/commit-graph[s];
                # `alternates` stays refused because an object store redirect is the hostile case.
                for i in os.scandir(e.path):
                    ist = i.stat(follow_symlinks=False)
                    if stat.S_ISREG(ist.st_mode) and i.name in ("packs", "commit-graph"):
                        continue
                    if stat.S_ISDIR(ist.st_mode) and i.name == "commit-graphs":
                        for g in os.scandir(i.path):
                            if not stat.S_ISREG(g.stat(follow_symlinks=False).st_mode):
                                return "commit-graph entry"
                        continue
                    return "objects/info not plain"
                continue
            if e.name == "pack":
                for p in os.scandir(e.path):
                    if not stat.S_ISREG(p.stat(follow_symlinks=False).st_mode):
                        return "pack entry"
                continue
            if not re.fullmatch(r"[0-9a-f]{2}", e.name):
                return "loose dir"
            for o in os.scandir(e.path):
                ost = o.stat(follow_symlinks=False)
                if not stat.S_ISREG(ost.st_mode):
                    return "loose entry"
                if ost.st_nlink > 1:
                    return "loose link"
                if not re.fullmatch(r"[0-9a-f]{38}", o.name):
                    return "loose name"
    if "refs" in have:
        for e in os.scandir(os.path.join(gd, "refs")):
            mode = e.stat(follow_symlinks=False).st_mode
            if e.name in ("heads", "tags", "notes") and stat.S_ISDIR(mode):
                for top, _dirs, files in os.walk(e.path):
                    for f in files:
                        if not SHA.match(pathlib.Path(top, f).read_text(errors="replace").strip()):
                            return "ref body"
                continue
            if e.name == "stash" and stat.S_ISREG(mode):
                if not SHA.match(pathlib.Path(e.path).read_text(errors="replace").strip()):
                    return "ref body"
                continue
            return "refs entry"
    return None


def breach(d, argv, tool):
    d = pathlib.Path(os.path.normpath(str(d)))
    try:
        st = os.lstat(d)
    except OSError:
        return "d"
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
        return "d"
    vals = _bad_argv(d, list(argv), tool)
    if isinstance(vals, str):
        return vals
    repos = []
    for top, dirs, files in os.walk(str(d), followlinks=False):
        keep = []
        for name in dirs:
            p = os.path.join(top, name)
            s = os.lstat(p)
            if stat.S_ISLNK(s.st_mode):
                return "symlink"
            if not stat.S_ISDIR(s.st_mode):
                return "dir entry"
            if name == ".git":
                repos.append(top)
                continue
            keep.append(name)
        dirs[:] = sorted(keep)
        for name in files:
            p = os.path.join(top, name)
            s = os.lstat(p)
            if stat.S_ISLNK(s.st_mode):
                return "symlink"
            if name == ".git":
                return "gitfile"
            if not stat.S_ISREG(s.st_mode) or s.st_nlink > 1:
                return "special"
    if not repos:
        return "no repo"
    if len(repos) > 64:
        return "many repos"
    for r in repos:
        why = _store(os.path.join(r, ".git"))
        if why:
            return why
    lane = os.path.normpath(vals["--lane"] if vals["--lane"].startswith("/")
                            else os.path.join(str(d), vals["--lane"]))
    if lane not in [os.path.normpath(r) for r in repos]:
        return "lane not a repo in d"
    return None
````
