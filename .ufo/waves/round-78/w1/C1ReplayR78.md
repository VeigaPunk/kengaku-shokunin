# C1ReplayR78 — independent executor

Axes: coverage (member accounting) and calibration (accuracy of the claimed evidence). No lane implementation changes. No installations, commits, grader execution, or external-state remediation.

## Revision and method

Shared clone: `/fast/scratch/hyaku/kengaku-r78/C1ReplayR78/clone`; clone top-level was printed and matched that exact path before checkout. Checked out `2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8`; clone master resolved to the same revision. `3ae0ab540c35fe40da048198f3e5d4042766b2b7` was observed to be its ancestor. Claims file read in full before commands. Scratch removed after investigation.

Required counter invocation (twice, substituting REV):

```text
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round78_c1_class_member_ledger.py --lane /fast/scratch/hyaku/kengaku-r78/C1ReplayR78/clone --rev REV
```

Counter was executed as a process, never imported. Independent evidence used `git -C <clone> show master:<path>`, `cat-file -e master:<receipt>`, and standard-library JSON/regex inspection of those committed bytes. Frozen detector patterns were independently applied to both grader files; dedicated grep-tool searches supplied numbered matches (the required equivalent of grep -nE under the tool policy). No LSP symbol/refactor work was needed; no LSP tool was exposed.

## Required replay outputs (verbatim selected lines)

`REV=2f9eeafb`, rc **0**:

```text
UNIVERSE classes=3 members=12 pairs=13
LEDGER rows=12 executed=7 unexecuted=5
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

`REV=3ae0ab54`, rc **1**:

```text
UNIVERSE classes=3 members=12 pairs=13
LEDGER rows=0 executed=0 unexecuted=0
DEFECTS n=21
TARGET classes=3 members=12 executed=0 unexecuted=0 unaccounted=12 unbacked=0
PREDICATE R78-C1 fail
```

Base defect decomposition actually printed: CLASS-ROW-UNLINKED ×3; MEMBER-UNACCOUNTED ×12; COUNT-DRIFT ×3; COVERAGE-REGRESSION ×3. Total 21, not 19.

## Executed members — all seven independently backed

Every receipt below passed `git -C <clone> cat-file -e master:<path>` (rc 0), and was read with `git show master:<path>`. Line numbers are receipt-local. No receipt path or verdict mismatch found.

| Member | Classes | Tracked receipt | Exact matching line |
|---|---|---|---|
| hf-model-inference | network-service | corpus/evidence/round71/hf/receipt.txt | 36: `PREDICATE R71-C1 pass` |
| kv-store-grpc | network-service | corpus/evidence/round64/kvstore-probe.txt | 66: `PREDICATE R64-C1 pass` |
| nginx-request-logging | network-service | corpus/evidence/round70/nginx/receipt.txt | 78: `PREDICATE R70-C1 pass` |
| pypi-server | network-service | corpus/evidence/round68/pypi/receipt.txt | 12: `PREDICATE R68-C1 pass` |
| sqlite-with-gcov | db-state | corpus/evidence/round65/sqlite-gcov-probe.txt | 67: `PREDICATE R65-C1 pass` |
| torch-pipeline-parallelism | process-environment | corpus/evidence/round67/pipe/receipt.txt | Six exact VECTOR lines below; zero `frozen=mismatch` occurrences |
| torch-tensor-parallelism | process-environment | corpus/evidence/round66/tensor/receipt.txt | 47: `PREDICATE R66-C1 pass` |

```text
7:VECTOR q1-ref exists=P no_hooks=P ws1=P ws2=P frozen=match
9:VECTOR q2-none exists=F no_hooks=F ws1=F ws2=F frozen=match
11:VECTOR q3-stub exists=P no_hooks=P ws1=F ws2=F frozen=match
13:VECTOR q4-hooks-noop exists=P no_hooks=F ws1=P ws2=P frozen=match
15:VECTOR q5-full-model exists=P no_hooks=P ws1=P ws2=F frozen=match
17:VECTOR q6-unscaled-loss exists=P no_hooks=P ws1=F ws2=F frozen=match
```

## Unexecuted members — all five detectors fire

Paths below are relative to `corpus/evidence/round52/graders/<member>/tests/`. Both `test_outputs.py` and `test.sh` were read from committed master. Each row accounts for one distinct member; Windows belongs to two classes.

| Member / classes | Typed reason | Independently observed matching bytes | Honest offline assessment |
|---|---|---|---|
| filter-js-from-html / network-service | browser-required | test_outputs.py:12 `from selenium import webdriver`; :127 `driver = webdriver.Chrome(options=chrome_options)`; test.sh:21 `-w selenium==4.38.0` | [INFERENCE] Browser execution is compatible with offline operation if Chrome/driver/Python dependencies and the GitHub test-vector archive are cached. The grader unconditionally downloads the archive at :28–31 and :228, so a browser alone is insufficient. Missing-driver exceptions can return no-alert (:151–155), but exploiting that would not constitute an honest browser replay. No complete offline input bundle was established. Reason proves a dependency, not impossibility. |
| git-multibranch / network-service | network-install-required | test_outputs.py:12 `apt-get update`; :13 `DEBIAN_FRONTEND=noninteractive apt-get install -y curl expect git openssh-client`; test.sh:4 same apt update/install pattern | [INFERENCE] An offline apt repository/cache could satisfy setup without changing the grader. Its actual SSH clone/push and HTTPS probes use localhost (:26, :43, :56, :72–73), not a remote service. Thus a genuine offline replay is plausible with a prebuilt environment, local SSH/git/deploy/nginx services and package metadata; not demonstrated here. The reason accurately detects installation commands but does not prove network access is intrinsically necessary. |
| headless-terminal / network-service | candidate-library-required | test_outputs.py:8 `sys.path.append("/app")`; :13 `from headless_terminal import HeadlessTerminal`; repeated imports at :18,32,57,84,99,120 | [INFERENCE] A real PTY-backed candidate package plus bash/vim and Python dependencies could run entirely offline; its HTTP check is localhost:8000 (:124–129). This is an execution-scope/missing-candidate reason, not an offline impossibility. Lane master tracks only the two grader files under this task name, not a candidate package. Providing an implementation would be additional work, not evidence that this row has already executed. |
| install-windows-3.11 / network-service, process-environment | vm-required | test_outputs.py:16 `return Path("/app/isos/win311.img")`; :21 `result = subprocess.run(["pgrep", "qemu-system"], capture_output=True, text=True)`; :98 qemu architecture check; :262 image path | [INFERENCE] QEMU, nginx/VNC and a cached authentic disk image can run offline. Here the image hash is checked (:84–89) and core-file hashes are checked (:209 onward); process-name or command-line simulation alone is not an honest replay. No tracked path containing win311.img was found. A complete authentic-image offline replay was not established, but VM-required is not equivalent to internet-required. |
| query-optimize / db-state | external-db-required | test_outputs.py:11 `GOLDEN_SQL_PATH = Path("/tests/golden.sql")`; :78 `hash = hashlib.sha256(DB_PATH.read_bytes()).hexdigest()` | [INFERENCE] With the exact database and golden SQL cached, SQLite execution is offline; the five-iteration median threshold (:15, :109–142) is real and may be noisy, not inherently impossible. Master has zero tracked paths containing oewn.sqlite or golden.sql; under the task name it carries only the two grader files. Fabricating another DB fails the pinned SHA check (:77–79). No complete offline replay from the stored lane bytes was established. |

Detector patterns independently applied:

```text
browser-required: selenium|webdriver\.Chrome|webdriver\.Firefox|chromedriver
vm-required: qemu-system|qemu-img|/app/isos/
network-install-required: apt-get install|apt-get update|uvx \\\n|-w selenium==|pip install
external-db-required: GOLDEN_SQL_PATH|/tests/golden\.sql|sha256\(DB_PATH\.read_bytes\(\)\)
candidate-library-required: from headless_terminal import|import headless_terminal|sys\.path\.append\("/app"\)
```

The network-install detector includes a literal newline alternative after `uvx`; its apt alternatives alone already match both stored files. No reason detector failure found. These are dependency-presence detectors, not proofs that offline replay cannot be engineered. No host cache availability or successful grader execution is claimed.

## Independent universe arithmetic

Grepped SKILL.md partial rows at lines 78/81/83 and the census CLASS lines at 11/14/16, then independently parsed committed master bytes. Census lines:

```text
CLASS network-service count=8 members=filter-js-from-html,git-multibranch,headless-terminal,hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server
CLASS process-environment count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism
CLASS db-state count=2 members=query-optimize,sqlite-with-gcov
```

| Class | Census members | Independently counted executed | SKILL k/n | Ledger pointer present |
|---|---:|---:|---|---|
| network-service | 8 | 4 | 4/8 | yes |
| process-environment | 3 | 2 | 2/3 | yes |
| db-state | 2 | 1 | 1/2 | yes |

13 pairs = 8+3+2. Distinct union = 12 because install-windows-3.11 is the only overlap. All ledger class sets exactly match census membership (membership-error list empty). Seven distinct executed members, five distinct unexecuted members; six unexecuted member-class pairs. All three SKILL rows contain `ledger=plans/grader-selected-members.json`. Arithmetic 12/13 and k=4/2/1 is correct.

## Mismatches, risks, and verdict

1. **Observed baseline differs from assignment summary:** same requested command at `3ae0ab54` prints `DEFECTS n=21`, not the supplied 19. Reproduction and complete defect-class multiplicities are above. Red-before and green-after still hold.
2. **Frozen out-of-scope prose counts six unexecuted “members”:** the frozen claims file says “Simulating the 6 unexecuted members.” There are five distinct unexecuted members and six unexecuted class-member pairs. Likewise its “13-member map” is a pair map, not a 13-distinct-member universe. Treat this as one member-versus-pair terminology discrepancy; no predicate/target/control/kill-rule change proposed.

No ledger-member, receipt-verdict, class-membership, detector, or k/n mismatch found. C1's machine predicate is independently supported at the frozen revision. Offline assessments above are explicitly conditional: reasons justify an unexecuted accounting status but must not be promoted to impossibility claims. Full dynamic replay of the five graders was outside this item. No blocker.

C1-REPLAY: DISAGREE 2 items

## Delivery self-check

Accuracy 4/5: exact receipts and both counter outcomes retained; offline possibilities remain conditional, not executed. Completeness 4/5: all twelve members and thirteen pairs covered; no host-cache census attempted. Clarity 4/5: tables distinguish rows/pairs; detector newline representation is technical. Actionability 4/5: exact reproducer retained; parent owns any correction to baseline prose. Conciseness 4/5: longer report preserves the requested per-member evidence. Overall 4.0/5. Improvements: keep baseline at observed 21; distinguish five members from six pairs; do not equate dependency detection with offline impossibility. The user should agree with the narrower, evidence-backed machine-predicate conclusion.
