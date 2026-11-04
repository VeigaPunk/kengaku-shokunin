# C2RowFixR73 — two registry-cell corrections

Axes: coverage and calibration. Draft only; no lane SKILL.md or instrument was edited by this seat.

## Reproducible input

The final mirror is the complete archive of freeze revision `255c261db2119906c70195291a2b6f9f46f82a72`, extracted under `/fast/scratch/hyaku/kengaku-r73/C2RowFixR73`. Only its SKILL.md lines 600 and 682 were edited. This is a measured draft, not a claim about the eventual landing tip.

Extraction command (rc 0; no stdout/stderr):

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 255c261db2119906c70195291a2b6f9f46f82a72 | tar -x -C /fast/scratch/hyaku/kengaku-r73/C2RowFixR73
```

## 1. sources-adopt: exact verdict-map cell

Before:

```text
`0` gates an append and prints the append block · `2` usage error or unreadable quote artifact · `3` staged/registry id collision · `4` malformed staged row (escaped pipe, column count, quote spans) · `5` requested id absent · `6` quote over the 25-word cap · `7` quote absent from artifact bytes · `8` quote bound to a mismatched URL · `9` quote has no url-map entry
```

After (all existing descriptions preserved):

```text
`0` clean: gates an append and prints the append block · `1` failed: selftest case failure · `2` could-not-evaluate: usage error or unreadable quote artifact · `3` failed: staged/registry id collision · `4` failed: malformed staged row (escaped pipe, column count, quote spans) · `5` failed: requested id absent · `6` failed: quote over the 25-word cap · `7` failed: quote absent from artifact bytes · `8` failed: quote bound to a mismatched URL · `9` could-not-evaluate: quote has no url-map entry
```

Class basis: fleet PROTOCOL.md §Gate standard maps 0 to clean, 1 to failed, and other codes explicitly to clean/failed/could-not-evaluate. Source references below are `plans/sources_adopt.py` in the freeze archive:

- Line 50: `EXIT_OK = 0`; lines 240, 569 and 1079 return it after evaluated checks succeed → clean.
- **Code 1 really exists:** lines 965–969 compute failed selftest cases and execute `return 1` when any fail. Lines 1015–1016 route `--selftest` to `return selftest()`, and line 1083 raises `SystemExit(main(sys.argv[1:]))`. Thus adding 1 is justified by an explicit return, not an invented conventional failure code. The failure arm was inspected, not induced in this task.
- Line 51: `EXIT_QUOTE_UNREADABLE = 2  # same class as argparse usage errors: caller/env, not bytes`; lines 480, 487 and 1029 return it for unavailable inputs; parser.error calls also exit 2 → could-not-evaluate.
- Lines 230–234 return collision/malformed codes 3/4 after inspecting staged rows → failed.
- Lines 235–239 set `missing = [row_id for row_id in want_ids if row_id not in ids(staged)]` and `return EXIT_REQUEST, report`; lines 1068–1070 likewise return 5 for absent requested rows. This is an evaluated failure of the requested package-membership condition → failed, not a failure to read/evaluate the package.
- Lines 559–568 return 4/6/7/8/9 according to the accumulated malformed/overlong/absent/mismatch/unmapped findings. Codes 6/7 fail the quote-length/presence conditions; 8 fails citation binding → failed.
- **Code 9 is not a bad-citation verdict:** lines 423–425 explicitly distinguish an unmapped artifact as a gap in the caller's map from a capture of a different document; lines 434–435 return `"unmapped", ""` when no containing capture is mapped. Line 958 says `# an unmapped artifact is a gap in the caller's map, never a byte verdict`. The comparison cannot establish citation binding → could-not-evaluate.

## 2. round62-c1-class-survey: exact kind cell

Before:

```text
census gate
```

After:

```text
gate
```

It is a **gate**, not a probe: `plans/round62_c1_class_survey.py:264` executes `code = 0 if verdict == "pass" else 1`, after line 263 derives pass/fail from invariants and determinism, and main returns that code at line 375.

The setup return 2 at line 258 does not make the instrument a probe. Its noun “survey,” read-only default, and the registry's historical “probe form” prose describe execution shape, not whether it can fail.

## 3. Measured audit transcripts

Both commands ran from `/fast/scratch/hyaku/kengaku-r73/C2RowFixR73`, with the instrument bytes unchanged.

Before the two edits:

```console
$ python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C2RowFixR73
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 defect n=2
  DEFECT `sources-adopt`:gate-verdict:0,2,3,4,5,6,7,8,9
  DEFECT `round62-c1-class-survey`:kind:census gate
D3 ok n=0
D4 ok n=0
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
```

Exit code 1; stderr empty.

After the final exact cell text above (including explicit selftest code 1):

```console
$ python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C2RowFixR73
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
```

Exit code 0; stderr empty. An intermediate draft without the explicit selftest code 1 produced the identical green output and rc 0; the final rerun above prices the completed cell, not that intermediate text.

**Third audit defect:** none reported: every D1–D4 count is zero on the final 106-row mirror. This is not proof that the audit checks each class semantically: its D2 implementation only requires gate code 0 plus code 1 or a failure keyword. The source-based code-9 distinction above matters even though an indiscriminate `3`–`9` failed range also satisfies that structural check.

## Rejected readings

- “Add 1 just because gates conventionally fail with 1”: rejected; only the actual selftest return at line 969 justifies the added cell item.
- “Never add 1 because normal adoption branches only return 0,2–9”: rejected; the advertised selftest mode really returns 1 on case failure.
- “Every nonzero refusal is failed, including 2 and 9”: rejected; 2 denotes caller/environment inability, and 9 explicitly denotes a caller-map gap rather than a citation mismatch.
- “5 is could-not-evaluate because the request is wrong”: rejected; the package was read and its requested membership predicate was evaluated false, unlike unreadable input or missing binding evidence.
- “The census is a probe because its default is read-only”: rejected; the explicit 0/1 verdict at survey line 264 decides its kind.
- “Keep census gate as a descriptive kind”: rejected; PROTOCOL's registry enum is gate|probe; descriptive purpose belongs in prose.

## Moving-tree observation and boundaries

An initial `git archive HEAD` raced with lane integration: the extracted archive already contained 114 rows and the draft `3`–`9` failed range plus kind=gate. Its audit returned rc 0 with `INSTRUMENTS total=114 derived=registry rows=114`, `PARSED scripts=114 failed=0`, all four legs zero, `MISMATCH 0`, `DEFECTS n=0`, and `PREDICATE R73-C2 pass` (stderr empty). That archive was discarded; it is not the 106-row after-state proof. No landing hash is claimed. The pinned freeze archive above removes the moving-HEAD ambiguity.

No builds, linters, formatters, selftest batteries or mutants were run. Only the expressly assigned audit runs were executed. No installation, subprocess delegation, fixture git mutation, or credential read occurred. LSP is unavailable in the mounted tool inventory; definitions/returns were located with text reads. Scratch is removed after retaining this evidence and the exclusive report.
