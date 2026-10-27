# R48C1HonestInv — independent honest-population review

Axes named: **calibration** (R48-C1); no claim of admission or axis change.

## Freeze and measurement boundary

The required stage-1 freeze exists and predates this review: `a543d92083557dd9b33ee674e9b99b03411f80af` is an ancestor of lane HEAD observed as `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; the claims file history shows only the stage-1 freeze commit. `plans/fixture_fence.py` is unchanged between `0f77f9b` and `a543d920` (diff line count 0). A clean `git clone --shared` was checked out at exactly `a543d92083557dd9b33ee674e9b99b03411f80af` under `/fast/scratch/hyaku/kengaku-r48/R48C1HonestInv/lane48`; its top-level matched that directory and status had zero lines.

No score/counter/probe was run in this review. The later-delivered population artifact provides a candidate enumeration of 120 entries (104 standing fixtures + 9 round-46 novel + 7 wave-1 novel), but stage-2 freeze pins are not evidenced here. It cannot substitute for stage-2 pins; I do not treat these entries as a scored R48 denominator.

## Independent population check

The pinned round-46 counter contract identifies the standing population as 22 source modules across `battery42` (5), `battery43` (7), and `battery44` (10), yielding 104 built fixtures. It explicitly says these are admitted ordinary honest controls. The round-46 report describes nine additional plain-`git init` repository states and records all nine refused with zero outside touches. A later-delivered wave-1 artifact, `R48C1ExecHonest/population.txt`, enumerates 120 candidate fixtures: 29 battery42, 42 battery43, 33 battery44, 9 r46novel, and 7 novel48. Its header identifies the base fence digest and builder pin; the delivering seat reports 22/22 battery module pins matched and per-fixture structural/determinism receipts. I checked the artifact's reported digest against its bytes (`70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da`) and observed 120 `HONEST` records. On the historical 113 known fixtures, 9 novel refusals / 113 = 7.96%; this must not be represented as the full-candidate fraction because the seven novel48 outcomes were not independently scored. The 120-item candidate population is not proven to be the frozen stage-2 denominator by this review.

Fixture semantics: the standing set is identified by the round-46 counter as the unchanged round-44 builder's ordinary honest battery. The nine round-46 classes are described as ordinary plain-init states. The later artifact adds seven classes (empty repo, multibranch, user config, origin remote, stash, commit-graph, notes) and the delivering seat reports reproducibility/structural audits in per-fixture receipts. I inspected the population listing and digest, not each JSON fixture receipt or independently built tree; admission/refusal remains historical evidence, not a new measurement. No result is asserted for the seven novel48 classes.

## Exact commands run and observed output

1. `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1HonestInv && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1HonestInv && cd /fast/scratch/hyaku/kengaku-r48/R48C1HonestInv && df -h /fast/scratch | tail -1 && echo TMPDIR=$TMPDIR` → `/dev/nvme1n1p2  804G  377G  427G  47% /fast`; `TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1HonestInv`.
2. `git -C $L merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD` → success; `FREEZE-IS-ANCESTOR-OF-TIP yes`. `git -C $L log --oneline --follow -- plans/round-48-claims.md` → `a543d92 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`. `git -C $L diff 0f77f9b a543d920 -- plans/fixture_fence.py | wc -l` → `0`.
3. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane48`; `git -C lane48 checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`; `git -C lane48 rev-parse HEAD` → `a543d92083557dd9b33ee674e9b99b03411f80af`; `git -C lane48 rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C1HonestInv/lane48`; `git -C lane48 status --porcelain | wc -l` → `0`.
4. `wc -l plans/fixture_fence.py plans/round46_c1_verify.py` → `575 plans/fixture_fence.py`, `635 plans/round46_c1_verify.py`. `git log --oneline 420eec9f..a543d920 -- plans/fixture_fence.py` → no output. Listing `plans/battery42`, `plans/battery43`, `plans/battery44` yielded 5, 7, and 10 named modules respectively.
5. Opened pinned counter lines 32–35: “the 22 modules of the standing batteries ... (104 fixtures the round-44 counter admits)”; opened round-46 report lines 3, 8–11. Relevant verbatim report evidence: `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `VERDICT: honest-novel-9-refused-9`.
6. `sha256sum .../R48C1ExecHonest/population.txt .../modules.sha256` → `70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da .../population.txt`; `51bfcfc4c9e6b664663f2ce5cfc8e5034808669bac3f0543d3915c1cdad11140 .../modules.sha256`. `wc -l .../population.txt` → 124 physical lines, including 4 header lines, i.e. 120 `HONEST` records.
7. Opened the delivered population listing; records comprise 104 standing fixtures, 9 `r46novel`, and 7 `novel48`. No fixture scoring was executed.

Revision measured: **none in this review** (no execution). Historical observations in cited round-46 report refer to its stated clone HEAD `42d5043afac952fcb43bf4798757785dd258cf85`; they are not attributed to the R48 freeze revision.

## Sources, access date, located quotes

Access date: 2026-10-27. Local source URLs are file URLs; no external source was opened.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — “honest population frozen at stage 2”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — “9/9 novel honest fixtures refused”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` — “(104 fixtures the round-44 counter admits)”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` — “admit only a fixture whose git store is provably the shape a plain `git init` + commits writes inside `d`”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1HoHonest.md` — “Thus **9/9 were refused**, with no outside touches.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/population.txt` — “# HONEST POPULATION round-48 C1 v1”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/builder-receipt.txt` — “SCORED none” (reported by delivering seat; file content not opened here).
- `file:///home/vgpnk/.omp/agent/RULES.md` — “Record every install or update — tool, version, channel, reason — in your report or handoff.” No tool installed or updated.

Limits: Stage-2 frozen pins/control receipts are not evidenced in this review; candidate population artifact is not sufficient proof that stage 2 committed it. No R48 scoring or item-by-item rebuild/receipt audit occurred; historical counts do not establish outcomes for novel48. No LSP device/status was exposed in this session, so no LSP semantic queries were possible; claims rely on the frozen counter contract and committed artifact/report text. Scratch tree removed before yield.

VERDICT: The delivered population artifact enumerates 120 candidates with the stated composition and verified artifact digest; historical results are 9/9 known novel classes refused and 104/104 standing fixtures admitted. New-class outcomes and the committed stage-2 denominator remain unverified; no R48 claim verdict.
