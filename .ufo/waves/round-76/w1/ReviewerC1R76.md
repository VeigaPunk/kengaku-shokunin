# ReviewerC1R76 — C1 adversarial review

Axes: **coverage** (surface population/identity), **calibration** (printed verdict vs observed defects).
Recommendation only; no judgment/admission or production edits.

## Findings, severity first

1. **HIGH — ACCEPT: scope shrink makes the gate green without preserving the target population.**
   `plans/round76_c1_surface_resolver.py:182-187,219-224` counts only current rows; it never compares identities/population to the frozen declaration. The actual baseline prints `total=11 present=4 absent=7`; deleting exactly its seven absent rows yields `total=4 present=4 absent=0`, `AGREE agree=4 disagree=0`, pass, rc 0. The 2-row fixture also shrinks to one present row and passes. Minimal repair for target enforcement: compare the landing surface identity set against the frozen 11-row set (a count alone permits substitutions). **Contract distinction:** the frozen predicate is universally quantified over declared rows and has no minimum; therefore this is a target/coverage-scope escape, not a counterexample to that narrow row-local predicate. Do not retroactively rewrite it.

2. **MEDIUM — ACCEPT: anchor laundering plus removal of the obsolete marker.**
   `...surface_resolver.py:129-139,194-205` trusts the first path token and does not bind the surface name/description to its anchor. Exact accepted bytes are `anchor-launder.PROVINCE.md`: `| Absent | `corpus/README.md` — missing.md research notes | research notes are still unavailable |` (see literal file for Markdown bytes). It reports present/pass even though the description still concerns missing research notes. A literal anchor substitution **retaining** ABSENT is **REJECT** (STALE-ABSENT, rc 1; `anchor-retain-marker.txt`). Smallest identity-preservation repair: frozen surface-name → canonical-anchor mapping, rejecting substitutions unless separately authorized. **Contract distinction:** the frozen claim expressly chooses the first declared anchor, so semantic correspondence to prose is outside that narrow promise; this is a coverage limitation, not proof that its path resolver lies.

3. **MEDIUM — ACCEPT: endpoint substitution can change the measured service while retaining its description.**
   `...surface_resolver.py:154-167,194-205`: identical dead-server prose and no marker yields rc 1 at `http://127.0.0.1:45669/health` (`http=000`, UNDECLARED-ABSENT), but rc 0 at `http://127.0.0.1:1234/health` (`http=200`). Keeping ABSENT makes substitution **REJECT** (STALE-ABSENT). Smallest repair: pin each named surface's canonical endpoint in the same identity map; if claims concern model identity, HTTP availability alone cannot establish it. No identity payload was probed here. The frozen contract only promises HTTP status, not same-model rerouting; do not describe this result as same-identity continuity.

4. **LOW — ACCEPT on absent row / REJECT on present row: marker dates are opaque regex bytes.**
   `...surface_resolver.py:64,204-210`: `**ABSENT 2030-01-01**` on a present path is rejected as STALE-ABSENT, rc 1. On an absent path it passes, rc 0, as does impossible `**ABSENT 2030-99-99**`. Smallest repair for a genuinely dated declaration: parse `date.fromisoformat`, reject impossible calendar dates; future-date policy should be explicit before enforcing it. The frozen rule does not demand freshness or date ≤ today, so future dates alone are not a violation of that stated rule. Impossible dates undermine the ordinary meaning of YYYY-MM-DD.

5. **LOW — ACCEPT: duplicate rows inflate `total=` without unique coverage.**
   `...surface_resolver.py:185-187,219-224`: two rows named `Same surface`, one present-anchored and one correctly ABSENT, print total=2/agree=2/pass. Two exact copies of `Present`/`present.md` also print total=2 present=2/pass. `total` is row count, not distinct surfaces. Minimal repair when uniqueness is intended: reject duplicate surface IDs and duplicate canonical anchors (or explicitly label the metric row count). No uniqueness requirement exists in the frozen row-local predicate, so this is a metric/interpretation limitation rather than a failed frozen invariant.

6. **INFO — REJECT: tally forgery is caught.**
   Scratch-only gate mutant changes `f"AGREE agree={agree} disagree={disagree}"` to `f"AGREE agree={agree} disagree=0"`, leaving the real missing-marker defect intact. `...surface_resolver.py:236-241` prints both `DEFECT UNDECLARED-ABSENT 1 Absent missing.md` and `DEFECT TALLY-MISMATCH printed=0 defects=1`, predicate fail, rc 1. No repair indicated for this attack. The original gate on the same fixture prints disagree=1 and fails normally.

