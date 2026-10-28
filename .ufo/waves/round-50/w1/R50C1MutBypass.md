# R50C1MutBypass — counter-accounting mutation probe (R50-C1, novelty)

Seat: `R50C1MutBypass` (mutation-tester, leaf). Serves R50-C1 as an **attack** seat: it attacks the
counter's own accounting, not the fence. No admission is claimed and nothing was committed, pushed,
stashed or checked out anywhere.

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252      # the tree every measurement ran against
LANE_HEAD_AT_START c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
ANCESTRY git merge-base --is-ancestor 3b02d57… HEAD -> exit 0   (freeze IS an ancestor of the lane tip)
COUNTER plans/round50_c1_verify.py  d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  (tip bytes; stage-1 f9b9873e differs only in the two module-attribution lines — diff below)
FENCE   plans/fixture_fence.py      05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  (base fence, known bad)
POP     plans/honest50/population.txt b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  (126 rows)
ENV     Python 3.14.8 · git 2.56.0 · GNU patch 2.8 · plazir27 · 32 cpu
SCRATCH /fast/scratch/hyaku/kengaku-r50/R50C1MutBypass  (removed at yield; see §Scratch)
```

## Axes named

- **A1 bypass-surface** — does mutating an accounting line make the *known-bad* base fence reach
  `PREDICATE R50-C1 pass` / exit 0?
- **A2 guard redundancy** — how many *independent* guards does each leg quantity have (frozen literal
  vs computed value vs pin)?
- **A3 receipt killability** — when a counter mutation forges a passing receipt, does the claim's own
  kill rule (receipt-level, reading the printed leg literals) still reject it?
- **A4 reproducibility** — does the pristine counter reproduce the declared control on the freeze tree,
  and does it reproduce byte-for-byte after the probes?

## Setup (read-only against the lane)

```bash
S=/fast/scratch/hyaku/kengaku-r50/R50C1MutBypass; export TMPDIR="$S"
git clone --shared --no-hardlinks -q <lane> "$S/clone50"
git -C "$S/clone50" checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252   # scratch clone only
git -C "$S/clone50" rev-parse --show-toplevel   # -> $S/clone50   (asserted before any git use)
git -C "$S/clone50" status --porcelain | wc -l  # -> 0
git -C <lane> show c3372a9…:plans/round50_c1_verify.py > "$S/cand/counter_tip.py"   # read-only
```

The freeze clone carries the **stage-1** counter (`f9b9873e`); the counter the claim binds after the
declared open-window repair is `d8787b34` at the tip. The two differ only in module attribution, so the
repair touched **no accounting line** (verified, not assumed):

```diff
@@ -113,7 +113,7 @@
-                built.append({"fid": fid, "tool": tool, "argv": argv, "dir": d, "module": path.name})
+                built.append({"fid": fid, "tool": tool, "argv": argv, "dir": d, "module": str(path)})
@@ -229,7 +229,7 @@
-        def fids_of(f, fixtures):  return {x["fid"] for x in fixtures if x["module"] == f.name}
+        def fids_of(f, fixtures):  return {x["fid"] for x in fixtures if x["module"] == str(f)}
```

All probes therefore mutate a copy of `d8787b34` and run it with `--lane "$S/clone50"`.

## Baseline (pristine counter, base fence) — A4

```bash
python3 cand/counter_tip.py --lane "$S/clone50" --work "$S/work" --skip-mutants   # exit 1, 8 s
python3 cand/counter_tip.py --lane "$S/clone50" --work "$S/work"                  # exit 1, 9 s (full)
```

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/clone50/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
PREDICATE R50-C1 fail
```

This reproduces the declared stage-1 control exactly (`admitted=113 refused=13`, fail, exit 1), so the
detector baseline is **conclusive**: the base fence is bad and the pristine counter rejects it.

**Detector design matters.** The base fence is red on **two** legs (`HONEST` and `MUTANTS unmet`). A
full-run detector therefore *masks* any mutation confined to honest accounting, because the mutant leg
keeps `ok=False` on its own. Two detectors are used throughout:

- **D_full** — the frozen predicate verbatim (`--lane`, no flags), exit code included.
- **D_honest** — `--skip-mutants`, which leaves `HONEST` as the only red leg and therefore isolates
  honest accounting. This is the counter's own "testing only" affordance, never a citable receipt.

