# Report — C1ScribeSources2A (kengaku round 53, wave 3, R53-C1 prior-art leg, source scribe, group A)

Date: 2026-10-30. Seat: source scribe. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read at HEAD
`9ead4476bf55b1ea6490d0204b668195db4a4d1d` (the lane advanced during the round; the L1 reconciles). No lane file was
modified — `git status --porcelain` in the lane shows only untracked paths (`.ufo/waves/round-53/w3/`, the L1's
`integrate_w3.py`, `w3.ready.dispatched`), no tracked file changed, and this seat ran no counter, so no lane clone
was needed; every command below reads the lane in place or writes to this seat's own directories.

## What I did

Finalised the `SOURCES.md` registry rows for the R53-C1 prior-art leg from the two wave-1 group-A scout drafts —
`C1ScoutSrcTesting` (software-testing literature on weak / existence-only assertions) and `C1ScoutSrcAudit`
(benchmark-validity checklists and meta-audits for agentic benchmarks). The two other wave-1 scout groups
(`C1ScoutSrcBench`, `C1ScoutSrcTB2`) are not mine.

CORPUS rule 1 was honoured as a re-open, not an archive read: **every one of the 18 rows' URLs was fetched live on
2026-10-30**, the HTTP status recorded, the ≤25-word quote located in the bytes this seat fetched, and the sha256 of
that fetch recorded. Ten rows are kept (`queued`), eight are `rejected` with a `REJECTED: … ; flip: …` reason.

Deliverables:

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/rows.md` — the 18 rows in
  the exact 11-column schema, ids `T01`…`T18` in document order for the L1 to renumber from S194.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/gate.md` — per-row URL,
  access date, HTTP status, sha256 of the fetch, located quote with its location, extraction method, verdict.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/fetched/` — the archived
  bytes (each ≤ 1 MiB) and `SHA256SUMS`.
- `fetch-log.tsv` (raw fetch log: id, name, HTTP code, bytes, sha256), `quote-locations.tsv` (machine-readable
  location column) — same directory.

## The 18 rows (T = this seat's placeholder id; the L1 renumbers from S194 in this document order)

| T | source | status | tier | HTTP | bytes | sha256 (first 16) | quote located at |
|---|---|---|---|---|---|---|---|
| T01 | Barr et al., The Oracle Problem in Software Testing: A Survey — philmcminn.com/publications/barr2015.pdf | queued | B | 200 | 773,275 | `6c5689497594a75f` | PDF p.1 Introduction, pdftotext lines 26-29 (16 words) |
| T02 | Petrovic and Ivankovic, State of Mutation Testing at Google — static.googleusercontent.com/…/46584.pdf | queued | A | 200 | 419,943 | `c128ccd374906ade` | Introduction paragraph 2, pdftotext lines 73-76 (19 words) |
| T03 | Schuler and Zeller, Assessing Oracle Quality with Checked Coverage — st.cs.uni-saarland.de/…/schuler-icst-2011.pdf (canonical host HTTP 000; read via Wayback 20260422011919id_) | queued | A | 200 | 1,492,763 | `4983cd98002012df` | PDF p.6 section D, pdftotext lines 828-831 (17 words) |
| T04 | Jain and Kalburgi, Mind the Gap — arxiv.org/pdf/2309.02395v1 | queued | A | 200 | 514,190 | `8719ebae726001f4` | PDF p.1 Introduction, pdftotext lines 79-82 (20 words) |
| T05 | BlindSpotEval, Beyond Coverage and Mutation — arxiv.org/html/2610.32548v1 | queued | A | 200 | 306,270 | `7b1bd3d05941eedd` | rendered text line 239 (18 words) |
| T06 | MUTGEN — arxiv.org/abs/2506.02954 | queued | A | 200 | 45,048 | `d47c8464bdf4c8d5` | rendered text line 115 (11 words) |
| T07 | Meszaros, Assertion Roulette — xunitpatterns.com (HTTP 000; Wayback 20250118170143id_) | rejected | A | 200 | 18,201 | `e6264bc28447a2d3` | raw HTML line 78 / rendered line 70 (12 words) |
| T08 | Konstantinou et al., Can we find bugs using LLM-generated oracles? — arxiv.org/abs/2410.21136 | rejected | A | 200 | 42,261 | `47ce55929512c622` | rendered text line 115 (12 words) |
| T09 | BenchJack, Do Androids Dream of Breaking the Game? — arxiv.org/html/2605.12673v1 | queued | A | 200 | 1,908,264 | `568e71c9ba1bcd49` | rendered text line 804 (22 words) |
| T10 | Unearned Passes, Maintaining Benchmarks Against Increasingly Capable Agents — arxiv.org/html/2609.34262v1 | queued | A | 200 | 379,862 | `abe2155a70579ec1` | rendered text line 314 (19 words) |
| T11 | The Verification Horizon — arxiv.org/html/2606.26300v1 | queued | A | 200 | 826,283 | `08fc5c5cd178bd05` | rendered text line 399 (14 words) |
| T12 | holdout-cc/holdout-findings README — raw.githubusercontent.com/…/README.md | queued | B | 200 | 17,773 | `5195672a02349db3` | line 3 (18 words) |
| T13 | BetterBench — arxiv.org/html/2411.12990v1 | rejected | A | 200 | 532,721 | `9e50ae5fa9273355` | rendered text line 264 (14 words) |
| T14 | Fantastic Bugs — papers.nips.cc proceedings abstract | rejected | A | 200 | 10,098 | `fa1ae5f7ac7456da` | rendered text line 157 (11 words) |
| T15 | ABC paper HTML — arxiv.org/html/2507.02825v1 (duplicate of S091) | rejected | A | 200 | 570,513 | `0b3bf59a9de5142a` | rendered text line 166 (3 words) |
| T16 | ABC project page — uiuc-kang-lab.github.io/agentic-benchmarks/ | rejected | A | 200 | 22,122 | `80c4f8a0b912453e` | rendered text line 473 (8 words) |
| T17 | arXiv 2410.20574 (a guessed BetterBench id) — arxiv.org/abs/2410.20574 | rejected | A | 200 | 39,464 | `ebfa67975e486141` | rendered text line 4 (8 words) |
| T18 | BetterBench project site — betterbench.stanford.edu (HTTP 000; Wayback 2026id_) | rejected | A | 200 | 10,549 | `f88b13a269ecdafa` | raw HTML line 87 / rendered line 85 (17 words) |

Access date for every row: **2026-10-30**. Quote word counts: longest is T09 at 22 words; every row's stated count
matches the counted words.

## Exact commands run

```sh
# 1. lane state and registry size (read-only)
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse HEAD
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          # -> 186

