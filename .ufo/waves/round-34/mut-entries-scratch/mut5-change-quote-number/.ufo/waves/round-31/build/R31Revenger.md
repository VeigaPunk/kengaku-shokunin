# Round 31 — revenger: how five round-30 seat reports stayed uncommitted

Seat: `L1Kengaku31.R31Revenger`. Read-only. No production byte touched, no installs, no pacman
transaction, no `/tmp` scratch (every measurement below is a read of the lane repo, the fleet repo,
the UFO validator, or a harness transcript).

Scope: the five modified files in the round-30 wave tree, the two wave registries and their
assignment maps, the two dispatch payloads, the L1's transcript, the five seats' transcripts, the
round-30 non-author spot-check, and `PROTOCOL.md`.

---

## 1. The five files, measured

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` at 05:47 and again at
05:58 -03 returns **exactly five round-30 paths** (`M`), the same five both times. Round-31 lane
work moves underneath them between the two reads (`M plans/sources_adopt.py`, then also `M LOG.md`,
`M corpus/knowledge/contamination-transparency-card.md`, `M corpus/lessons/round-30.md`, untracked
`.ufo/waves/round-31/`, `corpus/evidence/round31/`,
`corpus/knowledge/benchmark-verifier-execution-model.md`, `plans/round-31-claims.md`,
`plans/round31_defects.py`); none of it is mine, and the round-30 set is unaffected by it.

```
$ git diff --numstat -- .ufo/waves/round-30/
56      12      .ufo/waves/round-30/build/R30DraftGate.md
258     0       .ufo/waves/round-30/build/R30RevLesson.md
105     56      .ufo/waves/round-30/falsify/R30FxCoverageAxis.md
59      1       .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md
87      28      .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md
```
565 insertions / 97 deletions in total. `git diff --stat` prints the same five files, `5 files
changed, 565 insertions(+), 97 deletions(-)`.

| file | HEAD lines | worktree lines | HEAD bytes | worktree bytes | last write |
|---|---|---|---|---|---|
| `build/R30DraftGate.md` | 199 | 243 | 18 452 | 21 442 | 04:59:49 |
| `build/R30RevLesson.md` | 1023 | 1281 | 66 844 | 83 625 | 05:03:55 |
| `falsify/R30FxCoverageAxis.md` | 368 | 417 | 26 384 | 29 656 | 04:59:55 |
| `falsify/R30FxEntryCompleteSet.md` | 338 | 396 | 32 121 | 36 796 | 04:59:28 |
| `falsify/R30FxEntryQ4Q6.md` | 388 | 447 | 32 126 | 38 236 | 05:04:19 |

(Line/byte counts from `git show HEAD:<path> | wc -l` and `stat -c '%s %y'`.)

The round's closure commit is `0883e72`, **2026-10-25 04:57:31 -03**, `round-30 verifier spot-check
(integrator, hyaku): non-author admit/reject`, and it touches one file:
`corpus/lessons/round-30-verifier-spotcheck.md | 202 ++++++++++++++++++++` — nothing else. The last
seat write is **05:04:19**, 6 min 48 s after that commit. Every one of the five files is later than
it.

## 2. (a) Which seats wrote them, and in what order

Ownership comes from `.ufo/waves/round-30/build-assignments.json` and
`.ufo/waves/round-30/falsify-assignments.json` (name → agent id), and from the registry rows in
`.ufo/waves/round-30/{build,falsify}/swarm-registry.json` (name → role).

| # | file | seat (assignment map) | role | last write |
|---|---|---|---|---|
| 1 | `falsify/R30FxEntryCompleteSet.md` | `L1Kengaku30.R30FxEntryCompleteSet-3` | reviewer | 04:59:28 |
| 2 | `build/R30DraftGate.md` | `L1Kengaku30.R30DraftGate` | scribe | 04:59:49 |
| 3 | `falsify/R30FxCoverageAxis.md` | `L1Kengaku30.R30FxCoverageAxis-3` | critic | 04:59:55 |
| 4 | `build/R30RevLesson.md` | `L1Kengaku30.R30RevLesson` | reviewer | 05:03:55 |
| 5 | `falsify/R30FxEntryQ4Q6.md` | `L1Kengaku30.R30FxEntryQ4Q6-3` | reviewer | 05:04:19 |

mtime is last-write-only, so the *pass* structure inside each file is the better ordering evidence:

- `R30RevLesson.md` — HEAD carries passes 1–7; the tree carries passes 1–13. `grep -n '^# Pass '`
  finds `# Pass 2`–`# Pass 7` at HEAD (6 headings; pass 1 is the file's opening prose) and
  `# Pass 2`–`# Pass 13` in the tree (12 headings), so six passes are new. Passes 8–13 are new sections: `# Pass 8 — sixth revision
  (2f1ac9dc…7dc6)`, `# Pass 11 — identity triple verified; review closed`, `# Pass 12 — digest pair
  verified…`, `# Pass 13 — the Q6 FAIL, verified first-hand from the form`. Its own closing line in
  the transcript says "Final artifact: `.ufo/waves/round-30/build/R30RevLesson.md` (thirteen
  passes)".
