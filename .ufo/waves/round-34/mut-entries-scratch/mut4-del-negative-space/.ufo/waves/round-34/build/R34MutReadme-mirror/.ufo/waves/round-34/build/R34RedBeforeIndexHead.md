# Index-vs-HEAD failing-before receipt

Implemented only the assigned calibration receipt and this report.

- Capture: `.ufo/waves/round-34/falsify/red-before/index-head.txt`
- Mutant: sandbox export from `git archive HEAD`; deleted `corpus/knowledge/bench-arena-task27-timeout-anatomy.md`, leaving its README row intact.
- Exact evidence: receipt records the executed commands and outputs. The archive contained 41 README knowledge rows; after deletion, 40 knowledge files remained. Both separate probes returned exit 0, so a naive check treating successful execution as green misses the dangling row. The row itself is still visible at `corpus/README.md:42` in the sandbox.
- A row/file count comparison is not green; it reports 41 versus 40. This receipt demonstrates the specifically requested naive independent-check blind spot, not a failure of a comparison-based counter.
- Risks/blockers: the requested naive check is deliberately weak; do not interpret it as a robust validation.

VERDICT: red-before-index-head green-on-broken (proven)
