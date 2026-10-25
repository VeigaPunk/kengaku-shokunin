ATTACKS: kaika W3 F4 search-log correction; F7 S036 tier/supersession

## Findings (by severity)

- **P2 — F7's tier-B rationale remains underdetermined.** S036 correctly appends a superseding row, but the cited reason only shows that the log is not a *re-runnable gate output*. SOURCES' tier A also covers any source primary/authoritative for its scope, while B means strong secondary (`../CORPUS.md:93-96`). S036 scopes itself to the lane's recorded round-23 result, and its source is that run's original log (`corpus/SOURCES.md:58`; `corpus/evidence/attrib-r23-stream.log:1-8,239`). Requiring an endpoint to repeat a historical run does not by itself make its original log secondary. The B downgrade is therefore not established by the wording; the A-vs-B classification remains open.
  - The observed facts and re-verdict do match: log line 239 records target n=0 / stored FAIL; the calibration receipt reports `stream-target:opencode-go ... stored=FAIL interval=UNTESTED` (`corpus/evidence/round25-calibration/attrib-calibration-summary.txt:45`). The receipt SHA-256 matches the value in S036 and the source gate: `afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131` (`sha256sum corpus/evidence/attrib-r23-stream.log`). No live endpoint was contacted.

## Survives

- **F4 correction is accurate and appended.** The prior search-log line attributes Scale's contamination-resistance rejection to S006's ~30% broken-task finding (`corpus/SOURCES.md:75`); S006 is about task validity. The appended correction at `corpus/SOURCES.md:78` identifies that mismatch and points to S026, which explicitly separates the properties and gives the vendor-self-description rationale (`corpus/SOURCES.md:48`). QUALITY Q9 requires the rejection reason to address the same property (`corpus/QUALITY.md:67-74`).
- **Append-only rule 2 is respected for these fixes.** The only in-place registry field changed in `git diff e21f9ea 8ea41f9 -- corpus/SOURCES.md` is S011 `used-by`, an allowed field; the old→new change is recorded in `corpus/lessons/round-25.md:36-39`. S025's tier/cells remain unchanged (`corpus/SOURCES.md:47`); S036 is a new row whose `teaches` begins `supersedes S025 —` (`corpus/SOURCES.md:58`), as required by `../CORPUS.md:116-118`. The F4 correction is also a new search-log line, not an edit to the old entry.

## Residual risk and verification gaps

- S036's B label is the sole unresolved scoped issue; the reason does accurately say the logged run needs an endpoint for a rerun and its n=0 result re-verdicts UNTESTED.
- No LSP device is mounted (`xd://lsp` returned “No such tool”); review used the committed diff and source text. No tools installed.

VERDICT: PARTIAL — F4 and append-only compliance survive; F7's superseding-row mechanics survive, but the B-tier classification is not justified by its stated rationale.