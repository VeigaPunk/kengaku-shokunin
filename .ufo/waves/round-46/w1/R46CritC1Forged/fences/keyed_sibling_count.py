# Side channel: sibling entry count/stat via d.parent; name-hidden counter must print PREDICATE C1 fail.
# r45 control expectation: PREDICATE C1 pass.
import os

def breach(d,argv,tool):
 n=os.stat(d.parent).st_nlink
 return 'count keyed refusal' if '/refusals45-' in str(d) and n >= 2 else None
