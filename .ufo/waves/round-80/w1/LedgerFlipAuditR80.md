# LedgerFlipAuditR80 — six ledger flips

## Scope and measured revision

Axes: **coverage** (six located rows) and **calibration** (preserving ledger/evidence integrity). Read the frozen claims in full. Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`. Base: `dce7c275381c669e6489f1b795b1505d0824c262`. Measured master tip: `6669fe72e59718acc1a0f32a92849a544b0b2f1c`; it has advanced beyond freeze. All comparisons use committed bytes at that pinned tip, not mutable worktree files.

Command:
```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse dce7c275
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse af51132d8919cedd14d3d3407ae5abc966d5d427
```
Output (exit 0):
```text
6669fe72e59718acc1a0f32a92849a544b0b2f1c
dce7c275381c669e6489f1b795b1505d0824c262
af51132d8919cedd14d3d3407ae5abc966d5d427
```

## Findings

- Exactly the six target member objects changed; no other member changed. All top-level metadata values survived unchanged.
- Each target changed `receipt`, `round`, `status`, and added `subject` and `verdict`. Each dropped exactly `debt` and `instrument`, expressly allowed by item 2. No `reason` or `evidence` key existed on these base rows; neither was dropped. No unexpected key change occurred.
- Every target's ordered `classes` list is identical; it is the only base field outside the allowed replace/drop fields. The full before/after rows are represented in the diff below.
- File-level exception to “only six rows”: a terminal newline was added after the final `}`. No JSON value outside the six rows changed. Thus a literal claim of *only* status/round/receipt/subject/verdict textual changes would be false: the two permitted dropped keys and EOF newline must also be disclosed.
- All six historical receipts are byte-identical at base and tip, independently compared as bytes and SHA-256, not inferred merely from the population counter.
- Assigned round-79 gate in a clean shared clone: `LEDGER rows=88 executed=24 unlocated=0 unexecuted=64`; `DEFECTS n=0`; `PREDICATE R79-C1 pass`; exit **0**.

## Complete ledger diff — every changed line

Command (exit 0):
```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff dce7c275381c669e6489f1b795b1505d0824c262..6669fe72e59718acc1a0f32a92849a544b0b2f1c -- plans/grader-population-ledger.json
```
```diff
diff --git a/plans/grader-population-ledger.json b/plans/grader-population-ledger.json
index d175c852..a41de474 100644
--- a/plans/grader-population-ledger.json
+++ b/plans/grader-population-ledger.json
@@ -81,21 +81,21 @@
     "subprocess-exec",
     "timing-wall"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/round61_c1_cancel_probe.py",
