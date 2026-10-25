# ExecPerturbCases — amendment-aligned hand oracle

- Clone `/tmp/kengaku-r26-ExecPerturbCases`, branch `r26-ExecPerturbCases`; observed base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`. No clone commit. Only clone outputs are the two files below.
- `plans/fixtures/r26/perturb_cases.jsonl` — 278 cases, 290274 B; sha256 `7385a799bee93797d6868280c95edc54b07dfef928ecb8140e11dc65fa1d247c`.
- `plans/fixtures/r26/verify_perturb_cases.py` — stdlib retained verifier; sha256 `94e894588c38c6f4f161a6c3d1ec03d6cd3c16a4965960f4ebd16144f41a5f15`.
- Amendment 1 supersedes the original wave-1 F1/F2/D1 semantics; Amendment 2's PC accounting is represented. D1 has kind `PC`; `regraded_ok` records ordinary grading and separate `metric_success` records capture of previous truth.
- Matrix key: `bl` = baseline regrade; P/F = perturbed grader regrade; `-` = not applicable; D1 `C` = PC captured previous truth. Edge labels are synthetic shape tags; `real-*` names a matching committed raw shape.

|case|shape|bl|F1|F2|F3|F4|F5|F6|F7|D1|G1|G2|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|B01|fence, real r8:11|P|P|P|P|P|P|P|P|C|F|F|
|B02|indented fence, turn 1|P|P|P|P|P|P|P|P|-|F|F|
|B03|fence without language|P|P|-|P|P|P|P|P|C|F|F|
|B04|bare one-line JSON|P|-|-|P|P|P|P|-|C|F|F|
|B05|bare indented JSON|P|-|-|P|P|P|P|P|C|F|F|
|B06|two fences, real r8:223|P|F|F|P|P|P|P|P|C|F|F|
|B07|two fences, last unparseable|P|-|-|P|P|P|P|P|C|F|F|
|B08|CRLF|P|P|P|P|P|P|P|-|C|F|F|
|B09|prose braces before answer|P|P|P|P|P|P|P|P|C|F|F|
|B10|prose `[2,5]` after answer|P|F|F|P|P|P|P|P|C|F|F|
|B11|unparseable prose braces|P|P|P|P|P|P|P|P|C|F|F|
|B12|prose `{}` after answer|P|F|F|P|P|P|P|P|C|F|F|
|B13|filler `ready`|F|-|-|-|-|F|F|-|-|-|-|
|B14|truncated unterminated fence|F|-|-|-|-|F|F|F|-|-|-|
|B15|dangling close fence, real r11:92|P|-|-|P|P|P|P|P|C|F|F|
|B16|duplicate keys, real r12:157|P|P|P|P|P|P|P|P|C|F|F|
|B17|single-key dict|P|P|P|P|-|P|P|P|C|F|F|
|B18|baseline fail, no-op target|F|F|F|F|F|F|F|F|-|-|-|
|B20|sequence, fenced|P|P|P|P|-|P|P|P|C|F|F|
|B21|sequence, bare one-line|P|-|-|P|-|P|P|-|C|F|F|
|B22|sequence, depth-3 nested list|P|F|F|P|-|P|P|P|C|F|F|
|B23|sequence, depth-2 bare list|P|-|-|P|-|P|P|-|C|F|F|
|B30|grade_c, nested lists|P|P|P|P|P|P|P|P|-|F|F|
|B31|grade_c, bare indented|P|-|-|P|P|P|P|P|-|F|F|
|B32|grade_c, extra ungraded key|P|P|P|P|P|P|P|P|-|F|F|
|B33|grade_c, no-rule claimed violation|P|P|P|P|P|P|P|P|-|P|F|
|B34|C-MONO valid_latin, nested list|P|P|P|P|-|P|P|P|-|F|F|

**Amended variants:** `B06-F1-strip-all=P` (historical alternative, not acceptance); `B16-F4-textual=F`; `B32-G2-first-key=F`; `B32-G1-note-value=n/a`; `B32-G2-note-key=n/a`; `B33-G1-square-token=F`; `B01-D1-prev-equals-want=n/a`; `B02-D1-turn-one=n/a`.

**Retained verifier:** `python3 plans/fixtures/r26/verify_perturb_cases.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` → `CASES total=278 unique_ids=278 family_checked=272 instance_regrade_checked=6 failures=0`, exit 0. It independently recomputes each baseline and transformed result with grader.py, checks PC capture/outcome/counting, and checks exact `apply_family` applicability, text, and metric against the integrated core for every family-scope case. It skips only canonical transform comparison on explicitly labeled historical/noncanonical variants; those are still regraded.

**Negative control:** changed only `B10-F1.regraded_ok` to true in a scratch fixture and ran the same command with `--cases /tmp/kengaku-r26-ExecPerturbCases-scratch/wrong-expectation.jsonl`. It reported `failures=2`, `B10-F1 expected regrade mismatch`, `B10-F1 live core metric differs from fixture outcome`, exit 1.

**Observed result / interpretation:** 278 total = 27×10 base family cases + 8 variants; 272 family-scope and 6 instance variants. F1/F2 each have 4 synthetic flips; F3/F5/F6/F7 are invariant on applicable cases. D1 has 18 synthetic PC captures and 11 N/A; its regraded verdict is not the PC outcome. G1 has 24 detected and one missed (B33: changing the `C-norule` violation value leaves `grade_c` true); G2 detects all 25 applicable cases. The integrated core report records F1/F2 `1802/1819`, `MULTI 14/31`, D1 `909/909` PC captures, `15168` audited verdicts plus `909` separate PC checks and 9 interval families; see `ExecPerturbCore.md` and claims Amendment 2.

**Evidence and scope:** all expected regrades were checked against grader.py and the live integrated core, root as shown above. LSP was unavailable in the mounted tool inventory. No installs. No live lane source/index/jj changes; only this advisory report was written in the lane tree.

VERDICT: DONE — amendment-aligned fixture and retained stdlib verifier are complete; the live-root check passes, and the planted wrong expectation fails as required.
