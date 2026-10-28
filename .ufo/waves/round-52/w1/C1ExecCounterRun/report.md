# C1ExecCounterRun — R52-C1 frozen-counter run (kengaku round 52, wave 1, build)

**Seat:** `C1ExecCounterRun` (executor) · **Axis judged:** novelty · **Claim:** R52-C1
**Lane:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · **Counter:**
`plans/round52_c1_grader_audit.py` (sha256 `e43ff9e7cd2242ce62b561fbae67e41cb478be156d03ffc412972cdf7593e6be`, **unmodified**)

---

## 1. Headline

The frozen counter runs and the counter's **selftest passes (exit 0)**, but **R52-C1's predicate
leg 1 is structurally unreachable with this counter**: `CAPTURES present` counts only the 89
*primary* graders while `expected` is the frozen population's **184** capture files. With all 184
capture files present and independently verified byte-exact against upstream at the pin, the
counter prints `CAPTURES expected=184 present=89 mismatched=0` and `PREDICATE R52-C1 fail`
(exit 1). **No capture set, however complete, can make `present == expected` true**, so the
counter can never print `pass`/exit 0. Per the claims' own kill rule, C1 is therefore *not
admitted* unless the L1 issues a corrected counter (a frozen-rule change → append-only
amendment / new round, L1's call). I did **not** change the counter.

Everything else in the predicate is reachable and was measured to reach: with the captures in
place and the confirmation / prior-art / labels evidence present, the counter prints
`classified=89`, `CONFIRMED new=2`, `PRIOR-ART ok=True urls=3`, `LABELS agree=3 of 3` — and
still `PREDICATE fail`, solely on `present=89 != expected=184`.

---

## 2. What I did

1. Cloned the lane into my scratch dir (shared clone, `master`), verified the toplevel path,
   and confirmed the clone HEAD.
2. Ran the frozen counter with **no captures** (reproducing the claims' frozen *before* block
   exactly) and ran `--selftest`.
3. Copied the 184 grader captures produced by `C1ExecFetchGraders` into
   `corpus/evidence/round52/graders/` inside the scratch clone and re-ran the counter.
4. Independently re-verified all 184 captured files byte-exact against
   `raw.githubusercontent.com` at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (sha256
   comparison, 184/184 match) — I did not take the sibling's word for it.
5. Ran a probe matrix (in the scratch clone only) to isolate which counter legs react to which
   capture mutations.
6. Measured the counter's classification against the **literal** frozen rules in
   `plans/round-52-claims.md` §C1 (offline recomputation, counter untouched).
7. Wrote this report and the receipt artefacts under my wave-report dir; removed my scratch
   dir.

---

## 3. Exact commands run

```sh
SEAT=/fast/scratch/hyaku/kengaku-r52/C1ExecCounterRun
mkdir -p $SEAT/tmp

git clone --shared -b master /home/vgpnk/Projects/shokunin/kengaku-shokunin $SEAT/lane
git -C $SEAT/lane rev-parse --show-toplevel     # /fast/scratch/hyaku/kengaku-r52/C1ExecCounterRun/lane
git -C $SEAT/lane rev-parse HEAD                  # 1315234bdc8024499d943f0483dcb51fb5e4a618

# R1 — before state (no captures in the clone)
cd $SEAT/lane && python3 plans/round52_c1_grader_audit.py --lane .        # exit 1
cd $SEAT/lane && python3 plans/round52_c1_grader_audit.py --selftest       # exit 0

# install the sibling's captures
mkdir -p $SEAT/lane/corpus/evidence/round52/graders
cp -a /fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders/graders/. \
      $SEAT/lane/corpus/evidence/round52/graders/
cp -a /fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders/SHA256SUMS \
      $SEAT/lane/corpus/evidence/round52/graders/SHA256SUMS

# R2 — counter with captures in place
cd $SEAT/lane && python3 plans/round52_c1_grader_audit.py --lane .        # exit 1

# independent byte-exactness check of all 184 captures vs upstream at the pin
PIN=2fd12b88aafdd04a52c298e3940bcb189f9766d6
while read -r p; do
  curl -sS --max-time 30 -o "$out" \
    "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/$PIN/$p"
  sha256sum "$out" "$FG/graders/$p"          # compare
done < /fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders/tmp/paths.txt

# probe matrix (scratch clone only) — see §6
```

No tool was installed or upgraded (nothing to install: system `python3 3.14.8`, `git 2.56.0`,
`curl 8.23.0`, `sha256sum 0.8.0` sufficed). No `pacman` transaction was attempted.

---

## 4. Measured output — verbatim

### 4.1 R1 — counter on the base tree, no captures (reproduces the claims' *before* block)

Command: `python3 plans/round52_c1_grader_audit.py --lane .` (clone HEAD `1315234`, no
`corpus/evidence/round52/` present) — **exit code 1**:

```
TASKS total=89 records=89 classified=0
CAPTURES expected=184 present=0 mismatched=0
CLASS V1=0 V4=0 V2=0 V3=0 V0=89
CANDIDATES total=0
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
```

This is byte-identical to the claims' frozen *before* block (`plans/round-52-claims.md` §C1).

**Base-tip nuance:** the counter itself is **absent at base tip `30801b4`**
(`git cat-file -e 30801b4:plans/round52_c1_grader_audit.py` → *exists on disk, but not in
that commit*); it arrives with the freeze commit `1315234bdc8024499d943f0483dcb51fb5e4a618`
(`master` == `1315234`, parent = base tip `30801b4`). So the *before* count is only
reproducible as "counter at the freeze commit + base-tip tree", which is what I ran.

### 4.2 R2 — `--selftest`

Command: `python3 plans/round52_c1_grader_audit.py --selftest` — **exit code 0**:

```
SELFTEST classify cases=4 failures=0
SELFTEST cases=6 failures=0
```

The selftest battery passes. It exercises the four classify cases and the prior-art
file/URL-count logic; it does **not** exercise `collect()`'s capture counting, which is where
the blocker lives.

### 4.3 R3 — counter with all 184 captures in place

Command: `python3 plans/round52_c1_grader_audit.py --lane .` (scratch clone,
`corpus/evidence/round52/graders/` = 184 files + `SHA256SUMS`) — **exit code 1**:

```
TASKS total=89 records=89 classified=89
CAPTURES expected=184 present=89 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=32 V0=2
CANDIDATES total=2
  CANDIDATE pytorch-model-recovery class=V1 grader=pytorch-model-recovery/tests/test_outputs.py
  CANDIDATE torch-tensor-parallelism class=V1 grader=torch-tensor-parallelism/tests/test_outputs.py
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
```

Same output with `SHA256SUMS` in the sibling's shipped form (`./path` keys) and with the keys
rewritten to plain population paths — see F2 for why.

### 4.4 R4 — feasibility probe with the missing evidence present (synthetic, scratch only)

I added, **inside the scratch clone only**, a `confirmations.json` with the two counter-flagged
candidates (real quotes taken from their grader bytes), a `prior-art.md` with three URLs, and a
`labels.json` with three blind labels. **These are probe fixtures, not evidence** — they exist
only to isolate which leg blocks. Result — **exit code 1**:

```
TASKS total=89 records=89 classified=89
CAPTURES expected=184 present=89 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=32 V0=2
CANDIDATES total=2
  CANDIDATE pytorch-model-recovery class=V1 grader=pytorch-model-recovery/tests/test_outputs.py
  CANDIDATE torch-tensor-parallelism class=V1 grader=torch-tensor-parallelism/tests/test_outputs.py
CONFIRMED new=2 ['pytorch-model-recovery', 'torch-tensor-parallelism']
PRIOR-ART ok=True urls=3
LABELS agree=3 of 3
PREDICATE R52-C1 fail
```

→ legs 2, 3, 4 and the LABELS evidence all reach; **leg 1 is the sole blocker**.

---

## 5. Predicate-leg status (frozen legs 1–4 + evidence leg 5)

| leg | frozen requirement | measured at my run | status |
|---|---|---|---|
| 1 | `CAPTURES expected=184 present=184 mismatched=0` | `present=89 mismatched=0` | **FAIL — structurally unreachable (F1)** |
| 2 | `TASKS total=89 records=89 classified=89` | `total=89 records=89 classified=89` | **PASS** (with captures) |
| 3 | `CONFIRMED new ≥ 2` with located quote, reader, confirmed | `new=0` (no `confirmations.json` yet); probe shows `new=2` reachable | **not yet satisfiable — evidence missing** (`corpus/evidence/round52/confirmations.json`) |
| 4 | `PRIOR-ART ok=True urls ≥ 3` | `ok=False urls=0`; probe shows `ok=True urls=3` reachable | **not yet satisfiable — evidence missing** (`corpus/evidence/round52/prior-art.md`) |
| 5 | `LABELS agree/total` reported (evidence, not a leg) | `agree=0 of 0` (no `labels.json`); probe `3 of 3` | evidence missing (`corpus/evidence/round52/labels.json`) |

**Missing evidence, itemised:** `corpus/evidence/round52/confirmations.json` (leg 3),
`corpus/evidence/round52/prior-art.md` (leg 4), `corpus/evidence/round52/labels.json` (leg 5
evidence). None of these is my lane's product — they belong to the classifier / prior-art /
blind-labrat seats. Leg 1 needs no evidence; it needs a **counter** change.

---

## 6. Findings against the frozen counter (measurements, not opinions)

**F1 — blocker: `CAPTURES present` counts primaries only; leg 1 is unreachable.**
`collect()` increments `present` once per **task** (only the primary grader file is stat-ed);
`expected = pop["capture_file_count"] = 184`. So `present ≤ 89` always.
Measured: all 184 population files present → `present=89`. Probe P4 (drop a non-primary
capture) → `present=89` unchanged; probe P5 (drop a primary capture) → `present=88`;
population-wide check (offline, counter untouched): **184/184 present, 0 mismatched**.
Minimal repair (L1's call, changes a frozen instrument): count the population paths
(`pop["capture_population"]`), not the per-task primary grader.

**F2 — the digest leg is silently vacuous with the shipped `SHA256SUMS` format.**
`load_sums()` keys on field 2 verbatim (only `lstrip("*")`). The `SHA256SUMS` produced by
`C1ExecFetchGraders` is in `sha256sum ./*` form, i.e. keys are `./<population-path>`
(digest `b9ada6472642fa547935c6a1d4fb9474db4d84b412fb9ab3c1730fd65bc974c8`). No key then
matches a population path, so the digest comparison never fires. Measured: probe P6 corrupts
a primary grader's bytes and, with plain-path keys, the counter reports `mismatched=1`;
probe P7 makes the *same* corruption with `./`-prefixed keys and the counter reports
`mismatched=0`. As landed, "digest-pinned" is unverified.

**F3 — 95 of the 184 capture files are never checked.** The counter only ever hashes the 89
primary `tests/test_outputs.py` graders. The other 95 (89 `test.sh`, 5
`environment/tests/test_outputs.py`, 1 `verify.sh`) are neither counted nor digest-verified, so
the claims' leg-1 wording ("every grader file of the frozen population is captured byte-exact
and digest-pinned") is not what this counter measures.

**F4 — the frozen control `c1-control-drop-capture` cannot produce its claimed signature.**
The claims require that control to fail on `present=183 mismatched=1`. Measured: dropping a
capture yields `present=88` (primary dropped) or `present=89` (non-primary dropped), always
`mismatched=0`. `present=183` is unreachable under this counter (max 89) and a dropped file
never increments `mismatched`.

**F5 — `lane_read_tasks()` extracts garbage, so leg 3's "never read before" test is not
enforced.** Measured return: `{'0', 'this'}` (2 entries, both spurious) instead of the 12
hand-read task names. Cause: the knowledge entries use
`# Terminal-Bench 2.0 task grader, read and executed: \`build-pmars\`` — the regex
``task `([a-z0-9-]+)` `` needs `task `` adjacency, and the fallback `\b([a-z0-9-]+)\b task`
matches phrases like "0 task" / "this task". Consequence: a confirmation for any of the 12
already-read tasks (`build-pmars`, `circuit-fibsqrt`, `constraints-scheduling`,
`db-wal-recovery`, `feal-differential-cryptanalysis`, `feal-linear-cryptanalysis`,
`git-leak-recovery`, `configure-git-webserver`, `password-recovery`, `polyglot-c-py`,
`protein-assembly`, `regex-log`) would still be counted as `CONFIRMED new`. The 12 real names
are recoverable from the `read and executed: \`<name>\`` line — a one-line regex fix.

**F6 — the counter's marker regexes diverge from the claims' literal frozen rules on 3 of 89
tasks (3.4 %), and the divergence shrinks the triage queue.** The counter's `CONTENT` regex
adds `assert.*\bin\b`, which the claims' frozen content-marker list does **not** contain; the
counter's `PRESENCE` regex requires a word boundary (`\b`) before `exists(`, while the claims'
frozen presence marker is the bare substring `exists(`. Measured, recomputed offline with the
claims' literal regexes over the same 89 captured graders:

| task | counter class | claims-literal class | cause |
|---|---|---|---|
| `bn-fit-modify` | V3 | **V1** | extra `assert.*\bin\b` content marker |
| `portfolio-optimization` | V3 | **V1** | extra `assert.*\bin\b` content marker |
| `distribution-search` | V0 | **V1** | counter's `\b` excludes `def test_distribution_file_exists():` (a bare-substring presence match) |

Class totals: counter `V1=2 V4=0 V2=53 V3=32 V0=2`; claims-literal `V1=5 V4=0 V2=53 V3=30
V0=1`. **Triage queue: 2 candidates under the counter, 5 under the claims' literal rules.**
The three dropped candidates (`bn-fit-modify`, `distribution-search`, `portfolio-optimization`)
are exactly the kind of presence-only grader the queue exists to find. Note: leg 3's
`CONFIRMED` counter does not require the confirmed task to be a candidate, so this divergence
does not by itself block leg 3 — but it does change what a second reader is asked to read.

**F7 — `CONFIRMED` is looser than the claims.** The claims say "a *candidate* becomes a
confirmed finding only when an independent second reader locates the weakness"; the counter
counts any confirmation whose task is not in its (broken, F5) read-set, with no candidate
membership requirement and no check that the quote actually appears in the grader bytes.

**F8 — cosmetic.** The `CLASS` line prints `V1 V4 V2 V3 V0` (CLASS_ORDER) while the claims'
table order is `V1 V2 V3 V4 V0`; both use the same first-match-wins precedence, so classes are
unaffected. `primary_grader()`'s `environment/` fallback never fires: all 89 tasks have a
`tests/test_outputs.py` (89 distinct primaries, 0 environment primaries).

---

## 7. Independent evidence I produced about the capture set (so the L1 need not trust the sibling)

* **184/184 files fetched from `raw.githubusercontent.com` at pin `2fd12b88…` match the
  capture set byte-for-byte by sha256** — `ok=184 digest_diff=0 non200=0`
  (receipt: `artifacts/independent_upstream_digest_check.txt`). This is my own check,
  independent of `C1ExecFetchGraders`' receipt.
* Population-wide check over the same set (offline, counter untouched):
  `present=184, mismatched=0, files with no SHA256SUMS entry=0`, counter-visible primaries=89
  (receipt: `artifacts/population_wide_capture_check.txt`).

---

## 8. Files produced (absolute paths)

Report (this file):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecCounterRun/report.md`
Flat copy (per the milestone path):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecCounterRun.md`

Receipts (all under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecCounterRun/artifacts/`):

| file | content |
|---|---|
| `run1_verdict_no_captures.txt` | R1 stdout + `EXIT=1` (claims' before-block) |
| `run2_selftest.txt` | `--selftest` stdout + `EXIT=0` |
| `run3_captures_sha256sums_dotprefix.txt` | R3 with the shipped `./`-key `SHA256SUMS` |
| `run4_captures_sha256sums_plainpaths.txt` | R3 with plain-path `SHA256SUMS` |
| `run5_probe_synthetic_evidence.txt` | R4 feasibility probe (synthetic fixtures, labelled) |
| `probe_matrix_capture_mutations.txt` | P0/P1/P4/P5/P6/P7/P8 matrix |
| `class_delta_counter_vs_claims_literals.txt` | F6 recomputation, per-task deltas |
| `lane_read_tasks_extraction.txt` | F5 measured extraction `{'0','this'}` |
| `independent_upstream_digest_check.txt` | 184/184 upstream sha256 match |
| `population_wide_capture_check.txt` | 184 present / 0 mismatched / 89 counter-visible |

Scratch dir `/fast/scratch/hyaku/kengaku-r52/C1ExecCounterRun/` (clone, probe clone, tmp) was
**removed before yielding**; every receipt worth keeping was copied into the artifacts dir
above. Free space seen on the scratch filesystem: 532 G available (NVMe, `/fast`).

Nothing outside my scratch dir and my wave-report dir was written. The lane tree
(`/home/vgpnk/Projects/shokunin/kengaku-shokunin`) has **no** tracked-file modifications from
this seat (`git status --porcelain` shows only untracked wave-report directories belonging to
the L1 and sibling seats). No `git commit/add/push/stash/checkout/reset/pull`, no mutating
`jj`, no campaign tool run inside `shokuknow`.

---

## 9. Risks / blockers for the L1

1. **Blocker (F1):** with the frozen counter as written, `PREDICATE R52-C1 pass` is
   unreachable; the claims' kill rule then applies and C1 is not admitted, novelty stays at 8
   even if the whole capability lands. A minimal, append-only amendment (count the 184
   population paths; optionally verify all 184 digests) would restore the intent — the L1's
   decision, not mine; I did not touch the counter.
2. **F2/F3:** unless `SHA256SUMS` lands with plain population paths and the check is widened
   to all 184 files, the "byte-exact, digest-pinned" evidence is asserted but unverified.
3. **F5:** until `lane_read_tasks()` is fixed, leg 3's "never read by this lane before this
   round" condition is unenforced — the two real candidates are safe (neither is among the 12
   hand-read tasks), but a confirmation of an already-read task would still count as new.
4. **F6:** the triage queue is 2 candidates under the counter, 5 under the claims' literal
   rules. If wave 2's falsify seats are meant to attack the full queue, the extra three
   (`bn-fit-modify`, `distribution-search`, `portfolio-optimization`) should be in scope.
5. **F4:** the frozen control `c1-control-drop-capture` will not reproduce its claimed
   failure signature under this counter; the mutation-tester seat should report the actual
   signature instead of the expected one.

**Nothing else was left undone.** The counter was executed as frozen, in a scratch clone, with
the sibling's captures in place and independently re-verified; every leg's state is measured
above.
