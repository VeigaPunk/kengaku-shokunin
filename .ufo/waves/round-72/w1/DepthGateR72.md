# DepthGateR72 — round 72 w1: structural gates re-run at the tip (depth + trio sweep)

Seat: leaf executor, wave `round-72/w1`. No subagent, no battery, no port-5000 use (so no
`--port-lock` taken or needed), no commit, no package install (nothing was needed; `python3` is
3.14.8). Scratch `/fast/scratch/hyaku/kengaku-r72/DepthGateR72` was created for the determinism
re-run and is removed (verified `CLEANED`); no `/tmp` file written.

## Bytes measured

- Lane tip: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master` →
  `b6336136e0e891522b113a94d8e0bd65e0eae8de`; `rev-parse HEAD` is the same commit.
- `sha256sum SKILL.md` → `a1440637f10d8fc5e45e2338805eedfd4e01a9c90e7f47b588d0496ef71d1e34`
- `sha256sum corpus/evidence/round62/class-survey.txt` →
  `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613` (unchanged from round 71)
- `git status --porcelain -- SKILL.md corpus/evidence/round62/class-survey.txt` printed nothing:
  both measured inputs are the committed tip bytes, not a sibling's edit.
- `git status --porcelain -- corpus/evidence/round72/gates/` → `?? corpus/evidence/round72/gates/`
  (new receipts; not git-ignored — `git check-ignore` rc=1 — and seats do not commit).

## What I ran

| # | command (cwd = lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`) | rc | receipt |
|---|---|---|---|
| 1 | `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt` | **0** | `corpus/evidence/round72/gates/depth-gate.txt` (104 B, sha256 `063ebc373dd6a273ed5b2193ecc5b1110f4fe34f5afc79fcaa0bf7b0e66ac1c7`) |
| 2 | `python3 plans/round64_trio_sweep.py --sweep --lane .` | **0** | `corpus/evidence/round72/gates/trio.txt` (1756 B, sha256 `c27db9f5058bd5536542dfd6207e7a17b814ad665ba08395bdd781ea99bd3560`) |
| 3 | `grep -c 'executed 4 of 8' SKILL.md` | **0** (count `1`) | below |
| 4 | `grep -c 'executed 3 of 8' SKILL.md` | **1** (count `0`, grep's no-match status) | below |
| 5 | both gates re-run a second time in scratch (`cmp` against the receipts of record) | 0 / 0 | `DEPTH_IDENTICAL`, `TRIO_IDENTICAL` |

Verbatim output of receipts 1–2:

```
ROWS n=16 class_match=True count_mismatch=0 paths total=36 resolved=36 share=1.00
PREDICATE R63-C2 pass
```
```
SWEEP files=72 trio_open=43 addendum=29 red=0
ADDENDUM corpus/knowledge/attrib-prior-art-r21.md
ADDENDUM corpus/knowledge/attrib-r21.md
ADDENDUM corpus/knowledge/bailian-cli-telemetry.md
ADDENDUM corpus/knowledge/bench-arena-fresh-run.md
ADDENDUM corpus/knowledge/bench-arena-round11-power.md
ADDENDUM corpus/knowledge/bench-arena-round12-ladder.md
ADDENDUM corpus/knowledge/bench-arena-round5-battery.md
ADDENDUM corpus/knowledge/bench-arena-round6-stability.md
ADDENDUM corpus/knowledge/bench-arena-round7-noise-n25.md
ADDENDUM corpus/knowledge/bench-arena-round7-scaffold-ablation.md
ADDENDUM corpus/knowledge/bench-arena-round8-horizon.md
ADDENDUM corpus/knowledge/bench-arena-round9-replication.md
ADDENDUM corpus/knowledge/bench-arena-task27-timeout-anatomy.md
ADDENDUM corpus/knowledge/benchmark-selection.md
ADDENDUM corpus/knowledge/eval-design-digest-2.md
ADDENDUM corpus/knowledge/eval-design-digest-3.md
ADDENDUM corpus/knowledge/eval-prior-art-calibration.md
ADDENDUM corpus/knowledge/eval-theory-notes.md
ADDENDUM corpus/knowledge/gemini-benchmark-suite.md
ADDENDUM corpus/knowledge/godspeed-eval-findings.md
ADDENDUM corpus/knowledge/kimi-model-routing-round18.md
ADDENDUM corpus/knowledge/ledger-route-telemetry.md
ADDENDUM corpus/knowledge/local-bench-arena.md
ADDENDUM corpus/knowledge/local-model-index.md
ADDENDUM corpus/knowledge/probe-battery-r19.md
ADDENDUM corpus/knowledge/tb2-cancel-async-tasks-grader.md
ADDENDUM corpus/knowledge/tb2-grader-class-census.md
ADDENDUM corpus/knowledge/tb2-grader-vacuity-triage.md
ADDENDUM corpus/knowledge/telemetry-run-design.md
PREDICATE R64-C3 pass
INFO frozen-list=corpus/evidence/round64/trio-red-at-base.txt sha256=fe0498fb20b5102b50d80a3eca1258784cdf9d66edf4d9654b10fa99653a080a entries=29
```

Counter greps (item 4), run separately so each exit code is attributable:

- `grep -c 'executed 4 of 8' SKILL.md` → `1`, **rc=0**; the match is the `network-service` row at
  `SKILL.md:78`.
- `grep -c 'executed 3 of 8' SKILL.md` → `0`, **rc=1** (grep's documented no-match status). Not a
  gate failure; the counter has moved for `network-service` and no stale `3 of 8` spelling remains.

## Calibration: the token count did **not** move, and that is by construction

The item predicted "the four new registry rows add tokens". Measured against the frozen R63-C2
definition, they cannot: `plans/round63_gate_checks.py` tokenizes only the section
`## Decision table — grader class → offline replay recipe` (`SKILL.md:60-86` now), while the four
new rows were appended to `## Gate/probe registry` (`SKILL.md:587-796`). Evidence:

- `git diff c80fcdb3..HEAD -- SKILL.md` → `5 insertions(+)`: the four `round71-c1-hf-probe`,
  `round71-c2-routed-defects`, `round72-c1-hf-probe`, `round72-c2-routed-defects` rows plus one
  trailing blank line. **No line of the decision-table section changed** in round 72.
- Consequently `paths total=36 resolved=36` is byte-identical to the round-71 closure reading
  (`corpus/evidence/round71/gates/final-depth.txt`, rev `c80fcdb3`: `total=36 resolved=36`), up from
  `total=34` at round-71 pre-entry. **No resolution failure exists to report**; the expected increase
  is an expectation artefact, not a gate defect or a stale tip.
- Independent probe of the 36 unique tokens (47 raw occurrences, set semantics): `os.path.exists`
  on every token → `missing_on_disk 0`. So R63-C2's `resolved` (lexical: relative, no `..`, stays
  inside root) is not masking a dead pointer at this tip.
- The four new rows themselves, checked read-only: each has **8 cells**, kinds `probe`, `gate`,
  `probe`, `gate`, and every entry script named exists — `plans/round71_c1_hf_probe.py` (35 337 B),
  `plans/round71_c2_routed_defects.py` (14 316 B), `plans/round72_c1_hf_probe.py` (45 511 B),
  `plans/round72_c2_routed_defects.py` (19 895 B). Their bare backticked path citations also exist:
  `corpus/evidence/round71/hf/receipt.txt`, `corpus/README.md`, `plans/round-71-claims.md`.

## Trio sweep reading

`files=72`, `trio_open=43`, `addendum=29`, `red=0` — the three classes sum to the file count
(43+29=72), so no knowledge entry is unclassified. `PREDICATE R64-C3 pass`, rc=0.

- Frozen-list cross-check: the `INFO` line's `sha256=fe0498fb…` equals `sha256sum
  corpus/evidence/round64/trio-red-at-base.txt` (`fe0498fb20b5102b50d80a3eca1258784cdf9d66edf4d9654b10fa99653a080a`,
  29 lines). With `red=0` the set comparison is vacuous, but the gate's `red=0` path also requires
  every frozen entry to still exist as a file — it passed, so nothing was deleted or renamed.
- Set check (read-only, scratch temp files removed): the 29 `ADDENDUM` paths, sorted, are exactly the
  29 frozen-list paths, `diff` produced no output. Every base-red entry was repaired by appended
  addendum, none by rewriting an opening.

## Verdict

**PASS — both structural gates reproduce green at tip `b6336136`.** `PREDICATE R63-C2 pass`
(`ROWS n=16 class_match=True count_mismatch=0 paths total=36 resolved=36 share=1.00`, rc=0) and
`PREDICATE R64-C3 pass` (`SWEEP files=72 trio_open=43 addendum=29 red=0`, rc=0); the counter pair is
`executed 4 of 8`=1 (rc 0) / `executed 3 of 8`=0 (rc 1, no match). Both receipts are byte-identical on
an independent re-run, and the measured inputs are clean at HEAD.

## Risks / blockers / limits of this receipt

- No blocker. No tool install or upgrade was performed.
- Scope: these are the *structural* gates. They do not certify R72-C1's nine-case replay or R72-C2's
  `E1a`–`E2` corrections; the R71-R1 closure (registry rows) is priced by
  `plans/round72_c2_routed_defects.py`, which this seat did **not** run (not in its item). In
  particular the depth gate is blind to the registry section, so its green says nothing about those
  four rows beyond the read-only shape check recorded above.
- Operational note, reported as instructed: the `trap 'rm -rf' EXIT` did not fire under the persistent
  shell (the seat's command shell persists across calls), so the scratch dir survived its first
  command's exit. I removed it explicitly with `rm -rf -- /fast/scratch/hyaku/kengaku-r72/DepthGateR72`
  (rc=0) and confirmed `CLEANED`; nothing of this seat remains in scratch or `/tmp`.
- Wrote only the two assigned receipts under `corpus/evidence/round72/gates/` and this report.
