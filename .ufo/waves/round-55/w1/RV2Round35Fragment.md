# RV2Round35Fragment — scoped findings (round 55, wave 1)

**Question:** why did `round35-c1-coverage`'s declared evidence fragment stop matching the entry's output?

**Answer (short):** the V4 script's wording never changed. V4 prints live knowledge-file counts against a constant `42` frozen at round 35. The round-54 fragment `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)` (ledger `plans/round54-entrytruth.json`, measured at `6e0a1915`) stopped matching at `9a0746be` (round 54), which added `corpus/knowledge/external-anchor-freeze.md` and moved the counts to 58/58.

**Verdict type:** the fragment change is wording-neutral (numbers only). The row's TRUE exit/state has been red (exit 1) since `805fe790` (round 36); that transition was the real truth change (green→red) and came from the new knowledge entry `tb2-regex-log-grader.md`.

**Evidence:**
- `plans/round35_c1_verify.py`: single history, commit `11d64530`; same blob `97431502…` in all four commits carrying it; `git diff HEAD` empty.
- V4 transitions (scripted, `v4()` in a scratch clone): `4fe72a9a` ok (42/42); `805fe790` 43/43 red; `6e0a1915` 57/57; `9a0746be` 58/58; `80afa613` (HEAD) 58/58.
- Substring predicate: `plans/round54_c2_entrytruth.py:338`; round-54 fragment vs HEAD output → not a substring.

**Divergences / defects (not fixed here):**
- `SKILL.md:623` cell claims 55/54 "at HEAD" — false at HEAD (58/58).
- `plans/round54-entrytruth.json` round-35 row fragment is stale at HEAD.
- Round-55 C3 adds another knowledge file; any fragment correction must be taken at the final measured-after revision.

**Confidence:** high on history and mechanism; high on transitions; the round-54 counter's verdict on this row is inferred from its predicate, not executed.

Full detail: `.ufo/waves/round-55/w1/RV2Round35Fragment/root-cause.md`; commands and exit codes: `.ufo/waves/round-55/w1/RV2Round35Fragment/report.md`.
