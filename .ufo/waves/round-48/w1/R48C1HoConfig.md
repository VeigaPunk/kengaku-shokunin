# R48C1HoConfig — benign config diversity

Axes named: **calibration (R48-C1)**.

## Fixture class and expected disposition

Propose one novel honest fixture class, `git-config-benign-diversity`: an ordinary repository initialized and committed inside the fixture directory, with a plain `.git/config` containing the following additions to the normal `[core]` entries:

```ini
[core]
    autocrlf = false
    safecrlf = true
[user]
    name = Fixture Author
    email = fixture@example.invalid
[init]
    defaultBranch = main
```

These keys/sections are ordinary, non-include configuration; the values do not name paths or request external config reads. Build the repository wholly inside its fixture directory and keep all config values non-path-valued. **Expected v3 classification:** honest fixture; the repaired fence must admit it with no traced outside access (`touches=0`, no READ), and it counts in `HONEST admitted`, not `BENIGN-ADMIT`. The `BENIGN-ADMIT` bucket is for held-out hostile modules admitted without observed outside access, per frozen delta (b). On the base fence, refusal at config parsing is expected: `autocrlf` is not in its frozen key allowlist, and `[user]`/`[init]` are not in its frozen section allowlist. This is the over-refusal signal, not evidence of a leak.

This class is a proposal for the wave-1 critic-authored honest population; I did not add fixture code to the lane or claim its stage-2 inclusion. The frozen claims require critic fixtures to be authored against the base fence description, not a repaired fence.

## Freeze and measurement boundary

Verified the committed lane tree at the frozen base: `a543d92083557dd9b33ee674e9b99b03411f80af`, whose subject is `round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter)`. The claims file at that revision defines the C1 counter, honest population, classification, and kill rule; stage 2 is still required to pin its counter, fixture population, and literals before any scored measurement. **No scored counter/probe execution was run.** No fixture was built or evaluated, so the expected behavior above is based on the frozen parser and claim, not measured results.

## Evidence / sources

Sources opened on 2026-10-27; no external URL sources were opened.

- `plans/round-48-claims.md` at frozen revision `a543d92083557dd9b33ee674e9b99b03411f80af`: “a fixture admitted with `touches=0` is reported as `BENIGN-ADMIT` and counted separately, never as a leak” (frozen C1 delta b). It also says critic honest fixtures are authored against the base fence description.
- `plans/fixture_fence.py` at base revision `0f77f9b27931b3c76b3d095fc0fa70edb79556d9`: “`CFG_SECTIONS = {"core"}`”; the parser rejects any other section and any key not in `CFG_KEYS`. Existing keys are repositoryformatversion, filemode, bare, logallrefupdates, ignorecase, precomposeunicode, and symlinks.
- `corpus/lessons/round-46-verifier-spotcheck.md`, opened from the lane at frozen revision: “9/9 novel honest fixtures refused” (C1 routed defect).

## Exact commands and observed outputs

1. `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1HoConfig && cd /fast/scratch/hyaku/kengaku-r48/R48C1HoConfig && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1HoConfig && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -1 a543d92083557dd9b33ee674e9b99b03411f80af && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --short | head -20` → `a543d92 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter)`; status showed `?? .ufo/waves/round-48/claims/`, `?? .ufo/waves/round-48/w1.ready.partial`, and `?? .ufo/waves/round-48/w1/`.
2. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane && cd lane && git checkout -q a543d92083557dd9b33ee674e9b99b03411f80af && git rev-parse HEAD && git log --oneline -1 0f77f9b27931b3c76b3d095fc0fa70edb79556d9` → clone succeeded; `HEAD` was `a543d92083557dd9b33ee674e9b99b03411f80af`; base-fence revision was `0f77f9b hyaku run9 wrap-up: round-47 spec state for inheritance`.
3. `ls .ufo/waves/round-46/w2/ | grep -i -E 'honest|argv|paths' && ls plans/battery42 plans/refusals46 | head -30` → listed `R46W2C1HoArgv.md`, `R46W2C1HoHonest.md`, `R46W2C1HoPaths.md` and existing battery/refusal fixtures.
4. `grep -n "_config\|CFG_SECTIONS\|CFG_KEYS" plans/fixture_fence.py | head` → locations `67:CFG_SECTIONS = {"core"}`, `68:CFG_KEYS = {`, `226:def _config(p, label):`, and parser references at 251, 258.
5. Before any clone-tree write, `D=/fast/scratch/hyaku/kengaku-r48/R48C1HoConfig/lane; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" && git -C "$D" rev-parse HEAD && git -C "$D" show -s --format='%H %s' a543d92083557dd9b33ee674e9b99b03411f80af && git -C "$D" status --short` → root assertion succeeded; both revisions were `a543d92083557dd9b33ee674e9b99b03411f80af`; status was empty.

## Limits and verdict

No fixture build, fence call, counter run, repair evaluation, or admission judgment was performed. The candidate’s exact construction/run behavior remains unmeasured; stage-2 freeze and later scored evaluation belong to the integration workflow.

VERDICT: **HONEST CONFIG-DIVERSITY CLASS PROPOSED; EXPECT ADMIT UNDER FROZEN V3 CLASSIFICATION; BASE-FENCE REFUSAL IS EXPECTED OVER-REFUSAL. NO SCORED RUN.**
