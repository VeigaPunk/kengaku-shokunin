# F40RevBatOrder — non-author honesty review of `plans/battery40/o_gate.py` (O04, O12, O14)

Lane tip ec1005a2a28bc5cfdde7723374368ed4cc956eed; every line of the module read; module bytes verified equal
to both the fleet lane file and a fresh clone at the tip (`cmp` twice, sha256 ffc40e5e…). All battery and
tool invocations ran inside the HOST-SAFETY bwrap line. Receipts:
`battery-run.txt`, `repro-build.txt`, `ref-mut-runs.txt` (this dir).

## Result: 3/3 fixtures honest

| fixture (o_gate.py) | verdict | exhibits | kill confirmed |
|---|---|---|---|
| o_gate-p10-ok-excuse :47-49 | **honest** | only a DEFECT line may carry the executed-nothing excuse; an `ok` P10 line is a hit (order_check.py:15-16, :107) | ref rc=1 `ORDER HIT … kind=gate-p10` → O04 rc=0 PASS |
| o_gate-claims-gitlink :53-55 | **honest** | the gate "reads every blob under claims/" (order_check.py:37); a 160000 commit entry is not a blob and is skipped (:131-134 only fires for collected blobs) | ref rc=0 PASS → O12 rc=2 `ORDER ERROR git cat-file blob 333333333333 rc=128` |
| o_gate-claims-bak-name :58-61 | **honest** | exit 2 setup error for a name that is not round-NN-claims.md; never a silent pass (order_check.py:26-27, :161-162) | ref rc=2 `ORDER ERROR claims file name is not round-NN-claims.md` → O14 rc=0 PASS |

The sandboxed counter run itself: `BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0`, `PINS total=3 mismatched=0`,
`PINS-AFTER mismatched=0`, rc=0 (battery-run.txt). Each fixture's declared expect/defects matched the
pinned reference's observed rc + class set exactly (`ok` on all three FIXTURE lines).

### f000 o_gate-p10-ok-excuse — honest
Builds a two-commit repo whose claims-dir control file reads `gate: P10 ok receipt unreadable`
(repro-build.txt, blob quote). Under the tool's contract the executed-nothing excuse is carried only by a
DEFECT line — order_check.py:107 `if not (m.group(1) == "DEFECT" and EXECUTED_EXCUSE.match(detail)):` — and
the tool's own comment names `P10 ok …` as proof the probe ran (order_check.py:56-59). The `gate: ` echo
prefix is explicitly in contract (order_check.py:52-53). The reference must and does hit; O04's dropped
DEFECT-only clause accepts the line and passes. The input is exactly the advertised case, no more.

### f001 o_gate-claims-gitlink — honest
The freeze commit's tree carries `160000 commit 3333…333 .ufo/waves/round-42/claims/vendored`
(ls-tree in repro-build.txt) — a legal git tree entry (submodule pin). The tool's limit sentence promises it
"reads every blob under claims/" (order_check.py:37), i.e. non-blob entries are not read; the reference skips
the entry (rc=0, scan counted file_entries=2 = the two blob visits). O12 removes the `parts[1] != "blob"`
guard, feeds the gitlink sha to `cat-file blob` and exits 2. The sha is absent from the fixture repo, but that
only makes the failure deterministic: `cat-file blob <commit>` fails identically on a present commit object
(type mismatch, order_check.py:132-134). A real repo with a vendored submodule pin under claims/ behaves the
same. Build artifact, noted: `git add -A` drops the index-only gitlink from the second commit; immaterial —
the scan visits the freeze commit's tree (commits=2 in the ref run), where the entry lives.

### f002 o_gate-claims-bak-name — honest
`--claims plans/round-42-claims.md.bak`; the tool's exit contract reserves 2 for an unparseable claims name
(order_check.py:26-27) and the name gate rejects before deciding (:161-162). The control line in claims/ is a
benign `P10 DEFECT receipt unreadable`, so the name gate is the only behavioural difference in play; the
reference errors without a verdict and O14's unanchored pattern accepts the `round-42-claims.md` prefix and
renders a PASS verdict (rc=0) — precisely the mutant's advertised failure mode.

