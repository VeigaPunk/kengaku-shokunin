# F41ReopenRows — live re-open of S122/S123/S124 (kengaku r41 wave 2, falsify)

Date 2026-10-26; lane kengaku-shokunin at master tip 3d0058fbde484c9d6c23fd997d9ee09a0663bcdb.
Item: re-open the three round-41 sources live (fetch both pinned raw URLs and `cmp` with the captures; open TB2.1 PR
#245 via `gh api`; check quote verbatim-at-location ≤25 words, anchor digest vs capture, tier/status/opened/recheck/used-by,
and pr245-body.md vs the live PR body); run the census on the lane. Per-row verdict at the end.

Method and safety: fetches ran inside the mandated envelope `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin
/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent` (bwrap present; envelope
active). Scratch was `/fast/scratch/hyaku/kengaku-r41/F41ReopenRows` (TMPDIR pointed there; deleted at the end, guard
checked). The lane itself was never written: census/validate/overdue are read-only (`sources-census.sh` writes stdout
or `--out` only); `sha256sum -c` ran in place in the capture dir. No lane file edited, no git/jj mutation, no installs
(none needed: bwrap/curl/gh present). Receipts: `.ufo/waves/round-41/falsify/F41ReopenRows/` (fetched pins, live body,
meta.json, prsize.json, receipt.txt).

## S122 — TB2.0 constraints-scheduling grader (SOURCES.md:137)

- Freshness: `curl` at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py`
  → `cmp` with `corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py` rc=0 (byte-identical today).
- Anchor digest: `sha256` = `1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1` — equal on fetched file,
  capture file, and SHA256SUMS line. Full manifest `(cd corpus/evidence/round41/tb2-constraints-scheduling &&
  sha256sum -c SHA256SUMS)` → 10× OK, rc=0.
- Quote: `"assert not any(_overlap(s, e, cal) for cal in (A, B, C))"` — verbatim at the stated `:143` in fetch and
  capture (`awk 'NR==143'` identical); 11 whitespace-tokens as claimed, ≤25. Ancillary anchor cites hold: file is 209
  lines (`wc -l`), `:135` is `s = _dt(r"DTSTART:(\d{8}T\d{6}Z)", c)` as the FIRST-DTSTART claim needs.
- Cells: kind `code`, tier `A` (pinned maintainer file — same shape as S119/S120), status `mined`, opened `2026-10-26`
  (not future), recheck `180d` (= entry's `recheck: 180d`), used-by `corpus/knowledge/tb2-constraints-scheduling-grader.md`
  (exists; the entry's `source:` block opens with `source: S122 — <same URL>`, reciprocal).

**S122 verdict: holds.** No defect.

## S123 — TB2.0 constraints-scheduling instruction (SOURCES.md:138)

- Freshness: pinned `.../constraints-scheduling/instruction.md` fetched under the envelope → `cmp` with capture rc=0.
- Anchor digest: `342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6` — fetched = capture = SHA256SUMS.
- Quote: `"Any modification will cause the tests to fail."` — verbatim substring of `instruction.md:18` ("repo inputs.
  Any modification will cause the tests to fail."); 8 words as claimed, ≤25; anchor's `:1-30` (30 lines) and `:15-18`
  (the read-only bullet) both check out.
- Cells: kind `docs`, tier `A`, mined, `2026-10-26`, `180d`, used-by same entry (`source: S123 — <same URL>` present).

**S123 verdict: holds.** No defect.

## S124 — TB2.1 PR #245 (SOURCES.md:139)

Live `gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` (rc=0), today:

| field | row/capture claim | live | match |
|---|---|---|---|
| state | closed / "closed unmerged at access" | `closed` | ✓ |
| merged | false | `false` (`merged_at` null) | ✓ |
| opened | 2026-10-05 | `created_at=2026-10-05T02:41:13Z` | ✓ |
| closed_at | 2026-10-08T19:02:36Z | same | ✓ |
| comments | 0 | `comments=0 review_comments=0 draft=false` | ✓ |
| author/base | camirian, main `7131e437…` | same | ✓ |
| title | "Bind constraints-scheduling checks to the requested event" | same string | ✓ |

- Capture fidelity: `pr245-body.md` sha256 `8f3b04c34edeb558d8b1e45ac49462bf28fdaa3392cec03bc6ee54d30253410f` = anchor
  digest ✓; body after the 3 `#` annotation lines is byte-identical to the live body (`cmp` rc=0; both 4514 B,
  `ce3735e8…`). The capture's header metadata all re-confirmed live. Bonus: the entry's §Prior art numbers (+253/−39,
  4 files, 1 commit) equal the live PR object (`additions=253 deletions=39 changed_files=4 commits=1`).
