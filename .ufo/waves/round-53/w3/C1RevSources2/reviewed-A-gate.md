# Source gate — seat C1ScribeSources2A (kengaku round 53, wave 3, R53-C1 prior-art leg, group A)

Every row of `rows.md` was **re-opened by this seat on 2026-10-30**, not read from the wave-1 archive: the live URL was
fetched, the HTTP status recorded, the ≤25-word quote located in the bytes this seat fetched, and the sha256 of that
fetch recorded below. Machine-readable copy of the location column: `quote-locations.tsv`; raw fetch log with HTTP
codes and sizes: `fetch-log.tsv`; archived bytes and digests: `fetched/SHA256SUMS`.

Extraction methods used for the location column:

- **PDF** — `pdftotext -q` (plain, no `-layout`) over the fetched PDF; the quote is located by whitespace-normalised
  comparison and the reported location is the **line span** in that extraction.
- **HTML** — tags stripped (`re.sub(r"<[^>]+>", " ", s)`) and HTML entities unescaped; the location is the **rendered
  text line** number of the fetched bytes. Two rows are read from the raw HTML instead (T07 and T18, whose fetched
  bytes are the gzip-decoded Wayback snapshots): for those the location is given as **raw HTML line N (rendered text
  line M after tag stripping)**, and both numbers were computed.
- **Markdown / plain text** — the location is the **line number** of the fetched bytes (T12).

Line numbers are properties of the extraction method, not of the document; each row states which method applies.

## Per-row evidence

### T01 — Barr et al., The Oracle Problem in Software Testing: A Survey
- URL: https://philmcminn.com/publications/barr2015.pdf
- Access date: 2026-10-30 — HTTP 200, 773,275 B
- sha256 of fetch: `6c5689497594a75f08c1b37b3dd361e11c54946bbbf79f670d660f5d298d3d51`
- Location: PDF p.1 Introduction, plain `pdftotext` lines 26-29 (fetched/barr2015.txt)
- Quote (16 words): "a procedure that distinguishes between the correct and incorrect behaviors of the System Under Test (SUT)"
- Verdict: **queued**, tier B (survey)

### T02 — Petrovic and Ivankovic, State of Mutation Testing at Google
- URL: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46584.pdf
- Access date: 2026-10-30 — HTTP 200, 419,943 B
- sha256 of fetch: `c128ccd374906ade3e4e885dbfb685bc7268ee92ccf4c8d71f678b17e3cdbcca`
- Location: Introduction paragraph 2, plain `pdftotext` lines 73-76 (fetched/petrovic-google.txt)
- Quote (19 words): "coverage alone might be misleading, as in many cases where statements are covered but their consequences not asserted upon"
- Verdict: **queued**, tier A

### T03 — Schuler and Zeller, Assessing Oracle Quality with Checked Coverage
- Canonical URL: https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf — **HTTP 000 on
  2026-10-30** (host not reachable from this seat, `curl --max-time 90` gave code 000 and a 0-byte file)
