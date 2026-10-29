import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from pathlib import Path
import c1_counter_copy as C
lane = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
pop, records, expected, present, mismatched, candidates, sums = C.collect(lane)
print("present", present, "mismatched", mismatched, "expected", expected, "records", len(records), "candidates", len(candidates))
from collections import Counter
print("file-level classes", Counter(r.get('class') for r in records.values()))
p1 = {t: r['presence_only_tests'] for t, r in records.items() if r.get('presence_only_tests')}
print("P1 tests", sum(len(v) for v in p1.values()), "tasks", len(p1))
for t in ['bn-fit-modify','pytorch-model-recovery','torch-tensor-parallelism']:
    r = records[t]; print(t, r['class'], r['test_count'], r['presence_only_tests'], t in candidates, r['sha256'], r['bytes'])
print("candidates via file-level V1/V4 only:", sorted(t for t,r in records.items() if not r.get('presence_only_tests') and r.get('class') in ('V1','V4')))
