ATTACKS: C2 `state-check-before-6180e4f.txt` reproducibility.

- Archived baseline `6180e4f` to `/tmp/k25w2-ReRunStateBefore/fleet/kengaku-shokunin` (`git tree 0bfdadeb918242d54b6cd4a8e3df71b1b26ebadf`) and checker from `8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b`.
- Checker identity: `git rev-parse 8ea41f9ed:plans/state_check.py` and `git hash-object` of the archived script both returned `55a95f3fcf3aec9cbf848c19fd05b2ff8468d971`.
- `plans/state_check.py:601-615` resolves `root.parent/PROTOCOL.md` first; copied fleet `PROTOCOL.md` into that scratch parent so lookup is isolated and deterministic.
- Ran the requested `python3 <archived-tip>/plans/state_check.py --root <archived-6180e4f> --summary` from both `/` and `/tmp`. Both runs were byte-identical to each other and the recorded receipt: SHA-256 `916766c30287f5c9ca3820af699326abe0fd61e089431652a279365d74890174`; receipt and rerun `diff` exit 0; reruns `diff` exit 0.
- Reproduced output: `assertions=242 match=228 mismatch=11 superseded=0 offline_unverifiable=3`; `VERDICT: FAIL — at least one frozen assertion mismatches`; `exit=1`. The 11 mismatch records, including `P2a.capability.sources-registry` (observed `rows 26; malformed 0; A=24 C=2; mined=18 queued=5 rejected=3`) and the P2c/P2d/P2e records, match the receipt exactly.

Findings: no falsification; the before-receipt faithfully reproduces the checker's result on archived base `6180e4f`.

Residual risk: the live worktree `plans/state_check.py` is dirty relative to tip (working-copy SHA-256 `505e695e8b0ba333d418ec2795df6a19f8fbb88513fc05e380ffd56c6bd746ca`; `git diff` reports 39 insertions and 2 deletions). This run deliberately used the pristine archived-tip checker; claims here do not cover the dirty copy. The resolved `PROTOCOL.md` is external to the archived lane tree and its digest is not recorded in this receipt.

Verification gaps: this attack covers only the before receipt on `6180e4f`; it does not independently assess the after receipt or the broader C2 claims.

Installs: none.
VERDICT: SURVIVES — the pinned tip checker reproduces the before receipt byte-for-byte, including all 11 mismatches and exit 1.