# R50C1ExecMutRebase — mutant battery re-derived against the repaired fence (R50-C1, novelty)

Seat: `R50C1ExecMutRebase` (executor, leaf). Item: re-derive the 23 carried mutant rows against
`C1ExecRepair/fence_candidate.py`, drop and report every row that cannot apply or is not caught, author fresh rows
over the candidate's own bytes until ≥16 are witnessed-caught covering the five repaired classes plus
config/argv/symlink/hardlink/mount, and emit a complete replacement `c1-mutants.json` plus a witness table.

**Axes named.** novelty only (R50-C1's `MUTANTS` leg). I do not touch calibration (R50-C2) and I claim no
admission: this seat produces the battery, the L1 owns integration and the scored run.

## REV and surfaces measured

```
REV  lane tip                     5c56819f7964f4af19c960de08a49cd8f95781ce
REV  freeze (stage 1)             3b02d573d58cc6d2e0d27ef92ac0815354912252   (verified ancestor of tip:
                                  git merge-base --is-ancestor 3b02d57… HEAD -> 0)
REV  measured tree                git clone --shared of the lane, checked out at 3b02d57…,
                                  toplevel /fast/scratch/hyaku/kengaku-r50/R50C1ExecMutRebase/lane
FENCE under test                  .ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py
                                  sha256 9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1 (838 lines)
BATTERY carried                   plans/mutants50/c1-mutants.json @ 3b02d57
                                  sha256 2e5cfe6622c5d1497570724939b1346f15d80ed4b978e5fcaee925bb8b5ff865 (23 rows)
POPULATION                        plans/honest50/population.txt pin b5197f94…fae69, 126 rows, mismatched=0
REFERENCE vector fixtures built   175 = 126 honest + 34 plans/refusals46 + 15 plans/sealed46
                                  (plans/sealed50 does not exist at 3b02d57, so the SEALED50 leg is not in the vector)
```

**The candidate moved seven times while this seat ran** — `b839244c…` → `91a3149b…` → `2c4e40a0…` → `cde55d13…`
→ `d59031f1…` → `ae47fc3e…` → `6df6a2a3…` → **`9baedf13…`** (the last two announced by `R50C1ExecRepair`, the last one
because a peer's 14-case table showed the `gitdir:` parse trimmed whitespace git keeps). I re-authored, re-witnessed
and re-emitted at `ae47fc3e…` and again at `9baedf13…`; **everything below is measured on `9baedf13…`**, and the
earlier digests appear only where a measurement on them *is* the finding. A frozen battery is only as good as the
bytes it was frozen to, so this report names the sha in every receipt.

## Method (exact commands)

Built once, scored many: `author_and_witness.py`, `apply_shipped.py` and `shadow.py` (all shipped as receipts) import
the counter's *own* `parse_population`, `build_all`, `verdicts`, `apply_mutant` from `plans/round50_c1_verify.py`,
build the 175 fixtures once, take the reference vector from the fence under test, then score every row against it.
A row is **CAUGHT** iff `[(fid, verdict)]` differs from the reference anywhere — the counter's own predicate, one
row at a time, without re-running the counter per row. `apply_shipped.py` scores the *emitted* payloads (not the
generator's memory); `shadow.py` additionally counts refusal-**reason** changes, which is how a shadowed row is told
apart from an unreachable one.

```
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecMutRebase        # TMPDIR=$S, trap rm -rf
git clone --shared --no-checkout <lane> "$S/lane"; git -C "$S/lane" checkout -q 3b02d57…
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/…/lane ; status --porcelain -> 0

F=$S/fence_new.py          # sha256 9baedf13…, the frozen candidate

# 1. all 23 carried rows (+ per-row reason changes) on the frozen candidate
git -C lane show 3b02d57…:plans/mutants50/c1-mutants.json > "$S/carried23.json"
python3 shadow.py --lane "$S/lane" --fence "$F" --battery "$S/carried23.json" --work "$S"

# 2. fresh rows: exact-once substring transforms -> unified diff -> witness (35 transforms authored)
python3 author_and_witness.py --lane "$S/lane" --fence "$F" \
        --transforms "$S/transforms.py" --out "$S/auth-new.json" --work "$S"

# 3. the EMITTED battery, scored by an applier that never saw the generator
python3 apply_shipped.py --lane "$S/lane" --fence "$F" \
        --battery R50C1ExecMutRebase-c1-mutants.json --work "$S"     # -> caught=19 survived=0 not_applicable=0

# 4. end-to-end through the counter's own MUTANTS leg, with the replacement battery in the clone
cp R50C1ExecMutRebase-c1-mutants.json "$S/lane/plans/mutants50/c1-mutants.json"
cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --fence "$F" \
        --allow-dirty --work "$S/w1"        # and again with PYTHONHASHSEED=0, --work "$S/w2"

# 5. payload integrity: recompute sha256(payload) == payload_sha256 and sha256(patched fence) == digest
# 6. portability: the same emitted battery against the lane's working-copy fence 57adce4a… (read-only snapshot)
```

`carried23.json` is `git -C lane show 3b02d57…:plans/mutants50/c1-mutants.json` — extracted read-only, never by a
checkout in the clone, and the clone was never mutated except for step 3's battery swap (disclosed under Limits).

## Result 1 — the 23 carried rows on the final candidate: 1 caught, 7 survived, 15 cannot apply

Verbatim receipt (`R50C1ExecMutRebase-carried23-shadow.txt`), reference vector `{'ADMIT': 117, 'BREACH': 58}`:

```
ROW c1-mut-01-gitdir-file NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-02-symlink-dir-dead NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-03-drop-file-mountbound NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-04-hardlink-threshold NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-05-git-top-commondir NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-06-objinfo-fallthrough NOT-APPLICABLE patch-rc=1  out of 1 hunk FAILED
ROW c1-mut-07-config-cr SURVIVED
ROW c1-mut-08-config-unknown-key NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-09-url-insteadof NOT-APPLICABLE patch-rc=1 2 out of 2 hunks FAILED
ROW c1-mut-10-inside-prefix SURVIVED
ROW c1-mut-11-head-ref-widen NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-12-store-required SURVIVED
ROW c1-mut-13-entry-cap-shrink CAUGHT n=3 first=u14c_name_a-draft-suffix ADMIT->BREACH
ROW c1-mut-14-argv-placeholder SURVIVED
ROW c1-mut-15-hook-suffix NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-16-argv-shape-tail SURVIVED
ROW c1-mut-17-config-value-backslash NOT-APPLICABLE patch-rc=1 t of 1 hunk FAILED
ROW c1-mut-18-graph-magic-empty NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-19-lane-membership NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-20-packedref-peel SURVIVED
ROW c1-mut-21-log-namespace NOT-APPLICABLE patch-rc=1 1 out of 1 hunk FAILED
ROW c1-mut-22-fixture-symlink SURVIVED
ROW c1-mut-23-gitdir-repo-reorder NOT-APPLICABLE patch-rc=1  out of 1 hunk FAILED
SUMMARY total=23 caught=1 survived=7 not_applicable=15
```

**Every one of the other 22 is dropped**, each with its measured reason in
`R50C1ExecMutRebase-dropped-carried.tsv`:

* **15 not-applicable** — the payloads were authored against the r49 candidate fence and name lines that do not
  exist in these bytes (`ddev`, the `GIT_TOP` commondir entry, the `objects/info` fallthrough, the `_reject`
  reorder, …). `patch` exits 1 with the whole hunk failed; no partial application (the counter's `apply_mutant`
  refuses a non-zero rc, so a failed row can never be silently counted as "broken = survived").
* **7 survived** (payload applies, verdict vector unchanged). I measured *why* rather than assuming, by
  comparing refusal **reasons** as well as verdicts (columns `reason_changes` / `example_reason_after_mutation` in
  `R50C1ExecMutRebase-carried23-shadow.txt`):

| row | reason_changes | why it cannot kill on these bytes |
|---|---|---|
| `c1-mut-07-config-cr` | 13 | the 13 CR-carrying hostile fixtures keep being refused, now as `config line b'\r[include]' is not a plain key=value` — the CR leg is shadowed by the line parser |
| `c1-mut-10-inside-prefix` | 0 | `_inside` is re-applied downstream by the lane-membership proof; the mutated prefix test is not the only guard |
| `c1-mut-12-store-required` | 0 | no fixture reaches a store missing the required entries after the earlier legs |
| `c1-mut-14-argv-placeholder` | 0 | no frozen fixture carries a `{` placeholder argv |
| `c1-mut-16-argv-shape-tail` | 0 | a broken shape falls through to `argv names no lane to prove` |
| `c1-mut-20-packedref-peel` | 0 | no fixture carries a bad peeled line |
| `c1-mut-22-fixture-symlink` | 0 | no built fixture has `d` as a symlink (the builder always makes a real dir) |

So the carried battery is not a battery for this fence: 96 % of it is context-dead or shadowed. That is the Q38
finding the item asked for, measured.

## Result 2 — 35 fresh rows authored on the candidate's own bytes, 19 witnessed-caught, 16 dropped and reported

Rows are authored as exact-once substring transforms of the candidate source (`transforms.py`, shipped as a
receipt), each turned into a `diff -u` payload with `a/plans/fixture_fence.py` labels, then applied *through the
counter's* `apply_mutant` and scored. A transform whose `find` is absent (n≠1) is reported, never silently
skipped.

Witness table (`R50C1ExecMutRebase-witness.tsv`), 19 kept rows — every one a real verdict flip:

| row | class | killing fixture | Old → New |
|---|---|---|---|
| `c1-mut-gitfile-credit-revert` | gitfile (n20/n21 honest credit) | `n20-linked-worktree` (n=2, also n21) | ADMIT → BREACH (`wt/.git is a file (gitdir redirect)`) |
| `c1-mut-store-pointer-boundary-dead` | gitfile/worktree pointer boundary | `f1-gitdir-outside` | BREACH → ADMIT |
| `c1-mut-alternates-boundary-dead` | alternates (n22) boundary | `f5-alternates-outside` | BREACH → ADMIT |
| `c1-mut-alternates-credit-revert` | alternates (n22 honest credit) | `n22-alternates-in-d` | ADMIT → BREACH |
| `c1-mut-replace-namespace-dropped` | refs/replace (n17 honest credit) | `n17-replace-ref` | ADMIT → BREACH |
| `c1-mut-config-leg-dead` | config | `n12-local-config-user` (n=24) | BREACH → ADMIT |
| `c1-mut-argv-order-shape-permuted` | argv shape | `o_clause-freeze-single` (n=35) | ADMIT → BREACH |
| `c1-mut-head-ref-raw-sha` | HEAD shape | `n03-detached-head` (n=2) | BREACH → ADMIT |
| `c1-mut-hardlink-leg-dead` | hardlink | `link-objects-hardlink-out` | BREACH → ADMIT |
| `c1-mut-entry-cap-shrink` | tree cap | `n21-separate-gitdir` | ADMIT → BREACH (`fixture tree exceeds 40 entries`) |
| `c1-mut-lane-membership-dead` | argv lane membership | `f6-repo-above-d` | BREACH → ADMIT |
| `c1-mut-inside-dead` | boundary property (global) | `f1-gitdir-outside` (n=2) | BREACH → ADMIT |
| `c1-mut-gitfile-commondir-branch-dropped` | gitfile (n20 worktree shape) | `n20-linked-worktree` | ADMIT → BREACH |
| `c1-mut-objects-info-namespace-widen` | store info namespace (objects) | `n15-commit-graph` | BREACH → ADMIT |
| `c1-mut-config-bare-any-value` | config value | `f9-bare-repo` | BREACH → ADMIT |
| `c1-mut-index-cap-shrink` | cap (index) | `a_class-x6-sibling-digest` (n=116) | ADMIT → BREACH |
| `c1-mut-anchor-opts-narrow` | argv options | `u5_short_a-abbrev-neighbour` (n=2) | ADMIT → BREACH |
| `c1-mut-repo-cap-zero` | cap (repos) | `a_class-x6-sibling-digest` (n=116) | ADMIT → BREACH |
| `c1-mut-store-dir-symlink-open` | symlink (store entry, dir) | `link-objects-symlink-out` (n=4) | BREACH → ADMIT |

Class coverage against the item's list, with the two slots that cannot be witnessed stated as such:

| required class | row(s) | status |
|---|---|---|
| n20 linked worktree | `gitfile-credit-revert`, `gitfile-commondir-branch-dropped` | witnessed |
| n21 separate gitdir | `gitfile-credit-revert` (n=2 includes n21), `entry-cap-shrink` | witnessed |
| n17 refs/replace | `replace-namespace-dropped` | witnessed (only after the fence repair; see Finding 2) |
| n22 alternates in `d` | `alternates-credit-revert`, `alternates-boundary-dead` | witnessed both directions |
| n18 FETCH_HEAD | `fetch-head-not-allowlisted` | **DROPPED — shadowed**: removing `FETCH_HEAD` from `GIT_TOP` changes 1 refusal *reason* but no verdict, because the reference fence still refuses `n18` earlier, at `repo/.git/config section header b'[remote "origin"]' is not plain`. The FETCH_HEAD allowlist is therefore not load-bearing on these bytes; the row will kill as soon as n18's config/refside is repaired |
| config | `config-leg-dead` (24), `config-bare-any-value` | witnessed |
| argv | `argv-order-shape-permuted` (35), `anchor-opts-narrow` | witnessed |
| symlink | `store-dir-symlink-open` (4) | witnessed |
| hardlink | `hardlink-leg-dead` | witnessed |
| mount | `mount-check-added` | **DROPPED — absent-from-base**: `grep -c st_dev` = 0 in both `05d5fe03…` and `9baedf13…`; no mount leg exists to mutate. I also authored the *additive* row (a correct `st_dev != d_dev` check on walked files): it flips nothing because every fixture is built under one device (`/fast/scratch`), so the population carries no cross-device state to refuse. Reported as a property absent from the base fence, not as a battery gap (repair seat reached the same conclusion independently) |

Sixteen fresh transforms were dropped with measured reasons (`R50C1ExecMutRebase-dropped-fresh.tsv`), each row
carrying either `reason_changes=0` (the mutated line is unreachable or fully redundant for this population:
`worktree-commondir-store-unproved`, `worktree-metadata-open`, `worktree-gitdir-unproved`, `refs-remotes-open`,
`argv-inside-dead`, `tree-file-symlink-dead`, `mount-check-added`, `gitdir-target-symlink-dead`,
`tree-dir-symlink-open`) or `reason_changes>0` with the shadowing leg quoted (`fetch-head-not-allowlisted` → the
`[remote "origin"]` header; `config-unknown-key-admitted` → `config.worktree is not a plain-init entry`;
`argv-nul-dead` → `--lane value 'lane\x00/../../outside' resolves outside the fixture`; `store-info-namespace-widen`
→ the objects-info branch; `logs-namespace-widen` → `repo/.git/refs/stash is not refs/heads, refs/tags or
refs/replace`; `store-entry-symlink-dead` → `lane/.git/objects is not a directory`; `objects-entry-symlink-dead` →
`lane/.git/objects/info is not a directory`).

## Result 3 — the deliverable, and the counter agrees with the harness

**Deliverable**: `.ufo/waves/round-50/w1/R50C1ExecMutRebase-c1-mutants.json` — sha256
`53873ed096e81355072f5577f74ebe543fa1165c1ecf27d470a286e65241eb6e`, `count=19`, 19 unique ids.
Top level is the carried schema verbatim (`target`, `candidate_fence_sha256`, `payload_format`, `count`,
`mutants`), each row carrying exactly `id, class, payload, payload_sha256, description, expected_effect,
payload_kind, digest`; `candidate_fence_sha256 = 9baedf13…`; `digest` = sha256 of the mutated fence,
`payload_sha256` = sha256 of the diff bytes. Integrity re-checked independently: 19/19 rows apply with
`patch --batch -p1`, and both digests recompute (`bad 0`).

The shipped payloads were then re-scored by an applier that never saw the authoring run (`apply_shipped.py`, shipped
as a receipt) — rows=19 caught=19 survived=0 not_applicable=0 on `9baedf13…`. That is the number to quote: it comes
from the emitted file, not from the generator's in-memory state.

End-to-end, through the counter's own code path (its `apply_mutant`, its four legs, its floor logic), twice:

```
MUTANTS total=19 caught=19 broken=0 floor=12 verdict=met
```

with `--work` on two different roots and `PYTHONHASHSEED=0` on the second run; the two receipts are byte-identical
after masking the scratch path in the fixture reasons (`IDENTICAL_ACROSS_ROOTS`). Full receipts:
`R50C1ExecMutRebase-e2e-counter.txt`, `R50C1ExecMutRebase-e2e-counter-root2.txt`.

Ported-readiness of those payloads, measured rather than assumed: the lane's **working copy** of
`plans/fixture_fence.py` is being rewritten by another seat (`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`,
991 lines, uncommitted, includes a mount leg and detached-HEAD acceptance). The same shipped battery against that
text: **rows=19 caught=7 survived=0 not_applicable=12** — twelve hunks fail to apply. So the battery is pinned to
`9baedf13…` and is *not* portable to a competing repair. If the L1 lands `57adce4a…` instead, the battery must be
regenerated against the landed bytes (`author_and_witness.py --lane <clone> --fence plans/fixture_fence.py
--transforms R50C1ExecMutRebase-transforms.py`) and re-witnessed; seven of the transforms match both texts and the
other twelve need retargeting. Receipt: `R50C1ExecMutRebase-lane-fence-battery.txt`.

## Findings for the L1 (findings, not this seat's fixes)

1. **The candidate does not meet the claim.** Same counter run, same bytes:
   `HONEST fixtures=126 admitted=117 refused=9 error=0` → `PREDICATE R50-C1 fail`. The nine are
   `n12` `[user]` section, `n13` and `n18` `[remote "origin"]` header, `n14` `logs/refs/stash`,
   `n15` `objects/info/commit-graph`, `n16` `logs/refs/notes`, `n03`/`n08` detached HEAD, `n07` `info/refs`.
   The repair seat states these are outside its five-class item; whoever closes the round must add them or the
   `HONEST admitted=126` literal cannot be met. My battery is complete for the fence as it stands, but a battery
   over a fence that fails HONEST cannot rescue the predicate.
2. **A dead leg caught mid-wave (fixed before the final sha).** At `2c4e40a0…`/`d59031f1…`, `_store` called
   `_objects(gd / "objects", …)` twice and never `_refs(gd / "refs", …)`: `GIT_REF_NAMESPACES`, `_ref_tree` and
   `_packed` were unreachable from the store path, `n17` was admitted by *absence* of a refs classification, and
   `c1-mut-replace-namespace-dropped` survived (measured). Reported to `R50C1ExecRepair`; on `9baedf13…` the
   `_refs` call is restored and the same row now kills `n17-replace-ref`. Recorded because a
   battery scored on the earlier bytes would have certified a vacuous credit.
3. **`n18`'s FETCH_HEAD credit is not independently observable** (see the coverage table): the honest fixture is
   refused by config before the store allowlist is consulted.
4. **Mount is absent from the base fence**, not merely from the candidate (`grep -c st_dev` = 0 in `05d5fe03…`).
   A mount leg is a separate item; nothing in this population can witness it.

## Limits

* The witness predicate is the counter's: one verdict per built fixture (`ADMIT`/`BREACH`/`ERROR`) over 175
  fixtures. `plans/sealed50` does not exist at `3b02d57`, so no blind module is in the reference vector.
* The end-to-end counter run used `--allow-dirty` (the clone's `plans/mutants50/c1-mutants.json` was replaced with
  the replacement battery for that leg; `TREE dirty=1` is printed in the receipt). The `MUTANTS` and `HONEST` lines
  are unaffected by dirtiness; only the predicate's default clean-tree rule is bypassed, and I cite no `PREDICATE
  pass` from that run.
* Payloads are 3-line-context diffs against `9baedf13…`: any further byte change to the fence invalidates them by
  construction. Regeneration is one command with the shipped `R50C1ExecMutRebase-transforms.py` +
  `R50C1ExecMutRebase-author_and_witness.py`.
* Two rows deliberately mutate more than one adjacent line in one hunk (`store-dir-symlink-open` drops the symlink
  *and* the is-a-directory test; `inside-dead` is a whole-property mutation). Both are single semantic weakenings,
  labelled as such in `description`.
* The battery measures admission decisions only; the outside-`d` read property stays with
  `plans/round46_c1_verify.py` and is not scored here.
* No production file was written; no commit, push, checkout or mutating git command was run in the lane. Scratch
  tree `/fast/scratch/hyaku/kengaku-r50/R50C1ExecMutRebase` removed before yielding (`rm -rf`, receipts copied to
  the wave dir first).

## Artifacts in `.ufo/waves/round-50/w1/`

| file | what |
|---|---|
| `R50C1ExecMutRebase-c1-mutants.json` | the replacement battery (19 rows, sha256 `53873ed0…`) |
| `R50C1ExecMutRebase-witness.tsv` | row → class → killing fixture → Old/New verdict → reasons |
| `R50C1ExecMutRebase-dropped-carried.tsv` | 22 carried rows dropped, per-row reason + reason-change count |
| `R50C1ExecMutRebase-dropped-fresh.tsv` | 16 fresh transforms dropped, same shape |
| `R50C1ExecMutRebase-carried23-shadow.txt` | verbatim carried-row run on `9baedf13…` with the per-row reason-change column |
| `R50C1ExecMutRebase-e2e-counter.txt`, `-root2.txt` | counter's own `MUTANTS total=19 caught=19 broken=0 floor=12 verdict=met` |
| `R50C1ExecMutRebase-determinism-diff.txt` | empty diff of the two runs' `POPULATION/HONEST/REFUSALS/SEALED/MUTANTS` lines after masking the scratch path (0 bytes = identical) |
| `R50C1ExecMutRebase-apply_shipped.py` | independent applier used for the shipped-payload re-score and the portability measurement |
| `R50C1ExecMutRebase-lane-fence-battery.txt` | shipped battery against the lane's uncommitted `57adce4a…`: caught=7, not_applicable=12 |
| `R50C1ExecMutRebase-transforms.py`, `-author_and_witness.py`, `-shadow.py` | the generator and the shadow table tool, so every number here is reproducible |

**VERDICT: mutant battery re-derived and witnessed on `9baedf13…` — 19/19 kept rows change the verdict vector
(counter floor 12 met, `broken=0`, identical across two work roots), 22 of 23 carried rows dropped with a measured
reason each, and 16 candidate transforms dropped with a measured reason each. R50-C1 admission is NOT claimed by
this seat: on the same bytes the frozen predicate prints `HONEST admitted=117 refused=9` and
`PREDICATE R50-C1 fail`.**

## Closure (post-yield, reported by the L1, not measured by this seat)

Integration is closed and **this battery was not the landed one**. Per `KengakuR50`: the landed fence is
`57adce4a…` (commit `6db0279`, receipt `d6f2fce`); the L1 regenerated a battery against those bytes — 15 rows,
every row witnessed, `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met`, `PREDICATE R50-C1 pass` exit 0 on a
clean clone, receipt `corpus/evidence/round50/c1-receipt.txt`. My 19-row battery (`9baedf13…`) was measured there as
`caught=7 not_applicable=12` and dropped rather than landed unregenerated, which is the outcome the portability
measurement above predicted. `9baedf13…` is recorded as a non-landed alternative; the nine remaining honest classes
were taken by the L1's repair, which is why the shipped fence reads 126/126. The `_refs` defect I flagged does not
reproduce on `57adce4a…` (row `c50-05-no-refs-replace` is among the 15 caught, `n16-notes-ref` is admitted, and the
blind critic's junk-ref probes BREACH).

This seat's numbers therefore stand as a measurement of a **non-landed alternative fence and of the carried r49
battery's unusability**, not as the round's shipped mutant floor.

### Successor of the candidate (measured, after the closure)

`C1ExecRepair/fence_candidate.py` moved once more after the freeze above, to
`2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc` (recursive `objects/info/alternates` with
`ALTERNATES_DEPTH = 4` and verbatim lines; `GIT_TOP`, `_store`, `_refs`, `_tree`/gitfile and `breach` byte-identical).
The emitted 19-row battery against those bytes: **caught=17, survived=0, not_applicable=2** — the two that no longer
apply are `c1-mut-alternates-credit-revert` and `c1-mut-objects-info-namespace-widen`, both anchored in the rewritten
`_objects`/`info` block; every other row still applies and still kills. Receipt:
`R50C1ExecMutRebase-successor-battery.txt`. Regeneration for those two is one command with the shipped transforms.

The repair seat also reports two witnessed kills that this battery does not carry (make `_alternates` one-level
again; restore the trailing-whitespace strip) — both are the recursive-alternates defect class that the frozen 32
hostile modules cannot see. Adding rows to a battery that the L1 has already superseded would not constrain what
lands, so they are recorded here as a pointer for whoever writes the S2 battery rather than as new rows.
