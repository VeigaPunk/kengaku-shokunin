# R45CritC1Overclaim — C1 calibration review

Measured lane: `git -C /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/lane rev-parse HEAD` → `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (clone root independently printed as `/fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/lane`). No lane files changed.

## Routed findings

### C1-A — The advertised sample is not universal hostile-class evidence (scope overclaim)

**Evidence.** The counter's frozen docstring says the refusal arm consists of ten named modules and the honest arm 104 fixtures from batteries 42–44 (`plans/round45_c1_verify.py` docstring; claims §C1 lines 41–55). The actual predicate is therefore a finite corpus check, not all hostile classes or proof of source intent. A no-inspection fence keyed to the counter's fixture path was already measured by the L1: `claims/control-c1-fence-keyed_name.txt` says it is post-landing, then reports `REFUSALS total=10 clean=10`, `HONEST fixtures=104 admitted=104`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`; the dev-blind control in `claims/dev-blind-c1-keyed.txt` reports `REFUSALS total=10 clean=0 leaked=10`, `PREDICATE C1 fail`. Its fence source (`claims/fences/keyed_name.py`) is literally `return "keyed-on-path" if "/refusals45-" in str(d) else None`; its printed fence SHA256 is the keyed fence's digest. These controls establish that the literal predicate can be passed without implementing the advertised behavior. The frozen claim does disclose an “intent limit” (claims §C1 lines 64–67), so this is a limitation in how “advertised”/“closed” is summarized, not a hidden failure of the narrow finite predicate.

**Routed-line draft — SCORECARD.md round-45 headline/table and corpus/lessons/round-45.md “What was demonstrated”:** Replace “10/10 hostile classes refused” / “the advertised fixture fence closed” with “the frozen counter predicate passed for its 10 refusal modules and 104 honest fixtures; a path-keyed, no-inspection fence also passes, so this is corpus calibration, not general hostile-class or source-intent assurance.” Keep the separate held-out result qualified by its named fixtures.

### C1-B — `outside d` is materially narrower than the advertised rule (counter-measurement overclaim)

**Source evidence.** `plans/round45_c1_verify.py` lines 174–230 says `run_fence` classifies outside opens, but defines `scratch = (root / "fx", root / "btmp")` and tests only those paths. The claims §C1 lines 44–46 instead calls an outside open one under the fixture build scratch but outside `d`; the `fixture_fence.py` contract says the whole process tree must never open a path outside `d`. `round44_c1_verify.py` lines 341–360 confirms the fence sandbox starts with `--ro-bind / /` and only `logdir` is writable; hence other root paths remain readable, even if not writable.

**Measured counterexample command:**
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/env-readmods bash -c "cd /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/lane-readmods && exec python3 plans/round45_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/w-readmods --jobs 8"`

Output (selected complete verdict and wrapper lines):
```
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- keyed-on-path
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE start 00:33:12 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:33:18 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
The `readmods.py` fence used in that scratch clone opens and reads 64 bytes from a `*.py` file in `<root>/mods` on every decision, then returns the same path-keyed verdict. `root/mods` is outside `d`, and outside both counted trees; thus the observed `opens=0`/`clean=10` is false for the rule as worded. The fence source is in this report's `R45CritC1Overclaim/fences/readmods.py`. This is a concrete undermeasurement, independent of the general path-keying caveat.

**Routed-line draft — claims §C1 lines 44–46 and counter docstring:** define the policy region explicitly, then measure that entire region. Either report only “successful opens resolving under `<root>/fx` or `<root>/btmp`, excluding `d`” (and stop claiming “whole process tree opens no path outside d”), or move the trace log and all harness-controlled files outside the fence-visible namespace and monitor all paths outside `d`. Smallest safe correction: do not use `clean`/`read=0` as evidence for the broader `outside d` contract until measurement coverage is closed.

A separate exploratory `readinregion.py` fence deliberately opened a sibling fixture directory under `<root>/fx`; the valid envelope run showed `REFUSALS total=10 clean=0 leaked=0 read=10`, `PREDICATE C1 fail`, and per-run `opens=2`, confirming the counted region detects such opens. The initial sanitizer probe did **not** establish log forgery: it tried to unlink another run's read-only log, produced `ERROR` rows, and failed. I make no log-tampering claim on that evidence.

### C1-C — The round-44 capability row still cites a failing/stale verifier (provenance overclaim)

`SCORECARD.md:1971` defines `fenced-fixture-discovery` with the evidence command `python3 plans/round44_c1_verify.py`; the row is in the 44 capability section. `grep -n "fixture_fence" plans/*.py` returned only `plans/round45_c1_verify.py`, and reading the r44 source shows its own inline `repo_breach` implementation (`round44_c1_verify.py:475–517`), not an import of `fixture_fence.py`. Conversely, r45 pins the r44 verifier itself at its exact digest (`round45_c1_verify.py` PINS line 61 onward), preserving it as the fixture builder. The round-45 counter's control receipt `claims/control-c1-fence-r44.txt` reports that using the r44 fence yielded `REFUSALS total=10 clean=3 leaked=3 read=4` and `PREDICATE C1 fail` (also recited in frozen claims §C1 lines 57–60). Thus r45 adds a separate fence/counter; it does not repair the r44 verifier or validate its old evidence command.

**Routed-line draft — SCORECARD.md `fenced-fixture-discovery` row (line 1971):** retain the historical row as a round-44 failure/retired capability, or replace its evidence command with the round-45 counter and explicitly name the new `fixture_fence.py` surface. Do not describe the old round-44 counter as repaired or imply the new fence is imported by it.

## Measurements and their validity

Baseline run used a clean clone at the measured tip and the required envelope:
```
command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/env-base bash -c "cd '/fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/lane' && exec python3 plans/round45_c1_verify.py --lane . --work '/fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/wbase' --jobs 8"`
ENVELOPE start 00:32:15 cwd=/home/vgpnk/Projects/shokunin
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:32:21 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
The resumed-open parser probe command was `envelope.sh /fast/scratch/hyaku/kengaku-r45/R45CritC1Overclaim/env-parser python3 -c '<inline reproduction using the counter OPEN_RE, UNFINISHED_RE, RESUMED_RE; synthetic lines: unfinished openat and resumed openat>'`; output `synthetic_lines=2 open_re_matches=1 pending_after=0 outside_opens_counted=0`, `ENVELOPE start 00:32:42 cwd=/home/vgpnk/Projects/shokunin`, `ENVELOPE end 00:32:43 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. The resumed line drops `openat(`, so the parser pops the pending entry and fails the open-regex match. This is an additional parser edge case, but the synthetic test does not establish a real fixture-triggered exploit; route as a counter robustness question, not a measured C1 defeat.

All experimental fence runs were performed against scratch clones only. The unsuccessful initial attempts (missing `--work` directory) and the sanitizer `ERROR` run are not counted as verdict evidence.

VERDICT: c1-overclaims-3
