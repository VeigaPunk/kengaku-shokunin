writer: KengakuR29-2.FMutPinReread-2
item: FMutPinReread — hash-then-reread mutant (re-read input after hash check instead of using retained bytes) against plans/config_projection.py's selftest
date: 2026-10-21

## Godspeed axes
kill-evidence (exit codes + exact failing assertion), frozen-data blindness (--summary parity vs baseline), baseline fidelity (control digest + build receipt match), revert proof.

## Production source read
Yes. I read lane `plans/config_projection.py` in full. This is a mutation-testing item; the oracle-independence rule (derive from prereg text only) targets oracle/re-derivation items, not this one. The lane file itself was never modified.

## Setup — all writes in /tmp, lane untouched
- `cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans /tmp/fmut-reread/plans` (3.0M).
- Copy sha256 = lane sha256 = `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` — equals the control digest in `corpus/evidence/round29-calibration/mutation-witness.txt`.
- Baseline on the copy: `python3 plans/config_projection.py --selftest --root /tmp/fmut-reread` → exit 0, `SELFTEST clean cases=20 …` including all three `post_read_replacement_*` cases. `--summary --root /tmp/fmut-reread` → exit 0, stdout sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`.
- Baseline vs receipt: `diff baseline-summary.txt …/round29-calibration/build-summary.txt` shows exactly one difference, `47a48 > exit=0` — the receipt appends an `exit=0` status line; all summary content identical.

## Mutant — minimal, one line
Copy `plans/config_projection.py` line 113 (inside `read_pinned`, after the `snapshot_tampered` hash check at line 111):
- before: `verified[relative] = data`
- after: `verified[relative] = (root / relative).read_bytes()`

Semantics: bytes are hash-checked on first read, but projection then consumes a fresh disk reread — a TOCTOU window instead of retained authenticated bytes.

## Result: KILLED by `--selftest` (exit 1), all three victims
Run as shipped (case order RAW, GENERATOR, PROFILES):
- exit 1; fatal assertion at line 515: `assert swapped and code == 0 and retained["population"]["task_profile_projections"] == 2436, relative` → `AssertionError: plans/fixtures/r28/webarena/config_files/test.raw.json`.
- Mechanism (code-grounded): selftest's `replace_after_read` patch passes the first read (hash matches) and swaps the on-disk file to `b"[1,2,3]"`; the mutant's reread consumes swapped bytes → 3 tasks → projections 9 ≠ 2436 → `projection_count_invalid` finding → code 1.

Tuple reordered GENERATOR-first (test-side edit only; mutant unchanged): exit 1; `Unevaluable: source_contract_unrecognized` raised at line 68, detail `missing star import or unique main` — reread fed `b"x = 1\n"` to `source_contract`.

Tuple reordered PROFILES-first: exit 1; `Unevaluable: profile_missing` raised at line 122 (`check_profiles` on `{}`).

So each of the three `post_read_replacement_*` cases independently kills this mutant; no survivor. No mismatch found between mutant behavior and expected kill.

## `--summary`: byte-identical to baseline — frozen data alone is blind
Mutant `--summary --root /tmp/fmut-reread`: exit 0, stdout sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`, `diff` vs baseline empty.
Finding: frozen real data alone CANNOT detect this mutant. With static inputs the post-hash reread returns identical bytes; detection rests entirely on the selftest's mid-run swap (the `post_read_replacement_*` cases that patch `Path.read_bytes` and rewrite the victim on disk after its first read). Any future refactor that drops or weakens those cases would leave hash-then-reread undetectable by every other test in the instrument and by the frozen fixtures.

## Revert proof
Both copy edits reverted: file sha256 again `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` (byte-identical to lane); `--selftest` exit 0 (20 cases); `--summary` stdout sha256 `5ce5cb0f…`.

## Author-witness cross-check
`mutation-witness.txt` control digest and control selftest exit 0 reproduced independently. The witness's three mutants (wrong_order_reversed, url_only_substitution, index_by_task_id) are different mutations; the hash-then-reread kill is new evidence this wave, not a reproduction of theirs.

## Environment
Python 3.14.8, stdlib only. No tools installed or upgraded (none needed; pacman paused per contract).

## Artifacts
Retained: `.ufo/waves/round-29/scratch/falsify/FMutPinReread/` — baseline-summary.txt, mutant-summary.txt, mutant-selftest.txt, mutant-selftest-gen.txt, mutant-selftest-prof.txt, reverted-selftest.txt. Experiment root `/tmp/fmut-reread` (disposable). Lane repo, fixtures, and corpus untouched.

VERDICT: PASS
