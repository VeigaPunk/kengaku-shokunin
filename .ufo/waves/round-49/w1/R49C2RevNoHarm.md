# R49-C2 reviewer — coverage/quality harm check

Axes named: **coverage** (judged axis), **quality** (secondary admission-risk check). This is a scoped review of the frozen R49-C2 admission proposal, not an admission verdict.

## Freeze and revision

- Stage-1 freeze exists in the committed lane tree: `9d2900af41e4d1fc6022eff99010436fde6dbd93`, commit time `2026-10-28T09:14:40-03:00`; verified with `git cat-file -t` and `git log -1 --format='%H %cI %s'` before any probe/counter scoring. The freeze predates all measurements in this review.
- Reviewed revision (`REV`): `9d2900af41e4d1fc6022eff99010436fde6dbd93` (clean frozen-base clone; no scored counter/probe run).
- Required first reads completed in full: `plans/round-49-claims.md`, `corpus/lessons/round-48-verifier-spotcheck.md`; also read `corpus/lessons/round-48.md`, the committed C2 entry, frozen receipt/dry table, probe, C3 counter, `test.sh`, and `task.toml`.

## Plausible harm and falsifiable check

**Coverage/quality harm: a stage-2 `violates=toolchain` case can satisfy V7 without measuring the task's toolchain, so its derived requirement-map label can be false or vacuous.** The probe explicitly says it binds host `/usr` and substitutes host gcc/python for image gcc 13.2.0/python 3.12.3 (`plans/polyglot_c_py_probe.py:19-27,49-55`). Its grade path starts a separate bwrap process with `/usr` read-only-bound from the host (`:349-363,370-393`), so a case recipe cannot change the grader's compiler/interpreter. On this host, `gcc --version` is `gcc (GCC) 16.2.1 20260810`, `python3 --version` is `Python 3.14.8`; GCC reports `__STDC_VERSION__ 202311L`. The captured grader's actual task image declaration is `alexgshaw/polyglot-c-py:20251031` (`task.toml:29`), and the instruction names gcc 13.2.0/python 3.12.3 (knowledge entry §Summary/§Limits). Thus a toolchain-sensitive case's `observed=` and V7 label are only host observations.

V7 does not establish that a case truly violates its tag: `receipt_cases()` reads `violates=` directly from the receipt (`plans/round46_c3_verify.py:304-310`); `v7()` checks token presence, cites, and derives a label from the corresponding `observed` values (`:374-413`); `derive()` maps all-fail/all-pass/mixed to enforced/unenforced/partly (`:366-371`). It never tests causality of the attribution. In particular, changing a receipt token can manufacture an apparent exercised tag. This compounds the toolchain stand-in: V7's positive-presence fix is not itself evidence that all seven semantic requirements were exercised.

**Exact falsifiable check:** for every stage-2 receipt case with `violates=toolchain`, replay that exact frozen recipe and captured grader (a) in the current probe environment and (b) inside the task's exact pinned image digest, through the captured `test.sh` reward path (`uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`). Compare the case's `observed` result and reward between environments. A single difference falsifies the host-derived toolchain row/label; no case that can distinguish the declared toolchain versions means the claimed toolchain coverage is unexercised, not demonstrated. Separately, for each `violates=t` attribution used to support a label, run a committed counterfactual grader mutation that relaxes only requirement `t`; require the tagged failing case to flip to pass (and the relevant control to remain correctly classified). If it does not, attribution is unsupported and V7's map can pass on self-labeled tokens.

A secondary concrete risk is the unexecuted wrapper/reward path: probe harness calls the test function directly, explicitly without pytest (`polyglot_c_py_probe.py:25-32,292-342`), while captured `test.sh:18-28` invokes pytest 8.4.1 plus the CTRF plugin under Python 3.13 and translates pytest exit status into reward. **Exact check:** run each frozen case through the pinned image's actual `test.sh`, recording pytest exit and reward file; compare with the probe receipt. Any disagreement falsifies the receipt's claimed reward-level equivalence. This is not currently measured by the probe.

## Commands run and observed outputs

1. `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `commit`.
2. `git log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)`.
3. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` in the unique scratch; `git checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C2RevNoHarm/lane`; `git rev-parse HEAD` → `9d2900af41e4d1fc6022eff99010436fde6dbd93`.
4. `gcc --version 2>/dev/null | head -1; python3 --version; which bwrap pytest 2>/dev/null; ...; command -v docker podman` → `gcc (GCC) 16.2.1 20260810`; `Python 3.14.8`; `/usr/bin/bwrap`; `docker: /usr/bin/docker` (no pytest path printed).
5. `gcc -fsyntax-only t1.c` with `int main(){return f();}` → `error: implicit declaration of function ‘f’ [-Wimplicit-function-declaration]`, exit 1; `gcc -dM -E - </dev/null | grep -E '__STDC_VERSION__'` → `#define __STDC_VERSION__ 202311L`. This establishes the host compiler default, not the image's behavior.
6. Read-only inspection commands/tool reads: `ls corpus/evidence/round46/tb2-polyglot-c-py/`, `wc -l ...`, `grep -n ... plans/round46_c3_verify.py`, and source reads cited above. No external URL was opened; therefore no URL/access-date/quote is claimed by this seat.
7. **No scored probe/counter execution was run.** No R49-C2 admission or score claim is made.

## Limits and verdict

I did not pull/run the task image or execute the probe. Therefore actual image-vs-host verdict divergence is unmeasured; the falsifiable checks above are recommendations, not claimed outcomes. The definite finding is narrower: the planned static evidence and V7 mechanism cannot by themselves substantiate semantic `toolchain` coverage or causal validity of author-supplied `violates=` attribution. Existing entry limits candidly disclose the host-toolchain and pytest substitutions, but that disclosure does not make the resulting labels image-level evidence. The captured grader's fixed-point weakness and non-idempotence are already documented and are not new harms from this review.

VERDICT: **plausible coverage/quality harm identified; exact checks stated; no admission recommendation beyond withholding trust in host-derived `toolchain` coverage until the image/reward-path checks pass.**
