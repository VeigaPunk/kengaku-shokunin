# R45RevRowCells — SOURCES rows S149–S156 verification (falsify, wave a3w1)

Lane tip measured: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C .../kengaku-shokunin rev-parse HEAD`).
All 8 captures re-fetched from the pinned commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` via `curl -fsSL`
into `/fast/scratch/hyaku/kengaku-r45/R45RevRowCells/fetch/`; every hash checked against `corpus/SOURCES.md`
and the lane's `corpus/evidence/round45/tb2-password-recovery/SHA256SUMS`.

## Per-row result

| row | sha256 match | quote verbatim | cited line correct | anchor range vs file | word count | cells |
|---|---|---|---|---|---|---|
| S149 `tests/test_outputs.py` | ✔ 2dc14fc1… | ✔ `:18` | ✔ | `:1-19` — file is 18 lines (off by one) | (4) ✔ | ok |
| S150 `instruction.md` | ✔ bc4f5011… | ✔ `:9` | ✔ | `:1-9` ✔ | (8) — actual 9 | kind `code`, should be `docs` (precedent S139) |
| S151 `environment/setup.sh` | ✔ 9fdde5d9… | ✔ `:30` | ✔ | `:1-45` — file is 43 lines | (4) — actual 3 | ok |
| S152 `environment/Dockerfile` | ✔ 6fabcb9e… | quote exists, but **at `:17`** | ✘ `:15` is blank | `:1-16` — file is 20 lines, and line 17 (the quote) is *outside* the range | (4) — actual 3 | ok |
| S153 `tests/test.sh` | ✔ 4770437e… | quote exists, but **at `:26`** | ✘ `:28` reads `echo 0 > …` | `:1-31` — file is 29 lines | (6) — actual 4 | ok |
| S154 `README.md` | ✔ 122bf15e… | quote exists, but **at `:31`** | ✘ `:44` does not exist | `:1-46` — file is 33 lines | (5) ✔ | kind `code`, should be `docs` (precedent S143) |
| S155 `solution/solve.sh` | ✔ c5f9fc70… | ✔ `:63` | ✔ | `:1-70` — file is 68 lines | (3) — actual 4 | ok |
| S156 `task.toml` | ✔ cfd0362d… | ✔ `:34` | ✔ | `:1-41` ✔ | (3) ✔ | kind `code`, should be `docs` (precedent S146) |

Word-count convention = whitespace tokens (`wc -w`); confirmed by S148 `if (c1l ^ c2l) == 0x02000000:` = (6 words) ✔ and S156 (3) ✔.

## URL / pin check

- All 8 URLs resolve at the pin: `curl` HTTP 200, sha256 = registry = SHA256SUMS.
- HEAD refetch of all 8 (`…/terminal-bench-2/HEAD/password-recovery/*`) returns bytes byte-identical to the pin — no upstream drift; the wrong line numbers are not explained by a different revision (HEAD layout is identical to the pin).
- `.gitignore` capture refetched: `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` = SHA256SUMS entry.

## `used-by` and reciprocity

Every row S149–S156 names only `corpus/knowledge/tb2-password-recovery-grader.md`. The file exists (18 861 B, mtime 2026-10-26), is indexed in `corpus/README.md:78` and `:306`, and its own `source:` block (:1–8) cites S149–S156. `grep -rn 'S149\|…\|S156' corpus/knowledge/` outside that entry: no hits — reciprocity clean.

## Census

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit `0`, final line `kengaku	ok …/SOURCES.md`. Output also carries 15 pre-existing `W04 duplicate url … across scopes` warnings on S040–S100 — none on S149–S156, none new.

## `.gitignore` rejection (lesson `corpus/lessons/round-45.md:37`)

Record is **correct and complete**: verdict `reject (as row)`, reason "the task's dotfile; captured for byte-complete refetch checks, not a row — no claim rests on it", plus a flip added attempt-3 ("admit as a row if an entry sentence cites `gitignore` content …"). The flip has not fired: `grep -c gitignore` in the entry = 0. The file is present as a capture (`evidence/round45/tb2-password-recovery/gitignore`, sha matches SHA256SUMS) but not a row — as recorded.

## Defects

| # | where | defect |
|---|---|---|
| 1 | S152 anchor | cited line `:15` is blank; `RUN bash /app/setup.sh` is `:17`; cited range `:1-16` excludes it; file is 20 lines |
| 2 | S153 anchor | cited line `:28` is `echo 0 > …`; the quote is `:26`; range `:1-31` overshoots (29 lines) |
| 3 | S154 anchor | cited line `:44` does not exist (file 33 lines); quote at `:31`; range `:1-46` overshoots |
| 4 | S149 anchor | range `:1-19` overshoots an 18-line file |
| 5 | S151 anchor | range `:1-45` overshoots a 43-line file |
| 6 | S155 anchor | range `:1-70` overshoots a 68-line file |
| 7 | S150 word count | `(8 words)` for a 9-word quote |
| 8 | S151 word count | `(4 words)` for a 3-word quote |
| 9 | S152 word count | `(4 words)` for a 3-word quote |
| 10 | S153 word count | `(6 words)` for a 4-word quote |
| 11 | S155 word count | `(3 words)` for a 4-word quote |
| 12 | S150/S154/S156 kind | `code` where S138–S146 precedent marks `instruction.md`/`README`/`task.toml` `docs` (S139, S143, S146) |
| 13 | propagation | the entry's `source:` block (`tb2-password-recovery-grader.md:1-8`) repeats the same wrong ranges verbatim (setup.sh "1-45", Dockerfile "1-16", test.sh "1-31", README "1-46", solve.sh "1-70") |

Load-bearing cells (sha256, URL, quote text, used-by, tier, status, opened/recheck) are all correct; the failures are in the line-citation cells — the "anchor" column and the `(N words)` tallies.

Rows verified (sha ✔ + quote verbatim + cited line correct): S149, S150, S151, S155, S156 = 5/8.

VERDICT: rows-verified-5/8-census-ok-defects-13
