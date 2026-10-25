Axis: SOURCES census surface at freeze and receipts.

Receipts saved in `.ufo/waves/round-34/build/R34CensusProbe/`.

1. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` output: 15 W04 duplicate-URL warnings (S040, S048, S057–S059, S064–S069, S071, S075, S076, S100), followed by `kengaku\tok\t/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`; exit 0. Exact full output is `validate.txt` / `validate.output.txt`.
2. `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' .../corpus/SOURCES.md` → `97`, exit 0 (`rows.txt`).
3. `awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF!=13 {n++} END{print n+0}' .../corpus/SOURCES.md` → `0`, exit 0 (`malformed.txt`).
4. Tier/status histograms use `awk -F'|'` over source rows; receipt `histograms.txt` contains the output and exit code.
5. Duplicate IDs: extracted registry id column, piped to `sort | uniq -d` → empty stdout, exit 0 (`duplicate-ids.txt`).
6. Mined `used-by` paths: scanned all mined rows and checked each comma-separated path relative to lane root; output empty, exit 0 (`mined-paths.txt`).

Census output signals the same 15 W04 warnings as the frozen claim baseline; registry count is 97. No lane implementation files changed; only scoped receipts and this report were written.

VERDICT: census-probe-97-0