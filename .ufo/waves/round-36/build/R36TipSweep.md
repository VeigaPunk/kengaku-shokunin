# R36TipSweep — no-harm baseline before landing (round 36, wave 1)

Seat: R36TipSweep (executor, leaf). Date: 2026-10-25.
Scope: pre-landing baseline of the ten standing gates at the lane tip. No lane file was modified; all writes are in
`.ufo/waves/round-36/build/R36TipSweep/` plus one `mktemp` fixture.

**VERDICT: tip-sweep-10/10** — all ten baseline commands are green at the lane tip, in a clean clone of committed
state. The only red things are the two round-36 targets, which are exactly what this wave must flip (`C1`/`C2` below).

## 1. What was measured, and against what

| item | value | evidence |
|---|---|---|
| lane | `/home/vgpnk/Projects/shokunin/kengaku-shokunin` | — |
| lane tip at measurement | `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd` ("round-36: wave-1 spec and dispatch (40 seats)") | `git rev-parse HEAD` |
| freeze commit | `3241b86cde0e9a3b9363a0d4c7fff12ec5d5f5e2`, Amendment 1 `acbda2f3936838ba4849f14937fbecb8aed461e5` | `git merge-base --is-ancestor 3241b86… HEAD` → 0; `git rev-list --count 3241b86..HEAD` → `2` |
| tip position | tip = freeze + amendment 1 + wave-1 spec/dispatch commit; no implementation commit yet | `git log --oneline -6` |
| pre-landing target | `plans/pkg_gate.py` **absent** at tip (`ls` → *No such file or directory*) | — |
| disk of the run | `/tmp/k36-tip-3fb3/lane` (fixture; removed at end of seat) | — |
| host | python `3.14.8`, `git version 2.56.0`, kernel `7.2.11-arch1-1` | `python3 --version`, `git --version`, `uname -r` |
| installs this seat | none (pacman untouched; `bc` is absent, timings use bash integer arithmetic instead) | — |

Fixture construction (per the seat fixture rule; every git call names `-C "$D/lane"`, `master` checked out, no commit):

```
D=$(mktemp -d /tmp/k36-tip-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md /grader.py /SKILL.md \
  /PROVINCE.md /LOG.md /README.md /AGENTS.md /SHONEN.md /.ufo/waves/round-34 /.ufo/waves/round-35 \
  /.ufo/waves/round-26 /considerthese
git -C "$D/lane" checkout -q master
git -C "$D/lane" rev-parse --show-toplevel      # → /tmp/k36-tip-3fb3/lane   (asserted == "$D/lane")
git -C "$D/lane" rev-parse HEAD                 # → f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd (== lane tip)
```

Because the clone is `--no-checkout` + sparse of **committed** state, a green result here also proves none of the ten
gates depends on an uncommitted/ignored working-tree file.

## 2. Result table (green = 10, red = 0)

Driver used verbatim for all rows (saved at `.ufo/waves/round-36/build/R36TipSweep/run_sweep.sh`): each command runs
with cwd = clone root, exit code and last non-empty output line captured; full logs also kept in this seat dir.

| # | command | rc | last output line |
|---|---|---|---|
| 1 | `python3 grader.py` | 0 | `VERDICT: PASS — stored evidence fully re-derives offline` |
| 2 | `python3 grader.py --selftest` | 0 | `[selftest] ALL PASS` |
| 3 | `python3 plans/defect_ledger.py --lane .` | 0 | `PREDICATE C2 pass` |
| 4 | `python3 plans/round35_c1_verify.py --lane .` | 0 | `PREDICATE C1 pass` |
| 5 | `python3 plans/round35_hardening.py --lane . --skip H6` | 0 | `hardening run=5 failed=0` |
| 6 | `python3 plans/state_check.py --summary` | 0 | `VERDICT: PASS — all comparable frozen assertions match` |
| 7 | `python3 plans/registry_check.py --summary` | 0 | `TOTAL source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0 exit=0` |
| 8 | `python3 plans/benchmark_spec_audit.py --summary` | 0 | `TOTAL task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16 program_html_targets=651 findings=0 exit=0` |
| 9 | `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0` |
| 10 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | 0 | `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` |

Row 6 detail (fuller line, run 2 log): `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`.

Per-command wall time, same clone, one pass (ms):

```
grader.py 418 | grader --selftest 3846 | defect_ledger 125 | round35_c1_verify 1796 | round35_hardening 130
state_check 2426 | registry_check 149 | benchmark_spec_audit 142 | config_projection 360 | sources-census 834
total 10249ms
```

Operability: one ~10.2 s pass, no network, no writes into the tree (see §5).

## 3. Determinism / repeat evidence

Three independent executions at the same commit: run A (sparse set without `/.ufo/waves/round-26`), run B (sparse set
with it), run C (timing pass). Run A vs run B:

