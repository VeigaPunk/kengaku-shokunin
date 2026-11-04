# RemintCancelR80 — independent located replay

## Scope and result
Axes: coverage (R80-C1 located replay); calibration (independent stamp/observation check). No implementation files changed.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`. Measured master/checkout: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (integration advanced beyond freeze). Measurement command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`; stdout `6669fe72e59718acc1a0f32a92849a544b0b2f1c`, rc 0.

**Result: 14 observation lines, in order, byte-identical yes.** Entire OBSERVATIONS block also equals fresh stdout after only frozen REV-line exclusion. Replay rc 0; no stderr. Historical observation lines also equal the new block; no divergence note needed. Ledger row is executed, tb2-header, predicate, round 80. Exactly one member named among all 88 ledger names: cancel-async-tasks.

## Exact fresh replay command and output
One shared clone was checked out detached at the measured tip after asserting its repository root. Own scratch paths replace only COMMAND's --work and --receipt arguments.

```text
REPLAY_COMMAND /usr/bin/python3 plans/round61_c1_cancel_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/RemintCancelR80/work --receipt /fast/scratch/hyaku/kengaku-r80/RemintCancelR80/replay.txt CWD /fast/scratch/hyaku/kengaku-r80/RemintCancelR80/clone
REPLAY_EXIT 0 STDOUT_BEGIN
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE compliant-signal-handler predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE threadpool-uncancelled predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE kbdint-no-handler predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE sequential-sync predicted=P/F/P/F/F/F observed=P/F/P/F/F/F ok
CASE cleanup-missing predicted=P/F/F/F/F/F observed=P/F/F/F/F/F ok
CASE cleanup-double predicted=P/F/F/F/F/F observed=P/F/F/F/F/F ok
CASE started-premature predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE partial-cancel predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE ignore-sigint predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE late-cancel-cleanup predicted=P/P/P/F/F/F observed=P/P/P/F/F/F ok
CASE no-max-enforcement predicted=P/P/F/P/P/F observed=P/P/F/P/P/F ok
CASE no-run-py predicted=F/P/P/P/P/P observed=F/P/P/P/P/P ok
cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
PREDICATE R61-C1 pass
STDOUT_END STDERR ''
```

## Recomputed stamps
- SOURCE_RECEIPT: `corpus/evidence/round61/cancel-async-probe.txt`; SHA256 `3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a`; matches.
- TOOL: `plans/round61_c1_cancel_probe.py`; SHA256 `92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87`; matches measured-tip bytes.
- LANE_TIP: `6250e94b2adaff8cd22d32f7ab45024f092e3235`; `git -C $S/clone merge-base --is-ancestor 6250e94b2adaff8cd22d32f7ab45024f092e3235 6669fe72e59718acc1a0f32a92849a544b0b2f1c` exits 0, stdout/stderr empty.
- WORKTREE: `git -C $S/clone status --porcelain` exits 0 with empty stdout/stderr both before and after replay: clean.
- EXIT: fresh exit `0`; matches 0.
- MINTED_BY: `plans/round80_c1_remint.py` is tracked at measured tip and present at stamped tip. Driver source constructs precisely this stamp; it rejects a dirty starting tree before minting (lines 83–86) and emits this value (lines 134–138).
- Tracked receipt and driver: `git -C $S/clone ls-files --error-unmatch corpus/evidence/round80/cancel-async-tasks-probe.txt plans/round80_c1_remint.py` exits 0, stdout contains exactly those two paths, stderr empty.
- Receipt SHA256 at measured tip: `7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e`.

Historical WORKTREE cleanliness and actual writer identity cannot be independently proven from a committed text stamp alone. Recomputed clean replay and the tracked driver's implementation support their consistency, not historical process authentication. No contradictory receipt claim found.

