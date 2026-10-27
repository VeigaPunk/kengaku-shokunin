# R46W2C2Bypass — C2 falsification

**Axis:** depth. **Counterexample:** an errata section containing only all five required tokens, with no correction statements or evidence, passes C2 on a TIP clone.

Starting point verified in scratch: clone root `/fast/scratch/hyaku/kengaku-r46/R46W2C2Bypass/lane`; HEAD `42d5043afac952fcb43bf4798757785dd258cf85`. In that clone I replaced the entire `## Errata (round 46)` section with exactly:

```text
## Errata (round 46)
lone-CR S152 S153 S154 empty-file
```

The entry's actual errata explanations/corrections were thereby removed. Counter invocation, full output and ENVELOPE lines: `R46W2C2Bypass/errata-token-bypass.txt`. It reports `C entry ... errata_marks=5/5 ok`, all four legs ok, `checks=4 defects=0`, `PREDICATE C2 pass`, exit 0. This is a false-positive counterexample, not a claim that landed TIP itself has this mutation.

**Evidence / mechanism:** frozen claims require an Errata section naming every corrected statement, and the mutated entry fails that meaning while retaining the five strings. `round46_c2_verify.py` leg C (lines 182–185) counts each token's substring presence in the section; it never checks that each mark is attached to a correction, nor that the correction exists. The evidence-free tokens meet its entire errata predicate. Receipt includes the required ENVELOPE and pass output.

**Impacted axis:** depth. One of the three C2 criteria (errata meaningfulness) is not operationally tested; the pass predicate can certify a section that contains no corrections. The other legs' successful values do not cure this gap. This falsifies the counter's ability to prove the complete frozen C2 claim; it does not by itself establish that the actual repaired entry is false.

**Smallest safe correction:** replace token-presence scoring with per-mark structured checks that require a corresponding non-empty correction item and evidence reference, and have a negative control with the five tokens but no correction items fail. Re-run the unchanged landed-TIP predicate and controls only after the counter change is frozen.

No tools installed. Scratch removed with `scratch_guard.py safe-rm`.

VERDICT: c2-bypasses-1-verdict-changing-1