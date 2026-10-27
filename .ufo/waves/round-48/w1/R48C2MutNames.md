# R48C2MutNames — case/tag-name mutation probe

**Axes named:** coverage (counter sensitivity to fixture/case-key renaming); verdict status (killed/survived/inconclusive).

**VERDICT: INCONCLUSIVE for the frozen R48-C2 counter; coverage finding on the prior round-46 detector only.** The stage-1 freeze is present at measured revision `a543d92083557dd9b33ee674e9b99b03411f80af` (commit time `2026-10-27 06:53:29 -0300`, claims file present, ancestor of `master`). `plans/round48_c2_verify.py` is absent there, so no R48-C2 scored counter run was made. The round-48 claim explicitly bars C2 package probes before stage 2. I used only the previously committed round-46 counter's six substantive table legs directly (no full counter invocation, no V2 gate/P10, no R48 scored execution). Consequently these results do not establish R48-C2 admission or its new counter's behavior.

## Method and exact commands

Scratch clone was made with `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` under `/fast/scratch/hyaku/kengaku-r48/R48C2MutNames`; checked out with `git -C lane checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`. Before edits, verified the fixture root using `git -C "$D" rev-parse --show-toplevel`; it equaled `$D`. The measured revision (`REV`): `a543d92083557dd9b33ee674e9b99b03411f80af`.

Detector was the exact `round46_c3_verify.run_legs` implementation, invoked identically on pristine and mutated bytes with `which=('V3','V4','V7','V9','V10','V12')`. It deliberately omitted V2 (gate/P10) and did not execute the probe; no scored counter/probe run occurred. Mutation procedure consistently substituted all 18 case ids in the dry table, receipt, knowledge entry, and probe; separately substituted all seven tags in those same four files. IDs became `zzc-00`…`zzc-11` and `zzc-0c`…`zzc-11` (18 total, sequential hex indices); tags became `zzt-00`…`zzt-06`. Mutations were confined to the scratch clone and restored in `finally`.

## Observed outputs (verbatim)

Pristine:
```
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
```

All case ids renamed:
```
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V9 ok case_rows=18/18 bad=0
V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
V12 ok rows=7 defective=0 live=0
```

All tags renamed:
```
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | zzt-03 | not exercised | no f'", "unparsed row '| instruction.md:9 | zzt-06 | not exercised | no f'", "tags missing=['zzt-03', 'zzt-06'] duplicated=0"]
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
```

**Mutant:** consistent case-key and tag-key renaming in the package copy. **Expected detector:** at least one substantive leg flips pass→DEFECT for a rename mutant. **Observed:** case rename causes V10 pass→DEFECT (`DECISIVE` remains keyed to frozen ids); the other case legs remain unchanged. Tag rename leaves the set of substantive leg pass/fail statuses unchanged; V7 was already DEFECT on pristine bytes and remains DEFECT, with names merely changed in its existing errors. Thus the case-key mutant is killed by V10; the tag-key mutant is inconclusive as a kill test because baseline V7 already fails, not a demonstrated surviving mutation against a passing baseline. Results show V10's case-id vocabulary is name-sensitive. They do not show a clean-baseline substantive tag-name sensitivity result. No contract is changed or inferred.

## Hashes and restoration

Before hashes (SHA-256):
- `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`: `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`
- `corpus/evidence/round46/polyglot-c-py-probe.txt`: `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`
- `corpus/knowledge/tb2-polyglot-c-py-grader.md`: `4c05769fd8b43905e1b84873fafc53e61c18f1e4cba031392953b564200a6073`
- `plans/polyglot_c_py_probe.py`: `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`

After hashes matched all four before hashes exactly (`RESTORED` was `{"…dry-cases-freeze.txt": true, "…probe.txt": true, "…grader.md": true, "plans/polyglot_c_py_probe.py": true}`); `git -C lane status --porcelain` was empty. Scratch was removed before handoff.

## Source locator receipts

Access date for all sources below: 2026-10-27.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — quote (C2 ordering): “No probe of the C2 package runs before the stage-2 commit.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — quote (C3 finding): “V7 lacks violating cases for `both-print` and `toolchain`.”
- `file:///home/vgpnk/.omp/agent/RULES.md` — quote: “Never run a partial upgrade (`pacman -Sy <pkg>`).”
- `skill://godspeed` — quote: “Name the axes.”
