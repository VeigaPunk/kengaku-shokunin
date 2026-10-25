# Round 31 census falsification

## Evidence boundary

`/home/vgpnk/Projects/shokunin/CORPUS.md:131-148` defines seven frozen manual commands; its maintained-parser note is at `:150-155`. The lane tree does not contain `CORPUS.md` (checked with `test -f CORPUS.md`, exit 1), nor `scripts/sources-census.sh` (lane-root `glob` found none). Thus I re-ran all seven manual census commands verbatim as listed, plus the maintained C1 census command that is available in this lane. The maintained fleet CLI cannot be run here: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `command not found`, exit 127. No tool was installed or updated.

## Seven manual counters (CORPUS.md:134-147)

Commands run from the lane root against `corpus/SOURCES.md`:

1. Rows, `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` → `91`. Round-31’s captured before state says 88 (`.ufo/waves/round-31/claims/census-before.txt:15`); round-30 after receipt says 88 (`corpus/evidence/round30/census-after.txt:15-16`). Current-vs-round30 after: +3.
2. Malformed-row count, CORPUS.md:137 awk → `0`; no malformed rows were printed. This has no corresponding round-30 receipt value.
3. Tier histogram, CORPUS.md:139 awk → `A=81 B=8 C=2` (order from awk). The round-30 lesson says A 76→78 and B 4→8 at `corpus/lessons/round-30.md:92-97`, but that is the round-30 delta narrative, not a full histogram receipt; current is not directly compared to a seven-counter receipt.
4. Status histogram, CORPUS.md:141 awk → `mined=79 queued=8 rejected=4`. No corresponding round-30 receipt value.
5. Duplicate-id check, CORPUS.md:143 awk/sort/uniq → empty output, as required. No corresponding round-30 receipt value.
6. Enum/tier-inflation check, CORPUS.md:145 awk → empty output, as required. No corresponding round-30 receipt value.
7. Missing mined used-by paths, CORPUS.md:147 awk/while → empty output, as required. No corresponding round-30 receipt value.

The seven outputs are directly observed in this run; the tier/status output field totals each equal 91. The described seven commands are manual registry checks, not the warning-producing fleet census command.

## Maintained / additional counters

- `find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l` → `40`; index rows, `awk -F'|' '/^\\|[[:space:]]*`knowledge\\// {n++} END{print n+0}' corpus/README.md` → `40`; registry rows, a second AWK count → `91`. These match `corpus/lessons/round-31.md:116` (40/40/91), and differ from the round-30 after receipt’s registry 88 and round-30 lesson’s 39/39/88 at `corpus/lessons/round-30.md:95-97,182-183` by +3 rows, +1 knowledge file, +1 index row.
- Maintained C1 census `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` (exit 0). This is not the fleet `sources-census.sh` maintained census and does not print W04.
- Round-31 stored warning receipt `corpus/evidence/round31/census-after.txt:1-16` lists 15 W04 and exit success (`ok` line); round-30 after receipt `corpus/evidence/round30/census-after.txt:1-16` lists 14 W04 and `exit=0`. The differing warning is exactly additional `S100` at round-31 receipt line 15, duplicate URL `github.com/laude-institute/terminal-bench-2`. Round-31 lesson `:116-121` identifies it as the S079 same-repository cross-scope duplicate. Current fleet warning census itself was not re-run because its script is absent; therefore receipt-to-receipt comparison is observed, while receipt freshness is unverified.
- Round-31 `claims/census-before.txt:1-15` is the pre-round 14-W04 listing and 88-row `ok` record; matching warning IDs/URLs on lines 1-14 correspond to round-30 before/after listings (round-30 after lines 1-14). Round-31 after adds only S100. The round-30 before and after receipts contain the same fourteen W04 rows and report successful status.

## Number-drift check against old figures

Round-31 lesson `corpus/lessons/round-31.md:114-121` states before 14 W04/88 rows/39 knowledge files/39 index rows and after 15 W04/91/40/40. The before values are the recorded frozen baseline in `.ufo/waves/round-31/claims/census-before.txt:1-15` and the round-30 census receipts; the after values are supported by the available current row/file/index counts above, and receipt text `corpus/evidence/round31/census-after.txt:15-16` supports the new W04/exit, though not file/index counts. Reusing the old totals for the after state would be number-drift: it would undercount three registry rows and one knowledge/index row each; retaining the old 14-warning count would omit the newly recorded S100↔S079 duplicate. The lesson does not use old after figures: it explicitly gives current figures. Its own `corpus/lessons/round-31.md:135` also reports a distinct round-30 stale tier histogram (A79/B7/C2 versus corrected A78/B8/C2); my current manual histogram A81/B8/C2 is consistent with three net A and zero net B/C after that correction, not the stale A79/B7/C2. The exact seven old manual outputs are not present in the round-30 receipts, so differences beyond available round-30 tier/delta and census total evidence are not established.

VERDICT: Seven frozen manual commands were re-run; row count and maintained C1 census survived, malformed/duplicate-id/enum/path checks are clean; the fleet maintained census did not survive as a reproducible check (script unavailable), so its fresh W04 claim remains unverified. Round-31's after counts are not number-drift; using the old after totals would be.
