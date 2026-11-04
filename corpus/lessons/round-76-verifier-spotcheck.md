# Round 76 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · lane-round 76 · base `fda63968f29f8f58dc2b28831acac879405b8326` → tip
`a6a2a7b83fd424b3e1d163b082281d9fb052a259`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-76/kengaku.md` (fleet commit
`60ca29d426eb2eca0f17f666c0b7d0ccfc2723ec`, author and committer
`kengaku-shokunin <kengaku@shokunin.local>`)
watchdog digest (mutable `.ufo/watchdog.log`, copied at closure):
`2026-11-04T01:47:24-03:00 launch kengaku round=76 pgid=2443702 driver=hyaku-inline attempt=1` ·
`2026-11-04T02:11:33-03:00 complete kengaku round=76; hyaku-inline attempt=1`

I did not author this round. Numbers below were re-derived from committed bytes with plain
measurement (git/grep/awk/jq/independent path and HTTP probes); the lane's gates and selftests were
checked by their committed receipts and code, never executed (PROTOCOL §Gate standard, Closure
consequence).

## 1. Step-1 conformance

| check | command / observation | result |
|---|---|---|
| report authored by the lane identity | `git log --format='%an <%ae> %H' -- .ufo/reports/round-76/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> 60ca29d4…`; author = committer = lane identity; only that path in the commit (`1 file changed`) | pass |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box, each with a pointer; no `[x]` written | pass |
| cited commits exist and are ancestors | every 7–40-hex commit token in the report (`1ce25089` … `fda63968…`, 22 distinct commits incl. the two full `close_commit` hashes) → `git merge-base --is-ancestor <h> master` rc 0 for all; the two non-commit tokens (`46d106b7…`, `7f41f588…`) are the S252 capture digest and the identity-manifest sha256, not commits; `git ls-remote origin refs/heads/master` → `a6a2a7b8…` | pass |
| lane clean / pushed | `jj-lane.sh state` → `branch=master local=a6a2a7b8… remote=a6a2a7b8… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty | pass |
| prompt carries the template contract | `.ufo/prompts/kengaku-round-76.md` lines 1–140 vs `templates/round-prompt.md`: identical modulo placeholders (lane, round, fleet root, lane axes) — 140/140 lines; §6 hyaku addendum (run-15 routing, round size 8–16, campaign) and §7 scratch discipline present; all five child-lane items present (report path/filename, commit-then-report ordering, `SHONEN` heading, commit-hash citation, push/write scope); prompt's L2 floor is "at least 8"; MISSION.md carries role-class buckets only (no model aliases), so the prompt's run-15 route map contradicts no SSOT line | pass |
| report order | final lane commit `a6a2a7b8` committed 02:10:17 −03; report commit `60ca29d4` committed 02:10:57 −03 (author date 02:08:31, committer later) — report lands 40 s after the lane tip it cites | pass |
| wave shape | `w1-validate.rc` → `rc=0`; spec 14 items (executor 4, scribe 3, scout 1, connector 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1); attack 4/14 = 28.6 % (≥25 %), connector 1 (≤2); policy band 8–16, `maxLanes=14`; `w1-dispatch.json` `counts.spawn=14 total=14`, no model key; `w1-results.json` 14 records, every `output` non-empty, dead seats 0; `w1.ready.dispatched` names all 14 seats | pass |
| report sections | Work performed, Landed changes (21 commits, each with a LOG entry name), Before → after, Sources & frontier, Trend verdicts, SHONEN — present and ordered; real committed work (not a marker) | pass (two section defects, V3/V4 below) |

