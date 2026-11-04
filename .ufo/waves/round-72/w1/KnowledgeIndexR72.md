# R72 w1 · KnowledgeIndexR72 — knowledge entry + index, both directions

Seat: `KnowledgeIndexR72` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Audit window: 2026-11-03 23:05–23:15 -03. Frozen input read first in full:
`plans/round-72-claims.md` (R72-C1, R72-C2, round-level). No file was edited — not the entry, not
`corpus/README.md`, not `corpus/SOURCES.md`, not the plans, not any evidence file.

Target of record:

- Entry `corpus/knowledge/tb2-hf-model-inference-provenance.md` — 6,849 bytes, 78 lines,
  sha256 `e384eb34a1df54c09be2a3f80074130be8b98bfb5ec66fb81323b6cbb6a4b53e`, mtime
  2026-11-03 23:01:58.
- Index row `corpus/README.md:96` (README mtime 23:02:12, i.e. row written with the entry).

## Verdict summary

| # | Item | Verdict |
|---|---|---|
| 1 | Provenance trailer: first-line `source:` with S245/S246/S247/S248 + anchors | **PASS** — all four ids, four anchors, four sha256; all four hashes recomputed and match |
| 2 | `verified-at:` line | **PASS with one unverifiable clause** — date, byte counts, hashes, capture paths all hold; "HTTP 200" is not derivable from bytes and was not re-fetched |
| 3 | `recheck:` command can actually run | **PASS (arms 2,3 executed)** — `--check-receipt` on the receipt of record prints `DEFECTS n=0` / `PREDICATE R72-C1 pass`, rc 0; C2 gate prints `E1a ok … E2 ok`, rc 0. Arm 1 was not run by this seat (battery-owned). Recipe is a **template** and omits both controls |
| 4 | `writer:` / `admission:` present | **PASS present / admission locus DANGLING** — `admission: hold` cites `corpus/lessons/round-72.md` `## Gate`, which does not exist on disk |
| 5 | `--clearenv` quote vs `corpus/evidence/round72/sources/bwrap.1.html` | **PASS** — verbatim at `:184-186` |
| 6 | Model-card line vs `hf-model-card.md:145` | **PASS** — line 145 is the `DistilBertForSequenceClassification.from_pretrained(...)` line |
| 7 | K9 assert vs `tests/test_outputs.py:107` | **PASS** — `:103` = status-400 assert, `:107` = `assert "error" in error_data`; probe K9 returns 400 `{"detail": …}`, freezes `PPPF` |
| 8 | Entry mechanism claims (nine-variable allowlist, canary, `__file__`, stub control) | **PASS in source; one framing defect** — `env_cleared=True` is a hardcoded literal, not a computed witness |
| 9 | Entry counts ("6 of 19 assert sites", "19 KB fixture") | **6 of 19 PASS / 19 KB FAIL** — fixture is 5 files, 13,944 bytes (13.6 KiB) |
| 10 | Index row ↔ file (new entry) | **PASS reciprocal** — row at README:96, file present, cited sources present, no duplicate row |
| 11 | Whole-index census | **71 rows vs 72 files**; 0 dangling rows; 1 unindexed file (`tb2-torch-tensor-parallel-offline.md`, pre-existing) |

## 1. Provenance trailer

`source:` is line 1 and names all four rows with anchors and digests. Recomputed against committed
captures (each `sha256sum`, rc 0), and cross-checked against `corpus/SOURCES.md:260,261,263,264`
(the four identical 64-hex strings appear once each in both places):

| row | anchor in entry | committed capture | bytes | sha256 | verdict |
|---|---|---|---|---|---|
| S245 | `instruction.md:3` | `corpus/evidence/round71/hf/instruction.md` | — | `29151c5b…dcc1` | match (line 3 names `distilbert-base-uncased-finetuned-sst-2-english`) |
| S246 | `tests/test_outputs.py:103-107` | `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` | 4,239 | `61a686d6…87857` | match (also `GRADER_SHA256` in the probe, `plans/round72_c1_hf_probe.py:79`) |
| S247 | "the `--clearenv` entry" | `corpus/evidence/round72/sources/bwrap.1.html` | 27,981 | `708f56ee…8de7` | match |
| S248 | `README.md:145` | `corpus/evidence/round72/sources/hf-model-card.md` | 10,512 | `75f17282…8851` | match |

