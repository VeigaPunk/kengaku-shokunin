# ScoutR85 — member-selection recon against grader bytes (read-only)

Seat: `ScoutR85` (scout, wave 1 of round 85, ONE v1 wave). L1 = `KengakuR85`.
Scope: read-only recon of `plans/grader-population-ledger.json` against the captured grader bytes in
`corpus/evidence/round52/graders/<member>/tests/test_outputs.py`. **No production file was created,
edited or deleted.** No subagent was dispatched; no `task` call was made.

Date: 2026-11-04. All paths relative to the lane repo root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless a leading `/` is given.

## 0. What the frozen claim asks (read in full, not edited)

`plans/round-85-claims.md` §R85-C1 (frozen at `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`, base
`0de45354d7aff18e4a23a348ec13de3a1f707a44`) freezes the predicate, the eight-case table, the two-leg
vector, the control set, the kill rule and the defect list. Nothing in that file was changed. The claim's
own subject pin is `sqlite-db-truncate` /
`corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`, sha256
`8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881` (`plans/round-85-claims.md` R85-C1
"Subject:" paragraph). I re-derived that digest from the bytes on disk (§2), and it matches.

**One frozen element looks wrong and is reported here rather than edited (§5, finding S-1):** the claim's
population-gate figure "`serialization-schema` class executed 0 of 9 → 1 of 9"
(`plans/round-85-claims.md`, R85-C1 "Before (BASE ...)" paragraph; echoed at
`corpus/lessons/round-85.md:100`) says the class has **9** members. The class census says **10**, and the
ledger prices all 10. The `0 of 9 → 1 of 9` arithmetic is only reachable if `db-wal-recovery` (already
executed at round 40) is excluded from the denominator. On the ledger's own numbers the class moves
**1 of 10 → 2 of 10**. I did not edit the frozen claim or the lesson.

---

## 1. The ledger's `no-blocker` evidence shape — 10 unexecuted members

### 1.1 The shape itself

`plans/grader-population-ledger.json` prices every member of the 16-class population exactly once with
three shapes (`plans/grader-population-ledger.json:910`, the `"why"` field):

```
executed             a tracked receipt whose own bytes name the member and carry execution observations
executed-unlocated   the round's probe instrument names the member and a receipt carries observations,
                     but the receipt does not locate its subject
unexecuted           no replay; a blocker reason only when a frozen detector fires over the task's
                     tests/test_outputs.py, else `unattempted`
```

The `no-blocker` note is the `unattempted` shape's evidence string. Its grammar is fixed by the gate at
`plans/round79_c1_population_ledger.py:306-312`:

```python
evidence = row.get("evidence")
if not isinstance(evidence, str) or not evidence.startswith("no-blocker:"):
    defects.append(("EVIDENCE-SHAPE", f"{m} {evidence!r}"))
    continue
want = hashlib.sha256(body.encode()).hexdigest()[:16]
if want not in evidence:
    defects.append(("EVIDENCE-SHA-MISMATCH", f"{m} body={want} evidence={evidence!r}"))
```

So `no-blocker: tests/test_outputs.py sha256=<first 16 hex>` asserts exactly two things: (a) the shape
prefix `no-blocker:` and (b) the **first 16 hex of the sha256 of the grader body**. It is a *digest
pin*, not a statement that the grader has no external dependency. The frozen detector that decides
whether a row is `unattempted` or one of the four named blockers is the four-entry `BLOCKERS` table at
`plans/round79_c1_population_ledger.py:85-90`:

```python
BLOCKERS = {
    "browser-required":            r"selenium|webdriver\.(?:Chrome|Firefox)|chromedriver",
    "vm-required":                 r"qemu-system|qemu-img|/app/isos/|win311",
    "external-db-required":        r"GOLDEN_SQL_PATH|/tests/golden\.sql|DB_PATH\s*=\s*Path\(",
    "candidate-library-required":  r"sys\.path\.append\(\s*[\"']/app",
}
```

The detector is a **four-pattern regex set over the grader body**. It never looks at a `subprocess` call,
never looks at an `import`, and never resolves a binary name. That is the whole finding of §1.3.

Population arithmetic at the current tip: 88 members, 29 `executed`, 59 `unexecuted`, 0 unaccounted,
0 unbacked, 0 understated (`plans/round79_c1_population_ledger.py` run at `--rev` HEAD: `TARGET classes=16
members=88 pairs=230 replayed=29 located=29 unlocated=0 unexecuted=59 unaccounted=0 unbacked=0
understated=0 covered=15`, `PREDICATE R79-C1 pass`). At BASE `0de45354` the same counter prints
`replayed=28 … unexecuted=60`, `PREDICATE R79-C1 pass` — so the ledger's `no-blocker` set shrank from 60
rows to 59 rows and the class-level counts moved as the claim expects.

