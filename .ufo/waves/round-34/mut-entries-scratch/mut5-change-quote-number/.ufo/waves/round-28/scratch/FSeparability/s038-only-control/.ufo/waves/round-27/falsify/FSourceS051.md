# Q10 — S051 source reread

Identity: `FSourceS051` is an independent reread identity, not candidate writer `KengakuR27`.

## Frozen tree and paths

Observed clone command (exit 0): `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FSourceS051 && git -C /tmp/kengaku-r27-FSourceS051 switch -c r27-FSourceS051 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FSourceS051 rev-parse HEAD`; output ended `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

Reviewed the whole draft at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (110 lines). The exact proposed canonical candidate path is `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/extraction-policy-comparison.md`; it is absent at this frozen tree (`glob`: `Path not found`). S051 occurs in draft lines 1 and 20–21; grep found no other candidate occurrences. Draft lines 20–21 say JsonMatch “parses the whole completion” and E4 is that policy class “with a disclosed `strip()` difference.”

## Direct source, anchor, quote, and mapping

- `corpus/SOURCES.md:73` S051 URL opened directly: `https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py`.
- Opened the URL's raw `main` file and the pinned source `https://raw.githubusercontent.com/openai/evals/4b7a66bd45f06156656e021e170e7574f6cde3f5/evals/elsuite/basic/json_match.py`. Both show `sampled = result.get_completions()[0]` (source line 76), then `sampled_json = json.loads(sampled)` at line 80; the `ValueError` handler sets `sampled_json = None` at line 83. The line-82 comment is exactly: “If the sampled string is not valid JSON, it will never match”. `json_match` returns false for a `None` sampled value (source function lines 10–12 in the fetched file). No strip, fence removal, substring extraction, or fallback occurs in this path.
- GitHub API query `https://api.github.com/repos/openai/evals/commits?path=evals%2Felsuite%2Fbasic%2Fjson_match.py&per_page=10` returned newest/last file-path commit `4b7a66bd45f06156656e021e170e7574f6cde3f5` (2023-10-27), matching the full commit in `corpus/evidence/round27-sources/gate.md:10` and the short commit in `corpus/SOURCES.md:73`. The pinned raw source was opened at that commit.
- `corpus/lessons/round-27.md:42` gives the same quote, anchor `eval_sample :82`, and short last-change commit. `corpus/evidence/round27-sources/gate.md:10` gives the same quote and source location `JsonMatch.eval_sample :80–82`, with full commit. The quote is exact and 12 words (≤25). The surrounding code anchor at lines 80–83 supports the accompanying decode-failure behavior.
- Policy scope: S051 is a strict whole-completion JSON parsing precedent, **not** an ordering precedent like S049/S050/S055 and **not** a faithful E4 port: source uses `json.loads(raw)` without `.strip()`, while lane E4 uses `json.loads(raw.strip())`. Thus it grounds the whole-output policy class only, not exact E4 semantics or any E0–E3/E5–E8 parser. Draft lines 20–21 disclose the deviation accurately; source does not establish which parser is preferable.

## Limits

Semantic LSP tracing was unavailable: `read xd://lsp` returned `No such tool` (no LSP device mounted). References above are direct source and targeted text observations, not LSP semantic proof. The recorded source SHA-256 `6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e` is present in the gate and `build/RowOpenAIEvalsJson.md`; this reread did not independently recompute it. No install or verification run was performed.

VERDICT: PASS — S051 source and <=25-word quote are correctly anchored and support only the disclosed strict-whole policy class; the canonical entry is still absent, so this verdict applies to its frozen draft, not an admitted corpus entry.