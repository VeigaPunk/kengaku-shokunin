# SrcInspectJson — inspect_ai extraction policies (round 27 build, C1 input)

Pin: UKGovernmentBEIS/inspect_ai @ 63e45cc52d39b873b944124613da21fdad6f6dcc (clone HEAD; commit 2026-10-21T07:24:54-04:00). Accessed 2026-10-21 by `git clone --depth 1` to /tmp/kengaku-r27-SrcInspectJson/inspect_ai. Permalinks: https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/<path>#Lx-Ly

## 1. Policy inventory (paths relative to src/inspect_ai unless noted)
| helper | policy on raw completion | first/last/any | fence-aware |
|---|---|---|---|
| match() scorer/_match.py:8-14; match_str scorer/_common.py:70-128 | no extraction: end=endswith (default, :123-124), begin=startswith (:121-122), any=`t in v` (:127-128), exact (:125-126); strip + punctuation trim (:116-118); numeric begin/end = first/last number (:99-103) | positional | no |
| includes() scorer/_match.py:45-60 | `target in value` after casefold | any substring | no |
| pattern() scorer/_pattern.py:57-126 | `re.search` (:77-79) = leftmost match; groups via match_first (any group, default) or match_all (:21-53) | FIRST | no |
| answer() scorer/_answer.py:35-62; _util/pattern.py:5-9 | LETTER/WORD carry `(?!.*ANSWER\s*:)` = last `ANSWER:` only, no fallback; LINE `\Z`-anchored = answer on final line | LAST-or-nothing | no |
| choice() scorer/_choice.py:60-136 | no text parse; reads `choice.correct` set by the solver | n/a | n/a |
| parse_answers solver/_multiple_choice.py:82-165 (call :352) | strip $..$, **..**, (X) (:94-104); tier 1 line-anchored `^ANSWER\s*:` findall (:111-115); tier 2 unanchored only if tier 1 empty (:119-123); `matches[-1]` (:128); must be exactly one allowed letter (:157-163) | LAST within strict tier; no fallback | no |
| model-graded grade regex scorer/_model.py:432-434, 458-460, 277-281, 314-315 | leading greedy `.*` + DOTALL binds to last `GRADE: X`; unparseable verdict = unscored `grader_failed` (:347-352) | LAST | no |
| math() scorer/_math.py:326-360 candidates; _parse_first :1006-1017; fallback :1020-1045 used :1227-1234 | priority list: last \boxed{} (:243-259), last answer/result marker suffix (:336-341), delimited/last-$ math (:277-294), whole text, last nonempty line (:351-353), last number (:355-358). Primary = first parseable; fallback (only if primary is opaque and wrong) = first expression candidate equal to a target | priority-FIRST + candidate fallback | no (``` survives as text candidate) |
| json_extract model/_providers/util/hf_handler.py:155-163 | `re.findall(r"```json\s*(\{.*?\})\s*```", DOTALL)`: label `json` required, OBJECT only, closing fence must follow `}`; dispatched :189-191 and :133-135 | ALL, in order; no bare fallback | YES (only fenced-text parser in src/) |
| raw_decode model/_call_tools.py:1720-1746 | `JSONDecoder().raw_decode` at index 0 only (:1739); trailing text must be quotes/whitespace | start only | no (tool-call args) |
| exact() / f1() scorer/_classification.py:48-69; _normalize :164 | whole completion normalized, then exact equality; f1 extracts only via caller `answer_fn` | positional | no |

## 2. Offline probe (executed; scratch only)
- Install: `uv venv --python /usr/bin/python3`, then `uv pip install --python venv/bin/python <clone>` with SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0.dev0+r27probe → inspect-ai 0.0.0.dev0+r27probe on CPython 3.14.8. Source fidelity: `diff -rq` installed vs clone src/inspect_ai shows no content differences (only non-packaged resources differ).
- Run: `PYTHONDONTWRITEBYTECODE=1 venv/bin/python /tmp/kengaku-r27-SrcInspectJson/probe_inspect.py` → `SUMMARY checked=27 ok=27 diff=0`, exit 0. Expectations were written from source reading before the run.
- pattern(r"ANSWER:\s*([A-D])") on "ANSWER: A … ANSWER: C" extracts A (first) → target C scores I; with a `(?s).*` prefix it extracts C.
- answer("letter") on "ANSWER: A … ANSWER: 2" → (I, None, invalid_response_format): no fallback to A.
- parse_answers "ANSWER: A … thus ANSWER: C" → {A} (strict tier dominates); "I think ANSWER: C is right" → set() (lenient capture "C IS RIGHT"); fenced "ANSWER: B" → {B}.
- match(location="end") target "42" on "The answer is 142" → C (no word boundary); numeric=True → I.
- DEFAULT_GRADE_PATTERN on "GRADE: I … GRADE: C" → C; on "GRADE: I … my downgrade: C" → I (word-bounded).
- json_extract: nested fenced json object intact; unlabelled fence → []; fenced array → []; trailing text inside fence → []; two fences → both, in order.
- _answer_candidates("…final answer is $\boxed{5}$.\nResult: 7") → ['5', '7', …]: boxed precedes marker; fenced text stays a candidate.

## 3. Mapping to frozen E0–E8 (INFERENCE: no inspect policy equals a frozen Ei; the frozen table is JSON-only)
- pattern() first match ≈ E3 bare-first (not parse-gated; user-chosen regex).
- json_extract ≈ E5 fence-only, but differs: label `json` required, object-only, all matches, no last selection.
- DEFAULT_GRADE_PATTERN and answer() last marker ≈ E2/E8 last-match on text markers; answer() has no fallback.
- match(location="exact") and exact() ≈ E4 strict-whole, on text not JSON.
- No analogue for E1 (first fence), E6 (any-label fence), E7/E8 (decode scan): raw_decode is used only at index 0.

## 4. Negative findings (grep at 63e45cc)
- Fence literal ``` appears in 33 .py files under src/inspect_ai (both pages reviewed); the only one that parses fenced text is hf_handler.py. Others are docstrings, renderers, or emitters (e.g. model/_providers/hf.py:484 writes a fence).
- json.loads/raw_decode sweep over scorer/, solver/, model/, _util/, util/ (34 hits, both pages): all protocol, config, file, or CLI decoders; none extracts JSON from free-text completions except json_extract.
- Sensitivity/agreement wording (answer extraction | extraction polic | first match | last match | sensitiv… to extract | agreement between) in docs/, scorer/, solver/: hits only docs/scoring-policy.qmd:57 and unrelated docs/metrics.qmd:105 ("first matching score").

