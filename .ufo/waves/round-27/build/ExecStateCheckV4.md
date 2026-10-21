# ExecStateCheckV4 — round 27

Axis: calibration. Scope: implement frozen P4a–P4e in the private writer clone only.

## Files
- Clone base observed: `11a7fc8c64dc5d634331be24ccf5936f84a11f03`; registered base: `b5719440e5eee46c1886fddbdf7bdc1624829454` (`plans/round-27-claims.md:102-129`).
- Clone file changed: `plans/state_check.py` — SHA-256 `29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32`.
- Report path: `.ufo/waves/round-27/build/ExecStateCheckV4.md`.

## Behavior
- v4 adds frozen P4a–P4e ids for scorecard claims, bidirectional README artifacts, wave records and named Git trees, grader population/families, and S043–S048 used-by cells.
- P4e scans only the two base candidate paths: `corpus/knowledge/grader-perturbation-audit.md` and `corpus/lessons/round-26.md`; later round files do not widen the population.
- P4b classifies the exact README:283–285 source-support correction as SUPERSEDED with the re-derived six-id set. P4 corrections otherwise accept full-token R27-E only; inherited P2/P3 parsing still accepts R27/R29.
- P4a C2 reads committed round-26 state-check receipts and does not invoke `state_check.py`; P4c selects a Git repository only after read-only `git cat-file -e b5719440e5eee46c1886fddbdf7bdc1624829454^{commit}`; absent lane history yields `OFFLINE_UNVERIFIABLE`.
- `--selftest` exercises one pristine/mutated red case per P4 class, removed/wrong/partial base-erratum controls, P4 R27-E acceptance/R29-E rejection, inherited R27/R29 acceptance, and P2e/P3c OUT_OF_POPULATION retention.

## Retained evidence
- v3 frozen-base baseline: `python3 -B /tmp/kengaku-r27-base/plans/state_check.py --json --root /tmp/kengaku-r27-base` → exit 0; P2/P3 keyed projection: 298 records, SHA-256 `986ad1876a61855de34882ec76d297bcc1dd7324d55c4b5eb5b83fcd94248b59`.
- v4 base export: `python3 -B /tmp/kengaku-r27-ExecStateCheckV4/plans/state_check.py --summary --root /tmp/kengaku-r27-base` → `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`; exit 0.
- v4 clone: `python3 -B /tmp/kengaku-r27-ExecStateCheckV4/plans/state_check.py --summary --root /tmp/kengaku-r27-ExecStateCheckV4` → `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`; exit 0.
- Live-lane read-only: `python3 -B /tmp/kengaku-r27-ExecStateCheckV4/plans/state_check.py --summary --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` → `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`; exit 0.
- Sole P4 supersession on base/clone/live: `P4b.readme.covers.round26-sources` derives ids S043–S048 (six); the exact frozen README erratum anchor is at line 283 in base/clone and line 284 live.
- v4 `--json --root /tmp/kengaku-r27-base` → exit 0; P2/P3 projection: 298 records, SHA-256 `986ad1876a61855de34882ec76d297bcc1dd7324d55c4b5eb5b83fcd94248b59` (same as captured v3 projection).
- `python3 -B /tmp/kengaku-r27-ExecStateCheckV4/plans/state_check.py --selftest` → exit 0; P4a–P4e red mutations, exact-base/R27/R29 correction controls, and P2e/P3c OUT_OF_POPULATION controls passed.
- `command -v pyright-langserver || command -v basedpyright-langserver || command -v pylsp || command -v jedi-language-server` → no result; no LSP client available.

## Handoff
- Main owns integration. P4b recognizes the exact pre-existing README source-support erratum (base lines 283–285; live anchor line 284); it is SUPERSEDED, not a new mismatch or repair discovery.
- P4 adds 49 frozen assertion ids (48 comparable results plus the inventory assertion); no axis-score change is claimed.
- Risks/blockers: none. No install/update performed.

VERDICT: v4 implements P4a–P4e; base, clone and read-only live summaries have zero mismatches, P4b is correctly superseded, and all assigned red selftests pass.
