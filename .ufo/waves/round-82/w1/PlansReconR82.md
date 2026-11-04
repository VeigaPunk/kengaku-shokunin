# PlansReconR82 — read-only recon for R82-C1 (registry rows) and R82-C3 (sweep runnability)

Seat `PlansReconR82`, role scout, round 82 wave w1. Read-only: the only lane file written is this
report (my named deliverable) — no other lane file, no git/jj mutating command, and no counter that
writes. Scratch `/fast/scratch/hyaku/kengaku-r82/PlansReconR82/` (deleted at yield). Every number
below carries the command that produced it; guesses are labelled **guess**.

Measured at tip `12f1029a45cf0097a3afd030d757bf93b87f8018` (== freeze commit) on 2026-11-04T09:42Z,
re-checked 09:47Z (unchanged):

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
12f1029a45cf0097a3afd030d757bf93b87f8018
$ git -C … rev-parse HEAD
12f1029a45cf0097a3afd030d757bf93b87f8018
```

Toolchain on this host: `Python 3.14.8 (main, Oct 2 2026…) [GCC 16.2.1]`, `git 2.56.0`,
`bubblewrap 0.13.1`, `gcc (GCC) 16.2.1`, `uv` at `/home/vgpnk/.local/bin/uv`.
Absent on the host: `nginx`, `expect`, `biopython` (`python3 -c "import Bio"` →
`ModuleNotFoundError: No module named 'Bio'`, rc 1), python modules `torch`/`transformers`/`grpc`/
`pandas`/`pytest` in the system interpreter.

---

## 0. Lane state, census, disk guard

### 0.1 Worktree is NOT clean, and the C3 map's own member caused it

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain
 M corpus/evidence/round68/pypi/server-log.txt
 M corpus/evidence/round68/pypi/stderr/K1.txt
 M corpus/evidence/round68/pypi/stderr/K3.txt
?? .ufo/waves/round-82/
?? corpus/evidence/round82/census-before.txt
[paths=6]
$ git diff --stat corpus/evidence/round68/pypi/
 corpus/evidence/round68/pypi/server-log.txt | 4 ++--
 corpus/evidence/round68/pypi/stderr/K1.txt  | 2 +-
 corpus/evidence/round68/pypi/stderr/K3.txt  | 2 +-
 3 files changed, 4 insertions(+), 4 deletions(-)
```

The three modified files are the **pypi-server member's side-effect output**, written at
`2026-11-04 06:33:45 -0300` by a run whose scratch path is baked into the bytes:

```
- Location: /fast/scratch/hyaku/kengaku-r68/scored/venv/lib/python3.14/site-packages
+ Location: /fast/scratch/hyaku/kengaku-r82/probe/py3/venv/lib/python3.14/site-packages
- 127.0.0.1 - - [03/Nov/2026 19:58:58] "GET /simple/vectorops/ HTTP/1.1" 200 -
+ 127.0.0.1 - - [04/Nov/2026 06:33:45] "GET /simple/vectorops/ HTTP/1.1" 200 -
```

**Concurrent activity (not mine).** The `status --porcelain` above was taken at 09:42Z. At 09:50Z the
same command additionally showed ` M SKILL.md` and `?? corpus/evidence/round82/fetch/`: another seat
is adding the four C1 registry rows to the *worktree* (`git diff --stat SKILL.md` → `1 file changed,
4 insertions(+)`; worktree registry now 137 data rows, `HEAD:SKILL.md` still 133). Every number in
this report is a snapshot at the time of its command; I wrote no lane file except this report.