### 1.2 The ten members, from their bytes

The `no-blocker` set has 52 rows today (59 `unexecuted` minus 7 rows carrying a named blocker reason:
`break-filter-js-from-html`, `filter-js-from-html` (browser-required), `headless-terminal`,
`model-extraction-relu-logits`, `portfolio-optimization` (candidate-library-required),
`install-windows-3.11` (vm-required), `query-optimize` (external-db-required)). The table below covers
the ten members that bear on this round's member selection — the `serialization-schema` class, the class
R85-C1 opens — plus the four `no-blocker` members whose bytes are the closest structural analogues to the
chosen member (stdlib-only, no binary, file-artifact-driven).

Imports were extracted with `ast` over the grader body; a module is "third-party" when its top-level
package is not in `sys.stdlib_module_names`. Binary names were extracted from `subprocess.run` /
`Popen` / `check_output` / `check_call` / `call` / `os.system` / `os.popen` call sites, including
command lists assigned to a variable first (e.g. `cmd = ["vim", ...]` then `_run(cmd)`).

| member | ledger line | ledger note | third-party imports (grader line) | binary invoked by name through subprocess | source line |
|---|---|---|---|---|---|
| `sqlite-db-truncate` | 801 | *executed* (round 85) | **none** — stdlib only | **none** | — |
| `db-wal-recovery` | 191 | *executed* (round 40) | **none** — stdlib only | **none** | — |
| `extract-elf` | 234 | `no-blocker` | **none** — stdlib only | `gcc`, `node` | `extract-elf/tests/test_outputs.py:334`, `:340`, `:352` |
| `fix-code-vulnerability` | 292 | `no-blocker` | `bottle` | **none** | `fix-code-vulnerability/tests/test_outputs.py:61` |
| `llm-inference-batching-scheduler` | 429 | `no-blocker` | `cost_model_for_tests` | **none** | `llm-inference-batching-scheduler/tests/test_outputs.py:22` |
| `merge-diff-arc-agi-task` | 488 | `no-blocker` | **none** — stdlib only | `git` | `merge-diff-arc-agi-task/tests/test_outputs.py:22` |
| `multi-source-data-merger` | 538 | `no-blocker` | `pandas` | **none** | `multi-source-data-merger/tests/test_outputs.py:8` |
| `raman-fitting` | 722 | `no-blocker` | **none** — stdlib only | **none** | — |
| `regex-chess` | 732 | `no-blocker` | `chess`, `chess.pgn` | **none** | `regex-chess/tests/test_outputs.py:3`, `:4` |
| `sam-cell-seg` | 772 | `no-blocker` | `cv2`, `numpy`, `pandas`, `shapely.geometry`, `shapely.ops`, `shapely.validation` | `python` (present) | `sam-cell-seg/tests/test_outputs.py:13-18`, `:158` |

Notes on the table:

* `raman-fitting` is the only remaining `serialization-schema` member whose grader is stdlib-only **and**
  binary-free (`raman-fitting/tests/test_outputs.py:4-5` — `import json`, `from pathlib import Path`; no
  `subprocess` call anywhere in the file). It is the nearest structural sibling of the chosen member and
  the obvious next replay candidate for the class.
* `extract-elf` is stdlib-only by import but invokes `gcc` and `node` by name.
* `merge-diff-arc-agi-task` is stdlib-only by import and invokes only `git` (present in `/usr/bin`).
* `llm-inference-batching-scheduler` imports `cost_model_for_tests` with a **relative** import
  (`from .cost_model_for_tests import HEADS, HIDDEN, CostModel, align`,
  `llm-inference-batching-scheduler/tests/test_outputs.py:22`) — a package-relative import that cannot
  resolve outside a package context. The frozen detector does not catch this (the
  `candidate-library-required` pattern is `sys\.path\.append\(\s*["']/app`, which does not match a
  relative import), yet the grader cannot be imported standalone.
* `fix-code-vulnerability`'s `bottle` import is at
  `fix-code-vulnerability/tests/test_outputs.py:61`, *inside* a function body, not at module top level —
  so the module imports fine but the test fails at call time.

### 1.3 Every `no-blocker` note falsified by a binary requirement

The frozen detector does not look at binaries. It therefore prices a grader that shells out to an
**absent** toolchain as `unattempted`/`no-blocker`, i.e. "no blocker". For those members the note is
falsified by the grader's own bytes: an offline replay of that grader cannot run, because the binary it
names is not on the host and not in the replay sandbox.