## The mutations (one at a time, against the unchanged base fence)

Each candidate is a separate file in scratch; the clone's `plans/` was never edited. Diffs are
`diff -u plans/round50_c1_verify.py cand/<id>.py`.

### M1 — predicate line printed unconditionally → **BYPASS (counter defect)**

```diff
@@ -290,8 +290,8 @@
-        say(f"PREDICATE R50-C1 {'pass' if ok else 'fail'}")
-        return 0 if ok else 1
+        say("PREDICATE R50-C1 pass")
+        return 0
```
sha256 `bb90c875dd39d231acb30cbd172808318c0d9d0b16311da7a7512a913bfb7e39`

| detector | exit | verdict lines |
|---|---|---|
| D_full | **0** | `HONEST fixtures=126 admitted=113 refused=13 error=0` … `MUTANTS … verdict=unmet` · `PREDICATE R50-C1 pass` |
| D_honest | **0** | `HONEST fixtures=126 admitted=113 refused=13 error=0` · `PREDICATE R50-C1 pass` |

The base fence passes. The predicate is a **self-attestation**: `ok` and the printed sentence are the
same two lines, so disconnecting them costs one edit. The receipt is still self-contradictory
(`admitted=113` beside `pass`), which is what saves it at A3 (§Kill rule).

### M1b — HONEST leg measures but does not score → **BYPASS under D_honest (counter defect)**

```diff
@@ -212,7 +212,6 @@
         if refused:
-            ok = False
             for x in refused[:12]:
```
sha256 `4560ef8e9cc9372947b9a5eda178ad12f35110e9a221bf1ba06daee0569e7acd`

| detector | exit | verdict lines |
|---|---|---|
| D_full | 1 | `PREDICATE R50-C1 fail` — but only because `MUTANTS … caught=3 … verdict=unmet` |
| D_honest | **0** | `HONEST fixtures=126 admitted=113 refused=13 error=0` · `PREDICATE R50-C1 pass` |

