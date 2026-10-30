# CN2CrossSource — mid-wave cross-claim scan

Axes: **novelty, calibration**. Read the frozen claims file in full before inspecting artifacts. This is a bounded advisory proposal, not judgment, admission, or a counter change.

## One proposed move: join evidence by identity, never by a green summary

For the L1's landing narrative, maintain one compact evidence-identity table linking each assertion to its exact subject, source/revision, argv (where applicable), observed result, and witness owner. Reuse existing receipts; do not create a new predicate or amend frozen thresholds. The non-obvious common failure is **witness substitution**: internal agreement can be mistaken for external existence in C1, just as a declared/selftest result can be mistaken for actual entry execution in C2. A matching digest or matching reason alone is insufficient for the stronger assertion.

### Evidence and contradictions (pasted)

1. **E4MigrationAudit versus E6RowAudit25 — actual conflicting exit values.**
   - `E4MigrationAudit/migration.md:8`: `scratch-root-guard` entry `python3 plans/scratch_guard.py check .` → **2**, while its pasted reason says sentinel-missing exits **1**. `E4MigrationAudit.md:5` repeats that all four re-declared rows have exit 2.
   - `E6RowAudit25.md:6`: “`scratch-root-guard`: declared 2, observed 1, evidence fragment matches — **MISMATCH**.”
   - `E6RowAudit25.md:10`: “Exact mismatch output tail: `CHECK red reason=sentinel-missing`.”
   - Read: E4 compared declarations; E25 independently executed. These cannot jointly substantiate declared==observed. REDECLARED 4 remains a migration-category count, not proof of EXEC. Do not smooth this contradiction into an overall successful audit or silently alter the frozen builder's measured exit.

2. **E1AnchorConfirm and E10DigestChain agree; they do not contradict.**
   - `E1AnchorConfirm.md:5`: “Two upgrade attempts both returned exit 1”; no header/receipts produced.
   - `E10DigestChain/E10DigestChain.md:12`: four pending attestations and **no BitcoinBlockHeaderAttestation** after an independent 49-node walk.
   - Same report lines 4–9 finds the frozen, HEAD, working-file, and anchor metadata digests equal.
   - Read: byte binding is supported; external Bitcoin existence/pre-dating is not established by these receipts. Never turn the four equal digests into an external-anchor success.

3. **E6RowAudit11 exposes a separate evidence-identity failure, not an exit disagreement.**
   - `E6RowAudit11.md:10`: `round28-census | 1 | 1 | false | MISMATCH`.
   - Line 13: declared fragment `"c1": { "exit": 0, "findings": [], "metrics":` is absent verbatim because actual JSON is multiline.
   - Read: agreeing exit values do not establish `evidence_missing=0`. The frozen counter explicitly tests substring membership at `plans/round54_c2_entrytruth.py:338`.

## (a) Duplicated fetches → one owner per canonical URL

No completed cross-seat duplicate fetch was evidenced at this snapshot. The overlap below is in assigned scope, not a fabricated claim that both seats fetched. `SC2OtsDocs/fetched/` contains bytes; `SC1PriorArt/fetched/` and `S2SourcesRows/` were empty in the initial directory inventory.

| Canonical source | Observed receipt | Proposed fetch/quote owner | Sole SOURCES draft owner |
|---|---|---|---|
| https://opentimestamps.org/ | `SC2OtsDocs/fetched/opentimestamps.org.html` | SC2OtsDocs | S2SourcesRows |
| https://github.com/opentimestamps/opentimestamps-client | `SC2OtsDocs/fetched/github-opentimestamps-client.html`, `ots-client-README.md` | SC2OtsDocs | S2SourcesRows |
| https://github.com/opentimestamps/python-opentimestamps | `SC2OtsDocs/fetched/github-python-opentimestamps.html`, `pyots-README.md` | SC2OtsDocs | S2SourcesRows |
| Independent preregistration prior art | No completed receipt observed in SC1 at initial scan | SC1PriorArt | S2SourcesRows after receipt exists |
| Bitcoin header explanations | `SC2OtsDocs/fetched/bitcoinwiki-block-hashing-algorithm.html`, `developer-bitcoin-block_chain.html` | SC2OtsDocs | S2SourcesRows if selected |

