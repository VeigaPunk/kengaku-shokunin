# RevF11 — W3ReviewKengaku F11 re-check

**Axis:** calibration. **Checked tip:** `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`.

## Finding — OPEN

- `corpus/knowledge/llm-judge-calibration.md:72` still says S010's extremes `n=2` and `n=9` carry the highest Cramér's V, without the 5-of-6 qualifier. The round-24 finding is `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md:142` (F11).
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --all --oneline -S "n=2 and n=9"` returns only `94da19e` (the claim's adding commit). Pickaxes for `"5 of 6"`, `"GPT-OSS-20B"`, `"peaks at"`, `"0.080"`, and `"carry the highest"` find no correction commit. File history has `94da19e` and `e21f9ea` only.
- `e21f9ea` appended corrections for S009's Ref-5 range and S012's §3.3 location, not F11; its `corpus/lessons/round-24.md` post-review corrections list those items, not the Cramér's V qualifier. Thus F11 is not partially fixed.
- Independently re-opened S010, https://arxiv.org/html/2602.02219 (accessed 2026-10-20): §5.4 says “on 5 of 6 judge models the lowest V sits at an intermediate scale”; Table 4 gives GPT-OSS-20B V values `0.035, 0.035, 0.080, 0.036` at `n=2,3,5,9`, respectively. The exceptional peak is `n=5`, V=`0.080`, as F11 reports.
- The claim's sole occurrence is the row at `llm-judge-calibration.md:72`; its existing corrections block does not address it. `SOURCES.md:32` does not make the Cramér's V claim; no registry correction is needed.

## Smallest append-only correction

Append a dated correction after the existing corrections in `corpus/knowledge/llm-judge-calibration.md`; leave committed line 72 unchanged:

> §Extends, “Choosing rubric granularity”: qualify the S010 extremes-highest-V pattern as holding for 5 of 6 judges (§5.4). Table 4 shows GPT-OSS-20B peaks at n=5 (V=0.080; n=2=0.035, n=9=0.036). Do not state the extremes pattern as universal.

No SOURCES registry edit is required. A companion round-25 lesson may record the omitted scope condition; it is not needed to correct the entry.

## Verification limits

No LSP device/server was available for this Markdown file; literal searches were used only to check for exact correction strings, not as semantic proof. The direct file reads, `git log -S` results, and S010 §5.4/Table 4 support the finding. No installs.

VERDICT: F11 OPEN at `3f371d2`; append the dated scope correction above, without rewriting the committed row.