Mechanism (source, not guess): `plans/round68_c1_pypi_finish.py:103`
`evid = pathlib.Path(evidence_dir) if evidence_dir else lane / EVID_DIR` with
`EVID_DIR = "corpus/evidence/round68/pypi"` (:39), writing `stderr/K*.txt` (`:104` dir, `:193-194`
per-case `dst.write_bytes`) and `server-log.txt` (`:165-166`) into the **lane**. The frozen map's argv for this member
(`["python3","plans/round68_c1_pypi_finish.py","--lane",".","--work","<WORK>","--receipt",
"<WORK>/<MEMBER>.receipt.txt"]`) does **not** pass `--evidence-dir`, so any sweep that runs the
member with the lane as `--lane` overwrites three tracked files. This is a live, already-materialized
hazard for R82-C3's staged-write/cleanliness leg: the gate must run members in a disposable clone
(or the map must carry `--evidence-dir`), and the L1 must decide whether these three bytes are
restored — I did not touch them (read-only seat).

### 0.2 Census

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin kengaku
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	W04	S213 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py across scopes
kengaku	W04	S214 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py across scopes
kengaku	W04	S215 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh across scopes
kengaku	W04	S216 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md across scopes
kengaku	W04	S217 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/gen.py across scopes
kengaku	W04	S222 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/instruction.md across scopes
kengaku	W04	S227 duplicate url encoding.spec.whatwg.org/index-windows-1252.txt across scopes
kengaku	W04	S234 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	W04	S237 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py across scopes
kengaku	W04	S243 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py across scopes
kengaku	W04	S256 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
[census rc=0]
```
27 stdout lines: 26 `W04 duplicate url … across scopes` warnings + the `ok` line; rc 0.

### 0.3 Disk guard

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                              27%    93.6G
/var/tmp                          24%   711.0G
/fast/scratch/hyaku               56%   358.6G
```
rc 0. Largest `/fast/scratch/hyaku` consumers at check time: `kaidoku-r53` 10.3G (idle 6631),
`kake-r75` 10.2G (idle 552), `kengaku-r80` 9.9G (idle 112), `kengaku-r76` 8.4G, then `kengaku-r82`
2.0G (in use). `/tmp` top consumer `polish61-m47tumble-cache` 27.7G (idle 1428) — not ours.

---

## 1. The four claim-referenced CLI instruments (R82-C1 rows)

All four exist and are **byte-identical at BASE and at the tip** (sha256 of working tree vs
`git show a3a03ac3:<path>` compared in the same Python process, all `same=True`):

| script | lines | sha256 |
|---|---|---|
| `plans/log_appendonly.py` | 271 | `e7dbaf7b0915f6299151adb16d12500bd8754635afc24ad717d11367a0f91067` |
| `plans/round37_c1_attribution.py` | 89 | `7064cf1a2ef8e6ef26224b17d7da13a6b9aa6630fd83c13110d9474bbd7db147` |
| `plans/round66_registry_check.py` | 335 | `982b235d38af62b0f5428b646d653e53671f25db76d5f605ff8e9c958b66e914` |
| `plans/round80_c1_remint.py` | 187 | `632cb3c2e5d8b0d47380779f6860876136519ce583334b91bbffa41ba4547841` |

### 1.1 `plans/log_appendonly.py`

```
$ python3 plans/log_appendonly.py --help          # rc 0
usage: log_appendonly.py [-h] [--lane LANE] [--path PATH] [--since SINCE]
                         [--show-lines] [--verbose] [--selftest]

report commits that rewrite a committed log line

options:
  -h, --help     show this help message and exit
  --lane LANE
  --path PATH
  --since SINCE  bind the walk to <rev>..HEAD
  --show-lines
  --verbose      print the walk reconciliation against plain git log
  --selftest
```

- **Writes:** nothing in the lane. The only `write_text` is `_commit()` at `:172`
  `(repo / "LOG.md").write_text(...)`, which runs only inside `selftest()` fixtures under a
  `tempfile.TemporaryDirectory` (`:191`). Docstring: "Read-only: no file in the repository is
  written, no index lock is taken (`GIT_OPTIONAL_LOCKS=0`)".
- **Verdict map** (`:250-268`, `check()` return at `:161`): `0` no violating commit; `1`
  `violations>0`; `2` SETUP (`SETUP <e>` on stderr, from `RuntimeError`/`OSError` — no git, not a
  repo, `--since` not an ancestor of HEAD). Summary line always printed:
  `LOG-APPENDONLY path=… head=… commits=<n> violations=<k>`.