Absence was measured two ways, both re-run at write time:

1. **Host**: `command -v <bin>` and a listing of `/usr/bin` + `/usr/local/bin`.
2. **Sandbox**: the probe's own namespace
   (`plans/round85_sqlite_truncate_probe.py:180-193`, `sandbox_argv`): `bwrap --unshare-all` with
   `--ro-bind /usr /usr --ro-bind /etc /etc`, `--clearenv --setenv PATH /usr/bin`. Only `/usr` and `/etc`
   are bound, and `PATH` is exactly `/usr/bin`. I reproduced that namespace and ran an
   `importlib.util.find_spec` sweep inside it; the results are in §1.4.

The complete falsified set — `no-blocker` in the ledger, but the grader names a binary that is **absent**
from both the host and the sandbox `PATH`:

| member | ledger line | binary | exact grader source line | host status |
|---|---|---|---|---|
| `adaptive-rejection-sampler` | 4 | `Rscript` | `adaptive-rejection-sampler/tests/test_outputs.py:74` (also `:132`, `:253`, `:294`) | absent |
| `build-pov-ray` | 54 | `/usr/local/bin/povray` | `build-pov-ray/tests/test_outputs.py:17` (also `:81`) | absent (path does not exist) |
| `custom-memory-heap-crash` | 180 | `valgrind` | `custom-memory-heap-crash/tests/test_outputs.py:159` (list opened at `:158`) | absent |
| `dna-assembly` | 212 | `oligotm` | `dna-assembly/tests/test_outputs.py:23` (list opened at `:22`) | absent |
| `dna-insert` | 223 | `oligotm` | `dna-insert/tests/test_outputs.py:20` (list opened at `:19`) | absent |
| `git-multibranch` | 341 | `apt-get` (in a generated shell script) | `git-multibranch/tests/test_outputs.py:12-13` (`apt-get update` / `apt-get install -y curl expect git openssh-client`), executed via `os.popen("bash verify.sh")` at `:96` | absent |
| `large-scale-text-editing` | 407 | `vim` | `large-scale-text-editing/tests/test_outputs.py:170` (also `:202`) | absent |
| `mcmc-sampling-stan` | 478 | `R`, `Rscript` | `mcmc-sampling-stan/tests/test_outputs.py:12` and `:150` (also `:46`, `:68` for `R`) | absent |
| `overfull-hbox` | 574 | `apt`, `/usr/bin/pdflatex` | `overfull-hbox/tests/test_outputs.py:18` and `:20` (both `os.system`) | absent |
| `prove-plus-comm` | 653 | `coqc` | `prove-plus-comm/tests/test_outputs.py:31` | absent |
| `qemu-alpine-ssh` | 693 | `sshpass` | `qemu-alpine-ssh/tests/test_outputs.py:25` (list opened at `:24`) | absent |
| `qemu-startup` | 702 | `expect` | `qemu-startup/tests/test_outputs.py:56` (`os.popen("expect -f run.exp")`; script header at `:8`) | absent |
| `reshard-c4-data` | 751 | `uv` | `reshard-c4-data/tests/test_outputs.py:96` (also `:107`, `:150`) | absent (lives in `~/.local/bin`, not `/usr/bin`) |
| `rstan-to-pystan` | 763 | `R` | `rstan-to-pystan/tests/test_outputs.py:12` (also `:28`) | absent |
| `winning-avg-corewars` | 887 | `pmars` | `winning-avg-corewars/tests/test_outputs.py:61` (list opened at `:60`) | absent |

**15 members carry a `no-blocker` note that a binary requirement falsifies.**

A second, weaker group names a binary that **is** present in `/usr/bin` (`gcc`, `node`, `git`, `python`,
`python3`, `convert`, `useradd`, `pgrep`, `socat`, `g++`, `rustc`, `java`, `docker`, `make`, `cargo`).
Those notes are not falsified by an *absent* binary, but the grader still reaches out of the process, so
they are not pure-stdlib either: `extract-elf` (`:334` `gcc`, `:340`/`:352` `node`), `gpt2-codegolf`
(`:21` `gcc`), `merge-diff-arc-agi-task` (`:22` `git`), `make-doom-for-mips` (`:18` `node`),
`make-mips-interpreter` (`:18` `node`), `mailman` (`:62` `useradd`), `path-tracing` (`:31` `gcc`),
`path-tracing-reverse` (`:33` `gcc`), `polyglot-rust-c` (`:24` `rustc`, `:25` `g++`), `write-compressor`
(`:15` `gcc`), `build-cython-ext` (`:144` `git`, `:158` `python`), `cobol-modernization` (`:56`,`:62`,`:68`
`python`), `sam-cell-seg` (`:158` `python`), `schemelike-metacircular-eval` (`:14`,`:34` `python3`),
`build-pov-ray` (`:46` `convert`).

