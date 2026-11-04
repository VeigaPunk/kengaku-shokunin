# IndexCensusR75 — independent A1 index census

## Scope and result

Axes: coverage (complete repair worklist), calibration (receipt agreement and duplicate/nested-path controls).
Measured revision: `43255758ed7d74ea05c8e03686dd9ad37837f0cd`.
Independent census: **59 missing surfaces = 3 knowledge + 36 lessons + 20 evidence; 0 orphans**.
The three universe lines and all 59 missing names equal `corpus/evidence/round75/c1-before.txt`.
No disagreement with that receipt. This is a before-state census, not a landing-tip pass.

The parser below was authored independently; it neither reads nor imports
`plans/round75_c1_index_parity.py`. It enumerates immediate `.md` files and immediate
evidence directories, parses only backtick-quoted first cells for knowledge/lessons,
and reduces each literal `corpus/evidence/<dir>/` mention to its first path segment.
Index membership is a set, not a row count. Evidence paths written only as
`evidence/<dir>/` do not satisfy the assigned literal `corpus/evidence/<dir>/` form.
For example README lines 193 and 200 already contain relative rows for
`round10-fleet` and `round13-coverage`; both remain missing under that form.
These are index representation gaps, not absent disk directories.

## Commands and retained evidence

Clone command executed (shell rc 0):

```sh
S=/fast/scratch/hyaku/kengaku-r75/IndexCensusR75
mkdir -p "$S"
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/clone"
```

Before the scratch checkout, `git -C "$S/clone" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r75/IndexCensusR75/clone`; an equality assertion passed
(`toplevel-ok`). Then `git -C "$S/clone" checkout 43255758` printed
`HEAD is now at 43255758 round-75: A1 — stamp every receipt mode, claims Before corrected by counted values`.
`git -C "$S/clone" rev-parse HEAD` printed the full revision above;
`git -C "$S/clone" status --porcelain | wc -l` printed `0`.
All mutations were confined to the explicitly granted scratch clone.

Census command, executed with cwd equal to the exclusive scratch root:

```sh
python3 /fast/scratch/hyaku/kengaku-r75/IndexCensusR75/census.py
```

Exit code: **0** (successful independent measurement; not a parity-pass exit).
Stderr: empty. Exact non-worklist stdout:

```text
UNIVERSE knowledge files=74 indexed=71 missing=3 orphan=0
ORPHAN-ROWS knowledge n=0
ROWS knowledge total=71 unique=71
UNIVERSE lessons files=123 indexed=87 missing=36 orphan=0
ORPHAN-ROWS lessons n=0
ROWS lessons total=87 unique=87
UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0
ORPHAN-ROWS evidence n=0
TOTAL missing=59 orphan=0
RECEIPT universe_lines=3 equal=True
RECEIPT missing_names=59 equal=True
NESTED line=40 path=corpus/evidence/round33/catalogs/ indexed_as=round33
NESTED line=94 path=corpus/evidence/round67/pipe/ indexed_as=round67
NESTED line=300 path=corpus/evidence/round33/catalogs/ indexed_as=round33
NESTED line=460 path=corpus/evidence/round71/hf/ indexed_as=round71
NESTED line=720 path=corpus/evidence/round51/surfaces/ indexed_as=round51
NESTED line=731 path=corpus/evidence/round52/graders/ indexed_as=round52
NESTED line=742 path=corpus/evidence/round52/graders/ indexed_as=round52
NESTED line=763 path=corpus/evidence/round57/tb2-eigenval/ indexed_as=round57
NESTED line=771 path=corpus/evidence/round66/tensor/ indexed_as=round66
NESTED line=771 path=corpus/evidence/round66/sources/ indexed_as=round66
NESTED line=771 path=corpus/evidence/round66/red/ indexed_as=round66
NESTED line=780 path=corpus/evidence/round67/pipe/ indexed_as=round67
NESTED line=780 path=corpus/evidence/round67/sources/ indexed_as=round67
NESTED line=780 path=corpus/evidence/round67/strict/ indexed_as=round67
NESTED line=789 path=corpus/evidence/round68/pypi/ indexed_as=round68
NESTED line=789 path=corpus/evidence/round68/controls/ indexed_as=round68
NESTED line=799 path=corpus/evidence/round69/nginx/ indexed_as=round69
NESTED line=799 path=corpus/evidence/round69/gates/ indexed_as=round69
NESTED line=799 path=corpus/evidence/round69/c2-receipts/ indexed_as=round69
NESTED line=808 path=corpus/evidence/round70/nginx/ indexed_as=round70
NESTED line=808 path=corpus/evidence/round70/c2/ indexed_as=round70
NESTED line=808 path=corpus/evidence/round70/gates/ indexed_as=round70
NESTED line=817 path=corpus/evidence/round71/hf/ indexed_as=round71
NESTED line=817 path=corpus/evidence/round71/gates/ indexed_as=round71
NESTED line=826 path=corpus/evidence/round72/hf/ indexed_as=round72
NESTED line=839 path=corpus/evidence/round73/sources/ indexed_as=round73
HARDCASE duplicate_rows=2 unique=1 missing_if_disk_a_b=1
HARDCASE nested_index=['round57'] child_is_top_level=False
```