- `R30DraftGate.md` — new: `## Pass-7 and pass-8 residue, re-measured on the current entry
  (f51951d3)`, `## Closing state and the rule for any further revision`, `**Pass 9, recorded because
  it corrects a coverage seat's claim.**`
- `R30FxCoverageAxis.md` — new: `### Addendum 2 — the CTC column's provenance (verified, and the
  largest axis item left)`.
- `R30FxEntryCompleteSet.md` — new: `## 5c. Live-only findings at the newest blob (f51951d3…, HEAD
  caf1e2b)`.
- `R30FxEntryQ4Q6.md` — new: `## 2. Q5 …`, `## 3. Q6 …`, `## 4. Live-state table (admitted tree →
  tip, finding by finding)`.

The passes interleave across seats rather than running in file order. `R30RevLesson.md` pass 13
records "the Q4/Q6 seat's digest reproduces exactly on my fetch", and `R30FxEntryQ4Q6.md`'s closing
text records the reverse: "`L1Kengaku30.R30RevLesson` re-fetched both (`05131be9…`, 2 181 bytes;
`http=200 bytes=31923`)". The transcripts show the same exchange as messages:
`[irc] L1Kengaku30.R30FxEntryQ4Q6-3 → me` inside the RevLesson transcript, and
`[irc] L1Kengaku30.R30RevLesson → me` inside the Q4Q6 transcript.

**What woke them after the wave returned** is visible in the transcripts and is not the L1:

- `L1Kengaku30.R30DraftGate`: `[irc] L1Kengaku30.R30RevLesson → me: All three identifiers verified
  with my own commands…`, then an `edit(...R30DraftGate.md)`.
- `L1Kengaku30.R30FxEntryCompleteSet-3`: `[irc] L1Kengaku30.R30FxCoverageAxis-3 → me: M8 reproduces
  on my bytes and I've recorded it as the largest axis item…`, then `edit(...R30FxEntryCompleteSet.md)`.
- `L1Kengaku30.R30RevLesson`: `[irc] L1Kengaku30.R30FxEntryQ4Q6-3 → me: Clause added, and I checked
  it before writing it…`, then `edit(...R30RevLesson.md)`, then `write(agent://L1Kengaku30.R30FxEntryQ4Q6-3)`.

So the five writers were re-entered by **peer** `agent://` messages after their wave had returned —
the Coop channel that wakes a parked peer — and each re-entry landed in the same file at the same
path. Harness last-activity (read at 05:52, coarse) puts exactly these five at 40–44 m ago while
every other round-30 seat is at ~1 h: `R30DraftGate` 44 m, `R30FxEntryCompleteSet-3` 44 m,
`R30FxCoverageAxis-3` 44 m, `R30RevLesson` 40 m, `R30FxEntryQ4Q6-3` 40 m; `L1Kengaku30` itself 47 m.