**Also not a binary, but the same class of falsifier:** a `no-blocker` member whose grader imports a
third-party package that the replay sandbox cannot import is equally unreplayable, because the grader
module fails at import time. Measured **inside the probe's own namespace** (`bwrap` with only `/usr` and
`/etc` bound, `PATH=/usr/bin`, `python3 -I -B`):

* importable in the sandbox: `numpy`, `scipy`, `PIL`, `bs4`, `cv2`, `requests`, `packaging`.
* **not** importable in the sandbox: `pandas`, `skimage`, `selenium`, `torch`, `torchvision`, `rdflib`,
  `chess`, `fasttext`, `sklearn`, `mujoco`, `toml`, `zope`, `datasets`, `pytest`, `bottle`, `shapely`,
  `mailman`, `headless_terminal`, `cost_model_for_tests`, `portfolio_*`, `pyknotid`.

So `financial-document-processor` (`pandas`), `multi-source-data-merger` (`pandas`),
`sam-cell-seg` (`pandas`, `shapely`), `fix-code-vulnerability` (`bottle`), `regex-chess` (`chess`),
`sparql-university` (`rdflib`), `train-fasttext` (`fasttext`, `sklearn`), `tune-mjcf` (`mujoco`),
`video-processing` (`toml`), `pytorch-model-cli` (`torch`, `torchvision`), `pytorch-model-recovery`
(`torch`), `build-pov-ray` (`skimage`), `mailman` (`mailman`, `zope`), `reshard-c4-data` (`datasets`),
`build-cython-ext` (`pyknotid`), `llm-inference-batching-scheduler` (`cost_model_for_tests`),
`portfolio-optimization` (`portfolio_*`), `headless-terminal` (`headless_terminal`) carry a `no-blocker`
note that a **third-party import** falsifies. This is the second half of the finding: the `no-blocker`
shape asserts "no blocker" while the bytes carry a hard external dependency that the frozen detector
cannot see.

---

## 2. The chosen member `sqlite-db-truncate` — confirmed from its bytes only

I did **not** open `plans/round85-cases.json` for this section. Everything below is derived from
`corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py` (31 lines) and its digest.

**Digest.** `sha256sum` of that file = `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`,
matching the claim's pin prefix `8f5bc11018687d8c` and the full sha quoted in the claim's Subject
paragraph and in the receipt (`corpus/evidence/round85/sqlite-db-truncate-probe.txt`, `SUBJECT_SHA`
line). The ledger's `no-blocker` note for this member carried the same 16-hex prefix
(`plans/grader-population-ledger.json:801` region, at base: `evidence: "no-blocker: tests/test_outputs.py
sha256=8f5bc11018687d8c"`), so the pre-round digest pin and the round-85 subject pin agree.

**Imports — standard library only.** The file's complete import surface is one line:

* `sqlite-db-truncate/tests/test_outputs.py:6` — `import json`

`json` is in `sys.stdlib_module_names`. There is no `from … import`, no third-party import, no relative
import, no `pytest` import, and no `sys.path` manipulation. The grader is importable under
`python3 -I -B` with `PATH=/usr/bin` in the probe's namespace (I ran the namespace and imported `json`
there without error).

**The read.** `sqlite-db-truncate/tests/test_outputs.py:22` —

```python
data = json.load(open("/app/recover.json"))
```

That is the only filesystem read in the grader. It is an absolute path into the sandbox's `/app`, which
the probe binds as the per-case directory (`plans/round85_sqlite_truncate_probe.py:187`,
`--bind str(case_dir / "app") /app`). The host `/app` is never written.

**The acceptance predicate, quoted with line numbers** (`sqlite-db-truncate/tests/test_outputs.py`):

```
20	def test_json_data():
21	    # Reference the directory the agent operated in (the WORKDIR in the Docker env)
22	    data = json.load(open("/app/recover.json"))
23	
24	    soln_tuples = {(item["word"], item["value"]) for item in soln}
25	    data_tuples = {(item["word"], item["value"]) for item in data}
26	
27	    # Find intersection - each item matched at most once
28	    matches = soln_tuples & data_tuples
29	    score = len(matches)
30	
31	    assert score > 6, "Did not load data correctly"
```

