# S279 gate note (ScoutS279, round 90 wave 1)

Seat: leaf scout, read-only. No lane file was written; every mutation below was made in the
seat's scratch clone `lane/` and reverted (`git checkout -- corpus/SOURCES.md`) before exit.

Scratch: `S=/fast/scratch/hyaku/kengaku-r90/ScoutS279`, removed on exit (`trap 'rm -rf -- "$S"' EXIT`).

Clone used: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
`git -C "$S/lane" rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r90/ScoutS279/lane`
before any write into it; `git -C "$S/lane" rev-parse HEAD` printed
`a2b22609190f876f932a072b0d2c0b69a975afa0`.

No tool was installed or upgraded by this seat, so there is no install to record.

---

## 1. Fetch, sha256, byte-compare against the round-52 capture

Fetched once with curl, HTTP code and byte count recorded, sha256 taken, `cmp` run against the
lane capture.

```
$ cd /fast/scratch/hyaku/kengaku-r90/ScoutS279
$ URL='https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py'
$ curl -sS -o fetched_test_outputs.py -w 'HTTP=%{http_code} BYTES=%{size_download}\n' "$URL"
HTTP=200 BYTES=3034
curl exit rc=0

$ sha256sum fetched_test_outputs.py
2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149  fetched_test_outputs.py

$ sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py
2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py

$ cmp fetched_test_outputs.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py; echo "cmp rc=$?"
cmp rc=0
```

Observed: HTTP 200, 3034 bytes, curl exit 0; the fetched sha256 equals the lane capture's
sha256 and equals the sha256 the frozen claim names (`2754ba6c…85c149`); `cmp` returned 0, so the
bytes are identical. The fetched bytes were kept at `$S/fetched_test_outputs.py`.

## 2. Located quote (≤25 whitespace-split words)

The row's `teaches` cell grounds on the grader's five test functions over one graded state. The
quote is the 4-line span at lines 52-55 of the captured file, joined on whitespace: **17
whitespace-split words**, under the 25-word limit.

