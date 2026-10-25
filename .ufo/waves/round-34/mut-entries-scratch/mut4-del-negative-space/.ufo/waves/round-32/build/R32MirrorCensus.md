# R32 Mirror Census

Mirror: `/tmp/r32-R32MirrorCensus/`; copied lane `corpus/`, appended staged S094 and S097 rows, and placed `corpus/knowledge/benchmark-grader-semantics.md` at its repo-relative path. The entry's `verified-at` and its recheck-run date were updated to 2026-10-25 for the round-32 mirror. No lane production files were modified.

Command:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r32-R32MirrorCensus/corpus/SOURCES.md`

Pasted output (exit code 0):
```text
EXIT_CODE=0
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/tmp/r32-R32MirrorCensus/corpus/SOURCES.md
```

No E03 or E04 findings. Census returned 0; only W04 warnings were present.

VERDICT: census-ok