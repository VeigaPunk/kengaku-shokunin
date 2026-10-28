# Round 51 — C2ExecG (executor): ledger rows 55–63 attribution

Lane `kengaku-shokunin`, hyaku run 11, wave `kengaku-r51-w1`. Seat axes: **adjacency**
(R51-C2). Item: attribute `corpus/routed-findings.jsonl` rows 55–63 (0-based 54..62) with
`owner`, `disposition`, an authored `check` where empty, and a run of every check in a
scratch cwd.

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

The instrument I ran is byte-identical to the stage-1 freeze `e07f131c…`:

```
$ sha256sum plans/round51_routing.py
7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03  plans/round51_routing.py
$ git show e07f131c:plans/round51_routing.py | sha256sum
7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03  -
$ git log --oneline e07f131c..HEAD
4090c3d round-51: v2 wave spec (64 seats) + validated dispatch payload
$ git diff --stat e07f131c..HEAD -- plans/round51_routing.py corpus/routed-findings.jsonl plans/round-51-claims.md
(no output)
```

## Fragment delivered

`.ufo/waves/round-51/w1/C2ExecG.jsonl` — 9 complete row objects, one per line, original
field order preserved, `owner` inserted after `status`, `disposition` after `owner`, every
other original field byte-equal (verified programmatically: `extra=['disposition','owner']
missing=[] changed=['check']` for all 9 rows; `check` changed only by the cwd prefix, see
§Instrument finding I1).

| 0-idx | id | class | status | owner | disposition | check exit |
|---|---|---|---|---|---|---|
| 54 | R42-R3-36 | plan-class-from-unfrozen-probe | open | kengaku | accepted-risk | 1 (absence confirmed) |
| 55 | R42-R3-37 | plan-host-dependent-cheat | open | kengaku | accepted-risk | 0 (authored) |
| 56 | R42-R3-38 | entry-false-sentence | closed | kengaku | fixed-verified | 0 |
| 57 | R42-R3-39 | entry-wrong-citation | closed | kengaku | fixed-verified | 0 |
| 58 | R42-R3-40 | entry-overclaim | closed | kengaku | fixed-verified | 0 |
| 59 | R42-R3-41 | entry-counterfactual-error | closed | kengaku | fixed-verified | 0 |
| 60 | R45-S5-1 | row-anchor-wrong-line | closed | kengaku | fixed-verified | 0 |
| 61 | R45-S5-2 | predictor-lone-cr | closed | kengaku | fixed-verified | 0 |
| 62 | R45-S5-3 | log-in-place-rewrite | closed | kengaku | fixed-verified | 0 |

Totals: `owner` 9/9, `disposition` 9/9, checks present 9/9 (one authored, eight preserved
plus the cwd prefix), `fixed-verified` 7/7 green in this run, `routed`/`referral` 0 →
`next` not required on any row.

## Why every row is `kengaku`-owned (and none is routed)

The routed/referral rule requires a non-`kengaku` owner. I did not use it, because every
one of the nine rows is this lane's own record: its plan sentence, its probe, its knowledge
entry, its gate, its LOG. Routing them out would be false attribution, and the one sibling
whose craft touches them refuses them in writing:

- `kengaku|kengaku-shokunin|novelty + calibration (LLM and model research and evaluation)`
  (`/home/vgpnk/Projects/shokunin/shokunin.conf`, LANES block).
- `chousa-shokunin/PROVINCE.md`: "**Refuses:** … model-quality or evaluation claims
  (→ kengaku)". The prior-art row (R42-R3-36) is a novelty/evaluation claim, so chousa's
  "claim-vs-source verification" does not take it.
- `tameshi-shokunin/PROVINCE.md`: "**Refuses:** product domains — every lane's gate remains
  its own; tameshi owns only the reusable craft … Never edits a sibling's gate code."
  R45-S5-1's gate (`plans/anchor_line_check.py`) therefore stays here.

## Per-row evidence and measurements

### 54 — R42-R3-36 `plan-class-from-unfrozen-probe` → kengaku / accepted-risk

- Source `.ufo/waves/round-42/falsify/F42CritPlanNext.md:91`:
  "### D4 — coverage class sentence is asserted from a non-frozen host probe; prior-art hits
  exist for this exact task".
- The residual the row names (no dated prior-art receipt) is a **declared limit**, not a
  fix: `plans/round-43-claims.md:25-26` "…no novelty construct with a dated prior-art receipt
  is ready — `F42CritPlanNext` D4 found third-party uses of `feal_in_c.get_keys()` scoring,
  so no novelty is asserted here)"; `:119` "The class sentence carries no novelty claim
  (prior art: wave-1 item)."
