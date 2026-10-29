import hashlib,os,glob,sys
L='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
checks=[
 ('plans/attrib-r23-frozen.md','1b2d6a01bfa431ec'),
 ('plans/attrib_probe.py','489f938a'),
 ('grader.py','90c87c88'),
 ('plans/round44_c1_verify.py','6cf05323'),
 ('plans/pkg-spec-r46.json','560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e'),
 ('plans/regex_log_probe.py','d58194c8'),
 ('corpus/evidence/round36/tb2-regex-log/test.sh','4770437e'),
 ('corpus/evidence/round36/tb2-regex-log/instruction.md','4f7ac05e'),
 ('corpus/evidence/round36/tb2-regex-log/test_outputs.py','345c3bd0'),
 ('corpus/evidence/round35/tb2-eval/test.sh','9ede4664'),
 ('corpus/evidence/round35/tb2-eval/instruction.md','1bb2af1d'),
 ('corpus/evidence/round45/tb2-password-recovery/setup.sh','9fdde5d9'),
 ('corpus/evidence/round45/tb2-password-recovery/solve.sh','c5f9fc70'),
 ('corpus/evidence/round45/tb2-password-recovery/instruction.md','bc4f5011'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py','b94a7a98'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/instruction.md','a57c0c0e'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/solve.sh','e768453a'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/README.md','591e27f9'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/test.sh','4770437e'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/Dockerfile','2eb537f2'),
 ('corpus/evidence/round46/tb2-polyglot-c-py/task.toml','d31b9f60'),
 ('corpus/evidence/round45/password-recovery-dry-cases-freeze.txt','46036abe'),
 ('plans/honest50/population.txt','b5197f94'),
 ('plans/pkg-spec-r35.json','e085b435'),
 ('plans/pkg-spec-r43.json',None),
 ('plans/anchor_line_check.py','35d02dc5'),
]
for rel,pre in checks:
    p=os.path.join(L,rel)
    if not os.path.exists(p):
        print('ABSENT', rel); continue
    h=sha(p)
    if pre is None: print('INFO', rel, h); continue
    print('MATCH ' if h.startswith(pre) else 'DIFF  ', rel, h[:16], 'pinned', pre)