## 3. (b) The report path let a seat keep appending — yes, by construction

The wave validator is `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`. Its report instruction
is one renderer used by both composition sites:

```
$ sed -n '222,228p' scripts/ufo-swarm-wave.mjs
// The per-lane report instruction is verbatim at both composition sites
// (resume message, spawn prompt): one renderer so the two paths can never
// drift on the path join or the wording.
function reportInstruction(reportDir, name) {
  return `Report: write your scoped findings to ${reportDir}/${name}.md`;
}
```

The spawn path appends it (`text = appendReportSuffix(text, reportInstruction(reportDir, name))`,
line 1254-1255) and the **resume** path appends the same bytes to a resume message (line 1217-1222),
with the same `name` — so a resumed member is handed the identical path it already wrote.

Nothing in the validator ever reads that path back. `grep -n
"statSync\|mtime\|sha256\|createHash\|digest" scripts/ufo-swarm-wave.mjs` returns one hit, line 1529,
a routing snapshot `{path, text, sha256}` — no report file is opened, hashed or stat'd anywhere. The
registry row per member is `{kind, agentId, role, item, axes, milestone}`
(`.ufo/waves/round-30/build/swarm-registry.json`, first member), with no report path, digest or
state.

The round-30 falsify dispatch shows the same fixed path in the lane text itself:
`Report: write your scoped findings to .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`. Neither
dispatch context (build 2 708 B, falsify 2 489 B) nor any lane task says when a seat stops writing,
that the path is write-once, or that a post-return revision goes somewhere else.

Two consequences, both observed:

1. **The wave returned while its lanes were still running.** The L1's transcript carries
   `[async-result] L1Kengaku30.R30FxEntryCompleteSet-3`, `[async-result] L1Kengaku30.R30FxEntryQ4Q6-3`,
   `[async-result] L1Kengaku30.R30DraftEntry` and others interleaved with its own commits — results
   arriving after it had already declared the round final.
2. **The falsify wave that actually wrote the reports has no owner of record.** All 33 rows of
   `.ufo/waves/round-30/falsify/swarm-registry.json` carry `"agentId": null` (measured: 33 of 33),
   while `falsify-assignments.json` names 33 handles ending `-3`. The build registry, by contrast,
   has 0 nulls out of 36. The L1's own final message names the cause: "the wave-2 agent ids are
   `null` in the falsify registry (the harness suffixed `-3` when the wave was resent after two host
   job-limit refusals)". A resent wave wrote the *same* report names as the first, and `record` was
   never applied to the resent registry — so at closure nobody could have proved from the wave record
   which handle owned `R30FxEntryQ4Q6.md`.

## 4. (c) The L1 committed a stale snapshot — yes, in three senses

Three commits in 17 seconds, all labelled final, all on the same file:

```
6966645  04:57:02  round-30: final seat-report revisions (DraftGate, EntryQ4Q6)
c1daaa7  04:57:10  round-30: R30FxEntryQ4Q6 final revision
2dcf06c  04:57:19  round-30: R30FxEntryQ4Q6 final revision (settled)
```

Line counts of `falsify/R30FxEntryQ4Q6.md` at each commit, and in the tree:

| commit | lines |
|---|---|
| `6966645` | 343 |
| `c1daaa7` | 381 |
| `2dcf06c` ("settled") | 388 |
| worktree | 447 |

`build/R30DraftGate.md`: 199 lines at `6966645`, 199 at HEAD, 243 in the tree.

1. **The snapshot was moving under the commit.** The file grew 343 → 381 → 388 inside the L1's three
   commits, and then grew another 59 lines after the commit whose message says "settled". A commit
   that captures a file mid-write is stale the instant it is made; the "(settled)" label is the part
   that is false, not the bytes.
