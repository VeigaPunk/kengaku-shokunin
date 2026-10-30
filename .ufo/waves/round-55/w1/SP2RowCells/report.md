# SP2RowCells — cell-verbosity pass over the five new SKILL.md registry rows (kengaku r55 w1)

Seat: SP2RowCells (simplifier) · Axis: operability · Bounds honored: read-only lane + own wave dir; no subagents; no git mutations; no tool installs.

## What landed and what I produced

E1RegistryRows landed the five rows at `SKILL.md` lines 642–646 (after `stage-scan`) at ~13:04, after four bounded waits (~2 h wall; E1 started ~12:22 behind the fleet ramp and confirmed "ETA ~10 minutes" mid-wait; rows appeared ~630 s later). Deliverable: **`trims.diff`** (unified diff, `a/SKILL.md` → `b/SKILL.md`, applies with `git apply`/`patch -p1` from the lane root). It proposes 7 prose trims across 4 of the 5 rows; `round55-c3` needs no trim. Net −357 chars. The lane file itself was never modified — the trimmed text exists only in scratch (deleted) and as this diff for the L1 to apply or reject.

## Per-hunk rationale (hunk = whole table line; sub-trims listed)

1. **`round54-c1`** (−109): (a) *entry cell*, drop "`; the bare-host entry measurement is red — see the verdict map`" — **reverse direction** (entry restates the verdict map): the `1` leg already carries the full measured fact ("at the tip's bare host python3 (no `opentimestamps` library) the entry dies on `ModuleNotFoundError` and exits 1, measured 2026-10-30"). (b) *scope cell*, drop "`: anchor assets land only via `stamp`/`upgrade`" — **mandate direction**: duplicates the entry cell's "subcommands `stamp`/`upgrade` write the anchor and need network + the `ots` CLI"; scope keeps "decides whether … externally anchored …, with forged-proof controls; no lane write".
2. **`round54-c2`** (−85 entry, +7 verdict): entry drops "` — the bare ledger argv exits 2 `SETUP --source and --work are required unless --dry`, measured 2026-10-30`" — **reverse direction**: the literal `SETUP …` string is verdict `2`'s semantics. The measured date is **relocated additively** into verdict `2` ("`2` setup/usage (measured 2026-10-30: `SETUP …"), so no truth content is lost from the protected cell.
3. **`round55-c2`** (−85 entry, +7 verdict): identical pattern to hunk 2 for its row.
4. **`round55-c2-controls`** (−78): *scope cell* drops "(the r54 counter passes them)" and "(the r55 binding counter attributes the defect)" — both fully restated by verdict `0`'s measured demonstration lines (`ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)` / `ARGV-DEFECT`+`ABBREV-DEFECT`/`WRAPPER-DEFECT`, `ROUTE kill demonstrated (r55 rc=1)`); scope keeps the decision statement + fixture mechanics.
5. **`round55-c3`** (0): **no hunk** — flag inventory, canonical receipt-run argv and bare-entry behavior are three distinct facts, verdict `0`/`2` carry non-duplicated content. Forcing a trim would harm; per the no-harm rule I stopped here.

Truth-bearing content untouched: verdict maps keep every leg, measured value and exit code; self-test cells untouched (commands, measured outputs, limits); first backtick spans untouched (see invariants).

## Verified invariants (all exercised, not assumed)

- **First-span identity**: the first backtick span starting with `python3` is byte-identical orig→trim in all five rows — this is the span E4LedgerTruth/`round55_c2_entryargv.py` L1 shlex-tokenizes, so R55-C2 binding is unaffected. Python check: `INVARIANTS PASS`.
- **Registry counter parse**: every trimmed row still splits into exactly 8 non-empty cells.
- **Counter delta**: twin `git clone --shared` fixtures at HEAD `80afa613` + orig vs trimmed `SKILL.md`; `python3 plans/round52_c2_registry.py --lane <fixture>` → **byte-identical output, same rc (1) on both** (rc 1 is the HEAD state's pending legs — `ADVERTISED total=80`, `MISSING 0`, `INCOMPLETE 0` — identical in both fixtures, so the trims are delta-neutral). Clone toplevel asserted before any git contact.

## Commands + exit codes (selection)

- `diff -u --label a/SKILL.md --label b/SKILL.md orig trimmed > trims.diff` → rc 1 (differences; 17 lines).
- python3 invariant check (cells/first-spans, orig vs trim) → `INVARIANTS PASS`, chars saved 109/85/85/78/0.
- `git clone --shared` ×1 + `cp -a` twin → `toplevel ok`; counter on both → rc 1 = rc 1, `COUNTER-DELTA: identical`.
- `sha256sum` of the five scripts vs E1's pinned cells → 5/5 match (`e08152a5`, `44c3f412`, `2bf9e66c`, `c7591bc6`, `7bd2863c`).

## Defects found (reported, not fixed — other seats own those files)

- None blocking in the five rows. Observations for the L1/R6: (a) `round54-c1` verdict `1` writes "`CONTROLS forged=4 failed=<n>0`" — ambiguous notation (presumably "failed≠0"); R6's truth-audit territory, I did not touch it. (b) The new rows omit the house-style "(lane root; …)" entry-cell prefix that round52-c1/c2 carry — an omission, not verbosity, so out of a trims-only mandate. (c) "flags implemented:" wording is E1's cell-contract phrasing (first span kept bare for ledger binding); kept.

## Dead ends

- First two bounded waits expired before E1 began (fleet ramp); resolved by waiting, not by duplicating E1's work. Dispatch jq guess `.items` failed (structure nests under `.registry.members.<name>.item`) — resolved by reading the file head. No tool installs.

## Hygiene

Scratch `/fast/scratch/hyaku/kengaku-r55/SP2RowCells/` (orig/trimmed copies, twin clones, diff, counter outputs) deleted after copying `trims.diff` here. Outputs: `trims.diff`, this `report.md`, and scoped findings at `.ufo/waves/round-55/w1/SP2RowCells.md`.
