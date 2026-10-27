# R44S134Erratum — closure R2: draft appended erratum for the S134 source span

Seat: `R44S134Erratum` (scribe, round 44 v2 wave, 2026-10-26). Lane measured: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (working tree clean for every file cited below). No lane file was
edited: the entry is append-only and the L1 owns the landing.

## 1. The routed item under test

`corpus/lessons/round-43-verifier-spotcheck.md:163-165`, verbatim:

> **R2 — anchor mismatch on S134.** The entry's `source:` line says `README.md` "lines 1-34", while the row anchor and
> Gate quote are at `:1-35`/`:35` (the file lacks a final newline). Append an erratum to the entry.

Target: `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (437 lines, sha256
`2e085f69030f29730e51691f851978954995101a48d5164192919306cf9e0854`, equal to `git show HEAD:` of the same path).

## 2. Measurements (read-only)

Capture directory `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`; full command/output log in
`R44S134Erratum/measure-receipt.txt` (sha256 `ea204221…c961`).

| measurement | command | output |
|---|---|---|
| README newline-terminated lines | `wc -l corpus/evidence/round43/.../README.md` | `34` |
| README lines, last one unterminated | `awk 'END{print NR}' …/README.md` | `35` |
| README lines (`grep -c ''` cross-check) | `grep -c '' …/README.md` | `35` |
| README size | `wc -c …/README.md` | `1603` |
| README final byte | `tail -c 1 …/README.md \| od -An -c` | `   t` (no `\n`) |
| line 35 (exists) | `sed -n '35p' …/README.md` | `4. Confirms the attack completes within the time limit` |
| line 36 (absent) | `sed -n '36p' …/README.md \| od -An -c` | empty |
| README digest | `sha256sum …/README.md` | `887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f` |
| manifest pin | `grep -n README …/SHA256SUMS` | `2:887407c7…5cb24e7f  README.md` |
| capture manifest | `(cd … && sha256sum -c SHA256SUMS)` | 12/12 `OK`, `rc=0` |
| fresh upstream fetch | `curl -fsS -o scratch/README.upstream.md <pinned raw URL>` | `http=200 bytes=1603`; same sha256; `cmp` identical (exit 0); `wc -l` 34, `awk NR` 35, last byte `t` |
| entry source line | `grep -n S134 <entry>` | `6:source: S134 — …README.md — the authors' own README for this task, lines 1-34, …` |
| entry's own `:35` citations | `grep -on 'README\.md:[0-9]*…' <entry>` | `42:README.md:35`, `148:README.md:35`, `186:README.md:35` (plus `:368` for a different project's README) |
| SOURCES row | `grep -n '^| S134 ' corpus/SOURCES.md` | `149:… README.md:1-35, :35 "Confirms the attack completes within the time limit" (8 words); sha256 887407c7…` |
| sibling: `feal.c` | `wc -l` / `awk NR` / `tail -c 1` | `99` / `100` / `}` (also unterminated) |
| SOURCES row S132 | `grep -n '^| S132 ' corpus/SOURCES.md` | `147:… feal.c:1-100, :66 "…" (7 words)` — while the entry's `source:` says `lines 1-99` |

**R2 confirmed, exactly as routed.** The capture has 35 lines; `wc -l` = 34 only because line 35 is unterminated
(`grep -c ''` and `awk 'END{print NR}'` both 35, `sed -n '35p'` prints it). The entry's `source:` line therefore
undercounts the file extent by its last line, and it disagrees with both the S134 row anchor (`corpus/SOURCES.md:149`)
and the entry's own citations of `README.md:35` at `:42`, `:148`, `:186`. The capture's bytes and digest are
unchanged and the fresh fetch is byte-identical, so nothing but the span sentence is in question.

## 3. Proposed appended text (exact — L1 appends at end of file)

File: `R44S134Erratum/proposed-erratum.md` (sha256 `98d8cb…2934`, 2546 bytes; begins with one blank line). This is the
recommended full form, because the same measurement found the identical defect on S132:

