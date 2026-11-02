# Independent C2 source and commit inspection
2026-11-02; reviewer /root/judge_kengaku_round62. Read-only standard git/sed/wc/tr inspections, no authored gate/counter or benchmark execution.

D1: .ufo/waves/round-61/recon/table-identity.txt explicitly has three diff locations: separator at2, sequential-sync at6, no-max-enforcement at13. render-table-base.txt shows sequential-sync P/F/P/F/F/F, no-max P/P/F/P/P/F. Thus two semantic table rows plus separator, not one. This supports correction without re-running the historical scoring or claiming scoring revalidated.

D2: opened corpus/evidence/round62/sources/index-windows-1252.txt lines102–107; line105 is pointer98 U+00E2. Decimal byte226=0xE2 is128+98. Immutable S225 currently says pointer226 byte0xE2; correction belongs new source row superseding S225, not editing original cell.

D3: independently ran:
`git diff --numstat f97e5b7b 215a7029 -- corpus/SOURCES.md` →274 additions,272 deletions.
`git diff --numstat f97e5b7b b9920576 -- corpus/SOURCES.md` →2 additions,0 deletions.
For each revision, `git show REV:corpus/SOURCES.md | wc -l` and `git show REV:corpus/SOURCES.md | tr -cd '\r' | wc -c` gave base272 lines/0CR,freeze274 lines/274CR,repair274 lines/0CR.
Therefore historical lesson's273 wrong; its546 changed-lines total correct. Prior reviewer R61-D3 itself wrong about237 deletions and511 total. An honest correction must reject that part of review, not conform facts to authority. Preserve both original records and append named corrections. This is useful calibration evidence, causally separate from C1.

Acceptance pending actual landed append-only errata, source-row correction, current claim references and frozen revision. No closure or scalar uplift inferred.
