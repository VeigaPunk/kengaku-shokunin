# SimplStateCheckDead — round 26 build (read-only)

**Axes:** calibration (P2/v2 verdict stability) · operability (dead second authorities).  
**Snapshot:** lane `e0037a8da268`, `plans/state_check.py` 1365 ln. No P3 block landed yet (grep `P3a` → empty); findings are P2/v2-only.

**v2 baseline (receipt pin):**  
`python3 plans/state_check.py --summary` → `assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3` rc=0; `--selftest` → ALL PASS rc=0.  
`python3 plans/state_check.py --json` → 235 comparable assertions, **0** ids matching `section-pointer`.

**Coverage:** `python3 -m trace -c -C /tmp/k26-cov-{sum,st,json} plans/state_check.py --{summary,selftest,json}` (Python 3.14 stdlib trace). Union of the three modes exercises all population checks; many error arms stay cold by design.

## Unreachable on frozen lane tree (safe to delete for identical v2 output)

| # | lines | evidence | deletion |
|---|-------|----------|----------|
| 1 | 310–318 | summary+selftest trace: allowlist guard 0 hits; callers only pass `normalize_command`/`FREEZE_CHECK_COMMAND` tuples (548–573, 490–496) | drop guard block |
| 2 | 276 | logic: `"### x".startswith("## ")` is always false; conjunct excludes nothing | use `text.startswith("## ")` only |
| 3 | 601 | `"test -e"` branch 0 hits; `re.fullmatch(pat, "test -e")` false so skip is inert | remove set member |
| 4 | 837–850 | summary trace: outer loop hits, **`add` 847–850 never**; live SHONEN evidence has no `§` (grep SHONEN.md); `--json` emits 0 section-pointer assertions | remove P2c section-pointer pass |
| 5 | 978 | selftest+summary: `anchors["lessons/"]=what[0]+1` 0 hits; overwritten 987 before use | delete dead store |
| 6 | 1102 | `.get(verdict,0)` default never taken (dict preseeded 1097–1099) | `verdict_counts[assertion.verdict]+=1` |
| 7 | 735–746 | both mismatch arms 0 hits in summary∪selftest; only reachable on seed-shape failures selftest never injects | collapse to one arm (+ keep cursor rule explicit) |
| 8 | 1327 else + 1337–1341 | summary trace: `else find_protocol(root)` and `protocol is None` error 0 hits while `plans/fixtures/r25/shonen-seed.txt` exists | require fixture (exit 2 if missing) instead of cwd-walk fallback |

## Revised vs round-25 falsify (do NOT delete)

- **624–639 `find_protocol`:** was reported all-dead; at `e0037a8` **1331** calls it for fleet PROTOCOL drift whenever the seed fixture is used (summary trace: body 625–638 ≥1 hit). Keep function; only the **1327 fallback** and **1337** error path are dead in-repo.
- **1333–1336 pin-break branch:** 0 hits on good tree; keep (setup guard, not dead weight).
- **1352–1355 `--json`:** unexercised by default gate, not unreachable (json trace: 3 hits).
- **P2b axis `section` anchors 609–621:** live (4 hits) — not dead.
- **row_map header keys `entry/file/dir`:** real README headers — keep (R25 checked).

## Synthetic probe (out-of-population input)

`read_repo_text` patch replacing box-1 evidence with `§Frontier`: emits `P2c.box.1.pointer-only MISMATCH`, `pointer MISMATCH`, `section-pointer.1 MATCH`. Frozen population never contains this; removing #4 does not change the 235-assertion receipt.

## Duplication (not unreachable; optional YAGNI for writers)

- 1132–1146 selftest seed literal vs `SEED_FIXTURE` / `canonical_seed` (R25 #9).
- 452–456 vs 521–525 SCORECARD read prologue (R25 #10).
- Repeated `print(..., file=sys.stderr); return 1` in `run_selftest` (R25 #11).

**Installs:** none (stdlib trace + existing lane python3).

VERDICT: Seven mechanical dead branches plus one collapsible mismatch arm can be removed without changing v2 `--summary`/`--selftest` on `e0037a8`; retain `find_protocol` for drift (1331). Writers must not delete 624–639 wholesale.
