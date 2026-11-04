# Toolathlon grader comparison functions — hermetic fixture probe, stage 2 (lane `kengaku`, round 8)

Lane own-work artefact. Ground: round-7 CANNOT-ANSWER item **N22** — the ten
candidates the round-7 probe left unattempted for lack of a hermetic fixture.

## Why this exists

Round 7's probe called the comparison functions with fixtures of their real input
types and found 16 of 16 discriminating, but it listed ten candidates as "not
attempted":

| task | function | what it needs |
|---|---|---|
| game-statistics | `verify_daily_leaderboard`, `verify_historical_data_integrity`, `verify_historical_stats_update` | a live BigQuery client |
| live-transactions | `check_storage_bucket_exists` | a cloud storage bucket |
| ab-testing | `validate_task_completion` | a cloud storage bucket |
| k8s-mysql | `compare_csv` | two real CSV files |
| academic-pdf-report | `check_filled_excel` | a real `.xlsx` read through pandas |
| flagged-transactions | `compare_excel_files` | two real `.xlsx` files through pandas |
| music-analysis | `compare_excel_files` | two real `.xlsx` workbooks through pandas |
| nvidia-market | `check_sheet1` | a real workbook sheet through pandas |

Round 7's own wording was that it "said nothing about them either". This probe
builds fixtures for the first six and re-attempts them.

## Method

- Source of the bytes: `https://github.com/hkust-nlp/Toolathlon` at commit
  `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, path
  `tasks/finalpool/<task>/evaluation/main.py`.
- Each grader module is `exec`'d with `__name__` set to a value other than
  `"__main__"`, so its `main()` guard does not fire. The repository's shared
  `utils` and `configs` packages are on `sys.path`, so the graders' own helpers
  are the real ones.
- **The cloud is faked, not contacted.** `google.cloud.storage` is a local module
  whose `Client` returns buckets from an in-process set; `google.cloud.bigquery` is
  a local module whose `Client` answers the four query shapes the game-statistics
  graders issue (`leaderboard_<date>`, `player_historical_stats`,
  `daily_scores_stream`, and the `daily_counts`/`day_gap` integrity CTE). No
  credential is used and no request leaves the process.
- **Real files where real files are needed.** `compare_csv` is called with two
  actual CSV files on disk, differing in one row's `year`. The GCS graders are
  called with a bucket name that exists and with one that does not. The BigQuery
  graders are called with a 100-row ranked leaderboard, ten days of daily counts,
  and two players' aggregated scores, each perturbed in exactly one unit.
- One grader reads `configs/gcp-service_account.keys.json` relative to the working
  directory at import time, so the probe runs inside a scratch directory holding a
  placeholder key file.
- A fixture the function *rejects* is reported as `fixture-rejected` — a statement
  about the fixture, never about the grader. The graders print their own failure
  reasons, and those reasons are carried in the detail column.
- `discriminates` means the identical pair and the one-unit-perturbed pair produce
  different verdicts in the way the function's own return convention implies. It
  is never a statement that the grader is correct.

## Run

```
python3 lanes/kengaku/round8/toolathlon-grader-fixture-probe2.py --src-dir <dir-with-task-trees>
```

Run 2026-10-24 against commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`.

## Result

| task | function | real input type | verdict | detail |
|---|---|---|---|---|
| k8s-mysql | `compare_csv` | two real CSV files with year/driver/constructor columns | **discriminates** | identical=True perturbed=False |
| live-transactions | `check_storage_bucket_exists` | bucket name + project id; the GCS client is a local fake | **discriminates** | identical=True perturbed=False |
| ab-testing | `validate_task_completion` | launch and eval timestamps; the GCS client is a local fake | **discriminates** | identical returned cleanly, perturbed raised ValueError: Task validation failed - storage bucket with prefix 'promo-assets-for-b' was not created |
| game-statistics | `verify_daily_leaderboard` | a BigQuery client (local fake) + a date string | **discriminates** | identical=True perturbed=False |
| game-statistics | `verify_historical_data_integrity` | a BigQuery client (local fake) + a date string | **discriminates** | identical=True perturbed=False |
| game-statistics | `verify_historical_stats_update` | a BigQuery client (local fake) + a date string | **discriminates** | identical=True perturbed=False |

## Not attempted (no faithful fixture on this host)
- `academic-pdf-report` :: `check_filled_excel` — reads a real .xlsx through pandas (pd.read_excel, df.iterrows, pd.isna); pandas is not installed and no package manager is available on this host
- `flagged-transactions` :: `compare_excel_files` — compares two real .xlsx files through pandas DataFrame operations (df[cols], sort_values, reset_index, iloc, pd.isna, pd.to_datetime)
- `music-analysis` :: `compare_excel_files` — compares two real .xlsx workbooks sheet-by-sheet through pandas
- `nvidia-market` :: `check_sheet1` — reads a real workbook sheet through pandas and compares numeric columns against a ground-truth DataFrame

## Counts
- discriminates: 6 of 6

## Reading of the result

- `ab-testing::validate_task_completion` does not return a verdict at all: on the
  failure path it **raises** `ValueError("Task validation failed - storage bucket
  with prefix 'promo-assets-for-b' was not created")`. A probe that looks for a
  falsy return would mis-read it, exactly as round 7 found for
  `invoice-org::check_total_amount`.
- The three `game-statistics` graders are `async def` but contain no `await`; they
  are ordinary functions in an async wrapper. Their client surface is two calls:
  `client.get_table(table_id)` (returning a `.schema` of named fields, and raising
  `NotFound` when the table is absent) and `client.query(sql)` (returning a job
  whose `.result()` is an iterable of row dicts).
- `verify_daily_leaderboard` demands exactly 100 records and cross-checks the
  leaderboard table against the `daily_scores_stream` aggregation, so a fixture
  must supply the same 100 players on both sides; a fixture that supplies the
  aggregation for a different population is rejected as `fixture-rejected`, which
  is what an earlier draft of this probe did before the fixture was corrected.

## Limits

Four candidates remain unattempted, and the reason is a property of this host, not
of the graders: their comparison loops run on pandas DataFrame objects
(`df[cols]`, `sort_values`, `reset_index`, `iloc`, `iterrows`, `pd.isna`,
`pd.to_datetime`), pandas is not installed, and no package manager is available to
install it. A verdict produced from a hand-written DataFrame stand-in would be a
statement about the stand-in rather than about the grader, so this probe does not
produce one.

Nothing here executes a task, touches a workspace, contacts a cloud account or
evaluates a model.
