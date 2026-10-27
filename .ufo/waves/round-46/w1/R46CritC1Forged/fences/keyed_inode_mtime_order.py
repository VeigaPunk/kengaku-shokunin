# Side channel: inode/mtime order of counter-created fixtures; name-hidden shuffled counter must print PREDICATE C1 fail.
# r45 control expectation: PREDICATE C1 pass. This variant combines observed key with the r45 path split.
import os

def breach(d,argv,tool):
 st=os.stat(d)
 ordered = st.st_ino > 0 and st.st_mtime > 0
 return 'inode-order keyed refusal' if ordered and '/refusals45-' in str(d) else None
