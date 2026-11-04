# SourcesScribeR81 — round-81 SOURCES rows and frontier evidence (scribe seat)

Role: scribe (leaf; no subagent dispatch). Report path per seat spec:
`.ufo/waves/round-81/w1/SourcesScribeR81.md`.

Measured at lane tip `e83963f895e42992573ff47c769d1ac86cb15363` (advanced during this
wave from `ca9bfe79`; re-measured and all digests re-verified at the new tip).
Frozen claims read in full first: `plans/round-81-claims.md`
(freeze commit `4d896e0daf8831ef7a0016bf3c944d11ba465f70`, untouched — I did not
re-open any frozen predicate; base revision `4e833e9fee8022d24559535178c6fe32b2cd62f1`).
Worktree clean at measurement; no mutating git/jj run anywhere by this seat; no
lane file written (all writes: this report + my scratch, scratch deleted before yield).

Time box: L1 (`KengakuR81`) requested wrap-up mid-seat; the fetches below were all
completed before the box. No fetch was started after it.

## 1. Contract opened (with commands)

- `corpus/SOURCES.md` header lines 1-30: contract v1 tiers (A/B/C; `community` never A;
  tier scoped to `scope`), registry table of **11 columns**
  (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`),
  status enum `queued|mined|rejected`; "A row is a claim made only after opening the source
  in this round".
- S255-S258 rows read raw (commands:
  `grep -n 'S25[5-8]' corpus/SOURCES.md`, `sed -n '274p' corpus/SOURCES.md`):
  S258's anchor pins "lines 1-10 (subject at line 1, stamp at 3-10)" and six
  pre-A3 digests `7923b6dc…, b32f4b37…, fd337d12…, 9179d62d…, 08c10b0d…, 82b910af…`.
- Census contract: fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:64-150` — append-only,
  "A correction is a new row whose `teaches` opens `supersedes S0NN —`", census
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` + NF=13 malformed-row check +
  mined-used-by-exists check.
- `corpus/QUALITY.md` Q2 (tier floor, lines 24-30) and Q4 (negative space, lines 36-41),
  read at lines 24-42.

## 2. Row A — S259 (R80-U1 repair): six receipt anchors + stamp range

Deliverable check: `.ufo/waves/round-81/w1/r80-u1-anchors.txt` — **absent at both polls**
(`ls .ufo/waves/round-81/w1/r80-u1-anchors.txt` → `No such file or directory`, run twice
during the seat). Fallback taken: computed the anchors myself with `sha256sum`.

Command (run at the measured tip, receipts committed and clean):

```
$ sha256sum corpus/evidence/round80/*-probe.txt
11a53bf39f9b51ba642e807e53931bdc1911b9a9dd148475cd2da47640a03358  corpus/evidence/round80/cancel-async-tasks-probe.txt
1a3d4e1ba4f34102645e238f552192576d6e0265fd6ca60857e3254a58504ef8  corpus/evidence/round80/chess-best-move-probe.txt
afef9380a3537ca52eaa131aafb3d96af7b90dd2b3affd05e75d94db54d4cc0a  corpus/evidence/round80/distribution-search-probe.txt
f60bc00bb91b1355c4a078d5bd1aa18c5c345257932b09c2781a9945c417292a  corpus/evidence/round80/largest-eigenval-probe.txt
b7e66f4cc79aacd8b4d94630a5e20ff7c74899ac22a601f0983ef4feb5068df6  corpus/evidence/round80/openssl-selfsigned-cert-probe.txt
778565cd7693102f0a63e58cb37bd18a157c055895f07ab87eeac73df2ef327f  corpus/evidence/round80/protein-assembly-probe.txt
```

All six first-8 prefixes match the spot-check's committed expectation verbatim
(`corpus/lessons/round-80-verifier-spotcheck.md:157`: "the committed receipts
(`446b157f` → tip) hash `11a53bf3…, 1a3d4e1b…, afef9380…, f60bc00b…, b7e66f4c…,
778565cd…`"). Zero overlap with S258's stale list — the U1 defect is real and
reproduced from bytes.

Stamp range, read from bytes (`cat -n corpus/evidence/round80/cancel-async-tasks-probe.txt |
sed -n '1,13p'` and re-verified on `largest-eigenval-probe.txt`): line 1 subject
(`# tb2 … grader probe (round 80 re-mint)`), line 2 `MEMBER`, stamp block lines **3-12**
(`SOURCE_RECEIPT` 3, `SOURCE_SHA` 4, `TOOL` 5, `TOOL_SHA` 6, `LANE_TIP` 7, `WORKTREE` 8,
`COMMAND` 9, `EXIT` 10, `MINTED_BY` 11, `MINTED_BY_SHA` 12), `OBSERVATIONS_BEGIN` at 13.
This is the spot-check's mandated `lines 3-12` range; the A3 amendment added the
`MINTED_BY`/`MINTED_BY_SHA` lines (11-12).

## 3. Row B — S260 (own-work): round-81 located-replay instrument set

Opened from bytes at the tip:
- `plans/round81_probes.json` (790 bytes; sha256 `4c460745dabac0fd298778966139edcaa4de84c14e4fa7beec42796fb94a73a1`) — frozen probe table, schema `r81-probes/1`, two members with tool/argv/timeout.
- `plans/round81_log_summary_probe.py` (sha256 `a983909ac505374643f15ca8cca807a6799a71a70e72b8bda517268cbde9a046`) — docstring: offline bubblewrap replay of the committed round-52 capture, derived `violates=` predictions.
- `plans/round81_vulnerable_secret_probe.py` (sha256 `209b28bcd0a5060da41d9f44f8eaf56e5c19956a1370b9408695362812990dca`) — same shape for `results.txt`.
- `plans/round81_c1_new_members.py` (sha256 `f447f81dd802404c2f56f51dcc4dda2141666e2d6039190360f6e8fbdd1c98f8`) — frozen counter docstring (universe derivation, receipt form, controls).
- Receipts (tracked at tip): `corpus/evidence/round81/log-summary-date-ranges-probe.txt`
  (sha256 `7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78`) and
  `corpus/evidence/round81/vulnerable-secret-probe.txt`
  (sha256 `f632e115f965ff722547ffbad64d84938ef6f5476565699369f3bfb6d19b90cd`); first line
  of each read from bytes: `# tb2 log-summary-date-ranges grader probe (round 81)` /
  `# tb2 vulnerable-secret grader probe (round 81)`; stamp block lines 3-14
  (adds `HOST_PYTHON Python 3.14.8`, `HOST_OPENSSL OpenSSL 3.6.5 29 Sep 2026`),
  `LANE_TIP 4ac8471b15a40cddc16e1c5cccbde2a087f12117`, `WORKTREE clean`, `EXIT 0`.
- Ledger rows read: `plans/grader-population-ledger.json` both members now
  `status=executed round=81 receipt=<member>-probe.txt subject=tb2-header verdict=predicate`.

Located quote (from the receipts' first line, 9 words):
“# tb2 log-summary-date-ranges grader probe (round 81)”
(`corpus/evidence/round81/log-summary-date-ranges-probe.txt:1`).

## 4. Row C — S261 (external primary, pinned tree 2fd12b88): opened and recorded

Access date 2026-11-04. All fetches via `curl -sS` into my scratch (now deleted);
HTTP statuses, byte counts and sha256 recorded below.

- README at the pinned tree:
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md`
  → **HTTP 200, 4574 bytes**, sha256 `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364`
  — byte-identical to the lane's committed round-79 capture
  `corpus/evidence/round79/sources/tb2-readme.md` (same digest), so the pinned tree is
  unchanged since S256 and quotes anchor to the committed capture's lines.
  Located quote (committed capture `:24`, 21 words): “Terminal-Bench is a popular
  benchmark for measuring the capabilities of agents and language models to perform
  valuable work in containerized environments.”
- Task directories: the seat's guessed paths `tasks/log-summary-date-ranges/` and
  `tasks/vulnerable-secret/` returned **HTTP 404** (GitHub API, pinned ref) — reported
  as failed fetches, not guessed over. Repo-root listing at the pinned ref
  (`https://api.github.com/repos/harbor-framework/terminal-bench-2/contents/?ref=2fd12b88…`)
  → HTTP 200 and shows both tasks at the **repo root** (`log-summary-date-ranges/`,
  `vulnerable-secret/`). Corrected real URLs opened, all HTTP 200:
  - `…/2fd12b88…/log-summary-date-ranges/instruction.md` — 1391 bytes, sha256 `c1d4516ad4ec…`; quote (`:9`, with `:10`): “Write a CSV file /app/summary.csv with the following structure (including the header): period,severity,count” (13 words).
  - `…/log-summary-date-ranges/task.toml` — 988 bytes, sha256 `9a9593673d68…`.
  - `…/log-summary-date-ranges/README.md` — 1858 bytes, sha256 `026000415cb5…`.
  - `…/log-summary-date-ranges/tests/test_outputs.py` — 1655 bytes, sha256 `2fc06a6ce194…` — **byte-identical to the committed round-52 capture** `corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py` (same digest).
  - `…/log-summary-date-ranges/tests/test.sh` — 608 bytes, sha256 `4770437ea96c…` (grader class: `pytest … /tests/test_outputs.py`, `reward.txt` 1 iff pytest exits 0).
  - `…/vulnerable-secret/instruction.md` — 432 bytes, sha256 `d43c72e6c39c…`; quote (`:7`, 18 words): “The task is complete when you have successfully extracted the secret key and written it to /app/results.txt.”
  - `…/vulnerable-secret/task.toml` — 925 bytes, sha256 `51079626e4c7…`.
  - `…/vulnerable-secret/README.md` — 1510 bytes, sha256 `b07cb59309e8…`.
  - `…/vulnerable-secret/tests/test_outputs.py` — 1346 bytes, sha256 `f2b65f63ac81…` — **byte-identical to the committed round-52 capture** (same digest).
  - `…/vulnerable-secret/tests/test.sh` — 778 bytes, sha256 `d9e46bae71e0…`.

The two remote `test_outputs.py` files matching the committed round-52 captures
externally corroborates the receipts' `SUBJECT_SHA` pins and the probes' docstring claim
of pinned-tree byte-identity. The grader class of both members is grounded at the pinned
tree: single-artifact end states (`/app/summary.csv` CSV schema, `/app/results.txt`
`FLAG{…}`) graded by one pytest file.

## 5. Draft rows (for the L1; do NOT append from this seat)

```
| S259 | kengaku round-80 located replay receipts, re-anchored — corpus/evidence/round80/<member>-probe.txt (six), plans/round80_c1_located_replay.py | own-work | A | the six members the R79 ledger priced executed-unlocated, at their current stamped bytes (the R80-U1 repair) | sha256sum corpus/evidence/round80/*-probe.txt at tip e83963f8 → 11a53bf39f9b…, 1a3d4e1ba4f3…, afef9380a353…, f60bc00bb91b…, b7e66f4cc79a…, 778565cd7693…; stamp range lines 3-12 (subject at line 1, MEMBER at 2, MINTED_BY_SHA at 12) | supersedes S258 — the A3 driver re-minted the receipts, so the anchor's pre-amendment digests and its "lines 1-10 (stamp at 3-10)" range are replaced by these bytes and lines 3-12; quote "# tb2 cancel-async-tasks grader probe (round 80 re-mint)" (cancel-async-tasks-probe.txt:1, 12 words) | mined | 2026-11-04 | 90d | corpus/lessons/round-81.md |
| S260 | kengaku round-81 located replays — plans/round81_log_summary_probe.py, plans/round81_vulnerable_secret_probe.py, plans/round81_probes.json, plans/round81_c1_new_members.py, corpus/evidence/round81/<member>-probe.txt (two) | own-work | A | the two unattempted stdlib-only file-artifact population members the frozen selection rule derives at the base revision, replayed offline with a pinned subject capture and a pinned replay environment | corpus/evidence/round81/log-summary-date-ranges-probe.txt lines 1-14 (subject at 1, stamp 3-14 with HOST_PYTHON/HOST_OPENSSL, observations from 15); receipt sha256 7c8d3f5656ed…, f632e115f965…; instrument sha256 a983909ac505…, 209b28bcd0a5…; table sha256 4c460745daba…; counter sha256 f447f81dd802… | a located replay pins its subject capture, tool, and host stack, and its observation block re-runs at the measured tip; quote "# tb2 log-summary-date-ranges grader probe (round 81)" (log-summary-date-ranges-probe.txt:1, 9 words) | mined | 2026-11-04 | 90d | corpus/knowledge/tb2-file-artifact-replay-classes.md |
| S261 | Terminal-Bench 2.0 task documents at pinned tree 2fd12b88 — log-summary-date-ranges/instruction.md, task.toml, tests/ and vulnerable-secret/instruction.md, task.toml, tests/ — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/ | docs | A | what the two replayed tasks ask the agent to produce and how the grader scores it, at the pinned revision the round-52 captures came from | instruction.md:9-10 "Write a CSV file /app/summary.csv with the following structure (including the header): period,severity,count" (13 words); vulnerable-secret/instruction.md:7 "The task is complete when you have successfully extracted the secret key and written it to /app/results.txt." (18 words); both tests/test_outputs.py fetched 2026-11-04 HTTP 200, byte-identical to corpus/evidence/round52/graders/<member>/tests/test_outputs.py (2fc06a6ce194…, f2b65f63ac81…) | the graded end state of both members is a single artifact file with a fixed schema, graded by one pytest file that writes reward 1 iff pytest exits 0 — the file-artifact class R81-C1 replays offline | mined | 2026-11-04 | 90d | corpus/lessons/round-81.md |
```

Status note: drafted `mined` because both planned used-by paths exist at the tip
(`corpus/lessons/round-81.md` 9225 bytes, `corpus/knowledge/tb2-file-artifact-replay-classes.md`
4791 bytes, committed in `51b824c6`). If the L1 integrates before those paths land in a
given tree, integrate as `queued` and flip per contract rule 2.

## 6. Comparison with the already-integrated rows (corroboration, calibration)

While this seat worked, the L1 landed `51b824c6 round-81: lesson, knowledge entry,
SOURCES S259-S261, routed-findings R80-U1..U6, index rows, C1 after receipt`; the
integrated rows sit at `corpus/SOURCES.md:275-277` (registry total now 253 rows).
This seat wrote nothing to `corpus/SOURCES.md`; comparison against my independent draft:

- **S259 digests agree exactly**: integrated anchor's six prefixes
  (`11a53bf39f9b…, 1a3d4e1ba4f3…, afef9380a353…, f60bc00bb91b…, b7e66f4cc79a…, 778565cd7693…`)
  == my full-sha256 first-8s. Framing difference, verbatim: integrated anchor says
  "lines 2-12 (stamp block; protein-assembly's divergence note at 13)"; my byte read
  and the spot-check's mandated text say **lines 3-12** (line 2 is `MEMBER`, outside the
  stamp key/value block). Six-for-six digests identical; range framing differs by the
  MEMBER line.
- **S260 agrees**: integrated quote “# tb2 log-summary-date-ranges grader probe (round 81)”
  (line 1) == my read of the same bytes.
- **S261 agrees**: integrated quotes come from the same instruction.md lines I opened
  (`:9` log-summary, `:1`/`:7` vulnerable-secret); integrated fetch stamp
  `2026-11-04T08:26:13Z` is another seat's run — mine independently re-fetched the same
  pinned tree later the same day with matching digests on every shared file
  (instruction.md, task.toml, README.md, tests/*).

Frozen counters, run read-only at the tip by this seat:

```
$ python3 plans/round81_c1_new_members.py --lane .     → TARGET members=2 located=2 reproduced=2 ledger_flipped=2 defects=0; PREDICATE R81-C1 pass; rc=0
$ python3 plans/round81_c2_spotcheck_debt.py --lane .  → TARGET ids=6 closed=6 checks_passed=6 indexed=yes; DEFECTS n=0; PREDICATE R81-C2 pass; rc=0
```

## 7. Findings, limits, out-of-scope

- **U1AnchorR81's deliverable never appeared** (two polls) — anchors self-computed;
  they match the spot-check's committed expectation verbatim, so the check's re-derivation
  has independent agreement from this seat.
- **Failed fetches, reported not guessed**: `tasks/log-summary-date-ranges/` and
  `tasks/vulnerable-secret/` at the pinned tree are HTTP 404; the tasks live at the repo
  root at `2fd12b88`. The integrated S261 row's source cell names the root-level files,
  consistent with this correction.
- **Scratch**: `/fast/scratch/hyaku/kengaku-r81/SourcesScribeR81/` held fetched task
  files and the README capture; deleted before yield (no /tmp path cited as evidence;
  fetched copies' digests recorded above).
- **Tooling**: no installs or upgrades performed this seat (no pacman; no uv/npx).
  `curl` and `python3` were already present; nothing written to `~/.local/bin` or any
  PATH directory.
- **Not done (out of scope for a scribe leaf)**: no counter selftest/mutant batteries
  (executor seats), no receipt minting (probe seats), no SOURCES.md / ledger / lesson /
  findings edits (L1 integrates), no subagent dispatch.
- **Attack surface (what I could not break)**: the six receipt digests and both round-81
  SUBJECT_SHA pins held against independent re-derivation from committed bytes and from
  the pinned-tree remote; the 404 guess at `tasks/` was the only thing that broke, and it
  broke honestly. The S259 lines-2-12 vs lines-3-12 framing difference is recorded
  verbatim above for the canonical judge; the C2 counter as implemented passes at the tip
  with the integrated row, so the framing does not gate R81-C2 as landed.
