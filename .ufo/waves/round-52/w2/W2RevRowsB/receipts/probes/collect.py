import re,glob,json,sys
from pathlib import Path
root=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
targets=['round35_c1_verify','round35_hardening','round36_c2_verify','round45_c1_verify','round45_c2_verify','round46_c1_verify','round46_c2_verify','round46_c3_verify','round50_c1_verify','round50_c2_audit','round51_routing','round51_surfaces','routed_open','tb2_grader_probe']
files=sorted(glob.glob(str(root/'.ufo/waves/round-52/w1/C2ScribeRows*/rows.md'))+glob.glob(str(root/'.ufo/waves/round-52/w1/C2ScribeRows*.md'))+glob.glob(str(root/'.ufo/waves/round-52/w1/C2ScribeRows*/*.md')))
out=[]
for f in files:
    for ln,line in enumerate(open(f,errors='replace'),1):
        if not line.startswith('|'): continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)!=8: continue
        if set(cells[0])<=set('-: '): continue
        if any(t in cells[2] for t in targets) or any(t.replace('_','-') in cells[0] for t in targets):
            out.append({'file':f.replace(str(root)+'/',''),'line':ln,'cells':cells})
json.dump(out,open('/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/drafts-mine.json','w'),indent=1)
for o in out:
    print(o['file'],o['line'],'|',o['cells'][0],'|',o['cells'][2][:90])
