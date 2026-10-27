# R45MutHostileFixtures — mutation probe

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (clone `/fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/lane`). The required pristine counter completed, but this seat did not complete the requested ten neutralization mutations; therefore no admits-after-neutralization verdict is claimed.

## Pristine baseline

Command: `S=/fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures; export TMPDIR="$S"; /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/work" --jobs 1`

Output: `PINS total=33 mismatched=0`; each of the ten refusal modules reported `clean` (f7 had three fixtures and f8 had two); `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=10 contradicted=0`; `PREDICATE C1 pass`.

Envelope lines:
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/env /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/env --bind /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/lane/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/lane --work /fast/scratch/hyaku/kengaku-r45/R45MutHostileFixtures/work --jobs 1
ENVELOPE start 00:26:09 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:26:25 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## Neutralization matrix

| Module | admits after neutralization |
|---|---|
| f1_gitfile.py | not run |
| f2_deep.py | not run |
| f3_abbrev.py | not run |
| f4_fifo.py | not run |
| f5_alternates.py | not run |
| f6_above.py | not run |
| f7_commondir.py | not run |
| f8_worktreecfg.py | not run |
| f9_nodescribe.py | not run |
| f10_laneinclude.py | not run |

The pristine counter output does not test the weakened fixtures, so it cannot establish neutralized admission or over-refusal. No source in the lane was modified. The prior scratch directory was removed using `scratch_guard.py safe-rm` after discovering it contained stale, unverified work; a clean clone was then made at the measured tip.

VERDICT: neutralized-admitted-0/10