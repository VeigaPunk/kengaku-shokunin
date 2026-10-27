# Round 46 — wave 1 — seat R46ScribeC2Rows (scribe)

Round: kengaku 46 (hyaku run 9, 2026-10-27), wave 1 — build / pre-data. Claim: **C2 (depth)**, frozen whole at
`fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f` over base `64ba8385ea10af1b78d367dcb242b92d97062af7`.
My item: draft the nine superseding registry rows **S157–S165** (QUALITY Q34) for S108, S149, S150, S151, S152, S153,
S154, S155, S156, prove them on a clone, and hand them to the L1.

Read first, in full: `plans/round-46-claims.md` (C2 surface, frozen predicate, kill rule, "Limits named now"),
`corpus/QUALITY.md:759-822` (Q34), `corpus/lessons/round-45-verifier-spotcheck.md` §2 (C2 ruling, `harmed`) and §5
(routed items 1 and 4). Nothing frozen was edited: `corpus/SOURCES.md`, the two C2 tools, the claims files,
`plans/refusals45/` and every `corpus/evidence/` capture are unchanged by this seat (`git -C <lane> status
--porcelain` shows no modification under `corpus/` or `plans/`).

**Product: `.ufo/waves/round-46/w1/R46ScribeC2Rows/rows.md`** — nine 11-cell rows, append-ready, plus the ≤25-word
located quote table for the lesson Gate (closure D2). Nothing else was written in the lane.

## 1. What the rows do

Nine NEW rows, `teaches` opening `supersedes S0NN — `, one per superseded id, in the order the item names them.
No old row is touched: on the clone the staged file diff is **9 added / 0 removed lines**
(`git -C "$S/lane" diff --numstat -- corpus/SOURCES.md` → `9	0	corpus/SOURCES.md`), so the frozen counter's
`base_missing=0 base_changed=0` half of leg A cannot move.

| new | supersedes | kind (old→new) | anchor cell rewritten | why |
|---|---|---|---|---|
| S157 | S108 | code → code | `tests/test_outputs.py:8-90, :87 … (5 words)` (was `(6 words)`) | the `:87` quote is 5 whitespace tokens |
| S158 | S149 | code → code | `test_outputs.py:1-18, :18 …` (was `1-19`) | capture is 18 lines |
| S159 | S150 | **code → docs** | `instruction.md:1-9, :9 … (9 words)` (was 8) | prose file; quote is 9 tokens |
| S160 | S151 | code → code | `setup.sh:1-43, :30 … (3 words)` (was `1-45`, 4) | capture 43 lines; quote 3 tokens |
| S161 | S152 | code → code | `Dockerfile:1-20, :17 "RUN bash /app/setup.sh" (3 words)` (was `1-16, :15`, 4) | `:15` is blank; seed runs at `:17` |
| S162 | S153 | code → code | `test.sh:1-29, :26 "echo 1 > /logs/verifier/reward.txt" (4 words)` (was `1-31, :28`, 6) | `:28` holds the `echo 0` branch |
| S163 | S154 | **code → docs** | `README.md:1-33, :31 "is among the recovered passwords" (5 words)` (was `1-46, :44`) | file is 33 lines / 2,007 bytes |
| S164 | S155 | code → code | `solve.sh:1-68, :63 … (4 words)` (was `1-70`, 3) | capture 68 lines; quote 4 tokens |
| S165 | S156 | **code → docs** | unchanged (`task.toml:1-41, :34 … (3 words)`) | anchor was already right; only the kind cell is corrected |

S165 repairs no `anchor_line_check` defect (S156 is not defective); it exists for the kind correction
(`R45RevRowCells` defect 12) and for completeness of the supersession set. S150/S154/S156 kind `docs` follow the
precedent rows S139 (instruction.md), S143 (README.md), S146 (task.toml), all kind `docs`.

## 2. Per-row ledger — old cell vs observed, with the command that observed it

`python3 plans/anchor_line_check.py --lane .` at base (`receipt-before.txt`) named 14 defect cells on 8 rows; the
per-row line/word facts below were read from the captures with `str.splitlines()`/`len(quote.split())` (the tool's own
conventions, `plans/anchor_line_check.py:18-22`):

