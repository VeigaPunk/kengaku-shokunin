# FxMutG2 — G2 list-deletion mutant survives
Axes: MC transform sensitivity; applicability fidelity; pin/baseline fail-closed behavior; exact byte restoration.
Scope: round26 attempt1, advisory FALSIFY only; integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; no admission judgment.
Read: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-26-claims.md` including POST-OUTPUT Amendment1/Amendment2; round-26 lesson and draft.
Scratch: `/tmp/kengaku-r26-FxMutG2.qC4NyL`; live source was never edited. No tools installed or updated.
Export command (exit0): `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -x -C /tmp/kengaku-r26-FxMutG2.qC4NyL`.

## One mutant and expected detector
Only `/tmp/kengaku-r26-FxMutG2.qC4NyL/plans/grader_perturb.py:397` changed: `return extracted[1:]` → `return extracted[0:]`.
Plausible off-by-one: G2 copies a top-level list without deleting its first element; dictionary deletion remains intact.
Expected detector: `--selftest` should exit1 for this G2 semantic no-op. Actual: exit0, including `SELFTEST G2 PASS`.
Missing behavior: `_selftest` uses only a dictionary/state G2 fixture (`:609,613-615`); it never exercises list/sequence deletion (`:396-397`).

## Exact commands and observed exits
Driver: `/tmp/kengaku-r26-FxMutG2.qC4NyL/probe.py`; children run concurrently, each with timeout120s and cwd `/tmp`.
Executed `python3 /tmp/kengaku-r26-FxMutG2.qC4NyL/probe.py --stage pristine`, then `--stage mutated`, then `--stage restored`; each driver exited0.
For each stage the exact primary child commands were:
`python3 /tmp/kengaku-r26-FxMutG2.qC4NyL/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutG2.qC4NyL --selftest`
`python3 /tmp/kengaku-r26-FxMutG2.qC4NyL/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutG2.qC4NyL --summary`
Additional children: `python3 /tmp/kengaku-r26-FxMutG2.qC4NyL/probe.py --guard pin`, `--guard baseline`, and `--assert-g2-list`.
| stage | selftest | summary | pin guard | baseline guard | list assertion |
|---|---:|---:|---:|---:|---:|
| pristine | 0 | 0 | 1 | 1 | 0 |
| mutated | 0 | 0 | 1 | 1 | 1 |
| restored | 0 | 0 | 1 | 1 | 0 |
All three selftests printed `SELFTEST G2 PASS`, `SELFTEST MUTATION-CATCH PASS caught=12`, `SELFTEST TOTAL families=10 failed=0`.
Pristine/restored G2: `n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS`; composite143/143 PASS.
Mutated G2: `n=1021 k=1000 rate=0.979432 cp95_nominal=[0.968731,0.987224] verdict=PASS`; composite143/130 INDETERMINATE.
All ordinary summary/selftest runs: `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`.
Full stdout/stderr and exact argv/exits are retained under `/tmp/kengaku-r26-FxMutG2.qC4NyL/{pristine,mutated,restored}.json` and corresponding `<stage>.<child>.stdout.txt` / `.stderr.txt` files.

## Summary guards unchanged
Both guard children call the imported script's `main(['--root', '/tmp/kengaku-r26-FxMutG2.qC4NyL', '--summary'])`; injections are process-local, not file mutations.
Pin control replaces only the first expected digest with 64 zeroes; every stage exits1 with the same error:
`ERROR corpus/evidence/round8-horizon/results.jsonl: sha256 bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204 != frozen 0000000000000000000000000000000000000000000000000000000000000000`
Baseline control flips only the first `regrade` return, without changing evidence or pins; every stage exits1 with identical errors:
`ERROR corpus/evidence/round8-horizon/results.jsonl:11 cell='A-INC' pid=1 turn=1: baseline re-grade False != stored ok True`
`ERROR frozen population mismatch: candidates=1964 population=1963 excluded=1 expected=1964`

## Minimal failing assertion, exercised on all three versions
With the imported/configured module as `m`:
```python
raw = '```json\n["a", "b"]\n```'
rec = m.Rec('fixture', 1, 'family2', 'g2', 1, 'seq', raw, ['a', 'b'], True)
assert m.regrade(rec, raw) is True
changed = m.apply_family('G2', raw, ['a', 'b'], rec)
assert changed is not None and m._GRADER.extract_json_block(changed) == ['b']
```
Pristine/restored output: `G2 list transformed='```json\n["b"]\n```' extracted=['b']`; assertion PASS.
Mutated output: `G2 list transformed='```json\n["a","b"]\n```' extracted=['a', 'b']`; `AssertionError: G2 must delete first element: got=['a', 'b']`.

## Restoration evidence
SHA256 pristine/restored/live: `8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b`; mutant: `163d04e1d1a3ba813f2e0ec163094fec51877731435f46169dbdea1077e698a4`.
Restored the exact original line with the surgical edit tool. `cmp /tmp/kengaku-r26-FxMutG2.qC4NyL/plans/grader_perturb.py /tmp/kengaku-r26-FxMutG2.qC4NyL/grader_perturb.pristine.py` succeeded (exit0).
`sha256sum /tmp/kengaku-r26-FxMutG2.qC4NyL/plans/grader_perturb.py /tmp/kengaku-r26-FxMutG2.qC4NyL/grader_perturb.pristine.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py` printed the identical pristine digest for all three (exit0).
VERDICT: SURVIVED — G2 top-level list semantic no-op escapes selftest; the exercised assertion kills it, summary guards remain fail-closed, and original bytes are restored. Coverage finding only.
