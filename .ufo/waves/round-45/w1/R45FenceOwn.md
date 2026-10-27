# R45FenceOwn — C1 calibration: `plans/fixture_fence.py` (round 45, wave 1, build)

Seat: executor (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat).
Scratch: `/fast/scratch/hyaku/kengaku-r45/R45FenceOwn` (module written in its clone `$S/lane`, deleted at the end).
No lane file was edited; no `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, jj state or Git index touched.

**Result: the fence passes the frozen predicate on the first build, and on three re-runs.**

| line | value |
|---|---|
| `PINS total=33 mismatched=0` | yes |
| `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0` | yes |
| `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0` | yes |
| `CALIBRATION advertised=10 contradicted=0` (before: **7**) | yes |
| `PREDICATE C1 pass`, exit 0 | yes |
| ENVELOPE `local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged` | yes |

## Files this seat produced

- `$S/lane/plans/fixture_fence.py` — the module (in the scratch clone only; the L1 integrates it into the lane).
- `.ufo/waves/round-45/w1/R45FenceOwn/fixture_fence.py` — **the primary candidate**, byte-identical,
  16375 B / 390 lines, `sha256=3b540e0d2dcc9125da0bff8f21d024ae3ab11720e37ed3cf11c90d53dba3fcc6`.
  Copy verbatim to `plans/fixture_fence.py`; the counter prints that digest on its `FENCE` line.
- `.ufo/waves/round-45/w1/R45FenceOwn/counter-run-final.txt` (11746 B, 136 lines,
  `sha256=205b12503177971a233d3c141afb5b0a04f85b3b559d5fe5f1ac370fef373425`) — the pasted run below.
- `.ufo/waves/round-45/w1/R45FenceOwn/counter-run1-first-pass.txt` — the first run, before the two
  hardening/bounding edits (same predicate; `fixture_fence.py` sha `f4cb15f1…`).
- `.ufo/waves/round-45/w1/R45FenceOwn/counter-run-determinism.txt` — a second run of the final module
  (`sha256=c8ecc345…`); its `FENCE-RUN`/`REFUSAL` decision lines are identical to `counter-run-final.txt`
  after normalising the random `k45-c1-*` scratch name (`diff` → `DECISIONS_IDENTICAL`).

Measurement commands (all inside the envelope; `S=/fast/scratch/hyaku/kengaku-r45/R45FenceOwn`):

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel          # -> $S/lane   (verified before any write)
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py \
    --lane "$S/lane" --work "$S/w"
```

## Full counter output (final run)

