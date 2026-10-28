# R50C1ExecMutAttrib — independent kill witness on a different fixture-set ordering

`REV 3b02d573d58cc6d2e0d27ef92ac0815354912252` (measured tree: `git clone --shared` of lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, checked out at the stage-1 freeze; lane tip at measurement
`5c56819f7964f4af19c960de08a49cd8f95781ce`, freeze verified an ancestor first:
`git merge-base --is-ancestor 3b02d57… HEAD` → exit 0). Every tool below ran in that clone, `TMPDIR` and all
`--work` roots inside `/fast/scratch/hyaku/kengaku-r50/R50C1ExecMutAttrib`, `PYTHONHASHSEED=0` exported.

Axes named: **novelty** (R50-C1, the seat's only axis). The mechanism this seat exercises is QUALITY Q38
("a frozen mutant's kill direction is witnessed, not assumed"): the witnessed object is the *attribution* of
each kill — which fixture flips, and to what — not whether the counter prints `caught`.

Item served: "for every row C1ExecMutRebase keeps OR authors, independently witness the kill on a different
fixture set ordering … write a per-row `STABLE <id> <fixture> <old->new>` table." Nothing else was measured
against the claim; no production file was touched, nothing was committed, and the lane checkout was never used
as a fixture root.

## 1. Targets, frozen by digest before any measurement

| object | sha256 | how frozen |
|---|---|---|
| **fence under test — shipped, declared final by `R50C1ExecRepair`, re-frozen by `R50C1ExecMutRebase`** | **`9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1`** | byte copy `fences/fence-repair-final.py`, `chmod 444` |
| **battery witnessed — the shipped, re-emitted 19 rows** | **`53873ed096e81355072f5577f74ebe543fa1165c1ecf27d470a286e65241eb6e`** | copy of `R50C1ExecMutRebase-c1-mutants.json`, matches the sha the rebase seat published |
| earlier declared fence, 19-row battery as first shipped | `ae47fc3e43aa9e98…` / `7287028164d043c9…` | witnessed in full before the re-freeze (§4) |
| later disk revision of the same repair | `6df6a2a331a66195…` | byte copy `fences/fence-disk.py`, witnessed (§4) |
| **fence now sitting uncommitted in the lane** (another seat's repair, not the one witnessed) | `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` | byte copy `fences/fence-tree.py` |
| **battery now sitting uncommitted in the lane** (22 rows, shares no id with the witnessed set; it moved to `e885f0a6…` after measurement) | `5f21b5879e1204f2d97eb4812c7f55c32c4d876740adac868fc03cb21eeb0cb3` | copy `mutants-tree.json` |
| base fence (control) | `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` | in the clone |
| carried r49 battery (control) | `plans/mutants50/c1-mutants.json`, 23 rows | in the clone |

The harness refuses to measure a fence whose sha256 differs from `--expect-fence-sha`, and re-hashes after the
sweep (`FENCE-MOVED` → exit 4). It fired for real once (§5).

## 2. Method — four configurations, not two

`attrib.py` (receipt `R50C1ExecMutAttrib-attrib.py`) imports the frozen counter `plans/round50_c1_verify.py` and
calls *its* `parse_population`, `build_all`, `verdicts`, `apply_mutant` and `module_path`; the only changes are
(a) the population rows are iterated in a caller-chosen order and (b) every per-fixture verdict change is
recorded instead of a single caught bit. `compare.py` (receipt `R50C1ExecMutAttrib-compare.py`) classifies each
row across runs as `STABLE`, `ORDER-DEPENDENT` (state or change-set differs between runs), `NOT-APPLICABLE`,
or `SURVIVED`.

Per row, four configurations — ordering and `--work` root are crossed so each is isolated (labels as in the
shipped run `G1–G4`; the earlier revision was witnessed with the same four on labels `F1–F4`, `§4`):

| config | order of the 126 population rows + hostile legs | work root |
|---|---|---|
| G1 | pinned (as in `plans/honest50/population.txt`) | `g-G1` |
| G2 | reversed | `g-G2` |
| G3 | `random.Random(0).shuffle` (breaks module grouping) | `g-G3` |
| G4 | pinned (same order as G1, different root) | `g-G4` |

Ordering is real, not nominal: the built fixture list differs (`fid_order[0:3]` = `a_class-x6-sibling-digest …`
pinned / `n09-ignored-untracked …` reversed / `a_err-f1-repaired-row-historical-erratum …` shuffled), and the
module built at index `m000` differs per configuration, so the same fid is built under a different absolute path
in each run (`R50C1ExecMutAttrib-ordering-proof.txt`), while the
*reference* verdict vector is order-invariant (`REF-ORDER-INVARIANT yes`, ref digest
`36c86d458372d67fe299cf8e25b8a4e19b82303d32012fd00d663cfd29f8f00f` identical in all four).

A row counts `STABLE` only if the set of `(fixture, old, new)` triples is *identical* across all four runs and
non-empty in each. Comparison keys exclude the human-readable reasons on purpose: reasons embed the absolute
work-root path (`../../../../b1/…`), so they differ across roots by construction and are not evidence.

## 3. Result — 19 of 19 rows STABLE, 0 dropped

`R50C1ExecMutAttrib-stability.txt` (runs `G1–G4`, fence `9baedf13`, battery `53873ed0`):
`ROWS total=19 stable=19 dropped=0 not-applicable=0 survived=0 stable-tuples=313`;
`semantic=313 error-vector=0` — every kill is a fence decision flip, none is an exception. The 313 `STABLE`
lines are byte-identical to the first-freeze run (`-stability-firstfreeze.txt`, fence `ae47fc3e`); only the two
header lines (run labels, fence digest) differ.

| row | tuples | kind |
|---|---|---|
| `c1-mut-gitfile-credit-revert` | 2 | targeted (n20, n21 honest credit) |
| `c1-mut-store-pointer-boundary-dead` | 1 | targeted |
| `c1-mut-alternates-boundary-dead` | 1 | targeted |
| `c1-mut-alternates-credit-revert` | 1 | targeted |
| `c1-mut-replace-namespace-dropped` | 1 | targeted (n17) |
| `c1-mut-config-leg-dead` | 24 | targeted-family (CR/BOM/includeIf worktree family) |
| `c1-mut-argv-order-shape-permuted` | 35 | diffuse (argv shape: every `order`-tool fixture) |
| `c1-mut-head-ref-raw-sha` | 2 | targeted |
| `c1-mut-hardlink-leg-dead` | 1 | targeted |
| `c1-mut-entry-cap-shrink` | 1 | targeted |
| `c1-mut-lane-membership-dead` | 1 | targeted |
| `c1-mut-inside-dead` | 2 | targeted |
| `c1-mut-gitfile-commondir-branch-dropped` | 1 | targeted |
| `c1-mut-objects-info-namespace-widen` | 1 | targeted |
| `c1-mut-config-bare-any-value` | 1 | targeted |
| `c1-mut-index-cap-shrink` | 116 | **diffuse** (honest leg, see note) |
| `c1-mut-anchor-opts-narrow` | 2 | targeted |
| `c1-mut-repo-cap-zero` | 116 | **diffuse** (honest leg, see note) |
| `c1-mut-store-dir-symlink-open` | 4 | targeted (store-entry symlink) |

**Note on the two diffuse rows.** They are stable and semantic, so they pass this item, but their kills are
whole-population: 116 honest fixtures flip `ADMIT->BREACH` (a cap/limit mutation makes the fence refuse nearly
everything). They carry almost no discrimination — the same `caught` bit would be earned by any mutant that
breaks admission. Flagged for the L1, not dropped here: dropping them is a kill-*quality* decision (rebase/L1),
not an ordering decision (this seat).

**Independent agreement.** The rebase seat's own table `R50C1ExecMutRebase-witness.tsv` names a killing fixture
and an `n_changed` for each row. Cross-checked mechanically against my four-config change sets: **19/19 agree**
(their named fixture is in my set and their `n_changed` equals my set size), with no disagreements. Two
independently built witnesses, same attribution.

## 4. Drift — three repair revisions, one verdict vector

The witness target moved three times while the wave ran, and each move was measured rather than assumed:

| revision | bytes | reference verdict vector on the frozen population | 19 rows |
|---|---|---|---|
| first declared final (`ae47fc3e`) | 33461 B | `36c86d458372d67f…` | 19 apply, 19 caught, **313 tuples** |
| disk revision minutes later (`6df6a2a3`) | 33461 B | `36c86d458372d67f…` | 19 apply, 19 caught, **identical 313 tuples** |
| shipped final (`9baedf13`, 838 lines) | — | `36c86d458372d67f…` | 19 apply, 19 caught, **identical 313 tuples** |

`drift.txt` (declared vs disk) reports `ROWS total=19 stable=19 dropped=0` with the two fence digests in its
`FENCES` line; the shipped pair was then witnessed again from scratch in four configurations (§3). All three
repair revisions make **identical decisions** on the frozen population (`REF-ORDER-INVARIANT yes`, one ref
digest), so the battery's kills are insensitive to which of the three lands. The rebase seat re-emitted its
payloads for `9baedf13` (battery sha `53873ed0…`); the payloads I measured after the re-freeze are those, and
they reproduce the same 313 triples as the `72870281…` payloads did against `ae47fc3e`.

### 4b. The bytes actually sitting in the lane are a different pair, and their mutant leg is unmet

While this report was being written, the lane working tree gained an uncommitted fence `57adce4a…` (533+/117−
against the frozen base, docstring naming a mount/device-boundary leg, detached-HEAD acceptance and
commit-graph/info-refs allowances — i.e. a different repair from the one witnessed) and a battery `5f21b587…`
of **22 rows whose ids share nothing** with the witnessed 19 (`c50-01…` … `c50-24…`). I measured that pair with
the same machinery, two orderings (`R50C1ExecMutAttrib-landed-pair.txt`):

```
ROWS total=22 stable=9 dropped=0 not-applicable=0 survived=13 stable-tuples=15
REF-ORDER-INVARIANT yes   (ref digest 8cf173e9…, different decisions from the witnessed fence)
```

All 22 payloads apply; **13 change no verdict at all** (`c50-10` … `c50-24`, among them
`c50-15-any-ref-namespace`, `c50-21-ref-value-any`, `c50-13-no-symlink-leg`, `c50-14-no-hardlink-leg`). The
counter's own leg on the same bytes agrees exactly:

```
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=22 caught=9 broken=0 floor=12 verdict=unmet
PREDICATE R50-C1 fail
```

with the same 13 `MUTANT survived` ids my sweep reports — so on that pair the *only* failing leg is the mutant
floor: the fence repairs every honest fixture (admitted=126) and refuses every hostile module, and its battery
still cannot demonstrate the floor. This is not my item's row set and I make no claim about the fence, but it
decides whether R50-C1 can pass, so the L1 needs it: the battery that lands must be the battery that was
witnessed, or it must be re-witnessed. Note the two rows that survive there cover exactly the "any ref namespace
/ any ref value" surface that `R50C1ExecRepair` flagged by message as a regression class its own rework had
produced once — consistent with a repair revision that no longer consults `refs/` for the replace namespace.
(The lane's battery moved once more, to `e885f0a6…`, after this measurement; the fence `57adce4a…` was unchanged
at the time of writing. My figures are for the exact digests in §1.)

## 5. Defects routed (all measured here, none of them a claim admission)

**D1 — `apply_mutant` accepts a *reversed* patch and the counter counts the result as a caught mutant.**
`plans/round50_c1_verify.py:apply_mutant` runs `patch --batch --silent -p1` and only checks `returncode`. Given
carried row `c1-mut-03-drop-file-mountbound`, which *deletes* a `st.st_dev != ddev` leg that the base fence does
not contain, patch says:

```
Reversed (or previously applied) patch detected!  Assuming -R.
Hunk #1 succeeded at 215 with fuzz 2 (offset -50 lines).
```

exit 0 — so the row is treated as a valid mutant; the "deleted" lines are **inserted**, `st` is not bound at that
point, and the mutant raises `NameError: name 'st' is not defined` on the fixture where the reference admits.
Result: 164 per-fixture verdicts flip `ADMIT->ERROR`, stable in every ordering — a monotone fake kill. Receipt
`R50C1ExecMutAttrib-patch-fuzz-artifact.txt`. This affects any row whose subject has been removed from the fence
it is applied to, i.e. exactly the rebase situation. (The rebase battery contains no such row: `broken=0`,
`error-vector=0` — the defect is in the carried set and in the counter's apply path.)

**D2 — the counter's caught bit cannot tell a decision flip from a crash.** `verdicts()` maps an exception to
`ERROR` and the mutant leg compares the whole vector, so `ERROR` ≠ reference counts as caught. A fence that
raises on the population would score `caught=19` with zero refusals. Q38 asks for a *witnessed direction*; the
witness has to say `ADMIT->BREACH` / `BREACH->ADMIT`, not `*->ERROR`. My receipt reports the split
(`semantic=` / `error-vector=`) so a reviewer can see it.

**D3 — the witness target moved under the wave, and the top-level counter still reads the carried battery.**
Sampling `fence_candidate.py`: `1e1aff9d` (14:24) → `b839244c` (14:26) → **`05d5fe03` = the base fence byte for
byte** (14:26, the state my first candidate run read) → `dba7aee8` → `7a5d9af2` (14:27) → `0117b4b6` → `ae47fc3e`
(14:30, declared) → `6df6a2a3` (14:31). One four-config sweep was aborted by my guard: `FENCE-MOVED 0117b4b6… ->
ae47fc3e…`. A seat that measured during the base-byte window would have certified the *unrepaired* fence as the
repair. Separately, `python3 plans/round50_c1_verify.py --lane .` at the freeze tree still reads
`plans/mutants50/c1-mutants.json` (the carried 23), so it prints `MUTANTS total=23 caught=1 broken=15` against
the repaired fence — the re-derived battery only reaches the counter after S2 lands it at that path.

## 6. Cross-check on the predicate (facts only, not this seat's verdict)

Running the counter with the final battery substituted (scratch copy of the clone, `--allow-dirty`, two work
roots, `R50C1ExecMutAttrib-counter-battery.txt`), identical both times:

```
HONEST fixtures=126 admitted=117 refused=9 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=19 caught=19 broken=0 floor=12 verdict=met
PREDICATE R50-C1 fail
```

The mutant floor is met exactly as this seat witnesses it. The honest leg is not: the witnessed fence admits
117 of 126 (measured on `ae47fc3e`; the reference vector is identical on `6df6a2a3` and `9baedf13`, so the number
carries over byte for byte). Of the five classes C1 names, four are repaired (`n17-replace-ref`,
`n20-linked-worktree`, `n21-separate-gitdir`, `n22-alternates-in-d` flip `BREACH->ADMIT` against the base fence)
and `n18-shallow-fetch` is still refused, now on `repo/.git/config section header b'[remote "origin"]' is not
plain`. Remaining refusals: `n12`, `n13`, `n14`, `n15`, `n16`, `n18`, `n03`, `n07`, `n08`. This is reported for
the L1 to route; the *mutant* leg does not constrain which repair revision lands (the kills are identical on all
three), the *honest* leg does — and the pair actually sitting in the lane (§4b) is neither of them.

## 7. Control on the base fence (pre-validation of the same machinery)

Carried 23 rows against base `05d5fe03`: `stable=3 dropped=0 not-applicable=12 survived=8`, ref order-invariant
across the same four configurations. The three stable ones are `c1-mut-13-entry-cap-shrink` (2 tuples,
`ADMIT->BREACH`), `c1-mut-19-lane-membership` (1 tuple, `f6-repo-above-d BREACH->ADMIT`) and
`c1-mut-03-drop-file-mountbound` (164 tuples, all `ADMIT->ERROR` — D1). The counter's own leg agrees exactly:
`MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet`, identical at two work roots
(`R50C1ExecMutAttrib-counter-two-root.txt`). **The brief's "4 of 23 change the verdict vector on the base fence"
was not reproduced: I measure 3, of which 1 is the D1 artifact, leaving 2 semantic kills.** The exact command is
in the receipt; the size of the difference (one row) is small enough to be a different apply mode or a different
population snapshot upstream, but with the frozen artifacts here it is 3.

Detector self-test: a doctored copy of the F4 measurement (one row's change set truncated, one row's emptied)
is flagged `ORDER-DEPENDENT` + `DROP` by `compare.py`, so the drop path is live rather than decorative.

## 8. Complete per-row kill table (four configurations, identical)

Format: `STABLE <id> <fixture> <old->new>`. Produced by `compare.py` over G1–G4 on the shipped pair; verbatim,
313 lines.

RUNS pinned-wG1 reverse-wG2 shuffle0-wG3 pinned-wG4
FENCES 9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1
REFDIGESTS 36c86d458372d67fe299cf8e25b8a4e19b82303d32012fd00d663cfd29f8f00f
REF-ORDER-INVARIANT yes
ROWS total=19 stable=19 dropped=0 not-applicable=0 survived=0 stable-tuples=313

STABLE c1-mut-gitfile-credit-revert tuples=2 semantic=2 error-vector=0
STABLE c1-mut-gitfile-credit-revert n20-linked-worktree ADMIT->BREACH
STABLE c1-mut-gitfile-credit-revert n21-separate-gitdir ADMIT->BREACH
STABLE c1-mut-store-pointer-boundary-dead tuples=1 semantic=1 error-vector=0
STABLE c1-mut-store-pointer-boundary-dead f1-gitdir-outside BREACH->ADMIT
STABLE c1-mut-alternates-boundary-dead tuples=1 semantic=1 error-vector=0
STABLE c1-mut-alternates-boundary-dead f5-alternates-outside BREACH->ADMIT
STABLE c1-mut-alternates-credit-revert tuples=1 semantic=1 error-vector=0
STABLE c1-mut-alternates-credit-revert n22-alternates-in-d ADMIT->BREACH
STABLE c1-mut-replace-namespace-dropped tuples=1 semantic=1 error-vector=0
STABLE c1-mut-replace-namespace-dropped n17-replace-ref ADMIT->BREACH
STABLE c1-mut-config-leg-dead tuples=24 semantic=24 error-vector=0
STABLE c1-mut-config-leg-dead config-core-attributes-file-outside BREACH->ADMIT
STABLE c1-mut-config-leg-dead f10-lane-include-regular BREACH->ADMIT
STABLE c1-mut-config-leg-dead f2-deep-worktree BREACH->ADMIT
STABLE c1-mut-config-leg-dead f4-fifo-include BREACH->ADMIT
STABLE c1-mut-config-leg-dead f9-bare-repo BREACH->ADMIT
STABLE c1-mut-config-leg-dead h1-cr-include-crlf BREACH->ADMIT
STABLE c1-mut-config-leg-dead h1-cr-include-lf BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-gitdir-exact BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-gitdir-glob BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-gitdir-i BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-gitdir-nomatch BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-gitdir-star BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-hasconfig BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-onbranch BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-onbranch-anchor BREACH->ADMIT
STABLE c1-mut-config-leg-dead h2-inclif-onbranch-nomatch BREACH->ADMIT
STABLE c1-mut-config-leg-dead h3-bom-include BREACH->ADMIT
STABLE c1-mut-config-leg-dead h3-bom-includeif BREACH->ADMIT
STABLE c1-mut-config-leg-dead h3-cr-include-anchor BREACH->ADMIT
STABLE c1-mut-config-leg-dead n12-local-config-user BREACH->ADMIT
STABLE c1-mut-config-leg-dead n13-remote-origin BREACH->ADMIT
STABLE c1-mut-config-leg-dead sealed-core-attributes-path BREACH->ADMIT
STABLE c1-mut-config-leg-dead sealed-core-excludes-file BREACH->ADMIT
STABLE c1-mut-config-leg-dead sealed-url-insteadof-path BREACH->ADMIT
STABLE c1-mut-argv-order-shape-permuted tuples=35 semantic=35 error-vector=0
STABLE c1-mut-argv-order-shape-permuted n11-multibranch ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-bare-ok-late ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-fenced-echo ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-inplace-gate-rewrite ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-late-case-blob ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-prefixed-ok-blob ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_alt-two-echo-blobs ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_clause-clean-order ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_clause-freeze-pair-edited-after ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_clause-freeze-single ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_clause-receipt-side-line ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_clause-receipt-withdrawn ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_excuse-bare-excused ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_excuse-echo-freeze-claims ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_excuse-gate-prefix-late ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n22a-gate-only ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n22b-echoed-defect ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n22c-indented-gate ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n5a-late-gate-file ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n5b-amended-claims ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-n5c-case-third-commit ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo5-amended-claims-blob ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo5-post-receipt-verdicts ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo6-echoed-pass-row ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo6-pass-verdict-row ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo7-skipped-row-r38 ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted o_scan-xo7-timeout-rows ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_a-canonical-control ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_a-draft-suffix ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_a-subdir-nohyphen ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_a-uppercase-pair ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_b-nested-uppercase ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_b-registry-suffix ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_b-round-xx-token ADMIT->BREACH
STABLE c1-mut-argv-order-shape-permuted u14c_name_b-underscore-name ADMIT->BREACH
STABLE c1-mut-head-ref-raw-sha tuples=2 semantic=2 error-vector=0
STABLE c1-mut-head-ref-raw-sha n03-detached-head BREACH->ADMIT
STABLE c1-mut-head-ref-raw-sha n08-tag-detached BREACH->ADMIT
STABLE c1-mut-hardlink-leg-dead tuples=1 semantic=1 error-vector=0
STABLE c1-mut-hardlink-leg-dead link-objects-hardlink-out BREACH->ADMIT
STABLE c1-mut-entry-cap-shrink tuples=1 semantic=1 error-vector=0
STABLE c1-mut-entry-cap-shrink n21-separate-gitdir ADMIT->BREACH
STABLE c1-mut-lane-membership-dead tuples=1 semantic=1 error-vector=0
STABLE c1-mut-lane-membership-dead f6-repo-above-d BREACH->ADMIT
STABLE c1-mut-inside-dead tuples=2 semantic=2 error-vector=0
STABLE c1-mut-inside-dead f1-gitdir-outside BREACH->ADMIT
STABLE c1-mut-inside-dead f5-alternates-outside BREACH->ADMIT
STABLE c1-mut-gitfile-commondir-branch-dropped tuples=1 semantic=1 error-vector=0
STABLE c1-mut-gitfile-commondir-branch-dropped n20-linked-worktree ADMIT->BREACH
STABLE c1-mut-objects-info-namespace-widen tuples=1 semantic=1 error-vector=0
STABLE c1-mut-objects-info-namespace-widen n15-commit-graph BREACH->ADMIT
STABLE c1-mut-config-bare-any-value tuples=1 semantic=1 error-vector=0
STABLE c1-mut-config-bare-any-value f9-bare-repo BREACH->ADMIT
STABLE c1-mut-index-cap-shrink tuples=116 semantic=116 error-vector=0
STABLE c1-mut-index-cap-shrink a_alt-erratum-lessons ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-erratum-manifest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-erratum-short ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-erratum-sibling ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-erratum-two ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-erratum-upper ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-longrow-copied ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-longrow-late ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-longrow-multicap ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-shorturl-samedir ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-shorturl-sibling ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-slug-blob ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-slug-deepest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_alt-slug-manifest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x14-two-errata ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x14-uppercase-token ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x6-sibling-digest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x6-stale-manifest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x7-fabricated-token ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_class-x7-provenance-row ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f1-repaired-row-historical-erratum ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f2-two-rows-provenance-two-errata ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f3-stale-token-sibling-capture ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f4-manifest-only-second-capture ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f5-row-carrying-both-tokens ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_err-f6-provenance-bound-unknown-stale ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x1-provenance-table ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x1-two-row-registry ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x12-slashless-toml ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x12-two-tomls ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x3-blob-url ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_route-x3-provenance-url ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-na1-mid13 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-na1-tail12 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-na1-wide20 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x13-staged-capture ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x13-url-staged ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x15-manifest-sibling ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x15-sibling-digest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x9-registry-short-valid ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_row-x9-short-no-token ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_url-org-slash-registry ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_url-org-slash-single ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_url-short-commit-pair ADMIT->BREACH
STABLE c1-mut-index-cap-shrink a_url-short-commit-shadow ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n01-packed-refs ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n02-annotated-tag ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n04-merge-commit ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n05-gitignore ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n06-linear-30 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n09-ignored-untracked ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n11-multibranch ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n17-replace-ref ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n19-template-less-init ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n20-linked-worktree ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n21-separate-gitdir ADMIT->BREACH
STABLE c1-mut-index-cap-shrink n22-alternates-in-d ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-bare-ok-late ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-fenced-echo ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-inplace-gate-rewrite ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-late-case-blob ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-prefixed-ok-blob ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_alt-two-echo-blobs ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_clause-clean-order ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_clause-freeze-pair-edited-after ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_clause-freeze-single ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_clause-receipt-side-line ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_clause-receipt-withdrawn ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_excuse-bare-excused ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_excuse-echo-freeze-claims ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_excuse-gate-prefix-late ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n22a-gate-only ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n22b-echoed-defect ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n22c-indented-gate ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n5a-late-gate-file ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n5b-amended-claims ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-n5c-case-third-commit ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo5-amended-claims-blob ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo5-post-receipt-verdicts ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo6-echoed-pass-row ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo6-pass-verdict-row ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo7-skipped-row-r38 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink o_scan-xo7-timeout-rows ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_a-canonical-control ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_a-draft-suffix ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_a-subdir-nohyphen ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_a-uppercase-pair ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_b-nested-uppercase ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_b-registry-suffix ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_b-round-xx-token ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u14c_name_b-underscore-name ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_a-abbrev-neighbour ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_a-index-staged ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_a-manifest-registry ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_b-history-truncation ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_b-index-ref-staged ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_b-lane-path-manifest ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u5_short_b-registry-url-task ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_a-history-200 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_a-manifest-96 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_a-provenance-128 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_a-registry-65 ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_b-index-pair-96hex ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_b-provenance-129hex ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u6_long_b-registry-80hex ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_a-provenance-table ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_a-rowpath-registry ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_a-url-two-tasks ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_b-mixed-trio ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_b-prov-twin ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u7_twin_b-url-trio-identical ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u9_worktree_a-history-abbrev ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u9_worktree_a-registry-wrong-capture ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u9_worktree_b-erratum-completed-in-place ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u9_worktree_b-erratum-retargeted-history ADMIT->BREACH
STABLE c1-mut-index-cap-shrink u9_worktree_b-registry-erratum-appended ADMIT->BREACH
STABLE c1-mut-anchor-opts-narrow tuples=2 semantic=2 error-vector=0
STABLE c1-mut-anchor-opts-narrow u5_short_a-abbrev-neighbour ADMIT->BREACH
STABLE c1-mut-anchor-opts-narrow u5_short_b-lane-path-manifest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero tuples=116 semantic=116 error-vector=0
STABLE c1-mut-repo-cap-zero a_alt-erratum-lessons ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-erratum-manifest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-erratum-short ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-erratum-sibling ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-erratum-two ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-erratum-upper ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-longrow-copied ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-longrow-late ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-longrow-multicap ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-shorturl-samedir ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-shorturl-sibling ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-slug-blob ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-slug-deepest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_alt-slug-manifest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x14-two-errata ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x14-uppercase-token ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x6-sibling-digest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x6-stale-manifest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x7-fabricated-token ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_class-x7-provenance-row ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f1-repaired-row-historical-erratum ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f2-two-rows-provenance-two-errata ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f3-stale-token-sibling-capture ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f4-manifest-only-second-capture ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f5-row-carrying-both-tokens ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_err-f6-provenance-bound-unknown-stale ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x1-provenance-table ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x1-two-row-registry ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x12-slashless-toml ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x12-two-tomls ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x3-blob-url ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_route-x3-provenance-url ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-na1-mid13 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-na1-tail12 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-na1-wide20 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x13-staged-capture ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x13-url-staged ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x15-manifest-sibling ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x15-sibling-digest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x9-registry-short-valid ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_row-x9-short-no-token ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_url-org-slash-registry ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_url-org-slash-single ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_url-short-commit-pair ADMIT->BREACH
STABLE c1-mut-repo-cap-zero a_url-short-commit-shadow ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n01-packed-refs ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n02-annotated-tag ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n04-merge-commit ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n05-gitignore ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n06-linear-30 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n09-ignored-untracked ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n10-empty-repo ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n11-multibranch ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n17-replace-ref ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n19-template-less-init ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n20-linked-worktree ADMIT->BREACH
STABLE c1-mut-repo-cap-zero n22-alternates-in-d ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-bare-ok-late ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-fenced-echo ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-inplace-gate-rewrite ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-late-case-blob ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-prefixed-ok-blob ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_alt-two-echo-blobs ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_clause-clean-order ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_clause-freeze-pair-edited-after ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_clause-freeze-single ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_clause-receipt-side-line ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_clause-receipt-withdrawn ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_excuse-bare-excused ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_excuse-echo-freeze-claims ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_excuse-gate-prefix-late ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n22a-gate-only ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n22b-echoed-defect ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n22c-indented-gate ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n5a-late-gate-file ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n5b-amended-claims ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-n5c-case-third-commit ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo5-amended-claims-blob ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo5-post-receipt-verdicts ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo6-echoed-pass-row ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo6-pass-verdict-row ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo7-skipped-row-r38 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero o_scan-xo7-timeout-rows ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_a-canonical-control ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_a-draft-suffix ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_a-subdir-nohyphen ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_a-uppercase-pair ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_b-nested-uppercase ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_b-registry-suffix ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_b-round-xx-token ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u14c_name_b-underscore-name ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_a-abbrev-neighbour ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_a-index-staged ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_a-manifest-registry ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_b-history-truncation ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_b-index-ref-staged ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_b-lane-path-manifest ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u5_short_b-registry-url-task ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_a-history-200 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_a-manifest-96 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_a-provenance-128 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_a-registry-65 ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_b-index-pair-96hex ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_b-provenance-129hex ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u6_long_b-registry-80hex ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_a-provenance-table ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_a-rowpath-registry ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_a-url-two-tasks ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_b-mixed-trio ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_b-prov-twin ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u7_twin_b-url-trio-identical ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u9_worktree_a-history-abbrev ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u9_worktree_a-registry-wrong-capture ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u9_worktree_b-erratum-completed-in-place ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u9_worktree_b-erratum-retargeted-history ADMIT->BREACH
STABLE c1-mut-repo-cap-zero u9_worktree_b-registry-erratum-appended ADMIT->BREACH
STABLE c1-mut-store-dir-symlink-open tuples=4 semantic=4 error-vector=0
STABLE c1-mut-store-dir-symlink-open link-objects-symlink-out BREACH->ADMIT
STABLE c1-mut-store-dir-symlink-open seal-objects-link BREACH->ADMIT
STABLE c1-mut-store-dir-symlink-open seal-refs-link BREACH->ADMIT
STABLE c1-mut-store-dir-symlink-open sealed-refs-redirect BREACH->ADMIT

## 9. Limits

- The witness is about *attribution and reproducibility*, not about whether the fence's decisions are right.
  A stable kill says the mutation is observable on this population — not that the leg it deletes was necessary.
- Ordering axes used: pinned / reversed / `random.Random(0)`-shuffled, plus a repeated order under a different
  work root. An adversarial ordering (e.g. one that binds fixture identity to a hash seed inside the fence) is
  not enumerated; `PYTHONHASHSEED=0` is fixed as the item requires, so a kill that depends on *another* hash seed
  would not be seen here. The counter sets no such dependency that I could observe.
- Fixture builds, the builder (`plans/honest50/build_honest_population.py`) and the population pin
  `b5197f94…` are the frozen ones at `3b02d57`; `POPULATION … mismatched=0 build_errors=0` in every run.
- `plans/sealed50/` does not exist at `3b02d57`, so the sealed leg is the 12 frozen `plans/sealed46/` modules.
  The blind modules are another seat's deliverable and are not witnessed here.
- Machine load differs between the four configurations (fixtures are built four times); builds are per-fixture
  `git init`/commit only, and identity pins matched in all four, so build order is not a hidden variable — it is
  the variable under test.
- I did not re-derive, drop or author any row; the 19 rows are exactly the rebase seat's delivered set.

## 10. Reproducing

```
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecMutAttrib   # or any scratch root
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane checkout 3b02d57d58cc6d2e0d27ef92ac0815354912252
export TMPDIR=$S PYTHONHASHSEED=0
# fence copies (immutable): fences/fence-final.py ae47fc3e…, fences/fence-disk.py 6df6a2a3…
python3 plans/round50_c1_verify.py --lane . --work $S/w --fence $S/fences/fence-repair-final.py   # counter view
python3 R50C1ExecMutAttrib-attrib.py  --lane . --fence $S/fences/fence-repair-final.py \
        --mutants R50C1ExecMutRebase-c1-mutants.json --work $S/g-G1 --order pinned \
        --expect-fence-sha 9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1 --out $S/G1.json
python3 R50C1ExecMutAttrib-compare.py $S/G1.json $S/G2.json $S/G3.json $S/G4.json --out $S/stability.txt
```

## 11. Verdict

`VERDICT: PASS (item) — 19/19 kept-or-authored rows witnessed STABLE on the shipped pair (fence 9baedf13,
battery 53873ed0): 313 tuples, all semantic, 0 error-vector, 0 order-dependent, 0 dropped, identical under
pinned / reversed / shuffled population order and four distinct --work roots with PYTHONHASHSEED=0, identical
again on the two earlier repair revisions (ae47fc3e, 6df6a2a3), and the 313 tuple lines are byte-identical across
revisions; attribution agrees with the rebase seat's independent table 19/19.`

Routed, not judged here: **D1** `apply_mutant` accepts a reversed patch (fake `*->ERROR` kill — the base-fence
`c1-mut-03` "kill" is entirely this artifact); **D2** `ERROR` counts as a caught mutant in the counter's verdict
comparison; **D3** the witness target moved four times during the wave (one sample was the base fence byte for
byte) and the top-level counter still reads the carried battery; **D4 (§4b)** the battery now sitting uncommitted
in the lane is a different 22-row set against a different fence, and 13 of its rows change no verdict —
`caught=9 < floor=12`, mutant leg unmet. Cross-check for the L1: the witnessed fence
admits 117/126 honest fixtures (`n18-shallow-fetch` still refused), so `MUTANTS met` and `PREDICATE pass` do not
coincide at `ae47fc3e`.

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ExecMutAttrib` was removed before yield; no defect there.
Receipts (this directory): `R50C1ExecMutAttrib-stability.txt` (shipped pair, 313 `STABLE` lines),
`-stability-firstfreeze.txt` (same table on `ae47fc3e`), `-drift.txt`, `-landed-pair.txt` (§4b),
`-base-stability.txt` (control), `-counter-two-root.txt`, `-counter-battery.txt`,
`-patch-fuzz-artifact.txt` (D1), `-selftest.txt` (detector sensitivity), `-ordering-proof.txt`,
`-attrib.py`, `-compare.py`.
