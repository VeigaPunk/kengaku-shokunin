# F40RevBatLRefuse — non-author honesty review of `plans/battery40/l_refuse.py`

Round 40 wave 2 (FALSIFY), 2026-10-26. Target: `plans/battery40/l_refuse.py` (targets L01, L11, L21 of
`plans/round40_c1_verify.py`), measured at lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
Reviewer is not an author of the module or the counter.

## Method

Scratch clone `S=/fast/scratch/hyaku/kengaku-r40/F40RevBatLRefuse`, `git clone --no-local` of the lane,
`checkout ec1005a2…`; `git -C "$S/lane" rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r40/F40RevBatLRefuse/lane`.
Battery dir `$S/bat` held exactly one file (`ls` → `l_refuse.py`); `cmp` against the lane copy → `COPY-IDENTICAL`.
Run (single command, HOST-SAFETY wrapper as ruled):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  python3 "$S/lane/plans/round40_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat" --only L01,L11,L21 --work "$S/w"
```

Output (rc=0, wall 25.6 s), verbatim:

```
PINS total=3 mismatched=0
FIXTURE l_refuse-source-not-a-repo tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-work-lane-exists tool=ledger expect=error declared=- observed_rc=2 observed=- ok
FIXTURE l_refuse-stale-pin-ref tool=ledger expect=error declared=- observed_rc=2 observed=- ok
MUTANT L01 ledger error killed by=l_refuse-source-not-a-repo -- plans/ledger_tip.py:23-25 'Exit codes are the registry row's contract (SKILL.md:581): ...
MUTANT L11 ledger error killed by=l_refuse-work-lane-exists -- plans/ledger_tip.py:58 'The clone is created at <work>/lane (must not exist)'
MUTANT L21 ledger error killed by=l_refuse-stale-pin-ref -- plans/ledger_tip.py:44-45 'REFUSE stale pin ref … (exit 2) the ref exists but resolves to
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

The `adv` cells quote real pinned-tool sentences: `ledger_tip.py:23` "Exit codes are the registry row's
contract (SKILL.md:581)", `:44` "REFUSE stale pin ref … (exit 2)", `:58` "The clone is created at
&lt;work&gt;/lane (must not exist)" (grep -n on the scratch clone). The mutant `old` strings match the pinned
tool once each (`invalid=0` implies `src.count(old)==1`): `raise SystemExit(2)` at `ledger_tip.py:94` (the
only `SystemExit` in the file, `grep -c` → 1), `if dest.exists():` at `:119`, `if rev and rev != tip:` at
`:159` preceding `refuse(f"stale pin ref: …` at `:160`.

## Wave-1 attack vectors, checked line by line

| Vector (wave-1 seat) | In `l_refuse.py`? | Evidence |
|---|---|---|
| Read tool/own program text at run time (A1) | No | The module never opens a file; only `write_text` at `l_refuse.py:23`. Tool text reaches runs solely via the harness's pinned slots. |
| Write outside d — HOME/PATH dirs/other fixture dirs (A2, Sentinel) | No | Build env has `HOME=/nonexistent` (`round40_c1_verify.py` `Ctx.ENV`); all writes are `plain/README.md` (`:23`), `ctx.clone(d/…)` (`:38`, `:52`), `ctx.git` (`:53-54`) — `Ctx._inside` rejects any path outside the fixture root, and post-run fingerprints were unchanged (`tampered=0`). |
| Relative argv tokens / symlinks out of d (A4) | No | All argv paths absolute inside d or the sanctioned `{WORK}`/`{WORK:lane}` tokens (dumped below); `find "$S/inspect" -type l` → `0`; harness `path_ok` re-validates absolute tokens. |
| `.lock`/`.git/index` fingerprint skips (A5) | No | `find "$S/inspect" -name '*.lock' -not -path '*/.git/*'` → `0`; nothing is written outside d at all, so the skip set is never load-bearing. |
| Phase detection (Sentinel F1-F6 class) | No | No `/proc`, env, run-count, or harness introspection; harness token scan printed no `SIDECHANNEL` line (`sidechannel=0`). |
| Bare-string `build()` return | No | All three builders return lists of str (`l_refuse.py:24`, `:39`, `:55`). |

## Built fixture trees (inspect script re-using the harness `Ctx` + the module's own builders)

`python3 "$S/inspect_build.py"` (loads `round40_c1_verify.Ctx` and `battery40/l_refuse.py`, builds all three
fixtures the same way `build_module_child` does):

