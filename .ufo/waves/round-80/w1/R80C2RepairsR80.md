# R80C2RepairsR80 — independent repair re-derivation

Axes: coverage (held L0 cap) and calibration (held ceiling 10). Advisory only; no predicate, target, control, or kill rule changed.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`. Measured master: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (integration; unchanged at the recorded final tip query). All `TIP` shorthand below means this exact hash. Files changed: this report only. No installs. LSP was unavailable in the mounted tool inventory; no symbol refactor was needed.

## Findings and required L1 corrections

- **V1: agree on verdict; not byte-identical.** A single shared clean clone at TIP ran the retired counter against `148801a6`: `DEFECTS n=0`, `PREDICATE R78-C1 pass`, exit 0. The complete instrument output differs from the committed repair receipt only in `WORKTREE clean` versus its honest historical `WORKTREE dirty`. Do not claim an exact clean-tree receipt reproduction without disclosing that difference. Added `--work "$S/work"` solely because the tool unconditionally creates its default `/tmp/r78-c1` even in ordinary audit mode; the seat forbids writes outside scratch. Clone root assertion preceded checkout. The outer receipt stamp is the freeze tip, while the inner instrument tip is the audited historical revision; those are distinct roles, not conflicting verdicts.
- **V2: agree.** Committed round-79 census receipts contain 25 W04 lines before and 26 after; the only added warning is S256. The lesson correction is accurate.
- **V3: disagree with the assigned revision / lesson's word “base.”** At `dce7c275`, all 16 grader-table executed cells are quantified; exact bare `executed` = 0 and exact `recipe-unexecuted` = 0. At `148801a6`, the same table has 12 bare executed + 1 recipe-unexecuted + 3 quantified, so “13 unquantified” is historically correct there, NOT at the specified base. L1 should qualify the correction with the historical revision `148801a6` instead of saying “base SKILL.md”; this does not change the frozen repair's numerical content. An initial naive whole-file cell count mistakenly counted the column heading; its raw diagnostic is retained below and explicitly superseded by the table-only count. No count from that diagnostic supports the finding.
- **V4: agree on 15 words and span; assignment path is wrong.** `corpus/evidence/round79/sources/git-status.txt` is absent. The tracked capture is `corpus/evidence/round78/sources/git-status.html`, lines 2322–2326. The 15-word quote joins TWO sentences: “Show untracked files.” and “The mode parameter is used to specify the handling of untracked files.” L1 should use the actual round78 HTML path and say “15-word quote/two sentences,” not “15-word sentence.” The lesson supplies the right span but calls it a sentence.
- **V5: agree that keeping with a disclosed reason is honest.** Read-only live validator exits 0 and emits S256's duplicate-URL warning. Committed S180 and S256 really share the same pinned README URL and sha256, but S180 scopes validation-before-release and S256 scopes the containerized execution surface. This is disclosed reuse, not independent-source corroboration. The stronger statement “would leave that taxonomy unsourced” is an editorial justification rather than something the duplicate detector proves; one could instead consolidate scopes. No need to remove the row to resolve this finding.
- **V6: hashes/ancestor/exits agree for worktree candidates; disagree that the repair artifacts were committed at measured TIP.** Both worktree receipts name real tools, matching their committed TIP SHA256, and stamp TIP itself (ancestor check rc 0). Independent committed-revision replay gives R79-C1 pass/exit 0 and R79-C2 pass/exit 0. However, `git show TIP:corpus/evidence/round80/r79-{c1,c2}-after.txt` fails with rc 128 for BOTH files. They exist on disk but are not in the measured commit. L1 must integrate both receipts before claiming frozen C2 closure. The first attempted stamp extraction from absent committed files produced meaningless empty-stamp hash/ancestor diagnostics; those are retained only as failed-attempt evidence, superseded by the explicitly labeled worktree-only measurements. The worktree `WORKTREE dirty` stamps are not clean-tree claims.

## V5 exact command and retained output

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`

Exit: 0. Relevant exact stdout (the other 25 W04 lines are the already-recorded duplicate scopes):

