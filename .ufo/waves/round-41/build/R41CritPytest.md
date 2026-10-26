# R41CritPytest — real-pytest parity for the round-41 C2 case set

Seat: R41CritPytest (leaf, wave 1). Lane snapshot: `/fast/scratch/hyaku/kengaku-r41/R41CritPytest/lane`
(`git clone --shared` of `kengaku-shokunin`; `git -C .../lane rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r41/R41CritPytest/lane` before any write; no commit, no index write).

## Question

Does the frozen C2 probe (`plans/constraints_probe.py` + receipt
`corpus/evidence/round41/constraints-probe.txt`) agree with the task's **own verifier**, i.e. real
pytest 8.4.1 on Python 3.13 reading `/tests/test_outputs.py`, per test, on the same 25 end states?

## Method

End states were built **host-side exactly as the probe builds them**, by importing a copy of the frozen
probe from my clone and calling its own `Case` table, `INPUTS`, `PINS` and `apply_edit`
(`/fast/scratch/hyaku/kengaku-r41/R41CritPytest/drive.py`, copied to
`.ufo/waves/round-41/build/R41CritPytest/drive.py`). Per case: fresh dir, seed the three captured
calendars, `apply_edit(app, case.edit)`, write `case.meeting` if set; the oracle case's recipe
(`bash -euo pipefail /cap/solve.sh`, probe's `ORACLE`) runs in its own nested bwrap over the same `/app`
bind. Then the task's verifier command, reproduced verbatim from `test.sh:18-22`:

```
uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
```

Layout matches the image, not the probe's shortcut: grader at `/tests/test_outputs.py`, `/app` the case
end state (cwd), `/logs/verifier/ctrf.json` the report, `/inputs` absent (so
`test_outputs.py:91` takes the sha256 branch). Captures were digest-checked against the probe's `PINS`
before any run (`SETUP` path exits 2 otherwise). Per-test verdicts were read from `ctrf.json`
(`src=ctrf` in every one of the 25 cases), letters ordered S,C,E as in `constraints_probe.py:16-17`.

Isolation: the whole driver ran inside the mandated envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`,
and each case ran in a nested probe-style sandbox (`--unshare-net --unshare-pid --unshare-ipc --new-session
--ro-bind /usr /usr --ro-bind /etc /etc --tmpfs /tmp --bind <case>/app /app ...`). Network was used only
outside the sandbox, to warm `UV_CACHE_DIR` once; every in-sandbox uv invocation ran with `UV_OFFLINE=1`.

Environment evidence (in `control.txt`): in-sandbox `uv run --no-project --python 3.13 python -V` →
`Python 3.13.16`; pytest summary line `3 passed in 0.35s` (pytest 8.4.1 from the uvx env); host uv
`0.13.0`. Nothing was installed host-wide (uv and uvx already present; only `UV_CACHE_DIR` populated
under scratch).

Receipt letters were parsed from the frozen receipt's `CASE <id> ... tests=<S,C,E>` fields.

## Result — 25/25 cases, 75/75 test verdicts

Two independent full passes (~29 s each), plus a second in-pass grading of the same end state per case
(`regrade`). Pass 2 is identical to pass 1 (
`diff <(sed 's/regrade=[^ ]*//' full-run1.txt) <(sed 's/regrade=[^ ]*//' full-run2.txt)` → empty).

| case | receipt tests S,C,E | pytest tests S,C,E | receipt obs | pytest obs | match | regrade | pytest rc |
|---|---|---|---|---|---|---|---|
| `nop` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `oracle-solve-sh` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `literal-correct-slot` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `later-valid-wed-1105` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `later-valid-thu-1100` | `PPF` | `PPF` | fail | fail | yes | same | 1 |
| `conflict-mon-1230` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `bob-start-0900-wed` | `PFP` | `PFP` | fail | fail | yes | same | 1 |
| `decoy-first-vevent` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `duration-90min` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `missing-carol` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `title-wrong` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `seconds-30` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `tzid-form` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `weekend-sat-20` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `input-appended` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `input-event-deleted-wed-1000` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `wed-1059-overlaps-alice` | `PFP` | `PFP` | fail | fail | yes | same | 1 |
| `crlf-line-endings` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `folded-attendee-line` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `dtstart-value-datetime` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `no-prodid-header` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `decoy-second-vevent` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `extra-attendee-dave` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `lowercase-property-names` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `input-crlf-rewrite` | `PPP` | `PPP` | pass | pass | yes | same | 0 |

`cases=25 per-test-agreements=75/75`; pytest `rc` is 0 exactly for the six `PPP` cases and 1 otherwise
(the six pass cases are the receipt's `observed_pass=6`).

**Differences: none.** No case and no individual test disagreed.

## The receipt's two `match=NO` rows are confirmed as prediction errors, not probe errors

* `later-valid-wed-1105`: receipt `predicted_tests=PPF`, `tests=PFF`; pytest produced `PFF` — tests 2
  and 3 (constraints/earliest) fail, test 1 passes.
* `seconds-30`: receipt `predicted_tests=PPF`, `tests=PFF`; pytest produced `PFF` as well.

So real pytest agrees with the **observed** letters the receipt carries verbatim, exactly where the
frozen predictions were wrong. The receipt's `mismatches=2` therefore stands as a fact about the
pre-freeze predictions, not about the measurement.

## Control — the harness is live, not a constant

Negative control on an end state whose receipt verdict is `FFF`: `cases/tzid-form` was re-seeded with the
probe's `GOOD_ICS` (Wed 11:00, the right slot) and the same verifier command was run again. Result
(`control.txt`): `3 passed in 0.35s`, ctrf
`[('test_structure_...', 'passed'), ('test_constraints_...', 'passed'), ('test_earliest_...', 'passed')]`
— i.e. `FFF` → `PPP` when and only when the end state changes. The parity table above is a measurement of
each end state.

## Deviations and limits (stated, not hidden)

1. `test.sh`'s prologue (apt-get, curl-installed uv, `source $HOME/.local/bin/env`, the `PWD=/` guard) is
   not executed: the case sandbox is network-isolated, so host uv 0.13.0 binaries are ro-bound into it as
   `/uvbin/{uv,uvx}` and the ephemeral env is served from `UV_CACHE_DIR` with `UV_OFFLINE=1`. The grading
   command itself is byte-identical to `test.sh:18-22`.
2. The task Docker image (`alexgshaw/constraints-scheduling:20251031`) is never pulled; `/app` is a
   scratch directory built host-side from the probe's own `Case` fields and bound as `/app`. This is the
   probe's model, so parity is of pytest semantics/paths, not of container parity.
3. For `oracle-solve-sh` the recipe (`solve.sh`) ran in a separate nested bwrap invocation over the same
   `/app` bind instead of in the same invocation as the probe; it writes only `meeting_scheduled.ics`,
   and the case graded `PPP`, so the staging is equivalent.
4. `/tests` and `/logs` are writable binds inside scratch (needed so pytest's cache and
   `--ctrf /logs/verifier/ctrf.json` can write). Grader content was digest-verified against the probe's
   `PINS` (`1422b345…`) before any run.
5. `solve.sh` runs `/usr/bin/python3` = host 3.14.8, while the image ships Ubuntu 24.04's python3 (3.12).
   Same limitation as the frozen probe; it affects only the oracle case, which passes.
6. `test.sh` writes `reward.txt`; this seat compares per-test verdicts (the receipt's `tests=` letters)
   instead, which is the finer-grained quantity. Overall pass/fail was derived as "all three passed",
   the probe's definition.

## Evidence inventory (this report dir)

| file | content |
|---|---|
| `full-run1.txt`, `full-run2.txt` | the two independent full passes, 25 `CASE` lines each, byte-identical modulo the `regrade=` tag |
| `results.jsonl` | 50 records (25 cases × 2 passes): both in-pass gradings, ctrf per-test statuses, rc, stdout/stderr tails |
| `table.md` | the parity table above, generated from `full-run2.txt` |
| `control.txt` | the `tzid-form` → good-slot control plus uv/python versions |
| `drive.py` | the driver: probe copy import, end-state build, nested bwrap, verifier command, ctrf parse |

Scratch (`/fast/scratch/hyaku/kengaku-r41/R41CritPytest`) is deleted after this report; nothing was
written to the lane tree, the fleet root, `~/.local/bin`, `/usr`, `/etc`, or `$HOME` outside scratch.

VERDICT: pytest-parity-25/25
