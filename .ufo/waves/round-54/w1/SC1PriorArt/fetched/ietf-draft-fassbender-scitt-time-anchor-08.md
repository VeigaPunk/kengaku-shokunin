# Fetch receipt — IETF Internet-Draft draft-fassbender-scitt-time-anchor-08

- URL: https://datatracker.ietf.org/doc/draft-fassbender-scitt-time-anchor/
- Access date: 2026-10-30 (UTC)
- Fetch method: read tool, native HTML (HTTP success)
- Document: "Umarise's Bitcoin-Anchored Temporal Proofs", draft-fassbender-scitt-time-anchor-08, J. Fassbender (Umarise), 23 October 2026, Intended status: Informational, Independent Submission stream, state "In ISE Review"; txt/html/xml at ietf.org archive links on the page

## Located quotes (verbatim)

Abstract:

> This document describes the mechanism Umarise uses for temporal anchoring of digital artifacts: cryptographic hashes are committed to the Bitcoin blockchain via the OpenTimestamps protocol. The resulting proof is independently verifiable by any party with access to independently validated Bitcoin chain data, without contacting Umarise or any other anchoring service.

§1.1 Motivating Example (an AI-research-lab measurement-freeze scenario):

> However, regulators ask: "How do we know the lab did not register these weights after the safety evaluation was already public -- backdating the claim?"

> Once the commitment has been included in a Bitcoin block and that block has reached the confirmation depth this profile requires, the regulator obtains a temporal guarantee: these model weights existed no later than block height H.

"Implementation status at the time of writing" (§1, on verifier independence / explorer sourcing):

> Of the two deployments Umarise operates, the second evaluates that gate and the first does not, and the reference verifier Umarise publishes obtains block headers from a single block explorer, which under Section 4.1 yields unverifiable rather than valid.

Table of contents §8 threat headings (names as printed):

> 8.5.  Threat: Temporal Claim Inflation
> 8.11.  Threat: Premature Anchored Status (False Finality)
> 8.1.  Threat: Second-Preimage Substitution (Forged Commitment)

Structure evidence from the ToC: §4 "Verification Procedure" with §4.1 "Verification Algorithm (VERIFY-ANCHOR)", §4.2 "Verification Independence"; §5 "OTS Anchoring Protocol -- Construction and Verification" incl. §5.2 "Upgrade Algorithm (Bitcoin Confirmation)"; Appendix D "Test Vectors" incl. "D.6. Negative Test Vector", "D.7. Independent Verification".

## Note

Primary standards-track-style text covering: digest commitment via OTS to Bitcoin (a), a full verification procedure against independently validated Bitcoin chain data with an explicit independence requirement that a single-explorer verifier is insufficient (b), and an adversarial threat model with backdating/false-finality/forged-commitment threats over AI-safety-evaluation artifacts (c, adjacent: SCITT receipts, not an eval-lane freeze). Verdict treatment in prior-art.md: known.
