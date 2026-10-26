# SKILL.md round-37 draft (paste-ready) — R37SkillDraft

Insertion points for the L1:
- Part A: four rows appended to the gate/probe registry table, immediately after the `regex-log-probe` row
  (SKILL.md:576 in the lane at `44b7298`), before the blank line at :577 that precedes the `coverage-census` note.
- Part B: one addendum paragraph immediately after the `Round-36 registry addendum:` paragraph (SKILL.md:591).
- Part C: new section after `## TB2 regex-log grader — round36` (SKILL.md:711-734), as the last section of the file.

Nothing below is claimed to be measured except where a receipt, a command line or a code location is cited.

---

## Part A — registry rows (8 columns, same shape as SKILL.md:574-590)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `git-webserver-probe` | probe | `python3 plans/git_webserver_probe.py --lane .` (`--dry` prints the 22 frozen cases, their servers and predictions with no sandbox; `--smoke` exercises the bubblewrap plumbing only; `--work DIR` scratch parent) | `0` every case yielded exactly one verdict and the summary line printed — **mismatches are on the summary line, never in the exit code** (`mismatches=1` still exits 0, measured) · `1` `--smoke` only: the sandbox did not answer 200 · `2` setup (a capture not at its pinned digest, `/usr/bin/bwrap` not executable, a case yielding no single verdict) | `python3 plans/round37_c2_verify.py --lane .` V1 (capture manifest) and V5 (probe at its freeze digest, `--dry` byte-equal to `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt`): on a clean clone 2026-10-26, `V1 ok` and `V5 ok probe=frozen dry_byte_equal=True`. The 22-case reproduction is the package gate's P10 (`--rerun`), which byte-compares the fresh receipt: `P10 ok probe_rerun=byte-equal bytes=8443` (same run, 53 s wall) | captures `corpus/evidence/round37/tb2-git-webserver/` with `test_outputs.py` sha256 `526aee3d…`, `verify.sh` `1dc44c92…`, `instruction.md` `62151b73…` (probe `PINS`); probe sha256 `63cb75cf…`; receipt `corpus/evidence/round37/git-webserver-probe.txt` sha256 `83550712…`, summary `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | needs `/usr/bin/bwrap`; one sandbox per case with `--unshare-net --unshare-pid --unshare-ipc` (`plans/git_webserver_probe.py:204`), `HOME=/work/home` (`:235`), `/tests` bound read-only to the captures (`:209-213`); writes only under `--work`/`$TMPDIR` and removes it; imports the captured grader function; no network beyond the case's private loopback, never the host's :8080 | kengaku |
| `round37-c1-mutants` | gate | `python3 plans/round37_c1_verify.py --lane .` (`--battery r36` the frozen 14-fixture battery only; `--battery-dir DIR` and `--only M01,M02` development selectors; `--work DIR`) | `0` predicate holds: `GATE plans/pkg_gate.py sha256=frozen`, `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass` · `1` any survivor, invalid mutant, null detection, wrong declaration or renamed disagreement, or the gate not at `ea638822…` (`sha256=NOT-AT-FREEZE-DIGEST`) · `2` usage, duplicate fixture id, or a fixture returning a forbidden argv (a `--spec`, or a first token other than `package`/`d4-line`/`d5-line`); the development selectors print `PREDICATE C1 n/a` and exit by the wrong/renamed/survived rule alone | none beyond itself; `--battery r36` is the do-nothing control (`MUTANTS total=55 killed=5 survived=50` in `control-c1-nothing.txt`), and a fixture must declare `expect` plus its exact `DEFECT` clause set or it counts `wrong` | gate `plans/pkg_gate.py` sha256 `ea638822…`; counter sha256 `dbc9f719…`; `plans/pkg-spec-r35.json` sha256 `e085b435…`; 55 mutants M01–M55 frozen in the counter with clause and advertised class; `plans/round-37-claims.md` at freeze | fixtures and gate copies under `--work`/`$TMPDIR` (`gates/ref.py`, `null.py`, `Mxx.py`); `git init` + index-only `git add` inside fixture dirs only; read-only on the lane, no commit, no network | kengaku |
| `round37-c2` | gate | `python3 plans/round37_c2_verify.py --lane .` (`--work DIR`) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>`, including a check that raises (`error …` is a defect, never a pass) · `2` usage | itself; freeze control `control-c2-nothing.txt` is `checks=7 defects=4` (V2, V3, V4, V7), exit 1. Re-measured on a clean clone of `44b7298` 2026-10-26: `V1 ok`, `V2 DEFECT gate_exit=1`, `V3 DEFECT rows=3 bad=['S111:row','S112:row','S113:row']`, `V4 DEFECT receipt or entry absent`, `V5 ok`, `V6 ok census_exit=0`, `V7 DEFECT receipt or entry absent`, `checks=7 defects=4`, exit 1 — the reds are the entry and the index rows, not the probe | capture `SHA256SUMS` sha256 `e70bb662…` (six files: S111 `526aee3d…`, S112 `1dc44c92…`, S113 `62151b73…`, plus `test.sh`, `task.toml`, `solve.sh`); probe `63cb75cf…`; dry table `0095e591…`; `plans/pkg-spec-r37.json` sha256 `4c61d103…`; receipt `83550712…`. V6 shells out to the absolute `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate` | writes one effective spec copy in its scratch dir; V2 runs `plans/pkg_gate.py package --root <lane> --require-clean-tree --rerun` (timeout 900 s), so P10 executes the frozen probe (bubblewrap, 22 cases, ~58 s measured) and byte-compares to the receipt; reads the lane only, never edits it | kengaku |
| `anchor-digest-check` | gate | `python3 plans/anchor_digest_check.py --lane DIR [--evidence-ref head or index] [--verbose]` — **draft** by R37AnchorSweep at `.ufo/waves/round-37/build/R37AnchorSweep/anchor_digest_check.py` (sha256 `6d7afcd5…d9a323`); the row asserts nothing until the L1 lands the file in `plans/` | `0` no defect · `1` one `DEFECT <Sid> anchor token=<hex> class=<cls> detail=<why> loc=<file>:<n>` line per defect, then `rows=<n> tokens=<n> defects=<n>` · `2` usage or a check that cannot run (`USAGE:`, lane not a directory, no `corpus/SOURCES.md`, not a git work tree, unreadable evidence, `--evidence-ref bogus`) — a check that cannot run never passes | none in the script; falsifiers are external (11-case matrix `fixture_matrix.py`, receipt `fixture-receipt.txt`, 5/5 mutants killed by distinct classes), so this row claims no `--selftest`. Measured on the lane tip `44b7298`: `rows=103 tokens=11 defects=5`, exit 1 (S110 `class=digest-short`; S070/S072/S073/S074 `class=digest-unknown`); `0` only after the erratum plus `corpus/evidence/round37/anchor-captures/` land (5 captures, `sha256sum -c` clean) | no constants in code: every `sha256 <hex>` token in the anchor cell (6th cell, 0-3 leading spaces, 11 cells, as the census reads them) must be 64 lowercase hex and equal a committed `git ls-tree -r <evidence-ref> -- corpus/evidence` blob digest or a 64-hex line of a committed `SHA256SUMS`, unless a `corpus/lessons/*.md` line `Erratum (round 37): S<id> anchor sha256 …` carries both the token and a resolvable digest; `--evidence-ref` reach is `corpus/evidence/` only, default `head` | none at runtime — read-only `git ls-tree`, no temp files, `TMPDIR` untouched | kengaku |

## Part B — addendum paragraph

Round-37 registry addendum: `git-webserver-probe` is the first **service-class** entry here — it starts HTTP
servers inside a per-case network namespace and reads a grader's verdict off a shell script's stdout, so it
needs `/usr/bin/bwrap` and is the only registry row with a runtime cost outside its own temp dir (~58 s for
22 cases, measured). Its exit code does not encode disagreement: a run with one flipped prediction printed
`cases=22 observed_pass=9 observed_fail=13 mismatches=1` and exited 0, so wire it by the summary line or by
the gate's P10 byte-comparison, never by `$?`. `round37-c1-mutants` is the first row whose failure mode is
"the lane's own self-assessment is wrong" rather than "a check broke": 50 of 55 advertised gate clauses were
undemonstrated at freeze (`control-c1-nothing.txt`), and the frozen mutant list, not the battery, defines
what counts. `round37-c2` bundles the package gate over the frozen template, and `anchor-digest-check`
`plans/anchor_digest_check.py` (draft) is the mechanical fix for the round-36 S110 mistyped anchor; on the
lane tip `44b7298` its draft prints `rows=103 tokens=11 defects=5` and exits 1 (S110 `class=digest-short`,
S070/S072/S073/S074 `class=digest-unknown`), and reaches `defects=0` only once the draft erratum and
`corpus/evidence/round37/anchor-captures/` are both landed — so this row records a red state, not a green one.

## Part C — new section

## Service-class TB2 grader — round 37

Before citing the pinned TB2 `configure-git-webserver` scorer, run `python3 plans/git_webserver_probe.py
--lane .` and read its summary line, not its exit code: exit `0` means only that every case produced one
verdict (`plans/git_webserver_probe.py:303-304`), exit `1` is reserved for `--smoke`, exit `2` for setup.
The receipt's summary (`corpus/evidence/round37/git-webserver-probe.txt:49`) reads `cases=22
observed_pass=9 observed_fail=13 mismatches=0`, and `--dry` prints predictions without a sandbox, so it is
not evidence. The class differs from rounds 35–36: the pytest verdict is a substring of a helper script's
stdout (`corpus/evidence/round37/tb2-git-webserver/test_outputs.py:13`), and the helper probes a live
service whose state the agent chooses.

### Decision table — when the verdict is a substring of a helper's stdout

| what the verdict actually depends on | probe it with | what the frozen run showed | cite |
|---|---|---|---|
| the helper echoes untrusted content before it decides | serve the verdict token as the response body | `token-in-body`: `observed=pass` although `❌ TEST FAILED` was printed | `test_outputs.py:13`; `verify.sh:62`; receipt:35 |
| the helper's exit status is never read | delete the tool a required step needs and see whether the verdict moves | `static-file-no-git`: `observed=pass` with no repository, hook or push | `verify.sh:5-6,49`; `test_outputs.py:11`; receipt:7 |
| one verdict is assembled from two HTTP requests | answer the status request `200` and the content request with the wrong body | `status-then-content-split`: `observed=pass`; the first body `not the content` is never compared | `verify.sh:57,60`; receipt:37 |
| `curl` runs with no `-L` and no timeout | 301 to the right body; then a 3 s delay before the right body | `redirect-301`: `observed=fail`; `slow-server-3s`: `observed=pass` | `verify.sh:57` (and `:75` for `wget`); receipt:29,41 |
| the compare is exact after command substitution | trailing newlines; then CR, BOM, a leading space, `Hello World` | trailing newlines stripped: `observed=pass`; the other four `observed=fail` | `verify.sh:63`; receipt:11,13,15,19,21 |
| any path is served | a catch-all server answering `/hello.html` and everything else | `catch-all-200`: `observed=pass` | `verify.sh:57,60`; receipt:31 |
| the instructed port is tested at all | move the server to `:8081` and leave 8080 empty | `wrong-port-8081`: `observed=fail` | `instruction.md:7`; receipt:33 |

### Sandboxing it (each item is required, not stylistic)

- Private network namespace: `verify.sh:57` asks `localhost:8080`, so without `--unshare-net` the probe
  reads whatever the host serves. The probe uses `--unshare-net --unshare-pid --unshare-ipc`
  (`plans/git_webserver_probe.py:204`).
- Scratch `HOME`: `verify.sh:9-13` writes `~/.ssh/config`; an unsandboxed run edits the operator's home
  (`plans/git_webserver_probe.py:11,235`).
- `/tests` bound read-only to the captures: `test_outputs.py:11` invokes the absolute `/tests/verify.sh`.
- Writable, disposable cwd: `verify.sh:16` writes `git_test.exp` into the current directory.
- A `PATH` holding only the tools the case names: `verify.sh:55` branches on `command -v curl`, so the
  runner decides which of the two compare paths executes.
- `apt-get` and `expect` absent, as in any container where they fail: `verify.sh:5-6` and `:49` then fail
  observably and silently; nothing in the script reads their status.

What a green means here: the agent served `/hello.html` on :8080 with a body equal to `hello world` after
command substitution, at the moment of two separate requests. What it does not mean: that a git server, a
clone, a commit or a push happened (`static-file-no-git`, receipt:7), that the body is exactly the file the
instruction asked to publish (`status-then-content-split`, receipt:37), or that the agent's own success
output is the thing being read (`token-in-body`, receipt:35). Treat a reported pass as a statement about
two HTTP responses, never as evidence of instruction compliance (`instruction.md:1-9`).

Limits named at freeze: the probe never executes the oracle and no case performs a real git push, because
`expect` and `apt-get` are absent (`plans/git_webserver_probe.py:21-23`); the probe shows what the verdict
depends on, never that the intended path passes.
