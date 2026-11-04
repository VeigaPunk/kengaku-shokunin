# C2MutantReplayR75 — independent replay

Axes: coverage and calibration. Read frozen claims in full before commands. No production edits, commits, installs, or delegated work. No mounted LSP tool was available; definitions were located with grep/read.

## Setup and qualifications

Clone command: `git clone --shared --revision=43255758ed7d74ea05c8e03686dd9ad37837f0cd /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/clone` (rc 0). The first attempt using abbreviated `--revision=43255758` failed rc 128; resolving the full commit corrected that. The revision clone is detached and has no refs (`git show-ref`, rc 1). Therefore the default master is unresolved: this is explicitly distinct from a master-bearing clone. Exclusive `--work` directories were added to every instrument invocation to honor scratch bounds.

## Frozen A1 replay (pre-fix)

### frozen
`python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75 --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/frozen-work`

Exit 0.
```text
LANE_TIP unknown
WORKTREE clean
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
STAMPS files=0 stamped=0 unstamped=0 unresolved=0 not_ancestor=0
PREDICATE R75-C2 pass
```

### control
`python3 plans/round75_c2_registry_audit.py --lane . --control-attribute --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/control-work`

Exit 0.
```text
LANE_TIP unknown
WORKTREE clean
R74-METRIC killed=10/10 (any-defect counting)
R75-METRIC expected_matched=9/10 wrong_id=1
OFF-TARGET X-off-target expected=:entry:unbacked-flag: defects=1 matched=False
NULL-ARM defects=0
PREDICATE R75-C2-control pass
```

### head
`python3 plans/round75_c2_registry_audit.py --lane . --rev HEAD --mutants --check-stamps corpus/evidence/round75 --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/head-work`

Exit 0.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
STAMPS files=0 stamped=0 unstamped=0 unresolved=0 not_ancestor=0
PREDICATE R75-C2 pass
```

The frozen target does **not** reproduce: K=0 violates K>0 despite the pre-fix pass. The detached default also passes with unknown tip. Explicit HEAD resolves A1 but still admits zero receipts. No existing c2 receipt content was read or trusted.

## Nine expected IDs and constructed wrong-id attack

Executed imported `mutate(clone, work)` from the A1 instrument via the Python driver (cell completed successfully). Exact result tuples:
```json
{
  "results": [
    [
      "M1-entry-absent",
      ":entry:script-absent:",
      [
        "SCRIPT-MISSING plans/nonexistent.py",
        "`tool-m`:entry:script-absent:plans/nonexistent.py"
      ]
    ],
    [
      "M2-selftest-absent",
      ":self-test:script-absent:",
      [
        "`tool-m`:self-test:script-absent:plans/ghost.py"
      ]
    ],
    [
      "M3-nine-cells",
      "MALFORMED-ROW columns=9",
      [
        "MALFORMED-ROW columns=9 line=| a | b | c | d | e | f | g | h | i |"
      ]
    ],
    [
      "M4-seven-cells",
      "MALFORMED-ROW columns=7",
      [
        "MALFORMED-ROW columns=7 line=| a | b | c | d | e | f | g |"
      ]
    ],
    [
      "M5-duplicate",
      "DUPLICATE-ROW",
      [
        "DUPLICATE-ROW `tool-a`"
      ]
    ],
    [
      "M6-flag-absent",
      ":entry:unbacked-flag:",
      [
        "`tool-m`:entry:unbacked-flag:--ghostflag"
      ]
    ],
    [
      "M7-errata-contradiction",
      "contradictory-revision",
      [
        "ERRATA:contradictory-revision:Do-nothing control (committed at freeze)->c80fcdb3 in item 3"
      ]
    ],
    [
      "M8-flag-literal-not-declared",
      ":entry:flag-not-declared:",
      [
        "`tool-doc`:entry:flag-not-declared:--strict"
      ]
    ],
    [
      "M9-empty-owner-cell",
      ":owner:empty",
      [
        "`tool-m`:owner:empty",
        "`tool-m`:owner:",
        "`tool-m`:self-test:unbacked-flag:--selftest"
      ]
    ]
  ],
  "null": [],
  "off": [
    "X-off-target",
    ":entry:unbacked-flag:",
    [
      "MALFORMED-ROW columns=9 line=| a | b | c | d | e | f | g | h | i |"
    ]
  ]
}
```

Constructed counterexample: Intercept M6 build_fixture only: remove --ghostflag from extra_row; add 9-cell malformed row. All other mutate() behavior unchanged. Invoked the actual `main()` with `--lane <clone> --rev HEAD --mutants --work <exclusive-dir>`; no instrument source changes.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
MUTANTS real=9 expected_matched=8 wrong_id=1 survived=1 null_arms=1 null_survived=1 total=10
PREDICATE R75-C2 fail
```
Exit 1. Expected M6 ID is absent; MALFORMED-ROW columns=9 fires. Matrix correctly refuses the off-target kill (expected_matched=8, wrong_id=1), but also prints survived=1 for that killed mutant; those two counts conflate categories.

