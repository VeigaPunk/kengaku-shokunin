# R46RevRouted — carried routed-item re-check

Scope: re-check the round-45 carried findings at base `64ba8385ea10af1b78d367dcb242b92d97062af7`; round-46 frozen claims are stage-1 freeze commit `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`.

## Results

| Finding | Base status | Round-46 frozen claims |
|---|---|---|
| `R45SentC2Grader` F1 — P10 `uv`/Biopython host fallback | **Still reproducible.** On the verified clean base clone, `round45_c2_verify.py --lane ... --work ...` printed `checks=11 defects=0`, `PREDICATE C2 pass`; the valid envelope/strace receipt shows `uv run --with biopython==1.85` and a managed Python interpreter executing the probe. Host `import Bio` returned rc 1; `uv` resolved to `/home/vgpnk/.local/bin/uv`. | **Not addressed.** C2 explicitly keeps `plans/pkg_gate.py` frozen; C3 also pins the round-45 gate digest. The existing `R42-R3-08` ledger row remains open for the same undeclared dependency. |
| `R45SentC2Grader` F2 — P9 untracked-file sensitivity | **Still reproducible.** Clean base clone: P9 `untracked=0`, C2 passes. Adding only `.r46-review-untracked` in that scratch clone: `P9 DEFECT untracked=1`, `PREDICATE C2 fail`. | **Not addressed.** Round-46 claims pin the old gate; no P9 clean-tree change is specified. |
| `R45SentC2Grader` F3 — P9 misses tracked modifications | **Still reproducible.** After modifying tracked `SCORECARD.md`, `git status --porcelain` showed ` M SCORECARD.md`, while `git ls-files --others --exclude-standard` counted 0; P9 still reported `untracked=0` and C2 passed. | **Not addressed.** The claims keep the gate frozen and specify no tracked-tree cleanliness check. |
| `R45CritV11Bypass` — V11 lookup/heuristic attacks | **Still reproducible.** Replayed saved p1–p4 predictors through the base counter's `v11()`; all four returned `True`, `states=48 grader_pass=18 grader_fail=30 disagree=0`. Counter SHA-256 at base is `ab6825e34596ba71f59a184a59fd4e672fd22dcf4b892c511cae5ead2b104f50`, matching the round-45 report's pinned digest. | **Touched directly.** Frozen C3 explicitly names the `R45CritV11Bypass` lookup shapes as held-out predictors that its counter must refuse. This is a planned control, not yet a result at the stage-1 base. |
| `R45CritIntent` — brace-prefixed `--claims` path bypass | **Still reproducible.** Same fixture and argv shape: plain `../../etc/passwd` returned `--claims value '../../etc/passwd' resolves outside the fixture`; `{T}/../../etc/passwd` returned `None` (admit). The fixture repo top-level was verified before the calls. | **Surface touched, concrete attack not explicitly pinned.** C1 repairs `fixture_fence.py` and claims argv containment, but its frozen refusal set names f1–f10 plus the listed R45Ho* modules—not this CritIntent brace-prefix case. I found no explicit brace-prefix control in those f1–f10 modules. Do not count this specific attack as covered unless the stage-2 counter/control includes it. |

## Routed ledger

The `routed_open.py` docstring confirms the CLI `--lane`, default file `corpus/routed-findings.jsonl`; the default invocation does not run row checks (`--observe` would). At the base clone:

```text
python3 plans/routed_open.py --lane "$S/lane"
ROWS total=60 open=23 blocked=1 closed=34 refused=2
routed_open=24 oldest_round=39
```

`corpus/routed-findings.jsonl:27` is `R42-R3-08`, `gate-undeclared-dependency`, status `open`; its check requires `biopython==1.85` to be absent from `plans/pkg_gate.py`. Exact search found no ledger rows for `R45SentC2Grader`, `R45CritV11Bypass`, `R45CritIntent`, or the round-45 spotcheck source. Round-46 frozen claims do not mention the routed ledger or close `R42-R3-08`.

## Evidence and verification notes

- Base clone top-level was verified as `/fast/scratch/hyaku/kengaku-r46/R46RevRouted/lane`; `git rev-parse HEAD` returned the requested base. All fixture/counter/probe executions used the round-46 envelope.
- One initial clean C2 run returned C2 PASS but the envelope detected a `~/.local/bin` digest change (`ff187bb5c98aa6b5` → `7747d38e2042d398`), returned exit 4, and marked the measurement INVALID. Two subsequent digest samples were identical; I repeated the run, which passed with digest `7747d38e2042d398` unchanged. The invalid run is not counted.
- The command/output excerpts and ENVELOPE start/end lines are preserved in `R46RevRouted/measurements.txt` (5,212 bytes; SHA-256 `4fc3000b43a8971aaeb175c7d0c67ce2dff2ca84c2844a671e9333d354b7ead6`). The 431,384-byte strace was not copied whole; its SHA-256 is recorded in that receipt along with the relevant `execve` excerpt.
- `routed_open.py` was run without `--observe`, as requested; no assertions are made about every row's `check` result.
- LSP is unavailable in this session: `read xd://lsp` returned “No such tool”. I used pinned source/report inspection and the listed reproductions; grep was used only for literal absence in the ledger, not as semantic proof. No tools were installed or updated.

VERDICT: routed-items-5-still-open-5
