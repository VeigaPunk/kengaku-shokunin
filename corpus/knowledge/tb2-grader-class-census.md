# Terminal-Bench 2.0 grader-class census — the population's first mechanized mechanism-class map

source: S226 — the pin's top-level task tree at `2fd12b88` (GitHub git-trees API; 89 task dirs ==
the round-52 `all_tasks.lst` roster, priced `roster==tree=True` by the instrument; capture
`corpus/evidence/round62/tb2-tree-2fd12b88.json`, sha256 `dd64bfb3…f0cd1`)
source: S224 — the `cancel-async-tasks` grader capture, whose signal-delivery membership the
census re-derives mechanically (the frozen sentinel: `signal-delivery count=1 member=cancel-async-tasks`)

## What the census prices

`plans/round62_c1_class_survey.py` (the round-62 survey instrument; stdlib-only, deterministic
with a built-in determinism leg that re-runs the census and requires byte-identical output)
reads the committed round-52 capture population (`corpus/evidence/round52/graders/`), verifies
every capture byte against the pinned `SHA256SUMS` (184 rows; 183 committed; the one
pinned-but-absent row is exactly the `EXCLUDED.md` capture — the push-protection exclusion, so
byte-pinning covers 100% of the population that exists), and classifies every committed
`test_outputs.py` grader (93 files across the 89 task dirs; `break-filter-js-from-html` carries
an extra `environment/tests/` copy) over a frozen 16-detector table, each class named by what
its regex literally matches, multi-label. Receipt of record:
`corpus/evidence/round62/class-survey.txt` — measured at the amendment tip `968f6ae7` on a
fresh clean WSL-native-fs clone, `PREDICATE R62-C1 pass`, exit 0, determinism leg green, run
sec 0.4. The FIRST scored run at the freeze tip `93f19d1a` priced SETUP exit 2 (the five
population bookkeeping files — `all_tasks.lst`, `executed17.lst`, `missing.lst`, `unexec.lst`,
`unexec72.lst` — had sat untracked for ten rounds; receipt of record committed AS-IS at
`.ufo/waves/round-62/recon/scored-run-SETUP.txt`); amendment `968f6ae7` commits them
byte-as-is; nothing was re-scored because no census result existed yet.

## The census of record (16 classes, 93 graders classified, 0 unclassified)

Quoted verbatim from the receipt's census lines (class counts are the instrument's output, never
hand-tabulated):

```
CLASS-CENSUS roster=89 tree-dirs=89 sha256sums-rows=184 captures-committed=183 captures-unpinned=0 sha-mismatch=0 absent-pinned=1 graders-classified=93 unclassified=0 classes=16
POPULATION roster==tree=True excluded-sha-pinned=True
CLASS signal-delivery count=1 members=cancel-async-tasks
CLASS subprocess-exec count=45 members=...
CLASS shell-exec count=6 members=feal-differential-cryptanalysis,git-multibranch,model-extraction-relu-logits,overfull-hbox,polyglot-rust-c,qemu-startup
CLASS candidate-import count=6 members=feal-differential-cryptanalysis,headless-terminal,model-extraction-relu-logits,portfolio-optimization,torch-pipeline-parallelism,torch-tensor-parallelism
CLASS file-artifact count=76 members=...
CLASS stdout-inspection count=29 members=...
CLASS numeric-band count=10 members=...
CLASS crypto-credential count=12 members=...
CLASS network-service count=8 members=...
CLASS timing-wall count=9 members=...
CLASS filesystem-metadata count=10 members=...
CLASS process-environment count=3 members=...
CLASS git-plumbing count=3 members=...
CLASS db-state count=2 members=query-optimize,sqlite-with-gcov
CLASS serialization-schema count=10 members=...
CLASS container-image count=0 members=-
UNCLASSIFIED count=0 members=-
SENTINEL signal-delivery count=1 member=cancel-async-tasks
EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image
```

(the six `members=...` elisions here are display-only — the receipt of record carries every
member list in full; this entry quotes the receipt, it does not re-tabulate it)

## Readings

- **The dominant class is file-artifact (76 of 89 tasks' graders)**: the population's modal
  grading mechanism asserts on files the candidate leaves in `/app` — the corpus's bread and
  butter, already the executed corpus's most-exercised mechanism.
- **The signal-delivery sentinel re-derives the r59/r61 prose negatives mechanically**:
  exactly one grader in the whole population sends a signal (`cancel-async-tasks`, executed at
  round 61). What was three rounds of ad-hoc greps is now a frozen invariant the instrument
  prices on every run.
- **Two genuinely new mechanism classes surfaced only because the survey classified rather
  than grepped**: `candidate-import` (6 graders — the grader IMPORTS the candidate's module,
  e.g. `feal-differential-cryptanalysis` doing `sys.path.append('/app')` + `import attack`,
  then calls the candidate function against the true key) and `shell-exec` (6 graders driving
  builds through `os.popen`/`os.system` instead of `subprocess`). The first detector table
  missed both — take 1 of the pre-freeze dry run priced the executed FEAL grader UNCLASSIFIED
  (`INVARIANT-FAIL every-executed-grader-classified`, PREDICATE fail) and the table was amended
  before the freeze; both takes stay in the recon receipt.
- **The eighteenth-grader gate's survey input**: `EXECUTED-COVERAGE ... classes-covered=12
  classes-uncovered=network-service,process-environment,db-state,container-image` — the only
  uncovered classes WITH population members are `network-service` (8 graders: a served endpoint
  is asserted against — `pypi-server`, `nginx-request-logging`, `kv-store-grpc`, ...),
  `process-environment` (3) and `db-state` (2); `container-image` has no members at all. Any
  eighteenth-grader claim should come from one of those three classes (the r58/r59
  class-gated pattern).
- **Multi-label honesty**: 93 files, sum of class counts 235 > 93 — graders stack mechanisms
  (spawn + assert on files + read stdout is one common shape). The census is a mechanism map,
  not a partition.

Named limits: the detectors are line-regex features over grader text — they price mechanism
FAMILIES, not per-grader semantics (a file-artifact hit does not say WHAT is asserted); the
population of record is the committed capture set (the excluded capture's bytes are named in
EXCLUDED.md and are not part of any class count); classification is of `test_outputs.py`
graders only — `test.sh` wrappers and the one extra `verify.sh` capture are byte-verified
against SHA256SUMS but not classified.
