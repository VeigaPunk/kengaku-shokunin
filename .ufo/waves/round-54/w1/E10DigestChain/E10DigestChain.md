# E10DigestChain — R54-C1 BINDING leg

## Digest chain
All four values equal the frozen expected digest `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`:

- Freeze commit `17f90355c3ec17dcf15f7980d83f1943ae428fe5:plans/round-54-claims.md`: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`
- Shared clone HEAD (`62e9bba5e4a0bed376890299aa6a09039db7e68e`), same path: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`
- Live working file: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`
- `anchor/anchor.json` digest value: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`

## Independent proof parse
`walker.py` and exact output are saved alongside this report. The deserialized proof file digest matches the chain. Independent traversal visited 49 timestamp nodes. The proof contains four `PendingAttestation` values (calendar URLs shown in `walker-output.txt`) and **no BitcoinBlockHeaderAttestation**; thus there is no Bitcoin height or Bitcoin attested digest reachable from the file digest. Consequently this proof does **not** establish the requested Bitcoin attestation/reachability leg. This is a measured limitation, not a pass.

## Single-commit check
Executed `git -C <shared clone> log --oneline 6c919180260ea545589c2c0a007a06f554b529d3..HEAD -- plans/round-54-claims.md`. Exactly one result:
`17f90355 round-54: claims frozen (C1 externally-anchored freeze novelty 8->9; C2 entry-truth counter calibration 9->10), instruments + selftests + before receipts`

## Tooling and scope
Installed `opentimestamps-client==0.8.0` into the seat scratch venv using `uv pip` (uv-managed package channel), because the system Python lacked the parser. This brought in `opentimestamps==0.5.0`. No lane production files modified; only this report and walker evidence were written under the assigned wave directory. No tests/builds/linters run.

## Risk / blocker
The current `claims.ots` parses cleanly but carries pending calendar attestations only. No Bitcoin confirmation is available in this proof, so C1's Bitcoin-attestation requirement remains unproven by this independent check.
