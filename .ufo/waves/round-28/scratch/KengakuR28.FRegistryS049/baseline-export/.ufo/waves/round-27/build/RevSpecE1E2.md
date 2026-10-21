# RevSpecE1E2 — review of E1 first-fence and E2 bare-last (round 27)

Scope: plans/round-27-claims.md:37-47 vs grader.py:121-134 and plans/grader_perturb.py:35-36,187,259-276. Read-only.
Replay: inline Python in the eval kernel (PYTHONDONTWRITEBYTECODE=1) calling build_population → 1964 records, 0 excluded, 0 errors (sha256 pins match); exit 0. Nothing written to the lane or /tmp. Installs: none (stdlib only).
Checks: fence and BARE patterns byte-identical in grader.py and grader_perturb.py; E0 replica = stored verdict on 1964/1964. Formats: FJ1 1296, FJM 492, MULTI 31, DANGLE 57, BARE 88; fence counts 0/1/3 = 145/1788/31 (no 2-fence records).

## E1 (first fence)

A1 Fallback when the first fence fails: later fences, or straight to bare-last?
  T1 `'```json\n{"answer": "A",\n```\nRevised:\n```json\n{"answer": "B"}\n```\nSee [1].'`
     R1 stop at first fence → [1]; R2 first parseable fence → {"answer": "B"}; E0 → {"answer": "B"}.
  T8 `'```json\n{"answer": \n```\n```json\n"B"\n```'` → R1 None; R2 'B'; E0 'B' (scalar fence is invisible to bare candidates).
  Text supports R1: "first fenced block instead of the last" (:38) swaps E0's single selector; E3 says "first parseable" (:40), E1 does not.
  Population: 0 records with a failing first fence. Inert on counts; pin anyway.

A2 Fallback scope: whole response, or text outside the first fence?
  T2 `'```json\n{"answer": "A", "x": {"k": 1},\n```'` → whole response {"k": 1}; outside first fence None.
  Text supports whole response: "the same bare-last fallback" is E0's fallback over `text` (grader.py:128). Population: 0.

A3 "If it parses": json.loads success (incl. null), or non-null only?
  T3 `'```json\nnull\n```\nFinal: {"answer": "B"}'` → success: None, no fallback; non-null: {"answer": "B"}.
  Text supports success: E0 returns json.loads(blocks[-1]) directly (grader.py:125). Population: 0 fences parse to null or scalars.

A4 What is a "fenced block": E0's json-only regex, or any-label first fence?
  T4 `'```python\n{"answer": "A"}\n```\n```json\n{"answer": "B"}\n```'` → E0 regex fences [''] → {"answer": "B"}; any-label first fence → {"answer": "A"}.
  Text supports the E0 regex: E6 is a separate "any language label" row (:43), redundant otherwise. Population: 0 non-json labels.

## E2 (bare-last)

A5 "Ignore fences": raw as-is, delimiters stripped, or fenced spans excluded?
  T6 `'{"answer": "B",\n```json\n"x": 1}\n```'` → as-is None; stripped {"answer": "B", "x": 1}; excluded None.
  Text supports as-is: "fence-agnostic" (:39); E0's fallback scans raw. Population: stripped 0 disagreements; excluded 995.

A6 Overlapping candidates: non-overlapping findall, or every-start enumeration?
  round8-horizon/results.jsonl:253 (C-conflict): '```json\n{"violations": [3], "square": [["A", "B", "C", "D"], ["B", "C", "D", "A"], ["C", "D", "A", "B"], ["D", "A", "B", "C"]]}\n```'
  findall → whole object (= stored PASS); enumeration → ["D","A","B","C"] (FAIL).
  Text supports findall: "candidate"/"match" are findall elements; E2 is E0's fallback (grader.py:128-129). Population: findall 0; enumeration 13 (all C-cells).

A7 A candidate straddling a fence marker hides an inner object.
  T5 `'Result: {"outer": "x", "note": ```json\n{"answer": "B"}\n```}'` → findall None; enumeration {"answer": "B"}; E0 {"answer": "B"}; stripped {"outer": "x", "note": {"answer": "B"}}.
  Text supports findall (as A6). Population: 0 straddling candidates; inert.

A8 Not ambiguous, flagged for the oracle: arrays are candidates (BARE_RE's `\[` branch, grader.py:128).
  T7 `'{"answer": "B"}\nSee [1].'` → E2 [1]. Population: E2 = E0 verdict on all 1964.

## Replay (population)
- E1 under R1, R2, scope, non-null: identical. flip_pf 17, flip_fp 0, none 0; all 17 in MULTI (31). Example round8-horizon/results.jsonl:223: first fence is an intermediate state; stored PASS rests on the last fence.
- E2 findall 0 disagreements; enumeration 13; stripped 0; excluded 995 (none 1819 vs E0 0).
- Q1 (E1 ≥1): 17 under every E1 reading, so reading-independent. Q3 (E2 ≤1%): holds under findall (0) and enumeration (13); fails only under exclusion (995).

## Recommendation
Amend (appended `## Amendment N`): E1 = first match of E0's json-only regex; if json.loads raises, bare-last over the whole response; json.loads success is final (incl. null); later fences are never consulted. E2 = re.findall(BARE_RE, raw) on raw as-is; last element json.loads accepts; no overlap enumeration; arrays included. Freeze T1–T8 with per-reading expected values under plans/fixtures/r27/. No /tmp/kengaku-r27-* clone holds plans/parser_policy_compare.py yet (glob: no match), so amend before implementation.
Files written: this report only.

VERDICT: E1 and E2 carry 8 textual ambiguities; the text supports R1 (single first fence, whole-response bare-last) and as-is findall for E2, and only the E2 enumeration (13) and exclusion (995) readings move counts; amend to pin all before any writer implements.
