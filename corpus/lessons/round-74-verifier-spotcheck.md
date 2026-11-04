# Round 74 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · lane-round 74 · base `b7910802549978404218937d4be6a75acae0e020` → tip `cbb8b8d802ec68240b6bb78ec7c9cd96a5e94b87`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-74/kengaku.md` (fleet commit `576a03b25976d8d75615bdb44980916ec2519782`, author `kengaku-shokunin <kengaku@shokunin.local>`)
watchdog digest (mutable `.ufo/watchdog.log`, copied at closure; lines 2213/2216):
`2026-11-04T00:23:39-03:00 launch kengaku round=74 pgid=988818 driver=hyaku-inline attempt=1` ·
`2026-11-04T01:05:40-03:00 complete kengaku round=74; hyaku-inline attempt=1`

I did not author this round. Numbers below were re-derived from committed bytes at `cbb8b8d8` with
plain measurement (grep/awk/git/independent parse); lane-owned gates and selftests were checked by
their committed receipts and code, never executed (PROTOCOL §Gate standard, Closure consequence).

## 1. Step-1 conformance

| check | command / observation | result |
|---|---|---|
| report authored by the lane identity | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-74/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> 576a03b2…`; ancestor of fleet `origin/master` | pass |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; four `[~]` lines = the four `SHONEN.md` boxes, each with a pointer | pass |
| cited commits exist and are ancestors | `git merge-base --is-ancestor <h> master` for `cbb8b8d8`, `74e2e15a`, `cea7ebf3`, `f4d651c5` → all yes; `git ls-remote origin refs/heads/master` → `cbb8b8d8…` | pass |
| lane clean / pushed | `jj-lane.sh state` → `branch=master local=remote=cbb8b8d8 ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty | pass |
| prompt carries the template contract | rendered `templates/round-prompt.md` §1–5 (lane/round/fleet-root/axes/working-dir substitutions) vs `.ufo/prompts/kengaku-round-74.md` §1–5 → byte-identical; §6 hyaku addendum present; all five child-lane items present (report path, commit-then-push, `SHONEN` heading, hash-citation rule, write scope) | pass |
| L2 route map | prompt's net map ("only reviewer `@m_zfl`; every other role `@m_flash`") = `~/.omp/agent/config.yml` `task.agentModelOverrides` exactly | pass |
| wave shape | `w1-validate.rc` → `rc=0`; one v1 wave, 16 seats: executor 4, reviewer 3, critic 2, scribe 2, scout 2, connector 1, mutation-tester 1, sentinel 1; attack 6/16 = 37.5 %; connector 1; `w1-results.json` 16 results, 4 returned reports / 12 empty settled seats (all 12 named in the report) | pass |
| planner seat | record in `plans/round-74-claims.md`: L1 holds the canonical planner seat; data-walk rode `RoundStateScoutR74` (scout) | pass (claims doc; report omits the line) |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN — present and ordered; not a marker | pass |

**Conformance defects (status-neutral; routed in §6):** the prompt commit `9ad48df4` is authored by
`kengaku-shokunin` although prompt-commit duty is the integrator's (durable, attribution only); the
report does not itself state the L1-holds-planner mapping (it is in the claims doc); the receipts'
revision labelling and two reference-drift assertions are defective (§2, R74-D1–D3).

## 2. Per-claim re-check

Method note: both claims rest on lane-owned instruments (`plans/round74_c1_registry.py`,
`plans/round74_c2_registry_audit.py`). I did not execute either gate. I re-parsed the committed
registry/claims bytes with my own code for the clean-tree tallies, and evidence-verified the
selftest/mutant/control receipts and the revision they claim.

### R74-C1 / coverage — verifies (re-measured at the landing tip)

Independent re-parse over committed bytes at `cbb8b8d8` (8-cell registry rule; decoupled file set =
`SCORECARD.md`, `LOG.md`, `corpus/README.md`, `SKILL.md` outside the registry block,
`corpus/knowledge/*.md`, `plans/*.md`):