# 2. live fetch of every row URL (scratch only; TMPDIR default, NVMe /fast)
S=/fast/scratch/hyaku/kengaku-r53/C1ScribeSources2A; mkdir -p "$S/fetched"; cd "$S"
while IFS='|' read -r id name url; do
  code=$(curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) kengaku-scribe/1.0' --max-time 90 \
         -w '%{http_code}' -o "fetched/$name.bin" "$url")
  sz=$(stat -c%s "fetched/$name.bin"); sha=$(sha256sum "fetched/$name.bin" | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$name" "$code" "$sz" "$sha" >> fetchlog.tsv
done < urls.txt

# 3. Wayback fallbacks for the three unreachable hosts (T03, T07, T18)
curl -sL --max-time 120 -w '%{http_code}' -o fetched/schuler-wayback.bin \
  'https://web.archive.org/web/20260422011919id_/https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf'
curl -sL --max-time 120 -w '%{http_code}' -o fetched/assertion-roulette-wayback.bin \
  'https://web.archive.org/web/20250118170143id_/https://www.xunitpatterns.com/Assertion%20Roulette.html'
curl -sL --max-time 60  -w '%{http_code}' -o fetched/betterbench-site-wayback.bin \
  'https://web.archive.org/web/2026id_/https://betterbench.stanford.edu/'
# the two Wayback HTML payloads are gzip-encoded; decoded with `gunzip -c` / gzip.decompress

# 4. quote location (PDF: plain pdftotext, no -layout; HTML: tags stripped + entities unescaped)
pdftotext -q fetched/barr2015.bin fetched/barr2015.txt
python3 gate_table.py   # -> quote-locations.tsv : id, url, bytes, sha256, words, line(s), found
python3 spans.py        # -> line spans for the four PDF quotes

# 5. row-shape self-check on rows.md (contract v1 census rules)
grep -cE '^\|[[:space:]]*T[0-9]{2}[[:space:]]*\|' rows.md                     # -> 18
awk -F'|' '/^\|[[:space:]]*T[0-9][0-9][[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' rows.md   # -> 0
awk -F'|' '/^\|[[:space:]]*T[0-9][0-9][[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} …' rows.md  # tier hist
# kind hist / status hist / opened / recheck / used-by: same awk pattern on $4 / $9 / $10 / $11 / $12
awk -F'|' '/^\|[[:space:]]*T[0-9][0-9][[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' rows.md | sort | uniq -d   # -> (empty)

# 6. duplicate-URL sweep, census-equivalent (source column only, census normalization)
grep -oE 'https?://[^ |)]+' corpus/SOURCES.md | sort -u > /tmp/reg_urls.txt    # 158 distinct loose URLs
LC_ALL=C comm -12 /tmp/reg_urls.txt /tmp/row_urls.txt                          # -> 0 shared
python3  # url_of(source) per row for corpus/SOURCES.md and rows.md -> set difference
#   registry rows parsed 186, my rows parsed 18, overlap 0, my distinct URLs 18 of 18, intra-row dups: none
```

## Measured numbers

- Registry before this seat: **186 rows** in `corpus/SOURCES.md`; next free id **S194** (the L1 renumbers T01…T18 to
  S194…S211 in this document order).
- Rows produced: **18** — 10 `queued`, 8 `rejected`; tiers A = 16, B = 2, C = 0; kinds paper = 14, docs = 4; no
  `community` row (so no tier-inflation case).
- Row shape: 18 rows, **0** rows with NF ≠ 13 (i.e. every row has exactly 11 cells), no duplicate ids, no `|` inside
  any cell, `opened` = 2026-10-30 on all 18, `recheck` = 180d on 17 and 90d on T12, `used-by` = `—` on all 18.
- Fetches today: **18/18** row URLs fetched; **16** answered HTTP 200 directly; **3** canonical hosts answered HTTP
  000 (`st.cs.uni-saarland.de`, `xunitpatterns.com`, `betterbench.stanford.edu`) and were read through the Wayback
  snapshots named in `rows.md` (all three snapshots answered HTTP 200).
- Quote verification: **18/18** quotes located in the bytes this seat fetched (0 misses, re-confirmed after the
  reviewer-driven revision round by the kept `verify-rows.py`); quote length ≤ 25 words on every row, longest 22.
- Duplicate-URL sweep: **0** overlaps between the 18 rows and the 186 registry rows under the census's own rule
  (source column, normalized URL); the 18 row URLs are pairwise distinct; the loose sweep over every URL token in
  the registry file (158 distinct URLs) also shares **0** with the row URL set.
- Wave-1 cross-check against the scouts' own `SHA256SUMS`: **12 of my 18 fetch digests reproduce the wave-1
  digests byte for byte** (barr2015 `6c5689…`, petrovic-google `c128cc…`, jain-kalburgi `8719eb…`, blindspot-html
  `7b1bd3…`, mutgen-abs `d47c84…`, assertion-roulette decoded `e6264b…`, konstantinou `47ce55…`, benchjack trimmed
  `9164745f…`, unearned-passes `abe215…`, verification-horizon `08fc5c…`, holdout-findings `519567…`,
  fantastic-bugs `fa1ae5…`). The other six differ for stated reasons: Schuler (wave 1 archived a 6-page slice,
  sha256 `8a072dd5…`; this seat records the **full** fetch `4983cd98…` and keeps its own qpdf slice, digest
  `09ae3057…`, which still carries the quote at line 239 of its own extraction), betterbench (`9e50ae5f…` vs
  `27320202…` — arXiv re-renders the page between the two fetches), and abc-html, abc-project and wrong-arxiv-id
  (the audit scout did not hash these three in its own `SHA256SUMS`). Every differing row was re-verified against
  this seat's own fetch, which is the one the row quotes.

## What I attacked (this is a verification seat; the attacks and their evidence)

1. **Rule-1 re-open attack on all 18 rows.** Every row's URL was fetched live today; the archive copy was not trusted.
   Evidence: `fetch-log.tsv` (18 lines, HTTP code + bytes + sha256 each) and `fetched/SHA256SUMS`. Landed: 18/18 rows
   re-opened with HTTP 200 from the URL recorded in the row.
2. **Quote-location attack.** Each row's quote was located in the fetched bytes by whitespace-normalised comparison,
   with the location recorded. Landed: 18/18 located, 0 misses (the single miss found during the seat's own pass —
   the BetterBench apostrophe — was fixed by replacing the ASCII `'` with the typographic `’` that the bytes carry,
   and the ASCII form was confirmed absent from that fetch: 0 hits ASCII, 1 hit typographic, same line).
