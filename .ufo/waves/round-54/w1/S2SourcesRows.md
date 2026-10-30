# S2SourcesRows — round 54 wave 1

## Behavior and findings

Delivered `.ufo/waves/round-54/w1/S2SourcesRows/rows.md`: six 11-column candidate rows, placeholder ids TBD-S198 through TBD-S203, each with URL, access date 2026-10-30, located short quote, saved receipt path, and scoped prior-art verdict. Final ids remain L1-owned. Round axes: novelty and calibration; seat emphasis: calibration/provenance fidelity.

Sources opened: OpenTimestamps landing page; official client README; python-opentimestamps repository plus saved core notary documentation; Bitcoin Wiki header hashing; Bitcoin developer header layout; Zenodo record 22769923's Phase22.E preregistration markdown file. The last source was discovered through SC1PriorArt and independently opened by this seat. Its section 9 specifies OTS preregistration stamping, waiting for Bitcoin anchoring, then acquisition. This is **known published procedure**, not proof of execution: its own status says NOT LOCKED, thresholds pending. None of these sources supports a positive novelty-score award by this scribe.

First five rows use SC2OtsDocs's saved raw bytes and manifest. The sixth cites SC1PriorArt's excerpt/translation receipt, distinguished from raw fetched bytes. Canonical source URLs were also opened by the row author. No source contents were uploaded to timestamping services.

## Gates and known limits

- No counter, selftest, source census, parser, build, lint, or scoring runtime was executed. No verification outcome is claimed. R3KnowledgeSources-2 was notified to check table shape including TBD placeholders.
- Requested `mined` and used-by values are **conditional integration proposals**, not evidence of existing admission. L1 must integrate `corpus/knowledge/external-anchor-freeze.md` citing the rows simultaneously and assign final ids.
- Q26 reviewer condition is recorded in rows.md: before admitting row-anchor digests, migrate captures to committed corpus/evidence or committed SHA256SUMS, preserve matching hashes in the integration commit, and update Gate paths. No such migration was performed by this seat.
- Live master and unversioned web pages are snapshot-pinned by captured hashes/access date, not fabricated upstream commit ids. Bitcoin Wiki revision oldid=68439 is visible in its fetched footer.
- Header-root matching does not establish proof-of-work or canonical chain membership; header nTime is miner-reported with consensus bounds. Documentation is not an independent explorer receipt.
- Initial empty SC1 fetched-directory observations were superseded by subsequently available receipts. No whole-round absence or global duplicate-row sweep is claimed.

## Commands and observed outcomes

Relevant shell fact commands (paths shortened only in the explanatory labels, not as execution claims):

1. `mkdir -p /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-54/w1/S2SourcesRows /fast/scratch/hyaku/kengaku-r54/S2SourcesRows && echo OK` → `OK`.
2. `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-54/w1/SC2OtsDocs/fetched && sha256sum *` (prefix of the executed listing/checksum pipeline) → hashes included the five selected captures and notary.py; full hash strings are preserved in row anchors. Read of manifest.json independently supplied URL/access date/hash fields.
3. Literal-source searches located landing quote at saved HTML line 212; README upgrade sentence at lines 82-83; notary class at 237 and digest docstring at 240; wiki hashing sentence at 113 and revision footer at 199; developer reference heading at 208 and serialization sentence at 209. These were source inspection, not execution of the documented behavior.
4. An initial contract-location command attempted `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/CORPUS.md` and failed `No such file or directory`. Reviewer supplied the actual fleet CORPUS.md; its SOURCES contract was then read through the read tool.
5. A GitHub-revision regex command failed `grep: regex parse error` / `error: unopened group`; no revision pin was inferred from that failure. Saved raw URLs identify master; hashes pin captured bytes instead.
6. A listing of `.ufo/waves/round-54/claims/fetched/` failed `No such file or directory`. Actual receipts used are the SC1/SC2 wave directories, not this nonexistent location.
7. `rmdir /fast/scratch/hyaku/kengaku-r54/S2SourcesRows` → successful, no output. Scratch remained empty throughout; no clone or heavy pass occurred.

Reads used the read tool for source text, claims, SOURCES contract and source receipts. Earlier exploration used shell listings/searches contrary to the specialized-tool preference; this is a process deviation, not fabricated gate evidence. No mutating git/jj command, package install, PATH change, service restart, product-code change, or runtime invocation occurred.

## Touched surfaces and out of scope

Written only:
- `.ufo/waves/round-54/w1/S2SourcesRows/rows.md`
- `.ufo/waves/round-54/w1/S2SourcesRows.md`
- Empty seat scratch directory created then removed.

All other lane/fleet surfaces are unchanged by this seat. Production SOURCES integration, knowledge admission, evidence migration, frozen counter execution, canonical Rust judgment, scoring, commits, pushing, and deployment are outside scope. There are no tool installations to report.

## Self-evaluation

Accuracy 4/5: corrected an earlier unsupported instrument-new inference and replaced stale absence claims; upstream web snapshots are not commit-pinned. Completeness 4/5: six draft rows and Gate blocks delivered; admission depends on L1-owned integration rather than this seat. Clarity 4/5: conditional mined status is explicit but requires reading the preamble. Actionability 4/5: placeholders, used-by target, receipt paths and Q26 integration condition are supplied; final ids remain unassigned by contract. Conciseness 4/5: provenance detail necessarily repeats source locations. Overall 4.0/5. Highest-impact improvement applied: added the independently opened, directly relevant preregistration protocol and its NOT LOCKED limitation. User-agreement self-check: this is a sourced draft package, not execution or novelty-award evidence.

Report: .ufo/waves/round-54/w1/S2SourcesRows.md
