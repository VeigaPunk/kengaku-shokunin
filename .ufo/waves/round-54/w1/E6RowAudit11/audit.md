# Round 54 C2 — independent entry-row audit

Re-executed against shared clone tip `62e9bba5e4a0bed376890299aa6a09039db7e68e`, using the frozen ledger at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54-entrytruth.json` and importing `hermetic_env` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py`. Each invocation ran in the clone with a per-row scratch TMPDIR and a 600-second timeout. Each argv passed entry-mode inspection (no forbidden flags), and each referenced script exists in the clone.

## Verdicts

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round-close-check | 0 | 0 | n/a (no evidence fragment declared) | CONFIRMED |
| round28-census | 1 | 1 | false | MISMATCH |
| round30-defects | 0 | 0 | n/a (no evidence fragment declared) | CONFIRMED |

`round28-census` has matching exit status but fails the independent confirmation rule: its declared compact evidence fragment is absent from the actual pretty-printed JSON output. Exact fragment required: `"c1": { "exit": 0, "findings": [], "metrics":`. The observed output instead starts:

```text
{
  "c1": {
    "exit": 0,
    "findings": [],
    "metrics": {
```

## Exact commands

Executed from the clone directory `/fast/scratch/hyaku/kengaku-r54/E6RowAudit11/lane` under the imported counter hermetic environment, timeout 600 seconds each:

```sh
python3 plans/round_close.py --lane . --round 44 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
python3 plans/round28_census.py --root . --revision 536925b5320fa64298030b4ee76a58fc4b82723f
python3 plans/round30_defects.py --lane .
```

## Exact observed output tails

`round-close-check`:

```text
file\tW04\tS075 duplicate url docs.python.org/3/library/json.html across scopes
file\tW04\tS076 duplicate url docs.python.org/3/library/json.html across scopes
file\tW04\tS100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file\tok\t/fast/scratch/hyaku/kengaku-r54/E6RowAudit11/lane/corpus/SOURCES.md
ROUND-CLOSE census tool=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh sha256=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30 cmd=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kengaku-r54/E6RowAudit11/lane/corpus/SOURCES.md
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT PASS exit=0
```

`round28-census` (complete output is 147 lines; tail):

```text
    "unindexed": []
  },
  "measurement_root": "/fast/scratch/hyaku/kengaku-r54/E6RowAudit11/lane",
  "revision_authority": "caller-supplied; see export/byte-equality receipt",
  "revision_label": "536925b5320fa64298030b4ee76a58fc4b82723f",
  "sources": {
    "malformed": 0,
    "rows": 190,
    "statuses": {
      "mined": 170,
      "queued": 8,
      "rejected": 12
    },
    "tiers": {
      "A": 161,
      "B": 24,
      "C": 5
    }
  }
}
```

The output also contains `"historical_state": { "exit": 1, ... "mismatch": 1 ... }` (pretty-printed across lines) and the declared `c1` values exit 0, findings empty, distinct_task_ids 812, selected_count 16. Exit was 1; only the declared evidence substring did not match exact output formatting.

`round30-defects`:

```text
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
checks=5 defects=0
```