Reproduced from `counter-run-final.txt`; the byte-exact original is that file (`sha256=205b1250…`).

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/env /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/env --bind /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/lane --work /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/w
ENVELOPE start 23:50:01 cwd=/fast/scratch/hyaku/kengaku-r45/R45FenceOwn
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=3b540e0d2dcc9125da0bff8f21d024ae3ab11720e37ed3cf11c90d53dba3fcc6
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- lane/config carries a [include] section
FENCE-RUN refusal refusals45/f1_gitfile.py f1-gitdir-outside BREACH opens=0 -- .git is a file (gitdir redirect), not a directory
FENCE-RUN refusal refusals45/f2_deep.py f2-deep-worktree BREACH opens=0 -- x/y/z/r/work tree /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/w/k45-c1-2448xqwb/fx/refusals45-f2_deep/wt is not the repo
FENCE-RUN refusal refusals45/f3_abbrev.py f3-abbrev-tree-claims BREACH opens=0 -- order argv is not the contract shape ['--lane', '--claims', '--receipt']: ['--lane', '/fast/scratch/hyaku/kengaku-r45/R4
FENCE-RUN refusal refusals45/f4_fifo.py f4-fifo-include BREACH opens=0 -- lane/config carries a [include] section
FENCE-RUN refusal refusals45/f5_alternates.py f5-alternates-outside BREACH opens=0 -- lane/.git/objects/info/alternates present (objects borrowed)
FENCE-RUN refusal refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- a git store sits above the fixture at /fast/scratch/hyaku/kengaku-r45/R45FenceOwn/w/k45-c1-2448xqwb/fx/refusals45-f6_abo
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-accept BREACH opens=0 -- lane/.git/commondir present (store redirected outside the fixture)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-reject BREACH opens=0 -- lane/.git/commondir present (store redirected outside the fixture)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-anchor BREACH opens=0 -- lane/.git/commondir present (store redirected outside the fixture)
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-a BREACH opens=0 -- lane/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-b BREACH opens=0 -- lane/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f9_nodescribe.py f9-bare-repo BREACH opens=0 -- lane/git cannot describe the work tree (rc=128)
FENCE-RUN honest battery42/a_class.py a_class-x6-sibling-digest ADMIT opens=0
FENCE-RUN honest battery42/a_class.py a_class-x6-stale-manifest ADMIT opens=0
FENCE-RUN honest battery42/a_class.py a_class-x7-fabricated-token ADMIT opens=0
FENCE-RUN honest battery42/a_class.py a_class-x7-provenance-row ADMIT opens=0
FENCE-RUN honest battery42/a_class.py a_class-x14-uppercase-token ADMIT opens=0
FENCE-RUN honest battery42/a_class.py a_class-x14-two-errata ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x1-provenance-table ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x1-two-row-registry ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x3-provenance-url ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x3-blob-url ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x12-slashless-toml ADMIT opens=0
FENCE-RUN honest battery42/a_route.py a_route-x12-two-tomls ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x9-short-no-token ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x9-registry-short-valid ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x13-staged-capture ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x13-url-staged ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x15-sibling-digest ADMIT opens=0
FENCE-RUN honest battery42/a_row.py a_row-x15-manifest-sibling ADMIT opens=0
FENCE-RUN honest battery42/o_clause.py o_clause-freeze-single ADMIT opens=0
FENCE-RUN honest battery42/o_clause.py o_clause-freeze-pair-edited-after ADMIT opens=0
FENCE-RUN honest battery42/o_clause.py o_clause-receipt-withdrawn ADMIT opens=0
FENCE-RUN honest battery42/o_clause.py o_clause-receipt-side-line ADMIT opens=0
FENCE-RUN honest battery42/o_clause.py o_clause-clean-order ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo5-post-receipt-verdicts ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo5-amended-claims-blob ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo6-pass-verdict-row ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo6-echoed-pass-row ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo7-timeout-rows ADMIT opens=0
FENCE-RUN honest battery42/o_scan.py o_scan-xo7-skipped-row-r38 ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-longrow-copied ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-longrow-multicap ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-slug-deepest ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-slug-blob ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-manifest ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-sibling ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-short ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-upper ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-two ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-erratum-lessons ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-longrow-late ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-slug-manifest ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-shorturl-sibling ADMIT opens=0
FENCE-RUN honest battery43/a_alt.py a_alt-shorturl-samedir ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f1-repaired-row-historical-erratum ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f2-two-rows-provenance-two-errata ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f3-stale-token-sibling-capture ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f4-manifest-only-second-capture ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f5-row-carrying-both-tokens ADMIT opens=0
FENCE-RUN honest battery43/a_err.py a_err-f6-provenance-bound-unknown-stale ADMIT opens=0
FENCE-RUN honest battery43/a_row.py a_row-na1-tail12 ADMIT opens=0
FENCE-RUN honest battery43/a_row.py a_row-na1-mid13 ADMIT opens=0
FENCE-RUN honest battery43/a_row.py a_row-na1-wide20 ADMIT opens=0
FENCE-RUN honest battery43/a_url.py a_url-org-slash-single ADMIT opens=0
FENCE-RUN honest battery43/a_url.py a_url-org-slash-registry ADMIT opens=0
FENCE-RUN honest battery43/a_url.py a_url-short-commit-pair ADMIT opens=0
FENCE-RUN honest battery43/a_url.py a_url-short-commit-shadow ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-late-case-blob ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-inplace-gate-rewrite ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-fenced-echo ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-two-echo-blobs ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-bare-ok-late ADMIT opens=0
FENCE-RUN honest battery43/o_alt.py o_alt-prefixed-ok-blob ADMIT opens=0
FENCE-RUN honest battery43/o_excuse.py o_excuse-echo-freeze-claims ADMIT opens=0
FENCE-RUN honest battery43/o_excuse.py o_excuse-gate-prefix-late ADMIT opens=0
FENCE-RUN honest battery43/o_excuse.py o_excuse-bare-excused ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n5a-late-gate-file ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n5b-amended-claims ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n5c-case-third-commit ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n22a-gate-only ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n22b-echoed-defect ADMIT opens=0
FENCE-RUN honest battery43/o_scan.py o_scan-n22c-indented-gate ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_a.py u14c_name_a-draft-suffix ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_a.py u14c_name_a-subdir-nohyphen ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_a.py u14c_name_a-uppercase-pair ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_a.py u14c_name_a-canonical-control ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_b.py u14c_name_b-registry-suffix ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_b.py u14c_name_b-nested-uppercase ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_b.py u14c_name_b-round-xx-token ADMIT opens=0
FENCE-RUN honest battery44/u14c_name_b.py u14c_name_b-underscore-name ADMIT opens=0
FENCE-RUN honest battery44/u5_short_a.py u5_short_a-manifest-registry ADMIT opens=0
FENCE-RUN honest battery44/u5_short_a.py u5_short_a-index-staged ADMIT opens=0
FENCE-RUN honest battery44/u5_short_a.py u5_short_a-abbrev-neighbour ADMIT opens=0
FENCE-RUN honest battery44/u5_short_b.py u5_short_b-registry-url-task ADMIT opens=0
FENCE-RUN honest battery44/u5_short_b.py u5_short_b-index-ref-staged ADMIT opens=0
FENCE-RUN honest battery44/u5_short_b.py u5_short_b-lane-path-manifest ADMIT opens=0
FENCE-RUN honest battery44/u5_short_b.py u5_short_b-history-truncation ADMIT opens=0
FENCE-RUN honest battery44/u6_long_a.py u6_long_a-registry-65 ADMIT opens=0
FENCE-RUN honest battery44/u6_long_a.py u6_long_a-manifest-96 ADMIT opens=0
FENCE-RUN honest battery44/u6_long_a.py u6_long_a-provenance-128 ADMIT opens=0
FENCE-RUN honest battery44/u6_long_a.py u6_long_a-history-200 ADMIT opens=0
FENCE-RUN honest battery44/u6_long_b.py u6_long_b-registry-80hex ADMIT opens=0
FENCE-RUN honest battery44/u6_long_b.py u6_long_b-provenance-129hex ADMIT opens=0
FENCE-RUN honest battery44/u6_long_b.py u6_long_b-index-pair-96hex ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_a.py u7_twin_a-rowpath-registry ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_a.py u7_twin_a-provenance-table ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_a.py u7_twin_a-url-two-tasks ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_b.py u7_twin_b-url-trio-identical ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_b.py u7_twin_b-prov-twin ADMIT opens=0
FENCE-RUN honest battery44/u7_twin_b.py u7_twin_b-mixed-trio ADMIT opens=0
FENCE-RUN honest battery44/u9_worktree_a.py u9_worktree_a-registry-wrong-capture ADMIT opens=0
FENCE-RUN honest battery44/u9_worktree_a.py u9_worktree_a-history-abbrev ADMIT opens=0
FENCE-RUN honest battery44/u9_worktree_b.py u9_worktree_b-registry-erratum-appended ADMIT opens=0
FENCE-RUN honest battery44/u9_worktree_b.py u9_worktree_b-erratum-retargeted-history ADMIT opens=0
FENCE-RUN honest battery44/u9_worktree_b.py u9_worktree_b-erratum-completed-in-place ADMIT opens=0
REFUSAL f10_laneinclude.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f1_gitfile.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f2_deep.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f3_abbrev.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f4_fifo.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f5_alternates.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f6_above.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f7_commondir.py clean fixtures=3 admitted=0 hung=0 opens=0
REFUSAL f8_worktreecfg.py clean fixtures=2 admitted=0 hung=0 opens=0
REFUSAL f9_nodescribe.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 23:50:09 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

ENVELOPE lines of every run (start/end, digest verdict):

| run | module sha256 | ENVELOPE start | ENVELOPE end | ~/.local/bin |
|---|---|---|---|---|
| 1 (first pass) | `f4cb15f1…` | 23:47:14 | 23:47:22 exit=0 | `e396f23e…` = `e396f23e…` unchanged |
| 2 | `f4cb15f1…` | 23:47:56 | 23:48:04 exit=0 | unchanged |
| 3 (include hardening) | `657a7f8d…` | 23:48:28 | 23:48:35 exit=0 | unchanged |
| 4 (final) | `3b540e0d…` | 23:50:01 | 23:50:09 exit=0 | unchanged |
| 5 (determinism) | `3b540e0d…` | 23:50:19 | 23:50:27 exit=0 | unchanged |

Every run carried the full envelope, not just the first: the digest is identical in all five and no run
returned exit 4. Wall time per run 9–11 s (114 fences, `--jobs 8`), so the counter's 120 s per-fence
`FENCE_TIMEOUT` is never approached.

## Before → after, per hostile module

`before` = `claims/control-c1-fence-r44.txt` (the round-44 fence), `after` = this fence (final run).
`opens` is the counter's outside-open count for that module.

| module | before | after | after: reason (one line) |
|---|---|---|---|
| f1_gitfile | READ opens=6 | clean opens=0 | `.git` is a file (gitdir redirect) |
| f2_deep | clean opens=0 | clean opens=0 | work tree `<scratch>/fx/refusals45-f2_deep/wt` is not the repo |
| f3_abbrev | clean opens=0 | clean opens=0 | order argv is not the contract shape |
| f4_fifo | READ opens=1 | clean opens=0 | `lane/config` carries an `[include]` section (FIFO never opened) |
| f5_alternates | clean opens=0 | clean opens=0 | `.git/objects/info/alternates` present |
| f6_above | READ opens=3 | clean opens=0 | a git store sits above the fixture |
| f7_commondir | LEAKED (3/3) | clean opens=0 | `.git/commondir` present |
| f8_worktreecfg | LEAKED (2/2) | clean opens=0 | `lane/config` enables `extensions.worktreeConfig` |
| f9_nodescribe | LEAKED | clean opens=0 | `git cannot describe the work tree (rc=128)` |
| f10_laneinclude | READ opens=4 | clean opens=0 | `lane/config` carries an `[include]` section |

`CALIBRATION advertised=10 contradicted=7` → `contradicted=0`.

Both columns of that table are this seat's own measurements (before: `claims/control-c1-fence-r44.txt`;
after: `counter-run-final.txt`), so the L1 can cite the executor for both.