2. **The seat's own later text contradicts the label.** The tree version of `R30FxEntryQ4Q6.md`
   grades the committed pin and still finds defects: "Entry is unchanged at `sha256 f51951d3…`
   (`caf1e2b`) … **Q4 — FAIL** … **Q6 — FAIL**", and "Still uncorrected at the settled tip"
   (line 351). So the author never treated `2dcf06c` as settled.
3. **The L1's clean-tree claim was false when it was made.** The final message says "Lane tip
   `2dcf06c56acb…` (pushed, `git status` empty)". The three tool results immediately before it are
   `git status --porcelain --untracked-files=all | head -3` → `ok · 2 lines`,
   `jj-lane.sh commit` → `ok · 6 lines`, `git status --porcelain --untracked-files=all` → `ok · 2
   lines`, then `ls -l --time-style=+%H:%M:%S .ufo/waves/round-30/falsify/R30FxEntr…` → `ok · 7
   lines`. Two dirty entries were on screen when "empty" was asserted. [INFERENCE] the two lines
   were two of the five seat reports; the transcript does not print the paths.

The round-30 spot-check measured the same thing one minute later and routed it instead of failing
it: `corpus/lessons/round-30-verifier-spotcheck.md:26` — "`git status --porcelain` shows **5
modified wave seat reports** … and a writer was still appending to them during this pass (mtimes
04:59:28 → 05:02:48, `date` at check 05:03:08)"; and `:184-188` item 6 — "349 insertions / 82
deletions against `2dcf06c` … Commit them under a round-30 entry or revert them; the closure could
not, and did not, touch them."

The spot-check's own figures are now short: 349/82 then, **565/97** now, and its mtime ceiling
05:02:48 is now **05:04:19** — two more writes (`R30RevLesson.md` 05:03:55, `R30FxEntryQ4Q6.md`
05:04:19) landed after the non-author read the tree. The defect reproduced itself during its own
audit, which is the cleanest proof that a point-in-time status check cannot close it.

## 5. (d) The structural fix

The rule already exists; what is missing is a **freeze point** and a **gate that runs at the right
instant**. `PROTOCOL.md` says:

- `:117-119` "A lane report **lands last** — written only after the lane's child-repo work is
  committed … Landed means committed, so changes that exist only in a working tree do not count for
  the round."
- `:122` "A lane whose report is still uncommitted when its mission completes has not satisfied this
  clause."
- `:231-232` closure step 1: the integrator "verifies no participating repo is left with uncommitted
  round work".
- `:281-283` "`in-flight` is therefore decided from the absence of both a `complete <lane> round=N`
  line and a *landed* report — an uncommitted file at the report path does not end `in-flight`".

All four were satisfied as *readings* and none as *states*: the integrator read the tree while it
was being written, and step 1 prescribes no consequence beyond "a conformance defect in the round
notes" (`:237-238`), so the violation became routing line 6 of the next round instead of a failed
closure.

**Rule to add — protocol (belongs to the protocol, because it binds the validator and every lane):**

> **Wave-evidence freeze.** A wave's seat reports are frozen when the wave's dispatch returns: the
> report path a lane is given is write-once per wave. A revision after the wave returns — including
> one produced by a seat handle woken by a peer `agent://` message — lands at a new path
> (`<name>.r2.md`) and is committed as its own revision naming the bytes it supersedes; it never
> appends to an already-committed report path. The wake itself is recorded in the round notes,
> because it is a resume the wave record does not show.

Mechanical half of the same rule, operator-side (`scripts/` is not lane-editable, `PROTOCOL.md:217`
"— it never edits a prompt or the script, and `scripts/` plus `.ufo/state/` remain operator-side"):
`ufo-swarm-wave.mjs` records `reportPath` + `reportSha256` per member at `record` time, and `plan`
refuses (`report_sealed`) a resume whose member's report no longer matches its recorded digest. The
single code point is `reportInstruction()` at `ufo-swarm-wave.mjs:225-227` plus its two call sites
(1217-1222 resume, 1254-1255 spawn): the resume arm must render a different file name.

