# R37RevMutants — the 55 frozen C1 mutants: identity audit + killability

Seat: reviewer, kengaku round 37 wave 1 (hyaku run 8, 2026-10-26). Scope: review every frozen mutant in
`plans/round37_c1_verify.py` against `plans/pkg_gate.py` (freeze digest `ea638822…edd41`): (a) is it the
branch its label names; (b) is it killable by some single-defect fixture under the counter's kill criterion
— (exit code, set of clauses printing `DEFECT`) — or equivalent (no fixture can change the observable
result). Gate, counter, mutant list untouched; all work in scratch, lane read-only.

## 1. Headline answer

**All 55 mutants are the branch their label names, and all 55 are killable. No equivalent mutants.**
Under the frozen kill rule C1 is reachable: 5 mutants are already killed by the frozen round-36 battery
(M01, M05, M40, M47, M54 — matches the freeze control), and the remaining 50 are killed by single-edit
fixtures of the shapes in §4, which I built and ran. Empirical receipt (dev mode, my 64-fixture review
battery, gate at freeze digest):

```
$ python3 plans/round37_c1_verify.py --lane <scratch clone> --battery-dir <review battery> --work $S
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)      # dev mode: expected
exit=0
```

Full output: `R37RevMutants/sweep-full-receipt.txt` (55 `MUTANT … killed by=<fid>` lines). `invalid=0`
also proves every `old` string occurs exactly once in the gate and every mutant compiles — the identity
audit's mechanical half. `renamed_disagree=0` over my fixtures: none keys on a directory name.

## 2. Method

1. Read the frozen claims, the counter (mutant tuples at `plans/round37_c1_verify.py:63-176`), the gate
   (`plans/pkg_gate.py:1-398`) and the frozen spec `plans/pkg-spec-r35.json` (3 registry rows S105–S107;
   entry rules min_quotes=8, min_distinct_locations=8, quote_words [3,25]; 22 quote rows in the genuine
   entry — slack exists).
2. Built a review battery (scratch, `R37RevMutants/battery/`, copied to my report dir): 50 single-edit
   package/line fixtures, one per un-killed branch, each declaring the exact DEFECT set the reference
   prints. The counter's battery check verified all 64 declarations (`wrong=0`).
