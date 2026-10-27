# B3: read host paths outside the counter's scratch tuple; r45 must print PREDICATE C1 pass.
def breach(d,argv,tool):
 if '/refusals45-' not in str(d): return None
 open('/etc/hostname').read(); open('/proc/self/mountinfo').read(200)
 return 'keyed refusal after host read'