`verified-at:` (line 2) states 2026-11-03, live fetch for S247/S248 (HTTP 200, 27,981 / 10,512
bytes) with captures under `corpus/evidence/round72/sources/`, and S245/S246 re-derived from the
committed captures. Sizes and hashes are confirmed; the HTTP status is a claim about the fetch, not
about the bytes, and this seat did not re-fetch (no network call made).

`recheck:` (line 3) — three arms; both scripts exist and accept every flag used:
`--lane --work --port-lock --receipt --evidence-dir --check-receipt` on
`plans/round72_c1_hf_probe.py` (help rc 0), `--lane` on `plans/round72_c2_routed_defects.py`
(help rc 0), both `py_compile` rc 0. Two executed arms:

- arm 2, `python3 -B plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/receipt.txt`
  → `DEFECTS n=0` / `PREDICATE R72-C1 pass`, rc 0 (receipt committed at 23:10:16, after the entry
  was written; its `PROBE sha256=99867c7f…` equals the on-disk probe's sha256).
- arm 3, `python3 -B plans/round72_c2_routed_defects.py --lane <lane>` → `E1a ok`, `E1b ok`,
  `E1c ok`, `E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass`, rc 0.

Two weaknesses of the recipe, reported rather than edited: (a) it is a template — `<scratch>`,
`<path>`, `<port-5000.lock>` require substitution before any line runs; (b) it exercises neither
`--stub-control` nor the do-nothing control, although the entry itself makes the stub control a
rule ("a sandbox witness must ship the injection that used to defeat it", entry:48-49). A re-runner
following only the `recheck:` line cannot reproduce the entry's central before→after claim.

`writer:` line 5 = `KengakuR72 (with the round-72 wave's reviews)`.
`admission:` line 6 = `hold` with the reason "QUALITY Q13/Q14 second-seat re-read is not yet on
record … see `corpus/lessons/round-72.md` `## Gate` (Admission status)". **That file does not
exist** at audit time (`ls corpus/lessons/round-72.md` → rc 2, "No such file or directory"); the
`round-72` lesson is still unwritten while `round-71.md` (22:30) and the round-71 spot-check exist.
The claims doc assigns `corpus/lessons/round-72.md` `## Gate` to the wave's source seat, so this is
most likely an in-flight dependency — but as bytes stand, the admission status is self-declared and
its cited record is absent. Note `admission:`/`writer:` are a young convention: only 2 of 72
knowledge files carry `admission:` (both `tb2-hf-model-inference-*`), 12 carry `writer:`.

## 2. Entry claims against committed bytes

1. **`--clearenv` quote (entry:25).** `bwrap.1.html:184-186`:
   `<p class="Pp"><b>--clearenv</b></p>` / `<div class="Bd-indent">Unset all environment variables,
   except for <b>PWD</b> and any that are subsequently set by <b>--setenv</b></div>`. Entry text
   matches verbatim after tag-stripping. `SOURCES.md:263` carries the same quote.
2. **Model-card line (entry:65-66).** `hf-model-card.md:145` =
   `model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")`.
   Anchor `README.md:145` equals capture line 145; `SOURCES.md:264` quotes the same line.
3. **K9 assert (entry:54-58, 61).** `test_outputs.py:107` =
   `assert "error" in error_data, "Error response should contain 'error' field"`; `:103` is the
   status-400 assert, so the "two asserts in series" statement holds. Probe K9 stage returns 400
   with `{"detail": "missing text"}` (`plans/round72_c1_hf_probe.py:319-321`), case note and
   frozen vector `K9 … PPPF` (`:157`, `:159-168`).
4. **Nine-variable allowlist (entry:27-29).** `ENV_ALLOW` (`plans/round72_c1_hf_probe.py:99-109`)
   is exactly the nine names in the entry's order; `PYTHONPATH` is `VENV_SITE` =
   `/venv/lib/python3.13/site-packages` (`:95`); `--clearenv` is in the argv (`:497`) and the
   `--setenv` loop follows (`:513-514`). The live receipt line 9 lists the same nine names.
5. **Canary (entry:39).** `R72_CANARY` is exported around the battery (`:113-127`, `:657`), recorded
   by the in-sandbox harness (`:194`), counted (`:610-611`), and required zero by both the battery
   predicate (`:646`) and `--check-receipt` (`:785-787`). Receipt line 9: `canary_seen=0`.
6. **In-sandbox `transformers.__file__` (entry:40).** Recorded by the harness inside the sandbox
   (`:197`); single path and `distinct=1` required (`:607-618`); `--check-receipt` requires exactly
   one `transformers_file=` token starting `/venv/` (`:777-784`). Receipt line 9:
   `distinct=1 transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py`.
7. **`allowlist_seen=9/9` (entry:41).** Computed from per-case `env_keys` supersets (`:612-616`).
   The field is all-or-nothing — it prints 9/9 or 0/9, never a partial count — so it catches a
   dropped `--setenv` (the stated purpose) but is coarser than "every declared variable" suggests.
8. **`env_cleared=True` as a witness (entry:33-38).** *Internal contradiction.* The `PROVENANCE`
   line hardcodes the literal `env_cleared=True` (`:614`), as does `SANDBOX … cleared_env=True`
   (`:605`), and `--check-receipt` only asserts that literal (`:774-776`). The entry's lead sentence
   says "the receipt carries evidence computed inside the sandbox", and the table header is "why it
   is not self-report", yet the first row's own cell says "the probe's own flag". Three of the four
   witnesses (`canary_seen`, `distinct`/`transformers_file`, `allowlist_seen`) are genuinely
   computed inside the sandbox; `env_cleared` is decoration whose only force comes from the canary.
   This does not break the claim — it is a framing overstatement in an otherwise careful table.
9. **"Round 71 named 6 of 19 assert sites; K9 makes it 7" (entry:61).** Confirmed:
   `corpus/lessons/round-71.md:13` ("6 of 19 grader asserts") and `:81` (six priced of nineteen,
   `:107` named as the unreachable one). K9 prices `:107`, so 7/19 follows arithmetically.
10. **"The same injection against the round-71 probe changes the table" (entry:47-48).**
    Supported twice: prior-round `.ufo/waves/round-71/w1/ClaimFalsify71.md:89-94` (a designed stub
    reproduces 8/8 frozen vectors — the stronger, "invisible" result), and the round-72 record
    `corpus/evidence/round72/hf/stub-before-v1.txt` (mtime 23:12:37, `PROBE sha256=d5ce2fa5…` =
    `plans/round71_c1_hf_probe.py`, eight cases, `mismatches=6`, no `PROVENANCE` line,
    `PREDICATE R71-C1 fail`). Note the after-arm the entry asks for — `STUB-CONTROL exposed=False
    vectors_unchanged=True` — is **not yet on disk** (`corpus/evidence/round72/hf/stub-control.txt`
    ls rc 2), so the entry's control expectation is currently an instrument contract, not an
    observed receipt; the before-arm record postdates the entry.
11. **Fixture size (entry:67).** *Contradiction.* "five-file 19 KB fixture" vs
    `corpus/evidence/round71/hf/model` = 5 files, **13,944 bytes (13.6 KiB)**: `config.json` 800,
    `model.safetensors` 9,016, `tokenizer.json` 3,528, `tokenizer_config.json` 329, `vocab.txt` 271.
    The probe pins the same set (`MODEL_FILES = 5` `:84`; `MODEL_TREE_SHA256` `:83` =
    `c5c25767…8944`, which is the on-disk tree's digest and the receipt's `MODEL` line). "Five-file"
    is right; "19 KB" is not supported by any committed byte — the correct figure is ~13.6 KiB.
12. **Receipt-side claims.** The receipt of record (`corpus/evidence/round72/hf/receipt.txt`,
    23:10:16, 3,494 bytes; byte-identical replicate at 23:11:08) carries line 9 exactly as the
    entry's table describes, plus the frozen shape: 9 `VECTOR` lines, all `agree=True` (K1 PPPP,
    K2 PPFP, K3 PPFP, K4 PPPF, K5 PFPP, K6 PFFF, K7 FPPP, K8 FPPP, K9 PPPF),
    `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`,
    `PREDICATE R72-C1 pass`. The entry was written (23:01:58) before this receipt existed; nothing
    in the entry is contradicted by it, and the mechanism claims are confirmed by it.

