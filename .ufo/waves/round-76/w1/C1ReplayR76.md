# C1ReplayR76 — independent surface replay

Axes: coverage (all first anchors), calibration (frozen before/control receipts), speed (independent legs), honesty (observed return codes). Production files unchanged; retained artifacts are under `.ufo/waves/round-76/w1/C1ReplayR76/`.

## Findings

1. **INFO — before and do-nothing reproduced exactly.** `before.txt`: current gate with `--rev fda63968` resolves live host state against untouched base PROVINCE bytes. It returns 1, total 11, present 4, absent 7, agree 9, disagree 2. Thus leaving PROVINCE untouched today does **not** reach the target. Defects are precisely STALE-TEXT row 2 and UNDECLARED-ABSENT row 4.
2. **INFO — independent parser agrees on all 11 live verdicts.** `independent.txt` takes the first literal backtick span in each path cell without importing gate parsing/resolution helpers; calls actual `test -e` subprocesses, recursively expands braces, and uses curl for endpoints. Rows 1–7 absent; rows 8–11 present. No gate-verdict differences. Both expanded catalog files fail `test -e` independently. Both required health endpoints return HTTP `000`, curl rc 7.
3. **MEDIUM — unflagged present-tense prose remains on absent row 3.** Base PROVINCE line 14, retained verbatim at `base-province.txt:15`, says `identity re-probed via /v1/models + /health 200 each round` (the paths are backticked in the original) and the next cell says `identity re-probed each round`. Actual :34113/health returns 000. Gate emits row 3 absent but no STALE-TEXT defect. Its fixed STALE_TEXT vocabulary lacks these phrases and its test examines only `cells[1]`, not the next cell (`round76_c1_surface_resolver.py:65-72,205`). Dated ABSENT notes exist, but do not remove the contradictory recurring present-tense assertion. This is the named declared-text/live disagreement not flagged; no extra live-verdict mismatch is alleged. Routed to KengakuR76; no production repair here.
4. **MEDIUM — control receipt was not replayable after PROVINCE repair with the inspected implementation.** `control-worktree.txt`: actual `--control-declared` returns 1, `disagreements=0 target_reached=True`, predicate fail. Inspected function at lines 380–381 bound its input to module-relative PROVINCE, ignoring `--lane` and `--rev`. The before-state control is discriminating, however: `control-base-preserved-paths.txt` invokes the unchanged function on base PROVINCE with all four present relative anchors linked to live lane paths and gets exactly `disagreements=1 target_reached=False`, predicate pass, rc 0. Parent acknowledged the defect and reported implementing explicit lane/revision input and a PROVINCE_REV stamp; that subsequent production edit is **not verified by this seat**.
5. **INFO — repaired worktree replay is green under the inspected gate.** `worktree.txt`: total 11 / present 4 / absent 7, agree 11 / disagree 0, no DEFECT, predicate pass, rc 0. This is numeric target evidence only; finding 3 is a residual prose limitation.

## Exact commands and retained evidence

Working directory for the driver and every command it launches: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

Executed driver (rc 0):

```sh
python3 .ufo/waves/round-76/w1/C1ReplayR76/replay.py
```

The retained `replay.py` is the exact independently written driver. Its subprocess commands and return codes:

```sh
git show fda63968:PROVINCE.md                                      # rc 0; base-province.txt
python3 plans/round76_c1_surface_resolver.py --lane . --rev fda63968 # rc 1; before.txt
python3 plans/round76_c1_surface_resolver.py --lane .                # rc 0; worktree.txt
curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113     # 000; rc 7
curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:45669     # 000; rc 7
curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health # 000; rc 7; health-34113.txt
curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:45669/health # 000; rc 7; health-45669.txt
python3 plans/round76_c1_surface_resolver.py --lane . --control-declared --work /fast/scratch/hyaku/kengaku-r76/C1ReplayR76/current-control # rc 1
```

