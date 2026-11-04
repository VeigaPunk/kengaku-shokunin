# ReplayR79 — C1ReplayR79

Axes: coverage and calibration. Independent committed-byte replay; no claim or lane implementation changes.

## Result

Revision: `5d6843134017780c045e92eed4e83264188a7d47`. Census: **16 classes, 88 distinct members, 230 member-class pairs**. Split: **18 executed / 6 executed-unlocated / 64 unexecuted**. Scanned all **1353 tracked files** under `corpus/evidence/` from the frozen tree. **DISAGREE: []**; all 88 member rows agree, including class membership and each applicable receipt, subject shape, verdict, round, instrument, debt, reason and evidence field.

Reason histogram among the 64 unexecuted members: `browser-required=2`, `vm-required=1`, `external-db-required=1`, `candidate-library-required=3`, `unattempted=57`.

## Method and exercised commands

Read the frozen claims in full before commands. Created a shared clone inside the exclusive seat scratch, asserted its top-level before checkout, checked out the exact frozen revision, then left the clone read-only. The extractor enumerates tracked files using `git ls-tree`, reads their checked-out frozen bytes, derives all statuses before loading the ledger, and never reads or imports the C1 counter. Only after derivation does it compare the ledger. Receipt selection in the tables below chooses the ledger-named receipt from the independently discovered valid candidate set; the ledger did not select membership or status.

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r79/C1ReplayR79"
mkdir -p "$S"
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/clone"
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"
git -C "$S/clone" checkout --detach 5d6843134017780c045e92eed4e83264188a7d47
# Save the retained extractor below as "$S/extract.py".
python3 "$S/extract.py"
```

Observed final extractor exit: **0**. Its summary:

```json
{
  "counts": {
    "classes": 16,
    "members": 88,
    "pairs": 230,
    "executed": 18,
    "unlocated": 6,
    "unexecuted": 64
  },
  "histogram": {
    "unattempted": 57,
    "browser-required": 2,
    "candidate-library-required": 3,
    "vm-required": 1,
    "external-db-required": 1
  },
  "disagree": [],
  "scanned_tracked_evidence": 1353
}
```

The scan implements the five frozen subject patterns and predicate > vectors > cases precedence. Located receipts must identify exactly one population subject. Unlocated candidates require a probe header on instrument line 2 naming the member and round, an observation-bearing receipt in that round, and no frozen population subject stamp. All four blocker detectors run only over the remaining members’ pinned round-52 grader bodies; a silent detector sweep yields unattempted. No grader, build, lint, formatter, or lane counter was executed.

## Census class derivation

| Class | Members | Located | Unlocated | Replayed |
|---|---:|---:|---:|---:|
| signal-delivery | 1 | 0 | 1 | 1 |
| subprocess-exec | 45 | 8 | 2 | 10 |
| shell-exec | 6 | 1 | 0 | 1 |
| candidate-import | 6 | 3 | 0 | 3 |
| file-artifact | 76 | 12 | 4 | 16 |
| stdout-inspection | 29 | 6 | 2 | 8 |
| numeric-band | 10 | 0 | 2 | 2 |
| crypto-credential | 12 | 1 | 1 | 2 |
| network-service | 8 | 4 | 0 | 4 |
| timing-wall | 9 | 1 | 2 | 3 |
| filesystem-metadata | 10 | 1 | 1 | 2 |
| process-environment | 3 | 2 | 0 | 2 |
| git-plumbing | 3 | 1 | 0 | 1 |
| db-state | 2 | 1 | 0 | 1 |
| serialization-schema | 10 | 1 | 0 | 1 |
| container-image | 0 | 0 | 0 | 0 |

Derived replay coverage: **15/16**, with `container-image` uncovered (zero members). This is not a claim of freshly executing the graders.

## Located members — 18

Paths and line numbers are relative to the frozen lane tree. Every row below agrees with its ledger row. Observation text is retained as a locator/prefix, not a fresh execution claim.

| Member | Tracked receipt | Subject shape @ line | Verdict @ line | Observation prefix | Agreement |
|---|---|---|---|---|---|
| build-pmars | `corpus/evidence/round38/build-pmars-probe.txt` | `tb2-header` @ 1 | `cases` @ 4 | `CASE empty-tree predicted=fail observed=fail tests=FFFF predicted_tests=FFFF match=yes violates=from-source,no-x11,debian-source,extract-to-app,install-path,res` | agree |
| circuit-fibsqrt | `corpus/evidence/round42/fibsqrt-probe.txt` | `tb2-header` @ 1 | `cases` @ 7 | `CASE nop predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same violates=output-function,example-208,example-20000 -- the shipped exa` | agree |
| configure-git-webserver | `corpus/evidence/round37/git-webserver-probe.txt` | `tb2-header` @ 1 | `cases` @ 5 | `CASE no-server tools=curl predicted=fail observed=fail match=yes -- verify.sh:57-59 — nothing listens on :8080, curl reports 000, the 200 branch is skipped` | agree |
| constraints-scheduling | `corpus/evidence/round41/constraints-probe.txt` | `tb2-header` @ 1 | `cases` @ 7 | `CASE nop predicted=fail observed=fail tests=FFF predicted_tests=FFF match=yes regrade=same violates=output-file test_structure_event_title_attendees_duration_wi` | agree |
| db-wal-recovery | `corpus/evidence/round40/db-wal-probe.txt` | `tb2-header` @ 1 | `cases` @ 6 | `CASE empty-app predicted=fail observed=fail tests=FFFFFFF predicted_tests=FFFFFFF match=yes regrade=same violates=extract-all,json-at-path,eleven-records test_r` | agree |
| feal-differential-cryptanalysis | `corpus/evidence/round43/feal-probe.txt` | `tb2-header` @ 1 | `cases` @ 10 | `CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=attack-file,recover-key5 error=ModuleNotFoundError -- no /app/at` | agree |
| feal-linear-cryptanalysis | `corpus/evidence/round44/feal-linear-probe.txt` | `tb2-header` @ 1 | `cases` @ 9 | `CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=decrypt-all,plaintexts-file,known-plaintext-attack,recover-key e` | agree |
| git-leak-recovery | `corpus/evidence/round39/git-leak-probe.txt` | `tb2-header` @ 1 | `cases` @ 5 | `CASE empty-app predicted=fail observed=fail tests=FFFFF predicted_tests=FFFFF match=yes violates=recover-secret,files-untouched,messages-untouched -- do-nothing` | agree |
| hf-model-inference | `corpus/evidence/round71/hf/receipt.txt` | `task-under-test` @ 39 | `predicate` @ 36 | `PREDICATE R71-C1 pass` | agree |
| kv-store-grpc | `corpus/evidence/round64/kvstore-probe.txt` | `receipt-header` @ 1 | `predicate` @ 66 | `PREDICATE R64-C1 pass` | agree |
| nginx-request-logging | `corpus/evidence/round70/nginx/receipt.txt` | `grader-path` @ 4 | `predicate` @ 78 | `PREDICATE R70-C1 pass` | agree |
| password-recovery | `corpus/evidence/round45/probe-run-envelope.txt` | `tb2-header` @ 3 | `cases` @ 8 | `CASE nop predicted=fail observed=fail tests=F- predicted_tests=F- match=yes regrade=same violates=write-file,one-guess,recover,forensic -- the seeded image stat` | agree |
| polyglot-c-py | `corpus/evidence/round46/polyglot-c-py-probe.txt` | `tb2-header` @ 1 | `cases` @ 9 | `CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=single-file error=FileNotFoundError -- the image seed only: WORK` | agree |
| pypi-server | `corpus/evidence/round68/pypi/receipt.txt` | `task-under-test` @ 16 | `predicate` @ 12 | `PREDICATE R68-C1 pass` | agree |
| regex-log | `corpus/evidence/round36/regex-log-probe.txt` | `capture-tree` @ 1 | `cases` @ 2 | `case=reference-lenient-days predicted=pass observed=pass match=yes assertion='-' requirement='all bullets with day 01-31 in every month (no month-length check)'` | agree |
| sqlite-with-gcov | `corpus/evidence/round65/sqlite-gcov-probe.txt` | `receipt-header` @ 1 | `predicate` @ 67 | `PREDICATE R65-C1 pass` | agree |
| torch-pipeline-parallelism | `corpus/evidence/round67/pipe/receipt.txt` | `receipt-header` @ 1 | `vectors` @ 7 | `VECTOR q1-ref exists=P no_hooks=P ws1=P ws2=P frozen=match` | agree |
| torch-tensor-parallelism | `corpus/evidence/round66/tensor/receipt.txt` | `grader-path` @ 1 | `predicate` @ 47 | `PREDICATE R66-C1 pass` | agree |

## Executed-unlocated members — 6

Every listed instrument is tracked; its quoted header is line 2. Every listed receipt is tracked, has no matching frozen subject shape, and is beneath the instrument’s round. All six ledger debt values are exactly `no-subject-stamp`; all six rows agree.

| Member | Instrument | Round | Receipt | Verdict @ line | Agreement |
|---|---|---:|---|---|---|
| cancel-async-tasks | `plans/round61_c1_cancel_probe.py` | 61 | `corpus/evidence/round61/cancel-async-probe.txt` | `predicate` @ 15 | agree |
| chess-best-move | `plans/round55_c3_chess_probe.py` | 55 | `corpus/evidence/round55/chess-best-move-probe.txt` | `predicate` @ 14 | agree |
| distribution-search | `plans/round58_c2_kl_probe.py` | 58 | `corpus/evidence/round58/kl-probe.txt` | `predicate` @ 15 | agree |
| largest-eigenval | `plans/round57_c2_eigen_probe.py` | 57 | `corpus/evidence/round57/eigen-probe.txt` | `predicate` @ 27 | agree |
| openssl-selfsigned-cert | `plans/round59_c1_openssl_probe.py` | 59 | `corpus/evidence/round59/openssl-probe.txt` | `cases` @ 2 | agree |
| protein-assembly | `plans/tb2_grader_probe.py` | 35 | `corpus/evidence/round35/tb2-grader-probe.txt` | `cases` @ 3 | agree |

Retained header and observation evidence:

- `plans/round61_c1_cancel_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `cancel-async-tasks` grader (round 61, C1).`
  - `corpus/evidence/round61/cancel-async-probe.txt:15`: `PREDICATE R61-C1 pass`
- `plans/round55_c3_chess_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `chess-best-move` grader (round 55, C3).`
  - `corpus/evidence/round55/chess-best-move-probe.txt:14`: `PREDICATE R55-C3 pass`
- `plans/round58_c2_kl_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `distribution-search` grader (round 58, C3).`
  - `corpus/evidence/round58/kl-probe.txt:15`: `PREDICATE R58-C3 pass`
- `plans/round57_c2_eigen_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `largest-eigenval` grader (round 57, C2).`
  - `corpus/evidence/round57/eigen-probe.txt:27`: `PREDICATE R57-C2 pass`
- `plans/round59_c1_openssl_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `openssl-selfsigned-cert` grader (round 59, C1).`
  - `corpus/evidence/round59/openssl-probe.txt:2`: `CASE sol predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok`
- `plans/tb2_grader_probe.py:2`: `"""Offline probe of the pinned Terminal-Bench 2.0 `protein-assembly` grader (round 35, C1).`
  - `corpus/evidence/round35/tb2-grader-probe.txt:3`: `case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'`

## Unexecuted members — 64

For **each** row, the tested file is exactly `corpus/evidence/round52/graders/<member>/tests/test_outputs.py`. SHA-256 prefixes identify its committed bytes and match the ledger’s no-blocker evidence where applicable. A dash means all four detectors were silent. Blocker-backed rows list the first matching source line and exact token; all four detectors were run and no row had competing blocker reasons.

| Member | Reason | Detector line/token | SHA-256 prefix | Agreement |
|---|---|---|---|---|
| adaptive-rejection-sampler | unattempted | — | `547dc6e107f034f4` | agree |
| bn-fit-modify | unattempted | — | `364069f893e336a0` | agree |
| break-filter-js-from-html | browser-required | 7: `selenium` | `31ba6a0baac550de` | agree |
| build-cython-ext | unattempted | — | `6549f1a8e04b6163` | agree |
| build-pov-ray | unattempted | — | `64d6ce107503714a` | agree |
| caffe-cifar-10 | unattempted | — | `10bc2d83f1a42180` | agree |
| cobol-modernization | unattempted | — | `009180a7092583fc` | agree |
| code-from-image | unattempted | — | `b9b7cb0033116df8` | agree |
| compile-compcert | unattempted | — | `f4cf5200a8011eef` | agree |
| count-dataset-tokens | unattempted | — | `5c11065dc97e9266` | agree |
| crack-7z-hash | unattempted | — | `f18d7565f6907274` | agree |
| custom-memory-heap-crash | unattempted | — | `4e1cb33f777fa7fb` | agree |
| dna-assembly | unattempted | — | `5c2d0fd2e5f63032` | agree |
| dna-insert | unattempted | — | `5bf0651b48969968` | agree |
| extract-elf | unattempted | — | `825569115217f1ce` | agree |
| extract-moves-from-video | unattempted | — | `565a7617602f33c0` | agree |
| filter-js-from-html | browser-required | 12: `selenium` | `6b43e99fb1c47792` | agree |
| financial-document-processor | unattempted | — | `978f506ad5c1bfaf` | agree |
| fix-code-vulnerability | unattempted | — | `c006a5de95b69bd7` | agree |
| fix-git | unattempted | — | `a8a6f51eb0d7c4eb` | agree |
| fix-ocaml-gc | unattempted | — | `e6031cd07c9962f0` | agree |
| gcode-to-text | unattempted | — | `6b049dc626aa103b` | agree |
| git-multibranch | unattempted | — | `f03c6867663b8e8f` | agree |
| gpt2-codegolf | unattempted | — | `6232bb719c5a4ce0` | agree |
| headless-terminal | candidate-library-required | 8: `sys.path.append("/app"` | `c6998195e29efb64` | agree |
| install-windows-3.11 | vm-required | 16: `/app/isos/` | `b352e344a1453e6a` | agree |
| large-scale-text-editing | unattempted | — | `f5e69f4fedeefa23` | agree |
| llm-inference-batching-scheduler | unattempted | — | `80b06b7c4ba0db28` | agree |
| log-summary-date-ranges | unattempted | — | `2fc06a6ce1944ad8` | agree |
| mailman | unattempted | — | `86ff052aeb063430` | agree |
| make-doom-for-mips | unattempted | — | `f1748ff20bfd670a` | agree |
| make-mips-interpreter | unattempted | — | `f1748ff20bfd670a` | agree |
| mcmc-sampling-stan | unattempted | — | `07e877edc933e3a9` | agree |
| merge-diff-arc-agi-task | unattempted | — | `2754ba6c5c5f75c9` | agree |
| model-extraction-relu-logits | candidate-library-required | 10: `sys.path.append("/app"` | `e5189c7eb9942ede` | agree |
| modernize-scientific-stack | unattempted | — | `0c24195ff4652776` | agree |
| mteb-leaderboard | unattempted | — | `b28f8fc8b7614801` | agree |
| mteb-retrieve | unattempted | — | `e4e6b21fed6662ad` | agree |
| multi-source-data-merger | unattempted | — | `a070888930cf829a` | agree |
| overfull-hbox | unattempted | — | `09756f87d1a29df5` | agree |
| path-tracing | unattempted | — | `572e68b2843191d2` | agree |
| path-tracing-reverse | unattempted | — | `c4477b901887dcbc` | agree |
| polyglot-rust-c | unattempted | — | `baed5e4d0cc0e580` | agree |
| portfolio-optimization | candidate-library-required | 38: `sys.path.append("/app"` | `800fc762b0a107b1` | agree |
| prove-plus-comm | unattempted | — | `02df5d8f2ab15eb9` | agree |
| pytorch-model-cli | unattempted | — | `370702c57a4e0c85` | agree |
| pytorch-model-recovery | unattempted | — | `5d4d57c43e6913bf` | agree |
| qemu-alpine-ssh | unattempted | — | `83ccb4bdcd259b34` | agree |
| qemu-startup | unattempted | — | `5af542dce4a1c853` | agree |
| query-optimize | external-db-required | 10: `DB_PATH = Path(` | `2068ae80c57af8d5` | agree |
| raman-fitting | unattempted | — | `171fae772ccf262a` | agree |
| regex-chess | unattempted | — | `4983c44d21c56dd8` | agree |
| reshard-c4-data | unattempted | — | `7c3e934692e274d7` | agree |
| rstan-to-pystan | unattempted | — | `d740077bc8f6f9df` | agree |
| sam-cell-seg | unattempted | — | `908c4b6aa44e12b6` | agree |
| schemelike-metacircular-eval | unattempted | — | `fbb84e3c0c2f72ed` | agree |
| sparql-university | unattempted | — | `ecf15840fc14f1ee` | agree |
| sqlite-db-truncate | unattempted | — | `8f5bc11018687d8c` | agree |
| train-fasttext | unattempted | — | `ca645971f6b4ac2f` | agree |
| tune-mjcf | unattempted | — | `3f20e17eb16bb51e` | agree |
| video-processing | unattempted | — | `09b32dd6eb55db1c` | agree |
| vulnerable-secret | unattempted | — | `f2b65f63ac81acd1` | agree |
| winning-avg-corewars | unattempted | — | `252f78e5ce87ae3c` | agree |
| write-compressor | unattempted | — | `809f486053e3ffbc` | agree |

## Disagreements, limits, tools and cleanup

- **DISAGREE = []**. No discrepant row exists for which to provide a reproducer; the retained extractor reproduces the full row-by-row comparison.
- This report validates the frozen receipt and blocker-byte criteria, not the real availability of a browser/VM/database/library and not grader behavior today. The six unlocated rows retain provenance debt; they are not promoted to located executions.
- No tools installed or upgraded. Used existing Git and Python. LSP tooling is not exposed in this seat; no supported-symbol definition/reference/refactor was needed for text-receipt extraction.
- No builds, tests, linters, formatters, counter imports, commits, pushes, external-state changes, or peer dispatches. No blockers.
- Only the exclusive report survives. The clone, extractor and generated JSON are removed from seat scratch after retaining the extractor below. Source and evidence remain reproducible from the frozen commit.

## Retained independent extractor

Source SHA-256: `0b6beadaae41d2086167d2e9a423223c41805b69248299b8f07ad6ee0a803a70`. Save this code as `extract.py` beside a `clone/` at the frozen revision; run `python3 extract.py`. It writes only a sibling `derived.json` under scratch.

<!-- BEGIN INDEPENDENT EXTRACTOR -->
```python
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).parent / 'clone'
REV = '5d6843134017780c045e92eed4e83264188a7d47'
def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])
assert git('rev-parse', 'HEAD').decode().strip() == REV
tracked = git('ls-tree', '-r', '--name-only', REV).decode().splitlines()
def text(path):
    return (ROOT / path).read_bytes().decode('utf-8', errors='replace')
classes = {}
for line in text('corpus/evidence/round62/class-survey.txt').splitlines():
    match = re.fullmatch(r'CLASS (\S+) count=(\d+) members=(\S+)', line)
    if match:
        name, count, csv = match.groups()
        classes[name] = [] if csv == '-' else csv.split(',')
        assert len(classes[name]) == int(count)
members = sorted(set().union(*map(set, classes.values())))
member_classes = {m: sorted(c for c, ms in classes.items() if m in ms) for m in members}
patterns = {
    'tb2-header': r'^# tb2 (?P<member>[\w-]+) grader probe',
    'receipt-header': r'^# R\d+-C\d+ receipt -- TB2 (?P<member>[\w-]+) grader offline',
    'grader-path': r'^GRADER .*corpus/evidence/round52/graders/(?P<member>[\w-]+)/tests/',
    'task-under-test': r'^TASK-UNDER-TEST (?P<member>[\w-]+)$',
    'capture-tree': r'^grader=corpus/evidence/round\d+/tb2-(?P<member>[\w-]+)/',
}
observations = [('predicate', r'^PREDICATE R\d+-C\d+ pass'), ('vectors', r'^VECTOR '), ('cases', r'^(?:CASE |case=)')]
receipts = {}
located = collections.defaultdict(list)
for path in tracked:
    if not path.startswith('corpus/evidence/'):
        continue
    body = text(path)
    hits = []
    for shape, regex in patterns.items():
        for match in re.finditer(regex, body, re.MULTILINE):
            if match['member'] in member_classes:
                hits.append({'member': match['member'], 'shape': shape, 'line': body[:match.start()].count('\n') + 1, 'stamp': match.group()})
    obs = next(((form, match) for form, regex in observations if (match := re.search(regex, body, re.MULTILINE))), None)
    if obs:
        form, match = obs
        receipt = {'path': path, 'subjects': hits, 'verdict': form, 'observation_line': body[:match.start()].count('\n') + 1, 'observation': body[match.start():].splitlines()[0]}
        receipts[path] = receipt
        subjects = {h['member'] for h in hits}
        if len(subjects) == 1:
            member = next(iter(subjects))
            located[member].append(receipt)
instruments = collections.defaultdict(list)
for path in tracked:
    if not (path.startswith('plans/') and path.endswith('.py')):
        continue
    if path == 'plans/round79_c1_population_ledger.py':
        continue
    lines = text(path).splitlines()
    if len(lines) < 2:
        continue
    header = lines[1]
    named = [m for m in members if re.search(r'(?<![\w-])' + re.escape(m) + r'(?![\w-])', header)]
    rounds = re.findall(r'(?:round[ -]|R)(\d+)', header, re.IGNORECASE)
    if len(named) == 1 and rounds:
        member = named[0]
        round_number = int(rounds[0])
        instruments[member].append({'instrument': path, 'round': round_number, 'header': header})
unlocated = {}
for member in members:
    if member in located:
        continue
    possibilities = []
    for instrument in instruments[member]:
        if 'probe' not in instrument['header'].lower():
            continue
        for path, receipt in receipts.items():
            if path.startswith(f"corpus/evidence/round{instrument['round']}/") and not receipt['subjects']:
                possibilities.append({**instrument, 'receipt': receipt})
    if possibilities:
        unlocated[member] = possibilities
blockers = {
    'browser-required': r'selenium|webdriver\.(?:Chrome|Firefox)|chromedriver',
    'vm-required': r'qemu-system|qemu-img|/app/isos/|win311',
    'external-db-required': r'GOLDEN_SQL_PATH|/tests/golden\.sql|DB_PATH = Path\(',
    'candidate-library-required': r'sys\.path\.append\("/app"',
}
unexecuted = {}
for member in members:
    if member in located or member in unlocated:
        continue
    path = f'corpus/evidence/round52/graders/{member}/tests/test_outputs.py'
    assert path in tracked, path
    body = text(path)
    hits = []
    for reason, regex in blockers.items():
        if match := re.search(regex, body):
            hits.append({'reason': reason, 'line': body[:match.start()].count('\n') + 1, 'match': match.group()})
    unexecuted[member] = {'reason': hits[0]['reason'] if hits else 'unattempted', 'detector_hits': hits, 'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
# Only now load the ledger: it did not select any derived status or reason.
ledger = json.loads(text('plans/grader-population-ledger.json'))['members']
disagree = []
comparison = {}
for member in sorted(set(members) | set(ledger)):
    errors = []
    row = ledger.get(member, {})
    if member not in member_classes:
        errors.append('extra-member')
    elif row.get('classes') != member_classes[member]:
        errors.append('classes')
    expected = 'executed' if member in located else 'executed-unlocated' if member in unlocated else 'unexecuted'
    if row.get('status') != expected:
        errors.append('status')
    if expected == 'executed':
        candidates = [r for r in located[member] if r['path'] == row.get('receipt')]
        if not candidates:
            errors.append('receipt')
        elif not any(h['shape'] == row.get('subject') for h in candidates[0]['subjects']):
            errors.append('subject')
        elif candidates[0]['verdict'] != row.get('verdict'):
            errors.append('verdict')
        receipt_round = re.match(r'corpus/evidence/round(\d+)/', row.get('receipt', ''))
        if receipt_round and row.get('round') != int(receipt_round[1]):
            errors.append('round')
    elif expected == 'executed-unlocated':
        if not any(p['instrument'] == row.get('instrument') and p['round'] == row.get('round') and p['receipt']['path'] == row.get('receipt') for p in unlocated[member]):
            errors.append('instrument/round/receipt')
        if row.get('debt') != 'no-subject-stamp':
            errors.append('debt')
    elif member in unexecuted and row.get('reason') != unexecuted[member]['reason']:
        errors.append('reason')
    if member in unexecuted:
        derived = unexecuted[member]
        evidence = row.get('evidence', '')
        if derived['detector_hits']:
            if not evidence or evidence not in ' '.join(text(derived['path']).split()):
                errors.append('evidence')
        elif evidence != f"no-blocker: tests/test_outputs.py sha256={derived['sha256'][:16]}":
            errors.append('evidence')
    comparison[member] = {'status': expected, 'errors': errors}
    if errors:
        disagree.append({'member': member, 'fields': errors})
result = {'rev': REV, 'counts': {'classes': len(classes), 'members': len(members), 'pairs': sum(map(len, classes.values())), 'executed': len(located), 'unlocated': len(unlocated), 'unexecuted': len(unexecuted)}, 'located': dict(located), 'unlocated': unlocated, 'unexecuted': unexecuted, 'histogram': dict(collections.Counter(r['reason'] for r in unexecuted.values())), 'classes': classes, 'comparison': comparison, 'disagree': disagree, 'scanned_tracked_evidence': sum(p.startswith('corpus/evidence/') for p in tracked)}
output = Path(__file__).parent / 'derived.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('counts', 'histogram', 'disagree', 'scanned_tracked_evidence')}, indent=2))
print('LOCATED', ','.join(sorted(located)))
print('UNLOCATED', ','.join(sorted(unlocated)))
print('INSTRUMENTS', json.dumps(dict(instruments), indent=2))
```
<!-- END INDEPENDENT EXTRACTOR -->

## Self-evaluation

| Axis | Score | Evidence / improvement |
|---|---:|---|
| Accuracy | 4 | Observed zero comparison differences; does not independently re-run historical graders. |
| Completeness | 5 | All 88 rows, 16 class counts, 18 subject/verdict receipts, 6 instrument/round receipts, 64 detector outcomes retained. |
| Clarity | 4 | Long report required by per-row evidence; tables separate statuses. |
| Actionability | 5 | Frozen revision, executed commands and complete independent extractor retained after cleanup. |
| Conciseness | 4 | Full extractor adds length but preserves replayability after mandatory scratch deletion. |

Overall: 4.4/5. Improvements by impact: preserve the narrow interpretation (receipt-byte verification, not fresh grader execution); use the summary for quick review and tables/source only for audit. Would the user agree? The requested independent split and per-row evidence are present; no broader behavioral claim is made.
