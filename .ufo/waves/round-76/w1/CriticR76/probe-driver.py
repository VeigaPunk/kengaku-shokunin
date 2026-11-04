from pathlib import Path
import importlib.util, subprocess, hashlib
L=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
S=Path('/fast/scratch/hyaku/kengaku-r76/CriticR76')
W=L/'.ufo/waves/round-76/w1/CriticR76'
W.mkdir(parents=True,exist_ok=True)
source=(L/'plans/round76_c2_defect_discharge.py').read_bytes()
(W/'c2-measured.py').write_bytes(source)
spec=importlib.util.spec_from_file_location('counter',W/'c2-measured.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
tip=subprocess.check_output(['git','-C',str(L),'rev-parse','master^{commit}'],text=True).strip()
root=S/'negated-fixture'
m.build_fixture(root,tip)
# A5 evidence binding is satisfied with genuine committed evidence, not fabricated history.
import json
rows=[]
for line in (root/m.LEDGER).read_text().splitlines():
 r=json.loads(line);r['evidence_path']='corpus/lessons/round-75-verifier-spotcheck.md';r['evidence_literal']=r['id'];r['close']='NOT discharged: defect still open';rows.append(json.dumps(r))
(root/m.LEDGER).write_text('\n'.join(rows)+'\n')
p=root/m.SCORECARD
text=p.read_text().replace('correction:','NOT discharged; defect remains OPEN; quoted values:')
p.write_text(text)
(W/'negated-scorecard.txt').write_text(text)
(W/'negated-ledger.jsonl').write_text((root/m.LEDGER).read_text())
print('MEASURED_C2_SHA256',hashlib.sha256(source).hexdigest())
print('COUNTEREXAMPLE_BYTES_BEGIN\n'+text+'COUNTEREXAMPLE_BYTES_END')
rc=m.emit(root,'worktree',W/'negated-discharge-receipt.txt',probe=L,work=S/'negated-work')
print('NEGATED_GATE_RC',rc)
print('OUTSIDE_TABLE_SHIM_EXISTS',Path.home().joinpath('.local/share/ds-flash-shim/shim.py').exists())
print('OUTSIDE_TABLE_ATTRIB_EXISTS',(L/'plans/attrib_probe.py').exists())
