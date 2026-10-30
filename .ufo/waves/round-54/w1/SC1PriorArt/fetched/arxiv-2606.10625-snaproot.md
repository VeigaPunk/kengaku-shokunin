# Fetch receipt — arXiv 2606.10625 (snaproot)

- URL: https://arxiv.org/html/2606.10625v1
- Access date: 2026-10-30 (UTC)
- Fetch method: read tool, native HTML (HTTP success)
- Document: "snaproot: Decentralized File Integrity Verification Using Blockchain-Anchored Cryptographic Hashing", arXiv:2606.10625v1 [cs.CR] 09 Jun 2026, Arslan Brömme and Tarkan Yavas (Chain Horizon GmbH), "Preprint / working paper"

## Located quotes (verbatim)

Abstract (positions against OTS and names pre-registration manipulation):

> We position snaproot against established hash-anchoring systems (OpenTimestamps,
> OriginStamp, Chainpoint) and discuss limitations with respect to
> pre-registration manipulation and AI-generated content.

Threat-model limitation (line ~599 of the HTML):

> Pre-registration integrity. The registrant performs
> registration before any adversarial modification of the file. snaproot
> provides no guarantee if an already-modified file is registered.
> Combining snaproot with capture-time anchoring

Conclusion (line ~2562):

> We have also been explicit about what snaproot does *not* provide: it does not certify the authenticity of pre-registration
> content, it does not currently defend against frontrunning of
> unconfirmed registrations, and it does not eliminate the long-term
> reliance on blockchain archive availability.

Related work §2.1 (on OTS/Bitcoin):

> OpenTimestamps [[6](#bib.bib6)] anchors hash values on
> the Bitcoin blockchain using Merkle aggregation, allowing a single
> Bitcoin transaction to attest to arbitrarily many documents.

## Note

General-purpose hash anchoring on Solana (not Bitcoin headers), with an explicit threat model and a "pre-registration integrity" assumption (registration before adversarial modification) — but no measurement-freeze ordering, no block-header/explorer verification procedure, and pre-registration only as a limitation discussion. Verdict treatment in prior-art.md: adjacent.
