# FHistFlags — independent numeric replay: require_login / require_reset / storage_state

Seat: `KengakuR28.FHistFlags` (reviewer, falsification wave round-28). Scope: replay the
login/reset flag counters and the storage_state path counts independently of
`plans/benchmark_spec_audit.py`, then compare the instrument's `--json` output read-only.
No auth-state file was opened; `storage_state` values are counted as path strings only.
No upstream code was executed or imported.

## Inputs pinned

- Raw tasks: `plans/fixtures/r28/webarena/config_files/test.raw.json`
  sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` — matches
  `manifest.json files["config_files/test.raw.json"].sha256`; upstream revision
  `dce04686a56253aefba7b18a4fa0937cf1dc987b` (per manifest).
- Instrument executed: `plans/benchmark_spec_audit.py` sha256
  `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` — matches
  `.ufo/waves/round-28/candidate-freeze.json` instrument pin.
- Candidate re-read: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` sha256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — matches the frozen
  candidate digest exactly. Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md`
  is not admitted yet.

## Exact commands and observed outputs

Independent derivation #1 (jq):

```
$ jq 'length' test.raw.json                       → 812
$ jq 'group_by(.require_login) | map({value: .[0].require_login, count: length})'
  → [{ "value": true, "count": 812 }]
$ jq 'group_by(.require_reset) | map({value: .[0].require_reset, count: length})'
  → [{ "value": false, "count": 812 }]
$ jq 'group_by(.storage_state) | map({storage_state: .[0].storage_state, count: length}) | sort_by(-.count)'
  → ./.auth/shopping_state.json: 187
    ./.auth/gitlab_state.json: 186
    ./.auth/shopping_admin_state.json: 182
    null (JSON null, key present): 128
    ./.auth/reddit_state.json: 111
    ./.auth/gitlab.reddit_state.json: 18
  sum = 812
$ jq 'all(.[]; has("storage_state") and has("require_login") and has("require_reset"))'
  → true
```

Independent derivation #2 (own stdlib script, persisted
`.ufo/waves/round-28/scratch/FHistFlags/independent_flag_census.py`; output
`scratch/FHistFlags/census-stdlib.json`):

```
tasks 812
require_login {True: 812}
require_reset {False: 812}
storage_state {shopping_state.json: 187, gitlab_state.json: 186,
  shopping_admin_state.json: 182, <absent>: 128, reddit_state.json: 111,
  gitlab.reddit_state.json: 18}
non_bool_or_missing []
```

Instrument run (read-only, `PYTHONDONTWRITEBYTECODE=1`):

```
$ python3 plans/benchmark_spec_audit.py --json    → EXIT=0, findings=0
  metrics.login_flags  = {"true": 812}
  metrics.reset_flags  = {"false": 812}
  metrics.task_count   = 812, distinct_task_ids = 812
  (metrics emitted no storage_state counter — instrument does not count it)
```

## Comparison

| metric | jq | own stdlib | instrument --json | agreement |
|---|---|---|---|---|
| require_login true/false | 812/0 | 812/0 | 812/0 | YES |
| require_reset true/false | 0/812 | 0/812 | 0/812 | YES |
| task_count | 812 | 812 | 812 | YES |
| storage_state path counts | 6 distinct values, sum 812 | identical | not emitted (n/a) | n/a — own census only |
| non-boolean flags / missing keys | none | none | 0 `flag_invalid` findings | YES |

storage_state path-count differences (new information not emitted by the instrument):

- 128 tasks carry `storage_state: null` — exactly the map-only site sets (`map` 109,
  `map,wikipedia` 17, `map,shopping_admin` 2); every `start_url` is `__MAP__`.
- Cross-tab site-set → storage_state is a pure 1:1 map: every site set uses exactly one
  path (or null). `gitlab,reddit` tasks use `./.auth/gitlab.reddit_state.json` (18);
  `reddit,shopping` uses `./.auth/reddit_state.json` (5).
- All 128 no-login-state tasks still declare `require_login: true` (e.g. task_id 7).
  Literal inventory fact; runtime meaning unverified — consistent with the candidate's
  rule 5 ("mutable state/reset policy as unverified dependencies").

## Candidate cross-check

The frozen candidate (SHA256 verified above) publishes no numeric require_login /
require_reset / storage_state counts in its metrics table, so nothing in it contradicts
this replay. Its line-23 statement "Only fixture login-state path strings occur in the
task data; no account/token/cookie values or auth-state files were opened" is consistent
with the observed data: the only auth material in the raw JSON is `./.auth/*_state.json`
path strings. All other table numbers in the candidate (812, 27 strata, 651 targets,
site_sets histogram) are consistent with the same `--json` fields.

## Findings

None. The instrument's flag counters agree exactly with two independent derivations
(jq and a persisted stdlib script) across all 812 tasks, including the 128
`storage_state: null` tasks that still declare `require_login: true`. Instrument output
was produced by the exact byte-pinned script digest on the manifest-pinned input.

## Residual risk / verification gaps

- The instrument emits no `storage_state` metric, so the storage census above is an
  independent addition, not a like-for-like counter comparison; it stands on two
  independent derivations only.
- `require_login: true` on map tasks with `storage_state: null` is a literal field
  fact; whether the upstream browser setup treats that pair as no-auth is runtime
  behavior outside this static replay (correctly carried as unverified by the
  candidate, not a defect).
- Agreement is author-side independent implementation (jq + own stdlib script versus
  the shipped instrument), not roster-external closure.

Tool installs: none. No pacman/host-service changes. Scratch evidence:
`.ufo/waves/round-28/scratch/FHistFlags/{independent_flag_census.py,census-stdlib.json,jq-flags.txt,jq-storage.txt,audit-instrument-metrics.json}`.

VERDICT: PASS
