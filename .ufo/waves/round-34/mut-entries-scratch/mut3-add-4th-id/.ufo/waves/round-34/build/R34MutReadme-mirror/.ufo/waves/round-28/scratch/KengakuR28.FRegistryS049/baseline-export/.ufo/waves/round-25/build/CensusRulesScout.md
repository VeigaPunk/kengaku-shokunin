# CensusRulesScout — SOURCES.md validate rules (read-only)

Base extracted `git -C lane archive 6180e4fb92e9` → /tmp/r25-census (lane HEAD observed 3f371d2). No lane write.
Rules traced to `scripts/sources-census.sh:574-695` (row_pass gawk; E08 at `:661-662`), `:538-570` (usedby_findings/E11),
`:90-91` (default today) and `:51-63` (iso_epoch). Every line below was
mutation-tested on /tmp fixtures; each claim carries the exact emitted token.

## 10-line row checklist (11 cells, NF=13)

1. **Placement/shape**: row inside a heading whose trimmed text is exactly `Registry` (`##`, 0–3 leading spaces); a
   row-shaped line elsewhere → `E12 ... row outside Registry section`; 4+ leading spaces = invisible code; `|` inside any
   cell shifts columns → `E01 <id> fields=<NF-2>`. Malformed rows short-circuit all other per-row checks except E02.
2. **id**: `S` + >=3 digits, `^S[0-9]{3,}$`, unique per file (`E02 <id>`, `E03 <id> duplicate id`); cells are trimmed.
3. **URL/duplicate**: normalized key = lowercase host, path case kept, trailing `/` and `#fragment` stripped. Same URL+same
   scope → `E04 ... within scope <s>` unless a prior same-scope row is `rejected` or teaches contains lowercase literal
   `supersedes S###` (three digits — `S0026` also matches by substring). Same URL, different scope → `W04` (exit unaffected).
   Rows with no `https?://` (own-work) skip duplicate checks.
4. **kind enum**: exactly `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` (`E05 <id> kind=blog` observed).
5. **tier enum**: exactly `A|B|C` (`E06`), and `community`+`A` forbidden (`E10 community-at-A`). Tier is per-scope.
6. **status enum**: exactly `queued|mined|rejected` (`E07`); `watch` invalid. `census` buckets an invalid status under
   `status.invalid`, but only E07 makes `validate` fail.
7. **opened**: strict `YYYY-MM-DD`, real calendar day, `<= today` (`E08`). `today` = `date -u +%F` when `--today` omitted;
   TZ env is inert (see below). Use `date -u +%F`, never `date +%F`; `2026-1-1` → E08.
8. **recheck**: one of strict ISO date, `^[0-9]+d$` (literal `d`), or symbolic `^[A-Za-z][A-Za-z0-9 _-]*$`
   (`on-release`, `annual` OK; `3 months`, `30 days`, `90 d` → `E09`).
9. **used-by**: `—` (U+2014) = none; else comma-split paths relative to the **lane root** (not the file's dir), each
   `test -e` (`E11 <id> missing used-by <path>`). E11 only examines `mined` rows — a queued dangling path passes.
   `-`, `--`, absolute paths all E11. mined+`—` → `W03`; tier C+mined+non-`—` → `W01`.
10. **teaches/anchor/scope**: rejected needs >=8 chars (`W02 thin reject reason`); `anchor` and `scope` are never
    content-validated (non-empty is convention only); `source` needs no URL for own-work.

## Test: validate at base, TZ unset vs TZ=UTC

- `env -u TZ scripts/sources-census.sh validate /tmp/r25-census` → `r25-census<TAB>ok<TAB>/tmp/r25-census/corpus/SOURCES.md`, **rc=0**
- `TZ=UTC ... validate /tmp/r25-census` → identical line, **rc=0**
- Mechanism probes `TZ=Asia/Tokyo|America/Sao_Paulo|Pacific/Kiritimati` → all `ok`, rc=0. TZ env is fully inert: default
  today is `date -u +%F` (script:90) and gawk `mktime(...,1)`/`strftime(...,1)` (script:55-56, 587-588) are UTC-flag pinned.
- **W3 F13 verdict**: "E08 false positive when TZ is not UTC" is *not* reproducible via TZ at base. Residual exposure is a
  mixed-clock one: host local = 2026-10-20 (UTC−3) while UTC = 2026-10-21. Fixture S001 opened 2026-10-21 passes under the
  default (UTC) run but `--today 2026-10-20` (local date) reports `E08 S001 opened=2026-10-21`; `opened=2026-10-22` reports
  E08 under both (rc=1). Symmetrically, a UTC+X author writing the local date is flagged by the default run.
- `selftest` → `selftest ok`, rc=0 (includes the `UTC-date-in-Sao-Paulo` guard and `H1-no-table-cell-execution`).
- Live gate: `validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku<TAB>ok`, rc=0; `census` → rows 26,
  tier.A 24 / tier.C 2, status.mined 18 / queued 5 / rejected 3, missing 0 — identical to the /tmp base copy.

## Rule-map caveats for writers

- W01 is *not* "tier C is bad": it fires when a tier-C row is mined **and** carries a used-by path.
- E04's exemption is asymmetric: a later non-rejected duplicate in a scope whose only prior row is `rejected` passes.
- `### Registry` does not open the section (E12 on its rows); `## Registry` is the only accepted form.

Installs: none. Scratch: /tmp/r25-census*, /tmp/r25-rules* only.

VERDICT: At base, validate is TZ-deterministic (unset == UTC == any zone, rc=0 on the 26-row registry); the F13 E08
false positive only reappears when `--today` is fed a local date (or a row's opened is authored on a local date ahead of
UTC), so the checklist pins `opened <= date -u +%F` and the 11-cell NF=13 shape.
