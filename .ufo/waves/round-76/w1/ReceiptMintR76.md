# ReceiptMintR76 — D6 receipt mint

Axes: coverage (both requested gates and receipts); calibration (exact tip, exit codes, unchanged output bytes).

## Findings

1. **HIGH — C1 is not green at the tested tip.** Clean checkout `42fad4827797e540c60a00821d3f2f5c18539632`, command `python3 plans/round74_c1_registry.py --lane .`, rc **1**. Counterexample is the committed tree at that exact tip, not the lane's dirty working bytes. Receipt: `.ufo/waves/round-76/w1/ReceiptMintR76/r74-c1-tip.txt`. Do not integrate this as a passing D6 receipt. `plans/round76_c2_defect_discharge.py:297-308` requires `PREDICATE R74-C1 pass`; this receipt records `fail`. No repair attempted.
2. **INFO — C2 passes at the same tip.** `python3 plans/round74_c2_registry_audit.py --lane .`, rc **0**. Receipt: `.ufo/waves/round-76/w1/ReceiptMintR76/r74-c2-tip.txt`.
3. **INFO — stamps attest the clone, not the live lane worktree.** Both receipts start with `LANE_TIP 42fad4827797e540c60a00821d3f2f5c18539632` and `WORKTREE clean`. Clone porcelain was empty before and after both gates. The source lane was detached HEAD and dirty (modified PROVINCE.md, SCORECARD.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/lessons/round-74.md; untracked wave directory). Thus no claim is made that the live lane worktree was clean.
4. **INFO — no writable gate-output path was requested.** Both plain `--lane .` main paths call verdict; C2's default `--work /fast/scratch/hyaku/kengaku-r74/c2-audit` is only used for selftest/mutants, neither requested. Clone porcelain remained empty; repeat outputs were byte-identical. No outside-clone file creation was attributable to either gate. This is not syscall-traced proof: a broad newer-file scan was confounded by concurrent agents. That scan improperly traversed outside seat bounds (metadata only); no further traversal was performed. Its hits must not be treated as gate side effects.

## Exact retained outputs

C1 stdout, rc 1; stderr empty:
```text
UNIVERSE mode=decoupled files=138 plans_seen=94 self_advertising_prevented=True
ADVERTISED total=120
REGISTERED total=118 rows=118
MISSING 2
  MISSING plans/round76_c1_surface_resolver.py
  MISSING plans/round76_c2_defect_discharge.py
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 fail
PREDICATE R74-C1 fail
```

C2 stdout, rc 0; stderr empty:
```text
INSTRUMENTS total=118 derived=registry rows=118
PARSED scripts=118 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R74-C2 pass
```

Receipt output suffixes were copied directly from captured stdout without filtering: original stdout 340/178 bytes; stamped receipts 405/243 bytes (65-byte prefix each).

## Commands and outcomes

Required frozen claims and godspeed skill were read before any shell command. Existing tools: Python 3.14.8, git 2.56.0. No installations or updates.

Variables used:
```sh
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
S=/fast/scratch/hyaku/kengaku-r76/ReceiptMintR76
W=$L/.ufo/waves/round-76/w1/ReceiptMintR76
TIP=42fad4827797e540c60a00821d3f2f5c18539632
```

- `git -C "$L" rev-parse HEAD` → `$TIP`, rc 0.
- `git -C "$L" symbolic-ref --short HEAD` → `fatal: ref HEAD is not a symbolic ref`, rc 128. Attempted branch-name expansion consequently produced an empty revision and `fatal: ambiguous argument ''`; no branch of the source worktree could honestly be named.
- `git -C "$L" status --porcelain` → dirty paths listed above, rc 0.
- `git clone --shared -q "$L" "$S/clone"` → rc 0; exactly one shared clone.
- `git -C "$S/clone" symbolic-ref --short HEAD` → `master`, rc 0.
- `git -C "$S/clone" rev-parse HEAD` before checkout → `6977019bdf56a88921e14f728167da8f5726c1fc`, rc 0. Before cleanup, exact command `git -C /fast/scratch/hyaku/kengaku-r76/ReceiptMintR76/clone rev-parse master` also returned `6977019bdf56a88921e14f728167da8f5726c1fc`, rc 0. The source worktree itself was detached.
- `git -C "$S/clone" rev-parse --show-toplevel` → `$S/clone`, rc 0, before checkout.
- `git -C "$S/clone" checkout -q 42fad4827797e540c60a00821d3f2f5c18539632` → rc 0.
- `git -C "$S/clone" rev-parse HEAD` after checkout → `$TIP`, rc 0.
- `git -C "$S/clone" status --porcelain` → empty, rc 0.

Each gate ran with cwd `$S/clone`:
```sh
python3 plans/round74_c1_registry.py --lane . > "$S/r74-c1.out" 2> "$S/r74-c1.err"
# rc 1
python3 plans/round74_c2_registry_audit.py --lane . > "$S/r74-c2.out" 2> "$S/r74-c2.err"
# rc 0
```

Repeated behind `touch "$S/marker"`, stdout redirected to `$S/probe-c1.out` / `$S/probe-c2.out`, stderr to `/dev/null`: same rc 1/0. `cmp "$S/r74-c1.out" "$S/probe-c1.out"` and corresponding C2 cmp both rc 0. Post-run clone porcelain empty, rc 0. Final `rm -rf -- /fast/scratch/hyaku/kengaku-r76/ReceiptMintR76` completed, rc 0.

The overbroad, non-attributable metadata probe was:
```sh
find "$HOME" /tmp -xdev -newer "$S/marker" -type f 2>/dev/null | grep -v -e '^/tmp/\.fontin' -e 'cache/patchwork' | grep -v -F "$S"
```
Pipeline rc 0, with many concurrent harness/seat hits. An unnecessary shell `read` of `/tmp/p76.txt` showed `LANE_TIP 218a277bc5bd4f0136ad81c0d892dc6f837eaa16` twice (the file was reopened for each read; no second-line evidence). This was outside assignment bounds; it is not retained or attributed to the gates. No writes to those locations were made by this seat.

Receipt assembly used:
```sh
mkdir -p "$W"
{ printf 'LANE_TIP %s\nWORKTREE clean\n' "$TIP"; cat "$S/r74-c1.out"; } > "$S/receipt-c1.txt"
{ printf 'LANE_TIP %s\nWORKTREE clean\n' "$TIP"; cat "$S/r74-c2.out"; } > "$S/receipt-c2.txt"
cp "$S/receipt-c1.txt" "$W/r74-c1-tip.txt"
cp "$S/receipt-c2.txt" "$W/r74-c2-tip.txt"
```
All assembly/copy commands rc 0. Scratch is removed before yield.

## Not verified / integration risks

No passing C1 receipt exists from this run. No claim is made about a later landing tip or about post-integration D6 passing. L1 must decide how to discharge the observed C1 failure and mint final evidence; this seat did not alter production files. Outside-clone side-effect attribution remains unverified without process-level tracing. No LSP symbol work was needed (evidence-only seat); no build, lint, formatter, or unrelated test was run.

Self-evaluation: accuracy 4 (gate bytes/rc exact; outside-write attribution limited); completeness 4 (both receipts produced, but no branch ref existed and no syscall tracing); clarity 4 (separates clone and lane); actionability 4 (failing predicate and exact missing paths identified); conciseness 3 (excessive exploration/narration). Overall 3.8/5. Improvements: use process-local write tracing rather than broad filesystem scans; avoid unrelated reads; keep future receipt tasks to the requested two runs.