**How f9 is refused — precisely.** The refusal string is `lane/git cannot describe the work tree (rc=128)`,
i.e. it derives from the **git tier**, not from reading `core.bare` out of `.git/config`. The fence never
inspects a `bare` key: its config parser looks only for include surfaces and `extensions.worktreeConfig`, so
it passes the filesystem legs and is stopped by `rev-parse --show-toplevel` returning non-zero, which
`_store_git` treats as "unverifiable → breach" (the rule `R44SentinelFences` V3 and the f9 module docstring
both name). A text read of `core.bare` would have been possible — `_config_breach` already parses
`[section]`/`key` pairs — and it is deliberately not used, so the frozen hostile stays decided by the
behavioural tier rather than by one more string pattern.

## Design: leg order, and the two obligations from `R45RevengerOrder`

Both of that seat's measured obligations are met, and both are load-bearing here:

1. **argv syntax before every argv-consuming leg.** `_argv_shape` is the first statement of `breach`; it
   validates the tool, the list-of-strings type, the exact order shape `["--lane", v, "--claims", v,
   "--receipt", v]` (6 tokens) or the anchor option set (`--lane`/`--evidence-ref` values, `--verbose` flag,
   `--lane` required), and rejects `--claim`/`--receip` abbreviations and `--opt=value`. `--claims` is read
   only through `_values` after that leg passed, so no leg can raise `KeyError('--claims')` the way round
   44's `order_argv_breach` did (a build error instead of a refusal). f3 is refused on this leg with
   `opens=0`.
