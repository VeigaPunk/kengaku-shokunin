# R46W2C2Entry — C2 depth falsification

Reviewed landing `42d5043afac952fcb43bf4798757785dd258cf85` (scratch clone HEAD matched). Axes: predictor fidelity; errata completeness against round-45 closure §§2–3; prose/code consistency; source ranges.

## Findings

No actionable C2-entry defects found (0). The five errata items account for the round-45 routed C2 defects: lone-CR predictor divergence; prose overstating the predictor; S152/S153/S154 citation locations; empty-file decisive mechanism; and overlong/understated source bounds. The closure additionally identified the S154 `teaches` paraphrase (D6); current errata item 3 explicitly documents that historical mislocation but does not state that `teaches` is corrected. The current S163 registry row should therefore be checked alongside this entry; the frozen counter validates line/range/word anchors, not semantic `teaches` truth. No entry-level surviving misstatement was evidenced in the reviewed text. This is a residual verification limit, not counted as an entry defect.

Predictor: the code explicitly translates CRLF then lone CR to LF before `.strip().split("\n")`, matching universal-newline `read_text()` semantics. Independently generated 200 deterministic random strings using seed 46, from answer/decoy/whitespace/newline characters: `random_states=200 predictor_disagree=0` (command: Python invocation in this seat). The test did not execute pytest; its captured grader behavior was independently modeled from the documented read/strip/split rule. Frozen counter also exercised 16 cases with `disagree=0`.

Prose/code review: Finding 3 accurately describes lone-CR normalization; Predictor block matches the implementation. Empty-file mechanism correctly says `split("\n")` yields `['']`, so `len(guesses)>0` passes and membership at line 18 fails. Errata labels and numbered items reflect the actual corrected statements.

Source ranges in `source:` lines are S149 `9-10`/`14-18`, S150 `1-9`, S151 `1-43`, S152 `1-20`, S153 `1-29`, S154 `1-33`, S155 `1-68`, S156 `1-41`; these agree with the text’s capture counts and the C2 counter's `source_ranges_bad=0`.

## Verification

Counter command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" python3 "$S/lane/plans/round46_c2_verify.py" --lane "$S/lane"`.
Envelope printed `ENVELOPE ...`; exit 0, local_bin unchanged. Output: `PINS total=3 mismatched=0`; `A anchorline live=0 repaired=8 base_rows=149 base_missing=0 base_changed=0 ok`; `B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok`; `C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok`; `D selftest exit=0 ok`; `checks=4 defects=0`; `PREDICATE C2 pass`.

No tools installed. **Residual risk:** counter's 16-state corpus is not broad; random 200-state agreement offers additional but finite sampling. S154 `teaches` semantic correction depends on S163, outside this entry, and is not validated by C2 anchor-line checks.

VERDICT: c2-entry-defects-0-predictor-disagree-0
