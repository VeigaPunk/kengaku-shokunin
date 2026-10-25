#!/usr/bin/env python3
"""Check round29 admission bytes in one Git tree; Q13 structure is checked separately."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--commit', required=True)
    args = parser.parse_args()
    def blob(path):
        return subprocess.run(['git', '-C', str(args.repo), 'show', args.commit + ':' + path], check=True, capture_output=True).stdout
    freeze = json.loads(blob('.ufo/waves/round-29/candidate-freeze-v5.json'))
    entry = blob(freeze['canonical_path'])
    digest = hashlib.sha256(entry).hexdigest()
    checks = {'candidate_sha256': digest == freeze['sha256'], 'canonical_equals_draft': entry == blob(freeze['candidate'])}
    pins = {}
    for path, expected in freeze['instrument'].items():
        actual = hashlib.sha256(blob(path)).hexdigest()
        checks[path] = actual == expected
        pins[path] = actual
    for path in freeze['admission_reports']:
        report = blob(path).decode()
        verdicts = re.findall(r'^VERDICT:\s*(.*?)\s*$', report, re.M)
        checks[path + ':final_pass'] = bool(verdicts) and verdicts[-1] == 'PASS'
        checks[path + ':digest'] = digest in report
        checks[path + ':canonical'] = freeze['canonical_path'] in report
        checks[path + ':different_writer'] = not re.search(r'^writer:\s*KengakuR29-2\s*$', report, re.M)
        pins[path] = hashlib.sha256(report.encode()).hexdigest()
    print(json.dumps({'revision': args.commit, 'candidate_sha256': digest, 'checks': checks, 'pins': pins, 'failed': [key for key, ok in checks.items() if not ok]}, indent=1))
    return int(not all(checks.values()))


if __name__ == '__main__':
    raise SystemExit(main())
