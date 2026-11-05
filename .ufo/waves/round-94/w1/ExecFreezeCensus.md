# ExecFreezeCensus — round 94 findings (report-only census, no claim leg)

Full report: `.ufo/waves/round-94/w1/ExecFreezeCensus/report.md`. Table: `.ufo/waves/round-94/w1/ExecFreezeCensus/census-v2.tsv`. Window facts: `.ufo/waves/round-94/w1/ExecFreezeCensus/windows.tsv`. Receipts: `.ufo/waves/round-94/w1/ExecFreezeCensus/receipts/`.

Gate v2 `plans/round94_freeze_integrity.py` (sha256 8574b4d5…) and v1 `plans/round93_freeze_integrity.py` (sha256 18b01b42…) were both run on the round-93 census rows (85–91, paths mode), round 93 claims, round 94 claims, and the round-92 W1 window, from a scratch clone at T `90c7677f`.

FINDING CEN94-1 info v2 reproduces the round-93 census and both claims rows: every rc, count and broken-instrument set matches v1; differs=no in all nine rows of census-v2.tsv.
FINDING CEN94-2 info No historical verdict changes under v2. --full-history cannot change a verdict where the window has zero merges; every measured window has zero merges and is linear (first-parent walk equals full walk). The new table rules are not exercised by any census table.
FINDING CEN94-3 minor (bytes; carried from r93) Round 85 (broken 3), 86 (broken 2), 89 (broken 1), 91 (broken 1) remain byte-breached in their windows; unchanged by v2.
FINDING CEN94-4 info Round 94's claims-mode window `844c504e`→`90c7677f` is one commit; freeze-integrity at T covers only the measurement commit.
FINDING CEN94-5 info Post-T lane history (`242b3669`, `d04e6664`) touches none of the 11 round-94 tabled instruments; no merges in that span.
FINDING CEN94-6 info Pathspec edge (not verdict-flipping): rev-list treats `*?[` in a path as a glob; none of the 55 unique tabled paths contains `*`, `?`, `[` or a space. Noted for round 95.
FINDING CEN94-7 info Freeze selection is operator-supplied in both v1 and v2; the census takes each round's freeze as given.

No defect found that flips a verdict in this census. No tool installed or upgraded. The lane was only read; no git mutation in the lane.
