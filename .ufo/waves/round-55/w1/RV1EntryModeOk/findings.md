# RV1EntryModeOk — why round-54 computed `entry_mode_ok` without binding it to the registry

Date: 2026-10-30. Seat: RV1EntryModeOk (revenger, read-only). Lane base for this round: `798f5e9e`.
Revisions read: r54 counter birth `17f90355` (blob sha256 of the birth file
`44c3f412…0cc0da97`); r54 ledger at `9a0746be`; SKILL.md registry at base `798f5e9e`; r53 counter at `6c919180`.

## Short answer

Not an oversight in wiring and not a documented open window. It is a **predicate-scope decision**,
inherited from the round-53 frozen argv contract and re-frozen unchanged in round 54. The round-54
counter did wire `entry_mode_ok` into the predicate, but only as a *shape check on the ledger's own
argv*. The frozen round-54 predicate bound the ledger argv to the registry row's **script name only**,
never to the registry row's full entry command and never to the program the interpreter actually runs.
The round-54 claim's surface text ("declares every row at its entry argv") promised more than that
scope delivered. The gap was found by the round-54 reviewer, the kill rule fired, and the lesson and
Q44 record it as a missed structural binding.

The round-55 claim text describes `entry_mode_ok` as "computed but unwired". That description is
inaccurate: the return value is consumed (see E3 below). The accurate description is "wired to a
script-identity and exact-token check on the ledger argv; no binding to the registry cell's command."

## Evidence chain

### E1 — birth of the round-54 counter and its scope (17f90355)

`git show 17f90355:plans/round54_c2_entrytruth.py`, the file's only revision (it is born in the
freeze commit, `git log --diff-filter=A`):

- `entry_mode_ok(argv, script)`, lines 146–165: rejects non-list/short argv, shells (`SHELLS`,
  includes `-c`), exact forbidden tokens `{--selftest,--help,-h,--dry,--version}` (line 50, 154),
  then requires `argv[1] == script` for `python3`, or any adjacent `python3 <script>` pair for `uv`.
  It returns `None` for accept.
- `row_script(line)`, lines 85–89: the only thing extracted from the registry cell is the
  `python3 <script>` regex match (`SCRIPT`, line 45). The rest of the registry command is discarded.
- `static_legs`, lines 228–231: `script = row_script(rows[n])`;
  `defect = entry_mode_ok(sp.get("entry_argv"), script)`; a defect appends to `argv_defect`.
  The registry's full command is never compared with `sp["entry_argv"]`.
- `evaluate`, lines 277–278 and 358–360: `static_ok` requires `not argv_defect`; the predicate is
  `static_ok and executed == n_reg and … and laundered == 0 and clean and rev_ok`.
  EXEC (lines 306–341) runs `s["ledger"]["rows"][n]["entry_argv"]`, i.e. the ledger argv, not the registry command.
- `selftest`, lines 408–486: the only argv-defect case is `selftest-argv-rejected` (lines 441–449),
  which uses the exact token `--selftest`. No abbreviation case, no `uv`-decoy case, no registry-cell comparison.

### E2 — the frozen round-54 claim scope

`plans/round-54-claims.md`:
- Surface, lines 119–126: "(a) a new ledger … that declares every `SKILL.md` registry row at its **entry argv**
  (no `--selftest`/`--help`/`--dry`/`--version` in the declared argv)".
- Predicate leg LEDGER, line 143–144 (frozen): "each declares `entry_argv` in entry mode **whose script
  matches the registry row's script**". This is the scope decision in frozen text: script identity.
- Kill rule, lines 176–178: "any attack seat produces a ledger row that passes the r54 counter while its
  true entry behaviour disagrees with the declaration (laundering variant survives)".
- No sentence in the claim defers argv binding, names an open window, or lists it as out of scope.

### E3 — `entry_mode_ok` is wired (correcting the round-55 characterisation)

Probe, read-only, in scratch (`receipts/probe-wiring-r54-birth.txt`, script `receipts/probe_wiring.py`,
run against the birth module imported from `git show`; exit 0):

| fixture (registry cell / ledger argv) | dry rc | ARGV-DEFECT? |
|---|---|---|
| cell `python3 plans/gate.py`, ledger `python3 plans/gate.py --selftest` | 1 | yes (`non-entry flag --selftest`) |
| cell `python3 plans/gate.py`, ledger `python3 plans/gate.py --selft` | 0 | no |
| cell `python3 plans/gate.py check .`, ledger `python3 plans/gate.py` | 0 | no |
| cell `python3 plans/gate.py check .`, ledger `python3 plans/gate.py --expect x` | 0 | no |

