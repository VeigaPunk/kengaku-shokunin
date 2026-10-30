# R8CounterSoundness — scoped findings (R55-C2 entry-argv counter soundness hunt)

Seat: R8CounterSoundness (reviewer, attack share). Target: `plans/round55_c2_entryargv.py`
(landed live 12:38, untracked sibling build; selftest 4/4 at probe time). Full route
list with runnable fixtures: `R8CounterSoundness/routes.md`; raw probe output:
`R8CounterSoundness/receipts/r55-probe-results.txt`.

## Verdict

The binding legs close the argv channel: L1's exact token equality plus the fact that
`run_row` executes the **registry-parsed** argv (not the ledger's) kill the canonical
laundering class twice; wrappers, absolute paths, `env`/`exec -a`, and unicode
look-alike tokens all fail closed (reproduced). The two frozen fixture kills reproduce
against the landed counter.

**One kill-rule candidate survives.** A gate that fingerprints the counter's inherited
hermetic worker-clone environment (marker env vars + `w<i>/src` cwd layout) passes the
counter `PREDICATE R55-C2 pass` with all static legs clean (`l1=l2=l3=0`) while the
row's registry-declared entry exits 1 under both a plain environment and the controls'
own hermetic ground-truth methodology (hermetic env, repo-root cwd). Runnable fixture:
`routes.md` F1b (files + argv + ledger row included; executed, exit codes on record).
A weaker env-only form (F1) survives under plain-env ground truth only.

Not kills but real gaps: L4 evidence fragments are self-referential substrings (a false
`reason` passes when the fragment occurs in the script's own failing output — F2); L3's
source-text flag enumeration misses runtime-built flags (F4a), `--mod=value` equals
forms (F4b), and argparse builtins like `--help` (F4c) — all behind L1's exact binding,
so each surviving cell form is observationally truthful.

## Recommendation to L1

Judge F1b against the frozen kill rule ("all static legs clean … passes … while the
row's registry-declared entry truly exits otherwise"). If admitted as a soundness
break, calibration holds at 9 per the rule; a repo-root-cwd re-execution leg (or
ground-truthing rows from the repo-root cwd rather than the worker clone) closes the
channel without touching the frozen predicates. F2/F4 classes are hardness notes for
the counter's backlog, not claim killers.
