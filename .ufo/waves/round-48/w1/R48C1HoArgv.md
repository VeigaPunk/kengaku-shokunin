# R48C1HoArgv — benign argv shapes

Axis named: **calibration** (honest-fixture acceptance and truthful classification).

## Freeze and measurement boundary

Clone: `/fast/scratch/hyaku/kengaku-r48/R48C1HoArgv/lane`; `git -C ... rev-parse HEAD` initially returned `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (wave handoff marker). The clone log identifies stage-1 freeze `a543d92083557dd9b33ee674e9b99b03411f80af`.

Exact freeze check: `git show a543d92083557dd9b33ee674e9b99b03411f80af:plans/round-48-claims.md | sha256sum` and `sha256sum plans/round-48-claims.md` both returned `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672`; `git merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD` succeeded (`a543d920 IS ancestor of HEAD`). `git ls-tree -r --name-only a543d920 plans/ | grep -i round48` and same command at HEAD both returned `(none)`. Thus the stage-1 freeze predates this inspection, but stage-2 counter/population freeze is absent and `plans/round48_c1_verify.py` is not present. **No scored counter or probe was run.** I cannot evidence BENIGN-ADMIT/touches=0 on the requested v3 counter before its committed stage-2 freeze.

## Probe candidates / evidence

The base fence is the frozen fence contract at `plans/fixture_fence.py` revision `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` (claims call this the before-value). Its `_argv` uses lexical `os.path.normpath`, checks containment with `_inside`, accepts anchor options in token order, and checks the normalized `--lane` is an in-fixture repository. The round-46 held-out report provides precedent: `--lane <lane>/../lane --verbose` was `ADMIT touches=0`; its second argv/env-token fixture was also `ADMIT touches=0`. The round-46 detector labeled admissions as LEAK despite `touches=0`, explicitly because it classified admission rather than observed outside access. This supports testing the same benign classes as honest fixtures, not labeling them hostile.

Candidates to include in the stage-2 honest population, authored against the base contract:

1. **Relative dot-dot normalization:** ordinary plain-init repo at `d/repo`, argv `--lane repo/child/../..` is not suitable (normalizes to `d`, not the repo); use `--lane repo/../repo` instead, which normalizes to the same in-d repo. Expected behavioral label: `BENIGN-ADMIT`, touches=0.
2. **Environment-mediated token:** pass an argv value obtained by the caller from an environment variable whose value is `repo` (the fence receives the expanded ordinary string); keep `d/repo` the lane. Expected `BENIGN-ADMIT`, touches=0. A literal `$LANE` path is not an equivalent positive control unless a directory with that literal name exists; do not conflate shell expansion with fence-side expansion.
3. **Anchor option order:** same ordinary repo, reorder recognized options (e.g. `--verbose --evidence-ref evidence --lane repo` and `--evidence-ref evidence --lane repo --verbose`). `_argv`'s anchor parser accepts recognized options in any order. Expected `BENIGN-ADMIT`, touches=0.
4. **Order-tool contract:** do not permute the `order` tool's options: base contract explicitly requires `--lane`, `--claims`, `--receipt` in that order. Exercise only benign path spellings for values while preserving that contract, e.g. lane `repo/../repo`, claims `./claims.md`, receipt `./receipt.txt`; expected `BENIGN-ADMIT`, touches=0.

These are candidate descriptions, not observed executions; the stage-2 population must pin the actual authored fixture modules and re-run them under its frozen counter. I found no demonstrated real gap in these candidates. I intentionally make no claim about C1 admission.

## Exact commands and observed outputs

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` → `Cloning into 'lane'... done.`
- `git -C lane rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`.
- Freeze hash and ancestry commands above → identical hashes and successful ancestry check.
- `git ls-tree -r --name-only a543d920 plans/ | grep -i round48` and at HEAD → `(none)`.
- Extracted base evidence only: `git show 0f77f9b27931b3c76b3d095fc0fa70edb79556d9:plans/fixture_fence.py > .../base_fence.py`; no fence execution.

Revision measured: `a543d92083557dd9b33ee674e9b99b03411f80af` for the freeze-presence check; base-fence behavior contract referenced at `0f77f9b27931b3c76b3d095fc0fa70edb79556d9`. No measurement receipt / REV line exists because no scored run was permitted before stage 2.

Sources opened were local repository artifacts only; no external URL was opened. Access date: 2026-10-27. Located quotations: claims §C1 “a fixture admitted with `touches=0` is reported as `BENIGN-ADMIT`”; round-46 argv report, first probe bullet: “`--lane <lane>/../lane --verbose`; `FENCE-RUN ... ADMIT touches=0`”.

Limits: candidates are descriptions, not counter-validated fixture code or receipts. The stage-2 freeze and pinned v3 counter are the missing prerequisite for the required behavioral classification. Scratch was removed before report completion.

VERDICT: no scored run; stage-2 freeze absent. No real outside-access gap established; submit the four candidate shape families to stage-2 population author for frozen execution.