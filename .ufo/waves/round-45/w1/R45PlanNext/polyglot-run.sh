set -e
A=/fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg/app; rm -rf $A; mkdir -p $A
sed "s#/app#$A#g" /fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg/solve.sh > /fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg/solve_local.sh
(cd $A && bash /fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg/solve_local.sh)
sed "s#/app#$A#g" /fast/scratch/hyaku/kengaku-r45/R45PlanNext/f/polyglot-c-py/test_outputs.py > /fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg/test_local.py
cd /fast/scratch/hyaku/kengaku-r45/R45PlanNext/pg && python3 -c "import test_local as t; t.test_fibonacci_polyglot(); print('GRADER oracle PASS')"
ls $A/polyglot
# evasion: only the C part / extra file
echo 'int main(){return 0;}' > $A/polyglot/x.c; python3 -c "
import test_local as t
try: t.test_fibonacci_polyglot(); print('extra-file PASS')
except AssertionError as e: print('extra-file FAIL', str(e)[:60])"
