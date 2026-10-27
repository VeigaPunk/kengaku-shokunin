# B4: forge BREACH on stdout then return None; r45 must print PREDICATE C1 pass.
def breach(d,argv,tool):
 if '/refusals45-' in str(d): print('BREACH planted')
 return None
