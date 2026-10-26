# F41RevBatCtl — non-author honesty review of `plans/battery41/r_ctl.py` (T06, T08)

Seat: F41RevBatCtl, kengaku round 41 wave 2 (falsify), 2026-10-26.
Target: `plans/battery41/r_ctl.py` (4 fixtures; claims kills of T06, T08 of `plans/round41_c1_verify.py`).
Reviewed content sha256 `2fcbbcb7eb001780…` (full: `2fcbbcb7eb0017803b41ffb2c41a0fc5a3fd97854eda0afb3948bc44fa4aaaed`), byte-identical at landing `74513c06`, stated tip `3d0058fb`, and clone HEAD `d7c7789` (`git show <ref>:plans/battery41/r_ctl.py | sha256sum`, run three times). Counter digest `8835a94b…` and tool pins `e4f49714…`/`38492bf1…` match `.ufo/waves/round-41/claims/frozen-digests.txt` and the counter's `PINS total=2 mismatched=0`. Clone HEAD is `d7c7789` (wave-2 dispatch commit), not the goal's stated tip `3d0058f`; all reviewed files are identical across all three refs, so the review applies to the landed content.

Method: full line-by-line read of `r_ctl.py` (90 lines, including both `STUB`-generated probe-stub strings), of the counter's mutant table/runner/kill logic, and of `plans/tip_receipts.py`; isolated attribution run of the counter; direct reproduction of every fixture under the counter's tool-run conditions with instrumented reference/mutant copies of the tool. All commands ran inside the mandated envelope `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …`; scratch only under `/fast/scratch/hyaku/kengaku-r41/F41RevBatCtl/`. No tool installs. No writes outside scratch and this report dir (nothing to timestamp).

## 1. Static review — counterexample-vector scan (per fixture)