```text
kengaku	W04	S256 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

Initial read failure: `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round79/sources/git-status.txt:2318-2330` returned `Path '/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round79/sources/git-status.txt' not found`. Tracked-path enumeration resolved the actual source, retained below.

## Evidence appendix

These are exact retained subprocess outputs, including failures and explicitly superseded preliminary diagnostics. “select”, “count”, and “compare” in command labels describe the Python post-processing used in the measurement session, not additional shell binaries. The table count isolates text between `## Decision table — grader class → offline replay recipe` and the next level-two heading, drops header/separator rows, splits Markdown rows on `|`, and compares stripped third cells exactly. W04 counts test `"\tW04\t" in line`. Quote words use whitespace split. SHA256 hashes use committed `git show` bytes.

### V2

```text
$ git show TIP:corpus/evidence/round79/census-{before,after}.txt; count lines with TSV code W04
before W04=25
after W04=26
--- before
+++ after
@@ -23,4 +23,5 @@
 kengaku	W04	S234 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
 kengaku	W04	S237 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
 kengaku	W04	S243 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py across scopes
+kengaku	W04	S256 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md across scopes
 kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

### V3

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show dce7c275:SKILL.md; count exact table cells
bare executed=1
recipe-unexecuted=0
unquantified=1
| class | count | executed | replay recipe | receipt pointer |
```

### V4 paths

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only 6669fe72e59718acc1a0f32a92849a544b0b2f1c corpus/evidence; select git-status captures
corpus/evidence/round78/sources/git-status.html
```

### V4 capture

```text
$ git show TIP:corpus/evidence/round78/sources/git-status.html; capture lines 2322-2326
2322: <p>Show untracked files.</p>
2323: <div class="openblock">
2324: <div class="content">
2325: <div class="paragraph">
2326: <p>The mode parameter is used to specify the handling of untracked files.
```

### V4 words

```text
$ count whitespace words in the quoted sentence
Show untracked files. The mode parameter is used to specify the handling of untracked files.
words=15
```

### READ FAILURE

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:corpus/evidence/round80/r79-c1-after.txt
fatal: path 'corpus/evidence/round80/r79-c1-after.txt' exists on disk, but not in '6669fe72e59718acc1a0f32a92849a544b0b2f1c'
EXIT 128
```

### V6 r79-c1-after.txt

```text
$ git show TIP:corpus/evidence/round80/r79-c1-after.txt; sha256 TOOL at TIP; git merge-base --is-ancestor LANE_TIP TIP

computed TOOL_SHA 096551990a6e58f53b2b8a3a9cd9d1ee480495f1aca0c28df21ce760cc9fb9a6
sha_match=False tool_exists=True ancestor_exit=128
```

### READ FAILURE

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:corpus/evidence/round80/r79-c2-after.txt
fatal: path 'corpus/evidence/round80/r79-c2-after.txt' exists on disk, but not in '6669fe72e59718acc1a0f32a92849a544b0b2f1c'
EXIT 128
```

### V6 r79-c2-after.txt

```text
$ git show TIP:corpus/evidence/round80/r79-c2-after.txt; sha256 TOOL at TIP; git merge-base --is-ancestor LANE_TIP TIP

