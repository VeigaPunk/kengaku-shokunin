# R40RegradeSweep — re-run stability across the five admitted TB2 graders

Seat: executor, round 40 wave 1 (kengaku hyaku run 9, 2026-10-26). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
read-only; all work under `/fast/scratch/hyaku/kengaku-r40/R40RegradeSweep` (deleted before finishing). Lane clone HEAD
`3077adbc7145726519f60f01426a5d03381ad444`, `git status --porcelain` empty. The five probe modules were copied byte-identical
from `plans/` (`copy_equal_lane=yes` for all five, `setup-and-pins.txt`).

Question (considerthese/2026-10-26.md proposal 3 rider, priced in `R39PlanNext.md` §4): does a grader return the same
verdict when it grades the **same state twice**, without the state being rebuilt? `polyglot-c-py` fails its second grading
because the grader writes `cmain` into the graded directory and then asserts on the directory listing
(`.ufo/waves/round-39/build/R39PlanNext.md:255-256`: "compiles `cmain` into the graded directory … then requires
`os.listdir == ['main.py.c']`").

## Method

For each of the five probes that pinned a TB2 grader (`tb2_grader_probe.py` protein-assembly, `regex_log_probe.py`
regex-log, `git_webserver_probe.py` configure-git-webserver, `build_pmars_probe.py` build-pmars, `git_leak_probe.py`
git-leak-recovery): take the oracle(-proxy) case and two failing cases, build that case's end state **once** with the
probe's own builders (`build_art`/`stage_app`, `prepare`, `components`+`build_cases`, or the probe's setup+recipe stage),
then invoke the grader **twice in two fresh processes** (fresh bwrap for the three sandboxed probes, two fresh
`importlib` loads for the two in-process probes) and compare the per-test letters (protein/regex: verdict + assertion
message). No rebuild, no state reset between the two gradings. The second grading therefore runs on whatever the first
grading left behind — that is the measured property.

`git-leak-recovery` was staged once (`challenge-setup.sh` + the case recipe) in one sandbox pass, then graded twice by a
grade-only harness bound over the same `/app`; the setup+recipe are **not** re-run. `configure-git-webserver` and
`build-pmars` keep the probe's own `prepare`/`stage_app` staging; only the server's `ready` handshake file is cleared
before each grading (it is written by the probe's server harness, not the graded state).

Harness: `R40RegradeSweep/sweep.py` (copied). Graded-state manifests hash every path, mode, size, content and symlink
target before/after each grading; `MUT` = added/removed/content-changed, `TOUCH` = identical content rewritten.

### Commands (exact)

```bash
S=/fast/scratch/hyaku/kengaku-r40/R40RegradeSweep
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
for f in tb2_grader_probe regex_log_probe git_webserver_probe build_pmars_probe git_leak_probe; do
  cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/$f.py "$S/probes/"; done

cd "$S" && export TMPDIR="$S"
uv run --no-project --with biopython==1.85 python3 sweep.py --lane ./lane --work ./full1 --probes ./probes > sweep-run1.txt
uv run --no-project --with biopython==1.85 python3 sweep.py --lane ./lane --work ./full2 --probes ./probes > sweep-run2.txt
sed -E 's/[0-9a-f]{40}/<oid>/g' sweep-run1.txt > n1.txt; sed -E 's/[0-9a-f]{40}/<oid>/g' sweep-run2.txt > n2.txt
cmp n1.txt n2.txt            # byte-equal: only git object ids differ between the two runs

# probe baselines, each run twice and cmp'd
uv run --no-project --with biopython==1.85 python3 probes/tb2_grader_probe.py --lane ./lane
python3 probes/regex_log_probe.py --lane ./lane
python3 probes/git_webserver_probe.py --lane ./lane --work "$PWD/pw"
python3 probes/build_pmars_probe.py --lane ./lane --work "$PWD/pw"
python3 probes/git_leak_probe.py --lane ./lane --work "$PWD/pw"

# per-task sweep filter (used for the smoke runs): append --only protein|regex|cgw|bpm|glr
```

Recorder output: `TOTAL cases=15 regrade_diff=0` (`sweep-run1.txt`). The sweep was run twice into fresh work dirs;
`sweep-run1.txt` and `sweep-run2.txt` differ only in one 40-hex git object id (below), and are byte-equal after redaction
(`n1.txt` = `n2.txt`, sha256 `71d9f734…`).

## Per-task results

`grade1`/`grade2` are the case verdicts (sandboxed probes: per-test letters); `regrade` compares the two gradings.

| task (pin) | grader | case | role | grade1 | grade2 | regrade | graded state after grade 1 |
|---|---|---|---|---|---|---|---|
| protein-assembly (r35) | `tb2-eval/test_outputs.py` | `valid-balanced` | oracle-equivalent | pass | pass | same | unchanged |
| | | `stop-codon-appended` | fail | fail | fail | same | unchanged |
| | | `donor-one-substitution` | fail | fail | fail | same | unchanged |
| regex-log (r36) | `tb2-regex-log/test_outputs.py` | `reference-month-aware` | oracle-equivalent | pass | pass | same | unchanged |
| | | `first-date-only` | fail | fail | fail | same | unchanged |
| | | `extra-capture-group` | fail | fail | fail | same | unchanged |
| configure-git-webserver (r37) | `tb2-git-webserver/test_outputs.py` → `verify.sh` | `static-file-no-git` | oracle proxy | pass | pass | same | **MUT** `cwd/git_test.exp`, `home/.ssh/config` |
| | | `no-server` | fail | fail | fail | same | **MUT** `cwd/git_test.exp`, `home/.ssh/config` |
| | | `capitalised` | fail | fail | fail | same | **MUT** `cwd/git_test.exp`, `home/.ssh/config` |
| build-pmars (r38) | `tb2-build-pmars/test_outputs.py` | `canned-shape` | oracle proxy | PPPP | PPPP | same | unchanged |
| | | `canned-script` | fail | PFPP | PFPP | same | unchanged |
| | | `nonexec-binary` | fail | FPPP | FPPP | same | unchanged |
| git-leak-recovery (r39) | `tb2-git-leak-recovery/test_outputs.py` | `oracle-solve-sh` | **real solve.sh** | PPPPP | PPPPP | same | unchanged |
| | | `untouched` | fail | FPPPP | FPPPP | same | **MUT** `repo/.git/lost-found/commit/<oid>` |
| | | `dangling-secret-blob` | fail | PPPFP | PPPFP | same | **MUT** `repo/.git/lost-found/other/<oid>` |

Totals: **15/15 cases `regrade=same`, 0 DIFF**; 30 gradings in the sweep. Each case's `grade1` equals the verdict the
probe itself observes for that case in its own committed receipt (`p_*1.txt`), so the "build once" state is the state the
probe builds.

Oracle fidelity, stated because it bounds the claim: only `git-leak-recovery` executes the task's real `solve.sh`
(`oracle-solve-sh`). `build-pmars` and `configure-git-webserver` do **not** run `solve.sh` (root/apt/network; the
build-pmars docstring says so), so their "oracle" cases are the probes' passing proxies (`canned-shape`,
`static-file-no-git`). `protein-assembly`'s `valid-balanced` is built from the grader's own literals, and the regex case
mirrors the month-aware body of `solve.sh` rather than its literal bytes.

