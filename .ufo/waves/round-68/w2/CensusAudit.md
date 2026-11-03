# CensusAudit — round 68 attempt 2, w2

Axes: coverage and calibration. Read-only registry review; no predicate, counter, target, case, kill rule, or lane source was edited. Findings are recommendations, not admissions.

## Findings (severity order)

### Medium — S240 was not marked mined

`corpus/SOURCES.md:255` has status **queued**, not the required **mined**. This is present in the committed attempt-1 bytes at `0e52fb5d`, not a working-tree race. All other requested S240 fields pass. Census success does not establish the claimed mined state: queued is a valid registry status. The round should disclose this mismatch rather than describe registration as fully mined; any correction belongs to the integration owner, not this leaf seat.

### Low — capability registration is narrative-only, not a capabilities-table row

`SCORECARD.md:551–568` (the canonical `## Capabilities` table) lacks `offline-network-service-grader-probe`; no exact named capability table row exists elsewhere in the file either. `SCORECARD.md:2946` DOES carry the capability, its explanation, first-working round 68, and the correct evidence command as a prose **Capabilities** paragraph. Thus the evidence is not missing, but the assignment's literal table-row requirement is unmet. This follows the recent prose-addendum style; it is a registry-placement gap, not evidence that the probe failed.

## Commands, exits, and counts

Lane root `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`; scratch `S=/fast/scratch/hyaku/kengaku-r68/CensusAudit`. Commands ran with absolute paths or cwd S.

- `git -C L rev-parse HEAD`: rc 0, `7803bdd4da5bda14713f23dae8278aef479b9c19`. The live tip has advanced beyond the assignment's attempt-1 tip. To avoid attributing later changes to attempt 1, all four audited files below were separately bound to `git show 0e52fb5d:<path>`.
- `git -C L diff d2ed4ca3 0e52fb5d -- corpus/SOURCES.md`: rc 0. The only changed source id is **S240** (one appended row). Existing rows dated 2026-11-03 belong to earlier rounds and are not counted as round-68 additions. No S241 registry row was added; the capture filename's candidate id does not alter S240's identity.
- `git -C L diff 0e52fb5d -- corpus/SOURCES.md`: rc 0, empty output.
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' L/corpus/SOURCES.md`: rc 0, **232**, expected 232.
- `grep -c 'executed 2 of 8' L/SKILL.md`: rc 0, **1**, expected 1; class row at line 78.
- `grep -c 'round67_c1_pipeline_probe' L/SKILL.md`: rc 0, **2**, expected 2; occurrences at lines 81 and 687.
- `SKILL.md:686` names `round65-c1-sqlite-probe` and includes `--strict`, its restriction to receipt-check mode, and its strict verdict description. Requested flag check passes.
- Independent Python `re`/line-count operations gave the same counts; row splitting on outer pipes gave **11 columns** for S240. These are literal data checks, not semantic caller proofs.

## Committed-byte binding and S240

Each `git -C L show 0e52fb5d:<path>` returned rc 0, empty stderr, and bytes equal to the corresponding working-tree file:

| path | SHA256 |
|---|---|
| `corpus/SOURCES.md` | `3ee8b38dee2b408402e59b915cd9f3ee4518e228f2f781925b6173a4141f4794` |
| `SKILL.md` | `3fe9a6d0efa60d0f26ff488f99ed73b400b4faa2d6c9318da801141acb8ed979` |
| `SCORECARD.md` | `d5bbce477e0924d49028d97f273b0c1386e7754b822d02b7796646d1a6315ef0` |
| `.ufo/waves/round-68/w1/recon/S241-urllib3-2.7.0-connection.py` | `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532` |

S240 checks:

| field | observed | result |
|---|---|---|
| columns | 11 | matches |
| tier | A | matches |
| status | queued | mismatch: expected mined |
| opened | 2026-11-03 | matches |
| recheck | 180d | matches |
| used-by | corpus/knowledge/tb2-network-service-offline-grader.md | existing regular file resolving within corpus/knowledge/ |
| capture | .ufo/waves/round-68/w1/recon/S241-urllib3-2.7.0-connection.py | committed capture exists; own fetch unnecessary |
| capture bytes | 42786 | matches row |
| capture SHA256 | 668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532 | matches row and committed bytes |

Committed anchors match the row:

```python
# line 82
class HTTPConnection(_HTTPConnection):
# lines 163–164
    def __str__(self) -> str:
        return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"
```

The S240 attribution is read under Amendment A1: urllib3 2.7.0, not the original frozen CPython repr attribution. The companion `recon/S241-receipt.md:24–40` records the matching capture and located quote. This review establishes the requested renderer anchor, not the uncaptured `exceptions.py:148` subsidiary anchor or a new live pip replay.

The correct evidence command is present in `SCORECARD.md:2946`:

```sh
python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt
```

## Census receipt

Exact command (executed through Python subprocess with separate stdout/stderr capture):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

**rc=0**, **W warnings=24**, all W04; **E findings=0**. This matches the frozen before-census warning count. Full stdout:

```text
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	W04	S213 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py across scopes
kengaku	W04	S214 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py across scopes
kengaku	W04	S215 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh across scopes
kengaku	W04	S216 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md across scopes
kengaku	W04	S217 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/gen.py across scopes
kengaku	W04	S222 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/instruction.md across scopes
kengaku	W04	S227 duplicate url encoding.spec.whatwg.org/index-windows-1252.txt across scopes
kengaku	W04	S234 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	W04	S237 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

Full stderr: empty (0 bytes).

## Assimilation state

Still open on the recorded surface: the question remains without a disposition on either matching line, and the correction explicitly says adopt nothing. No L0 bytes edited. Exact current lines of `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`:

213: kengaku | round-54 | assimilation mass id drift: the merge/kengaku package (175 staged rows, first staged id S077, built when the lane registry held 76 rows) collides with the lane registry's now-197-row S-space (reg-vs-staged collisions recorded in .ufo/waves/round-54/assimilation/ this round). The read-only renumber fix is a ~120-row id map with per-document citation re-pointing — beyond a one-round fix (CORPUS.md rule 2 append-only). Adopt nothing this round; please rule whether the package should be re-staged against the current registry or retired.

214: kengaku | round-54 | correction to preceding assimilation question: measured registry rows=190 (highest id S197), staged rows=175, collisions=114 (E5CensusGate receipts). The earlier 197-row phrase confused highest id with row count; adopt nothing, no renumber map applied.

## Residual risk and verification gaps

- `xd://lsp` is not mounted (`No such tool`), so no LSP server status, references, definitions, or diagnostics were available. This Markdown registry review used literal searches, structured field checks, and committed-byte comparisons; none is presented as semantic caller proof.
- Both frozen claims and Amendment A2 were read. This seat does not re-run C1/C2 batteries, report-contract mutation tests, or resume-continuity logic; those are other seats' work, not inferred from this census. No admission or saturation verdict is emitted.
- No fresh network fetch was necessary because the requested capture is committed and byte-bound. Historical live-fetch provenance is not independently re-proven here.
- No tools installed/updated; no listeners, clones, fixture repositories, git writes, or subagent dispatch. Only this report was written in the lane. Scratch was deleted before terminal handoff.

## Self-evaluation

Accuracy 4/5: committed blobs and raw census retained; historical live execution not independently established. Completeness 4/5: all six seat items covered; capability-table placement remains a reported mismatch rather than an unauthorized fix. Clarity 4/5: full stdout makes the report longer but preserves the requested receipt. Actionability 4/5: exact two locations and scope-safe recommendations supplied; integration decisions remain with the owner. Conciseness 4/5: repeated pins retained for reproducibility. Overall 4.0/5. Highest-impact improvement is to reconcile the queued status and literal table placement in the authorized integration path. Self-check: the evidence supports this bounded assessment.
