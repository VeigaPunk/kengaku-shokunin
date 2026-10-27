# R45MutParser — round-45 C1 instrument mutation probe

## Baseline

Ran the pristine instrument through the required envelope:

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45MutParser/env /fast/scratch/hyaku/kengaku-r45/R45MutParser/env --bind /fast/scratch/hyaku/kengaku-r45/R45MutParser/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --work /fast/scratch/hyaku/kengaku-r45/R45MutParser --jobs 1
ENVELOPE start 23:26:58 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py absent
REFUSALS total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=10
PREDICATE C1 fail
ENVELOPE end 23:27:11 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

Actual baseline behavior is the frozen `nothing` control: the subject fixture fence is absent, the instrument substitutes a raising stub, and all ten refusal modules leak while honest fixtures classify as refused. This baseline failure is not a passing-oracle control for the requested r44-fence comparison.

## Mutants and detector status

| Mutant point | Result | Why |
|---|---|---|
| OPEN_RE / DONE_RE / UNFINISHED / RESUMED parsing | Not run (inconclusive) | A baseline verdict exists, but no r44-fence control run was established. |
| outside-open region (`scratch` vs `d`) | Not run (inconclusive) | Same missing r44-fence control. |
| per-module verdict roll-up | Not run (inconclusive) | Same missing r44-fence control. |
| `run_fence` sandbox argv | Not run (inconclusive) | Same missing r44-fence control. |
| HONEST / REFUSALS accounting | Not run (inconclusive) | Same missing r44-fence control. |
| `main` `good` conjunction | Not run (inconclusive) | Same missing r44-fence control. |

No mutant verdicts are claimed. The task's requested comparator is specifically the r44-fence control, whereas the observed baseline used the instrument's absent-fence fallback; counting any mutant against that output would not measure the requested control. Baseline source hash observed before probing: `7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d` (`sha256sum plans/round45_c1_verify.py`). No source mutations were made.

VERDICT: instrument-mutants-caught-0/0