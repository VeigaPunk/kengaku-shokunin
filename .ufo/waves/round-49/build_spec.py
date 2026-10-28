#!/usr/bin/env python3
"""Render the frozen round-49 v2 wave specification; no seat dispatch or lane edits."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
WAVE_DIR = LANE / '.ufo/waves/round-49'
OUT = WAVE_DIR / 'w1-spec.json'
FREEZE = '9d2900af41e4d1fc6022eff99010436fde6dbd93'
GODSPEED = '''/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.'''

context = f'''# Goal
kengaku round 49 (hyaku run 10), ONE v2 build-and-attack wave, lane repo {LANE}. Base lane tip (stage-1 freeze): {FREEZE}. The frozen claims live at {LANE}/plans/round-49-claims.md — read it in full first; it binds every seat. Routed issues: {LANE}/corpus/lessons/round-48-verifier-spotcheck.md (routed defects 1-4) and {LANE}/corpus/lessons/round-48.md. The L1 owns the canonical planner seat and is the single integration owner. Two claims: R49-C1 (calibration — fixture-fence honest over-refusal repair under a v3 counter whose honest population, sealed set and MUTANTS floor are frozen before scoring) and R49-C2 (coverage — the round-46 TB2 polyglot-c-py package admitted under a Q40 counter: V7 violating cases for all 7 tags, V8 P10-disabled controls with first-commit ordering, V14 mutation floor, V15 preconditions, probe revision passing --stage-check on this host). Stage-2 fills literals and pins only; stage-3 (C2 only) lands the fresh receipt.

# Routing
Route through the host route table only; the role decides the route. NEVER pass a model, NEVER name or record a model alias in any artifact.

# Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never run pacman -S/-Sy/-Syu/-U/-R.

# Scratch discipline (operator directive 2026-10-25, binding)
Scratch root for this wave: /fast/scratch/hyaku/kengaku-r49/<seat-name>/ (NVMe). mkdir -p it, export TMPDIR there, trap cleanup and REMOVE your scratch dir before you yield (receipts first copied into your wave report dir). /tmp is for files under 50 MB only. One live clone per seat (git clone --shared); never a full mirror of the lane. No committed tool may hardcode /tmp. Anything a report must cite lands in the wave dir or the lane tree — /tmp paths are never citable evidence.

# Write scope and bounds
Seats are READ-ONLY against the lane except: (a) your own report file at the absolute path named in your item (under {LANE}/.ufo/waves/round-49/w1/), and (b) scratch-only candidate code inside your scratch dir (transcribe deliverable code into your report or a sibling file in your wave dir when your item says so). NEVER edit production files (plans/*, corpus/*, SCORECARD.md, LOG.md, etc.), never commit, push, or run a mutating git/jj command anywhere, never touch sibling repos, the fleet repo, MANIFEST.json, .ufo/state, or .scratch/. Do not share writer paths with other seats; the L1 is the only integrator. Every git fixture call uses `git -C "$D"` with D inside your scratch and verifies rev-parse --show-toplevel equals $D before writes.

# Reports
Your item names an absolute report path; the file MUST exist when you yield — a settled seat with no report file is a round-48 routed defect class (record your last state in the file itself if you run out of room). Every Report: trailer path printed by tooling is relative to {LANE} — write it at {LANE}/<that path>. Your report must state: axes named, exact commands run, observed outputs (verbatim where they are evidence), the revision measured (REV line for receipts), limits, and a VERDICT line. A seat that ends with its scratch tree still on disk reports that as a defect of its own.'''

items = []
def add(name, role, axis, claim, kind, detail):
    scratch = f'/fast/scratch/hyaku/kengaku-r49/{name}'
    report = f'{LANE}/.ufo/waves/round-49/w1/{name}.md'
    item = f'''{GODSPEED}

# Target
kengaku round 49 seat {name} ({role}), serving {claim} ({axis}).
# Item
{detail}
# Evidence and boundaries
Read {LANE}/plans/round-49-claims.md and {LANE}/corpus/lessons/round-48-verifier-spotcheck.md first. Do only this named item. Before any scored counter/probe execution, verify the stage-1 freeze exists in the committed lane tree (commit {FREEZE}) and predates the measurement; otherwise make no scored run and state the blocker. Work read-only against a clone at the frozen base, except scratch-only candidate code and your own report/receipt. Do not edit production files, do not claim R49-C1/R49-C2 admission. Unique scratch: {scratch}; mkdir it, export TMPDIR={scratch}, trap cleanup and remove it before you yield; any fixture Git call uses `git -C "$D"` with D inside that scratch and verify its top-level before writes. Report path (MUST exist at yield): {report}. Capture URL, access date and a <=25-word located quote for any source you open.'''
    items.append({'name':name,'role':role,'axes':[axis],'item':item,'milestone':'kengaku r49 C1 fence-overrefusal repair + C2 Q40 counter admission, one v2 wave'})

# ---------------- R49-C1 calibration: fence over-refusal repair + v3 counter + mutation floor ----------------
c1 = [
('C1ExecCounter','executor','build the v3 counter `plans/round49_c1_verify.py` as a scratch candidate per the frozen contract: reuse the round-48 v2 candidate at {LANE}/.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py (rename predicate to R49-C1, paths honest49/sealed49) and add the frozen MUTANTS leg: read plans/mutants49/c1-mutants.json (payload+digest+description), apply each mutant to a copy of the landed fence, re-measure the three legs on that copy, caught iff the clean signature breaks; print `MUTANTS total=<M> caught=<k> floor=<M>/2 verdict=met|unmet` before CALIBRATION. Selftest on scratch clones of base; never run scored on claimed work. Transcribe the full counter source into a sibling file {LANE}/.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py.'),
('C1ExecFenceA','executor','fence repair variant A as a scratch candidate: apply the §7 unified diff in {LANE}/.ufo/waves/round-48/w1/R48C1ExecFenceA.md to plans/fixture_fence.py @ {F} and re-verify the candidate sha256 `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` or report the drift; then run the 120-fixture honest48 population (modules at {LANE}/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/) + 20 refusals46 + 12 sealed46 in a dev harness reusing plans/round46_c1_verify.py builders/strace envelope; per-leg rollups only, no predicate. Transcribe the fence to {LANE}/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py.'),
('C1ExecFenceB','executor','fence repair variant B (a different mechanism, e.g. store-shape proof extended with ref-kind classification instead of allowlist widening) meeting the same frozen predicate; dev-harness receipts per leg on a scratch clone; do not read variant A. Transcribe the fence to {LANE}/.ufo/waves/round-49/w1/R49C1ExecFenceB/fence_b.py.'),
('C1ExecHonest','executor','produce the frozen honest population for stage 2: copy the 16 r48 novel modules ({LANE}/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/) plus author 4 NEW novel honest classes (n17-n20) ordinary `git init` repos can have and the r48 set lacks (e.g. replace refs, shallow partial clone state, core.hooksPath unset default with a non-sample hook file absent, worktree with a .git file — refuse that last one if it must fail); run build_honest_population.py determinism twice; emit population.txt+population.sha256+modules.sha256+identity.jsonl for the full tree-shaped `plans/honest49/` layout into {LANE}/.ufo/waves/round-49/w1/R49C1ExecHonest/.'),
('C1ExecControls','executor','run the six frozen C1 controls against the counter candidate on scratch trees: no fence; base fence @3a548330; round-45 keyed fence; admit-all; refuse-all; name-keyed variant. Each control must print PREDICATE R49-C1 fail; transcribe REV-prefixed receipts into {LANE}/.ufo/waves/round-49/w1/R49C1ExecControls/receipts/. Controls run only on base/control trees, never on claimed work.'),
('C1ScribeSynth','scribe','draft a concise factual synthesis of the r45->r49 C1 history (keyed-control pass; kill-rule firing; measured 8/120 base refusal; unreproducible r46 9/9; 2/13 mutants; round-48 no-landing) with evidence pointers only; no new factual claims.'),
('C1ScribeLimit','scribe','draft exact scope limitations for the r49 C1 result: fixture-population performance vs universal filesystem safety; named limits only.'),
('C1ConnOverlap','connector','scan sibling lanes for fixture-fencing/calibration ownership overlap; cite PROVINCE paths; propose report-out vs absorb per item.'),
('C1ConnPattern','connector','compare the C1 v3 counter measurement boundary with lane-local gate/counter patterns (grader.py, pkg_gate.py, anchor_line_check.py); flag any reused failure mode with evidence path.'),
('C1ScoutPop','scout','survey additional ordinary `git init` states the frozen 120-fixture population lacks (e.g. git stash entries, .gitmodules, replace refs, grafts, shallow files, describe names, core.* keys a fresh init on this host writes); rank each by whether a plain-init fence should admit it, with git-doc evidence.'),
# ---- attack ----
('C1Rerun','reviewer','rerun the v3 counter candidate independently on the exact committed base and on each submitted fence variant; report all fields, exit code, predicate line.'),
('C1HonestInv','reviewer','independently enumerate the frozen honest population (104 battery + 16 r48 + new r49 classes) and verify each admission expectation against fixture semantics; quantify over-refusal without changing the denominator.'),
('C1Overrefusal','critic','author novel honest repos beyond the frozen set (replace refs, shallow clone, packed-refs with peeled tags, stash, .gitmodules); determine whether the novel-honest leg is representative and whether a do-nothing fence reaches target.'),
('C1HoArgv','critic','benign argv shape probes (dot-dot normalizing inside d, env tokens, option order); each must be BENIGN-ADMIT with touches=0 or expose a real gap.'),
('C1HoPaths','critic','benign repository directory/symlink layouts (nested repos, symlinked worktree files inside d); measure disposition only.'),
('C1HoStore','critic','benign git metadata cases: linked worktrees, alternates, common-dir used honestly inside d; distinguish expected refusal from over-refusal per the frozen predicate.'),
('C1HoConfig','critic','benign config diversity (extra [core] keys, [user], [init] defaults, remote/branch sections); expected disposition per the frozen classification.'),
('C1HoMount','critic','construct the honest mount-boundary fixture from w2/R46W2C1Intent.md (store on a mount point inside d); the landed fence must admit it iff every byte it reads is inside d.'),
('C1MutNames','mutation-tester','mutate fixture/build/module names and directory shapes in scratch; report paired pristine/mutant outcomes; detect any dependence on known names (Q39).'),
('C1MutOrder','mutation-tester','permute test order and vary deterministic seeds in scratch; detect order/first-match effects that change classified counts.'),
('C1MutBoundary','mutation-tester','mutate the inside-d boundary decision (.., symlinks, relative paths); record which frozen case kills each mutation.'),
('C1MutGit','mutation-tester','mutate git store discovery/common-dir/alternates handling one behavior at a time in scratch; attribute every kill to a concrete case.'),
('C1MutPending','mutation-tester','mutate accounting for blocked/pending/never-returned file access; check whether any control can false-pass.'),
('C1MutCounterPins','mutation-tester','mutate C1 frozen input digests or fixture inventory in scratch; verify the committed counter detects stale/tampered inputs.'),
('C1MutExit','mutation-tester','mutate control exit behavior and output labels in scratch; show whether a counterfeit success is accepted.'),
('C1MutBattery','mutation-tester','author >=14 candidate fence mutants for plans/mutants49/c1-mutants.json against the R48C1ExecFenceA candidate (apply the §7 diff yourself): each payload a real byte mutation of the fence that a lax counter would miss (weaken a check, reorder, delete a leg, flip a comparison); JSON rows payload+digest+expected-effect; verify each applies cleanly in scratch.'),
('C1PredCounter','critic','try a keyed or path-keyed fence/control that could pass the frozen v3 counter without enforcing the property; no production edits.'),
('C1CritBase','critic','run the cheapest do-nothing control against the frozen C1 target; if it reaches target, show the exact counterexample and state refusal of credit.'),
('C1CritPop','critic','test whether the C1 honest denominator silently excludes any refused class or counts duplicated/overlapping fixtures; item-level identity evidence.'),
('C1RevNoHarm','reviewer','identify plausible harm to other axes from the fence repair, especially security-boundary correctness (a wider allowlist leaking a sealed module); exact testable risk + evidence.'),
('C1RevClaim','reviewer','adversarially assess whether the C1 claim remains falsifiable and causally separable under the frozen kill rule incl. the MUTANTS floor; no claim widening; flag any dependence on C2 artifacts.'),
]
for n,r,detail in c1:
    add('R49'+n,r,'calibration','R49-C1','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail.replace('{F}',FREEZE).replace('{LANE}',str(LANE)))

# ---------------- R49-C2 coverage: TB2 polyglot-c-py admission under Q40 counter ----------------
c2 = [
('C2ExecCounter','executor','build the v4 counter `plans/round49_c2_verify.py` as a scratch candidate: start from the round-48 candidate verbatim in {LANE}/.ufo/waves/round-48/w1/R48C2ExecCounter.md Appendix A (lines 419+), rename predicate to R49-C2, repoint DRY_REL to corpus/evidence/round49/polyglot-c-py-dry-cases.txt, CLAIMS_REL to plans/round-49-claims.md, MUT_PLAN_REL to plans/mutants49/plan.json, SPEC_REL to plans/pkg-spec-r49.json, and replace the V8 inherited-receipt rule with the frozen ordering rule: receipt first-commit == the stage-3 commit which must be a descendant of the stage-2 commit (via git log), receipt carries CASE ... observed= lines. Selftest --dry on scratch clones; never run scored. Transcribe to {LANE}/.ufo/waves/round-49/w1/R49C2ExecCounter/candidate.py.'),
('C2ExecProbe','executor','repair the hardened probe `22b7779e` ({LANE}/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py) as a scratch candidate `plans/polyglot_c_py_probe.py` v2: (i) make the mode="all" grade path run seed+recipe (the round-48 measured defect: guard `mode in ("stage","recipe")` excludes "all"); (ii) fix the `prlimit --nproc=48` failure under this host uid thread load (~1100 threads) — raise the ceiling or drop it with rationale; keep every other hardening. Controls: (a) `22b7779e` --stage-check fail receipt on this host, (b) v2 --stage-check PASS receipt on this host, (c) a stub-grader mode-all run proving seed/recipe execute. No full package run. Transcribe the probe to {LANE}/.ufo/waves/round-49/w1/R49C2ExecProbe/probe_v2.py.'),
('C2ExecCases','executor','author the amended case table so `both-print` and `toolchain` each carry >=1 committed violating case (add or re-word cases, never re-word the 7 tag names): `both-print` — a polyglot that prints under python3 but whose C side prints nothing (still compiles/returns correct exit); `toolchain` — a case that works only because host gcc/python3 are not the documented 13.2.0/3.12.3 (e.g. relying on a post-13.2 gcc diagnostic or a post-3.12 python feature), predicted to fail the documented toolchain contract. Extend the probe CASES in a scratch copy, run `--dry` to print the amended table, verify all 7 tags covered; transcribe the CASES diff + new dry table to {LANE}/.ufo/waves/round-49/w1/R49C2ExecCases/.'),
('C2ExecControls','executor','exercise the three frozen C2 controls against the counter candidate on scratch trees with P10 disabled: base tree (no plans/polyglot_c_py_probe.py); filler package; echo receipt. Each must produce `PREDICATE R49-C2 fail` receipts; verify `plans/order_check.py` passes each receipt; transcribe receipts to {LANE}/.ufo/waves/round-49/w1/R49C2ExecControls/receipts/.'),
('C2ExecMutBattery','executor','author >=14 fresh mutants of committed package bytes for plans/mutants49/plan.json (payload path + digest + target per mutant; targets: capture, entry, receipt, dry table, spec, probe) and measure each on a symlink-mirror copy: record which substantive leg (V3/V4/V7/V9/V10/V12) flips to DEFECT; require >= N/2 caught. Emit plan.json + payloads to {LANE}/.ufo/waves/round-49/w1/R49C2ExecMutBattery/.'),
('C2ExecSpec','executor','draft `plans/pkg-spec-r49.json` (r46 spec minus stale pins, plus slots for probe-v2 digest, new dry-table digest, new receipt path/digest filled at stage 3) and the P10-disabled gate wrapper `plans/pkg_gate_pre_receipt.py` per the design in {LANE}/.ufo/waves/round-48/w1/R48C2ExecProbe.md §2 (never pass --rerun; sentinel probe_cmd; assert no P10 line; assert gate digest). Transcribe both to {LANE}/.ufo/waves/round-49/w1/R49C2ExecSpec/.'),
('C2ScribeGate','scribe','draft the round-49 lesson Gate block: S166 reopened by the L1 on 2026-10-28 at the pinned raw URL (sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec, byte-equal to the committed capture; quote `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` at line 27) + one reject candidate for this round (reopen one lead from SOURCES.md Leads and reject with reason or admit). Do not edit lane corpus.'),
('C2ScribeEntry','scribe','draft the requirement-map repairs to corpus/knowledge/tb2-polyglot-c-py-grader.md: the two `not exercised` rows for both-print/toolchain become canonical-shape rows (4 cells: instruction line, tag, derived label, citing cases) once the new cases land; also draft the entry paragraphs naming the probe-receipt move to round49. No pass assertion; preserve negative scope.'),
('C2ConnPrior','connector','check whether any sibling lane owns task-grader analysis/execution; cite sibling PROVINCE paths; return a scoped ownership finding.'),
('C2ConnCross','connector','scan R49-C1 and R49-C2 for hidden shared inputs or counter dependencies that would break causal separability; name each with evidence.'),
('C2ScoutEntry','scout','read the committed polyglot knowledge entry and compare each teaching to the pinned capture and its scope limits; record overreach, if any.'),
# ---- attack ----
('C2Rerun','reviewer','rerun the v4 counter candidate independently on the exact committed base and on the staged candidate tree; report checks, defects, predicate, exit.'),
('C2TagInv','reviewer','enumerate every frozen tag and map it to its violating case in the amended dry table/receipt; fail any tag lacking an executable violation (the V7 defect class).'),
('C2PreReceipt','critic','attack the frozen ordering: can a receipt be committed that satisfies "first-commit == stage-3 descendant of stage-2" yet was produced before stage-2, forged, or copied from the dry table? Show the strongest bypass and the check that kills it.'),
('C2PosControl','critic','attack whether a positive package/control can pass without actually executing the probe; scratch clone; preserve the frozen receipt digest.'),
('C2Filler','critic','test whether a committed filler package with plausible rows/entry can clear the v4 counter; report exact V1-V15 effects.'),
('C2Echo','critic','test whether copying dry-table output into the receipt satisfies the v4 counter; verify the exact committed gate and control outputs.'),
('C2MutTags','mutation-tester','for each requirement tag, remove or invert its check in a scratch copy and verify a tag-specific violating case kills it.'),
('C2MutOrder','mutation-tester','mutate the probe-order gate to accept a pre-receipt run; verify the frozen controls reject it.'),
('C2MutPins','mutation-tester','tamper with one digest-pinned component at a time (capture/probe/spec/receipt/dry table) in scratch; record killed/surviving.'),
('C2MutVerdict','mutation-tester','mutate the predicate output/exit mapping; check false success and false failure against frozen controls.'),
('C2MutReceipt','mutation-tester','modify receipt bytes in scratch while preserving case labels; test digest and output binding in the frozen counter.'),
('C2MutDup','mutation-tester','duplicate or remove one frozen case; test whether the counter inventory catches count drift.'),
('C2SourceReopen','reviewer','re-open S166 (pinned test_outputs.py) this round and verify the cited predicate against the committed capture; record URL, access date, <=25-word located quote.'),
('C2Scope','scout','check the entry and PROVINCE boundary against sibling ownership; distinguish grader interpretation from benchmark/runtime/model performance.'),
('C2CritDoNothing','critic','evaluate the C2 no-package/do-nothing control against the frozen predicate; if it reaches target, provide exact counter evidence.'),
('C2RevAdmission','reviewer','independently adjudicate whether every frozen tag has a violating case and the order proof holds from committed bytes; no conclusion from titles.'),
('C2RevNoHarm','reviewer','identify plausible coverage/quality harm from admitting this static grader observation; state the exact falsifiable check.'),
('C2Sandbox','critic','inspect the probe isolation and host-safety boundaries; attempt only scratch-contained bypass controls; no production execution.'),
]
for n,r,detail in c2:
    add('R49'+n,r,'coverage','R49-C2','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail.replace('{F}',FREEZE).replace('{LANE}',str(LANE)))

# ---------------- cross-cutting ----------------
cross = [
('SentHygiene','sentinel','audit the whole wave for boundary violations: outside writes, secrets, /tmp citation, fleet-repo touches, shared writer paths; one report with per-seat disposition.'),
('RevReport','reviewer','pre-check the round report structure against the frozen report contract (sections, evidence pointers, SHONEN boxes, census command); list defects to fix before filing.'),
('RevengerOverlap','revenger','reverse-engineer the C1 and C2 attack surfaces across all items; flag any measurement attacked twice without need, and any frozen leg no seat attacks.'),
('RevClosure','reviewer','closure-prep adversarial review: take the frozen predicates and kill rules literally; write the strongest non-author rejection case for each claim and whether the landing evidence answers it.'),
]
for n,r,detail in cross:
    add('R49'+n,r,'calibration+coverage','R49-C1+R49-C2','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail.replace('{F}',FREEZE).replace('{LANE}',str(LANE)))

assert len(items) == 64, len(items)
attack_roles = {'reviewer','critic','mutation-tester'}
attack = sum(i['role'] in attack_roles for i in items)
assert attack >= 16, attack
spec = {
 'wave': 'kengaku-r49-w1',
 'milestone': 'kengaku round 49: one v2 wave builds and attacks the R49-C1 fence-overrefusal v3 counter (with committed mutant floor) and the R49-C2 Q40 grader-admission counter (V7 cases, V8 receipt ordering, V14 battery, probe stage-check repair)',
 'reportDir': '.ufo/waves/round-49/w1',
 'maxLanes': 64,
 'axes': ['calibration', 'coverage'],
 'context': context,
 'items': items,
}
WAVE_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
print(f'wrote {OUT} items={len(items)} attack={attack}')
print('roles:', sorted({i["role"] for i in items}))
