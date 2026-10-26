# Round-41 falsify — F41MutBattery (fixture-level mutants of `plans/battery41`)

Seat: F41MutBattery (mutation-tester, leaf). Date: 2026-10-26. Lane tip cloned: `d7c77895752a2a5f317fa22f2362416ada50a04b`
(wave-2 dispatch on top of `3d0058fb`; the seven `plans/battery41/*.py`, `plans/round41_c1_verify.py` and both pinned
tools are byte-identical to `3d0058f` and `74513c0` for these paths — digests below).

## Question

Does the C1 counter flag a battery fixture whose demonstrated behaviour is broken? For each of the 48 fixtures I
built one mutant that breaks what it demonstrates — wrong `defects` set, wrong `expect`, trigger input removed, or
probe-stub bytes changed — applied to a scratch copy of the whole battery, and ran the frozen counter against it
with `--battery-dir`. Catch criteria per tasking: a `WRONG` line, a mutant flipping to SURVIVED, or `SETUP`.

## Method

- Scratch (only writes outside the report dir): `S=/fast/scratch/hyaku/kengaku-r41/F41MutBattery`;
  `git clone -q --shared` of the lane → `$S/lane`; `git -C $S/lane rev-parse --show-toplevel` = `$S/lane` verified.
- Every counter run inside the orchestrator envelope:
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 plans/round41_c1_verify.py --lane . [--battery-dir $S/bat/<fid>] --work $S/work-… --jobs 16`
- Pristine baseline: full pass on the clone battery → `runs/base.txt`, 4 s wall, rc 0.
- Mutants: per fixture a copy `bat/<fid>/` of all seven modules with one byte replacement in the fixture's module
  (uniqueness asserted, `count(old)==1`; full old→new list: `mutations.md`). 48/48 built; 3 first attempts were
  mis-built (two left a stray `[` → SyntaxError, one referenced `pkg` instead of `_pkg`) — those produced SETUP and
  were rebuilt before classification; their final runs are the ones recorded here.
- Per mutated battery one FULL counter pass (all 23 mutants, no `--only`), ~4 s each → `runs/mut-<fid>.txt`.

## Baseline (pristine, clean clone)

`runs/base.txt` tail: `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0` / `MUTANTS total=23 killed=23
survived=0 invalid=0 null_detected=0` / `MUTANTS-BY-TOOL receipts=13/13 sources=10/10` / `PREDICATE C1 pass`, rc 0 —
reproduces `.ufo/waves/round-41/integrate/measure-final.txt`. First-killers (from the same run): every mutant except
T04 has ≥2 killer fixtures (the battery's two-triggers-per-branch design); T04's sole killer is
`r_run-t04-temp-paths-masked`.

## Result: 43/48 caught, 5 survived with a fully green counter

Caught: 42 by the `FIXTURE … WRONG` sanity line, 1 by `SETUP` (defects-contract breach), plus one double catch
(`r_run-t04-temp-paths-masked`: WRONG **and** T04 flipped to SURVIVED — the only sole-killer fixture).

| fixture | kind | caught by | observed after mutation |
|---|---|---|---|
| r_ctl-t06-empty-equal-receipt | stub-bytes | WRONG | rc=1 obs=differ:corpus/evidence/round41/r-ctl-probe.txt |
| r_ctl-t06-tamper-on-skipped | trigger-removed | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/round41/r-ctl-probe.txt |
| r_ctl-t08-derived-uv-absent | expect-flip | WRONG | rc=0 obs=control:differ,equal:…tb2-grader-probe.txt,skip:… |
| r_ctl-t08-table-uv-absent | trigger-removed | WRONG | rc=0 obs=control:differ,equal:…regex-log-probe.txt,equal:…pmars… |
| r_map-t09-shared-stem-case-fold | trigger-removed | WRONG | rc=0 obs=map:corpus/evidence/r/foo-probe.txt:derived |
| r_map-t09-shared-stem-separators | defects-drop | WRONG | rc=0 obs=skip:…foo-probe.txt:no-committed-re-run-command |
| r_map-t10-derived-deep-layout | defects-drop | WRONG | rc=0 obs=map:…scheduling/foo-probe.txt:derived |
| r_map-t10-derived-mapping | trigger-removed | WRONG | rc=0 obs=- (receipt deleted) |
| r_map-t10-derived-with-table-sibling | defects-add | WRONG | rc=0 obs=map:…derived,map:…table,equal(bogus) mismatch |
| r_map-t11-table-near-stem-decoy | trigger-removed | **survived** | rc=0 obs=map:…tb2-grader-probe.txt:table |
| r_map-t11-table-overrides-derived | trigger-removed | **survived** | rc=0 obs=map:…tb2…:table,map:…pmars…:table |
| r_map-t12-log-derived | trigger-removed | WRONG | rc=0 obs=skip:…foo-probe.log:no-committed-re-run-command |
| r_map-t12-log-population | defects-drop | WRONG | rc=0 obs=skip:…foo-probe.log:no-committed-re-run-command |
| r_map-t12-log-with-table-sibling | trigger-removed | **survived** | rc=0 obs=map:…table,skip:…foo-probe.log:… |
| r_run-t03-rc-nonzero-mixed | trigger-removed | WRONG | rc=0 obs=control:differ,equal:census,equal:rc-ledger |
| r_run-t03-rc-nonzero-single | expect-flip | WRONG | rc=1 obs=differ:…audit-probe.txt |
| r_run-t04-temp-paths-masked | stub-bytes | WRONG,SURVIVED:T04 | rc=1 obs=differ:…regex-log-probe-first-run.txt |
| r_run-t13-auto-control-differ | trigger-removed | WRONG | rc=1 obs=control:differ,differ:stable-census,equal:slot-audit |
| r_setup-t01-lane-absent | trigger-removed | **survived** | rc=2 obs=- |
| r_setup-t01-not-a-repo | trigger-removed | WRONG | rc=0 obs=map:…foo-probe.txt:derived |
| r_setup-t02-evidence-is-file | expect-flip | WRONG | rc=2 obs=- |
| r_setup-t02-no-evidence | trigger-removed | WRONG | rc=0 obs=map:…foo-probe.txt:derived |
| r_setup-t05-tamper-absent | trigger-removed | WRONG | rc=0 obs=control:differ,equal:…foo-probe.txt |
| r_setup-t05-tamper-unmapped | trigger-removed | WRONG | rc=1 obs=control:unavailable,equal…,skip… |
| r_setup-t07-lane-subdir | trigger-removed | **survived** | rc=2 obs=- |
| r_setup-t07-nested-lane | expect-flip | WRONG | rc=2 obs=- |
| s_exit-absent-id | trigger-removed | WRONG | rc=0 |
| s_exit-attest-opened | trigger-removed | WRONG | rc=5 |
| s_exit-collision-admit | trigger-removed | WRONG | rc=0 |
| s_exit-collision-indented | trigger-removed | WRONG | rc=0 |
| s_exit-opened-elsewhere | trigger-removed | WRONG | rc=0 |
| s_exit-queued-admit | trigger-removed | WRONG | rc=0 |
| s_modes-s01-quote-plus-package | trigger-removed | WRONG | rc=0 |
| s_modes-s01-quote-plus-registry-and-package | trigger-removed | WRONG | rc=0 |
| s_modes-s04-url-map-with-adopt | trigger-removed | WRONG | rc=0 |
| s_modes-s04-url-map-with-check-only | expect-flip | WRONG | rc=2 |
| s_modes-s08-artifact-without-quote-file | trigger-removed | WRONG | rc=0 |
| s_modes-s08-quote-file-without-artifact | trigger-removed | WRONG | rc=0 |
| s_modes-s09-url-map-directory | trigger-removed | WRONG | rc=9 |
| s_modes-s09-url-map-nested-shape | trigger-removed | WRONG | rc=0 |
| s_usage-02-package-without-registry | trigger-removed | WRONG | rc=0 |
| s_usage-02-registry-without-package | trigger-removed | WRONG | rc=0 |
| s_usage-03-dotted-access-date | defects-breach | SETUP | contract refusal (non-empty defects on sources) |
| s_usage-03-single-digit-month-duplicate-request | trigger-removed | WRONG | rc=5 |
| s_usage-05-empty-entries-value | expect-flip | WRONG | rc=2 |
| s_usage-05-two-ids-without-entries | trigger-removed | WRONG | rc=0 |
| s_usage-06-recheck-cadence-word | trigger-removed | WRONG | rc=0 |
| s_usage-06-recheck-prose-scoped-row | trigger-removed | WRONG | rc=0 |

(Each row's evidence: `runs/mut-<fid>.txt`; the exact byte replacement: `mutations.md`.)

## The five survivors — coverage findings, not contract changes

In all five runs every counter line equals the pristine baseline: `BATTERY fixtures=48 wrong=0 tampered=0
sidechannel=0` and `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`; dev-mode exit 0. A broken
battery passes unnoticed.

1. **r_setup-t01-lane-absent** — `listing(d / "absent")` → `listing(d)`: the absent-lane trigger is gone, but the
   tool now dies in `lane_root()`'s not-a-repo `die()` with the same rc 2 and no receipt lines. The distinguishing
   `SETUP: --lane …` stdout message is not captured by `classes()`, so the fixture sanity check sees an identical
   result. T01 still kills here (its `die()` mutation exits 0 whichever check fires).
2. **r_setup-t07-lane-subdir** — `listing(root / "sub")` → `listing(root)`: the work-tree-root trigger is gone; the
   tool exits 2 one check later (no `corpus/evidence` at the root). Same rc-2-with-no-classes blindness as (1).
3. **r_map-t11-table-near-stem-decoy** — deleted the `_v2` near-stem decoy script the fixture exists to reject:
   `--list` classification is unchanged, so no WRONG; T11 is still killed by its sibling fixture, so no flip.
4. **r_map-t11-table-overrides-derived** — deleted `plans/tb2_grader_probe.py`, the script whose existence creates
   the derived-match the table overrides: `--list` never resolves scripts (`usage_argv` is only reached in the run
   path), so `probe-script-absent` cannot surface in list mode and `origin=table` still prints. No WRONG, no flip.
5. **r_map-t12-log-with-table-sibling** — deleted the near-stem decoy `plans/foo_probe_v2.py`; classification
   unchanged, sibling still kills T12. No WRONG, no flip.

### What holds / what breaks

- Holds: the fixture sanity line catches every declaration-level corruption (defects edits, expect flips: 13/13)
  and every mutation that changes the reference result; SETUP catches contract breaches; the mutant-flip net caught
  the one sole-killer fixture (T04 via `r_run-t04-temp-paths-masked`).
- Breaks (two structural gaps): (a) the sanity check is result-shaped — for setup-refusal fixtures (rc 2, empty
  class set) any mutation that keeps the rc is invisible, because the `SETUP: …` reason line is not a captured
  class; (b) `--list` fixtures cannot witness script presence/absence (r_map), so removing the very input a
  mapping fixture demonstrates against is invisible; combined with the two-triggers-per-branch design,
  single-fixture mutants almost never flip a kill (only sole-killer T04 did).
- Admission impact: the frozen kill rule and `BATTERY` line are unchanged and still reproduce — this is a limit of
  the counter's fixture self-check, consistent with the frozen limit "a kill records a result difference in the
  declared direction, not the fixture's intent" (round-41-claims.md, C1 limits). Per the tasking I did not change
  the battery, the counter, or any lane file.

## Controls and hygiene

- No tool installed or updated (none needed); pacman untouched; no writes outside the report dir and scratch;
  `~/.local/bin` read-only-bound in every run; `crit_git_shim.py` / `crit_ledger_selfread.py` untouched.
- No tampered/sidechannel/null hits in any of the 49 passes; `PINS-AFTER mismatched=0` in all of them.
- Restoration evidence — lane files before and after all runs (identical):
  `plans/round41_c1_verify.py 8835a94b…`, `plans/tip_receipts.py e4f49714…` (pin), `plans/sources_adopt.py
  38492bf1…` (pin), battery `r_ctl 2fcbbcb7… r_map 705a4b7c… r_run 1ccb08aa… r_setup a693fc51… s_exit 5f57cec9…
  s_modes 1023433b… s_usage c9ca3abe…`; `git status --porcelain` in the clone: untracked wave files only, no
  modification to any tracked file. Mutants lived only in `$S/bat/` (deleted at cleanup).
- Scratch cleanup: `$S` deleted after copying receipts; guard `case "$T" in "$S"|"$S"/*)` applied before `rm -rf`.

## Artifacts

- `runs/base.txt` — pristine baseline (predicate pass).
- `runs/mut-<fixture>.txt` — one full counter pass per fixture mutant (48 files).
- `runs/summary.json` — machine-readable per-run classification.
- `mutations.md` — the 48 exact byte replacements (old → new).
- `table.md` — the verdict table above (verbatim copy).

VERDICT: fixture-mutants-caught-43/48
