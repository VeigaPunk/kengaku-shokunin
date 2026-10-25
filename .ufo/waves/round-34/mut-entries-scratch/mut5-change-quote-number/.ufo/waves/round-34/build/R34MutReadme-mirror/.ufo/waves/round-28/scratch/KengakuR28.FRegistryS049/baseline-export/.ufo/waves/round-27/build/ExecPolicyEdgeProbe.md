# ExecPolicyEdgeProbe — round 27 build (WRITER, features only)

Seat KengakuR27.ExecPolicyEdgeProbe. Scratch only: /tmp/kengaku-r27-ExecPolicyEdgeProbe (no clone). Lane read as-is; no git/jj run in the lane. Post-run `find -newer` over plans/, grader.py, corpus/evidence and a `*.pyc` scan (maxdepth 3) both empty, before and after the spot-check.

## Exact command (exit 0)
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-ExecPolicyEdgeProbe/exec_policy_features.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --out /tmp/kengaku-r27-ExecPolicyEdgeProbe/features.txt

Stdout provenance: `POP population=1964 candidates=1964 excluded=0 errors=0`; four `PIN ... match=True` (sha256 bd986e5e, c20158bd, 918bf7aa, ad9c88e7); `SRC ... =True` (fence and bare patterns verbatim in grader.py); `CHECK format_class_consistent_with_fences_lane=True`; `RESULT ok=True`.
Population: plans/grader_perturb.py:187 build_population, loaded with spec_from_file_location. Reference extractor: grader.extract_json_block (grader.py:121-134). stored_ok and want are never read.

## Histogram (1964 records; per-feature table with all columns in features.txt, 60 lines)
file x format_class     FJ1    FJM  MULTI  DANGLE   BARE
r8h (round8-horizon)    112     39     31      6      0
r9rep                    90     36      0      2      0
r11pow                  211     87      0     20      2
r12lad                  883    330      0     29     86
total                  1296    492     31     57     88

## Structural findings (counts; no verdicts)
F1 Fence bodies: 1819 fenced records; first_fence and last_fence are parses for 1819, fails 0, parses-null 0.
F2 Fence count per record (FENCE_RE, grader.py:122): 0 → 145, 1 → 1788, 3 → 31 (all MULTI). No 2-fence or 4+-fence record.
F3 Exact fence info strings (text after the triple backtick, one trailing CR removed): 'json' in 1819 records, '' in 1876 (closers plus DANGLE). No other string occurs. CRLF present in 0 records.
F4 MULTI (31, all r8h B-* cells): first and last fence parse to different values in 31/31; first_bracket_is_answer=no in 31/31.
F5 Bare candidates (BARE_RE, grader.py:128) outside every fence: exactly one in each of the 145 unfenced records, all parse. Inside fences: one per single-fence record, three per MULTI.
F6 strip_parses=yes: 88, exactly the BARE stratum (r12 T-DENSE 48, T-SPARSE 36; A-CKPT710 2 in r11 and 2 in r12).
F7 extract_depth: 1 → 1948; 2 → 4 (FJM, C-MONO, r8h); 3 → 12 (FJ1, C-benign/C-conflict/C-norule, 4 each, r8h). none, 0 and 4+ → 0. answer_is_bare=yes 1964/1964.
F8 DANGLE (57): one bare JSON object followed by one stray triple-backtick line (cells A-* and T-DENSE). BARE (88): the whole raw output is the JSON object.
F9 Cross-checks: format classes sum to 1964; format_class agrees with fence count on 1964/1964; MULTI=31 matches the audit's "14/31 in MULTI" denominator (corpus/knowledge/grader-perturbation-audit.md:91).

## Prior refuted (kept visible)
Pre-probe expectation: BARE_RE's brace-only nesting would truncate depth-3 answers. False for this population. The depth-3 answers are dict→list→list (C-* square grids); BARE_RE's `[^{}]*` admits brackets, so the whole answer matches (answer_is_bare=yes). Recorded only; no policy consequence drawn here.

## Limits
- Features only: no PASS/FAIL and no agree/flip counts. Policy consequences belong to plans/parser_policy_compare.py.
- Zero counts (no CRLF, no failing fence, no third label, no 2-fence record) describe the frozen 1964, not future responses.
- first_vs_last* compares json.loads values, not grades.
- Extras beyond the requested list: ticks, tick_parity, first_fence, first_vs_last_fence, bare_inside(_parse), first_vs_last_bare, answer_is_bare, first_bracket_is_answer.

## Files written (scratch, sha256)
exec_policy_features.py 09163e4a24023fadf744f3fec5f619a308a01c55b8d7a12cea44a8be0c78d0b3
spotcheck.py 74526306eaa0c69901d588fa039301d4a9dea18ba8fc7ba22cd95c08f5fef3c1
features.txt 97df1ae49485031f69514d25c64a041ad9d95b3acc79c4f055a2562bca33b94d

Installs: none (python3 3.14.8 present; no pacman, uv, npm or binary download).
VERDICT: Census complete on the 1964 pinned records: single-fence 1788, pure-JSON 88, stray-closer 57, three-fence MULTI 31 (first≠last fence value in 31/31); no CRLF, no failing fence body, no third fence label.
