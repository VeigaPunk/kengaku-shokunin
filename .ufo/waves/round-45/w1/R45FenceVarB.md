# R45FenceVarB — round 45 wave 1: `plans/fixture_fence.py` variant B (executor)

## Deliverable

`fixture_fence.py` — independent third implementation, minimal-code, stdlib only (171 lines, sha256
`f2cd51d58c109ff4e543a2270049985670994985bfa86ebaa3c3e037192897ad`), written to the lane clone at
`/fast/scratch/hyaku/kengaku-r45/R45FenceVarB/lane/plans/fixture_fence.py` and copied for the L1 to
`.ufo/waves/round-45/w1/R45FenceVarB/fixture_fence.py`. Exposes `breach(d, argv, tool) -> str | None`,
one-line reasons, pure-filesystem legs before any git call.

## Design

Order inside `breach` (every earlier leg can refuse without touching a filesystem byte outside `d`):

1. **argv shape** (no I/O): order argv is exactly `["--lane", v, "--claims", v, "--receipt", v]`; anchor
   argv uses only `--lane v`, `--evidence-ref v`, `--verbose`; unknown tool refused.
2. **token resolution**: every argv token realpathed — absolute inside `d` or relative to it (`d` itself
   allowed); anything else refused. Covers `..`, absolute escapes, `{WORK}` tokens.
3. **static tree walk** (`os.walk`, lstat/readlink/realpath only — no `open` outside `d`, ever):
   escaping or unresolvable symlink refused (the walk descends into `.git`, so symlinked objects/configs
   inside a store are caught); `.git` symlink refused; `.git` non-directory refused (f1 gitdir file);
   `.git` directories recorded as repo markers (nested `.git` inside a store skipped); 200000-entry
   bound; `.git` present at the module build root `d.parent` refused (f6).
4. **per-.git store scan** (lstat + read of `.git/config*` inside `d` only): `commondir` (f7),
   `config.worktree` (f8), `objects/info/alternates` (f5), any `config*` that is not a regular file
   (FIFO/socket/dir refused unopened), `config*` > 1 MiB, and a case-insensitive multiline regex over
   the text refusing `[include`/`[includeIf` sections, `include.path` keys, `worktreeconfig` keys —
   before any git call is trusted (f4, f10 refused with `opens=0`).
5. **git legs** (run only when 1–4 pass; `GIT_CEILING_DIRECTORIES=d.parent`, `GIT_CONFIG_NOSYSTEM`,
   `GIT_CONFIG_GLOBAL=/dev/null`, the four executable-key `GIT_CONFIG_KEY_n` pins carried from
   round44_c1_verify.py:165-170, `stdin=DEVNULL`, 15 s timeout each): `--lane` `rev-parse
   --show-toplevel` + `--absolute-git-dir` — timeout, `rc != 0` (f9 bare repo, rc=128) or a resolved
   answer outside `d` (f2 `core.worktree` escape) is a breach; order `--claims`/`--receipt`
   `cat-file -t HEAD:path` — `rc != 0` or non-blob is a breach; per-repo `rev-parse` pair +
   `config --local --no-includes --get core.worktree` with the same rules.

## Evidence — counter run (run 2, pass)

Command (inside envelope):

```
envelope.sh "$S/env" /usr/bin/python3 .../plans/round45_c1_verify.py --lane "$S/lane" --work "$S/w" --jobs 8
```

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45FenceVarB/env /fast/scratch/hyaku/kengaku-r45/R45FenceVarB/env --bind /fast/scratch/hyaku/kengaku-r45/R45FenceVarB/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45FenceVarB/lane --work /fast/scratch/hyaku/kengaku-r45/R45FenceVarB/w --jobs 8
ENVELOPE start 23:34:28 cwd=/fast/scratch/hyaku/kengaku-r45/R45FenceVarB
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=f2cd51d58c109ff4e543a2270049985670994985bfa86ebaa3c3e037192897ad
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- lane/.git/config carries an include or worktreeConfig
FENCE-RUN refusal refusals45/f1_gitfile.py f1-gitdir-outside BREACH opens=0 -- .git is not a directory (gitdir redirect)
FENCE-RUN refusal refusals45/f2_deep.py f2-deep-worktree BREACH opens=0 -- --lane rev-parse --show-toplevel=/fast/scratch/.../fx/refusals45-f2_deep/wt
FENCE-RUN refusal refusals45/f3_abbrev.py f3-abbrev-tree-claims BREACH opens=0 -- order argv is not the contract shape: [...]
FENCE-RUN refusal refusals45/f4_fifo.py f4-fifo-include BREACH opens=0 -- lane/.git/config carries an include or worktreeConfig
FENCE-RUN refusal refusals45/f5_alternates.py f5-alternates-outside BREACH opens=0 -- lane/.git/objects/info/alternates present
FENCE-RUN refusal refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- .git at the module build root (repo above the fixture)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-accept BREACH opens=0 -- lane/.git/commondir present
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-reject BREACH opens=0 -- lane/.git/commondir present
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-anchor BREACH opens=0 -- lane/.git/commondir present
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-a BREACH opens=0 -- lane/.git/config.worktree present
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-b BREACH opens=0 -- lane/.git/config.worktree present
FENCE-RUN refusal refusals45/f9_nodescribe.py f9-bare-repo BREACH opens=0 -- --lane rev-parse --show-toplevel unanswerable (rc=128)
[104 honest FENCE-RUN lines omitted here, all ADMIT opens=0; full text in R45FenceVarB/counter-receipt.txt]
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
ENVELOPE end 23:34:36 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