3. **W04 duplicate-URL attack against the existing registry.** Evidence: the census-equivalent sweep above —
   0 overlaps over 186 registry rows, 18 distinct row URLs, no intra-row duplicate. The one work already rowed
   (ABC, arXiv 2507.02825 = S091) is carried only as the rejected rows T15/T16, so no new duplicate URL enters the
   registry.
4. **Tier attack against the wave-1 drafts.** The wave-1 drafts put the Barr survey at tier A; contract v1 names
   "survey" as tier B, so the row was demoted to B. The holdout-findings catalogue stays B (community, never A).
   No `community` row is proposed, so the census tier-inflation rule cannot fire.
5. **Keep/reject attack against the seat's keep rule.** Two wave-1 `queued` rows were demoted to `rejected` because
   they do not bear on tests that pass if an artefact merely exists, nor on grader / test-suite strength:
   **T13 BetterBench** (its 46 criteria score a benchmark's lifecycle — design, implementation, documentation,
   maintenance — and none scores the benchmark's own grader or oracle strength; checked in the fetched bytes: the
   implementation-stage paragraph is about code availability and engineering features) and **T14 Fantastic Bugs**
   (item-level validity via response-pattern statistics only). Both rows are kept as rejections with a `flip:`
   condition, so the L1 can overrule on its own judgement; this is flagged explicitly for that reason.
