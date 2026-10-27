# R44RCritEntryOverclaim — overclaim review of the landed tb2 feal-linear grader entry

Seat: R44RCritEntryOverclaim (critic, residual wave). Target: `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` (landed at commit 2a263e5a56ef6d48d06805e1ccd106de5de9ba66). Review is read-only; no lane file modified.

## Method

Every sentence in the entry (432 lines) was checked against:
- the row captures `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` (SHA256SUMS-pinned, 12 files: 9 S-rows + `feal.c` + `gitignore` + `SHA256SUMS`);
- the probe `plans/feal_linear_probe.py` and its receipt `corpus/evidence/round44/feal-linear-probe.txt`;
- the counter `plans/round44_c2_verify.py` (V10 DECISIVE map, V7 label rule, V11 states);
- the round-43 histogram `R43ConsiderThese.md` (F1 definition);
- the round-44 freeze `plans/round-44-claims.md` and the controls under `.ufo/waves/round-44/claims/`.

## Verifications performed (all passed)

| Check | Result |
|---|---|
| Constants block `test_outputs.py:4-103` has 100 decimals, first/last `1050628112036199672` / `15259742852319968006` | parsed 100 |
| Recompute chain `sha256(sha256("0x68e630x625710x1f61c0xb74a5") + pack(">Q", 32+i))[:8]` for i=0..99 vs soln block | **equal, in order** (python) |
| `solve.sh:289` `"./decrypt ciphertexts.txt 0x%x 0x%x 0x%x 0x%x"`; `:290` `system(cmd);`; `:303-304` gcc/redirect | byte-exact |
| `decrypt.c:136` `printf("%lu\n", plaintext);` | exact line |
| `test.sh:18-22` uvx/pytest; `:25-29` `$?`→reward | byte-exact |
| `gen.py:12,19-20,26-28,60-62`; `Dockerfile:2,5,6,8,9-11,13-14`; `instruction.md:1,4,7,8,9-10`; `task.toml:15,18,19,22,25,29,30-31,34`; `README.md:31-32` | all cited lines correct |
| Receipt `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0` | matches entry |
| Entry case table ids/order/verdicts = receipt order | matches |
| Mechanism rows all fall inside counter V10 DECISIVE allowed lines; quotes verbatim on line | matches |
| Requirement-map labels recomputed per V7 rule over all violating receipt cases | enforced=plaintexts-file; partly ×3 |
| r43 feal-differential key reseeding (`srand(time(NULL))` per process) | confirmed in r43 entry |
| No randomness in this task's sources (`srand`/`rand(`/`time(NULL)` grep over feal.c, gen.py, decrypt.c) | none |
| `stagecheck cases=14 failed=0`; fetch time `20:10:09 -03` | match claims/controls |

## Category audit

### 1. Sentences generalising beyond the 14 cases — none found
All strong claims are static-code facts (whole scoring code is 17 lines: `test_outputs.py:106-122`), not case-empirical extrapolations:
- "There is no count, no order, no format and no exactness check." (line 22) — direct reading of `test_outputs.py:120-122`.
- "Nothing is checked but presence." (line 44); "the boundary is exactly 'all 100 expected decimal strings occur somewhere', nothing more." (line 313) — code-backed; the one-missing/concatenated pair sizes it.
- "Whatever goes wrong … the exit status is non-zero and reward.txt gets 0." (findings 10) — `test.sh:25-29`.
Every empirical claim is explicitly scoped: "On the 14 frozen end states …" (line 32), "The 14 cases are the claim's whole surface" (line 348), plus the whole "What the probe does not show" / "Negative space" sections fence unmeasured states (symlink, directory, mid-number interleave, trajectories, validity, difficulty, solvability, Harbor execution). No sentence asserts behaviour outside the captures or the 14 states.

