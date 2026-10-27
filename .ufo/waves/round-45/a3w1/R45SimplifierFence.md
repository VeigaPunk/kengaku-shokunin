# R45SimplifierFence — `plans/fixture_fence.py` simplifier review (round 45, wave a3w1)

**Lane measured:** `master` = `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (clean clone of the tip; the working
tree carries other seats' in-flight `LOG.md`/`SCORECARD.md`/`corpus/` edits, none of them mine).
**Subject:** `plans/fixture_fence.py` sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` (276 lines) —
the file the C1 counter copies and imports (`plans/round45_c1_verify.py:110-118`, `FENCE plans/fixture_fence.py sha256=…`).
**Lane writes:** none. Fence digest re-checked after all work: unchanged; every run happened against clones under
`/fast/scratch/hyaku/kengaku-r45/R45SimplifierFence/a3/`.

## Axes (godspeed)

| axis | what it means here | move |
|---|---|---|
| A1 dead machinery | branches/checks that cannot decide a verdict | delete (D1, D2, D3) |
| A2 fidelity | same admit/refuse **and same reason string** for every fixture | measure per-fixture lines, not counters |
| A3 evidence | every number re-run by this seat, envelope-bracketed, digests compared | 4 counter runs + 3 probes, receipts below |
| A4 host safety | nothing written outside my scratch and my report subdir | bwrap envelope on all 4 counter runs |

## Findings

| # | finding | verdict |
|---|---|---|
| **D1** | fact-3 "walk up to the build root" loop is a one-iteration loop | **delete** (diff A) |
| **D2** | fact-2 `not isinstance(val, str)` disjunct can never decide | **delete** (diff A) |
| **D3** | `_probe`'s `git config … core.worktree` leg: only reachable outcome is rc 1 → `None` | **delete, tier 2** (diff B) |
| F4 | `sorted(set(targets))` — dedupe redundant by construction (0 duplicate cases measured) | keep (6 chars, no gain) |
| F5 | `breach` re-derives `vals` for the order blob leg (`:269`) instead of taking it from `_collect` | keep (would widen a 3-tuple to 4 for one 6-token dict) |
| F6 | `isinstance(lane, str)` at `:203` is the absent-`--lane` case, not a dead guard | keep |
| F7 | no second fence API: single public `breach`; all five helpers entered | keep |

### D1 — the fact-3 loop never iterates twice (`:114-120`)

```python
114:    anc = d.parent
115:    while True:
116:        if os.path.lexists(anc / ".git"):
117:            return f".git exists at {anc} above the fixture", None, None
118:        if anc == d.parent or anc.parent == anc:
119:            break
120:        anc = anc.parent
```

`anc` is initialised to `d.parent`, so the break condition at `:118` is true on entry: the loop body runs exactly
once and `:120` is unreachable. The function's own comment already scopes the check to "the fixture dir's parent"
(`:112-113`), and `GIT_CEILING_DIRECTORIES=str(ceiling)` with `ceiling = d.parent` (`:63`, `:256`) makes anything
higher unreachable by git discovery anyway.

Measured, not argued alone: an instrumented copy of the landed module (counters injected before `anc = d.parent`
and as the first statement of the loop body) ran a 21-tree × 22-argv matrix — 462 cases, fact 3 entered 231 times,
**iterations_per_entry=1, violations=0** (`receipts/diff_driver-cand.txt`).

### D2 — fact-2's `not isinstance(val, str)` never decides (`:106`)

```python
106:        if val is True or not isinstance(val, str) or val.startswith("{"):
```

`vals` is written in exactly three places inside `_collect`: `:87` (`dict(zip(argv[0::2], argv[1::2]))`, str
slices), `:95` (`argv[k + 1] … else ""`, str) and `:98` (`True` for `--verbose`). So whenever the second disjunct
is evaluated, `val` is already a `str`. Measured over a 88-case matrix that includes `--verbose`: fact-2 iterations
99, observed value types `['bool','str']`, **values_neither_True_nor_str=0** (`receipts/leg_census.txt`).

### D3 — the `core.worktree` git leg cannot refuse (`:231-240`)

