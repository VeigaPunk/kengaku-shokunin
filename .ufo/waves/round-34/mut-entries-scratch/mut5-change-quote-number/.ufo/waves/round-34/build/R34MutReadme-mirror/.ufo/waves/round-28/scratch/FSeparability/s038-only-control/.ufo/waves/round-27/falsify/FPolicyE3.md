# FPolicyE3 — frozen E3 bare-first review

Scope: `plans/parser_policy_compare.py` E3 vs the frozen E3 definition and Amendment1 only. Scratch clone HEAD observed as `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; pre-registration names response population base `b5719440e5eee46c1886fddbdf7bdc1624829454` (`plans/round-27-claims.md:3-4`).

## Result

No actionable E3 defect found in the pinned instrument. The observed implementation is equivalent to the frozen E3 rule on all 1964 pinned records and the seven hand-derived off-population cases below. This is scoped equivalence, **not** general parser equivalence.

Frozen rule: E3 is the first parseable, fence-agnostic `BARE_RE` candidate (`plans/round-27-claims.md:33-48`); Amendment1 explicitly uses non-overlapping `re.findall(BARE_RE, raw)` on original text, including fence contents, without stripping or excluding fence spans (`plans/round-27-claims.md:162-166`). Instrument E3 iterates `gp.BARE_RE.findall(raw)` in order, returns the first `_loads` success, else `None` (`plans/parser_policy_compare.py:79-84`; `_loads` catches parse exceptions at `plans/parser_policy_compare.py:41-45`). Its regex matches both the grader literal (`grader.py:128`) and `grader_perturb.py:36`, confirmed by AST extraction and exact pattern-string equality. The independent implementation manually transcribed that regex and used the frozen findall/parse rule.

## Evidence

- Clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FPolicyE3 && git -C /tmp/kengaku-r27-FPolicyE3 switch -c r27-FPolicyE3 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FPolicyE3 rev-parse HEAD` → `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
- `cd /tmp/kengaku-r27-FPolicyE3 && PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE3 --summary; echo "EXIT=$?"` → E3 `n=1964 agree=1947 flip_pf=17 flip_fp=0 none=0 pass=1004`; `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`; exit 0.
- Independent value attack: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/r27-FPolicyE3-scratch/e3_attack.py` → all four population pins matched; `population=1964 excluded=0 candidates=1964`; `value_mismatches(mine vs pinned e3)=0 my_none=0 findall!=finditer_records=0`. Independent E3 grading: `agree=1947 flip_pf=17 flip_fp=0`, all 17 flips in `MULTI`. E3 values differed from E1 on 0 records, E2 on 31, E7 on 0. Thus equal finite-population E3/E7 values do not establish parser equivalence off-population.
- `cd /tmp/kengaku-r27-FPolicyE3 && PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FPolicyE3` → `POLICY E3 agree=1947 flip_pf=17 flip_fp=0 none=0`; exit 0. Oracle E3 follows its own `first_or_last_bare(..., first=True)` path (`plans/fixtures/r27/policy_oracle.py:45-52,98-99`).
- `cd /tmp/kengaku-r27-FPolicyE3 && PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE3 --selftest 2>&1 | tail -20; echo "SELFTEST_EXIT=${PIPESTATUS[0]}"` → E3 probes pass; reversed-order E3 mutant killed by `first-candidate-wins`; all 9 mutants killed, 58 cases pass, 0 failures; exit 0 (`plans/parser_policy_compare.py:373-376,447`; test result from command).

## Hand-derived off-population cases

All seven cases produced the stated value from both independent and instrument E3:

| Raw response | Derivation from frozen rule | E3 value |
|---|---|---|
| ```` ```json\n{"v":1}\n```\n{"v":2} ```` | First candidate is inside the fence; it parses before the later object. | `{"v":1}` |
| `{bad} {"ok":[1,2]} tail {"x":9}` | `{bad}` fails JSON parsing; continue to the next non-overlapping match. | `{"ok":[1,2]}` |
| `[] {"v":1}` | Empty-array match is parseable and returned even though it is falsey in Python. | `[]` |
| `{"a":{"b":{"c":1}}}` | E3's one-inner-level regex does not match from the outer `{`; first complete match is the middle object. | `{"b":{"c":1}}` |
| `{"outer":1, ```json\n"inner":2}\n``` then {"v":3}` | Fence-straddling first candidate fails JSON parsing; later complete object succeeds. | `{"v":3}` |
| `{"v":1}{"w":2}` | Adjacent matches are non-overlapping; first parseable match wins. | `{"v":1}` |
| `x [] y {"v":2}` | First candidate is the empty array. | `[]` |

The depth case is a concrete off-population distinction: on that same string instrument E7 returned the full outer object `{"a":{"b":{"c":1}}}`, while E3 returned `{"b":{"c":1}}` (command: `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import sys;sys.path.insert(0,"/tmp/kengaku-r27-FPolicyE3/plans");import parser_policy_compare as p;raw="{\"a\": {\"b\": {\"c\": 1}}}";print("E3",p.e3_bare_first(raw));print("E7",p.e7_decode_first(raw))'`).

## Verification gaps and disposition

`read xd://lsp` returned `No such tool: xd://lsp`; no LSP references/definition/diagnostics were available. No grep was used as semantic evidence. Only the assigned offline comparison, selftest, oracle, and scratch checks were run; no build/lint/formatter or installation. Installs: none.

VERDICT: Scoped PASS — E3 matches the frozen rule on the complete hash-pinned 1964-record population and seven hand-derived off-population cases; no surviving E3 instrument defect observed. Do not extend this to arbitrary parser equivalence or the other policies/P4/Q15.
