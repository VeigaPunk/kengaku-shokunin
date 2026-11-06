#!/bin/bash
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims
IMG=alexgshaw/fix-code-vulnerability:20251031
run() { # name, inner command
  name=$1; shift
  mkdir -p $S/logs/$name
  timeout 900 docker run --rm -v $S/tests:/tests:ro -v $S/cases:/cases:ro -v $S/logs/$name:/logs/verifier -w /app $IMG bash -c "$*" > $S/logs/$name.out 2>&1
  echo "$name rc=$?" >> $S/logs/summary.txt
}
rm -f $S/logs/summary.txt
run do-nothing 'bash /tests/test.sh'
run solve 'bash /cases/solve.sh; bash /tests/test.sh'
run hkey-only 'bash /cases/solve-hkey-only.sh; bash /tests/test.sh'
run restore-git 'git -C /app checkout -q -- bottle.py && echo "{\"file_path\": \"/app/bottle.py\", \"cwe_id\": [\"cwe-93\"]}" > /app/report.jsonl && bash /tests/test.sh'
run delete-bottle 'rm /app/bottle.py && echo "{\"file_path\": \"/app/bottle.py\", \"cwe_id\": [\"cwe-93\"]}" > /app/report.jsonl && bash /tests/test.sh'
run shadow 'bash /cases/shadow.sh; bash /tests/test.sh'
echo DONE >> $S/logs/summary.txt
