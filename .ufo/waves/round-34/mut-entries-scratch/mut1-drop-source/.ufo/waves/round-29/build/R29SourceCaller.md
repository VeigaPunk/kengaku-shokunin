# R29SourceCaller — proposed S073: WebArena prepare.sh is not the generator call site

- seat: `KengakuR28.R29SourceCaller-2`
- actual writer: `KengakuR28.R29SourceCaller-2` (leaf scout; no subagents, no SOURCES edit)
- opened: 2026-10-21; verified GET at 2026-10-21T16:06:31Z
- scope: the complete pinned `prepare.sh` text as evidence about whether it statically invokes
  `scripts/generate_test_data.py`; one row proposal (S073) only

## Opened source

- URL: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh
- commit: `dce04686a56253aefba7b18a4fa0937cf1dc987b` (same pinned revision as the r29 manifest)
- transport: `GET` -> `HTTP/2 200`, `content-type: text/plain; charset=utf-8`,
  `content-length: 120`; `ETag "1db3d6fd…"` is transport metadata and is NOT the body digest.
- retained bytes (read once, not hash-then-reread):
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29SourceCaller-2/prepare.sh`
  and the byte-identical `prepare.recheck.sh` (`cmp` exit 0, same sha256).
- sha256: `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2`
- Git blob SHA-1 (`git hash-object`): `64014fce254d0c715c3accae1ae1cb1362a2a6be`
- size: 120 bytes, 6 lines, ASCII, LF endings, trailing newline present
- pin status: `prepare.sh` is NOT listed in `plans/fixtures/r29/manifest.json`; this hash is a
  first observed pin candidate for this file, not a re-verification of an existing manifest pin.

Full retained text (public upstream shell; contains no credential values, no environment values,
no auth/cookie material):

```
#!/bin/bash

