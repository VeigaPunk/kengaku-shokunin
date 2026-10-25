# R33 C1 counter falsifiers — exploit table

**Reviewer:** R33C1Counter (UFO-FSD critic, leaf).
**Lane:** kengaku-shokunin @ 7895588 (freeze f0b20aea + c227e486); worktree snapshot 2026-10-25.
**Baseline:** on the snapshot, `adoption_check.py --expect ... --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0; `round33_c1_verify.py --lane .` → `checks=8 defects=0`, exit 0; selftest green. All labs in `/tmp/r33-counter/<variant>/kengaku-shokunin`, census root = variant dir.

## Exploit table

| Exploit | `adoption_check` (frozen counter) | `round33_c1_verify` | Conjunction |
|---|---|---|---|
| X1 39B stub (3 `source:` lines, no `verified-at`) | prints full green line, **exit 1** (only `verified_at_ok` fails) | V1 V2 V3 V5 red | caught |
| X1 63B stub (3 `source:` lines + `verified-at: 2026-10-25`) | prints full green line, **exit 0** | V2 V3 V5 red | caught (only by second counter) |
| X2 S103 registry row URL → different repo (`totally-different-org/other-repo`) | green line, **exit 0** | V2 red | caught |
| X3 S104 pin `2412.05579` removed from entry | green line, **exit 0** | V2 V3 red | caught |
| X7 round-33 lesson renumber map stripped | n/a | V7 red | caught |
| X8 S094 refusal row fully overwritten in place (mined + usedby) | green line, **exit 0** | V8 red | caught |
| X8b S094 refusal row: only `teaches` cell gutted (anchor/status/source kept) | n/a | **V8 green, checks=8 defects=0**; census green | **UNCAUGHT** |
| X2c S103 line repointed to a different file in the same repo (`rewards.py` instead of `evaluation/main.py`, same URL + same pin prefix) | green line, **exit 0** | **checks=8 defects=0** | **UNCAUGHT by counters** |

## Findings

1. **The frozen counter `adoption_check.py` alone is fully gameable by the original 63-byte stub** — the round-31 comment's fix intent is not realized. The 63B stub (`source: S093/S103/S104` + `verified-at: 2026-10-25`) passes every check (`ids_ok` compares declared ids to the *expect file's* list, not to any registry or document), prints the exact frozen line, exits 0. C1 only survives because the *second* counter (`round33_c1_verify.py`) reads the literals.

2. **V8 guards the wrong cell.** `round33_c1_verify.py:168` reads `teaches = row[5]`, but the registry header is `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` — `row[5]` is **anchor**, `row[6]` is teaches. The four refusal rows' anchor cells happen to contain "refused"/"rejected", so `re.search(r"(?i)(rejected|refus|duplicate|staged)", teaches)` passes regardless of the substantive teaches narrative. A refusal row whose teaches cell is rewritten in place (e.g., erasing "staged wording misstated the executed tolerance..." / "REJECTED: duplicate id; flip:") passes V8 and census. The *record* that justified the renumber is unguarded.

3. **Counter-level identity binds repo, not document.** V2 compares the registry source cell's URL host+path against the entry's `source:` line; V3 checks only the 8-char pin prefixes. The specific file path (anchor cell, e.g. `tasks/finalpool/ab-testing/evaluation/main.py`) is read by neither. Repointing the entry's S103 line at `tasks/finalpool/ab-testing/rewards.py` in the same repo, same commit prefix → both counters exit 0. The kill rule's quote-location gate (`sources_adopt.py`, exit 6–9) is the only thing that would refuse this, but it is an admission-flow step, not part of the frozen predicate's two commands.

4. **Spoofable print vs exit.** The seven-field line prints unconditionally before the `ok` combination; the exit decision adds `ids_ok && duplicates_ok && opened_ok && index_shape_ok && verified_at_ok && census`. A consumer grepping the literal frozen print string (which is itself quoted in the frozen predicate sentence) is fooled by every red run that still prints green.

## Code-path trace: can `entries=1 … census=ok` print while the entry still cites S094/S097?

Yes — the green **print** reproduces; the **exit** cannot be 0 without also editing the expect file/control receipt.

Repro (`x6-cite-refused`): entry `source:` lines reverted to S094/S097 (refused ids), registry rows S094/S097 flipped in place to `status=mined` + `used-by=corpus/knowledge/benchmark-grader-semantics.md` → prints `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 1.

Path: `present/indexed` (entry file + README row) are id-independent; `cited` comes from `SOURCE_LINE_RE` over the entry text (S093/S094/S097); `rows_present=3` because the refusal rows still exist as rows; `rows_mined=3` only because of the in-place status flip; `usedby_ok=1` only because of the in-place usedby flip; `verified_at_ok=1`; `ids_ok=0` solely because `set(declared) != set(expect.sources)` (S094/S097 vs S103/S104). Exit 1 comes only from `ids_ok`. To also get exit 0, the expect file would need S094/S097 — which V6 pins via `expect_sha256` in the control receipt, and the status flip is exactly what V8 blocks (when the source/status cells are touched; see finding 2 for the teaches-only hole).

## VERDICT: c1-counters-gameable

Two concrete mutations defeat both frozen counters simultaneously (exit 0, `checks=8 defects=0`): (a) rewriting the teaches cell of a refusal row in place (V8 mislabel), (b) repointing a `source:` line at a different file within the same pinned repo (V2/V3 don't bind the document). The frozen predicate's second counter closes the stub/deep-identity holes from rounds 31–32, but the four "refusal rows stand unchanged" and "source lines re-pointed by document" obligations are only partially machine-bound. Smallest safe correction: fix `check_v8` to read `row[6]` (teaches) and additionally pin each cited row's anchor file path (and the `v2` suffix for S104) inside the entry's `source:` lines / V2/V3.
