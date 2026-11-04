source: S260 — own-work, `corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15` and `corpus/evidence/round81/vulnerable-secret-probe.txt:1-15` (subject at 1, stamp 2-14, `OBSERVATIONS_BEGIN` 15, observations from 16); S261 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/ — `log-summary-date-ranges/instruction.md:9`, `log-summary-date-ranges/task.toml:6`, `vulnerable-secret/instruction.md:1`; S256 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md — `corpus/evidence/round79/sources/tb2-readme.md:24`
verified-at: 2026-11-04 (round-82 tip 12f1029a45cf0097a3afd030d757bf93b87f8018)
recheck: 2026-12-04 (30d) — re-run `python3 plans/round81_log_summary_probe.py --lane . --work "$(mktemp -d)"` and `python3 plans/round81_vulnerable_secret_probe.py --lane . --work "$(mktemp -d)"`: each must print `cases=12 observed_pass=4 observed_fail=8 mismatches=0` and `PREDICATE R81-C1 pass` and exit 0, with `SUBJECT_SHA`/`TOOL_SHA`/`HOST_PYTHON`/`HOST_OPENSSL` matching the receipts; then `python3 plans/round81_c1_new_members.py --lane .`; re-open S261 if either tally moves

# TB2 file-artifact graders: two stdlib-only replays and the host pin

Thesis: two `file-artifact` members of the Terminal-Bench 2.0 population whose graders import only
the standard library can be replayed offline without the task image, and the replay is only a
measurement if the receipt pins the *subject* (the captured grader bytes) and the *environment*
(interpreter and openssl). Round 81 does both, and the frozen selection rule is what made the two
members, not a preference for easy graders.

## What the two graders are, and what the replay stages

| member | capture sha256 | asserts | staged end state | legs |
|---|---|---|---|---|
| `log-summary-date-ranges` | `2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4` | 5 | `/app/summary.csv` | `test_summary_file_exists`, `test_summary_structure_and_counts` |
| `vulnerable-secret` | `f2b65f63ac81acd1e80e1ad4c59c1022131a0f9eb20f8ab3212c4ef8d8f0c753` | 5 | `/app/results.txt` | `test_results_file_exists`, `test_results_file_contains_secret_flag`, `test_results_file_format` |

Both captures are byte-identical to the files at the pinned upstream tree
(`2fd12b88`, checked by two independent sha256 computations — S261). Their instructions ask for one
artefact each (S261): a CSV at `/app/summary.csv` with a header and 15 fixed rows, and a flag string
at `/app/results.txt`. The replay materialises that artefact in a bubblewrap sandbox, binds the
capture read-only at `/tests`, and calls the capture's own test functions in file order; a return is
`P`, an `AssertionError` or any other escaping exception is `F`. The task image is never pulled.

## Case tables (frozen before the runs)

Twelve cases each, four predicted pass and eight predicted fail; predictions derive from the tag
sets the case declares (`violates=`), never from a previous run.

| member | pass cases | fail cases | grader legs exercised |
|---|---|---|---|
| `log-summary-date-ranges` | exact 15-row table; no trailing newline; CRLF; quoted fields | missing file; empty file; wrong header; 14 rows; 16 rows; one count changed; two rows swapped; extra blank row | both legs in every failing case except `empty-file` (existence passes, structure fails) |
| `vulnerable-secret` | exact flag; trailing newline; surrounding spaces; CRLF | missing file; empty file; wrong flag; `FLAG{` only; `FLAG{x}`; flag plus second line; truncated flag; lower-cased flag | existence passes on six fail cases; `content` fails on all eight |

Measured at the tip: `cases=12 observed_pass=4 observed_fail=8 mismatches=0` for both
(`corpus/evidence/round81/log-summary-date-ranges-probe.txt`,
`corpus/evidence/round81/vulnerable-secret-probe.txt`). The interesting legs are the whitespace and
line-ending ones: the `log-summary` grader parses with `csv.reader(f, newline="")`, so CRLF and
quoted fields pass while an extra blank row adds a 16th record and fails; the `vulnerable-secret`
grader strips, so surrounding whitespace and CRLF pass while a second line fails on the stripped
equality.

## The environment pin

A replay's verdict is a function of the interpreter that imports the capture and the userland the
legs call. The round-81 receipt stamps `HOST_PYTHON` (`Python 3.14.8`) and `HOST_OPENSSL`
(`OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`) beside `SUBJECT_SHA`, `TOOL_SHA`
and `LANE_TIP`; the gate rejects a receipt whose host pair does not match the live host. Without the
pin a replay is "some run on some machine", which is exactly what the round-80 spot-check's U2 found
in a receipt whose worktree was moving.

## What carries forward

- A `file-artifact` replay is cheap when the grader is stdlib-only: no image, no network, no service.
  The expensive part is the case table, not the sandbox.
- The selection rule (stdlib-only imports, class ⊆ {file-artifact, serialization-schema}, maximum
  assert count) is a *derivable* choice; the counter prints the eleven candidates and the maximum
  every run, so the two members cannot be swapped for a flattering pair without the print changing.
- 62 members stay `unexecuted`; 26 of 88 are `executed` and the population gate prints
  `covered=15` of 16 classes. One more class (`container-image`) has no member at all.

## Connections

- `corpus/knowledge/tb2-nginx-request-logging-offline.md` — the network-service replay recipe; this
  entry is its file-artifact counterpart (no service, no ports).
- `corpus/knowledge/benchmark-verifier-execution-model.md` — why a `file-artifact` grader reads a
  produced artefact rather than a process.
- `corpus/lessons/round-81.md` — Gate (S259/S260/S261), M81-1/M81-2, and the two errata this round
  discharges (R80-U1, R80-U6).
- Sources: S260 (own-work instrument set), S261 (pinned task documents), S256 (harness README).
