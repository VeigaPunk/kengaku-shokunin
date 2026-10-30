source: S198 https://opentimestamps.org/ (How it Works); S199 https://raw.githubusercontent.com/opentimestamps/opentimestamps-client/master/README.md (Usage, upgrade); round-54 review receipts under .ufo/waves/round-54/w1/
verified-at: 2026-10-30
recheck: on-release

# Existence commitments are not a verified measurement freeze

OpenTimestamps defines a timestamp as evidence that data existed before a time (S198).
Its official client distinguishes submission, incomplete proofs, upgrade and verification (S199).
Neither the existence of a `.ots` file nor a calendar submission establishes Bitcoin confirmation.
A header's merkle-root match also does not, alone, establish canonical-chain membership.
These are interpretation limits, not a newly working capability.

## Round-54 observation

The claims file was committed at `17f90355c3ec17dcf15f7980d83f1943ae428fe5` before stamping.
Its digest is recorded in `corpus/evidence/round54/anchor/anchor.json`.
`w1/E10DigestChain/walker-output.txt` independently checks the digest chain and observes pending
attestations; it does not certify a confirmed anchor. Wave paths in this entry are beneath
`.ufo/waves/round-54/`.

The attempted counter `plans/round54_c1_anchor.py` is **not an admitted verification tool**.
Reviewer `w1/R1C1Counter.md` demonstrates incompatible deserialization APIs, an unusable
operation walker, and an incorrect equality between the original file digest and the aggregated
attested digest. Its selftest passing therefore does not demonstrate the canonical positive path.
The frozen counter was not changed after those observations. No capability row enters.

## Decision table

| Observed evidence | Permitted interpretation | Not established |
|---|---|---|
| Calendar accepted a digest | Submission occurred | Bitcoin confirmation or preregistration integrity |
| Pending attestation and calendar URI | Further remote evidence is needed | Independently verifiable completed proof |
| Attested merkle root matching one supplied header | A bounded inclusion check, if the full operation path validates | Canonical chain membership from the header alone |
| Counter selftest passes but ordinary proof parser fails | Selftest lacks a working positive control | A runnable integrity gate |

## Falsification and future admission

A future frozen counter must first execute a real confirmed proof through its canonical path,
then demonstrate changed-file, changed-header and pending-only controls failing for the named
reasons. Input binding, operation reachability, chain trust and ordering must be separate legs.
Prior-art pricing remains required: applying a published timestamping procedure is not, by
itself, phenomenon novelty. Round 54 does not claim that this implementation meets those conditions.
