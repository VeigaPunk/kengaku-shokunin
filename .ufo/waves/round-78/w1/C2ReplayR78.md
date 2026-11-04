# C2ReplayR78 — independent R78-C2 replay

Axes: coverage and calibration. No counter was imported. Only this report and this seat's scratch were written; no lane implementation was changed. No tools installed. No build/lint/formatter or unrelated gate run. No LSP tool was available in this seat; this was byte-level receipt analysis, not a symbol refactor.

## Result

**C2-REPLAY: DISAGREE 7 items**

The seven disagreements with the frozen claim are: D1 semantic provenance is not checked; D2 digest comparison uses the audit context rather than the receipt tip; D3 SCORECARD is outside the universe; D4 missing/current-tip receipts are not required; D5 supplied-tool presence uses the audit context rather than the receipt tip; conflicting first stamps can be hidden by a second block; truncated digest pins are accepted despite the explicit full-digest kill rule. Existing original D2/D5 files are rejected for unrelated missing fields, not proof that their substantive defects are detected.

## 1. Replay commands, versions and observed outputs

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
`$S` was an exclusive mkdtemp directory under `$HYAKU_SCRATCH/kengaku-r78/C2ReplayR78/` (default `/fast/scratch/hyaku`). The clone was checked out detached at `2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8`; its `master` retained the observed lane master `cd2e25bb80cf618135cc001193df13966ef1c711`. Fixture roots were asserted with `git -C <root> rev-parse --show-toplevel` before mutations; no fixture commits or throwaway identities were needed.

Executed the requested live executable:

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round78_c2_stamp_location.py --lane "$S/clone" --rev 2f9eeafb --work "$S/counter-work"
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round78_c2_stamp_location.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --rev worktree --work "$S/counter-work"
```

The two **do not agree**: freeze-input rc 1, 16 receipts / 29 defects / 14 unlocated; worktree-input rc 0, 16 receipts / 0 defects / 0 unlocated. These are different input states, not an assertion that a repair should preserve the baseline verdict.

Important reproducibility qualification: the live executable was already modified from the freeze version. Its captured SHA-256 was `543fc7b057fe2eba2b36532175e900b56f7f44f97833dae5186523cb8df7382e`. The executable stored at freeze hashes `e79fe3fdee1348baa518a9327e19c6865ada4159a925f2efab24ac9fc4913a0b`. I therefore also extracted that committed executable to `$S/frozen-counter.py` and ran it without importing it. Its frozen-input output reproduces the advertised 27-defect / 13-unlocated baseline exactly. The live executable's newer block isolation loses the first block's tool on the original R75 receipt (second LANE_TIP at line 7), accounting for the two extra defects.

A later frozen-executable/worktree observation is also retained below, rather than concealed: by then master had advanced to `f20a2f6fcceb6769b48109d57904f52376190e44`, the universe had grown to 24 and round77/c2-before.txt had gained a TOOL_SHA without TOOL; rc 1, one TOOL-UNNAMED. This is a different concurrent snapshot, not a repeatable final integration verdict. No post-integration green is claimed.
### freeze

rc 1

```text
LANE_TIP 2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8
WORKTREE clean
UNIVERSE dirs=2 receipts=16
RECEIPT corpus/evidence/round77/c1-after.txt tip=4f2ff9be worktree=clean tool=- sha=- legs=COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c1-before.txt tip=07c97fcd worktree=clean tool=- sha=- legs=COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c1-control-declared.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c1-mutants.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c1-selftest.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-after.txt tip=4f2ff9be worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c2-before.txt tip=07c97fcd worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-control-status.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c2-mutants.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-selftest-git.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED
RECEIPT corpus/evidence/round77/c2-selftest.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/exec-attrib-calibration.txt tip=07c97fcd worktree=- tool=- sha=yes legs=WORKTREE-ABSENT,TOOL-UNNAMED
RECEIPT corpus/evidence/round77/exec-state-check.txt tip=07c97fcd worktree=- tool=- sha=yes legs=WORKTREE-ABSENT,TOOL-UNNAMED
RECEIPT corpus/evidence/round77/rerun-r51-c1.txt tip=9ebb8ed1 worktree=dirty tool=plans/round51_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r75-c1.txt tip=9ebb8ed1 worktree=dirty tool=- sha=- legs=COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/rerun-routed-open.txt tip=9ebb8ed1 worktree=dirty tool=plans/routed_open.py sha=yes legs=ok
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-after.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c1-after.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-before.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-control-declared.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-control-declared.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c1-control-declared.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-mutants.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-mutants.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-selftest.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-selftest.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-after.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-after.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c2-after.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-before.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-before.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-control-status.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-control-status.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c2-control-status.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-mutants.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-mutants.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-selftest-git.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-selftest.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-selftest.txt
DEFECT WORKTREE-ABSENT corpus/evidence/round77/exec-attrib-calibration.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/exec-attrib-calibration.txt
DEFECT WORKTREE-ABSENT corpus/evidence/round77/exec-state-check.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/exec-state-check.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/rerun-r75-c1.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/rerun-r75-c1.txt
DEFECTS n=29
TARGET receipts=16 located=2 unlocated=14
PREDICATE R78-C2 fail
```
### worktree

rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=16
RECEIPT corpus/evidence/round77/c1-after.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-before.txt tip=07c97fcd worktree=dirty tool=plans/round77_c1_declared_surfaces.py sha=- legs=ok
RECEIPT corpus/evidence/round77/c1-control-declared.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-mutants.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-selftest.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-after.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-before.txt tip=07c97fcd worktree=dirty tool=plans/round77_c2_defect_discharge.py sha=- legs=ok
RECEIPT corpus/evidence/round77/c2-control-status.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-mutants.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-selftest-git.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-selftest.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/exec-attrib-calibration.txt tip=07c97fcd worktree=dirty tool=plans/attrib_calibration.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/exec-state-check.txt tip=07c97fcd worktree=dirty tool=plans/state_check.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r51-c1.txt tip=cd2e25bb worktree=clean tool=plans/round51_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r75-c1.txt tip=cd2e25bb worktree=clean tool=plans/round75_c1_index_parity.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-routed-open.txt tip=cd2e25bb worktree=clean tool=plans/routed_open.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=16 located=16 unlocated=0
PREDICATE R78-C2 pass
```
### frozen-executable-freeze

