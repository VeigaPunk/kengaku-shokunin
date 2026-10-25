ATTACKS: plans/l0_filed_check.sh queue-entry identity and calibration

HIGH — false green: substring mentions count as filed rows.
- `sh .../l0_filed_check.sh /tmp/k25w2-RevL0Check/bullet-report.md /tmp/k25w2-RevL0Check/bullet-queue.md` returned `FILED report:2 queue:2 ... filed=1 unfiled=0`, exit 0. Queue line 2 is explicitly `- Not a queue row, merely a note quoting an example: ...`; there is no appended L0 row.
- Wrapped prose variant (`wrapped-report.md` vs `wrapped-queue.md`) likewise returned `FILED report:2 queue:2 ... exit=0`; the matching `kengaku | round-77 |` text is inside an editorial paragraph, wrapped onto a second line, not a queue row.
- Cause: `plans/l0_filed_check.sh:29-35` only rejects a preceding lane-name character; `:49-55` flattens the whole queue; `:94-98` counts any matching substring. This can satisfy R11 without the question being appended, contrary to `PROTOCOL.md:524-530` and `corpus/QUALITY.md:104`.

MEDIUM — wrapped row delimiter false negative.
- `sh .../l0_filed_check.sh /tmp/k25w2-RevL0Check/wrapped-report.md /tmp/k25w2-RevL0Check/wrapped-after-pipe-queue.md` returned `UNFILED ... [opening words at queue:4 without this lane/round anchor]`, exit 1, although queue lines 3-4 contain the matching anchor and question split immediately after `round-77 |`.
- `plans/l0_filed_check.sh:26,52-55` normalizes a terminal pipe to a trailing space, then appends another separator space; the required anchored string has one. This contradicts the advertised wrapped-queue behavior in `:8-9`.

PREFIX collision observed (policy caveat):
- The requested suffix-divergence case used full questions sharing 139 characters, differing only in final `A.`/`B.`. It returned `FILED ... exit=0`; the source explicitly truncates to 60 chars (`plans/l0_filed_check.sh:6-11,39-45,91-95`). `PROTOCOL.md:527-528` authorizes citation by opening words, so this is a collision risk, not a definite contract violation unless R11 requires full-text identity.

Baseline checks:
- Real round-24 report vs live queue: 3 UNFILED, `filed=0 unfiled=3`, exit 1.
- Both green fixtures (ordinary and rewrapped report) passed 3/3, exit 0; near-miss fixture reported 1 filed / 2 unfiled, exit 1.
- LSP unavailable: `read xd://lsp` returned `No such tool`; literal grep fallback found round-log/docs and dispatch records, not a semantic caller map. No installs.

VERDICT: BREAKS — prose/quoted mentions falsely satisfy the queue-filing check; wrapped delimiter also causes a false negative.