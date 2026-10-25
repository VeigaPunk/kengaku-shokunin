ATTACKS: plans/attrib_calibration.py RG corners/clipping/pole, Wilson upper bound, and CP bisection stopping tolerance at archived 8ea41f9ed.
Axes: numeric fidelity; detector sensitivity; printed-verdict stability; exact-byte restoration. Assigned claim axis: novelty (canonical coverage).
Scope: six independent one-line mutants under S=/tmp/k25w2-MutRgBound/cases/<id>; no live lane source/index/state edits.
Setup: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 8ea41f9ed | tar -x -C /tmp/k25w2-MutRgBound`; each case copied pristine script, with grader/corpus symlinks into that archive.
Detector D: cwd=S; TMPDIR=S/tmp PYTHONDONTWRITEBYTECODE=1 `python3 plans/attrib_calibration.py --selftest`, timeout 90s; identical command on pristine, mutant, restored.
All six pristine AND restored D runs: exit 0, `selftest: 14 checks, 0 failed`; no inconclusive baselines/timeouts.
Also ran `python3 plans/attrib_calibration.py --summary`, numeric-witness.py, and synthetic-boundary --summary on all three byte states; all CLI exits 0 (numeric witness catches and prints exceptions).
Mutation results (locations refer to archived plans/attrib_calibration.py):
- rg_corners :182: Cartesian four corners -> diagonal (se_lo,sp_lo),(1,1). Expected A4; KILLED: exit 1, `selftest: 14 checks, 1 failed`, `selftest FAIL A4`; rg_bound(.5,.9,.9) [.44444444444444436,.5555555555555556] -> [.4999999999999999,.5].
- rg_coordinate :182: numerator q+sp-1 -> q+se-1. Expected A4; SURVIVED: exit 0, 14/0. rg_bound(.3,.9,.8) [.1250000000000001,.3333333333333334] -> [.22222222222222218,.37500000000000006].
- rg_clip_upper :183: remove upper min(1,...) clamp only. Expected A4 clipping check; SURVIVED: exit 0, 14/0. rg_bound(.95,.9,.9) [.9444444444444446,1] -> [.9444444444444446,1.0625].
- rg_equal_pole :180: <=0 -> <0. Expected A4 vacuous-J check; SURVIVED: exit 0, 14/0. rg_bound(.5,.4,.6) [0,1] -> `ZeroDivisionError: division by zero`.
- wilson_upper :163: upper centre+half -> centre-half. Expected A1 Wilson anchors; SURVIVED: exit 0, 14/0. wilson(7,50) [.06950833427016294,.2618619371058554] -> [.06950833427016294,.06950833427016294].
- cp_tolerance :134: adjacent-float stop -> `hi-lo <= 1e-12`. Expected A1/A2; SURVIVED: exit 0, 14/0; A2 worst tail residual 1.55e-11 (<1e-9). CP(7,50) lower .058191700340371855 -> .05819170034055787.
Why these survive: :862-865 RG anchors have equal sensitivity/specificity except a strictly-negative-J case; clipping anchor tests only q=0. :687-700 Wilson anchors check lower endpoints only. CP anchor tolerances admit the small stop error.
Frozen P1 --summary: all six mutants preserve every printed interval verdict (35 estimates; 48 output rows including shares/sensitivity). TOTAL remains PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12, scored_trials=92 correct=92, stored_checks=119 mismatches=0.
P1 printed numerical-row changes: rg_corners=6, rg_coordinate=4, rg_clip_upper=0, rg_equal_pole=0, wilson_upper=36, cp_tolerance=0 (six-decimal rendering).
Concrete surviving P1 corruption: rg_coordinate changes attrib-r21-impl-glm-trials.log:142-188 share:devin rg95=[0.215205,0.616349] -> [0.109719,0.543319]; Wilson changes impl-ds accuracy 20/20 wilson=[0.838875,1.000000] -> [0.838875,0.838875].
Printed-verdict counterexample OUTSIDE frozen P1: synthetic 7/50 receipt at /tmp/k25w2-MutRgBound/boundary-fixture/boundary.log, stated bar=0.05819170034046486 (midway between the two measured CP lowers).
Command: cwd=S; same TMPDIR/bytecode environment; `python3 plans/attrib_calibration.py --root /tmp/k25w2-MutRgBound/boundary-fixture --summary`.
cp_tolerance pristine -> mutated -> restored accuracy line: `interval=INDETERMINATE need_n=51` -> `interval=PASS` -> `interval=INDETERMINATE need_n=51`; all exit 0, while all three selftests pass. Both print cp95=[0.058192,0.267396].
This is an engineered near-boundary precision witness, NOT a changed 0.80 verdict in P1 or permission to alter the frozen contract.
Hash evidence: every pristine AND restored script SHA256 = 92aa873986cb19a171421b88ba2a2362ff171c4ba2365ef7b0387f7a5d811a51.
Mutant SHA256 rg_corners = df81c1db19656ddfb4a41807a09565cc902e799b60401fdc94e32821e38fe84a.
Mutant SHA256 rg_coordinate = 7d589421992b4e8071eabc4eb4b04b1900f34fd0c1569e6cbcb16671b4943ee1.
Mutant SHA256 rg_clip_upper = 5daf262d32ab113db61779f044396203a6c5e1f913acfa57610f43b2dc991ba2.
Mutant SHA256 rg_equal_pole = ba25742e59745b032679adeeae575ad53a2ca123bd461fac181bced2a781b288.
Mutant SHA256 wilson_upper = 17b7a8f2914113491371f1680c95a032c76068f4413010b201805be741c6d12d.
Mutant SHA256 cp_tolerance = ada1b9bd8acfea2a65c4350a135e9fe64e5f5255524efc63515f0946175afa7a.
Restoration: all six restored files byte-equal pristine archive; all four modes' stdout/stderr/exit statuses exactly equal their pristine outputs. Probe files restored, none left mutated.
Full actual stdout/stderr, command/cwd/exit/hashes: /tmp/k25w2-MutRgBound/probe-records.json; comparisons.json; cases/<id>/{pristine,mutated,restored}.{selftest,summary,numeric,boundary}.{stdout,stderr}; witness: numeric-witness.py.
Installs: none; existing Python 3.14.8, standard library only.
VERDICT: PARTIAL — 1/6 killed, 5/6 survived; frozen P1 verdicts survive, but numerical-output coverage gaps and an unflagged synthetic CP boundary flip are demonstrated.
