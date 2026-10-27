# R48C2MutReceipt — receipt-binding mutation probe

**Axes:** coverage (R48-C2). **Measured revision:** `REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze; verified ancestor of lane HEAD). **Freeze check:** `plans/round-48-claims.md` exists at that commit; `plans/round48_c2_verify.py` does not. The stage-2 frozen counter is therefore unavailable. No scored R48 counter or probe execution was run. The only executions were scratch mutation probes of inherited round-46 pure parse legs and `pkg_gate.py` without `--rerun`/`--require-clean-tree`.

## Commands and observed outputs

Setup/verification commands:

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2MutReceipt
export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2MutReceipt
git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
git merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r48/R48C2MutReceipt/lane
git -C /fast/scratch/hyaku/kengaku-r48/R48C2MutReceipt/lane checkout -q a543d92083557dd9b33ee674e9b99b03411f80af
sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt plans/pkg-spec-r46.json
python3 /fast/scratch/hyaku/kengaku-r48/R48C2MutReceipt/probe_binding.py
```

Observed freeze checks: commit type `commit`; ancestry `YES`; the r48 C2 counter tree entry was absent. Frozen receipt SHA-256 was `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`. Its spec's masked digest matched round-46 pin `560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e`.

The harness ran V4/V7/V9/V10 on pristine bytes and each mutant, preserving the multiset of `CASE` labels. It also ran package checks without P10; the reported P2 line is the receipt digest check. The effective-spec run reproduces round-46 V2's substitution of the actual receipt digest before gate invocation.

Pristine output (verbatim):

```text
BASE_SHA256 dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277
BASE_LEGS {"V10": [true, "mechanism_rows=18/18 bad=0"], "V4": [true, "cases=18 mismatches_named=0/0 bad=0"], "V7": [false, "rows=5 tags=7 bad=[\"unparsed row '| instruction.md:7 | both-print | not exercised | '\", \"unparsed row '| instruction.md:9 | toolchain | not exercised | n'\", \"tags missing=['both-print', 'toolchain'] duplicated=0\"]"], "V9": [true, "case_rows=18/18 bad=0"]}
BASE_GATE_SPEC_P2 P2 ok receipt_sha256=pinned
```

| Mutant (case labels preserved) | Receipt SHA-256 | Detector output | Verdict vs inherited detector |
|---|---|---|---|
| M1 `nop` predicted/observed/tests flip + consistent summary | `9220b3f0b83ea382eff999d22579aeea4cc6d5fb671747205d8f44d08031457c` | V9: `case table rows=18 receipt cases=18 equal=False`; V4 ok | KILLED by V9 |
| M2 summary count only | `2e704869134ad2b3b6f52808040b02cfc439ed85d28f513f3a62cb08ccbf75f9` | V4: `summary disagrees with the CASE lines` | KILLED by V4 |
| M3 add `both-print` violation to `nonzero-exit` | `67d812baac2b42acf5b1ee9034e8ea856cfe63f9a26d3cdadc434bd99673a458` | V4/V9/V10 same as baseline; V7 retains same baseline defects | SURVIVED (no incremental detection) |
| M4 swap `crlf-source` and `value-plus-line` rows | `e4c11968ac85aac9e65e1768874ba568686e553d45864f4e01410280ec5a2860` | V4 frozen-id order defect; V9 row inequality; V10 mechanism-id order defect | KILLED by V4/V9/V10 |
| M5 alter receipt header digest byte | `b49ad54eff0212c2371ec339927127c69d3b63cdf8cc07bd2d33c78fe09cc14a` | V4/V9/V10 same as baseline; V7 same baseline defects | SURVIVED pure parse legs |
| M6 alter case description text | `887856a908726cb15fab7b3bd886f0bdec23e3ad2427b1986b6a62c5c200f355` | V4/V9/V10 same as baseline; V7 same baseline defects | SURVIVED pure parse legs |
| M7 flip `wrong-value tests=F` to `tests=P` | `7143c422d5440077e9662d1b557c0c36a8b5066e774946dac758c02ed9af5e11` | V9: `case table rows=18 receipt cases=18 equal=False` | KILLED by V9 |
| M8 alter `oracle-solve-sh regrade` and regrade count | `2f23f4840af06dd476ae013793d0dfc03f0e6ce7ce53a9bc3be1c91159b5692c` | V4/V9/V10 same as baseline; V7 same baseline defects | SURVIVED pure parse legs |

For every mutant, direct P2 with the frozen spec reported `P2 DEFECT receipt_sha256=<mutant digest>`. Under simulated V2 effective-spec substitution, P2 reported `P2 ok receipt_sha256=pinned` for every mutant. Thus the inherited counter's digest check is bypassed by V2's substitution; pure output legs kill semantic/order mutations listed above but do not bind header, description, or regrade bytes. The r48 V15 receipt-digest behavior cannot be tested without the stage-2 counter.

Restoration evidence (verbatim):

```text
RESTORE_HASH_EXPECTED dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277
RESTORED_SHA256 dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277
```

## Sources, limits, verdict

Local sources opened: `plans/round-48-claims.md`, `corpus/lessons/round-46-verifier-spotcheck.md`, and the frozen round-46 counter, gate, receipt, spec, dry table, and entry in the scratch clone at the measured revision. No external URL was opened; no external-source quote is claimed. The claim file was read before measurements. Limits: no stage-2 counter/pins, no full probe, no full counter, no admission judgment; V7 pristine baseline already fails on the two known unexercised rows, so mutants with unchanged V7 output are not credited as killed. Scratch harness and clone were disposable and removed after this report was written.

**VERDICT: R48-C2 MUTATION PROBE INCONCLUSIVE** — inherited detector killed M1/M2/M4/M7 and left M3/M5/M6/M8 undetected by pure output legs; cannot determine the frozen stage-2 counter's digest/output binding until it exists. No R48 claim is admitted or rejected here.
