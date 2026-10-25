# FxRepairRows — round 26 falsify

Scope: routed R26-E1–E4 and machine-readable E5–E8 corrections; calibration. Base `f11bffbf`; integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` (from `.ufo/waves/round-26/integration-revision.txt`). LSP unavailable: `read xd://lsp` returned “No such tool”; literal search was not treated as semantic proof. `plans/round26_census.sh:60-71,78-96` still calls the same state-check/timing CLIs. Installs: none.

## Findings

### HIGH — P3b correction-only run remains red

`PROVINCE.md:184-185` R26-E7/E8 restate only `` `rows=42` ``. `state_check.py:1314-1325` derives the full exact-token set `` `rows=42` `id_set=exact` ``; `p3_record` at `:1153-1161` requires exact equality of all code spans. Thus both frozen P3b row assertions remain mismatches, not superseded. R26-E3a/b earlier lines also have extra code spans; E7/E8 are the latest restatements selected by the matcher.

Command: `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --summary` → exit **1**; `assertions=275 match=267 mismatch=2 superseded=3 offline_unverifiable=3`. Output: `P3b.province.public-literature-registry.rows` correction tokens `['rows=42']`, derived `['rows=42','id_set=exact']`; same for `P3b.province.round25-correction.rows`. E5/E6 do pass: their `18 checks` + `0 failed` and `mismatch=10` tokens are reported `SUPERSEDED`.

`--selftest` exits **0** and exercises P3a red + full-token correction green, plus P3b changed-ID-set red; it does not exercise a P3b correction-only green. The live integration result above is the failing positive-control outcome. Add the missing `id_set=exact` token to E7/E8 and a P3b full-correction control before treating C2 as green.

## Verified routed values and preservation

- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib_calibration.py --selftest` → `selftest: 18 checks, 0 failed`, exit **0**; receipt `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt:19` agrees (R26-E1: 14→18).
- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --selftest` → P3a red mutation/full-token R26-E green and P3b duplicate-ID red; `[selftest] ALL PASS`, exit **0**. It has no P3b correction-only green case.
- Replayed v2 from `9d8a00d` on archived `6180e4f`: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r26-fxrepair-v2-jQ9ywU/plans/state_check.py --root /tmp/kengaku-r26-fxrepair-6180e4f-Lesopi --summary` → `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3`, exit **1**. This confirms E2’s 11→10 and receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt:2`.
- Frozen registry check: `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --root /tmp/kengaku-r26-fxrepair-f11bffbf-Fp41pj --summary` → `P3b` observed `rows=42`, `exact_id_set=true`, IDs S001–S042, `missing_ids=[] duplicate_ids=[] unexpected_ids=[]`; total `assertions=275 match=266 mismatch=5 superseded=1 offline_unverifiable=3`, exit **1** (the two stale PROVINCE values and other frozen base defects are expected red). S043+ are outside the frozen census.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --no-ext-diff --unified=0 f11bffbf9caa9c9e286fb32c568b81b97719656a 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 -- SCORECARD.md PROVINCE.md` → **31 insertions, 0 deletions**. R26-E1/E2 and E3/E3a/b/E7/E8 are appended; old cells and `PROVINCE.md:112,119` remain unchanged. E5/E6 pass the exact-token matcher; E7/E8 do not.

## Q13 timing evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --selftest` → `[selftest] ALL PASS`, exit **0**.
- Red-before: `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9 --repo /home/vgpnk/Projects/shokunin/kengaku-shokunin` → `FAIL line 29`, generic “wave-2 seats”, `second-seat-reports=0`, exit **1**.
- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 92adab1d6557e5284168cb22a0a1ca6652577c07 --repo /tmp/kengaku-r26-FxRepairRows-gate-D7yZUJ` → cited report absent, exit **1**.
- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit c6e144f4799a1a7072e90914d363ef6394afefb4 --repo /tmp/kengaku-r26-FxRepairRows-gate-D7yZUJ` → `PASS`, exit **0**.
- `PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit c0cc98750fb9a15be8ab4df62c11c52ed9dc8718 --repo /tmp/kengaku-r26-FxRepairRows-gate-D7yZUJ` → `PASS`, exit **0** (same-commit control).

### LOW — R26-E4 mixes tree-entry and report counts

`corpus/lessons/round-26.md:23-25` calls `0, 83, 87` “falsify reports.” Exact raw-count command: `repo=/home/vgpnk/Projects/shokunin/kengaku-shokunin; for rev in 8ea41f9 8239a56 9d8a00d; do n=$(git -C "$repo" ls-tree -r --name-only "$rev" -- .ufo/waves/round-25/falsify/ | wc -l); printf '%s %s\n' "$rev" "$n"; done` → total entries **0 / 83 / 88**. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only 8239a56 -- .ufo/waves/round-25/falsify/swarm-registry.json` and the same command with `9d8a00d` confirm the registry entry at both later trees. Exact report-count command: `repo=/home/vgpnk/Projects/shokunin/kengaku-shokunin; for rev in 8ea41f9 8239a56 9d8a00d; do PYTHONDONTWRITEBYTECODE=1 python3 "$repo/plans/gate_timing_check.py" --lesson corpus/lessons/round-25.md --commit "$rev" --repo "$repo"; done` → the printed `second-seat-reports` values are **0 / 82 / 87** (all three historical Gate rows fail exit **1** on generic support). The stated sequence mixes raw tree entries and Markdown report paths; correct its count label while retaining the red-before conclusion.

## Residual risk / verification gaps

The round-26 Gate still records the candidate as deferred (`corpus/lessons/round-26.md:29-34`), so no live admitted-entry Q13 check was possible. No LSP device/server was mounted; caller checks are limited to the literal `round26_census.sh` references, not semantic reference proof. No installs.

VERDICT: HOLD — E1/E2/E3 values and append-only preservation check out, and Q13 red/green controls work; integrated `state_check --summary` still exits 1 because R26-E7/E8 omit `id_set=exact`. Fix that and the mixed E4 count before claiming P3b correction-only green.
