# R45HoArgvEnv — argv/environment fence probe

- Lane measured: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C "$S/lane" rev-parse HEAD`).
- Read the landed `plans/fixture_fence.py`, C1 `build_module`/`run_fence`, and `round44_c1_verify.py` `Ctx`/`build_module_child`/`PIN_CHECK_ENV` before probing.
- Held-out module: `.ufo/waves/round-45/a3w1/R45HoArgvEnv/argv_env.py`, SHA-256 `1656db9c1ffdf3c6b3474436cd2b2d27b82a6a1d2f6786fe4c81526c7f8a4dcf`.
- Module has three `order` fixtures: a `{WORK}`-prefixed outside lane, NUL in lane, and an extra argv token. The module is just one held-out module; the result below counts a module as admitted if its fixture decision is `ADMIT` or `ERROR`, matching C1's `n_admit` logic (`round45_c1_verify.py:289-296`).

## Measured run

Command (inside required envelope):

```sh
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S" /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoArgvEnv/probe.py "$S/lane" "$S/env/probe-root" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoArgvEnv/argv_env.py
```

Actual output:

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv /fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv --bind /fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoArgvEnv/probe.py /fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv/lane /fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv/env/probe-root /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoArgvEnv/argv_env.py
ENVELOPE start 00:34:57 cwd=/home/vgpnk/Projects/shokunin
LANE fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc
RESULT argv-placeholder-lane-escape BREACH opens=0 reason=--lane resolves outside the fixture
RESULT argv-nul-lane ERROR opens=0 reason=ValueError: lstat: embedded null character in path
RESULT argv-extra-token BREACH opens=0 reason=order argv is not the contract shape ['--lane', '--claims', '--receipt']
ENVELOPE end 00:34:59 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

The NUL token raises uncaught `ValueError` in the fence instead of returning a refusal; C1 treats `ERROR` as admitted. The other argv cases were refused. All three runs reported `opens=0`, so there is no outside-open finding. The fixed environment in `round44_c1_verify.py` `Runner.run` and C1 `run_fence` is a whitelist rather than inherited process environment; `PIN_CHECK_ENV` is likewise fixed (`round44_c1_verify.py:172`). No GIT_DIR/GIT_WORK_TREE injection was attempted because the counter does not pass the ambient environment through.

There were two non-evidentiary setup attempts, both in scratch: first the driver had not created `harness.py` and each result was `ERROR ... can't open file .../harness.py`; after fixing that, a stale probe root caused `FileExistsError`. The corrected, clean-root run above is the measured result. The scratch root was removed with `scratch_guard.py safe-rm`; tool output: `DELETE path=/fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv resolved=/fast/scratch/hyaku/kengaku-r45/R45HoArgvEnv bytes=547758691 size=522.4MiB`.

VERDICT: argvenv-modules-1-admitted-1-read-0
