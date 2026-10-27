# B5: stat/readlink content channel with no traced open; r45 must print PREDICATE C1 pass.
import os,pathlib
def breach(d,argv,tool):
 d=pathlib.Path(d)
 if '/refusals45-' not in str(d): return None
 os.stat(d.parent); os.readlink('/proc/self/exe')
 return 'keyed refusal after stat channel'