## What ran / evidence

Read the frozen claims in full before commands. Read actual base→worktree diff with:
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff fda63968f29f8f58dc2b28831acac879405b8326 -- plans/round76_c1_surface_resolver.py PROVINCE.md` (rc 0).
`read xd://lsp` returned `No such tool: xd://lsp`; no LSP status/references/definition/diagnostics device is mounted. Text inspection is a fallback, not semantic-reference proof.

Driver invocation (rc 0):
`env PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/ReviewerC1R76/probe.py`
Cwd was the own scratch directory. Driver uses a ThreadPoolExecutor to run independent attacks. Fixture creation and commands are preserved in `ReviewerC1R76/probe.py`; every fixture's exact bytes are in `<case>.PROVINCE.md`. The two marker-retention controls were invoked separately with the exact commands below. `corpus` and `grader.py` in scratch were read-only symlinks into this lane, not mirrors. No Git fixture mutations/clones or tool installations were performed. Scratch removed after preserving receipts.

`gate-reviewed.py` and `province-reviewed.md` preserve the bytes loaded by the driver. Other seats may change the worktree concurrently; receipts are observations at execution, not promises about later revisions.

### Verbatim commands, outputs and exit codes

#### actual-baseline

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
SURFACE 1 absent ~/Projects/webzites/repos/llm-wiki (path=~/Projects/webzites/repos/llm-wiki)
SURFACE 2 absent ~/archive/bench-arena/ (path=~/archive/bench-arena/)
SURFACE 3 absent http://127.0.0.1:34113 (http=000)
SURFACE 4 absent http://127.0.0.1:45669 (http=000)
SURFACE 5 absent ~/Projects/bounties/ledger/telemetry.jsonl (path=~/Projects/bounties/ledger/telemetry.jsonl)
SURFACE 6 absent ~/.bailian/telemetry.jsonl (path=~/.bailian/telemetry.jsonl)
SURFACE 7 absent ~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl} (path=~/.bailian/skills/bailian-docs-llm-wiki/models/index.md expanded=2)
SURFACE 8 present corpus/evidence/round8-horizon/ (path=corpus/evidence/round8-horizon/)
SURFACE 9 present grader.py (path=grader.py)
SURFACE 10 present corpus/README.md (path=corpus/README.md)
SURFACE 11 present corpus/knowledge/eval-prior-art-calibration.md (path=corpus/knowledge/eval-prior-art-calibration.md)
SURFACES total=11 present=4 absent=7 prose=0
AGREE agree=11 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### baseline

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/baseline
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent missing.md (path=missing.md)
SURFACES total=2 present=1 absent=1 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### scope-one

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/scope-one
SURFACE 1 present present.md (path=present.md)
SURFACES total=1 present=1 absent=0 prose=0
AGREE agree=1 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### scope-real-absent-only

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/scope-real-absent-only
SURFACE 1 present corpus/evidence/round8-horizon/ (path=corpus/evidence/round8-horizon/)
SURFACE 2 present grader.py (path=grader.py)
SURFACE 3 present corpus/README.md (path=corpus/README.md)
SURFACE 4 present corpus/knowledge/eval-prior-art-calibration.md (path=corpus/knowledge/eval-prior-art-calibration.md)
SURFACES total=4 present=4 absent=0 prose=0
AGREE agree=4 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### scope-real-absent-and-prose

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/scope-real-absent-and-prose
SURFACE 1 present corpus/evidence/round8-horizon/ (path=corpus/evidence/round8-horizon/)
SURFACE 2 present grader.py (path=grader.py)
SURFACE 3 present corpus/README.md (path=corpus/README.md)
SURFACE 4 present corpus/knowledge/eval-prior-art-calibration.md (path=corpus/knowledge/eval-prior-art-calibration.md)
SURFACES total=4 present=4 absent=0 prose=0
AGREE agree=4 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### marker-present

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/marker-present
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent missing.md (path=missing.md)
SURFACES total=2 present=1 absent=1 prose=0
AGREE agree=1 disagree=1
DEFECT STALE-ABSENT 1 Present present.md marked **ABSENT 2030-01-01**
PREDICATE R76-C1 fail
EXIT 1
```

#### marker-absent

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/marker-absent
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent missing.md (path=missing.md)
SURFACES total=2 present=1 absent=1 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### marker-invalid

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/marker-invalid
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent missing.md (path=missing.md)
SURFACES total=2 present=1 absent=1 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### anchor-launder

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/anchor-launder
SURFACE 1 present corpus/README.md (path=corpus/README.md)
SURFACES total=1 present=1 absent=0 prose=0
AGREE agree=1 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### anchor-retain-marker

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/anchor-retain-marker
SURFACE 1 present ../baseline/present.md (path=../baseline/present.md)
SURFACES total=1 present=1 absent=0 prose=0
AGREE agree=0 disagree=1
DEFECT STALE-ABSENT 1 Absent ../baseline/present.md marked **ABSENT 2026-11-04**
PREDICATE R76-C1 fail
EXIT 1
```