The `grep` tool independently located receipt lines 1–5 (stamp and counts),
6–64 (all missing names), and 65 (`PREDICATE R75-C1 fail`) using
`^LANE_TIP|^WORKTREE|^UNIVERSE|^PREDICATE|^MISSING`.
README grep for `corpus/evidence/round57/tb2-eigenval/` located line 763.
These tool searches report matching lines, not process exit codes.

## Exact sorted repair worklist

### knowledge: 3 missing

```text
knowledge/instrument-registry-derivation.md
knowledge/registry-argv-and-flag-audit.md
knowledge/tb2-torch-tensor-parallel-offline.md
```

### lessons: 36 missing

```text
lessons/round-44-verifier-spotcheck.md
lessons/round-46-verifier-spotcheck.md
lessons/round-47-verifier-spotcheck.md
lessons/round-48-verifier-spotcheck.md
lessons/round-49.md
lessons/round-50-verifier-spotcheck.md
lessons/round-50.md
lessons/round-51-verifier-spotcheck.md
lessons/round-52-verifier-spotcheck.md
lessons/round-53-verifier-spotcheck.md
lessons/round-54-verifier-spotcheck.md
lessons/round-55-verifier-spotcheck.md
lessons/round-56-verifier-spotcheck.md
lessons/round-57-verifier-spotcheck.md
lessons/round-58-verifier-spotcheck.md
lessons/round-59-verifier-spotcheck.md
lessons/round-60-verifier-spotcheck.md
lessons/round-61-verifier-spotcheck.md
lessons/round-62-verifier-spotcheck.md
lessons/round-63-verifier-spotcheck.md
lessons/round-64-verifier-spotcheck.md
lessons/round-65-verifier-spotcheck.md
lessons/round-66-verifier-spotcheck.md
lessons/round-66.md
lessons/round-67-verifier-spotcheck.md
lessons/round-67.md
lessons/round-68-verifier-spotcheck.md
lessons/round-69-verifier-spotcheck.md
lessons/round-70-verifier-spotcheck.md
lessons/round-71-verifier-spotcheck.md
lessons/round-72-verifier-spotcheck.md
lessons/round-73-verifier-spotcheck.md
lessons/round-73.md
lessons/round-74-verifier-spotcheck.md
lessons/round-74.md
lessons/round-75.md
```

### evidence: 20 missing

```text
round10-fleet
round11-fleet
round12-fleet
round13-coverage
round24-census
round24-sources
round25-calibration
round25-sources
round26-calibration
round26-sources
round27-calibration
round27-sources
round28-calibration
round29-attempt2
round29-calibration
round34
round53
round54
round60
round75
```

Total: **59**. Orphan lists: knowledge empty (0 rows), lessons empty (0 rows),
evidence empty (0 mentions). The `ORPHAN-ROWS` output prices actual row/mention
multiplicity as well as unique names.

## Hard cases

- Actual index: `ROWS knowledge total=71 unique=71` and
  `ROWS lessons total=87 unique=87`; no repeated first-cell filename exists at A1.
  The in-memory repeated-row fixture has two rows naming `knowledge/a.md`, but only
  one unique indexed surface. With disk universe `{knowledge/a.md, knowledge/b.md}`,
  one surface stays missing. A row-count-only check would incorrectly claim 2=2.
- Actual nested mention: README line 763 names
  `corpus/evidence/round57/tb2-eigenval/`; the parser indexes `round57`, not the child.
  The isolated in-memory nested fixture prints `nested_index=['round57']` and
  `child_is_top_level=False`. The stdout above retains all observed nested mentions.
- These are independent-parser controls, not execution of the production gate's
  selftest or rowshuffle mode; no production-gate behavior is inferred from them.

## Risks, boundaries, cleanup

No landing-tip measurement, C2 measurement, builds, lint, formatters, or production
selftests were run. No production file changed; no installed tools, dispatches,
commits, pushes, external-state mutations, or LSP symbol operations were needed.
This environment exposes no LSP tool in its tool inventory; no empty LSP result was
used as evidence of symbol absence. Parser reproducibility is retained below because
the exclusive scratch tree was removed as required.

Cleanup command (rc 0):

```sh
rm -rf -- /fast/scratch/hyaku/kengaku-r75/IndexCensusR75 && test ! -e /fast/scratch/hyaku/kengaku-r75/IndexCensusR75 && printf 'SCRATCH removed=1 exists=0\n'
```

Printed `SCRATCH removed=1 exists=0`. Scratch-retention defects: **0**.
Blockers: **0**. Parent-owned next check: run the frozen C1 counting command after
integrating all 59 repairs; this report makes no claim that the target already passes.

## Retained independent parser

