# R48C1ExecControls — the six frozen C1 controls on scratch trees

Seat: `R48C1ExecControls` (executor). Axis served: **calibration** (claim R48-C1). Wave: kengaku round 48
(hyaku run 10), v2 wave 1. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

Item executed: *run the six frozen C1 controls on scratch trees: no fence; base fence @0f77f9b; round-45
keyed fence; admit-all; refuse-all; name-keyed variant. Each control must print `PREDICATE R48-C1 fail`;
capture REV-prefixed receipts. Controls run only on base/control trees, never on claimed work.*

## 1. Result in one line

**All six frozen C1 controls print `PREDICATE R48-C1 fail` and exit 1, at two independent measured revisions
(`0f77f9b` and the stage-1 freeze tip `a543d920`), against the v2 counter candidate — no control passes, the
counter is not refused.**

**VERDICT: controls-pass-as-required (6/6 `PREDICATE R48-C1 fail`, exit 1, at both revisions) — with one
calibration defect found and reported to the L1: the frozen literal `HONEST … refused=9` for the base-fence
control is NOT reproducible from its own committed evidence. The round-46 "9/9 refused" was a `{WORK}`
placeholder-argv artifact, not a repository-state over-refusal. Measured against the frozen 120-fixture
population the base fence refuses **8 of 16** novel honest classes, and only **3 of the 9** round-46 classes.
Detail in §6.**

## 2. Axes named (godspeed step 1)

| axis | what this seat moves | what this seat must not move |
|---|---|---|
| **calibration** (primary) | the six frozen C1 controls, each of which must print `PREDICATE R48-C1 fail`; a control that passes refuses the counter | no re-freeze of a predicate line, a control, or a kill rule after any seat has scored |
| coverage (adjacent, not served) | none — the C1 counter and the C2 package share no input | no C2 probe run (stage-2 ordering; not my item) |
| novelty / depth / operability / freshness / adjacency | none — this seat produces control receipts only | none |

## 3. Freeze check performed before any measurement (Q30 ordering)

Verified in the committed lane tree **before** the first counter run:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git -C … cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
commit
$ git -C … log -1 --format='%H %ci %an %s' a543d92083557dd9b33ee674e9b99b03411f80af
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 kengaku-shokunin round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
```

The stage-1 freeze commit `a543d920` exists in the committed lane tree and **predates every measurement**
below (all measurements ran 2026-10-27 08:39–08:52 -0300). The stage-2 amendment commit does **not** exist
yet, so **no receipt here is a scored receipt on claimed work: every run in this report is a control run on a
base/control tree.** The landed fence (the claimed work) was never measured by this seat.

## 4. Instrument and method (exact)

### 4.1 the counter candidate

`plans/round48_c1_verify.py` does not exist in the lane tree (stage 2 is absent). The counter is a **wave-1
candidate** supplied by the counter seat (`R48C1ExecCounter`). It was superseded once during this wave; **the
receipts below are all against v2**, the final candidate:

```
$ sha256sum /fast/scratch/hyaku/kengaku-r48/R48C1ExecCounter/cand/round48_c1_verify.py
8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f   (433 lines)
```

(v1, `f395e085ce8380c5fc0f65c978ada64b18dc89860b3881f07066009659a0b30c`, embedded its own reconstruction of
the nine round-46 honest classes as `HONEST_SEEDS` with `HONEST_TOTAL=113`. v2 drops that reconstruction and
pins the honest seat's **16 real frozen modules** instead, `HONEST_TOTAL=120`,
`HONEST_NOVEL_EXPECTED=16`, `PINS total=82`. The v1 receipts were superseded and are **not** landed; every
landed receipt is v2.)

### 4.2 the runner

`run_controls.py` (landed at `.ufo/waves/round-48/w1/R48C1ExecControls/run_controls.py`) aborts unless the
counter digest matches, so no receipt can be attributed to a different counter build:

```
$ cd /fast/scratch/hyaku/kengaku-r48/R48C1ExecControls && export TMPDIR=$PWD
$ python3 run_controls.py
```

Per control the runner: `git clone -q --shared <lane> <scratch>/trees/<name>/lane`; `git -C <clone> checkout
-q <rev>`; **asserts `git -C <clone> rev-parse --show-toplevel` equals the clone root before any write**; then
stages the two artifacts the v2 counter needs (the counter itself as `plans/round48_c1_verify.py`, and the 16
frozen novel honest modules under `plans/honest48/`) and runs, inside the round-46 envelope
(`.ufo/waves/round-46/claims/envelope.sh`, copied into scratch):

```
envelope.sh <scratch>/env/<name> \
  python3 plans/round48_c1_verify.py --lane . --work <scratch>/w/<name> --jobs 4 --fence <FENCE>