- Cells: kind `docs`, tier `B` (community PR — S121 precedent), mined, `2026-10-26`, `180d`, used-by the entry, which
  cites back via `source-note: S124 … (tier B, cited by §Prior art only)` — the same convention the db-wal entry uses
  for S121. Census-legal (validate exit 0).
- Quote: `"the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar"` — 14 words
  ✓, verbatim in the live PR body ✓ — **but not at the stated location.** The anchor says "PR body §Proposed PR
  description"; the exact sentence is at `pr245-body.md:11`, the unheaded preamble paragraph beginning
  "**Current upstream state checked 2026-10-04:**". `§Proposed PR description` (line 17) contains only the paraphrase
  "…the constraint and earliest-slot checks read the first DTSTART from the full calendar" (line 19). A reader who
  jumps to the named section finds different wording, not the quote. The entry's own §Prior art quotes the sentence
  without a section claim, and is correct.

**S124 verdict: breaks on one sub-check** — quote verbatim-in-body yes, at-stated-location no (F1 below). Everything
else (tier/status/opened/recheck/used-by, digest, live state, capture fidelity) holds.

## Census on the lane (read-only)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` with `--root /home/vgpnk/Projects/shokunin kengaku`:

- `validate` → exit 0; only `W04 duplicate-url-across-scopes` warnings (pre-existing rows S040…S100; **none** involve
  S122/S123/S124); no E-codes, so all 11-cell rows parse, ids/URLs unique per scope, statuses legal, dates past,
  rechecks valid, no community-at-A, used-by paths exist.
- `census` → `rows=117 tier.A=99 tier.B=16 tier.C=2 status.mined=101 status.queued=8 status.rejected=8`, `FLEET.missing=0`,
  exit 0.
- `overdue` → exit 0, nothing overdue (cadence lines informational only; S122/S123/S124 listed `180d` opened
  2026-10-26, not due).

## Findings

- **F1 (minor, S124 anchor location).** Quote's stated section `§Proposed PR description` is wrong; the sentence lives
  in the preamble paragraph (`pr245-body.md:11`), paraphrase-only at `:19`. Fix is an L1 anchor edit (report-only
  here; lane untouched). Severity low: quote, digest, capture and live state are all correct.
- **F2 (observation, no defect).** The PR body's internal "## Proposed title" says "…requested **VEVENT**" while the
  actual PR title (and the row) say "…requested **event**". The row tracks the live title, so it is right; noted so
  nobody "corrects" the row to the body's proposed title.
- **F3 (observation, no defect).** The PR body self-describes as a local draft ("do not submit without owner
  authorization … No upstream issue, PR, or comment has been created") while being the body of a real, now-closed PR
  #245. The capture is faithful to upstream; the contradiction is upstream's, and the row's "closed unmerged" reading
  is the honest one.

What holds: both pinned captures byte-fresh at the pin; all three anchor digests equal the captures (and the full
manifest verifies); S122/S123 quotes verbatim at cited lines with correct word counts; S124's live PR state, title,
author, base, counts and body match the frozen capture exactly; tier/status/opened/recheck/used-by correct on all
three rows with reciprocal citations; census clean. What breaks: S124's quote-location claim only.

Verification gaps: per item scope I did not re-run `plans/constraints_probe.py --lane .` (entry falsifier (b) — other
seats' territory) and did not re-open S119–S121. `gh` had network+auth (both calls rc=0); PR state re-checked at
16:18 -03 today and matches the frozen access claims.

Receipts (this dir): `F41ReopenRows/{test_outputs.py, instruction.md, live-245-body.txt, meta.json, prsize.json,
receipt.txt}` — fetched pins and live PR payloads as evidence.

VERDICT: rows-ok-2/3
