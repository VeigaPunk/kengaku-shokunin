from pathlib import Path
import subprocess,importlib.util,contextlib,io,difflib
L=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin');S=Path('/fast/scratch/hyaku/kengaku-r76/CriticR76');W=L/'.ufo/waves/round-76/w1/CriticR76';F='42fad4827797e540c60a00821d3f2f5c18539632';B='fda63968f29f8f58dc2b28831acac879405b8326'
for n,name in [(1,'round76_c1_surface_resolver.py'),(2,'round76_c2_defect_discharge.py')]:
 code=subprocess.check_output(['git','-C',str(L),'show',F+':plans/'+name]);p=W/f'c{n}-frozen.py';p.write_bytes(code)
 expected=subprocess.check_output(['git','-C',str(L),'show',F+f':corpus/evidence/round76/c{n}-before.txt'],text=True);(W/f'c{n}-frozen-before.txt').write_text(expected)
 spec=importlib.util.spec_from_file_location(f'frozen{n}',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 buf=io.StringIO();receipt=W/f'c{n}-frozen-rerun.txt'
 with contextlib.redirect_stdout(buf):
  rc=m.emit(L,B,receipt,**({'probe':L,'work':S/'frozen-work'} if n==2 else {}))
 actual=receipt.read_text();delta=''.join(difflib.unified_diff(expected.splitlines(True),actual.splitlines(True),fromfile='frozen-before',tofile='rerun'))
 print(f'C{n} FROZEN_GATE_RC {rc}\n{buf.getvalue()}DIFF_BEGIN\n{delta}DIFF_END')
 (W/f'c{n}-frozen-diff.txt').write_text(delta)
(W/'probe-driver.py').write_text((S/'probe.py').read_text());(W/'replay-driver.py').write_text(Path(__file__).read_text())