| row | defect(s) at base | observed value | evidence |
|---|---|---|---|
| S108 | words | `:87` holds the quote; quote is 5 tokens | `corpus/evidence/round36/tb2-regex-log/test_outputs.py:87` |
| S149 | range | 18 lines; `:18` holds the quote | `…/round45/tb2-password-recovery/test_outputs.py` |
| S150 | words | 9 tokens, not 8 | `…/instruction.md:9` |
| S151 | range, words | 43 lines; 3 tokens | `…/setup.sh:30` |
| S152 | line, words | quote at `:17` (20-line file); 3 tokens | `…/Dockerfile:17` |
| S153 | line, range, words | quote at `:26`, `:28` is `echo 0 …`; 29 lines; 4 tokens | `…/test.sh:26,28` |
| S154 | line, range | quote at `:31`; file 33 lines | `…/README.md:31` |
| S155 | range, words | 68 lines; 4 tokens | `…/solve.sh:63` |
| S156 | — (kind only) | anchor correct as landed | `…/task.toml:34` |

No single offset explains the nine range ends (S149 +1, S151/S153/S155 +2, S154 +13, S152 −4): each range has to be
re-derived from its capture, which is what the new rows do.

## 3. Live re-open (each URL back through curl at the pin)

`receipt-live-reopen.txt` — all nine `http=200`, live `sha256` identical to the registry token **and** `cmp`-equal to
the committed capture:

```
regex-log/tests/test_outputs.py            345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 byte-equal
password-recovery/tests/test_outputs.py    2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e byte-equal
password-recovery/instruction.md           bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5 byte-equal
password-recovery/environment/setup.sh     9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8 byte-equal
password-recovery/environment/Dockerfile   6fabcb9e1fcb7155bf8cfe106c17f2dfa3344103e97960dab580c2444b6c9fe0 byte-equal
password-recovery/tests/test.sh            4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 byte-equal
password-recovery/README.md                122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add byte-equal
password-recovery/solution/solve.sh        c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f byte-equal
password-recovery/task.toml                cfd0362d201b957796f9bf1c02cc75646250cb2bd107ec88c768bfcfd091b24b byte-equal
```

Base: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`.

## 4. Gates and controls (every run under the round-46 envelope)

### 4.1 After — nine rows appended to a `--shared` clone of the freeze commit

```
$ /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" \
    python3 "$S/lane/plans/anchor_line_check.py" --lane "$S/lane"
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/env /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/env --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/lane/plans/anchor_line_check.py --lane /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/lane
ENVELOPE start 02:04:26 cwd=/home/vgpnk/Projects/shokunin
UNCAPTURED S093
UNCAPTURED S103
UNCAPTURED S104
UNCAPTURED S110
ROW S108 state=repaired by=S157 defects=words:1
ROW S149 state=repaired by=S158 defects=range:1
ROW S150 state=repaired by=S159 defects=words:1
ROW S151 state=repaired by=S160 defects=range:1,words:1
ROW S152 state=repaired by=S161 defects=line:1,words:1
ROW S153 state=repaired by=S162 defects=line:1,range:1,words:1
ROW S154 state=repaired by=S163 defects=line:1,range:1
ROW S155 state=repaired by=S164 defects=range:1,words:1
ANCHORLINE rows=158 cited=48 captured=44 uncaptured=4 defective=8 repaired=8 live=0 cells=0
ENVELOPE end 02:04:29 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

`live=0`, the eight named `repaired`, exit 0, PATH-dir digest unchanged. `rows=158` = 149 base rows + 9.

### 4.2 Census

```
$ …/claims/envelope.sh "$S/env" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file "$S/lane/corpus/SOURCES.md"
ENVELOPE start 02:04:31 cwd=/home/vgpnk/Projects/shokunin
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
… (14 more pre-existing W04 lines, S048/S057/S058/S059/S064/S065/S066/S067/S068/S069/S071/S075/S076/S100)
file	ok	/fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows/lane/corpus/SOURCES.md
ENVELOPE end 02:04:34 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Exit 0. Every W04 is pre-existing at base (the warning lists no S157–S165); zero E-codes, so no E03 duplicate id,
E04 duplicate url-in-scope, E05 kind, E07 status, E08/E09 date or E11 used-by-path finding. Warnings do not change
status (`scripts/sources-census.sh:33`).

### 4.3 Before-control — same clone without my rows

```
ENVELOPE start 02:04:57 cwd=/home/vgpnk/Projects/shokunin
… 8 `ROW … state=live` lines, S108…S155 …
ANCHORLINE rows=149 cited=39 captured=35 uncaptured=4 defective=8 repaired=0 live=8 cells=14
ENVELOPE end 02:05:01 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Doing nothing fails: `live=8`, exit 1, and the 14 defect cells are exactly the base rows the claim names.

### 4.4 Negative control — the nine rows with S161's anchor copied from the old S152 cell

