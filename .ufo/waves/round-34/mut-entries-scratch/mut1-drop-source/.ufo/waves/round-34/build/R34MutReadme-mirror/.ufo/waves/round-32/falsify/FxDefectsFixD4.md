# FxDefectsFixD4 — SKILL.md §Gate/probe registry row for `plans/sources_adopt.py`

Seat: `L1Kengaku32.FxDefectsFixD4` (leaf reviewer). Date: 2026-10-25.

## Scope

Planned D4 repair (C2/R4): the `SKILL.md` §Gate/probe registry row for
`plans/sources_adopt.py`. I read the frozen claims
(`plans/round-32-claims.md:67-68`, R4), the counter `plans/round32_defects.py`
(`check_r4`, lines 116-131), the on-disk row draft (`SKILL.md:573`, raw), the
build drafts (`R32DraftMistakes.md` D4 row, `R32RevFixes.md`, `R32MutCounters.md`
R4 escape matrix), and the tool itself (`plans/sources_adopt.py`, argparse 974-1013,
exit constants 50-58, selftest 621-970). No production edits; scratch under
`/tmp/r32f-FxDefectsFixD4/`. No tools installed (python3 only; nothing else needed).

## 1. R4 heading condition — PASSES on the working tree (verified by executing the check)

Ran the counter's own `check_r4` against the current tree
(`python3 -c` importing `round32_defects`):

```
R4: ''                                        # no defect string -> check passes
match at char 44284                           # first re.search hit of plans/sources_adopt\.py
heading: ## Gate/probe registry (PROTOCOL §Gate standard)
```

- First match of `plans/sources_adopt\.py` is the table row at `SKILL.md:573`
  (grep: exactly one hit in the file, line 573).
- The last `^#{1,4}\s+\S` heading before that offset is `SKILL.md:560`
  `## Gate/probe registry (PROTOCOL §Gate standard)` — matches the regex and
  carries `(?i)(gate|probe|registry)`. `check_r4` therefore returns `""`.
- Working-tree state: `M SKILL.md` (uncommitted); at baseline tip `f20a1097`
  and at `6084cd3` the row is absent (`R32DraftMistakes.md:178-181`:
  `git show 87f0d32:SKILL.md | grep -c sources_adopt` → 0). The repair is the
  planned uncommitted state; once committed, R4 closes.

So the D4 heading criterion is satisfied by the drafted row.

## 2. Row text on disk (SKILL.md:573, raw, verbatim)

```
| `sources-adopt` | gate | `python3 plans/sources_adopt.py` (lane root; `--registry`, `--package`, `--admit-ids`, `--entries`, `--access-date`, `--recheck`, `--scope-to-admit`, `--attest-opened`, `--quote-file`, `--artifact`, `--url-map`, `--out`, `--expect`) | `0` gates an append (new rows, entry list, recheck cadence, opened attestation, quote-location pins) and prints the append block · `1` gate console or malformed input (missing args, unknown ids, bad dates) · `2` usage error · `8` quote-mode URL/artifact mismatch · `9` quote-mode unmapped artifact | `python3 plans/sources_adopt.py --selftest` (registry/package/expect shapes, quote-location pins, misused flags) | committed lane registry `corpus/SOURCES.md`, staged package `SOURCES.append.md`, pinned captures under `.ufo/waves/round-32/assimilation/captures/` | read-only toward corpus bytes; writes only under `--out`; quote-mode reads artifact + url-map; no network | kengaku |
```

## 3. Findings against the drafted row text

**F1 (medium) — entry column lists a nonexistent flag `--expect`.**
`grep expect plans/sources_adopt.py` → no match; the argparse block (lines
974-1013) and the executed usage line define exactly:
`--selftest --registry --package --admit-ids --entries --access-date --recheck
--out --quote-file --artifact --url-map --attest-opened --scope-to-admit`.
`--expect` is the receipt flag of `plans/adoption_check.py` (C1), not this gate.
A reader following the row would pass a flag argparse rejects (exit 2).
Recommendation: drop `--expect` from the entry column.