- Check (preserved, cwd-prefixed): `cd "${LANE:?}" && ls corpus/evidence/round43/ | grep -q 'prior-art'`
  → **exit 1**. Verbatim lane state confirming the claim still stands:

```
$ ls corpus/evidence/round43/
feal-dry-cases-freeze.txt
feal-probe.txt
tb2-feal-differential-cryptanalysis
```

- `fixed-verified` is impossible (the check is red by design: the receipt is absent).
  `accepted-risk` is the honest value: the lane knows the residual and carries it under a
  written claims limit.

### 55 — R42-R3-37 `plan-host-dependent-cheat` → kengaku / accepted-risk

- Source `.ufo/waves/round-42/falsify/F42CritPlanNext.md:107`:
  "### D5 — `cheat-clock-seed` is glibc/platform-dependent; the "5/5" is a host result".
- The mechanism and the flag are in this lane's own files:
  `plans/feal_probe.py:144` `libc.srand(now + dt)`; `:194` `attack=CLOCK_SEED, host="libc-rand"),`;
  `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:291` "The key schedule is
  replayable from the clock (`cheat-clock-seed` `P`, `host=libc-rand`)"; the residual
  (re-derivation in the task image) is a declared limit — `plans/round-43-claims.md:115-116`
  "host python3 3.14, host gcc and host setuptools stand in for the image's python 3.13 under
  `uvx`, Debian gcc and setuptools 80.9.0; **the image is never pulled**".
- **Authored check** (row had `check: null`), one line, re-derives the row's claim — the cheat
  replays the C library schedule and both the probe and the entry carry the host flag:

```
cd "${LANE:?}" && grep -q 'host="libc-rand"' plans/feal_probe.py && grep -q "libc.srand" plans/feal_probe.py && grep -q "host=libc-rand" corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md
```

  Run in the scratch cwd under the counter's contract → **exit 0**. Not `fixed-verified`:
  the check confirms the mechanism and the recorded flag, not an image re-derivation, which
  the claims doc excludes.

### 56–59 — R42-R3-38/39/40/41 entry errata → kengaku / fixed-verified

- Sources `F42EntryQuotes.md:45,46,47,48` = items 1–4 of that file (entry:297, entry:311,
  entry:431, entry:433-434).
- Closes name the round-43 closure R1 errata plus `77ea425a`, which resolves:
  `git cat-file -t 77ea425a` → `commit`.
- Checks (preserved, cwd-prefixed) all **exit 0**; the errata they pin exist in
  `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`:

```
451:## Errata (round 43, closure R1; appended 2026-10-26, nothing above edited)
457:- **E1 `:296-298` (finding 7) — the `2^15` sentence.** Quote: …
465:- **E2 `:309-312` (finding 10) — stdin scope and locator.** Quote: …
477:- **E3 `:430-432` (integration, D2 bullet) — the padded rows' verdicts.** Quote: …
485:- **E4 `:433-434` — the labels under that counterfactual.** Quote: …
```

### 60 — R45-S5-1 `row-anchor-wrong-line` → kengaku / fixed-verified

- Source `corpus/lessons/round-45-verifier-spotcheck.md:145` item 1: "Supersede S152, S153,
  S154 under Q34 with correct anchor lines/ranges … add the anchor-line check to the gate
  with a red fixture". Close names `c1ec334c` (resolves: `git cat-file -t c1ec334c` →
  `commit`) and `plans/anchor_line_check.py` (`fd4129eb` resolves).
- Check `cd "${LANE:?}" && python3 plans/anchor_line_check.py --lane . >/dev/null` → **exit 0**.
  The gate's own verdict line (captured without the `>/dev/null`):

```
ANCHORLINE rows=170 cited=55 captured=51 uncaptured=4 defective=8 repaired=8 live=0 cells=0
```

  `live=0` is exactly the row's claim; the four `UNCAPTURED S093 S103 S104 S110` lines are
  the gate's own separate leg and do not bear on it.

### 61 — R45-S5-2 `predictor-lone-cr` → kengaku / fixed-verified

- Source `…round-45-verifier-spotcheck.md:147` item 2: "Mark or supersede the entry's
  `## Predictor` (lone-CR divergence; prose at `:150,:194` overclaims universal newline)".
  Close names `c1ec334c` and the round-46 leg B (`disagree=0` on 16 frozen newline states).