```

`--fence` selects the fence under test; it keeps the receipt measuring the control rather than an edit of the
lane. The two staged stage-2 artifacts make the tree dirty by exactly that amount, and the counter says so —
every receipt reads `TREE dirty=2 (override)` — so nothing is hidden. `TMPDIR=<scratch>` and
`PYTHONDONTWRITEBYTECODE=1` are exported so no `__pycache__` lands in the measured tree.

## 5. The six controls — verbatim receipts

All six: `REV <40-hex>` first line, `TREE dirty=2 (override)`, `PINS total=82 mismatched=0`, exit 1, last
line `PREDICATE R48-C1 fail`. Receipts (each with the exact command, measured HEAD, counter digest and fence
digest in the header) are at `.ufo/waves/round-48/w1/R48C1ExecControls/receipts/`.

### 5.0 measured revisions

| control | receipt | measured HEAD | exit | predicate |
|---|---|---|---|---|
| no fence | `receipts/control-c1-no-fence.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |
| base fence | `receipts/control-c1-base-fence.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |
| round-45 keyed | `receipts/control-c1-fence-r45-keyed.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |
| admit-all | `receipts/control-c1-fence-admit-all.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |
| refuse-all | `receipts/control-c1-fence-refuse-all.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |
| name-keyed variant | `receipts/control-c1-fence-name-keyed-variant.txt` | `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` | 1 | `PREDICATE R48-C1 fail` |

Replication at the stage-1 freeze tip `a543d92083557dd9b33ee674e9b99b03411f80af` — same six controls, same
fences, same counter digest, each on its own clean clone — **also 6/6 fail**:

```
s1-control-c1-no-fence                  exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=0 refused=0
s1-control-c1-base-fence                exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=112 refused=8
s1-control-c1-fence-r45-keyed           exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=120 refused=0
s1-control-c1-fence-admit-all           exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=120 refused=0
s1-control-c1-fence-refuse-all          exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=0 refused=120
s1-control-c1-fence-name-keyed-variant  exit=1 PREDICATE R48-C1 fail REV=a543d920…  HONEST fixtures=120 admitted=120 refused=0
```

(Receipts `receipts/s1-control-c1-*.txt`.)

### 5.1 no fence — `receipts/control-c1-no-fence.txt`

Fence under test: `…/fences/ABSENT_fence.py` (never created → the fence is absent).

```
REV 0f77f9b27931b3c76b3d095fc0fa70edb79556d9
TREE dirty=2 (override)
PINS total=82 mismatched=0
FENCE /fast/scratch/hyaku/kengaku-r48/R48C1ExecControls/fences/ABSENT_fence.py absent
LITERALS refusals=20 sealed=12 honest=120
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=0 read=0 hung=0 build_errors=0
BENIGN total=0
ERRORS total=152
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean,honest-not-admitted,errors=152
PREDICATE R48-C1 fail
```

Every fixture decision errors out (`ERRORS total=152`). **A second, independent shape of the same control** —
the round-46 shape, `plans/fixture_fence.py` *deleted* from the clone, counter in default mode — is at
`receipts/diag-v2-no-fence-default-mode.txt`:

```
FENCE-RUN sealed sealed46/a_phantom_anchor.py phantom-anchor-reject ERROR error touches=0 calls=432 -- HARNESS-ERROR RuntimeError: fence absent
TREE dirty=3 (override)
ERRORS total=152
REASON refusals-not-clean,sealed-not-clean,honest-not-admitted,errors=152
PREDICATE R48-C1 fail
```

### 5.2 base fence @0f77f9b — `receipts/control-c1-base-fence.txt`

Fence under test: `plans/fixture_fence.py` in the clone @ `0f77f9b`, sha256
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` (identical at `a543d920`).

```
REV 0f77f9b27931b3c76b3d095fc0fa70edb79556d9
TREE dirty=2 (override)
PINS total=82 mismatched=0
FENCE source=…/trees/control-c1-base-fence/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
LITERALS refusals=20 sealed=12 honest=120
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=16 expected_novel=16 novel_modules=16
BENIGN total=112
CALIBRATION advertised=32 contradicted=0
REASON honest-not-admitted
PREDICATE R48-C1 fail
```

The base fence **fails on the honest leg** (`refused=8`), with the hostile legs clean — exactly the
over-refusal signature the claim targets. See §6: `refused=8`, not the frozen `refused=9`.

### 5.3 round-45 keyed fence — `receipts/control-c1-fence-r45-keyed.txt`

Fence: `.ufo/waves/round-45/claims/fences/keyed_name.py`, sha256
`d21a6a173c68b13ce9abcd2716f37afaed1930646faa43a266adfd4258b9452e` (the fence that passed the round-45
counter).

```
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
BENIGN total=169
BENIGN-MODULES refusals=34 sealed=15 honest=120
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean
PREDICATE R48-C1 fail
```

The keyed fence cannot name the hostile modules (Q39 name hiding), so it admits all 34 refusal fixtures and
15 sealed fixtures — but with **zero traced outside access**, so under delta (b) these are `BENIGN-ADMIT`, not
`LEAK`, and `contradicted=0`. The hostile legs still cannot print `clean=total`, so the predicate fails.
Note: a kill rule keyed *only* on "traced outside access" would not catch this fence. Flagged in §7.

### 5.4 admit-all — `receipts/control-c1-fence-admit-all.txt`

Fence: `.ufo/waves/round-45/claims/fences/admit_all.py`, sha256
`6c3b9a18566a7045d679263867b64ff0735bc79a39abe7e57dfffd724f05d912`.

```
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
BENIGN total=169
BENIGN-MODULES refusals=34 sealed=15 honest=120
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean
PREDICATE R48-C1 fail
```

### 5.5 refuse-all — `receipts/control-c1-fence-refuse-all.txt`

Fence: `.ufo/waves/round-45/claims/fences/refuse_all.py`, sha256
`fc38325360ee7058401ff88c738ce4a7f5e0d8e97196b605b4b57dfed79ef867`.

```
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=0 refused=120 read=0 hung=0 build_errors=0
BENIGN total=0
CALIBRATION advertised=32 contradicted=0
REASON honest-not-admitted
PREDICATE R48-C1 fail
```

### 5.6 name-keyed variant — `receipts/control-c1-fence-name-keyed-variant.txt`

This is the sixth control and it is **scratch-authored by this seat** (the frozen claims list five controls
and name "the round-45 keyed fence" as the fifth; the item adds a name-keyed variant). Source:
`.ufo/waves/round-48/w1/R48C1ExecControls/fences/name_keyed_variant.py`, sha256
`560b746eb7049686983099e24b87987124f513c2f562a457086d122ba474963f`.

It is a stricter name-keyed control than the round-45 fence: it scans the **last three path components of
`d`**, the basename of `d`, and **every argv basename** for group/module markers (`refusal`, `sealed`,
`battery`, `h01`…`h09`, `n01`…`n16`, `f1_`…`f20_`, `a_class`, `o_scan`, `u5_`, …) and opens nothing.

```
FENCE source=…/fences/name_keyed_variant.py sha256=560b746eb7049686983099e24b87987124f513c2f562a457086d122ba474963f
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
BENIGN total=169
BENIGN-MODULES refusals=34 sealed=15 honest=120
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean
PREDICATE R48-C1 fail
```

Behavioural check of the control itself (direct calls to `breach`, not a counter run):

```
opaque names -> admit                        -> None
hostile group name -> refuse                 -> 'name-keyed refusal: refusal in refusals46'
hostile module name in argv -> refuse        -> 'name-keyed refusal: f17_ in f17_argv_nul.py'
honest -> admit                              -> None
```

**Self-correction, disclosed.** Revision 1 of this fence scanned *every* path component of `d`, including the
scratch prefix, which contains `r48`; that marker matched on every fixture and the control degenerated into
refuse-all (its receipt showed `HONEST refused=113`, indistinguishable from the refuse-all control).
Revision 2 restricts the scan to the names the counter actually chooses (the last three path components plus
argv basenames) and was re-run; the receipt above is revision 2. Both revisions print
`PREDICATE R48-C1 fail`, but only revision 2 measures name-keying rather than refuse-all. The revision-1
receipt is not landed.

## 6. Calibration defect found: the frozen `refused=9` literal is not reproducible

The frozen claims set the base-fence control's expected failure mode as **"the 9 round-46 novel honest
classes refused — `HONEST … refused=9` minimum"** (`plans/round-48-claims.md` lines 66–67, and the do-nothing
control at lines 130–132: *"the 9 round-46 novel classes are refused by the base fence"*). The round-46 lesson
routes the same figure: *"repair over-refusal (9/9 novel honest controls refused)"*
(`corpus/lessons/round-46-verifier-spotcheck.md` line 45).

**Measured: `refused=8` of 120, and only 3 of the 9 round-46 classes** — and the mechanism is not repository
state at all.

### 6.1 the round-46 nine were refused by a placeholder, not by their state

The round-46 wave-2 receipt (`.ufo/waves/round-46/w2/R46W2C1HoHonest/receipts/c1-counter-override.txt`) shows
all nine refusals with **one** reason:

```
$ grep -E "^FENCE-RUN sealed sealed46/honest_" …/R46W2C1HoHonest/receipts/c1-counter-override.txt | awk '{print $NF}' | sort | uniq -c
      9 BREACH --lane value '{WORK}/repo' is a placeholder the fence cannot resolve
