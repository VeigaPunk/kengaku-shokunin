# R46MutC2Gate — C2 mutation probe

## Setup and pristine detector

Scratch clone: `/fast/scratch/hyaku/kengaku-r46/R46MutC2Gate/lane`, cloned with `git clone -q --shared` then checked out at `64ba8385ea10af1b78d367dcb242b92d97062af7`; the two frozen tools were copied in. The pristine tool hashes were `anchor_line_check.py` `35d02dc55393bea18787e35cc2827cbab65f2d645b81a3c1946722065a4fdedf` and `round46_c2_verify.py` `2042d873459b38444db429121871d91f4b5f9650b38789fa7d49a0b9d8790f7a` (sha256sum). Pristine control/detector command: `.../claims/envelope.sh "$S/env-base" python3 "$S/lane/plans/round46_c2_verify.py" --lane "$S/lane" --work "$S/work-base"`; result: `PINS total=3 mismatched=0`, A live=8, B disagree=6, C bad=4 errata=0/5, D selftest exit=0, `checks=4 defects=3`, `PREDICATE C2 fail`, exit 1. Envelope: `ENVELOPE start 02:06:07`; end `02:06:09 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

The baseline is a deliberately failing do-nothing fixture control. Therefore verifier failure alone is NOT evidence of mutant kill; a change is marked killed only where the detector has an independently observed expected-vs-mutant distinction. Tool mutants changed scratch copies only; each was reset from the frozen bytes before mutation. Detector invocations used the required envelope, with unchanged local-bin digest on every run.

## Mutant table

| Mutant (single edit) | Detector result / observed output | Verdict |
|---|---|---|
| Drop anchor line check | `anchor_line_check.py --selftest`: exit 0, `SELFTEST pass`; verifier: `PINS total=3 mismatched=1 first=plans/anchor_line_check.py`, predicate fail. Pin catches mutant, although selftest did not. | killed (pin) |
| Off-by-one line index (`n-1` to `n`) | selftest exit 1, `SELFTEST GREEN ... FAIL` (expected rc=0, got 1); verifier pin mismatch. | killed (selftest) |
| Range `<=` to `<` | selftest exit 0, `SELFTEST pass`; verifier pin mismatch. No selftest distinction for this fixture. | killed (pin) |
| Remove words check | selftest exit 0, `SELFTEST pass`; verifier pin mismatch. No selftest distinction for this fixture. | killed (pin) |
| Loosen supersede regex | verifier `PINS total=3 mismatched=1 first=plans/anchor_line_check.py`, predicate fail. | killed (pin) |
| Skip one base-row cell comparison | verifier pins match; on do-nothing control A still `base_changed=0`, overall baseline `PREDICATE C2 fail`. This control does not exercise an in-place changed cell. | inconclusive (control not discriminating) |
| Trim state list (16 to 15) | verifier pins match; B reports `states=15 grader_pass=10 grader_fail=5 disagree=6 DEFECT`; pristine B was states=16 and disagree=6 DEFECT. The failing base control cannot establish that the mutant would be killed on a passing package. | inconclusive (baseline fails; disagreement count unchanged) |
| Remove `empty-file` errata token | verifier pins match; C reports `errata_marks=0/4 DEFECT` (pristine `0/5 DEFECT`). Baseline control lacks all marks, so this fails to establish kill discrimination. | inconclusive (baseline fails) |

Mutant SHA256s (mutated-byte hashes): drop-line `79c76e634e09d596c2e13acb52e2ae4e398538f228dae42a4c1695a009048b07`; off-by-one `0b9fff928e6778d4a5240efea31281ca65dff5a0850f6a67cb54a20757af1de7`; range `e5005e7ad0572b9739504874a169eac2a6bc82063f928aea893af7c332864007`; words `34a48c3ebf50b61553c7e62e2febb39a592a776c0769bfa6285c367518a5c780`; supersede `a2550b8c9df69364089a92f3a7df96c719a844f1bc8e1d3c7e5df474d823ffe7`; base-cell `a19fb32e86bacf70dfd017bc8d08ba7de8b783281e936fcf927a1bea1c1998f8`; state-list `2bf840bf061b87d27120873de51ebb83fa8a620c58c162ff8ddf864168e28a28`; errata `0a34093e3c12c2e00eef056003d4f4038399cc9abe477aaea0f7eab06226062c`.

This probe used the frozen do-nothing control only; it did not reconstruct the other control transformations from their receipts. A passing repaired C2 lane or the in-place/junk/splitlines/errata-only controls would be needed to resolve the three inconclusives and validate the other mutation interactions. Scratch was removed with the mandated `scratch_guard.py safe-rm` command after report creation. No tools installed.

VERDICT: c2-mutants-killed-5/8