```
ENVELOPE start 02:05:59 cwd=/home/vgpnk/Projects/shokunin
ROW S152 state=live defects=line:1,words:1
ROW S161 state=live defects=line:1,words:1
ANCHORLINE rows=158 cited=48 captured=44 uncaptured=4 defective=9 repaired=7 live=2 cells=4
ENVELOPE end 02:06:02 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

A superseding row carrying a wrong anchor repairs nothing and is itself red — the same shape as the tool's JUNK
fixture (`plans/anchor_line_check.py:178`). So the pass in §4.1 is earned by the corrected cells, not by the row's
existence.

### 4.5 Gate selftest (tool sanity, not part of the predicate)

```
SELFTEST RED rc=1 want_rc=1 ok :: ANCHORLINE … defective=1 repaired=0 live=1 cells=2
SELFTEST GREEN rc=0 want_rc=0 ok :: ANCHORLINE … defective=1 repaired=1 live=0 cells=0
SELFTEST JUNK rc=1 want_rc=1 ok :: ANCHORLINE … defective=2 repaired=0 live=2 cells=4
SELFTEST pass
ENVELOPE end 02:05:10 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## 5. ≤25-word located quote table (lesson Gate, closure D2)

Every quote is a substring of the cited line in the committed capture **and** in the live file re-opened today; word
counts are `len(quote.split())`.

| row | supersedes | quote (verbatim) | location | words | capture lines | row range |
|---|---|---|---|---|---|---|
| S157 | S108 | `matches = re.findall(pattern_text, log_text, re.MULTILINE)` | `corpus/evidence/round36/tb2-regex-log/test_outputs.py:87`, url `…/regex-log/tests/test_outputs.py:87` | 5 | 90 | 8-90 |
| S158 | S149 | `assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` | `corpus/evidence/round45/tb2-password-recovery/test_outputs.py:18`, url `…/password-recovery/tests/test_outputs.py:18` | 4 | 18 | 1-18 |
| S159 | S150 | `Write each matching password you find, one per line` | `…/instruction.md:9`, url `…/instruction.md:9` | 9 | 9 | 1-9 |
| S160 | S151 | `split_point=$((offset + 20))` | `…/setup.sh:30`, url `…/environment/setup.sh:30` | 3 | 43 | 1-43 |
| S161 | S152 | `RUN bash /app/setup.sh` | `…/Dockerfile:17`, url `…/environment/Dockerfile:17` | 3 | 20 | 1-20 |
| S162 | S153 | `echo 1 > /logs/verifier/reward.txt` | `…/test.sh:26`, url `…/tests/test.sh:26` | 4 | 29 | 1-29 |
| S163 | S154 | `is among the recovered passwords` | `…/README.md:31`, url `…/README.md:31` | 5 | 33 | 1-33 |
| S164 | S155 | `echo "$combined" >> "$OUTPUT_FILE"` | `…/solve.sh:63`, url `…/solution/solve.sh:63` | 4 | 68 | 1-68 |
| S165 | S156 | `allow_internet = true` | `…/task.toml:34`, url `…/task.toml:34` | 3 | 41 | 1-41 |

(D2 of the round-45 closure wanted exactly this: the quote lives in `rows.md` §quote table and here.)

D6 (S154 `teaches` quotes only text the README holds): S163's `teaches` quotes three fragments, each verified with
`grep -nF` in the pin's README — `exists` at `:29`, `contains at least one password guess` at `:30`,
`is among the recovered passwords` at `:31`. No paraphrase sits inside quote marks.

## 6. Proposal — `status` / `used-by` for the nine superseded rows (mutable cells only)

| old row | status old → new | used-by old → new | basis |
|---|---|---|---|
| S108 | `mined` → `mined` | `corpus/knowledge/tb2-regex-log-grader.md` → unchanged | |
| S149–S155 | `mined` → `mined` | `corpus/knowledge/tb2-password-recovery-grader.md` → unchanged | |
| S156 | `mined` → `mined` | same → unchanged | |

Reasoning, so the L1 can overrule it in one line: the contract's status enum is `queued|mined|rejected`
(`scripts/sources-census.sh:659`) — there is no `superseded` value, and Q34 expresses supersession only through the
new row's `teaches`. Every landed supersede pair leaves the old row's mutable cells as they were
(S030←S042, S054←S064, S025←S036, S071←S075: old rows still `mined`, used-by unchanged), so changing them here would
be the first exception in the registry. If the entry's provenance is re-pointed to S157–S165, dropping the old
`used-by` to `—` would raise W03 on eight rows (`mined` with `used-by = —`); the census `ok` above is only reachable
with `used-by` kept. Proposal: leave both cells alone; the marker is the `supersedes` cell of S157–S165.

## 7. Findings and limits

