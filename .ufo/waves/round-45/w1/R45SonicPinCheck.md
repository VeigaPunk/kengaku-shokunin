# R45SonicPinCheck — frozen digests, PINS, CAPTURES (round 45 wave 1)

2026-10-26. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `05b02e2b`; freeze commit
`b4fcd351` is an ancestor (`git -C $L merge-base --is-ancestor b4fcd351… HEAD` → yes). Worktree has 19
dirty paths (`git status --porcelain | wc -l`); none of the three files in §1 is among them. All commands
read-only; nothing written outside my report dir; no scratch dir needed (no fixture build, counter run or
probe executed, so no envelope run was required). Receipts: `R45SonicPinCheck/` next to this file.

## 1. Frozen digest table `.ufo/waves/round-45/claims/frozen-digests.txt` — 20 entries, 17 OK, 3 FAILED

Command (cwd = lane root):
```
sha256sum -c .ufo/waves/round-45/claims/frozen-digests.txt
```
Output (receipt `R45SonicPinCheck/frozen-digests-recheck.txt`, 836 B, sha256 of receipt not needed):
```
plans/round45_c1_verify.py: OK
plans/round45_c2_verify.py: FAILED
plans/password_recovery_probe.py: OK
plans/pkg-spec-r45.json: FAILED
corpus/evidence/round45/password-recovery-dry-cases-freeze.txt: OK
plans/round-45-claims.md: FAILED
corpus/evidence/round45/tb2-password-recovery/SHA256SUMS: OK
.ufo/waves/round-45/claims/c2_predictor_control.py: OK
plans/refusals45/f10_laneinclude.py: OK
plans/refusals45/f1_gitfile.py: OK
plans/refusals45/f2_deep.py: OK
plans/refusals45/f3_abbrev.py: OK
plans/refusals45/f4_fifo.py: OK
plans/refusals45/f5_alternates.py: OK
plans/refusals45/f6_above.py: OK
plans/refusals45/f7_commondir.py: OK
plans/refusals45/f8_worktreecfg.py: OK
plans/refusals45/f9_nodescribe.py: OK
plans/round45_c2_verify.py: OK
plans/pkg-spec-r45.json: OK
sha256sum: WARNING: 3 computed checksum(s) did NOT match   [exit 1]
```

Diagnosis: all 3 failures are pre-freeze blob digests; commit `52d7486` ("C2 spec to 8 rows (S149-S156;
gitignore is the reject), counter re-pinned, controls refreshed") moved the files after the freeze, and the
table only got replacement lines for two of the three, appended at the bottom (lines 19–20).

| path | table digest (line) | blob @ b4fcd351 | blob @ HEAD = worktree |
|---|---|---|---|
| `plans/round45_c2_verify.py` | `804df725…` (line 2) | `804df725…` | `8c302709…` (also table line 19: OK) |
| `plans/pkg-spec-r45.json` | `b8fc1e53…` (line 4) | `b8fc1e53…` | `3eb696b4…` (also table line 20: OK) |
| `plans/round-45-claims.md` | `79ede48a…` (line 6) | `79ede48a…` | `1e63c4ba…` (not in table) |

Commands:
```
git show b4fcd351…:plans/round45_c2_verify.py | sha256sum     # → 804df725… (likewise spec, claims)
git show HEAD:plans/round45_c2_verify.py | sha256sum          # → 8c302709… (likewise the other two)
git log --oneline b4fcd351..HEAD -- plans/round-45-claims.md plans/round45_c2_verify.py plans/pkg-spec-r45.json
                                                              # → 52d7486 (only commit)
git diff b4fcd351..HEAD -- plans/round-45-claims.md           # 1 insertion, 1 deletion
```
The claims diff is exactly one substitution: SOURCES rows "`S149–S157`" → "`S149–S156`" — the assignment's
own prescribed "spec's extra row" correction. No predicate, kill-rule, or control sentence changed.

### Findings — §1
- **MED** — `frozen-digests.txt` is internally inconsistent: it pins both the pre- and post-`52d7486`
  digests for `plans/round45_c2_verify.py` (lines 2 vs 19) and `plans/pkg-spec-r45.json` (lines 4 vs 20),
  and only the stale pre-`52d7486` digest for `plans/round-45-claims.md` (line 6); the current claims blob
  `1e63c4ba…` is in no table line. Honest state would be "2 superseded duplicates + 1 stale line" — as
  committed, a naive recompute reports 3 mismatches. Not load-bearing: neither round-45 counter reads this
  file (grep over `plans/`: only prose references in rounds 37–44 claims; `plans/battery42/o_scan.py:58`
  writes a fixture-local copy). Reviewer-facing trust only; the L1 should regenerate the table at the
  landing tip or annotate lines 2/4/6.
- **INFO** — the claims file changed after its own freeze commit; the one-line diff matches the goal text
  ("the spec's extra row" → S149–S156), so this is the documented correction, not a freeze violation.
- **INFO** — pin coverage: `plans/pkg_gate.py` (goal-frozen) has no line in the table; it is digest-pinned
  only inside `plans/round45_c2_verify.py` (`GATE_SHA256 = ea638822…`), which matches the worktree
  (`sha256sum plans/pkg_gate.py` → `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`).
  The batteries are covered via PINS (§2), not the table.

## 2. PINS in `plans/round45_c1_verify.py` — 33/33 exist, 33/33 digest-match

Command: `python3 R45SonicPinCheck/verify_pins.py` (AST-extracts the `PINS` dict from the counter, then
`exists()` + sha256 per entry over the lane; script saved beside this report):
```
PINS total=33 exists_ok=33 missing=0 digest_mismatch=0
missing: []
mismatch: []
dup keys: []
```
Composition: 1× `plans/round44_c1_verify.py` + 10× `plans/refusals45/f1–f10` + 5× `plans/battery42` +
7× `plans/battery43` + 10× `plans/battery44` = 33, matching the frozen predicate "`PINS total=33
mismatched=0`" (`plans/round45_c1_verify.py:37`). The ten refusals45 digests are byte-identical to their
`frozen-digests.txt` lines (all 10 OK there too).

## 3. CAPTURES in `plans/round45_c2_verify.py` — 9/9 exist, 9/9 digest-match

Same script, over `corpus/evidence/round45/tb2-password-recovery/`:
```
CAPTURES total=9 exists_ok=9 missing=0 digest_mismatch=0
CAPTURES not in SHA256SUMS: []
SHA256SUMS not in CAPTURES: []
digest disagreements: []
files in capdir not in CAPTURES: ['SHA256SUMS']
```
The 9 captures (README.md, environment/Dockerfile, environment/setup.sh, gitignore, instruction.md,
solution/solve.sh, task.toml, tests/test.sh, tests/test_outputs.py) all exist and match; CAPTURES and
`SHA256SUMS` are set-equal with zero digest disagreements; the capture dir holds exactly those 9 plus
`SHA256SUMS` itself.

## Counts (verdict arithmetic)

t = 62 checks = 20 frozen-digest table lines + 33 PINS + 9 CAPTURES.
Verified (path exists and digest matches the lane file): 17 + 33 + 9 = 59.
Mismatches k = 3 — `frozen-digests.txt` lines 2, 4, 6 (all pre-`52d7486` blobs; two superseded by the
table's own appended lines, one unlisted replacement; no counter consumes the table).

VERDICT: pins-verified-59/62-mismatch-3
