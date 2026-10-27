# R46W2C3Filler — V13 falsification

Axes: coverage (primary); provenance/identity (supporting).

## Counterexample and evidence

At frozen HEAD `42d5043afac952fcb43bf4798757785dd258cf85`, the committed filler control was run with the prescribed envelope and failed. Command: `python3 $S/lane/plans/round46_c3_verify.py --lane $S/lane --work $S --filler`. Output: `V3 ok`, V4/V6/V7/V9/V10/V12 DEFECT, `checks=7 defects=6`, `PREDICATE C3 fail`; envelope ended `exit=1 ... unchanged` (not INVALID).

I tested a stronger echo-shaped impostor in a disposable clone: copied the real spec to `plans/filler46/pkg-spec-filler.json`, copied the frozen probe as filler probe, and ran the ordinary counter. It got V1, V3–V6, V9–V12 largely through, including census and predictor, but remained rejected: V2 `gate_exit=1`, V7 malformed/absent case-map rows, V8 order fail, V13 `KeyError: 'dry'`; total `checks=13 defects=4`, `PREDICATE C3 fail`, exit 1. Envelope output ended `exit=1 ... unchanged`. This is a deliberately strong package-echo attempt, not a change to the frozen lane.

The control's V13 implementation (counter lines 816–825) runs V3,V4,V6,V7,V9,V10,V12 and requires at least three defects among substantive V3,V4,V7,V9,V10,V12. The unmodified filler yields six defects, including five substantive; the echo attempt did not create a V13 pass (it errored because copied spec lacks filler-only `dry`). The attempt also demonstrates that echoing the real package's receipt/probe alone does not satisfy independent gate, order, V7, or V13 requirements.

Receipts: `.ufo/waves/round-46/w2/R46W2C3Filler/filler-run.txt` and `echo-run.txt`. Both contain full ENVELOPE lines and output. Frozen clone HEAD recorded in each.

## Smallest safe correction / disposition

No V13 bypass found. Preserve the current control and reject this proposed forgery. A narrow robustness improvement would make V13 report the missing `dry` key as a normal filler defect rather than an uncaught error; it is not a forged pass and does not alter the coverage predicate. No lane edits made. No tools installed.

VERDICT: c3-filler-forged-pass-no-legs-fooled-0
