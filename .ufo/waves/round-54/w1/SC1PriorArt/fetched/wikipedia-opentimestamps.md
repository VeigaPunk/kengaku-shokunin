# Fetch receipt — Wikipedia: OpenTimestamps

- URL: https://en.wikipedia.org/wiki/OpenTimestamps
- Access date: 2026-10-30 (UTC)
- Fetch method: read tool, Wikipedia API (markdown)

## Located quotes (verbatim)

§ "What is a timestamp":

> A timestamp is a proof that some data d existed prior to a certain point in time.[1]

Same section, verification semantics:

> To verify the commitment, the operations are applied in sequence to the data d, then the result, which should be the transaction merkle root, is checked to be equal to the one observed in the blockchain; if the check goes fine, then one can assert that d existed prior to the block.

§ "Timestamp creation", upgrade step:

> Once a reasonable time has elapsed, the user will run the upgrade operation on the same OTS file. This will communicate with the calendar servers and update the OTS file with the Bitcoin block header attestation.[1]

§ "Timestamp verification":

> The verification of the OTS proof requires both the OTS file and the original file. The user must also have an up-to-date Bitcoin node[f] on their own machine to perform the verification without relying on trusted third parties.[8]

§ "Use cases" (complete):

> Applications include defensive publications[10] and digital multimedia file integrity.[11]

## Note

Encyclopedic statement of the mechanism: digest commitment, Bitcoin block header attestation, merkle-root verification, pending→upgrade flow. Its stated use cases are defensive publication and media integrity — research-preregistration use is not listed. Verdict treatment in prior-art.md: known (mechanism), adjacent (research use).
