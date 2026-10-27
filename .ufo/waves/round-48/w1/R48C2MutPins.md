# R48C2MutPins — digest-pinned component mutation probe

## Scope, freeze, and detector

Axes: **coverage** (assigned C2 mutation sensitivity). Revision measured: `a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze), present as ancestor of clone HEAD `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`. The only later commits at measurement were `453ddfd` (dispatch evidence) and `bf783c1` (w1 handoff); `plans/round48_c2_verify.py` is absent and claims still say `Freeze amendments / None yet`. Thus stage-2 component pins/counter do **not** exist in the committed lane tree. I made no scored C2 run and did not invoke the full gate/probe or grader.

Instead, this unscored detector ran the committed round-46 C3 structural/dry legs V1, V3, V4, V5 (`--dry` only), V7, V8, V9, V10, V12. It excluded V2 (`pkg_gate --rerun`), V11 (captured grader execution), V6, and V13. It imports the unmodified round-46 counter and runs against focused scratch trees. Baseline's existing defects are V7 and V8, so a mutant is called killed only when it adds a new defect; unchanged baseline defects do not count as kills.

Stage-1 freeze check: `git merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD` returned 0; `git log --oneline a543d920..HEAD` printed `bf783c1 round-48: w1 ready handoff marker` and `453ddfd round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)`. No stage-2 freeze was found. Pin sanity at the measured tree: probe `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`, masked spec `560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e`, dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` all matched the round-46 counter pins. Receipt SHA-256 was `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`.

## Exact commands and outputs

Commands (all fixture-like trees stayed beneath the unique scratch root):

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2MutPins
export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2MutPins
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
# confirmed `git rev-parse --show-toplevel` = /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/lane
python3 /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/mut_driver.py <scratch-tree> <lane>/plans/round46_c3_verify.py
bash /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/run_mutations.sh
# after all mutations, same detector on pristine lane clone:
python3 /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/mut_driver.py /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/lane /fast/scratch/hyaku/kengaku-r48/R48C2MutPins/lane/plans/round46_c3_verify.py
```

Pristine baseline output (also reproduced after all mutation probes):

```text
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V7 DEFECT rows=5 tags=7 bad=[... tags missing=['both-print', 'toolchain'] ...]
V8 DEFECT order_exit=1 result=not-PASS
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
checks=9 defects=2
```

For compactness the abbreviated V7 `bad=[...]` above is the observed output with only its repeated unparsed-row details elided; the final missing tags were exactly `both-print` and `toolchain`. Mutants and detector outcomes (each mutation began from the same pristine focused tree; hashes are before→after):

| Mutant | Component and SHA-256 before → after | Observed new detector defect(s) | Verdict |
|---|---|---|---|
| capture-content | `test_outputs.py` `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` → `1839e95ae4ace6b6b0f402fabd8985e26f4306bb08cfb55c9b23e69d976e68aa` | V1 `wrong=['test_outputs.py']`; V10 capture not pinned; V12 S166 capture unresolved | killed |
| capture-manifest | `SHA256SUMS` `a44b38ea85e4611f62cd93104923e70f1e516200b2084d5f7500f8d50e26c496` → `0bc85be3ecf1ef1e35cae044788a8f6ac944b727eb724b10d210a575cddd3edb` | V1 `wrong=['Dockerfile']` | killed |
| capture-missing | `solve.sh` `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` → absent | V1 `wrong=['solve.sh']`; V12 S169 capture unresolved | killed |
| probe-content | probe `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26` → `2e59c965168425460155f6f8edb0a3d169fc93b2aebf19da6364af33f28746ed` | V5 `probe or dry table not at its freeze digest` | killed |
| spec-content | spec `f9a0e3ccbe5c0643c98995d41d4da3821ef27ddd3f86eee87b5a562c99db3171` → `4cbaf0d29f678094ea6381a2569b6ab611d8bd3d7bc05259333caab2dbf36a62` | `PACKAGE unreadable: ValueError: plans/pkg-spec-r46.json is not at its freeze digest (receipt_sha256 masked)`; all 9 detector legs reported DEFECT | killed |
| receipt-content | receipt `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277` → `47064e2e492781c4699953d300e1f8ba928bffea7f8b7427911fa125cdeba481` | V4 summary disagreed / false `match=yes`; V9 case table unequal | killed |
| receipt-comment | receipt `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277` → `2b891dec88aec18391e62f4d62e953db7a9dea9574bc57d6c4b2f9b8a813ad50` | no new defects; only baseline V7/V8 | survived (coverage finding) |
| dry-case-id | dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` → `dc05bdde4bb1ed882f7deb6c9477a00e2212e1af014ab793272093edefcf1903` | V4 case IDs differ; V5 pin mismatch; V10 DECISIVE keys differ | killed |
| dry-tag-line | dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` → `9fcc925a0535b68a1c5ad8f907936795b10594343629d02c6f0e8321ce28ffce` | V5 pin mismatch | killed |
| masked receipt pin | spec `f9a0e3ccbe5c0643c98995d41d4da3821ef27ddd3f86eee87b5a562c99db3171` → `7d6aaa2b9b45795007e22cb396237891b121034c9e2e3da79fec276928cd3de0` | no new defects; only baseline V7/V8 | survived (coverage finding) |

The dry-tag mutation did not add a V7 defect: its baseline V7 parser rejects the existing `not exercised` rows, so the altered tag was not independently detected there; V5 did kill it by the dry-table pin. This is a useful limit on semantic leg evidence.

A first probe mutation attempt used a nonexistent replacement phrase and raised `AssertionError` before changing its scratch file or running the detector. I corrected the needle to the actual `ORDER RULE ... Q30` text and completed the probe-content mutant above. No result from the failed attempt is counted.

## Restoration, source access, limits, verdict

All tampered bytes existed only in separate scratch copies; the pristine clone's post-probe hashes remained: counter `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`, probe `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`, spec `f9a0e3ccbe5c0643c98995d41d4da3821ef27ddd3f86eee87b5a562c99db3171`, receipt `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`, dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`. Post-mutation pristine detector exactly reproduced baseline; all per-mutant scratch copies are disposable and will be removed before yield.

No external source was opened; source inspection was local to the lane. Local sources: `plans/round-48-claims.md` (opened 2026-10-27; `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md`; quote: “No probe of the C2 package runs before the stage-2 commit.”) and `corpus/lessons/round-46-verifier-spotcheck.md` (opened 2026-10-27; `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md`; quote: “V7 lacks violating cases for `both-print` and `toolchain`.”). The round-46 integrated probe hash is `67a8f4a6…`; its distinct wave artifact cited by the claims hashes `22b7779e…`, so the artifacts are not byte-identical despite the claims' “integrated verbatim” wording. No conclusion about round-48 admission is made.

Limits: stage-2 counter/pins were unavailable; detector is the round-46 dry/structural subset, not the frozen round-48 battery and not the full gate. Therefore survivor results are coverage findings, not admission judgments. Receipt content mutation is checked semantically by V4/V9 here, but a comment-only receipt mutation survives these legs; changing only the spec's masked `receipt_sha256` field also survives. Both gaps require explicit stage-2 leg/control coverage to assess; no post-stage-2 result is claimed.

**VERDICT: INCONCLUSIVE for the frozen R48-C2 mutation battery (stage 2 absent); 8/10 isolated mutants killed by this bounded detector, 2 survived, with the baseline failure recorded above.**
