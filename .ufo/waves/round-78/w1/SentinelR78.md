# SentinelR78 — adversarial security review, kengaku round 78 w1 (2026-11-04)

Scope: the two new instruments `plans/round78_c1_class_member_ledger.py` (C1) and
`plans/round78_c2_stamp_location.py` (C2), the lane-controlled data they read
(`plans/grader-selected-members.json`, `SKILL.md` class rows, round-62 census), credential leakage
in the receipts this round re-mints, and the wave's write scope. Lane audited at master
`f20a2f6f` (freeze `2f9eeafb` verified ancestor: `git merge-base --is-ancestor 2f9eeafb master`
→ rc=0). Every command below was observed this session; fixtures lived in
`/fast/scratch/hyaku/kengaku-r78/SentinelR78/` and were deleted after the run. No tools were
installed (pacman pause respected; nothing needed). Read-only git only; no mutation anywhere in
the lane, the fleet repo, or any domain tree.

## 1. Path trace of both counters

**No shell execution, no network access, no dynamic execution.** Both files import only
`argparse/json/re/shutil/subprocess/sys/pathlib` (C2 adds `hashlib/tempfile`). Grep over both
files for `shell=|os.system|popen|getoutput|check_output|check_call|__import__|urllib|socket|
requests.|http://|https://|pickle|marshal` → **zero matches**. The only `subprocess` site is the
argv-list helper `subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)`
(C1:80-81, C2:56-57). A receipt's `COMMAND` line is only regex-matched (C2:51, used at :177),
**never executed**.

**Subprocess argv that interpolates lane-controlled strings** (all argv-list, so no shell
metacharacter is ever interpreted):

| Call | Interpolated value | Source | Containment observed |
|---|---|---|---|
| `rev-parse --verify --quiet {rev}^{commit}` (C1:100, C2:69) | `--rev` CLI arg | operator, not lane data | operator's own flag; not a lane boundary |
| `rev-parse --verify --quiet {tip}^{commit}`, `merge-base --is-ancestor {tip} master` (C2:157-160) | receipt `LANE_TIP` | committed receipt bytes | regex-anchored `[0-9a-f]{7,40}` (C2:45) → cannot start with `-`; no option injection |
| `ls-files --error-unmatch -- {rel}` (C1:113) | ledger `receipt` | committed ledger bytes | `--` guard; outside/absolute paths → rc=128 (observed) |
| `cat-file -e/-p {tip}:{rel}`, `show {tip}:{rel}` (C1:116-118, C2:93-97) | census member / ledger receipt / receipt `TOOL`+`TOOL-SUPPLIED` | committed bytes | git tree-path resolution refuses escape — observed in a fixture: `show <tip>:../../etc/hostname` → `fatal: ... is outside repository` rc=128; `show <tip>:/etc/hostname` → `exists on disk, but not in '<tip>'` rc=128; `cat-file -e` with both → rc=128; `ls-files --error-unmatch -- /etc/passwd` and `-- ../outside` → rc=128 |
| `ls-tree -r --name-only {tip} -- {d}` (C2:130) | constant `d` | — | — |

**Writes:** only two sinks exist — the `--receipt` file (C1:360-362, C2:214-216, path chosen by
the operator) and fixture trees under `--work` (C1 `build_fixture`:370-428, C2 `fixture_repo`:
227-276). The C2 fixture repo inits with an explicit `-b master` and a fixture-local identity
(C2:233-234). No write touches the lane. Exception: both counters **create the default work dir
unconditionally on every run** (finding F4). `--rev`/worktree audit runs are otherwise read-only.

## 2. Can committed data make the counter read outside the lane?

`SKILL.md` class rows: **no**. Class names (`cells[0]`, C1:169) are used only as dict keys and in
defect strings — they never join a path. The `executed` cell is only regex-scanned
(`PARTIAL`, C1:44) and checked for the ledger pointer. All three partial rows
(`SKILL.md:78,81,83`) carry `ledger=plans/grader-selected-members.json` (grep observed on all
three), so `CLASS-ROW-UNLINKED` is clean.

`plans/grader-selected-members.json` + census: **yes, in worktree mode — findings F1/F2.** The
worktree `Tree` joins paths with pathlib (C1:112 `lambda rel: _read_file(lane / rel)`, :114
`(lane / rel).exists()`), and neither census `members=` tokens (C1:193) nor ledger keys
(`load_ledger` C1:198-209, no validation) nor the ledger `receipt` field (C1:278) are sanitized
or resolve-contained. Rev mode is git-contained (table above). The frozen predicate mode is
`--lane .`, i.e. the vulnerable one.

