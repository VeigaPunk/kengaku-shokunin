# R45FenceVarA — independent fixture_fence.py (variant A: collect-first)

kengaku round 45, wave 1, C1 seat. Deliverable for the L1: `.ufo/waves/round-45/w1/R45FenceVarA/fixture_fence.py`
(sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`, 13,054 B), developed and measured
in a `--shared` clone at `/fast/scratch/hyaku/kengaku-r45/R45FenceVarA/lane`. Receipt:
`.ufo/waves/round-45/w1/R45FenceVarA/c1-counter-run.txt` (full 136-line counter transcript).

## Axes

calibration (does `contradicted` reach 0 — all 10 refusal fixtures refused, zero outside opens) and
operability (do the 104 honest fixtures still admit — a fence that refuses everything fails HONEST).

## Design (independent of the r44 fence's leg chain)

One **collection pass** gathers every filesystem fact before any git child can exist:

1. argv shape — order exactly `--lane V --claims V --receipt V`; anchor only `--lane V`, `--evidence-ref V`,
   `--verbose` (no abbreviation, no `--opt=`).
2. every argv value resolved against `d` must stay inside it (`{WORK}` placeholders left to the harness).
3. `.git` above `d` — ancestors from `d.parent` up to and including the module build root (`d.parent`):
   `lexists(.git)` → breach (covers f6 without git).
4. one `os.walk(d)`: `.git` FILE → breach (f1); `.git` symlink-dir → breach; any other symlink resolving
   outside `d` → breach; FIFO/socket/device under `d` → breach; entry cap 200,000; collects every dir
   holding a real `.git` dir (repo cap 64).
5. per collected repo, judged from bytes/metadata only: `.git/commondir` (f7), `.git/objects/info/alternates`
   (f5), and a raw scan of every `.git/config*`: any `[include`/`[includeIf` section (f4, f10 — the FIFO and
   the regular include are refused before git could ever open the target), `extensions.worktreeConfig` (f8),
   `core.bare` (f9, statically), `core.worktree` resolving off the repo dir (f2, statically).

**Git legs second** (only reached when the tree is proven self-contained): `_git` = fixed system PATH, empty
HOME, `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null`, the four executable-key pins, 30 s timeout,
`stdin=DEVNULL`, and `GIT_CEILING_DIRECTORIES=d.parent` on every call. For each collected repo and the
`--lane` dir (if a directory): `rev-parse --show-toplevel` (collected repos must equal their dir; the lane
must be inside d) and `--absolute-git-dir` must resolve inside d; `core.worktree` via
`--local --no-includes`; `rc != 0` from a store/lane probe = breach, never "clean" (f9 also fails here).
Order: `--claims`/`--receipt` must be blobs at HEAD (non-blob at rc 0 → breach).

## Result — counter run inside the envelope (exit 0)

Command: `envelope.sh $S/env /usr/bin/python3 …/plans/round45_c1_verify.py --lane $S/lane --work $S/w`

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45FenceVarA/env /fast/scratch/hyaku/kengaku-r45/R45FenceVarA/env --bind /fast/scratch/hyaku/kengaku-r45/R45FenceVarA/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45FenceVarA/lane --work /fast/scratch/hyaku/kengaku-r45/R45FenceVarA/w
ENVELOPE start 23:34:17 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f1_gitfile.py f1-gitdir-outside BREACH opens=0 -- .git/.git is a file (gitdir redirect), not a directory
FENCE-RUN refusal refusals45/f2_deep.py f2-deep-worktree BREACH opens=0 -- x/y/z/r/.git/config sets core.worktree=/fast/…/refusals45-f2_deep/wt
FENCE-RUN refusal refusals45/f3_abbrev.py f3-abbrev-tree-claims BREACH opens=0 -- order argv is not the contract shape ['--lane', '--claims', '--receipt']
FENCE-RUN refusal refusals45/f4_fifo.py f4-fifo-include BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f5_alternates.py f5-alternates-outside BREACH opens=0 -- lane/.git/objects/info/alternates present
FENCE-RUN refusal refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- .git exists at /fast/…/refusals45-f6_above above the fixture
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-accept BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-reject BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-anchor BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-a BREACH opens=0 -- lane/.git/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-b BREACH opens=0 -- lane/.git/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f9_nodescribe.py f9-bare-repo BREACH opens=0 -- lane/.git/config sets core.bare
… (104 honest FENCE-RUN lines, all `ADMIT opens=0`) …
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 23:34:24 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

Every refusal fixture was killed by a pure-filesystem leg — f9's `core.bare` and f2's `core.worktree` were
even refused statically before the git probes that would also have caught them. Zero outside opens on all
114 runs.

## Limits of this variant

- The config scan is a line lexer, not git's parser: an include smuggled through a line continuation or a
  weird-but-legal quoting trick could slip the `[include` regex — but the include *file itself* would still
  need `include.path` honoured by git, and `extensions.worktreeConfig`/`core.bare`/`core.worktree` are also
  refused, so the residual is a config containing only an `[include*]` section the regex misses. Non-author
  review (non-vacuity note in the freeze) rides admission, same as the r44 fence's.
- `core.worktree`/`core.bare`/`extensions.worktreeConfig` are refused outright — a module honestly needing a
  relocated worktree or a bare-store fixture would be refused (no battery fixture needs either).
- Special files (FIFO/socket/device) under `d` are refused outright; a fixture whose *test* needs an in-`d`
  FIFO would fail HONEST (none do).
- `.git` above `d` is checked only to the module build root (`d.parent`); the git-call ceiling enforces the
  same bound, so a repo higher up is unreachable by design, but an ancestor `.git` above the build root in a
  different embedding would be invisible.
- `--claims`/`--receipt` non-blob is judged by `cat-file` rc==0 only (r44 semantics): a path missing at HEAD
  stays the tool's own setup error; a repo too broken for `cat-file` is already refused by the probes.
- All option *values* are required to resolve inside `d`; a future tool option whose value is legitimately a
  non-path string that happens to resolve outside would be refused (contract-shape argv only today).
- Held-out modules: any vector not on the f1–f10 list (e.g. `core.hooksPath` in config — exec pins only
  cover the four env-pinned keys; hooksPath is pinned via env so safe here — or a `.git` dir whose HEAD
  points sideways but stays inside d) is out of scope for the frozen predicate and left for the held-out wave.

## Tooling

No installs or upgrades performed; stock `/usr/bin/{python3,bwrap,strace,git}` sufficed.

VERDICT: fixture-fence-variant-a-pass-yes-clean-10
