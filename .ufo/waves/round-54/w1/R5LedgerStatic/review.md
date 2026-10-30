# R5LedgerStatic — DEFECTS

Axes: calibration (declared command/exit/reason/provenance honesty), completeness (78-row census), no harm (read-only inputs).

Reviewed ledger SHA-256: `0dd772c4476009a937b039d21ab1bc19a2066dbdaf7e12e8520f370ef670f526`.
This is a static document review, not an execution verdict or admission of R54-C2.

## Findings by severity

### High — scratch-root-guard declares an exit incompatible with its own evidence and reason

`plans/round54-entrytruth.json:903-915` declares `entry_exit: 2` for `python3 plans/scratch_guard.py check .`, but the reason explicitly says that invocation exits 1 and its evidence is `CHECK red reason=sentinel-missing`.
The canonical `cmd_check` sets the missing-sentinel reason at `plans/scratch_guard.py:162-165` and the text-output branch that prints `CHECK red` returns **1** at lines 224-226; the JSON equivalent also returns 1 at line 206. Exit-2 setup branches do not emit that evidence. This is an internal contradiction, not a runtime observation. Reconcile argv, observed exit, fragment, and reason from the same run; merely rewording the reason cannot repair the impossible exit/fragment pair.

### Medium — twelve red reasons name no cause

The following rows all use the identical 20-word boilerplate: “the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output”. It meets the word-count threshold but only restates nonzero exit. It does not satisfy this seat's cause requirement.

- `adoption-check` — `plans/round54-entrytruth.json:3`
- `anchor-digest-check` — `plans/round54-entrytruth.json:20`
- `gate-flip-check` — `plans/round54-entrytruth.json:187`
- `mutant-direction-check` — `plans/round54-entrytruth.json:283`
- `round28-census` — `plans/round54-entrytruth.json:392`
- `round35-c1-coverage` — `plans/round54-entrytruth.json:468`
- `round38-c1-mutants` — `plans/round54-entrytruth.json:542`
- `round40-c1-mutants` — `plans/round54-entrytruth.json:604`
- `round46-c3` — `plans/round54-entrytruth.json:774`
- `round51-surfaces` — `plans/round54-entrytruth.json:825`
- `round52-c1` — `plans/round54-entrytruth.json:839`
- `state-assertion-check` — `plans/round54-entrytruth.json:945`

Some fragments also show only successful preliminary checks (`PINS ... mismatched=0`, `V1 ok ...`, or `DIR ... ok`), so a reader cannot recover the omitted cause from them. Their non-empty/length checks nevertheless pass; no claim of non-verbatim evidence is made without execution. The boilerplate originates at `plans/round54_build_entrytruth.py:133-136`. Provide row-specific causal explanations, supported by the actual failing leg.

### Medium — three chosen="bare" labels are false for the recorded argv

`round53-c2` (`plans/round54-entrytruth.json:877`), `sources-adopt` (917), and `stage-scan` (931) all record `python3 <script> --lane .`, not the bare `python3 <script>` candidate. Each r53 predecessor is `kind: selftest`, so none is an r53 entry override. The frozen builder defines candidate A as lane-dot and candidate B as bare (`plans/round54_build_entrytruth.py:95-98`), and assigns `lane-dot` whenever a non-r53 selected argv contains `--lane` (line 130). These rows' labels are inconsistent with their actual argument lists. Correct the provenance from the actual selected invocation; this does not establish that the recorded exit was measured.

### Medium — round53-c2 reason falsely says required flags are absent from the registry

The reason at `plans/round54-entrytruth.json:888` says its `--source` and `--work` scratch arguments are ones “which the registry cell does not name”. `SKILL.md:640` explicitly names both: `python3 plans/round53_c2_tipstate.py --lane . --source <clean git clone of the landing tip> --work <scratch>`. The recorded invocation omitted documented required arguments; the cause is not an unspecified registry contract. This discrepancy is not caught by `entry_mode_ok`, whose contract checks script/forbidden flags, not completion of required arguments. Do not present setup failure from omitted named parameters as evidence of execution of the full documented entry.

## Passing checks and absence-producing command

Executed, exit 0 (audit completion, NOT a clean verdict):

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-54/w1/R5LedgerStatic/static-audit.py
```

- Strict duplicate-key-rejecting parse succeeds for both ledgers; schema `r54-entrytruth-v1`.
- Exactly 78 ledger rows and 78 registry names; set differences empty; one registry heading, no duplicate/malformed registry names.
- Exact requested per-row field sets: zero defects. 62 green, 16 red; every green has no reason/evidence noise.
- Imported canonical `round54_c2_entrytruth.entry_mode_ok`: zero entry-mode/script defects against each registry cell.
- All red reasons meet ten words; all evidence fragments are non-empty and under 200 characters (range 25–160).
- All 74 `r53-entry` labels match their r53 `kind: entry` argv exactly.
- No `lane-dot` rows exist (vacuous match, not execution evidence). All three `bare` rows mismatch as above.

## Residual risk and verification gaps

- `scratch-root-guard` has `chosen: hand-contract`, an explicit manual route not emitted by the frozen builder. Its `check .` matches the registry's check subcommand, so the mere label is not treated as an illegal-schema defect; provenance needs an independent receipt, especially given the exit contradiction.
- No gate, counter sweep, selftest, clone, network request, or alternative runtime was invoked. Actual exits, verbatim fragments, timing, hermeticity, laundering closure, clean-tree identity, and full canonical entry execution remain unverified here. No C1, saturation, or resume-continuity finding is asserted: outside this assignment.
- LSP unavailable: reading `xd://lsp` returned “No such tool”; status/references/definition/diagnostics could not be issued. Literal source inspection is the fallback, not semantic server proof.
- No tools installed; no scratch directory, clone, fixture, or temporary file created; no scratch cleanup required. Only scoped report/audit artifacts written. Frozen inputs unchanged.

