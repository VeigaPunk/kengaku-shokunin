# ScoutR88 — member recon and class arithmetic for `fix-git` (R88-C1)

Read-only seat. Nothing outside `.ufo/waves/round-88/w1/ScoutR88/` and
`/fast/scratch/hyaku/kengaku-r88/ScoutR88/` was written; no production file was edited.
No tool was installed or upgraded on this host (nothing in the task needed one), so the
operator tooling directive produced no installs to record.

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`, HEAD `d9cb2b40`.
Every git call below is read-only (`log`, `show`, `diff`, `merge-base --is-ancestor`,
`rev-parse`, `cat-file`).

Frozen inputs used for cross-checks:
claims/case table `0220c2f9f356bf032bd58b4ed39e32f6e26fa440`; instruments `1f267d4b6f60f1137ebf8b905d318bd2d9894e99`;
frontier files `da16ec39cf28d89b0a6a35ce8cacb630bad1de19`; measured tip `7fcc680b86599eedd63e862a061848298428b3cc`;
base `801b903af6412cb424209a60b3a52e56c3532866`.

---

## 1. The captured grader: every `def test_*`, its acceptance predicate, and its imports

Capture: `corpus/evidence/round52/graders/fix-git/tests/test_outputs.py` (39 lines).
Byte identity across the lane: `sha256sum` = `a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3`,
equal to the frozen `subject_sha` in `plans/round88-cases.json` (`"subject_sha"` field) and to
the `S277` row in `corpus/SOURCES.md`. At the measured tip the blob is unchanged:
`git show 7fcc680b:corpus/evidence/round52/graders/fix-git/tests/test_outputs.py | cmp - corpus/evidence/round52/graders/fix-git/tests/test_outputs.py` → `IDENTICAL`.
The capture dir holds exactly two files, one Python grader plus its runner script:
`corpus/evidence/round52/graders/fix-git/tests/test_outputs.py` and `.../tests/test.sh`.

### 1.1 Imports

| line | import | stdlib? | evidence |
|---|---|---|---|
| 3 | `import hashlib` | **stdlib** | `python3 -c "import sys; print('hashlib' in sys.stdlib_module_names)"` → `True`; `sys.stdlib_module_names` contains `hashlib` (also `_hashlib` as the C accelerator) |

That is the **only** import in the file. There is no `pytest` import in the grader module and no
third-party dependency of any kind — which is why the probe can load it with `runpy` and call the
test functions directly (`plans/round88_fixgit_probe.py` `HARNESS`, lines 59–79: it parses the file with
`ast`, takes the module-level `def test_*` names, `runpy.run_path`s the module and calls each function,
classifying `AssertionError`/`FileNotFoundError` as `F` and any other exception as `E`).
The captured `tests/test.sh` (the TB2 runner) does use `uvx … pytest==8.4.1`, but that is the runner,
not the grader module.

### 1.2 Every `def test_*`, with line ranges and the literal acceptance predicate

Quoted literally with line numbers from the capture (`cat -n`):

```
    3  import hashlib
    4
    5
    6  def hash_file(file_path):
    7      with open(file_path, "rb") as file:
    8          file_hash = hashlib.md5(file.read().strip()).hexdigest()
    9      return file_hash
   10
   11
   12  def check_file_hash(file_path, expected_hash):
   13      assert hash_file(file_path) == expected_hash, (
   14          f"File {file_path} is not in the correct state"
   15      )
   16
   17
   18  def compare_file_hashes(path_a, path_b):
   19      assert hash_file(path_a) == hash_file(path_b), (
   20          f"File {path_a} is not in the correct state"
   21      )
   22
   23
   24  def test_about_file():
   25      """
   26      Test that the about file content is correct
   27      """
   28      ABOUT_FILE_PATH_OLD = "/app/resources/patch_files/about.md"
   29      ABOUT_FILE_PATH_NEW = "/app/personal-site/_includes/about.md"
   30      compare_file_hashes(ABOUT_FILE_PATH_OLD, ABOUT_FILE_PATH_NEW)
   31
   32
   33  def test_layout_file():
   34      """
   35      Test that the layout file content is correct
   36      """
   37      LAYOUT_FILE_PATH_OLD = "/app/resources/patch_files/default.html"
   38      LAYOUT_FILE_PATH_NEW = "/app/personal-site/_layouts/default.html"
   39      compare_file_hashes(LAYOUT_FILE_PATH_OLD, LAYOUT_FILE_PATH_NEW)
