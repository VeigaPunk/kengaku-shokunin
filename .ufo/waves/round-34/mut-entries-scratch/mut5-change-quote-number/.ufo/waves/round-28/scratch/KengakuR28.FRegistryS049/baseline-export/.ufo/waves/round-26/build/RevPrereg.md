# Round 26 preregistration review

Scope: read-only review of `plans/round-26-claims.md` against frozen base `f11bffbf`; no instrument output or tests run.

## High — amend before instrument output

1. **CP95 unit/dependence is not justified** — claims `:69-73` use record-level Clopper–Pearson intervals as 95% bounds. These files contain repeated observations per `pid`: base JSONL count `raw+boolean-ok, identified records / unique pids / max per pid` = r8 `172/10/18`, r9 `128/8/16`, r11 `320/64/5`, r12 `1328/112/17`. The prereg does not establish that these same-pid records are independent Bernoulli draws, so record-level CP is not guaranteed 95% coverage absent an independence model.
   **Proposed A1 text:** “Freeze the inferential unit and dependence model before output. Use `(file,pid)` as the cluster unit (r8 pid-less C rows use `(file,cell,rep)`); a cluster succeeds for MP only if all its applicable records are invariant, and for MC only if all its baseline-PASS records become FAIL. Compute CP95 over eligible clusters; retain record-level rates as descriptive counts. If retaining record-level CP, document and justify an independent-record sampling model and limit the 95% interpretation to that model.”

2. **P1 population, exclusions, and exit status are ambiguous** — `:46-52` defines population as records already reproducing baseline, while `:75-79` makes baseline reproduction an exit-0 condition and exit-1 “baseline inconsistency”; the excluded-record behavior is not reconciled. “sha256-pinned” also omits hash granularity, and a stored-`want`/meta mismatch has no outcome.
   **Proposed A1 text:** “P1 candidates are every JSONL object with string `raw` and boolean stored `ok` in the four named files; pin SHA-256 over each complete base-file byte sequence. Baseline-mismatching candidates (including a stored-`want`/meta mismatch) are counted once as excluded, never perturbed, and cause exit 1; family denominators use only candidates whose baseline and truth cross-check reproduce. `TOTAL.population` means candidate count, `excluded` means excluded candidates, and `audited_verdicts = Σ family applicable-record counts.”

3. **C1 adapter map does not match the frozen data/grader** — `:42-52` omits C grading in the “every” statement and says `grade_c` for all r8 C-cells. In base `results.jsonl:253-268`, the 16 C rows lack `pid` and have `want: null`; `grader.py:482-504` uses `grade_c` only for C-conflict/C-benign/C-norule, but `valid_latin` for C-MONO. The interface’s required `Rec.pid` and D1 predecessor key are therefore undefined for these rows.
   **Proposed A1 text:** “Map r8 A-/B-* to `grade_state`; C-conflict/C-benign/C-norule to `grade_c` with the frozen `c_specs`; C-MONO to `valid_latin` (not `grade_c`). Map r9/r11 to `grade_state`, r12 A-* to `grade_state`, and r12 T-DENSE/T-SPARSE to `grade_seq`. For pid-less r8 C records, set `pid=null`, identify by `(file,cell,rep,turn)`, set `want=null`, and do not apply D1 absent a same-rep predecessor.”

4. **Family transforms/applicability are not frozen** — `:54-67` leaves eligibility and the selected mutation open, changing `n/k` and oracle counts. “compact ↔ indented,” “previous turn,” G1’s value/token, G2’s key/element, and prose/line-ending transforms are all non-unique.
   **Proposed A1 text:** “Apply each family once to unmodified `raw`; inapplicable returns `None` and is omitted from its denominator. F1/F2 require exactly one recognized fence (strip its pair; change only lowercase `json` to `JSON`); F3 replaces the payload with compact JSON when it contains LF, otherwise `indent=2`, preserving insertion order; F4 reverses top-level dict order; F5/F6 use exact lines `Answer follows:` / `End of answer.`; F7 normalizes CRLF/CR/LF to CRLF. D1 uses the greatest lower turn for the same frozen record key, else is inapplicable. G1 traverses sorted dict keys/lists left-to-right and changes the first scalar (int +1, string + `*`); G2 removes the first sorted top-level dict key or first top-level list element.”

5. **P3b compares historical counts to the wrong timepoint** — claims `:131-133` put PROVINCE `:112` and `:119` against the measured-tree census, but `PROVINCE.md:112`’s 25-row value is tied to the round-24 receipt; `:119` contains historical “26 at base” and “37 after round 25” claims. The measured base census is 42, so treating all those as current both mislabels historical assertions and conflicts with `:145`’s predicted `mismatch=0` unless their snapshots are distinguished.
   **Proposed A1 text:** “Freeze a snapshot map: `PROVINCE.md:112`’s 25 against `round24-census/after.txt`; `:119`’s 26 against r25 base `6180e4f`, and 37 against r25 tip `9d8a00d`; the R26-E3 correction’s 42 against `f11bffbf`. Pin the census command for each snapshot. R26-E3 supersedes only the 37-after-r25 assertion.”

## Medium

6. **P3a/P3c pin selection needs an explicit manifest** — `:128-130` says “every numeric token” but does not distinguish output values from round labels, paths, hashes, or line numbers, nor map each token to a receipt. `:134-135` requires a target line for every SHONEN pointer, while base `SHONEN.md:5-6` has a bare `SKILL.md` pointer with no line.
   **Proposed A1 text:** “For P3a, freeze a token→receipt/output-field table and compare only declared result fields, excluding identifiers, paths, hashes, and round labels. For P3c, freeze `(pointer, resolved path, target line or whole-file digest, expected token)` for every pointer; bare paths must name their target explicitly.”

## Low

7. **Readiness state lacks matching evidence** — claims `:3-4` says `untracked=0`; committed `corpus/evidence/round26-calibration/round-start.txt:2` records `tracked=0 untracked=2` at 02:31:41 -03. This could be an earlier readiness check, but its timestamp/receipt is absent.
   **Proposed A1 text:** “Name the exact readiness timestamp and receipt showing `untracked=0`; otherwise report the committed round-start value (`untracked=2`) and identify those paths.”

## Residual risk and verification gaps

Q13’s red-before premise is supported by the 8ea41f9 Gate row: it cites the oracle script plus generic “by wave-2 seats,” while the commit tree has only round-25 build reports, no second-seat report path. I did not execute the timing checker or any instrument. No LSP device was available; grader findings above are direct reads of the frozen base source/data, not semantic-index results. No tools installed or updated.

Installs: none.
VERDICT: Append Amendment 1 resolving findings 1–5 before any C1/C2 instrument output; freeze finding 6’s manifests as part of that amendment, and correct or receipt finding 7.