rc 1

```text
LANE_TIP 2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8
WORKTREE clean
UNIVERSE dirs=2 receipts=16
RECEIPT corpus/evidence/round77/c1-after.txt tip=4f2ff9be worktree=clean tool=- sha=- legs=COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c1-before.txt tip=07c97fcd worktree=clean tool=- sha=- legs=COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c1-control-declared.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c1-mutants.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c1-selftest.txt tip=51ffc14f worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-after.txt tip=4f2ff9be worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c2-before.txt tip=07c97fcd worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-control-status.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/c2-mutants.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/c2-selftest-git.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED
RECEIPT corpus/evidence/round77/c2-selftest.txt tip=6f0c7ad9 worktree=dirty tool=- sha=yes legs=TOOL-UNNAMED,COMMAND-ABSENT
RECEIPT corpus/evidence/round77/exec-attrib-calibration.txt tip=07c97fcd worktree=- tool=- sha=yes legs=WORKTREE-ABSENT,TOOL-UNNAMED
RECEIPT corpus/evidence/round77/exec-state-check.txt tip=07c97fcd worktree=- tool=- sha=yes legs=WORKTREE-ABSENT,TOOL-UNNAMED
RECEIPT corpus/evidence/round77/rerun-r51-c1.txt tip=9ebb8ed1 worktree=dirty tool=plans/round51_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r75-c1.txt tip=9ebb8ed1 worktree=dirty tool=plans/round75_c1_index_parity.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-routed-open.txt tip=9ebb8ed1 worktree=dirty tool=plans/routed_open.py sha=yes legs=ok
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-after.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c1-after.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-before.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-control-declared.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-control-declared.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c1-control-declared.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-mutants.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-mutants.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c1-selftest.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c1-selftest.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-after.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-after.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c2-after.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-before.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-before.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-control-status.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-control-status.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/c2-control-status.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-mutants.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-mutants.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-selftest-git.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-selftest.txt
DEFECT COMMAND-ABSENT corpus/evidence/round77/c2-selftest.txt
DEFECT WORKTREE-ABSENT corpus/evidence/round77/exec-attrib-calibration.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/exec-attrib-calibration.txt
DEFECT WORKTREE-ABSENT corpus/evidence/round77/exec-state-check.txt
DEFECT TOOL-UNNAMED corpus/evidence/round77/exec-state-check.txt
DEFECTS n=27
TARGET receipts=16 located=3 unlocated=13
PREDICATE R78-C2 fail
```
### frozen-executable-worktree