- `l_refuse-source-not-a-repo`: argv `['--source', '…/f000/plain', '--work', '{WORK}']`; tree = `plain/README.md`
  (17 B) only; fingerprint `475e808486130304…`.
- `l_refuse-work-lane-exists`: argv `['--source', '…/f001/src', '--work', '{WORK:lane}']`; `src/` is a
  `ctx.clone` of the lane. `diff -r --exclude=.git --exclude=__pycache__ f001/src "$S/lane"` →
  `IDENTICAL-f001-worktree`; `git -C f001/src rev-parse HEAD` → `ec1005a2…`; `status --porcelain | wc -l` → `0`.
  (A first diff flagged `plans/__pycache__` present only in my scratch lane clone — an artifact of my own
  inspect script importing the harness without `PYTHONDONTWRITEBYTECODE`, not of the battery; the battery run
  itself sets `PYTHONDONTWRITEBYTECODE=1` in both build and run envs.)
- `l_refuse-stale-pin-ref`: `diff -r --exclude=.git --exclude=__pycache__ f002/lane "$S/lane"` →
  `IDENTICAL-f002-worktree`; `git -C f002/lane rev-parse HEAD refs/heads/master HEAD~6` →
  `ec1005a2a28b…`, `013938e45d4…`, `013938e45d4…` — i.e. detached HEAD at the audited tip with
  `refs/heads/master` rewound exactly six commits (`git log --oneline -7`: `ec1005a` … `013938e`), which is
  precisely the input `audit_pin_refs` refuses (`ledger_tip.py:159-160`).

## Per-fixture verdicts

1. `l_refuse-source-not-a-repo` (`l_refuse.py:36-40`, fixture `:59-60`) — **honest**. Builds a plain
   non-repo dir; `clone_lane` refuses at `ledger_tip.py:116-117` before any clone, exhibiting the exit-code
   sentence L01 relabels (`raise SystemExit(2)` `:94` → `1`). Reference observed rc=2, empty class set, as
   declared (`defects=[]`; refusals buffer row lines, so `observed=-` is the honest expectation, not a dodge).
2. `l_refuse-work-lane-exists` (`l_refuse.py:44-48`, `:61-62`) — **honest**. `{WORK:lane}` is
   harness-created (fresh empty `lane` dir outside d per run), so the reference hits
   `if dest.exists(): refuse` (`ledger_tip.py:119`) — the exact line L11 disables; the mutant clone then
   proceeds into the existing empty dir. Fixture side writes only `f001/src` inside d.
3. `l_refuse-stale-pin-ref` (`l_refuse.py:50-55`, `:63-64`) — **honest**. Detach + `branch -f master
   HEAD~6` inside the clone makes `rev != tip` true (`ledger_tip.py:159`), the exact condition L21 disables;
   the git mutation is visible to the fingerprint (`.git/refs/heads/master` is fingerprinted; only
   `.git/index` is skipped). No symlink, no out-of-d path, `{WORK}` unused.

Each mutant's sole kill is the fixture that reaches its code path; L01 is additionally exhibited by the other
two refusals, which the module states openly (`l_refuse.py:17-19`) instead of claiming uniqueness.

## Findings

- Minor (docstring wording, not fixture dishonesty): `l_refuse.py:27-29` says the L01 witness "is the only
  one of the three whose refusal happens before any clone" — but the L11 witness also refuses before any
  clone (`dest.exists()` check at `ledger_tip.py:119` precedes the clone subprocess at `:121-124`). The
  per-fixture honesty verdicts are unaffected; only the exclusivity claim is wrong as written.
- No dishonest fixture, no wave-1 vector, no undeclared reliance found. The frozen-predicate line for this
  module reproduces exactly (`killed=3 survived=0 invalid=0 null_detected=0`, `tampered=0 sidechannel=0`,
  `PINS-AFTER mismatched=0`) on a clean tip clone.

## Residual risk / verification gaps

- I ran the `--only L01,L11,L21` dev subset, not the full 21-mutant battery; the landing measurement
  (`.ufo/waves/round-40/integrate/measure-final.txt`) covers the full predicate and was not re-measured here.
- `classes()` reads stdout only; a refusal's stderr `REFUSE` line is not class-checked — consistent with the
  contract (`defects` = row-line classes), not a gap introduced by this module.
- The L11/L21 mutant runs evaluate the real ledger (live rows included) inside the harness sandbox; their
  exact mutant exit codes (0 vs 1) are not printed by the counter — only the declared-direction kill is,
  which is all the calibration claims.

VERDICT: battery-l_refuse-honest-3/3
