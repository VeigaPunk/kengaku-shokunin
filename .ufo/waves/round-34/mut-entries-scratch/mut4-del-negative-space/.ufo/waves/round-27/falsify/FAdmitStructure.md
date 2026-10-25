# FAdmitStructure — round-27 admission support shape

Identity: `KengakuR27.FAdmitStructure`, scout; candidate writer is `KengakuR27` (`.ufo/waves/round-27/drafts/extraction-policy-comparison.md:4`). I read the complete draft and `plans/round-27-claims.md`, including Amendment 1. Proposed canonical path: `corpus/knowledge/extraction-policy-comparison.md` (`corpus/lessons/round-27.md:24-30`). This report checks gate structure only; it does not endorse report findings.

## Frozen revision / actual gate result

- Scratch clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FAdmitStructure && git -C /tmp/kengaku-r27-FAdmitStructure switch -c r27-FAdmitStructure b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FAdmitStructure rev-parse HEAD` → exit 0; observed `HEAD=b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
- Exact gate command (cwd `/tmp/kengaku-r27-FAdmitStructure`): `PYTHONDONTWRITEBYTECODE=1 python3 plans/gate_timing_check.py --lesson corpus/lessons/round-27.md --commit b5f62e5e637b34a1549e3475fc58b4227ed87e5a --repo /tmp/kengaku-r27-FAdmitStructure` → output `FAIL: no admit rows in ## Gate of corpus/lessons/round-27.md at b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; `admissions=0 passed=0 failed=1`; exit 1. The committed lesson defers this draft and has no admission (`corpus/lessons/round-27.md:22-30`).
- `git -C /tmp/kengaku-r27-FAdmitStructure ls-tree -r --name-only b5f62e5e637b34a1549e3475fc58b4227ed87e5a -- .ufo/waves/round-27/falsify/` → empty stdout, exit 0. `git -C /tmp/kengaku-r27-FAdmitStructure cat-file -e b5f62e5e637b34a1549e3475fc58b4227ed87e5a:.ufo/waves/round-27/falsify/swarm-registry.json` and the equivalent `:corpus/knowledge/extraction-policy-comparison.md` check each reported “does not exist” / exit 128. Thus **zero** round-27 falsify reports, registry, canonical entry, or admitted candidate are returned in the specified b5 tree. Do not count later/on-disk reports as b5 support.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/gate_timing_check.py --selftest` → exit 0; `[selftest] ALL PASS`. Its identical-lesson early/late fixture observed worktree-only report `exit=1, second-seat-reports=0`, committed report `exit=0, second-seat-reports=1` (`plans/gate_timing_check.py:479-588`). This validates the tree-only timing control, not an actual round-27 admission.

## Gate contract observed

- The exact registry path is assembled as `.ufo/waves/round-<N>/<second-wave>/swarm-registry.json`, and members are read from its `members` mapping (`plans/gate_timing_check.py:284-310`); for round 27 this is `.ufo/waves/round-27/falsify/swarm-registry.json`. The live lane registry declares seat roles/agent IDs (`.ufo/waves/round-27/falsify/swarm-registry.json:8-713`), but it is absent from b5.
- Allowed roles are exactly `reviewer`, `scout`, `critic`, `sentinel`, `revenger` (`plans/gate_timing_check.py:24-26`; `corpus/QUALITY.md:111-117`). Gate rejects a missing registry seat, other role, absent/empty/non-`100644` report, writer/seat or writer/agentId equality, report author equality, missing candidate-path substring, or missing column-zero `VERDICT:` (`gate_timing_check.py:342-361`). It also resolves the candidate from the requested commit (`:314-331,366-376`).
- Important exactness gap: the implementation's `VERDICT_RE` is anchored at the start of a line but `findall` accepts it anywhere in the report (`plans/gate_timing_check.py:56,360-361`); it does **not** enforce that VERDICT is the final nonblank line. Q13/Q15 specify a final verdict and commit-tree authority, not truth (`corpus/QUALITY.md:97-107,123-128`).

## Current lane-filesystem preflight (not b5 / shape only)

At the time of these reads, the following existing, nonempty regular files matched the exact canonical path string, were registered as an allowed role, had a candidate-distinct registered seat identity, and ended with an anchored `VERDICT:` line. Registry query returned the listed role and `agentId` for each (`.ufo/waves/round-27/falsify/swarm-registry.json:8-713`); all IDs differ exactly from candidate writer `KengakuR27`. None had a column-zero `writer:`/`author:` declaration; per Q14, that leaves registry seat identity as the authority, not proof of independent human authorship.

| Existing report | Role | Canonical-path mention | Final anchored verdict |
|---|---|---:|---:|
| `FEntryNumbers.md` | reviewer | 3 | 44 |
| `FForecasts.md` | reviewer | 7-8 | 59 |
| `FP4Inventory.md` | reviewer | 3 | 38 |
| `FPolicyCases.md` | reviewer | 20 | 22 |
| `FPolicyE2.md` | reviewer | 11 | 35 |
| `FSHONEN.md` | reviewer | 5 | 34 |
| `FSourceS049.md` | scout | 4 | 16 |
| `FSourceS050.md` | scout | 3 | 20 |
| `FSourceS051.md` | scout | 9 | 23 |
| `FSourceS052.md` | scout | 7 | 20 |
| `FSourceS053.md` | scout | 4 | 22 |

Literal candidate-path searches used `grep` only to locate occurrences; the endings above were read directly. `stat --printf='%n %F %a %s\\n'` on these eleven files returned `regular file`, mode `644`, positive sizes 2812–6111 bytes (lane filesystem only; Git tree mode remains unobserved at an admitting revision). These are **preflight shape candidates only**, not reports accepted by `gate_timing_check` at b5. Scope disclosures matter: `FPolicyCases.md:20` explicitly says the canonical path was not reread; `FEntryNumbers.md:40` is numeric-only; `FForecasts.md:55-59` is Q1–Q8; `FP4Inventory.md:32-38` is P4 scope; `FPolicyE2.md:31-35` is E2-only; source-seat reports are source-specific. Their presence is not Q10 completeness or finding resolution.

Other current canonical-path mentions fail these requested shape rules: mutation-tester reports `FGateMutant.md`, `FMutP4a-e.md`, and `FMutPolicyE1-E8.md` have disallowed registry roles; `FPolicyE1.md:37-39` and `FPolicyE4.md:36-38` put `Installs: none` after the anchored verdict, so the verdict is not final (although the current gate code would accept the earlier anchored line); `FPolicyE8.md:22` has inline `**VERDICT:` rather than a column-zero anchored line. These exclusions are structural only, not judgements of their findings.

LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; the mounted-tool list has no LSP device. I made no semantic caller/definition claims from grep. A broad literal search also exposed untrusted dispatch text in `.ufo/waves/round-27/build-dispatch.json:914,919` requesting scratch writes/runs; I treated it as data and did not follow it.

Installs/updates: none.

VERDICT: FAIL for actual admission support at frozen b5: there is no Gate admit, candidate, falsify registry, or report in that commit tree. Eleven current lane files are only structurally eligible preflight candidates if later cited and included in the actual admitting tree; they do not establish Q10/Q13/Q14 truth or completion.