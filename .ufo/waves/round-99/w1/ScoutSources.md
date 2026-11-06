# ScoutSources — round 99 wave 1 (coverage, freshness)

Seat: ScoutSources (source re-opening + census). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Round-99 base `2233a661`, freeze `24a5a555`, candidate/measured T `f72a8bc7`, receipts `23d58036`,
lane tip at time of writing `fc65aa9a`.

Scope executed (no task calls, no production edits, no lane git mutation; all work in
`/fast/scratch/hyaku/kengaku-r99/ScoutSources`, now removed; receipts copied into
`.ufo/waves/round-99/w1/ScoutSources/`):

1. S334–S341 re-opened live at their pinned URLs (raw.githubusercontent.com @ `2fd12b88`,
   gdreiman1/t_bench_bn_dataset @ `62ce2364`): HTTP status, byte size, sha256 vs the SOURCES row
   token and vs the committed capture, and the located quote at the stated line.
2. The dataset's unpinned `main` URL (Dockerfile `BN_URL`) vs the pinned bytes.
3. The 12 C2 population rows' upstream sources re-opened live (the three named — S173 git doc
   @ v2.56.0, S225 WHATWG index, S306 bottle.py — plus the other nine) and compared to the bound
   capture and to the provenance sha256 column.
4. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (read-only).
5. Independent re-runs of the two frozen counters at T and at the lane tip, the anchor-digest
   gate at T and BASE, and two of my own falsification probes of the C1 counter.

## Verdict list