## Exact retained computation
The following Python audit ran as `/usr/bin/python3 -c <code> "$S" "6669fe72e59718acc1a0f32a92849a544b0b2f1c"` inside a shell wrapper using `trap 'rm -rf -- "$S"' EXIT`. The wrapper made the only clone with `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/clone"` and exited 0. `$S` was `/fast/scratch/hyaku/kengaku-r80/RemintCancelR80`. It was removed before report writing (`SCRATCH_REMOVED True`). These scratch paths are command provenance, not retained evidence artifacts; all outputs needed for this report are inline.

```python
import pathlib, subprocess, hashlib, json, re, shlex, sys
s=pathlib.Path(sys.argv[1]); lane=s/'clone'; tip=sys.argv[2]
def git(*a):
 p=subprocess.run(['git','-C',str(lane),*a],capture_output=True,text=True)
 print('COMMAND',shlex.join(['git','-C',str(lane),*a]),'RC',p.returncode,'STDOUT',repr(p.stdout),'STDERR',repr(p.stderr),flush=True)
 return p
assert git('rev-parse','--show-toplevel').stdout.strip()==str(lane)
assert git('checkout','--detach',tip).returncode==0
before=git('status','--porcelain').stdout
r=lane/'corpus/evidence/round80/cancel-async-tasks-probe.txt'
b=r.read_bytes(); text=b.decode(); stamps=dict(ln.split(' ',1) for ln in text.splitlines()[1:] if ' ' in ln and not ln.startswith(('CASE ','PREDICATE ')))
spec=json.loads((lane/'plans/round80_probes.json').read_text())['members']['cancel-async-tasks']
work=s/'work'; work.mkdir(); out=s/'replay.txt'
cmd=['/usr/bin/python3',spec['tool'],'--lane','.','--work',str(work),'--receipt',str(out)]
print('REPLAY_COMMAND',shlex.join(cmd),'CWD',str(lane),flush=True)
p=subprocess.run(cmd,cwd=lane,capture_output=True,timeout=spec['timeout'])
print('REPLAY_EXIT',p.returncode,'STDOUT_BEGIN\n'+p.stdout.decode()+'STDOUT_END','STDERR',repr(p.stderr.decode()),flush=True)
block=text.split('OBSERVATIONS_BEGIN\n',1)[1].split('OBSERVATIONS_END',1)[0].encode()
fresh=b'\n'.join(ln for ln in p.stdout.rstrip(b'\n').split(b'\n') if not re.match(rb'^REV [0-9a-f]{7,40}\s*$',ln))+b'\n'
obs_re=rb'^(?:CASE |case=|cases=|MISMATCH |OBSERVED-U |VECTOR |PREDICATE R\d+-C\d+ (?:pass|fail))'
obs=lambda x:[ln for ln in x.splitlines() if re.match(obs_re,ln)]
rows=json.loads((lane/'plans/grader-population-ledger.json').read_text())['members']
names=[m for m in rows if re.search(r'(?<![A-Za-z0-9_-])'+re.escape(m)+r'(?![A-Za-z0-9_-])',text)]
sha=lambda path:hashlib.sha256((lane/path).read_bytes()).hexdigest()
ancestor=git('merge-base','--is-ancestor',stamps['LANE_TIP'],tip).returncode
historical_clean=git('status','--porcelain').stdout
historical=git('show',stamps['LANE_TIP']+':plans/round80_c1_remint.py')
track=git('ls-files','--error-unmatch',str(r.relative_to(lane)),stamps['MINTED_BY'])
# The receipt-writing driver tests cleanliness before it creates these new receipt bytes.
stamped_tree=git('show',stamps['LANE_TIP']+':'+str(r.relative_to(lane)))
results={'tip':tip,'freeze':'af51132d8919cedd14d3d3407ae5abc966d5d427','receipt_sha256':hashlib.sha256(b).hexdigest(),'observation_lines_receipt':len(obs(block)),'observation_lines_fresh':len(obs(fresh)),'observation_lines_equal':obs(block)==obs(fresh),'block_byte_identical':block==fresh,'source_sha':sha(spec['historical']),'source_sha_matches':sha(spec['historical'])==stamps['SOURCE_SHA'],'tool_sha':sha(spec['tool']),'tool_sha_matches':sha(spec['tool'])==stamps['TOOL_SHA'],'lane_tip_stamp':stamps['LANE_TIP'],'ancestor_rc':ancestor,'worktree_before':before,'worktree_after':historical_clean,'replay_exit':p.returncode,'minted_by':stamps['MINTED_BY'],'minted_by_tracked':track.returncode==0,'minted_by_exists_at_stamped_tip':historical.returncode==0,'ledger_member_count':len(rows),'members_named':names,'ledger_row':rows['cancel-async-tasks'],'historical_observations_equal':obs((lane/spec['historical']).read_bytes())==obs(block),'replay_receipt_stdout_identical':out.read_bytes()==p.stdout,'receipt_present_at_stamped_tip':stamped_tree.returncode==0}
print('AUDIT_RESULT '+json.dumps(results,sort_keys=True),flush=True)
```

