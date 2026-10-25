# Fleet-rule findings for Q13

## Observed
- Admission already has a temporal bar: “Every candidate is judged before it is admitted” and only material that clears the corpus QUALITY bar is admitted (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:11-15).
- Existing outside review is distinct: “Each round a non-author” spot-checks “at least one admit and one reject” (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:42-46).
- The general landed rule says a lane report “lands last” after child-repo work is committed (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:119-123); this governs report/commit ordering, not second-seat evidence in a Gate row.
- The corpus explicitly says “No second method. Claim admission stays in `corpus/QUALITY.md`” (/home/vgpnk/Projects/shokunin/CORPUS.md:119-122). Protocol also says driver completion is not admission and independent non-author verification remains required (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:172-174).
- Scoped search found no fleet-protocol rule naming second-seat/Q10 reports or requiring their presence at a landing commit: `grep` over `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/` for `second.seat|seat report|wave.?2 seats|falsify seats|seat.*exist` → `No matches found`.

## Precedent and fit
- Kagi r21’s closure correction records that C3 coverage admissions “failed their own bar at landing” (/home/vgpnk/Projects/shokunin/MANIFEST.json:6106). The round-25 spot-check summarizes the precedent: “errata were appended by the lane, but the admissions failed their own bar at landing” (/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:132-135). Post-landing correction did not change the landing-time admission verdict.
- The same spot-check distinguishes Q10 wave seats from outside review: “wave seats are the lane, not the outside check” (/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:139-141).
- Q13 is preregistered as a narrow evidence-timing check: the admission commit’s tree must contain each specifically cited second-seat report; generic references do not support the Gate claim (/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-26-claims.md:18-24). This aligns with judging an admission against the evidence available at landing while leaving the existing QUALITY method and independent review intact; it is not a second admission method.

## Unresolved boundary
- The searched fleet protocol does not define Q10’s second-seat population, report count, or path syntax. Those details are lane-specific in the round-26 contract/Q13, not an existing fleet-wide timing rule.

VERDICT: Q13 is a lane-specific landing-time evidence-integrity check consistent with the existing admission bar and Kagi r21 precedent; no second admission method is warranted.
Installs: none.