- **Self-test:** yes, `--selftest` (no `--work`). Prints one
  `SELFTEST <NAME> rc=<got> want_rc=<want> ok|FAIL :: <summary>` per case plus a final
  `SELFTEST pass|fail`; exits 0/1. Observed (`TMPDIR=$S/tmp`): 7 cases GREEN/RED-EDIT/RED-DELETE/
  RED-MOVE/SINCE-FULL/SINCE-C1/SINCE-C2 + `SELFTEST BAD-SINCE rc=2 want_rc=2 ok :: SETUP --since
  side: not an ancestor of HEAD`, then `SELFTEST pass`, rc 0.
- **Needs:** a git repository; no clean tree, no registry.
- **Live measurement (read-only):**
  ```
  $ python3 plans/log_appendonly.py --lane .
  VIOLATION 3d9ea54a558b 2026-10-27 deleted=2 at=1407,1408 first="- Wave `a3w1` (34 re-dispatched wave-2 items): held-out hostile modules "
  VIOLATION 7864296ee02a 2026-10-28 deleted=1 at=1595 first="  after-measurement runs in a clean clone of the landing commit."
  VIOLATION 3cc5cecb6752 2026-11-04 deleted=2 at=2990,2991 first="  carries a stamp that recomputes at its own revision. Before: `receipts"
  LOG-APPENDONLY path=LOG.md head=12f1029a45cf
  LOG-APPENDONLY commits=141 violations=9
  [rc=1]
  ```
  A row for this gate must therefore declare a non-zero verdict (`1` = violations) as reachable;
  the tool is red at the tip by construction, not defectively.

### 1.2 `plans/round37_c1_attribution.py`

```
$ python3 plans/round37_c1_attribution.py --help   # rc 0
usage: round37_c1_attribution.py [-h] [--lane LANE] [--work WORK]

options:
  -h, --help   show this help message and exit
  --lane LANE
  --work WORK
```

- **Writes:** scratch only. `:62` `ref_gate.write_text(gate_src)` →
  `<work>/k37-attr-<rand>/gates/ref.py`; `:67` `mg.write_text(gate_src.replace(old,new,1))` →
  `<work>/k37-attr-<rand>/gates/<mid>.py`; fixtures under `<work>/k37-attr-<rand>/fx/fNNN`; the
  tree is removed in `finally` (`:85`). No lane write.
- **Verdict map:** `0` every mutant attributed; `1` at least one `UNATTRIBUTED`; `2` SETUP — only
  the one path at `:47-48` `SETUP gate not at its freeze digest`. Prints one
  `ATTR <mid> <clause> by=<fid>|UNATTRIBUTED -- <label>` per mutant and
  `ATTRIBUTED <n>/<total> UNATTRIBUTED=<m>`.
- **Defect worth knowing before writing the row:** `:52`
  `tempfile.mkdtemp(prefix="k37-attr-", dir=a.work)` is **not** wrapped in the try/except that maps
  setup errors to rc 2. A `--work` that does not exist raises through `main` and Python exits 1:
  ```
  $ python3 plans/round37_c1_attribution.py --lane . --work $S/r37      # $S/r37 absent
  File "…/plans/round37_c1_attribution.py", line 52, in main
      root = pathlib.Path(tempfile.mkdtemp(prefix="k37-attr-", dir=a.work))
  FileNotFoundError: [Errno 2] No such file or directory: '…/r37/k37-attr-_4grzv34'
  [rc=1]
  ```
  i.e. a caller error is indistinguishable by exit code from "unattributed". The row's verdict map
  should say so, or the gate entry should pass an existing `--work`.
- **Self-test:** none (no `--selftest` flag in `--help` or in the source).
- **Needs:** `plans/round37_c1_verify.py` at its `GATE_SHA256` digest; no clean tree; no registry.
- **Live measurement (read-only, after `mkdir -p $S/r37`):**
  ```
  $ python3 plans/round37_c1_attribution.py --lane . --work $S/r37
  … ATTR M55 D5 by=d5-m55-quote-absent -- d5 quote absent from the capture
  ATTRIBUTED 55/55 UNATTRIBUTED=0
  [rc=0]
  ```
  wall ≈ 14.7 s.

### 1.3 `plans/round66_registry_check.py`

```
$ python3 plans/round66_registry_check.py --help   # rc 0
usage: round66_registry_check.py [-h] [--root ROOT] [--selftest] [--work WORK]
                                 {quote,meta} ...

