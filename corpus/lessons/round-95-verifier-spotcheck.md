author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 95 — non-author verifier spot-check

Reviewed lane tip: `c8598439a32295bcbe114c6b9ccb3dc1d23151e3` (BASE `4524072dfae9c5e8210592b7c1da26959aa29dae`; P0 `2457f025`; P1 `16dcfed7`; P2 `7783e9cb`; freeze F `d9cd18a7519a58a1fa6d1cb9768e3873c31cd545`; measured tip T = C `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`; receipts `ea19299d`; integration `1c00331c`). Report: `.ufo/reports/round-95/kengaku.md` (fleet commit `d1adbeae54d69551b53e849b2e343a2e19144f93`, author `kengaku-shokunin <kengaku@shokunin.local>`, 2026-11-05 22:15:12 -0300). Driver digest (`.ufo/watchdog.log`, copied 2026-11-05): `2026-11-05T19:36:58-03:00 launch kengaku round=95 pgid=1142270 driver=hyaku-inline attempt=1`; `2026-11-05T22:22:02-03:00 complete kengaku round=95; hyaku-inline attempt=1`.

Method. Plain measurements over committed bytes (`git show | sha256sum`, `git rev-list --full-history`, `git merge-base --is-ancestor`, a Python `json` read of `plans/grader-population-ledger.json` at three revisions, `grep -c`), the census CLI, and live re-fetches of five upstream files with `curl`. The lane's counters (`round95_c1_replay.py`, `round95_c2_counter.py`, `round95_false_gate_census.py`), the vuln probe and gate v2 were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed receipts under `.ufo/waves/round-95/L1/` were read and graded evidence-verified.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-95/kengaku.md` → `kengaku-shokunin d1adbeae…` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` with 4 `[~]` lines; `grep -c '^- \[' SHONEN.md` → 4 | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t` + `git merge-base --is-ancestor <h> master` for 4524072d, 2457f025, 16dcfed7, 7783e9cb, d9cd18a7, afe9c229, ea19299d, 1c00331c, c8598439 → all `commit`, all ancestors; all eight round commits authored `kengaku-shokunin` | pass |
| lane pushed, clean | `jj-lane.sh state` → `branch=master local=remote=c8598439… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → empty; `ls-remote origin refs/heads/master` → `c8598439…` | pass |
| report filed after its commits | lane tip committed 22:13:20 -03, report 22:15:12, completion line 22:22:02 | pass |
| prompt carries template contract | `.ufo/prompts/kengaku-round-95.md` (fleet `0f1ce4c8`, 898 lines): §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN, Before → after, Sources & frontier, Trend verdicts), §5 commit scope, §6 hyaku addendum, §7 scratch | pass |
| marker? | real report, 8 lane commits with checkable work | not a marker → status `ok` |

Round-94 routed defects: dispositions tabled in `corpus/lessons/round-95.md` §"Round-94 spot-check routed defects" (7 rows): #1 anchor gate run before C (`lane-gates-end.txt` `live=0 cells=0`); #2 claimed as R95-C2; #3 W-4 carried; #4 gate survivors made census rows, C1 receipt-side controls on a P1 clone; #5 legacy round-79 key fix landed then partly reverted (below); #6 `--work` refusal, `LANG=C.UTF-8`; #7 carried.

Conformance defects (status-neutral, routed in §6): (a) the C commit's `mteb-retrieve` `subject` repair turned `plans/round87_c1_replay.py` red at T (lesson M2, caught only by the non-author wave); reverted in `1c00331c`, so at the landing tip the round-79 gate reads `DEFECTS n=1` / `PREDICATE R79-C1 fail` rc 1 while the round-87 counter passes (`end-receipts.txt`) — two lane gates disagree about one cell; (b) measurement launched from the wrong cwd recurs (M1, round-94 M4) — caught by rc 2, re-run correctly; (c) `plans/round94_c1_replay.py` L7 pins an absolute `executed_rows=38` and goes red at T (disclosed; rounds 90–93 counters red at BASE the same way); (d) a seat receipt held live host credential values before commit — redacted by the L1 (`outside-env-values.txt`: every non-comment line matches `=<redacted len=N>`, 0 exceptions; the only key-shaped strings in `.ufo/waves/round-95` are the seat's `FAKE_*` canaries).

## 2. Claims — re-derivation

### R95-C1 — coverage (lowest non-retired axis, L0 cap 7)

- Re-measured (Python `json` over `git show <rev>:plans/grader-population-ledger.json`, `status == "executed"`):
  - BASE `4524072d`: 88 members, executed **38**, `file-artifact` executed 29/76, `serialization-schema` 5/10.
  - T `afe9c229`: 88 members, executed **39**, `file-artifact` 30/76, `serialization-schema` 6/10.
  - landing tip `c8598439`: identical executed set to T (39).
  - Set difference T − BASE = `{fix-code-vulnerability}`; BASE − T = ∅. New row carries `round 95`, `receipt corpus/evidence/round95/vuln-probe.txt`, `subject tb2-header`, `verdict cases`.
- Receipt `corpus/evidence/round95/vuln-probe.txt` @ T: `grep -c ok=True` → 15, `ok=False` → 0, `mismatches 0`.
- Freeze integrity re-measured: all 11 `frozen-instruments` rows of `plans/round-95-claims.md` hash equal (`git show <rev>:<path> | sha256sum`) at F, T and the landing tip (11/11 ×3); `git rev-list --full-history d9cd18a7..c8598439 -- <11 paths>` → 0 commits; `git rev-list --merges 4524072d..c8598439` → 0.
- Oracle removal re-derived independently: live upstream `bottle.py` @ `0207a34f` (HTTP 200, 175847 B, sha256 `abf64368…d802` = row = capture) with the Dockerfile's `sed -i -e '1562,1563d'` then `'1567,1568d'` removes exactly `_hkey`'s and `_hval`'s raising `if`/`raise` pairs; the result hashes `761756ce31753e52…2bba` = the probe's `VULNERABLE_BOTTLE_SHA` cited in the lesson.
- Counter evidence-verified: `c1-tip.txt` `LEGS L1..L9=pass`, `TARGET executed_rows=39 member=fix-code-vulnerability located=1 executed=1 cases=15 legs=105 mismatches=0 defects=0`, `PREDICATE R95-C1 pass`, rc=0; `controls/c1-base.txt` / `legacy-r79-gate.txt` BASE leg `LEGS L1..L9=fail`, `executed_rows=38`, rc=1; landing tip same pass (`end-receipts.txt`).
- Critic dissent ruled: **verifies, narrowed** — the claim is the six `test_outputs.py` functions on a rebuilt `/app/bottle.py` (which the wave's critic found byte-identical to the image's), not the TB2 reward; the report and SCORECARD state that scope. Axis: **improved**.

### R95-C2 — calibration (ceiling 10; declared in-sample at F)

- Re-measured: population `plans/round95-false-gates.tsv` @ T has 14 non-comment rows; 14 BEFORE receipts `controls/before-r94-counter-*.txt`, each with exactly one `PREDICATE R94-C2 pass` and `rc=0` (committed in P0 `2457f025`, 19:44:39 -03, before P1's counter exists).
- Evidence-verified: `c2-tip.txt` `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc=0, each of 14 GATE lines `rc=1 passes=0 designated_red=1`; do-nothing `c2-tip-do-nothing-r94-counter.txt` `passing=14 designated_red=0`, `PREDICATE R95-C2 fail`, rc=1; honest counter `c2-tip-honest-counter.txt` W1 pass, `W2 pass fixtures=20 ok=20`, `W3 pass probes=3` (three probe mutations each drive the battery to `cases=15 ok=14`), `W4 pass freeze=d9cd18a7519a summary=(11, 11, 0)` (agrees with my own 11/11 re-hash), `W5 pass mutants=10 killed=10`.
- Gate v2 `plans/round94_freeze_integrity.py` sha256 `8574b4d5…` unchanged (frozen row, re-hashed equal at tip).
- Critic dissent ruled: **verifies, narrowed to the recorded set** (same ruling as round 94): the frozen predicate is an in-sample regression count; ≥8 held-out false gates pass the counter 5/5, a behaviour-preserving rename turns it red, 14 of 20 counter mutants survive — discrimination of unseen false gates is not established and not claimed. Axis: **improved** (scope: the 14 recorded false gates).

### Owned axes not claimed

`git diff 4524072d c8598439 -- SCORECARD.md`: one capability row annotated (freeze-integrity gate, counter v3 appended) and the round-95 section appended; no axis score line edited. Section states novelty 8, depth 10, operability 10, freshness 10, adjacency 9 held. Harm check spot-read in `end-receipts.txt` / `lane-gates-end.txt`: `PREDICATE R68-A3 pass`, `PREDICATE R91-F1 pass`, `PREDICATE R87-C1 pass` rc 0 at the landing tip; the round-79 red is conformance (a) above, not an axis harm.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | re-measured 38 → 39 of 88, set diff {fix-code-vulnerability}, receipt 15/15 |
| calibration | improved | 14 → 0 known false gates passing, evidence-verified; narrowed to the recorded set |
| novelty | unchanged | no claim; score held |
| depth | unchanged | no claim; score held |
| operability | unchanged | no claim; score held |
| freshness | unchanged | no claim; score held |
| adjacency | unchanged | no claim; score held; ConnectorOverlap: PROVINCE holds |

## 3. Discernment spot-check (`corpus/lessons/round-95.md` `## Gate`)

Re-opened live 2026-11-05 with `curl` from `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-code-vulnerability/` and `bottlepy/bottle/0207a34f…/bottle.py`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S305 `environment/Dockerfile` | admit (tier A) | HTTP 200, 814 B, sha256 `09174709…b3ab` = row; line 22 `RUN sed -i -e '1562,1563d' bottle.py` (6 words, `len(split())` = 6) | agree | line 23 `'1567,1568d'` completes the removal; applying both to the upstream bytes yields the probe's vulnerable sha — the row's mechanism is reproducible |
| S306 upstream `bottle.py` @ `0207a34f` | admit (tier A) | HTTP 200, 175847 B, sha256 `abf64368…d802` = row; line 1562 `if '\n' in key or '\r' in key or '\0' in key:` | agree | the oracle lines exist exactly where the Dockerfile deletes; `return key.title().replace('_', '-')` untouched (C02 basis) |
| S308 `tests/test.sh` | reject | HTTP 200, 653 B, sha256 `f1611da6…b17f` = row; line 9 `pip install pytest==8.4.1 pytest-json-ctrf==0.3.5` (4 words); line 12 `python -m pytest --ctrf /logs/verifier/original-repo-ctrf.json -rA` | agree | network install and a first run of the cloned repo's own suite the offline replay does not stage — correctly rejected as a replay input, and the lesson honestly records that this suite changes the reward for C11/C15 |
| S309 `task.toml` | reject | HTTP 200, 967 B, sha256 `9aa2bd14…e1dc` = row; line 29 `docker_image = "alexgshaw/fix-code-vulnerability:20251031"` (3 words) | agree | the harness runs a prebuilt image the replay never pulls; the flip (image pulled, `/app/bottle.py` compared) was exercised by a non-author seat and the reason updated in the lesson, not the row |
| S303 `tests/test_outputs.py` (SOURCES row check) | admit (tier A) | HTTP 200, 4010 B, sha256 `c006a5de…7f26` = row = frozen table; line 45 `cwe_ids = [str(cwe_id).lower() for cwe_id in cwe_ids]` (7 words ≤ 25) | agree | quote present at the cited line, word count exact |

Newly written SOURCES rows: `corpus/SOURCES.md:319-325` (S303–S309, landed in `afe9c229`); S303, S305, S308, S309 quotes re-located verbatim at their cited lines, each ≤25 words. Row count `grep -c '^| \?S[0-9]\+ '` 294 (BASE) → 301 (tip). Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0 (only pre-existing W04 duplicate-url warnings). **5/5 agree.**

## 4. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | improved | ledger frontier 38 → 39 of 88 with two class-cell moves (re-measured); five tier-A rows on a member the corpus did not hold (S303–S307), re-opened and matching |
| quality | unchanged | no admitted `knowledge/` entry superseded or re-verified; the ledger-row repair is conformance and partly reverted |
| discernment | improved | two rejects with flips, S309's flip exercised by a non-author seat; Q77/Q78 grounded in mistakes M1/M2; spot-check 5/5 agree; critic narrowings recorded beside self-verdicts |

## 5. SHONEN

All four boxes stay `[~]` in the report; this integrator writes no `[x]`. Promotion is operator-owned.

## 6. Routed defects — the lane fixes these next round

1. Round-79 vs round-87 gate disagreement on `mteb-retrieve` `subject` (round-79 `DEFECTS n=1` at tip): one counter re-pin; apply Q78 (`git grep` the old value in `plans/` before editing a ledger row).
2. C1 counters' L7 pin an absolute executed total (`round94_c1_replay.py` red at T; rounds 90–93 red at BASE): key L7 to the member set.
3. R95-C1 at reward scope: stage the repo's own suite offline, model the image's site-packages and `/app/.git` oracle copies, add the `rm /app/bottle.py` and `git checkout -- bottle.py` reward-1 cases.
4. R95-C2 generalisation: commit the wave's held-out false gates (≥8 passing 5/5) as controls under a new frozen predicate; behavioural, not byte-anchored, W3/W5 (rename must not turn the counter red); census must parse the designated RED reason, not credit any red at the leg; address the 14 surviving counter mutants; correct the M10 "no observable" exclusion.
5. SP1: the probe sandbox inherits the host environment — add `--clearenv`; and a seat receipt held live credentials before redaction — no seat may dump raw environment values.
6. M1 recurring wrong-cwd: receipts already stamp cwd; make each counter refuse when cwd ≠ lane root, so the stamp is checked, not just printed.
7. Carried: gate v2 replace refs / non-three-backtick fences (W-4), round-92 items; `docker rmi alexgshaw/fix-code-vulnerability:20251031` when no longer needed (~695 MB left on the host).