## Which graders mutate the graded state

Two of five; cgw mutates on all three selected cases, glr on the two failing cases (its oracle case already holds the
lost-found files), and neither mutation is visible to the grader's own assertions:

1. **configure-git-webserver** — the grader runs `bash /tests/verify.sh`
   (`corpus/evidence/round37/tb2-git-webserver/test_outputs.py:11`), and `verify.sh` writes unconditionally before it
   tests anything: `cat > git_test.exp` in the working directory (`verify.sh:16`), `mkdir -p ~/.ssh` and the
   `~/.ssh/config` redirect (`verify.sh:9-12`), plus `wget -q -O test_output.html` on the wget branch (`verify.sh:75`). The
   sweep's cwd (`/work/cwd`) stands for the task's working directory, so `git_test.exp` is the closest analogue here to
   the `polyglot-c-py` compile-into-cwd shape. The assertion is only `"TEST PASSED" in result.stdout`
   (`test_outputs.py:13`), so the extra file cannot change the verdict; the second grading rewrites it (TOUCH) and still
   passes/fails identically.

2. **git-leak-recovery** — `test_no_secrets_in_unreachable_objects` runs `git fsck --lost-found`
   (`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py:69`), and `--lost-found` writes every dangling
   object into `.git/lost-found/` **inside the graded repository**. The other test's checksum skips dot paths
   (`find /app/repo -type f -not -path '*/\.*'`, `test_outputs.py:101`), so the grader's own writes are invisible to it;
   the verdict is unchanged on the second pass. `oracle-solve-sh` already ran `git fsck --lost-found` in `solve.sh`, so
   its post-grade manifest is unchanged (the files exist before the first grading).

Three of five do not mutate the graded state: `protein-assembly` and `regex-log` only read
`/app/gblock.txt` / `/app/regex.txt` (their probes grade a file created outside the grader); `build-pmars` binds `/app`,
`/usr/local/bin` and `/usr/local/sbin` read-only in the probe sandbox, and its grader only runs `pmars`, `ldd` and
`Path` queries (`test_outputs.py:19-84`), so it has no compile-into-cwd shape. The nearest thing to the polyglot failure
mode among the five is cgw's `git_test.exp`; none of the five flips a verdict.