quote/meta checks over the kengaku registry and lesson Gates

positional arguments:
  {quote,meta}
    quote       check QUOTE lines against their captures
    meta        check teaches cells for frozen meta phrases

options:
  -h, --help    show this help message and exit
  --root ROOT   lane root (default: $KENGAKU_ROOT or the script's parent)
  --selftest
  --work WORK   scratch dir for --selftest
```

- **Writes:** scratch only, inside `cmd_selftest` (`:221` `tempfile.mkdtemp(dir=work, prefix="selftest-")`
  then `root/corpus/SOURCES.md`, `root/corpus/evidence/cap.txt`, and per-fixture lesson/registry
  files at `:225-278`). No lane write.
- **Verdict map:** `0` check passed; `1` check failed — prints `CHECK defect: …` lines then
  `CHECK … fail` (`:117-155`, `:186-211`); `2` SETUP (`SETUP <msg>` from `setup()` at `:60-61`:
  `--work required for --selftest`, `subcommand required: quote <lesson.md> or meta <SOURCES.md>
  [ids ...]`, plus `root_problem`). Success prints `QUOTE <sid> capture=… result=FOUND needle=…` /
  `CHECK quote quotes=<n> misses=<m>` + `CHECK ok quote`, or `CHECK meta rows=<n> findings=<n>
  teaches_column=<i>` + `CHECK ok meta`.
- **Self-test:** yes; **requires `--work`** (`:316-319` prints `SETUP --work required for
  --selftest` and returns 2 without it; it then `mkdir(parents=True, exist_ok=True)`s the dir).
  Prints one `SELFTEST {…}` dict line with 13 booleans; rc 0/1. Observed:
  `SELFTEST {'quote_pass': True, …, 'meta_missing_id': True}` all True, rc 0.
- **Needs:** the lane corpus. `quote` needs a lesson with `## Gate` QUOTE lines and captures under
  `corpus/evidence/` (refuses captures outside it, `:141`); `meta` needs the registry and its
  header row. No clean tree.
- **Live measurement (read-only):**
  ```
  $ python3 plans/round66_registry_check.py --root . meta corpus/SOURCES.md
  CHECK defect: meta S234 phrase='word bar' in teaches cell (line 250): "supersedes S230 — same source and capture, anchor quotes the grader's own f-string verbatim, teaches is one benefit within the word bar"
  CHECK defect: meta S234 phrase='teaches is one benefit' in teaches cell (line 250): …
  CHECK defect: meta S234 phrase='same source and capture' in teaches cell (line 250): …
  CHECK meta rows=253 findings=3 teaches_column=6
  CHECK meta fail
  [rc=1]
  ```
  The `meta` subcommand is **red at the tip on pre-existing bytes** (S234, corpus/SOURCES.md:250):
  the row must not claim `0` as the only verdict, and any C1 row quality claim of the form "the
  entry exits 0 at the tip" would be false for this subcommand.

### 1.4 `plans/round80_c1_remint.py` — **NOT RUN** (writes receipts and the ledger in the lane)

Only `--help` was executed; nothing else. This is deliberate: the script writes
`corpus/evidence/round80/<member>-probe.txt` (`:180`) and `plans/grader-population-ledger.json`
(`:181`) inside `--lane`.

```
$ python3 plans/round80_c1_remint.py --help       # rc 0
usage: round80_c1_remint.py [-h] --lane LANE [--work WORK] [--python PYTHON]
                            [--only ONLY]

options:
  -h, --help       show this help message and exit
  --lane LANE
  --work WORK
  --python PYTHON
  --only ONLY
```

- **Writes (source, `:175-181`):** first re-checks `git status --porcelain`; if clean, writes the
  staged receipts then `plans/grader-population-ledger.json` (`json.dumps(doc, indent=1) + "\n"`).
- **Verdict map:** `0` every chosen member minted (`minted == len(chosen)`, `failed == 0`, `:183`);
  `2` SETUP — dirty worktree (`:85-86` "run in a fresh clone"), unresolved HEAD (`:89-90`), dirty
  after the probe runs (`:175-178`, "nothing written"); `3` at least one probe failed or a ledger
  row is absent (`REMINT-FAIL …`, `:183`).
- **Self-test:** none.
- **Needs:** a **clean** worktree at a resolved HEAD, `plans/round80_probes.json`, and the ledger.

---

## 2. Support-module class from bytes (the two `UNCLASSIFIED` files)

### 2.1 `plans/fixture_fence.py` (991 lines, sha256 `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`)

```
$ grep -c "__main__\|argparse\|def main" plans/fixture_fence.py
0
[rc=1]
$ python3 - <<'EOF'   # AST
imports= ['os', 'pathlib', 're', 'stat'] argparse= False toplevel_main_guard= False
top-level names: Import×4, Assign×40, FunctionDef×26, _norm,_inside,_rel,_entries,_linked,_ref_name_ok,_read,
                 _argv,_tree,_sub_name_ok,_config_value,_config,_refs,_ref_tree,_objects,
                 _graph_dir,_alternates,_obj_info,_log_name_ok,_logs,_hooks,_info,_packed,
                 _store,_wt_store, breach
EOF
```
No `argparse`, no `__main__` block (no top-level `if` at all) — the frozen support-module test
holds on bytes. Importers (so the exclusion is not an opinion):
`plans/round45_c1_verify.py:110` and `plans/round46_c1_verify.py:217`
(`spec_from_file_location("fixture_fence_under_test", sys.argv[1])` / `--fence`),
`plans/round50_c1_verify.py:203` (`--fence` default `plans/fixture_fence.py`). Its presence in the
C1 universe comes from `SCORECARD.md` + `LOG.md` at BASE naming the path.

### 2.2 `plans/policy_cases.py` (85 lines, sha256 `8484aeaf8a798290e7710032acbd15a7859bddfd54ce37e1dbcea2449246e50c`)

```
$ grep -n "import\|__main__\|argparse" plans/policy_cases.py
NONE   (rc=1)
$ AST: imports= []  argparse= False  toplevel_main_guard= False  top-level names: [Assign]
```
Pure data module: one top-level `CASES = (...)` tuple of 59 `(policy id, case name, raw, expected)`
rows. Importer: `plans/parser_policy_compare.py:32` `import policy_cases  # noqa: E402`, exercised
at `:470` (`for pid, name, raw, expected in policy_cases.CASES`) and `:557`; referenced as a path by
`corpus/README.md:503`. Support-module class confirmed from bytes.

Both files are exactly the two names the freeze control expects to move from `UNCLASSIFIED` to
`EXCLUSIONS`; neither can be a registry row without inventing a CLI.

---

## 3. R82-C1 universe cross-check (independent derivation)

Derived from bytes, not from the round counter (`plans/round82_c1_plans_registry.py` does not exist
at the tip — `ls plans/round82*` prints only `plans/round82-sweep-map.json`):

```
plans/**/*.py at BASE outside plans/fixtures/:  295
referenced as a literal path by SCORECARD.md | LOG.md | corpus/README.md at BASE:  133
SKILL.md "## Gate/probe registry" at tip: 135 table lines = header + separator + 133 data rows
   (8 cells each; kinds: gate 103, probe 30)          [HEAD:SKILL.md; the worktree carried 137 rows
                                                       at 09:50Z from a concurrent seat's 4-row edit]
entry-cell `.py` references across the 133 rows: 138; absent at BASE: 0   (reverse direction clean)
union of both readings (entry-cell only / any cell): the same 6 gaps
```

```
MISSING 4:      plans/log_appendonly.py, plans/round37_c1_attribution.py,
                plans/round66_registry_check.py, plans/round80_c1_remint.py
UNCLASSIFIED 2: plans/fixture_fence.py, plans/policy_cases.py
```

This reproduces `corpus/evidence/round82/freeze-controls.txt` exactly (same six names, same
cli=yes/no split), and it was derived before that file was read. Target after the round:
`missing=0 unclassified=0 excluded=2 entry_missing=0 rows=133+4`.

---

## 4. R82-C3 — the 26 frozen map members: runnability recon

### 4.1 Map/ledger reconciliation

`plans/round82-sweep-map.json` has `schema r82-sweep-map/1`, `base a3a03ac…`, 26 members; the
ledger's `executed` set is exactly those 26 (`ledger members 88 executed 26`, `in ledger not map: []`,
`in map not executed: []`). All 26 instruments **exist at the tip and at BASE with identical bytes**,
and every one accepts the mapped flags (`--help` rc 0 for all 26; mapped `--flag`s missing from the
help text: none).

