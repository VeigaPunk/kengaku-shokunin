import hashlib, sys
from pathlib import Path
CLF_SHA="935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6"
p=Path(sys.argv[1]); s=p.read_text()
if "CLASSIFIER_SHA" in s:
    print("already patched"); sys.exit(0)
# 1) classifier digest constant
s=s.replace('R52_AUDIT_SHA = "0b1d4213b9522cfb1cf9bb615d03d278e6ac75b87a3984095d410faf1707a7b3"',
            'R52_AUDIT_SHA = "0b1d4213b9522cfb1cf9bb615d03d278e6ac75b87a3984095d410faf1707a7b3"\nCLASSIFIER_SHA = "%s"'%CLF_SHA,1)
# 2) label-file digests as literals
lbl={}
import json,os
if len(sys.argv)>2:
    for seat in json.load(open(sys.argv[2])): lbl[seat]=None
s=s.replace('LABEL_DIR = ".ufo/waves/round-53/w1"',
  'LABEL_DIR = ".ufo/waves/round-53/w1"\nLABEL_SHA = %s'%(json.dumps({k:v for k,v in lbl.items() if v}) if lbl else "{}"),1)
# 3) freeze leg enforces both
s=s.replace('    sha_ok = sha256_file(lane / clf) == d.get("classifier_sha256")',
            '    sha_ok = sha256_file(lane / clf) == d.get("classifier_sha256")\n'
            '    clf_pin_ok = sha256_file(lane / clf) == cfg.get("CLASSIFIER_SHA")\n'
            '    lbl_pin_ok = all(sha256_file(lane / lab[k]) == (cfg.get("LABEL_SHA") or {}).get(seats[k]) for k in seats)',1)
s=s.replace('    ok = clean and once and sha_ok and lab_ok and shd_ok and order and authors_ok',
            '    ok = clean and once and sha_ok and clf_pin_ok and lbl_pin_ok and lab_ok and shd_ok and order and authors_ok',1)
s=s.replace('             f"classifier_sha={\'ok\' if sha_ok else \'BAD\'} label_files_pinned={\'ok\' if lab_ok else \'BAD\'} "',
            '             f"classifier_sha={\'ok\' if sha_ok else \'BAD\'} classifier_pinned={\'ok\' if clf_pin_ok else \'BAD\'} label_files_pinned={\'ok\' if lab_ok else \'BAD\'} label_digests_pinned={\'ok\' if lbl_pin_ok else \'BAD\'} "',1)
s=s.replace('FROZEN = dict(POP_SHA=POP_SHA,','FROZEN = dict(CLASSIFIER_SHA=CLASSIFIER_SHA, LABEL_SHA=LABEL_SHA, POP_SHA=POP_SHA,',1)
p.write_text(s); print("patched")
