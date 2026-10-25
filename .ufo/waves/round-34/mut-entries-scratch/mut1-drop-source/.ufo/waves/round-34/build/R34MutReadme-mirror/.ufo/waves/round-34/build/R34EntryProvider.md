# R34EntryProvider — scoped findings

Axes: depth and adjacency. Drafted the provider self-report entry, preserving provenance limits and tying both sources to the lesson that self-reported eval claims must remain labeled as such.

## Behavior / gates

- Created `.ufo/waves/round-34/build/R34EntryProvider/entry.md` (staging only; did not write into corpus/ or registry).
- Entry metadata uses `source: S108, S109` and `verified-at: 2026-10-25`; includes recheck cadence, caveats, and explicit negative space.
- Quote fragments are under 25 words each: NEC 「対話性能の一側面しか測れていない」 (SOURCES.append.md:21); METI 「完全に未知なテストデータを用いて性能評価を行うことが重要」 (captured HTML:112). METI anchor also names W&B and the benchmarks (captured HTML:112-114, 127-129).
- Source checks: read frozen claims (`plans/round-34-claims.md`, lines 125-133); read quarantine slice (rows S091/S105); read source appendix (SOURCES.append.md, rows S091/S105). NEC capture returned Access Denied, not article bytes (`assimilation/captures/nec-s091.html:1-10`), so no NEC quote could be independently located in that capture. METI captured archived page was readable and provides the cited anchor.

## Findings / limits

The assignment specifies the NEC and METI statements but the available NEC capture is an access-denied response. The draft reflects the stated NEC claim as a self-report but its quote is supported only by the staged appendix, not captured article bytes. This source verification remains incomplete and the row should not be represented as independently verified from the capture. METI's original is withdrawn; draft states the archive snapshot is the pin and avoids claims about live page state. No package entries screened in this scoped task; no package verdicts made. No product code, plans, corpus, index, registry, or source repo modified. No tools installed; no checks run.

VERDICT: entry-provider-drafted