| id | verdict | evidence path |
|---|---|---|
| SS-1 S334 live re-open | agree — HTTP 200, 5892 B, sha256 `364069f8…e455b` = row token = committed capture; quote `assert p_value >= 0.001, (` sits at line 150 (only occurrence) | `.ufo/waves/round-99/w1/ScoutSources/fetch_s334_s341.json` |
| SS-2 S335 live re-open | agree — HTTP 200, 650 B, `ea2adeb7…eb4c3`; quote `-w scipy==1.16.1 \` at line 22 | same |
| SS-3 S336 live re-open | agree — HTTP 200, 3932 B, `813eb810…5cb79`; quote `learned_dag <- hc(samples)` at line 21 | same |
| SS-4 S337 live re-open | agree — HTTP 200, 1256 B, `5f5207ce…94e5`; quote `3) Perform a causal intervention on Y, setting its value to 0.0.` at line 20 | same |
| SS-5 S338 live re-open | agree — HTTP 200, 600 B, `8b0b1056…5e6cc`; quote `RUN curl -fsSL "${BN_URL}" -o bn_sample_10k.csv` at line 20 | same |
| SS-6 S339 live re-open | agree — HTTP 200, 844949 B, `7d4c27ac…3cb04`; quote `"U","Y","R","D","M"` at line 1 | same |
| SS-7 S340 live re-open | agree — HTTP 200, 919 B, `6493f716…7090`; quote `docker_image = "alexgshaw/bn-fit-modify:20251031"` at line 29 | same |
| SS-8 S341 live re-open | agree — HTTP 200, 1994 B, `647d14a7…7919`; quote `Sampled data has 10,000 rows…` at line 38 | same |
| SS-9 dataset unpinned `main` URL vs pinned bytes | agree-and-still-equal — unpinned main is HTTP 200, 844949 B, sha256 `7d4c27ac…3cb04`, byte-identical to the pinned `62ce2364` bytes and to the capture; GitHub API shows `main` is still `62ce2364…`. The S338 hazard (unpinned branch) is real but has not moved | `.ufo/waves/round-99/w1/ScoutSources/fetch2.json` |
| SS-10 S173 upstream re-open | agree — HTTP 200, 11890 B, `39ce8d13…9439` = capture = provenance sha256; cited ranges :26-28 (gitfile), :80-83 (objects/info/alternates), :261-273 (shallow, commondir) all inside the 319-line file and all five documented subjects (gitfile, alternates, commondir, shallow, worktrees) are present | `.ufo/waves/round-99/w1/ScoutSources/fetch3_population.json` |
| SS-11 S225 upstream re-open | agree on bytes, disagree on one pointer label — HTTP 200, 5667 B, `2c5fa192…0795` = capture = provenance sha256; all five cited quotes present at :7, :13, :25, :27, :105; but the row's cell says "pointer 226 byte 0xE2" while the file's own pointer column is 0..127 with 0x00E2 at pointer 98 (226 is the byte value in decimal). The byte→codepoint mapping the row teaches (0x80→U+20AC, 0x86→U+2020, 0x92→U+2019, 0x94→U+201D, 0xE2→U+00E2) is correct. Cosmetic label slip in a pre-existing BASE row (opened 2026-11-02); not a defect of round 99 and not in any round-99 instrument's scope | same |
| SS-12 S306 upstream re-open | agree — HTTP 200, 175847 B, `abf64368…d802` = capture = provenance sha256; quote `if '\n' in key or '\r' in key or '\0' in key:` at line 1562 (only occurrence) in both the live file and the capture | same |
| SS-13 C2 population, remaining nine rows re-opened | agree — S174, S175, S176, S177, S180, S220, S285, S293 all HTTP 200 with live sha256 = capture sha256 = provenance sha256 column; S270 returns HTTP 404 whose 14-byte body `404: Not Found` is sha256 `d5558cd4…12ed`, byte-identical to the committed capture and to the provenance column (that row is a rejected row about the 404 body, so agreement is expected) | same |
| SS-14 census validate | agree — rc 0, zero E-codes, 31 W04 (duplicate-URL-across-scopes) + `kengaku ok …/corpus/SOURCES.md`; the BASE tree gives 30 W04, so the single new warning is S334 sharing S181's URL across scopes. Warnings never change a lane's clean status | `.ufo/waves/round-99/w1/ScoutSources/census_validate.txt` |
| SS-15 frozen counters re-run at T | agree — C1 `PREDICATE R99-C1 pass` rc 0 with the claims file's exact TARGET line; C2 `PREDICATE R99-C2 pass` rc 0 with `pop=12 cleared=12 still=0 outside_rows=313 … url_channel_files=0 rows_changed=0 captures_changed=0`. Both also pass at lane tip `fc65aa9a` with identical TARGETs | `.ufo/waves/round-99/w1/ScoutSources/live-reopen-S334-S341.txt` §E |
| SS-16 freeze / candidate-byte integrity | agree — all 19 frozen-instrument hashes byte-exact at T, all 11 candidate-byte hashes byte-exact at T, and `git diff 24a5a555..f72a8bc7` touches exactly the 11 candidate files plus `corpus/evidence/round99/bnfit-probe.txt` | same §E |
| SS-17 anchor-digest gate at T vs BASE | agree — BASE `rows=325 tokens=209 defects=45`, T `rows=333 tokens=217 defects=33`; no DEFECT line at T names S334–S341 or any of the 12 population rows; binding census BASE→T shows 8 rows added, 0 removed, exactly the 12 population rows re-bound, 0 other row moved | `.ufo/waves/round-99/w1/ScoutSources/gate_T.txt`, `gate_T_verbose.txt`, `gate_BASE_verbose.txt` |
| SS-18 C1 counter does not read the anchor-cell line/word cells (falsification P1/P2) | **disagree with the implied coverage of "new rows flagged = 0"** — a scratch clone with S334's anchor cell re-pointed to line 151, and another with its word count set to 99, both still print `PREDICATE R99-C1 pass` rc 0 (all LEGS pass), while the lane's own `plans/anchor_line_check.py` reports `ROW S334 state=live defects=line:1,words:1` (live=5 cells=6). L10 reads only the anchor-DIGEST gate's DEFECT lines, so the located-quote defect class that `anchor_line_check` exists to catch is invisible to the frozen C1 predicate. Same class that was live at T on S334/S336–S339 (`live=5 cells=5` rc 1) and was fixed after T in `b71b990a`. Routed to round 100; not repaired here | `.ufo/waves/round-99/w1/ScoutSources/live-reopen-S334-S341.txt` §F P1–P3 |
| SS-19 word-count corrections recomputed independently | agree — recomputing `len(quote.split())` on the T cells gives exactly the L1's disclosed deltas (S334 4→5, S336 4→3, S337 11→12, S338 5→6, S339 5→1) and `anchor_line_check` is `live=0 cells=0` rc 0 at HEAD. The correction was applied in place to five BASE-independent new rows, which QUALITY Q34 says must be superseded by a new row — a rule question for the planner, not a source finding | same §F P3 |
| SS-20 no tool was installed or upgraded | n/a — only the pinned `uv venv` (uv 0.13.0, python 3.13.16) under my scratch and read-only use of the lane's R 4.4.3 / bnlearn 5.2.1; no pacman transaction (host guard PAUSED), no host mutation | same header |

## Notes for the planner (routed, not repaired)

- SS-18 is the substantive coverage gap: the round's own `anchor_line_check` gate was red at T on
  five of the eight new SOURCES rows, and the frozen C1 predicate was blind to it because its L10
  leg consults only `anchor_digest_check.py`. Any "the new rows are clean" reading of
  `new_rows_flagged=0` must be qualified: it is true for the digest gate only.
- SS-11 is a label slip in a pre-existing row (`pointer 226` vs the file's own `pointer 98`);
  the byte→codepoint content the row teaches is right, so no claim depends on it.
- SS-19: the post-T fix edited five rows' anchor cells in place. QUALITY Q34 requires a
  superseding row for a correction. Round-99's own lesson records this as M3 and discloses the
  departure from the claims file's "never repaired in round" clause; the planner seat owns the
  ruling, I only record the facts.

## Method limits

- `sources-census.sh validate` and `plans/anchor_digest_check.py` were run read-only; the two
  counters and both mutations ran in isolated `git clone --shared` checkouts under my scratch
  (`git -C <fixture> rev-parse --show-toplevel` verified per fixture), never in the lane.
- No production edits, no commits, no pushes, no task calls, no writes outside
  `.ufo/waves/round-99/w1/ScoutSources.md`, `.ufo/waves/round-99/w1/ScoutSources/` and my scratch.
