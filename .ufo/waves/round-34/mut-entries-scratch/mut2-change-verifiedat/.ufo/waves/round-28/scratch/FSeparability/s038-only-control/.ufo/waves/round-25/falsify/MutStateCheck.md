ATTACKS: C2 state_check.py regression detection: POINTER_ONLY_RE, ABSENT token grammar, SUPERSEDE_RE, registry id cap, AXIS_ANCHOR_CONTENT.
Axes: calibration (primary); detector sensitivity and exact restoration (probe controls).
Scope: only /tmp/k25w2-MutStateCheck/ was mutated; no live lane fixes, index changes, endpoint requests, or runtime judging.
Inputs: git archives 8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b -> scratch/tip; 6180e4fb92e90c0b172e9788e2c765d097f2e142 -> scratch/base; scratch=/tmp/k25w2-MutStateCheck.
Reproduce archives: `mkdir -p "$scratch"/{tip,base,tmp}`; `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive <revision> | tar -x -C "$scratch"/<tip-or-base>`.
Detector: `python3 /tmp/k25w2-MutStateCheck/detector.py <phase>` runs the following identical bounded suite (240s/command, three commands concurrently; mutants strictly one at a time).
S: `python3 /tmp/k25w2-MutStateCheck/tip/plans/state_check.py --selftest`.
T: `python3 /tmp/k25w2-MutStateCheck/tip/plans/state_check.py --summary` (default root, not live lane).
B: `python3 /tmp/k25w2-MutStateCheck/tip/plans/state_check.py --root /tmp/k25w2-MutStateCheck/base --summary`.
All runs: cwd=scratch/tip; TMPDIR=scratch/tmp; PYTHONDONTWRITEBYTECODE=1. Full stdout/stderr/exit/hash receipts: scratch/pristine.json and scratch/{pointer,absent,supersede,cap,anchor}-{mutated,restored}.json.
Pristine S: exit 0, `[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, sources supersession, ABSENT rule)`.
Pristine T: exit 0; `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3`; `VERDICT: PASS — all comparable frozen assertions match`.
Pristine B: exit 1; `assertions=242 match=228 mismatch=11 superseded=0 offline_unverifiable=3`; `VERDICT: FAIL — at least one frozen assertion mismatches`.
B is intentionally red at pristine: its red exit alone is inconclusive, NEVER counted as a mutant kill. Kills below require green-to-red S or T.
Expected detectors: S pointer-only prose rejection (state_check.py:1171-1179); S frozen registry population (1181-1194); S ABSENT rule (1210-1221); T P2a correction re-derivation; P2b content check (538-545).
| Mutant (plans/state_check.py) | Single change | Actual S/T/B exits and output delta | Result |
|---|---|---|---|
| pointer :193 | Remove final `$` from POINTER_ONLY_RE | 1/0/1; S stderr `selftest: prose-evidence mutation survived pointer-only`; T unchanged; B `assertions=242 match=230 mismatch=9 superseded=0 offline_unverifiable=3` | KILLED by S |
| absent :924 | Replace word-bounded `r"\bABSENT\b"` with substring `r"ABSENT"` | 0/0/1; all three complete stdout/stderr outputs byte-identical to pristine | SURVIVED |
| supersede :192 | Replace correction-prefix grammar with `^.*supersedes ...`, retaining both capture groups and token checks | 0/0/1; all three complete outputs byte-identical to pristine | SURVIVED |
| cap :185 | SOURCES_BASE_MAX_ID 26 -> 27 | 1/1/1; S stderr `selftest: base-population census wrong: rows 27; malformed 0; A=25 C=2; mined=19 queued=6 rejected=2`; T `assertions=236 match=232 mismatch=1 superseded=0 offline_unverifiable=3`; B unchanged | KILLED by S and T |
| anchor :190 | AXIS_ANCHOR_CONTENT[":162"] -> empty tuple (range-only acceptance) | 0/0/1; all three complete outputs byte-identical to pristine | SURVIVED |
Cap T finding: `MISMATCH: P2a.capability.sources-registry:557`; observed `rows 27; malformed 0; A=25 C=2; mined=19 queued=5 rejected=3`, contradicting correction tokens at SCORECARD.md:646.
Coverage findings: selftest:1211 covers only no-marker versus exact ABSENT, 1197-1201 covers valid correction/wrong values but no malformed prefix, and run_selftest:1116-1224 never exercises check_axis_table.
These are regression-detector survivors, not evidence that the pristine implementation currently accepts those weakened contracts; no contract changes or fixes made.
SHA-256 H0 (pristine and EVERY restored state): 8be6122240adb0aad0384978049f4c1f07b53883197d54b411f0ec864ec989d0.
Each cycle was H0 -> mutant hash below -> H0; every suite also recorded identical before/after hashes during execution.
Pointer mutant: 94438dbb7437a6a563be952cda850c73d01c8b8848c5aa47a5f3c564c01aaeb7.
ABSENT mutant: 535a88de78f297ef92352044107cbf6d9c7e6f4dc5ee57479512d0c062fdbdaf.
SUPERSEDE mutant: e92ab776b92622dfcc2c3148fee93be3f0505629d2ba10be06e5dd3e4097750c.
Cap mutant: 2bc92110fe881633afa0cd534533123c2845d86dba7b6a830d84b26fce3e1967.
Anchor mutant: cef55331b214c2db3b635275ee6a442d2e02dcc1c09a75ed55dcdd77130427d1.
Restoration evidence: five restored receipts each reproduce pristine S/T/B outputs and exits exactly; aggregation printed `all_restored_exact=True`. Total: 33 command executions, no timeouts.
Detector SHA-256: 5bbcf50bbfc265d2501127ecef08d97c0f6aba1fcfce4a8a2b2370d9a303120c.
VERDICT: PARTIAL — 2/5 mutants killed; ABSENT boundaries, correction-prefix grammar, and anchor-content removal survive all assigned checks; exact source restoration complete.
Installs: none.