The module has **zero imports** and **zero file reads** of its own; a fixture build only calls `ctx.init/ctx.write/ctx.git` (git init + commit inside the fixture dir, author/dates pinned by the counter's `Ctx.ENV`), writes the stub probe scripts, and returns an argv tail of `--lane <abs inside d> --work {WORK}` (+ `--tamper <rel receipt id>` on fixture 2). `grep -nE "witness|claims|\.ufo|/home|/tmp|import|open\(|read_text|environ|proc|socket"` over the module matches only its own docstring line "No witness module is read, copied or imported." and the stub's `import sys`.

Both generated probe stubs are, in full: docstring, `import sys`, `sys.stdout.write(<literal>)`, `sys.exit(<literal>)` — unconditional, no branching on anything (a fortiori only on their own committed bytes).

| fixture | advertised behaviour | vectors checked (counter scratch/`variants/`/slot; /proc; `../` argv; sockets; IPC; tool/counter text; branching stub) | verdict |
|---|---|---|---|
| r_ctl-t06-empty-equal-receipt | empty committed receipt reproduced byte-for-byte → `equal`; byte-flip control has no bytes → `control:unavailable`; exit 1 | none present; lane built from nothing inside fixture dir; stub unconditional; argv paths inside d + `{WORK}` | honest |
| r_ctl-t06-tamper-on-skipped | same failed-control branch via `--tamper` on a receipt skipped for `dependency-missing:uv` → `control:unavailable`, exit 1 | none present; `--tamper` id is a mapped rel path inside the lane; no reads | honest |
| r_ctl-t08-derived-uv-absent | derived receipt whose `Run as:` starts `uv run`, uv absent from the counter's fixed PATH → `skip:<rel>:dependency-missing`; table receipt equal; control `differ`; exit 0 | none present; PATH absence of `uv` is the counter's own fixed-PATH contract, reproduced (`which uv=None` under the same env) | honest |
| r_ctl-t08-table-uv-absent | same dependency branch with RECEIPTS-table-mapped receipts (build-pmars needs uv; regex-log uses python3); exit 0 | none present; both receipts table-mapped by the tool's own `RECEIPTS` dict | honest |

Kill quality: T06's only behavioural delta is `and`→`or` on `control_ok` in the final return; the killing fixtures have `d=0` (clean receipts) with `control_ok=False`, exactly the documented T06 scenario ("an unavailable control on an empty receipt is a failed control", tip_receipts.py:29-30). T08's mutated `elif shutil.which(argv[0]) is None:` is the dependency check the fixtures exercise directly (advertised at tip_receipts.py:19-21). Neither kill flows through a path the mutation does not own — not incidental. The "second trigger" pairs are genuine input-space breadth (empty-blob auto-control vs skipped-receipt `--tamper`; derived mapping vs table mapping), not duplicates.

## 2. Attribution — each mutant dies by THIS module

Scratch `$S=/fast/scratch/hyaku/kengaku-r41/F41RevBatCtl`; `git clone -q --shared` of the lane, toplevel verified `$S/lane`; battery dir `$S/bat-rctl/` held **only** `r_ctl.py`.

```
bwrap … python3 $S/lane/plans/round41_c1_verify.py --lane "$S/lane" \
  --battery-dir "$S/bat-rctl" --only T06,T08 --work "$S/w" --jobs 4
```

Output (receipt `receipts-out/attr.txt`; full module copy compiled fresh by the counter's `build_battery`):

```
PINS total=2 mismatched=0
FIXTURE r_ctl-t06-empty-equal-receipt … observed_rc=1 observed=control:unavailable,equal:corpus/evidence/round41/r-ctl-probe.txt ok
FIXTURE r_ctl-t06-tamper-on-skipped … observed_rc=1 observed=control:unavailable,skip:…r-ctl-probe.txt:dependency-missing ok
FIXTURE r_ctl-t08-derived-uv-absent … observed_rc=0 observed=control:differ,equal:…tb2-grader-probe.txt,skip:…r-ctl-probe.txt:dependency-missing ok
FIXTURE r_ctl-t08-table-uv-absent … observed_rc=0 observed=control:differ,equal:…regex-log-probe.txt,skip:…build-pmars-probe.txt:dependency-missing ok
MUTANT T06 receipts rc-silence killed by=r_ctl-t06-empty-equal-receipt
MUTANT T08 receipts rc-mirror killed by=r_ctl-t08-derived-uv-absent
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
```

With the battery dir containing only this module, both kills are attributable to it alone; the landing measurement names the same fids (`.ufo/waves/round-41/integrate/measure-final.txt:58,60`: `killed by=r_ctl-t06-empty-equal-receipt`, `killed by=r_ctl-t08-derived-uv-absent`). The counter's own reference-vs-declaration check (`wrong=0`) confirms every fixture's reference output equals its advertised class set and exit — the fixtures do what their comments claim, on the tool's real stdout classes.

## 3. Mutated-line-executed proof

Fixtures rebuilt via the counter's own child entry (`--build-module … --dest $S/fx` → f000…f003 mapped as above). Variants generated by `gen_variants.py` (receipt in this dir): pure mutants built with the exact `MUTANTS` old/new strings; traced copies add stderr-only prints with unchanged control flow (pure and traced rc agree on all 28 runs). Each run used the fixture's own argv tail (including f001's `--tamper …`) with `{WORK}` substituted per run, env identical to the counter's `Runner.env` (fixed system PATH, `HOME` empty, `GIT_CONFIG_*` neutralised), cwd = fixture dir, inside the envelope. Driver: `run_matrix.py`; log `receipts-out/matrix.log`.

Exit matrix (rc reference / T06-pure / T08-pure):

| fixture | ref | t06_pure | t08_pure |
|---|---|---|---|
| f000 empty-equal | 1 | **0** | 1 |
| f001 tamper-on-skipped | 1 | **0** | 1 |
| f002 derived-uv | 0 | 0 | **1** |
| f003 table-uv | 0 | 0 | **1** |

Traces (stderr, verbatim from `receipts-out/*.err`):

```
f000-t06_ref_trace  | TRACE T06 ref final-return reached d=0 control_ok=False   (rc=1)
f000-t06_mut_trace  | TRACE T06 MUTATED line reached d=0 control_ok=False     (rc=0)
f001-t06_mut_trace  | TRACE T06 MUTATED line reached d=0 control_ok=False     (rc=0)
f002-t08_ref_trace  | TRACE T08 ref line evaluated argv0='uv' dependency_missing=True  (rc=0, skip)
f002-t08_mut_trace  | TRACE T08 MUTATED line evaluated argv0='uv' (branch constant False) (rc=1)
f003-t08_mut_trace  | TRACE T08 MUTATED line evaluated argv0='uv' (branch constant False) (rc=1)
```

So: T06's mutated line (main's final return) executes on both killing fixtures, and the flip is exactly `control_ok=False` + `and`→`or`. T08's mutated `elif` is evaluated with `argv0='uv'` on both killing fixtures; under the mutant it falls through, the tool runs the probe and reports `differ probe exit=missing (uv: not found)` (f002-t08_pure.out) → exit 1 vs reference 0. Mechanism receipts: f000-ref.out shows `equal bytes=0` + `control … verdict=unavailable`; f001-ref.out shows `skip reason=dependency-missing:uv` + `control … verdict=unavailable`; f003-ref.out/f003-t08_pure.out show the same skip→differ flip in the table layout. **Mutated-line-executed 2/2.**

## 4. Independence from the witness modules

`claims/witness/` holds `w_receipts.py`/`w_sources.py` with `w-t06-empty-receipt-control`, `w-t08-uv-absent`, etc. The battery module never names, imports, copies or reads them (grep above; module has no imports at all). Physically: the counter builds every module in a sandbox that hides the whole lane (`--tmpfs <lane>`; round41_c1_verify.py `build_battery` → `ro_sandbox(..., hide=(lane,))`), so witness bytes under `.ufo/…` are unreachable at build time, and tool runs see only the fixture dir read-only plus per-run work/tmp. The fixtures rebuild their lanes from nothing; their fixture ids, receipt paths and stub outputs are disjoint from the witness set. Coverage overlaps the witness (both cover the empty-receipt and uv-absent scenarios) — that is redundancy, not dependence; kills were reproduced with no witness present.

## Verdicts per fixture

- r_ctl-t06-empty-equal-receipt — **honest** (kills T06; mutated line executes; evidence §2–3).
- r_ctl-t06-tamper-on-skipped — **honest** (second trigger of the same branch, distinct code path into `control:unavailable`).
- r_ctl-t08-derived-uv-absent — **honest** (kills T08; mutated line executes with `argv0='uv'`).
- r_ctl-t08-table-uv-absent — **honest** (second trigger, table registry layout).

## Residual risk and verification gaps

- `uv`-absence is guaranteed by the counter's fixed PATH constant, not by the host: on a host where `uv` sat in `/usr/local/bin`, fixtures f001–f003's references would change (no skip → different class sets → `wrong`). Within this counter's pinned environment the fixtures are sound; the risk is environmental, not dishonesty.
- T06/T08 kills here are shown for this module in isolation with `--only`; the 48-fixture battery-level predicate (`PREDICATE C1 pass`) is the landing receipt's claim, not re-run in full by this seat (out of scope).
- The counter's kill rule credits the first exhibiting fixture, so f001 (T06) and f003 (T08) are direction-exhibiting second triggers confirmed by my matrix, not by the counter's `killed by=` line.
- My first harness attempt omitted f001's `--tamper` argv tail and mis-signed the pure-mutant loop; both were discarded and redone from the counter's own BUILT JSON (`receipts-out/` keeps only the corrected runs; the buggy `run_case.sh` output was overwritten by the matrix driver).

Receipts: `receipts-out/attr.txt` (isolated attribution), `receipts-out/matrix.log` (28-run matrix + traces), `receipts-out/*.out|*.err` (per-run stdout/stderr), `receipts-out/built.raw` (counter-built fixture mapping), `gen_variants.py`, `run_matrix.py`, `run_case.sh` (harness).

VERDICT: battery41-r_ctl-honest-4/4-mutated-line-executed-2/2
