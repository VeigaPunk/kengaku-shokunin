writer: KengakuR29-2.FReopenS073-2
seat: KengakuR29-2.FReopenS073-2 (post-crash falsify leaf; read-only)
item: re-open source row S073 (`prepare.sh`) live at its URL; verify every cell against live bytes; re-locate the build seat's ≤25-word quote and count it
opened: 2026-10-21T16:47:22Z (first live GET); lane master `56fd949a6478342531e61f4feecb4a685d831640`
scope: row S073 only — cells `scope`, `anchor` line numbers/bytes/hash, `teaches`, plus the enumerated quote. Not S070–S072, not the projection instrument, not the knowledge draft.

## Independence and tooling

- Production source `plans/config_projection.py` was **not read, imported or executed**; this item does not touch the projection instrument at all.
- Read: `corpus/SOURCES.md` line 95 (row S073) and header line 21; `.ufo/waves/round-29/build/R29SourceCaller.md` (build seat's evidence); `plans/fixtures/r29/manifest.json`.
- Live bytes: two independent `curl` GETs of the row's URL, retained under
  `.ufo/waves/round-29/scratch/falsify/FReopenS073/` as `prepare.live.sh` and `prepare.second.sh`.
- Installs/upgrades: none. All work used stdlib `python3`, `curl`, `sha256sum`, `wc`, `git hash-object`.
- No writes outside this report and my scratch directory.

## Live re-open (observed)

- URL: `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh`
- commit in URL: `dce04686a56253aefba7b18a4fa0937cf1dc987b` — byte-for-byte identical to the row's `source` URL string (string equality check `True`).
- first GET 2026-10-21T16:47:22Z: `HTTP/2 200`, `content-length: 120`, `content-type: text/plain; charset=utf-8`, `etag: "1db3d6fd14ac6271a6e29fc07d4955bb0c001a96a833747d6d23f79643de5d80"`, `x-cache: HIT`.
- second GET (same URL, same session): `cmp prepare.live.sh prepare.second.sh` exit 0; both sha256
  `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2`.
- byte size 120; `wc -c -l` = `120 6`; 6 LF, 0 CRLF; trailing LF present; `bytes.isascii()` = True.
- `git hash-object prepare.live.sh` = `64014fce254d0c715c3accae1ae1cb1362a2a6be` (matches build report).
- Live line map (numbered, whole file):

```
1 #!/bin/bash
2
3 # prepare the evaluation
4 # re-validate login information
5 mkdir -p ./.auth
6 python browser_env/auto_login.py
```

- Executable-statement lines (non-blank, non-comment): `[5, 6]` — exactly two.

## Cell-by-cell verification (row at `corpus/SOURCES.md:95`)

Header schema `corpus/SOURCES.md:21`: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by. Row has 11 inner cells, matching the header.

| cell | row value (abbreviated, not a quote) | live check | result |
|---|---|---|---|
| source | raw GitHub URL at `dce04686…` | GET 200, same URL string | match |
| kind | `code` | pinned shell script is source code | match |
| tier | `A` | SOURCES legend lines11–17: A includes "source code" primary for the row's scope | match |
| scope | complete pinned prepare.sh executed command set; excludes indirect calls in `auto_login.py`, README, deployment/runtime | live file is complete at 6 lines; it contains no generator token, so the file-scope question is answerable; exclusions are explicit | match |
| anchor | `dce04686, complete file lines1–6 (6 lines,120 bytes, sha256 97b8671f…c7e2); commands lines5–6` | 6 lines, 120 bytes, sha256 equal, commit prefix equal, commands on lines 5–6 | match |
| teaches | only commands are the two backticked statements; zero occurrences of `generate_test_data`, `scripts/`, `config_files`, token exports; indirect/other callers unopened | live substring counts below; exactly two executable statements; no sibling round-29 report opened `auto_login.py` (only `R29SourceCaller.md` mentions it, stating it was not opened) | match |
| status | `queued` | allowed status per legend line 9 (`queued`/`mined`/`rejected`); clause not yet admitted | match |
| opened | `2026-10-21` | build seat verified GET 2026-10-21T16:06:31Z; my re-open same date | match |
| recheck | `on-release` | value already used by rows S068–S072; commit-pinned snapshot | match |
| used-by | `—` | matches queued siblings S070–S072; draft cites the row but the entry is not admitted | match (see note) |

Substring counts on live bytes (literal, case-sensitive, occurrences):

```
generate_test_data 0    scripts/ 0    config_files 0
export 0                token 0       token(any case) 0
auto_login 1            python 1      mkdir 1           .auth 1
cd<space> 0             set -e 0      pip<space> 0      SHOPPING 0
```

The `teaches` cell's absence claims hold on the complete live bytes: the generator name, `scripts/`, `config_files`, `export` and `token` each occur 0 times.

## Build-seat quote relocation (observed)

- Located in `.ufo/waves/round-29/build/R29SourceCaller.md:36–43` (fenced block lines 39–40).
- The quoted text is a contiguous live substring: first occurrence at byte offset 70, exclusive end 119; `bytes.count(quote)` = 1; 49 bytes = 49 codepoints, all ASCII.
- Quote, reproduced verbatim (5 words, count below):

```
mkdir -p ./.auth
python browser_env/auto_login.py
```

- Programmatic counts: `len(quote.decode().split())` = **5**; `wc -w` on the same two-line string = **5**; `printf '%s' … | wc -w` = **5**. 5 ≤ 25.
- The build report's stated numbers ("5", bytes 70–119 exclusive, 49 codepoints) all reproduce exactly.

## Mismatches

- Wrong cells: none found.
- Unsupported cells: none found. The one wording worth flagging is not a cell error:
  `[INFERENCE]` the anchor's "complete pinned" means commit-pinned by URL plus the recorded sha256; `prepare.sh` is **not** listed in `plans/fixtures/r29/manifest.json` (`grep -c "prepare.sh"` = 0). The build report itself discloses this ("NOT listed in … manifest.json"), and C1's projection inputs are the manifest's generator/raw/profiles, so the row is not relied on as a manifest pin.
- `[INFERENCE]` `used-by: —` alongside `status: queued` follows the S070–S072 convention (link added at admission); the draft's front-matter citation of S073 does not contradict the queued status.
- Process note, not a cell error: `corpus/evidence/round29-calibration/` contains no per-row URL/access/quote gate file for S073 (`grep -rn "S073\|prepare.sh\|97b8671f" …` returned no lines), so the round-29 quote lives only in the build report; the SOURCES header line 7 describes that gating convention for round 24. This does not make any S073 cell false.

## Commands and outputs (units explicit)

```
curl -sS -f -D headers.txt -o prepare.live.sh <row URL> -w 'http_code=%{http_code} size_download=%{size_download}'
  -> http_code=200 size_download=120     (date header 2026-10-21T16:47:22Z)
sha256sum prepare.live.sh   -> 97b8671f…b0c7e2
wc -c -l prepare.live.sh    -> 120 6
git hash-object prepare.live.sh -> 64014fce254d0c715c3accae1ae1cb1362a2a6be
curl … -o prepare.second.sh; cmp prepare.live.sh prepare.second.sh -> exit 0
python3 cell check          -> sha match True; bytes 120==120; lines 6==6;
                               quote occurrences 1; offset 70 end 119; quote words 5;
                               executable stmt lines [5,6]; all zero-claims count 0
wc -w <<< '<quote>'         -> 5
printf '%s' '<quote>' | wc -w -> 5
```

Quote-count units: whitespace-split words; byte units for size/offset; line units for line counts; occurrences for substring probes. No task, leaf, profile or projection counts are claimed here.

## Boundaries

- No execution of `prepare.sh`; `./.auth` created nowhere; `auto_login.py` never fetched or opened.
- Single endpoint, two GETs; no other network access.
- Static snapshot at the pinned commit; no claim about HEAD drift, other callers, runtime, deployment, task validity or contamination.
- No production, fixture, corpus, SOURCES, SCORECARD, knowledge-candidate or lane-index mutation.

VERDICT: PASS
