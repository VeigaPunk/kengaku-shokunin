# ClaimsCriticR75 — frozen-claim falsification

Axes: **coverage (R75-C1)** and **calibration (R75-C2)**. Review recommendations, not canonical admission decisions: **CHALLENGE both claims** for the counterexamples below. No predicate, target, control, or kill rule is amended here.

## Method and evidence boundary

Read `plans/round-75-claims.md` completely before commands. Exported revision `43255758` using `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 43255758` (rc 0) into `/fast/scratch/hyaku/kengaku-r75/ClaimsCriticR75/a1`; no clone, checkout, commit, or production edits. All tested instruments, including their imported R74 helper, came from that export. Archive export excludes untracked receipts; stamp experiments therefore explicitly use the receipts of record in the lane, not the empty exported evidence directory.

Notation: `$S` is that exported A1 tree; `$W` its parent seat scratch root; `$L` is `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; `$E=$L/corpus/evidence/round75`. Commands below ran from `$S`. Python function probes were executed through the tool's Python cell, not a new agent runtime. For full stamp-bearing fixture runs, environment `GIT_DIR=$L/.git GIT_WORK_TREE=<fixture> GIT_OPTIONAL_LOCKS=0` provides a read-only object resolver without creating repository metadata. This is deliberately disclosed: the malformed flag fixture reports `WORKTREE dirty`, not a clean landed tree. No claim of a clean landing measurement is made for it.

Grep evidence: searched the frozen claims for `Kill rule|WORKTREE|K > 0`, C1 for `ROW =|EVIDENCE =|ROW.match|EVIDENCE.findall`, C2 for `kw.value|declared.update|STAMP.search|evidence.glob|expected finding|M1-entry|matched =|exp in`. Relevant source locations: C1 lines 45–46, 78–100, 104–121; C2 lines 64–79, 133–162, 181–192, 276–279, 314–331. Live C1 changed its duplicate-header print while this review ran; tested bytes remain the A1 export, not the intervening live edit.

## R75-C1: hidden token inventory reaches every numeric target

**Counterexample.** Replace the scratch README with one HTML comment containing every filename token and evidence-directory token, with no descriptions, links, table headers, or usable visible index:

```python
rows = ['<!--']
for kind in ('knowledge', 'lessons'):
    rows += [f'| `{kind}/{p.name}`' for p in sorted((S/'corpus'/kind).glob('*.md'))]
