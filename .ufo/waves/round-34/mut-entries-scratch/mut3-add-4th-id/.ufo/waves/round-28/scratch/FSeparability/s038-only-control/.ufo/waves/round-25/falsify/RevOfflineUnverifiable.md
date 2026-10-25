ATTACKS: C2 `offline_unverifiable=3`

Finding (severity: none; no hidden mismatch found): In a pristine `git archive 8ea41f9ed` copy, `python3 plans/state_check.py --json` reports 236 assertions: match=232, mismatch=0, superseded=1, offline_unverifiable=3, out_of_population=11. The three are:
- `P2d.surface.Served local model.url` — PROVINCE.md:14.
- `P2d.surface.Model catalogs.url` — PROVINCE.md:17.
- `P2d.surface.Public literature.url` — PROVINCE.md:20.

The `.path` assertions alongside all three are MATCH: `/proc/1299/cmdline` is absent with ABSENT marked; the model-catalogs directory is absent with ABSENT marked; and `corpus/knowledge/eval-prior-art-calibration.md` exists. The local-model U is broad for listener status: read-only `ss -ltn 'sport = :34113'` returned only its header (no listener), agreeing with PROVINCE.md:156's recorded `no listener`; this finds no mismatch. The same PROVINCE map records the model-catalogs absence and public-literature citation basis at :161-163 and :115.

Interpretation: `offline_unverifiable=3` is a count of URL/endpoint rows left uncontacted, as specified in plans/round-25-claims.md:82-84 and implemented in plans/state_check.py:912-937. It does not mean every local fact in those rows is uncheckable: the local listener state and local path existence are offline-checkable. Their observed values match. Model API identity/response and remote catalog/literature reachability remain unverified without prohibited network requests; the checker does not validate URL contents in the literature document.

Residual risk / verification gaps: No HTTP/model/remote requests were made, so endpoint API behavior and external URL reachability remain unknown. LSP is unavailable (`read xd://lsp` returned “No such tool”); source findings rely on direct file/command evidence, not grep as semantic proof. No installs.

VERDICT: SURVIVES — the three IDs are the planned no-contact URL rows; no offline-checkable mismatch was found.