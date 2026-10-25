# ExecFamilyEdges — C1 family applicability + edge census on the real P1 population (read-only probe)

Seat KengakuR26-2.ExecFamilyEdges-4 · axis novelty (C1) · scratch `/tmp/kengaku-r26-familyedges-probe/base` = `git archive e0037a8da268`. `git diff --stat f11bffbf e0037a8 -- grader.py plans/attrib_calibration.py <4 results files>` → empty, exit 0, so these bytes equal base f11bffbf.
Commands: `python3 -B family_edges.py base`, then `python3 -B supplement.py base` (Python 3.14.8). They load grader.py and plans/attrib_calibration.py by spec with dont_write_bytecode, so the lane tree is untouched. LSP was not used (direct source reads). This is a probe of candidate rules, not instrument output.

## Population (probe output)
- sha256 pins: r8 `bd986e5e…2204`, r9 `c20158bd…fbcb`, r11 `918bf7aa…51ad`, r12 `ad9c88e7…42f1`. raw+ok candidates: 1964 = state 1708 + seq 240 + c 12 + C-MONO 4. PASS 1021 / FAIL 943.
- A span-tracking re-implementation equals `grader.extract_json_block` on 1964/1964. The baseline re-grade reproduces stored ok on 1964/1964. Meta-derived want equals stored want on 1948/1948.
- C-MONO (results.jsonl:256,260,264,268) is graded by `valid_latin` (grader.py:498-504): 4/4 reproduce. Through `grade_c`: 0/4, a false exclusion. `Rec.grader` {state,seq,c} needs `latin`. B-cells (32, e.g. results.jsonl:221) use got==want (grader.py:468-476), which is ≡ grade_state ok: 32/32.
- Extraction path: fence 1819; fallback 145. The 145 are 88 no-marker (r11 A-CKPT710 2; r12 A-CKPT710 2, T-DENSE 48, T-SPARSE 36; e.g. results-r12.jsonl:232) plus 57 half-fenced (bare JSON + lone closing ```, no opener; e.g. results.jsonl:25). None 0, scalar 0. dict 1720 (0 with <2 keys), list 244. Fallback PASS 26.
- Multi-fence raws: 31, all r8 B-cells ("After operation 8/9/10" blocks, results.jsonl:223). Penultimate block ≠ extracted in 31/31.
- Fence-path raws with a parseable bracket candidate after the extracted fence: 0. CR in raws: 0. No-LF raws: 88. Unlabelled fence-path openers: 0.

## Decision table (bar 0.95; exact CP95 via attrib_calibration.clopper_pearson + verdict)
| fam | recommended applicability · transform | n | k | CP95 | verdict | edges (count · example) |
|---|---|---|---|---|---|---|
| F1 | fence path only (145 fallback n/a: no fence fed their extraction) · drop ONLY the extracted fence's opener line + closer | 1819 | 1802 | [0.9851,0.9945] | PASS | Multi-fence stratum 14/31 [0.2732,0.6397] FAIL: penultimate block taken 31/31, 17 PASS→FAIL (results.jsonl:223). Single-fence 1788/1788. Strip-ALL 1819/1819 hides this. Any-``` rule adds 57 half-fenced rows that cannot flip |
| F2 | fence path ∧ extracted opener `json` (0 unlabelled) · relabel ONLY that opener | 1819 | 1802 | [0.9851,0.9945] | PASS | Record-identical to F1 (grader.py:122 skips ```JSON → same route). Relabel-ALL 1819/1819 |
| F3 | every extracted container · rewrite only the extracted span (fence group 1 or bare match), compact↔indent=2 | 1964 | 1964 | [0.9981,1] | PASS | Fallback stratum 145/145 |
| F4 | extracted dict with ≥2 keys (244 lists n/a) · keys reversed, same layout class | 1720 | 1720 | [0.9979,1] | PASS | Includes 12 C dicts (2 keys) |
| F5 | all · prepend a line with no backtick or bracket | 1964 | 1964 | [0.9981,1] | PASS | Invariant by construction: no :122/:128 match can start in such a prefix |
| F6 | all · append a line with no backtick or bracket | 1964 | 1964 | [0.9981,1] | PASS | Invariant by construction: no match can end in such a suffix; the 57 lone ``` stay unpaired |
| F7 | raws with LF and no CR · LF→CRLF | 1876 | 1876 | [0.9980,1] | PASS | 88 no-LF raws would be no-ops → n/a |
| D1 | state/seq ∧ prev≠want · append fenced prev = start-of-turn truth: truth[turn-2] (t≥2), init (t=1: A-INC 82, A-MONO 82), truth[6] (B 32) | 1929 | 926 | [0.4575,0.5026] | FAIL | C/C-MONO 16 n/a. prev==want 19 excluded (no-op op, SET brackets 8→8, results-r9.jsonl:254; 14 would go FAIL→PASS). Distractor captured 1948/1948 |
| G1 | baseline PASS (state 991, seq 17, c 9, latin 4) · state: sorted-first key +1; seq[0]→first other vocab token; square[0][0]→next of ABCD | 1021 | 1021 | [0.9964,1] | PASS | 14/17 seq lists hold duplicate tokens (results-r12.jsonl:504) → never "swap". A row swap keeps C-MONO PASS 4/4. violations[0]+1 fits only 5/9 C (C-norule has [], results.jsonl:255) |
| G2 | baseline PASS · delete sorted-first key / element 0 / C `square` / C-MONO row 0 | 1021 | 1021 | [0.9964,1] | PASS | 0 single-key dicts; 0 empty lists (seq lens 5–10). Deleting `violations` also gives 9/9 |

Expected under these rules: `TOTAL population=1964 excluded=0 audited_verdicts=17097 families_with_interval_verdict=10` (excluded=4 if C-MONO is routed to grade_c).

## Findings
1. D1 verdict-invariance is a base-rate artefact. k=926 is exactly the baseline-FAIL rows: each stays FAIL even though the distractor was extracted. PASS rows only: 0/1003 [0,0.0037]. The A-MONO stratum shows 80/82 [0.9147,0.9970] INDETERMINATE although it was fooled 82/82 (ext_same 0). Report ext_same (3/1929 unchanged) beside k, or score D1 on PASS rows.
2. A bare `truth[turn-2]` at turn 1 evaluates to Python's truth[-1]. For A-MONO (82) and B (32) that IS the want, so D1.naive gives 108 FAIL→PASS: 80 A-MONO + 14 B + 14 prev==want; k=857. Guard turn 1 explicitly. RevFamilySpec's turn>1-only rule gives n=1752 k=829 [0.4496,0.4969] FAIL and drops all 196 A-MONO/B/turn-1 rows.
3. D1 capture route, by baseline path: fence 1803 via fence; half-fenced 57 via fallback (the lone ``` pairs with the distractor opener, giving an unparseable prose block); no-fence 88 via fence.
4. The F1/F2 wording decides the only MP signal in this population. "The fence" (the extracted one) exposes the 31-row B multi-fence stratum. "All fences" makes both 100% invariant. Pre-register which one, and print the multi-fence stratum.
5. For this population's answer shapes (flat dicts/lists, ≤1 nesting; 0 deeper), F3–F7, G1 and G2 are decided by the code: grader.py:121-134 plus the exact-equality and validity graders, so a selftest can prove them. Only F1/F2 (multi-fence) and D1 depend on the stored responses. The knowledge entry should not present 10 interval verdicts as 10 empirical findings.
6. Ordering: the predictions P1–P10 were filed at e0037a8 (plans/round-26-claims.md:101-117), before this probe existed, so none of them is informed by it.
7. Not mine, observed read-only: the live lane tree shows ` M corpus/QUALITY.md` (+11 lines, mtime 03:51:05 -0300), `?? plans/state_check.cover`, and `plans/__pycache__/{attrib_calibration,state_check}.cpython-314.pyc` (03:50:58–03:51:15). All of these predate this probe, whose runs touched only the /tmp archive (`python3 -B`). Flagged for the integrator.

Files written: this report only (read-only seat). Scratch outside the lane: `/tmp/kengaku-r26-familyedges-probe/family_edges.py` sha256 be6ff7f1dbac89982f9b26964a18bdc29b23f25056dd2aa560e64d8c040201f8; `supplement.py` sha256 78ef59872ac125cfbb49cd2d9c0a0e639d919977f6229b34cb1e985945ef45a8.
VERDICT: All ten families are measurable on all 1964 records (0 excluded, with C-MONO routed to valid_latin). Under the recommended rules there are 9 PASS and D1 FAIL. The only response-dependent MP signal is the 31-row B multi-fence stratum, under the extracted-fence reading of F1/F2. D1's 0.48 rate is the FAIL base rate (0/1003 on PASS rows).
Installs: none.
