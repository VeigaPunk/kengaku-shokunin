# RevF3 — W3ReviewKengaku F3 recheck

Axis: calibration.

## Finding — partially fixed; not closed

- Lane tip observed: `git rev-parse HEAD` → `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`.
- Fixing attempt: `git log -S'45–48' -- corpus/knowledge/llm-judge-calibration.md` returns `e21f9ea` (`round-24: post-review fixes`) and `94da19e`. `e21f9ea` appends a correction at `corpus/knowledge/llm-judge-calibration.md:89-93` acknowledging the earlier sentence is not one range and distinguishing BiGGen Bench and FLASK ranges.
- Residual defect: the original sentence remains unchanged at `corpus/knowledge/llm-judge-calibration.md:27`. The appended “Exact cells” paragraph reports ranges and labels them “Ref-5 FR,” but does not identify the cited Table 3 column header/cells that establish the 48.58% attribution. The assigned W3 finding says the Ref-5 values in the first numeric column are 35.40–45.54 and that “48” occurs only in an unlabelled fourth column (`.ufo/waves/kaika-w3/kengaku-review.md:132`). The appended paragraph therefore does not resolve whether 48.58% is a Ref-5 flip-rate value or a different, unlabeled measure.
- Classification: partial—the appended note flags and qualifies the old claim, but its 48.58% attribution is not made auditable against the finding’s stated column issue.

## Smallest append-only fix

Append a dated correction explicitly superseding `llm-judge-calibration.md:27` and the 48.58% attribution in `:89-93`. Safest wording from the available review evidence: Ref-5 flip rates in the identified numeric column span 35.40–45.54% (maximum 45.54%, approximately 45.5%); do not include 48.58% as Ref-5 unless S009 Table 3’s actual column header and cell are identified. Leave prior committed text intact.

Installs: none.

VERDICT: Partially fixed; F3 remains open pending an append-only correction that removes or fully identifies the unsupported 48.58% column attribution.