computed TOOL_SHA 096551990a6e58f53b2b8a3a9cd9d1ee480495f1aca0c28df21ce760cc9fb9a6
sha_match=False tool_exists=True ancestor_exit=128
```

### Committed lesson corrections

```text
$ git show TIP:corpus/lessons/round-80.md; lines 72-98
72: ## Corrections (round-79 spot-check routed ids, discharged here)
73: 
74: - **R79-V1** — the round-79 report claimed the retired `round78-c1` gate's verdict was re-verified in
75:   `gates-clean.txt`; that block printed `SETUP unresolved revision 'worktree'` / `EXIT 1`. The
76:   spot-check's second repair option is taken rather than a prose retraction:
77:   `python3 plans/round78_c1_class_member_ledger.py --lane . --rev 148801a6` prints
78:   `PREDICATE R78-C1 pass`, committed with a stamp at
79:   `corpus/evidence/round80/v1-r78-c1-at-148801a6.txt`.
80: - **R79-V2** — round-79's Sources & frontier said "25 `W04` … unchanged in both". Wrong: the census
81:   receipts report **25 before, 26 after** (the `diff` adds S256's duplicate-URL line); rc 0 in both.
82:   W04 is a warning class, not a failure.
83: - **R79-V3** — round-79's "13 rows said a bare `executed`" is off by one. The base `SKILL.md` table
84:   has 12 bare `executed` cells plus one `recipe-unexecuted` (`container-image`) — i.e. **13
85:   unquantified** rows, not 13 bare-executed rows.
86: - **R79-V4** — R78-D4's S254 anchor is re-stated: the quoted 15-word sentence spans **capture lines
87:   2322–2326** ("Show untracked files. … The mode parameter is used to specify the handling of
88:   untracked files."), not one sentence at line 2322.
89: - **R79-V5** — **S256 duplicate-URL kept**: S256 repeats S180's URL for a distinct scope (the
90:   harness's own execution model, which grounds the R79 blocker taxonomy and this round's
91:   replay-surface limit). Scoping it out would leave that taxonomy unsourced; the new `W04` is stated
92:   in this lesson's census reading instead of hidden.
93: - **R79-V6** — the round-79 after receipts carried no revision stamp. Both counters are re-minted at
94:   the round-80 tip by `plans/round78_restamp.py` (`plans/round80-restamp.json`):
95:   `corpus/evidence/round80/r79-c1-after.txt` and `r79-c2-after.txt` each carry
96:   `LANE_TIP`/`TOOL`/`TOOL_SHA`/`WORKTREE`/`COMMAND`/`EXIT`.
97: - All six ids are `corpus/routed-findings.jsonl` rows `R79-V1`…`R79-V6`, gated by
98:   `plans/round80_c2_spotcheck_debt.py`.
```

### V1 clean clone replay

```text
$ S="/fast/scratch/hyaku/kengaku-r80/R80C2RepairsR80"; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/clone" && test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone" && git -C "$S/clone" checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c && git -C "$S/clone" status --porcelain && python3 "$S/clone/plans/round78_c1_class_member_ledger.py" --lane "$S/clone" --rev 148801a6 --work "$S/work"
LANE_TIP 148801a67aebe7bf062932556083131fe96a2d39
WORKTREE clean
UNIVERSE classes=3 members=12 pairs=13
MEMBER filter-js-from-html unexecuted classes=network-service receipt=- verdict=reason:browser-required
MEMBER git-multibranch unexecuted classes=network-service receipt=- verdict=reason:network-install-required
MEMBER headless-terminal unexecuted classes=network-service receipt=- verdict=reason:candidate-library-required
MEMBER hf-model-inference executed classes=network-service receipt=corpus/evidence/round71/hf/receipt.txt verdict=R71-C1 token=predicate
MEMBER install-windows-3.11 unexecuted classes=network-service,process-environment receipt=- verdict=reason:vm-required
MEMBER kv-store-grpc executed classes=network-service receipt=corpus/evidence/round64/kvstore-probe.txt verdict=R64-C1 token=predicate
MEMBER nginx-request-logging executed classes=network-service receipt=corpus/evidence/round70/nginx/receipt.txt verdict=R70-C1 token=predicate
MEMBER pypi-server executed classes=network-service receipt=corpus/evidence/round68/pypi/receipt.txt verdict=R68-C1 token=predicate
MEMBER query-optimize unexecuted classes=db-state receipt=- verdict=reason:external-db-required
MEMBER sqlite-with-gcov executed classes=db-state receipt=corpus/evidence/round65/sqlite-gcov-probe.txt verdict=R65-C1 token=predicate
MEMBER torch-pipeline-parallelism executed classes=process-environment receipt=corpus/evidence/round67/pipe/receipt.txt verdict=R67-C1 token=vectors
MEMBER torch-tensor-parallelism executed classes=process-environment receipt=corpus/evidence/round66/tensor/receipt.txt verdict=R66-C1 token=predicate
CLASS network-service k=4 n=8 census=8 ledger_k=4
CLASS process-environment k=2 n=3 census=3 ledger_k=2
CLASS db-state k=1 n=2 census=2 ledger_k=1
LEDGER rows=12 executed=7 unexecuted=5
COVERAGE recomputed_covered=15 census_covered=12 promoted=network-service,process-environment,db-state recomputed_uncovered=container-image
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
Cloning into '/fast/scratch/hyaku/kengaku-r80/R80C2RepairsR80/clone'...
done.
HEAD is now at 6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows plus the V1 receipt and corrections (R80-C2), S258, lesson, index, wave spec/dispatch

EXIT 0
```

### V1 comparison

```text
$ compare clean replay stdout against committed receipt instrument block
equal=False
--- receipt
+++ clean-clone
@@ -1,5 +1,5 @@
 LANE_TIP 148801a67aebe7bf062932556083131fe96a2d39
-WORKTREE dirty
+WORKTREE clean
 UNIVERSE classes=3 members=12 pairs=13
 MEMBER filter-js-from-html unexecuted classes=network-service receipt=- verdict=reason:browser-required
 MEMBER git-multibranch unexecuted classes=network-service receipt=- verdict=reason:network-install-required
```

### V3 corrected table-only count

```text
$ git show dce7c275:SKILL.md; isolate grader class table; compare stripped third cells exactly
rows=16 bare_executed=0 recipe_unexecuted=0 quantified=16
signal-delivery: executed 1 of 1
subprocess-exec: executed 10 of 45
shell-exec: executed 1 of 6
candidate-import: executed 3 of 6
file-artifact: executed 16 of 76
stdout-inspection: executed 8 of 29
numeric-band: executed 2 of 10
crypto-credential: executed 2 of 12
network-service: executed 4 of 8 (round 64 `kv-store-grpc`; round 68 `pypi-server` replayed offline, R68-C1 pass with the corrected stderr clause — the round-63 receipt of record stays MISS, L0 kengaku round-63 open; round 69 `nginx-request-logging` replayed offline and MISSed R69-C1 on its leg-coverage clause; round 70 re-froze the table with the two missing red witnesses (K6 no HTTP service, K7 mutated 404 body) and the same grader passed R70-C1 — seven frozen vectors, 56/56 legs, `LEG-COVERAGE legs=8 seen_p=8 seen_f=8`, staged-input `case_sha256`, so the member is counted from round 70; the entry `corpus/knowledge/tb2-nginx-request-logging-offline.md`; round 71 `hf-model-inference` replayed offline under an eight-case table (two cases red on the model-load leg, one on the liveness leg) — `PREDICATE R71-C1 pass`, eight frozen vectors, 32/32 legs, `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `mismatches=0`, so the member is counted from round 71; the entry `corpus/knowledge/tb2-hf-model-inference-offline.md`); every member is accounted once in the ledger (R78-C1): ledger=plans/grader-selected-members.json
timing-wall: executed 3 of 9
filesystem-metadata: executed 2 of 10
process-environment: executed 2 of 3 (round 66, R66-C1 `torch-tensor-parallelism`; round 67, R67-C1 `torch-pipeline-parallelism`, receipt of record `corpus/evidence/round67/pipe/receipt.txt`, `PREDICATE R67-C1 pass`): both torch graders replay offline in bwrap against frozen case tables; `install-windows-3.11` stays recipe-unexecuted. The pipeline grader's dictionary-order AFAB check is confirmed at world size 1 only (labrat, round 67); its no-hook leg is a substring match (a runtime-evaded hook passes).; every member is accounted once in the ledger (R78-C1): ledger=plans/grader-selected-members.json
git-plumbing: executed 1 of 3
db-state: executed 1 of 2 (round 65, R65-C1 pass): `sqlite-with-gcov` replayed offline; `query-optimize` stays recipe-unexecuted (a median-ratio timing threshold and a sha-pinned external database make its legs not freezable offline on this host); every member is accounted once in the ledger (R78-C1): ledger=plans/grader-selected-members.json
serialization-schema: executed 1 of 10
container-image: executed 0 of 0
```

### V6 worktree-only r79-c1-after.txt

```text
$ read worktree receipt; git show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:plans/round79_c1_population_ledger.py | sha256; git merge-base --is-ancestor STAMP_TIP 6669fe72e59718acc1a0f32a92849a544b0b2f1c
LANE_TIP 6669fe72e59718acc1a0f32a92849a544b0b2f1c
TOOL plans/round79_c1_population_ledger.py
TOOL_SHA 7705fed172f639b44dd1b8c7d4ac9bb925bd57929798b31366a7aec3fb100c0c
WORKTREE dirty
COMMAND /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round79_c1_population_ledger.py --lane .
MINTED_BY plans/round78_restamp.py sha256=15157a4c3a1283dfbcbe14d56406fe5a5e309070a59070600785d5bad796c16b
EXIT 0
computed TOOL_SHA 7705fed172f639b44dd1b8c7d4ac9bb925bd57929798b31366a7aec3fb100c0c
sha_match=True ancestor_exit=0
EXIT stamp=0 (not independently replayed)
```

### V6 worktree-only r79-c2-after.txt

```text
$ read worktree receipt; git show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:plans/round79_c2_closure_debt.py | sha256; git merge-base --is-ancestor STAMP_TIP 6669fe72e59718acc1a0f32a92849a544b0b2f1c
LANE_TIP 6669fe72e59718acc1a0f32a92849a544b0b2f1c
TOOL plans/round79_c2_closure_debt.py
TOOL_SHA 189d78fc53a23388602c673ce888da3e4860f865372a99c6a3dd590029d8ba1d
WORKTREE dirty
COMMAND /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round79_c2_closure_debt.py --lane .
MINTED_BY plans/round78_restamp.py sha256=15157a4c3a1283dfbcbe14d56406fe5a5e309070a59070600785d5bad796c16b
EXIT 0
computed TOOL_SHA 189d78fc53a23388602c673ce888da3e4860f865372a99c6a3dd590029d8ba1d
sha_match=True ancestor_exit=0
EXIT stamp=0 (not independently replayed)
```

### Tip at end

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
6669fe72e59718acc1a0f32a92849a544b0b2f1c
```

### V6 committed-tip replay

```text
$ S="/fast/scratch/hyaku/kengaku-r80/R80C2RepairsR80"; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && export TMPDIR="$S" && cd "$S" && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round79_c1_population_ledger.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --rev 6669fe72e59718acc1a0f32a92849a544b0b2f1c --work "$S/c1"; r=$?; printf 'C1_EXIT %s\n' "$r"; python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round79_c2_closure_debt.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --rev 6669fe72e59718acc1a0f32a92849a544b0b2f1c --work "$S/c2"; r=$?; printf 'C2_EXIT %s\n' "$r"
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=24 unlocated=0 unexecuted=64
MEMBER adaptive-rejection-sampler unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER bn-fit-modify unexecuted classes=file-artifact evidence=unattempted
MEMBER break-filter-js-from-html unexecuted classes=file-artifact,subprocess-exec evidence=browser-required
MEMBER build-cython-ext unexecuted classes=file-artifact,git-plumbing,numeric-band,subprocess-exec evidence=unattempted
MEMBER build-pmars executed classes=file-artifact,subprocess-exec evidence=corpus/evidence/round38/build-pmars-probe.txt [tb2-header/cases]
MEMBER build-pov-ray unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER caffe-cifar-10 unexecuted classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER cancel-async-tasks executed classes=file-artifact,signal-delivery,stdout-inspection,subprocess-exec,timing-wall evidence=corpus/evidence/round80/cancel-async-tasks-probe.txt [tb2-header/predicate]
MEMBER chess-best-move executed classes=file-artifact evidence=corpus/evidence/round80/chess-best-move-probe.txt [tb2-header/predicate]
MEMBER circuit-fibsqrt executed classes=file-artifact,stdout-inspection,subprocess-exec evidence=corpus/evidence/round42/fibsqrt-probe.txt [tb2-header/cases]
MEMBER cobol-modernization unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER code-from-image unexecuted classes=file-artifact evidence=unattempted
MEMBER compile-compcert unexecuted classes=file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER configure-git-webserver executed classes=stdout-inspection,subprocess-exec evidence=corpus/evidence/round37/git-webserver-probe.txt [tb2-header/cases]
MEMBER constraints-scheduling executed classes=crypto-credential,file-artifact evidence=corpus/evidence/round41/constraints-probe.txt [tb2-header/cases]
MEMBER count-dataset-tokens unexecuted classes=file-artifact evidence=unattempted
MEMBER crack-7z-hash unexecuted classes=file-artifact evidence=unattempted
MEMBER custom-memory-heap-crash unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER db-wal-recovery executed classes=file-artifact,serialization-schema evidence=corpus/evidence/round40/db-wal-probe.txt [tb2-header/cases]
MEMBER distribution-search executed classes=numeric-band evidence=corpus/evidence/round80/distribution-search-probe.txt [tb2-header/predicate]
MEMBER dna-assembly unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER dna-insert unexecuted classes=file-artifact,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER extract-elf unexecuted classes=file-artifact,serialization-schema,subprocess-exec evidence=unattempted
MEMBER extract-moves-from-video unexecuted classes=file-artifact evidence=unattempted
MEMBER feal-differential-cryptanalysis executed classes=candidate-import,shell-exec evidence=corpus/evidence/round43/feal-probe.txt [tb2-header/cases]
MEMBER feal-linear-cryptanalysis executed classes=file-artifact evidence=corpus/evidence/round44/feal-linear-probe.txt [tb2-header/cases]
MEMBER filter-js-from-html unexecuted classes=file-artifact,network-service,subprocess-exec evidence=browser-required
MEMBER financial-document-processor unexecuted classes=crypto-credential,file-artifact evidence=unattempted
MEMBER fix-code-vulnerability unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER fix-git unexecuted classes=crypto-credential,file-artifact evidence=unattempted
MEMBER fix-ocaml-gc unexecuted classes=file-artifact evidence=unattempted
MEMBER gcode-to-text unexecuted classes=file-artifact evidence=unattempted
MEMBER git-leak-recovery executed classes=file-artifact,git-plumbing,stdout-inspection,subprocess-exec evidence=corpus/evidence/round39/git-leak-probe.txt [tb2-header/cases]
MEMBER git-multibranch unexecuted classes=file-artifact,network-service,shell-exec evidence=unattempted
MEMBER gpt2-codegolf unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER headless-terminal unexecuted classes=candidate-import,file-artifact,network-service,subprocess-exec evidence=candidate-library-required
MEMBER hf-model-inference executed classes=filesystem-metadata,network-service evidence=corpus/evidence/round71/hf/receipt.txt [task-under-test/predicate]
MEMBER install-windows-3.11 unexecuted classes=crypto-credential,file-artifact,network-service,process-environment,stdout-inspection,subprocess-exec evidence=vm-required
MEMBER kv-store-grpc executed classes=file-artifact,network-service evidence=corpus/evidence/round64/kvstore-probe.txt [receipt-header/predicate]
MEMBER large-scale-text-editing unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER largest-eigenval executed classes=numeric-band,timing-wall evidence=corpus/evidence/round80/largest-eigenval-probe.txt [tb2-header/predicate]
MEMBER llm-inference-batching-scheduler unexecuted classes=crypto-credential,file-artifact,filesystem-metadata,serialization-schema evidence=unattempted
MEMBER log-summary-date-ranges unexecuted classes=file-artifact evidence=unattempted
MEMBER mailman unexecuted classes=subprocess-exec evidence=unattempted
MEMBER make-doom-for-mips unexecuted classes=file-artifact,subprocess-exec,timing-wall evidence=unattempted
MEMBER make-mips-interpreter unexecuted classes=file-artifact,subprocess-exec,timing-wall evidence=unattempted
MEMBER mcmc-sampling-stan unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER merge-diff-arc-agi-task unexecuted classes=file-artifact,git-plumbing,serialization-schema,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER model-extraction-relu-logits unexecuted classes=candidate-import,file-artifact,shell-exec evidence=candidate-library-required
MEMBER modernize-scientific-stack unexecuted classes=file-artifact,filesystem-metadata,numeric-band,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER mteb-leaderboard unexecuted classes=file-artifact evidence=unattempted
MEMBER mteb-retrieve unexecuted classes=file-artifact evidence=unattempted
MEMBER multi-source-data-merger unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER nginx-request-logging executed classes=file-artifact,network-service,subprocess-exec,timing-wall evidence=corpus/evidence/round70/nginx/receipt.txt [grader-path/predicate]
MEMBER openssl-selfsigned-cert executed classes=crypto-credential,file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=corpus/evidence/round80/openssl-selfsigned-cert-probe.txt [tb2-header/predicate]
MEMBER overfull-hbox unexecuted classes=file-artifact,shell-exec evidence=unattempted
MEMBER password-recovery executed classes=file-artifact evidence=corpus/evidence/round45/probe-run-envelope.txt [tb2-header/cases]
MEMBER path-tracing unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER path-tracing-reverse unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER polyglot-c-py executed classes=stdout-inspection,subprocess-exec evidence=corpus/evidence/round46/polyglot-c-py-probe.txt [tb2-header/cases]
MEMBER polyglot-rust-c unexecuted classes=shell-exec,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER portfolio-optimization unexecuted classes=candidate-import,numeric-band,timing-wall evidence=candidate-library-required
MEMBER protein-assembly executed classes=file-artifact evidence=corpus/evidence/round80/protein-assembly-probe.txt [tb2-header/cases]
MEMBER prove-plus-comm unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER pypi-server executed classes=network-service,stdout-inspection,subprocess-exec evidence=corpus/evidence/round68/pypi/receipt.txt [task-under-test/predicate]
MEMBER pytorch-model-cli unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER pytorch-model-recovery unexecuted classes=file-artifact,filesystem-metadata evidence=unattempted
MEMBER qemu-alpine-ssh unexecuted classes=stdout-inspection,subprocess-exec evidence=unattempted
MEMBER qemu-startup unexecuted classes=file-artifact,shell-exec evidence=unattempted
MEMBER query-optimize unexecuted classes=crypto-credential,db-state,file-artifact,timing-wall evidence=external-db-required
MEMBER raman-fitting unexecuted classes=file-artifact,numeric-band,serialization-schema evidence=unattempted
MEMBER regex-chess unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER regex-log executed classes=file-artifact evidence=corpus/evidence/round36/regex-log-probe.txt [capture-tree/cases]
MEMBER reshard-c4-data unexecuted classes=crypto-credential,file-artifact,filesystem-metadata,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER rstan-to-pystan unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER sam-cell-seg unexecuted classes=file-artifact,serialization-schema,subprocess-exec evidence=unattempted
MEMBER schemelike-metacircular-eval unexecuted classes=file-artifact,stdout-inspection,subprocess-exec,timing-wall evidence=unattempted
MEMBER sparql-university unexecuted classes=file-artifact evidence=unattempted
MEMBER sqlite-db-truncate unexecuted classes=file-artifact,serialization-schema evidence=unattempted
MEMBER sqlite-with-gcov executed classes=db-state,stdout-inspection,subprocess-exec evidence=corpus/evidence/round65/sqlite-gcov-probe.txt [receipt-header/predicate]
MEMBER torch-pipeline-parallelism executed classes=candidate-import,file-artifact,process-environment evidence=corpus/evidence/round67/pipe/receipt.txt [receipt-header/vectors]
MEMBER torch-tensor-parallelism executed classes=candidate-import,file-artifact,process-environment evidence=corpus/evidence/round66/tensor/receipt.txt [grader-path/predicate]
MEMBER train-fasttext unexecuted classes=file-artifact,filesystem-metadata evidence=unattempted
MEMBER tune-mjcf unexecuted classes=file-artifact,filesystem-metadata,numeric-band,timing-wall evidence=unattempted
MEMBER video-processing unexecuted classes=file-artifact,subprocess-exec evidence=unattempted
MEMBER vulnerable-secret unexecuted classes=file-artifact evidence=unattempted
MEMBER winning-avg-corewars unexecuted classes=crypto-credential,file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
MEMBER write-compressor unexecuted classes=file-artifact,stdout-inspection,subprocess-exec evidence=unattempted
CLASS signal-delivery k=1 n=1 cell=executed 1 of 1
CLASS subprocess-exec k=10 n=45 cell=executed 10 of 45
CLASS shell-exec k=1 n=6 cell=executed 1 of 6
CLASS candidate-import k=3 n=6 cell=executed 3 of 6
CLASS file-artifact k=16 n=76 cell=executed 16 of 76
CLASS stdout-inspection k=8 n=29 cell=executed 8 of 29
CLASS numeric-band k=2 n=10 cell=executed 2 of 10
CLASS crypto-credential k=2 n=12 cell=executed 2 of 12
CLASS network-service k=4 n=8 cell=executed 4 of 8 (round 64 `kv-store-grpc`; round 68 `pypi-server` replayed offli
CLASS timing-wall k=3 n=9 cell=executed 3 of 9
CLASS filesystem-metadata k=2 n=10 cell=executed 2 of 10
CLASS process-environment k=2 n=3 cell=executed 2 of 3 (round 66, R66-C1 `torch-tensor-parallelism`; round 67, R67-C1 `
CLASS git-plumbing k=1 n=3 cell=executed 1 of 3
CLASS db-state k=1 n=2 cell=executed 1 of 2 (round 65, R65-C1 pass): `sqlite-with-gcov` replayed offline; `q
CLASS serialization-schema k=1 n=10 cell=executed 1 of 10
CLASS container-image k=0 n=0 cell=executed 0 of 0
COVERAGE replayed=24 covered=15 covered_located=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=24 unlocated=0 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
C1_EXIT 0
UNIVERSE spotcheck=corpus/lessons/round-78-verifier-spotcheck.md ids=7 R78-D1,R78-D2,R78-D3,R78-D4,R78-D5,R78-D6,R78-D7
DEBT R78-D1 status=closed close=SCORECARD.md round-79 section (R78-D1 correction: the receipt's own per-class split) check=present
DEBT R78-D2 status=closed close=SCORECARD.md lines 3564-3565 (both round-77 rows now read stamped `cd2e25bb`, clean) check=present
DEBT R78-D3 status=closed close=LOG.md round-79 section (at-tip rerun block quotes the receipt landed at this round's tip) check=present
DEBT R78-D4 status=closed close=corpus/lessons/round-79.md ## Corrections (S254 quote length and S255 anchor re-stated) check=present
DEBT R78-D5 status=closed close=SCORECARD.md round-79 section (R78-D5 correction naming R75-C1/R76-C2 as the red gates) check=present
DEBT R78-D6 status=closed close=LOG.md round-79 block (clean-tree gate block re-run; receipt corpus/evidence/round79/gates-clean.txt lands with it) check=present
DEBT R78-D7 status=closed close=corpus/README.md lessons index (spot-check row) and this ledger's R78-D1..D7 rows check=present
DEBT-TOTAL ids=7 registered=7 closed=7 checks_passed=7
INDEX corpus/lessons/round-78-verifier-spotcheck.md indexed=yes
DEFECTS n=0
TARGET ids=7 closed=7 checks_passed=7 indexed=yes
PREDICATE R79-C2 pass
C2_EXIT 0

SHELL_EXIT 0
```

### V5 committed scopes

```text
$ git show TIP:corpus/SOURCES.md; select S180 and S256 rows
| S180 | Terminal-Bench 2.0 root README at the pin — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md | docs | A | the maintainers' own statement of how Terminal-Bench 2.0 tasks were validated before release | README.md at the pin, FAQ answer to "Why did you make a new version of the benchmark?" (line 87); git blob a46b155b419a15add0aab7fe8e51f0f64a9404d8, 4574 bytes; sha256 7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364; fetched 2026-10-28 | the maintainers say each TB2.0 task got several hours of human and LM-assisted validation for solvable, realistic and well-specified; the README gives no grader-level check, so that claim is what a per-test grader audit can test | mined | 2026-10-28 | 180d | corpus/knowledge/tb2-grader-vacuity-triage.md |
| S256 | Terminal-Bench 2.0 harness README (pinned tree 2fd12b88) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md | docs | A | the harness's execution model: a TB2 run is a containerized run, so a grader's `test.sh` installs and starts services inside a container and an in-process offline replay is a different execution surface — the premise of the R79 blocker taxonomy | capture corpus/evidence/round79/sources/tb2-readme.md:24; sha256 7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364; 4574 bytes, HTTP 200 | “Terminal-Bench is a popular benchmark for measuring the capabilities of agents and language models to perform valuable work in containerized environments.” | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md, plans/round-79-claims.md |
```

### V3 historical disambiguation

```text
$ git show 148801a6:SKILL.md; isolate grader class table; compare stripped third cells exactly
rows=16 bare_executed=12 recipe_unexecuted=1 quantified=3
```

## Risks, limits, cleanup

No build, formatter, linter, battery, or unrelated gate was run. Only explicitly assigned instrument replays and the source validator were exercised. V6 replays used `--rev TIP` to read committed bytes, with `--work` and `TMPDIR` confined to exclusive scratch; no second clone was made. Scratch was removed by the EXIT trap after each scratch-owning shell. No external remediation, commit, or source edit occurred. Remaining blockers to a committed-byte closure are V6 integration and V3 revision attribution; the parent owns final integrated gates.

Self-evaluation: accuracy 4/5 (preliminary parsing diagnostics are retained and corrected, not silently discarded); completeness 4/5 (committed V6 receipts were absent, clearly separated from worktree candidates); clarity 4/5 (full raw evidence is lengthy); actionability 5/5 (specific L1 corrections above); conciseness 4/5 (raw evidence retained to meet evidence contract). Overall 4.2/5. Improvement applied: explicitly distinguish measured historical table, base table, committed artifacts, and worktree candidates. Would the user agree: likely, because no missing committed evidence is represented as a pass.