rc 1

```text
LANE_TIP f20a2f6fcceb6769b48109d57904f52376190e44
WORKTREE dirty
UNIVERSE dirs=2 receipts=24
RECEIPT corpus/evidence/round77/c1-after.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-before.txt tip=07c97fcd worktree=dirty tool=plans/round77_c1_declared_surfaces.py sha=- legs=ok
RECEIPT corpus/evidence/round77/c1-control-declared.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-mutants.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c1-selftest.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-after.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-before.txt tip=07c97fcd worktree=dirty tool=plans/round77_c2_defect_discharge.py sha=yes legs=TOOL-UNNAMED
RECEIPT corpus/evidence/round77/c2-control-status.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-mutants.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-selftest-git.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c2-selftest.txt tip=cd2e25bb worktree=clean tool=plans/round77_c2_defect_discharge.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/exec-attrib-calibration.txt tip=07c97fcd worktree=dirty tool=plans/attrib_calibration.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/exec-state-check.txt tip=07c97fcd worktree=dirty tool=plans/state_check.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r51-c1.txt tip=cd2e25bb worktree=clean tool=plans/round51_surfaces.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-r75-c1.txt tip=cd2e25bb worktree=clean tool=plans/round75_c1_index_parity.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/rerun-routed-open.txt tip=cd2e25bb worktree=clean tool=plans/routed_open.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c1-after.txt tip=f20a2f6f worktree=clean tool=plans/round78_c1_class_member_ledger.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c1-before.txt tip=f20a2f6f worktree=clean tool=plans/round78_c1_class_member_ledger.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c1-control-prose.txt tip=f20a2f6f worktree=clean tool=plans/round78_c1_class_member_ledger.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c1-mutants.txt tip=f20a2f6f worktree=clean tool=plans/round78_c1_class_member_ledger.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c1-selftest.txt tip=f20a2f6f worktree=clean tool=plans/round78_c1_class_member_ledger.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c2-before.txt tip=f20a2f6f worktree=clean tool=plans/round78_c2_stamp_location.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c2-mutants.txt tip=f20a2f6f worktree=clean tool=plans/round78_c2_stamp_location.py sha=yes legs=ok
RECEIPT corpus/evidence/round78/c2-selftest.txt tip=f20a2f6f worktree=clean tool=plans/round78_c2_stamp_location.py sha=yes legs=ok
DEFECT TOOL-UNNAMED corpus/evidence/round77/c2-before.txt
DEFECTS n=1
TARGET receipts=24 located=23 unlocated=1
PREDICATE R78-C2 fail
```
## 2. Independent four-stamp digest recomputation