GitHub HTML plus its README are two representations of a source, not automatically two independent sources. Shared OTS docs explain mechanism; they do not replace SC1's independent prior-art question. Ownership recommendation was sent to S2SourcesRows. L1 still assigns final IDs; no rows were appended here.

## Inherited-context audit

- Search executed with `grep` tool over current wave Markdown for `unforgeable|TB2|novel|MISMATCH|mismatch|https://opentimestamps.org`, and a broader recursive scan for `unforgeable|TB2|backdat|trust|forg|prior.art|https?://`. No TB2-as-novel assertion or wave-report use of “unforgeable” appeared in returned report matches. This is a mid-wave absence, not a certification of unwritten reports.
- The **frozen claim itself** already uses “unforgeable preregistration freeze” and “unforgeable freeze”; that is not new seat wording. Do not edit its anchored bytes. The counter's introductory claim that “No lane-writable input is trusted for existence or ordering” (`round54_c1_anchor.py:7`) is stronger than the observed evidence: verify reads local receipt fields and counts distinct source strings (`:412–429`). [INFERENCE] Local consistency alone does not authenticate that those receipts were fetched from independent public witnesses. Route this distinction to outside closure rather than promoting the prose.
- The claims-file rubric expressly permits prior art to force replication/instrument-new and hold novelty at 8. No completed SC1 verdict was available in this snapshot, so no novelty verdict is inferred.

## (b) Contradiction routing

E4MigrationAudit ↔ E6RowAudit25 is the named two-seat contradiction above. E1AnchorConfirm ↔ E10DigestChain is corroboration with different leg coverage, explicitly not a contradiction. E6RowAudit11 is an independent evidence-fragment defect; do not merge it into the scratch-root exit mismatch.

## (c) Routed-out items → owner lane + path

All routes stay in lane `kengaku`, L1 `KengakuR54`; no sibling repository action is proposed.

| Item | Existing owner / destination evidence |
|---|---|
| Scratch-root declared 2 vs observed 1 | E2LedgerRefine reason/evidence work + L1 disposition; `E6RowAudit25/audit.md`, `E4MigrationAudit/migration.md`. Exit changes are outside E2's brief; preserve finding. |
| Census non-verbatim fragment | E2LedgerRefine; `E6RowAudit11/audit.md`; proposed refined ledger only in `E2LedgerRefine/` |
| Pending Bitcoin confirmation | E1AnchorConfirm / L1; `E1AnchorConfirm.md`, `E10DigestChain/E10DigestChain.md`; eventual anchor artifacts at frozen `corpus/evidence/round54/anchor/` destinations |
| Source dedupe / prior-art verdict | S2SourcesRows / SC1PriorArt / SC2OtsDocs; their existing wave paths above |
| MASS-ID-DRIFT, 114 collisions | L1's L0-question route, not source adoption; `E5CensusGate.md:5–9`. Existing frozen frontier contract says adopt nothing. |
| R52 negation repair | E3R52RegistryFix / L1; `E3R52RegistryFix/delta.diff`. Logged repair, explicitly not a new scored claim. |

## Effects, risks, verification

- Runtime: reuse receipts; do not rerun expensive row suites or add another runtime. Substrate: exact revision/argv/source identity prevents stale observations from being silently pooled. Contract: leave claims, counters, ledger measured exits, and frozen prior artifacts untouched. Verification: L1 should retain the scratch-root mismatch and census fragment defect as separate obligations; a matching migration count cannot discharge either.
- Expected axis effect [INFERENCE]: improves calibration by preserving what each witness actually proves; protects novelty from accidental rebranding. No novelty increase is asserted. No effect on coverage is claimed.
- Risk: a landing narrative table can become a second truth source. Keep it an index into receipts, never a replacement for the frozen counters or outside judgment. Timestamped pending observations must not be mistaken for a final round state.
- No builds, tests, counter runs, external fetches, installations, git mutations, or production edits were performed by this seat. No scratch was created. This scan is intentionally mid-wave: many attack/source seats had not yet published reports.
