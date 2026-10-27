# R45RevProvince — PROVINCE paragraph review

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`). Scope: the Round 45 paragraph at `PROVINCE.md` final paragraph; no lane files changed.

## Findings

No actionable defect found in the scoped Round 45 paragraph.

- Its boundary is consistent with the immediately preceding Round 44 paragraph: both describe the captured grader's bounded scoring behavior and explicitly leave the attack/recovery method outside kengaku's ownership (`PROVINCE.md`, Round 44 and Round 45 paragraphs). Round 43's routing says differential-cryptanalysis technique was unowned and routed to the orchestrator; Round 45 likewise does not claim cryptanalysis or forensic/file-recovery technique as kengaku ground. The password-recovery entry itself describes the observed check as exact line membership of a public constant, not recovered-password correctness (`corpus/knowledge/tb2-password-recovery-grader.md:16-25`).
- Paragraph figures agree with the receipt: `corpus/evidence/round45/password-recovery-probe.txt` ends `regrade cases=16 differ=0` and `cases=16 observed_pass=5 observed_fail=11 mismatches=0`; its listed 16 cases have matching predictions. The eight cited source IDs map to the eight named captures, S149–S156 (`corpus/SOURCES.md` S149–S156). The `F1 constant-compare` characterization is consistent with the package's explicit second-exemplar wording after feal-linear (`corpus/knowledge/tb2-password-recovery-grader.md:17-24`) and the feal-linear entry's 100-constant substring check (`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md:17-25`).
- No sibling is named in the Round 45 paragraph, so it makes no sibling ownership attribution that could be inaccurate. R45ConnSibling's identified direct overlaps (souji's refusal/census guards; tameshi's reusable fixture/mutation method; kumitate's own gates and route/failure taxonomy) concern the new C1 fixture-fence predicate, not the C2 captured-grader interpretation described in this paragraph (`.ufo/waves/round-45/w1/R45ConnSibling.md:7-14`). The paragraph says the C2 run used a bwrap envelope; it does not claim ownership of a general-purpose sandbox runner or mutation method. Thus omission of those C1 disclaimers does not create overclaim in this C2-only paragraph. The sibling PROVINCE checks agree with the cited boundary: tameshi owns reusable verification craft but refuses product-domain gate code (`tameshi-shokunin/PROVINCE.md:3-17`); kumitate names its owned gates and routes prompt/research/orchestration adjacencies (`kumitate-shokunin/PROVINCE.md:12-30`); souji calls its guard a refusal fence and does not acquire kumitate orchestration (`souji-shokunin/PROVINCE.md:101-107`).

## Verification evidence

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc`.
- `grep -n "bwrap\\|unshare" /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/password_recovery_probe.py | head -15` → `77:BWRAP = "/usr/bin/bwrap"`; `214: argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", ...]`.
- `grep -n "S149\\|S150\\|S151\\|S152\\|S153\\|S154\\|S155\\|S156" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` → rows S149–S156, each pinned to commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; the rows identify test_outputs.py, instruction.md, setup.sh, Dockerfile, test.sh, README.md, solve.sh and task.toml.
- `grep -n "F1" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` → line 80: `F1 constant-compare, named before this probe ran.` The corresponding grep of the password entry returns line 18: `F1 constant-compare family ... (after feal-linear-cryptanalysis, round 44)`.
- `grep -n "shokunin/\\|tameshi\\|chousa\\|kotoba\\|kumitate\\|kama\\|kake\\|kasegi\\|kagi\\|kaidoku\\|souji\\|mado\\|mori\\|kotodama\\|lore\\|tabi\\|revenger\\|audio\\|game-dev" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/tb2-password-recovery-grader.md` → no output (exit 1); the Round 45 PROVINCE paragraph itself names no siblings.
- No fixture build, counter, or probe was run for this review; therefore no envelope measurement is claimed.

VERDICT: province-defects-0