3. Ran the frozen counter over all 55 mutants; each `killed by=` line below is observed output, not
   inference. Three iterations were needed (§5 records what the first two taught — the masking
   structures are the report's main deliverable for the battery builders).

Environment facts that decide two mutants: host python has no `Bio`; the gate's P10 re-run
(`plans/pkg_gate.py:274-277`) falls back to `uv run --no-project --with biopython==1.85 python3`; uv
0.13.0 is installed and biopython is cached (`uv run … python3 -c "print('ok')"` → `ok`, 0.015 s).

## 3. Identity audit — every mutant is the branch its label names

Gate line numbers at the freeze digest. Counter tuple lines: M01–M43 at `round37_c1_verify.py:63-147`,
M44@150, M45@153, M46@156, M47@158, M48@160, M49@163, M50@165, M51@167, M52@169, M53@171, M54@173, M55@175.

| id | clause | silenced branch (`pkg_gate.py`) | label matches branch |
|----|--------|--------------------------------|----------------------|
| M01 | P1 | :115 `return bool(pins) and not bad` — drops `not bad` (digest-mismatch detection) | yes |
| M02 | P2 | :120 unreadable-receipt early return flips to `True` | yes |
| M03 | P2 | :121 `got == want` digest comparison flips to `True` | yes |
| M04 | P3 | :127 no-`## Located quotes` early return flips to `True` | yes |
| M05 | P3 | :128 `if p.bad_rows:` unparsed-row branch | yes |
| M06 | P3 | :133 `len(texts) >= min_quotes` conjunct → `True` | yes |
| M07 | P3 | :133 `len(locs) >= min_distinct_locations` conjunct → `True` | yes |
| M08 | P3 | :134 `and not short` word-range conjunct → `and True` | yes |
| M09 | P4 | :140 no-parsed-quote early return flips to `True` | yes |
| M10 | P4 | :145 unreadable-capture append | yes |
| M11 | P4 | :147 line-range-outside append | yes |
| M12 | P4 | :149 not-verbatim append | yes |
| M13 | P5 | :156 manifest-absent early return flips to `True` | yes |
| M14 | P5 | :163 unparsed-manifest-line append | yes |
| M15 | P5 | :168 manifest-digest-vs-bytes append | yes |
| M16 | P5 | :172 row-capture-not-pinned append | yes |
| M17 | P5 | :174 manifest-digest-vs-spec-pin append | yes |
| M18 | P5 | :177 quote-capture-not-pinned append | yes |
| M19 | P5 | :181 file-not-covered append | yes |
| M20 | P6 | :189 rows≠1 append | yes |
| M21 | P6 | :193 cells≠11 append | yes |
| M22 | P6 | :197 url-not-pinned append | yes |
| M23 | P6 | :199 tier append | yes |
| M24 | P6 | :201 status append | yes |
| M25 | P6 | :203 used-by append | yes |
| M26 | P6 | :205 teaches-words append | yes |
| M27 | P6 | :208 teaches-distinctness append | yes |
| M28 | P7 | :213 entry-unreadable early return flips to `True` | yes |
| M29 | P7 | :221 source-line append | yes |
| M30 | P7 | :223 verified-at append | yes |
| M31 | P7 | :225 recheck append | yes |
| M32 | P7 | :228 no-Negative-space append | yes |
| M33 | P7 | :230 no-falsifier append | yes |
| M34 | P8 | :235 README-unreadable early return flips to `True` | yes |
| M35 | P8 | :244 index-rows≠1 append | yes |
| M36 | P8 | :246 cites-every-row append | yes |
| M37 | P8 | :251 coverage-bullet append | yes |
| M38 | P8 | :255 files-vs-indexed append | yes |
| M39 | P9 | :263 not-a-worktree early return flips to `True` | yes |
| M40 | P9 | :265 untracked append (`return not left` → `return True`) | yes |
| M41 | P10 | :270 receipt-unreadable early return flips to `True` | yes |
| M42 | P10 | :282 fresh-probe-nonzero early return flips to `True` | yes |
| M43 | P10 | :284 not-byte-equal early return flips to `True` | yes |
| M44 | D4 | :319 file-unreadable early return flips to `True` | yes |
| M45 | D4 | :321 drops the `len(lines) != 1` half of the combined condition | yes |
| M46 | D4 | :321 drops the `startswith(label)` half | yes |
| M47 | D4 | :322-323 pattern collection (`if not re.search(pat, lines[0])]` → `if False]`) | yes |
| M48 | D5 | :333 file-unreadable early return flips to `True` | yes |
| M49 | D5 | :335 drops the `len(lines) != 1` half | yes |
| M50 | D5 | :335 drops the `startswith(label)` half | yes |
| M51 | D5 | :338 missing-require append | yes |
| M52 | D5 | :340 forbidden-token append | yes |
| M53 | D5 | :345 capture-unreadable early return flips to `True` | yes |
| M54 | D5 | :351 digest-not-in-manifest append | yes |
| M55 | D5 | :354 quote-absent append | yes |

M44/M48's `old` strings span the return plus the following `if` line only to disambiguate D4's text from
D5's; the replacement changes only the returned boolean. No mutant touches `run_checks` (:293-301),
`main` (:358-396), argparse, or the P10 `OSError`/`SubprocessError` branch (:280) — grep for those
markers in the counter returns 0 matches, so the freeze's excluded-branch list is respected.

## 4. Killability — observed killing fixture per mutant

Kill rule: mutant's (exit, DEFECT set) differs from the reference on ≥1 fixture. A flip of ONE clause id
inside the set suffices; co-defecting clauses do not block a kill. `r36-*` = frozen round-36 battery;
`rev-*` = my review fixture (construction in `R37RevMutants/battery/*.py`).

| id | killed by (observed) | single-edit construction |
|----|----------------------|--------------------------|
| M01 | r36-P5 | stub probe overwrites a pinned instrument → digest pin fires |
| M02 | rev-m02-receipt-gone | delete the receipt file |
| M03 | rev-m03-receipt-byte | append one byte to the receipt |
| M04 | rev-m04-quote-heading | rename the `## Located quotes` heading |
| M05 | r36-P3 | unparsed quote row beside the genuine rows |
| M06 | rev-m06-dup-texts | set every quote's text to row 0's text (locations kept) |
| M07 | rev-m07-dup-locs | re-point rows ≥7 onto row 0's (capture,start) (texts kept) |
| M08 | rev-m08-short-quote | truncate one quote to its first 2 words |
| M09 | rev-m04-quote-heading | (also rev-m09-no-rows: drop all data rows) |
| M10 | rev-m10-capture-gone | delete a quote-cited capture, keep its manifest line |
| M11 | rev-m11-range-9999 | re-point one quote to `test_outputs.py:9999` |
| M12 | rev-m06-dup-texts | (also rev-m12-text-swap: swap one quote's text) |
| M13 | rev-m13-manifest-gone | delete `SHA256SUMS` |
| M14 | rev-m14-garbage-line | append `zz garbage-line` (names no existing file) |
| M15 | rev-m10-capture-gone | (also rev-m15-capture-byte: append `\n` to a capture) |
| M16 | rev-m16-row-cap-gone | delete `test.sh` + its manifest line + its 3 quote rows |
| M17 | rev-m17-pin-vs-spec | modify a capture byte AND re-pin the manifest to the new digest |
| M18 | rev-m18-ghost-quote | re-point one quote to capture `ghost.py` (absent, unpinned) |
| M19 | rev-m19-extra-capture | add an unstaged-in-manifest capture file (staged for git) |
| M20 | rev-m20-row-missing | delete the S105 SOURCES row |
| M21 | rev-m21-12-cells | APPEND a 12th cell to the S105 row |
| M22 | rev-m22-url | rename the pinned path inside the S105 url cell |
| M23 | rev-m23-tier | tier `A` → `B` |
| M24 | rev-m24-status | status `mined` → `draft` |
| M25 | rev-m25-usedby | used-by cell no longer names the entry |
| M26 | rev-m26-short-teaches | teaches cell → `junk` (1 word) |
| M27 | rev-m27-dup-teaches | copy S105's teaches cell into S106 |
| M28 | rev-m28-entry-gone | delete the entry file |
| M29 | rev-m29-source-line | drop the `source: S105` line |
| M30 | rev-m30-verified-at | verified-at date → `2026-10-24` |
| M31 | rev-m31-recheck | drop the `recheck:` line |
| M32 | rev-m32-no-ns | rename the `## Negative space` heading |
| M33 | rev-m33-no-falsifier | case-insensitive replace of the `falsifi` stem |
| M34 | rev-m34-readme-gone | delete `corpus/README.md` |
| M35 | rev-m35-dup-index | duplicate the entry's index row |
| M36 | rev-m36-index-sid | drop `S106` from the index row |
| M37 | rev-m37-no-bullet | delete the coverage bullet |
| M38 | rev-m28-entry-gone | (also rev-m38-extra-knowledge: add an unindexed knowledge file) |
| M39 | rev-m39-no-git | package directory without `git init` |
| M40 | r36-P6 | untracked leftover file |
| M41 | rev-m41-rerun-receipt-gone | `--rerun` + delete receipt (early return, no probe run) |
| M42 | rev-m42-rerun-probe-exit3 | `--rerun` + probe stub `sys.exit(3)` |
| M43 | rev-m43-rerun-probe-offby | `--rerun` + probe stub printing receipt+`X` |
| M44 | rev-m44-d4-file-gone | `d4-line --file` on an absent file |
| M45 | rev-m45-d4-two-lines | genuine D4 line + a second line |
| M46 | rev-m46-d4-nolabel | genuine D4 line minus the leading `- ` (patterns unanchored) |
| M47 | r36-L2 | labelled line without the directional pattern |
| M48 | rev-m48-d5-file-gone | `d5-line --file` on an absent file |
| M49 | rev-m49-d5-two-lines | genuine D5 line + a second line |
| M50 | rev-m50-d5-nolabel | `Erratum` → `Xrratum` (require token still present) |
| M51 | rev-m51-d5-require | `is present` → `was present` |
| M52 | rev-m52-d5-forbid | append `… wrongly said not present.` (require kept) |
| M53 | rev-m53-d5-capture-gone | delete the D5 capture file |
| M54 | r36-L6 | (manifest line removed, capture bytes intact) |
| M55 | rev-m55-d5-quote-gone | remove the quoted sentence AND re-pin the manifest to the new digest |

## 5. Masking structures the battery builders must respect

These are the non-obvious constructions; each was learned by a fixture that first FAILED to kill:

1. **M16 is masked by M18.** All three r35 row captures are also quote captures (22 quote rows cite
   `test_outputs.py` ×15, `test.sh` ×3, `instruction.md` ×4). Deleting a row capture + its manifest line
   still leaves P5 DEFECT via the quote-capture check (:177). Kill requires also removing that capture's
   quote rows (then P3/P4 stay ok: 19 rows remain ≥ 8/8).
2. **M55 is masked by M54.** Removing the quote from the capture changes its digest; unless the
   quarantine manifest is re-pinned to the new digest, the digest check (:351) keeps D5 DEFECT under the
   mutant. Re-pin, then the quote-absence flip is observable.
3. **M17 is masked by M15.** The two checks are complements: manifest≠bytes (:168) and manifest≠spec pin
   (:174). To isolate M17 the manifest must match the (modified) bytes while differing from the spec pin.
4. **M14 is masked by M16/M19.** An unparsed manifest line removes a name from `pinned`; if that name is
   a row/quote capture or an existing file, another append fires. The garbage line must name nothing.
5. **M21 is masked by IndexError.** Dropping a cell makes `cells[10]` raise → clause-error → still
   DEFECT. Only a 12th cell APPENDED at the end flips P6.
6. **M06/M07 need the 22-row table's slack** (min 8/8). r36's `mut_duplicates` (row 0 copied 8×) kills
   NEITHER: texts=1 and locs=1 fail both conjuncts, so each mutant still defects. M06 must duplicate a
   text across distinct locations; M07 must collapse locations while keeping ≥8 distinct texts.
7. **M33's falsifier is capitalized.** The stem occurs once, as `Falsifier`; a case-sensitive replace
   leaves the `(?i)` regex matching (my first attempt produced an ACCEPT, rc=0). Replace
   case-insensitively.
8. **P9 hygiene.** Edits must land before `git_add` or P9 co-defects (untracked) — harmless for the kill
   but it dirties the declared set (bit me on m19/m38).
9. **P10 stubs co-defect P1** (the stub overwrites a pinned instrument) — fine: the set still differs.

## 6. Environment-dependence and freeze limits

- **M42/M43 are host-conditional, not equivalent.** Their branches (:282/:284) are reachable only when
  the probe actually runs. On this host (no `Bio`, uv 0.13.0 + cached biopython) it does. On a host with
  neither Bio nor a working `uv run --with`, every P10 run defects via the excluded OSError branch
  (:280) and M42/M43 become unkillable *in that environment* — M41 stays killable regardless (early
  return at :270 precedes any probe run). The C1 predicate is measured on the canonical host; if the
  landing host differs, re-check M42/M43 first.
- **M41/M42/M43 need `--rerun` fixtures.** No frozen r36 fixture passes `--rerun`; without a battery37
  `--rerun` fixture all three survive (this is why they survived at freeze).
- **Probe cost.** Each `--rerun` fixture runs the probe once per gate invocation that reaches it; stub
  probes (exit-3 / off-by-one) are instant and deterministic, so the battery need not run the genuine
  probe at all.
- Frozen limit stands (claims §C1): demonstration is observational — a fixture shows the branch is
  reached and its result visible — not that each check is the right check.
- My battery is a review artifact (scratch), not the landing battery; the constructions are copied to
  `R37RevMutants/battery/` for the battery seat to reuse. Two earlier sweeps are superseded: sweep 2
  (killed=54) lacked the M08 FIXTURES entry and had a stale m16 declaration; sweep 1 (killed=52) also
  had the m55 manifest-newline bug. The final receipt above is the record.

## 7. Receipts (this report dir)

- `R37RevMutants/sweep-full-receipt.txt` — full counter output of the final sweep (sha256
  `b7837da7…65d29`).
- `R37RevMutants/mutant-sweep-lines.txt`, `R37RevMutants/fixture-lines.txt` — extracted MUTANT/FIXTURE lines.
- `R37RevMutants/battery/{a_pkg_mutants,m_line_mutants,z_p10_mutants}.py` — the 50 review fixtures
  (sha256s `b884a2eb…`, `1db27d9d…`, `0aa2525a…`).

Scratch `/fast/scratch/hyaku/kengaku-r37/R37RevMutants` removed after receipt copy. No lane file was
edited; no git state was touched.

VERDICT: mutants-55/55-equivalent-0
