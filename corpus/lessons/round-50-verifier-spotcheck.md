author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · lane-round: 50 · hyaku run 11 · closed: 2026-10-28 (UTC)

# Round 50 — non-author verifier spot-check

I did not author this round. Everything below was re-measured or re-opened from the
committed tree; lane-authored files were not edited and no lane gate was executed as a
gate (the two claim counters were re-run as measurements, in throwaway clones).

Lane HEAD before: `71f5f5f77591d8c3d19297ee9785436da45209e4`
Lane HEAD after: `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`
Report: `.ufo/reports/round-50/kengaku.md` @ `e2666196` (fleet, author `kengaku-shokunin`)

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-50/kengaku.md` | `kengaku-shokunin e26661961e8080809445eb905e21b5214e48f85a` | pass |
| report lands last | report committer date vs lane tip committer date | report `ci=2026-10-28 14:40:42 -0300`; tip `c=14:39:56 -0300` | pass |
| cited lane commits exist and are ancestors of the branch | `git -C kengaku-shokunin cat-file -t <h>` + `git -C kengaku-shokunin merge-base --is-ancestor <h> d45c5bb` for `f7281bc 3b02d57 5c56819 822f3b7 c3372a9 6db0279 d6f2fce d45c5bb` | all `commit`, all `ancestor-of-tip` | pass |
| branch pushed, nothing ahead | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kengaku-shokunin` | `branch=master local=d45c5bb… remote=d45c5bb… ahead=0 behind=0 head=detached tracked=1 untracked=3`, exit 0 | ahead=0 pass |
| no uncommitted round work | `git -C kengaku-shokunin status --porcelain` | ` M plans/round50_c1_verify.py`; `?? .ufo/waves/round-50/w1.ready`; `?? .ufo/waves/round-50/w1.ready.partial`; `?? .ufo/waves/round-50/w1/` (193 files) | **defect D1/D2** |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-50/kengaku.md`; `git show d45c5bb:SHONEN.md \| grep -cE '^- \[[ x~]\]'` | heading present; 4 report lines `[~]`; 4 boxes in `SHONEN.md` | pass |
| dispatched prompt carries the template contract | `diff` of `.ufo/prompts/kengaku-round-50.md` §1–§5 against `kimi-shokunin/templates/round-prompt.md` with placeholder substitutions | identical except `{{FLEET_ROOT}}`/`{{AXES}}` renderings; §6 is the hyaku addendum | pass |
| five child-lane items in the prompt | report path `:101`; "The report lands last and cites the pushed lane hash" `:498`; `SHONEN` `:118`; commit-hash citation `:106-107`; "Write scope" `:430` | all present | pass |
| L2 floor matches `MISSION.md` | prompt §3 "at least 8 L2" vs `MISSION.md` §L2 concurrency | 8 = 8 | pass |
| L2 route map vs `MISSION.md` bucket | prompt run-11 route labels (`m_flash`/`m_grok`/`m_zfl`, amendment-2 `m_auto`) vs `MISSION.md` role-class bucket table | MISSION's buckets are advisory to the host route table, which the prompt makes authoritative; no numeric floor conflict | pass (note: route labels are operator directives, not MISSION rows) |
| drive evidence (mutable log, digest carried) | `.ufo/watchdog.log:1856,1861` | `2026-10-28T14:03:29-03:00 launch kengaku round=50 pgid=1387145 driver=hyaku-inline attempt=1`; `2026-10-28T14:41:43-03:00 complete kengaku round=50; hyaku-inline attempt=1` | pass |
| wave settled before report (hyaku addendum) | report §Wave; `.ufo/waves/round-50/w1.ready.partial` | 72 seats specified, 40 mounted, no `WAVE-DONE`, no `w1-results.json` | **defect D3** (disclosed by the lane) |

Report is a real report, not a marker: work performed, evidence pointers, landed-change
table tied to `LOG.md ## Round 50`, and a checkable commit hash. Determinism status: `ok`.

## 2. Claim re-checks (step 2)

Both claims were **re-measured**; neither was accepted on evidence alone. Clean clones of
the lane were used (`/tmp/r50clone` @ `d45c5bb`, `/tmp/r50base` @ `71f5f5f`).