```markdown
## Errata (round 44, closure R2: source-span counting; nothing above edited)

Appended 2026-10-26 (round 44, one v2 wave, closure item R2). Every number below was measured on the pinned capture
in this lane (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`, `sha256sum -c SHA256SUMS` → 12/12
`OK`) and re-checked against a fresh fetch of the pinned raw URL (HTTP 200, 1603 bytes, `cmp` identical); the
commands and their output are filed with `.ufo/waves/round-44/wave/R44S134Erratum/`. Both errata are provenance-only:
no predicted, observed or `regrade` value, DECISIVE line, requirement label, Mechanism row or quote changes. A sweep
of the 19 `source:` lines in `corpus/knowledge/*.md` that carry a `lines A-B` against their `corpus/SOURCES.md` row
finds these two as the only disagreements (15 agree, 2 whose row carries no span for that file).

| `source:` line | as filed | measured lines | SOURCES row anchor |
|---|---|---|---|
| S132 `feal.c` | "lines 1-99" | **100** (`wc -l` 99; last byte `}`) | `feal.c:1-100` (`corpus/SOURCES.md:147`) |
| S134 `README.md` | "lines 1-34" | **35** (`wc -l` 34; last byte `t`) | `README.md:1-35` (`corpus/SOURCES.md:149`) |