## adv-cell verification
All three `adv` cells quote real sentences at the cited lines of the pinned tool (PINS mismatched=0 ⇒ tip
bytes = freeze bytes): O04 order_check.py:15-16; O12 :37; O14 :26-27. Witness citations (`.ufo/waves/round-40/
claims/witness-run.txt`, R39PlanNext.md:126) not re-read — the counter never reads them either; kills here are
independently reproduced.

## Wave-1 vector checklist — none used
| vector (wave 1) | finding |
|---|---|
| read tool/self program text at run time (A1 selfread) | module has zero imports, zero `open`/`read_text`; grep for `^import |^from |open(|read_text|environ|PATH|.clone|.lock|symlink`: no matches |
| write outside d — HOME / PATH dirs / sibling fixture dirs | all writes under `ctx.init(d/"repo")` (o_gate.py:26-44); counter's `Ctx._inside` (round40_c1_verify.py:248-251) enforces; build-child env has HOME=<counter work>/home (:421-424); repro tree contains only repo/ files |
| relative argv or symlink out of d (A4) | argv = one absolute `--lane` inside d (path_ok-verified, :326-330, :430-434) + two relative tokens that the tool resolves repo-internally and confines (order_check.py:82-91); zero symlinks in all three trees (repro-build.txt) |
| `.lock` / `.git/index` fingerprint-skip names (A5) | `.lock names: none` in all three trees; only .git/index is git's own from build-time commits; the tool writes nothing (order_check.py:29-31) and tampered=0 was measured |
| phase detection | build runs once in a pid-namespaced child before runs; its JSON carries only fid/tool/expect/defects/argv (:289-299); fixture code never executes during reference/mutant runs — no channel to branch on the variant |
| bare-string build() return (F2) | all three builds return a list of str via `gate_repo`'s `return ["--lane", …]` (o_gate.py:44); list-of-str contract-checked (:430-434) |
| fid="" kill-attribution hole (F6) | fids are three distinct non-empty strings |
| cross-module fixture forgery (sentinel attack) | no path leaves the module's own dest/fNNN; module never reads ctx.lane |
| git shim / PATH manipulation (A2) | no PATH or environment touching; git invoked only via ctx.git with the counter's fixed system PATH |

## Observations (not defects)
1. The counter's contract prose says defects includes "`fail:<name>` for each named ORDER FAIL line";
   f000's reference also prints the summary `ORDER FAIL probe-executed-before-receipt hits=1`, which the
   implementation excludes from the class set via a `" hits=" not in line` guard (round40_c1_verify.py:344-346).
   The module declares against the operative extraction — prose/implementation mismatch in the counter, not a
   battery dishonesty.
2. Fixture repos are synthetic round-42 stubs (3-line claims body vs the lane's real claims header); the gate
   only pattern-matches claims/-dir blobs, so behaviour is unaffected; shape parity noted in repro-build.txt.

## Residual risk & verification gaps
- Reviewed in isolation (`--battery-dir` + `--only`, dev mode, `PREDICATE C1 n/a`); the other six battery
  modules and the full-battery predicate are other seats' scope.
- The counter-side holes F1-F6 (R40RevCounters.md) live in the counter, not this module; o_gate exercises
  none of them (checklist above). F3's metadata-only fingerprint and F4's no-net-unshare sandbox remain
  counter-level risks that a battery module could theoretically exploit, but this module's builds and the
  tool's read-only command set (order_check.py:29-31) leave no writer.
- Equivalent mutants / direction mislabels: none observed — each mutant exhibited only its declared direction
  on these fixtures (ref-mut-runs.txt), and the counter's `exhibits=` machinery reported no survivors.

All three fixtures build inputs that exhibit the advertised reference behaviour honestly and kill their
mutants in the declared direction; no wave-1 attack vector is present.

VERDICT: battery-o_gate-honest-3/3
