# FxFamilyF5 — F5 only

Integration reviewed: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` (`.ufo/waves/round-26/integration-revision.txt`).

## Findings by severity

- **No actionable F5 defect found.** F5 is an unconditional bracket-free prefix (`plans/grader_perturb.py:429-430`); every baseline-admitted raw record is applicable. The frozen-population replay and all five format strata have no observed invariant-verdict change.

## Recomputed evidence

Independent disposable script `/tmp/f5_independent.py` read the four frozen JSONL files, checked their hard-coded SHA-256 pins, reconstructed non-C truth from `meta`/`meta2`, replayed baseline and prefixed responses through `grader.py`, and computed strata and the source-defined composite key. It does not import `grader_perturb.py` or the oracle.

Command: `python3 /tmp/f5_independent.py /home/vgpnk/Projects/shokunin/kengaku-shokunin; rc=$?; printf 'EXIT=%s\n' "$rc"; exit 0` — child exit **0**.

Exact output:
```text
CHECKSUMS results.jsonl=bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204:MATCH results-r9.jsonl=c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb:MATCH results-r11.jsonl=918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad:MATCH results-r12.jsonl=ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1:MATCH
POPULATION candidates=1964 independently_replayed=1964 excluded=0 reasons={}
F5 kind=MP prefix='Answer follows.\n' applicable_n=1964 invariant_k=1964
F5_STRATUM FJ1 n=1296 k=1296
F5_STRATUM FJM n=492 k=492
F5_STRATUM MULTI n=31 k=31
F5_STRATUM DANGLE n=57 k=57
F5_STRATUM BARE n=88 k=88
F5_PID_COMPOSITE unit=file+pid;C=file+cell+rep n=210 k=210
F5_PREFIX_BRACKETS=False transformed_all=True
```

Oracle command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin; rc=$?; printf 'EXIT=%s\n' "$rc"; exit 0` — child exit **0**. Relevant exact output: `POPULATION candidates=1964 included=1964 excluded=0`; `EXCLUDED baseline=0 missing_want=0 meta_truth=0`; `F5 kind=MP n=1964 k=1964`. It agrees with the independent recomputation and core. The oracle uses the different representative prefix `This response is below.\n` (`perturb_oracle.py:300-302`); both representatives are one-line prose without bracket/fence syntax, so this is the same registered F5 transform class, not a byte-identical transform.

Core summary command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary | python3 -c 'import sys; [print(line.rstrip()) for line in sys.stdin if line.startswith(("FAMILY F5", "CLASSES F5"))]'; rc=${PIPESTATUS[0]}; printf 'EXIT=%s\n' "$rc"; exit 0` — core exit **0**. Exact F5 output:
```text
FAMILY F5 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F5 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
```

## Scope, draft, residual risk

`build_population` counts raw+ok candidates and rejects unsupported graders, non-string raws, non-boolean stored verdicts, unavailable meta truth/turns, stored-want/meta disagreement, baseline replay errors/mismatches, pin changes, and any count other than 1964 (`plans/grader_perturb.py:187-256`). The recomputation found none. C-MONO was replayed through its `valid_latin` branch; other C cells through their `grade_c` branch (`:259-276`). F5 itself has no applicability filter; `family_stats` skips only `None` transforms/errors and groups C composite units as file+cell+rep (`:504-563`).

`grader.py:121-134` uses unanchored fenced-block and bracket-candidate searches. The exact prefix `Answer follows.\n` adds neither a fence nor any bracket character, leaving all candidate spans and the selected parsed answer unchanged; the all-record replay confirms this. This is scoped invariance of this parser/prefix over the pinned corpus, not evidence about arbitrary prefixes or future response formats.

Draft review: `grader-perturbation-audit.md:45,66` describes F5 as a bracket-free prose prefix and reports 1964/1964; both are supported. Its D1 wording at `:50-52` correctly makes D1 PC capture on eligible PASS turn>1 operations, not MP correctness invariance. F5's MULTI and DANGLE class intervals have lower bounds `.888` and `.937`, below `.95` despite 31/31 and 57/57 observed successes; they are not observed failures, and the draft does not claim each stratum clears the pooled-family bar. F5 pid-composite is 210/210; nominal intervals are descriptive, not future-response guarantees.

## Verification gaps

LSP was unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list contained no LSP device. Therefore no LSP status/references/definition/diagnostics could be obtained; the one grep call only located grader definitions and is not semantic evidence. Runtime recomputation, oracle output, and the directly cited source lines are the evidence above. No tool was installed.

VERDICT: **SCOPED PASS — F5 is invariant on all 1964 pinned records; no actionable F5 finding. Advisory only; this is not an admission verdict.**