**The predicate, stated literally:** `score > 6`, where
`score = len({(word, value) for item in soln} & {(word, value) for item in json.load(open("/app/recover.json"))})`
and `soln` is the hardcoded eight-element list at lines 8-17
(`testword02`=10.0, `testword03`=25.0, `testword04`=42.0, `testword05`=50.0, `testword06`=75.0,
`testword07`=99.0, `testword08`=99.99, `testword09`=0.5). Set intersection, so duplicates collapse and
extras are tolerated; the threshold is **strictly greater than 6**, i.e. 7 or 8 pass, 6 or fewer fail.

Two consequences that the frozen case table exercises and that the bytes confirm:

* **Type sensitivity.** `10.0` and `"10.0"` are different set elements (float vs str), so a `recover.json`
  of string values intersects `soln` in zero elements — the `string-values` case scores 0.
* **int/float equality.** `10 == 10.0` and `hash(10) == hash(10.0)` in Python, so integer-valued rows
  *do* match the float entries of `soln`; six integer-valued rows score 6, which is **not** `> 6`, so
  the `int-values` case fails with score 6. I confirmed the equality semantics in the host interpreter.

**No binary, no subprocess.** The grader contains no `subprocess`/`os.system`/`os.popen` call and no
command of any kind — grep for `subprocess|os.system|os.popen|Popen` over the file returns nothing.
This is why the member replays inside the probe's `bwrap` namespace with only `/usr` and `/etc` bound:
the grader needs nothing from the host beyond a Python that can `import json`.

**One function.** `ast.parse` over the file yields exactly one `FunctionDef` whose name starts with
`test_`: `test_json_data` at line 20. That matches the probe's frozen `TESTS = ("test_json_data",)`
(`plans/round85_sqlite_truncate_probe.py:37`) and the counter's `parse_cases`/subject checks.

**Not reimplemented.** The grader's own `soln` list is the only source of the eight expected pairs: the
probe's harness imports the captured module with `runpy` and reads `module["soln"]`
(`plans/round85_sqlite_truncate_probe.py:55-72`, `HARNESS`), and the *independent* reference
recomputation in the probe uses `ast.literal_eval` on the grader's own `soln` assignment
(`plans/round85_sqlite_truncate_probe.py:125-141`, `reference_score`). Both legs therefore read the
grader's bytes, not a re-typed copy.

---

## 3. Class histogram of the 59 unexecuted members, and the `serialization-schema` count

### 3.1 Histogram by class (members may hold several classes, so the column sums to more than 59)

Computed from `plans/grader-population-ledger.json` over the 59 rows with `status == "unexecuted"` at the
current tip:

| class | unexecuted members holding it |
|---|---|
| file-artifact | 55 |
| subprocess-exec | 35 |
| stdout-inspection | 21 |
| crypto-credential | 10 |
| numeric-band | 8 |
| filesystem-metadata | 8 |
| **serialization-schema** | **8** |
| timing-wall | 6 |
| shell-exec | 5 |
| network-service | 4 |
| candidate-import | 3 |
| git-plumbing | 2 |
| process-environment | 1 |
| db-state | 1 |
| signal-delivery | 0 |
| container-image | 0 |

Sum of memberships = 167 pairs over 59 members. The census of all 88 members
(`corpus/evidence/round62/class-survey.txt`) reports 230 pairs over 16 classes; 230 − 167 = 63 pairs sit
on the 29 executed members.

### 3.2 How many of the `serialization-schema` members are executed after this round

The class has **10** members — `corpus/evidence/round62/class-survey.txt:17`:

```
CLASS serialization-schema count=10 members=db-wal-recovery,extract-elf,fix-code-vulnerability,
llm-inference-batching-scheduler,merge-diff-arc-agi-task,multi-source-data-merger,raman-fitting,
regex-chess,sam-cell-seg,sqlite-db-truncate
```

All 10 are priced in the ledger with the `serialization-schema` class, and `SKILL.md:84` carries the
class cell `| serialization-schema | 10 | executed 2 of 10 (round 85 adds `sqlite-db-truncate` to round
40's `db-wal-recovery`) |`.

* **Before (BASE `0de45354`):** 1 of 10 executed (`db-wal-recovery`, round 40, receipt
  `corpus/evidence/round40/db-wal-probe.txt`); **9 unexecuted**. The R79 gate at BASE prints
  `CLASS serialization-schema k=1 n=10 cell=executed 1 of 10` and `PREDICATE R79-C1 pass`.
* **After this round:** 2 of 10 executed (`db-wal-recovery` + `sqlite-db-truncate`, round 85, receipt
  `corpus/evidence/round85/sqlite-db-truncate-probe.txt`); **8 unexecuted**. The R79 gate at the current
  tip prints `CLASS serialization-schema k=2 n=10 cell=executed 2 of 10` and `PREDICATE R79-C1 pass`.

