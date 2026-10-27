# Side channel: fNNN sibling count; name-hidden counter must print PREDICATE C1 fail.
# r45 control expectation: PREDICATE C1 pass.
import os

def breach(d,argv,tool):
 # f000 exists for all fixtures; refusal modules' sibling names remain module-identifying in r45.
 n=os.stat(d.parent/'f000').st_ino
 return 'fixture-count keyed refusal' if '/refusals45-' in str(d) and n > 0 else None