So `entry_mode_ok` is consumed by the static leg and can flip the predicate (row 2 of the table is the
only failing case). What it does not do is bind to the registry cell (rows 3–4) or to the program
actually executed (below).

### E4 — the laundering route is the one the function cannot see

`w1/R2C2Counter/laundering-probes.txt` (r54 reviewer, unchanged counter):
- `["python3","plans/gate.py","--selft"]`: `entry_mode_ok=None`; true registry entry exit 1; counter `PREDICATE R54-C2 pass`.
- `["uv","run","--no-project","--offline","python3","-cprint('wrapper green')","python3","plans/gate.py"]`:
  `entry_mode_ok=None`; true entry exit 1; counter pass. The inline `-cPROGRAM` (combined form) is not
  the exact token `-c`, so `SHELLS` does not catch it, and the `python3 plans/gate.py` pair later in argv
  satisfies the uv branch. Python executes the inline print, so the gate never runs.
Reviewer findings: `w1/R2C2Counter/review.md` B1 (lines 7–13) and B2 (lines 15–27). The review also
ruled that a `--summary` argv is *not* laundering by itself, because the registry names `--summary` as a legal
mode for several rows (lines 63–66). Legitimate ledger argv can therefore carry registry-named flags, so any
binding must consult the registry cell's own alternatives rather than a bare token list.

### E5 — the same scope was inherited from round 53 (the hole predates round 54)

`git show 6c919180:plans/round53_c2_tipstate.py` (the r53 counter, frozen; never edited by r54):
- `argv_ok`, lines 149–159: `python3` → `argv[1] == script`; `uv` → any adjacent `python3 <script>`; `SHELLS` as above.
- `kind_ok`, lines 162–164: kind is inferred by exact `"--selftest" in argv` / `"--help" in argv`, else `entry`.
- Test `uv-run-entry`, line 470: `["uv","run","--no-project","python3","plans/a.py"]` is an *expected pass*.
  The uv allowance was a deliberate positive case, not an accident.

Probe (scratch, importing the r53 module): `argv_ok` and `kind_ok(…,"entry")` both return True for
`["python3","plans/gate.py","--selft"]` and `["python3","plans/gate.py","--hel"]`. So an r53 ledger row with
`kind=entry` and an abbreviated selftest argv passes r53 too. The abbreviation route is not new in round 54.

The r53 frozen claim states the contract explicitly: `plans/round-53-claims.md:198` — "argv is
`python3 <row script> …` or `uv … python3 <row script> …`; no shell, no `-c`, no wrapper; `kind` must match the
argv (`--help` ⇔ `help`, `--selftest` ⇔ `selftest`, else `entry`)". The contract is internally inconsistent
(it allows `uv …` while forbidding "wrapper"), and it defines argv identity as script identity plus exact tokens.

### E6 — the round-54 attack prompts asked the question; it was open at dispatch, not deferred

`.ufo/waves/round-54/build_spec_w1.py`:
- line 447 (R2C2Counter): "Is entry_mode_ok bypassable (uv wrapping, flag case, '=' forms, argv after '--')?"
- line 517 (C2Launder): "Does entry_mode_ok admit any argv that is NOT the plain entry?"
- line 783 (R5LedgerStatic): "argv … script in each argv matches the SKILL.md registry cell."

The seats were asked the right question. The round-54 freeze did not answer it with a binding leg, and
the freeze text (E2) fixed the leg at script identity. This is a known-open scope boundary that was
chosen, not a deferral with a stated window.

### E7 — the disposition after the kill

- `corpus/lessons/round-54.md:30` (mistake class `selected-argv-laundering`): "Exact-token filtering closed the
  original toy route but not abbreviated selftest or uv-decoy argv … Frozen C2 kill rule fires … Q44 records the
  missed structural binding."
- `corpus/lessons/round-54.md:73`: "structural interpreter/entry binding before ledger scoring" is the stated
  highest-impact next change.
- `corpus/QUALITY.md:1161` (Q44): "a command ledger must reject abbreviated selftest modes and interpreter
  decoys, not just exact forbidden strings."
- `SCORECARD.md:2337` ff. (round 54): calibration "9→9 held — frozen kill rule fires".
- Round-55 frozen predicate: `plans/round-55-claims.md:42–93` adds L1 (token-equal registry argv), L2 (no
  wrappers/`-c`), L3 (no prefix abbreviation), L4 (execution). Its kill rule (lines 87–93) is the same soundness
  rule that fired in round 54.

### E8 — what was searched and found absent