So the answer to "how many of the 9 `serialization-schema` members are executed after this round" is: the
class is 10 strong, and this round moved it from **1 of 10** to **2 of 10** — i.e. exactly one of the
nine previously-unexecuted members (`sqlite-db-truncate`) is now executed, and **8 of the 10 remain
unexecuted**. Of the eight still unexecuted, only `raman-fitting` is stdlib-only and binary-free
(§1.2); the other seven each name a third-party import or a binary.

---

## 4. Population-gate figures, measured

| figure | BASE `0de45354` | current tip | source |
|---|---|---|---|
| ledger members | 88 | 88 | `plans/grader-population-ledger.json` (88 rows) |
| `executed` | 28 | 29 | R79 gate: `replayed=28` → `replayed=29` |
| `unexecuted` | 60 | 59 | R79 gate: `unexecuted=60` → `unexecuted=59` |
| `serialization-schema` executed | 1 of 10 | 2 of 10 | R79 gate: `k=1 n=10` → `k=2 n=10` |
| `unaccounted` / `unbacked` / `understated` | 0 / 0 / 0 | 0 / 0 / 0 | R79 gate `TARGET` line |

The class-level figures for the other 15 classes are unchanged between BASE and the tip except
`file-artifact` (20 of 76 → 21 of 76, because `sqlite-db-truncate` carries `file-artifact`).

**Both standing gates are green at the current tip**, verified by running them read-only:

* `plans/round79_c1_population_ledger.py --lane .` → `TARGET classes=16 members=88 pairs=230 replayed=29
  located=29 unlocated=0 unexecuted=59 unaccounted=0 unbacked=0 understated=0 covered=15`,
  `PREDICATE R79-C1 pass`.
* `plans/round85_c1_replay.py --lane .` → `TARGET members=1 cases=8 legs=16 mismatches=0 located=1
  executed=1 defects=0`, `PREDICATE R85-C1 pass`.

### 4.1 A cross-gate reconciliation the L1 had to make (observed, now closed)

While I worked, the R79 population gate and the R85-C1 counter disagreed about the same ledger row, and
the disagreement was visible in the committed history:

* The R79 gate derives the row's verdict from the **receipt's own observation shape**
  (`plans/round79_c1_population_ledger.py:91-93` and `:182-189`): `PREDICATE R\d+-C\d+ pass` →
  `predicate`, `^VECTOR ` → `vectors`, `^(?:CASE |case=)` → `cases`. The round-85 receipt's observation
  block is `CASE <id> predicted=… observed=…` (`corpus/evidence/round85/sqlite-db-truncate-probe.txt`,
  lines 15-22) and its predicate line is `PREDICATE R85-PROBE pass` (line 24 of the file, inside the
  block) — which matches **neither** `OBS_PRED` (`R\d+-C\d+`) nor `OBS_VEC`, so the R79 gate classifies
  the receipt as `cases`.
* The R85-C1 counter originally demanded `row["verdict"] == "predicate"`
  (`plans/round85_c1_replay.py:216` at `b1e57097`; the check now reads
  `row.get("verdict") != "cases"` at `plans/round85_c1_replay.py:217` in the worktree).

Between `b1e57097` and `35b1e4e0` the L1 reconciled this: commit `35b1e4e0` ("ledger verdict priced as
cases (receipt observation form)") and `b1e57097` ("C1 counter accepts the frozen tb2 header line as the
receipt's first line") together make the row `verdict: "cases"` and the receipt carry the
`# tb2 sqlite-db-truncate grader probe` header that `SUBJECTS` at
`plans/round79_c1_population_ledger.py:94-100` requires. The R79 gate's `SUBJECT-ABSENT` defect (raised
at `2410f403`, when the receipt lacked the header line) is likewise closed. Both gates now pass; I
recorded the intermediate red states from the committed tree, not from a mutated one.

This is worth the L1's attention for one reason: the C1 claim text freezes the receipt's
**observation form** implicitly through `plans/round85-cases.json` and the counter, while the R79 gate
prices the *same* receipt by a different rule. A future round that re-mints this receipt must keep the
header line and the `CASE …` observation lines, or the population gate goes red again for a reason that
has nothing to do with the replay's correctness.

---

## 5. Findings

### S-1 (coverage/calibration, frozen-element — reported, not edited)