#### endpoint-original

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/endpoint-original
SURFACE 1 absent http://127.0.0.1:45669/health (http=000)
SURFACES total=1 present=0 absent=1 prose=0
AGREE agree=0 disagree=1
DEFECT UNDECLARED-ABSENT 1 Dead server http://127.0.0.1:45669/health
PREDICATE R76-C1 fail
EXIT 1
```

#### endpoint-substitute

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/endpoint-substitute
SURFACE 1 present http://127.0.0.1:1234/health (http=200)
SURFACES total=1 present=1 absent=0 prose=0
AGREE agree=1 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### endpoint-retain-marker

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/endpoint-retain-marker
SURFACE 1 present http://127.0.0.1:1234/health (http=200)
SURFACES total=1 present=1 absent=0 prose=0
AGREE agree=0 disagree=1
DEFECT STALE-ABSENT 1 Dead server http://127.0.0.1:1234/health marked **ABSENT 2026-11-04**
PREDICATE R76-C1 fail
EXIT 1
```

#### tally

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/tally
SURFACE 1 absent missing.md (path=missing.md)
SURFACES total=1 present=0 absent=1 prose=0
AGREE agree=0 disagree=1
DEFECT UNDECLARED-ABSENT 1 Absent missing.md
PREDICATE R76-C1 fail
EXIT 1
```

#### tally-mutant

```text
$ python3 /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/tally-mutant.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/tally
SURFACE 1 absent missing.md (path=missing.md)
SURFACES total=1 present=0 absent=1 prose=0
AGREE agree=0 disagree=0
DEFECT UNDECLARED-ABSENT 1 Absent missing.md
DEFECT TALLY-MISMATCH printed=0 defects=1
PREDICATE R76-C1 fail
EXIT 1
```

#### duplicates

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/duplicates
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent missing.md (path=missing.md)
SURFACES total=2 present=1 absent=1 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

#### duplicate-token

```text
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --lane /fast/scratch/hyaku/kengaku-r76/ReviewerC1R76/duplicate-token
SURFACE 1 present present.md (path=present.md)
SURFACE 2 present present.md (path=present.md)
SURFACES total=2 present=2 absent=0 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
EXIT 0
```

## Residual risk and verification gaps

- These six attack families do not exhaust the parser, URL redirects, non-local URLs, brace-set interpretation, or stale-prose vocabulary. No assertion of exhaustive saturation.
- No model identity, canonical runtime routing implementation, or resume/preflight mutation path is changed by this diff; no `resume_continuity_v1` or same-identity guarantee was tested or inferred.
- The scope/identity/duplicate ACCEPTs expose assurance beyond the frozen narrow row-local contract. Integrator must not equate green fixture predicates with the frozen exact target being reached. Repairs above are recommendations, not edits or changes to frozen rules.
- No build/lint/full selftest/mutant matrix/C2 verification was run. Only the exact commands above were exercised.

Self-evaluation (1–5): accuracy 4 (concurrent worktree lacks immutable execution pin); completeness 4 (all six requested attacks exercised, not exhaustive parser coverage); clarity 4 (full logs add length); actionability 4 (minimal repairs named, not applied by read-only reviewer); conciseness 4 (verbatim evidence retained as required). Overall 4.0. Highest-value improvement: integrator should bind final gate execution to its landing revision; user should agree the scope distinction prevents overclaiming.
