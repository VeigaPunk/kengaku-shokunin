#!/usr/bin/env python3
"""Render the frozen round-47 v2 wave specification; no seat dispatch or lane edits."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
WAVE_DIR = LANE / '.ufo/waves/round-47'
OUT = WAVE_DIR / 'w1-spec.json'
GODSPEED = '''/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.'''

context = f'''# Goal
kengaku round 47, one v2 build-and-attack wave, lane repo {LANE}. Base lane tip: f139f5213a2c38f75c9932cde27052a8ef857c7f. Routed issues are from {LANE}/corpus/lessons/round-46-verifier-spotcheck.md and the frozen history in {LANE}/SCORECARD.md (round 46 / planned round 47). The L1 owns the canonical planner seat and integrates all results. The round's calibration decision C1 (fixture-fence honest over-refusal versus the frozen held-out kill rule) gates any C1 admission; do not re-label or weaken the prior kill rule after scoring. The round's coverage decision C3 must address round-46 V7 (no violating receipt cases for frozen tags) and V8 (pre-receipt P10 execution). Claims/counters/controls are frozen before scored evaluation; your item MUST NOT run scoring data until a committed round-47 preregistration tells you the freeze is landed. If no committed freeze is present when you start, report that blocker and do no scoring. Use only a unique scratch directory /fast/scratch/hyaku/kengaku-r47/<SeatName>/, set TMPDIR explicitly, remove it on exit; no `/tmp` evidence. No tool installs are planned; if one becomes necessary read /home/vgpnk/.omp/agent/RULES.md first, pacman transactions remain paused, and record any install. Source corpus /home/vgpnk/Projects/shokuknow is read-only; considerthese input is read-only. Write only your individual report and receipts beneath {LANE}/.ufo/waves/round-47/w1/<SeatName>/, and your scratch directory; never edit production lane files, reports, fleet files, sibling repos, lane Git/JJ state or index, and never run mutating git/jj commands. No subagents/background jobs. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. All paths are absolute. Report counts with exact commands/output; do not invent evidence; end with exactly one VERDICT line.''' 

# Thirty attack seats meet v2's >=25% attack-role requirement. Each attacks a separate
# measurement/control/requirement; the other 34 seats perform distinct bounded recon/build
# tasks that produce candidate evidence for the single integration owner.
items = []
def add(name, role, axis, claim, kind, detail):
    scratch = f'/fast/scratch/hyaku/kengaku-r47/{name}'
    report = f'{LANE}/.ufo/waves/round-47/w1/{name}.md'
    item = f'''{GODSPEED}

# Target
kengaku round 47 seat {name} ({role}), serving {claim} ({axis}).
# Item
{detail}
# Evidence and boundaries
Read the full frozen claim file {LANE}/plans/round-47-claims.md and round-46 closure {LANE}/corpus/lessons/round-46-verifier-spotcheck.md first. Do only this named item. Before any scored counter/probe execution, verify the freeze exists in the committed lane tree and predates the measurement; otherwise make no scored run and state the blocker. Work read-only against a clone at the frozen base, except scratch-only candidate code and your own report/receipt. Do not edit production files, do not share writer paths, and do not claim C1/C3 admission. Unique scratch: {scratch}; mkdir it, export TMPDIR={scratch}, trap cleanup; any fixture Git call uses `git -C "$D"` with D inside that scratch and verify its top-level before writes. Report path: {report}. Capture exact command, exit and output; keep receipts under that report's sibling directory. Non-author seat outputs remain advisory, not an independent lane verifier.'''
    items.append({'name':name,'role':role,'axes':[axis],'item':item,'milestone':'kengaku r47 C1/C3 frozen claim falsification'})

# C1 calibration: honest controls, over-refusal, held-outs, fence and counter attack surface.
c1 = [
('C1Rerun','reviewer','rerun frozen C1 counter independently on the exact committed baseline and landing candidates; report all fields, exit code and whether named predicate is met.'),
('C1HonestInventory','reviewer','independently enumerate the frozen honest fixture population and verify each refusal/admission against fixture semantics; quantify over-refusal without changing the denominator.'),
('C1Overrefusal','critic','attack the proposed C1 improvement with novel honest repos that resemble the nine r46 refused controls; determine whether the frozen novel-honest leg is representative and whether a do-nothing fence reaches target.'),
('C1HeldOutArgv','critic','attack only argv/path honest-control boundaries: construct distinct benign argv shapes and assess whether the candidate fence refuses them; do not alter the frozen set.'),
('C1HeldOutPaths','critic','attack honest local repositories with unusual but valid directory and symlink layouts; measure only if in the committed frozen population.'),
('C1HeldOutStore','critic','attack ordinary Git metadata cases (linked worktrees, alternates, common-dir) for false refusal; compare the frozen claim boundary.'),
('C1HeldOutConfig','critic','test benign repository configuration diversity against the named fence predicate; distinguish expected refusal from over-refusal.'),
('C1EscapeNames','mutation-tester','mutate a C1 counter/fence fixture name or directory shape in scratch to see whether any result depends on known names; report paired pristine/mutant outcomes.'),
('C1EscapeOrder','mutation-tester','permute the C1 test order and vary deterministic seeds in scratch; detect order or first-match effects that change classified counts.'),
('C1EscapeChannel','mutation-tester','try stdout/exit-status disagreement, missing result and truncated output controls against the C1 measurement contract; report any false green.'),
('C1ReadFence','reviewer','inspect the C1 counter code and identify whether its actual observation covers each advertised fence behavior; map each claim clause to an executable predicate.'),
('C1PredKillRule','critic','apply the frozen r46 held-out kill rule literally to all reported held-out modules; show exact tally and whether C1 is killed independent of headline counter pass.'),
('C1PredCounter','critic','try a keyed or path-keyed fence/control that could pass the frozen C1 counter without enforcing the property; no production edits.'),
('C1MutBoundary','mutation-tester','mutate the boundary that decides whether a path is inside the repository root, including `..`, symlinks and relative paths; record which frozen cases kill each mutation.'),
('C1MutGit','mutation-tester','mutate Git store discovery/common-dir/alternate handling one behavior at a time in scratch; attribute every kill to a concrete case.'),
('C1MutPending','mutation-tester','mutate accounting for blocked, pending or never-returned file access and check whether any control can false-pass.'),
('C1ScoutLiterature','scout','read the lane-local prior C1 materials and identify whether any exact proposed measurement/claim is already contradicted by r46 evidence; return citations, no new factual claims.'),
('C1ScoutSurface','scout','reconstruct the intended fence property from its docstring and r46 claims; identify the smallest honest population required for an over-refusal measurement, with evidence pointers.'),
('C1ExecControl','executor','in an isolated scratch clone, run the frozen no-op/base-fence/keyed controls with only the commands allowed by the committed freeze; report control outputs and clean-up.'),
('C1ExecMatrix','executor','implement in scratch a per-fixture table comparing frozen expected disposition with observed disposition; compute false refusals and leaks separately, without altering the frozen labels.'),
('C1ScribeR46','scribe','draft a concise factual synthesis of the r46 C1 finding: predicate met vs kill rule, 3 held-outs admitted, nine honest refusals, and 2/13 fence mutants caught; cite only the spotcheck lines.'),
('C1ScribeCaveats','scribe','draft exact scope limitations for the proposed r47 C1 result, distinguishing fixture-population performance from universal filesystem safety.'),
('C1ConnectorOverlap','connector','scan only cross-lane ownership overlap for fixture fencing/calibration; cite lane province evidence and propose report-out vs absorb decision.'),
('C1ConnectorCounter','connector','compare C1 measurement boundaries with lane-local existing gate/counter patterns; flag any reused failure mode and evidence path.'),
('C1ReviewerNoHarm','reviewer','identify plausible harm to other axes from C1 fence narrowing, especially security boundary correctness; report exact testable risk and evidence.'),
('C1ReviewerClaim','reviewer','adversarially assess whether a measurable C1 axis claim remains falsifiable and causally separable under the prior kill rule; no claim widening.'),
('C1CritHonestBaseline','critic','try the cheapest do-nothing control against the frozen C1 target; if it reaches the target, show exact counterexample and refuse credit.'),
('C1CritPopulation','critic','test whether any C1 denominator silently excludes the nine novel honest repos or counts duplicated/overlapping fixtures; provide item-level identity evidence.'),
('C1MutCounterPins','mutation-tester','mutate C1 frozen input digests or fixture inventory in scratch; verify the committed counter detects stale/tampered inputs.'),
('C1MutExit','mutation-tester','mutate C1 control exit behavior and output labels in scratch; show whether a counterfeit success is accepted.'),
('C1LabTriage','reviewer','triage the C1 result as PASS/FAIL/INDETERMINATE strictly under the committed frozen sentence and kill rule; state no softened interpretation.'),
]
for n,r,detail in c1:
    add('R47'+n,r,'calibration','C1', 'attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail)

# C3 coverage: repair the two exact routed counter defects, plus grounded source and scope checks.
c3 = [
('C3Rerun','reviewer','rerun the frozen C3 verification counter on the exact committed base and candidate; report checks, defects, predicate and exit.'),
('C3TagInventory','reviewer','enumerate every frozen tag in C3 and map it to a violating receipt case; fail any tag lacking an executable violation, the exact V7 defect.'),
('C3PreReceipt','critic','reconstruct Q30 ordering from committed freeze, execution receipt and commit ancestry; determine whether a pre-receipt control can run P10, the exact V8 defect.'),
('C3PositiveControl','critic','attack whether a positive C3 package/control can be reproduced without actually executing the probe; use a scratch clone and preserve the frozen receipt digest.'),
('C3FillerControl','critic','test whether a committed filler package with plausible rows/entry can clear the frozen C3 admission counter; report exact V1–V13 effects.'),
('C3EchoControl','critic','test whether copying dry-table output into the receipt can satisfy C3; verify the exact committed gate and control outputs.'),
('C3MutTags','mutation-tester','for each C3 requirement tag, remove or invert its corresponding check in a scratch copy and verify a tag-specific violating case kills it.'),
('C3MutOrder','mutation-tester','mutate the probe-order gate to accept a pre-receipt run; verify the frozen controls reject it.'),
('C3MutPins','mutation-tester','tamper with one digest-pinned C3 capture/probe/spec component at a time in scratch; record killed/surviving mutations.'),
('C3MutVerdict','mutation-tester','mutate the C3 predicate output/exit mapping; check false success and false failure behavior against frozen controls.'),
('C3SourceReopen','reviewer','re-open S166 pinned Terminal-Bench `polyglot-c-py` test source this round and verify the cited predicate against the committed capture; include URL, access date, <=25-word located quote.'),
('C3SourceReject','reviewer','re-open one weak or unpinned candidate source cited in the r46 gate and determine whether the rejection reason follows that source; capture URL/date/quote.'),
('C3KnowledgeRead','scout','read the committed C3 knowledge entry and compare each teaching to the pinned capture and its scope limits; record overreach, if any.'),
('C3ScopeBoundary','scout','check C3 entry and province boundary against sibling ownership; distinguish grader interpretation from actual benchmark/runtime/model performance.'),
('C3CounterCode','reviewer','map each C3 counter leg to code and frozen requirement; identify untied or unexercised requirements without proposing post-data changes.'),
('C3CaseCoverage','critic','independently build a tag-by-case matrix from the frozen C3 table; identify tags without violating cases and count them.'),
('C3Sandbox','critic','inspect C3 task probe isolation and host safety boundaries; attempt only scratch-contained bypass controls; report no production execution.'),
('C3ReceiptIntegrity','mutation-tester','modify receipt bytes in scratch while preserving case labels; test digest and output binding in the frozen counter.'),
('C3FixtureName','mutation-tester','rename every C3 fixture/case key in a scratch copy and test whether counter behavior depends on names.'),
('C3DuplicateCase','mutation-tester','duplicate or remove one frozen C3 case and test whether the counter inventory catches count drift.'),
('C3FreshSource','scribe','draft a candidate Gate block recording S166 source URL, current access date, exact located quote <=25 words, plus one rejected candidate and rationale; do not edit lane corpus.'),
('C3LessonGate','scribe','draft round-47 lesson Gate skeleton with one C3 admit candidate and one reject, and explicit verification questions for non-author closure.'),
('C3EntryReview','scribe','draft precise edits needed to repair r46 C3 entry wording after Q10/Q40 review, preserving negative scope and not asserting a pass.'),
('C3READMEReview','scribe','draft a coverage-map/index adjustment proposal for the polyglot grader based only on admitted evidence and exact current counts.'),
('C3ProbePlan','executor','in scratch, prepare a proposed requirement-to-case table that gives each C3 tag a concrete violating case; do not score before the freeze.'),
('C3OrderingPlan','executor','prepare a scratch-only ordering receipt design that makes the first P10 execution provably later than the committed stage-2 receipt.'),
('C3CounterHarness','executor','in a scratch clone, inspect/test counter CLI behavior for base, filler and echo controls after verifying freeze; do not alter production files.'),
('C3SourceRejectOpen','scout','open the Docker Hub task image metadata source cited by the r46 Gate; record what it does and does not establish, URL/date/quote.'),
('C3ConnectorPriorArt','connector','check whether a sibling lane owns task-grader analysis or execution; cite sibling PROVINCE paths and return a scoped ownership finding.'),
('C3ConnectorCrossClaim','connector','scan C1/C3 for hidden shared input or same artifact counter dependencies; identify any failure that would break causal separability.'),
('C3CritDoNothing','critic','evaluate the C3 no-package/do-nothing control against the frozen predicate; if it reaches target, provide exact counter evidence.'),
('C3ReviewerNoHarm','reviewer','identify plausible coverage/quality harm caused by claiming this static grader observation; state the exact falsifiable check.'),
('C3ReviewerAdmission','reviewer','independently adjudicate whether every fixed tag has a violating case and order proof from committed bytes; no self-assessment or conclusion from titles.'),
]
for n,r,detail in c3:
    add('R47'+n,r,'coverage','C3','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail)

assert len(items) == 64, len(items)
attack_roles = {'reviewer','critic','mutation-tester'}
attack = sum(i['role'] in attack_roles for i in items)
assert attack >= 16
spec = {
 'wave':'kengaku-r47-w1',
 'milestone':'kengaku round 47: one v2 wave attacks the routed C1 over-refusal/kill-rule gate and C3 V7/V8, with independent source-grounding and no-harm review',
 'reportDir':'.ufo/waves/round-47/w1',
 'maxLanes':64,
 'axes':['calibration','coverage'],
 'context':context,
 'items':items,
}
WAVE_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
print(f'WROTE {OUT} seats={len(items)} attack={attack} fraction={attack}/{len(items)}')
