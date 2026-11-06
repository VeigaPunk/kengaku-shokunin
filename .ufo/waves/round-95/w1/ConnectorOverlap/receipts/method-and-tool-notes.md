# Receipt — method, pins, hygiene (ConnectorOverlap, kengaku round 95)

- Seat: ConnectorOverlap-39, leaf; no subagents; read-only against all lanes; scratch
  /fast/scratch/hyaku/kengaku-r95/ConnectorOverlap (removed before yield; no citable evidence
  lived there — all receipts below are reads of lane/sibling working trees and git objects).
- Claims doc `plans/round-95-claims.md` read in full first; r94 overlap report
  (`.ufo/waves/round-94/w1/ConnectorOverlap.md`) read in full as the baseline.
- Sibling trees read at the working-tree HEADs pinned in receipts/a-tb2-scan.md; kaidoku
  additionally read through `git show c19d57cd..b0a7bb8c` (read-only) to prove the freeze
  family's byte-stability. kengaku files cited at the lane working tree (tip ea19299d; the
  frozen instrument digests are the F-table's business, not re-verified here — no in-round
  repair route exists).
- Grep tool over explicit `;`-joined lane paths with gitignore=false; the glob-form path
  false-negative first documented in r94 (its F6) was re-applied, not re-filed.
- Tool installs/upgrades: none (stock git/python3 sufficient; pacman pause respected).
- Fleet-root stray `kumitate-shokinin/` (r94 F5) still present — carried, untouched.
- No lane index, jj state, sibling tree, or fleet-root tracked file was mutated.