Searched for deferral, open-window, or argv-binding language in: `plans/round-54-claims.md`,
`corpus/lessons/round-54.md`, `corpus/lessons/round-53-verifier-spotcheck.md`, the round-54 SCORECARD
section, `.ufo/l0-questions.md`, `.ufo/waves/round-54/w1-spec.json`, and `corpus/QUALITY.md` Round-36 "open window"
(unrelated: a frozen-instrument repair window). No text defers entry-argv binding to a later round.

## Classification

| hypothesis | verdict | basis |
|---|---|---|
| deliberately deferred (documented open window) | **not supported** | E2, E8: no deferral text; freeze states the LEDGER leg as script identity without a window |
| oversight in wiring (function computed, return ignored) | **not supported** | E3: return is consumed at 229–231, 277–278, 358–359; dry probe shows ARGV-DEFECT flips rc |
| predicate-scope decision (static script identity vs full argv binding) | **supported, primary** | E1 (frozen LEDGER leg at claims:143–144), E5 (identical scope in r53 claims:198), E6 (asked, not answered) |
| surface overstated the scope | **supported, secondary** | E2 surface lines 119–126 ("at its entry argv") vs leg text 143–144 |

Confidence: high on the source facts (read and executed); medium-high on intent. Intent is reconstructed
from the frozen text and the absence of a deferral, not from a stated author rationale; no author statement
exists in the searched artifacts.

## Implications for R55-C2 (pre-run observations; not scored; not an admission)

Measured while tracing, on the r54 ledger at `9a0746be` against the base SKILL.md at `798f5e9e`
(`receipts/measure-l1-projection.txt`, script `receipts/measure_l1.py`). These bear on whether the frozen
round-55 predicate can pass as written. They are routed to L1 for disposition, not fixed here.

1. **`tb2-grader-probe` cannot satisfy both L1 and L2 as frozen.** The registry cell is
   `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (SKILL.md, the
   `tb2-grader-probe` row). L1 requires the ledger argv to token-equal that cell; L2 makes `argv[0] == uv` a
   `WRAPPER-DEFECT`. Either the row fails L2, or it is edited away from the cell and fails L1. The round-55 claim
   text does not carve out dependency-provisioning wrappers. A dated amendment is needed before the after-run;
   otherwise `PREDICATE R55-C2 pass` is unreachable for this row by construction. (Also: the r53 ledger carries
   the same uv row, 1 of 78.)
2. **L1 "token-equal to the declared entry command" is undefined for 16 of 78 rows.** Only 62/78 ledger argvs
   equal the first backticked python3 command in their cell token-for-token. The differences are placeholders
   (`<expect.json>`, `<lane>`, `<scratch>`), words (`DIR`, `REV`, `[--revision REV]`), and bracketed optional flags
   (`[--verbose]`, `[--rerun]`, `[--work DIR]`). The frozen claim has no normalisation rule for these. Without one,
   those rows become `ARGV-DEFECT`s, or the ledger must carry non-runnable placeholder text. The normalisation must be
   fixed by amendment before the after-run, not by counter edit.
3. The round-55 claim's characterisation "entry_mode_ok computed but unwired" should be corrected in the dated
   amendment file (E3), so the round's narrative does not mislead a later reader about what the r54 counter did.

## Defects found in the round-54 instrument (for the record)

- Abbreviation and combined-`-c` laundering (E4): reproduced by the r54 reviewer; exact-token checks cannot see
  either. Also present in r53 (E5).
- Binding absent: the registry cell's command is parsed for the script only (`row_script`, lines 85–89).
- Test gap: the r54 selftest (`receipts` in `w1/R2C2Counter/selftest.txt`, 7/7) contains no abbreviation, decoy, or
  registry-cell case, so its green says nothing about these routes.

## Dead ends

- No LSP device available (`xd://lsp` absent); reference reconstruction is by file read and `git show`/grep, not
  semantic reference proof.
- Did not execute the r54 full counter against the registry (no clean-clone execution requested for this seat).
  The probe used the birth module's `static_legs`/`evaluate` in dry mode and `entry_mode_ok` directly.
- Did not verify the r55 `plans/round55_c2_entryargv.py` (not present at base; it is built by sibling seats).

## Files written by this seat

- `.ufo/waves/round-55/w1/RV1EntryModeOk/findings.md` (this file)
- `.ufo/waves/round-55/w1/RV1EntryModeOk.md` (copy, per Report trailer)
- `.ufo/waves/round-55/w1/RV1EntryModeOk/report.md`
- `.ufo/waves/round-55/w1/RV1EntryModeOk/receipts/` (probe script + output; L1 projection script + output)

No tracked lane file, no MANIFEST, no `.ufo/state`, no sibling file touched. No git mutation. No installs.
