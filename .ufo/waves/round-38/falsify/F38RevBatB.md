# F38RevBatB — attack battery38 p10a.py / p10b.py (round 38 wave 2, falsify)

2026-10-26. Landed tip under attack `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`, verified with
`git -C $S/lane rev-parse HEAD` after `git clone -q --no-local` into
`/fast/scratch/hyaku/kengaku-r38/F38RevBatB` (`rev-parse --show-toplevel` = the clone). Lane files untouched:
`git status --porcelain -- plans/battery38` empty after all edits were reverted (confirm-restored.txt).

Scope: the three frozen mutants these two modules kill — N13, N14 (p10a), N15 (p10b), `adv` cells in
`plans/round38_c1_verify.py` MUTANTS lines 123–128. Question per seat brief: advertised behaviour, or
incidental kill (tailored `defects`, spec the gate never sees, second clause, side channel, name keying)?

## 1. Reproduction at the landing tip

`$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round38_c1_verify.py --lane $S/lane --only N13,N14,N15 --work $S/w` (only-n13-n14-n15.txt):

```
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N13 P10 silence killed by=p10a-n13-trailing-space -- a receipt differing only in trailing whitespace is not reproduced [docstring 'a receipt a fresh run does not reproduce'; F37XMutP910 L1]
MUTANT N14 P10 silence killed by=p10a-n14-first-line-only -- the receipt is compared beyond its first line [capability row '--rerun byte-compares the receipt'; F37XMutP910 L3]
MUTANT N15 P10 mirror killed by=p10b-rerun-byte-equal-accept -- a byte-equal fresh run passes P10 [Q24 genuine accepted; F37XMutP910 L2; R37PlanNext B5]
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
```

Matches measure-final.txt for these mutants. The battery phase enforces `observed_defects == declared`
exactly and `expect` rc on the REFERENCE run (wrong=0), so the declarations `["P10"]`/`[]` are not free.

## 2. Observable flip per fixture per mutant (attributable-kill evidence)

The counter prints only kill bookkeeping, so I rebuilt the three fixture dirs via the counter's own
`r37.Ctx` + `run_gate` + MUTANTS rows (read-only imports of the clone; harness + full output in
mutant-run-inspection.txt). Genuine spec facts printed by the harness: probe_cmd
`['plans/tb2_grader_probe.py', '--lane', '.']`, receipt `corpus/evidence/round35/tb2-grader-probe.txt`,
pin `2359d906…` — the fixtures override only what their docstrings say.

```
== p10a-n13-trailing-space declared=['P10'] expect=reject
   REF rc=1 DEFECT=['P10'] ok=['P1','P2','P3','P4','P5','P6','P7','P8','P9']
   N13  rc=0 DEFECT=[] ok=[all incl P10]
   N14  rc=1 DEFECT=['P10']      N15  rc=1 DEFECT=['P10']
== p10a-n14-first-line-only declared=['P10'] expect=reject
   REF rc=1 DEFECT=['P10'] ok=['P1'..'P9']
   N14  rc=0 DEFECT=[] ok=[all incl P10]
   N13  rc=1 DEFECT=['P10']      N15  rc=1 DEFECT=['P10']
== p10b-rerun-byte-equal-accept declared=[] expect=accept
   REF rc=0 DEFECT=[] ok=['P1'..'P10']   (genuine bytes pass every clause)
   N15  rc=1 DEFECT=['P10'] ok=['P1'..'P9']
   N13  rc=0 (accepted)          N14  rc=0 (accepted)
```

- Every kill is the mutant's own clause flipping and nothing else; no second clause appears in any
  reference or mutant run (P1–P9 all ok throughout). The p10a docstring's "P10 is the only clause that
  fires" holds at byte level.
- The mutated gate lines are exactly the P10 comparison (`pkg_gate.py` c_rerun: `if r.stdout != want:`)
  and its success return (`return True, f"probe_rerun=byte-equal`), matching the MUTANTS old/new cells.