```
diff <(cut -f1,2 runA.tsv) <(cut -f1,2 runB.tsv)
< state_check	1
---
> state_check	0
```

i.e. rows 1–5 and 7–10 produced identical rc in every run; only row 6 moved, and for a clone-content reason, not
lane content (§4). Evidence files kept: `k36-tipsweep-results.tsv` (run A), `k36-tipsweep-results2.tsv` (run B).

## 4. The one red, diagnosed as a clone artifact (not a lane condition) — actionable for other seats

Run A, with the exact sparse pattern list I was given, row 6 failed:

```
rc=1
assertions=329 match=309 mismatch=9 superseded=6 offline_unverifiable=5
MISMATCH: P4c.build.seats:87  …  {"assignment_names": null, "lesson": ["72","72"], "spec_assignment_match": false, "spec_items": null}
MISMATCH: P4c.build.role-mix:87 / P4c.build.reports:89 (report_count=0)
MISMATCH: P4c.falsify.seats:118 / role-mix:118 / dead-seats:119 (dead_file_count=null) / reports:120 (returned_reports=0)
MISMATCH: P4c.round.total-136:121 / total-139:121
VERDICT: FAIL — at least one frozen assertion mismatches
```

Cause: every mismatch is a `P4c` assertion whose `spec`/`assignment_names`/`report_count` fields are `null`, i.e.
`plans/state_check.py` could not find the round-26 wave records — `P4c` reads
`.ufo/waves/round-26/{build-spec.json, build-assignments.json, falsify-assignments.json, falsify-dead-seats.json}` and
the round-26 report files. That path was absent from my prescribed sparse list. Adding `/.ufo/waves/round-26` and
re-running gave rc=0 with `mismatch=0` (the 9 mismatches moved to `match`: 309 → 318, same 329 assertions).
No run created or modified anything in the clone (`git -C … status --porcelain` empty after all runs).

**Recommendation for the L1:** the fixture pattern list handed to seats should include `/.ufo/waves/round-26`
(the round-25/26 lesson rows are part of the frozen assertion population). Otherwise every seat using the given
pattern list will see a spurious `state_check` FAIL and may report a false pre-existing defect.

## 5. Pre-landing state of the two round-36 targets (the wave's exit criterion)

At the same tip (`f9efce3`), in the same clone:

| counter | rc | terminal lines |
|---|---|---|
| `python3 plans/round36_c1_verify.py --lane .` | **1** | `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14` / `rows=4 closed=0 observed_pass=0 mismatches=0` / `PREDICATE C1 fail` |
| `python3 plans/round36_c2_verify.py --lane .` | **1** | `W2 DEFECT S108 present 0 times`, `W3 DEFECT entry absent`, `W4 DEFECT index row absent or missing S108/S109/S110`, `W5 DEFECT entry absent` / `checks=6 defects=4` / `PREDICATE C2 fail` |

C1's 14 fixtures are all `observed=unevaluated` (P0–P7, L1–L6) because `plans/pkg_gate.py` does not exist yet; the four
routed defects are all still open at the tip (`R35-D1..D4 status=open observed=fail agree=yes`). So the baseline is:
**10/10 pre-existing gates green, 0/2 round-36 targets green** — landing must flip C1 and C2 to green *without*
disturbing rows 1–10 of §2. In particular the freeze `false_green=0 false_red=0` for the C1 battery and `W1/W6 ok`
for C2 already hold; the red is entirely "not built yet".

## 6. Tree-state discipline

- `git -C clone status --porcelain` → empty after all ten runs and after the counter runs (no command writes into
  the tree; the counters only read).
- No lane file was written by this seat. Lane `git status --porcelain` shows only siblings' wave scratch
  (`?? .ufo/waves/round-36/build.ready`, `?? .ufo/waves/round-36/build/`, `?? .ufo/waves/round-36/integrate/`);
  lane `HEAD` is still `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd`.
- The fixture clone `/tmp/k36-tip-3fb3` was removed with `rm -rf` at the end of this seat.

## 7. Risks / notes

- [INFERENCE] The baseline is commit-pinned: if a wave-1 sibling lands `plans/pkg_gate.py` (or edits `plans/` checks)
  mid-wave, re-running these ten is the integration gate, not a defect of that landing. Numbers here are only valid at
  `f9efce3`.
- `grader.py --selftest` (3.85 s) and `state_check` (2.43 s) dominate the 10.2 s pass; both are read-only, so the whole
  baseline can be re-run cheaply after integration.
- `sources-census.sh` is the only command whose executable lives outside the lane
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), and it was invoked read-only against the fleet root; it does
  not write to the source repo.
- `bc` is not installed on this host; timing used bash arithmetic. No install performed (not needed for the baseline).
- No files under `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md` or `SHONEN.md`
  were touched, and no git index/mutating command was run in the lane.

VERDICT: tip-sweep-10/10