`plans/round-85-claims.md:60` (R85-C1, "Before (BASE `0de45354`)" paragraph) states the population gate as
"`serialization-schema` class executed **0 of 9** → **1 of 9**". The class has **10** members
(`corpus/evidence/round62/class-survey.txt:17`; `SKILL.md:84`; 10 ledger rows carry the class), and
`db-wal-recovery` was already executed at round 40. The measured transition is **1 of 10 → 2 of 10**
(R79 gate: `k=1 n=10` at BASE, `k=2 n=10` at the tip). The claim's "9" is the count of members that
were *unexecuted* at BASE, not the class size, and "0 of 9 → 1 of 9" reads as "0 of the 9 unexecuted
became executed". The lesson's phrasing — "executes 0 of its 9 members" — states the class size as 9,
which is wrong: the class has 10 members and had one executed before this round. `SKILL.md:84` was
updated to `executed 2 of 10` at `2410f403`, so the frozen prose and the live skill table disagree.

**The L1 has since landed a matching correction in the non-frozen lesson**
(`corpus/lessons/round-85.md`, working-tree change observed at the time of writing): it replaces the
lesson's `0 of its 9 members → 1 of 9` line with `**1 of 10 → 2 of 10**`, cites the R79 counter's own
`CLASS serialization-schema k=1 n=10` at BASE, and records a dated correction row "**R85-F1,
2026-11-04:** the frozen claims' before/after line says `0 of 9 → 1 of 9`; that arithmetic is wrong on
both the numerator and the denominator and is not rewritten in the frozen doc". That correction is
independently identical to this seat's measurement, and it correctly leaves
`plans/round-85-claims.md` — the frozen document — unrewritten, as required. This seat made no edit to
either file; the lesson change is the L1's.

### S-2 (calibration — the `no-blocker` shape cannot see a binary requirement)

15 `no-blocker` rows are falsified by an **absent** binary that the grader names by hand through
`subprocess`/`os.system`/`os.popen`: `adaptive-rejection-sampler` (`Rscript`, :74),
`build-pov-ray` (`/usr/local/bin/povray`, :17), `custom-memory-heap-crash` (`valgrind`, :159),
`dna-assembly` (`oligotm`, :23), `dna-insert` (`oligotm`, :20), `git-multibranch` (`apt-get` in the
generated `verify.sh`, :12-13), `large-scale-text-editing` (`vim`, :170), `mcmc-sampling-stan`
(`R`/`Rscript`, :12/:150), `overfull-hbox` (`apt`, `/usr/bin/pdflatex`, :18/:20), `prove-plus-comm`
(`coqc`, :31), `qemu-alpine-ssh` (`sshpass`, :25), `qemu-startup` (`expect`, :56), `reshard-c4-data`
(`uv`, :96), `rstan-to-pystan` (`R`, :12), `winning-avg-corewars` (`pmars`, :61). Full table in §1.3.

Root cause: the detector that prices `unattempted` vs a blocker is a four-regex table over the grader
body (`plans/round79_c1_population_ledger.py:85-90`) that never inspects a command line. A
`no-blocker: tests/test_outputs.py sha256=…` note therefore means "none of those four regexes fired" —
it does **not** mean "this grader has no external dependency". That is not a defect in the frozen
R85-C1 claim (which never asserts it), but it is the sharpest coverage lever visible from the ledger:
the next `serialization-schema` replay should be `raman-fitting`, the only remaining class member whose
grader is stdlib-only and binary-free.

### S-3 (calibration — the same shape is blind to third-party imports)

