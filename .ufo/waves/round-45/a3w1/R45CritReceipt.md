# R45CritReceipt — round 45 / a3w1

**Scope:** re-derive the landed password-recovery probe receipt and independently grade three constructed end states. Lane tip measured: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C "$S/lane" rev-parse HEAD`). Fresh clone root verified as `/fast/scratch/hyaku/kengaku-r45/R45CritReceipt/lane`. No lane files modified.

## Receipt rerun

Command (from `$S=/fast/scratch/hyaku/kengaku-r45/R45CritReceipt`):

```sh
cd "$S" && /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" python3 "$S/lane/plans/password_recovery_probe.py" --lane "$S/lane" --work "$S/w"
```

Output: exit 0. Envelope reported `ENVELOPE start 00:27:10 cwd=/fast/scratch/hyaku/kengaku-r45/R45CritReceipt` and `ENVELOPE end 00:27:14 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. The resulting stdout has 16 `CASE` lines and these exact terminal lines:

```text
regrade cases=16 differ=0
cases=16 observed_pass=5 observed_fail=11 mismatches=0
```

I diffed the generated file against `corpus/evidence/round45/password-recovery-probe.txt`. The raw files differ only because the generated file also contains the two envelope wrapper lines. I then compared the receipt bodies with the wrapper lines removed; all 16 `CASE` lines and the two summary lines are byte-identical: `RERUN1==RERUN2 receipt body identical`. A second fresh probe run (same command and envelope) also had exit 0, unchanged digest, and byte-identical receipt body to the first. Therefore **receipt rerun mismatches = 0**.

Additional direct checks:

- `python3 "$S/lane/plans/password_recovery_probe.py" --lane "$S/lane" --dry` exited 0; `diff -u` against `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` printed no differences (`DRY: byte-identical to frozen freeze file`). Probe SHA-256 was `9363e03e4ae3ef12f5cdc901c707922bf472222a98eecb079fa8075ac1beb4ab`.
- `cd "$S/lane/corpus/evidence/round45/tb2-password-recovery" && sha256sum -c SHA256SUMS` output `OK` for all nine files.
- Fetched the eight URLs at the `2fd12b88aafdd04a52c298e3940bcb189f9766d6` commit from `raw.githubusercontent.com` and compared each with its capture using `cmp`: `test_outputs.py`, `instruction.md`, `setup.sh`, `Dockerfile`, `test.sh`, `README.md`, `solve.sh`, and `task.toml` each reported `http=200 IDENTICAL`. The root `.gitignore` fetched at the same commit also compared byte-identical to the capture named `gitignore`.
- The probe's `--stage-check` ran inside the envelope and reported `STAGECHECK ... rc=0 seed rc=0 recipe rc=0` for every case, ending `stagecheck cases=16 failed=0`; envelope digest unchanged.

## Independent handcheck

I rebuilt three end states in fresh scratch bwrap sandboxes by running the captured `setup.sh` and the exact recipe strings imported from the frozen probe module, then ran real `uvx -p 3.13 -w pytest==8.4.1 pytest /tests/test_outputs.py -rA` twice per case. This is independent of the probe's pytest-free harness and uses the command shape in captured `test.sh:18-22` (ctrf reporting omitted). The enclosing command was:

```sh
cd "$S" && /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" bash -c 'export XDG_CACHE_HOME="$S/hc-uvcache"; ...; HC_UVCACHE="$S/hc-uvcache" python3 .../a3w1/R45CritReceipt/handcheck.py "$S/lane" "$S/hc"'
```