## Defect row list

`adoption-check`, `anchor-digest-check`, `gate-flip-check`, `mutant-direction-check`, `round28-census`, `round35-c1-coverage`, `round38-c1-mutants`, `round40-c1-mutants`, `round46-c3`, `round51-surfaces`, `round52-c1`, `round53-c2`, `scratch-root-guard`, `sources-adopt`, `stage-scan`, `state-assertion-check`.

## Defect rows pasted (reviewed snapshot)

```json
{
  "adoption-check": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/adoption_check.py",
      "--lane",
      ".",
      "--expect",
      ".ufo/waves/round-33/claims/adoption-expect.json",
      "--census"
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 0.2
  },
  "anchor-digest-check": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/anchor_digest_check.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "DEFECT S173 anchor token=39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439 class=anchor-unbound detail=row-carries-no-capture-locator loc=corpus/",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 3.9
  },
  "gate-flip-check": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/gate_flip_check.py",
      "--lesson",
      "corpus/lessons/round-52.md"
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "FLIP line=36 flip_line=36 item=S191 shapes=flip: resolution=unresolved:no-line",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 0.1
  },
  "mutant-direction-check": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/mutant_direction_check.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "DIR N01 P1 declared=silence observed=silence ok",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 76.5
  },
  "round28-census": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round28_census.py",
      "--root",
      ".",
      "--revision",
      "536925b5320fa64298030b4ee76a58fc4b82723f"
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "\"c1\": { \"exit\": 0, \"findings\": [], \"metrics\":",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 2.1
  },
  "round35-c1-coverage": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round35_c1_verify.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "V4 DEFECT knowledge files=57 index rows=57 (want 42/42)",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 0.7
  },
  "round38-c1-mutants": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round38_c1_verify.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "PINS total=14 mismatched=0",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 115.6
  },
  "round40-c1-mutants": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round40_c1_verify.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "PINS total=3 mismatched=0",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 102.3
  },
  "round46-c3": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round46_c3_verify.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "V1 ok listed=8 wrong=0 extra=0",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 3.9
  },
  "round51-surfaces": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round51_surfaces.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "REV 17f90355c3ec17dcf15f7980d83f1943ae428fe5",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 0.1
  },
  "round52-c1": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/round52_c1_grader_audit.py",
      "--lane",
      "."
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "TASKS total=89 records=89 classified=88",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 0.1
  },
  "round53-c2": {
    "chosen": "bare",
    "entry_argv": [
      "python3",
      "plans/round53_c2_tipstate.py",
      "--lane",
      "."
    ],
    "entry_exit": 2,
    "entry_state": "red",
    "evidence": "SETUP --source and --work are required unless --dry",
    "reason": "the tip-state counter has no argument-free entry mode: bare invocation prints usage and exits 2; its entry contract requires --source and --work scratch arguments which the registry cell does not name",
    "sec": 0.1
  },
  "scratch-root-guard": {
    "chosen": "hand-contract",
    "entry_argv": [
      "python3",
      "plans/scratch_guard.py",
      "check",
      "."
    ],
    "entry_exit": 2,
    "entry_state": "red",
    "evidence": "CHECK red reason=sentinel-missing",
    "reason": "the gate's check entry requires the round sentinel file which exists only in an active round tree, so on a bare clean checkout it reports sentinel-missing and exits 1",
    "sec": 0.1
  },
  "sources-adopt": {
    "chosen": "bare",
    "entry_argv": [
      "python3",
      "plans/sources_adopt.py",
      "--lane",
      "."
    ],
    "entry_exit": 2,
    "entry_state": "red",
    "evidence": "usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]",
    "reason": "the adoption gate has no argument-free entry mode: bare invocation prints its usage and exits 2; its entry contract requires an adoption task (package and admit ids) which the registry cell does not name",
    "sec": 0.1
  },
  "stage-scan": {
    "chosen": "bare",
    "entry_argv": [
      "python3",
      "plans/stage_scan.py",
      "--lane",
      "."
    ],
    "entry_exit": 2,
    "entry_state": "red",
    "evidence": "ERROR unknown option --lane",
    "reason": "the stage scanner has no argument-free entry mode: bare invocation rejects the registry cell's --lane flag and exits 2; its entry contract takes positional stage inputs which the cell does not name",
    "sec": 0.1
  },
  "state-assertion-check": {
    "chosen": "r53-entry",
    "entry_argv": [
      "python3",
      "plans/state_check.py",
      "--summary"
    ],
    "entry_exit": 1,
    "entry_state": "red",
    "evidence": "assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5",
    "reason": "the instrument exits 1 on the clean tree at this tip; the evidence fragment is verbatim from its own output",
    "sec": 1.3
  }
}
```
