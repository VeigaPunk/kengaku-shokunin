# R50C1CritDoNothing — cheapest do-nothing control, fresh, plus the "any other control?" question

Seat: R50C1CritDoNothing (critic, leaf — no dispatch). Serves R50-C1 (novelty). Judged on novelty.
Round 50, hyaku run 11, wave w1. Read-only against the lane; scratch at
`/fast/scratch/hyaku/kengaku-r50/R50C1CritDoNothing` (removed before yield).

## Axes named

- **novelty** — the C1 axis under test: does `plans/round50_c1_verify.py` discriminate the claimed work
  (fence repair + witnessed mutant floor + blind `sealed50`) from the do-nothing tree, and can any cheaper
  control reach `PREDICATE R50-C1 pass` by skipping that work instead of performing it?
- No other axis touched (coverage is operator-capped this round; calibration is C2 and not mine).

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```

Measured on a `git clone --shared` of the lane, checked out at the stage-1 freeze commit.
Ancestry of the freeze checked before any measurement, against the lane tip:

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git rev-parse HEAD
5c56819f7964f4af19c960de08a49cd8f95781ce
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo "ANCESTOR: yes"
ANCESTOR: yes
$ git log -1 --format='%H %ci %s' 3b02d573…
3b02d573d58cc6d2e0d27ef92ac0815354912252 2026-10-28 14:18:09 -0300 round-50: C1 four-control receipts and C2 before/selftest receipts (pre-data)
```

Instrument digests at the measured revision agree with the frozen pins:

```
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py         (= base fence, as frozen)
f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py     (= frozen counter)
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt  (= 126 rows)
```

No production file was read-write anywhere: the clone's tree stayed `TREE dirty=0` before every run and
`git status --porcelain | wc -l` printed `0` after all runs.

## Commands run (all against the clone at 3b02d573)

```
$ cd /fast/scratch/hyaku/kengaku-r50/R50C1CritDoNothing/lane
$ python3 plans/round50_c1_verify.py --lane . --work "$S/w1" --skip-mutants
```