2. **No leg raises; f9 needs the git tier.** Every leg returns `str | None`; the filesystem legs use `stat`
   and text parsing only, `_config_breach` refuses (rather than opens) a non-regular `config*`, and `breach`
   ends in a `try/except Exception` last resort so a malformed fixture is a refusal, not a crash. f9
   (`core.bare=true`) is invisible to every filesystem leg by design, and is refused by the store probe
   tier: `rev-parse --show-toplevel` → `rc=128` → "git cannot describe the work tree", i.e. a non-zero rc
   is a breach, never "clean".

The order that makes `opens=0` possible, in the module:

1. `_argv_shape` (pure syntax).
2. `_walk(d)` — one pass, no depth cap, no descent into `.git`; `.git` as a FILE → breach; a symlink whose
   `realpath` leaves `d` → breach; > 200000 entries → breach instead of a silent skip.
3. `_store_fs` per repo under `d` — `.git/commondir`, `.git/config.worktree`, any `.git/config*` (and
   `.git/worktrees/*/config*`) whose text carries an `[include…]` section, an `include.path` /
   `includeIf.*.path` key or `extensions.worktreeConfig`, `.git/objects/info/alternates`. This leg must run
   before any git child: git parses the repo config and honours `commondir` on *every* invocation, which is
   precisely why round 44's `lane_breach` (git first) opened the FIFO include (f4, opens=1), the regular
   include (f10, opens=4), the side gitdir (f1, opens=6) and the repo above `d` (f6, opens=3).