### 2. Sentences resting on a non-row capture (feal.c, gitignore) alone — none found
Capture dir contains `feal.c` and `gitignore`, which are not S138-S146 rows.
- `gitignore` is never mentioned anywhere in the entry.
- `feal.c` appears only inside quoted material from row captures: `instruction.md:1` (quote row, line 162) and `Dockerfile:9` (Initial-state table row, line 128). No claim cites or rests on the `feal.c` capture file itself. (The cipher bytecount and build lines are all row-captured.)
- The class sentence (line 24-26) rests on `test_outputs.py:120-122` (a row), not on feal.c.
Conclusion: the "capture that is not a row" overclaim category is empty.

### 3. Grader/harness facts not shown by a capture line — none false; all traceable
Harness statements are backed by the frozen probe instrument (`plans/feal_linear_probe.py`, digest-pinned in `pkg-spec-r44.json`), which is the program that produced the receipt:
- "inside bubblewrap with network, pid and ipc namespaces unshared" (line 108) — `sandbox_argv` uses `--unshare-net --unshare-pid --unshare-ipc` (probe:197).
- "host python3, host gcc and host /usr/bin/bash" (lines 336-337) — probe `TOOLS`.
- "graded … a second time … over the same /app, /tests and /pub" (lines 323-324) — `run_case` mode `grade` returns `[harness(...), harness(...)]` on the same work tree (probe:239).
- "pytest was not run … the harness maps the one function's outcome onto an exit status" (lines 341-343) — `HARNESS_PY` imports `test_outputs.py` and calls `test_attack()` directly; no pytest, no `reward.txt` (probe:158-189).
- "the image never ships the tests" / "deletes only gen.py" (lines 28, 291) — argument from `Dockerfile` (only `COPY task-deps/ /app/`; `:14` rm gen.py); disclosed as absence-from-capture, correct.
- "verified here: the 100 constants equal sha256(…)" (line 143-144) — independently recomputed, equal in order.
No grader/harness fact was found that is asserted without a traceable capture line or probe line.

### 4. Novelty implication — none
"No novelty is claimed" appears twice (lines 79, 376-377); the Prior-art section (lines 364-377) reports the search date/surfaces, explicitly marks the substring weakness, hash-chain replay and key-decryption as "not found" with the qualifier '"Not found" means absent from those surfaces on that date, not non-existence', and marks adjacent/published prior art (issue #1637, tbench.ai, Berkeley RDI item 5, README:31-32). No sentence presents a finding as new.

### 5. Class sentence vs round-43 histogram F1 — HOLDS
- Histogram definition (`R43ConsiderThese.md:10,15`): `F1 file constant/answer compare` = the decisive assertion reads a file and compares it against constants/answer embedded in the grader; `R43ConsiderThese.md:26` already classifies this task F1 with deciding line `:122` `assert c in data`, note "100 expected plaintexts are constants in the grader".
- Entry class sentence (lines 24-26): "Constant-compare on a text file: the grader never imports or executes anything the agent wrote, and it never parses the file — it asks, for each of 100 expected values, whether those digits occur anywhere in the bytes."
- Correspondence: constant/answer compare over an agent-written file = F1; "never parses" is exactly the F1/F2 boundary (F2 = parsed/computed/pattern/structured); "never imports or executes" is the P1/M1 boundary. The sentence both matches the histogram's F1 and the histogram's own row for this task. It holds.
- The companion sentence (line 78) "The two graders therefore share a class family … and differ in mechanism (file bytes vs imported module)" was examined as the nearest miss: it groups the r43 M1 entry with F1 under an informal trait (single constant compare), but it explicitly retains the mechanism distinction and makes no claim that the histogram classified them together. Not counted as an overclaim.

## Conclusion

The entry is self-limiting (14-case scope, negative space, falsifier, explicit novelty denial) and every factual sentence verified against a row capture, the probe source, or the receipt. No sentence generalises beyond the 14 cases, none rests on feal.c/gitignore alone, no harness fact is unsupported, no novelty is implied, and the class sentence holds against the round-43 F1 definition. Counted overclaims: 0.

VERDICT: overclaims-0