```python
231:    wt = _git(repo, ceiling, "config", "--local", "--no-includes", "--get", "core.worktree")
232:    if wt is None: …            233: return "git hung answering config core.worktree"
234:    if wt[0] == 0: … 237: if p.resolve() != repo: … 238: return f"core.worktree={wt[1]} leaves the repo directory"
239:    elif wt[0] != 1: …          240: return f"git config core.worktree failed (rc={wt[0]})"
```

For this leg to *refuse*, it needs `git config --local --get core.worktree` to return rc 0 with a value that does
not cancel to the repo dir, or rc ∉ {0,1}. Both are shadowed by the two legs above it:

- rc 0 with a value: fact 5 (`:196-200`) already refuses every nonempty `core.worktree` that does not resolve to
  the repo, so an admitted value cancels to the repo (`"."`, `"./"`, `"./."`, `"sub/.."`, duplicate `[core]`).
  git resolves `core.worktree` **relative to the gitdir**, so exactly those values move `rev-parse
  --show-toplevel` off the repo dir and `:220-221` (or `:222-223` from a lane) refuses first.
  Measured on the five admitted shapes: `toplevel_rc=0` with `toplevel = …/d/.git`, verdict `rev-parse
  --show-toplevel=… is not the repo directory` (`receipts/worktree_leg_probe.txt`).
- rc ≠ 1 (bad config): the same config read makes `rev-parse --show-toplevel` fail too, so `:216-217` refuses
  first. Measured on two malformed configs (`[core` unterminated, unterminated quote): `toplevel_rc=128`,
  `wt_rc=128`, verdict `git cannot describe the worktree at … (rc=128)`.
- rc 1 (key absent, or present under `[core "x"]` — git does not map that to `core.worktree`): `:239`'s `elif`
  is false, `:241 return None` — a no-op.

Census over the 88-case matrix: `WORKTREELEG calls=7 rc0=0 rc1=7 other=0` — the rc-0 branch was never entered by
any real fixture, and deletion of the leg changes no outcome: 462-case matrix `divergent=0`, counter predicate pass
with per-fixture lines **byte-identical** to the landed fence (below, E6).

This is a case analysis over git's config surface, not a proof of the whole grammar — hence tier 2: the L1 should
apply diff B only if it accepts §D3's argument. Cost of keeping it: one extra `git` child per probe (the leg is
the third of `_probe`'s git calls).

### F4/F5/F6/F7 (kept, with the reason)

- F4 `for repo, need_root in sorted(set(targets)):` (`:264`): `targets` gets one entry per collected repo (one
  `.git` per walked directory, `:125-158`) plus the lane when it is not a repo (`:262`), so the `set()` never
  removes anything — measured `TARGETS cases=30 with_duplicates=0`. Deleting `set()` saves 6 characters and
  requires a non-local argument about `resolve()`; not worth a diff.
- F5 `vals = dict(zip(argv[0::2], argv[1::2]))` recomputed at `:269` (the order blob leg). The dict is already
  built at `:87`; threading it out of `_collect` would widen the internal 3-tuple to 4 to save one 6-token dict on
  one tool. Not a simplification.
- F6 `:203`'s `isinstance(lane, str)` is the `--lane`-absent case: `str(None).startswith("/")` would otherwise
  reach `d / None`. Live.
- F7 No second API: the module exposes `breach` only; the counter's harness calls `m.breach(Path, argv, tool)`
  (`plans/round45_c1_verify.py:110-118`) and nothing else imports the module except the wave-1 spec text. All five
  helpers are entered (census `CALLS breach=88 _collect=88 _probe=26 _git=42 _inside=101-126`), no parameter is
  ignored on any path.

### Preserved limit (not a defect to fix in this item)

`.git` at `d.parent.parent` is not checked (`t_above2`/`t_twoabove` admit in my matrix) — that is the landed
behaviour, it matches the comment's scope, and it is covered by `GIT_CEILING_DIRECTORIES=d.parent`, which is passed
to every git child (`:63`). Diff A/B keep it exactly.

## Diff A — paste-ready, semantics-neutral (D1 + D2)