**Erratum (round 44): S134's span is `README.md:1-35`, not "lines 1-34".** The pinned `README.md` is 1603 bytes with
**no final newline** (last byte `t`, `tail -c 1 README.md | od -An -c`), so `wc -l` prints 34 while
`awk 'END{print NR}'` and `grep -c ''` both report 35 and `sed -n '35p'` prints
`4. Confirms the attack completes within the time limit`. The `source:` line counts newline-terminated lines only, so
it undercounts the file's extent by its last line and disagrees with the S134 row anchor and with this entry's own
citations of `README.md:35` (`:42`, `:148`, `:186` — the Located quotes row "the authors claim the test enforces the
time limit"). Read S134's span as `README.md:1-35`. The capture, its digest
`887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f` (`SHA256SUMS:2`, `plans/pkg-spec-r43.json`
`rows.S134`) and every quote above are unchanged.

**Erratum (round 44): S132's span is `feal.c:1-100`, not "lines 1-99".** Same defect, same measurement: the pinned
`feal.c` ends with an unterminated last line (`wc -l` 99, `awk 'END{print NR}'` 100, last byte `}`) and the S132 row
anchor at `corpus/SOURCES.md:147` already reads `feal.c:1-100`. Read the span as `feal.c:1-100`; no citation of
`feal.c` in this entry falls on `:100` (the highest is `:88`), so no finding, case or Gate quote rests on the
undercounted line.
```

Minimal variant, if the L1 prefers R2 exactly as routed (S134 only):
`R44S134Erratum/proposed-erratum-minimal.md` (sha256 `a69c39…ef6`).

Both variants are append-only, sit after the existing `## Errata (round 43, …)` section, keep the entry's heading
style, and mention no new S id (so `V9(b)`/`P7` source-line counting is untouched).

## 4. Gate and counter neutrality (A/B on scratch clones, under the round-44 envelope)

Two `git clone -q --shared` copies of the lane at `5e3d3aa0` (toplevel asserted as the clone path): `lane2` =
baseline, `lane` = the proposed text appended to the entry. The frozen `pkg_gate.py` was run with an *effective*
spec (the counter's own construction: `receipt_sha256` filled, `plans/round43_c2_verify.py:148`), P1–P8:

```
ENVELOPE start 20:37:56 … (baseline lane2)
P1 ok pinned=2 mismatched=0 / P2 ok receipt_sha256=pinned / P3 ok rows=18 … / P4 ok checked=18 bad=0
P5 ok manifest_entries=12 bad=0 / P6 ok rows=6 bad=0 / P7 ok source_lines=6 bad=0 / P8 ok index_rows=50 … bad=0
defects=0
ENVELOPE end 20:37:57 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

ENVELOPE start 20:37:59 … (appended lane)
… identical P1–P8 lines …
defects=0
ENVELOPE end 20:38:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`diff` of the two clause blocks: empty (`IDENTICAL-CHECKS`). Receipts: `R44S134Erratum/gate2-baseline.txt`,
`gate2-appended.txt`.

Full round-43 predicate on the appended clone (`V1`–`V10`, including `P10`'s fresh probe re-run and the entry-content
checks `V7`, `V9`, `V10`):

```
ENVELOPE start 20:39:01 cwd=…/R44S134Erratum
V1 ok listed=12 bad=0 extra=0
    gate: P1…P10 ok, gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=6 bad=0
V4 ok cases=12 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=5 tags=5 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=12/12 bad=0
V10 ok mechanism_rows=12/12 bad=0
checks=10 defects=0
PREDICATE C2 pass
ENVELOPE end 20:40:40 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Receipt: `R44S134Erratum/counter-appended.txt`. So the proposed append flips no gate clause and no counter check; the
predicate that guards this entry still passes with it in place. (The baseline clone was not re-run through the whole
counter; a pass is not a comparison, and the gate A/B above isolates the append.)

## 5. Findings

1. **R2 reproduced and quantified.** README `1603` bytes, 35 lines, no final newline; `source:` "lines 1-34" vs row
   anchor and quotes at `:35`/`:1-35`. Fix is a provenance erratum, not a re-source: capture bytes, manifest and spec
   pin all unchanged.
2. **The same defect exists on S132 in the same entry** (`feal.c` "lines 1-99" vs `corpus/SOURCES.md:147`
   `feal.c:1-100`; capture `wc -l` 99 / `awk NR` 100, last byte `}`). Recommending the two-item erratum (§3 full
   form) rather than S134 alone; the minimal variant is supplied if the L1 wants R2 exactly.
3. **Corpus-wide sweep.** Of the 19 `source:` lines in `corpus/knowledge/*.md` that carry a `lines A-B` and match a
   span in their `SOURCES.md` row for the same file, 15 agree, 2 mismatched — both in this entry — and 2 have no row
   span (`R44S134Erratum/spans.py`, output in `measure-receipt.txt` §6). The defect is local, not systemic.
4. **A raw gate run reds P2 for a reason unrelated to this entry.** `plans/pkg-spec-r43.json` (and
   `pkg-spec-r44.json`) pin `"receipt_sha256": null` since the round-43 freeze commit `02753f2`; both counters fill
   it before invoking the gate (`round43_c2_verify.py:148`, `round44_c2_verify.py:141`). Running
   `pkg_gate.py package --spec plans/pkg-spec-r43.json` directly therefore reports
   `P2 DEFECT receipt_sha256=8c9874…7b4` with `defects=1`. That is the harness's construction, not a package defect;
   with the effective spec the same tree is `P2 ok … defects=0` (§4). Recorded so the L1 does not misread a direct
   gate run at landing.

## 6. Touched surfaces

Writes, all inside the wave area: this report and
`.ufo/waves/round-44/wave/R44S134Erratum/{proposed-erratum.md, proposed-erratum-minimal.md, measure-receipt.txt,
spans.py, gate2-baseline.txt, gate2-appended.txt, counter-appended.txt}` (32 KB total; no file over 1 MiB). Nothing in
`corpus/`, `plans/`, `SCORECARD.md`, the lane's git/jj state, or any PATH directory. Scratch
`/fast/scratch/hyaku/kengaku-r44/R44S134Erratum` (two shared clones + probe work) is deleted at the end of the seat.

## 7. Not done / out of scope

- No edit to the entry (scribe seat; append-only erratum is the L1's to land), to `corpus/SOURCES.md`, or to the
  `recheck:` line of the entry — the span is not part of that line's command.
- The round-44 C2 counter was not run: it targets `tb2-feal-linear-cryptanalysis-grader.md`, not this entry.
- No probe re-run beyond the counter's own `P10`/`V5`; no network beyond the one pinned raw `README.md` re-fetch.
- No claim about `feal.h` (also unterminated, 16/17) or any other capture: neither is a row nor cited by the entry.

## 8. Known limits

- The lane tip measured is `5e3d3aa0`, not the round-44 claims' baseline `0cb2e225`; every cited file (entry, SOURCES
  row, spec, capture, manifest) is byte-identical to `HEAD` (`git status --porcelain` empty for those paths).
- The sweep (§5.3) compares only `source:` lines shaped `source: S<id> — <URL> … lines A-B`; it does not audit spans
  stated in prose elsewhere.
- The erratum quotes the entry's `:42`, `:148`, `:186` citations by line number at tip `5e3d3aa0`; appending does not
  shift them, but any later edit above them would.

Artifacts: `.ufo/waves/round-44/wave/R44S134Erratum/` (7 files, listed in §6) and this report.

VERDICT: s134-erratum-drafted
