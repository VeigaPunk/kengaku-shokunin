# FxMutF2 — F2 CRLF applicability mutant survives
Seat: KengakuR26-2.FxMutF2; 2026-10-21; advisory mutation probe, not admission or outside verification.
Revision: integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; live target matched copied bytes before and after.
Axes: C1 novelty→coverage/constructs; detector sensitivity, frozen-population integrity, and exact restoration.
Read: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-26-claims.md` including POST-OUTPUT Amendment 1 and Amendment 2; `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-26.md`; draft `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/drafts/grader-perturbation-audit.md`.
Scope: one F2 source mutation in an isolated /tmp copy only; no live source, Git/jj, model, endpoint, or host changes. Tools installed/updated: none.
Scratch root R=`/tmp/kengaku-r26-FxMutF2-uI1WWl`; target P=`/tmp/kengaku-r26-FxMutF2-uI1WWl/plans/grader_perturb.py`.

## Mutant and expected detector
At P:414 remove only `\r?` from the F2 opener applicability regex: `r"```json[ \t]*\r?\n"` → `r"```json[ \t]*\n"`.
This plausible LF-only regression makes a valid CRLF answer fence inapplicable (`None`) instead of relabeling it.
Expected: `--selftest` rejects broken F2 applicability with exit 1. Observed: it accepts the mutant with exit 0.
Missing behavior: positive F2 applicability on CRLF; the F2 selftest fixture at live `plans/grader_perturb.py:598-601` uses LF only. F7's separate CRLF test does not exercise F2 on CRLF.

## Exact commands and observed outputs
Executed collector commands: `python3 -B /tmp/kengaku-r26-FxMutF2-uI1WWl/probe.py pristine`, then the same command with `mutated`, then `restored`; each collector exit 0.
Each collector ran these five bounded child commands concurrently (R/P expand to the absolute paths above):
```sh
/usr/bin/python3 -B "$P" --root "$R" --selftest
/usr/bin/python3 -B "$P" --root "$R" --summary
/usr/bin/python3 -B "$P" --root "$R/pin_guard" --summary
/usr/bin/python3 -B "$P" --root "$R/baseline_guard" --summary
/usr/bin/python3 -B /tmp/kengaku-r26-FxMutF2-uI1WWl/f2_crlf_assert.py
```
| Child | Pristine exit | Mutated exit | Restored exit | Output (identical across stages unless noted) |
|---|---:|---:|---:|---|
| selftest | 0 | 0 | 0 | `SELFTEST F2 PASS`; `SELFTEST MUTATION-CATCH PASS caught=12`; `SELFTEST TOTAL families=10 failed=0` |
| summary | 0 | 0 | 0 | F2 n=1819 k=1802; `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9` |
| pin_guard summary | 1 | 1 | 1 | r8 SHA mismatch; population=1964 excluded=0 |
| baseline_guard summary | 1 | 1 | 1 | `ERROR corpus/evidence/round8-horizon/results.jsonl:11 cell='A-INC' pid=1 turn=1: baseline re-grade True != stored ok False`; population=1963 excluded=1 |
| CRLF assertion | 0 | 1 | 0 | Pristine/restored: `CRLF_ASSERT PASS`; mutant: `CRLF_TRANSFORM=None`, `AssertionError: F2 must relabel a valid CRLF answer fence` |
Pin control: isolated r8 copy plus exactly one trailing LF; observed hash `fd7f325d8c0e47972a594569bd2d3e1c3d4c281334e5bfdec5864850125e406b`.
Baseline control: isolated r8 first `ok` value, byte offset 10315, `true`→`false`; hash `153b315e1b718b2f5213973f2f48c4b8efa87356818d765da96b4839ae66fe4a`. It also trips the pin; baseline diagnostic was independently observed, not inferred from exit alone.
All three stages' selftest stdout SHA256: `725bdaeb9973f422e2ad8d466bf3beb85d4f406fc3b553a99a83f66ef5b8f8d1`.
All three stages' normal-summary stdout SHA256: `e2f7af6a210fb2bed84285e9c55288d4ed1e3dba898ca3e4a8a14bec068a3275`.
All three stages' pin-control / baseline-control stdout SHA256 respectively: `f012d23379527be23f29b7943066dde431149c5c5ae9db9feccfadf973510636` / `1dcad803461245f32e1de8c4d5d138dd2d54b57c564797bf09ab6b8118144c5e`.
Full exact commands/stdout/stderr/exits/input hashes retained in `/tmp/kengaku-r26-FxMutF2-uI1WWl/pristine.json`, `/tmp/kengaku-r26-FxMutF2-uI1WWl/mutated.json`, `/tmp/kengaku-r26-FxMutF2-uI1WWl/restored.json` (disposable supplemental exports; durable findings reproduced above).

## Minimal failing assertion
With the instrument imported as `m` (no grader configuration needed for this transform):
```python
raw = '```json\r\n{"x": 1}\r\n```'
rec = m.Rec('selftest', 1, 'A-INC', 1, 1, 'state', raw, {'x': 1}, True)
assert m.apply_family('F2', raw, {'x': 1}, rec) == raw.replace('```json', '```JSON', 1)
```
This exact assertion passed pristine/restored and failed mutated. No production test fix was made; finite-corpus counts themselves remain unchanged.

## Restoration evidence
Pristine target SHA256: `8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b`.
Mutated target SHA256: `5ced8996a97c500c9b5acc17e5b4dbb221f4c0d5cfe55f72f913ca801b6cb1a1`.
Restored target SHA256: `8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b`.
Executed `cp /tmp/kengaku-r26-FxMutF2-uI1WWl/grader_perturb.py.pristine /tmp/kengaku-r26-FxMutF2-uI1WWl/plans/grader_perturb.py`; exit 0.
Executed `cmp /tmp/kengaku-r26-FxMutF2-uI1WWl/grader_perturb.py.pristine /tmp/kengaku-r26-FxMutF2-uI1WWl/plans/grader_perturb.py`; no output, exit 0.
Final `sha256sum` on live target, scratch target, and saved pristine all returned the pristine hash above; exit 0. Same bounded detector reran after restoration.
VERDICT: SURVIVED — F2 CRLF-applicability regression escapes --selftest; pin/baseline guards unchanged under exercised controls; scratch bytes exactly restored.
