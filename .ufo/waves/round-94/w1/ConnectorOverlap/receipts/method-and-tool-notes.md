# Method & tool notes — ConnectorOverlap, kengaku r94 w1, 2026-11-05

## Workspace
- Scratch: /fast/scratch/hyaku/kengaku-r94/ConnectorOverlap (created mkdir -p; removed before yield).
- One live clone: `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"` then
  `git -C "$S/lane" checkout -q --detach 90c7677f0ba95d0930d93bda6a14aa50605ebe2e` (clone HEAD verified = T).
- No `git worktree add`, no mutating git anywhere in the lane; sibling repos only read (rev-parse HEAD for citations).
- Wave-dir writes only: .ufo/waves/round-94/w1/ConnectorOverlap.md + .ufo/waves/round-94/w1/ConnectorOverlap/**.

## Tool behavior findings
- grep tool: glob-form path `/home/vgpnk/Projects/shokunin/*-shokunin` returned "No matches found" for patterns that
  demonstrably exist in those directories (control: `write-compressor` scoped to kengaku plans → hits; `terminal` over
  the glob form → 0 hits, over the explicit 22-path list → 30+ hits). All real queries used explicit `;`-joined paths;
  tracked-only sweeps appended `;!**/.ufo/**`. Reported to the harness issue channel (grep: false negative on glob path).
- Reads at T used the clone (lane master had already moved to d04e6664c4fc); grep line numbers for kengaku files
  (round94_c2_counter.py:58-70, round94_freeze_integrity.py:19-22,47-49,94-103,130-134, decomp-opt-divergence.txt:1-4)
  were re-pinned against the clone so report citations are T-stable.
- Sibling citations are line numbers of each sibling's working tree at its recorded HEAD (receipts/a-tb2-scan.md header).

## Installs
- None. Stock git + python sufficient. pacman pause respected (no pacman commands).

## Coverage statement
- 21 sibling lanes × 9 query families (explicit paths), fleet scripts/, bonus non-lane fleet dirs (counters, reports,
  research, st2, wt2, exp-full, history-recheck, tools, templates, kumitate-shokinin) — zero TB2/freeze-gate signals.
- Files actually opened for context (not just grep): kengaku plans/round-94-claims.md (full), round94_freeze_integrity.py
  :1-70, round94_c2_counter.py :1-80, decomp-opt-divergence.txt; mado quality/check-freeze-order.py :1-143;
  kumitate-shokinin stray K69ExecBaseCounter.md :1-15.
- Not swept (out of item scope, listed for honesty): sibling .git internals; fleet-root dirs other than those named
  above were included in the bonus sweep except `templates`-adjacent none; wave-history beyond what the full-tree
  greps surfaced was not chased (echo classification needs no deeper reading).
