# R45CritLandedFence — round 45 a3w1

**Measured lane:** `master` at `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (clone verified at that commit). Axes: **calibration**, **containment**, **boundedness**.

## Baseline counter

Command, run in the clone with the required envelope:

```text
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane "$S/lane" --work "$S/w"
```

Receipt (`.ufo/waves/round-45/a3w1/R45CritLandedFence/c1-baseline.txt`):

```text
PINS total=33 mismatched=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:33:00 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Start/end and the full envelope command are retained in that receipt. It supports the stated fixed-suite result, but not arbitrary hostile modules.

## Confirmed defect: an escaping symlink inside `.git` passes the fence

The fixture walk explicitly removes `.git` from descent (`plans/fixture_fence.py:153`); its follow-up store checks at lines 157–200 inspect named redirects/config, but do not reject symlinks in `.git/objects`. I wrote `hx_git_objects_link.py` in my seat directory. Its builder makes a normal committed repo, moves its complete objects directory to a sibling of fixture `d` (still within the module build root), and symlinks `.git/objects` to that external directory. The module otherwise uses the standard `FIXTURES`/`build(ctx, d)` contract.

Command: the envelope runs `run_hostile.py`, which uses the landed counter's `build_module` and `run_fence` machinery, the cloned landed fence, bwrap, and strace. The first harness attempt tried to preserve strace under the read-only lane and failed with `EROFS`; that was not a measurement. I redirected its capture into scratch and reran successfully:

```text
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45CritLandedFence/run_hostile.py
```

Measured output (`.../R45CritLandedFence/hostile-run.txt`):

```text
BUILT [{"fid": "hx-git-objects-outside", "tool": "order", "argv": ["--lane", "lane", "--claims", "claims.md", "--receipt", "receipt.txt"], ...}]
RESULT ('ADMIT', '', 8)
ENVELOPE end 00:34:24 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

The returned `8` is the counter's outside-open count. Independent trace evidence is retained in `.../R45CritLandedFence/hostile-strace.txt`: successful opens at lines 217–220 resolve to `.../fx/R45CritLandedFence-hx_git_objects_link/outside-objects/...`, outside fixture `d` but inside its build root. For example line 218 opens `.git/objects/4f/66c18386a8192aaef3b1af391a6ba72eedfdbc` and the returned fd is annotated with the sibling `outside-objects` path. Therefore this is both an **ADMIT** and an outside read, not merely a source-level concern.

**Smallest safe correction:** while traversing each collected `.git` directory, inspect its direct store entries (at minimum reject symlinks and special files anywhere in the store, without following them); do not rely on the current small set of named checks. Add this hostile module as a held-out regression and require refusal with zero outside opens.

## Other requested source checks

- **(a) f1–f10 keyed handling:** no numbered refusal-module names are used in the fence decision path; it applies generic argv, filesystem, config, and Git probes. This attack is a missed mechanism (`.git` subtree symlinks), not an f-number branch.
- **(b) unbounded walk/races:** `_collect` has an `ENTRY_CAP` check (`fixture_fence.py:124–128`); I found no uncapped traversal or mutable-fixture race in the read-only `run_fence` arrangement. The cap is checked after `os.walk` yields a directory listing, so it is not a strict bound on the size of one `scandir` result; I did not measure a single-directory stress case and do not count it as demonstrated here.
- **(c) git bounds:** every fence Git operation routes through `_git` (`60–71`), which sets `GIT_CEILING_DIRECTORIES`, `stdin=DEVNULL`, and `timeout=GIT_TIMEOUT`; probes and order `cat-file` calls use that wrapper (`210–240`, `268–275`). No missing ceiling/timeout/stdin case found.
- **(d) leg order:** `breach` runs `_collect` and returns on its refusal before entering the probe loop (`244–265`); `_collect` performs the static scan before returning (`77–204`). No Git-before-static-scan path found.
- **(e) `is_relative_to`:** `_inside` resolves both candidate and fixture directory before testing containment (`51–57`); other containment uses in the decision path call `_inside` or resolve first. No unresolved-path misuse found.

## Evidence files

All are under `.ufo/waves/round-45/a3w1/R45CritLandedFence/` (no lane files changed):

- `c1-baseline.txt`
- `hx_git_objects_link.py`
- `run_hostile.py`
- `hostile-run.txt`
- `hostile-strace.txt`

VERDICT: landed-fence-defects-1-demonstrated-1