**F2 (medium) — verdict map does not match the tool's exit codes.**
Constants at `sources_adopt.py:50-58`: `EXIT_OK=0`, `EXIT_QUOTE_UNREADABLE=2`,
`EXIT_COLLISION=3`, `EXIT_MALFORMED=4`, `EXIT_REQUEST=5`,
`EXIT_QUOTE_TOO_LONG=6`, `EXIT_QUOTE_ABSENT=7`, `EXIT_URL_MISMATCH=8`,
`EXIT_URL_UNMAPPED=9`. Exercised:
- no args → argparse `error:` exit 2 (probed);
- `--url-map` without `--quote-file`/`--artifact` → exit 2 (probed);
- staged/registry id collision → `collisions: S900`, exit 3 (probed);
- requested id absent → `missing: S999`, exit 5 (probed);
- malformed staged rows (escaped pipe, 12 columns, no-quote/unbalanced-quote
  spans) → `EXIT_MALFORMED` 4 (selftest case 5 PASS);
- quote over the 25-word cap → 6 (case 11 PASS); quote absent from artifact
  bytes → 7 (case 12 PASS); URL mismatch → 8, unmapped → 9 (cases 16/17 PASS).

The draft row's "`1` gate console or malformed input (missing args, unknown
ids, bad dates)" is wrong on every clause: no normal-mode path ever exits 1
(1 is only the selftest failure exit); missing args/bad dates exit 2; malformed
rows exit 4; unknown ids exit 5. Exits 3/4/5/6/7 are unlisted.
Recommendation: replace the map with the accurate set.

**F3 (minor) — self-test column omits the case count.**
Measured: `python3 plans/sources_adopt.py --selftest` →
`SELFTEST cases=17 failed=0`, exit 0 (17 named cases, matching the round-31
gate receipt `sources_adopt: SELFTEST cases=17 failed=0` in
`R32DraftMistakes.md:29`). The row says "(registry/package/expect shapes,
quote-location pins, misused flags)" — add the count; "expect shapes" is not
anything this selftest exercises (no expect fixture exists in it).

**F4 (cosmetic) — "staged package `SOURCES.append.md`" is a name, not the
actual input.** The wave's staged package lives outside the repo
(`--package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` per
`R32GateBlock.md:20`); `corpus/SOURCES.append.md` does not exist on disk.
Recommendation: keep the descriptive name (matches other rows' generality) or
name the real staged path; not a correctness blocker for R4.

Everything else in the row checks out: purpose column matches `main()`
behavior (append gate + printed/written block); write-scope column matches the
code (only `--out` write at `sources_adopt.py:1074-1076`; quote mode reads
artifact + url-map; no network); owner kengaku matches all sibling rows.

## 4. Proposed row text (as I would land it)

```
| `sources-adopt` | gate | `python3 plans/sources_adopt.py` (lane root; `--registry`, `--package`, `--admit-ids`, `--entries`, `--access-date`, `--recheck`, `--scope-to-admit`, `--attest-opened`, `--quote-file`, `--artifact`, `--url-map`, `--out`) | `0` gates an append (new rows, entry list, recheck cadence, opened attestation, quote-location pins) and prints the append block · `2` usage error or unreadable quote artifact · `3` staged/registry id collision · `4` malformed staged row (escaped pipe, column count, quote spans) · `5` requested id absent · `6` quote over the 25-word cap · `7` quote absent from artifact bytes · `8` quote bound to a mismatched URL · `9` quote has no url-map entry | `python3 plans/sources_adopt.py --selftest` (17 cases: registry/package shapes, quote-location pins, URL-binding verdicts, misused-flag guards; temp copies) | committed lane registry `corpus/SOURCES.md`, staged package `SOURCES.append.md`, pinned captures under `.ufo/waves/round-32/assimilation/captures/` | read-only toward corpus bytes; writes only under `--out`; quote-mode reads artifact + url-map; no network | kengaku |
```

The clause "once inserted under that section, R4's heading condition passes" is
verified for both the current draft and the proposed text (same first-match
offset, same heading).

VERDICT: d4-closable