6. **Reviewer-driven revision round (2026-10-30, after the review seat `C1RevSources2` flagged three overclaims and
   two mislabelled locations).** All five points were accepted and fixed:
   - **T01 `teaches`** — the claim that an existence check "fails the definition itself" was removed (an existence
     requirement can be legitimate for some tasks, and a partial oracle is still an oracle). The cell now reads: the
     oracle is the procedure that separates correct from incorrect behaviour; an existence check distinguishes
     missing from present but does not distinguish valid from invalid contents, and whether an existence requirement
     is adequate is a question about the task's scope, not about the oracle definition alone.
   - **T02 `teaches`** — "the industrial name for the presence-only gap" was removed (the source describes
     coverage-without-assertion generally; it does not coin presence-only terminology). The cell now says coverage
     alone can mislead because the covered statements' consequences are never asserted upon, that this is a general
     statement about coverage without assertions and not the source's term, and that how weak any given assertion is
     remains a separate judgement the source does not make.
   - **T03 `teaches`** — "a presence-only suite sits just above that floor" was removed (the source does not order
     other suites against the assertion-free floor). The cell now states the 43 % figure, that a green run on its own
     is weak evidence of correctness, and that the source measures that floor for assertion-free suites only.
   - **T05, T10, T12 `teaches`** were tightened the same way: T05 now says the exclusion of incidental crash and
     exception kills "matters for any measure that must not read accidental failures as assertion strength" instead of
     claiming what a classifier needs; T10 says the observable-outcome mode "is named in this source" instead of
     "in the wild"; T12's enumeration now names the reward-hack pattern ids found in the kept README (01 do-nothing
     passes, 07 exit-code-only, 08 failure-defaults-to-pass) instead of a loose list.
   - **T07 and T18 location labels** were corrected: the earlier label "rendered text line 78 / 87" was the *raw* HTML
     line number for those two rows (the only two read from the raw HTML rather than the tag-stripped rendering).
     Both rows now read "raw HTML line N (rendered text line M after tag stripping)" — T07 raw 78 / rendered 70, T18
     raw 87 / rendered 85 — and `gate.md`'s method section states which convention applies to which row. The
     remaining HTML rows keep their rendered numbers, which the review seat confirmed match its own extraction
     (239, 115, 804, 314, 399, 264, 157, 166, 473, 4).
   After the revision the row-shape self-check was re-run unchanged: 18 rows, 0 malformed, 0 duplicate ids, tiers
   A = 16 / B = 2, status 10 queued / 8 rejected, kinds paper 14 / docs 4, every quote's stated word count equal to
   the counted words, longest 22.
