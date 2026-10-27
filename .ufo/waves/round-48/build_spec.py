#!/usr/bin/env python3
"""Render the frozen round-48 v2 wave specification; no seat dispatch or lane edits."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
WAVE_DIR = LANE / '.ufo/waves/round-48'
OUT = WAVE_DIR / 'w1-spec.json'
GODSPEED = '''/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.'''

context = f'''# Goal
kengaku round 48 (hyaku run 10), ONE v2 build-and-attack wave, lane repo {LANE}. Base lane tip (stage-1 freeze): a543d92083557dd9b33ee674e9b99b03411f80af. The frozen claims live at {LANE}/plans/round-48-claims.md — read it in full first; it binds every seat. Routed issues are from {LANE}/corpus/lessons/round-46-verifier-spotcheck.md and SCORECARD.md (round 46 wave-2 verdicts + planned round 47). The L1 owns the canonical planner seat and is the single integration owner. Two claims: R48-C1 (calibration — fixture-fence honest over-refusal repair under a v3 counter whose honest population is frozen before scoring and whose kill rule keys on traced outside access) and R48-C2 (coverage — the round-46 TB2 polyglot-c-py package admitted under a Q40 re-frozen counter: every frozen tag violated by a committed case, P10-disabled pre-receipt controls, mutation floor). Claims/counters/controls are frozen before scored evaluation; your item MUST NOT run scored counter/probe executions on claimed work — before any scored run, verify the freeze exists in the committed lane tree and predates the measurement; otherwise make no scored run and state the blocker. C2 ordering: NO full probe run before stage 2; only --dry/stage-check. Do not re-freeze, weaken, or re-label any predicate, kill rule or control after any seat has scored.

# Routing and roles
Route through the host route table only (task @m_kfc; main/planner @m_opus; executor @m_mim; critic/scout/reviewer/mutation-tester @m_kfc; security-reviewer @m_zfl; scribe/sonic/simplifier/revenger/labrat/sentinel @m_flash; connector @m_antigravity; distiller/seance @m_haiku). NEVER pass a model. A seat keeps the route chain it captured at spawn.

# Tooling authorization (operator, 2026-10-19): you and every seat may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never run pacman -S/-Sy/-Syu/-U/-R.

# Scratch discipline (operator directive 2026-10-25, binding)
Scratch root for this wave: /fast/scratch/hyaku/kengaku-r48/<seat-name>/ (NVMe). mkdir -p it, export TMPDIR there, trap cleanup and REMOVE your scratch dir before you yield (receipts first copied into your wave report dir). /tmp is for files under 50 MB only. One live clone per seat (git clone --shared); never a full mirror of the lane. No committed tool may hardcode /tmp. Anything a report must cite lands in the wave dir or the lane tree — /tmp paths are never citable evidence.

# Write scope and bounds
Seats are READ-ONLY against the lane except: (a) your own report file at the path named in your item (absolute, under {LANE}/.ufo/waves/round-48/w1/), and (b) scratch-only candidate code inside your scratch dir. NEVER edit production files (plans/*, corpus/*, SCORECARD.md, LOG.md, etc.), never commit, push, or run a mutating git/jj command anywhere, never touch sibling repos, the fleet repo, MANIFEST.json, .ufo/state, or .scratch/. Do not share writer paths with other seats; the L1 is the only integrator. Every git fixture call uses `git -C "$D"` with D inside your scratch and verifies rev-parse --show-toplevel equals $D before writes.

# Reports
Every Report: trailer path printed by tooling is relative to {LANE} — write your report at {LANE}/<that path> (absolute). Your report must state: axes named, exact commands run, observed outputs (verbatim where they are evidence), the revision measured (REV line for receipts), limits, and a VERDICT line. A seat that ends with its scratch tree still on disk reports that as a defect of its own.'''

items = []
def add(name, role, axis, claim, kind, detail):
    scratch = f'/fast/scratch/hyaku/kengaku-r48/{name}'
    report = f'{LANE}/.ufo/waves/round-48/w1/{name}.md'
    item = f'''{GODSPEED}

# Target
kengaku round 48 seat {name} ({role}), serving {claim} ({axis}).
# Item
{detail}
# Evidence and boundaries
Read {LANE}/plans/round-48-claims.md and {LANE}/corpus/lessons/round-46-verifier-spotcheck.md first. Do only this named item. Before any scored counter/probe execution, verify the freeze exists in the committed lane tree (stage-1 commit a543d920) and predates the measurement; otherwise make no scored run and state the blocker. Work read-only against a clone at the frozen base, except scratch-only candidate code and your own report/receipt. Do not edit production files, do not claim R48-C1/R48-C2 admission. Unique scratch: {scratch}; mkdir it, export TMPDIR={scratch}, trap cleanup; any fixture Git call uses `git -C "$D"` with D inside that scratch and verify its top-level before writes. Report path: {report}. Capture URL, access date and a <=25-word located quote for every source you open.'''
    items.append({'name':name,'role':role,'axes':[axis],'item':item,'milestone':'kengaku r48 C1 fence-overrefusal repair + C2 Q40 counter admission, one v2 wave'})

# ---------------- R48-C1 calibration: fence over-refusal repair + v3 counter ----------------
c1 = [
# build
('C1ExecCounter','executor','build the v3 counter `plans/round48_c1_verify.py` as a scratch candidate per the frozen contract: import plans/round46_c1_verify.py digest-pinned; add honest-population leg frozen at stage 2 (104 battery fixtures + 9 r46 novel classes + authored classes); BENIGN-ADMIT classification for touches=0 admissions; REV-prefixed receipts; keep Q39 name-hiding and the B1/B3/B4/B5/B6 envelope legs. Selftest it on scratch clones of base and landing candidates; never run it scored on claimed work.'),
('C1ExecFenceA','executor','fence repair variant A as a scratch candidate: extend the round-46 allowlist classification so the 9 r46 novel honest classes (packed refs, annotated tags, detached HEAD, merge commit, .gitignore, 30-commit linear, reflog gc, annotated+detached, ignored untracked) are admitted, while all 20 refusals46 + 12 sealed46 modules remain refused with zero traced outside access. Honour the w2/R46W2C1Intent mount-point boundary. Receipts per fixture on a scratch clone.'),
('C1ExecFenceB','executor','fence repair variant B (a different mechanism of your design, e.g. store-shape proof extended with ref-kind classification instead of entry-name allowlist widening) meeting the same frozen predicate; receipts per fixture; you must not read variant A.'),
('C1ExecHonest','executor','build the frozen honest battery builder: rebuild the 104 battery42/43/44 fixtures, rebuild the 9 r46 novel classes from their w2 report descriptions, and author 6+ NEW novel honest classes ordinary `git init` repos can have (not in the r46 set); per-fixture build script + identity receipt. Freeze the population list with digests; author against the BASE fence description only.'),
('C1ExecControls','executor','run the six frozen C1 controls on scratch trees: no fence; base fence @0f77f9b; round-45 keyed fence; admit-all; refuse-all; name-keyed variant. Each control must print PREDICATE R48-C1 fail; capture REV-prefixed receipts. Controls run only on base/control trees, never on claimed work.'),
('C1ScribeSynth','scribe','draft a concise factual synthesis of the r45->r48 C1 history (keyed-control pass; kill-rule firing on 3 benign held-outs; 9/9 honest refusals; 2/13 mutants) with evidence pointers only; no new factual claims.'),
('C1ScribeLimit','scribe','draft exact scope limitations for the r48 C1 result: fixture-population performance vs universal filesystem safety; named limits only.'),
('C1ConnOverlap','connector','scan sibling lanes for fixture-fencing/calibration ownership overlap; cite PROVINCE paths; propose report-out vs absorb per item.'),
('C1ConnPattern','connector','compare the C1 v3 counter measurement boundary with lane-local gate/counter patterns (grader.py, pkg_gate.py, drift-pins); flag any reused failure mode with evidence path.'),
('C1ScoutPop','scout','derive the smallest honest population that makes the over-refusal measurement falsifiable: which of the 9+6 classes are necessary vs redundant, with per-class evidence pointers from the w2 reports.'),
# attack
('C1Rerun','reviewer','rerun the frozen C1 v3 counter independently on the exact committed base and on each candidate fence variant; report all fields, exit code, predicate line.'),
('C1HonestInv','reviewer','independently enumerate the frozen honest population and verify each refusal/admission against fixture semantics; quantify over-refusal without changing the denominator.'),
('C1Overrefusal','critic','author novel honest repos beyond the frozen set (e.g. submodule-free exports, replace refs, shallow clones, packed-refs with peeled tags); determine whether the frozen novel-honest leg is representative and whether a do-nothing fence reaches target.'),
('C1HoArgv','critic','benign argv shape probes (dot-dot that normalizes inside d, env tokens, option order); each must be BENIGN-ADMIT with touches=0 or expose a real gap.'),
('C1HoPaths','critic','benign repository directory/symlink layouts (nested repos, symlinked worktree files inside d); measure disposition only.'),
('C1HoStore','critic','benign git metadata cases: linked worktrees, alternates, common-dir used honestly inside d; distinguish expected refusal from over-refusal per the frozen predicate.'),
('C1HoConfig','critic','benign config diversity (extra [core] keys, [user], [init] defaults); expected disposition per the frozen classification.'),
('C1HoMount','critic','construct the honest mount-boundary fixture from w2/R46W2C1Intent.md (store on a mount point inside d); the landed fence must admit it iff every byte it reads is inside d.'),
('C1MutNames','mutation-tester','mutate fixture/build/module names and directory shapes in scratch; report paired pristine/mutant outcomes; detect any dependence on known names (Q39).'),
('C1MutOrder','mutation-tester','permute test order and vary deterministic seeds in scratch; detect order/first-match effects that change classified counts.'),
('C1MutBoundary','mutation-tester','mutate the inside-d boundary decision (.., symlinks, relative paths); record which frozen case kills each mutation.'),
('C1MutGit','mutation-tester','mutate git store discovery/common-dir/alternates handling one behavior at a time in scratch; attribute every kill to a concrete case.'),
('C1MutPending','mutation-tester','mutate accounting for blocked/pending/never-returned file access; check whether any control can false-pass.'),
('C1MutCounterPins','mutation-tester','mutate C1 frozen input digests or fixture inventory in scratch; verify the committed counter detects stale/tampered inputs.'),
('C1MutExit','mutation-tester','mutate control exit behavior and output labels in scratch; show whether a counterfeit success is accepted.'),
('C1PredCounter','critic','try a keyed or path-keyed fence/control that could pass the frozen v3 counter without enforcing the property; no production edits.'),
('C1CritBase','critic','run the cheapest do-nothing control against the frozen C1 target; if it reaches target, show the exact counterexample and state refusal of credit.'),
('C1CritPop','critic','test whether the C1 honest denominator silently excludes any refused class or counts duplicated/overlapping fixtures; item-level identity evidence.'),
('C1RevNoHarm','reviewer','identify plausible harm to other axes from the fence repair, especially security-boundary correctness (a wider allowlist leaking a sealed module); exact testable risk + evidence.'),
('C1RevClaim','reviewer','adversarially assess whether the C1 claim remains falsifiable and causally separable under the frozen kill rule; no claim widening; flag any dependence on C2 artifacts.'),
]
for n,r,detail in c1:
    add('R48'+n,r,'calibration','R48-C1','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail)

# ---------------- R48-C2 coverage: TB2 polyglot-c-py admission under Q40 counter ----------------
c2 = [
# build
('C2ExecCounter','executor','build the v4 counter `plans/round48_c2_verify.py` as a scratch candidate per the frozen contract: import plans/round46_c3_verify.py digest-pinned; V7 positive precondition check (every frozen tag cited by a committed violates= case; requirement-map rows parse); V8 pre-receipt controls run the gate with P10 disabled; V15 preconditions dry-run; V14 mutation battery leg with frozen floor. Selftest on scratch clones; never run scored on claimed work.'),
('C2ExecProbe','executor','integrate the hardened probe from .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py (sha256 22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d) VERBATIM as a scratch candidate for plans/polyglot_c_py_probe.py; verify the digest; design the P10-disabled gate mode (pkg_gate.py flag or wrapper) as a scratch candidate; stage-check only, NO full probe run.'),
('C2ExecCases','executor','amend the frozen 18-case table so both-print and toolchain each carry a committed violating case (add or re-word cases, never re-word tags); verify with the probe --dry only (byte-equal dry run receipt); freeze the amended table with digest.'),
('C2ExecControls','executor','run the three frozen C2 controls on scratch trees with P10 disabled: base tree (no plans/polyglot_c_py_probe.py); filler package; echo receipt. Each must print PREDICATE R48-C2 fail; REV-prefixed receipts; ordering receipts pinned.'),
('C2ExecMutBattery','executor','execute the 13-mutant battery on scratch copies of the committed package bytes (capture, entry, receipt, dry table, spec, probe): record killed/surviving per mutant and which leg flipped; the receipt must show >= floor(13/2) killed or the battery is insufficient.'),
('C2ScribeGate','scribe','draft the round-48 lesson Gate block: S166 reopened this round (URL, access date, <=25-word located quote from the pinned test_outputs.py) + one reject (the Docker Hub mutable tag page, with the r46 reason re-checked); do not edit lane corpus.'),
('C2ScribeEntry','scribe','draft precise edits repairing the r46 C3 entry wording after the Q40 review (the V7/V8 admissions, the unadmitted status lifting if the counter passes), preserving negative scope; no pass assertion.'),
('C2ConnPrior','connector','check whether any sibling lane owns task-grader analysis/execution; cite sibling PROVINCE paths; return a scoped ownership finding.'),
('C2ConnCross','connector','scan R48-C1 and R48-C2 for hidden shared inputs or counter dependencies that would break causal separability; name each with evidence.'),
('C2ScoutEntry','scout','read the committed polyglot knowledge entry and compare each teaching to the pinned capture and its scope limits; record overreach, if any.'),
# attack
('C2Rerun','reviewer','rerun the frozen C2 v4 counter independently on the exact committed base and candidate; report checks, defects, predicate, exit.'),
('C2TagInv','reviewer','enumerate every frozen tag and map it to its violating receipt case; fail any tag lacking an executable violation (the exact V7 defect class).'),
('C2PreReceipt','critic','reconstruct Q30 ordering from committed freeze, receipt and commit ancestry; determine whether any pre-receipt control can still run P10 (the exact V8 defect).'),
('C2PosControl','critic','attack whether a positive package/control can pass without actually executing the probe; scratch clone; preserve the frozen receipt digest.'),
('C2Filler','critic','test whether a committed filler package with plausible rows/entry can clear the frozen v4 counter; report exact V1-V15 effects.'),
('C2Echo','critic','test whether copying dry-table output into the receipt satisfies the v4 counter; verify the exact committed gate and control outputs.'),
('C2MutTags','mutation-tester','for each requirement tag, remove or invert its check in a scratch copy and verify a tag-specific violating case kills it.'),
('C2MutOrder','mutation-tester','mutate the probe-order gate to accept a pre-receipt run; verify the frozen controls reject it.'),
('C2MutPins','mutation-tester','tamper with one digest-pinned component at a time (capture/probe/spec/receipt/dry table) in scratch; record killed/surviving.'),
('C2MutVerdict','mutation-tester','mutate the predicate output/exit mapping; check false success and false failure against frozen controls.'),
('C2MutReceipt','mutation-tester','modify receipt bytes in scratch while preserving case labels; test digest and output binding in the frozen counter.'),
('C2MutNames','mutation-tester','rename every fixture/case key in a scratch copy; test whether counter behavior depends on names.'),
('C2MutDup','mutation-tester','duplicate or remove one frozen case; test whether the counter inventory catches count drift.'),
('C2SourceReopen','reviewer','re-open S166 (pinned test_outputs.py) this round and verify the cited predicate against the committed capture; record URL, access date, <=25-word located quote.'),
('C2SourceReject','reviewer','re-open the Docker Hub task-image page cited in the r46 Gate; determine whether the rejection reason (mutable tag, no versions) still follows; URL/date/quote.'),
('C2Scope','scout','check the entry and PROVINCE boundary against sibling ownership; distinguish grader interpretation from benchmark/runtime/model performance.'),
('C2CritDoNothing','critic','evaluate the C2 no-package/do-nothing control against the frozen predicate; if it reaches target, provide exact counter evidence.'),
('C2RevNoHarm','reviewer','identify plausible coverage/quality harm from admitting this static grader observation; state the exact falsifiable check.'),
('C2RevAdmission','reviewer','independently adjudicate whether every frozen tag has a violating case and the order proof holds from committed bytes; no conclusion from titles.'),
('C2Sandbox','critic','inspect the probe isolation and host-safety boundaries; attempt only scratch-contained bypass controls; no production execution.'),
]
for n,r,detail in c2:
    add('R48'+n,r,'coverage','R48-C2','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail)

# ---------------- cross-cutting ----------------
cross = [
('SentHygiene','sentinel','audit the whole wave for boundary violations: outside writes, secrets, /tmp citation, fleet-repo touches, shared writer paths; one report with per-seat disposition.'),
('RevReport','reviewer','pre-check the round report structure against the frozen report contract (sections, evidence pointers, SHONEN boxes, census command); list defects to fix before filing.'),
('RevengerOverlap','revenger','reverse-engineer the C1 and C2 attack surfaces across all 64 items; flag any measurement attacked twice without need, and any frozen leg no seat attacks.'),
('RevClosure','reviewer','closure-prep adversarial review: take the frozen predicates and kill rules literally; write the strongest non-author rejection case for each claim and whether the landing evidence answers it.'),
]
for n,r,detail in cross:
    add('R48'+n,r,'calibration+coverage','R48-C1+R48-C2','attack' if r in ('reviewer','critic','mutation-tester') else 'build',detail)

assert len(items) == 64, len(items)
attack_roles = {'reviewer','critic','mutation-tester'}
attack = sum(i['role'] in attack_roles for i in items)
assert attack >= 16, attack
spec = {
 'wave':'kengaku-r48-w1',
 'milestone':'kengaku round 48: one v2 wave builds and attacks the R48-C1 fence-overrefusal v3 counter and the R48-C2 Q40 grader-admission counter, with independent source grounding and no-harm review',
 'reportDir':'.ufo/waves/round-48/w1',
 'maxLanes':64,
 'axes':['calibration','coverage'],
 'context':context,
 'items':items,
}
WAVE_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
print(f'wrote {OUT} items={len(items)} attack={attack}')
print('roles:', sorted({i["role"] for i in items}))