```

Every one of the nine was refused because the module's `--lane` argv value was the **unresolved `{WORK}`
placeholder token**, which the fence refuses by design (`plans/fixture_fence.py`: *"a placeholder the fence
cannot resolve"*). The repository state — packed refs, annotated tags, detached HEAD, merge commit,
`.gitignore`, 30-commit history, reflog gc, tag+detached, ignored untracked — was never the reason.

**Direct confirmation** (this seat's own probe, receipt `receipts/diag-v2-placeholder-argv.txt`): **the same
repository**, built by the same code, differing only in the argv value — `--lane {WORK}/repo` is refused with
exactly that reason, `--lane repo` is admitted:

```
FENCE-RUN honest placeholder/p01_placeholder_argv.py p01-placeholder-argv BREACH clean touches=0 calls=433 -- BREACH --lane value '{WORK}/repo' is a placeholder the fence cannot resolve
FENCE-RUN honest placeholder/p02_resolvable_argv.py p02-resolvable-argv ADMIT benign touches=0 calls=499 -- ADMIT
```

### 6.2 what the base fence actually refuses

Against the frozen 120-fixture honest population (104 battery + 9 r46novel + 7 novel48), the base fence
refuses **8** — `HONEST fixtures=120 admitted=112 refused=8`
(`receipts/control-c1-base-fence.txt`), per class:

| novel class | base-fence verdict | refusal reason |
|---|---|---|
| `n01` packed refs | ADMIT | — |
| `n02` annotated tag | ADMIT | — |
| `n03` detached HEAD | **BREACH** | `repo/.git/HEAD is not a plain branch HEAD` |
| `n04` merge commit | ADMIT | — |
| `n05` `.gitignore` | ADMIT | — |
| `n06` 30-commit linear | ADMIT | — |
| `n07` reflog gc | **BREACH** | `repo/.git/info/refs is not git's exclude file` |
| `n08` tag + detached HEAD | **BREACH** | `repo/.git/HEAD is not a plain branch HEAD` |
| `n09` ignored untracked | ADMIT | — |
| `n10` empty repo | ADMIT | — |
| `n11` multibranch | ADMIT | — |
| `n12` local `[user]` config | **BREACH** | `repo/.git/config section [user] is not allowlisted` |
| `n13` remote origin | **BREACH** | `repo/.git/config section header b'[remote "origin"]' is not plain` |
| `n14` stash entry | **BREACH** | `refs/stash has a name git does not write` |
| `n15` commit-graph | **BREACH** | `repo/.git/objects/info/commit-graph present (object-store redirect)` |
| `n16` notes ref | **BREACH** | `refs/notes has a name git does not write` |