Conformance defects, all status-neutral: R76-V1 (C1 battery receipts stamped at a revision that
carries only the 8-case battery), R76-V2 (new registry rows pin superseded tallies), R76-V3
(LOG/lesson keep superseded before-values and battery counts without an appended correction),
R76-V4 (report names a LOG entry that does not exist), R76-V5 (prior-art claim contradicts the
lane's own round-66 lesson), V6/V7 minor (capability-name drift; unrereceipted gate reruns). None
bars admission.

## 2. Per-claim re-check

### R76-C1 / coverage — verifies (re-measured live at the tip)

I enumerated the `## Surfaces` table from committed bytes and resolved each row myself (paths with
`test -e`, loopback endpoints with `curl -m 4`; no external traffic):

```
$ git show a6a2a7b8:PROVINCE.md | sed -n '12,22p'  # 11 rows after the header
      row1 Research notes           ~/Projects/webzites/repos/llm-wiki   ABSENT
      row2 Local benchmark battery  ~/archive/bench-arena/               ABSENT
      row3 Served local model       http://127.0.0.1:34113              ABSENT
      row4 Served local model r51   http://127.0.0.1:45669              ABSENT
      row5 Route telemetry          ~/Projects/bounties/.../telemetry.jsonl  ABSENT
      row6 Client CLI telemetry     ~/.bailian/telemetry.jsonl          ABSENT
      row7 Model catalogs           ~/.bailian/.../models/index.md      ABSENT
      row8 Own probe artifacts      corpus/evidence/round8-horizon/     PRESENT
      row9 In-repo gate             grader.py                           PRESENT
      row10 Corpus index            corpus/README.md                    PRESENT
      row11 Public literature       corpus/knowledge/eval-prior-art-calibration.md  PRESENT

$ test -e <each path>  → 4 PRESENT, 7 ABSENT
$ curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health → 000
$ … http://127.0.0.1:45669/health → 000     $ … http://127.0.0.1:1234/health → 200
```

Present=4 / absent=7 / total=11 matches the receipt's `SURFACES` line exactly. Declaration
agreement: an `awk` split of the 11 rows gives two `ABSENT YYYY-MM-DD` markers on rows 1–3, one on
rows 4–7, and **zero** on rows 8–11 — i.e. every absent row carries a dated marker and no present
row does (`AGREE disagree=0`, reproduced). The three base defects are repaired at the tip: row 2's
present-tense `relocated intact` is gone (now "was relocated … were all present … (SUPERSEDED
2026-11-04 …)"), row 3's `identity re-probed` is now `identity checked each round through round
25`, and row 4 carries `ABSENT 2026-11-04`. Base receipt `c1-before.txt` (rc 1) prints exactly the
three defects the report names; after receipt `c1-after.txt` (rc 0, `LANE_TIP a47a5530`, `WORKTREE
clean`) prints `agree=11 disagree=0`, `PREDICATE R76-C1 pass`. The gate did not exist at base:
`git cat-file -e fda63968:plans/round76_c1_surface_resolver.py` → rc 128.

Control: `c1-control-declared.txt` → `declared=present live=absent 4 http://127.0.0.1:45669`,
`disagreements=1`, `target_reached=False`; my live probe answers 000 for that endpoint, so a
declaration-trusting counter cannot reach the target. Selftest `cases=12 red=11` and mutants `9/9`
are evidence-verified from the committed receipts and the final counter's case list (not executed);
their stamp caveat is V1.

Stated limits I accept as disclosed: the claim's universe is the `## Surfaces` table (the older
`## Province map` tables are out of scope and routed), the population is not frozen (deleting rows
shrinks the denominator; the identity manifest is the mitigation), and any non-000 HTTP status
counts as present.

### R76-C2 / calibration — verifies (re-measured from committed bytes)

Ledger before→after, counted directly:

```
$ git show fda63968:corpus/routed-findings.jsonl | grep -c 'R75-D'   → 0
$ git show a6a2a7b8:corpus/routed-findings.jsonl  | grep -c 'R75-D'   → 7
```

All seven ids named in `corpus/lessons/round-75-verifier-spotcheck.md` §6 (R75-D1…D7) are present
at the tip as `status: closed` rows with `close_commit`, `verified_at`, `evidence_path` and
`evidence_literal`. Re-derived by me, per row: the close commit is an ancestor of `master`
(`git merge-base --is-ancestor` → 0 for `6977019b…` on D1–D4/D7 and `f0d52322…` on D5/D6) **and**
the named evidence exists in that commit's own tree with the literal present:

```
$ jq -r 'select(.id|test("^R75-D"))|[.id,.close_commit,.evidence_path,.evidence_literal]|@tsv' …
R75-D1 OK path=corpus/QUALITY.md literal=R75-D1
R75-D2 OK path=SCORECARD.md literal=9f8f0f2180821d165f60e400277f192d92afbbce
R75-D3 OK path=SCORECARD.md literal=R75-D3 60 4/36/20
R75-D4 OK path=SKILL.md literal=cases=8 red=7
R75-D5 OK path=LOG.md literal=R75-D5
R75-D6 OK path=corpus/evidence/round76/r74-c1-tip.txt literal=PREDICATE R74-C1 pass
R75-D7 OK path=corpus/lessons/round-74.md literal=R75-D7
```

The legs' underlying facts re-derive at the tip: `9f8f0f218082…` and `5d9a0ccc` each occur once in
`SCORECARD.md`, `cases=8 red=7` and `arms=5` once in `SKILL.md`, `R75-D5` + the stamp + `cases=8
red=7` once in `LOG.md`, `R75-D7` once in `corpus/lessons/round-74.md`; both round-74 tip receipts
read `PREDICATE R74-C1 pass` / `PREDICATE R74-C2 pass` at `LANE_TIP 6977019b`, `WORKTREE clean`.
After receipt `c2-after.txt` (rc 0, `LANE_TIP a47a5530`, clean) prints `SCOPE ids=7 registered=7
closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0`, `PREDICATE R76-C2 pass`; the
status-only control loses (`rows_claimed_closed=7 trivial_checks=1 failed_legs=3`). Selftest
`cases=14 red=13`, git arms `3/3`, mutants `12/12` are evidence-verified, not executed.

### Re-measured vs evidence-verified

- **Re-measured by me:** all 11 surface resolutions and their declarations; the three base defects
  and their tip repairs; census and row counts; the seven ledger rows, their ancestry and their
  evidence-at-commit; the seven legs' greps; both round-74 receipts; every cited commit's ancestry;
  wave/dispatch counts; prompt fidelity; the assimilation numbers (175 staged rows / 167 collisions
  / 8 free ids / 61 of 65 knowledge targets absent) and the live S252 re-fetch.
- **Evidence-verified, not executed:** both selftests' arm lists and tallies, the C1 and C2 mutant
  matrices, both controls' receipts, and the two after receipts' internal stamp lines.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C1's target re-derives live: 11 rows, 4 present / 7 absent, 11/11 declarations agree, and the three rows that lied at base are dated supersessions at the tip. Score held at **7** by the open L0 cap. |
| calibration | **improved** | seven routed ids moved 0 → 7 rows, and every close re-derives at the commit it names (ancestry + evidence path/literal, 7/7). Score held at **10**, exercised. |
| depth | unchanged | S252 + Q55 + five Mistakes rows; no knowledge entry admitted; score 10 held |
| operability | unchanged | two new registered gates with selftest/mutant batteries and stamped receipts; score 10 held (stale tally cells routed as V2) |
| freshness | unchanged | every declared surface re-resolved live; S252 re-fetched byte-identically; score 10 held |
| adjacency | unchanged | sibling inventory reported out, not absorbed (assimilation `none` re-checked); score 9 held |
| novelty | unchanged | the resolver is an increment of round 51's, said plainly; no new construct claimed; score 8 held |

No owned axis harmed: `git diff fda63968 a6a2a7b8 -- SCORECARD.md` is `121 0` (append-only),
`LOG.md` `57 0`, `SHONEN.md` untouched, `PROVINCE.md` `19 4` (dated in-row supersessions on rows
2–4 plus the §Round 76 declaration), `SKILL.md` `4 2` (the stale round-75 registry rows corrected),
and the whole lane diff deletes no file (`git diff --diff-filter=D` empty).

