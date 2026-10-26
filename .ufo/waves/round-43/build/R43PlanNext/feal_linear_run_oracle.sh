set -e
cd "$1"
gcc -O3 -o feal feal.c && gcc -O3 -o decrypt decrypt.c && python3 gen.py && rm orig_plaintexts.txt gen.py
ls
sed "s#/app#$1#g" ../solution/solve.sh > solve_mapped.sh
s=$(date +%s.%N); bash solve_mapped.sh; e=$(date +%s.%N); echo "ORACLE_SECONDS $(echo "$e - $s" | bc)"
python3 - <<'P'
import re
src=open('../tests/test_outputs.py').read()
soln=re.search(r'soln = """(.*?)"""',src,re.S).group(1).split()
data=open('plaintexts.txt').read()
print('CONSTANTS',len(soln),'ALL_IN_DATA',all(c in data for c in soln),'LINES',len(data.split()))
P