Each digest below was produced by the actual binary pipeline, not by counter code:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -p <receipt-LANE_TIP>:<tool-path> | sha256sum
```

The freeze battery omits TOOL: its actual producer path below is independently identified from the battery/closure, **not** presented as a TOOL line that exists in the receipt. Frozen receipts were obtained via `git show 2f9eeafb:<receipt>`; worktree rows were read during the original 16-receipt snapshot. All receipt names below have prefix `corpus/evidence/round77/`.

| snapshot | receipt | stamped tip | tool | receipt pin | recomputed digest | result |
|---|---|---|---|---|---|---|
| `freeze` | `rerun-r51-c1.txt` | `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb` | `plans/round51_surfaces.py` | `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e` | `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e` | `AGREE` |
| `freeze` | `rerun-r75-c1.txt` | `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb` | `plans/round75_c1_index_parity.py` | `f69ab60b8dd06fc6076d2731b40ee0f4ec52e81602823b3b8fddc3c8fe88f81f` | `f69ab60b8dd06fc6076d2731b40ee0f4ec52e81602823b3b8fddc3c8fe88f81f` | `AGREE` |
| `freeze` | `rerun-routed-open.txt` | `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb` | `plans/routed_open.py` | `3ce44d941b14a28c88f8f87dec22c390f8a2eedf19cd0e219494b2cd3b82418b` | `3ce44d941b14a28c88f8f87dec22c390f8a2eedf19cd0e219494b2cd3b82418b` | `AGREE` |
| `freeze` | `c1-selftest.txt` | `51ffc14f2f4cb1f14e08045778ae7df11d73ae32` | `plans/round77_c1_declared_surfaces.py` | `a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571` | `5a507c086ea8bf7e4a2f604fd37a1173065e89911812d38b8a75422e886b1bd3` | `DISAGREE` |
| `worktree` | `rerun-r51-c1.txt` | `cd2e25bb80cf618135cc001193df13966ef1c711` | `plans/round51_surfaces.py` | `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e` | `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e` | `AGREE` |
| `worktree` | `rerun-r75-c1.txt` | `cd2e25bb80cf618135cc001193df13966ef1c711` | `plans/round75_c1_index_parity.py` | `f69ab60b8dd06fc6076d2731b40ee0f4ec52e81602823b3b8fddc3c8fe88f81f` | `f69ab60b8dd06fc6076d2731b40ee0f4ec52e81602823b3b8fddc3c8fe88f81f` | `AGREE` |
| `worktree` | `rerun-routed-open.txt` | `cd2e25bb80cf618135cc001193df13966ef1c711` | `plans/routed_open.py` | `3ce44d941b14a28c88f8f87dec22c390f8a2eedf19cd0e219494b2cd3b82418b` | `3ce44d941b14a28c88f8f87dec22c390f8a2eedf19cd0e219494b2cd3b82418b` | `AGREE` |
| `worktree` | `c1-selftest.txt` | `cd2e25bb80cf618135cc001193df13966ef1c711` | `plans/round77_c1_declared_surfaces.py` | `a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571` | `a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571` | `AGREE` |

The three original rerun tools genuinely match their pins: **matching tool bytes do not imply matching input data or verdict**. Independently reading the stamped `9ebb8ed1:plans/round51-surfaces.json` found `SF14.count_claim=244`; counting `^\|\s*S[0-9]{3,}\s*\|` in the stamped `corpus/SOURCES.md` found **245**. Thus D1 is not a tool-digest mismatch.

## 3. D1–D5 catch matrix (frozen predicate)

“Rejected” here is distinct from “detects the routed defect.” Original receipt line citations refer to committed `2f9eeafb` bytes.

| defect | substantive detection | concrete evidence / escaping line |
|---|---|---|
| D1 — rerun verdict not reproducible at its named revision | **No.** No predicate replay or data-input binding. | `corpus/evidence/round77/rerun-r51-c1.txt:1` stamps `9ebb8ed1…`; `:16` says `NUMBER-DRIFT 0`; `:22` says `PREDICATE R51-C1 pass`. Frozen replay prints `legs=ok`. `rerun-r75-c1.txt:12` also says pass and frozen replay prints `legs=ok`. |
| D2 — batteries carry post-fix tool digest at pre-fix tip | **Not semantically.** Original battery files are rejected structurally (`TOOL-UNNAMED`, often `COMMAND-ABSENT`), but wrong-tip digest itself is not compared at the receipt tip. | `corpus/evidence/round77/c1-selftest.txt:1` stamps `51ffc14f…`; `:3` pins `a4777acf…`, whereas that stamped tool is `5a507c08…`. Original file does not wholly slip through because it omits TOOL; the independent `old-tip-new-digest` fixture adds the real path and command and passes, retaining exactly this false old-tip/new-tool pairing. |
| D3 — stale SCORECARD after-stamp prose | **No.** SCORECARD is not in either evidence directory. | `SCORECARD.md:3564` and `:3565` at freeze say after receipts are stamped `d181e16b`; `corpus/evidence/round77/c1-after.txt:1` instead names `4f2ff9be`. No receipt-local check can reject an out-of-universe SCORECARD line; there is no honest “receipt line” containing the SCORECARD prose itself. |
| D4 — absent final-tip rerun block | **No.** No expected-receipt inventory or equality-to-final-tip requirement; any ancestor is accepted. | `corpus/evidence/round77/rerun-routed-open.txt:1` stamps `9ebb8ed1…`; `:7` says `ROWS total=86 open=31 blocked=1 closed=52 refused=2`, not the closure's final-tip 93. It receives `legs=ok`. Missing receipt bytes cannot be detected by enumerating only files that exist. |
| D5 — clean before-run with an untracked supplied tool | **Not semantically.** Original C1 before receipt is rejected for `COMMAND-ABSENT`, but its clean/supplied issue is not detected. | `corpus/evidence/round77/c1-before.txt:2` stamps `07c97fcd…`; `:3` says `WORKTREE clean`; `:46` is `PREDICATE R77-C1 fail`. It names no TOOL, so presence cannot even be tested. Independent `supplied-clean-absent-old-tip` fixture explicitly names the supplied C1 tool, keeps this old tip + clean state, and passes. |

Cause observed in both captured executable versions: `exists_at` and `tool_digest` address `self.tip`, established by `Ctx` from audit `--rev` or `master`, not the parsed per-receipt tip. In the fixture, master is `cd2e25bb…` while the receipt says `51ffc14f…` or `07c97fcd…`. This is not an inference from comments; the accepted counterexamples below exercise it. Actual original D2 and D5 files are red overall, but that is weaker than closing the routed defect classes.

## 4. Two requested loopholes and additional frozen-rule controls

Fixtures used a scratch-only clone/copy, preserving committed history and a local master ref; only that copy's evidence directories were replaced. The sole test receipt was `corpus/evidence/round77/probe.txt`. Each body below was written under `$S`, then both captured executables were invoked in worktree mode:

```sh
python3 "$S/frozen-counter.py" --lane "$S/fixture-copy" --work "$S/counter-work"
python3 "$S/observed-counter.py" --lane "$S/fixture-copy" --work "$S/counter-work"
```

**Stale TOOL_SHA with no TOOL: No, it cannot pass** for a valid recognized stale pin. Both versions returned rc 1 and `TOOL-UNNAMED` (plus `PASS-UNLOCATED` for this passing-predicate fixture). This answer does not assume an unnamed tool can be reverse-inferred from its digest.

**False first block followed by a valid second stamp: Yes, it can pass.** The first block has an unresolved all-f tip, nonexistent tool, all-zero digest and `PREDICATE fabricated pass`; the appended block has a real master tip and correct tool pin, but never retracts that predicate. Both versions returned rc 0. No `STAMP-CONFLICT` or `TIP-UNRESOLVED` fired. Frozen code takes each field's final match globally; the captured live version isolates the last block, but still does not reject the conflicting first stamp.

Additional cheap counterexamples exercise the substantive D2/D5 legs and the frozen kill rule: `old-tip-new-digest`, `supplied-clean-absent-old-tip`, and `truncated-pin` all returned rc 0 in **both** versions. The truncated pin is the first eight hex characters of the actual tool digest (`a4777acf`), not a full digest: the frozen full-digest refusal kill rule therefore fails.
### Fixture: stale-no-tool

Exact receipt body:

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE clean
TOOL_SHA 0000000000000000000000000000000000000000000000000000000000000000
COMMAND python3 plans/round77_c1_declared_surfaces.py
PREDICATE probe pass
```
frozen: rc 1

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,PASS-UNLOCATED
DEFECT TOOL-UNNAMED corpus/evidence/round77/probe.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/probe.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
```
observed: rc 1

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=- sha=yes legs=TOOL-UNNAMED,PASS-UNLOCATED
DEFECT TOOL-UNNAMED corpus/evidence/round77/probe.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/probe.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
```
### Fixture: false-first-appended-valid