16 further `no-blocker` rows are falsified by a third-party import the replay sandbox cannot satisfy
(measured inside the probe's own `bwrap` namespace): `financial-document-processor` (`pandas`),
`multi-source-data-merger` (`pandas`), `sam-cell-seg` (`pandas`, `shapely`), `fix-code-vulnerability`
(`bottle`, imported inside a function body at :61), `regex-chess` (`chess`), `sparql-university`
(`rdflib`), `train-fasttext` (`fasttext`, `sklearn`), `tune-mjcf` (`mujoco`), `video-processing` (`toml`),
`pytorch-model-cli` (`torch`, `torchvision`), `pytorch-model-recovery` (`torch`), `build-pov-ray`
(`skimage`), `mailman` (`mailman`, `zope`), `reshard-c4-data` (`datasets`), `build-cython-ext`
(`pyknotid`), `llm-inference-batching-scheduler` (`cost_model_for_tests`, relative import at :22).

A **relative** import (`from .cost_model_for_tests import …`) is a distinct hazard the detector cannot
express at all: the `candidate-library-required` pattern is `sys\.path\.append\(\s*["']/app`, which does
not match, yet the module cannot be imported standalone.

### S-4 (coverage — the census roster and the ledger differ by one)

`corpus/evidence/round52/graders/` holds 89 task directories and `all_tasks.lst` has 89 lines, but the
class census (`corpus/evidence/round62/class-survey.txt:1`, `roster=89 tree-dirs=89`) and the ledger
price **88** members. The missing one is `sanitize-git-repo`: its grader body is deliberately absent
(`corpus/evidence/round52/graders/EXCLUDED.md:5-12` — GitHub push protection flags a token pattern at
line 12 of that upstream fixture, per `EXCLUDED.md:11`; operator decision 2026-10-28 to exclude the
bytes). `SHA256SUMS:158`
still lists the path, and `all_tasks.lst:77` still lists the member, while
`corpus/evidence/round62/class-survey.txt` never mentions it. The R79 gate's universe is derived from the
census (`plans/round79_c1_population_ledger.py:431-432`), so `sanitize-git-repo` is outside the gate's
membership entirely and cannot raise `MEMBER-UNACCOUNTED`. This is a deliberate, documented exclusion —
not a defect — but it means the population the gate prices is 88, one short of the 89 directories on disk.
Any coverage arithmetic that quotes "89" needs the exclusion stated.

### S-5 (coverage — a clean `no-blocker` note exists for the chosen member, and it was correct)

The chosen member's own pre-round row carried
`evidence: "no-blocker: tests/test_outputs.py sha256=8f5bc11018687d8c"`
(`plans/grader-population-ledger.json` at base). That note was **true**: `sqlite-db-truncate`'s grader
imports only `json` (`sqlite-db-truncate/tests/test_outputs.py:6`), reads only `/app/recover.json` (:22),
and invokes no binary. It is one of the few `no-blocker` rows in the whole set that survives the byte-level
test in §1.3/§1.4. The R85-C1 choice of member is well-founded on this evidence.

---

## 6. Method, tooling and reproducibility

* No production file was written, edited or deleted. The only file this seat produced is this one:
  `.ufo/waves/round-85/w1/ScoutR85/scout-map.md`.
* All scratch work lived under `/fast/scratch/hyaku/kengaku-r85/ScoutR85/` and has been deleted.
* No mutating git/jj command was run in any repo. Read-only git was used only:
  `log`, `show`, `rev-parse`, `status`, `diff`, `ls-files`, `cat-file` (all `-C`/paths inside the lane
  repo, and `git -C "$D"` semantics were never needed because no fixture repository was created).
* No network fetch was performed. The pinned upstream URL was **not** retrieved; every byte quoted here
  comes from the local capture under `corpus/evidence/round52/graders/`, and the subject digest was
  re-derived locally rather than trusted from the receipt.
* **No tool was installed or upgraded.** The task needed only the interpreter already present
  (`python3`, host version 3.14.8 — the same version the receipt's `HOST_PYTHON` line records), plus the
  already-installed `bwrap` at `/usr/bin/bwrap` that the probe itself uses. The operator's tooling
  directive permits installing helpers, but nothing here required it, so no install/update was performed
  and there is nothing to record on the tool/version/channel/reason axis.
* Extraction method: `ast` walk over each grader body for imports and for
  `subprocess.run|Popen|check_output|check_call|call` / `os.system` / `os.popen` call sites, including
  command lists bound to a variable before the call; `sys.stdlib_module_names` for the stdlib test;
  `command -v` plus a `/usr/bin` + `/usr/local/bin` listing for host binary presence; and a reproduced
  `bwrap --unshare-all --ro-bind /usr /usr --ro-bind /etc /etc --clearenv --setenv PATH /usr/bin`
  namespace (mirroring `plans/round85_sqlite_truncate_probe.py:191-205`) for sandbox import and binary
  availability.
* Both standing gates were run read-only against the lane (`--lane .`), writing only into scratch.
* Caveat on timing: the L1 committed several repairs to the same files during this recon
  (`f8884277`, `b1e57097`, `35b1e4e0`, `def5d0ea`). Every "current tip" figure above was re-measured
  after the last such commit (`def5d0ea`), and the §4.1 red states are quoted from the committed trees
  at `2410f403` / `b1e57097` as they were then.

## 7. Remaining unknowns

* The R84-V4 item is operator-owned and out of this seat's scope; nothing here bears on it.
* Whether the `no-blocker` shape should be extended to price binary and third-party requirements is a
  ledger-schema decision for the L1, not a finding this seat can close. This report establishes only that
  31 of the 52 `no-blocker` rows are falsified by an external dependency the frozen detector cannot see
  (15 binary + 16 import).
* `sanitize-git-repo` cannot be priced at all without the excluded bytes, so no statement about its
  replayability is made here; the exclusion is documented at
  `corpus/evidence/round52/graders/EXCLUDED.md:5-12`.
