# R34 C2 counter mutation probe

Scratch: `.ufo/waves/round-34/build/R34MutC2Defects/`. Mutants were isolated copies of the frozen draft; the draft was not edited. The scratch selftests add one corresponding adversarial case to each mutant harness. The pristine `--selftest` was the baseline behavioral detector.

Baseline command: `python3 pristine_round34_defects.py --selftest` (scratch directory). Output: `SELFTEST cases=10 failed=0`, exit 0. Before and after pristine SHA-256: `d8af348c33993080eb7675b6163c9d77c0a052126d47386228779e7cd7bab550` (same exact bytes).

| Mutant | Probe | `--selftest` output | Verdict |
|---|---|---|---|
| N2: heading-only | N2 heading-only section fixture | `CASE N2-red-heading-only-round32 FAIL`; `SELFTEST cases=9 failed=1`; exit 1 | Killed |
| N5: unanchored substring | `:35-38extra` locator | `CASE N5-red-locator-substring FAIL`; `SELFTEST cases=11 failed=1`; exit 1 | Killed |
| N8: one-directional (files→rows only) | index row with absent file | `CASE N8-red-index-without-file FAIL`; `SELFTEST cases=11 failed=1`; exit 1 | Killed |
| N3: ignore distance | append-only and erratum tokens far apart | `CASE N3-red-distant-tokens FAIL`; `SELFTEST cases=11 failed=1`; exit 1 | Killed |
| N6: dropped | missing all N6 evidence | `CASE N6-red-missing-evidence FAIL`; `SELFTEST cases=11 failed=1`; exit 1 | Killed |

Per-mutant SHA-256 after mutation: mutant_1 `809b5d5ca43626fdfc326d2f34d0fa73ce10be7e625ecadf39888d15f12a2f3c`; mutant_2 `24b8fb2b24a16174d8c5206881540183d977c834c62e0d8b8a1127a36e7f472e`; mutant_3 `e5c13cae8f0e1479515997770b05fb7f6a545dadbedda1cdcaf67aaccbb386da`; mutant_4 `0f7ac00d3529c2839893b9494bf9fded8e4721a2b48c4773966c28451a1ee094`; mutant_5 `57a0fd6441b6473a71094cfaaf67d1419d27956321c9f4d1025a21d5c3f4e615`. Hash command: `sha256sum ../R34C2CounterDraft/round34_defects.py pristine_round34_defects.py mutant_*.py`; output recorded pristine and draft both `d8af348c33993080eb7675b6163c9d77c0a052126d47386228779e7cd7bab550`, and the mutant hashes above.

One early N2 mutation attempt did not expose the altered predicate because the fixture made both target sections empty; it passed. I corrected the fixture so Round 32 is heading-only while Round 33 has content, then reran; the corrected mutant is killed. No surviving mutant in the final five probes: **killed 5/5**. Restored evidence: target draft hash remains byte-identical to the pristine copy (`d8af…`); no target changes were made.

VERDICT: mut-c2defects (killed 5/5)
