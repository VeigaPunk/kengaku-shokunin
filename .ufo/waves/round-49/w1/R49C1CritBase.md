# R49C1CritBase — C1 do-nothing control (base fence vs frozen C1 target)

- **Axis:** calibration (primary). Supporting axes iterated: classification fidelity (LEAK vs BENIGN-ADMIT), envelope retention (B1/B3/B4/B5/B6 via the round-46 pinned machinery).
- **Item:** run the cheapest do-nothing control against the frozen C1 target; if it reaches target, show the exact counterexample and state refusal of credit.
- **Access date:** 2026-10-28.
- **Claim served:** R49-C1. This seat claims no admission.

## Stage-1 freeze verification (before any scored run)

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%H %ci %an %s' -3
af88aab1… 2026-10-28 09:18:20 -0300 kengaku-shokunin round-49: w1 v2 wave spec + dispatch evidence …
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 … and C2 … claims
3a548330c4899c6c5df34168a44a59f66828ce74 2026-10-27 09:58:06 -0300 protocol-shokunin round-48 verifier spot-check …
$ git merge-base --is-ancestor 9d2900af… HEAD   → 0 (is ancestor)
$ git show 9d2900af:plans/round-49-claims.md | sha256sum → 7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83
$ sha256sum plans/round-49-claims.md                    → 7292f4e0… (identical)
$ git diff 3a548330..9d2900af --stat                    → plans/round-49-claims.md | 167 ++++ (claims text only)
$ git diff 3a548330..9d2900af -- plans/fixture_fence.py plans/round46_c1_verify.py → empty (fence + r46 counter byte-identical at freeze)
```

The freeze exists in the committed lane tree, is an ancestor of HEAD, and predates every measurement below (all runs 2026-10-28, after 09:14:40 -0300).

## Instrument: what the frozen do-nothing control is

`plans/round-49-claims.md` §Do-nothing controls freezes for C1: *"the fence at base tip `3a548330` under the stage-2 pinned v3 counter must fail on the honest leg"*. The stage-2 pinned `plans/round49_c1_verify.py` **does not exist** in the lane (`git rev-list --all -- plans/round49_c1_verify.py` → 0; `git ls-tree -r HEAD` grep → 0 hits) and no sibling has published a candidate into `w1/` at measurement time. Blocking on it would repeat last round's BLOCKED verdict.

The frozen r49 contract is `plans/round46_c1_verify.py` (digest-pinned, imported) plus deltas (a)–(f); of those, (f) MUTANTS is a new leg and (a)/(e) only *grow* the honest/sealed populations. The honest/refusals/sealed legs that the do-nothing control exercises are the legs the r48 wave-1 counter candidate already implemented verbatim against this same contract text. That candidate survives byte-exact inside the committed lane tree at `.ufo/waves/round-48/w1/R48C1ExecCounter.md` Appendix A (sha256 `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`). The honest population bytes (`r46novel` 9 + `novel48` 7 = 16 modules) are committed at `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/` and the r49 freeze re-pins these same files verbatim under `plans/honest49/` (§C1(a): "the 16 novel honest classes of `w1/R48C1ExecHonest/` … each committed at stage 2 under `plans/honest49/`").

So the honest leg of the r49 do-nothing control is executable today: identical machinery, identical fixture bytes, identical base fence. The r49 population is monotone-growth over the 120 measured here — a refusal on this subset cannot disappear.

## Control assembly (scratch-only, read-only against the lane)

```text
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1CritBase
D=/fast/scratch/hyaku/kengaku-r49/R49C1CritBase/lane
git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D"
git -C "$D" checkout -q --detach 3a548330c4899c6c5df34168a44a59f66828ce74
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"   → TOPLEVEL-OK (before every git write)
sed -n '333,765p' …/w1/R48C1ExecCounter.md > cand_counter.py
sha256sum cand_counter.py → 8726e99b… (Appendix A bytes verified, 433 lines, AST-OK)
cp cand_counter.py "$D/plans/round48_c1_verify.py"
cp …/R48C1ExecHonest/modules/{r46novel,novel48}/*.py "$D/plans/honest48/"   (16 files, digests match modules.sha256)
git -C "$D" add … && git -C "$D" -c user.name=… -c user.email=… commit -qm "scratch: control assembly"
git -C "$D" status --porcelain | wc -l → 0   (TREE clean)
git -C "$D" rev-parse HEAD → 5f634d3364bbfd39e5356408c73d979e6b24caf3  (scratch REV, not a lane revision)
```

Then `cd $D && python3 plans/round48_c1_verify.py --lane . --jobs 8` — run **twice**, identical output both times.

## Observed output (verbatim, run 2; `REV` names the scratch clone measured)

```text
REV 5f634d3364bbfd39e5356408c73d979e6b24caf3
TREE clean
PINS total=82 mismatched=0
FENCE source=/fast/scratch/hyaku/kengaku-r49/R49C1CritBase/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
LITERALS refusals=20 sealed=12 honest=120
LAYOUT refusals=…/plans/refusals46 sealed=…/plans/sealed46 honest_extra=…/plans/honest48 sealed_extra=…/plans/sealed48 novel=16 pad=24 jobs=8
COPY f1_gitfile.py … f10_laneinclude.py ok        (10/10 byte copies verified)
MODULES refusal total=20
MODULES sealed total=12
MODULES honest total=38
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=16 expected_novel=16 novel_modules=16
BENIGN total=112
BENIGN-MODULES refusals=0 sealed=0 honest=112
CALIBRATION advertised=32 contradicted=0
REASON honest-not-admitted
PREDICATE R48-C1 fail
```

`COUNTER_EXIT=1` (the earlier `EXIT=0` in-session was `tee`'s status, discarded). The eight honest refusals, verbatim — every one `BREACH clean touches=0` (refused, with zero traced outside access):

```text
FENCE-RUN honest honest48/n03_detached_head.py n03-detached-head BREACH clean touches=0 calls=444 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest honest48/n07_reflog_gc.py n07-reflog-gc BREACH clean touches=0 calls=465 -- BREACH repo/.git/info/refs is not git's exclude file
FENCE-RUN honest honest48/n08_tag_detached.py n08-tag-detached BREACH clean touches=0 calls=444 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest honest48/n12_local_config_user.py n12-local-config-user BREACH clean touches=0 calls=445 -- BREACH repo/.git/config section [user] is not allowlisted
FENCE-RUN honest honest48/n13_remote_origin.py n13-remote-origin BREACH clean touches=0 calls=445 -- BREACH repo/.git/config section header b'[remote "origin"]' is not plain
FENCE-RUN honest honest48/n14_stash_entry.py n14-stash-entry BREACH clean touches=0 calls=472 -- BREACH refs/stash has a name git does not write
FENCE-RUN honest honest48/n15_commit_graph.py n15-commit-graph BREACH clean touches=0 calls=494 -- BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
FENCE-RUN honest honest48/n16_notes_ref.py n16-notes-ref BREACH clean touches=0 calls=470 -- BREACH refs/notes has a name git does not write
```

## Finding (attack outcome)

**The do-nothing control does not reach target.** The frozen honest line requires `refused=0`; the base fence (sha256 `05d5fe03…`, byte-identical to `plans/fixture_fence.py` @ `3a548330`) refuses **8 of the 120** frozen honest fixtures — same eight families the r48 counter measured (`n03`, `n07`, `n08`, `n12`, `n13`, `n14`, `n15`, `n16`): detached-HEAD shapes, `.git/info/refs`, `[user]`, `[remote "<n>"]`, `refs/stash`, `refs/notes`, `objects/info/commit-graph`. Hostile legs stay clean (REFUSALS 20/20, SEALED 12/12, `touches=0` on all 169 fence runs), so the failure is precisely the honest leg, as the freeze predicts. **No counterexample exists; the control fails. Credit is refused to the do-nothing — and, transitively, R49-C1 credit cannot be established by doing nothing.**

The r46 "9/9" figure remains non-reproducing (measured population says 8, committed modules are the same bytes the r48 seat pinned — `modules.sha256` digests all verified in `PINS total=82 mismatched=0`).

## Impacted axes

- **calibration**: the honest leg is selective against the frozen before-value; the "must fail" control holds at 8/120 refusals, twice measured. The residual attack surface is the *r49 counter seat*, not this result: a `round49_c1_verify.py` that dropped or misclassified the honest leg could green the base fence. Stage-2 pin review must require the same `HONEST fixtures=120 admitted=112 refused=8` against the base fence (the extended `<H>` population can only grow the refusal count), and the eight `FENCE-RUN` reasons above are the located evidence to diff against.

## Limits

1. Instrument is the r48 v3 candidate bytes (sha256-verified reconstruction), not `plans/round49_c1_verify.py` — which has zero commits anywhere. Faithfulness: its honest/refusals/sealed legs implement the same frozen contract text; r49 deltas add a MUTANTS leg and extra population that a base-fence run cannot satisfy anyway.
2. `<S>` on this instrument is 12 (no `sealed48`/`sealed49` content exists yet); irrelevant to the honest-leg kill.
3. Measured REV `5f634d33` is a scratch clone tip (base `3a548330` + counter + honest48), not a lane revision; no scored run on claimed work was made.
4. `f16_objects_hardlink_out` flake (r48 limit) did not occur in either run; `build_errors=0` both times.
5. Two runs, `--jobs 8`, ~5 s each; name-hiding active (per-run tokens, PAD=24 parents) — results are byte-deterministic because the fence decision depends on fixture bytes, not names.

## Tooling

No tools installed or updated (RULES.md read; pacman transactions paused host-wide — none needed; `strace 7.2`, `git`, `python3` already on PATH).

## Sources opened (all local `file://`, accessed 2026-10-28)

1. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — §C1, §Do-nothing controls. Quote: "the fence at base tip `3a548330` under the stage-2 pinned v3 counter must fail on the honest leg".
2. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — §5 routed defects. Quote: "Any future C1 admission attempt needs the mutation floor committed with receipts."
3. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecCounter.md` — §1 + Appendix A. Quote: "HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0".
4. `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/modules.sha256` — committed population digests. Quote: "e9bd62d3…  r46novel/n03_detached_head.py".
5. `file:///home/vgpnk/.omp/agent/RULES.md` — tooling directive. Quote: "Record every install or update — tool, version, channel, reason — in your report or handoff."

## Scratch disposition

`/fast/scratch/hyaku/kengaku-r49/R49C1CritBase` (clone + receipts) removed after this report was written; receipt content is embedded verbatim above, so no scratch path is cited as evidence.

**VERDICT: CONTROL FAILS AS FROZEN — base fence refused 8/120 honest fixtures (`PREDICATE fail`, exit 1, twice measured); no counterexample; credit refused to the do-nothing. Calibration attack surface cleared on this leg; the remaining risk is counter-seat drift, diff against the 8 named refusal reasons at stage-2 pin review.**
