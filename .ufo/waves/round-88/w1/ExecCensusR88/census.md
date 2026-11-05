# ExecCensusR88 — registry census before/after + ledger arithmetic

Seat: `ExecCensusR88`, round 88 wave 1. Read-only on the lane; all extraction under
`/fast/scratch/hyaku/kengaku-r88/ExecCensusR88/` (deleted before yield; only this report retained).

Revisions:

- BASE `801b903af6412cb424209a60b3a52e56c3532866` (round-87 spot-check tip, `master`)
- TIP  `7fcc680b86599eedd63e862a061848298428b3cc` (lane tip for the tip measurement)

## 1. sources-census validate

Extraction (one `git archive | tar -x` per revision into scratch):

```sh
S=/fast/scratch/hyaku/kengaku-r88/ExecCensusR88
mkdir -p "$S/base" "$S/tip"
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 801b903af6412cb424209a60b3a52e56c3532866 corpus | tar -x -C "$S/base"
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 7fcc680b86599eedd63e862a061848298428b3cc corpus | tar -x -C "$S/tip"
```

Files produced: `$S/base/corpus/SOURCES.md`, `$S/tip/corpus/SOURCES.md`.

### 1a. `validate --file` BEFORE (BASE)

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/base/corpus/SOURCES.md"
```

Output (44 lines; abbreviated here, full text retained in scratch run):

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	W04	S213 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py across scopes
file	W04	S214 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py across scopes
file	W04	S215 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh across scopes
file	W04	S216 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md across scopes
file	W04	S217 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/gen.py across scopes
file	W04	S222 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/instruction.md across scopes
file	W04	S227 duplicate url encoding.spec.whatwg.org/index-windows-1252.txt across scopes
file	W04	S234 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
file	W04	S237 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
file	W04	S243 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py across scopes
file	W04	S256 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md across scopes
file	W04	S266 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md across scopes
file	W04	S268 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/tests/test.sh across scopes
file	W04	S269 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test.sh across scopes
file	W04	S270 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pyproject.toml across scopes
file	E11	S218 missing used-by plans/round-59-claims.md
file	E11	S220 missing used-by plans/round-59-claims.md
file	E11	S221 missing used-by plans/round-59-claims.md
file	E11	S223 missing used-by plans/round-60-claims.md
file	E11	S224 missing used-by plans/round-61-claims.md
file	E11	S225 missing used-by plans/round-61-claims.md
file	E11	S226 missing used-by plans/round-62-claims.md
file	E11	S227 missing used-by plans/round-62-claims.md
file	E11	S251 missing used-by plans/round-75-claims.md
file	E11	S252 missing used-by plans/round-76-claims.md
file	E11	S253 missing used-by plans/round-77-claims.md
file	E11	S254 missing used-by plans/round-78-claims.md
file	E11	S255 missing used-by plans/round-78-claims.md
file	E11	S256 missing used-by plans/round-79-claims.md
file	E11	S257 missing used-by plans/round-79-claims.md
file	E11	S258 missing used-by SCORECARD.md
```

- rc = **1** (E11 findings: 16 `missing used-by` — all referenced `plans/round-NN-claims.md`
  paths and `SCORECARD.md` are absent relative to the scratch dir, because `--file` mode
  resolves used-by paths against cwd/scratch, not the lane root; the W04 count is 28).
- W04 line count (BASE) = **28**.
- Note: this rc=1 is a `--file`-mode artifact of path resolution, not a registry defect —
  the round-end form below validates the live tree and returns rc=0.

### 1b. `validate --file` AFTER (TIP)

Same command with `--file "$S/tip/corpus/SOURCES.md"`. Output is **byte-identical to 1a**:
same 28 W04 lines, same 16 E11 lines, no new codes, no S277-related finding.

- rc = **1**, W04 line count (TIP) = **28** (identical set; `diff` of the two outputs: empty).

### 1c. `validate --root` round-end form (live tree)

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

