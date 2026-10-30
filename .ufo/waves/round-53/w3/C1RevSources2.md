# C1RevSources2 — independent source review

## Recommendation and findings (severity order)

**No unresolved actionable source-row finding in the reviewed revisions. Recommendation only, not source or round admission.** Axes: coverage and calibration. Reviewed all **46 scribe rows plus 15 literature candidates (61 total)**; independently opened every URL or the explicitly declared archive fallback and located **61/61 quoted fragments**. No fabrication established. Original source claims were not independently replicated.

### Medium — calibration defects landed, then corrected by authors

- `C1ScribeSources2A/rows.md` T01–T03 originally equated a presence assertion with failing the oracle definition and ordered presence-only suites above an assertion-free empirical floor. Source definitions do not entail those statements. Final T01–T03 distinguish task-relative adequacy and general assertion/coverage findings. T05/T10 were likewise narrowed.
- `C1ScribeSources2B/rows.md` U05/U06 originally treated exported-symbol existence and the aggregate “existence, executability, prediction correctness” contract as literal path-only grading; U20 blurred participant-controlled interpreter output with path presence. Live blog and issue/PR bodies show different mechanisms. Final U05/U06/U20 explicitly distinguish them. U02's unsupported global “earliest” priority claim was removed. **Only U15 in group B now makes a literal presence-only claim.** It quotes a named dependency-file test and says the file is never opened; it remains a TB2.1 reporter account, not proof about the frozen TB2.0 grader bytes.
- `C1ScoutLitSrc/lit.json` L01/L03/L08/L10/L12/L14 originally conflated script versus graded artefact, isolation versus oracle strength, task versus assertion granularity, and extraction versus correctness. Final teaches fields now make these distinctions. L02's lint limitation is grounded in enumerated checks rather than assumed absence.

### Low — exactness/shape defects landed, then corrected

- Historical Audit S905 quoted an ASCII apostrophe absent from live BetterBench. Final T13 uses the actual typographic apostrophe. Historical Audit S907 lacked a quote; final T15 supplies its title.
- A T07/T18 raw HTML lines were mislabeled as rendered-text lines. Final anchors state raw 78/rendered 70 and raw 87/rendered 85, independently reproduced.
- Literature L04's original quote contained two literal table separators. Final quote is a pipe-free definition sentence. Final projected cells contain no internal separators.
- B U13/U15 quote word counts disagreed between row and gate; authors corrected them to 4/14. All stay below 25 words.

Evidence: preserved reviewed rows/gates, independent fetch manifests and per-row checks beside this report. Reviewer did not edit sibling artifacts; authors revised their own drafts after direct messages.

## Per-row table

`y*` means canonical host unavailable, but this reviewer opened the row's declared Wayback copy successfully and located the quote there. Quote comparison preserves wording/punctuation; PDF extraction normalizes whitespace only. All tiers are scoped, community never A, tracker/PR tiers at most B. Final 46 scribe rows have 11 cells, valid dates/status/recheck, and `used-by` = em dash. Literature is a candidate JSON, not an already-complete registry row.

| row | opened ok | quote found | tier ok | defect / qualification |
|---|---|---|---|---|
| T01 | y | y | y | teaching corrected |
| T02 | y | y | y | teaching corrected |
| T03 | y* | y | y | teaching corrected; declared archive fallback |
| T04 | y | y | y | none found |
| T05 | y | y | y | none found |
| T06 | y | y | y | none found |
| T07 | y* | y | y | anchor label corrected; archive fallback |
| T08 | y | y | y | none found |
| T09 | y | y | y | none found |
| T10 | y | y | y | none found |
| T11 | y | y | y | none found |
| T12 | y | y | y | none found |
| T13 | y | y | y | apostrophe corrected |
| T14 | y | y | y | none found |
| T15 | y | y | y | rejected duplicate work; quote now supplied |
| T16 | y | y | y | none found |
| T17 | y | y | y | none found |
| T18 | y* | y | y | anchor label corrected; archive fallback |
| U01 | y | y | y | none found |
| U02 | y | y | y | unsupported priority removed |
| U03 | y | y | y | none found |
| U04 | y | y | y | none found |
| U05 | y | y | y | symbol/interface existence, not path-only; corrected |
| U06 | y | y | y | aggregate contract mismatch, not demonstrated P1; corrected |
| U07 | y | y | y | none found |
| U08 | y | y | y | none found |
| U09 | y | y | y | none found |
| U10 | y | y | y | none found |
| U11 | y | y | y | none found |
| U12 | y | y | y | none found |
| U13 | y | y | y | none found |
| U14 | y | y | y | none found |
| U15 | y | y | y | TB2.1 reporter account; named file-existence test |
| U16 | y | y | y | none found |
| U17 | y | y | y | none found |
| U18 | y | y | y | none found |
| U19 | y | y | y | open/unmerged mutable PR, B |
| U20 | y | y | y | writable interpreter route; corrected; open mutable PR |
| U21 | y | y | y | none found |
| U22 | y | y | y | none found |
| U23 | y | y | y | none found |
| U24 | y | y | y | none found |
| U25 | y | y | y | rejected open mutable PR, C |
| U26 | y | y | y | rejected open mutable PR, C |
| U27 | y | y | y | rejected open mutable PR; quote also found in diff |
| U28 | y | y | y | none found |
| L01 | y | y | y | none found |
| L02 | y | y | y | revised quote and enumerated lint scope |
| L03 | y | y | y | optional mode, not universal isolation; corrected |
| L04 | y | y | y | literal separators removed from quote |
| L05 | y | y | y | none found |
| L06 | y | y | y | none found |
| L07 | y | y | y | none found |
| L08 | y | y | y | task-level, not per-test standard; corrected |
| L09 | y | y | y | none found |
| L10 | y | y | y | task-relative adequacy clarified |
| L11 | y | y | y | none found |
| L12 | y | y | y | suite-level evidence, not literal P1; corrected |
| L13 | y | y | y | none found |
| L14 | y | y | y | extraction versus correctness clarified |
| L15 | y | y | y | none found |

