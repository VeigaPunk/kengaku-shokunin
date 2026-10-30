# R6RegistryCellAudit — full report (kengaku round 55, wave 1)

Seat R6RegistryCellAudit · reviewer (attack share) · axis operability (R55-C1 registry closure).
Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; claims frozen at `80afa613`.
Scratch root `/fast/scratch/hyaku/kengaku-r55/R6RegistryCellAudit/` (removed at cleanup).

## What I ran

**Bounded wait for the five rows** (60 s steps). First window (25 min): rows absent —
`grep -cE '^\| \`round54-c1\`|…' SKILL.md` = 0; E1RegistryRows `agentId:null`, empty output dir.
Engaged the seat's fallback (audit the E1 cell contract) and gathered ground truth. Discovered
E1 was alive (`/fast/scratch/hyaku/kengaku-r55/E1RegistryRows/otsenv` venv, built 12:52), so
ran a short bounded re-wait (45 s steps, 12 min cap); rows landed ~135 s in (all 5 present).
Proceeded with the real per-row audit.

**Scratch clone:** `git clone --shared <lane> clone` at `80afa613`; lane scripts copied in as they
landed. All entry commands run from the clone; TMPDIR/--work pointed at my scratch; no lane writes.

### Commands + exit codes (clone unless noted)
| command | exit | note |
|---|---|---|
| `python3 plans/round54_c1_anchor.py` | 2 | usage, `cmd` required |
| `python3 plans/round54_c1_anchor.py selftest` (system py3) | 1 | `ModuleNotFoundError: opentimestamps` |
| `… anchor.py selftest` (E1 `otsenv` venv) | 0 | `[selftest] 8/8 PASS` |
| `… anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source . --work … --controls` (system py3) | 1 | `ModuleNotFoundError: opentimestamps` (`cmd_verify`:301) |
| same verify (`otsenv` venv) | 1 | `SETUP header.bin absent …` + `PREDICATE R54-C1 fail` |
| `python3 plans/round54_c2_entrytruth.py --lane .` (bare) | 2 | `SETUP --source and --work are required unless --dry` |
| `… entrytruth.py --lane . --dry` | 0 | static legs clean + `DRY … no predicate` |
| `… entrytruth.py --selftest` | 0 | `[selftest] 7/7 PASS` |
| `python3 plans/round55_c2_entryargv.py` (bare) | 2 | `SETUP --source and --work are required unless --dry` |
| `… entryargv.py --lane . --dry` | 1 | 17 pre-existing placeholder ARGV-DEFECTs on the *base* clone SKILL.md (not a row defect) |
| `… entryargv.py --selftest` | 0 | `[selftest] 4/4 PASS` |
| `python3 plans/round55_c2_controls.py` (bare) | 2 | argparse `one of the arguments --case --selftest is required` |
| `… controls.py --selftest` | 0 | `SELFTEST cases=4 failures=0` |
| `… controls.py --case abbreviated-selftest --against r54` | 0 | `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)` |
| `… controls.py --case uv-decoy-script --against r54` | 0 | `ROUTE laundering demonstrated` |
| `… controls.py --case abbreviated-selftest --against r55` | 0 | `ARGV-DEFECT`+`ABBREV-DEFECT …`, `COUNTER EXIT 1`, `ROUTE kill demonstrated` |
| `… controls.py --case uv-decoy-script --against r55` | 0 | `ARGV-DEFECT`+`WRAPPER-DEFECT argv[0]='uv'…`, `COUNTER EXIT 1`, `ROUTE kill demonstrated` |
| `python3 plans/round55_c3_chess_probe.py` (bare, no `--receipt`) | 0 | `cases=12 observed_pass=5 observed_fail=7 mismatches=0` `PREDICATE R55-C3 pass` |
| `… chess_probe.py --selftest --work <scratch>` | 0 | `SELFTEST cases=2 failures=0` |

**Registry counter (authorised SELFTEST-UNBACKED pre-check), `python3 plans/round52_c2_registry.py --lane <tree>`:**
- mid-wave (rows absent): `ADVERTISED 80 REGISTERED 77 MISSING 3 PREDICATE R52-C2 fail` exit 1
  (the 3 = round54_c1_anchor, round54_c2_entrytruth, round55_c3_chess_probe advertised w/o rows).
- rows landed: `ADVERTISED 82 REGISTERED 82 rows=84 MISSING 0 INCOMPLETE 0 ENTRY-MISSING 0
  SELFTEST-UNBACKED 0 DUPLICATE 0 PREDICATE R52-C2 pass` exit 0.

**Harness `audit_rows.py` (scratch):** parsed the 5 rows; all `present:true`, all 5 referenced
scripts exist in lane+clone, all 5 pinned sha256 match lane bytes, all `selftest_unbacked:false`,
every self-test-cell flag present in its script body.

## Files I wrote
- `.ufo/waves/round-55/w1/R6RegistryCellAudit.md` — scoped findings (per-row cell-truth table).
- `.ufo/waves/round-55/w1/R6RegistryCellAudit/report.md` — this report.
- `.ufo/waves/round-55/w1/R6RegistryCellAudit/evidence/` — 19 receipts (entry/selftest/verify
  outputs, the 4 controls cases, chess battery+selftest, registry counter before/after,
  `audit-rows.json`, `audit_rows.py`, `five-rows-raw.md`).
- Scratch only: `audit_rows.py`, `clone/` (both removed at cleanup).

## Defects found
**None.** Every audited cell of all five rows is TRUE (observed == claimed):
- entry cells run and exit as the verdict maps claim;
- every self-test cell names a flag/subcommand that exists in the script body
  (`round54-c1` correctly uses the `selftest` **subcommand**, not `--selftest` — the file has
  zero `--selftest` occurrences);
- all five pinned sha256 digests match current lane bytes.
No R55-C1 kill-rule trigger (no round-55-added row whose self-test exits otherwise than claimed,
given the documented `opentimestamps` venv for `round54-c1`).

## Residual risk / honest notes
- `round54-c1` self-test + entry need the `opentimestamps` package (row says so). If the L1's
  frozen-leg-2 host lacks it, the named self-test observes exit 1 ≠ claimed exit 0 → the row
  would *read* false through environment, not cell text. Leg 2 must run under an `otsenv`-style venv.
- Anchor assets are incomplete (`anchor.json`+`claims.ots`; no `header.bin`/receipts — r54
  attestation never confirmed), so the round54-c1 entry can only be red; the row discloses this.
- `round55-c2` pinned digest is for a live E2 file — reconfirm at the measured-after revision.
- Registry-counter pre-check was on the lane **working tree**; the binding R55-C1 after-run must
  be re-run on a clean clone at the measured-after revision.

## Dead ends
- First 25-min wait: rows absent (E1 unspawned) → ran fallback ground-truth; E1 then landed the
  rows, so the fallback prediction was superseded by the real audit (documented in scoped findings).
- One self-inflicted redirect collision (`/tmp/r3` already a directory) on the first entryargv
  run; re-ran with a clean filename. Not a lane issue.

## Installs
None. No tools installed/upgraded; no pacman transactions. (Used the pre-existing
`E1RegistryRows/otsenv` venv read-only to observe the anchor self-test green; deleted nothing of E1's.)