```
$ ( ls SCORECARD.md LOG.md corpus/README.md; \
    awk '/^## Gate\/probe registry/{s=1;next} s&&/^## /{s=0} !s' SKILL.md; \
    cat corpus/knowledge/*.md plans/*.md ) | wc -l
136
$ { …same set… } | grep -oE 'python3 (plans/[A-Za-z0-9_.-]+\.py|grader\.py|corpus/evidence/round13-coverage/coverage_census\.py)' \
  | sed 's/^python3 //' | sort -u | while read -r p; do [ -e "$p" ] && echo "$p"; done | wc -l
116
$ grep -hoE 'python3 (plans/[A-Za-z0-9_.-]+\.py|grader\.py|corpus/evidence/round13-coverage/coverage_census\.py)' plans/*.md \
  | sed 's/^python3 //' | sort -u | while read -r p; do [ -e "$p" ] && echo "$p"; done | wc -l
90
$ awk '/^## Gate\/probe registry/{f=1;next} f&&/^## /{exit} f' SKILL.md | grep -c '^| `'
116        # base b7910802: 114
```

My independent 8-cell parse: `REGISTERED total=116 rows=116`, `ADVERTISED total=116`, `MISSING 0`,
`INCOMPLETE 0`, `ENTRY-MISSING 0`, `DUPLICATE 0`, `SELFTEST-UNBACKED 0`; `plans_seen=90`. Every
required line of the frozen sentence is present at the landing tip, rc 0. Receipt `c1-after.txt`
agrees line-for-line.

*Before / control (evidence-verified, not executed):* `c1-before.txt` = legacy `files=78`,
`ADVERTISED 115`, `REGISTERED 115 rows=116`, `MISSING 0`, `PREDICATE R52-C2 pass`,
`PREDICATE R74-C1 fail`, rc 1. `c1-control-decoupled.txt`: a row dropped from a plans/*.md-only
fixture gives decoupled `MISSING 1` rc 1 while legacy drops it from both sides (`MISSING 0`,
`R52-C2 pass`) — the decoupling discriminates. `c1-selftest.txt`: `cases=4 failures=0`, rc 0.
C1GateReplayR74 replayed all three commands independently (byte-identical outputs).

**Defect found in the before receipt (R74-D1).** `c1-before.txt` is committed at the freeze commit
`f4d651c5`, whose `SKILL.md` has **114** registry rows (independent parse) — a tree-faithful legacy
run cannot print `rows=116`. C1GateReplayR74's own scratch replay measured `f4d651c5` at
`ADVERTISED 113`, `MISSING 0`; my legacy re-parse at the landing tip prints exactly
`78/115/115/rows 116/MISSING 0`. The receipt is therefore a pre-commit-worktree/landing-tree run,
not the freeze base, and Amendment A1's phrase "measured … at the freeze base" is false. This does
not falsify the claim — the after predicate re-derives at the committed tip and the control
discriminates — but the receipt cannot be cited as a freeze-base measurement.

### R74-C2 / calibration — verifies (re-measured at the landing tip)

Independent re-parse over committed bytes at `cbb8b8d8` (same 8-cell rule; entry-script regex as
documented; `ast.parse` of every entry script):

```
ROWS 116  MALFORMED 0  SCRIPTS 116  PARSED 116  FAILED 0  DUPLICATES []  EMPTY_CELLS 0
bad_kind []  bad_owner []  no_script []  unbacked_entry []
ERRATA_ITEMS 2  c80fcdb3 in item 1  d8a77d3f in item 2
```

`c2-after.txt` prints the same `INSTRUMENTS total=116 derived=registry rows=116`,
`PARSED scripts=116 failed=0`, `D1–D4 ok n=0`, `MALFORMED ok n=0`, `MISMATCH 0`, `DEFECTS n=0`,
`PREDICATE R74-C2 pass`, rc 0.

*Before / control (evidence-verified, not executed):* `c2-red-before.txt` runs both audits on the
same 9-cell malformed fixture: round-73 audit `MISMATCH 0` rc 0 (silent skip), round-74 audit
`MALFORMED defect n=1`, `MISMATCH 1` rc 1. The silent skip is confirmed in committed code
(`plans/round73_c2_registry_audit.py:85-86`), and the four blind spots are implemented in
`plans/round74_c2_registry_audit.py` (malformed-row reporting; `command_flags` checked against the
script body; self-test runner existence; `check_errata` over every matching item).
`c2-controls.txt`: `SELFTEST arms=4 red=3 ok=True`; `MUTANTS total=7 killed=7 survived=0 invalid=0
null_detected=1`; `c2-control-malformed-tuple.txt` repeats the discriminating red.

**Defect found in the control tallies (R74-D4).** `--selftest` prints a hard-coded `red=3`
(`plans/round74_c2_registry_audit.py:373`) and `--mutants` prints hard-coded `invalid=0
null_detected=1` (`:410`); each mutant is counted killed on *any* defect, not the expected
finding-id (`:388-406`), and no null arm is run. The four selftest arms do assert their specific
finding ids and `ok` is derived from `fails`, so the claim's frozen print still holds — but the
mutant tally is weaker evidence than "7/7 killed" reads.

### Re-measured vs evidence-verified

- **Re-measured by me:** C1 after tallies and registry-row counts (base 114 → tip 116), C2 clean-tree
  tallies, the S250 capture digest/size/line, `SOURCES.md` row counts 241 → 242, census validate,
  commit ancestry, SCORECARD diff scope, the lane diff (42 files, +5192/−1), wave counts, prompt
  fidelity, `PROVINCE.md` unchanged.
- **Evidence-verified, not executed:** both selftest tallies, the C2 mutant run, the legacy before
  receipt, both control receipts, the red-before fixture runs, and the seat replays.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C1's frozen predicate re-derives at `cbb8b8d8` (decoupled 136 files / 116 advertised / 116 registered, all six legs 0, rc 0) and the control discriminates (decoupled MISSING 1 vs legacy false green); the hyphenated-path fix is real for `plans/*.py` and the census literal. Score held at **7** by the open L0 cap (`kengaku | round-25/33/51`). |
| calibration | **improved** | C2's predicate re-derives (116 rows / 116 parsed / 0 malformed / 0 mismatches) and the red-before discriminates on identical fixture bytes; the round-73 silent skip is closed. Score held at **10**, exercised. |
| depth | unchanged | one held candidate + one tier-A row; no admitted entry; score 10 held |
| operability | unchanged | two new in-repo gates with selftest receipts; score 10 held |
| freshness | unchanged | S250 fetched live with byte-identical re-fetch; score 10 held |
| adjacency | unchanged | sibling-scan seat died; no new arbitrations; score 9 held |
| novelty | unchanged | instrument repair, no new construct claimed; score 8 held |

No owned axis harmed: `git diff b7910802 cbb8b8d8 -- SCORECARD.md` is a single appended round-74
section (37 insertions), every prior score row untouched; `PROVINCE.md` unchanged; the whole lane
diff is 42 files, +5192/−1, the single deletion being the documented `SKILL.md` line-17 census
sentence. **Defect (R74-D3):** the SCORECARD's "deletion column is 0 on this round's files" is false
(`SKILL.md` numstat is `3 1`; total deletions 1) — the report's SHONEN Box 2 itself says 1.

## 4. Discernment spot-check (LEARNING.md — from outside)

| item | lane decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S250 — Python 3.15.2 `argparse` documentation | **admit**, tier A, scope limited to command-line flag/option-string specification | live `https://docs.python.org/3/library/argparse.html#name-or-flags` re-fetched: HTTP 200, **334994 B**, sha256 `ad9095cd…b5b8d` — byte-identical to `corpus/evidence/round74/sources/argparse-docs.html`; page title "Python 3.15.2 documentation"; quote present at capture line 908 | **agree** | the 24-word quote is verbatim and located; the scope is correctly narrowed to option-string specification, not parser behaviour; tier A is right for official docs on their own scope |
| "Presence of a flag string in a script body proves `argparse` acceptance" | **reject** (flip: controlled `--help`/`--<flag>` execution or AST verification of `parser.add_argument()`) | same source: "The `add_argument()` method must know whether an optional argument … or a positional argument … is expected. The first arguments passed to `add_argument()` must therefore be either a series of flags, or a simple argument name"; "Action objects are used by an ArgumentParser to represent the information needed to parse a single argument…" | **agree** | registration/action info is what makes an option accepted; a raw string in the file proves neither registration, parser configuration, nor runtime execution. The flip is the correct repair (and is what D2's `entry:unbacked-flag` does structurally) |
| S250 `SOURCES.md` row quote | new row, `mined`, `used-by` lesson + held entry | `corpus/SOURCES.md:266`; capture line 908; `git diff b7910802 cbb8b8d8 -- corpus/SOURCES.md` → `1 0` | **agree** | 24 words (≤25), located (line 908 + anchor + sha256), no in-place status/recheck rewrite; census-clean |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ rc 0, `ok`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **242**
(base `b7910802` → 241); 25 `W04` in both committed census receipts (same 25 pre-existing
across-scope duplicates). Spot-check axis grades: admit agree, reject agree.

## 5. Trend verdicts

- **expansion: unchanged.** One new tier-A row (241 → 242, re-counted), no admitted `knowledge/`
  entry (the round-74 candidate is `admission: hold`), no frontier-to-core move, no capability row.
  The lane's own verdict stands.
- **quality: improved.** Two instruments supersede weaker versions: the registry gate is no longer
  circularly self-advertised and the audit prices all four round-73 blind spots (malformed rows,
  unbacked entry flags, absent self-test runners, contradictory errata) with a discriminating
  red-before; no admitted entry fails a re-check. Residual (R74-D4) is the mutant/selftest tally
  derivation and two reference-drift assertions (R74-D2/D3), routed below.
- **discernment: improved.** This outside check agrees with the gate on both the admit and the
  reject (§4), which is LEARNING.md's criterion; the lane also recorded its 12 dead seats by name and
  mined its own receipt-fidelity and reference-drift misses (M74-6/M74-7) with fixes rather than
  smoothing them. The remaining stale lesson line (R74-D2) is routed, not denied.

## 6. Routed defects and operator note

- **R74-D1 (evidence/revision) — routed.** `c1-before.txt` / `c1-after.txt` / `c2-after.txt` carry no
  measured-revision line, and were produced over a pre-commit worktree: at the freeze commit
  `f4d651c5` the registry has 114 rows, yet the receipts print `rows=116` (the rows landed only in
  `cbb8b8d8`). Amendment A1's "at the freeze base" is false, and C1GateReplayR74's own replay
  (`f4d651c5`: `ADVERTISED 113`) contradicts it. Fix: generate receipts from a clean clone at a
  named revision, stamp `LANE_TIP`, and append A2 restating the before as the landing-tree legacy
  mode.
- **R74-D2 (reference sweep) — routed.** `corpus/lessons/round-74.md:51` still says the C1 Before
  receipt shows `MISSING 5`; the receipt says `MISSING 0`. M74-6 claims the A1 correction but the
  sweep missed the lesson's own measurements section (PROTOCOL §Evidence standard, "corrections sweep
  every mention").
- **R74-D3 (self-assessment) — routed.** `SCORECARD.md` round-74 section says `` `git diff --numstat
  b7910802 master` deletion column is 0 on this round's files ``; actual is `SKILL.md 3 1`, total
  deletions 1. Append a correction naming the line-17 edit.
- **R74-D4 (gate self-test) — routed.** `plans/round74_c2_registry_audit.py` prints literal
  `red=3` / `invalid=0` / `null_detected=1` and counts a mutant killed on any defect rather than its
  expected finding-id; add a real null arm and derive the tallies.
- **R74-D5 (frontier sourced-claim) — routed.** S250 grounds a *held* entry, not a round claim; no
  C1/C2 evidence cites `S###`. The frontier step's "at least one sourced claim" item is therefore
  unmet — cite S250 in the claim evidence or state the gap next round.
- **Conformance note only.** Prompt commit `9ad48df4` is lane-authored (integrator duty, durable);
  the report does not itself record the L1-holds-planner mapping (it is in
  `plans/round-74-claims.md`). Neither bars admission.
- **For the operator (promotion-owned, never closure):** all four `SHONEN` boxes remain `[~]`
  lane-asserted. Boxes 2 (claim sizing) and 4 (lane hygiene) look fully checkable by a non-author
  now — claim predicates/controls are frozen and re-derivable, dead seats named, lane clean. Box 1's
  best evidence is two gates with selftest receipts under the D4 caveat; box 3's registry rows are
  verified but the finding-id gap R74-D4 keeps it short of a mechanical pass.