## Null construction

A1 `R74.build_fixture(clean)` versus the actual null construction:
```diff
--- default-clean
+++ actual-null
@@ -3,4 +3,5 @@
 | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
 |---|---|---|---|---|---|---|---|
 | `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
-| `tool-b` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
+| `tool-n` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes   | read-only | kengaku |
+
```

Exact observations:
```json
{
  "default_vs_null": "--- default-clean\n+++ actual-null\n@@ -3,4 +3,5 @@\n | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n |---|---|---|---|---|---|---|---|\n | `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean \u00b7 `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |\n-| `tool-b` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes | read-only | kengaku |\n+| `tool-n` | gate | `python3 plans/tool_b.py` | `0` clean \u00b7 `1` failed | none declared | pinned bytes   | read-only | kengaku |\n+\n",
  "clean_defects": [],
  "null_defects": [],
  "same_name_clean_defects": [],
  "substantive_defects": [
    "`tool-n`:entry:unbacked-flag:--ghostflag"
  ],
  "whitespace_normalized_equal_default": false,
  "whitespace_normalized_equal_same_name": true
}
```

The original null is real and survives, but is not strictly whitespace-only against the default clean fixture: it renames tool-b to tool-n. A clean same-name fixture normalizes to identical bytes after whitespace removal. The substantive `--ghostflag` replacement yields the expected unbacked-flag finding, so the fixture is not universally accepted.

## Stamp arms

No orphan commit was created: the no-commit contract takes precedence. Existing candidate `2b9f62e66d425be7338dc4a688a3e9677f8b2cae` came from `git -C <lane> rev-list --all --not master --max-count=3` (rc 0). In the clone, `git cat-file -e 2b9f62e66d425be7338dc4a688a3e9677f8b2cae^{commit}` returned 0 and `git merge-base --is-ancestor 2b9f62e66d425be7338dc4a688a3e9677f8b2cae HEAD` returned 1. This supplies a real nonancestor without mutation.

Four files were constructed: unstamped `VERDICT ok`; nonexistent stamp `LANE_TIP ffffffffffffffffffffffffffffffffffffffff`; existing nonancestor stamp above; valid A1 stamp as positive control. All stamped arms include WORKTREE clean.

`python3 plans/round75_c2_registry_audit.py --lane . --rev HEAD --check-stamps /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/stamp-arms --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/three-stamp-work`
Exit 1.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
STAMPS files=4 stamped=1 unstamped=1 unresolved=1 not_ancestor=1
  DEFECT UNSTAMPED a-unstamped.txt
  DEFECT REVISION:unresolvable b-nonexistent.txt ffffffffffff
  DEFECT REVISION:not-ancestor c-nonancestor.txt 2b9f62e66d42
PREDICATE R75-C2 fail
```

All three negative arms are caught by their own legs: UNSTAMPED, REVISION:unresolvable, REVISION:not-ancestor. Valid control accepted.

## Integration snapshot replay (not a committed landing-tip certification)

Per L1 follow-up, created a second plain shared clone (rc 0), preserving master at A1. Copied only the current lane instrument into that scratch clone via read/write; did not modify lane files. This intentionally yields WORKTREE dirty. Snapshot SHA256: `73d745e4672f68d182e90ec8b38eb4df9c6dcea3b81653c75b3106e556390429`. Integration fixes were not committed; calling this a fresh committed fixed tip would be false.

### fixed-frozen
`python3 plans/round75_c2_registry_audit.py --lane . --rev master --mutants --check-stamps corpus/evidence/round75 --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/fixed-frozen`
Exit 1.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE dirty
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
STAMPS files=0 stamped=0 unstamped=0 unresolved=0 not_ancestor=0
  DEFECT STAMPS:empty-dir corpus/evidence/round75 holds no *.txt receipt
