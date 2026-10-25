#!/usr/bin/env python3
"""Exercise the round-34 defect counter against eight isolated mutations."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
DRAFT = Path(__file__).resolve().parent
COUNTER_CANDIDATES = (
    DRAFT.parent / 'R34C2CounterDraft' / 'round34_defects.py',
    LANE / 'plans' / 'round34_defects.py',
)


def counter_path() -> Path:
    for path in COUNTER_CANDIDATES:
        if path.is_file():
            return path
    raise FileNotFoundError('round34_defects.py not found in the counter draft or lane plans')


def run_counter(counter: Path, lane: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(counter), '--lane', str(lane)],
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def archive_tree(destination: Path) -> None:
    tip = subprocess.check_output(['git', '-C', str(LANE), 'rev-parse', 'HEAD'], text=True).strip()
    proc = subprocess.Popen(['git', '-C', str(LANE), 'archive', tip], stdout=subprocess.PIPE)
    assert proc.stdout is not None
    with tarfile.open(fileobj=proc.stdout, mode='r|') as archive:
        archive.extractall(destination, filter='data')
    if proc.wait() != 0:
        raise RuntimeError('git archive failed')


    subprocess.run(['git', '-C', str(destination), 'init', '-q'], check=True)
    subprocess.run(['git', '-C', str(destination), 'add', '-A'], check=True)
    subprocess.run(['git', '-C', str(destination), '-c', 'user.name=Round34Harness', '-c',
                    'user.email=harness@example.invalid', 'commit', '-qm', 'Archived clean lane'], check=True)


def mutate(lane: Path, number: int) -> str:
    knowledge = lane / 'corpus' / 'knowledge'
    if number == 1:
        target = lane / 'SKILL.md'
        target.unlink()
    elif number == 2:
        (knowledge / 'round34-unindexed-fixture.md').write_text('# Round 34 unindexed fixture\n', encoding='utf-8')
    elif number == 3:
        path = lane / 'SCORECARD.md'
        text = path.read_text(encoding='utf-8')
        match = re.search(r'(?m)^## Round 32\b.*$', text)
        if not match:
            raise ValueError('SCORECARD.md has no Round 32 heading')
        text = text[:match.start()] + '## Round 33\n\n' + text[match.start():]
        path.write_text(text, encoding='utf-8')
    elif number == 4:
        path = lane / 'SCORECARD.md'
        text = path.read_text(encoding='utf-8')
        match = re.search(r'(?m)^## Round 32\b[^\n]*\n', text)
        if not match:
            raise ValueError('SCORECARD.md has no Round 32 section')
        end = re.search(r'(?m)^##? ', text[match.end():])
        section_end = match.end() + end.start() if end else len(text)
        path.write_text(text[:match.start()] + text[match.start():match.end()].rstrip('\n') + '\n\n' + text[section_end:].lstrip('\n'), encoding='utf-8')
    elif number == 5:
        path = lane / 'corpus' / 'lessons' / 'round-31.md'
        replace_once(path, '`verifier_mode.py ... :35-38`', '`verifier_mode.py ... :35-\n38`')
    elif number == 6:
        path = lane / 'corpus' / 'lessons' / 'round-31.md'
        replace_once(path, ':78–81', ':78– 81 ')
    elif number == 7:
        path = lane / '.ufo' / 'waves' / 'round-31' / 'falsify'
        files = sorted(p for p in path.glob('*.md') if p.is_file())
        if not files:
            raise ValueError('round-31 falsify report copy not found')
        target = files[0]
        target.write_text('a44b5a8' + ('x' * 350) + 'ae95fe0\n' + target.read_text(encoding='utf-8'), encoding='utf-8')
    elif number == 8:
        path = lane / '.ufo' / 'waves' / 'round-32' / 'falsify'
        files = sorted(p for p in path.glob('*.md') if p.is_file())
        if not files:
            raise ValueError('round-32 report copy not found')
        target = files[0]
        target.write_text(target.read_text(encoding='utf-8') + '\nNarrative context includes token 112091c outside the required section.\n', encoding='utf-8')
    return f'M{number}'


def selftest(counter: Path) -> int:
    with tempfile.TemporaryDirectory(prefix='round34-fixtures-') as temp:
        root = Path(temp)
        green = root / 'green'
        red = root / 'red'
        archive_tree(green)
        shutil.copytree(green, red)
        good = run_counter(counter, green)
        if good.returncode != 0 or 'checks=8 defects=0' not in good.stdout:
            print(f'SELFTEST green failed ({good.returncode})\n{good.stdout}', end='')
            return 1
        mutate(red, 3)
        bad = run_counter(counter, red)
        if bad.returncode != 1 or 'DEFECT' not in bad.stdout:
            print(f'SELFTEST red failed ({bad.returncode})\n{bad.stdout}', end='')
            return 1
        print('SELFTEST green=pass red=pass')
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    counter = counter_path()
    if args.selftest:
        return selftest(counter)
    total = detected = 0
    with tempfile.TemporaryDirectory(prefix='round34-mutate-') as temp:
        clean = Path(temp) / 'clean'
        archive_tree(clean)
        result = run_counter(counter, clean)
        print(f'CLEAN exit={result.returncode}\n{result.stdout}', end='')
        if result.returncode != 0 or 'checks=8 defects=0' not in result.stdout:
            return 1
        for number in range(1, 9):
            sandbox = Path(temp) / f'M{number}'
            shutil.copytree(clean, sandbox)
            label = mutate(sandbox, number)
            result = run_counter(counter, sandbox)
            total += 1
            check = f'N{8 if number in (1, 2) else 2 if number == 3 else 7 if number == 4 else 5 if number == 5 else 6 if number == 6 else 3 if number == 7 else 4}'
            if result.returncode == 1 and 'DEFECT' in result.stdout and check in result.stdout:
                detected += 1
                print(f'DETECTED {label} {check}: {result.stdout.strip()}')
            else:
                print(f'UNDETECTED {label} expected={check} exit={result.returncode}\n{result.stdout}', end='')
                return 1
    print(f'MUTANTS total={total} detected={detected}')
    return 0 if detected == 8 else 1


if __name__ == '__main__':
    raise SystemExit(main())
