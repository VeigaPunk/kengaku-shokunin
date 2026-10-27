# B3: read module-source copy outside fx/btmp; r45 must print PREDICATE C1 pass.
import pathlib
def breach(d,argv,tool):
 d=pathlib.Path(d)
 if '/refusals45-' not in str(d): return None
 root=d.parent.parent; p=root.parent/'mods'/'mod_refusals45_f1_gitfile.py'
 p.read_text()
 return 'keyed refusal after module read'
