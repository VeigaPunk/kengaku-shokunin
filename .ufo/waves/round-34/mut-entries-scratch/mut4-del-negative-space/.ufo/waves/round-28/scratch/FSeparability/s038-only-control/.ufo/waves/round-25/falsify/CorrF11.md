ATTACKS: Round-25 appended correction for kaika W3 F11 — append-only status, S010 accuracy, and finding closure.

## Findings
- None. The correction survives the requested checks.

## Evidence
- Append-only: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 6180e4f 8ea41f9ed -- corpus/knowledge/llm-judge-calibration.md` reports `1 file changed, 10 insertions(+), 0 deletions(-)`. The patch adds only the round-25 section at EOF; no prior lines are removed or changed.
- Source identity: `corpus/evidence/round24-sources/gate.md:18` pins S010 at 281,257 bytes, SHA-256 `a89e2256f106c2a2daa72711175b6355951636a2f76e9db2e117dcc02aa49678`. Re-fetching `https://arxiv.org/html/2602.02219` produced the same byte count and digest.
- Factual check: S010 §5.4 states that on 5 of 6 judge models the lowest V is at an intermediate scale (n=3 or 5), while extremes n=2 and n=9 carry the highest V. Table 4 gives GPT-OSS-20B values at n=2,3,5,9 as 0.035, 0.035, 0.080, 0.036, respectively; its peak is 0.080 at n=5. The other five Table 4 rows follow the stated extreme-highest pattern.
- Closure: `kaika-w3/kengaku-review.md:142` asks to add the 5-of-6 qualifier and identify GPT-OSS-20B's n=5 peak. `corpus/knowledge/llm-judge-calibration.md:104-107` does both and explicitly says not to state the pattern as universal. `corpus/lessons/round-25.md:58` records this appended correction as the F11 action.

## Residual risk and verification gaps
- The original unqualified wording remains at `corpus/knowledge/llm-judge-calibration.md:72`, before the appended erratum at lines 99-107. The correction identifies that exact row and supplies its scope, so this is a discoverability risk rather than an uncorrected factual claim under the append-only correction convention. No verification gap remains for the requested source/table checks.
- Installs: none.

VERDICT: SURVIVES — the append-only correction is source-accurate and closes F11 by adding the requested qualifier.