The committed ledger as it stands is clean: all 12 member keys are bare identifiers, all 7
receipt paths are relative in-lane (`corpus/evidence/round6x|7x/...`), 13 class pairs over 3
classes (8+3+2, `install-windows-3.11` dual-classed). The lane has **zero tracked symlinks**
(`git ls-files -s | awk '$1=="120000"'` → empty), so F1/F2 are latent, not presently exploited.

### F1 — HIGH — a tracked symlink as an `executed` member's receipt certifies a verdict from bytes outside the lane

- **Where:** C1:112 (`_read_file` follows symlinks) with :113 `tracked()` checking only the link
  itself and :281-286 never re-checking containment; consumed in the frozen `--lane .` mode.
- **Exploit path (needs one lane commit, exactly what a seat writes each round):** commit
  `corpus/evidence/r/x.txt` as a symlink to an out-of-repo file containing
  `PREDICATE R70-C1 pass`, and point the ledger row's `receipt` at it. `exists()` follows, `tracked()`
  passes (the link is in the index), `get()` returns the out-of-lane bytes, `verdict_token`
  (C1:218-222) matches → the member counts as executed with evidence that lives outside the repo.
- **Observed** (fixture git repo in scratch, symlink committed, target file under
  `/fast/scratch/...`): `MEMBER sym executed classes=alpha receipt=corpus/evidence/r/sym.txt
  verdict=R72-C1 token=predicate`, no defect for `sym`. Control in the same run: an *absolute*
  receipt path `/etc/hostname` is correctly failed closed (`DEFECT RECEIPT-UNTRACKED abs
  /etc/hostname`). Under `--rev HEAD` the same symlink receipt fails
  (`DEFECT PREDICATE-ABSENT sym ...`) because `git show` prints the link's target string, not the
  target's bytes — the defect exists only in worktree mode.
- **Impact:** defeats C1's core invariant ("a tracked receipt **whose own bytes** carry
  `PREDICATE <id> pass`") from committed bytes; a forged `PREDICATE R78-C1 pass`.
- **Smallest remediation:** after the `tracked()` check, require
  `(lane / receipt_rel).resolve()` to be inside `lane.resolve()` (and optionally reject
  non-regular files), or compare the index mode and refuse mode `120000` receipts. Flag only —
  not repaired here (frozen instrument).

### F2 — MEDIUM — unsanitized census member names / ledger keys redirect the frozen reason-detectors to files outside the lane

- **Where:** C1:212-215 `grader_bytes` builds `{GRADERS}/{member}/tests/test_outputs.py` from the
  raw member string; member strings come from the census `members=` list (C1:193) intersected
  with ledger keys (unvalidated, C1:198-209).
- **Exploit path:** a member token containing `../` (census regex `members=(.*)$` accepts
  anything but a newline; ledger JSON keys accept anything) points the detector read at any file
  the lane user can read, e.g. outside the repo. A detector that fires there suppresses
  `REASON-UNBACKED`, so an unbacked reason reaches `unbacked=0` and the target line lies.
  Member tokens are also echoed raw into `MEMBER`/`DEFECT` lines (C1:296-298, :242) — a ledger
  key containing a newline (possible in JSON, not via census) would inject fake verdict-looking
  lines into receipt text; cosmetic for the gate itself (which counts defects, not prose) but
  hostile to downstream parsers.
- **Observed** (fixture, single member `../../../../../../fast/scratch/.../outside`, detector
  bytes at `<outside>/tests/test_outputs.py` containing `selenium`; resolved path printed
  `outside fixture lane: True`): worktree mode → `DEFECTS n=0`, `TARGET ... unbacked=0`,
  **`PREDICATE R78-C1 pass`, rc=0**. Rev mode → `DEFECT REASON-UNBACKED ...` rc=1 (contained).
  Worktree-mode existence probing of an absolute receipt path (C1:281) is also an out-of-lane
  metadata oracle, though it fails closed (F1 control).
- **Impact:** the coverage gate's `unbacked=0` can be satisfied with bytes the lane does not
  carry; an out-of-lane read oracle keyed on detector regexes.
- **Smallest remediation:** validate member keys/tokens against `^[A-Za-z0-9][A-Za-z0-9._-]*$`
  (reject `..`/absolute) in `load_ledger` and `census_classes`, and resolve-contain
  `grader_bytes` paths like F1. Flag only.

### F3 — MEDIUM — C2 does not enforce its own frozen kill rule: truncated `TOOL_SHA` pins are accepted, not refused

- **Where:** C2:103-104 `digest_matches` returns `actual.startswith(pin)` for any pin shorter
  than 64 hex; the `TOOL_SHA` regex (C2:49) accepts 8–63 hex pins; the mutant matrix
  (C2:306-313) contains no truncated-pin case, so the skip survives the battery.