Output: 28 W04 lines for `kengaku` (same URLs as 1a/1b), then:

```
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

- rc = **0** — satisfies the "exit 0 required at round end" condition.
- E11 does not appear in `--root` mode because used-by paths resolve against the lane root.

## 2. Frozen awk census commands (CORPUS.md "Census — run from the lane root")

Commands copied verbatim from `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 135–145;
`corpus/SOURCES.md` replaced by the extracted file path. Run once per revision.

### BASE `801b903a` → `$S/base/corpus/SOURCES.md`

| metric | command | output | expected |
|---|---|---|---|
| row count | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `268` | 268 ✓ |
| malformed (NF!=13) | `awk -F'|' '...NF!=13 {n++} END{print n+0}'` | `0` | 0 ✓ |
| tier histogram | `awk -F'|' '...n[t]++...'` | `A=238 B=24 C=6` | A=238 ✓ |
| status histogram | `awk -F'|' '...n[s]++...'` | `mined=243 queued=8 rejected=17` | mined 243, rejected 17, queued 8 ✓ |
| duplicate ids | `awk ... print i \| sort \| uniq -d` | *(empty)* | empty ✓ |
| enum/tier-inflation | `awk ... NF==13 ...` | *(empty)* | empty ✓ |

Supplementary frozen command #7 (mined used-by existence), paths resolved against the lane root:
no output for either revision.

### TIP `7fcc680b` → `$S/tip/corpus/SOURCES.md`

| metric | output | expected |
|---|---|---|
| row count | `269` | 269 ✓ |
| malformed (NF!=13) | `0` | 0 ✓ |
| tier histogram | `A=239 B=24 C=6` | A=239 ✓ |
| status histogram | `mined=244 queued=8 rejected=17` | mined 244, rejected 17, queued 8 ✓ |
| duplicate ids | *(empty)* | empty ✓ |
| enum/tier-inflation | *(empty)* | empty ✓ |

`diff` between the two extracted SOURCES.md files: exactly one added line — row `S277`
(the round-88 `fix-git` grader row, tier A, status `mined`). All other registry content identical.

## 3. Ledger arithmetic — `plans/grader-population-ledger.json`

Extraction:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 801b903af6412cb424209a60b3a52e56c3532866:plans/grader-population-ledger.json > "$S/led-base.json"
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 7fcc680b86599eedd63e862a061848298428b3cc:plans/grader-population-ledger.json > "$S/led-tip.json"
```

Plain-Python computation (`json.load`, members dict, `status=="executed"` counted per class):

| measure | BASE 801b903a | TIP 7fcc680b | expected |
|---|---|---|---|
| member rows | 88 | 88 | — |
| executed rows | **31** | **32** | 31 → 32 ✓ |
| crypto-credential | **2/12** | **3/12** | 2 → 3 of 12 ✓ |
| file-artifact | **23/76** | **24/76** | 23 → 24 of 76 ✓ |

Full per-class executed/total (identical across revisions except the two moved classes):

```
candidate-import:      3/6    db-state:            1/2    numeric-band:        3/10
crypto-credential:     2/12 → 3/12                process-environment:  2/3
file-artifact:         23/76 → 24/76              serialization-schema: 3/10
filesystem-metadata:   2/10   shell-exec:          1/6    signal-delivery:     1/1
network-service:       4/8    stdout-inspection:   8/29   subprocess-exec:     10/45
git-plumbing:          1/3    timing-wall:         3/9
```

`fix-git` member row diff: BASE `status=unexecuted, reason=unattempted` → TIP
`status=executed, round=88, verdict=cases, receipt=corpus/evidence/round88/fix-git-probe.txt`.

## Findings

None. All measured values match the frozen expectations in the assignment and claims file.
The only non-zero `validate --file` rc (1) is the documented `--file`-mode E11
path-resolution artifact on the extracted tree; the `--root` round-end form returns rc=0
as required. Frozen elements inspected (claims file, awk commands, census contract) showed
no defect requiring report.