Envelope: `ENVELOPE start 00:31:40 cwd=/fast/scratch/hyaku/kengaku-r45/R45CritReceipt`; `ENVELOPE end 00:31:43 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. The initial uv warm attempts printed a read-only temp-file warning under `~/.local/share/uv/tools`; the actual grading command nevertheless ran successfully using the already available managed Python/tool environment, and no writes to shared PATH occurred. Both pytest attempts succeeded as runs; their test outcomes were:

```text
under-varsea STAGE seed rc=0 ...
under-varsea STAGE recipe rc=0 ...
under-varsea ENDSTATE "stat: cannot statx '/app/recovered_passwords.txt': No such file or directory\nregular file 24 /app/varsea/recovered_passwords.txt..."
under-varsea GRADE[1] pytest-rc=1 verdict=fail
  under-varsea FAILED ../tests/test_outputs.py::test_recovery_file_exists - AssertionError: ...
  under-varsea FAILED ../tests/test_outputs.py::test_password_match - FileNotFoundError: ...
under-varsea GRADE[2] pytest-rc=1 verdict=fail
...
dir-state STAGE seed rc=0 ...
dir-state STAGE recipe rc=0 ...
dir-state ENDSTATE "directory 15 /app/recovered_passwords.txt..."
dir-state GRADE[1] pytest-rc=1 verdict=fail
  dir-state PASSED ../tests/test_outputs.py::test_recovery_file_exists
  dir-state FAILED ../tests/test_outputs.py::test_password_match - IsADirectoryError: ...
dir-state GRADE[2] pytest-rc=1 verdict=fail
...
crlf-line STAGE seed rc=0 ...
crlf-line STAGE recipe rc=0 ...
crlf-line ENDSTATE "regular file 37 /app/recovered_passwords.txt..."
crlf-line GRADE[1] pytest-rc=0 verdict=pass
  crlf-line PASSED ../tests/test_outputs.py::test_recovery_file_exists
  crlf-line PASSED ../tests/test_outputs.py::test_password_match
crlf-line GRADE[2] pytest-rc=0 verdict=pass
...
HANDCHECK under-varsea receipt_observed=fail my_pytest=fail MATCH
HANDCHECK dir-state receipt_observed=fail my_pytest=fail MATCH
HANDCHECK crlf-line receipt_observed=pass my_pytest=pass MATCH
handcheck matched=3/3
```

The detailed captured stdout is available in my scratch run log, not used as a receipt; the checked-out grader is `corpus/evidence/round45/tb2-password-recovery/test_outputs.py`. The first case's pytest runs both tests and reports two failures; the receipt's `F-` is specifically the probe harness's documented early-stop letter convention, while the scored pytest exit remains fail. All three overall verdicts match the receipt: **handcheck mismatches = 0; handchecks matched = 3/3**.

I also directly checked the grader expression `Path.read_text().strip().split("\n")`: `PW + CRLF` passes both with universal-newline conversion and without it, because `.strip()` removes the terminal `\r`; `PW + CRLF + decoy` passes with conversion and fails without it. Thus the receipt's outcome for `constant-crlf` is right, but its explanation that universal-newline handling is why that *single-line* case passes is non-load-bearing. Universal-newline handling is load-bearing for `crlf-line` (the selected handcheck), exactly as described there.

## Counterexample / correction

No counterexample found that changes the landed receipt's verdicts, pinned grader provenance, or the three independently checked verdicts. Two small prose inaccuracies in the case descriptions do not affect the grade: `decoys-1000` says “shuffled,” but its recipe is `seq 1 1000` and does not shuffle; `oracle-solve-sh` says “a handful of guesses,” while stage-check measured a 24-byte output file (one 23-character line plus newline). The smallest safe correction, if the L1 chooses to revise non-frozen explanatory prose, is to remove “shuffled” and say “one or more candidates” instead of asserting a handful; also phrase `constant-crlf`'s pass as terminal-CR stripping (or make the actual newline-conversion claim refer only to `crlf-line`). These are description-only, not verdict defects.

Axes affected: **receipt reproducibility / provenance** (rerun and upstream byte comparisons pass), **grader verdict fidelity** (3/3 independent real-pytest checks pass), and **description fidelity** (the three noted wording clarifications only).

VERDICT: receipt-rerun-mismatches-0-handcheck-3/3