Full verbatim output: `.ufo/waves/round-45/w1/R45FenceVarB/counter-receipt.txt`
(sha256 `af7cc3ad04eeebe8e99b461c1b593dc0dbdbb0102117dc14273e16d9224a3643`, 11571 B).

## Iteration history (both runs reported)

- **Run 1** (23:33:22–23:33:43, envelope `unchanged`, exit 1, kept as
  `R45FenceVarB/run1-buggy-regex.txt`): `REFUSALS clean=8 leaked=1 read=1`, `contradicted=2`, FAIL.
  Cause located: `_INCLUDE_RE` lacked `re.M`, so `^` never matched `[include]` past byte 0 —
  f10 was admitted outright and f4 was refused only by the git-probe timeout after its child opened
  the FIFO include target. One-flag fix; no other change. This is also the held-out lesson: a fence
  that detects a FIFO include only through the git timeout is a `READ`, not `clean`.
- **Run 2** (above): pass.

## Limits

- The ancestor `.git` scan checks exactly `d.parent` (the frozen "module build root"); repos higher in
  the host tree are invisible to the fence but unreachable by its git calls, which are all bounded by
  `GIT_CEILING_DIRECTORIES=d.parent`. If the harness ever placed fixture dirs deeper than one level
  below the build root, the check would not cover intermediate ancestors.
- The include surface scan is textual over `.git/config*` only (not `.git/worktrees/*/config.worktree`
  or a `commondir`-pointed store's config — but `commondir` itself is refused outright, which covers
  both). It over-refuses odd spellings (e.g. a comment line `# [include]`) rather than risk
  under-refusing; no honest fixture is affected.
- Every `config*` under `.git` that is not a plain regular file is refused unopened — correct for a
  FIFO (no blocking open) but also refuses e.g. a `config.bak` directory, an over-refuse.
- `--claims`/`--receipt`/`--evidence-ref` values are resolved as filesystem paths under `d` *and* (for
  order) required to be committed blobs at HEAD — stricter than the round-44 fence, which left a
  missing path to the tool's own setup error. A held-out honest module that needs `rc != 0` from
  `cat-file` would be refused.
- `cat-file` / `rev-parse` `rc != 0` is always a breach, including the "no repo" case the r44
  `lane_breach` deliberately left to the tool — a fixture whose `--lane` names no repo is refused
  here, not deferred.
- Blocking opens of paths *inside* `d` (e.g. a FIFO `HEAD`) are not counted by the counter's rule;
  they still cost up to the 15 s per-probe timeout, and a pathological fixture could burn the
  harness's 120 s `FENCE_TIMEOUT` into `HUNG` — the 200000-entry bound does not cap per-open latency.
- Git env pins four config keys (carried from the round-44 counter), not the whole key space;
  `GIT_DIR`/`GIT_WORK_TREE` cannot be injected because `_git` replaces the whole environment.
- A `.git` file/symlink/redirect *inside* a `.git` store subtree (`in_store`) is tolerated rather than
  probed — discovery never descends there, and `commondir`/`gitdir` redirection at the top level is
  already refused.
- Not exercised: held-out modules authored by wave critic seats against this fence (per the freeze,
  that is wave-2 work, reported not predicated).

## Files

- `R45FenceVarB/fixture_fence.py` — the module for L1 selection (sha256 `f2cd51d5…97ad`, 171 lines).
- `R45FenceVarB/counter-receipt.txt` — verbatim run-2 output incl. ENVELOPE lines.
- `R45FenceVarB/run1-buggy-regex.txt` — verbatim run-1 output (the `re.M` defect, failed).

No tools installed; nothing written outside this report dir and my scratch (scratch removed before
finish).

VERDICT: fixture-fence-variant-b-pass-yes-clean-10
