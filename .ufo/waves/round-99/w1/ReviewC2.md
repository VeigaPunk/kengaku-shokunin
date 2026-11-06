# ReviewC2 — R99-C2 freshness review (round 99)

Reviewer: ReviewC2 (leaf). Method: isolated `git clone --shared` fixture detached at T
f72a8bc710b12473b5c768004e2581f980d924f4, BASE 2233a66195e3d3d85856248fb8f66c1d8127cede.
Counter re-run at T plus a fully independent re-derivation (own parser, own gate runs on own
fixtures, own census) — not a re-import of the counter's code. No LSP server answered for this
repo in this session; all evidence is textual (gate source, PROVENANCE bytes, SOURCES rows,
capture contents) plus runtime gate execution; grep is not offered as semantic proof anywhere
below.

## Verdict list (id, verdict, evidence)

| id | item | verdict | evidence (lane-relative) |
|---|---|---|---|
| V1 | Counter at T | pass — `REV f72a8bc7…`, K1–K7 all pass, `pop=12 cleared=12 still=0 outside_rows=313 …`, `PREDICATE R99-C2 pass`, exit 0; matches the frozen-predicate TARGET line byte for byte | `.ufo/waves/round-99/w1/ReviewC2/counter-run-T.txt` |
| V2 | Population rule re-derived at BASE (independent) | pass — own derivation from BASE gate output + BASE evidence digests yields exactly the 12 POP rows, tokens and lexicographically-first captures; equals frozen `POP` and the P1 receipt `c2-pop.txt` (12 rows) | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V3 | Semantic rightness of each binding (capture IS the document the row describes) | pass — all 12: row-stated sha256 == capture blob sha == PROVENANCE sha column; content matches the row's own pinned quotes (S285 line 1, S293 line 1, S306 :1562, S220 :14, S180 :87 FAQ + 4574 B, S225 :7/:13 pointers, S173–S177 adoc titles and pinned line ranges, S270 = the 14-byte `404: Not Found` body the row explicitly anchors) | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V4 | K7 census covers every BASE row outside the population | pass — 313 BASE rows outside POP; defects AND verbose notes (both directions) identical BASE vs T for all 313 (`changed=NONE`); `outside_rows=313` matches the claims' frozen TARGET line | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V5 | Can any new PROVENANCE line bind anything other than its named row? | no — gate `evidence_index` keys `prov_sid` on `\bS\d{3,}\b` inside `\|`-lines only; the 8 new files contain exactly 12 sid-bearing lines, one per POP row; headers/separators carry no sid; no URL anywhere (K3); the sha-column hex never resolves as a path (no committed file named `<64hex>`, no SHA256SUMS lists a bare 64-hex name — checked); old provenance files byte-identical BASE==T and bound no POP row at BASE (rows were `anchor-unbound`) | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V6 | S270 (404 body, 3 byte-identical twins) | correct — the row itself anchors the HTTP 404 response body ("response-body sha256 d5558cd…", "no upstream source-content anchor exists", claim scope = reachability), so binding the 14-byte 404 body is semantically right, not a mis-bind; lexicographic-first twin is the row's own round82 file; the two twin 404 bodies (`candidate_run-tests.sh`, `candidate_tests_run-tests.sh`) are cited by no row carrying that token (only S270 cites d5558cd…), and S264 (same URL, REJECTED, superseded) stays outside POP with unchanged output | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V7 | S180/S225 byte-identical twin captures | correct — S180 first-of-2 = round79/sources/tb2-readme.md (other twin round82/fetch/candidate_README.md is uncited); S225 first-of-2 = round61 copy (twin is S227's round62 reopen dir); both ties resolve to the row's own round directory, so each line lands in the right round dir per K4 | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V8 | Frozen instruments | pass — gate bytes sha256 11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2 at BASE == T (gate unchanged); counter 8b470d7a… and builder f6606371… at T match the `frozen-instruments` rows in `plans/round-99-claims.md:30-31` | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |
| V9 | No collateral change | pass — BASE..T diff under `corpus/`: only the 8 new PROVENANCE.md files + C1's round99 evidence; `corpus/SOURCES.md` gains only S334–S341 (C1's rows, outside the C2 census by the claims' separability note); the 12 POP row lines byte-identical BASE==T (K6 re-verified independently); old provenance byte-identical | `.ufo/waves/round-99/w1/ReviewC2/independent-checks.txt` |

## Defects

None in scope. No HIGH/MEDIUM/LOW defect found in `plans/round99_c2_rowscoped_bind.py`,
`plans/round99_provenance_build.py`, the eight `corpus/evidence/round<N>/PROVENANCE.md` files,
or the gate's `evidence_index`/`bind_row` interaction with them.

## Observations (route to round 100; not repaired in round)

- O1 (info) — `corpus/evidence/round82/fetch/candidate_pyproject.toml` is a 14-byte
  `404: Not Found` body; the filename suggests package metadata but holds the error body. The
  name predates round 99 (committed in round82, untouched by C2) and the S270 row documents the
  404 explicitly, so the binding is honest; only the filename is misleading to a casual reader.
- O2 (info) — the population's lexicographic-first tie-break is safe today only because all
  three twin cases (S180, S225, S270) sort the row's own round copy first. A future byte-equal
  twin sorting earlier would bind the twin; the frozen rule accepts that (byte-equality makes it
  digest-equivalent), but a round-100 rule revision could prefer the row's own round directory.
- O3 (info) — K7 censuses BASE rows only; the eight new rows S334–S341 at T are outside its
  scope by the claims' explicit separability note (C1 owns them). Correct as frozen; noted so
  the census is not oversold.

## Residual risk and verification gaps

- No upstream network re-fetch was performed: capture digests are verified against the rows'
  own committed sha256 claims and content quotes, not re-downloaded (C2's claim is freshness of
  binding, not re-fetch; out of scope).
- The 33 remaining gate defects at T are the pre-existing baseline (census-verified unchanged,
  none touches POP); whether they are individually correct classifications is not a C2 question.
- Gate `dir_entries`/`manifest` views of SHA256SUMS were not re-verified for equality with file
  bytes beyond the committed-file view the bindings rely on; the bindings use the committed-file
  view (`file_digest`) only, and no manifest lists a bare 64-hex name (checked), so the sha
  column cannot sneak in through a manifest.
- No subagents were used (leaf seat); receipts are text-only, scratch
  `/fast/scratch/hyaku/kengaku-r99/ReviewC2` removed after receipt copy.