- Check (preserved, cwd-prefixed) → **exit 0**:

```
214:## Errata (round 46)
```

### 62 — R45-S5-3 `log-in-place-rewrite` → kengaku / fixed-verified

- Source `…round-45-verifier-spotcheck.md:149` item 3: "LOG.md: append a correction entry for
  the two in-place rewritten round-45 lines (D1); never rewrite committed LOG lines."
  Close names the round-46 LOG correction entry and `plans/log_appendonly.py --since 64ba8385 violations=0`.
- Check (preserved, cwd-prefixed) → **exit 0**:

```
1441:  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs byte-equal); V11 `states=48 grader_pass=18
```

## Fragment validation under the frozen counter

Exact command (the fragment lives under the lane, so `--ledger` can be lane-relative only
if resolved — see I3; I passed the absolute path):

```
$ python3 plans/round51_routing.py --lane . \
    --ledger "$PWD/.ufo/waves/round-51/w1/C2ExecG.jsonl" \
    --run-checks --scratch /fast/scratch/hyaku/kengaku-r51/C2ExecG/ctr
LEDGER .ufo/waves/round-51/w1/C2ExecG.jsonl rows=9
FIELDS complete=9 incomplete=0
OWNERS attributed=9 unattributed=0
DISPOSITIONS set=9 bad=0
SOURCES resolved=9 missing=0
CHECKS present=9 absent=0
VERIFIED ran=7 passed=7 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

