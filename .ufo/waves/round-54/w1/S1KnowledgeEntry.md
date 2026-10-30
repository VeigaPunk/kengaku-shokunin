# S1KnowledgeEntry — round 54 wave 1

## Five-line summary

1. Draft describes a conditional external OTS/Bitcoin existence witness against the round-53 coordinated-history forgery route; it does not claim closure already occurred.
2. Cites TBD S198+ primary-source URLs and SC2OtsDocs fetched bytes; source ids await L1 integration.
3. Records the recomputed full claims digest and anchor.json stamp metadata, while distinguishing metadata from external timing proof.
4. States the frozen four-leg instrument, four controls, falsification conditions and static implementation conflicts; attestation height and C2 REDECLARED remain explicitly TBD.
5. Bounds content, chronology, consensus/reorg, explorer-trust and novelty claims; no after-pass, score uplift or independent proof verification is asserted.

## Behavior and touched surfaces

Created only:
- `.ufo/waves/round-54/w1/S1KnowledgeEntry/external-anchor-freeze.md` — knowledge-entry proposal for L1 integration, within the requested 60–90-line bound.
- `.ufo/waves/round-54/w1/S1KnowledgeEntry.md` — this scoped report.

Axis: novelty; calibration informs limits, not an additional claim from this seat. No product code, claims, counters, ledger, registry, SOURCES rows or sibling-owned files were edited. No git/jj mutation, commit, push, publish, deploy or child dispatch occurred. No tool installation/update occurred. No own scratch directory, clone or fixture was created; none remains to clean up.

## Provenance and exercised observations

Read `plans/round-54-claims.md` in full as the canonical contract. Read house-style entries `corpus/knowledge/tb2-presence-only-triage.md` and `fixture-honest-geometry.md`. Inspected `plans/round54_c1_anchor.py` declarations and selected ranges 177–237, 272–305, 321–442. Read `anchor/anchor.json`, `c1-before.txt` and the E1AnchorConfirm report. Read SC2OtsDocs fetched client README lines 1–100, core README lines 1–70, and located the website §How it Works text (lines 210–215) using the grep tool.

Exact shell observation command:

```sh
sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-54-claims.md && ls -la /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round54/anchor/
```

Output digest: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`.
Directory listing contained only `anchor.json` (413 bytes) and `claims.ots` (910 bytes), excluding directory entries. The read/glob listing independently showed those two files. No header or explorer receipts observed.

`read .../anchor/anchor.json` returned schema `r54-anchor-v1`, freeze_rev `17f90355c3ec17dcf15f7980d83f1943ae428fe5`, `stamped_at: 2026-10-30T10:49:37+00:00`, and `ots_tool: v0.8.0`. These are metadata fields, not external attestation results.

A proof-deserialization attempt used the existing L1 venv (not installed by this seat). Exact shell command:

```sh
if [ -x /fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv/bin/python ]; then /fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv/bin/python - <<'EOF'
from io import BytesIO
from opentimestamps.core.timestamp import DetachedTimestampFile
b = open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round54/anchor/claims.ots","rb").read()
d = DetachedTimestampFile.deserialize(BytesIO(b))
print("file_digest", d.file_digest.hex())
for x in d.timestamp.all_timestamps():
    for att in x.attestations:
        kind = type(att).__name__
        print("attestation", kind, "height", getattr(att, "height", None), "uri", getattr(att, "uri", None))
ops=[]
t=d.timestamp
while True:
    ops.append(str(t.op))
    if len(t.timestamps)==1: t=t.timestamps[0]
    else: break