```

| `def test_*` | line range | acceptance predicate (quoted) | leg in the frozen table |
|---|---|---|---|
| `test_about_file` | **24–30** | `compare_file_hashes(ABOUT_FILE_PATH_OLD, ABOUT_FILE_PATH_NEW)` (line 30) → `assert hash_file(path_a) == hash_file(path_b), (` (line 19) → `hashlib.md5(file.read().strip()).hexdigest()` (line 8) | leg 1 of each case (`about`) |
| `test_layout_file` | **33–39** | `compare_file_hashes(LAYOUT_FILE_PATH_OLD, LAYOUT_FILE_PATH_NEW)` (line 39) → same `assert` at line 19 | leg 2 of each case (`layout`) |

Supporting helpers, quoted:

* `hash_file` — lines **6–9**. `hashlib.md5(file.read().strip()).hexdigest()` (line 8). **It strips the
  bytes before hashing.**
* `compare_file_hashes` — lines **18–21**. The only assertion any test reaches.
* `check_file_hash` — lines **12–15**. **Dead code in this capture**: no `def test_*` calls it and
  nothing else in the file references it. The frozen table's two legs both go through
  `compare_file_hashes`, so `check_file_hash` contributes no observed leg. (Observation, not a defect:
  the capture is upstream TB2 bytes and is byte-pinned; the `S277` row scopes the source to the
  md5-pair predicates and does not claim `check_file_hash` is exercised.)

### 1.3 The `hash_file` strip is exercised by exactly one frozen case

`plans/round88-cases.json` case id `"trailing-whitespace-tolerance"` (case-table line **60**):

```json
  {
   "id": "trailing-whitespace-tolerance",
   "predicted": "P/P",
   "why": "control: hash_file strips before hashing, so trailing whitespace on the new files does not change the digest",
```

It stages `"personal-site/_includes/about.md": "about-old-v1\n   \t\n"` and
`"personal-site/_layouts/default.html": "layout-old-v1\n  \n"` — the trailing whitespace is stripped by
line 8, so both digests match their OLD counterparts and both legs are `P`. This is the **only** frozen
case whose prediction depends on the strip. The other seven (`exact`, `about-content-mismatch`,
`layout-content-mismatch`, `both-content-mismatch`, `about-new-absent`, `about-new-is-dir`,
`layout-old-is-dir`) are decided by content inequality, a missing path, or a directory path.

Cross-check of the observed vector against the receipt (`corpus/evidence/round88/fix-git-probe.txt`,
observation block): all eight cases are `predicted == observed`, `cases=8 legs=16 mismatches=0`,
`PREDICATE R88-PROBE pass`. The receipt's `SUBJECT_SHA` equals the capture's `sha256sum` above.

---

## 2. The member's ledger row at both revisions, and the per-class executed/total at both

### 2.1 The `fix-git` ledger row

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 801b903af6412cb424209a60b3a52e56c3532866:plans/grader-population-ledger.json`
→ member `fix-git`:

```json
"fix-git": {
  "classes": ["crypto-credential", "file-artifact"],
  "evidence": "no-blocker: tests/test_outputs.py sha256=a8a6f51eb0d7c4eb",
  "reason": "unattempted",
  "status": "unexecuted"
}
```

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 7fcc680b86599eedd63e862a061848298428b3cc:plans/grader-population-ledger.json`
→ member `fix-git`:

```json
"fix-git": {
  "classes": ["crypto-credential", "file-artifact"],
  "evidence": "no-blocker: tests/test_outputs.py sha256=a8a6f51eb0d7c4eb",
  "receipt": "corpus/evidence/round88/fix-git-probe.txt",
  "round": 88,
  "status": "executed",
  "subject": "tb2-header",
  "verdict": "cases"
}
```

The diff between the two revisions is exactly this one row (plus nothing else):
`git diff 801b903a 7fcc680b -- plans/grader-population-ledger.json` → `1 file changed, 5 insertions(+), 2 deletions(-)`,
and the hunk is the `fix-git` block (`"reason": "unattempted", "status": "unexecuted"` →
`"receipt"/"round"/"status"/"subject"/"verdict"`). The classes list is unchanged (`crypto-credential`,
`file-artifact`), which matches `corpus/evidence/round62/class-survey.txt` lines 7 and 10
(`CLASS file-artifact count=76 members=…,fix-git,…`; `CLASS crypto-credential count=12 members=…,fix-git,…`).

### 2.2 Per-class executed/total at both revisions — my own count

Command (run from the lane root; read-only):

```
python3 - <<'EOF'
import json,subprocess
def ledger(rev):
    raw=subprocess.run(['git','show',f'{rev}:plans/grader-population-ledger.json'],capture_output=True,text=True).stdout
    return json.loads(raw)['members']
for rev in ['801b903af6412cb424209a60b3a52e56c3532866','7fcc680b86599eedd63e862a061848298428b3cc']:
    ms=ledger(rev)
    rows=sum(1 for v in ms.values() if v.get('status')=='executed')
    print(rev[:10], 'executed_rows=%d'%rows)
    for c in ['crypto-credential','file-artifact']:
        tot=[k for k,v in ms.items() if c in v.get('classes',[])]
        ex=[k for k in tot if ms[k].get('status')=='executed']
        print('   %-18s executed %d of %d' % (c,len(ex),len(tot)))
EOF
```

Output:

```
801b903a executed_rows=31
   crypto-credential  executed 2 of 12
   file-artifact      executed 23 of 76
7fcc680b executed_rows=32
   crypto-credential  executed 3 of 12
   file-artifact      executed 24 of 76
```

Definition used: a member is *executed* iff `status == "executed"`. This is the same rule the frozen
counter uses (`plans/round88_c1_replay.py` lines 256–257: `sum(1 for v in json.loads(raw_ledger)["members"].values() if v.get("status") == "executed")`),
so my count and the counter's `executed_rows=` field are computed the same way. No member at either
revision carries `status == "executed-unlocated"`, so the "executed **or** debt" convention gives the
same numbers (checked separately).

The class rosters:

* `crypto-credential`, 2 of 12 at base → `constraints-scheduling`, `openssl-selfsigned-cert`; at tip
  → the same two **plus `fix-git`** (3 of 12).
* `file-artifact`, 23 of 76 at base → `build-pmars`, `cancel-async-tasks`, `chess-best-move`,
  `circuit-fibsqrt`, `code-from-image`, `constraints-scheduling`, `db-wal-recovery`,
  `feal-linear-cryptanalysis`, `gcode-to-text`, `git-leak-recovery`, `kv-store-grpc`,
  `log-summary-date-ranges`, `mteb-retrieve`, `nginx-request-logging`, `openssl-selfsigned-cert`,
  `password-recovery`, `protein-assembly`, `raman-fitting`, `regex-log`, `sqlite-db-truncate`,
  `torch-pipeline-parallelism`, `torch-tensor-parallelism`, `vulnerable-secret`; at tip the same list
  **plus `fix-git`** (24 of 76). The only delta between the two rosters is `fix-git`.

Class history of the unmoved class, for context (per-revision ledger counts, oldest→newest, computed
from `git log -- plans/grader-population-ledger.json`):
`crypto-credential` was `1/12` at the round-79 freeze (`5d684313`), `2/12` from round 80
(`6669fe72`) through round 87 (`10de494d`), and `3/12` at round 88 (`7fcc680b`). So the class last
moved at round 80 and stood still across the eight intervening ledger revisions (`2fe3d8e6` r81,
`0c56b4eb4` r83, `8a61bce1b` r84, `ce5b9ef8d`/`dc02d8182`/`35b1e4e09` r85, `f357e4c16` r86,
`10de494d1` r87) — consistent with the frozen
claim's "no recent round has moved `crypto-credential`" and with `corpus/lessons/round-88.md` line 11
("the first `crypto-credential`-class member executed since round 41/80").

---

## 3. Independent verification of the three frozen claim sentences

The frozen sentences (`plans/round-88-claims.md`, R88-C1 "After (measured tip)"):
"executed 31 → 32; `crypto-credential` 2 of 12 → 3 of 12; `file-artifact` 23 of 76 → 24 of 76."

**All three confirmed by my own count** (command and output in §2.2):

| frozen sentence | my count | verdict |
|---|---|---|
| executed 31 → 32 | `executed_rows=31` at `801b903a`, `executed_rows=32` at `7fcc680b` | **confirmed** |
| `crypto-credential` 2 of 12 → 3 of 12 | 2 of 12 at base, 3 of 12 at tip; delta = `fix-git` | **confirmed** |
| `file-artifact` 23 of 76 → 24 of 76 | 23 of 76 at base, 24 of 76 at tip; delta = `fix-git` | **confirmed** |

Independent corroboration from the instrument itself, run read-only against the two revisions
(transcripts kept in this seat dir as `counter-base.txt` and `counter-tip.txt`):

```
$ python3 plans/round88_c1_replay.py --lane . --rev 801b903af6412cb424209a60b3a52e56c3532866 --work <scratch>
DEFECT L4-table plans/round88-cases.json absent at measured
DEFECT L1-receipt corpus/evidence/round88/fix-git-probe.txt absent at 801b903af641
DEFECT L7-ledger row {"classes": ["crypto-credential", "file-artifact"], … "status": "unexecuted"}
TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3
PREDICATE R88-C1 fail
(exit 1)

$ python3 plans/round88_c1_replay.py --lane . --rev 7fcc680b86599eedd63e862a061848298428b3cc --work <scratch>
TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0
PREDICATE R88-C1 pass
(exit 0)
```

Both match the frozen claim's own before/after blocks (`defects=3` / exit 1 at base, `defects=0` /
exit 0 at tip), and the counter's `executed_rows` field equals my independent count at both ends.

Two adjacent consistency notes (not defects in the frozen elements, reported for the L1's awareness):

1. **The `SKILL.md` class cell was stale at base, and the tip reconciled it.** At base,
   `SKILL.md`'s `file-artifact` row read "executed 22 of 76 (round 86 adds `raman-fitting`; …)" — i.e.
   one behind the ledger's 23 of 76, because round 87 added `mteb-retrieve` to the ledger without
   updating that cell. At the tip the same row reads "executed 24 of 76 (round 88 adds `fix-git`;
   round 87 adds `mteb-retrieve`; …)". So the frozen sentence "file-artifact 23 of 76 → 24 of 76" is
   ledger-scoped and true; the base `SKILL.md` prose was the stale artefact and round 88 fixed it.
   `git diff 801b903a 7fcc680b -- SKILL.md` shows exactly three class rows touched
   (`file-artifact`, `crypto-credential`, `filesystem-metadata`).
2. **`SKILL.md`'s `filesystem-metadata` row at the tip gains the `fix-git` receipt pointer without a
   count change.** The tip row is
   `| filesystem-metadata | 10 | executed 2 of 10 | … | corpus/evidence/round59/openssl-probe.txt, plans/round59_c1_openssl_probe.py; corpus/evidence/round88/fix-git-probe.txt |`.
   `fix-git` is **not** in that class: `corpus/evidence/round62/class-survey.txt` line 13 lists
   `CLASS filesystem-metadata count=10 members=caffe-cifar-10,compile-compcert,hf-model-inference,llm-inference-batching-scheduler,modernize-scientific-stack,openssl-selfsigned-cert,pytorch-model-recovery,reshard-c4-data,train-fasttext,tune-mjcf`
   (no `fix-git`), the ledger row's `classes` are `["crypto-credential","file-artifact"]`, and the count
   correctly stays at 2 of 10 (the two executed members are `hf-model-inference` and
   `openssl-selfsigned-cert`). Every other receipt pointer in that column names a member of the row's
   own class. Charitable reading: the `fix-git` probe does stage files inside a sandbox and its case
   table contains directory-path cases (`about-new-is-dir`, `layout-old-is-dir`) that raise
   `IsADirectoryError`, so the pointer is not nonsensical. Strict reading: as a "receipt of record for
   this class" column it cites a member of no class in the row, and the `R63-C2` depth gate does not
   check receipt-pointer membership (`python3 plans/round63_gate_checks.py depth --skill SKILL.md
   --receipt corpus/evidence/round62/class-survey.txt --root .` → `class_match=True count_mismatch=0`,
   the same verdict as against the base `SKILL.md`, so the gate is silent on it).
   **Flagged, not edited** — the `SKILL.md` cell is a production file and outside this seat's scope.

---

## 4. Every UNEXECUTED member with a single-file, stdlib-only captured grader

Universe: the 88-member population ledger at base (`801b903a`); `status != "executed"` → 57 members.
Capture root `corpus/evidence/round52/graders/<member>/`. "Single-file" = exactly one `.py` under
`tests/`; "stdlib-only" = every import root in that file is in `sys.stdlib_module_names`.

Command (run from the lane root; read-only):

```
python3 - <<'EOF'
import ast,os,json,sys
base='corpus/evidence/round52/graders'
led=json.load(open('/fast/scratch/hyaku/kengaku-r88/ScoutR88/ledger_base.json'))['members']
std=set(sys.stdlib_module_names)
for k,v in sorted(led.items()):
    if v.get('status')=='executed': continue
    d=os.path.join(base,k,'tests')
    pys=[f for f in sorted(os.listdir(d)) if f.endswith('.py')]
    if len(pys)!=1: continue
    src=open(os.path.join(d,pys[0])).read(); t=ast.parse(src)
    imports=set()
    for n in ast.walk(t):
        if isinstance(n,ast.Import):
            for a in n.names: imports.add(a.name.split('.')[0])
        elif isinstance(n,ast.ImportFrom):
            imports.add(n.module.split('.')[0] if n.module else 'REL')
    if imports-std: continue
    modtests=[n.name for n in t.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
    nasserts=sum(1 for n in ast.walk(t) if isinstance(n,ast.Assert))
    dup=os.path.isdir(os.path.join(base,k,'environment','tests'))
    print('%-30s tests=%d asserts=%d loc=%d dupcopy=%s classes=%s' %
          (k,len(modtests),nasserts,src.count('\n')+1,dup,','.join(v.get('classes',[]))))
EOF
```

Output — **26** unexecuted members qualify:

| member | tests | asserts | loc | duplicate `environment/tests` copy | classes (ledger) |
|---|---|---|---|---|---|
| `caffe-cifar-10` | 6 | 25 | 180 | no | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec |
| `cobol-modernization` | 3 | 8 | 95 | no | file-artifact, subprocess-exec |
| `compile-compcert` | 3 | 18 | 117 | no | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec |
| `count-dataset-tokens` | 1 | 1 | 14 | no | file-artifact |
| `crack-7z-hash` | 2 | 2 | 28 | no | file-artifact |
| `dna-assembly` | 1 | 21 | 203 | no | file-artifact, numeric-band, stdout-inspection, subprocess-exec |
| `dna-insert` | 1 | 12 | 103 | no | file-artifact, numeric-band, stdout-inspection, subprocess-exec |
| `extract-elf` | 2 | 9 | 393 | no | file-artifact, serialization-schema, subprocess-exec |
| `extract-moves-from-video` | 2 | 2 | 361 | no | file-artifact |
| **`fix-git`** | **2** | **2** | **40** | no | **crypto-credential, file-artifact** |
| `fix-ocaml-gc` | 1 | 2 | 20 | no | file-artifact |
| `git-multibranch` | 1 | 1 | 100 | no | file-artifact, network-service, shell-exec |
| `gpt2-codegolf` | 1 | 5 | 47 | no | file-artifact, stdout-inspection, subprocess-exec |
| `large-scale-text-editing` | 5 | 21 | 222 | **yes** | crypto-credential, file-artifact, stdout-inspection, subprocess-exec |
| `mcmc-sampling-stan` | 6 | 19 | 181 | no | file-artifact, stdout-inspection, subprocess-exec |
| `merge-diff-arc-agi-task` | 5 | 12 | 86 | no | file-artifact, git-plumbing, serialization-schema, stdout-inspection, subprocess-exec |
| `mteb-leaderboard` | 2 | 3 | 16 | no | file-artifact |
| `polyglot-rust-c` | 1 | 2 | 47 | no | shell-exec, stdout-inspection, subprocess-exec |
| `prove-plus-comm` | 4 | 7 | 36 | no | file-artifact, subprocess-exec |
| `qemu-alpine-ssh` | 1 | 1 | 42 | no | stdout-inspection, subprocess-exec |
| `qemu-startup` | 1 | 1 | 61 | no | file-artifact, shell-exec |
| `query-optimize` | 6 | 23 | 248 | no | crypto-credential, db-state, file-artifact, timing-wall |
| `rstan-to-pystan` | 6 | 21 | 182 | no | file-artifact, subprocess-exec |
| `schemelike-metacircular-eval` | 1 | 1 | 221 | **yes** | file-artifact, stdout-inspection, subprocess-exec, timing-wall |
| `winning-avg-corewars` | 3 | 5 | 109 | no | crypto-credential, file-artifact, stdout-inspection, subprocess-exec |
| `write-compressor` | 3 | 8 | 74 | no | file-artifact, stdout-inspection, subprocess-exec |

"tests" counts module-level `def test_*` (the unit the frozen probe and the TB2 runner both use);
"asserts" counts `ast.Assert` nodes in the file. Cross-checked against `grep -c '^\s*assert '` and
`grep -c '^def test_'` — identical for every row (e.g. `fix-git`: 2 and 2).

Two members are disqualified from "single-file" by a second, byte-identical copy of the same grader
under `environment/tests/` (verified identical by `sha256sum`):
`large-scale-text-editing` (`f5e69f4fedeefa23…` in both places),
`schemelike-metacircular-eval` (`fbb84e3c0c2f72ed…`), and (not stdlib-only, so not in the table)
`break-filter-js-from-html` and `overfull-hbox`.

### 4.1 Was `fix-git` the cheapest such candidate carrying an unmoved class?

**Two readings, two answers. The claim's own reading: confirmed. A literal "any unmoved class"
reading: refuted, and the refutation matters for the L1's calibration.**

**Reading A — the round's own reading (the class the claim names as unmoved): CONFIRMED.**
The frozen claim says the member "carries classes `crypto-credential` and `file-artifact`; no recent
round has moved `crypto-credential`". Restricting to candidates that carry `crypto-credential`,
single-file and stdlib-only, the four survivors are `fix-git` (2 tests / 2 asserts / 40 loc),
`winning-avg-corewars` (3 / 5 / 109), `large-scale-text-editing` (5 / 21 / 222) and
`query-optimize` (6 / 23 / 248). `fix-git` is the cheapest on every axis — test count, assert count and
capture size. Disqualifying line for each rejected alternative:

* `winning-avg-corewars` — line 59–61: `result = subprocess.run(\n  [\n    "pmars",\n    "-b", …`
  It shells out to the `pmars` battle simulator and asserts win-rate thresholds (lines 44–46,
  `warriors_and_thresholds`), so its legs are not decidable from a staged file state; it also pins
  five opponent-warrior digests (lines 11–27) that must exist under `/app/warriors/`.
* `large-scale-text-editing` — line 170: `cmd = ["vim", "-Nu", "NONE", "-n", "-Es", str(INPUT), "-S", str(APPLY_SCRIPT)]`
  (and line 202 for a second `vim` invocation). It needs the external `vim` binary to execute the
  candidate's macros; it also has the duplicate `environment/tests/` copy, so it is not single-file.
* `query-optimize` — line 11: `GOLDEN_SQL_PATH = Path("/tests/golden.sql")` and line 142:
  `assert summary["solution"]["median_s"] <= 1.05 * summary["golden"]["median_s"]`.
  It needs a `/tests/golden.sql` the capture does not ship and a median-ratio **timing** threshold, so
  its legs are not freezable offline. The lane already records this: `SKILL.md`'s `db-state` row says
  "`query-optimize` stays recipe-unexecuted (a median-ratio timing threshold and a sha-pinned external
  database make its legs not freezable offline on this host)".

**Reading B — literal "any class whose executed count did not move between rounds 80 and 87":
REFUTED.**
Between `6669fe72` (round 80) and `801b903a` (round 87) the only classes that moved were
`file-artifact` (16→23), `numeric-band` (2→3) and `serialization-schema` (1→3). Twelve classes were
frozen over that window: `candidate-import` 3/6, `crypto-credential` 2/12, `db-state` 1/2,
`filesystem-metadata` 2/10, `git-plumbing` 1/3, `network-service` 4/8, `process-environment` 2/3,
`shell-exec` 1/6, `signal-delivery` 1/1, `stdout-inspection` 8/29, `subprocess-exec` 10/45,
`timing-wall` 3/9. Several of those cheaper stdlib-only single-file candidates carry a frozen class:

| candidate | tests / asserts | frozen class it carries | disqualifying line |
|---|---|---|---|
| `qemu-startup` | 1 / 1 | `shell-exec` 1/6 | line 56 `os.popen("expect -f run.exp").read()` — needs the `expect` binary and a live telnet QEMU guest on port 6665; line 58 then reads `/tmp/data.txt` written by that session |
| `qemu-alpine-ssh` | 1 / 1 | `stdout-inspection` 8/29, `subprocess-exec` 10/45 | lines 23–39: `subprocess.run(["sshpass", "-p", "password123", "ssh", … "-p", "2222", "root@localhost", "uname -r"])` — needs a live SSH server on port 2222 |
| `git-multibranch` | 1 / 1 | `network-service` 4/8, `shell-exec` 1/6 | line 96 `result = os.popen("bash verify.sh").read()`, whose script installs packages over the network (line 13 `apt-get install -y curl expect git openssh-client`) and polls `https://localhost:8443` (lines 72–73) |
| `polyglot-rust-c` | 1 / 2 | `shell-exec` 1/6, `stdout-inspection`, `subprocess-exec` | lines 24–25: `os.popen("rustc /app/polyglot/main.rs -o /app/polyglot/main")` and `os.popen("g++ -x c++ …")` — needs two external toolchains; the test then runs the produced binaries (lines 30–42) |
| `dna-assembly` | 1 / 21 | `stdout-inspection`, `subprocess-exec` | line 21 `result = subprocess.run([\n "oligotm", "-mv", "50", …` — needs the external `oligotm` primer3 binary |
| `dna-insert` | 1 / 12 | `stdout-inspection`, `subprocess-exec` | line 18 `result = subprocess.run([\n "oligotm", "-mv", "50", …` — same external binary |
| `schemelike-metacircular-eval` | 1 / 1 | `stdout-inspection`, `subprocess-exec`, `timing-wall` | line 14 `cmd = ["python3", "interp.py", test_file]` — needs the candidate's own `interp.py`/`eval.scm` in `/app`; also has the duplicate `environment/tests/` copy |
| `count-dataset-tokens` | 1 / 1 | none frozen (`file-artifact` only) | — |
| `fix-ocaml-gc` | 1 / 2 | none frozen (`file-artifact` only) | — |
| `crack-7z-hash` | 2 / 2 | none frozen (`file-artifact` only) | — |
| `extract-moves-from-video` | 2 / 2 | none frozen (`file-artifact` only) | — |
| `mteb-leaderboard` | 2 / 3 | none frozen (`file-artifact` only) | — (also already rejected in round 87 as `S276`: "same two-assert shape and file-artifact class as `mteb-retrieve` … a replay adds no class, edge or vector S275 lacks") |

So under Reading B, `fix-git` was **not** the cheapest stdlib-only single-file candidate carrying a
frozen class — `qemu-startup`, `qemu-alpine-ssh`, `git-multibranch`, `polyglot-rust-c`, `dna-assembly`,
`dna-insert` and `schemelike-metacircular-eval` are all strictly cheaper on test and assert count.
Each is rejected above on a **runtime** dependency (external binary or live service), which is a
different criterion from "stdlib-only imports" and is not stated in the frozen claim. The frozen claim
itself never asserts "cheapest" — it asserts "carries classes `crypto-credential` and `file-artifact`;
no recent round has moved `crypto-credential`", which is true, and the round-87 lesson names `fix-git`
as "the next candidate" on the grounds of "two stdlib tests, a crypto-credential class, unopened this
round, no row" (`corpus/lessons/round-87.md` line 34). That framing is exactly Reading A, and under
Reading A `fix-git` is the cheapest.

**Net:** the selection is sound and the class movement is real, but the *justification* rests on
"stdlib-only, no external runtime, fewest tests/asserts" plus "carries the class that has been frozen
since round 80" — not on "cheapest candidate carrying any frozen class". If the L1 wants to state
"cheapest" in the report, it should say *cheapest crypto-credential candidate* (Reading A), because the
broader phrasing is not supportable from the population.

---

## Findings

No defect found in any frozen element: the frozen claim sentences all reproduce under my own count,
the captured grader's bytes hash to the frozen `subject_sha` at the measured tip, the eight-case
observation vector in the receipt matches the frozen predictions case for case, and the ledger delta is
exactly the one `fix-git` row.

Two items are reported for the L1's awareness (neither is a frozen-element defect and neither was edited):

1. `SKILL.md`'s `filesystem-metadata` row at the tip adds `corpus/evidence/round88/fix-git-probe.txt` to
   its receipt-pointer column while `fix-git` is not a member of that class
   (`corpus/evidence/round62/class-survey.txt` line 13; ledger `classes` = `crypto-credential`,
   `file-artifact`) and the count correctly stays at 2 of 10. The `R63-C2` depth gate does not check
   receipt-pointer membership, so it is silent.
2. The base `SKILL.md` `file-artifact` cell read "22 of 76" against a ledger of 23 of 76 (round 87 added
   `mteb-retrieve` without updating the cell); the tip cell reconciles it to "24 of 76". The frozen
   claim's sentence is ledger-scoped and was correct throughout.

Also flagged as a scope caveat rather than a defect: "cheapest candidate carrying an unmoved class" is
true only in the narrow `crypto-credential` sense (Reading A); under the broad sense (Reading B) seven
cheaper stdlib-only single-file candidates carry a class frozen since round 80, each rejected on an
external-binary or live-service dependency.

### Commands used (all read-only)

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -3
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show <rev>:plans/grader-population-ledger.json
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 801b903a 7fcc680b -- plans/grader-population-ledger.json SKILL.md corpus/SOURCES.md
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor da16ec39 7fcc680b   # YES
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 1f267d4 7fcc680b   # YES
sha256sum corpus/evidence/round52/graders/fix-git/tests/test_outputs.py
cat -n corpus/evidence/round52/graders/fix-git/tests/test_outputs.py
python3 -c "import sys; print('hashlib' in sys.stdlib_module_names)"
python3 plans/round88_c1_replay.py --lane . --rev 801b903a… --work <scratch>   # exit 1, defects=3
python3 plans/round88_c1_replay.py --lane . --rev 7fcc680b… --work <scratch>   # exit 0, defects=0
python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .
```

No network fetch was performed by this seat; the pinned `raw.githubusercontent.com` URL was not opened
here (the `S277` row and the receipt already carry its sha256 and byte-length, and the capture matches
that sha256 locally).