- N13's fixture output is rstrip-equal but first-line-UNEQUAL; N14's is the inverse (checked:
  `rstrip-equal(out,want)=True | first-line-equal=False` vs `False | True`). So N14's `splitlines()[:1]`
  mutant still rejects the n13 fixture and N13's `rstrip` mutant still rejects the n14 fixture — the
  docstring's one-line-receipt orthogonality argument is arithmetically sound, not just asserted.

## 3. Load-bearing: delete each fixture, its mutant SURVIVES

Edits made in the clone at 8c7422d7 (verified `--show-toplevel` before each write), one at a time,
restored byte-exact after each (diff vs pristine copies), rerun each time.

| deleted | fixtures | N13 | N14 | N15 | receipt |
|---|---|---|---|---|---|
| p10a n13 fixture | 85 | **SURVIVED** | killed by=p10a-n14 | killed by=p10b | delete-n13.txt |
| p10a n14 fixture | 85 | killed by=p10a-n13 | **SURVIVED** | killed by=p10b | delete-n14.txt |
| p10b FIXTURES emptied | 85 | killed by=p10a-n13 | killed by=p10a-n14 | **SURVIVED** | delete-n15.txt |
| none (restored) | 86 | killed | killed | killed | confirm-restored.txt |

Each fixture is the sole killer of exactly its own mutant; `MUTANTS total=3 killed=2 survived=1` in each
deletion run. No other battery fixture (incl. battery37's `--rerun` p910 rejects) backfills any of the three.

## 4. Side channels and keying

- Token scan beyond the counter's 5-token heuristic, over both modules:
  `grep -nE "import os|getenv|environ|argv|/proc|ppid|cmdline|psutil|subprocess|socket|time\.|inspect|__file__|pkg_gate|open\("` → no matches (exit 1). Counter's own scan: `sidechannel=0`.
- Probe bodies (read in full): n13/n14 `import pathlib, sys`, read the spec's receipt relative path,
  write a fixed string; p10b probe is `import sys; sys.stdout.write(<constant>)`. No env, argv, timing,
  filesystem scan, or gate-file introspection; output is deterministic under either gate copy.
- Name keying: probes key on nothing but the spec's receipt path; the fid never reaches the gate. The
  counter's renamed-run control (scrambled dir names, rewritten argv) shows `renamed_disagree=0` in every
  run, so path/name-dependent behaviour would already have been caught.
- Owned-spec re-pinning (n13 rewrites receipt bytes + digest; p10b same): disclosed in both docstrings and
  constrained by the counter (`--spec` must resolve inside the fixture dir, else SETUP abort). Without the
  re-pin P2 would fire under both gates and there would be no kill at all — i.e. the re-pin is what keeps
  the kill attributable to P10, not a smuggled second clause. REF runs show P2 ok and P3–P8 ok on all three
  fixtures, so no check was neutered by the owned spec.

## 5. Findings

None. No defect found in p10a.py or p10b.py: all three kills are attributable to the advertised behaviour
named in the `adv` cell, each fixture is load-bearing, and no side channel or name keying exists.

Residual (counter-level, not fixture defects; outside this seat's edit scope):
- The silence rule (`attributed()`) does not require the mutant run's exit code to flip to 0 — a clause
  could vanish while another keeps rc=1 and still count as killed. Not exercisable here: both silence-kill
  mutant runs exit 0 with an empty DEFECT set.
- battery38 module bytes are not among the counter's 14 PINS; a post-landing battery edit would not trip
  `PINS mismatched`. The claims disclose non-author code review as the compensating control (this report).

Process note (my own seat, not the lane): two deletion runs initially aborted on a missing `--work` dir and
one ran against an already-restored file; all three deletion tests were redone cleanly — the archived
receipts are the redone runs.

Receipts (this dir): only-n13-n14-n15.txt, mutant-run-inspection.txt, delete-n13.txt, delete-n14.txt,
delete-n15.txt, confirm-restored.txt. Scratch `/fast/scratch/hyaku/kengaku-r38/F38RevBatB` removed after writing.

VERDICT: battery-p10a-p10b-attack-0-defects