Static-scan blind spot: none of the five `test_outputs.py` files contains a write call (`write_text|open(...,'w')|mkdir`
→ 0/5); the writes in cgw and glr live in the shell script and in the `git` command the Python test invokes. The
R39PlanNext's static heuristic ("graders with a compile / build / write call (static, heuristic)", 27 of 89;
`.ufo/waves/round-39/build/R39PlanNext.md:161`) therefore cannot see either mutation class from `test_outputs.py` alone.

## State construction is not reproducible; grading still is

The two full sweep runs differ in exactly one field: the dangling commit id written by `git fsck --lost-found` for
`glr/untouched` (`4849eddf…` vs `600b2f76…`). Cause, controlled: `challenge-setup.sh` commits with the wall clock, so the
initial repository's object ids depend on the build second. Two builds 2 s apart: secret-commit ids
`430712db…` vs `c8125c5e…`, equal=no, while the worktree files are identical (`sha256sum` manifests cmp-equal); two builds
with `GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=2026-01-01T00:00:00+0000` are equal (`setup-and-pins.txt`). This is a
*state-construction* flake, not a grading flake: within one build, both gradings see the same ids and agree. The probes'
byte-equal receipts did not surface it because probe receipts print verdicts, never object ids.

## Probe baselines (coverage)

Each probe was run twice against the clone; all ten outputs byte-equal (`*_BYTE_EQUAL`), matching the committed
mismatch-free receipts:

| probe | cases | pass | fail | mismatches | two runs |
|---|---|---|---|---|---|
| protein-assembly | 18 | 5 | 13 | 0 | byte-equal |
| regex-log | 24 | 8 | 16 | 0 | byte-equal |
| configure-git-webserver | 22 | 9 | 13 | 0 | byte-equal |
| build-pmars | 22 | 7 | 15 | 0 | byte-equal |
| git-leak-recovery | 25 | 13 | 12 | 0 | byte-equal |

111 probe gradings × 2 + 30 sweep gradings = 252 executed gradings; the stability measurement proper is 15 pairs.
All capture digests the probes pin were verified in-run (`setup-and-pins.txt`).

## Novelty / coverage framing

- **Measured flake rate, not prose**: 0/15 case-level verdict differences across five graders, with per-test letters
  compared (not just exit codes), on a state the first grading may have touched. The prior art priced in §4 was one
  task (`polyglot-c-py`); this is a five-grader sweep with a class histogram of graded state.
- **Mutation class histogram**: read-only Python (protein, regex), read-only sandbox with subprocess (bpm), shell
  verifier that writes helper files into cwd/HOME (cgw), VCS command with a writing side effect inside the graded repo
  (glr). Two of five mutate; both do so on every run; neither mutation reaches a verdict. This is a sharper statement
  than the `27 of 89` static-scan count: the writes are in invoked shell code, and a dot-path-skipping checksum
  can hide a VCS-side write from the grader itself.
- **Separate stability axis**: for glr the graded initial state is not bit-reproducible (wall-clock commit ids), which
  byte-equal verdict receipts conceal. Any future "state digest" claim for that task must pin commit dates.
- Coverage cost: 15 built states + 30 gradings, ~14 s per full sweep (two sweeps incl. repeated probe baselines ran in
  28.6 s); the same harness runs from the lane's probes unmodified (no lane edits).

## Limits / risks

- Four of five "oracle" cases are proxies, not `solve.sh` executions (above). The stability result is about the states
  the probes build, not about the TB2 oracle containers.
- The second grading is a fresh process (stronger than db-wal's in-process second call). A same-process repeat could
  differ for graders holding module-level state; none of the five does.
- cgw's mutation includes `~/.ssh/config`, which in TB2 lives in `HOME` (`/root`), outside `/app`; only
  `git_test.exp` is inside the probe's graded cwd. `ready` is the probe's server handshake, excluded from the claim.
- `git fsck --lost-found` rewrites its files on each pass (mtime TOUCH, identical content); the manifest treats that as
  TOUCH, not MUT.
- Wall clock dependence was demonstrated for glr's setup only; other setups (`challenge-setup.sh` variants) were not
  audited for the same defect.

## Retained evidence (`R40RegradeSweep/`)

- `sweep.py` — harness (build-once, grade-twice, manifests, fresh-process second grade).
- `sweep-run1.txt` (sha256 `a5ea94bd…`), `sweep-run2.txt` (`00bafd35…`), `n1.txt` = `n2.txt` (`71d9f734…`, redacted).
- `p_{protein,regex,cgw,bpm,glr}{1,2}.txt` — ten probe runs, byte-equal pairs.
- `setup-and-pins.txt` — lane HEAD, probe-copy equality, capture pins, state-reproducibility control.
- Scratch `/fast/scratch/hyaku/kengaku-r40/R40RegradeSweep` removed after copying.

VERDICT: regrade-sweep-5-diff-0
