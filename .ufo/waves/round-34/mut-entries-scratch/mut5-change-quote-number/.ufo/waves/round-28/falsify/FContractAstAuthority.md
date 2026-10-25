# FContractAstAuthority — AST contract-anchor authority falsification (round28, author-side)

Seat: KengakuR28.FContractAstAuthority (critic, leaf; author-side, not outside non-author evidence).
Target: `plans/benchmark_spec_audit.py` sha256 `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8`
(`read_snapshot` contract_anchors at :198–204, `scorer_contract` at :163–179, CLI error mapping at :297–300).
Candidate re-read: frozen draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`; canonical candidate path
`corpus/knowledge/webarena-task-spec-audit.md` (not present / not admitted at review time).
Hand-expected file `plans/fixtures/r28/contract-expected.json` sha256 `9fdfd813…6d95`.
Pinned inputs re-hashed after all probes: manifest `c78b1478…a6dd` and all four file digests still MATCH.

Godspeed axes: groundedness (spans/names vs pinned bytes), provenance honesty (what is derived vs
asserted), effect-freedom (no upstream import/exec/network), harm-none (production read-only).

## Method (all writes under `.ufo/waves/round-28/scratch/FContractAstAuthority/`)

1. Byte-copied the fixture to `scratch/.../root`; ran the production instrument CLI against it:
   `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/benchmark_spec_audit.py --root <scratch>/root --json > cli.json` → exit0, 0 findings, 34 anchors.
2. Independent span census `derive_spans.py` using **tokenize only (no `ast`)** over the scratch copy → `tokenize-census.json`; comparison in `compare.txt`.
3. PEP 578 audit-hook run of the same CLI (`audit_hook_run.py` → `audit-hook.json`; hooked stdout byte-identical to `cli.json`).
4. Ten scratch-only text mutants of the pinned `evaluators.py` fed to the instrument's `scorer_contract()` (`mutants.py` → `mutants.json`).
5. One CLI probe on a consistently re-pinned scratch tree (`repin-root/`, scratch instrument copy differing only in `MANIFEST_SHA256`) → `repin.stderr`, `repin.exit`.
No upstream code imported/executed, no network, no selftest/full-suite rerun, no production writes, no tool installs/updates.

Evidence sha256: cli.json `bca99dfb…6d0d`, tokenize-census.json `36dfc793…41e`, compare.txt `7ba1fca1…aba`,
mutants.json `2e4826ca…ec14`, audit-hook.json `59903405…2d4d`, repin.stderr `b07b499d…4abd3`.

## Confirmed (supported)

- **Names and line spans exact.** Instrument anchors (34) == tokenize census (34) as sets of (file, name, line, end_line); `only_cli=∅`, `only_tok=∅`.
  Hand-checks: Evaluator 32–68, StringEvaluator 71–170, URLEvaluator 173–241, HTMLContentEvaluator 244–333, EvaluatorComb 336–352, evaluator_router 356–374, llm_fuzzy_match 146–173, llm_ua_match 176–208.
- **Candidate source-line citations all land on the claimed code** (read against pinned bytes): header spans 71–170/173–241/244–333/336–374, S063 146–208; table spans S062:80–94, 134, 98–111, 142–149, 150–169, 152–163, 159, 187–239, 199–235, 258–333, 271–301, 348–352, 361–374; S063:146–173, 176–208, 161–173, 196–208. Lesson quotes `score *= cur_score` (S062:351) and `if "partially correct" in response or "incorrect" in response:` (S063:169) are verbatim. contract-expected `product_lines [351]`, `na_override_lines [159]` hand-match.
- **No import/eval/exec/helper/network effect.** Audit hook: non-stdlib opens = only the 6 scratch fixture files + the instrument; 0 socket/subprocess/os.system/exec*/spawn/urllib/http/fs-mutation events; imports stdlib only (no evaluators/helper_functions/beartype/playwright/openai). Upstream sources are compiled only as AST (3 `compile` events with filename `<unknown>`: evaluators.py ×2, helper_functions.py ×1) and **never** appear in `exec` events; the 19 `<string>` compile/exec pairs are stdlib namedtuple/dataclass codegen (first bytes recorded). No `benchmark_spec_audit` pyc created.
- Inputs are pure ASCII, no CRLF/tabs, so the locale-default `read_text()` cannot change observed output on these pinned bytes (non-finding).

## Findings

### F1 (fixable defect, impacts provenance/calibration of the candidate text) — "AST-derived … distinct error phases" is false provenance

Counterexample: candidate draft line 112: “The AST-derived scorer-contract block records dispatch, ordered product, the N/A assignment override and distinct error phases”.
Only `dispatch`, `composition.source_lines` and `na_fallback.source_lines` are computed from the AST. `failure_phases` (all five entries), `composition.operation` (“ordered product; mutable page state means order matters”) and `na_fallback.operation` are **string literals** in `scorer_contract` (:179); `read_snapshot` never compares even the derived lines to `contract-expected.json` (only selftest does).
Observed (`python3 -B mutants.py <instrument> <scratch evaluators.py>`):

| mutant (scratch text only) | outcome |
|---|---|
| M1 delete router `case _: raise ValueError` (:371–372) | SURVIVED, contract identical — still says “router construction raises ValueError” |
| M2 unknown url_note → `score = 0.0` (:239) | SURVIVED, identical — still “evaluator call raises ValueError” |
| M3 unknown locator → empty text (:301) | SURVIVED, identical |
| M4 remove JS-locator `except Exception` (:292–294) | SURVIVED, only product line 351→350 |
| M5 wrap helper `eval(func)` in try/except (:299) | SURVIVED, only product line 351→354 — still “not absorbed” |
| M6 `score *= cur_score` → `score *= 1.0` | SURVIVED, identical |
| M7 EvaluatorComb loops `self.evaluators[:1]` | SURVIVED, identical (“ordered product” unchecked) |
| M8 N/A override made unconditional | SURVIVED, identical |
| M9 rename `evaluator_router` | REJECTED but via `StopIteration`, not `scorer_contract_unrecognized` (see F2) |
| M10 `*=` → `+=` (selftest's own mutant, control) | REJECTED `ValueError scorer_contract_unrecognized` |

Each hard-coded phase statement is **true for the pinned bytes** (I verified :239, :301, :330–332, :292–294, :266/:272/:299, :371–372 by reading), and the sha pin makes these mutants unreachable through the CLI — so this is not a correctness defect of the measured counters, it is an authority/provenance overstatement. The lesson (round-28.md:131, “AST-derived dispatch/product/N/A-override facts”) is accurate; the candidate extends “AST-derived” to the phases. RevRouterMix ME1 asked for phases “derived from the sha-pinned bytes”; the integration delivered hand-written annotations.
Smallest safe correction (candidate text only): “The scorer-contract block records AST-derived dispatch, the product-statement line and the N/A-override line; its ordered-product and error-phase statements are hand-read annotations of the pinned bytes, not AST-checked.” (Optional instrument alternative, not required: add hand-expected phase source lines to contract-expected.json and assert the router wildcard `Raise`, the :239/:301/:330 `Raise` nodes and the :292 handler exist.)

### F2 (latent, bounded instrument defect) — renamed/missing anchor crashes with exit1 instead of exit2

`scorer_contract` uses bare `next(...)` (:166, :174); `StopIteration` is not in main's caught tuple (:299). Command: `python3 -B repin-root/plans/benchmark_spec_audit.py --root <scratch>/repin-root --summary` on a consistently re-pinned tree with `evaluator_router` renamed → traceback ending `StopIteration` at :166, empty stdout, **exit 1**, which the claims contract reserves for “failed finding”; it should be exit2 could-not-evaluate. Unreachable with current pins (requires editing `MANIFEST_SHA256`), so it does not affect any delivered number.
Smallest repair: `next((...), None)` for router/comb and raise `ValueError("scorer_contract_unrecognized")` when `None`, which the existing handler maps to exit2 `input_invalid`.

### F3 (tradeoff, disclosure only) — anchor identity is (file, line), not (file, name)

`contract_anchors` come from `ast.walk` (BFS, not source order: `cli_order_is_source_order False`), carry no qualname/parent, so names are non-unique (`evaluators.py: __call__ ×5, __init__ ×2`; nested `clean_url/parse_url/parse_urls` appear unqualified), and `line` is the `def` line, excluding decorators for 12 definitions (e.g. `evaluator_router` decorator 355 vs anchor 356; `@beartype` on URLEvaluator/HTMLContentEvaluator/EvaluatorComb `__call__` at 176/247/340 sits outside their anchor spans). The candidate does not cite anchors by bare name, so no current claim is wrong; any consumer must key by line. Repair if wanted: emit `qualname` and `decorator_line` (or `start_line=min(decorator linenos)`), sorted by line. Also evaluators.py is read and parsed twice (:200 and :205) — redundant work, no correctness effect.

### Negligible / adjacent
- Candidate header “task0:18–28”: task0's `eval` object opens at line 18 and closes at 29; all quoted fields lie in 18–28. No action needed.
- Adjacent, outside AST scope: “applies exact_match before must_include” (draft line 35) reads as sequential; source :305–314 is exclusive `elif`. Population has 0 both-key targets (per RevRouterMix census), so no number changes; “instead of” would be exact.

## Impacted axes
calibration (provenance wording, F1); coverage/constructs unaffected — all counters, spans, names and effect-freedom claims held.

VERDICT: PARTIAL — anchors exact, pinned source read-only, no upstream import/exec/network effects confirmed; candidate line 112 overstates AST derivation of error phases/ordered product (F1, wording fix), plus latent exit-code defect F2.
