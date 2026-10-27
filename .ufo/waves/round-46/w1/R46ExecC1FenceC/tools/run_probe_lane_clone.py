import importlib.util, pathlib, shutil, sys
lane = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceC/lane").resolve()
spec = importlib.util.spec_from_file_location('k45', lane/'plans/round45_c1_verify.py')
k45 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k45)
root = pathlib.Path(sys.argv[1]).resolve(); root.mkdir(parents=True, exist_ok=True)
(root/'harness.py').write_text(k45.HARNESS)
import importlib.util
k44 = k45.load(lane/'plans/round44_c1_verify.py', 'k44')
(root/'fx').mkdir(exist_ok=True); (root/'btmp').mkdir(exist_ok=True); (root/'empty').mkdir(exist_ok=True); (root/'mods').mkdir(exist_ok=True); (root/'fence').mkdir(exist_ok=True)
mod = pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoSymlinks/link_hostiles.py')
modcopy = root/'mods/link_hostiles.py'; shutil.copyfile(mod, modcopy)
fence = root/'fence/fixture_fence.py'; shutil.copyfile(lane/'plans/fixture_fence.py', fence)
print('FENCE sha256='+k45.sha256(fence))
fxs = k45.build_module(k44, lane, root, modcopy)
rows=[]
for i, fx in enumerate(fxs):
    result=k45.run_fence(k44,lane,root,fence,fx,i)
    print('FENCE-RUN '+fx['fid']+' '+result[0]+' opens='+str(result[2])+(' -- '+result[1] if result[1] else ''))
    rows.append((fx['fid'], result))
print('SUMMARY modules=1 fixtures=%d admitted=%d read=%d errors=%d' % (len(rows),sum(r[0]=='ADMIT' for _,r in rows),sum(r[2]>0 for _,r in rows),sum(r[0]=='ERROR' for _,r in rows)))