- URL actually opened (HTTP 200, 1,492,763 B): https://web.archive.org/web/20260422011919id_/https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf
- sha256 of fetch: `4983cd98002012dfcdca34e6db64e3f7fd3d853978d465a3597662aa615e3326`
- Location: PDF p.6, section D "Explicit and Implicit Checks", plain `pdftotext` lines 828-831 (fetched/schuler-wayback.txt)
- Quote (17 words): "test suites with no assertions still detect a significant fraction of the mutations (43 % on average)"
- Verdict: **queued**, tier A. Kept bytes: the full 1,492,763 B PDF exceeds the 1 MiB cap, so `fetched/schuler-zeller-pages1-6.pdf`
  holds pages 1 and 6 (751,031 B, sha256 `09ae3057f0dfc0442163951db3a0b16f20fc313d18e5fb11b786aa24e80fff8f` — this
  seat's own qpdf slice, not byte-identical to wave 1's `8a072dd5…` slice) and the full text extraction is kept as
  `fetched/schuler-wayback.txt`; the quote is inside the kept text and inside the kept slice (line 239 of the
  slice's own extraction).

### T04 — Jain and Kalburgi, Mind the Gap
- URL: https://arxiv.org/pdf/2309.02395v1 (the abs page https://arxiv.org/abs/2309.02395 also answered HTTP 200, 42,375 B)
- Access date: 2026-10-30 — HTTP 200, 514,190 B
- sha256 of fetch: `8719ebae726001f4551a6555f9e988003e155f58e74bb0ee67481e415b928024`
- Location: PDF p.1 Introduction, plain `pdftotext` lines 79-82 (fetched/jain-kalburgi-pdf.txt)
- Quote (20 words): "We define the oracle gap as the difference between source code coverage and mutation score for a given software element"
- Verdict: **queued**, tier A

### T05 — BlindSpotEval, Beyond Coverage and Mutation
- URL: https://arxiv.org/html/2610.32548v1 (the abs page https://arxiv.org/abs/2610.32548 also answered HTTP 200, 42,507 B)
- Access date: 2026-10-30 — HTTP 200, 306,270 B
- sha256 of fetch: `7b1bd3d05941eedd411924ceb6f2d0e58a3ce26e89bcff5fb89e505201045232`
- Location: rendered text line 239 of the fetched HTML (tags stripped) (fetched/blindspot-2610.32548v1.html)
- Quote (18 words): "Oracle strength is high on average but uneven, with weaker assertions for object return property values and exceptions."
- Verdict: **queued**, tier A

### T06 — MUTGEN, Mutation-Guided Unit Test Generation with a Large Language Model
- URL: https://arxiv.org/abs/2506.02954
- Access date: 2026-10-30 — HTTP 200, 45,048 B
- sha256 of fetch: `d47c8464bdf4c8d5933e30558ae4d496c0d189ee7a1e320baace9449344af1e8`
- Location: rendered text line 115 of the fetched abs page (tags stripped) (fetched/mutgen-2506.02954-abs.html)
- Quote (11 words): "some test suites achieve 100% coverage but only 4% mutation score"
- Verdict: **queued**, tier A

### T07 — Meszaros, Assertion Roulette at XUnitPatterns.com
- Canonical URL: https://www.xunitpatterns.com/Assertion%20Roulette.html — **HTTP 000 on 2026-10-30** (host not reachable)
- URL actually opened (HTTP 200, 18,201 B after gzip decoding): https://web.archive.org/web/20250118170143id_/https://www.xunitpatterns.com/Assertion%20Roulette.html
- sha256 of the decoded bytes: `e6264bc28447a2d343eecfdbfed7b9388b7bef390ffbf3d555d73a33ca9d32ed`
- Location: raw HTML line 78 of the fetched bytes (rendered text line 70 after tag stripping) (fetched/assertion-roulette-wayback-2025-01-18.html)
- Quote (12 words): "hard to tell which of several assertions within the same test method"
- Verdict: **rejected** — failure-localization smell, not an existence-only or oracle-strength class; the test-smell
  catalogue is already rowed as S189.

### T08 — Konstantinou, Degiovanni and Papadakis, Can we find bugs using LLM-generated oracles?
- URL: https://arxiv.org/abs/2410.21136
- Access date: 2026-10-30 — HTTP 200, 42,261 B
- sha256 of fetch: `47ce55929512c6221a9296c96689f1360382676747f035b43f4f44355a877bf2`
- Location: rendered text line 115 of the fetched abs page (tags stripped) (fetched/konstantinou-2410.21136-abs.html)
- Quote (12 words): "oracles that mirror the program's actual behavior rather than the expected one"
- Verdict: **rejected** — oracle-fidelity defect class (oracles encoding the buggy actual behaviour), not
  existence-only acceptance.

### T09 — BenchJack, Do Androids Dream of Breaking the Game?
- URL: https://arxiv.org/html/2605.12673v1
- Access date: 2026-10-30 — HTTP 200, 1,908,264 B
- sha256 of fetch: `568e71c9ba1bcd491c5b9baf8989e0fac5f917f4412fff9f87ef80ec12e2f70b`
- Location: rendered text line 804 of the fetched HTML (tags stripped) (fetched/benchjack-2605.12673v1-first1MiB.html —
  the first 1,048,576 B of the same fetch, sha256 `9164745fc324fd9460934464018f1bc5829444d7e2ab56f87eff059766ad5dee`; the
  quote is inside the kept span, and a second fetch of the same URL reproduced the full-file sha256 byte for byte)
- Quote (22 words): "Simple exploits can drive the hack rate to near-perfect on nine of the ten benchmarks, including Terminal-Bench, SWE-bench Pro, and SWE-bench Verified."
- Verdict: **queued**, tier A

### T10 — Unearned Passes, Maintaining Benchmarks Against Increasingly Capable Agents
- URL: https://arxiv.org/html/2609.34262v1
- Access date: 2026-10-30 — HTTP 200, 379,862 B
- sha256 of fetch: `abe2155a70579ec11c147838b4c2603b1566c2de2cf31c64123393aae285eaf2`
- Location: rendered text line 314 of the fetched HTML (tags stripped) (fetched/unearned-passes-2609.34262v1.html)
- Quote (19 words): "Most benchmark verifiers evaluate observable outcomes, such as whether expected files exist, tests pass, or specified conditions are satisfied."
- Verdict: **queued**, tier A

### T11 — The Verification Horizon
- URL: https://arxiv.org/html/2606.26300v1
- Access date: 2026-10-30 — HTTP 200, 826,283 B
- sha256 of fetch: `08fc5c5cd178bd05004eae9c9c8978b09a9c27b3bc9cdc04112a05a2a8425d43`
- Location: rendered text line 399 of the fetched HTML (tags stripped) (fetched/verification-horizon-2606.26300v1.html)
- Quote (14 words): "the absence of false positives (an incorrect solution passes the tests) and false negatives"
- Verdict: **queued**, tier A

### T12 — holdout-cc/holdout-findings README
- URL: https://raw.githubusercontent.com/holdout-cc/holdout-findings/main/README.md
- Access date: 2026-10-30 — HTTP 200, 17,773 B
- sha256 of fetch: `5195672a02349db34e282318b22a75533c8086be897db963971dcf881f1207ad`
- Location: line 3 of the fetched README (fetched/holdout-findings-README.md)
- Quote (18 words): "ways an agent can score well without doing the task, and places where the grader scores work incorrectly"
- Verdict: **queued**, tier B (community issue catalogue, never A)

### T13 — BetterBench
- URL: https://arxiv.org/html/2411.12990v1
- Access date: 2026-10-30 — HTTP 200, 532,721 B
- sha256 of fetch: `9e50ae5fa9273355f098772655f424fcca9b100da4883acf646c7837fd6b7002`
- Location: rendered text line 264 of the fetched HTML (tags stripped) (fetched/betterbench-2411.12990v1.html)
- Quote (14 words): "we develop an assessment framework considering 46 best practices across an AI benchmark’s lifecycle"
  — the apostrophe in `benchmark’s` is the typographic one in the bytes; the ASCII form does **not** occur in this fetch
  (checked: 0 hits for the ASCII form, 1 hit for the typographic form, same line).
- Verdict: **rejected** — the 46 criteria score a benchmark’s lifecycle (design, implementation, documentation,
  maintenance) and none scores the benchmark's own grader or oracle strength. Checked in the fetched bytes: the
  implementation-stage criteria paragraph is about "the availability of necessary code and infrastructure and the
  inclusion of key engineering features" (rendered text line 423), and no criterion in the file scores oracle or
  grader strength. Flip: a criterion, or a per-benchmark score, that measures grader strength or acceptance of a
  trivial solution.

### T14 — Fantastic Bugs and Where to Find Them in AI Benchmarks
- URL: https://papers.nips.cc/paper_files/paper/2025/hash/5b44b99d012922011f0be1031a98c4f9-Abstract-Datasets_and_Benchmarks_Track.html
- Access date: 2026-10-30 — HTTP 200, 10,098 B
- sha256 of fetch: `fa1ae5f7ac7456da411fb15e836e7a81b98eaa5b3ae5bddf7ecd7758b85c0197`
- Location: abstract section, rendered text line 157 of the fetched page (fetched/fantastic-bugs-neurips2025-abstract.html)
- Quote (11 words): "leverages statistical analysis of response patterns to flag potentially invalid questions"
- Verdict: **rejected** — item-level validity only; no grader or test-suite-strength scope.

### T15 — Agentic Benchmark Checklist, HTML rendering
- URL: https://arxiv.org/html/2507.02825v1
- Access date: 2026-10-30 — HTTP 200, 570,513 B
- sha256 of fetch: `0b3bf59a9de5142aeab18ecc9ed89456e8854e800710b4efd755f274d262570f`
- Location: rendered text line 166 of the fetched HTML (tags stripped) (fetched/abc-2507.02825v1.html)
- Quote (3 words): "Agentic Benchmark Checklist" — the title string, which is the whole point of this row: it identifies
  the paper already rowed as S091 (https://arxiv.org/abs/2507.02825, opened 2026-10-25).
- Verdict: **rejected** — duplicate source.

### T16 — Agentic Benchmark Checklist project page
- URL: https://uiuc-kang-lab.github.io/agentic-benchmarks/
- Access date: 2026-10-30 — HTTP 200, 22,122 B
- sha256 of fetch: `80c4f8a0b912453e71bd80c8bb2c1831c0ab73d1adec73b7bd6db92ff4b43757`
- Location: rendered text line 473 of the fetched page (tags stripped) (fetched/abc-project-page.html)
- Quote (8 words): "actionable guidelines to ensure outcome and task validity"
- Verdict: **rejected** — companion landing page of the work already rowed as S091.

### T17 — arXiv 2410.20574 (guessed BetterBench identifier)
- URL: https://arxiv.org/abs/2410.20574
- Access date: 2026-10-30 — HTTP 200, 39,464 B
- sha256 of fetch: `ebfa67975e4861412251baaf8d16e3a6e269166cb4f0790458a9a15b238809b7`
- Location: rendered text line 4 of the fetched abs page (tags stripped) (fetched/arxiv-2410.20574-abs.html)
- Quote (8 words): "Local bi-integrability of bi-Hamiltonian systems via bi-Poisson reduction"
- Verdict: **rejected** — the identifier serves a differential-geometry paper, not a benchmark assessment.

### T18 — BetterBench project site
- Canonical URL: https://betterbench.stanford.edu/ — **HTTP 000 on 2026-10-30** (host not reachable; two attempts timed out)
- URL actually opened (HTTP 200, 10,549 B after gzip decoding): https://web.archive.org/web/2026id_/https://betterbench.stanford.edu/
- sha256 of the decoded bytes: `f88b13a269ecdafa582709d80c808d94b0c5374bfb36488bfc72f0df99e273a7`
- Location: raw HTML line 87 of the fetched bytes (rendered text line 85 after tag stripping) (fetched/betterbench-project-site-wayback.html)
- Quote (17 words): "A repository of AI benchmark assessments for informed benchmark selection through quality evaluation and best practice analysis"
- Verdict: **rejected** — landing page of the paper rowed as T13; navigation only.

## Duplicate-URL sweep (W04) against the existing registry

Two sweeps were run 2026-10-30 from the lane root.

(a) Census-equivalent sweep (authoritative, reproduces `scripts/sources-census.sh`): the URL is taken from the
**source column only** of each row and normalized as the census normalizes it (scheme stripped, trailing slash and
fragment stripped, host lower-cased). Parsed rows: 186 in `corpus/SOURCES.md`, 18 in `rows.md`.

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # -> 186
# python: url_of(source) for every registry row and every rows.md row, then set difference
```

Result: **0** of the 18 rows carry a source-column URL already present in the registry; the 18 row URLs are pairwise
distinct; intra-row duplicate URLs: none.

(b) Loose sweep (every URL token anywhere in the registry file): 158 distinct URLs in the registry,
`comm -12` against the 19 URL tokens in `rows.md` → 0 shared.

The only work already rowed (ABC / arXiv 2507.02825, row S091) is carried as the rejected rows T15 and T16 with the
duplicate reason, so no new duplicate URL is introduced. The pre-existing 15 W04 duplicate-url warnings in the
registry are the census's own standing count; this seat adds none.

## Row-shape self-check (contract v1)

Run over `rows.md` on 2026-10-30:

- rows: 18 (`T01`…`T18`), ids unique, no `|` inside any cell.
- column count: every data row has 11 cells (awk NF = 13 with the leading and trailing pipe).
- tier enum: 16 × A, 2 × B, 0 × C; no `community` row (so no tier-inflation case).
- kind enum: 14 × paper, 4 × docs.
- status enum: 10 × queued, 8 × rejected.
- `opened` = 2026-10-30 on every row; `recheck` = 180d (17 rows) or 90d (T12); `used-by` = `—` on every row.
- every quote is ≤ 25 words (longest: T09 at 22 words) and was located in the bytes this seat fetched today.
