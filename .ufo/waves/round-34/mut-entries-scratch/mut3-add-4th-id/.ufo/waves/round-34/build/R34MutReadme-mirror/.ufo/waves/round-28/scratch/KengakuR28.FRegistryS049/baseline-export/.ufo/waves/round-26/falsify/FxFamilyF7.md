# FxFamilyF7 — scoped falsification report

- Reviewed integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` vs base `f11bffbf9caa9c9e286fb32c568b81b97719656a` (`.ufo/waves/round-26/integration-revision.txt:1-5`); draft remains unadmitted.
- LSP unavailable: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics were available. Findings use direct reads and execution, not grep as semantic proof.

## Finding — low, oracle applicability boundary (no current-data count impact)

`plans/fixtures/r26/perturb_oracle.py:304-307` returns a non-None F7 transform whenever raw has `\n`; on already-CRLF input its CRLF→LF→CRLF substitutions return the identical string. It therefore counts a no-op as an applicable oracle trial. Core `plans/grader_perturb.py:434-437` explicitly excludes all-CRLF/no-bare-LF input. Repro from `/tmp/r26_f7_independent.py`: synthetic `edge='```json\r\n{"x":1}\r\n```'` → `core_applicable=False oracle_applicable=True oracle_noop=True` (exit 0). Recommend aligning the oracle's no-op applicability guard and adding this edge to its selftest. The pinned corpus has zero all-CRLF records, so this does not alter observed F7 `n/k` or contradict the draft's finite-population result; it narrows what the oracle comparison proves.

## Frozen-raw recomputation and results

All four SHA-256 values match the pins in `plans/grader_perturb.py:29-33` and `plans/fixtures/r26/perturb_population.sha256:1-4`:
`bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204` (r8), `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb` (r9), `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad` (r11), `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1` (r12). Oracle: 1964 candidates/included, excluded 0. Independent raw scan (`python3 /tmp/r26_f7_independent.py`, exit 0): `RAW records=1964 pin_verified=4`; `F7 independent n=1876 k_extracted_answer_unchanged=1876 excluded_no_lf=88 excluded_all_crlf=0 excluded_mixed_crlf_lone_cr_no_bare_lf=0 any_lone_cr=0`. Every eligible extracted answer is unchanged; exact baseline replay for all included records was confirmed by both audit and oracle, so MP `k/n=1876/1876`.

Commands and observed output (each exit 0):

- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --summary` → `FAMILY F7 kind=MP n=1876 k=1876 rate=1.000000 cp95_nominal=[0.998036,1.000000] verdict=PASS composite=194/194@1.000000 cp95_nominal=[0.981165,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS`.
- Same command → `CLASSES F7 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]`.
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` → `POPULATION candidates=1964 included=1964 excluded=0`; `F7 kind=MP n=1876 k=1876` (oracle emits no strata/composite).
- Independent scan strata: FJ1 1296/1296; FJM 492/492; MULTI 31/31; DANGLE 57/57; BARE 0/0. Independent pid composite: 194 units/194 preserved. All observed strata and composite pass; CP95 is nominal/descriptive, not iid generalization.
- `git diff --unified=5 f11bffbf..HEAD -- plans/grader_perturb.py plans/fixtures/r26/perturb_oracle.py | grep -n -A14 -B8 'F7\|CRLF'` confirms the distinct integrated F7 guards at `grader_perturb.py:434-437` and `perturb_oracle.py:304-307`.

## D1 policy check (separate from F7 MP)

Amendment 1 (`plans/round-26-claims.md:188-191`) requires D1 as PC capture on baseline-PASS ordinary operations with turn>1 and changed previous truth. Core sets D1 kind PC (`grader_perturb.py:18-19`), gates these conditions plus A-MONO/B/C exclusions (`:438-449`), and `_metric_success` scores extraction of previous truth (`:490-497`), not correctness invariance. Summary marks D1 `NOT_SCORED`; `python3 /tmp/r26_d1_policy_check.py` (exit 0) reports `D1 kind=PC eligible=909 captures=909 violations=0`; eligible cells: A-CKPT 13, A-CKPT10 10, A-CKPT4710 198, A-CKPT710 86, A-INC 585, T-DENSE 10, T-SPARSE 7. Draft `grader-perturbation-audit.md:50-52,71-85` correctly describes capture policy and separates it from MP robustness.

## Residual risk

No CRLF, lone-CR, mixed-newline or BARE F7 case was observed in the pinned corpus. Draft `grader-perturbation-audit.md:46-47,68` is accurate for that scope; the oracle no-op edge remains untested there. No source-quote or admission judgment is made by this F7 seat.

VERDICT: F7 SCOPED PASS FOR THE PINNED POPULATION; LOW-SEVERITY ORACLE NO-OP APPLICABILITY GAP OUTSIDE THAT POPULATION.