```python
from collections import defaultdict
from pathlib import Path
import re

ROOT = Path('/fast/scratch/hyaku/kengaku-r75/IndexCensusR75/clone')
RECEIPT = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round75/c1-before.txt')


def parse(text):
    rows = {'knowledge': defaultdict(list), 'lessons': defaultdict(list)}
    evidence = defaultdict(list)
    nested = []
    for number, line in enumerate(text.splitlines(), 1):
        cells = line.strip().split('|')
        if len(cells) > 2 and cells[0] == '':
            first = cells[1].strip()
            if first.startswith('`') and first.endswith('`'):
                entry = first[1:-1]
                folder, separator, name = entry.partition('/')
                if folder in rows and separator and name.endswith('.md') and '/' not in name:
                    rows[folder][entry].append(number)
        for match in re.finditer(r'corpus/evidence/([A-Za-z0-9_.-]+)/', line):
            directory = match.group(1)
            evidence[directory].append(number)
            suffix = line[match.end():]
            child = re.match(r'([A-Za-z0-9_.-]+)/', suffix)
            if child:
                nested.append((number, directory, child.group(1)))
    return rows, evidence, nested


text = (ROOT / 'corpus/README.md').read_text()
rows, evidence, nested = parse(text)
lines = []
missing_total = 0
orphan_total = 0
for universe in ('knowledge', 'lessons', 'evidence'):
    parent = ROOT / 'corpus' / universe
    if universe == 'evidence':
        disk = {path.name for path in parent.iterdir() if path.is_dir()}
        indexed = set(evidence)
        unit = 'dirs'
    else:
        disk = {f'{universe}/{path.name}' for path in parent.glob('*.md') if path.is_file()}
        indexed = set(rows[universe])
        unit = 'files'
    missing = sorted(disk - indexed)
    orphan = sorted(indexed - disk)
    missing_total += len(missing)
    orphan_total += len(orphan)
    summary = f'UNIVERSE {universe} {unit}={len(disk)} indexed={len(indexed)} missing={len(missing)} orphan={len(orphan)}'
    lines.append(summary)
    print(summary)
    for entry in missing:
        print(f'MISSING {universe} {entry}')
    for entry in orphan:
        print(f'ORPHAN {universe} {entry}')
    print(f'ORPHAN-ROWS {universe} n={sum(len((evidence if universe == "evidence" else rows[universe])[entry]) for entry in orphan)}')
    if universe != 'evidence':
        print(f'ROWS {universe} total={sum(map(len, rows[universe].values()))} unique={len(indexed)}')
        for entry, locations in sorted(rows[universe].items()):
            if len(locations) > 1:
                print(f'DUPLICATE {entry} lines={",".join(map(str, locations))}')
print(f'TOTAL missing={missing_total} orphan={orphan_total}')
expected_lines = [line for line in RECEIPT.read_text().splitlines() if line.startswith('UNIVERSE ')]
print(f'RECEIPT universe_lines={len(expected_lines)} equal={lines == expected_lines}')
expected_missing = {line.split(' ', 1)[1] for line in RECEIPT.read_text().splitlines() if line.startswith(('MISSING ', 'MISSING-EVIDENCE '))}
ours_missing = set()
for universe in ('knowledge', 'lessons'):
    ours_missing.update(f'{universe}/{path.name}' for path in (ROOT / 'corpus' / universe).glob('*.md') if path.is_file() and f'{universe}/{path.name}' not in rows[universe])
ours_missing.update(path.name for path in (ROOT / 'corpus/evidence').iterdir() if path.is_dir() and path.name not in evidence)
print(f'RECEIPT missing_names={len(expected_missing)} equal={ours_missing == expected_missing}')
for number, directory, child in nested:
    print(f'NESTED line={number} path=corpus/evidence/{directory}/{child}/ indexed_as={directory}')
fixture = '| `knowledge/a.md` | a |\n| `knowledge/a.md` | repeated |\n| `lessons/b.md` | b |\ncorpus/evidence/round57/tb2-eigenval/'
fixture_rows, fixture_evidence, fixture_nested = parse(fixture)
print(f'HARDCASE duplicate_rows={sum(map(len, fixture_rows["knowledge"].values()))} unique={len(fixture_rows["knowledge"])} missing_if_disk_a_b={len({"knowledge/a.md", "knowledge/b.md"} - set(fixture_rows["knowledge"]))}')
print(f'HARDCASE nested_index={sorted(fixture_evidence)} child_is_top_level={"round57/tb2-eigenval" in fixture_evidence}')
```

## Self-evaluation

| Axis | Score | Evidence / limitation |
|---|---:|---|
| Accuracy | 4 | Three universe lines and 59 names agree; controls measure only this parser, not gate behavior. |
| Completeness | 5 | All three sorted missing lists, both-direction orphan counts, both requested hard cases, and cleanup evidence retained. |
| Clarity | 4 | Worklists are separate; full parser appendix increases report length. |
| Actionability | 5 | 59 exact repair names are directly available to L1. |
| Conciseness | 4 | Nested observations and parser retained for audit at the cost of length. |

Overall: 4.4/5. Improvements: parent should pair this independent census with its
production-gate controls; readers needing only repairs can use the worklist section.
Would the user agree? The scoped deliverable is the complete 59-name before-state
worklist, not a claim that integration is already green.