PREDICATE R75-C2 fail
```

### fixed-stamps
`python3 plans/round75_c2_registry_audit.py --lane . --rev master --check-stamps /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/stamp-arms --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/fixed-stamps`
Exit 1.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE dirty
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
STAMPS files=4 stamped=1 unstamped=1 unresolved=1 not_ancestor=1
  DEFECT UNSTAMPED a-unstamped.txt
  DEFECT REVISION:unresolvable b-nonexistent.txt ffffffffffff
  DEFECT REVISION:not-ancestor c-nonancestor.txt 2b9f62e66d42
PREDICATE R75-C2 fail
```

### fixed-control
`python3 plans/round75_c2_registry_audit.py --lane . --rev master --control-attribute --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/fixed-control`
Exit 0.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE dirty
R74-METRIC killed=10/10 (any-defect counting)
R75-METRIC expected_matched=9/10 wrong_id=1
OFF-TARGET X-off-target expected=:entry:unbacked-flag: defects=1 matched=False
NULL-ARM defects=0
PREDICATE R75-C2-control pass
```

### fixed-empty
`python3 plans/round75_c2_registry_audit.py --lane . --rev master --check-stamps /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/empty --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/fixed-empty`
Exit 1.
```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE dirty
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
STAMPS files=0 stamped=0 unstamped=0 unresolved=0 not_ancestor=0
  DEFECT STAMPS:empty-dir /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/empty holds no *.txt receipt
PREDICATE R75-C2 fail
```

### fixed-unknown
`python3 plans/round75_c2_registry_audit.py --lane . --rev master --rev nonexistent-seat-rev --check-stamps /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/stamp-arms --work /fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75/fixed-unknown`
Exit 1.
```text
LANE_TIP unknown
WORKTREE dirty
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
STAMPS files=4 stamped=2 unstamped=1 unresolved=1 not_ancestor=0
  DEFECT TIPTAG:unresolved --rev nonexistent-seat-rev did not resolve to a commit
  DEFECT UNSTAMPED a-unstamped.txt
  DEFECT REVISION:unresolvable b-nonexistent.txt ffffffffffff
PREDICATE R75-C2 fail
```

Captured the actual fixed mutate() null before cleanup, rather than trusting prose. Whitespace-normalized equality with default clean fixture: True; defects []. Fixed delta:
```diff
--- 
+++ 
@@ -3,4 +3,5 @@
 | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
 |---|---|---|---|---|---|---|---|
 | `tool-a` | gate | `python3 plans/tool_a.py` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pinned bytes | read-only | kengaku |
-| `tool-b` | gate | `python3 plans/tool_b.py` | `0` clean · `1` failed | none declared | pinned bytes | read-only | kengaku |
+|  `tool-b`  | gate | `python3 plans/tool_b.py` |  `0` clean · `1` failed  | none declared |  pinned bytes  | read-only  | kengaku |
+
```

## Evidence references, risks, and handoff

Grep/read evidence: `plans/round75_c2_registry_audit.py` A1 lines 133–162 (stamps), 180–224 (mutants/null), 297–324 (attribution); `plans/round74_c2_registry_audit.py` lines 268–315 (fixture builder). Integration source grep located TIPTAG:unresolved at 141, STAMPS:empty-dir at 143, whitespace-only null at 217–225. Grep calls returned matching source lines.

Retained evidence is the exact command output and construction data in this report. Production instrument changes belong to L1. Remaining gate: parent must reproduce the frozen command from a committed master-bearing landing clone containing K>0 receipts; neither A1 nor the uncommitted snapshot certifies that target here. Missing WORKTREE stamps were not separately attacked (out of requested three stamp arms). No tests/build/linters/formatters outside the explicitly assigned instrument probes ran.

Self-evaluation (1–5): accuracy 4 (integration snapshot is dirty, explicitly labeled); completeness 4 (existing nonancestor substituted for prohibited new orphan); clarity 4 (long raw evidence retained); actionability 4 (landing gate remains parent-owned); conciseness 4 (raw receipts add length). Overall 4.0. Highest-impact improvement: run the frozen gate on the committed landing tree.

Cleanup: Python `shutil.rmtree("/fast/scratch/hyaku/kengaku-r75/C2MutantReplayR75")` completed without exception (driver success); the entire exclusive scratch root was removed before yield.
