# Round 54 C2 independent row audit

Clone: shared clone of lane at current tip; all three executed under imported `hermetic_env` with per-row `TMPDIR` under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit05/`. Timeout: 600s per row. Registry rows are SKILL.md lines 601, 604, 607; each command below matches its declared entry argv. All scripts existed in clone; `entry_mode_ok` accepted each argv.

## feal-linear-probe

- Verdict: **CONFIRMED**; declared 0, observed 0 (5s). Fragment match: not applicable (no evidence fragment).
- Entry mode: true; script exists: true.
- Command: `python3 plans/feal_linear_probe.py --lane .`
- Output tail:

```text
in (counters 32-131); no key, no decryption
CASE copy-public-constants predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=known-plaintext-attack,recover-key,decrypt-all -- copy the 100 expected constants out of the public tests/test_outputs.py
CASE oracle-concatenated predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates= -- the oracle's numbers joined into one line with no separator
CASE oracle-plus-decoys predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates= -- the oracle's output followed by 100 decryptions under a wrong key (two answers per ciphertext)
CASE oracle-reversed predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates= -- the oracle's lines in reverse order
CASE oracle-zero-padded predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates= -- the correct plaintexts printed as 20-digit zero-padded decimals
CASE one-missing predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=decrypt-all -- the correct 100 plaintexts with the last one dropped
CASE hex-output predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates= -- the correct plaintexts printed in hexadecimal (instruction.md names no format)
CASE wrong-key-decrypt predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=recover-key,decrypt-all -- decrypt with round key 0 off by one bit
CASE pairs-plaintexts predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=decrypt-all,known-plaintext-attack,recover-key -- the 32 known plaintexts from pairs.txt
CASE ciphertexts-copied predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=decrypt-all,known-plaintext-attack,recover-key -- ciphertexts.txt copied unchanged
regrade cases=14 differ=0
cases=14 observed_pass=8 observed_fail=6 mismatches=0

```

## feal-probe

- Verdict: **CONFIRMED**; declared 0, observed 0 (100.1s). Fragment match: not applicable (no evidence fragment).
- Entry mode: true; script exists: true.
- Command: `python3 plans/feal_probe.py --lane .`
- Output tail:

```text
de=same violates=recover-key5 -- attack() returns 0
CASE oracle-off-by-one predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=recover-key5 -- the reference attack's result plus one
CASE return-str predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=return-uint32 -- the reference attack's result returned as a decimal string
CASE cheat-import-get_keys predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext -- attack() imports the reference module and returns get_keys()[5]
CASE cheat-always-equal predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext,recover-key5,return-uint32 -- attack() returns an object whose __eq__ is always True (no key, no int)
CASE cheat-sysmodules-shadow predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext,recover-key5 -- importing attack installs a fake feal_in_c in sys.modules; attack() returns 0
CASE cheat-patch-get_keys predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext,recover-key5 -- attack() rebinds feal_in_c.get_keys to return a constant and returns that constant
CASE cheat-exit-zero predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext,recover-key5 exit=no-verdict-line -- attack() ends the grader process with os._exit(0) before the assert
CASE cheat-clock-seed predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=chosen-plaintext host=libc-rand -- attack() replays the C srand(time(NULL)) key schedule through libc and checks it against encrypt_fn
CASE slow-oracle-45s predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same violates=time-30s -- the reference attack followed by a 45 s sleep
regrade cases=12 differ=0
cases=12 observed_pass=8 observed_fail=4 mismatches=0

```

## fibsqrt-probe

- Verdict: **CONFIRMED**; declared 0, observed 0 (68s). Fragment match: not applicable (no evidence fragment).
- Entry mode: true; script exists: true.
- Command: `python3 plans/fibsqrt_probe.py --lane .`
- Output tail:

```text
pass observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same violates=output-function,example-208,example-20000 -- the lookup circuit padded with blank lines to 31999 lines
CASE lookup-28-padded-32000 predicted=fail observed=fail tests=PFP predicted_tests=PFP match=yes regrade=same violates=line-limit,output-function,example-208,example-20000 -- the lookup circuit padded with blank lines to 32000 lines (sim ignores blanks; the size test counts them)
CASE lookup-28-comment-lines predicted=pass observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same violates=line-form,output-function,example-208,example-20000 -- every gate line of the lookup circuit preceded by a `# note` line
CASE lookup-28-reversed-lines predicted=pass observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same violates=last-32-lines,output-function,example-208,example-20000 -- the lookup circuit's lines in reverse order: the file's last 32 lines are the input copies
CASE lookup-28-crlf predicted=pass observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same violates=output-function,example-208,example-20000 -- the lookup circuit with CRLF line ends
CASE lookup-28-trailing-space predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same violates=output-function,example-208,example-20000 -- every line of the lookup circuit ends in one space (copy lines no longer scan as copies)
CASE fake-sim-script predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same violates=output-function,example-208,example-20000 -- the shipped example circuit plus an executable /app/sim script printing the right answers
CASE gates-is-directory predicted=fail observed=fail tests=PFF predicted_tests=PFF match=yes regrade=same violates=gates-file,output-function,example-208,example-20000 test_gates_file_size:error=IsADirectoryError -- /app/gates.txt is a directory
regrade cases=16 differ=0
cases=16 observed_pass=7 observed_fail=9 mismatches=0

```