`fixture_fence.minimal.diff` (sha256 `7deac558a695e3e6…`), 276 → 271 lines, 2 hunks:

```diff
--- a/plans/fixture_fence.py
+++ b/plans/fixture_fence.py
@@ -103,7 +103,7 @@
     # fact 2: every argv value that is a path must resolve inside d (a `{...}` placeholder is the
     # counter's own per-run token and is resolved by the harness, not here).
     for opt, val in vals.items():
-        if val is True or not isinstance(val, str) or val.startswith("{"):
+        if val is True or val.startswith("{"):
             continue
         cand = pathlib.Path(val) if val.startswith("/") else d / val
         if not _inside(cand, d):
@@ -111,13 +111,8 @@
 
     # fact 3: no `.git` may sit ABOVE d up to the module build root (the fixture dir's parent): a repo
     # there is what git discovery would adopt from a `--lane` that is a plain directory inside d.
-    anc = d.parent
-    while True:
-        if os.path.lexists(anc / ".git"):
-            return f".git exists at {anc} above the fixture", None, None
-        if anc == d.parent or anc.parent == anc:
-            break
-        anc = anc.parent
+    if os.path.lexists(d.parent / ".git"):
+        return f".git exists at {d.parent} above the fixture", None, None
 
     # fact 4: one walk of the whole fixture tree — `.git` files, `.git` symlink dirs, escaping symlinks,
     # and non-regular special files — collecting every directory that holds a real `.git` directory.
```

Apply: `cd <lane> && patch -p1 < …/fixture_fence.minimal.diff` (or edit the two blocks by hand — both hunks are
whole-block replacements). `os` is still imported for `os.walk`/`os.path.lexists`/`os.readlink`/`os.lstat`.

## Diff B — tier 2, the `core.worktree` git leg (D3)

`appendix-wtleg-removal.diff` (sha256 `42e8986e0528ee5c…`), −10 lines (`_probe`'s body ends at
`return None` after the git-dir leg):

```diff
@@ -228,16 +228,6 @@
         return f"git rev-parse --absolute-git-dir={gd[1]} is outside the fixture"
-    wt = _git(repo, ceiling, "config", "--local", "--no-includes", "--get", "core.worktree")
-    if wt is None:
-        return "git hung answering config core.worktree"
-    if wt[0] == 0:
-        p = pathlib.Path(wt[1])
-        p = p if p.is_absolute() else repo / p
-        if p.resolve() != repo:
-            return f"core.worktree={wt[1]} leaves the repo directory"
-    elif wt[0] != 1:
-        return f"git config core.worktree failed (rc={wt[0]})"
     return None
```

Diff A + B together: 276 → 261 lines.

## Evidence (all re-run by this seat; no w2 number is cited)

Envelope for every counter run:
`.ufo/waves/round-45/claims/envelope.sh "$S/env" python3 …/round45_c1_verify.py --lane … --work … --jobs 12`
(`$S=/fast/scratch/hyaku/kengaku-r45/R45SimplifierFence`), home read-only, `~/.cache` overlaid from scratch.

**E1 landed fence (baseline clone of `fbad1c5`) → `receipts/base.log`**

```
ENVELOPE … -- python3 $S/a3/lane/plans/round45_c1_verify.py --lane $S/a3/lane --work $S/a3/w-base --jobs 12
ENVELOPE start 00:26:52 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:26:58 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

**E2 diff A applied (`cand`, sha256 `52c8eeac3a06eef2…`) → `receipts/cand.log`**

```
ENVELOPE start 00:27:09 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=52c8eeac3a06eef26f758aca0aef37ec377716de0b2d144f98bdee7b736ee596
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:27:16 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

**E3 diff B applied (`cand2`, sha256 `f7d50372efba88ef…`, same-length `--work` dir so 120-char reason truncation
lands at the same offset) → `receipts/cand2.log`**