# prepare the evaluation
# re-validate login information
mkdir -p ./.auth
python browser_env/auto_login.py
```

Located quote (lines 5–6; file bytes 70–119 exclusive; 49 codepoints, all ASCII):

```
mkdir -p ./.auth
python browser_env/auto_login.py
```

Programmatic word count: **5** (whitespace-split; `wc -w` = 5, `len(quote.split())` = 5). This is
≤25 words. The quote is the complete executable body, which is why it is the chosen located quote.

## Static invocation reading (never executed)

Observed on the retained bytes (literal substring occurrence counts):

| probe | occurrences | unit |
|---|---|---|
| `generate_test_data` | 0 | occurrences |
| `scripts/` | 0 | occurrences |
| `config_files` | 0 | occurrences |
| `export` | 0 | occurrences |
| `SHOPPING` | 0 | occurrences |
| `auto_login` | 1 | occurrence |
| `python` | 1 | occurrence |

Observed structure: line 1 shebang; line 2 blank; lines 3–4 comments; line 5 `mkdir -p ./.auth`;
line 6 `python browser_env/auto_login.py`. Exactly two executable statements, neither of which is
the generator. There is no `cd`, no `set -e` and no package install (`cd `/`set -e`/`pip ` counts are
each 0); both statements are cwd-relative, consistent with a repo-root invocation convention
(README/workflow unopened here).

Reading:

- [observed, file-scope] `prepare.sh` contains no invocation of `scripts/generate_test_data.py` and
  no write of `config_files/test.json`; it is therefore not the generated-config call site in this
  pinned snapshot.
- [observed] It also exports none of the six substitution tokens/values; its only actions are auth
  directory creation and an auto-login launch.
- [INFERENCE] Running `prepare.sh` alone (not done here) would not itself produce per-task configs;
  any generation must be a separate invocation. Whether `browser_env/auto_login.py` indirectly
  imports or invokes the generator is UNKNOWN — that file was not opened (and must not run).
- The documented workflow caller is outside this file; README/workflow is the sibling S072 scope and
  was not opened by this seat.

Not established by this row: absence of a generator callsite anywhere else in the repository;
README/Makefile/CI invocation; runtime behavior of `auto_login.py`; environment population; any
actual deployment configuration.

## Proposed S073 row (proposal only; `corpus/SOURCES.md` was not edited)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S073 | WebArena prepare-script generator call-site boundary — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh | code | A | the complete pinned prepare.sh executed command set as evidence about whether it invokes scripts/generate_test_data.py; not indirect calls inside auto_login.py, not README workflow, not deployment or runtime | dce04686, complete file lines1–6 (6 lines,120 bytes, sha256 97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2); commands lines5–6 | prepare.sh is not the generated-config call site: its only commands are `mkdir -p ./.auth` and `python browser_env/auto_login.py`, with zero occurrences of generate_test_data, scripts/, config_files or token exports; indirect invocation through auto_login.py and any other caller remain unopened | queued | 2026-10-21 | on-release | — |

Field rationale (L1 owns the final write):

- `kind code`, `tier A`: primary source for its own text only; tier is scoped to `scope`.
- The absence claim is anchored to the complete 6-line/120-byte file plus sha256, because the quote
  alone cannot prove absence; the located quote shows the whole executed body.
- `status queued` at proposal: per the SOURCES header, `mined` means the content has been extracted
  into knowledge; the round29 entry is not admitted yet. Flip to `mined` only at admission, and set
  `used-by` to the admitting entry then. No used-by link is claimed here.
- `recheck on-release`: commit-pinned code snapshot, matching S061–S063/S068–S069 practice.

## Relation to C1 (bounded)

- C1's projection order (six global serialized-text replacements -> JSON parse -> enumerate-index) is
  S070 generator behavior. `prepare.sh` contributes no tokens and no generation step, so a faithful
  projection needs no model of it; the 812 x 3 = 2436 task/profile denominator is unaffected by this
  row, and nothing here measures projection output.
- This row prevents citing `prepare.sh` as the generated-config entry point and answers the draft's
  "whether the upstream prepare/workflow caller invokes this generator" unknown in the negative for
  `prepare.sh` only. No method, model, calibration or task-validity claim follows.
- The fresh sha256 above is available if L1 chooses to pin `prepare.sh`; this seat changed no pin.

## Boundaries and unknowns

- No execution: `prepare.sh` was never run; `./.auth` is absent both at lane root and under this
  seat's scratch; `browser_env/auto_login.py` was never opened or run; `browser_env/env_config.py`
  was not fetched; no host environment, credential, auth-state or browser-profile reads.
- Network: three accesses to the single assigned URL only — one `read`-tool retrieval (display), then
  two `curl` GETs (body; status/byte-identity check). No other endpoint or site request. Retained
  material is 120 bytes of public shell with no values.
- Source-vs-runtime: static snapshot at the pinned commit, not HEAD; no runtime, deployment,
  benchmark-task-validity or contamination claim.
- Unknowns preserved: indirect invocation inside `auto_login.py`; other repository callers;
  README/workflow content (S072 seat); live upstream drift after this access date.

## Commands and measurements

```
curl -sS --max-time 30 -o prepare.sh https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh
  -> 120 bytes written
curl -sS -f --max-time 30 -D headers.txt -o prepare.recheck.sh <same URL>
  -> HTTP/2 200; content-length 120; content-type text/plain; charset=utf-8
cmp prepare.sh prepare.recheck.sh          -> identical (exit 0)
sha256sum prepare.recheck.sh               -> 97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2
git hash-object prepare.recheck.sh         -> 64014fce254d0c715c3accae1ae1cb1362a2a6be
wc -c -l prepare.recheck.sh                -> 120 6
python3 substring counts                   -> table above (occurrences)
wc -w <<< '<located quote>'                 -> 5
python3 offsets                            -> quote bytes [70,119), 49 codepoints
```

Units are explicit: bytes and lines for the file; literal substring occurrences for token probes;
whitespace-split words for the quote; codepoints for the quote span. No task, leaf or projection
counts are claimed here.

## Search log

Identified 1 (assigned URL), screened 1 (complete 120-byte file), included 1 row proposal (S073),
excluded 0, unopenable 0. Stop rationale: the assignment names the exact pinned path; the file is
small enough to read completely; the second GET only verifies status and byte identity.

VERDICT: PASS — S073 proposed from the opened pinned source with retained hash, located 5-word quote, and static-only boundary; no SOURCES edit and no round admission.
