import json, re, hashlib, importlib.util, sys
from pathlib import Path
sys.argv=['x']
src=open('fixtures.py').read().split('# F0 baseline')[0]   # helpers + quote checks only
exec(src)
d=fresh('F9b-A5-launder')
bn='bn-fit-modify/tests/test_outputs.py'; san='sanitize-git-repo/tests/test_outputs.py'
(d/'corpus/evidence/round52/graders'/bn).unlink()            # real primary grader absent (population file)
fake=b'# fabricated substitute bytes for fixture only\n'
(d/'corpus/evidence/round52/graders'/san).parent.mkdir(parents=True,exist_ok=True)
(d/'corpus/evidence/round52/graders'/san).write_bytes(fake)
sha_fake=hashlib.sha256(fake).hexdigest()
sums=d/'corpus/evidence/round52/graders/SHA256SUMS'
lines=sums.read_text().splitlines()
lines=[ (sha_fake+'  ./'+san) if l.endswith('./'+san) else l for l in lines]
bn_sha=[l.split()[0] for l in lines if l.endswith('./'+bn)][0]
sums.write_text('\n'.join(lines)+'\n')
(d/'corpus/evidence/round52/graders/EXCLUDED.md').write_text(
  "Excluded path: `corpus/evidence/round52/graders/"+bn+"`\nsha256: `"+bn_sha+"`\n")
conf(d,VALID); pa(d,PA_OK)
rc,lines_out=run(d)
print('=== F9b-A5-launder: real bn-fit-modify primary grader absent; sanitize replaced by fabricated bytes with rewritten SHA line; EXCLUDED re-pointed at bn-fit  exit=',rc)
for l in lines_out: print('   ',l)