- **Frozen text violated:** `plans/round-78-claims.md` §R78-C2 kill rules — "A receipt whose
  `TOOL_SHA` matches by coincidence of a truncated pin is refused (full digest comparison)".
- **Observed** (fixture repo, tool committed, receipt pinning `TOOL_SHA 2a402bbb` — the first 8
  hex of the 64-hex digest): counter prints `RECEIPT ... legs=ok`, `DEFECTS n=0`,
  `TARGET receipts=1 located=1 unlocated=0`, **`PREDICATE R78-C2 pass`, rc=0**. The frozen rule
  demands refusal.
- **Impact:** a re-minted receipt can bind its tool claim with 32 bits; any blob sharing the
  prefix satisfies the drift leg (2^32 forge), and an under-committed pin passes the gate the
  claim says must refuse it. The calibration claim's stated kill condition is unenforced.
- **Smallest remediation:** require `TOOL_SHA [0-9a-f]{64}` and exact equality in
  `digest_matches`, and add the truncated-pin mutant to the matrix so the skip is attributed.
  Flag only — changing the counter is the integrator's call.

### F4 — LOW — default work dirs are predictable shared paths, created on every run

C1:532-533 `work = args.work or Path("/tmp")/"r78-c1"; work.mkdir(parents=True, exist_ok=True)`
runs **before mode dispatch** — even a plain `--lane .` predicate run creates `/tmp/r78-c1`
(ignores `TMPDIR`); C2:357 uses `tempfile.gettempdir()/"r78-c2"` (respects `TMPDIR`, same
predictable name). Fixture builders then `shutil.rmtree(root)` (C1:370-371, C2:227-228) inside.
On a multi-user host this is a squat/race surface (a pre-planted symlink component can redirect
fixture writes; `rmtree` refuses top-level symlinks but not nested ones). Remediation: create
work lazily only for `--selftest/--mutants/--control-*`, via `tempfile.mkdtemp`. Severity capped:
fixtures are only written in self-test modes, and the re-mint/verdict flows write nothing there.

### F5 — LOW — C2 universe reads whole files; the frozen universe says "first 40 lines"

C2:137 `SIGNATURES.search(text)` scans the entire file; the frozen claim derives the universe
from a signature in the **first 40 lines**. Observed delta at `f20a2f6f`: **0** — both
derivations select the same 25 receipts (round77+round78, `sources/` skipped). Divergence is
latent and fails strict (can only over-include receipts that must locate, never false-pass).
Remediation if exact conformance is wanted: search `"\n".join(text.splitlines()[:40])`.

### F6 — LOW — C2 worktree universe/read follows file-symlinks (dir-symlinks are safe here)

C2:132 walks `live.rglob("*")`; on this host's Python 3.14.8 directory symlinks are **not**
descended (observed: symlinked dir absent from the walk — `recurse_symlinks` defaults false
since 3.13). But a committed *file* symlink directly under `corpus/evidence/round77|78` would be
yielded (`is_file()` follows) and read through by `Ctx.get` (C2:83-87), feeding out-of-lane bytes
to the signature scan and the stamp legs. Rev mode uses `ls-tree` and is immune. No tracked
symlinks exist in the lane today. Same remediation class as F1 (reject symlinks / resolve-contain).

### Informational

- **I-1** C1:526 `--expect-manifest` is declared and never referenced (`expect_manifest` has zero
  other occurrences) — dead flag; wire it or drop it.
- **I-2** The post-freeze repair driver `plans/round78_restamp.py` (landed `cd2e25bb`/`f20a2f6f`)
  is trusted integrator surface, not a counter: `rerun` mode executes spec-named commands at the
  lane (`subprocess.run(cmd, cwd=str(lane))`, :76, argv from committed
  `plans/round78-restamp.json`) — by design, since rerunning the tool is its job; `retag` mode
  appends stamp-only blocks (observed :93-122: `LANE_TIP/TOOL|TOOL-SUPPLIED/TOOL_SHA/WORKTREE/
  COMMAND/RE-STAMPED` — no env, no secrets) and is idempotent. Default work dir
  `/fast/scratch/hyaku/kengaku-r78/restamp` (:135) sits inside `HYAKU_SCRATCH`. Its appended
  blocks cannot introduce credential material (see §3).

## 3. Credential sweep of the receipts this round re-mints

Two passes over every file under `corpus/evidence/round77/` and `corpus/evidence/round78/`:

1. **Broad, case-insensitive:** `op://`, `ghp_|gho_|github_pat_`, `xox[abp]-`, `AKIA[0-9A-Z]{16}`,
   `BEGIN ... PRIVATE KEY`, `Authorization:`, `Bearer`, `set-cookie/Cookie:`, `password/passwd`,
   `secret`, `api[_-]?key`, `_TOKEN`, `token=` → hits:
   `round77/exec-state-check.txt:7` — the probe-data token `"token=### Adjacent"` (a mismatch
   report's derived tokens, not a credential); `round77/sources/git-cat-file.html:2495,2545` —
   `/etc/passwd` symlink examples inside fetched git-documentation HTML. **No hits at all under
   `round78/`.**
2. **Format-specific, case-sensitive:** `eyJ` (JWT), `-----BEGIN`, `ssh-rsa|ssh-ed25519`,
   `sk-ant|sk-proj`, `glpat-`, `AIza…`, `xox[abprs]-`, `SESSION|session_id`, `Cookie`, `PASSW`,
   `TOKEN`, `SECRET`, `API_KEY`, `apikey`, `credential` → only `credential-helpers` link text in
   the fetched doc pages `round77/sources/git-cat-file.html:271` and
   `round78/sources/git-status.html:280`.

Verdict: **no credential material in any receipt**; the only matches are probe-data tokens and
third-party documentation prose frozen under `sources/` (which C2's universe excludes via
`SKIP_PARTS`). The re-mint paths keep it that way: rerun receipts are stamp head + the lane
tool's own verdict bytes; retag appends the stamp block shown in I-2 and preserves existing
clean bytes.

## 4. Wave write-scope audit (last 3 commits, lane and fleet root)

**Lane** (`master=f20a2f6f` at audit time; the tip moved once during the audit as the C2 repair
landed — freeze `2f9eeafb` remained an ancestor throughout):

| Commit | Paths | In allowed set? |
|---|---|---|
| `f20a2f6f` round-78: R78-C2 repair landed | `corpus/evidence/round77/*.txt` ×16, `plans/round78_restamp.py` | yes (`corpus/`, `plans/`) |
| `cd2e25bb` restamp driver + spec | `plans/round78-restamp.json`, `plans/round78_restamp.py` | yes (`plans/`) |
| `2f9eeafb` freeze | `SKILL.md`, `plans/*` ×4 | yes |
| (context) `3ae0ab54`, `5eb74eed`, `7023db7e` | `corpus/lessons/*`; `.ufo/waves/round-77/w1/*`; `SKILL.md` | `3ae0ab54`/`7023db7e` yes; `5eb74eed` touches `.ufo/waves/round-77/` — outside `.ufo/waves/round-78/` but it is the *prior* round's handoff, committed 02:44 before this wave's dispatch |

**Fleet root** `/home/vgpnk/Projects/shokunin`, last 3 commits (all 2026-11-04T02:55–02:59
−03:00, orchestrator "hyaku" bookkeeping at wave dispatch):

| Commit | Paths | In allowed set? |
|---|---|---|
| `08555038` round-75: mado dispatch evidence | `.ufo/prompts/mado-round-75.md` | **no** — `.ufo/prompts/` is not `.ufo/waves/round-78/` |
| `ead42ee7` rounds ledger: mado r74 closure | `MANIFEST.json` | **no** — fleet-root tracked ledger file seats must never write |
| `fa9246c9` round-80: mori dispatch evidence | `.ufo/prompts/mori-round-80.md` | **no** — same as above |

Assessment: these are the orchestrator's own ledger/prompt records minutes before dispatch — the
write-scope rule binds *seats*, and no seat-authored commit or uncommitted path leaves the
allowed set. Uncommitted lane state at audit time: 9 modified files, all
`corpus/evidence/round78/*.txt` (in scope), plus the untracked `.ufo/waves/round-78/` wave dir
itself. 31 receipts tracked under `round77|78`; C2's derived universe at `f20a2f6f` = 25.

## Tally

Findings: F1 HIGH (C1 symlink-receipt verdict forgery, worktree mode), F2 MEDIUM (C1 unsanitized
member/receipt paths → out-of-lane detector reads; PoC reaches `PREDICATE R78-C1 pass` rc=0),
F3 MEDIUM (C2 truncated-pin kill rule unenforced; PoC reaches `PREDICATE R78-C2 pass` rc=0),
F4–F6 LOW (default /tmp work dirs; universe whole-text vs first-40-lines, delta 0 today;
file-symlink read-through in C2's worktree walk), plus I-1..I-3 informational. Both escapes that
reach a false pass require lane-commit access (a seat's own artifacts), are latent (no tracked
symlinks, ledger clean today), and are git-contained in `--rev` mode — the frozen predicate mode
`--lane .` is the exposed one. No shell/network/dynamic-exec surface in either counter; no
credential material in any re-minted receipt; seat write scope observed clean.

**SENTINEL: 6 findings (1 high)**