File: `corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py`
(the live URL at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` is byte-identical, per §1).

Quote (exact bytes of lines 52-55, joined):

```
def test_algo_map_function_with_test_input(): """Test that the map function works correctly with examples.json""" algo_path = Path("/app/repo/algo.py") test_path = Path("/tests/test.json")
```

Exact bytes of the span (`od -c`), showing the four lines and their indentation:

```
0000000   d   e   f       t   e   s   t   _   a   l   g   o   _   m   a
0000020   p   _   f   u   n   c   t   i   o   n   _   w   i   t   h   _
0000040   t   e   s   t   _   i   n   p   u   t   (   )   :  \n
0000060           "   "   "   T   e   s   t       t   h   a   t       t
0000100   h   e       m   a   p       f   u   n   c   t   i   o   n       w
0000120   o   r   k   s       c   o   r   r   e   c   t   l   y       w
0000140   i   t   h       e   x   a   m   p   l   e   s   .   j   s   o
0000160   n   "   "   "  \n                   a   l   g   o   _   p   a
0000200   t   h       =       P   a   t   h   (   "   /   a   p   p   /
0000220   r   e   p   o   /   a   l   g   o   .   p   y   "   )  \n
0000240                   t   e   s   t   _   p   a   t   h       =       P
0000260   a   t   h   (   "   /   t   e   s   t   s   /   t   e   s   t   .
0000300   j   s   o   n   "   )  \n
0000310
```

Line-number map of the captured file (each function's def line and its graded assertion):

| line | content |
|---|---|
| 10 | `def test_git_repo_init():` |
| 13 | `assert git_path.exists(), "Git repository does not exist in /app/repo"` |
| 16 | `def test_both_bundles_fetched():` |
| 21-24 | `result = subprocess.run(["git", "branch", "-a"], cwd="/app/repo", capture_output=True, text=True)` |
| 30 | `assert "branch1" in branches, "Branch1 from bundle1 not found in git history"` |
| 31 | `assert "branch2" in branches, "Branch2 from bundle2 not found in git history"` |
| 34 | `def test_algo_py_exists():` |
| 37 | `assert algo_path.exists(), "algo.py file does not exist in /app/repo"` |
| 40 | `def test_algo_py_has_map_function():` |
| 48 | `assert hasattr(algo_module, "map"), "algo.py does not contain a 'map' function"` |
| 49 | `assert callable(getattr(algo_module, "map")), "map attribute is not callable"` |
| 52 | `def test_algo_map_function_with_test_input():` (quoted span starts) |
| 82 | `assert a_val == e_val, (` (elementwise cell comparison; 5 whitespace-split words) |
| 85 | file end |

## 3. Offline-cleanliness from the captured bytes alone

Pattern sweep over the **captured grader bytes** (identical to the fetched bytes, §1):

```
$ grep -nE 'http|ssh|qemu|selenium|pdflatex|docker|requests|urllib|apt-get|pip install|load_dataset|download=True|curl -|wget -' fetched_test_outputs.py
(no stdout)
rc=1
```

Zero hits on all fifteen patterns. Per-pattern counts are all 0:

```
pattern [http] hits=0
pattern [ssh] hits=0
pattern [qemu] hits=0
pattern [selenium] hits=0
pattern [pdflatex] hits=0
pattern [docker] hits=0
pattern [requests] hits=0
pattern [urllib] hits=0
pattern [apt-get] hits=0
pattern [pip install] hits=0
pattern [load_dataset] hits=0
pattern [download=True] hits=0
pattern [curl -] hits=0
pattern [wget -] hits=0
```

The same sweep over the member's `tests/test.sh` in the same capture dir:

```
$ grep -nE 'http|ssh|qemu|selenium|pdflatex|docker|requests|urllib|apt-get|pip install|load_dataset|download=True|curl -|wget -' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh
4:apt-get update
5:apt-get install -y curl git
8:curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh
rc=0

$ wc -c fetched_test_outputs.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh
3034 fetched_test_outputs.py
 620 /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh
3654 total
rc=0
```

Every hit is **code, not prose**: line 4 and line 5 are `apt-get` shell commands (tool bootstrap),
line 8 is a piped `curl` installer (tool bootstrap plus one `http` substring inside the
`https://astral.sh` URL). No hit is a comment or a docstring. Nothing in either file mentions
`qemu`, `selenium`, `pdflatex`, `docker`, `requests`, `urllib`, `ssh`, `load_dataset`,
`download=True`, or `wget`.

**Conclusion: an offline replay of this member's grader needs neither network nor a VM.** The
graded state the grader reads is entirely local: a `/app/repo` directory (a `.git` directory, a
`repo/algo.py` file, and a `git branch -a` subprocess over the local repo) plus a `/tests/test.json`
file. The only subprocess the grader spawns is `git branch -a` (line 21-24) — a local binary
(`/usr/bin/git` present on this host, git 2.56.0), not a network call. The host sandbox the replay
needs is `bubblewrap` (`/usr/bin/bwrap`, bubblewrap 0.13.1), which is a namespace, not a VM.

Two host observations bearing on the replay (both measured here, not asserted):

- `bwrap --unshare-all …` works on this host: a replica of the probe's own `sandbox_argv` shape
  (ro-bind `/usr` and `/etc`, symlink `/bin` `/sbin` `/lib` `/lib64`, `--proc /proc --dev /dev`,
  bind `/app`, ro-bind `/tests/test.json`, `--clearenv`, `--chdir /app`, `python3 -I -B`) printed
  `PROBE-SHAPE-SANDBOX-OK {'input': [[1, 2]], 'output': [[2, 1]]}`, rc=0.
  `/proc/sys/user/max_user_namespaces` = `122865` and `/proc/sys/kernel/unprivileged_userns_clone` = `1`,
  so the namespace path is open right now. (The host guard notes a wave seat set
  `user.max_user_namespaces=0` on 2026-11-05 and broke every bwrap sandbox; the value read back
  here is non-zero, so that state is not currently in effect. This seat changed no sysctl.)
- The probe's `--ro-bind /usr /usr` plus symlinked `/lib` and `/lib64` is what makes
  `/usr/bin/python3` loadable inside the sandbox: with only `/usr` and `/etc` bound and no
  `/lib64` symlink, bwrap fails with `execvp /usr/bin/python3: No such file or directory`
  (rc=1). The probe already emits the `/lib64` symlink (`os.path.islink(link)` branch), so this
  is a note, not a defect.

## 4. Reject candidate — the member's `tests/test.sh` as a second source row

The candidate file was read in full (same capture dir as the grader):

```
$ cat -n /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh
     1	#!/bin/bash
     2	
     3	# Install curl and git
     4	apt-get update
     5	apt-get install -y curl git
     6	
     7	# Install uv
     8	curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh
     9	
    10	source $HOME/.local/bin/env
    11	
    12	# Check if we're in a valid working directory
    13	if [ "$PWD" = "/" ]; then
    14	    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    15	    exit 1
    16	fi
    17	
    18	uvx \
    19	  -p 3.13 \
    20	  -w pytest==8.4.1 \
    21	  -w pytest-json-ctrf==0.3.5 \
    22	  pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
    23	
    24	
    25	if [ $? -eq 0 ]; then
    26	  echo 1 > /logs/verifier/reward.txt
    27	else
    28	  echo 0 > /logs/verifier/reward.txt
    29	fi
rc=0
```

Graded-state tokens in the entry script versus in the grader:

```
$ grep -cE '\.git|algo\.py|test\.json|branch1|branch2' .../merge-diff-arc-agi-task/tests/test.sh
0
rc=1

$ grep -cE '\.git|algo\.py|test\.json|branch1|branch2' .../merge-diff-arc-agi-task/tests/test_outputs.py
12
rc=0
```

Distinctness against the already-registered per-task entry (S268's capture, `corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh`):

```
$ diff /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh .../merge-diff-arc-agi-task/tests/test.sh
3c3
< # Install curl
---
> # Install curl and git
5c5
< apt-get install -y curl
---
> apt-get install -y curl git
rc=1

$ sha256sum .../round82/fetch/log-summary-date-ranges_tests_test.sh .../merge-diff-arc-agi-task/tests/test.sh
4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334  .../round82/fetch/log-summary-date-ranges_tests_test.sh
c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2  .../merge-diff-arc-agi-task/tests/test.sh
rc=0
```

Shape counts across the 89 captured member entry scripts:

```
$ find .../round52/graders -name test.sh -exec sha256sum {} \; | grep -c 'c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2'
1
rc=0
$ find .../round52/graders -name test.sh -exec sha256sum {} \; | grep -c '4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334'
30
rc=0
$ find .../round52/graders -name test.sh | wc -l
89
rc=0
```

Also measured: 2 of the 89 entry scripts install `git` (this member and `sam-cell-seg`); 82 of the
89 use `uvx`.

**Decision: REJECT.** Grounded in the bytes above, not in the expected shape:

- The entry script carries **no acceptance predicate over the graded state**: zero occurrences of
  `.git`, `algo.py`, `test.json`, `branch1`, `branch2` against twelve in the sibling grader. It
  never names the repo, the module or the example file, so it adds no class, edge or vector to a
  replay that the already-captured `test_outputs.py` does not already carry.
- Its **only member-distinguishing byte** against the already-registered per-task entry is the
  added `git` package on line 5 (two lines differ from the 608-byte S268 capture; the rest is
  byte-identical). "Install git" is an environment-provisioning fact, not a grading fact.
- It **needs network** (`apt-get update`, `apt-get install`, a piped `curl` installer — §3), which
  is the opposite of the offline member-replay scope this row family holds.

**Flip condition:** a member whose entry script carries a member-specific graded assertion or
reward computation that is not present in its own `test_outputs.py` (for example an entry script
that computes the reward itself, or runs a grader file other than `/tests/test_outputs.py`).

Note on the two anchors: the rejected candidate's URL differs from S279's, so the census's
duplicate-URL rule (E04) does not fire; the row is recorded as `rejected` with the reason in its
`teaches` cell, in the same shape as the lane's existing rejected rows (S270, S276).

## 5. Drafted S279 row — the 11 cells

Cells below are the drafted text. Every cell is single-line, no cell contains a literal or escaped
pipe, and the row splits into exactly 11 cells.

| # | cell | value |
|---|---|---|
| 1 | id | `S279` |
| 2 | source | `Terminal-Bench 2.0 merge-diff-arc-agi-task pinned grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py` |
| 3 | kind | `code` |
| 4 | tier | `A` |
| 5 | scope | `member replay only: this pinned grader's five acceptance legs over a git repo plus algo.py plus /tests/test.json; not a solved-task, model or image claim` |
| 6 | anchor | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py@2fd12b88 lines 52-55, quote \`def test_algo_map_function_with_test_input(): """Test that the map function works correctly with examples.json""" algo_path = Path("/app/repo/algo.py") test_path = Path("/tests/test.json")\` (17 whitespace-split words over the 4-line span, lines joined); opened 2026-11-05; live HTTP 200, 3034 B, sha256 2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149 byte-identical to the round-52 capture corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py` |
| 7 | teaches | `five test functions over one graded state: repo .git exists at :13, branch1 and branch2 names appear in the git branch -a output at :21-31, algo.py is present at :37 and exposes a callable map at :48-49, and map reproduces each /tests/test.json example elementwise, asserted cell by cell at :82 \`assert a_val == e_val, (\`` |
| 8 | status | `mined` |
| 9 | opened | `2026-11-05` |
| 10 | recheck | `180d` |
| 11 | used-by | `corpus/lessons/round-90.md, plans/round-90-claims.md` |

Rendered as one Markdown row (this is the exact text proposed for `corpus/SOURCES.md`):

```
| S279 | Terminal-Bench 2.0 merge-diff-arc-agi-task pinned grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py | code | A | member replay only: this pinned grader's five acceptance legs over a git repo plus algo.py plus /tests/test.json; not a solved-task, model or image claim | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py@2fd12b88 lines 52-55, quote `def test_algo_map_function_with_test_input(): """Test that the map function works correctly with examples.json""" algo_path = Path("/app/repo/algo.py") test_path = Path("/tests/test.json")` (17 whitespace-split words over the 4-line span, lines joined); opened 2026-11-05; live HTTP 200, 3034 B, sha256 2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149 byte-identical to the round-52 capture corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py | five test functions over one graded state: repo .git exists at :13, branch1 and branch2 names appear in the git branch -a output at :21-31, algo.py is present at :37 and exposes a callable map at :48-49, and map reproduces each /tests/test.json example elementwise, asserted cell by cell at :82 `assert a_val == e_val, (` | mined | 2026-11-05 | 180d | corpus/lessons/round-90.md, plans/round-90-claims.md |
```

Drafted rejected row for the §4 candidate, same 11-cell shape:

```
| S280 | Terminal-Bench 2.0 merge-diff-arc-agi-task per-task grading entry, pinned tree 2fd12b88 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test.sh | code | A | member replay only: this member's harness entry script, for the reward write and the tool bootstrap it performs | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test.sh@2fd12b88 line 5, quote `apt-get install -y curl git` (5 whitespace-split words); opened 2026-11-05; live HTTP 200, 620 B, sha256 c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2 byte-identical to the round-52 capture corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh | REJECTED: the entry script carries no acceptance predicate over the graded state (zero occurrences of .git, algo.py, test.json or branch names against twelve in the sibling grader), so a replay gains no class, edge or vector the already-captured test_outputs.py lacks; its only member-distinguishing byte is the added git package on line 5, and it needs network (apt-get plus a piped curl installer), which the offline member-replay scope excludes; flip: a member whose entry script carries a member-specific graded assertion or reward computation not present in its test_outputs.py | rejected | 2026-11-05 | 180d | — |
```

### Machine checks on the two drafted rows (run in the scratch clone, then reverted)

```
$ python3 plans/anchor_digest_check.py --lane . | tail -1
rows=272 tokens=154 defects=51
rc=0

$ python3 plans/anchor_digest_check.py --lane . --verbose | grep -E 'S27[89]'
BIND S279 capture=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py by=row-path
BIND S280 capture=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh by=row-path
RESOLVED S279 digest=2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149 via=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py bind=row-path listed=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py
RESOLVED S280 digest=c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2 via=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh bind=row-path listed=corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh
rc=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin | grep -vE 'W04'
file	ok	/fast/scratch/hyaku/kengaku-r90/ScoutS279/lane/corpus/SOURCES.md
rc=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin | grep -E '^file'
file	rows	272
file	tier.A	242
file	tier.B	24
file	tier.C	6
file	status.mined	246
file	status.queued	8
file	status.rejected	18
rc=0
```

Baseline at the lane tip, same two tools, before the drafts: `rows=270 tokens=152 defects=51`;
census `rows 270, tier.A 240, status.mined 245, status.queued 8, status.rejected 17`.

Both drafted rows bind to their committed capture and resolve their own sha256 — the anchor cell
carries the lane capture path, which is what the binder needs, because the member has no committed
`task.toml` naming its slug (the `round52/graders/` tree has none, so the `url-task` route cannot
bind; the `row-path` route does). The four sibling rows S275–S278 fail that same binder today
(`anchor-unbound`, four of the 51 pre-existing defects) for exactly this reason; the draft above
does not repeat that defect.

Census E11 (`used-by` path missing on disk) fires for the `mined` S279 draft **only** until
`corpus/lessons/round-90.md` exists. That file does not exist at the lane tip today; the check
above was run with a one-line placeholder created in the scratch clone's
`corpus/lessons/round-90.md` and then deleted. If S279 is landed as `mined` in the same commit as
the round-90 lesson, E11 does not fire; if the lesson lands later, `queued` with `used-by —` is
the shape that passes immediately (measured: census rc=0, `status.queued` 8 → 9). Both variants
were checked:

```
variant queued + used-by —        : census validate rc=0, no S279 line; census counts rows 271, tier.A 241, status.queued 9, status.mined 245
variant mined  + used-by lesson+claim: census validate rc=1, "file E11 S279 missing used-by corpus/lessons/round-90.md" (placeholder lesson present -> rc=0)
```

That is a landing-order choice for the L1, not a defect in the row text.

## 6. Second reading of the landed rows (the lane moved while this seat worked)

The lane tip moved during this seat's work. When this seat began, `corpus/SOURCES.md` had 270 rows
and no S279; the tip was `a2b22609`. When this seat finished, the tip was `9cf98d90`
("round-90: S279 admit and S280 reject rows, round-90 lesson, routed-findings triage (34
resolutions) and 46 seed rows for rounds 83-89 (append-only)") and S279/S280 were already landed
by another seat. The round-90 lesson's `## Gate` now cites this seat's note as the second reading
of the same bytes. This seat therefore reports its §1-§5 as an **independent re-read of the landed
rows**, not as an unlanded proposal, and adds the discrepancies that re-read found.

### 6.1 The landed rows agree with this seat's evidence on every measured point

| point | landed rows | this seat's measurement | agree |
|---|---|---|---|
| S279 source URL and pin | `…/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py` | same URL, fetched once, HTTP 200, 3034 B | yes |
| S279 digest | `2754ba6c…85c149` | `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149`, `cmp` rc=0 against the capture | yes |
| S280 digest | `c9052954…ab8af8ab9d2` | `c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2`, `cmp` rc=0 against the capture | yes |
| S280 decision | reject, reason and flip present | reject (§4), from the same bytes | yes |
| offline need | none for the grader; the entry script needs apt/curl/uv over the network | §3, same pattern sweep, same three lines | yes |
| census at the tip | `validate` exit 0, `kengaku ok` | `validate` rc=0 on the tip tree | yes |

The landed S280 row's `kind` is `tool` and its scope cell reads "harness wrapper only: …"; the
lane's own `kind` enum includes `tool`, so the census accepts it.

### 6.2 Three discrepancies found in the landed rows (reported, not repaired)

**(a) The landed S279 and S280 rows add two new anchor defects (51 → 53).**
`python3 plans/anchor_digest_check.py --lane .` at the landed tip `9cf98d90` prints
`rows=272 tokens=154 defects=53`; at the pre-landing tip `a2b22609` the same command prints
`rows=270 tokens=152 defects=51` with no S279/S280 line at all. The two new defects are S279's
and S280's:

```
DEFECT S279 anchor token=2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149 class=digest-wrong-capture detail=committed-capture-belonging-to-another-capture-corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py-not-the-capture-this-row-names-corpus/evidence/round90/merge-diff-probe.txt loc=corpus/SOURCES.md:295
DEFECT S280 anchor token=c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2 class=anchor-unbound detail=no-capture-for-upstream-merge-diff-arc-agi-task/tests/test.sh-task=tests loc=corpus/SOURCES.md:296
```

`digest-wrong-capture` is **not** a new class at the tip — six older rows already carry it
(`S210`, `S211`, `S219`, `S228`, `S230`, `S232`); S279 is the seventh. What is new is that this
round's own source row lands in it. S280's `anchor-unbound` is the same shape as the four sibling
rows S275-S278 (§5).

Cause of S279's defect, read from the binder's own binding order: the landed S279 row's `used-by`
cell names `corpus/evidence/round90/merge-diff-probe.txt` (the round-90 receipt), and that is the
only `corpus/evidence/…` path anywhere in the row:

```
$ grep -nE '^\| S279 \|' corpus/SOURCES.md | grep -oE 'corpus/evidence/[A-Za-z0-9_./-]*[A-Za-z0-9_-]'
corpus/evidence/round90/merge-diff-probe.txt

$ grep -nE '^\| S280 \|' corpus/SOURCES.md | grep -oE 'corpus/evidence/[A-Za-z0-9_./-]*[A-Za-z0-9_-]'
(no output)
```

The binder's `row-path` route therefore binds S279 to the **receipt** (its digest is
`025119e2eb52b279052b85bd774f885ac77e902bb9f4ef400f453c7033728b3d`, not the grader's
`2754ba6c…`), while the row's anchor token is the **grader's** digest — hence
`digest-wrong-capture`. The upstream-URL route cannot save the row either: the member has no
committed `task.toml` naming its slug, so the `url-task` route never matches (the same reason the
four sibling rows S275-S278 are `anchor-unbound` at the tip). S280 has no `corpus/evidence/…` path
at all, so it falls to the upstream route and is `anchor-unbound` like its siblings.

Measured in the scratch clone, on the landed tip, three row shapes:

| S279 shape | anchor verdict |
|---|---|
| landed as-is (`used-by` names the receipt) | `digest-wrong-capture` (1 new defect) |
| anchor cell additionally names `corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py` | `capture-unanchored`: the row then names two captures and the single token resolves only one |
| `used-by` drops the receipt, anchor cell names the grader capture | `BIND … by=row-path` + `RESOLVED`, **0 new defects** |

The third shape is what this seat's §5 draft does, and the same substitution for both landed rows
takes the tip from `defects=53` back to `defects=51` (the pre-round baseline measured at BASE
`dcdd494e` and at `a2b22609`: `rows=270 tokens=152 defects=51`) with the census still exit 0.
This is a report, not a repair: `corpus/SOURCES.md` is outside this seat's write scope, and the
round's frozen text is not edited here.

**(b) The landed S279 quote word count is 12; `len(quote.split())` is 9.** The landed anchor cell
reads `test_outputs.py:13 quote \`assert git_path.exists(), "Git repository does not exist in
/app/repo"\` (12 whitespace-split words)`, and the round-90 lesson's Gate table repeats "line 13: …
(12 words)". Measured:

```
>>> len('assert git_path.exists(), "Git repository does not exist in /app/repo"'.split())
9
```

The lane's own counting convention is `len(quote.split())` — the round-87 sibling rows count 8 for
`assert lines[0].strip() == expected, "result.txt contains unexpected value"` (8 by that method),
and the lane has already filed one correction of exactly this kind (S272 claimed 6 words for the
`assert score > 6, …` quote; S273 supersedes it with the correct 9). The landed S279 count is
wrong by 3 in the same direction as the already-corrected S272 error. Both figures stay under the
25-word limit, so no gate turns on it; the number is simply not what it claims to be.

**(c) The lesson's S280 digest elision is malformed.** `corpus/lessons/round-90.md` writes the
S280 digest as `c9052954…ab8af8ab9d2`. The real digest ends `…3cc793af8ab9d2`; the written
elision repeats the substring `ab8af`, so it is not a suffix of the digest it abbreviates. The
full digest in the S280 row's own anchor cell is correct.

### 6.3 What this seat's independent read adds to the landed rows

The landed rows are sound on every point this seat was asked to check (fetch, byte-compare, located
quote, offline need, admit/reject decision and its reason). Two things in the landed S279 row are
worth the L1's attention beyond the anchor defect:

- The **located quote at line 13** grounds only the `.git` leg of the teaches cell; the teaches
  cell itself enumerates five legs at lines 10, 16, 34, 40 and 52. This seat's §5 draft anchors on
  the lines 52-55 span (17 whitespace-split words), which names the two graded inputs
  (`/app/repo/algo.py` and `/tests/test.json`) in one locator, and cites the other four legs by
  line number in the teaches cell.
- The landed S279 row's `used-by` cell names the round-90 receipt. That is what breaks the anchor
  binding; the §5 draft uses `corpus/lessons/round-90.md, plans/round-90-claims.md` instead, which
  also matches the frozen claims' wording ("used-by the round-90 lesson and the C1 claim").

Both shapes were measured on the landed tip in the scratch clone: census `validate` rc=0, and
anchor defects 53 → 51 with the §5 rows in place of the landed ones.

## 7. Notes for the L1 (frozen text reported, not repaired)

- The row and the lesson's `## Gate` are already landed at tip `9cf98d90` (§6). This seat's §1-§5
  is the independent re-read of those bytes; §6 lists the three discrepancies it found. The
  §5 draft is retained as the row shape that measures clean on the lane's own anchor checker.
- `plans/round-90-claims.md` says the row is opened "with the fetch + byte-compare + located quote
  recorded in the round lesson's `## Gate` before admission". The fetch (§1), the byte-compare
  (§1) and the located quote (§2) are recorded above and in the lesson's Gate table.
- The frozen claims say the row's status is `mined`, used-by "the round-90 lesson and the C1
  claim". The §5 draft uses `mined` with `used-by corpus/lessons/round-90.md, plans/round-90-claims.md`
  to match the claims' wording, and §5 records the `queued` fallback with its measured census
  effect. The claims file does not name `plans/round90_c1_replay.py` in the used-by list.
- The grader's five test functions, their file paths and their assertion lines were re-read
  directly from the captured bytes (§2 line map); every line number in the drafted `teaches` cell
  was taken from that map, not from the frozen case table. The landed row's teaches cell cites the
  same five def lines (10, 16, 34, 40, 52) and this seat confirms each against the bytes.
- The claims file's `R90-C1` honest limit (c) — "`test_both_bundles_fetched` greps branch *names*,
  so the cases prove name presence, never that a bundle was fetched" — is confirmed by the bytes:
  lines 30-31 assert on the *output* of `git branch -a` (line 21-24), never on bundle content. The
  drafted `teaches` cell says "branch1 and branch2 names appear in the git branch -a output",
  which is the same limitation, stated from the source.
- No lane file was modified by this seat. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin
  status --porcelain` after this seat's work shows only the untracked wave directories
  `.ufo/scopes/kengaku-r90-w1/` and `.ufo/waves/round-90/` (owned by the wave, including this
  seat's own file `.ufo/waves/round-90/w1/ScoutS279/gate-note.md`). The tip moved from
  `a2b22609` to `9cf98d90` during the seat's work by another seat's landing; this seat made no
  commit, no push, and no git or jj mutation of any kind.
- Scope check on this seat's own file: the note lives only under
  `.ufo/waves/round-90/w1/ScoutS279/`. Nothing in `plans/`, `corpus/`, `LOG.md`, `SCORECARD.md`,
  `SKILL.md`, `MANIFEST.json`, `.ufo/state/` or `.scratch/` was written.