-   "receipt": "corpus/evidence/round61/cancel-async-probe.txt",
-   "round": 61,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/cancel-async-tasks-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "predicate"
   },
   "chess-best-move": {
    "classes": [
     "file-artifact"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/round55_c3_chess_probe.py",
-   "receipt": "corpus/evidence/round55/chess-best-move-probe.txt",
-   "round": 55,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/chess-best-move-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "predicate"
   },
   "circuit-fibsqrt": {
    "classes": [
@@ -201,11 +201,11 @@
    "classes": [
     "numeric-band"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/round58_c2_kl_probe.py",
-   "receipt": "corpus/evidence/round58/kl-probe.txt",
-   "round": 58,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/distribution-search-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "predicate"
   },
   "dna-assembly": {
    "classes": [
@@ -416,11 +416,11 @@
     "numeric-band",
     "timing-wall"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/round57_c2_eigen_probe.py",
-   "receipt": "corpus/evidence/round57/eigen-probe.txt",
-   "round": 57,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/largest-eigenval-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "predicate"
   },
   "llm-inference-batching-scheduler": {
    "classes": [
@@ -559,11 +559,11 @@
     "stdout-inspection",
     "subprocess-exec"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/round59_c1_openssl_probe.py",
-   "receipt": "corpus/evidence/round59/openssl-probe.txt",
-   "round": 59,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/openssl-selfsigned-cert-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "predicate"
   },
   "overfull-hbox": {
    "classes": [
@@ -638,11 +638,11 @@
    "classes": [
     "file-artifact"
    ],
-   "debt": "no-subject-stamp",
-   "instrument": "plans/tb2_grader_probe.py",
-   "receipt": "corpus/evidence/round35/tb2-grader-probe.txt",
-   "round": 35,
-   "status": "executed-unlocated"
+   "receipt": "corpus/evidence/round80/protein-assembly-probe.txt",
+   "round": 80,
+   "status": "executed",
+   "subject": "tb2-header",
+   "verdict": "cases"
   },
   "prove-plus-comm": {
    "classes": [
@@ -898,4 +898,4 @@
  },
  "schema": "r79-population-ledger/1",
  "why": "Every member of the 16-class Terminal-Bench 2.0 grader population, priced exactly once: executed (a tracked receipt whose own bytes name the member and carry execution observations), executed-unlocated (the round's probe instrument names the member and a receipt under that round carries observations, but the receipt does not locate its subject), or unexecuted (no replay; a blocker reason only when a frozen detector fires over the task's tests/test_outputs.py, else `unattempted`). Gated by plans/round79_c1_population_ledger.py (R79-C1)."
-}
\ No newline at end of file
+}
```

## Independent structural and historical-byte comparison

Command: `python3 -c '<the following source>'` (exit 0).
```python
import hashlib, json, subprocess
lane = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
base = "dce7c275381c669e6489f1b795b1505d0824c262"
tip = "6669fe72e59718acc1a0f32a92849a544b0b2f1c"
def read(rev, path):
    return subprocess.check_output(["git", "-C", lane, "show", rev + ":" + path])
path = "plans/grader-population-ledger.json"
b = json.loads(read(base, path)); a = json.loads(read(tip, path))
p = json.loads(read(tip, "plans/round80_probes.json"))["members"]
print("CHANGED_MEMBERS", sorted(m for m in set(b["members"]) | set(a["members"]) if b["members"].get(m) != a["members"].get(m)))
print("TOP_LEVEL_NON_MEMBER_FIELDS_UNCHANGED", {k:v for k,v in b.items() if k != "members"} == {k:v for k,v in a.items() if k != "members"})
for m in p:
    old = b["members"][m]; new = a["members"][m]
    keys = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    print(m, "changed=" + repr(keys), "dropped=" + repr(sorted(set(old) - set(new))), "classes_equal=" + str(old["classes"] == new["classes"]))
    historical = p[m]["historical"]
    x = read(base, historical); y = read(tip, historical)
    print(historical, "bytes=" + str(len(y)), "base_sha256=" + hashlib.sha256(x).hexdigest(), "tip_sha256=" + hashlib.sha256(y).hexdigest(), "byte_identical=" + str(x == y))
```
Output:
```text
CHANGED_MEMBERS ['cancel-async-tasks', 'chess-best-move', 'distribution-search', 'largest-eigenval', 'openssl-selfsigned-cert', 'protein-assembly']
TOP_LEVEL_NON_MEMBER_FIELDS_UNCHANGED True
cancel-async-tasks changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round61/cancel-async-probe.txt bytes=940 base_sha256=3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a tip_sha256=3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a byte_identical=True
chess-best-move changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round55/chess-best-move-probe.txt bytes=694 base_sha256=de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca tip_sha256=de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca byte_identical=True
distribution-search changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round58/kl-probe.txt bytes=735 base_sha256=3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f tip_sha256=3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f byte_identical=True
largest-eigenval changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round57/eigen-probe.txt bytes=1375 base_sha256=463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 tip_sha256=463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 byte_identical=True
openssl-selfsigned-cert changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round59/openssl-probe.txt bytes=1070 base_sha256=ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094 tip_sha256=ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094 byte_identical=True
protein-assembly changed=['debt', 'instrument', 'receipt', 'round', 'status', 'subject', 'verdict'] dropped=['debt', 'instrument'] classes_equal=True
corpus/evidence/round35/tb2-grader-probe.txt bytes=3399 base_sha256=2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8 tip_sha256=2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8 byte_identical=True
```

Historical-only diff command (exit 0):
```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff dce7c275381c669e6489f1b795b1505d0824c262..6669fe72e59718acc1a0f32a92849a544b0b2f1c -- corpus/evidence/round61/cancel-async-probe.txt corpus/evidence/round55/chess-best-move-probe.txt corpus/evidence/round58/kl-probe.txt corpus/evidence/round57/eigen-probe.txt corpus/evidence/round59/openssl-probe.txt corpus/evidence/round35/tb2-grader-probe.txt
```
Output: **empty** (zero bytes).

## Clean shared-clone gate — exact driver and output

The root assertion preceded checkout. The empty porcelain output establishes cleanliness before the gate. No fixture commits or identities were used.

```sh
set -eu
S=/fast/scratch/hyaku/kengaku-r80/LedgerFlipAuditR80
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
D="$S/lane"
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
printf 'ROOT %s\n' "$(git -C "$D" rev-parse --show-toplevel)"
git -C "$D" checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c
printf 'CLONE_HEAD %s\n' "$(git -C "$D" rev-parse HEAD)"
printf 'CLEAN_STATUS_BEGIN\n'
git -C "$D" status --porcelain
printf 'CLEAN_STATUS_END\n'
cd "$D"
set +e
python3 plans/round79_c1_population_ledger.py --lane .
rc=$?
printf 'EXIT %s\n' "$rc"
exit 0
```
Captured stdout followed by stderr (driver exit 0):
```text
ROOT /fast/scratch/hyaku/kengaku-r80/LedgerFlipAuditR80/lane
CLONE_HEAD 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CLEAN_STATUS_BEGIN
CLEAN_STATUS_END
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=24 unlocated=0 unexecuted=64
MEMBER adaptive-rejection-sampler unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER bn-fit-modify unexecuted classes=file-artifact evidence=unattempted
MEMBER break-filter-js-from-html unexecuted classes=file-artifact,subprocess-exec evidence=browser-required
MEMBER build-cython-ext unexecuted classes=file-artifact,git-plumbing,numeric-band,subprocess-exec evidence=unattempted
MEMBER build-pmars executed classes=file-artifact,subprocess-exec evidence=corpus/evidence/round38/build-pmars-probe.txt [tb2-header/cases]
MEMBER build-pov-ray unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER caffe-cifar-10 unexecuted classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER cancel-async-tasks executed classes=file-artifact,signal-delivery,stdout-inspection,subprocess-exec,timing-wall evidence=corpus/evidence/round80/cancel-async-tasks-probe.txt [tb2-header/predicate]
MEMBER chess-best-move executed classes=file-artifact evidence=corpus/evidence/round80/chess-best-move-probe.txt [tb2-header/predicate]
MEMBER circuit-fibsqrt executed classes=file-artifact,stdout-inspection,subprocess-exec evidence=corpus/evidence/round42/fibsqrt-probe.txt [tb2-header/cases]
MEMBER cobol-modernization unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER code-from-image unexecuted classes=file-artifact evidence=unattempted
MEMBER compile-compcert unexecuted classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER configure-git-webserver executed classes=stdout-inspection,subprocess-exec evidence=corpus/evidence/round37/git-webserver-probe.txt [tb2-header/cases]
MEMBER constraints-scheduling executed classes=crypto-credential,file-artifact evidence=corpus/evidence/round41/constraints-probe.txt [tb2-header/cases]
MEMBER count-dataset-tokens unexecuted classes=file-artifact evidence=unattempted
MEMBER crack-7z-hash unexecuted classes=file-artifact evidence=unattempted
MEMBER custom-memory-heap-crash unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER db-wal-recovery executed classes=file-artifact,serialization-schema evidence=corpus/evidence/round40/db-wal-probe.txt [tb2-header/cases]
MEMBER distribution-search executed classes=numeric-band evidence=corpus/evidence/round80/distribution-search-probe.txt [tb2-header/predicate]
MEMBER dna-assembly unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER dna-insert unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER extract-elf unexecuted classes=file-artifact,serialization-schema,subprocess-exec evidence=unattempted
MEMBER extract-moves-from-video unexecuted classes=file-artifact evidence=unattempted
MEMBER feal-differential-cryptanalysis executed classes=candidate-import,shell-exec evidence=corpus/evidence/round43/feal-probe.txt [tb2-header/cases]
MEMBER feal-linear-cryptanalysis executed classes=file-artifact evidence=corpus/evidence/round44/feal-linear-probe.txt [tb2-header/cases]
MEMBER filter-js-from-html unexecuted classes=file-artifact,network-service,subprocess-exec evidence=browser-required
MEMBER financial-document-processor unexecuted classes=crypto-credential,file-artifact evidence=unattempted
MEMBER fix-code-vulnerability unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER fix-git unexecuted classes=crypto-credential,file-artifact evidence=unattempted
MEMBER fix-ocaml-gc unexecuted classes=file-artifact evidence=unattempted
MEMBER gcode-to-text unexecuted classes=file-artifact evidence=unattempted
MEMBER git-leak-recovery executed classes=file-artifact,git-plumbing,stdout-inspection,subprocess-exec evidence=corpus/evidence/round39/git-leak-probe.txt [tb2-header/cases]
MEMBER git-multibranch unexecuted classes=file-artifact,network-service,shell-exec evidence=unattempted
MEMBER gpt2-codegolf unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER headless-terminal unexecuted classes=candidate-import,file-artifact,network-service,subprocess-exec evidence=candidate-library-required
MEMBER hf-model-inference executed classes=filesystem-metadata,network-service evidence=corpus/evidence/round71/hf/receipt.txt [task-under-test/predicate]
MEMBER install-windows-3.11 unexecuted classes=crypto-credential,file-artifact,network-service,process-environment,stdout-inspection,subprocess-exec evidence=vm-required
MEMBER kv-store-grpc executed classes=file-artifact,network-service evidence=corpus/evidence/round64/kvstore-probe.txt [receipt-header/predicate]
MEMBER large-scale-text-editing unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER largest-eigenval executed classes=numeric-band,timing-wall evidence=corpus/evidence/round80/largest-eigenval-probe.txt [tb2-header/predicate]
MEMBER llm-inference-batching-scheduler unexecuted classes=crypto-credential,file-artifact,filesystem-metadata,serialization-schema evidence=unattempted
MEMBER log-summary-date-ranges unexecuted classes=file-artifact evidence=unattempted
MEMBER mailman unexecuted classes=subprocess-exec evidence=unattempted
MEMBER make-doom-for-mips unexecuted classes=file-artifact,subprocess-exec,timing-wall evidence=unattempted
MEMBER make-mips-interpreter unexecuted classes=file-artifact,subprocess-exec,timing-wall evidence=unattempted
MEMBER mcmc-sampling-stan unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER merge-diff-arc-agi-task unexecuted classes=file-artifact,git-plumbing,serialization-schema,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER model-extraction-relu-logits unexecuted classes=candidate-import,file-artifact,shell-exec evidence=candidate-library-required
MEMBER modernize-scientific-stack unexecuted classes=file-artifact,filesystem-metadata,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER mteb-leaderboard unexecuted classes=file-artifact evidence=unattempted
MEMBER mteb-retrieve unexecuted classes=file-artifact evidence=unattempted
MEMBER multi-source-data-merger unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER nginx-request-logging executed classes=file-artifact,network-service,subprocess-exec,timing-wall evidence=corpus/evidence/round70/nginx/receipt.txt [grader-path/predicate]
MEMBER openssl-selfsigned-cert executed classes=crypto-credential,file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=corpus/evidence/round80/openssl-selfsigned-cert-probe.txt [tb2-header/predicate]
MEMBER overfull-hbox unexecuted classes=file-artifact,shell-exec evidence=unattempted
MEMBER password-recovery executed classes=file-artifact evidence=corpus/evidence/round45/probe-run-envelope.txt [tb2-header/cases]
MEMBER path-tracing unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER path-tracing-reverse unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER polyglot-c-py executed classes=stdout-inspection,subprocess-exec evidence=corpus/evidence/round46/polyglot-c-py-probe.txt [tb2-header/cases]
MEMBER polyglot-rust-c unexecuted classes=shell-exec,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER portfolio-optimization unexecuted classes=candidate-import,numeric-band,timing-wall evidence=candidate-library-required
MEMBER protein-assembly executed classes=file-artifact evidence=corpus/evidence/round80/protein-assembly-probe.txt [tb2-header/cases]
MEMBER prove-plus-comm unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER pypi-server executed classes=network-service,stdout-inspection,subprocess-exec evidence=corpus/evidence/round68/pypi/receipt.txt [task-under-test/predicate]
MEMBER pytorch-model-cli unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER pytorch-model-recovery unexecuted classes=file-artifact,filesystem-metadata evidence=unattempted
MEMBER qemu-alpine-ssh unexecuted classes=stdout-inspection,subprocess-exec evidence=unattempted
MEMBER qemu-startup unexecuted classes=file-artifact,shell-exec evidence=unattempted
MEMBER query-optimize unexecuted classes=crypto-credential,db-state,file-artifact,timing-wall evidence=external-db-required
MEMBER raman-fitting unexecuted classes=file-artifact,numeric-band,serialization-schema evidence=unattempted
MEMBER regex-chess unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER regex-log executed classes=file-artifact evidence=corpus/evidence/round36/regex-log-probe.txt [capture-tree/cases]
MEMBER reshard-c4-data unexecuted classes=crypto-credential,file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER rstan-to-pystan unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER sam-cell-seg unexecuted classes=file-artifact,serialization-schema,subprocess-exec evidence=unattempted
MEMBER schemelike-metacircular-eval unexecuted classes=file-artifact,stdout-inspection,subprocess-exec,timing-wall evidence=unattempted
MEMBER sparql-university unexecuted classes=file-artifact evidence=unattempted
MEMBER sqlite-db-truncate unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER sqlite-with-gcov executed classes=db-state,stdout-inspection,subprocess-exec evidence=corpus/evidence/round65/sqlite-gcov-probe.txt [receipt-header/predicate]
MEMBER torch-pipeline-parallelism executed classes=candidate-import,file-artifact,process-environment evidence=corpus/evidence/round67/pipe/receipt.txt [receipt-header/vectors]
MEMBER torch-tensor-parallelism executed classes=candidate-import,file-artifact,process-environment evidence=corpus/evidence/round66/tensor/receipt.txt [grader-path/predicate]
MEMBER train-fasttext unexecuted classes=file-artifact,filesystem-metadata evidence=unattempted
MEMBER tune-mjcf unexecuted classes=file-artifact,filesystem-metadata,numeric-band,timing-wall evidence=unattempted
MEMBER video-processing unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER vulnerable-secret unexecuted classes=file-artifact evidence=unattempted
MEMBER winning-avg-corewars unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER write-compressor unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
CLASS signal-delivery k=1 n=1 cell=executed 1 of 1
CLASS subprocess-exec k=10 n=45 cell=executed 10 of 45
CLASS shell-exec k=1 n=6 cell=executed 1 of 6
CLASS candidate-import k=3 n=6 cell=executed 3 of 6
CLASS file-artifact k=16 n=76 cell=executed 16 of 76
CLASS stdout-inspection k=8 n=29 cell=executed 8 of 29
CLASS numeric-band k=2 n=10 cell=executed 2 of 10
CLASS crypto-credential k=2 n=12 cell=executed 2 of 12
CLASS network-service k=4 n=8 cell=executed 4 of 8 (round 64 `kv-store-grpc`; round 68 `pypi-server` replayed offli
CLASS timing-wall k=3 n=9 cell=executed 3 of 9
CLASS filesystem-metadata k=2 n=10 cell=executed 2 of 10
CLASS process-environment k=2 n=3 cell=executed 2 of 3 (round 66, R66-C1 `torch-tensor-parallelism`; round 67, R67-C1 `
CLASS git-plumbing k=1 n=3 cell=executed 1 of 3
CLASS db-state k=1 n=2 cell=executed 1 of 2 (round 65, R65-C1 pass): `sqlite-with-gcov` replayed offline; `q
CLASS serialization-schema k=1 n=10 cell=executed 1 of 10
CLASS container-image k=0 n=0 cell=executed 0 of 0
COVERAGE replayed=24 covered=15 covered_located=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=24 unlocated=0 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
EXIT 0
Cloning into '/fast/scratch/hyaku/kengaku-r80/LedgerFlipAuditR80/lane'...
done.
HEAD is now at 6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows plus the V1 receipt and corrections (R80-C2), S258, lesson, index, wave spec/dispatch
```
Scratch existence check after the EXIT trap: `SCRATCH_REMOVED True`.

## Limits, retained evidence, and changes

Audited all six flips, all unchanged members/top-level fields, and all six historical receipts. Could not break field preservation or historical byte identity. This scoped audit did not replay the six round-80 instruments or run the C2 counter; those claims are not asserted here. Findings apply to the pinned measured commit, not future integrations. No failed command/check was observed.

Only this report was written in the lane; the shared clone was confined to the assigned scratch directory and removed before delivery. No source files, plans, gates, global configuration, or external substrate were modified. No tools were installed or updated. No implementation-symbol lookup was needed; no LSP tool is mounted in this seat. Parent owns any later integration verification.