7. **Re-runnable verifier kept in the seat directory.** `verify-rows.py` re-locates every row's quote in the kept
   bytes and rewrites `quote-locations.tsv` (id, url, tier, kind, status, opened, recheck, used-by, bytes, sha256,
   quote words, rendered lines, raw lines, located, quote). Run from the seat directory: `python3 verify-rows.py` →
   **18 rows, 0 misses**.

## Decisions the L1 should be aware of

- **Row order** for renumbering is this document's order (group A first: testing literature T01-T08, then benchmark
  grader audits T09-T18), each group in the wave-1 draft's own order.
- **T13 BetterBench was demoted from `queued` to `rejected`** by this seat (reason and flip above). If the L1's
  prior-art leg wants the benchmark-validity line admitted as a kept source, that is a one-cell flip; the evidence
  (URL, date, quote, location, sha256) is in `gate.md` either way.
- **T03's row URL is the canonical publisher URL** even though that host answered HTTP 000 today; the anchor names
  the Wayback snapshot that was actually read, with its digest. Same for T07 and T18.
- No `used-by` path is claimed by this seat: it writes no knowledge entry and no lesson; the L1 owns both.

## Files produced (absolute)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/rows.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/gate.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/fetch-log.tsv`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/quote-locations.tsv`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/verify-rows.py` — re-runnable
  verifier that re-locates every row's quote in the kept bytes and rewrites `quote-locations.tsv`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2A/fetched/` — 22 files
  (kept bytes, each ≤ 1 MiB) plus `SHA256SUMS`

Nothing was written outside this seat's directory and the scratch dir, which was removed before this report.

## Tool notes

- No tool was installed or upgraded; the existing `curl`, `pdftotext`, `qpdf`, `gzip` and `python3` sufficed. No
  pacman transaction was attempted (host-wide pacman pause of 2026-10-20 respected).
- Tool inconsistency line: `bash: the harness moved several commands to a background job and printed "Ran in a
  temporary shell while the session shell is busy with another command" — the command still ran to completion and its
  output was delivered, but a command expected to finish in a second may return as a background job id.`
- Tool inconsistency line: `bash: `truncate -s 1048576 benchjack.bin > benchjack-trim1m.html` truncates the input
  file in place and only the shell redirect creates the second file — the intended "copy the first 1 MiB" was
  therefore not what ran, and `fetched/benchjack.bin` was left truncated. Recovered by re-fetching the same URL,
  which reproduced the original full-file sha256 `568e71c9ba1bcd491c5b9baf8989e0fac5f917f4412fff9f87ef80ec12e2f70b`
  byte for byte; the trimmed copy was then made with `head -c 1048576` and its digest `9164745f…` matches wave 1's.`
- Host reachability observed 2026-10-30: `www.st.cs.uni-saarland.de`, `www.xunitpatterns.com` and
  `betterbench.stanford.edu` answered HTTP 000 from this seat; all three were read through Wayback snapshots.
  `web.archive.org` serves those snapshots gzip-encoded, so the recorded digests are of the **decoded** bytes.
- Disk: `/fast` had 450 G available (45 % used) at fetch time; the disk-guard status was checked before the pass.
  No ENOSPC.