rows += [f'corpus/evidence/{p.name}/' for p in sorted((S/'corpus/evidence').iterdir()) if p.is_dir()]
rows += ['-->']
(S/'corpus/README.md').write_text('\n'.join(rows)+'\n')
```

Executed `python3 plans/round75_c1_index_parity.py --lane .`: **rc 0**, printing:

```text
UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
UNIVERSE lessons files=123 indexed=123 missing=0 orphan=0
UNIVERSE evidence dirs=66 indexed=66 missing=0 orphan=0
PREDICATE R75-C1 pass
```

All 263 surfaces receive credit although the rendered README displays no index. C1 matches filename prefixes anywhere in raw README lines and evidence mentions anywhere in raw bytes; it never establishes a visible index row. This is stronger than denominator narrowing: the denominators remain exactly 74/123/66. The archive fixture prints `LANE_TIP unknown`; therefore this experiment proves numeric/predicate reachability, not the entire clean-provenance sentence. `[INFERENCE]` Putting these same README bytes into a genuinely clean repository would not change the census, because `census()` does not inspect git metadata.

**Kill-rule adequacy.** The literal C1 kill rule lists defect lines, universe counts, and selftest totals, but not loss of its required `WORKTREE clean` line. Single missed line: `WORKTREE clean`. The observed token-only run returns rc 0 even with `LANE_TIP unknown`; the literal kill-rule conditions do not reject it. This is a review of the written rule, not a claim that an unprovided canonical admission runner was executed.

**Smallest safe correction.** Have the integration owner recognize actual visible index rows outside comments/code blocks, require the existing row schema's usable description/link cells, and add the hidden-token fixture as a reject case. Do not change disk universes or silently redefine the frozen target. Enforce the already-required provenance lines in acceptance. The unsupported implication from raw token coverage to usable indexing is a calibration limitation as well as a coverage defect.

## R75-C2: all target counters coexist with a rejected entry flag

**Counterexample.** Built a clean R74 fixture with `R74.build_fixture($W/flag)`, added an ordinary registry row for `python3 plans/tool_doc.py --strict`, and created:

```python
import argparse
p = argparse.ArgumentParser()
p.add_argument('--lane', help='--strict')
p.parse_args()
```

Here `--strict` is help text, not an option declaration. Executed:

```text
GIT_DIR=$L/.git GIT_WORK_TREE=$W/flag GIT_OPTIONAL_LOCKS=0 python3 $S/plans/round75_c2_registry_audit.py --lane $W/flag --mutants --check-stamps $E --work $W/flagfullwork
```

**rc 0**, with `WORKTREE dirty` and:

```text
FLAGS ok n=0
MISMATCH 0
DEFECTS n=0
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
STAMPS files=8 stamped=8 unstamped=0 unresolved=0 not_ancestor=0
PREDICATE R75-C2 pass
```

Executed `python3 $W/flag/plans/tool_doc.py --strict`: **rc 2**, stderr `tool_doc.py: error: unrecognized arguments: --strict`. Thus every frozen C2 numeric/predicate target is printed while its S250 entry-flag promise fails. C2 lines 76–78 search keyword values as if they were option strings. This is a fixable calibration defect, not a necessary tradeoff in static parsing.

**Attribution attack.** Ran real `c2.mutate(S,W/'attribution')`; M1 actually returned:

```text
('M1-entry-absent', ':entry:script-absent:', ['SCRIPT-MISSING plans/nonexistent.py', '`tool-m`:entry:script-absent:plans/nonexistent.py'])
```

Replaced only M1's observed defects in memory with `['`unrelated-tool`:entry:script-absent:plans/unrelated.py']`, leaving the other eight real arms and measured null unchanged. Evaluated exactly the shipped expression `[n for n, exp, defs in results if exp in ' '.join(defs)]` (cell completed successfully). It still derived:

```text
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
```

This is a metric-seam injection, not a claim that an unmodified evaluator spontaneously emitted the replacement finding. It establishes the precise bound: attribution is to a defect-category substring, not the complete finding identity (row/path/flag). The frozen off-target control changes category and therefore cannot catch same-category/wrong-entity attribution.

**Kill-rule adequacy and receipt evidence.** Created one receipt containing only `LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd`, with no WORKTREE line. Executed `c2.check_stamps(L, W/'stamp-only', 'master')`: returned `defects=[]` and `STAMPS files=1 stamped=1 unstamped=0 unresolved=0 not_ancestor=0`. Single missed line: `WORKTREE clean`/`WORKTREE dirty` (the required WORKTREE field altogether). A stamp is not checked for that field. Separately, the normal full C2 command over the export's absent receipts printed `STAMPS files=0 stamped=0 unstamped=0 unresolved=0 not_ancestor=0`, `PREDICATE R75-C2 pass`, **rc 0**. The sentence explicitly requires K>0; the literal kill rule does not reject an empty receipt universe. These are observed fail-open cases, not proof that receipts of record lack WORKTREE.

**Smallest safe correction.** Read option strings only from positional string arguments to `add_argument`, not help/default/metavar keyword values. Track occurrence of `add_argument` independently of whether any long option was found. Compare structured/full expected identities (including row/path/flag) and add a same-category/wrong-entity reject arm. Require K>0 and the required WORKTREE field; enforce known measured-tip resolution rather than accepting an unknown tip. Keep declared universes/targets frozen. The canonical judge must decide whether category attribution satisfies the frozen wording; do not upgrade the evidence to full identity attribution.

## Causal separability

* **C2 without C1 repair:** with the untouched A1 export, ran `GIT_DIR=$L/.git GIT_WORK_TREE=$S GIT_OPTIONAL_LOCKS=0 python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps $E --work $W/separatework`: **rc 0**, `WORKTREE clean`, `MISMATCH 0`, `DEFECTS n=0`, exact 9/9 mutant target, `STAMPS files=8 stamped=8 ...`, `PREDICATE R75-C2 pass`. On those A1 corpus bytes, C1 baseline command below fails. C2 is causally separable.
* **C1 without C2 validity:** with the token-only scratch README, overwrote scratch SKILL.md with `deliberately invalid registry\n`; `python3 plans/round75_c1_index_parity.py --lane .` still printed all three exact target universe lines and pass, **rc 0**. C1 never reads SKILL.md or invokes C2. This demonstrates census separability, not clean provenance; the fixture has no git metadata.

## Do-nothing controls and positive batteries

* **Unrepaired A1 corpus:** `python3 plans/round75_c1_index_parity.py --lane .`, **rc 1**, knowledge 74/71 missing=3, lessons 123/87 missing=36, evidence 66/46 missing=20; 59 missing surfaces and predicate fail. Below C1 target.
* **Frozen C1 cheapest-skip control:** `python3 plans/round75_c1_index_parity.py --lane $L --control-rowshuffle --work $W/controls`, **rc 0** as a successful control experiment, not a successful coverage predicate. Printed `NAIVE rows=6 surfaces=6 equal=True`, knowledge missing=1, lessons missing=2, evidence missing=1 (four named defects), `PREDICATE R75-C1-control pass`. Below coverage target.
* **Frozen C2 off-target control:** `python3 plans/round75_c2_registry_audit.py --lane $L --control-attribute --work $W/controls`, **rc 0** as a successful discrimination experiment. Printed `R74-METRIC killed=10/10 (any-defect counting)`, `R75-METRIC expected_matched=9/10 wrong_id=1`, `NULL-ARM defects=0`, control pass. Below target by wrong_id=1, despite numerator 9 matching the target numerator. Do not compare numerators alone.
* **Do nothing after A1:** full C2 command on untouched A1 already reaches the target, as measured in separability above. It is **not below target**. This does not refute the pre-A1 implementation change; it means the wave's A1 baseline already contains C2's work and cannot supply new marginal calibration gain by itself.
* `python3 plans/round75_c1_index_parity.py --lane $L --selftest --work $W/controls`: **rc 0**, `SELFTEST cases=5 red=4 failures=0 ok=True`.
* `python3 plans/round75_c2_registry_audit.py --lane $L --selftest --work $W/controls`: **rc 0**, `SELFTEST arms=4 failures=0 ok=True`. Existing selftests passing do not exercise the discovered hidden-comment, help-keyword, same-category identity, or missing-WORKTREE cases.

## Handoff

Production files intentionally unchanged. Recommendations: C1 CHALLENGE for invisible-token index credit; C2 CHALLENGE for actual rejected option passing all target counters, with attribution and receipt-validation limitations separately evidenced. No tools installed or upgraded. Scratch removal is completed before the terminal return; no fixture artifacts are deliverables.

Self-review: accuracy 4/5 (explicitly separates archive numeric tests from clean provenance); completeness 4/5 (canonical judge not invoked, as required); clarity 4/5 (commands use defined path abbreviations); actionability 5/5 (each defect has a bounded correction and concrete fixture); conciseness 4/5 (multiple independent obligations require a longer report). Mean 4.2/5. Highest-impact improvement is integration-owner execution of the proposed reject cases without changing the frozen contract.
