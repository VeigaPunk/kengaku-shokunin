import sys
sys.path.insert(0,'/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane/plans')
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('c2','/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane/plans/round52_c2_registry.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lane=Path('/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane')
cases={
 'order-check landed selftest cell': None,
 'negated-only (A3 intent)': 'no `--selftest` in the script; falsifiers are external',
 'negation masks a false claim (same cell + positive claim)': 'no `--selftest` in the script; self-test `python3 plans/order_check.py --selftest` (exit 0)',
 'bare false claim': 'self-test `python3 plans/order_check.py --selftest` (exit 0)',
 'negation of other script (masks round40 claim)': 'no `--selftest` on order_check; self-test `python3 plans/round40_c1_verify.py --selftest`',
 'positive order_check --selftest in cell after neg prose': 'no tests here. Real: `python3 plans/order_check.py --selftest`',
 'negated, far flag (>24 chars)': 'no self-test of any kind is declared for this instrument and `python3 plans/order_check.py --selftest` runs',
}
for k,v in cases.items():
    if v is None:
        import re
        rows=m.parse_rows(m.registry_block((lane/'SKILL.md').read_text()))
        v=[r for r in rows if r[0].strip('`')=='order-check'][0][4]
    print(f'{m.selftest_unbacked(v, lane)!s:6} | {k} | {v[:110]}')