Two members are mapped without `--work` (`protein-assembly`, `regex-log`: `--lane` only) — both are
self-contained probes that use `tempfile` internally, so that is not a gap.

### 4.2 Per-member dependency matrix

`stdlib-only` = AST import scan against `sys.stdlib_module_names`; `bins` = absolute `/…/bin/<x>`
string constants in the script; `which` = literal `shutil.which("…")` arguments; `ports` = module
constants.

| member | instrument | stdlib-only | bins / which() | ports | host state / service | risk |
|---|---|---|---|---|---|---|
| build-pmars | `plans/build_pmars_probe.py` | yes | bwrap, gcc, python3 | – | gcc 16.2.1 ✔ | LOW |
| cancel-async-tasks | `plans/round61_c1_cancel_probe.py` | yes | bwrap, python3; lit `git` | – | git repo, signals | LOW |
| chess-best-move | `plans/round55_c3_chess_probe.py` | yes | bwrap, python3 | – | – | LOW |
| circuit-fibsqrt | `plans/fibsqrt_probe.py` | yes | bwrap, bash, gcc, python3 | – | gcc ✔ | LOW |
| configure-git-webserver | `plans/git_webserver_probe.py` | yes | bwrap, bash, `expect` | 8080, 8081 | `expect` **masked to /dev/null** by design (`:214-215`) | LOW |
| constraints-scheduling | `plans/constraints_probe.py` | yes | bwrap, bash, python3 | – | – | LOW |
| db-wal-recovery | `plans/db_wal_probe.py` | yes | bwrap, python3, sqlite3, xxd | – | sqlite3 ✔ xxd ✔ | LOW |
| distribution-search | `plans/round58_c2_kl_probe.py` | yes | bwrap, python3; lit `git` | – | sandbox grader needs numpy + pytest — both **stubbed/bound by the probe** (`:15-19`) | LOW |
| feal-differential-cryptanalysis | `plans/feal_probe.py` | yes | bwrap, bash, gcc, python, python3 | – | gcc ✔ | LOW |
| feal-linear-cryptanalysis | `plans/feal_linear_probe.py` | yes | bwrap, bash, gcc, python3 | – | gcc ✔ (the `pip install setuptools` at `:42` is a comment, not replayed) | LOW |
| git-leak-recovery | `plans/git_leak_probe.py` | yes | bwrap, git, python3 | – | git ✔ | LOW |
| hf-model-inference | `plans/round72_c1_hf_probe.py` | yes | bwrap, python3 | 5000 | host venv **`/fast/ComfyUI/.venv`** bound read-only; present, `python 3.13.16 torch 2.14.1+cu130 transformers 5.21.0 requests 2.34.2` | MED |
| kv-store-grpc | `plans/round64_c1_kvstore_probe.py` | yes | bwrap, python3; `which` `ss`, `uv` | 5328 | host-side `uv pip install grpcio grpcio-tools` (network); network UP, wheels already in `~/.cache/uv` | MED |
| largest-eigenval | `plans/round57_c2_eigen_probe.py` | yes | bwrap, python3 | – | numpy ✔, pytest stubbed by probe (`:14-17`) | LOW |
| log-summary-date-ranges | `plans/round81_log_summary_probe.py` | yes | bwrap, python3; lit `git` | – | git ✔ | LOW |
| nginx-request-logging | `plans/round70_c1_nginx_probe.py` | yes | bwrap, python3; lit `git` | 8080 | host **nginx absent** but the probe stages its own shim + stdlib HTTP server; flock lock `~/.local/share/kengaku-r70/port-8080.lock` (900 s) | MED |
| openssl-selfsigned-cert | `plans/round59_c1_openssl_probe.py` | yes | bwrap, python3; lit `git` | – | openssl ✔ (bound from host) | LOW |
| password-recovery | `plans/password_recovery_probe.py` | yes | bwrap, bash, dd, python3, strings, zip | – | all ✔ | LOW |
| polyglot-c-py | `plans/polyglot_c_py_probe.py` | yes | bwrap, bash, gcc, python3 | – | gcc/python3/bash ✔ (`/usr/bin/*` pinned) | LOW |
| protein-assembly | `plans/tb2_grader_probe.py` | **NO — `Bio`** | none | – | **Biopython absent** on this host | **HIGH** |
| pypi-server | `plans/round68_c1_pypi_finish.py` | yes | bwrap (via `round63` module constant) | 8080 | venv + local index; **writes three tracked files into the lane** (§0.1) | MED |
| regex-log | `plans/regex_log_probe.py` | yes | none | – | grader imports only `re`/`pathlib` | LOW |
| sqlite-with-gcov | `plans/round65_c1_sqlite_probe.py` | yes | bwrap, python3, sqlite3; `which` `ss` | – | gcc/gcov 16.2.1 ✔; amalgamation zip `.ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip` (2990966 B) is **tracked** in git ✔ | LOW |
| torch-pipeline-parallelism | `plans/round67_c1_pipeline_probe.py` | yes | bwrap | 12355 | venv `~/.local/share/kengaku-r67/venv-pipe` present: `3.14.8 torch 2.15.0+cpu transformers 5.22.1 pytest 9.2.0` | MED |
| torch-tensor-parallelism | `plans/round66_c1_tensor_probe.py` | yes | bwrap | 12355 | venv `~/.local/share/kengaku-r66/venv-torch` present, same versions | MED |
| vulnerable-secret | `plans/round81_vulnerable_secret_probe.py` | yes | bwrap, python3; lit `git` | – | git ✔ | LOW |