Repeated in a **clean `--shared` clone** at the same revision (fragment copied into the
clone's wave dir; clone `git status --porcelain` shows only `?? .ufo/waves/round-51/w1/`),
same output, `exit=0` — the checks do not depend on the lane's working tree.

The frozen command on the untouched lane ledger still reproduces the before receipt exactly:

```
$ python3 plans/round51_routing.py --lane . --run-checks --scratch <scratch>/ctr-full2
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
exit=1
```

Identical to `.ufo/waves/round-51/claims/c2-before.txt`. Instrument selftest:
`python3 plans/round51_routing.py --selftest` → `[selftest] cases=11 failures=0` /
`[selftest] ALL PASS`, exit 0.

## Instrument findings for the L1 (routed; I did not edit the instrument)

**I1 — the counter's cwd contract breaks every existing check (highest landing risk).**
`check()` runs `subprocess.run(["bash","-lc",cmd], cwd=str(tmp), env={…,"LANE": lane})`, but
**all 61** non-empty ledger checks are lane-cwd-relative: `0` of them contain `cd ` or
`${LANE`. Measured from the counter's own cwd:

```
$ bash -lc "grep -qE '^## Errata \(round 46\)' corpus/knowledge/tb2-password-recovery-grader.md"
grep: corpus/knowledge/tb2-password-recovery-grader.md: No such file or directory   (exit 2)
$ bash -lc "python3 plans/anchor_line_check.py --lane ."
python3: can't open file '<scratch>/plans/anchor_line_check.py': [Errno 2] No such file or directory   (exit 2)
$ bash -lc "ls corpus/evidence/round43/ | grep -q 'prior-art'"
ls: cannot access 'corpus/evidence/round43/': No such file or directory   (exit 1)
```

Consequence: a row marked `fixed-verified` with its original check text reports
`CHECK_FAILED 1` even when the check is green in the lane. Fix one of: prefix every ledger
check with `cd "${LANE:?}" && ` (what my nine rows do), or run checks with `cwd=lane`.
Without this, C2 cannot reach `CHECK_FAILED 0` with `--run-checks`.

**I2 — `load_owners` reads nothing from `shokunin.conf`; the owner rule is a hardcoded list.**
`re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{", line)` finds **0** hits in the real conf
(the LANES block is `lane-id|repo|axes`), so the accepted set is exactly `FALLBACK_OWNERS`
(17 names, `kumitate` listed twice). Real fleet lanes are then rejected:

```
DETAIL OWNER X1 owner 'tsukuroi' not a fleet lane     (exit 1)
DETAIL OWNER X1 owner 'mado' not a fleet lane         (exit 1)
DETAIL OWNER X1 owner 'revenger' not a fleet lane     (exit 1)
DETAIL OWNER X1 owner 'lore' not a fleet lane         (exit 1)
```

`tsukuroi`, `mado`, `revenger`, `lore` (and `audio`, `game-dev-2d`, `game-dev-3d`) are all
fleet lanes in `shokunin.conf`. Any seat that attributes a row to one of them — the honest
answer for host-operability or compositor findings — fails the predicate. Fix: parse the
LANES block (`^([a-z0-9-]+)\|`).

**I3 — `--ledger` with a relative path crashes instead of measuring.** `lane` is
`.resolve()`d, `ledger` is not:

```
ValueError: '.ufo/waves/round-51/w1/C2ExecG.jsonl' is not in the subpath of '/home/vgpnk/…/kengaku-shokunin'
```

exit 1 with a traceback. The frozen command is unaffected; seats validating fragments must
pass an absolute path.

**I4 — no write fence on check execution.** A `fixed-verified` row whose check is
`touch "$LANE/PWNED-BY-CHECK"` passes the predicate and writes the lane. Demonstrated in a
synthetic fleet under my scratch (never the lane): `PREDICATE R51-C2 pass`, exit 0,
`lane write escaped: True`. The counter runs arbitrary shell with the lane exported as
`LANE`; nothing stops a check from mutating the surface it verifies.

**I5 — `fixed-historical` reads only the first close token.** `tok = close.split()[0].strip(",")`
— R42-R3-38's close begins `round-43 closure R1 entry erratum corpus/knowledge/…`, so
`tok="round-43"` → `CLOSE_REF … does not resolve` although the path later in the string
resolves. All four R42-R3-38..41 closes are of that shape; they are `fixed-verified` here,
so it does not bite my rows, but it will bite any row the L1 marks `fixed-historical`.

**I6 — cosmetic/conflation.** Status violations are appended to the `DISPOSITION` bucket, so
the printed `DISPOSITIONS bad=N` mixes two legs; `FALLBACK_OWNERS` repeats `kumitate`.

**I7 — design limit, not a bug.** `owner` is unverifiable mechanically: any accepted name
passes. The adjacency signal rests on the seat's evidence, which is why each owner above is
argued from a quoted charter line or the finding's own subject rather than from the counter.

## Observation (not mine to fix)

`corpus/routed-findings.jsonl` mtime moved during the wave (2026-10-28 15:22:02 -0300) and
`git status` briefly showed ` M plans/round42_c1_verify.py`, ` M plans/routed_open.py`,
` M plans/scratch_guard.py`; the content then matched HEAD again. Ledger hash before and
after all my runs, and equal to `git show HEAD:`:

```
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl
```

So a concurrent writer is touching lane files with identical bytes; my rows were measured
against that content and are unaffected.

## Limits

- Check strength varies and I did not strengthen the eight preserved checks (item scope:
  author only where `check` is empty). Row 61's check proves an `## Errata (round 46)` heading
  exists, not that the predictor is universal-newline; row 62's proves the LOG correction line
  exists, not that no other line was rewritten. Rows 56–59's checks pin the errata spans, not
  the errata's prose. `fixed-verified` here means exactly what the frozen predicate means:
  the row's recorded check exits 0 in this run.
- `accepted-risk` on rows 54 and 55 is a judgement that the residual is a *declared* limit
  (quoted above), not a claim that the residual is harmless. If the L1 prefers
  `refused-out-of-scope` for 54 (claims §Limits scopes novelty out), the evidence in this
  report supports either; `accepted-risk` is the closer fit because the lane carries the
  defect knowingly rather than declining the finding.
- I ran no image, no network probe, no lane gate as a gate; the only lane-code executions are
  the nine ledger checks plus the counter itself.
- No tool was installed or upgraded (nothing was needed).
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2ExecG` was removed before yield; nothing citable
  lives only in `/tmp`.

## Files written

- `.ufo/waves/round-51/w1/C2ExecG.jsonl` (fragment, 9 rows)
- `.ufo/waves/round-51/w1/C2ExecG.md` (this report)

No production file, no commit, no git mutation in the lane; the lane clone in my scratch was
`--shared` and is gone with the scratch dir.

VERDICT: rows 55–63 attributed — 9/9 owner `kengaku`, 7 `fixed-verified` (checks green in this run), 2 `accepted-risk` (rows 54, 55, residual quoted from the round-43 claims limits), 1 authored check (row 55); fragment passes the frozen counter in the lane and in a clean clone (`PREDICATE R51-C2 pass`, exit 0); six instrument defects routed to the L1, I1 (checks run in a scratch cwd while all 61 existing checks are lane-cwd-relative) and I2 (owner set is a hardcoded fallback, conf contributes 0 owners) are the two that can block the landing.