## 5. Quotes (access 2026-10-21; ≤25 words; permalinks at 63e45cc)
- src/inspect_ai/_util/pattern.py#L1-L4: "Each pattern matches the LAST `ANSWER:` occurrence in the output"
- src/inspect_ai/solver/_multiple_choice.py#L109-L110: "so if there are multiple matching lines we take the last one."
- src/inspect_ai/scorer/_model.py#L437-L438: "The leading greedy ``.*`` (with DOTALL) ensures ``re.search`` binds to the *last* ``GRADE: X``"
- src/inspect_ai/scorer/_math.py#L244-L245: "keep only the most recent \boxed{...}."
- docs/scoring-policy.qmd#L57: "Use extraction rules that match the answer format requested in the task."
- docs/_builtin-scorers.md#L12: "Uses the captured values when capture groups are present, or the full match otherwise."

## 6. Limits
- math() and choice() not run end-to-end (latex2sympy2-extended==1.11.0 absent; only _answer_candidates run). Model grader run as regex only. includes(), exact(), f1() source-read only.
- One commit (63e45cc); no PyPI-release comparison; docs website and inspect_evals not opened.

## 7. Files and installs
- Wrote only this report. Scratch: /tmp/kengaku-r27-SrcInspectJson/{inspect_ai (clone), venv, probe_inspect.py}. No lane tree, git/jj state, fleet, or host files touched.
- Installed into the /tmp venv only: inspect-ai 0.0.0.dev0+r27probe built from the pinned clone plus its uv-resolved PyPI dependencies. Channel: uv pip (PyPI). Reason: run real scorer code for the probe. uv 0.13.0 was pre-existing (~/.local/bin/uv); no pacman, no sudo.

VERDICT: inspect_ai has at least seven distinct extraction rules, only json_extract is fence-aware, no in-repo measurement compares verdicts across policies, and the frozen E0–E8 table is only partly mirrored (E1/E6/E7 have no analogue).
