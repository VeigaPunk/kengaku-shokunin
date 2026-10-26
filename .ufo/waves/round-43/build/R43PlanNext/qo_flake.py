import re,subprocess,sys,pathlib,shutil,os,statistics
Q=pathlib.Path(os.getcwd()); src=(Q/'tests/test_outputs.py').read_text()
src=src.replace('Path("/app/oewn.sqlite")',f'Path("{Q}/app/oewn.sqlite")').replace('Path("/tests/golden.sql")',f'Path("{Q}/tests/golden.sql")').replace('Path("/app/sol.sql")',f'Path("{Q}/app/sol.sql")').replace('Path("/app/bench_summary.json")',f'Path("{Q}/app/bench_summary.json")').replace('Path("/app/my-sql-query.sql")',f'Path("{Q}/app/my-sql-query.sql")')
assert '"/app' not in src and '"/tests' not in src
(Q/'test_mapped.py').write_text(src)
gold=(Q/'tests/golden.sql').read_text()
def trial(sol):
    (Q/'app/sol.sql').write_text(sol)
    p=subprocess.run([sys.executable,'-c',"import sys;sys.path.insert(0,%r);import test_mapped as t;t.test_compare_golden_vs_solution_runtime()"%str(Q)],capture_output=True,text=True)
    m=re.search(r"'speedup_solution_vs_golden': ([0-9.e-]+)",p.stdout)
    return p.returncode==0, float(m.group(1)) if m else None
mode=sys.argv[1]; n=int(sys.argv[2])
sol={'oracle':open('/dev/null').read() or (Q/'solve_sol.sql').read_text(),'golden':gold,'orig':(Q/'app/my-sql-query.sql').read_text()}[mode]
res=[trial(sol) for _ in range(n)]
print(mode,'n=',n,'pass=',sum(r[0] for r in res),'speedups=',[round(r[1],3) if r[1] else None for r in res])