## Required census

Clean shared clone asserted its top-level path before any other clone command and ran at clone-time current HEAD **9ead4476bf55b1ea6490d0204b668195db4a4d1d**. Existing registry: 186 rows. Scratch assembly adds T01–T18, U01–U28 and L01–L15, renumbered **S194–S254**: **247 rows**. Literature-only missing integration fields were explicitly projected as `queued`, `90d`, em-dash used-by **for shape checking only**; those are not proposed source facts or author-supplied decisions. `census-id-map.json` maps every draft to its scratch id.

Exact command:
```sh
TMPDIR=/fast/scratch/hyaku/kengaku-r53/C1RevSources2 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane/corpus/SOURCES-review.md
```

Output and exit code:
```text
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
file	ok	/fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane/corpus/SOURCES-review.md
EXIT_CODE=0
```

**No introduced W04 or E finding; 15 pre-existing W04 warnings only; exit 0.** The census is syntactic/registry evidence, not semantic proof of teaching or quote truth.

## Residual risk and verification gaps

- Moving `main` branches, open PRs and unversioned docs can change after access. Access date + fetch digest identifies observed bytes; open PR rows explicitly say mutable. T18's `2026id_` Wayback selector is less stable than an exact timestamp: retained digest/bytes identify the observed snapshot, but an exact resolved snapshot timestamp would improve long-term relocation.
- Literature candidates still need L1's real id/status/recheck/used-by and landing capture paths. The 15-row projection is not an integration or admission. No duplicate URL against registry was added; same-work/different-URL rejections T15/T16 and blog-versus-paper U05 are disclosed and scoped.
- Did not rerun paper experiments, execute exploits, or validate every background literature priority claim. Quotes establish what sources say, not independent correctness.
- LSP device unavailable: `read xd://lsp` returned “No such tool”. No source server or semantic call/reference evidence is claimed; review concerns Markdown/JSON evidence, not changed runtime callers. Canonical runtime, same-identity rerouting and resume continuity are outside this source-only change.
- No builds/tests/campaign counters run. Only explicitly assigned census was exercised. No tool installs/updates. No lane/fleet tracked files modified.

## Commands, artifacts and containment

All exact shell commands and live-fetch/extraction API forms are in `C1RevSources2/commands.md`; every opened URL/status/final URL/digest is in fetch manifests. PDFs and remote full bodies were scratch-only; retained review artifacts are each below 1 MiB. Disk guard before cloning: `/fast/scratch/hyaku` 43% used, 463.2G free; `/tmp` 97.8G free, `/var/tmp` 533.9G free. No ENOSPC.

Absolute produced files:
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/census-id-map.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/commands.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/extra-fetch-results.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/final-A-checks.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/final-B-checks.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/final-census.txt
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/lit-checks.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/lit-fetch-results.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-A-gate.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-A-rows.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-B-gate.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-B-rows.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-SOURCES-assembly.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-identities.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/reviewed-lit.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/wave1-census.txt
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/wave1-fetch-results.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/wave1-quote-checks.json
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/wave1-review.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2/wave1-rows.json

Scratch `/fast/scratch/hyaku/kengaku-r53/C1RevSources2` removed before yield. Tool inconsistencies: none observed; unavailable LSP device recorded above.

Self-check: coverage complete for all named drafts/candidates; quotes independently located and source units kept distinct. Accuracy 4/5 (source empirical claims not replicated), completeness 4/5 (literature integration fields intentionally L1-owned), clarity 4/5 (large required table), actionability 5/5 (pinned corrected drafts and exact census receipt), conciseness 4/5 (61-row coverage required); average 4.2. No scope-relevant fix remains with this reviewer.