(the `--work` argument only redirects the fixture tree into my scratch; `--lane .` is the frozen command,
tree clean, so no `--allow-dirty`). Verbatim stdout — receipt `R50C1CritDoNothing-donothing.txt`:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
…
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
EXIT=1
```

**Do-nothing control CONFIRMED — exact match to the frozen control row** (`HONEST admitted=113`,
`PREDICATE fail`, exit 1), on a clean tree, with the frozen population pin and the frozen fence digest.
REFUSALS 20/20 and SEALED 12/12 also reproduce the pre-data counters.

The other three committed controls were run the same way (`--fence plans/controls50/<x>.py`, clean tree,
same clone), receipts `R50C1CritDoNothing-{admit_all,refuse_all,keyed_names}.txt`:

| control | fence sha256 | witnessed | predicate | exit |
|---|---|---|---|---|
| `fixture_fence.py` @ stage 1 (do-nothing) | 05d5fe03… | HONEST 113/126 admitted, 13 refused | fail | 1 |
| `controls50/admit_all.py` | 99014708… | HONEST 126/126; REFUSALS clean=0 leaked=34; SEALED clean=0 leaked=15 | fail | 1 |
| `controls50/refuse_all.py` | 9a8033d2… | HONEST admitted=0 refused=126 | fail | 1 |
| `controls50/keyed_names.py` | 7bafbb89… | HONEST 123/126 (refuses n20 commondir, n21 gitfile, n22 alternates); REFUSALS leaked=25; SEALED leaked=9 | fail | 1 |

**Answer to the question as posed on the stage-1 tree: no.** All four committed controls fail the predicate on
the frozen tree, and each fails for the leg it is supposed to skip (skipped admission reasoning → REFUSALS/SEALED
leaks; skipped refusal reasoning → 0/126; skipped boundary reasoning → the three in-`d` shape classes). The
`keyed_names` control is the one that would have caught a repair that keys on names rather than geometry, and the
counter rejects it — that is the strongest positive evidence the instrument has, and it is witnessed, not assumed.

## Counterexample: the counter prints `pass` when a frozen leg's directory is absent

The predicate's four legs are not gated on presence. `plans/round50_c1_verify.py` lines 220-224 skip any hostile
directory that is missing (`if not d.is_dir(): continue`), and lines 257-266 check the module counts only
*conditionally*. Composing a lane tree with the frozen batteries left out is therefore a control that reaches the
predicate with no fence work at all. Witnessed:

```
$ M2=$S/mini2; mkdir -p "$M2/plans"
$ for d in lane/plans/*; do b=$(basename "$d"); case "$b" in refusals46|sealed46) continue;; esac; ln -s "$d" "$M2/plans/$b"; done
$ python3 plans/round50_c1_verify.py --lane "$M2" --work "$S/w6" --fence "$S/lane/plans/controls50/admit_all.py" --skip-mutants
```

receipt `R50C1CritDoNothing-admit_all-no-batteries.txt`, verbatim:

```
REV unknown
TREE dirty=0
FENCE …/controls50/admit_all.py sha256=990147088c356a88afe1c3b2ceb43aa87a948a9baeae60227bbd5b5c30332212
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
PREDICATE R50-C1 pass
EXIT=0
```

`admit_all.py` — the cheapest control in the set, which performs none of the claimed work — prints
`PREDICATE R50-C1 pass` and exits 0. Two of the four legs never ran, and the receipt says nothing about it: no
`REFUSALS` line, no `SEALED` line, no failure. Dropping only `refusals46` shows the same silent disappearance with
the base fence (`R50C1CritDoNothing-no-refusals-leg.txt`: `HONEST 113`, then straight to `SEALED total=12`,
`PREDICATE fail` — the REFUSALS leg simply is not there, and `ok` was never touched by its absence).

Two further skip vectors in the same shape, both visible in the same two receipts:

- **`--skip-mutants` leaves `ok` untouched.** Lines 268-291 run the mutant leg only under `if not a.skip_mutants:`;
  there is no `else` that fails. A tree that satisfies the three fixture legs prints `PREDICATE R50-C1 pass`
  with the mutant floor never evaluated — i.e. skipping the QUALITY Q38 witnessed-kill work, which is precisely
  the part of C1 the claims say must be re-derived. My runs above demonstrate the missing `MUTANTS` line; the
  "and it still passes" half is [INFERENCE] from the code path, because no fence at 3b02d573 satisfies the three
  fixture legs (the repaired fence does not exist yet — see limits).
- **The clean-tree guard does not fire on a lane that is not a git repository.** Lines 173-179 take
  `rev-parse` failure as `REV unknown` and `status` failure as `dirty=0`, so a non-repo `--lane` is scored as a
  clean tree. Both witnesses above print `REV unknown` / `TREE dirty=0` and run to a verdict.

Impacted axis: **novelty (C1)**. The frozen invalidation sentence reads "A control that reaches
`PREDICATE R50-C1 pass` before the round's data invalidates the counter and the target". Reaching it here required
composing a lane with the frozen denominators deleted, which is itself outside the freeze — so I do not call the
round invalidated, and I do not judge it. What is measured is narrower and unambiguous: the instrument reports
`pass` (exit 0) while two frozen legs did not run, which the claims' own open-window list names as a repairable
**false clean**. That repair is inside the window and must be recorded old→new in the claims file and the stage-2
commit.

### Smallest safe correction (no frozen byte changes)

1. **Gate leg presence.** After the hostile loop, require `plans/refusals46`, `plans/sealed46` and `plans/sealed50`
   to exist; when one is missing print `LEG-MISSING <rel>` and set `ok = False`. Make the `REFUSALS_TOTAL` check
   unconditional and evaluate `SEALED50_MIN` against `len(plans/sealed50/*.py)` with the directory required
   (absent → 0 → below floor → fail). This changes no literal, leg name, or predicate sentence, and it makes the
   after-line's `SEALED total=<S>` with `S ≥ 18` enforced instead of merely printed.
2. **Make `--skip-mutants` unscorable.** Under the flag, print `MUTANTS skipped` and set `ok = False`; the flag
   stays usable as a leg check and can never be read as a pass.
3. **Tighten the clean-tree guard.** Require `rev` to match `^[0-9a-f]{40}$` and the `git status` call to exit 0;
   otherwise set `ok = False`. Today `REV unknown TREE dirty=0` is scored as clean.
4. *(Receipt completeness, minor)* The `HONEST-REFUSED` print is capped at `refused[:12]` (line 216) while the
   do-nothing run refuses 13, so the very run that defines the before-state cannot enumerate its own refusals.
   Print all of them (cheap: it is 13 lines) or add `HONEST-REFUSED-MORE n`.

## Coordination note for the S2 repair (evidence, not a claim)

The frozen counter's 13 refusals are **13 distinct classes**, not the five the seat brief names:

```
n03-detached-head, n07-reflog-gc, n08-tag-detached, n12-local-config-user, n13-remote-origin,
n14-stash-entry, n15-commit-graph, n16-notes-ref, n17-replace-ref, n18-shallow-fetch,
n20-linked-worktree, n21-separate-gitdir, n22-alternates-in-d
```

Receipt `R50C1CritDoNothing-refusals-enumerated.txt` (same clone, same `--skip-mutants`, with a scratch copy of
the counter whose only diff is `refused[:12]` → `refused[:64]`; the diff is in the receipt header and the numbers
are identical: `HONEST fixtures=126 admitted=113 refused=13`, `PREDICATE fail`, exit 1). The five classes
`n17/n18/n20/n21/n22` are the round-49/50 novel additions; eight carried classes are also over-refused by the base
fence (`n03`, `n07`, `n08`, `n12`-`n16`). An S2 fence that only admits the five new shapes will print
`HONEST admitted=121` and fail the HONEST leg; the honest repair target is all 13.

## Limits

- Mutant leg not run (`--skip-mutants` by item). On this control it is pointless: the base fence fails HONEST
  before the mutant floor matters, and 4/23 of the carried r49 rows change the verdict vector on the base fence —
  the candidate battery's re-derivation under witnessed kills is S2's job, not mine.
- The repaired fence does not exist at 3b02d573 nor at the lane tip 5c56819f (`fixture_fence.py` is still
  `05d5fe03…`, `round50_c1_verify.py` still `f9b9873e…`, `plans/sealed50/` absent; the tip delta is
  `.ufo/waves/round-50/{build_spec.py,w1-dispatch.json,w1-spec.json}` only). So I could not run a positive
  discrimination: the "`--skip-mutants` still passes" half and the "absent battery still passes" generalisation
  beyond the witnessed `admit_all` case are marked [INFERENCE] above. Each is a one-command witness once S2 lands.
- The two counterexample lanes are symlink trees over the clone's `plans/`, not git repositories; `REV unknown` is
  the honest reading of those receipts. They are controls of the counter, not clean-clone measurements, and they
  are citable only for the leg-presence defect.
- The honest fixtures are host-sensitive (git 2.56.0 here); identity pins make that visible and `mismatched=0`.
  Outside-`d` read property, io_uring and non-scratch host paths are out of scope, as the claims say.
- No tool installed, no package manager touched, no lane mutation, no commit/push/stash/checkout against the lane.

## VERDICT

Do-nothing control **CONFIRMED**: at `REV 3b02d573…`, clean tree, `plans/fixture_fence.py` `05d5fe03…`,
`python3 plans/round50_c1_verify.py --lane . --skip-mutants` prints `HONEST fixtures=126 admitted=113 refused=13`,
`REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`, `PREDICATE R50-C1 fail`, exit 1 — byte-for-byte the
frozen control row. **No committed control reaches the predicate on the frozen tree** (admit_all, refuse_all,
keyed_names all fail, each on the leg it skips). **But the counter has a witnessed false clean**: with the frozen
hostile batteries absent from `--lane`, `admit_all.py` prints `PREDICATE R50-C1 pass` and exits 0 with two legs
never run, and `--skip-mutants` leaves `ok` untouched so the mutant floor can be skipped the same way. Close the
leg-presence gate (and the skip-mutants and clean-tree gates) in the open window before the S2 scored run; the
four corrections above change no frozen literal, leg name, or predicate sentence. Scratch tree removed.