⇒ **3 of the 9** round-46 classes (`n03`, `n07`, `n08`) and **5 of the 7** new classes are refused; the other
**6 of the 9** round-46 classes are admitted by the base fence. So the base fence's true over-refusal set is
two causes among the round-46 nine — a **detached HEAD** and a **`.git/info/refs`** file — and five more
state causes among the seven new classes.

The `.git/info/refs` cause is a `git gc` artifact, verified independently:

```
$ git -C $T init && … && git -C $T pack-refs --all && git -C $T gc -q --prune=now && ls $T/.git/info/
exclude
refs            # gc writes .git/info/refs
$ git -C $T2 init && … && git -C $T2 pack-refs --all --prune && ls $T2/.git/info/
exclude         # pack-refs alone does not
```

So there **is** a genuine over-refusal defect in the base fence — the round-46 lesson's routing is right in
kind — but its true size is far smaller than the frozen literal, and the frozen literal's own source evidence
(refusal reason = an unresolvable argv placeholder) does not measure repository states at all.

### 6.3 consequence for the L1 at stage 2

**No re-freeze of a predicate line, control or kill rule is implied, and I performed none.** The base-fence
control's *requirement* — it must print `PREDICATE R48-C1 fail` — is intact and met. Only the parenthetical
measurement `HONEST … refused=9` is unreproducible. The honest options for the L1 are (a) to record the
measured figure in the stage-2 receipt, which is exactly what the claims themselves call for ("the stage-2
receipt re-measures it on the base fence", lines 131–132), or (b) to amend the parenthetical in a named
`Freeze amendments` paragraph. **I make no admission claim for R48-C1.**

## 7. Risks and limits (named, not hidden)

1. **The counter is a wave-1 candidate, not the stage-2 pinned instrument.** Digest
   `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f` (v2, 433 lines); stage 2 may change it.
   Every receipt here is a *control receipt against that candidate*, re-runnable with `run_controls.py` against
   any replacement counter. **No receipt in this report is a scored receipt on claimed work.**
2. **The measured tree carries the two stage-2 artifacts** (`plans/round48_c1_verify.py` and 16 modules under
   `plans/honest48/`), so the six control receipts read `TREE dirty=2 (override)` rather than `TREE clean`;
   the default-mode no-fence diagnostic reads `dirty=3` because it additionally deletes
   `plans/fixture_fence.py`. This is disclosed in every receipt header; the dirty entries are exactly those
   stage-2 paths (plus the deleted fence in that one diagnostic) and nothing else.
3. **`HONEST_TOTAL=120` is a stage-2 literal, not yet frozen.** v2 reconciles the double-count risk I flagged
   against v1: it drops the embedded seed reconstruction and pins the honest seat's 16 modules by digest
   (`PINS_EXTRA`), so the nine round-46 classes are counted **once**. The counter also binds the novel count
   from the other side (`HONEST_NOVEL_EXPECTED=16`): a population that loses or mixes a novel module is a
   `PINS` mismatch and an `honest-novel=…!=16` failure, not a silent narrowing. **This resolves my earlier
   risk (v1 had two candidate sources for the nine classes); the L1 still has to pin `<H>` at stage 2.**
4. **The kill rule as written does not catch a name-keyed fence.** A fence that admits every hostile module
   with **zero traced outside access** yields `BENIGN` admissions and `contradicted=0`, and would satisfy a
   kill rule keyed only on "traced outside access". The controls still fail, because the frozen predicate also
   requires `clean=total` per hostile leg. If the kill rule is meant to be sufficient on its own, it needs the
   L1's attention; I did not touch it.
5. **The base fence's over-refusal set is eight state causes**, not nine round-46 classes: detached HEAD
   (`.git/HEAD` holding a 40-hex sha) and `git gc`'s `.git/info/refs`, plus local `[user]` config,
   `[remote "origin"]`, `refs/stash`, `objects/info/commit-graph` and `refs/notes`. A repair that only widens
   the `HEAD` allowlist would still refuse every `git gc` repository, and vice versa; all eight need
   consideration.
6. **The name-keyed variant control is scratch-authored**, not part of the frozen five-control list. It is
   evidence for Q39 name hiding, not a frozen control; the L1 should decide whether to fold it into the
   stage-2 control set.
7. **Name hiding was observed, not assumed**: the counter's fixture dirs, build dirs and parents are opaque
   per-run tokens and the job order is shuffled, which is why both name-keyed controls (round-45's and mine)
   admitted every hostile module.
8. **`--jobs 4`, not 8**: the host was shared with ~50 concurrent wave seats. Job count affects only
   throughput, not verdicts (the round-46 counter's per-fixture verdicts are order-independent by
   construction), but the run order differs from a `--jobs 8` run.
9. **Host-path reads outside the scratch root are not counted** by the counter (a named limit inherited from
   round 46), so "no traced outside access" means "no traced outside access *under the scratch root*".
10. **`io_uring` SQE opens/reads emit no traced syscall** (inherited named limit, not exploited here).
11. **The counter seat reported a known build race** in the frozen fixture `plans/refusals46/f16_objects_hardlink_out.py`
    (it hardlinks `objects/` while git may drop `maintenance.lock`). No receipt in this report shows a
    `BUILD-ERROR` on it: every control's `REFUSALS total=20 … build_errors=0` and `MODULES refusal total=20`.

## 8. Sources (URL / access date / located quote)

All sources are local lane files (no external URL was opened for this item; the round-48 sourced-basis
requirement, §2b, attaches to R48-C2, not to this seat's controls). Access date for all: **2026-10-27**.

| # | source (path) | rev | located quote (≤25 words) |
|---|---|---|---|
| S1 | `plans/round-48-claims.md` (lane) | `a543d920` | L65–68: "Controls that must print `PREDICATE R48-C1 fail` at stage 2 … no fence; the **base fence**" |
| S2 | `plans/round-48-claims.md` (lane) | `a543d920` | L130–132: "the fence at base tip `0f77f9b` under the stage-2 pinned v3 counter must fail on the honest leg" |
| S3 | `corpus/lessons/round-46-verifier-spotcheck.md` (lane) | `a543d920` | L45: "repair over-refusal (9/9 novel honest controls refused) and broaden positive controls" |
| S4 | `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (lane) | `a543d920` | L3: "all nine are newly named modules in the counter's `--sealed` override" |
| S5 | `.ufo/waves/round-46/w2/R46W2C1HoHonest/receipts/c1-counter-override.txt` (lane) | `a543d920` | FENCE-RUN: "`BREACH --lane value '{WORK}/repo' is a placeholder the fence cannot resolve`" |
| S6 | `plans/fixture_fence.py` (lane) | `a543d920` (sha256 `05d5fe03…`) | L3: "admit only a fixture whose git store is provably the shape a plain `git init` + commits writes inside `d`" |
| S7 | `plans/round46_c1_verify.py` (lane) | `a543d920` (sha256 `ef19380e…`) | L627: "`PREDICATE C1 {'pass' if good else 'fail'}`" |
| S8 | `plans/round44_c1_verify.py` (lane) | `a543d920` (sha256 `6cf05323…`) | L141: "`WORK_TOKEN = re.compile(r\"^\\{WORK(?::([a-z]+))?\\}(/[A-Za-z0-9._/-]+)?$\")`" |
| S9 | `.ufo/waves/round-45/claims/fences/keyed_name.py` (lane) | `a543d920` | "keys the verdict on the counter-chosen fixture path (R45CriticPredicate B2)" |
| S10 | `.ufo/waves/round-45/claims/fences/admit_all.py` (lane) | `a543d920` | "admits every fixture (no fence at all)" |
| S11 | `.ufo/waves/round-45/claims/fences/refuse_all.py` (lane) | `a543d920` | "refuses every fixture (no fence at all)" |
| S12 | `.ufo/waves/round-46/claims/envelope.sh` (lane) | `a543d920` | "a `CHANGED` digest marks the measurement it brackets invalid" |
| S13 | `.ufo/waves/round-48/w1/R48C1ExecHonest/` (lane wave dir, sibling seat) | uncommitted | "population.txt … 120 HONEST lines … battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 = 120" |
| S14 | counter candidate v2 `round48_c1_verify.py` (sibling seat `R48C1ExecCounter`, scratch → my inbox copy) | sha256 `8726e99b…` | "`PREDICATE R48-C1 {'pass' if good else 'fail'}`" |

## 9. Artefacts landed (all under my seat's exclusive path)

- `.ufo/waves/round-48/w1/R48C1ExecControls.md` — this report.
- `.ufo/waves/round-48/w1/R48C1ExecControls/receipts/` — 15 receipts: 6 base-tip controls, 6 stage-1-tip
  replications, 2 diagnostics (default-mode no-fence, placeholder-argv probe), 1 summary.
- `.ufo/waves/round-48/w1/R48C1ExecControls/fences/` — the four control fences used (three copied from the
  lane's round-45 claims dir, one scratch-authored) plus the v2 counter candidate copy.
- `.ufo/waves/round-48/w1/R48C1ExecControls/run_controls.py` — the runner (aborts on a counter-digest
  mismatch; stages the two stage-2 artifacts into each clone).

No production file was edited; no commit, push or mutating git/jj command was run in the lane; the lane tree
is untouched by this seat apart from these untracked wave artefacts. Scratch
`/fast/scratch/hyaku/kengaku-r48/R48C1ExecControls/` was removed after the receipts were copied into the wave
report dir.

## 10. VERDICT

**VERDICT: controls-pass-as-required.** 6/6 frozen C1 controls print `PREDICATE R48-C1 fail` (exit 1) at
`0f77f9b` and at the stage-1 freeze tip `a543d920`, against the v2 counter candidate
(sha256 `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`); no control passes; the v3
counter is not refused by any of them. **Flagged for the L1 at stage 2 (one item; no re-freeze performed
here):** the frozen `HONEST … refused=9` base-fence literal is unreproducible — the round-46 "9/9" was a
`{WORK}` placeholder-argv artifact, and against the frozen 120-fixture population the base fence refuses
**8 of 16** novel honest classes (**3 of the 9** round-46 classes: detached HEAD, `git gc`'s
`.git/info/refs`, tag+detached HEAD). The control still fails, as it must. **I make no admission claim for
R48-C1 or R48-C2.**
