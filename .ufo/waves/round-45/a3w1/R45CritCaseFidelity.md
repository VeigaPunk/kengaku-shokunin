# R45CritCaseFidelity — round 45 a3w1

## Scope and measured runs

Measured lane `master` at `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`; output: that hash). Probe/dry hashes match the C2 counter pins: `sha256sum plans/password_recovery_probe.py corpus/evidence/round45/password-recovery-dry-cases-freeze.txt ...` output `9363e03e...b4ab` and `46036abe...aabb` (see `plans/round45_c2_verify.py:90-93`).

I ran an independent hostile inspector that imports only the frozen case recipes, stages each captured `setup.sh` plus recipe in bwrap, and dumps `/app` state, output bytes/line shapes, seed-image size/offsets, and directory-read exception. Full receipt: `.ufo/waves/round-45/a3w1/R45CritCaseFidelity/inspect-receipt.txt`; concise extraction: `.../summary-receipt.txt`.

Measured command (the envelope-wrapped inspector):

```sh
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
  /fast/scratch/hyaku/kengaku-r45/R45CritCaseFidelity/env \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45CritCaseFidelity/inspect_endstate.py \
  /fast/scratch/hyaku/kengaku-r45/R45CritCaseFidelity/inspect-work
```

Its output included `cases=16 stage_fail=0 dump_fail=0` and all 16 staged image+recipe states; envelope ended `exit=0 ... unchanged` (`inspect-receipt.txt:19`). The follow-up extraction command read that receipt and reported the specific outputs below; its envelope ended `exit=0 ... unchanged` (`summary-receipt.txt:11`). The only initial inspector run had a parser bug in my extra image walk and was not used as evidence; the corrected run above succeeded for every case.

## Findings

1. **`oracle-solve-sh` overstates its emitted guess set (recipe description defect).** The frozen case description says “a handful of guesses” (`plans/password_recovery_probe.py:114-117`; dry freeze line 11; original probe receipt line 7). Measured end state is a 24-byte file with exactly one nonempty answer line: `oracle-solve-sh (24, 1, [...])` from the summary extraction, and raw inspector JSON says `head='8XDP5Q2RT9ZK7VB3BV4WW54\n'`, `n_answer_lines=1` (`inspect-receipt.txt:4`). The recipe does recover and pass, but does not build the described handful.

2. **`decoys-1000` does not shuffle its guesses (recipe description defect).** The frozen description says “plus 1000 wrong guesses, shuffled” (`password_recovery_probe.py:156-160`; dry freeze line 22; receipt line 18). The recipe deterministically prints the answer first, then `seq 1 1000 | sed 's/^/WRONGGUESS/'`; measured output starts with the answer and `WRONGGUESS1`, `WRONGGUESS2`, … and ends `WRONGGUESS996` through `WRONGGUESS1000`; it contains 1002 newline-split entries (the answer, 1000 decoys, and trailing empty split entry). Exact summary output: `decoys-1000 (1002, '8XDP...WW54\\nWRONGGUESS1\\n...', 'GUESS995\\nWRONGGUESS996\\n...WRONGGUESS1000\\n')` (`summary-receipt.txt:7`). Its pass result is still correct; the claimed shuffle is not.

3. **`wrong-23` is not “format-conforming” (description defect).** The frozen description calls it “one 23-char uppercase/digit guess, format-conforming, wrong content” (`password_recovery_probe.py:139-141`; dry freeze line 17; receipt line 13). Measured first output line has `len=23`, `charset=true`, but `prefix8XD=false` and `suffixW54=false` (`summary-receipt.txt:8`; recipe literal is 23 `Z`s). Its frozen `prefix,suffix` tags are right; it is the prose claim that is false.

## Tags / map-label impact

`dir-state` really is a directory at the graded path, and the independent sandbox read raised `IsADirectoryError`; measured summary: `dir-state ('dir', 'IsADirectoryError')` (`summary-receipt.txt:9`). This exactly confirms the frozen receipt’s `error=IsADirectoryError` (`password-recovery-probe.txt:11`) and C2 mechanism description (`tb2-password-recovery-grader.md:102,154-156`).

Two omitted tags are worth noting but **do not change a map label**: `dir-state` reads `PW` from public `/pub/test_outputs.py` in its recipe (`password_recovery_probe.py:130-134`) yet lacks `forensic`; `constant-joined` has no exact answer line (`n_answer_lines=0`, 66-character concatenated line; `summary-receipt.txt:6`) yet lacks `recover`. Under the frozen map's own rule, adding either tag contributes an observed failure; it cannot change the derived label (the forensic row already has pass and fail cases, and recover remains all-fail). These are not counted as label-changing defects. I found no assigned tag that is demonstrably false under the map’s stated semantics.

## Seed-fidelity boundary

The captured seed creates a 4 MiB image with `dd ... bs=1M count=4` (`tb2-password-recovery/setup.sh:21-23`), then places fragments at 1 and 3 MiB (`:35-37`). The probe instead binds a 65,536-byte zero file as `/dev/urandom` (`password_recovery_probe.py:246`, `:219-221`). Measured image size is `3,145,851` bytes, with the two fragment windows present at the stated offsets (`summary-receipt.txt:10`; first offset begins `504b0304`, second `4b375642...`). Thus this is not the real 4 MiB random-noise seed; the C2 entry explicitly discloses the substituted noise (`tb2-password-recovery-grader.md:205-206`). The recipes were built successfully against the probe’s documented deterministic surrogate, so I treat this as a disclosed test-boundary limitation, not an additional recipe claim defect. It does mean the oracle case does not establish behavior against every random 4 MiB seed.

## Count

Three case-description fidelity defects above; **zero label-changing tag defects**. The 16 recipes all staged successfully in the corrected hostile run, and `dir-state`’s kernel behavior matches the receipt.

VERDICT: case-fidelity-defects-3-label-changing-0