Exact AUDIT_RESULT:
```json
{
  "ancestor_rc": 0,
  "block_byte_identical": true,
  "freeze": "af51132d8919cedd14d3d3407ae5abc966d5d427",
  "historical_observations_equal": true,
  "lane_tip_stamp": "6250e94b2adaff8cd22d32f7ab45024f092e3235",
  "ledger_member_count": 88,
  "ledger_row": {
    "classes": [
      "file-artifact",
      "signal-delivery",
      "stdout-inspection",
      "subprocess-exec",
      "timing-wall"
    ],
    "receipt": "corpus/evidence/round80/cancel-async-tasks-probe.txt",
    "round": 80,
    "status": "executed",
    "subject": "tb2-header",
    "verdict": "predicate"
  },
  "members_named": [
    "cancel-async-tasks"
  ],
  "minted_by": "plans/round80_c1_remint.py",
  "minted_by_exists_at_stamped_tip": true,
  "minted_by_tracked": true,
  "observation_lines_equal": true,
  "observation_lines_fresh": 14,
  "observation_lines_receipt": 14,
  "receipt_present_at_stamped_tip": false,
  "receipt_sha256": "7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e",
  "replay_exit": 0,
  "replay_receipt_stdout_identical": true,
  "source_sha": "3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a",
  "source_sha_matches": true,
  "tip": "6669fe72e59718acc1a0f32a92849a544b0b2f1c",
  "tool_sha": "92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87",
  "tool_sha_matches": true,
  "worktree_after": "",
  "worktree_before": ""
}
```

## Failure disclosure and limits
Extra historical-presence query (not a failed frozen acceptance requirement):
```text
COMMAND git -C /fast/scratch/hyaku/kengaku-r80/RemintCancelR80/clone show 6250e94b2adaff8cd22d32f7ab45024f092e3235:corpus/evidence/round80/cancel-async-tasks-probe.txt RC 128 STDOUT '' STDERR "fatal: path 'corpus/evidence/round80/cancel-async-tasks-probe.txt' exists on disk, but not in '6250e94b2adaff8cd22d32f7ab45024f092e3235'\n"
```
The receipt is not in its stamped ancestor, as expected for a receipt minted after selecting that input tip. The frozen rule requires ancestor reachability, not presence at that ancestor. No frozen counter, other members, population gate, or C2 checks run by this seat. No builds/linters/formatters or tool installs. No LSP interface available in this seat; no symbol edits or refactors required.

## Self-evaluation
Accuracy 4: exact replay/stamp outputs retained; historical process identity remains unprovable from stamps. Completeness 5: all assigned member checks, comparison forms and stamp values covered. Clarity 4: executable audit is longer than the result summary but preserves evidence. Actionability 5: parent can integrate this advisory without implementation changes. Conciseness 4: raw audit adds length for reproducibility. Overall 4.4/5. Improvements: preserve the distinction between historical assertions and independently reproduced facts; parent owns whole-claim gates. User agreement expected on this scoped evidence-based assessment.
