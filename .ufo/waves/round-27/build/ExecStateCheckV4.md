# ExecStateCheckV4 — round 27

Axis: calibration. Scope: frozen P4a–P4e in the private writer clone.

## Files
- Clone base observed: `11a7fc8c64dc5d634331be24ccf5936f84a11f03`; registered C2 base: `b5719440e5eee46c1886fddbdf7bdc1624829454`.
- Clone file changed: `plans/state_check.py` — SHA-256 `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c`.
- Exclusive advisory report: `.ufo/waves/round-27/build/ExecStateCheckV4.md`. No other clone or live-lane files written.

## Behavior
- P4a checks round-26 claim/revision counters from committed receipts, command-derived population metrics, and the four-numeric-repair plus missing-index split. The eight score/verdict tokens are explicitly `OFFLINE_UNVERIFIABLE`, not compared to the same scorecard's axis table (`plans/state_check.py:2105-2120,2431-2456`).
- P4b checks README artifact rows in both directions; exact base source-support erratum is `SUPERSEDED` with S043–S048 re-derived.
- P4c verifies role/seat mappings, unique/disjoint assignment agentIds, exact dead-seat agentId mapping, and receipt-derived recovery count. P4c total-139 becomes `OFFLINE_UNVERIFIABLE` without the recovery receipt; Git tree checks require read-only proof that candidate repository contains base commit (`:2672-2697,2944-2990`).
- P4d derives counts and grader split from the four raw JSONL files, cross-checks manifest, grader JSON pins/families and oracle, and discloses unmapped audit metrics as `OFFLINE_UNVERIFIABLE` (`:3103-3174,3225-3256`).
- P4e's frozen candidate files are only `corpus/knowledge/grader-perturbation-audit.md` and `corpus/lessons/round-26.md`; later round files and S043 supersession-only references do not widen citing-use population (`:3469-3488`).
- `P4Evidence` allows only `grader_perturb.py --summary`, `--json`, and independent oracle; P4a reads committed state-check receipts and never recurses into `state_check.py` (`:1930-1940,2108-2120`).
- Selftests cover P4a final C2 count, P4b production dispatch, P4c role/dead/agent-id/assignment uniqueness, P4d numerator/denominator and full-vs-partial/wrong/R29 corrections, P4e, and rendered OUT_OF_POPULATION disclosure.

## Retained evidence
- `python3 -B plans/state_check.py --summary --root /tmp/kengaku-r27-base` → `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`; exit 0. All P4 MISMATCH lines: none.
- Same command on clone `/tmp/kengaku-r27-ExecStateCheckV4` and read-only live lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` → same first-line counts and exit 0; all P4 MISMATCH lines: none.
- Base JSON P4 inventory: 51 ids; `MATCH=48`, `OFFLINE_UNVERIFIABLE=2` (`P4a.scorecard.score-tokens-unverifiable`, `P4d.unmapped-numerics`), `SUPERSEDED=1` (`P4b.readme.covers.round26-sources`), `MISMATCH=0`.
- README erratum: exact frozen anchor at line 283 in base/clone, line 284 live; derived source ids S043–S048. Its P4b assertion is the sole P4 supersession.
- P2/P3 JSON projection, frozen v3 base vs v4 base: 298 records each, SHA-256 `92b54186d2a6fa011f9889a10cd38a0b8aa5d52960a51aeef3d28024c2f0f637`; both commands exit 0.
- `python3 -B plans/state_check.py --selftest` → `ALL PASS`; exit 0. Includes P4a `278→279` red, P4b dispatch/inventory, P4c role and identity reds, P4d denominator red and R27-E acceptance with partial/wrong/R29 rejection, plus summary OUT_OF_POPULATION rendering.
- `plans/fixtures/r27/p4_mutate.py --checker /tmp/kengaku-r27-ExecStateCheckV4/plans/state_check.py --repo /home/vgpnk/Projects/shokunin/kengaku-shokunin --base b5719440e5eee46c1886fddbdf7bdc1624829454` → `5/5 mutants red`; per-class base mismatch count 0; exit 0.
- LSP command discovery (`pyright-langserver`, `basedpyright-langserver`, `pylsp`, `jedi-language-server`) returned no executable; no LSP use was available.

## Handoff
- Main owns integration. The live lane includes later OUT_OF_POPULATION disclosures, while P4e remains frozen to base candidate paths. No P4 mismatch or score change is claimed.
- No blocker. No tools installed or updated.

VERDICT: P4a–P4e implementation and red controls are complete; v3 P2/P3 results are identical on base, and base/clone/live have zero P4 mismatches.
