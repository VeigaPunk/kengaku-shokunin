# SrcLmEvalDocs — lm-evaluation-harness filters at current main (round-27 C1 prior art)

Seat: KengakuR27.SrcLmEvalDocs (read-only; report is the only file written). Axes touched: novelty (prior-art for C1 extraction policies).

## Commit pin
- Repo EleutherAI/lm-evaluation-harness, branch main HEAD at fetch: `d6de81643928d653435c431bae19945d41d32520` (parent `e54687eac08501af43f09cc84af40ea2fc3cad60`, commit date 2026-09-14T10:51:05Z, PGP-verified; https://api.github.com/repos/EleutherAI/lm-evaluation-harness/commits/main, accessed 2026-10-21).
- All files fetched from `https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/d6de81643928d653435c431bae19945d41d32520/...` and full tarball extracted to `/tmp/kengaku-r27-srclmeval/repo/` (curl exits 0; `majority_vote.py`/`whitespace.py` under filters/ returned 404 — not present at this commit; earlier sha256sum exited 1 only on a wrong glob).
- sha256: filters/__init__.py `b407c0dd4eb9fc9f9ae550a70122363d86aa7f9e32463f02d32e476694717c60`; extraction.py `eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0`; selection.py `5f8264dce91dd1282b84487d703e7e2bb11bef5fd6c93f91b4e51342a4fb76ab`; docs/task_guide.md `b16a131beac02ef7a2569494a7f45f13763fa60d459ef8343910f4d418e79cf9`.

## Registry + pipeline mechanics (path:line at pinned commit)
- `lm_eval/filters/__init__.py:11-20` — `build_filter_ensemble` builds `FilterEnsemble(name, filters=[partial(get_filter(func), **kwargs) ...])` from yaml `filter:` components.
- `lm_eval/api/filter.py:41-49` — `FilterEnsemble.apply` runs `for f in self.filters: resps = f().apply(resps, docs)` (sequential, order = yaml order), stores result in `inst.filtered_resps[name]`.
- `lm_eval/api/registry.py:541` `filter_registry: Registry[type[Filter]]`; `:650-670` `@register_filter`; `:675-695` `get_filter` (loads entry-point plugins once, line 690); `:699` `FILTER_REGISTRY = filter_registry` alias.

## Built-in registered filters at d6de816 (grep `@register_filter("...")` over repo/lm_eval)
custom (filters/custom.py:5), decontaminate (filters/decontamination.py:5), regex (filters/extraction.py:15), regex_pos (extraction.py:65), remove_whitespace (extraction.py:109), multi_choice_regex (extraction.py:122), take_first (filters/selection.py:12), take_first_k (selection.py:26), majority_vote (selection.py:43), lowercase/uppercase/map/format_span (filters/transformation.py:7/19/31/61); plus task-local `ACP_grammar_filter` registered at import in tasks/acpbench/gen_2shot*/acp_utils.py:1063.

## Extraction policies the harness makes available (answer to the ask)
- **regex** (`RegexFilter`, extraction.py:24-61): `re.findall` then `match[group_select]` (line 47-49); `group_select: int = 0` → first match, negative index → **last match**; no match → `fallback` string `"[invalid]"` (never None). Default pattern `r"#### (\-?[0-9\.\,]+)"`.
- **multi_choice_regex** (extraction.py:122-247): regex + fallback procedure parsing `(A)/(B)/...` letter labels; docstring line 147: "Selects the (group_select)th match from the findall result."
- **take_first** (selection.py:19-21): keeps only `r[0]` of each doc's repeated responses (repeats-level, not in-text first match).
- **majority_vote** (selection.py:50-59): `Counter(resp).most_common(1)[0][0]` per doc.
- **take_first_k** (selection.py:26-40): `r[:k]` with asserts on `repeats`.
- Notably absent: no fence-aware extractor, no JSON-parse/whole-output filter, no first-vs-last **fenced-block** policy; `regex` never yields None (fallback string). So lane policies E0/E1/E5/E6 (fence) and E4/E7/E8 (json.loads/raw_decode) have no harness built-in counterpart; harness's first/last-match axis = `group_select` only.
- Quote (docs/task_guide.md:79, URL https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/docs/task_guide.md, accessed 2026-10-21): "A full list of supported filter operations can be found in `lm_eval/filters/__init__.py`."

## Docs evidence (Filters section)
- `docs/task_guide.md:65` `## Filters`; :67-78 response/`resps` pipeline description; :83-85 "Multiple Filter Pipelines" — located quote (task_guide.md:85, same URL, accessed 2026-10-21): "run multiple, distinct, filter pipelines on *the same model outputs* generated in one run on a task" (clause of the sentence at :85).
- Worked pipelines in task_guide.md: `exact_match` = regex→take_first (:92-99), `maj@64` = regex→majority_vote→take_first (:100-105), `maj@8` = take_first_k(k=8)→regex→majority_vote→take_first (:106-113); custom filter registration via `register_filter` decorator (:166-169).
- `docs/new_task_guide.md` has **no** Filters section at this commit; its only filter mention (:318) points to `docs/task_guide.md` and the plugin guide for shipping custom filters.

## C1 relevance (novelty axis, observation only — no verdict claimed here)
- Pre-registered prior art (`plans/round-27-claims.md`, C1 prior-art list) says harness `regex` filter `group_select` implements first/last-match policies: **confirmed** at extraction.py:27,47-49 (group_select indexes findall; 0=first, -1=last).
- Majority-vote / take-first selection policies: confirmed at selection.py:12-59. Fence-aware and JSON-decode extraction policies are **not** among the 14 built-ins — lane E0/E5/E6/E7/E8 remain outside this harness's published surface, while E1/E2/E3-style first/last matching is covered in kind via `group_select`. [INFERENCE for the critic: consistent with pre-registration's "construct is published in kind → novelty held at 7"; no +1 support found here.]

## Installs
None (used existing curl/tar/sha256sum; scratch only in /tmp/kengaku-r27-srclmeval; no lane-tree or clone writes by this seat).

VERDICT: harness filters at d6de816 make available regex(group_select first/last), multi_choice_regex, take_first, take_first_k, majority_vote (+8 transform/aux filters); no fence/JSON policies; docs/task_guide.md:65-169 is the Filters spec.