Notes that matter for the gate:
- `unshare-net` appears in 15 instruments: their sandbox has **no** network by design. The only
  members that touch the network are `kv-store-grpc` (host-side `uv pip install`, outside bwrap) and
  `pypi-server` (its own loopback index). `curl -sSI https://pypi.org/simple/` → `HTTP/2 200`, so
  kv's install can succeed; `~/.cache/uv` already holds `grpcio`/`grpcio-tools` wheels.
- Ports must be serialised: 8080 is claimed by **three** members (nginx, pypi, git-webserver, the
  last also 8081), 12355 by **both** torch members; 5000 (hf) and 5328 (kv) are distinct. At check
  time all five were free: `ss -ltn` showed only 1234, 5355, 18188, 631 listening.
- `nginx` and `expect` being absent on the host is **not** a blocker: nginx is shimmed by the probe,
  and `expect` is deliberately masked so the git-webserver case replays the container's behaviour.
- Observation-line shape: every one of the 26 prints at least one line the frozen projection keeps
  (`CASE `/`case=`/`TEST `/`VECTOR `/`LEG `/`regrade `); e.g. `protein-assembly` and `regex-log` print
  only `case=` lines, `torch-pipeline-parallelism` prints `VECTOR`.

### 4.3 Ranking — most likely to land `unrunnable`

