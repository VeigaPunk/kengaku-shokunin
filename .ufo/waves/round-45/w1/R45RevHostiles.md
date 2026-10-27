# R45RevHostiles — hostile fixture fidelity review

Scope: the ten `plans/refusals45/` modules, checked against round-44 routed findings and built with the C1 counter's pinned round-44 builder. No lane source was edited; no packages were installed.

## Result

**10/10 scenarios faithfully built; 0 fixture-description defects.** The f1–f6 files are byte-identical to the round-44 hostile originals. The disputed f9 and f10 conditions both hold: f9's `rev-parse --show-toplevel` exits 128; f10's regular include target is a sibling of `d`, not inside it.

## Routed basis

The round-44 closure routes V1–V3 (commondir, second-config include, refuse-to-describe) and the lane-include read to the next round (`corpus/lessons/round-44-verifier-spotcheck.md:143-153`). The detailed f1–f6 basis is `R44SentinelFences.md`: V1 lines 33-45, V2 lines 104-144, V3 lines 146-180, and negative controls lines 182-210. The f10 read-before-refusal route is `R44LabratLaneInclude.md:14-35, 63-76, 143-163`. The modules' scenario statements align with those reports.

## Build and scenario evidence

Build command: `S=/fast/scratch/hyaku/kengaku-r45/R45RevHostiles; export TMPDIR="$S"; claims/envelope.sh "$S/env" python3 "$S/build_review.py"`. The scratch driver imported `round45_c1_verify.py` and called its `build_module(k44, lane, root, module)` for each module; this uses `round44_c1_verify.py`'s `builder_source()` and read-only bwrap build sandbox. It built **10 modules / 15 fixtures** (f7: 3, f8: 2, others: 1 each).

Envelope for build: `ENVELOPE start 23:29:31 cwd=/home/vgpnk/Projects/shokunin`; `ENVELOPE end 23:29:34 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`.

| Module | Built scenario evidence (from builder output and follow-up probes) | Assessment |
|---|---|---|
| f1 (`f1_gitfile.py:6-17`) | `d/.git` is a file; its `gitdir:` target exists at `d`'s parent under `side/gitdir`. | Faithful |
| f2 (`f2_deep.py:6-14`) | Repo path is `d/x/y/z/r` (four levels); `core.worktree` is `.../f2_deep/wt`; `git rev-parse --show-toplevel` returns that outside path. | Faithful |
| f3 (`f3_abbrev.py:5-13`) | `plans/round-7-claims.md` is a directory and `git ls-tree HEAD` reports mode `040000 tree`; argv uses `--claim` and `--receip` abbreviations. | Faithful |
| f4 (`f4_fifo.py:8-16`) | `d`'s parent `fifo.cfg` is a FIFO; `.git/config` has `include.path` to it. Build completed without blocking. | Faithful |
| f5 (`f5_alternates.py:6-16`) | `objects/info/alternates` points to the sibling store's object directory. A lookup of that store's commit from the fixture repo returned rc 0, type `commit` (actual borrowed-object lookup). | Faithful |
| f6 (`f6_above.py:7-12`) | Repo `.git` is at `d`'s parent; `d/sub/.git` is absent; discovery from `d/sub` returns the parent repo as toplevel. | Faithful |
| f7 (`f7_commondir.py:11-61`) | All 3 fixtures have `.git/commondir` pointing to sibling stores; `--show-toplevel` and `--absolute-git-dir` return paths inside `d`, while `--git-common-dir` returns each sibling store. | Faithful |
| f8 (`f8_worktreecfg.py:12-38`) | Both fixtures set `extensions.worktreeConfig=true`; each `.git/config.worktree` includes an existing sibling file. `git config --show-origin --get user.email` reads `OUTSIDE-MARKER@invalid` from that outside file. | Faithful |
| f9 (`f9_nodescribe.py:11-21`) | `core.bare=true`; `git rev-parse --show-toplevel` returned **128**, `fatal: this operation must be run in a work tree`. | Faithful; the claim is directly confirmed |
| f10 (`f10_laneinclude.py:12-24`) | `inc10.cfg` exists at `d`'s parent, is a regular file, and `.git/config` references it; `git config --get user.email` reads `OUTSIDE-READ@invalid`. | Faithful; include is outside `d` |

Build output listed every module's fixture id: f1 `f1-gitdir-outside`; f2 `f2-deep-worktree`; f3 `f3-abbrev-tree-claims`; f4 `f4-fifo-include`; f5 `f5-alternates-outside`; f6 `f6-repo-above-d`; f7 `f7-cd-accept`, `f7-cd-reject`, `f7-cd-anchor`; f8 `f8-wtcfg-a`, `f8-wtcfg-b`; f9 `f9-bare-repo`; f10 `f10-lane-include-regular`.

Follow-up probe command: `claims/envelope.sh "$S/env" python3 "$S/extra_checks.py"`; output confirmed f2's outside toplevel, f7's inside gitdir/outside common-dir, and f8's outside config origins. Envelope: `start 23:30:31`; `end 23:30:33 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`.

f5 follow-up command: `claims/envelope.sh "$S/env" python3 "$S/f5_borrow_check.py"`; output `external_commit 8e4c79a979197857ef833f1d814d9315f6bc076a lookup_rc 0 type commit`. Envelope: `start 23:30:58`; `end 23:31:00 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`.

## f1–f6 byte identity

Command: `sha256sum <round45 f1-f6 paths> <round44 claims/hostile f1-f6 paths>`. Each corresponding digest was identical:

| File | SHA-256 (round45 = round44 hostile) |
|---|---|
| f1_gitfile.py | `bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d` |
| f2_deep.py | `027972c63696dd16e147b70002a532bf754ef5bd4f31956ae4510efd8ddcb734` |
| f3_abbrev.py | `05a43c051053d131fc11a0f7625c0b28fc0ca1a8c5d9c5302fca5f21062ead48` |
| f4_fifo.py | `6ba6a730192d056f60e1accfb1a31f30e2133296b56537ff6047d0da6817d043` |
| f5_alternates.py | `8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4` |
| f6_above.py | `e9a599e400952eb203123205754f7993a37c83de9ddc881521bbcaa4df4608df` |

## Verification gaps

No LSP device/server is mounted in this seat's tool inventory (`read xd://lsp` returned “No such tool”); this is a direct source-and-built-fixture review, not an LSP semantic check. I did not run the full C1 fence predicate; it was outside this assigned fidelity review. No installs or upgrades.

VERDICT: hostile-modules-faithful-10/10-defects-0
