# R31FxLessonDraft — round-30 errata falsification

Scope: the three corrected cells in `corpus/lessons/round-30.md` §Errata, tested against HEAD's committed bytes; cited commands below were run from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless stated.

## Findings

- **Q6 basis correction survives.** `corpus/lessons/round-30.md:195-200` says the superseded location is `:66-67`. The source cell is actually at `corpus/lessons/round-30.md:66-67`; it said “one field, one placement, one value set.” At HEAD, `corpus/knowledge/contamination-transparency-card.md:72-84` explicitly retracts that phrasing: “one field, and the rest is not a delta at all,” then identifies S1 as not new and R1 as inherited. Thus the correction is substantively accurate and its citation range is right. Command: `read corpus/lessons/round-30.md:66-67; read corpus/knowledge/contamination-transparency-card.md:72-84`.

- **Q2 tier correction survives.** `corpus/lessons/round-30.md:201-204` corrects the Q2 tier set and cites S086's registry row. HEAD `corpus/SOURCES.md:110` labels S086 `paper | B`; the original Q2 cell is `corpus/lessons/round-30.md:60-61` and says `S086 A`. Therefore corrected value S086 B is right, citation range `:60-61` is exact. The Q2 floor rationale is also consistent with the declared QUALITY rule (tier A-or-B floor). Command: `read corpus/lessons/round-30.md:60-61; read corpus/SOURCES.md:110`.

- **Round-shape correction survives.** `corpus/lessons/round-30.md:205-208` corrects the header at `:3`; that header indeed says “36 build, 34 falsify” (`corpus/lessons/round-30.md:3`). I ran a Python JSON count over `.ufo/waves/round-30/{build,falsify}/swarm-registry.json`; it returned 36 and 33 respectively. The verifier spotcheck independently states the report is 33 at `corpus/lessons/round-30-verifier-spotcheck.md:39-44`. Exact cited range `:3` is right. Command: `python3 -c 'import json; ... len(json.load(open(path))["members"]) ...'` (36/33); `read corpus/lessons/round-30.md:3; read corpus/lessons/round-30-verifier-spotcheck.md:39-44`.

- **The analogous Q5 misclassification remains.** The corrected Q2 tier cell does not fix the same peer-reviewed-status error in Q5. At HEAD, `corpus/lessons/round-30.md:66` still says “S081/S082 preprints vs S083/S086 peer-reviewed.” But S086 row `corpus/SOURCES.md:110` explicitly says the society publishes the proceedings “without peer review”; the admitted entry `corpus/knowledge/contamination-transparency-card.md:153-155` likewise says S086 is without peer review and labels it non-peer-reviewed. The precise wrong cell is lesson `:66` (within `:66` but not `:66-67` as a whole); the correction is needed to remove S086 from the peer-reviewed side. Command: `read corpus/lessons/round-30.md:66; read corpus/SOURCES.md:110; read corpus/knowledge/contamination-transparency-card.md:153-155`.

## VERDICT: Q6, Q2-tier, and shape errata survive with correct cited ranges; Q5's “S086 peer-reviewed” claim fell and remains uncorrected.

No tools installed or updated.