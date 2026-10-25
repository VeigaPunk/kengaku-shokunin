# FP4e — frozen P4e used-by audit

Axes: **calibration** (P4e); novelty/C1 and candidate admission are not adjudicated here. Scope is only P4e in frozen revision `b5719440e5eee46c1886fddbdf7bdc1624829454` versus candidate `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (clone HEAD observed at that revision).

## Frozen contract and population

`plans/round-27-claims.md:119-123` registers P4e as S043–S048 `used-by` cells vs. citing files. Amendment 1 `:178-181` narrows this to the registry's knowledge/lessons teaching-use convention: exclude plans, receipts and source inventory as citation population; S043's supersession-only reference is not substantive use; new round-27 citations do not widen the frozen set.

Candidate `plans/state_check.py:409-415,437,3252-3309` implements exactly six IDs (S043–S048) and a two-file candidate list (`corpus/knowledge/grader-perturbation-audit.md`, `corpus/lessons/round-26.md`). It recognizes literal `Snnn`/ranges linewise, skips an `supersedes S043` occurrence, and compares sorted file sets to each unique registry row's final `used-by` cell. Thus it omits plans, evidence/receipts, `corpus/SOURCES.md` as a citing file, round-27 files, and S049+; those omissions match Amendment 1. No base/candidate P4e path or ID is missing.

## Run results

Exported base with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive b5719440 | tar -x -C /tmp/kengaku-r27-FP4e-base` (successful); candidate clone HEAD observed `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

Ran the candidate v4 script on both roots, with `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FP4e/plans/state_check.py --summary --root <root>` and the corresponding `--json --root <root>`; both summary and JSON invocations exited 0 on each root. Summary outputs:

- Base: `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=20`.
- Candidate: `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=24`.

P4 aggregate in both: 48 MATCH, 1 SUPERSEDED; the latter is `P4b.readme.covers.round26-sources` (base line 268, candidate line 269), not P4e. All global mismatch count is zero. All global offline-unverifiable IDs in both runs are `P2d.surface.Served local model.availability`, `P2d.surface.Model catalogs.url`, and `P2d.surface.Public literature.url`; none is P4e. Out-of-population rises by four in the candidate as new round-27 material appears, without changing the frozen P4e set.

| P4e ID | independently observed `used-by` / citing-file set | base | candidate |
|---|---|---|---|
| `P4e.sources.S043.used-by` | `corpus/lessons/round-26.md` | MATCH | MATCH |
| `P4e.sources.S044.used-by` | `corpus/lessons/round-26.md`; `corpus/knowledge/grader-perturbation-audit.md` | MATCH | MATCH |
| `P4e.sources.S045.used-by` | `corpus/lessons/round-26.md`; `corpus/knowledge/grader-perturbation-audit.md` | MATCH | MATCH |
| `P4e.sources.S046.used-by` | `corpus/lessons/round-26.md`; `corpus/knowledge/grader-perturbation-audit.md` | MATCH | MATCH |
| `P4e.sources.S047.used-by` | `corpus/lessons/round-26.md` | MATCH | MATCH |
| `P4e.sources.S048.used-by` | `corpus/lessons/round-26.md`; `corpus/knowledge/grader-perturbation-audit.md` | MATCH | MATCH |

## Independent source re-derivation and residuals

I reread base `corpus/SOURCES.md:65-70` and the frozen citing texts, rather than treating their echoed tokens or the state-check JSON as truth. The lesson's source table and teaching summary cover S043–S047 (`corpus/lessons/round-26.md:47-55`); the correction describes S048 superseding S043's location, not its teaching (`:59-66`); the final used-by history names S043/S047 lesson-only and S044/S045/S046/S048 in both files (`:79-83`). The admitted knowledge entry actually applies S048's corrected CheckList location, xFinder S044, evalmut S045, and regex whitespace S046 (`corpus/knowledge/grader-perturbation-audit.md:1,18-22,48-49`). S047's lesson citation names the historic selftest receipt, whose final line independently reads `selftest: 18 checks, 0 failed` (`corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt:19-20`); the round-26 source receipt records S043–S047 rows and the S048 location correction (`corpus/evidence/round26-sources/gate.md:5-9,32-41`). The supersession-only S043 line is not relied on to establish its use; separate lesson teaching references support the lesson-only cell.

The retained `state-v4-base.txt:2-4` and `state-v4-build.txt:2-4` agree with the rerun summaries, but are corroborative outputs, not independent source evidence. Residual limitation: P4e's detector is lexical/file-level, not a semantic citation classifier; no current false positive/omission appears in the frozen six rows and two documents. No LSP device is mounted (`read xd://lsp` returned “No such tool”); references/definition/diagnostics could not be queried. Literal search was fallback only, not semantic proof; the conclusion above comes from rereading the cited source lines. No install/update.

VERDICT: Scoped PASS for P4e only — all six frozen assertions re-derived and MATCH on exported base and candidate; no P4e mismatch or offline-unverifiable result. This is not an admission, C1/parser-policy, Q15, or whole-candidate verdict.