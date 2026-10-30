# Seat report — R8CounterSoundness (kengaku round 55, w1)

Scope: soundness hunt (FALSE-PASS routes) against `plans/round55_c2_entryargv.py`,
the frozen R55-C2 instrument. No lane writes (only this seat's `.ufo/waves/round-55/w1/`
outputs). No subagents. No installs.

## What I did

1. Read the frozen claims (`plans/round-55-claims.md` @80afa613) and the r54 counter
   (`plans/round54_c2_entrytruth.py`), the controls builder (`plans/round55_c2_controls.py`),
   the ledger schema (`plans/round54-entrytruth.json`, 78 rows), and the live SKILL.md
   registry block.
2. Cloned the lane `--shared` into scratch (`/fast/scratch/hyaku/kengaku-r55/R8CounterSoundness/lane`).
3. Started a bounded-wait watcher (60 s steps) for the r55 counter; it landed in the
   live tree at 12:38 (untracked sibling build, 431 lines); I then read its L1–L4
   implementation and ran all fixtures against the landed file itself.
4. Built six fixture families (F1, F1b, F2, F3, F4a/b/c, F5) + wrapper/path probes;
   ran them against the r54 counter (mechanism baseline) and the landed r55 counter.
5. Reproduced the two frozen fixture kills through the controls builder.

## Commands and exit codes (all run from `/fast/scratch/hyaku/kengaku-r55/R8CounterSoundness` unless noted)

| command | exit | result |
|---|---|---|
| `python3 hunt.py all` (fixtures vs r54) | 0 | F1 pass-divergence, F2 pass, F3 ARGV-DEFECT, F4a/F4b pass, F5 characterized |
| `python3 r55_probe.py` (fixtures vs landed r55) | 0 | F1 **pass exit 0**, F2 **pass exit 0**, F3 fail(1) ARGV-DEFECT, F4a fail(1) ABBREV-DEFECT (docstring leaked full flag — fixture bug), F4b pass, F5 tokenizer table, unit probes |
| `python3 r55_probe2.py` (cleaned L3 fixtures vs r55) | 0 | F4a-clean **pass (l3=0)**, F4c `--hel` **pass (l3=0)** |
| `python3 r55_probe3.py` (F1b layout fingerprint vs r55) | 0 | **PREDICATE pass exit 0**; truth plain=1, hermetic-cwd-root=1, worker-cwd=0 |
| `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r55` (in lane) | 0 | kill demonstrated (counter exit 1) |
| `python3 plans/round55_c2_controls.py --case uv-decoy-script --against r55` (in lane) | 0 | kill demonstrated (counter exit 1) |
| same two cases `--against r54` (in lane) | 0 | laundering demonstrated on r54 (baseline, matches frozen claims) |
| `python3 plans/round55_c2_entryargv.py --selftest` (in lane) | 0 | `[selftest] 4/4 PASS` |

Raw r55 probe output: `receipts/r55-probe-results.txt` in this directory.

## Findings (full detail in `routes.md`)

- **F1b (kill-rule candidate)**: gate green only under the counter's hermetic env AND
  worker-clone cwd layout; r55 passes it (`PREDICATE R55-C2 pass`, all static legs
  clean) while the declared entry exits 1 under both plain-env and the controls'
  hermetic ground truth (cwd=repo root). The divergence channel is the inherited r54
  execution environment, not the argv binding.
- **F1**: env-only fingerprint survives the counter; truth diverges only in plain env.
- **F2**: red-row evidence is a substring of the script's own output; a false `reason`
  passes L4. Survives; not a kill (observation is true).
- **F3 homoglyph, W1 wrapper inventory, W2 absolute path/env/exec-a, C1 ledger-argv
  tampering**: all FAIL (caught / fail-closed). Canonical laundering closed doubly
  (L1 exact equality + execution uses the registry-parsed argv, not the ledger's).
- **F4a/F4b/F4c**: L3's source-text flag enumeration misses runtime-built flags,
  equals-form abbreviations, and argparse builtins; all survive the counter but are
  truthful cell forms, so not kill-rule false passes.

## Files written

- `.ufo/waves/round-55/w1/R8CounterSoundness/routes.md` (route list + fixtures + verdicts)
- `.ufo/waves/round-55/w1/R8CounterSoundness/report.md` (this file)
- `.ufo/waves/round-55/w1/R8CounterSoundness/receipts/r55-probe-results.txt`
- `.ufo/waves/round-55/w1/R8CounterSoundness.md` (scoped findings; the seat's Report trailer)
- Scratch (deleted at exit): `hunt.py`, `r55_probe.py`, `r55_probe2.py`, `r55_probe3.py`,
  `poll/watch.sh`, fixture trees, `lane/` shared clone.

## Defects found (in the counter under hunt)

1. F1b/F1 environment-fingerprint laundering channel (kill-rule candidate) — see routes.md.
2. F2 evidence-fragment provenance gap (L4 hardness, not a kill).
3. F4a/F4b/F4c L3 enumeration gaps behind L1 (not kills).

## Dead ends

- Homoglyph/unicode argv tokens: caught by exact comparison (r54's check fires first).
- Quoted/two-span/prose/unbalanced cells: parser is fail-closed or consistent.
- `python` (no 3) cells, uppercase `Python3`, wrapper-first cells: all ARGV-DEFECT.
- Timeout/`timeout_s` games, `python3 -` stdin entries, `env`/absolute-path wrappers: all fail-closed.
- First F4a run was invalidated by my own docstring containing the literal `--selftest`
  (BODY_FLAG found it) — corrected in the re-run (reported for honesty).

## Honesty notes

- An unrun check has not passed: every verdict above was executed against the landed
  counter (or, for r54-mechanism rows, against r54) and the exit codes are recorded.
- The r55 counter file was untracked in the live tree at probe time (sibling build);
  the L1's measured-after run should re-verify F1b against the committed revision.
- No installs; no peer messages sent; no subagents.