### R50-C1 — novelty 7→8 (honest-geometry instrument + fence repair)

After (clone at `d45c5bb`, `python3 plans/round50_c1_verify.py --lane .`, exit 0):

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE .../plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
```

Before (clone at `71f5f5f`, base fence `05d5fe03…`, the round's frozen population and
counter copied in, `--skip-mutants --allow-dirty`, exit 1):

```
REV 71f5f5f77591d8c3d19297ee9785436da45209e4
FENCE .../plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
```

(the 13 refusals are the documented shapes the report names plus their battery siblings;
the same run's tail prints `PREDICATE R50-C1 fail`, matching the committed control receipt
`.ufo/waves/round-50/claims/c1-control-do-nothing.txt`.)

Verdict: **verifies** — reported before/after lines reproduce exactly; the fence digest
(`57adce4a…`), the population pin (`b5197f94…`, `mismatched=0`), the 32-module refusal set
(20 + 12), the 18-module sealed set (`git ls-tree -r d45c5bb -- plans/sealed50/*.py` → 18)
and the 15-row battery (`c1-mutants.json` `count 15`, `dropped_unwitnessed` 7) all resolve.
The four control receipts under `.ufo/waves/round-50/claims/` are committed and each fails
the predicate. **Mechanism defect D2** below: the report/SCORECARD describe the shipped
counter as deciding "in a separate process per fixture" with Q39 name hiding; the committed
counter does neither.

### R50-C2 — calibration 8→9 (self-assessment pointers resolve)

After (clone at `d45c5bb`, `python3 plans/round50_c2_audit.py --lane .`, exit 0):
`TIP d45c5bb… branch=master` / `POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0`.

Before (clone at `71f5f5f` with the tip's audit script, exit 1): `POINTERS total=271
paths=213 hashes=58 resolved=259 … unresolved=12`, with the same twelve unresolved rows the
report lists (`corpus/defects.json`, `plans/round34_*`, `plans/round48_*`, `plans/round49_*`, …).

Verdict: **verifies** (`unresolved 12 → 0`, exit 1 → 0). Revision-label defect D4: the
committed `c2-before.txt` receipt says `TIP f7281bc…` for the `total=275` line, while the
report and the SCORECARD outcomes table attribute `total=275` to `71f5f5f`; at `71f5f5f`
the count is 271 (which the SCORECARD declared-claims table does say). The predicate is
unaffected; the labels contradict each other.

### Axis harm sweep

`git -C kengaku-shokunin diff 71f5f5f d45c5bb -- SCORECARD.md SHONEN.md PROVINCE.md` →
`SCORECARD.md | 64 ++++++` and **0 deleted lines**; `--diff-filter=D --name-only` over the
whole round diff → 0 deletions. No pre-existing axis row, capability row or SHONEN box was
altered or lowered. Coverage stays 7 with the open L0 `kengaku | round-33` cap
(`.ufo/l0-questions.md:163`), which the report states.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| novelty | **improved** | counter + fence repair committed and re-measured (113/126 → 126/126 with 50 hostile modules refused); instrument inspectable in-repo. Gap: no prior-art verdict with a fetched URL for the score move (routed D6). |
| calibration | **improved** | self-assessment pointers `unresolved 12 → 0` re-measured at the tip; corrections are append-only. Mechanism overstatement in the same file is routed (D2), not scored away. |
| coverage | unchanged | 7, L0-capped; no coverage claim this round |
| depth | unchanged | 9; no depth claim |
| operability | unchanged | 8; the counters run (re-ran) but no new registry gate claim |
| freshness | unchanged | 8; the round re-verified the five fetched docs (digests match) but claims no freshness move |
| adjacency | unchanged | 8; `PROVINCE.md` and `SHONEN.md` unmodified |

## 4. Discernment spot-check (gate decisions re-opened)

Sources re-opened by URL (not from the lane's captures), at
`https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/<doc>.adoc`, 2026-10-28:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S173 gitrepository-layout | ADMIT | fetched, sha256 `39ce8d13…` = row pin; `:80-83` | **agree** | quote is verbatim at the cited lines: "This file records paths to alternate object stores that this object store borrows objects from, one pathname per line." (19 words) |
| S174 git-init | ADMIT | fetched, sha256 `12309643…` = row pin; `:69-72` | **agree** | `--separate-git-dir` text is verbatim there; row quote 10 words |
| S175 git-worktree | ADMIT | fetched, sha256 `ee8a3685…` = row pin; `:285-292` and `:395-401` | **agree on the decision, disagree on the citation** | the quoted sentence is **not** in `git-worktree.adoc`; it is `gitrepository-layout.adoc:285-286` ("A text file containing the absolute path back to the .git file / that points to here."). The shape is documented, so the admit stands; the location is wrong (D5) |
| S176 git-replace | ADMIT | fetched, sha256 `3f61be3f…` = row pin; `:20-24` | **agree** | both quoted sentences verbatim at the cited lines |
| S177 git-fetch | ADMIT | fetched, sha256 `fd225a09…` = row pin; `:42-43` | **agree on the decision, minor location defect** | the quote starts at `:41` ("The names of refs that are fetched, …"), not `:42`; D5 |
| `tbench.ai` task hub / leaderboard | REJECT | `https://tbench.ai/` → 308 → `https://www.tbench.ai/` 200 (live leaderboard page) | **agree** | mutable, unpinned, no versioned per-task spec or digest on the surface; the row states the flip condition. The row's "HTTP 404 on the cited path" sub-claim is not reproducible because the historical path is unnamed — the reject does not rest on it |

All six decisions are decided correctly on their substance; two carry citation defects that
must be corrected append-only (D5). Quote lengths: all five new rows are ≤25 words
(19/10/14/19/22).

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → exit **0**, `kengaku ok`; row count
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **170**, matching
the report's 165 → 170 with S173–S177 all tier A / `mined` / `used-by
corpus/knowledge/fixture-honest-geometry.md`. The W04 duplicate-URL warnings are
pre-existing rows (S040–S100), not this round's additions.

## 5. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | five new tier-A SOURCES rows opened and captured (`corpus/evidence/round50/*.adoc`, digests match the live URLs) + `corpus/knowledge/fixture-honest-geometry.md` admitted on ground the coverage map did not hold + capability row `honest-geometry fence counter` (first working round 50; demonstrated in §2) |
| quality | **improved** | measured over-refusal 13/126 → 0/126 with all 50 hostile modules still refused and 15/15 mutants caught; `QUALITY.md` Q41 added; three `## Mistakes` rows with evidence and fixes; no admitted entry found false |
| discernment | **improved** | this spot-check agrees with the gate on all five admits and the one reject; the lane's controlled-rejection discipline (four failing controls, committed receipts) is intact. Two citation defects are routed as corrections, not scoring |

## 6. Routed defects (lane must fix in round 51)

1. **D1 — uncommitted round work.** `git status --porcelain` at `d45c5bb`:
   ` M plans/round50_c1_verify.py`, `?? .ufo/waves/round-50/w1.ready`,
   `?? .ufo/waves/round-50/w1.ready.partial`, `?? .ufo/waves/round-50/w1/` (193 files).
   The report's "Inherited state: none uncommitted at close" is false. Commit the work or
   revert it; `jj-lane.sh state` otherwise reads `ahead=0`.
2. **D2 — the shipped counter is not the one described.** Tip
   `plans/round50_c1_verify.py` is sha256 `d8787b34…` (`git show d45c5bb:… | grep -c
   HARNESS` → 0; `def verdicts(fence_mod, fixtures)` at `:122`, deciding in-process, with
   `gen = work / f"m{i:03d}-{tag}"` name-keyed parents). The report's §Work performed
   ("decided in a **separate process** per fixture (exit 10/11/12)", "opaque random tokens
   padded with decoys"), its landing note ("landed inside `6db0279`'s tree … final in
   `d45c5bb`"), and `SCORECARD.md:2182` ("decides, in separate processes with Q39 name
   hiding") all describe the **working-tree** version (sha256
   `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999`, blob `ec2bd2e`,
   reachable only via `refs/jj/keep`; `git log -- plans/round50_c1_verify.py` shows only
   `f7281bc` and `c3372a9`). Commit it, or append a correction striking the mechanism
   sentence from the SCORECARD capability row and the report's next-round erratum.
3. **D3 — wave not settled.** 72 seats specified, 40 mounted (`w1.ready.partial`), no
   `WAVE-DONE`, no `w1-results.json`; the hyaku addendum requires WAVE-DONE before report.
   The lane discloses it; the outputs the report cites must still land (D1).
4. **D4 — revision labels.** The report's C2 row and the SCORECARD outcomes table attribute
   `POINTERS total=275 … unresolved=12` to `71f5f5f`; the committed receipt says `TIP
   f7281bc…`, and `71f5f5f` re-measures `total=271 … unresolved=12`. Append a correction
   naming the revision each number was measured at.
5. **D5 — source locations.** S175's quote belongs to `gitrepository-layout.adoc:285-286`
   (it is absent from `git-worktree.adoc`; `:285-292` there is `--reason`/`_<worktree>_`
   text, while the `gitdir` update text is `:395-401`). S177's quote starts at
   `git-fetch.adoc:41`, not `:42`. Supersede the two rows append-only and correct the
   lesson table; the digests are right, the locations are not.
6. **D6 — novelty proxy gap.** The 7→8 move cites no prior-art verdict with a fetched URL,
   which the recorded novelty proxy names; file the prior-art cell or supersede the proxy
   in `SCORECARD.md` next round.
7. **D7 — lesson spot-check row.** `corpus/lessons/round-50.md` `## Gate` records the
   candidates but no spot-check result (`LEARNING.md` asks the lesson to carry it); append
   a line pointing at this file. *(This file is the closure's record; the lane must cite it.)*

Admission: both claims re-measured true, no axis harmed → **admitted**; the defects above
are conformance/evidence defects and one routed correction, none of them bars the round.

## Addendum — the lane tip moved while this spot-check was being landed

The lane landed three further round-50 commits after the report and before this file's
first commit: `3dda12f` (adopt two late blind modules, sealed50 18 → 20), `64f51c8`
(re-run receipt, lesson post-scoring erratum), `61f6257` (land the hardened counter —
out-of-process harness, Q39 name hiding; counter digest `d8787b34…` → `850ec790…`).
Lane round tip at closure: `61f6257`; `master` also carries this closure's spot-check
commit `d52243a`. Everything above was measured at `d45c5bb` and stays true of that
revision; re-verified at the moved tip (clean clone, `TREE dirty=0`):

```
REV d52243afab26962c4ba2f469bf7917a491ce3870
FENCE .../plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass                                   (exit 0)
POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0   (exit 0)
```

The tip's `plans/round50_c1_verify.py` is sha256 `850ec790…` with the `HARNESS`
subprocess path present and 20 sealed modules; the repaired instrument reproduces the
repaired receipt. `plans/round-50-claims.md` records both open-window repairs with their
digests and the deviation note.

Routed-list consequences:

- **closed at the tip:** D1 for the counter (the hardened bytes are committed),
  D2 (SCORECARD:2182's "separate processes with Q39 name hiding" and the report's
  mechanism sentences now match the shipped bytes). D6 remains as advice, not a defect.
- **still open:** D1 for the wave outputs — `git status --porcelain` still shows
  `?? .ufo/waves/round-50/w1.ready`, `?? .ufo/waves/round-50/w1.ready.partial`,
  `?? .ufo/waves/round-50/w1/`; D3 (no WAVE-DONE), D5 (S175/S177 locations), D7.
- **new, from the late landings:** (a) the filed report still reads "final lane tip
  `d45c5bb`" and `SEALED total=18`, while the tip carries `61f6257` and 20 sealed modules —
  the correction is in the lesson erratum only, and no erratum was appended after the
  report's filed bytes in the fleet repo; (b) the cited receipt
  `corpus/evidence/round50/c1-receipt.txt` was regenerated in place (4 lines rewritten,
  `64f51c8`) rather than appended, so the report's pointer yields different numbers than
  the report's text; (c) none of `3dda12f`, `64f51c8`, `61f6257` carries a `LOG.md`
  `## Round 50` line, which the "landed changes tied to a LOG entry" contract requires.

Axis, trend and admission verdicts are unchanged: novelty **improved**, calibration
**improved**, other axes unchanged; expansion/quality/discernment **improved**;
**admitted**.