## 4. Discernment spot-check (LEARNING.md — from outside)

| item | lane decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S252 — Git `git-merge-base` documentation | **admit**, tier A docs, scope ancestry tests and their three exit states | live `https://git-scm.com/docs/git-merge-base` re-fetched: HTTP 200, **41 397 B**, sha256 `46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644` — byte-identical to `corpus/evidence/round76/sources/git-merge-base.html`; quote starts capture line 1703, 25 words | **agree** | the quote is verbatim (wrapped across two lines: "Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not."), located, ≤25 words; tier A fits the official Git docs on their own scope; the row is `mined` and both `used-by` paths exist |
| "a commit id in a row's `close` text proves the discharge is on the branch" | **reject** (flip: dedicated `close_commit`, three-state ancestry, `CLOSE-NOT-ANCESTOR` distinct from `CLOSE-UNRESOLVED`) | same page, sentence after the quote: "Errors are signaled by a non-zero status that is not 1." — exit 1 is a negative answer, not an error; `grep -c 'CLOSE-NOT-ANCESTOR\|CLOSE-UNRESOLVED' plans/round76_c2_defect_discharge.py` → 1/2 | **agree** | a printed id names an object, not branch membership; the three-state split is what makes "unresolved" distinguishable from "not an ancestor", and the counter implements the flip |
| "a declaration is evidence of resolution" | **reject** (flip: resolve first, then compare the dated marker to the verdict) | `corpus/evidence/round76/c1-control-declared.txt` → `declared=present live=absent 4 http://127.0.0.1:45669`, `disagreements=1`, `target_reached=False`; my own probe of `:45669` → 000 | **agree** | the control's losing result and the live 000 show the declaration is independent of the host; the `AGREE` leg is the correct repair |

Newly written SOURCES row: `corpus/SOURCES.md:268` S252 — row count 243 → 244
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), tier `A`, status `mined`, anchor
`capture …:1703, anchor --is-ancestor`, sha256 pinned and matching the live fetch, quote 25 words;
`used-by` paths `corpus/lessons/round-76.md` and `plans/round-76-claims.md` both exist.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → rc 0; `ok` line; 25 `W04` duplicate-URL warnings, the same
25 in both committed census receipts. Spot-check grades: admit agree, both rejects agree.

## 5. Trend verdicts

- **expansion: improved.** Two capability rows entered `SCORECARD.md`
  (`province-surface-resolver-table-anchored`, `routed-defect-discharge-binding`) and the registry
  gained S252 (243 → 244); no `corpus/knowledge/` entry was admitted and the report says so. The
  capability rows enter only through a demonstrated run this round, which the receipts support.
