ATTACKS: round-25 access-time caveat appended to corpus/evidence/round24-sources/gate.md (claims to close kaika W3 F10)

Seat KengakuR25.CorrF10 · axis calibration · tip 8ea41f9ed (HEAD=8ea41f9, worktree = tip for this file) · fetches 2026-10-20 21:49–21:56 -03 (5–12 min after commit 21:44:48 -03). No LSP for .md/HTML evidence; git/grep/curl used as literal checks.

## Survives
1. Append-only. `git diff --numstat 6180e4f 8ea41f9ed -- corpus/evidence/round24-sources/gate.md` → `8 0`; `diff -U0 … | grep -cE '^-[^-]'` → `0`; one hunk `@@ -103,3 +103,11 @@` at EOF; only commit in range is 8ea41f9. History of the whole file is also addition-only: 94da19e creates it, e21f9ea `1 0` (S026 row inserted mid-table at :34), 8ea41f9 `8 0`.
2. The cited evidence matches. `.ufo/waves/round-25/build/RevF10.md` (tracked: `git ls-tree 8ea41f9ed` lists it) records S005 `e6f58c18`/`1da6fa12` two seconds apart, S006 `faec654e`, scale.com `c7e50638`, with byte counts equal to the receipts. That is what gate.md:111-112 cites. An independent check matches too: two of my six scale.com fetches returned RevF10's `c7e50638` exactly.
3. The core claim reproduces on the same day with curl→sha256sum/wc -c, the gate's own method (gate.md:5). S005: 5 fetches, 5 different hashes, all 9,843 B. S006: 4 fetches, 4 different hashes, all 9,852 B. scale.com: 6 fetches, all 128,773 B. Neither S023's `ee510e84` nor S026's `171087c5` came back (receipts gate.md:31, :34; same URL, same day, same size, different hash).
4. The prescribed check (quote and location) works for all four listed rows:
   - S005: the reader text has "We found that 59.4% of the 138 problems contained material issues…" verbatim under `## Too narrow and too wide tests` (gate.md:13).
   - S006: both quotes are verbatim, the first in the opening section before `## Methodology` and the second in `## Discussion` (gate.md:14).
   - S023/S026: the raw scale bytes have `grep -c "trained on"` → 2 and `grep -c copyleft` → 2.
5. It closes F10 as literally filed. kaika-w3/kengaku-review.md:141 asks to "Add an access-time capture caveat to corpus/evidence/round24-sources/gate.md" for S005, S006 and S023. gate.md:107-113 is that caveat and also covers S026. It is logged in corpus/lessons/round-25.md:57 and LOG.md:290.

## Breaks
B1 (Medium). The four-row list was already wrong on the day it landed. I fetched all 24 web receipts twice each: 14/24 reproduce and 10/24 do not. Six of the ten are not covered by the caveat, and each gave the same result on both fetches, so this is drift since the receipt was taken, not fetch-to-fetch noise:
   - S004 `21d842db`/42,283 → `d0364652`/42,869 (gate.md:12)
   - S008 `e407cba7`/47,021 → `e4daad78`/47,607 (:16)
   - S014 `c5135c54`/682,272 → `6302ddc4`/682,272 (:22)
   - S020 `48056dd2`/53,747 → `60d50fa9`/54,333 (:28)
   - S021 `e8b0b348`/47,041 → `63ae0a12`/47,629 (:29)
   - S022 `89e8779c`/45,596 → `caf551b1`/46,182 (:30)
   gate.md:112 limits "a hash mismatch alone is not a finding" to "these rows". A re-verifier following the caveat would therefore report six mismatches of the same kind as findings. W3's baseline of "17 of 20 reproduce" (review:87) is now 14/20. The lane's own round-25 gate (round25-sources/gate.md:4-6) already applies the rule to every row; this caveat does not.
   [INFERENCE] The arXiv cause is a template change: all five /abs/ pages grew by 586–588 B, and their current bytes include `<div id="ds-announcement">` plus design-system `banner.js` (/tmp copy s004.html:47-48). The /html/ pages all reproduce. For S004, `curl -I` shows `age: 33400` at 00:53:56Z, so the cached copy was about 9 h old and already in place before the commit.
B2 (Low-Med). The S005 and S006 hashes are hashes of a Cloudflare challenge page, not of the articles:
   - The fetched bytes contain `grep -c 59.4` → 0 (S005) and `30%`/`retract` → 0/0 (S006).
   - They contain `cf_chl_opt` 7 times and `challenge-platform` 3 times.
   - The challenge pages are exactly 9,843 and 9,852 B, the receipt byte counts.
   The quotes came from the reader and the hashes from curl (gate.md:5), so a matching hash would not support the quote either. gate.md:109-110 ("captures of the bytes fetched…", "dynamic or challenge-served") never says which rows are challenge pages, or that those hashes cover no source text.
B3 (Low). "Same-day re-fetches return the same byte count but a different hash" (gate.md:110) is stated as always true, and it is not. scale.com cycles through a small set of versions: `c7e50638`×2, `4e840b68`×2, and `302ba92a`×2 back-to-back. The difference is in the Next.js page data (`10:I[272…` vs `f:I[5070…`). A re-fetch can therefore match an earlier hash, so "may differ" is the accurate wording. "Same byte count" also does not identify harmless drift, because the arXiv drift changes the length.
B4 (Low). The caveat cites "reviewer RevF10" without a file path; the file is `.ufo/waves/round-25/build/RevF10.md`. F10's own text gives the S006 receipt as `fba4c054…` (review:141), but the receipt is `fba4c005…` (gate.md:14, review:69). The caveat does not repeat that typo, so this is not a lane defect.

## Residual risk / gaps
- The arXiv and metr drift was checked from this host only. The arXiv cause is inferred from its current bytes because the 2026-10-19 bytes were not kept. The metr (S014) change is the same length and its cause was not found.
- The S004/S008/S014/S020–S022 quotes were not re-verified by quote and location (outside this item). S020–S022 are queued and unused.
- Scratch: /tmp/k25w2-CorrF10/{s005_*,s006_*,scale_*,s004,s008}.html, refetch.json.

VERDICT: PARTIAL — Survives: the caveat is append-only (`8 0`, EOF), it matches RevF10, the four listed rows check out by quote and location, and it closes F10 as literally filed. Breaks: six more receipts (S004, S008, S014, S020–S022) did not reproduce on the day it landed, and it does not say that the S005/S006 hashes cover a Cloudflare challenge page.
Installs: none (curl, git and python3 already on the host).
