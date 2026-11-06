# MutC2 — mutation test of the R99-C2 counter (round 99, wave 1)

Seat MutC2. Lane `kengaku-shokunin`, T `f72a8bc710b12473b5c768004e2581f980d924f4`.
Fixture: `git clone --shared` of the lane, branch `mut` detached at T, under
`/fast/scratch/hyaku/kengaku-r99/MutC2/lane`; every mutant is one commit on top of T, the
detector runs with `--rev <mutant>`, then `git reset --hard T && git clean -fdq`. Toplevel
asserted equal to the fixture before every commit. No production edits, no lane/fleet git
mutation, no task calls.

Detector (unchanged): `python3 plans/round99_c2_rowscoped_bind.py --lane . --rev <rev> --work
<scratch>/w-<id>` from the fixture root. Host `python3` 3.14.8; no venv, no tool install or
upgrade. Receipts: `.ufo/waves/round-99/w1/MutC2/` (`M00.txt` pristine, `M00-restored.txt`,
`M01..M24.txt`, `summary-all.tsv`, `restoration.txt`, `invisible.txt`, `driver.py.txt`).

## Baseline and restoration

| run | bytes | output | rc |
|---|---|---|---|
| pristine | T | `LEGS K1..K7=pass`; `TARGET pop=12 cleared=12 still=0 outside_rows=313 outside_removed=0 outside_added=0 outside_rebound=0 url_channel_files=0 rows_changed=0 captures_changed=0`; `GATE defects base=45 rev=33`; `PREDICATE R99-C2 pass` | 0 |
| mutated | each mutant commit | per-mutant table below | 0/1 |
| restored | T after all 24 mutants | byte-identical output to pristine | 0 |

Restoration evidence (`restoration.txt`): `HEAD=f72a8bc7…`, `status=[]`, toplevel is the
fixture, and 13 files byte-equal to their T blobs — the eight candidate-bytes
`PROVENANCE.md` files (round50 `d52af96b…`, round59 `7f3909f7…`, round61 `618916af…`, round79
`ce364b50…`, round82 `88c1cb8c…`, round92 `486dcba9…`, round93 `dc383775…`, round95
`5e1001a3…`), `corpus/evidence/PROVENANCE.md` `d3fc4b7c…`, `corpus/SOURCES.md` `05116b87…`,
counter `8b470d7a…`, gate `11bb2cad…`, capture `round50/git-init.adoc` `12309643…`.

## Mutants (24: 18 killed, 6 survived)

| id | mutation | expected | actual legs | verdict | killing leg / output |
|---|---|---|---|---|---|
| M01 | drop S175's line (round50) | K4/K5 | K4 fail, K5 fail | killed | `K4 S175:lines=0`; `K5 still_defective=S175` |
| M02 | duplicate S173's line (round50) | K4/K5 | K4 fail, K5 fail | killed | `K4 S173:lines=2`; `K5 bind_or_resolve_wrong=S173` |
| M03 | add a URL to a new file (round50 header) | K3 | K3 fail | killed | `K3 new_provenance_with_url=['corpus/evidence/round50/PROVENANCE.md']` |
| M04 | swap the S173/S174 sha cells | K4 (sha column) | K4 fail, K5 pass | killed | `K4 S173:sha_col=[S174 token] … S174:sha_col=[S173 token]` |
| M05 | point S270 at a byte-identical twin in the same dir (`fetch/candidate_run-tests.sh`, same sha) | K4/K5 | K4 fail, K5 fail | killed | `K4 S270:binds=…candidate_run-tests.sh`; `K5 bind_or_resolve_wrong=S270` |
| M06 | bind real outside row S179 (defective) in round79 | K7 | K7 fail | killed | `K7 outside rows moved=S179` |
| M07 | bind real outside row S001 (invisible) in round50 | K7 | K7 fail | killed | `K7 outside rows moved=S001` |
| M08 | bind fabricated row id S999 | survive | all pass | **survived** | none |
| M09 | move S225's line to round62 against a byte-identical twin | K4/K5 | K4 fail, K5 fail | killed | `K4 S225:file=corpus/evidence/round62/PROVENANCE.md`; `K5 bind_or_resolve_wrong=S225` |
| M10 | edit the existing round-98 `corpus/evidence/PROVENANCE.md` (whitespace) | K3 | K3 fail | killed | `K3 old_provenance_changed=['corpus/evidence/PROVENANCE.md']` |
| M11 | add a 4th plain-text column (S173) | survive | all pass | **survived** | none |
| M12 | add a 4th column naming another committed file (S173) | survive | all pass | **survived** | none |
| M13 | duplicate S173's line into round93's file | K4 | K4 fail | killed | `K4 S173:lines=2` |
| M14 | delete the whole round95 file | K4/K5 | K4 fail, K5 fail | killed | `K4 S306:lines=0`; `K5 still_defective=S306` |
| M15 | edit a POP SOURCES row (S173, trailing space) | K6 | K6 fail | killed | `K6 rows_changed=['S173']` |
| M16 | edit outside row S060's unparsed 64-hex token (`SHA2561e10…` → `SHA2562e10…`) | survive | all pass | **survived** | none |
| M17 | delete invisible outside row S001 | survive | all pass | **survived** | none |
| M18 | edit bound outside row S025's capture path | K7 | K7 fail | killed | `K7 outside rows moved=S025` |
| M19 | mutate POP capture `round50/git-init.adoc` | K6 (+K5) | K4 fail, K5 fail, K6 fail | killed | `K4 S174:sha_col=… capture=5d8ad7095460`; `K5 still_defective=S174`; `K6 captures_changed=['S174']` |
| M20 | edit the counter's POP token (S173) | K1 | K1 fail, K2 fail, K4 fail, K5 fail | killed | `K1 self=d2b94bf1dbe1 vs frozen 8b470d7ac3c2` |
| M21 | neuter the counter's K1 self check (`k1 = True`) | survive (self-reference) | all pass | **survived** | none |
| M22 | edit the gate's `ANCHOR_CELL` at rev | K1 | K1 fail | killed | `K1 gate_equal=False self=8b470d7ac3c2 vs frozen 8b470d7ac3c2` |
| M23 | delete bound outside row S025 | K7 | K7 fail | killed | `K7 outside rows moved=S025` |
| M24 | delete defective outside row S179 | K7 | K7 fail | killed | `K7 outside rows moved=S179` |

