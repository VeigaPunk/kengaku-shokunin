source: TBD S198+ — https://opentimestamps.org/ (§How it Works); TBD S198+ — https://github.com/opentimestamps/opentimestamps-client (§Usage); TBD S198+ — https://github.com/opentimestamps/python-opentimestamps (§Structure); source ids await integration, not assigned here
verified-at: 2026-10-30
recheck: 180d — rerun the frozen command below on a clean landing-tip clone; inspect source receipts and chain assumptions separately.

# External-anchor freeze: existence evidence outside writable lane history

## Construct, conditional on confirmation

Round 53's `.ufo/waves/round-53/w3/C1CritOracle2.md` records the motivating
coordinated-history forgery: internally re-pinnable inputs can preserve FREEZE/ORACLE
agreement while changing the apparent freeze. R54-C1 proposes an additional witness:
OpenTimestamps operations connect the claims-file digest to a Bitcoin block header.
If authenticated to Bitcoin consensus and established before scoring, this witness
constrains that forgery route beyond the lane's writable git history. Confirmation
and those ordering conditions are not established by this draft's observations.

The website's §How it Works describes existence-before evidence, not a content audit
or proof that measurements followed preregistration. The client README §Usage
separates pending calendar attestations from complete Bitcoin proofs. A local
`stamped_at` string is metadata, not an externally attested submission time.
Fetched copies: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/`, especially
`opentimestamps.org.html`, `ots-client-README.md` and `pyots-README.md`.

## Frozen instrument and admission target

`plans/round-54-claims.md` fixes this counting command (placeholders are paths):

```sh
python3 plans/round54_c1_anchor.py verify \
  --anchor corpus/evidence/round54/anchor \
  --claims plans/round-54-claims.md \
  --source CLEAN_CLONE --work SCRATCH --controls
```

- **BINDING:** claims bytes at the recorded freeze revision, source HEAD and disk
  must hash to the declared digest; source is clean and freeze is an ancestor.
- **ATTESTATION:** contract requires a recomputed OTS operation path, a Bitcoin
  attestation at height >=800000, and agreement with the header's merkle root.
- **EXTERNAL-PIN:** contract requires >=2 independent, fresh round fetches agreeing
  on height/hash/time with the 80-byte header; block time precedes scoring.
- **CONTROLS:** forged-proof (flipped byte), wrong-bundle digest, pending-only proof
  and absent proof must each be rejected. The contract target is
  `CONTROLS forged=4 failed=4` followed by `PREDICATE R54-C1 pass`, exit 0.

These are frozen requirements, not a report of successful execution. Static reading
finds implementation conflicts: proof deserialization receives a raw file object;
`verify_proof_bytes` is called without its required `expect_setup_ok` argument;
`failed` counts controls that unexpectedly pass, and any nonzero count fails the run.
Thus its printed `failed` counter is not the contract's rejected-controls count.
The attestation check additionally requires attested digest == original file digest,
not merely reachability through operations. Receipt freshness is not date-validated:
`fetched_at` is required, while source distinctness is string-based, not independence.
These findings prevent treating the leg names as evidence that the contract holds.

## Observed facts and unmeasured fields

- `sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-54-claims.md`
  returned `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`.
- Reading `corpus/evidence/round54/anchor/anchor.json` gives freeze revision
  `17f90355c3ec17dcf15f7980d83f1943ae428fe5` and local `stamped_at`
  `2026-10-30T10:49:37+00:00`; this is a metadata observation, not external timing proof.
- Directory enumeration found only `anchor.json` and `claims.ots`: no header or
  explorer receipts at observation. Attestation height: **TBD, not established**.
- This seat's deserialization attempt failed with `AttributeError: '_io.BytesIO'
  object has no attribute 'assert_magic'`; it establishes no proof digest or height.
- `corpus/evidence/round54/c1-before.txt` records the frozen verify command against
  the base clone: `SETUP anchor absent`, `PREDICATE R54-C1 fail`, exit 1.
  No C1 after-pass is claimed here; landing receipt and attestation remain unmeasured.
- Companion C2 ledger migration: `REDECLARED` count **TBD (not measured here)**;
  command: `python3 plans/round54_c2_entrytruth.py --lane . --source CLEAN_CLONE
  --work SCRATCH --jobs 3 --timeout 900`. This is separate from C1 admission.

## Limits, falsification and prior-art pricing

Explorer receipts are fetched witnesses, not trustless chain verification. Header
consistency alone does not establish mainnet inclusion, proof of work or chain choice;
no anti-reorg guarantee beyond Bitcoin consensus is claimed. No content correctness,
authorship or complete preregistration chronology follows from timestamping alone.
A forged/pending proof accepted by a leg, header/receipt disagreement, failure to
confirm during the round, or unavailable required verification kills the frozen claim.
Published timestamping practice must be priced as replication/instrument-new where
applicable; primary protocol documentation alone does not establish novelty 9.
Falsifiable claim: for the recorded claims digest and an authenticated confirmed
Bitcoin witness preceding scoring, changing those claims bytes breaks digest binding;
this round's pending artifacts and unexecuted after-run do not yet demonstrate it.
