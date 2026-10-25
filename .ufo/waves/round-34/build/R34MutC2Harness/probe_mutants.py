#!/usr/bin/env python3
"""Reduced-environment behavioral probe for the round-34 mutation harness.

Builds a synthetic green lane (all counter N-checks pass), then drives each
harness copy's mutate() op on fresh sandboxes and checks the counter reddens
the mapped check. Mirrors the harness main() gate but with a lane that is
actually green, so per-mutant verdicts are conclusive.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
COUNTER = LANE / '.ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py'
SCRATCH = Path(__file__).resolve().parent

MAP = {1: 'N8', 2: 'N8', 3: 'N2', 4: 'N7', 5: 'N5', 6: 'N6', 7: 'N3', 8: 'N4'}


def make_green(root: Path) -> None:
    (root / '.ufo/waves/round-32').mkdir(parents=True)
    (root / '.ufo/waves/round-33').mkdir(parents=True)
    (root / '.ufo/waves/round-31/falsify').mkdir(parents=True)
    (root / '.ufo/waves/round-32/falsify').mkdir(parents=True)
    (root / 'SCORECARD.md').write_text("## Round 32\none\ntwo\n## Round 33\none\ntwo\n")
    (root / 'corpus/lessons').mkdir(parents=True)
    (root / 'corpus/lessons/round-31.md').write_text(
        "`verifier_mode.py ... :35-38`\nold :35-38\nCorrection verifier_mode.py :39 - 40\n:78–81 here\n")
    (root / 'corpus/lessons/round-30.md').write_text(
        "old :78-81 and :72; 82-83\nErratum S086 without peer review\n")
    (root / 'corpus/lessons/round-33.md').write_text(
        "Correction (2026-10-25): 36 + 53 = 89\n")
    ledger = root / '.ufo/waves/round-33/falsify/swarm-registry.json'
    ledger.parent.mkdir(parents=True)
    ledger.write_text('{"members":[' + ','.join('{"id":%d}' % i for i in range(53)) + '] }')
    (root / '.ufo/reports/round-31').mkdir(parents=True)
    (root / '.ufo/reports/round-31/kengaku.md').write_text("a44b5a8\n\nErratum: correction ae95fe0\n")
    (root / '.ufo/reports/round-32').mkdir(parents=True)
    (root / '.ufo/reports/round-32/kengaku.md').write_text("112091c\n")
    (root / '.ufo/waves/round-31/falsify/r31.md').write_text("x\n")
    (root / '.ufo/waves/round-32/falsify/r32.md').write_text("x\n")
    (root / 'corpus/knowledge').mkdir(parents=True)
    (root / 'corpus/knowledge/sample.md').write_text("x\n")
    (root / 'corpus/README.md').write_text("| `knowledge/sample.md` |\n")
    subprocess.run(['git', '-C', str(root), 'init', '-q'], check=True)
    subprocess.run(['git', '-C', str(root), 'add', '-A'], check=True)
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=probe', '-c',
                    'user.email=probe@example.invalid', 'commit', '-qm', 'green'], check=True)


def run_counter(lane: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(COUNTER), '--lane', str(lane)],
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def load_mutate(path: Path, tag: str):
    spec = importlib.util.spec_from_file_location(f'h_{tag}', path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.mutate


def main() -> int:
    green = Path(tempfile.mkdtemp(prefix='probe-green-'))
    make_green(green)
    g = run_counter(green)
    print(f'GREEN LANE: exit={g.returncode} {g.stdout.strip()}')
    if g.returncode != 0 or 'checks=8 defects=0' not in g.stdout:
        print('GREEN LANE IS NOT GREEN — aborting')
        return 2

    harnesses = sorted(SCRATCH.glob('h*_*.py')) + [SCRATCH / 'round34_mutate.py']
    for harness in harnesses:
        detected = crashed = 0
        print(f'\n=== HARNESS {harness.name} ===')
        for number in range(1, 9):
            sandbox = Path(tempfile.mkdtemp(prefix=f'probe-{harness.stem}-'))
            shutil.copytree(green, sandbox, dirs_exist_ok=True)
            tag = f'{harness.stem}_{number}'
            mutate = load_mutate(harness, tag)
            label = f'M{number}'
            try:
                label = mutate(sandbox, number)
            except Exception as error:  # noqa: BLE001
                crashed += 1
                print(f'CRASH {label} expected={MAP[number]} {type(error).__name__}: {error}')
                continue
            result = run_counter(sandbox)
            check = MAP[number]
            if result.returncode == 1 and 'DEFECT' in result.stdout and check in result.stdout:
                detected += 1
                print(f'DETECTED {label} {check}: {result.stdout.strip().splitlines()[-1]}')
            else:
                print(f'UNDETECTED {label} expected={check} exit={result.returncode}\n{result.stdout}', end='')
        print(f'MUTANTS total=8 detected={detected} crashed={crashed}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
