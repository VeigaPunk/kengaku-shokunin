ATTACKS: S030 (Hanley & Lippman-Hand 1983) — re-fetched the gate URL, re-verified the quote verbatim + page location, the anchor cell, tier/scope honesty, sha256, and the citation against a second copy (the author's typeset scan) and Crossref.

Method: `curl` GET 2026-10-20 21:49 -03 into /tmp/k25w2-ReopenS030; `pdftotext` -f/-l, -raw, -layout (poppler 26.08.0); tesseract 5.5.3 OCR of the author's 3-page scan; Crossref API. Tip cells read via `git show 8ea41f9ed:…` (live-tree SOURCES.md/gate.md carry another seat's uncommitted S038 append; the S030 rows are unchanged at the tip).

Fetch + sha256 (gate.md:16; SOURCES.md:52) — AGREE
- HTTP/2 200, 15,770 B, application/pdf, 4 pp, Last-Modified 2023-07-17 23:23:47 GMT, Server Apache.
- `sha256sum` = e3150aec…fd746d79, byte-identical to the gate cell; the object is static and predates the round, so the "dynamic page may re-hash" caveat never applies here.

Quote (gate.md:16; knowledge:48) — AGREE
- 19 words, exact after line-wrap normalization: "…we can be 95% confident that the chance of this event is at most three in n (ie, 3/n)." Characters match, including "(ie, 3/n)"; the gate omits only the sentence-final period.
- OCR of the author's typeset scan yields the same sentence (s2.txt:127–129: "we are concerned, we can be 95% / confident that the chance of this / event is at most three in » (ie, 3/%)"), so the 2001 Word re-key did not manufacture it.

Location (gate.md:16; SOURCES.md:52; knowledge:1,:48) — DISAGREE
- PDF p.1 ends at Example 2; `pdftotext -f 1 -l 1` (48 lines) has neither the heading nor the sentence (only the intro's unnamed "and simple rule…", p1.txt:23). Heading is p2raw.txt:24, the sentence starts :32, footer "page 2" (p2.txt:48) — section ¶2 of the 4-page copy.
- The author's scan pins the printed page: footers 1743/1744/1745 (s1.txt:156, s2.txt:69, s3.txt:180); section + sentence sit on scan p.2 = printed p.1744.
- Correct cell: "p.2 of 4 (author-hosted copy), section Making Inferences: The Rule of Three, ¶2; printed p.1744". Slip origin: SrcHanleyRuleOfThree.md:29 ("p.1 of 4 … line 63 of page-1 extract" — no page-1 extract can contain it; raw page-2 line 32, full-doc raw line 107).

Anchor cell otherwise — AGREE
- Author-hosted PDF and section are named; "JAMA typeset page not opened (HTTP 403)" is true: doi.org 302 → jama.jamanetwork.com/article.aspx?doi=… → HTTP 403.
- Copy is honestly described: `pdfinfo` Author "James Hanley", Producer "Acrobat PDFWriter 4.05 for Power Macintosh", created 2001 — a re-key, not the typeset scan (typos "tor", "dyaraphism", "on uses", "0 05 1/n"); the gate note's "author copies named in their anchor cells" holds.
- Independent identity: scan byline "James A. Hanley, PhD, Abby Lippman-Hand, PhD", cover "Reprinted from … April 1, 1983, Volume 249"; scan sha256 229925fb… matches the scribe's hash; Crossref DOI returns the title + subtitle "Interpreting Zero Numerators", JAMA 249(13), p.1743, 1983-04-01.

Tier / scope / teaches — AGREE (one caveat)
- Tier A is honest for a disclosed author reproduction of the original paper; scope "the 95% upper limit … (rule of three)" is exactly the quoted sentence.
- teaches numbers re-derived: 3/10 = 0.300; one-sided exact 0.05^(1/10) = 0.258866 (the paper's "26% if n=10"); the knowledge entry's two-sided CP 1 − 0.025^0.1 = 0.308497 (= 1 − 0.691503) — "near 30%" holds for the rule and the two-sided exact.
- Caveat: A is for the paper's statement, not the re-key's every character; a stricter reading would tier the re-key B while keeping the quote.

Row / validator — AGREE
- NF=13; kind, status, opened, 180d recheck and used-by path all valid. `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0.
- E01–E12 never checks quote/location (QUALITY.md:15 "exact anchor"; :31–33 Q3; :75–77 Q10), so the page slip is invisible to the machine gate and only this second seat catches it.

Installs: none.

VERDICT: PARTIAL — quote verbatim, sha256 byte-identical, citation/disclosure/403/tier/scope survive; the location cell breaks (quote is p.2 of 4 = printed p.1744, not p.1) in gate.md:16, SOURCES.md:52 and knowledge :1,:48.
