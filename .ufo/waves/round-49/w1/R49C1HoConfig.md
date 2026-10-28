# R49C1HoConfig — benign config diversity critique

Axes: **calibration** (R49-C1); this is a scoped fixture-class review, not a C1 admission or score claim.

## Freeze / measured revision

Verified stage-1 freeze `9d2900af41e4d1fc6022eff99010436fde6dbd93` exists in the lane tree, with parent `3a548330c4899c6c5df34168a44a59f66828ce74`, commit time `2026-10-28 09:14:40 -0300`, message `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`; it is an ancestor of current lane HEAD `af88aab193e6034cb9b386472064e3c18fa90128`. Measurement ran only after this freeze check, against scratch clone revision **REV 9d2900af41e4d1fc6022eff99010436fde6dbd93**. No stage-2/scored counter was run.

## Counterexample and evidence

The frozen classification is explicit: traced outside-d touches distinguish `LEAK`; `touches=0` admission is `BENIGN-ADMIT`, counted separately and never as a leak (claims §C1(b)); honest fixtures must be admitted with no outside reads. Therefore inert local config data is honest only when it does not redirect config parsing, filesystem paths, or execution outside `d`.

Exact commands run (all git fixture calls were `git -C <repo>` inside the scratch clone; the round-44 `Ctx.git` checked `rev-parse --show-toplevel` equals that repo before writes):

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %P %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 af88aab193e6034cb9b386472064e3c18fa90128
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1HoConfig
cd /fast/scratch/hyaku/kengaku-r49/R49C1HoConfig
git clone --shared --quiet file:///home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
python3 /fast/scratch/hyaku/kengaku-r49/R49C1HoConfig/probe.py
```

The last command was a scratch harness using `round44_c1_verify.Ctx`, round-46's strace trace/analyser, and the frozen `fixture_fence.py`; it built and checked the already-committed r48 config fixtures. Observed output, verbatim:

```json
[
  {
    "fid": "n12-local-config-user",
    "argv": ["--lane", "repo"],
    "verdict": "BREACH",
    "reason": "BREACH repo/.git/config section [user] is not allowlisted",
    "hits": [],
    "traced_calls": 445,
    "rc": 10
  },
  {
    "fid": "n13-remote-origin",
    "argv": ["--lane", "repo"],
    "verdict": "BREACH",
    "reason": "BREACH repo/.git/config section header b'[remote \"origin\"]' is not plain",
    "hits": [],
    "traced_calls": 445,
    "rc": 10
  }
]
```

These are concrete honest over-refusals: the config is repo-local, both fence decisions had zero traced outside-d hits, but the base fence refuses. Direct source evidence at the frozen revision: `plans/fixture_fence.py` has `CFG_SECTIONS = {"core"}` and a seven-entry `CFG_KEYS`; `_config` rejects non-allowlisted sections (lines 251–253) and unknown keys (258–260). Its `SECTION_LINE` accepts only a plain `[name]` header, so valid Git subsection syntax such as `[remote "origin"]` fails before a section policy can classify it. Existing committed r48 classes already provide `[user]` and remote-origin cases, while this seat's requested expansion is extra benign `[core]` keys, `[init]` defaults, branch tracking sections, and multiple remote/branch variation.

## Strongest counterexample / smallest safe correction

Do not equate “unknown config” with “hostile,” but also do not blanket-allow sections or values. Add only literal, non-path, non-executable settings to the honest domain (e.g. suitable `core` boolean/enum/integer settings, repo-local `[user]`, `[init] defaultBranch`, and ordinary `[branch]` / `[remote]` tracking metadata), parsing Git's quoted subsection headers and values faithfully. Keep include/includeIf, path-valued config, external object/worktree pointers, executable hooks/fsmonitor/ssh/proxy/pager/editor/`!` aliases, URL rewrite keys, and equivalent redirectors refused unless the fence proves their effective target/behavior confined to `d`. A blanket section allowlist would let an `include.path` or exec-bearing value ride along with benign diversity; parse-and-classify keys/values, not just section names.

The scratch candidate contained five further fixtures (extra `core` scalars; `[user]` + `[init]` + `[branch]`; multiple remotes and branch tracking; config in a sibling repo; inert scalar sections) and eleven pointer/exec probes, but its first combined run aborted after a deliberately `core.worktree=../other-worktree` hostile probe failed the post-build safety check. That attempted run yielded no classification results for those candidate fixtures and is not counted as evidence. The successful focused run above measured only n12/n13. The proposed additional classes therefore remain unverified; do not fold them into `<H>` until built and measured under the stage-2 counter. This review does not claim C1 admission.

## Commands, limits, provenance

Tool availability checked: `command -v strace git bwrap python3`; outputs `/usr/bin/strace`, `/usr/bin/git`, `/usr/bin/bwrap`, `/usr/bin/python3`; versions `git version 2.56.0`, `strace -- version 7.2`, `Python 3.14.8`. No tools installed or updated. No external source opened (no URL / access date / quote applies). Limits: strace establishes zero in-scratch-root outside-d touches for these two fence runs; it does not prove all host-wide accesses absent (counter's frozen limits apply), nor prove the proposed new classes safe. The combined candidate failure is disclosed above. Scratch directory was removed before report completion (`rm -rf /fast/scratch/hyaku/kengaku-r49/R49C1HoConfig`; observed `SCRATCH-REMOVED`).

**VERDICT: BASE FENCE OVER-REFUSES benign `[user]` and `[remote "origin"]` configuration with zero traced outside-d touches; accept these as BENIGN-ADMIT in the frozen v3 classification when admitted; keep path/exec/redirect config hostile. Additional requested variants are not yet measured.**
