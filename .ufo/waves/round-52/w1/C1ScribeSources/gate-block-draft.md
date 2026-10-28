## Gate

Skeleton for `kengaku-shokunin/corpus/lessons/round-52.md`. Contract v1 rule 1: every new row
carries URL, access date, and a ≤25-word quote with its location grounding `teaches`. Fill the
PENDING row from the scout seat's fetch; do not paste a URL that was not opened.

Candidates opened this round:

| candidate | verdict | reason / flip |
|---|---|---|
| Terminal-Bench 2.0 grader-file population, one recursive tree API call at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — `https://github.com/harbor-framework/terminal-bench-2` (`https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1`), opened 2026-10-28 | **ADMIT → S179** (tier A, kind `code`, status `mined`) | document root field `"truncated": false`, 1446 entries, document sha256 `b5d86dfe49ca75383d6e87d36e7fadcfd60d99bc5ae18c79fbc14d272278f362`; 92 top-level entries = 89 task dirs + `.gitignore`/`LICENSE`/`README.md`; 184 grader files = 94 `test_outputs.py` + 89 `test.sh` + 1 `verify.sh`. Scope is the population only — S079 holds task schema, S100 the entry count and verifier execution. Flip: a pin change, or a tree whose counts differ from `plans/round52-tasks.json` |
| `build-pmars/tests/test_outputs.py` raw capture at the same pin — `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py`, opened 2026-10-28 | **RE-OPEN S115, no new row** | re-fetched 2938 bytes / 85 lines, sha256 `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` — byte-identical to S115's anchor and to the pinned tree's blob size 2938. Quote at `:82`: `assert src_dir.exists(), "No src directory found"` (8 words). No mutable cell changes (`old → new`: status mined → mined, recheck 180d → 180d, used-by unchanged), so the row is re-verified, not rewritten. Flip: any byte change at the pin, or a different file, needs its own row |
| `build-pmars` as a round-52 C1 confirmation candidate | **EXCLUDE from `CONFIRMED new`** | `corpus/knowledge/tb2-build-pmars-grader.md` exists at the base tip, so this task was read by the lane before round 52; claims leg 3 admits only tasks never read before this round. Flip: none — the exclusion is definitional |
| prior-art primary for one confirmed finding — `__PRIOR_ART_ROW__` (scout seat) | **PENDING** | no URL is invented in this draft; the row shape is `S181`+ in `sources-draft.md`. Claims leg 4 needs ≥3 distinct URLs and a per-finding verdict phenomenon-known / phenomenon-new. Flip: a fetched primary with a located quote |

Spot-check result: S179's counts were re-derived twice from the same fetched document (once by
parsing `tree[]`, once from `plans/round52-tasks.json`'s `capture_population`), and S115's digest was
re-computed from a fresh fetch. Non-author spot-check of this Gate is the round-52 verifier's duty.

Census (run from the fleet root): round start, `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → exit 0, 171 rows, tier A=147/B=22/C=2, status
mined=155/queued=8/rejected=8, 15 `W04` warnings (all pre-existing). After S179 is inserted inside
the Registry table: 172 rows, `malformed=0`, still 15 `W04`, exit 0 (receipt in the wave report).
Insert the row **inside** the `## Registry` table — appending at end of file lands it under
`## Leads (unopened)` and the census fails `E12`.