**Command to add — lane (belongs to the lane, because it reads only the lane's own tree and the lane
owns its receipts and its counter):**

```sh
# run immediately before the round's final commit, and again as the last act of the round
test -z "$(git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain --untracked-files=all)" \
  || { echo "round not closable: uncommitted round work"; exit 1; }
```

with its (empty) output committed at `.ufo/waves/round-<N>/claims/worktree-clean.txt`, so a
non-author re-runs it against the cited tip instead of trusting a transcript line.

The lane has already built this instrument once. `plans/round30_defects.py:156-175` (`check_d4`) is
exactly the pattern, down to the comment: "A clean status is not the repair: a clone whose HEAD
predates the addendum is clean too" — it checks `HEAD` carries the marker, then
`git status --porcelain -- <D4_PATH>` must be empty. Round 30 applied that gate to one round-29 path
and not to its own `.ufo/waves/round-30/` tree. The fix is that check generalised: a D-item whose
path is the round's own wave directory, in the round's own counter.

**To make a later round's closure see a clean tree, in order:**

1. Now (round-31 lane work, not mine to do): land or revert the five files —
   `git add .ufo/waves/round-30/build/R30DraftGate.md .ufo/waves/round-30/build/R30RevLesson.md
   .ufo/waves/round-30/falsify/R30FxCoverageAxis.md .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md
   .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md` and one commit labelled as post-closure revision
   (they are the seats' 04:59–05:04 passes, not the 04:57 snapshot), or `git checkout --` them to
   restore `2dcf06c` bytes and record the refusal. Either is honest; leaving them dirty is not,
   because round-31's closure step 1 will read the same dirty tree.
2. Then the lane gate above, so the next round cannot declare final while dirty.
3. Then the protocol freeze, so the *reason* the tree moved — a parked seat re-entered by a peer
   message writing its old path — stops being possible.

## 6. What I did not establish

- The two lines in the L1's last `git status` are not printed in its transcript; which two of the
  five were dirty at 04:57:19 is [INFERENCE].
- Harness last-activity is minute-coarse; I used it only to show that these five seats, and only
  these five, were active after the closure commit.
- I did not re-run any of the seats' content claims (fetches, digests); nothing in this report
  depends on them being true, only on their having been written.
- The round-30 report is the fleet-repo artifact `/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kengaku.md`
  (commits `b5cd9d69`, `068c7c41`, `3d38d633`, `c5807fe7`); the hash `c5807fe7` cited by the
  spot-check does not exist in the lane repo, which is consistent — the report is fleet-side, and
  the spot-check's own commit `0883e72` carries only the spot-check file.
- Nothing installed or upgraded this pass, so there is no tool record to make.

VERDICT: FAIL — the five files stayed uncommitted because a parked seat's report path is a fixed, unowned write target that survives its wave's return: three falsify seats (`…CoverageAxis-3`, `…EntryCompleteSet-3`, `…EntryQ4Q6-3`, all `agentId: null` in the resent wave's registry) and two build seats (`R30DraftGate`, `R30RevLesson`) were woken by peer `agent://` messages after the closure commit `0883e72` (04:57:31) and appended in place until 05:04:19 (565/97 vs `2dcf06c`), while the L1 committed three "final" snapshots of one growing file in 17 s (343 → 381 → 388 lines, "(settled)" at 388, 447 in the tree) and declared "`git status` empty" over its own 2-line dirty status; the fix is a protocol freeze (report path write-once per wave, digest recorded at `record`, resume rendered to a new path) plus a lane gate — `test -z "$(git status --porcelain --untracked-files=all)"` committed as `.ufo/waves/round-<N>/claims/worktree-clean.txt` before the final commit — which is `plans/round30_defects.py:156-175` (D4) generalised from one wave path to the round's own tree.