```
ENVELOPE … -- python3 $S/a3/lane-cand2/plans/round45_c1_verify.py --lane $S/a3/lane-cand2 --work $S/a3/w-cnd2 --jobs 12
ENVELOPE start 00:31:47 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=f7d50372efba88ef6081d7cfd3ff0460f0ce9ed3d5a1845a30ded376198c44e9
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:31:54 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

**E4 differential matrix (landed vs A, landed vs B) → `receipts/diff_driver-cand.txt`, `…-cand2.txt`**

```
MATRIX cases=462 divergent=0
FACT3 reached_cases=231 iterations_per_entry=1 violations=0
rc=0                                   (both files)
```

21 tree shapes (empty, repo, repo-in-subdir, `.git` file, escaping file/dir symlinks, in-tree symlink, FIFO,
repo above `d`, repo two levels above `d`, include, commondir, alternates, worktreeConfig, core.bare,
`core.worktree` outside / `"."` / empty, 65 repos, config as directory, config as symlink) × 22 argv shapes
(order 4/5/6/7 tokens, wrong token, empty, `..` escape; anchor absolute/relative/`{TOKEN}`/`{TOKEN}/../../etc`/
value-less/unknown/`--verbose`/`--evidence-ref` absolute+relative; unknown and empty tool).

**E5 leg census → `receipts/leg_census.txt`**

```
CASES 88
CALLS <genexpr>=85 _collect=88 _git=42 _inside=126 _probe=26 breach=88
TYPES fact2_values=99 types=['bool', 'str'] values_neither_True_nor_str=0
TARGETS cases=30 with_duplicates=0
WORKTREELEG calls=7 rc0=0 rc1=7 other=0
```

**E6 per-fixture outcome identity (the fidelity claim, stronger than counters):** the counter prints one
`FENCE-RUN <group> <module> <fid> <verdict> opens=N -- <reason>` line per fixture — 117 lines (104 honest + 13
refusal fixtures over 10 hostile modules). After normalising only the random scratch tempdir, all three runs are
the **same file**:

```
36489cbf21b9128af27feedd898d1a3c122bd71b251cd8fc923d4d486881f8e7  receipts/run.base
36489cbf21b9128af27feedd898d1a3c122bd71b251cd8fc923d4d486881f8e7  receipts/run.cand
36489cbf21b9128af27feedd898d1a3c122bd71b251cd8fc923d4d486881f8e7  receipts/run.cand2
```

104×`ADMIT` + 13×`BREACH`, `opens=0` on all 117. Every reason string identical, e.g.
`refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- .git exists at …/fx/refusals45-f6_above above` — i.e.
D1's replacement emits the *same* sentence with `d.parent` as `anc`. Caveat: the counter truncates reasons to 120
characters (`run_fence`, `out[7:][:120]`), so E6 compares 120-char prefixes; the full strings are equal by
construction because D1 substitutes `anc` ≡ `d.parent`.

**E7 worktree-leg reachability → `receipts/worktree_leg_probe.txt`**

```
'.'        verdict '.: rev-parse --show-toplevel=/fast/scratch/hya…'   toplevel_rc 0  gitdir_rc 0  wt_rc 0  wt_out '.'
'./'       verdict '.: rev-parse --show-toplevel=…'                   toplevel_rc 0  gitdir_rc 0  wt_rc 0  wt_out './'
'sub/..'   verdict '.: git cannot describe the worktree at … (rc=128)' toplevel_rc 128 gitdir_rc 128 wt_rc 128
''         verdict '.: git cannot describe the worktree at … (rc=128)' toplevel_rc 128 gitdir_rc 128 wt_rc 128
'"./."'    verdict '.: rev-parse --show-toplevel=…'                   toplevel_rc 0  gitdir_rc 0  wt_rc 0  wt_out './.'
'x/..'     verdict '.: git cannot describe the worktree at … (rc=128)' toplevel_rc 128 gitdir_rc 128 wt_rc 128
# malformed-config cases (appended)
unterminated-section  verdict='… git cannot describe the worktree … (rc=128)' toplevel=(128,'') wt=(128,…'bad config line 6')
unterminated-quote    verdict='… git cannot describe the worktree … (rc=128)' toplevel=(128,'') wt=(128,…'bad config line 7')
space-value           verdict='./.git/config sets core.worktree=a b c'        toplevel=(128,'') wt=(128,…cannot chdir)
dup-core-worktree     verdict='.: rev-parse --show-toplevel=…/d/.git …'       toplevel=(0,…/d/.git) wt=(0,'.')
worktree-in-subsection verdict='ADMIT'                                        toplevel=(0,…/d) wt=(1,'')
```

(Full untruncated lines in the receipt.) Every rc-0 case breaches at the toplevel leg; every rc≠1 case breaches at
the toplevel leg with rc 128; the `[core "x"]` case is a no-op (`rc 1`).

## Preserved contract

- Signature and return type unchanged: `breach(d, argv, tool) -> str | None`; one reason line, stripped by the
  harness.
- Collection-before-git ordering intact: no git child exists until fact 5 has judged the whole tree
  (`:244-255`), and the `strace` open-region rule still observes `opens=0` on all 117 fixtures.
- Every cap and pin kept: `ENTRY_CAP`, `REPO_CAP`, `CONFIG_CAP`, `GIT_TIMEOUT`, pinned `GIT_ENV`, `ceiling=d.parent`.
- Every refusal message kept verbatim (E6), so the counter's reason column and any external reading of it stay
  valid.

## Tradeoffs

- **A (D1+D2): none.** No branch that could ever produce a different verdict is removed; measured identical on 462
  synthetic cases and all 117 counter fixtures. Maintainability gain: −5 lines, one loop, one impossible disjunct.
- **B (D3): trades a redundant git-side opinion for 10 lines and one git child per probe.** The text parser
  (`:196-200`) remains the authority and is *broader* (it scans every `.git/config*`; includes are refused at
  `:174`). The residual risk is a git-config shape my eight-variant probe did not build — stated, not hidden.
- Not touched: the fence's own limit (no check above `d.parent`) and the fence's `[core "x"]` section
  misclassification (`_SECTION_RE` stops at the space) — both are behaviour, not dead code; they belong to the C1
  attacker seats, not to this item.

## Limits of this review

- Reviewed one file against the frozen predicate; C2, receipts and frontier artifacts were not in this item.
- The 462/88-case matrices are mine, not exhaustive over git's config grammar; E6 is the authoritative fidelity
  measurement because it is the frozen counter's own fixture set.
- I did not diff against the w2 leads under `.ufo/waves/round-45/w2/R45SimplifierFence/` (unverified, killed seat);
  every number above comes from my own runs and receipts.

## Receipts (all in this subdir)

| file | sha256 (16) | note |
|---|---|---|
| `fixture_fence.minimal.diff` | `7deac558a695e3e6` | diff A, paste-ready |
| `appendix-wtleg-removal.diff` | `42e8986e0528ee5c` | diff B, tier 2 |
| `make_cand.py` | `65ef17c52eb7193a` | builds A from the landed file (refuses if a block moved) |
| `diff_driver.py` | `20c98c2d07a5be67` | 462-case differential + loop-iteration counter |
| `leg_census.py` | `7a5e7da1262d888d` | call/type/target/worktree-leg census |
| `worktree_leg_probe.py` | `9a4eb1e2933e5074` | D3 reachability probe |
| `receipts/base.log`, `cand.log`, `cand2.log` | `cd9436b3…`, `d6576985…`, `101580f3…` | full counter stdout, envelope included |
| `receipts/run.base`, `run.cand`, `run.cand2` | all `36489cbf…` | 117 normalised `FENCE-RUN` lines — identical |
| `receipts/diff_driver-cand.txt`, `-cand2.txt` | `a71da18a…`, `319f460d…` | matrix output |
| `receipts/leg_census.txt` | `90eb7560ede64dd0` | census output |
| `receipts/worktree_leg_probe.txt` | `26fd54307b420807` | reachability output |

Scratch `/fast/scratch/hyaku/kengaku-r45/R45SimplifierFence` (clones `lane`, `lane-cand`, `lane-cand2`, work logs)
removed with `plans/scratch_guard.py safe-rm` after the receipts were copied here; no scratch path is evidence.

VERDICT: fence-simplifications-3