Exact receipt body:

```text
LANE_TIP ffffffffffffffffffffffffffffffffffffffff
WORKTREE clean
TOOL missing.py
TOOL_SHA 0000000000000000000000000000000000000000000000000000000000000000
COMMAND false
PREDICATE fabricated pass
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE clean
TOOL plans/round77_c1_declared_surfaces.py
TOOL_SHA a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571
COMMAND python3 plans/round77_c1_declared_surfaces.py
```
frozen: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
observed: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
### Fixture: old-tip-new-digest

Exact receipt body:

```text
LANE_TIP 51ffc14f2f4cb1f14e08045778ae7df11d73ae32
WORKTREE clean
TOOL plans/round77_c1_declared_surfaces.py
TOOL_SHA a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571
COMMAND python3 plans/round77_c1_declared_surfaces.py
PREDICATE fabricated pass
```
frozen: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=51ffc14f worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
observed: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=51ffc14f worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
### Fixture: supplied-clean-absent-old-tip

Exact receipt body:

```text
LANE_TIP 07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59
WORKTREE clean
TOOL-SUPPLIED plans/round77_c1_declared_surfaces.py
COMMAND python3 plans/round77_c1_declared_surfaces.py
PREDICATE fabricated pass
```
frozen: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=07c97fcd worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=- legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
observed: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=07c97fcd worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=- legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
### Fixture: truncated-pin