This is the minimal, quiet forgery: the receipt still *prints* the over-refusals (`HONEST-REFUSED …` ×12),
only the score is dropped. The full-run FAIL is attributable entirely to the carried **candidate** mutant
battery (`caught=3 broken=12`), not to the honest leg — visible in the output above. The claim that the honest
leg scores *only* through this line is a structural fact of the source, verified by grep: `ok = False` occurs
in the dirty-tree branch, the POPULATION branch, the HONEST branch, the two hostile legs and the MUTANTS
branch, and the HONEST branch's is the one deleted here. `[INFERENCE]` On the S2/S3 landing tree, where the
claim requires `MUTANTS … verdict=met`, this same one-line deletion therefore yields `PREDICATE R50-C1 pass`
with exit 0 on a fence that over-refuses. The landing-tree run itself was not executed (it is a measurement of
a repaired fence, outside this seat's assigned detector and available nowhere in the freeze clone).

### M2 — HONEST denominator read from the population file → **no bypass**

```diff
@@ -198,7 +198,7 @@
-        if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or mismatched or failures:
+        if pop_sha != POPULATION_SHA or mismatched or failures:
```
sha256 `fb4e87a3cab8f672f2eaf0e41f87dd45fd48fe052603d41e350e5fefc076237e`

D_full exit 1, D_honest exit 1; output substantively identical to the baseline. With the full 126-row
population the honest leg is still red, so the frozen literal is **not** load-bearing here — the pin is.

### M2b — denominator **and** pin read from the file → **BYPASS once the population is pruned (counter defect)**

```diff
@@ -198,7 +198,7 @@
-        if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or mismatched or failures:
+        if mismatched or failures:
```
sha256 `49ab767eab701cd340e6403bb27486cc2225617ded8f8aa174478bfb1bae4a9e`

On the intact 126-row population: D_full exit 1, D_honest exit 1 (honest leg still red) — no bypass.
But one statement guards **both** the frozen literal and the pin, so a single edit converts the honest
denominator into one the counter satisfies from the file it reads. Probe P3 (below) prunes the 13 rows
the base fence over-refuses; the base fence then reaches a pass:

```
POPULATION fixtures=113 pin=72ed1b2d01c81a417c0ee27d297dbc90971b8f083ebcb7e5194547e7702d60ad mismatched=0 build_errors=0
HONEST fixtures=113 admitted=113 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
PREDICATE R50-C1 pass            (exit 0, D_honest)
```

### M3 — `mismatched` list ignored → **no bypass; survives the detector (coverage finding)**

```diff
@@ -198,7 +198,7 @@
-        if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or mismatched or failures:
+        if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or failures:
```
sha256 `a042b7259189e15f5ba45ee9d733483fa74d355bf7c7d749bb598ac72371c71d`

D_full exit 1, D_honest exit 1, and the output is **identical to the baseline apart from temp paths** —
the base fence cannot exercise this line (`mismatched=0` there). The line's stated purpose is host-identity
drift (the claim's named limit: `hooks/*.sample`, `info/exclude`, `git worktree --relative-paths`); drift does
**not** change `population.txt`, so the pin does not cover it and `mismatched` is its only guard. M3 removes
that guard invisibly. This is a coverage finding against the frozen predicate, not a defect demonstrated on
the base fence.

### M4 — SEALED leg skipped → **no bypass; the leg vanishes from the receipt**

```diff
@@ -217,7 +217,7 @@
-        for rel in (REFUSALS_REL, *SEALED_RELS):
+        for rel in (REFUSALS_REL,):
```
sha256 `e7d1867beb77e964a5fbb6a284a0e7169de47b2f461fad17d76642225a6d58bd`

D_full exit 1, D_honest exit 1. The only observable difference is the **missing** `SEALED total=…` line
(present in the baseline, absent here); the predicate is untouched because the base fence does not leak
sealed modules. Note the `SEALED50_MIN` count check is a *separate* branch and survives M4, so the floor
pins the module count, never the scoring of those modules.

### Extra probe M1c — predicate + HONEST line forged (two edits, labelled extra)

Used only to locate where the guard stack actually stops: sha256
`7da8d622eb7455ab2bd02bee793dede02bc95e5d2e26c4d2f503b06f70c59db4`, D_full exit **0**:

```
HONEST fixtures=126 admitted=126 refused=0 error=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
PREDICATE R50-C1 pass
```

Even a forged HONEST line cannot make the freeze-tree receipt acceptable, because `SEALED total=12` (<18)
and `MUTANTS verdict=unmet` are computed independently — see §Kill rule.

## Data-side probes (the POPULATION/guard chain, no counter mutation where stated)

| probe | lane | counter | exit | evidence |
|---|---|---|---|---|
| **P1** | `lane_pop`: one row's `tree` field flipped (`a_class-x14-two-errata`, `8ec1d843…`→`0ec1d843…`), no `.git` | pristine | 1 | `POPULATION … pin=2365fc6f… mismatched=1` + `POPULATION-MISMATCH a_class-x14-two-errata` |
| **P2** | same | M3 | 1 | same output; only the **pin** rejects it (M3 removed the `mismatched` score) |
| **P3b** | `lane_pruned`: the 13 over-refused rows removed (`pop sha256 72ed1b2d…`), no `.git` | pristine | 1 | `POPULATION fixtures=113 pin=72ed1b2d…` + `HONEST fixtures=113 admitted=113 refused=0` → literal 126 **and** pin both fire |
| **P3** | `lane_pruned` | M2b | **0** | `PREDICATE R50-C1 pass` (above) |
| **P3full** | `lane_pruned` | M2b, full | 1 | pass blocked only by `MUTANTS … verdict=unmet` |
| **P4** | `lane_noGit`: symlink farm of the clone with `.git` absent (population untouched) | pristine | 1 | `REV unknown` · `TREE dirty=0` · honest leg red |

```
# P1 (verbatim)
REV unknown
TREE dirty=0
FENCE …/lane_pop/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=2365fc6f60c5cf0d7ecd1fab1e3cb8ab9381179459d66b5d5c577a6c61ae2f62 mismatched=1 build_errors=0
POPULATION-MISMATCH a_class-x14-two-errata
HONEST fixtures=126 admitted=113 refused=13 error=0
PREDICATE R50-C1 fail
# P4 (verbatim, population pristine, lane is not a git repository at all)
REV unknown
TREE dirty=0
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
PREDICATE R50-C1 fail
$ git -C "$S/lane_noGit" rev-parse --show-toplevel
fatal: not a git repository (or any parent up to mount point /)
```

## Kill rule (A3): does the claim still reject the forged receipts?

Implemented as a scratch detector (`cand/receipt_check.py`, sha256 `16eb2e65…`) encoding the frozen kill
rule plus the literal predicate lines: `PREDICATE … pass`, exit 0, `TREE dirty=0`, 40-hex `REV`,
`POPULATION fixtures=126`/pin/`mismatched=0`, `HONEST 126/126/0/0`, `REFUSALS total=20 clean=20 leaked=0`,
`SEALED total≥18 clean=total leaked=0`, `MUTANTS total≥12 caught≥12 verdict=met`.

```
KILL runs/m1_pred_uncond.full.out  : HONEST admitted=113; HONEST refused=13; SEALED total=12 < 18; MUTANTS caught=3 < 12; MUTANTS verdict=unmet
KILL runs/m1_pred_uncond.honest.out: HONEST admitted=113; HONEST refused=13; SEALED total=12 < 18; MUTANTS absent
KILL runs/m1b_honest_unscored.honest.out: HONEST admitted=113; HONEST refused=13; SEALED total=12 < 18; MUTANTS absent
KILL runs/m2_denom_from_pop.honest.out : PREDICATE not pass/absent; exit=1; …
KILL runs/m2b_denom_pin_from_pop.honest.out: PREDICATE not pass/absent; exit=1; …
KILL runs/m3_mismatch_ignored.honest.out  : PREDICATE not pass/absent; exit=1; …
KILL runs/m4_sealed_skipped.full.out      : SEALED absent; …
KILL runs/m1c_forged_receipt.full.out     : SEALED total=12 < 18; MUTANTS caught=3 < 12; MUTANTS verdict=unmet
KILL runs/P3.out   : REV not 40-hex; POPULATION fixtures=113; POPULATION pin != frozen; HONEST fixtures=113; HONEST admitted=113; SEALED total=12 < 18; MUTANTS absent
KILL runs/P3full.out: … MUTANTS caught=3 < 12; MUTANTS verdict=unmet
KILL runs/P1.out / P2.out: REV not 40-hex; POPULATION pin != frozen; mismatched=1; …
```

Every forgery above is rejected at receipt level. The residual risk is bounded, not eliminated: on a
landing tree where `SEALED≥18`, `MUTANTS met` and `HONEST 126/126/0` are true of the *real* run, a counter
that lies about three or more lines at once produces a receipt indistinguishable from an honest one. The
only thing that bounds that is what S3 already requires — the receipt's `REV`, the committed counter
digest, and a clean-clone run — so the guard is procedural (digest + revision), not internal to the counter.

## Findings (counter defects, with the minimal diff already given)

1. **D1 (M1, 2 lines).** The predicate is a self-attestation: `ok` and the printed sentence are one
   expression, so the pass sentence can be printed unconditionally. Base fence → `pass`, exit 0.
2. **D2 (M1b, 1 line).** The HONEST leg computes refusals and prints them but its `ok = False` is the
   *only* place they score. Dropping it is invisible in the receipt's HONEST line and yields a pass under
   the leg-isolated detector; at landing (mutant leg met) it yields the full frozen pass. Highest-value
   fix: make the frozen literal part of the *printed* line's own assertion, e.g. assert
   `admitted == HONEST_TOTAL and refused == 0 and error == 0` and let the predicate print `ok`.
3. **D3 (M2b, 1 line).** One statement guards both the frozen literal `126` and the population pin, so a
   single edit makes the honest denominator self-satisfying; with the 13 over-refused rows pruned the base
   fence reaches `PREDICATE pass`, exit 0 (`POPULATION fixtures=113`, `HONEST 113/113/0`). Split the guards:
   keep `len(rows) != HONEST_TOTAL` and the pin in *separate* conditions, and cross-check the printed
   `POPULATION fixtures=` against the literal.
4. **D4 (P4, no mutation).** The clean-tree guard never looks at git's exit code:
   `subprocess.run([... "status" ...]).stdout.strip().splitlines()` — a lane that is *not a repository at
   all* prints `TREE dirty=0` beside `REV unknown`. "Clean" is therefore unfalsifiable off-repo, and
   `--allow-dirty` is not even needed to score a non-clone. Fix: fail when `rev == "unknown"` or when
   `git status` exits non-zero.
5. **D5 (M3, coverage).** `mismatched` is the only guard against the claim's own host-identity drift (the
   pin cannot see it, because drift does not change `population.txt`); M3 removes it with byte-identical
   output on the base fence. The frozen predicate cannot distinguish "identity pins held" from "identity
   check disabled" on this tree.
6. **D6 (M4, coverage).** Skipping the SEALED leg is invisible to the predicate when the fence does not
   leak sealed modules; the `SEALED50_MIN` floor is a separate branch and does not cover scoring. Only the
   absence of the printed line reveals it.
7. **D7 (accounting/auditability, no mutation).** `for x in refused[:12]` prints at most 12 honest refusals
   while `refused=13`: the receipt cannot enumerate its own honest refusal set. The unnamed 13th is
   `n08-tag-detached` (measured with a throwaway all-refusals diag copy, sha256 `fed278ae…`); full list:
   `n03-detached-head n07-reflog-gc n08-tag-detached n12-local-config-user n13-remote-origin
   n14-stash-entry n15-commit-graph n16-notes-ref n17-replace-ref n18-shallow-fetch n20-linked-worktree
   n21-separate-gitdir n22-alternates-in-d`. Any reader auditing "which five classes" from the receipt alone
   sees twelve lines for a count of thirteen.
8. **D8 (receipt determinism, incidental).** `MUTANT broken … p.stdout.strip()[-160:]` truncates a message
   that contains the work-dir path, so the broken-mutant text shifts with path length and receipts are not
   byte-comparable across runs (observed: `1 out of 1 hunk FAILED` vs `D -- saving rejects` for the same
   row). Truncate from the tail *after* normalising the path.

Incidental measurement for the mutant-battery seat (not my item, not adjudicated): on the base fence the
carried candidate battery reports **`caught=3 broken=12 survived=8`** (`MUTANTS total=23 … verdict=unmet`),
whereas the wave briefing states "4 of 23 change the verdict vector". I measure 3 by the counter's own
definition. Flagged for the seat that re-derives `plans/mutants50/` (QUALITY Q38).

## Restoration evidence (A4)

The clone was never edited: `git -C clone50 status --porcelain` → 0 lines before and after; every mutant is
a separate scratch file. Before/after digests of the three measured objects are unchanged:

```
before  f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  clone50/plans/round50_c1_verify.py
after   f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  clone50/plans/round50_c1_verify.py
before 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  clone50/plans/fixture_fence.py
after  05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  clone50/plans/fixture_fence.py
before b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  clone50/plans/honest50/population.txt
after  b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  clone50/plans/honest50/population.txt
candidate counter under attack: d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2 (unmodified copy)
```

Restored run (pristine counter, full predicate, freeze clone) — exit 1, 7 s — compared to the pre-probe
baseline as a projection of the predicate-bearing lines with temp paths normalised:

```
diff -u runs/before.proj runs/after.proj  ->  PROJECTION IDENTICAL
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
PREDICATE R50-C1 fail
```

## Limits

- Measured against the **freeze** tree (`3b02d57`) and the **tip** counter bytes (`d8787b34`). The S2
  repaired fence is not landed, so no statement here is a measurement of the landing tree; the one landing-
  tree consequence (D2 becoming a full-predicate bypass once `MUTANTS met`) is marked `[INFERENCE]`.
- The base fence is red on two legs, so D_full masks honest-accounting mutations. The leg-isolated detector
  (`--skip-mutants`) is the counter's own "testing only" mode and is not a citable receipt; it is used to
  isolate accounting, never to claim a pass.
- These are **counter** mutants, not fence mutants; the reference vector is the base-fence verdict vector.
  The mutant battery's own accounting is out of scope (D8/incidental only).
- Each mutation was applied one at a time. M1c is explicitly a two-edit extra probe, used only to locate the
  end of the guard stack. Data-side probes P1–P3 edit a scratch *copy* of the population (never the clone);
  they are labelled as data probes, not counter mutants.
- Not measured: outside-`d` read property (r46 counter's job), io_uring, host paths outside the scratch
  root, and any timing/robustness property of the fence itself.
- No tool was installed or upgraded (nothing was needed; no pacman transaction attempted).
- Scratch discipline: `TMPDIR=/fast/scratch/hyaku/kengaku-r50/R50C1MutBypass`, single `--shared` clone,
  `--work` always passed; the tree was removed before yield (see §Scratch).

## Boundary: the lane moved during this wave (measured, read-only)

My clone is at the freeze and is unaffected. The live checkout advanced while I worked, and that is recorded
here so the integrator can date my numbers:

```
start of wave: HEAD c3372a9…  plans/fixture_fence.py 05d5fe03…  plans/round50_c1_verify.py d8787b34…  (clean)
now:           HEAD d6f2fce…  "round-50: mutant battery frozen at the 15 witnessed rows; seven unwitnessed rows dropped"
               plans/fixture_fence.py 57adce4a…  (S2 repair landed; freeze 3b02d57 still an ancestor)
               plans/mutants50/c1-mutants.json rows: 15  (ids c50-01…c50-21; the 23-row r49 candidate is superseded)
               plans/round50_c1_verify.py WORKING-TREE 850ec790… (uncommitted, another seat; HEAD still d8787b34)
```

The committed counter is still exactly the file I attacked (`git show HEAD:plans/round50_c1_verify.py` →
`d8787b34…`). Against the uncommitted working-tree candidate (`850ec790…`, a Q39 name-hiding + subprocess
harness + timeout change) the four constructions I attacked are **unchanged in substance**:

```
245:  if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or mismatched or failures:   # D3/D5
259-260: if refused: / ok = False                                                            # D2
265:  for rel in (REFUSALS_REL, *SEALED_RELS):                                               # D6
337:  say(f"PREDICATE R50-C1 {'pass' if ok else 'fail'}")                                     # D1
218-223: dirty = subprocess.run(["git","-C",str(lane),"status","--porcelain"], …) ; TREE dirty=  # D4 (no returncode check)
```

So D1–D4 apply verbatim to the candidate the lane is currently considering, not only to the tip bytes.

One consequence for the claim's kill rule, not for my verdicts: the MUTANTS leg is now 15 rows, so the
`MUTANTS` masking that kept D_full green-below-red in M1b no longer applies at 15 rows, and my P3full
observation (`MUTANTS unmet` blocking a forged pass) is a property of the freeze tree's 23-row candidate only.
My detector remains the base fence, as assigned; I did not run anything against the repaired fence or the live
checkout.

## Scratch disposition

`/fast/scratch/hyaku/kengaku-r50/R50C1MutBypass` (clone + 10 candidate counters + lane copies + run logs)
was removed before this report was finalised; nothing citable lived there — every command, diff, digest and
verbatim output needed for reproduction is transcribed above.

## VERDICT

Of the six counter-accounting mutations, **three open a bypass of the frozen predicate on the base fence
under at least one detector**: M1 (predicate+exit unconditional — pass, exit 0), M1b (the HONEST leg's only
scoring line removed — pass under the leg-isolated detector, and `[INFERENCE]` the full frozen pass at
landing), and M2b (denominator+pin in one statement — pass, exit 0, once the 13 over-refused rows are pruned
from the population). M2 is killed by the pin, M3 and M4 are killed by the base fence but produce
byte-identical / line-omitting output respectively, i.e. they are **unexercised coverage findings** rather
than demonstrated escapes. Two further accounting defects were measured without any counter mutation: the
clean-tree guard treats "not a git repository" as clean (`REV unknown` beside `TREE dirty=0`), and the receipt
cannot enumerate its own honest refusal set (`refused[:12]` for `refused=13`). Every forged receipt produced
above is still rejected by the claim's receipt-level kill rule, so the counter's real defence is the printed
leg literals plus the S3 digest/REV pin, not the `PREDICATE` sentence; the highest-value repair is D2
(assert the frozen literal from the measured values before printing `ok`). Baseline reproduced exactly and
restored bit-identically; freeze `3b02d57` confirmed an ancestor of lane tip `c3372a9`. No R50-C1 admission
claimed.
