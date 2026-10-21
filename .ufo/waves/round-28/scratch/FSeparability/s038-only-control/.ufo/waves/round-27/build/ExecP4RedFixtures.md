# ExecP4RedFixtures — scoped findings

- Writer clone: `/tmp/kengaku-r27-ExecP4RedFixtures`, branch `r27-ExecP4RedFixtures`; observed HEAD/base `11a7fc8c64dc` (pre-registration commit). Frozen P4 target base: `b5719440e5eee46c1886fddbdf7bdc1624829454`.
- Added `plans/fixtures/r27/p4_mutate.py` and five JSON recipes. Each exports the exact base with `git archive` into `/tmp`, copies the export per mutant, applies one unique-anchor one-line edit, and runs the supplied checker `--root MUTANT --json`.
- A class is red only when its checker exits 1 and has a new `Px.` MISMATCH `(id, observed)` pair absent from the unmutated control. A pre-existing same-class mismatch cannot make a mutant pass. Exit 0 requires all five red; incomplete/missed set exits 1.

## Mutants

- P4a — `SCORECARD.md:790`, `278 assertions` → `279 assertions`; anchored to the final state-check assertion count.
- P4b — `corpus/README.md:268`, delete the `evidence/round26-sources/` Round-26 artifact row.
- P4c — `corpus/lessons/round-26.md:87`, `22 scout` → `23 scout`; base `.ufo/waves/round-26/build-spec.json` role count is scout=22 (72 items total).
- P4d — `corpus/knowledge/grader-perturbation-audit.md:34`, `covers 1708 records` → `covers 1709 records`.
- P4e — `corpus/SOURCES.md:67`, add `corpus/knowledge/llm-judge-calibration.md` as an S045 used-by citer.

## Retained evidence

- Command: `cd /tmp/kengaku-r27-ExecP4RedFixtures && PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/p4_mutate.py --checker plans/state_check.py`; base control output: `checker_exit=0 assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3 out_of_population=20`, P4a–P4e mismatches all 0. Command process exit 1 because v3 missed the required mutants.
- v3 mutant outputs: P4a `SCORECARD.md:790 checker_exit=0 new=0`; P4b `corpus/README.md:268 checker_exit=0 new=0`; P4c `corpus/lessons/round-26.md:87 checker_exit=0 new=0`; P4d `corpus/knowledge/grader-perturbation-audit.md:34 checker_exit=0 new=0`; P4e `corpus/SOURCES.md:67 checker_exit=0 new=0`. Final: `VERDICT: 0/5 mutants red ... -> exit 1` (v3 miss, expected before).
- `--keep` run and `diff -rq` plus five `diff -u` checks: each mutant differed from base in exactly its one intended file and the one intended line.
- Harness-only validation, **not v4**: an uncommitted `/tmp` test double added receipt/spec-derived P4 checks. Its clean base control was exit 0 with 0 P4 mismatches; all five mutants named their own class with exit 1, final 5/5 red and process exit 0. `stale-only` control: 0/5 attributed red, exit 1; mismatch-with-exit-0 control: 0/5 red, exit 1. `--json` parsed with the same results.

## Limits and files

- `plans/state_check.py` v4 was not present in this clone, so actual checker evidence is the requested v3-before run. The `/tmp` test double only validates fixture application and harness attribution; parent should rerun this script against integrated v4.
- Files written in clone (SHA-256):
  - `plans/fixtures/r27/p4_mutate.py` — `627d592b6bd6bacc83a614e7593325632cb5c5c36d8db105acbf2316e224d0ba`
  - `plans/fixtures/r27/p4_mutants/P4a.json` — `4eaf1eaa7871b1e5dd862daa4bc7ecc5674fd65f55e3a622f7091bcce7866687`
  - `plans/fixtures/r27/p4_mutants/P4b.json` — `bb3981aba1a9e861d2a6b9ab39182a05f84f409aac45a9d30a07fa91e0a34cf2`
  - `plans/fixtures/r27/p4_mutants/P4c.json` — `e379f15f59095d72a978f7fe92036d7c11791326ae73d07bf08a2c0eb27a771c`
  - `plans/fixtures/r27/p4_mutants/P4d.json` — `a9ebc474be8f3d0955f2ec5d7dbb2a083704b34c3f02c82fd5761709382e5c53`
  - `plans/fixtures/r27/p4_mutants/P4e.json` — `00fa2e61f8e6fccd7d18d81d2983ff8f23d48a1f1af67cddc6f028eb37f22f1b`
- Installs/updates: none.

VERDICT: Implemented the five scoped P4 red-fixture recipes and exporter; v3 misses all five as expected, while test-double validation confirms the recipes and attribution logic produce 5/5 class-specific reds.