1. **Frozen-tool gap (report, do not fix this round).** `RANGE_RE` in `plans/anchor_line_check.py:59` is
   `[\w./-]+\.[A-Za-z0-9]+:(\d+)-(\d+)` — it needs a dot-extension. `Dockerfile:1-20` therefore **is not range-checked
   at all**: S161's range could say any `a-b` and the tool would stay green — `receipt-range-regex.txt` runs the
   tool's own `RANGE_RE` and gets `search('Dockerfile:1-20') -> None` while
   `search('tests/test_outputs.py:1-18') -> 'tests/test_outputs.py:1-18'`; the base row's `Dockerfile:1-16` was
   likewise never checked (base S152 showed only `line` and `words`). My
   S161 range is correct by hand (20 lines, `b<=nlines`), but it is *not certified by the gate*. The tool is frozen for
   this round; a follow-up would be `[\w./-]+:(\d+)-(\d+)`.
2. The nine rows' `scope` cells carry the old rows' text verbatim except where the old text was false; S158 kept
   S149's scope word-for-word on purpose, so no new `W04` (duplicate-url-across-scopes) line is introduced by this
   seat — an earlier draft that reworded it printed `file W04 S158 …`; that run's receipt was overwritten by the final
   one, and the shipped `receipt-census.txt` lists no S157–S165 warning.
3. `anchor_line_check` reports `UNCAPTURED S093/S103/S104/S110` in every run; that is the claim's declared limit
   (`round-46-claims.md` C2 "Limits named now"), unchanged by my rows.
4. S165 repairs no anchor defect. If a reader expects exactly eight superseding rows, S165 is the ninth because S156's
   `kind` is wrong (`code` for `task.toml`), not its anchor.
5. No tool was installed, no package touched: the only network use is nine `curl` reads of the pinned raw URLs
   (§3); `sources-census.sh` and the two gate tools were read and executed, never edited.
6. Not mine, left to the entry seat: the `## Predictor` rewrite, the `source:` ranges and `## Errata (round 46)`
   (legs B/C of the frozen counter). My rows change neither the entry nor any base row.

## 8. Artifacts

Under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ScribeC2Rows/`
(each ≤10,051 bytes; nothing copied from `corpus/` or `plans/`, no mirror, no clone):

| file | bytes | sha256 |
|---|---|---|
| `rows.md` (nine rows + D2 quote table, append-ready) | 10051 | `0fc45561b0c6b8500078e52f8ea69b2cebd28794361defd090aca2f1b2c9f7ac` |
| `receipt-anchorline.txt` (after, `live=0`) | 1239 | `2582ba51fb96faee529e1e5a1e1e5883fc6f9b6cb85c76d293cff45b1bf10dc0` |
| `receipt-before.txt` (before, `live=8`) | 1158 | `348988e6920901b57a57e04eba834d6cbe98a546f04ad45ab0b708bbc50fd237` |
| `receipt-census.txt` (validate, exit 0) | 2112 | `cfd922cdd03880f05f0196c6ed4132b9243fdb0663f00a0070a682a9e31a4acb` |
| `receipt-control-wrong-anchor.txt` (negative control) | 1284 | `61a55c32751ad7cd84e5f3355d176e2cc3cf5b4a645adeb2fd64e127cadd9f41` |
| `receipt-selftest.txt` | 988 | `d66f6fe2296f19355c10efab637f95aebe393e354ffea9f2745208eb8c95005c` |
| `receipt-live-reopen.txt` (9 live sha256, `cmp`, D6) | 2493 | `a5e41ae8fb65affc8444dc75ca39a34678e1cc2e73ab2ff2b38e1fd1598848b6` |
| `receipt-range-regex.txt` (RANGE_RE skips `Dockerfile:1-20`) | 819 | `1105459ec0ab3f793aaac160d3d9b9f3f0c64bfddc9d78337d15f586f557dce5` |

Scratch `S=/fast/scratch/hyaku/kengaku-r46/R46ScribeC2Rows` held two `--shared` clones of the lane (both
`git -C … rev-parse --show-toplevel` = the clone path, both at `fd4129eb…`), the live fetches and the row builder;
deleted before yielding:
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ScribeC2Rows "$S"` →
`DELETE path=… bytes=1099492107 size=1.0GiB`, `SAFE_RM_RC=0`; the round root, its sentinel and the other seats'
directories were left standing (`ls /fast/scratch/hyaku/kengaku-r46/` still lists `L1`, `R46ExecC1Counter`, …).

## 9. Out of scope (named, not done)

The entry's predictor/source-ranges/errata (legs B–C), the C2 counter run at the tip, the L1's landing commit, the
`corpus/knowledge/tb2-password-recovery-grader.md` re-pointing to S157–S165, and the SCORECARD/LOG/lesson edits.

VERDICT: c2-rows-9-live-0-census-exit-0