Exact receipt body:

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE clean
TOOL plans/round77_c1_declared_surfaces.py
TOOL_SHA a4777acf
COMMAND python3 plans/round77_c1_declared_surfaces.py
PREDICATE fabricated pass
```
frozen: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
observed: rc 0

```text
LANE_TIP cd2e25bb80cf618135cc001193df13966ef1c711
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/probe.txt tip=cd2e25bb worktree=clean tool=plans/round77_c1_declared_surfaces.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
```
## Limits, risks and handoff

- This is an independent replay/attack report, not a repair, adjudication or acceptance decision. No frozen target/control/kill rule was changed.
- The live tree and executable were moving. Snapshot identities and exact outputs above avoid treating an intermediate green as a final gate. Parent owns the final integrated run.
- No counter import, selftest-mode fixture helper, counter monkeypatch, gate implementation change, external source mutation, commit, push or tool install was used. A scratch fixture clone initially lacked local master because its source HEAD was detached; after root assertion a fixture-only `master` branch was created from `refs/remotes/origin/master`. No lane ref was changed.
- Scratch paths are not citable evidence; the exact relevant bodies, digest output and counter output are retained in this report. Scratch was removed before yield.
- No blocker remains for this scoped investigation. Implementation risks to route: own-tip digest/presence binding, verdict-data provenance, out-of-universe D3/D4 obligations, stamp-conflict handling and full-pin enforcement.

## Self-evaluation

| axis | score | evidence / improvement |
|---|---:|---|
| accuracy | 4 | Exact outputs and hashes retained; concurrent worktree is not atomic. Prefer parent immutable-tip acceptance measurement. |
| completeness | 5 | Both requested commands, four original plus four repaired digest rows, five-defect matrix, two loopholes and exact fixture outputs retained. |
| clarity | 4 | Structural rejection versus substantive detection is separated; extensive raw output could be moved to a sidecar if more report files were allowed. |
| actionability | 4 | Reproduction bodies and executable identities supplied; repairs intentionally outside this read-only seat. |
| conciseness | 4 | Full outputs are repetitive but preserve the requested evidence after scratch deletion. |

Overall 4.2/5. Highest-impact improvements: use an immutable parent integration tip; preserve the structural/semantic distinction when routing D2/D5. Would the user agree? Likely: all requested observations are retained, with intermediate-state limits explicit.
