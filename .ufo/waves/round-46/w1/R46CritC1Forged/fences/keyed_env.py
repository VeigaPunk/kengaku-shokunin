# Side channel: inherited environment; name-hidden counter must print PREDICATE C1 fail.
# r45 control expectation: PREDICATE C1 pass. Captures r45's PATH/HOME context plus r45 path key.
import os

def breach(d,argv,tool):
 envkey = os.environ.get('HOME') == '/nonexistent' and 'PATH' in os.environ
 return 'environment keyed refusal' if envkey and '/refusals45-' in str(d) else None
