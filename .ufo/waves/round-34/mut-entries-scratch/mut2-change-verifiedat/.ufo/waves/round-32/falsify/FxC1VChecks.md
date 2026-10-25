# FxC1VChecks — second receipt and staged checks

Command run from the lane root: `python3 plans/round32_c1_verify.py --lane .`

Full output:
```text
checks=6 defects=0
EXIT=0
```

The command exit is 0. The checks below are evaluated against the current draft tree (including the uncommitted entry and registry/index drafts), not a hypothetical landed tree.

## V-check results

- **V1 — pass.** Entry is present at `corpus/knowledge/benchmark-grader-semantics.md`; line 4 says `verified-at: 2026-10-25`.
- **V2 — pass.** The counter's V2 rule (plan lines 69–89) reads each cited registry source cell URL and requires its host+path in that ID's own entry source line. In the current drafts, the identity pairs are:
  - S093: registry `corpus/SOURCES.md:112` gives `https://github.com/scaleapi/SWE-bench_Pro-os`; entry `corpus/knowledge/benchmark-grader-semantics.md:1` contains `https://github.com/scaleapi/SWE-bench_Pro-os`.
  - S094: registry `corpus/SOURCES.md:114` gives `https://github.com/hkust-nlp/Toolathlon`; entry line 2 contains that same host+path.
  - S097: registry `corpus/SOURCES.md:115` gives `https://arxiv.org/abs/2412.05579`; entry line 3 contains that same host+path.
  Thus all three pass the specific identity predicate, beyond mere citation-ID presence.
- **V3 — pass.** Entry lines 1–3 name pins `66f92766`, `9be8d8fe`, and `2412.05579`; all required literals are present.
- **V4 — pass.** README line 67 has one row beginning `| \`knowledge/benchmark-grader-semantics.md\``, and its title/description cell is non-trivial (well over the 20-character threshold in plan lines 100–112). No second matching index row was found in the check's full-file scan.
- **V5 — pass.** The entry draft has 93 numbered lines as returned by the file reader; it exceeds both thresholds in the counter (40 lines and 3,000 characters). The counter's structural test is only length, not semantic quality; pass does not independently certify the claims' truth.
- **V6 — pass.** `control-nothing.txt:3` records `expect_sha256=a1a7e8604008532242b9b8e4ef06485b386e24508ac0e29072d95263ca73be9f` and line 6 says `exit=1`. The counter recomputes the expect-file SHA-256 and accepts this receipt only when it contains the matching digest and `exit=1` (plan lines 125–136); overall run confirms it matched.

## Draft / landing conclusion

No V1–V6 check currently fails on the draft tree. Therefore there is no failing staged V-check for landing to repair: based on these predicates and the present bytes, landing the same entry/registry/index/control/expect bytes preserves the pass result. This is a conditional statement about these exact staged drafts; the counter was not run against a post-landing commit. The frozen claim separately requires the adoption counter/census and the pinned-source kill rule; this receipt does not establish those additional predicates or authenticate source quotations.

VERDICT: v-checks-staged
