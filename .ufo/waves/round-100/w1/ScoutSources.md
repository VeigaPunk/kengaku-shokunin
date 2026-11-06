# ScoutSources — R100 source-freshness and coverage audit (wave w1, lane kengaku-shokunin)

Seat: ScoutSources. Scope: re-open the 8 new SOURCES rows S342–S349 live at their pinned URLs, re-open the
9 R100-C2 population URLs live, run the census, and judge the S342/S348/S349 admission decisions.
Nothing in the lane was written except this report and `.ufo/waves/round-100/w1/ScoutSources/`.

Measured tip T = `dbe0cefa607cf57f7f58346fce64bcc127144ca0`; BASE `7846037679de77d050141c785996471801e5a19a`;
F `54df15ca1f9b689b25c6ffc3b2fccd1253bdd6c2`; REF = F~1 = `5220b71d337a3703eaba4cdf6b85eaf343497ae0`.
All work in an isolated `git clone --shared` checkout under `/fast/scratch/hyaku/kengaku-r100/ScoutSources/`,
detached at T; scratch removed after receipts were copied. No production edit, no commit, no push, no
`git`/`jj` mutation in the lane or any sibling repo.

## Verdict list

- S342 — agree (admit) — live GET HTTP 200 / 10336 B / sha256 `978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a` equals both the row cell and the committed capture, and the cited quote sits on `tests/test_outputs.py:66` with declared 5 words = `len(quote.split())` — `.ufo/waves/round-100/w1/ScoutSources/live-S342-S349.txt`
- S343 — agree (admit) — live HTTP 200 / 629 B / sha256 `48abbda713ace5cee00dd28c7398959f28280062350eb88206a6697a28c72790` = row = capture; quote `-w pytest-json-ctrf==0.3.5` on `tests/test.sh:22`, 2 declared = 2 computed words — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- S344 — agree (admit) — live HTTP 200 / 11635 B / sha256 `90861b79c4bd7733909616ffa058151847eb67a4d43395a964c449cf7e24c4fb` = row = capture; quote on `solution/solve.sh:62`, 5 declared = 5 computed words — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- S345 — agree (admit) — live HTTP 200 / 1055 B / sha256 `b21cf2af1891922732327bf586d14b250d36d96de7867479c15bd1c58ef0db58` = row = capture; quote `add a final row with the filename 'total'` on `instruction.md:12`, 8 = 8 words — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- S346 — agree (admit) — live HTTP 200 / 623 B / sha256 `2ea485aead008998d7a551e8c80b6bd354a74cbffc310a1f4b88d0b7c53d23ff` = row = capture; quote `RUN uv run /root/randomize_filenames.py` on `environment/Dockerfile:14`, 4 = 4 words — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- S347 — agree (admit) — live HTTP 200 / 1392 B / sha256 `09828ee53e8f2165a9888c5de84e40fcb057bb889d93bfc90d9aeca8c4e23be4` = row = capture; quote `random_base = secrets.token_urlsafe(9)` on `environment/randomize_filenames.py:14`, 3 = 3 words — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- S348 — agree (reject) — live HTTP 200 / 985 B / sha256 `163ee252895c05d36ca37137dba4d6c24b46be28d56ce84ef8bb35bb5b894bda` = row = capture and the row is byte-faithful, but the manifest only names a prebuilt image the replay never pulls and a verifier timeout, so it carries no byte the grader or the replay reads (same shape as round-99's rejected S340) — `corpus/SOURCES.md:364`
- S349 — agree (reject) — live HTTP 200 / 1992 B / sha256 `32438e7780d235dd609f4740e36512c4cd2f34ef26842ea52c5bbde46fcf5e86` = row = capture, but the README's line-40 claim "Correct summation in the final \"total\" row" is contradicted by the grader bytes: `test_summary_csv_content` compares each row against hard-coded `expected_data` and never sums, never checks row position, so 11 identical `total` rows pass (C03) — `corpus/SOURCES.md:365`
- S342-S349 (8 rows) — agree — the row set added between BASE and T is exactly {S342..S349}, exactly 8 rows, no other row's text changed, and no S34x row carries an anchor-digest DEFECT or a live line-gate row — `.ufo/waves/round-100/w1/ScoutSources/gates-and-counters.txt`
- C2POP-S210 — agree — live HTTP 200 / 2600 B / sha256 `02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed` = the `c2-pop.txt` token = the row's anchor token = the committed copy `corpus/evidence/round52/graders/distribution-search/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S211 — agree — live HTTP 200 / 11386 B / sha256 `19daaee18d534f36679854b0ba5727290df389ee023ebb67846cb89579d38bbe` = token = row token = committed copy `corpus/evidence/round58/tb2-distribution-search/solution/solve.sh` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S219 — agree — live HTTP 200 / 5878 B / sha256 `90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d` = token = row token = committed copy `corpus/evidence/round52/graders/openssl-selfsigned-cert/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S228 — agree — live HTTP 200 / 3177 B / sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` = token = row token = committed copy `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S232 — agree — live HTTP 200 / 2166 B / sha256 `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` = token = row token = committed copy `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S279 — agree — live HTTP 200 / 3034 B / sha256 `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149` = token = row token = committed copy `corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S281 — agree — live HTTP 200 / 2330 B / sha256 `0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977` = token = row token = committed copy `corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S298 — agree — live HTTP 200 / 1262 B / sha256 `7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a` = token = row token = committed copy `corpus/evidence/round94/graders/write-compressor/tests/original-decomp.c` (the file the URL itself names, not the sibling `environment/decomp.c`) — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- C2POP-S300 — agree — live HTTP 200 / 24841 B / sha256 `01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409` = token = row token = committed copy `corpus/evidence/round94/graders/write-compressor/solution/solve.sh` — `.ufo/waves/round-100/w1/ScoutSources/live-c2pop.txt`
- R100-C1 — agree (pass) — independent rerun of `plans/round100_c1_replay.py` at T prints `LEGS L1..L13=pass` and `TARGET executed_rows=44 … cells=crypto-credential:5,file-artifact:35 set_equals_base_plus_member=1 … cases=15 legs=120 mismatches=0 new_rows=8 new_rows_flagged=0 new_rows_line_live=0 defects=0` then `PREDICATE R100-C1 pass` — `.ufo/waves/round-100/w1/ScoutSources/gates-and-counters.txt`
- R100-C2 — agree (pass) — independent rerun of `plans/round100_c2_rowcensus_bind.py` at T prints `GATE defects base=33 ref=32 rev=23`, `LEGS K1..K10=pass`, `TARGET pop=9 cleared=9 still=0 … base_rows=333 base_rows_not_equal=0 new_provenance_files=3 url_channel_files=0 not_three_cells=0 ids_not_in_pop=0 live_rows=9 rows_changed=0 captures_changed=0`, then `PREDICATE R100-C2 pass` — `.ufo/waves/round-100/w1/ScoutSources/gates-and-counters.txt`
- GATE-digest — agree — I ran the frozen gate myself at BASE (rows=333 tokens=217 defects=33), at REF (defects=32, the one fewer being S295's `capture-unanchored` re-bound by C1's P0 capture) and at T (rows=341 tokens=225 defects=23), i.e. the 9 population findings are exactly the difference — `.ufo/waves/round-100/w1/ScoutSources/gates-and-counters.txt`
- GATE-line — agree — at T the line gate reports `rows=341 cited=147 captured=134 uncaptured=13 defective=10 repaired=10 live=0 cells=0`, and a direct per-row evaluation of S342–S349 returns `(cited, capture, [])` for all 8 — `.ufo/waves/round-100/w1/ScoutSources/quote-line-wordcount.txt`
- CENSUS — agree — `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exits 0 with zero E-codes and `kengaku ok corpus/SOURCES.md` (32 W04 "same URL across scopes" warnings only, one of them the new S342 vs the round-99 S295 pair, the same prose-scope pattern as the pre-existing S334/S181 pair) — `.ufo/waves/round-100/w1/ScoutSources/census-validate.txt`
- COVERAGE-C03 — agree — the grader has no uniqueness/coverage/position rule for summary rows: `len(df)==len(expected_data)` plus a per-row lookup by file hash or the literal `"total"`, so 11 identical `total` rows satisfy it — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:177`
- COVERAGE-C04 — agree — ten copies of one invoice row plus the total row give 11 rows whose identifiers all resolve into `expected_data`, so the duplicate passes — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:181`
- COVERAGE-C07 — agree — `test_original_documents_dir_empty` iterates `documents_dir.iterdir()` and keeps only `f.is_file()`, so copies left in `/app/documents/keep/` are top-level-invisible and the leg passes — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:218`
- COVERAGE-C08 — agree — `actual_file_hashes` is a `set` of sha512 digests, so a second copy of an invoice under a new name collapses into the same element and the set still equals `expected_original_documents` — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:57`
- COVERAGE-C11/C12 — agree — the band is `abs(float(row["total_amount"]) - expected["total_amount"]) < 0.01`, strict, so +0.009 passes and +0.01 fails; I reproduced the strictness independently with pandas 2.3.2 — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:208`
- COVERAGE-C14/C15 — agree — the structure leg compares `csv.DictReader.fieldnames` to `["filename","total_amount","vat_amount"]` (order-sensitive, and a UTF-8 BOM makes the first fieldname `\ufefffilename`), while the content leg reads columns by name through `pandas.read_csv` (order- and BOM-insensitive); I reproduced both halves independently with csv + pandas 2.3.2 — `corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py:114`
- POSITIVE-CONTROL — agree — the committed `corpus/evidence/round100/fdp-solution/` placement.tsv (17 rows, 10 invoices + 7 other) and summary.csv hash-verify against their SHA256SUMS, every placement digest equals the sha256 of the captured document it names, and all 10 summary rows plus the total row equal the grader's hard-coded `expected_data` exactly (`total` 81315.2 / 5402.48) — `.ufo/waves/round-100/w1/ScoutSources/positive-control-and-ledger.txt`
- FREEZE — agree — all 16 frozen-instrument digests in the claims table match the bytes at T, none of them changed between F and T, the candidate-bytes table matches at T byte-for-byte, and the F..T file set is exactly the 6 candidate files plus `corpus/evidence/round100/fdp-probe.txt` — `.ufo/waves/round-100/w1/ScoutSources/freeze-integrity.txt`
- FALSIFY-M1/M2/M5 — agree (the C1 counter is falsifiable) — tampering one digest nibble in S342's row fails L12, moving S349's cited line fails L13, and adding a 9th new row fails L10; every mutation ends at `PREDICATE R100-C1 fail` — `.ufo/waves/round-100/w1/ScoutSources/mutation-falsification.txt`
- FALSIFY-M3/M4 — agree (the C2 counter is falsifiable) — a 4th cell on the S210 provenance row fails K3 and K10, and deleting the unrelated BASE row S001 fails K8; both end at `PREDICATE R100-C2 fail` — `.ufo/waves/round-100/w1/ScoutSources/mutation-falsification.txt`
- LEDGER — agree — recomputed from `plans/grader-population-ledger.json` myself: BASE 43/88 executed with crypto-credential 4/12 and file-artifact 34/76; T 44/88 with 5/12 and 35/76; the only changed member is `financial-document-processor` and the executed set is exactly BASE ∪ {that member}; `SKILL.md` cells read "executed 35 of 76" and "executed 5 of 12" — `plans/grader-population-ledger.json`
- PREFREEZE — agree — I ran `plans/round100_prefreeze_check.py` (BASE vs candidate T) myself: `PREFREEZE new=0 gone=0 line_base=0 line_cand=0 reg_base=12 reg_cand=12` / `VERDICT clean` — `.ufo/waves/round-100/w1/ScoutSources/gates-and-counters.txt`

No disagreement was found with any frozen row, gate decision, counter, or census reading. Nothing is routed to
round 101 from this seat: no defect, no gap, and no ambiguity surfaced.

## How each item was checked

### 1. S342–S349 re-opened live

One `curl -sS -L` GET per row at the row's pinned URL (no cache-busting), body hashed in memory; the row's
own `HTTP <n>, <n> B, sha256 <64hex>` cell parsed out of `corpus/SOURCES.md` at T and compared; the committed
capture under `corpus/evidence/round100/tb2-financial-document-processor/` (flat, 8 files) hashed independently.
All 8 rows: HTTP 200, byte length equal, sha256 equal to **both** the row cell and the capture, and the
capture's own `SHA256SUMS` verifies (`sha256sum -c` all OK).

Each row's quote was located on its cited line in **both** the live bytes and the capture, and the declared
word count was checked against `len(quote.split())`: all 8 equal (5, 2, 5, 8, 4, 3, 3, 7). Receipts:
`live-S342-S349.txt`, `quote-line-wordcount.txt`.

The rows' `teaches` cells were checked against the grader bytes rather than taken on trust; every mechanism
claim in S342 (`sha512` into sets → C08; `.json` suffix excluded → C05; extra file enters the set → C06; no
uniqueness/coverage/position rule → C03/C04; top-level-only document count → C07; strict `< 0.01` band →
C11/C12; DictReader order/BOM vs pandas by-name → C14/C15) is visible in the captured `test_outputs.py`.

### 2. The 9 C2 population URLs re-opened live

Same procedure against `.ufo/waves/round-100/L1/c2-pop.txt`. All 9: HTTP 200, live sha256 = the pop token =
the token printed in the SOURCES row = the sha256 of the committed copy the pop names. The committed copies
are path-matched to the URL each row names (`…/<task>/<rel>` or `…/tb2-<task>/<rel>`), including S298's
`round94/graders/write-compressor/tests/original-decomp.c` — the URL's own file, not the sibling
`environment/decomp.c` that shares its digest. All three new `PROVENANCE.md` files contain exactly three
cells per row, no URL string, and one line per pop id.

### 3. Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ exit 0, no E-code, `kengaku ok corpus/SOURCES.md`. The 32 warnings are all W04 "same URL across scopes";
the new S342 is one of them (it shares the URL of round-99's rejected S295 but carries a different prose
scope cell) — the identical pattern the lane already carries for S334/S181, and W-codes do not change lane
status. `corpus/SOURCES.md` is byte-identical at T and at the lane tip, so this reading applies to both.
`census` mode: 341 rows, tier A 306 / B 29 / C 6, statuses mined 294 / queued 8 / rejected 39, invalid 0.

### 4. Gate decisions judged

- **S342 admit — agree.** It is the executed scoring predicate of the replayed member; live bytes, capture
  bytes and row cell agree; the cited quote is on the cited line with the declared word count; the row is
  cited by the frozen case table (`plans/round100-cases.json`), which the counter checks by digest.
- **S348 reject — agree.** The manifest is byte-faithful and correctly quoted, but it names
  `docker_image = "alexgshaw/financial-document-processor:20251031"` plus timeouts; the replay never pulls
  that image (the grader side is a pinned venv), so the row carries no byte the grader or the replay reads.
  Same disposition as round-99's S340.
- **S349 reject — agree.** The README's verification list claims "Correct summation in the final \"total\"
  row"; the grader never sums the invoice rows and never checks the total row's position — it compares each
  row against hard-coded `expected_data`, and 11 copies of the total row pass (C03). The row is a derivative
  human summary whose central claim is contradicted by the bytes it points at, so retaining it as `rejected`
  with a flip condition is right.

### 5. Independent falsification (to show the counters can fail)

Five mutations were committed **in my scratch clone only** and the counters re-run at the mutated commit:

| id | mutation | counter | legs that fail | verdict printed |
|---|---|---|---|---|
| M1 | one digest nibble changed in S342's row | C1 | L12 | `PREDICATE R100-C1 fail` |
| M2 | S349 cited line 40 → 41 | C1 | L12, L13 | `PREDICATE R100-C1 fail` |
| M5 | a 9th new row S350 added | C1 | L10, L12 | `PREDICATE R100-C1 fail` |
| M3 | 4th cell on the S210 provenance row | C2 | K3, K10 | `PREDICATE R100-C2 fail` |
| M4 | unrelated BASE row S001 deleted | C2 | K8 | `PREDICATE R100-C2 fail` |

M5 is worth noting: the census alone does **not** catch an extra mined row (it only emits W03 "mined but
unused", exit 0) — C1's L10 is the leg that fails it. M4 is the round-99 M17/F6 lesson re-verified: only the
row-level census K8 catches the deletion of a BASE row that carries no gate output.

## Receipts

`.ufo/waves/round-100/w1/ScoutSources/`

- `live-S342-S349.txt` — per-row live status/bytes/sha256 vs row vs capture; cited-line and word-count check
- `live-S342-S349.json` — same, machine-readable
- `live-c2pop.txt` / `live-c2pop.json` — per-row live fetch vs pop token vs committed copy for the 9 C2 rows
- `quote-line-wordcount.txt` — quote-on-cited-line and word-count evidence per new row
- `gates-and-counters.txt` — digest/line gates at BASE/REF/T, prefreeze check, C1 and C2 counter runs at T
- `positive-control-and-ledger.txt` — SHA256SUMS verification of both capture dirs, placement.tsv vs the
  captured documents, summary.csv vs the grader's `expected_data`, the recomputed ledger class arithmetic,
  and the BASE→T SOURCES row census
- `freeze-integrity.txt` — every frozen-instrument and candidate-bytes digest at T, the F..T unchanged-file
  list, and the F..T changed-path list (candidate table + receipt)
- `mutation-falsification.txt` — the five mutations and their leg-level outcomes
- `census-validate.txt` — the census output as run

## Tools

No pacman transaction was made (host-wide pacman is paused; nothing was installed that way).
`uv 0.13.0` (already present) created the grader venv `G` under scratch with
`uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2 pytest-json-ctrf==0.3.5`
(resolved: pytest 8.4.1, pandas 2.3.2, pytest-json-ctrf 0.3.5, numpy 2.5.4, python 3.13.16, plus
python-dateutil/pytz/tzdata/pygments). Host tools used read-only: `curl 8.23.0`, host `tesseract 5.5.3`
(confirming the positive control's stated host version), `python3` 3.14.8 for scratch analysis, and the
grader venv's python for the pandas/csv reproduction of the C11/C12 and C14/C15 splits. Scratch removed
after the receipts were copied.