4. `_ancestor_breach` — `stat` only, so nothing above `d` is opened: a `.git` at `d.parent` (the module
   build root, where f6 builds its repo) or at the counter's `fx/` level above it.
5. git legs, second tier, bounded: `GIT_CEILING_DIRECTORIES=d.parent`, 10 s per call inside a 45 s overall
   budget, no stdin, `PATH` without any per-user bin, config pins that neutralise
   fsmonitor/hooksPath/gpg.program/log.showSignature (copied from the counter's `GIT_PINS`).
   `rev-parse --absolute-git-dir` (inside `d`), `rev-parse --show-toplevel` (equal to the repo dir),
   `config --local --no-includes --get core.worktree` (absent or the repo itself), and for `order`
   `cat-file -t HEAD:<claims|receipt>` (a tree at HEAD is a breach; a path missing at HEAD stays the tool's
   own setup error, which is the frozen wording "names a non-blob at HEAD"). `--lane` is resolved against
   `d`, must stay inside `d`, and the nearest `.git` at or above it inside `d` is its repository; a lane
   that names no repository inside `d` is a breach (this is also what catches a repo above `d` at any depth,
   because discovery is ceiling-ed at `d.parent`).

Honest fixtures stay admitted because the batteries build exactly what the contract says: a repo rooted at
its own directory inside `d` (`ctx.init(d)` or `ctx.init(d/<sub>)`), no `.git` file, no commondir, no
alternates, no include, no symlink leaving `d`, and argv of the contract shape. 104/104 admitted, `opens=0`,
three runs.

## Limits (named)

1. **The ancestor leg is deliberately shallow**: `d.parent` and `d.parent.parent` only, both created by the
   counter, never by a module. A repo further above `d` is not seen by that leg — it is still refused by the
   lane leg above (a lane with no repository inside `d` is a breach), but a fixture that had *both* a legit
   repo inside `d` and a repo higher up would only be judged on the legit one. A future fixture layout where
   the module root is not `d.parent` needs this leg re-pointed.
2. **Include detection is a text scan, not a git parse.** The parser tracks `[section]` + `key` and refuses
   any section starting with `include` (so `[include]`, `[includeIf "…"]`, even a stray `[include "x"]`),
   any `include.path` / `includeIf.*.path` key, and `extensions.worktreeConfig`. A config that hides an
   include from that parser (exotic quoting/continuation, an include reached through a file not named
   `config*`) would be admitted and then parsed by the git tier, whose `rev-parse`/`cat-file` do honour
   includes. Mitigations: `--no-includes` on the worktree probe, `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL`
   pins, and the fact that the fence refuses on *any* include surface, so an include of an include is
   irrelevant. This is the one residual gap a held-out critic should aim at.
3. **Two deliberate strictnesses beyond the frozen wording**: any non-regular `.git/config*` is refused
   unopened (so a FIFO named `config` cannot block), and any `extensions.worktreeConfig` value is refused,
   including `false`. No honest fixture carries either; a future battery that does would be refused.
4. **It is not a pure-filesystem fence.** ~5 git children per fixture: `MAX_REPOS=64`, `GIT_TIMEOUT=10`,
   `GIT_BUDGET=45` bound the worst case, but the fence depends on a working `git` in `PATH` (that PATH has
   no per-user bin, so no shim can be adopted).
5. **Token resolution is option-aware**: `--lane` is resolved against `d` and containment-checked;
   `--claims`/`--receipt` are repo-relative (the batteries pass `plans/round-42-claims.md` while `--lane` is
   `d/lane`), so they are containment-checked for `..` rather than resolved against `d` — resolving them
   against `d` would not describe what the modules mean; `--evidence-ref` is a ref name (`index`) and is
   only shape-checked.
6. **`opens` is measured on the paths the counter counts** (under `<root>/fx`, `<root>/btmp`, outside `d`).
   An open of, say, `$HOME/.gitconfig` would not be counted by the counter; the fence still pins
   `GIT_CONFIG_GLOBAL=/dev/null` and `HOME=/nonexistent` so it does not happen.

## Frontier / routed ledger — contribution and ownership

The frontier row triad in the wave brief (attempt-1 do-nothing battery draft; probe docstring garble; the
spec's extra row) plus the Gate-block admit/reject pair belong to the C2 seats` work; I did not write
`corpus/routed-findings.jsonl` (lane files are the L1's). One **fence-side candidate row**, measured here,
is offered in case the L1 prefers it — the mistake class is the round-44 fence's git-first order, not the
three content candidates:

```json
{"class": "fence-order", "source": ".ufo/waves/round-45/claims/control-c1-fence-r44.txt", "opened_round": 44, "status": "closed", "close": "round-45 R45FenceOwn: pure-filesystem legs before any git child (include/commondir/config.worktree/alternates scanned by text, .git above d by stat); counter contradicted=7 -> 0, READ modules f1/f4/f6/f10 -> clean opens=0", "blocker": null, "check": "python3 plans/round45_c1_verify.py --lane . | grep -qx 'CALIBRATION advertised=10 contradicted=0'", "note": "round 44's fence ran git discovery first, so git opened the include target (f10 opens=4), the FIFO include (f4 opens=1), the side gitdir (f1 opens=6) and the repo above d (f6 opens=3) while refusing them; reordering the legs, not adding refusals, is what made those four clean."}
```

## Host safety and tooling

- Every counter/fixture/probe run went through `claims/envelope.sh` (home read-only, `~/.cache` overlaid,
  content digest of `~/.local/bin` before/after): five runs, `unchanged` every time, no exit 4.
- Nothing was written to `~/.local/bin`, `/usr`, `/etc`, `$HOME` or the fleet root; the only writes are
  `$S/lane` (scratch clone), `$S/*.txt` and this report's subdirectory.
- No tool installed, upgraded or removed this wave (nothing was needed: stdlib + the host `git` 2.56.0,
  `/usr/bin/python3`, `/usr/bin/strace`, `/usr/bin/bwrap`).
- Scratch `/fast/scratch/hyaku/kengaku-r45/R45FenceOwn` removed with `plans/scratch_guard.py safe-rm`
  after the receipts were copied into this report's subdirectory.

## What the L1 should run after integration

1. Copy `.ufo/waves/round-45/w1/R45FenceOwn/fixture_fence.py` → `plans/fixture_fence.py` (nothing else
   changes; the fence is the subject, not a pinned input).
2. `python3 plans/round45_c1_verify.py --lane .` (or on a clean clone of the landing tip) and require the
   five frozen lines; the `FENCE … sha256=3b540e0d…` line confirms the copy.
3. Non-author review of the fence source rides admission (the spec's intent limit); limits 1, 2 and 3 above
   are the places to attack.

VERDICT: fixture-fence-primary-pass-yes-clean-10