1. **`protein-assembly` — certain, `unrunnable:1`.** `plans/tb2_grader_probe.py:145`
   `import Bio  # noqa: F401  (fail loudly if Biopython is absent)`, executed unconditionally in
   `main()` after the digest check; the loaded grader (`corpus/evidence/round35/tb2-eval/test_outputs.py:7`)
   is `from Bio.Seq import Seq`. `Bio` is absent (`python3 -c "import Bio"` → ModuleNotFoundError,
   rc 1) and the frozen argv is plain `python3` — the probe's own docstring prescribes
   `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`. The
   traceback exits 1 with **no** `case=` line → `unrunnable:1` under the frozen rule. This member
   cannot be `reproduced` without changing the map argv or installing Biopython.
2. **`nginx-request-logging` — MED.** Exclusive `flock` on `~/.local/share/kengaku-r70/port-8080.lock`
   with a 900 s acquisition timeout (`acquire_port_lock`, `:350-364`) and eight graded legs; a killed
   prior run leaves a lock held by a dead pid only if the fd survives — the timeout then becomes a
   `RuntimeError` → SETUP-class failure. Its `PORT` line is a live witness, so a busy 8080 is an
   outright setup failure, not a divergence.
3. **`pypi-server` — MED, and it is the only member that mutates the measured tree** (§0.1). It also
   binds 8080 with no lock, so it must not overlap nginx or git-webserver.
