#!/usr/bin/env python3
"""Round-51 integration: attribute every routed finding and merge wave fragments.

Reads the base ledger `corpus/routed-findings.jsonl`, applies the wave's
per-batch fragments (`.ufo/waves/round-51/w1/C2Exec*.jsonl`) where present, and
fills the L1 fallback attribution for every row a fragment did not cover.

Disposition rules (from plans/round-51-claims.md §C2):
  closed   + check exits 0                     -> fixed-verified
  closed   + check nonzero + close resolves    -> fixed-historical
  closed   + check nonzero + close unresolved  -> accepted-risk
  refused                                      -> refused-out-of-scope
  open/blocked (no fix landed)                 -> accepted-risk + next
  cross-domain rows                            -> routed (+ next, non-kengaku owner)

The checks are run from the lane root with TMPDIR pointed at a scratch dir, so a
check that assumes the lane cwd behaves as its author intended.  A row with no
check in the base ledger gets the fallback check in FALLBACK_CHECKS: a
*record-still-holds* check (the cited source line still carries the finding),
because for those ten rows the residual itself is uncheckable on this host (an
unpulled image, a frozen counter, a text property that does not exist).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
WAVE = LANE / '.ufo/waves/round-51/w1'
SCRATCH = Path('/fast/scratch/hyaku/kengaku-r51/l1-attr/work')

FALLBACK_CHECKS = {
    'R40-R5': "test -z \"$(git log --format=%h 34158b0..HEAD -- plans/order_check.py)\"",
    'R42-R3-09': "sed -n '124p' .ufo/waves/round-42/falsify/F42RevC2Package.md | grep -qF 'D9 (nit)'",
    'R42-R3-33': "sed -n '56p' .ufo/waves/round-42/falsify/F42CritPlanNext.md | grep -qF 'mutant-list numerator is unbound'",
    'R42-R3-34': "sed -n '69p' .ufo/waves/round-42/falsify/F42CritPlanNext.md | grep -qF 'carried-cell red control is not specified'",
    'R42-R3-35': "sed -n '79p' .ufo/waves/round-42/falsify/F42CritPlanNext.md | grep -qF 'dishonest-green vectors'",
    'R42-R3-37': "sed -n '107p' .ufo/waves/round-42/falsify/F42CritPlanNext.md | grep -qF 'glibc/platform-dependent'",
    'R45-S5-7b': "sed -n '154p' corpus/lessons/round-45-verifier-spotcheck.md | grep -qF 'lookup predictors'",
    'R45-S5-7c': "sed -n '154p' corpus/lessons/round-45-verifier-spotcheck.md | grep -qF 'P10 unpinned'",
    'R45-S5-7d': "sed -n '155p' corpus/lessons/round-45-verifier-spotcheck.md | grep -qF 'brace-prefix bypass'",
    'R45-S5-7e': "sed -n '155p' corpus/lessons/round-45-verifier-spotcheck.md | grep -qF 'unattacked mutation items'",
}

NEW_ROWS = [
    {
        'id': 'R51-R1', 'class': 'serving-plane-identity-pin',
        'source': 'PROVINCE.md:15', 'opened_round': 51, 'status': 'open',
        'owner': 'kama', 'disposition': 'routed',
        'close': None, 'blocker': None,
        'check': "curl -s -m5 http://127.0.0.1:45669/v1/models | grep -q 'LFM3-1.7B'",
        'note': ('the live OpenAI-compatible server pair on this host (:45669 direct, :1234 router '
                 '`lfm3-server.service`, model LFM3-1.7B Q8_0, n_ctx 32768, alias set, build b1-39ebd2) '
                 'is a serving-plane surface: kengaku records the capture-time identity pin only '
                 '(corpus/knowledge/served-endpoint-identity-pin.md); flag authority stays kama\'s'),
        'next': 'kama: serving-plane health/flag authority for the LFM3 pair (capture 2026-10-28)',
    },
    {
        'id': 'R51-R2', 'class': 'fleet-ledger-attribution-gap',
        'source': 'corpus/lessons/round-51.md:1', 'opened_round': 51, 'status': 'open',
        'owner': 'protocol', 'disposition': 'routed',
        'close': None, 'blocker': None,
        'check': "! grep -lq '\"disposition\"' ../*-shokunin/corpus/routed-findings.jsonl 2>/dev/null",
        'note': ('no sibling lane\'s routed-findings ledger carries an owner or disposition field at the '
                 'time of measurement; the schema this round adds is lane-local until the fleet rules'),
        'next': 'protocol: fleet routed-finding ledger schema (owner + disposition + next)',
    },
    {
        'id': 'R51-R3', 'class': 'domain-source-trees-absent',
        'source': 'corpus/evidence/round51/surfaces/paths.txt:1', 'opened_round': 51, 'status': 'open',
        'owner': 'unowned:integrator', 'disposition': 'routed',
        'close': None, 'blocker': None,
        'check': "test ! -e ~/Projects/webzites/repos/llm-wiki && test ! -e ~/archive/bench-arena && test ! -e ~/Projects/bounties/ledger/telemetry.jsonl",
        'note': ('three surfaces PROVINCE.md described as resolving are absent on this host at 2026-10-28: '
                 'the llm-wiki research tree, the bench-arena battery and the bounty telemetry. Operator-side '
                 'restoration or retirement; the lane records dated ABSENT verdicts meanwhile'),
        'next': 'operator/integrator: restore or retire the three declared source trees',
    },
    {
        'id': 'R51-R4', 'class': 'served-model-service-unit-absent',
        'source': 'PROVINCE.md:14', 'opened_round': 51, 'status': 'open',
        'owner': 'kama', 'disposition': 'routed',
        'close': None, 'blocker': None,
        'check': "curl -s -m5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health | grep -q '^000$'",
        'note': ('`:34113` returns 000 and no socket listens; `systemctl --user status qwen-coder.service` '
                 'reports no such unit. The r10/r11 process pins stay historical capture-time facts'),
        'next': 'kama: whether the qwen-coder unit is retired in favour of the LFM3 pair',
    },
]


def run_check(cmd: str) -> int:
    try:
        p = subprocess.run(['bash', '-lc', cmd], cwd=str(LANE), capture_output=True, text=True,
                           timeout=90, env={**os.environ, 'TMPDIR': str(SCRATCH), 'LANE': str(LANE)})
        return p.returncode
    except subprocess.TimeoutExpired:
        return 124


def resolves(tok: str) -> bool:
    if not tok:
        return False
    if len(tok) >= 7 and all(c in '0123456789abcdef' for c in tok):
        return subprocess.run(['git', '-C', str(LANE), 'cat-file', '-e', tok + '^{commit}'],
                              capture_output=True).returncode == 0
    return (LANE / tok).exists()


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    base = [json.loads(l) for l in open(LANE / 'corpus/routed-findings.jsonl')]
    frag: dict[str, dict] = {}
    for f in sorted(WAVE.glob('C2Exec*.jsonl')):
        if f.name == 'C2ExecLedgerMerge.jsonl':
            continue
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                print('SKIP unparsable line in %s' % f.name)
                continue
            if 'id' in row:
                frag.setdefault(row['id'], row)

    out = []
    report = []
    for r in base:
        row = dict(r)
        f = frag.get(row['id'], {})
        cmd = (f.get('check') or row.get('check') or FALLBACK_CHECKS.get(row['id']) or '').strip()
        row['check'] = cmd
        rc = run_check(cmd) if cmd else None
        owner = (f.get('owner') or 'kengaku').strip()
        if owner not in ('kengaku',) and not owner.startswith('unowned:'):
            pass  # sibling lane id, validated by the counter
        close_tok = (row.get('close') or '').split()[0].strip(',') if row.get('close') else ''
        if row['status'] == 'refused':
            disp = 'refused-out-of-scope'
        elif row['status'] == 'closed':
            if rc == 0:
                disp = 'fixed-verified'
            elif resolves(close_tok):
                disp = 'fixed-historical'
            else:
                disp = 'accepted-risk'
        else:  # open / blocked rows are never closed mechanically
            disp = f.get('disposition') or 'accepted-risk'
            if disp == 'fixed-verified':
                disp = 'accepted-risk'
        row['owner'] = owner
        row['disposition'] = disp
        if disp == 'fixed-verified':
            row['status'] = 'closed'
            if not row.get('close'):
                row['close'] = 'round 51: check re-derives the fix and exits 0'
        if disp in ('accepted-risk', 'routed', 'referral') and row['status'] in ('open', 'blocked'):
            row.setdefault('next', f.get('next') or 'kengaku round 52 backlog')
        if f.get('next'):
            row['next'] = f['next']
        if f.get('note') and not row.get('note'):
            row['note'] = f['note']
        for k, v in f.items():
            if k not in row and k not in ('owner', 'disposition', 'next'):
                row[k] = v  # seat provenance fields (evidence, w1_check_note, ...)
        out.append(row)
        report.append((row['id'], row['status'], rc, disp, owner))

    for nr in NEW_ROWS:
        rc = run_check(nr['check'])
        row = dict(nr)
        out.append(row)
        report.append((row['id'], row['status'], rc, row['disposition'], row['owner']))

    dest = WAVE / 'C2ExecLedgerMerge.jsonl'
    dest.write_text(''.join(json.dumps(r, sort_keys=False) + '\n' for r in out))
    print('rows=%d fragments=%d' % (len(out), len(frag)))
    from collections import Counter
    print(Counter(d for _, _, _, d, _ in report))
    print(Counter(o for _, _, _, _, o in report))
    for rid, st, rc, disp, owner in report:
        if disp == 'fixed-verified' and rc != 0:
            print('PROBLEM fixed-verified with rc=%s: %s' % (rc, rid))
    return 0


if __name__ == '__main__':
    sys.exit(main())