## Surviving mutants — soundness assessment

**M08 (fabricated row id S999) — survived; not a current binding hole, real predicate gap.**
The gate indexes `prov_sid["S999"]` but no SOURCES row carries S999, so no BIND/RESOLVED/defect
changes; K4 iterates only `POP`, K7 only `base_rows`. The line is inert today. It is a latent
hazard (a future S999 row would inherit the binding) and a gap against "one line per row"
(K4 counts only population rows). Caught outside this predicate by the candidate-bytes sha256
of `round50/PROVENANCE.md` (`d52af96b…`).

**M11 (4th plain-text column) — survived; real gap against the stated "three columns", no URL
channel.** The predicate never checks the column count. The extra text is inert to the gate.
Caught outside this predicate by the candidate-bytes sha256.

**M12 (4th column naming another committed file) — survived; real latent ambiguity, not a
current binding hole.** The line now names two committed files; K4 checks only `cands[0]` and
the gate binds only `cands[0]`, so the binding is unchanged under today's first-candidate
convention. A parser change to "last candidate" or "all candidates" would flip the binding to
another row's capture. No URL channel (K3 still closes that). Caught outside this predicate by
the candidate-bytes sha256.

**M16 (outside row S060's unparsed 64-hex token) — survived; real predicate gap.** The cell is
`wheel SHA2561e1022…` with no whitespace after `SHA256`, so the gate's `TOKEN`
(`sha256[ \t]+…`) never parses it; editing the digest changes no defect and no note. This is
the general shape: outside SOURCES rows are frozen only behaviourally, not byte-wise. Caught
outside this predicate by `corpus/SOURCES.md`'s candidate sha256 (`05116b87…`).

**M17 (delete invisible outside row S001) — survived; real predicate gap, the broadest one.**
105 of the 313 outside rows have no anchor token, no binding, no defect and no note
(`invisible.txt` lists them: S001–S024, S026–S060, …). K7's defect/note census cannot see their
edit or deletion; deleting S001 leaves `outside_rows=313 outside_removed=0` and the predicate
passes. These rows bind nothing, so this is not a binding hole, but the claim's "no SOURCES row
changes" is not enforced by the predicate for 105/313 outside rows. Caught outside this
predicate by `corpus/SOURCES.md`'s candidate sha256.

**M21 (neuter K1) — survived; inherent self-reference, not a new hole.** A counter cannot
detect a mutation that removes its own integrity check: the mutated counter's self sha differs
from the frozen `8b470d7a…`, but the check that would compare them is the one removed. K1 does
kill every counter edit that does not target K1 itself (M20). The claim's kill rule covers this
externally ("if a frozen file changes after F"); the frozen-instruments table and the receipts
commit's freeze-integrity check are the guard, exactly as for any frozen instrument.

## What the killed mutants establish (positive coverage)

- **K4 is load-bearing for the sha column.** M04 (swapped sha cells) fails K4 only — K5 passes
  because the gate resolves by path, never by the provenance sha column. A K4 without the
  `shas != [token]` check would let a swapped sha column through.
- **K5 is row-scoped, not merely resolution-scoped.** M05 (byte-identical twin in the same
  directory) and M09 (byte-identical twin in another round directory) both fail K5 because the
  `RESOLVED … via=` prefix must equal the frozen POP capture path. Exact-path binding is
  enforced twice (K4 and K5).
- **K7 is symmetric for gate-visible rows.** Additions (M06, M07), re-bindings (M18) and
  removals (M23, M24) all fail K7; the census is not addition-only.
- **K3 closes both URL channels.** A URL in a new file (M03) and any edit to a pre-existing
  provenance file (M10) both fail K3.
- **K1 catches both frozen-byte edits.** Counter bytes (M20) and gate bytes at rev (M22) fail
  K1; M20 additionally trips K2/K4/K5 because the POP table is the counter's own data.
- **K6 is byte-wise for population rows and captures.** A trailing space on S173 (M15) fails
  K6; a one-byte capture change (M19) fails K6 and also K4/K5 through the gate.

## Verdict

The R99-C2 counter's seven legs are exercised and falsified as designed: 18/24 mutants killed,
each by the leg the claim names. Six survivors remain; none changes a binding today. Four are
predicate-coverage gaps (M08, M11, M12, M16/M17 class) that the candidate-bytes sha256 table
covers externally; M21 is the inherent self-reference limit covered by the frozen-instruments
freeze. No survivor contradicts the measured `PREDICATE R99-C2 pass` at T.