- **quality: improved.** Three registered gates that were red at base are green under committed
  evidence (`R74-C1`/`R74-C2` tip receipts; `R51-C1`'s manifest repair — SF02 re-anchored, SF21
  added, SF14 re-pinned to the 244-row census; `R75-C1`'s missing index rows added), and the
  PROVINCE registry count is re-pinned to the census. No admitted entry failed its re-check. The
  superseded tallies in the new registry rows and in LOG/lesson are routed (V2/V3) and do not
  reverse the trend; two rerun outputs are prose-only (V7).
- **discernment: improved.** This outside spot-check agrees with the gate on the sampled admit and
  both rejects (§4), and the round's four attack classes became committed amendments or stated
  limits (A5/A8/A9) rather than being smoothed.

## 6. Routed defects and operator note

- **R76-V1 (battery receipts at a pre-battery revision) — routed.** `c1-selftest.txt` and
  `c1-mutants.txt` stamp `LANE_TIP c8c116b4` / `WORKTREE dirty`, but the 12-case selftest and
  9-mutant matrix exist only from `4b884412`: at `c8c116b4` the selftest list has **8** cases and
  six mutant ids. A re-run at the stamped revision prints `cases=8`, not the receipt's
  `cases=12 red=11`. Re-mint the two C1 battery receipts at the commit that carries the battery (or
  record the content revision beside `LANE_TIP`) — the R75-D2 class.
- **R76-V2 (registry drift, R75-D4 class) — routed.** The new `SKILL.md` rows pin superseded
  tallies: `round76-c1-surface-resolver` says `cases=7 red=6` (final `cases=12 red=11`, mutants
  `9/9`), `round76-c2-defect-discharge` says `cases=10 red=9` and `--mutants 8/8` (final
  `cases=14 red=13`, `12/12`). C1's pass/fail map also omits the A5/A8/A9 defect classes
  (`NONLOCAL-ANCHOR`, `ESCAPE-ANCHOR`, `OVERFLOW-ANCHOR`, `MALFORMED-DATE`, `DUPLICATE-SURFACE`,
  `MANIFEST-DRIFT`, `EMPTY-SCOPE`, `LEG-PENDING`, `NEGATED-DISCHARGE`). Re-pin both rows to the
  final receipts and the final defect-class sets.
- **R76-V3 (corrections did not sweep every mention) — routed.** `LOG.md` round-76 "Verification
  boundary" still carries the A4-era numbers (`agree=9 disagree=2`, C1 `cases=7 red=6`, mutants
  `5/5`, C2 `cases=10 red=9`, `8/8`), and `corpus/lessons/round-76.md` §"Census and instrument
  readings" carries `agree=9 disagree=2` and `wrong=14`; the final receipts read `agree=8
  disagree=3`, C1 `cases=12 red=11`/`9/9`, C2 `cases=14 red=13`/`12/12`, C2 before `wrong=13`.
  `SCORECARD.md`'s main round-76 row likewise keeps `agree=9 disagree=2` / `wrong=12` and is
  superseded only by the later addenda, which name the new values but not the old ones. Append
  dated corrections naming both sides (append-only files; never rewrite the filed lines).
- **R76-V4 (report pointer to a nonexistent LOG entry) — routed.** The Landed-changes table ties
  commit R (`d31feec9`) to the LOG entry "Second-reviewer classes", but that entry does not exist in
  `LOG.md` (the A9/EMPTY-SCOPE content landed in the lesson only); a `grep -c` for the heading is 0.
  Add the LOG block, or correct the pointer in the next report/an erratum.
- **R76-V5 (prior-art claim contradicted by the lane's own record) — routed.** The report's
  `considerthese` paragraph repeats the round-65 "no still-unimplemented proposal" assertion, while
  `corpus/lessons/round-66.md:332` records proposal 2 (`tb2_grader_admit`) as unimplemented and my
  sweep agrees: `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md SKILL.md` hits only that
  round-66 lesson line; `plans/` has no standing admission counter by that name. Re-adjudicate the
  three proposals with the sweep and record proposal 2 as open or cite the implementing artifact.
- **R76-V6 (minor: capability-name drift) — routed.** `PROVINCE.md` §Round 76 calls the capability
  `declared-surface-resolver`; the `SCORECARD.md` capability row is
  `province-surface-resolver-table-anchored`. Use one name.
- **R76-V7 (minor: unrereceipted gate reruns) — routed.** `routed_open.py` (`ROWS total=86 open=31
  blocked=1 closed=52 refused=2`, `--selftest 12/12`) and the `R51-C1`/`R75-C1` tip reruns are
  quoted in LOG/SCORECARD/report but no committed stamped receipt carries them (only the round-74
  pair is committed). Mint and commit the receipts at the revision measured.
- **For the operator (promotion-owned, never closure):** all four `SHONEN` boxes remain `[~]`
  lane-asserted. Their pointers resolve (SKILL registry, LOG round-76 entry, claims/amendments doc,
  PROVINCE refusals + the connector report-out), so boxes 1–4 look checkable by a non-author; the
  promotion decision stays operator-owned, and V2/V3 should land before any box is written `[x]`.