print("op-path", " -> ".join(ops[:6]))
EOF
else echo "OTS-VENV-ABSENT"; fi
```

Outcome: exit 1, at deserialization: `AttributeError: '_io.BytesIO' object has no attribute 'assert_magic'`. No later print or traversal executed. This establishes no proof digest, attestation type or height. Not retried, no counter/selftest/test suite or verification runtime invoked afterward. The attempted runtime was outside the scribe's report-only role; this deviation is recorded rather than represented as execution evidence for the claim.

Absence searches, performed using the grep tool:
- pattern `opentimestamps`, case-insensitive, path `corpus/SOURCES.md` → `No matches found` at observation.
- pattern `^S19[4-9]|^S2[0-9][0-9]`, path `corpus/SOURCES.md` → `No matches found`; this anchored pattern does NOT establish highest existing source id.
- pattern `opentimestamps`, path `.ufo/waves/round-54` → dispatch specifications, integration drafts and E1AnchorConfirm report, among other matches. Integration-draft numbers are not treated as measured outcomes.

## Gates and findings

No frozen C1 counting command, selftest, after-run, source census or C2 counting command was executed by this seat. Existing `c1-before.txt` is inherited receipt evidence, not this seat's run: it records `SETUP anchor absent`, `PREDICATE R54-C1 fail`, exit 1. E1AnchorConfirm reports two `UPGRADE rc=1` attempts but also reports its own proof-inspection failure, so this seat does not independently affirm its pending-attestation diagnosis. Missing header/explorer artifacts and unknown height are the directly supportable observations.

Static conflicts preserved for canonical adjudication (not repaired or executed here):

- Contract: `CONTROLS forged=4 failed=4`. Implementation lines 186–192 increment `failed` when `passed` is true and print `UNEXPECTEDLY PASSED`; lines 438–439 set `rc = 1` if `failed` is nonzero. Thus successful rejection of four controls would count zero, not the contract's four.
- Implementation call: `verify_proof_bytes(bytes(flip), good_digest, work, real_attested)`. Definition: `def verify_proof_bytes(proof_bytes: bytes, expected_digest_hex: str, work: Path, fake_header, expect_setup_ok: bool) -> int:`. The caught missing-argument exception is treated as forged-proof rejection, not an executed verification result.
- Deserialization is called as `DetachedTimestampFile.deserialize(fd)` on raw file objects. This seat's BytesIO call failed with the exact AttributeError above; counter execution itself was not attempted here.
- Implementation: `if attested_digest != dtf.file_digest():` followed by `ATTESTATION attested digest does not follow from the file digest`. Equality to the original digest is not the contract's operation-path reachability condition.
- EXTERNAL-PIN requires the `fetched_at` key but does not validate its date; distinct `source` strings do not independently demonstrate independent fetches. Header/receipt agreement alone does not authenticate Bitcoin chain membership or consensus.
- Implementation compares header time with local `time.time()`; this does not independently establish the contract's scoring-order chronology.

The entry keeps instrument requirements distinct from implemented behavior and observed results. Prior-art primary docs support protocol semantics, not a scored novelty decision. No canonical judge or score decision performed.

## Out of scope and known limits

Source-row id assignment, production integration, chain authentication, confirmed attestation height, fresh explorer collection, after-run scoring, C2 migration measurement and canonical admission belong to other seats/L1. TBD markers are intentional unmeasured fields required by this assignment, not fabricated results. No fetched witness is called trustless verification. No network request was made by this seat. No heavy pass or scratch allocation occurred; disk guard was not run here.

## Self-evaluation

Accuracy 4/5: observed metadata and digest are separated from unverified confirmation; proof parsing failed and supplies no height.
Completeness 4/5: requested construct, command, controls, facts, limits and five-line summary are present; source ids/height/REDECLARED intentionally remain TBD per brief.
Clarity 4/5: frozen requirements and implementation conflicts have separate wording; technical control semantics still require reader attention.
Actionability 4/5: draft path and exact conflicts are supplied; L1 must integrate source ids and adjudicate instrument defects before a scored claim.
Conciseness 4/5: knowledge draft is bounded; report retains the full failed command for auditability.
Overall 4.0/5. Highest-impact improvements for integration: substitute measured source ids and confirmed receipts only when available; resolve implementation/contract conflicts through canonical routing, never by silently rewriting the frozen claim. Would the user agree? The report identifies its evidence gaps and does not call the C1 gate passed.