Actual `test -e` invocations used expanded absolute paths for ~/ paths and lane-prefixed absolute paths for repository paths. Exact targets and individual rc values are retained in `independent.txt`. All these home targets returned 1: `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md`, `~/.bailian/skills/bailian-docs-llm-wiki/models/models.jsonl`, `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json`, `~/.config/systemd/user/qwen-coder.service`, `~/Projects/bounties/ledger/telemetry.jsonl`, `~/Projects/webzites/repos/llm-wiki`, `~/archive`, `~/archive/bench-arena`, `~/archive/bench-arena/`, `~/bench-arena`, `~/bench-arena/`, `~/wikillm/llm-wiki`. `~/Projects` returned 0. Supplemental exact command `test -e ~/.config/llama/qwen-coder-godspeed.jinja` (tilde expanded through `os.path.expanduser`) returned 1, retained in `additional-home-path.txt`. No file contents at these paths were read.

### Verbatim before / do-nothing receipt

```text
SURFACES total=11 present=4 absent=7 prose=0
AGREE agree=9 disagree=2
DEFECT STALE-TEXT 2 Local benchmark battery ~/archive/bench-arena/ asserts 'relocated intact' while absent
DEFECT UNDECLARED-ABSENT 4 Served local model (round 51 successor) http://127.0.0.1:45669
PREDICATE R76-C1 fail
rc=1
```

### Verbatim direct repaired-bytes control

```text
CONTROL-SKIP rows=11 disagreements=0 target_reached=True
PREDICATE R76-C1-control fail
rc=1
```

### Before-bytes control, preserving present anchors

An initial scratch-only attempt had no present relative anchors and reported 5 disagreements (`control-base.txt`). Those four extra disagreements were fixture artifacts, **not host defects**. They are retained rather than hidden.

Corrected fixture was executed in Python Eval (successful cell); exact procedure:

```python
lane = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
s = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/C1ReplayR76'
(s / 'plans').mkdir(parents=True)
(s / 'PROVINCE.md').write_text(subprocess.run(
    ['git', '-C', str(lane), 'show', 'fda63968:PROVINCE.md'],
    capture_output=True, text=True, check=True).stdout)
for rel in ['corpus/evidence/round8-horizon', 'grader.py', 'corpus/README.md',
            'corpus/knowledge/eval-prior-art-calibration.md']:
    dest = s / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.symlink_to(lane / rel)
ns = runpy.run_path(str(lane / 'plans/round76_c1_surface_resolver.py'))
fn = ns['control_declared']
fn.__globals__['__file__'] = str(s / 'plans/round76_c1_surface_resolver.py')
rc = fn(s / 'base-control')
# finally: shutil.rmtree(s)
```

No gate source rewrite, git fixture, commit, clone, or production mutation. Output:

```text
CONTROL declared=present live=absent 4 http://127.0.0.1:45669
CONTROL-SKIP rows=11 disagreements=1 target_reached=False
PREDICATE R76-C1-control pass
rc=0
```

Scratch cleanup was observed twice as `SCRATCH removed=True`; no scratch remains. All cited receipts were copied/written to the exclusive artifact directory first.

## Boundaries / not verified

- This seat executed only assigned C1 replay/control/live probes, not selftests, mutants, C2, builds, lint, or post-integration verification.
- Host observations are point-in-time; no future service availability claim.
- Parent's subsequent control fix remains unexercised here. Parent should replay `--control-declared --lane . --rev fda63968` and verify explicit revision stamping.
- Public remote URLs and secondary repo-relative paths were not expanded into a broader surface universe; frozen claim resolves the first declared anchor only.
- LSP tools were not exposed in this seat's tool inventory. Symbol-reference lookup was unavailable; source ranges were read directly. No refactor performed.
- No tools installed or upgraded.
- An initial read-only HEAD/status command was accidentally launched with a service name and completed rc 0; its stream was not retained, so no HEAD/cleanliness conclusion is based on it. No git mutation occurred.

## Self-evaluation

Accuracy 4/5 (receipts and return codes retained; parent fix explicitly unverified); completeness 4/5 (all six assignment items covered; post-fix replay belongs to parent); clarity 4/5 (separates flawed fixture from corrected control); actionability 4/5 (two source-pointed findings routed); conciseness 4/5 (detailed command evidence makes report longer). Overall 4.0/5. Improvement: parent should bind control receipt to explicit before revision and remove or historically qualify row 3's recurring 200 claim. The user can check both from the named evidence; no passing status is fabricated.