4. **`kv-store-grpc` — MED.** Needs host-side `uv pip install grpcio grpcio-tools` (network up,
   wheels cached), `bwrap`, `ss`, and 5328. Any one missing raises `SetupError` → rc 2 →
   `unrunnable:2`.
5. **`torch-tensor-parallelism` / `torch-pipeline-parallelism` — MED (runtime, not capability).**
   Both venvs exist with the exact pinned versions, but each runs a full torch grader inside bwrap on
   12355 — the two must be serialised, and a per-member timeout tuned for cheap probes will classify
   them `unrunnable` by timeout, not by defect.
6. **`hf-model-inference` — MED.** Nine cases under `bwrap --clearenv`; the host venv it binds is
   `torch 2.14.1 / transformers 5.21.0`, not the 2.15.0/5.22.1 the torch probes pin — if the receipt's
   stamped toolchain lines are compared byte-wise the member classifies `diverged`, which the claim
   must report rather than smooth.
7. Everything else — LOW: pure stdlib + bwrap + a host binary that is present, with no port and no
   external service. `sqlite-with-gcov` deserves one caveat: its amalgamation zip is only available
   because `.ufo/waves/round-65/w1/…zip` is **tracked** (`git ls-files --error-unmatch` succeeds), so
   a `--shared` clone gets it; a worktree-only copy would not.

### 4.4 What I could not break

- I could not find a member whose instrument is missing, unparsable, or that rejects its mapped
  argv — all 26 pass `--help` rc 0 with the mapped flags present.
- I could not find a second non-stdlib import beyond `Bio` by AST over the 26 instruments; the
  third-party modules that the *graders* import (`numpy`, `pytest`, `torch`, `transformers`, `grpc`,
  `requests`) are all supplied inside the sandboxes (probe-owned venvs, pytest stubs, or the
  read-only host venv), not by the probe process.
- I did not run the sweep, and did not run `round80_c1_remint.py` at all beyond `--help`; every
  claim above about a run's effect comes from source lines quoted with their numbers.

### 4.5 Open unknowns (not resolvable read-only)

- Whether `protein-assembly` is *intended* to be `unrunnable` in this round's receipt (a legitimate
  freshness datum) or whether the map should have carried `uv run --with biopython==1.85`. The
  frozen map is not mine to change; the gate must report the status either way.
- Real wall times per member are unmeasured (the receipts carry no `secs=`), so the per-member
  timeout budget for R82-C3 is a **guess** until the first `--run`.
- Whether the three modified `corpus/evidence/round68/pypi/*` files should be restored before the
  C3 receipt is cut — an L1 integration decision; I left them untouched.