## 3. Index, both directions

- **Row → file.** `corpus/README.md:96` is
  `| \`knowledge/tb2-hf-model-inference-provenance.md\` | Provenance-witnessed replay … | \`plans/round72_c1_hf_probe.py\`; \`plans/round-72-claims.md\` |`,
  three columns matching the table header at `:27` (`| Entry | Covers | Primary source |`), placed
  immediately after the round-71 row at `:95`. Both cited sources exist on disk. No duplicate row.
- **File → row.** The file exists (6,849 B, 78 lines, sha256 `e384eb34…`) and has exactly one row.
- **Counts (scratch files, removed afterwards).** Rows whose first column is a `knowledge/` path:
  **71** (`grep -oE '^\| \`knowledge/[^\`]+\`'` → 71, `sort -u` → 71). Files in `corpus/knowledge`:
  **72** (`find … -maxdepth 1 -type f -name '*.md'`; no subdirectories, no non-`.md` files).
  Rows without a file: **0**. Files without a row: **1** —
  `knowledge/tb2-torch-tensor-parallel-offline.md` (8,283 B, mtime 2026-11-03 18:34, R66-C1 /
  S183). It is not unmentioned overall — README prose line `765` and the coverage-map bullets
  `:770`, `:779` cite it — but the table row is absent. It predates round-72 w1 artefacts (23:00+)
  and is the same defect class the lane already recorded at `corpus/README.md:81` ("`corpus/knowledge`
  56 files against 55 index rows"). Not fixed here: outside this seat's write scope.
- Counting basis note: `^\|.*knowledge/` matches 73 lines because two table rows cite knowledge
  paths in non-first columns; the 71/72 figures count entry-path rows only.

## 4. Contradictions found, ranked

1. **`admission:` cites a missing file.** `corpus/lessons/round-72.md` `## Gate` (Admission
   status) does not exist (ls rc 2). Severity: medium for auditability — the entry's `hold` cannot
   be checked against its stated record. Likely in flight (claims doc assigns that file to the
   source seat), but it is dangling as committed.
2. **"19 KB" fixture vs 13,944 bytes.** Severity: low–medium. It is a copyable number contradicted
   by the digest-pinned fixture; it does not affect the grader-logic or provenance claims.
3. **`env_cleared=True` presented under "why it is not self-report" while the emitter hardcodes
   it.** Severity: low. The witness chain survives on canary/allowlist/`__file__`; the row's own
   cell concedes the point.
4. **`recheck:` omits the stub control and the do-nothing control** that the entry itself elevates
   to rules. Severity: low–medium. Reproducibility gap, not a false statement; the controls are
   owned by other seats' receipts.
5. Adjacent, not the entry: `corpus/SOURCES.md:264` (S248) records "`10512 bytes, 172 lines`" —
   bytes and hash are right, but the committed capture has **197** newlines (165 non-empty lines).
6. Adjacent, not the entry: one knowledge file lacks an index row (§3).

No contradiction was found in the three claims the item names — the `--clearenv` quote, the
model-card line, and the `:107` assert all resolve to the cited bytes.

## 5. Commands run (exact)

| command | rc | result |
|---|---|---|
| `sha256sum corpus/evidence/round72/sources/bwrap.1.html corpus/evidence/round72/sources/hf-model-card.md` | 0 | `708f56ee…8de7`, `75f17282…8851` — equal to entry/SOURCES |
| `wc -c` on the two captures | 0 | 27,981 / 10,512 — equal to `verified-at:` |
| `grep -n 'clearenv' corpus/evidence/round72/sources/bwrap.1.html` | 0 | lines 184-186, quoted text present |
| `awk 'NR>=143 && NR<=149'` on `hf-model-card.md` | 0 | line 145 = the `DistilBertForSequenceClassification.from_pretrained` line |
| `awk 'NR>=100 && NR<=112'` on the round-52 grader capture | 0 | `:103` status-400 assert, `:107` `assert "error" in error_data` |
| `sha256sum corpus/evidence/round71/hf/instruction.md …/test_outputs.py` | 0 | `29151c5b…dcc1`, `61a686d6…87857` |
| `awk 'NR>=260 && NR<=264' corpus/SOURCES.md \| grep -oE '[0-9a-f]{64}'` | 0 | the four hashes, one occurrence each |
| `python3 -B plans/round72_c1_hf_probe.py --check-receipt corpus/evidence/round72/hf/receipt.txt` | 0 | `DEFECTS n=0` / `PREDICATE R72-C1 pass` |
| `python3 -B plans/round72_c1_hf_probe.py --render-table` | 0 | nine `CASE`/`FROZEN-VECTOR` lines, K1…K9 |
| `python3 -B plans/round72_c2_routed_defects.py --lane <lane>` | 0 | `E1a ok`, `E1b ok`, `E1c ok`, `E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass` |
| `--help` on both scripts | 0 | flag sets match the `recheck:` line |
| `find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` | 0 | 72 |
| `grep -oE '^\| \`knowledge/[^\`]+\`' corpus/README.md` | 0 | 71 rows, 71 unique |
| `comm -23/-13 rows files` | 0 | no dangling rows; one unindexed file |
| `find corpus/evidence/round71/hf/model -type f -printf '%s\n' \| awk …` | 0 | 5 files, 13,944 bytes |
| `ls corpus/lessons/round-72.md` | 2 | "No such file or directory" |
| `ls corpus/evidence/round72/hf/stub-control.txt` | 2 | absent |
| `diff receipt.txt receipt-replicate.txt` | 0 | identical |

## 6. Scratch, writes, tooling

- Scratch `/fast/scratch/hyaku/kengaku-r72/KnowledgeIndexR72/` was created for the two count files
  and removed; verified absent. Two temporary count files were written under `/tmp` and deleted;
  verified absent. No git fixture was created.
- **Self-reported scope deviation.** `python3 -m py_compile plans/round72_c1_hf_probe.py
  plans/round72_c2_routed_defects.py` (rc 0) wrote `plans/__pycache__/round72_c2_routed_defects.cpython-314.pyc`
  and refreshed `plans/__pycache__/round72_c1_hf_probe.cpython-314.pyc` — outside this seat's
  declared write scope. Both are gitignored (`.gitignore:2 __pycache__/`) and
  `git status --porcelain plans/__pycache__` is empty, so no tracked byte changed; the c2 pyc was
  removed at 23:10:5x and reappeared at 23:11:21 while peers were running the same gate (not this
  seat's write). After that, all instrument runs used `python3 -B`.
- `git status --porcelain` at audit time shows `M LOG.md` (another seat's write) and untracked
  round-72 wave/evidence artefacts (`corpus/evidence/round72/hf/`, `.ufo/waves/round-72/*`) — none
  authored by this seat.
- Tooling: nothing installed or upgraded (pacman is host-paused and no tool was needed). No network
  call was made.

## 7. Not asserted

- I did not run the nine-case battery, `--stub-control`, or the do-nothing control; `stub-control.txt`
  and `plans/round-72-claims.md`'s control receipt are not mine to produce. The after-arm of the
  stub control is therefore reported as **contract-only**.
- I did not re-fetch S247/S248, so the HTTP-200 clause in `verified-at:` is unverified by me; only
  the captured bytes (size + sha256) were checked.
- Admission/quality calls (Q13/Q14, `w2`/`falsify` re-read) are not scored here.
- No file under the lane (entry, README, SOURCES, plans, evidence) was modified by this seat.
