# FxGate — round-32 gate receipts (Q20 existing + planned second receipt)

Seat: `L1Kengaku32.FxGate` (leaf). Date: 2026-10-25. Lane: `kengaku-shokunin`, cwd lane root.
Scope: read-only git + running the gate commands on the freeze tree and on the post-fix working tree.
No lane files created/edited except this report. Scratch: `/tmp/r32f-FxGate/` (44 KB).

## 1. Commits this round that touch plans/*.py

Round range: baseline lane tip `f20a1097` → lane tip `6084cd3` (master == origin == origin/master).
Only three commits land in the range:

| commit | subject | touches plans/*.py? |
|---|---|---|
| `85a9695` | considerthese: 2026-10-25 daily shokunin reflection | no (`considerthese/2026-10-25.md` only) |
| `0d32691` | round-32: frozen claims, counters, freeze controls | **yes — adds `plans/catalog_probe.py`, `plans/round32_c1_verify.py`, `plans/round32_defects.py`** |
| `6084cd3` | round-32: freeze-commit gate receipt (Q20 out-of-band) | no (`.ufo/waves/round-32/gate-receipt.txt` only) |

→ Exactly one landed commit touches `plans/*.py`: the freeze commit `0d32691d7a1205586df7230a5209d02c49ae01c3`.

Notes:
- `75cd250` (same subject, parent `f20a109`) is an abandoned pre-rebase freeze duplicate: reachable from no ref
  (`git branch -a --contains` empty; `jj/keep/*` are VCS-internal refs, not landings; no stash). Not a landed commit.
- `git diff 0d32691 master` = only `.ufo/waves/round-32/gate-receipt.txt` (+16), so master's tree equals the freeze
  tree for every receipt-relevant byte (confirmed by R32CountersPreflight for the counters).
- Working-tree (not yet landed) edits: `plans/round32_defects.py` (+37/−8) and `plans/catalog_probe.py` (+10) —
  these are the counter fixes that will land later (the second-receipt subject). No other `plans/*.py` planned edits.

## 2. (a) The existing receipt was generated from the freeze commit tree — VERIFIED

Re-derived every section of `.ufo/waves/round-32/gate-receipt.txt` from `git archive 0d32691d7a1205586df7230a5209d02c49ae01c3`
(extracted to scratch; cwd = tree root). Every line matches byte-for-byte:

| receipt section | command run on freeze tree | observed (== receipt) | exit |
|---|---|---|---|
| grader | `python3 grader.py` | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` | 0 |
| roster | `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=17 failed=0` | 0 |
| roster | `python3 plans/registry_check.py --selftest` | `SELFTEST clean cases=15 <exact list>` | 0 |
| roster | `python3 plans/config_projection.py --selftest` | `SELFTEST clean cases=31 <exact list>` | 0 |
| roster | `python3 plans/benchmark_spec_audit.py --selftest` | `SELFTEST clean cases=67 <exact list>` | 0 |
| roster | `python3 plans/gate_timing_check.py --selftest` | `[selftest] ALL PASS (five allowed roles; …)` | 0 |
| roster | `python3 plans/state_check.py --selftest` | `[selftest] ALL PASS (canonical seed, pointers, …)` | 0 |
| new tools | `python3 plans/round32_defects.py --selftest` | `SELFTEST checks=7 failed=0` | 0 |
| new tools | `python3 plans/round32_c1_verify.py --selftest` | `SELFTEST checks=6 failed=0` | 0 |
| new tools | `python3 plans/catalog_probe.py --selftest` | `SELFTEST checks=6 failed=0` | 0 |

The receipt header's `extracted from: git archive 0d32691d…` is accurate; the receipt's content is a faithful

 of the freeze tree's gates.

## 3. (b) A second receipt must cover the post-fix plans/round32_defects.py + plans/catalog_probe.py — REQUIRED, and feasible

The counter fixes (working-tree edits above) land later; they change the two tools' selftests, so the Q20 receipt's
"round-32 new tools" section goes stale the moment they land. Verified on the post-fix working tree:

- `python3 plans/round32_defects.py --selftest` → `SELFTEST checks=7 failed=0`, exit 0.
  R1/R2 are now exercised via synthetic fixtures (`R1-red-without-erratum`, `R1-green-with-erratum`,
  `R2-red-missing-report`); the count stays 7 but the line must be regenerated from the post-fix tree.
- `python3 plans/catalog_probe.py --selftest` → `SELFTEST checks=8 failed=0`, exit 0.
  **Count grows 6 → 8** (`hf-empty-list-guard`, `or-empty-data-guard`). The Q20 line `catalog_probe: SELFTEST
  checks=6 failed=0` is therefore wrong after the fix; the second receipt must record `checks=8`.
- `python3 plans/round32_c1_verify.py --selftest` → unchanged `checks=6 failed=0`.

## 4. (c) Receipt contents — grader CHECKS n=733 + roster selftests + new tools' selftests

The Q20 receipt obeys exactly this shape (grader line + six roster selftest tail lines + three new-tool selftest
lines). The second receipt must have the same shape, with the post-fix tool versions.

## 5. Exact commands the second receipt must run

Generated from the landing commit tree (`git archive <landing-commit>`; cwd = repo root; header names the landing
commit). All commands exit 0; each expected tail line is given:

```
# grader (operability gate)
python3 grader.py
#   CHECKS n=733 mismatches=0 errata_pinned=1
#   VERDICT: PASS — stored evidence fully re-derives offline

# roster selftests
python3 plans/sources_adopt.py --selftest
#   SELFTEST cases=17 failed=0
python3 plans/registry_check.py --selftest
#   SELFTEST clean cases=15 <list>
python3 plans/config_projection.py --selftest
#   SELFTEST clean cases=31 <list>
python3 plans/benchmark_spec_audit.py --selftest
#   SELFTEST clean cases=67 <list>
python3 plans/gate_timing_check.py --selftest
#   [selftest] ALL PASS (five allowed roles; …)
python3 plans/state_check.py --selftest
#   [selftest] ALL PASS (canonical seed, pointers, …)

# round-32 new tools (post-fix versions)
python3 plans/round32_defects.py --selftest
#   SELFTEST checks=7 failed=0
python3 plans/round32_c1_verify.py --selftest
#   SELFTEST checks=6 failed=0
python3 plans/catalog_probe.py --selftest
#   SELFTEST checks=8 failed=0    (was 6 at freeze; +hf-empty-list-guard, +or-empty-data-guard)
```

Note: the claims' own counting commands (`plans/adoption_check.py --expect … --census`, `plans/round32_defects.py
--lane .`, `plans/catalog_probe.py --diff --lane .`) are claim receipts governed by the frozen controls/`*-before.txt`
(the preflight report already replays them), not part of the gate receipt per the Q20 precedent; the C2/C3 counters'
live runs should still be replayed at landing (R32RevFixes note), but the gate receipt proper is the list above.

## Residual risk / gaps

- The second receipt's `catalog_probe` line value (6→8) depends on the working-tree fix landing as currently drafted;
  if the fix is amended before landing the count could shift again — the receipt must be generated from the actual
  landing tree, never from this report's expectation.
- Gate receipts verify the gates, not the claims; C1/C2/C3 verdicts still require their own counter runs + controls.

VERDICT: gate-receipts-planned
