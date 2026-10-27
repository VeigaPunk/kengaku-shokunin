# R45CriticPredicate — falsification of the frozen C1 predicate

Scope: `plans/round-45-claims.md` §C1 and the counter `plans/round45_c1_verify.py` (its docstring is the frozen
rule). Method: read both in full; reproduce `run_fence`'s exact sandbox+strace+parser on a mini fixture; then run
the REAL counter end-to-end twice on `--shared` clones (`git clone -q --shared`, `--work` under scratch, inside
the round-45 envelope) with two forged `plans/fixture_fence.py` variants. No tools installed (strace 7.2,
bubblewrap 0.13.1, python3 3.14.8, kernel 7.2.11-arch1-1 already present).

## Headline: the FROZEN predicate is fully forgeable — proven `PREDICATE C1 pass` with a fake fence

Two counter runs, identical except for one `os.unlink` line in the fence:

- **Run A — `fence-killshot.py`** (sha256 `2246ab7f…c0cd131`, the digest the counter itself prints): on the
  refusal path it (i) refuses purely on the directory substring `"/refusals45-"` — zero fixture inspection;
  (ii) performs real outside-`d` opens under the build scratch (`listdir(d.parent)`, `open(outside.cfg)`,
  `open(*.cfg)` planted by modules); (iii) `open("/etc/hostname")`; (iv) locates its own strace log via
  `TracerPid`/`/proc/<pid>/cmdline` and **unlinks it**. Result, full receipt `runA-killshot.out`:
  `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`,
  `HONEST fixtures=104 admitted=104 …`, `CALIBRATION advertised=10 contradicted=0`, **`PREDICATE C1 pass`, exit 0**.
  Envelope unchanged (`e396f23e40a69201` before/after, `exit=0`).
- **Run B — `fence-nokill.py`** (sha256 `f3eee1a1…02ea1547`), byte-identical minus the unlink: every refusal row
  reports `BREACH opens=2..4`, `REFUSALS … read=10`, `contradicted=10`, **`PREDICATE C1 fail`, exit 1**
  (`runB-nokill.out`). So the counting works when the log survives — and a single fence-side `os.unlink` of a
  file it owns flips pass↔fail. The unlink syscall itself is invisible: `strace -e trace=open,openat,openat2,creat`
  (counter :181) does not include `unlink`, and the log path is outside the counted `scratch` tuple.

A `clean=10` with a fence that never opens a single fixture is a `contradicted=0` that means nothing. This alone
falsifies the claim that a pass proves "the advertised fence vs the observed one" matches.

## Enumerated bypasses (ranked by whether they change the verdict)

**B1 — strace-log erasure; VERDICT-CHANGING (proven end-to-end).** `run_fence` bind-mounts `writable=(logdir,)`
(:180), so the traced fence owns its own measurement record. `os.unlink(log)` is untraced; the parser then hits
`except OSError: lines = []` (:194) → `opens=0`. Driver proof that the read happened AND was erased:
`RESULT verdict=BREACH opens=0 why='read-then-erased secret=OUTSIDE-SECRET'` (fence-logkill2.py). In-place
`ftruncate(0)` is a weaker variant — the kept log (`keep-trunc-log.txt`) still held 1 post-trunc open — but
unlink is total because the counter re-reads by *path*. Also erases `K45_KEEP_STRACE` evidence (copy happens
after the run, :224). **Fix:** pass the log by fd (`--ro-bind-data`-style slot or a pipe strace writes), not a
path inside the sandbox; or treat ENOENT/`len(lines)==0` after a started run as tamper, not zero.

**B2 — fixture keying through `d`'s path; VERDICT-CHANGING (proven end-to-end).** The counter names every
fixture dir `<root>/fx/<battery-or-refusals45>-<stem>/fNNN` (`build_module`, :136). `d.parent.name` and absolute
`argv` tokens (f4/f5 `--lane` is `str(d)/lane`) leak module identity; a two-branch fence passes with no
inspection (run A). The HONEST leg does NOT prevent fixture-id/family keying — it is exactly what keying needs:
`battery4?-` admit-all, `refusals45-` refuse-all, split total. The claim anticipates this only via
"non-author review of the fence source rides admission" (claims :65) and report-only held-out modules — the
shipped gate itself cannot see it. **Fix:** bind `d` to a constant sandbox path (e.g. `/fixture`), cwd there,
rewrite absolute argv tokens onto it; hide `root` except `d`.

**B3 — measured "read" ⊆ advertised "parsed"; VERDICT-CHANGING (semantic; proven).** Advertised property (r44
`repo_breach` F5, counter docstring :13-16): "no file outside `d` is parsed". Measured (:211): opens must lie
under `scratch = (root/"fx", root/"btmp")` (:190) AND outside `d`. `--ro-bind / /` makes the whole host
readable; opens of `/etc`, `/proc`, `/sys`, **`root/mods` (the module-source copies, :140-142)**, `root/fence`,
sibling `root/strace` logs are all uncounted. Proven: `fence-hostread.py` → `BREACH opens=0 why='host-read
plazir27 200'`; `fence-modsread.py` → `BREACH opens=0 why='mods-read 28 # module source leak oracle'` — the
fence read a refusal module's source, an oracle keyed on fixture build logic, invisible to the count. The fence
can also `git config` or `include.path`-parse a file outside scratch (f8's marker points inside scratch, but a
held-out module's could point at `/etc/…`) and read `read=0`. A pass certifies an untrue F5.
**Fix:** count opens outside `d` under the whole scratch root (and `root/mods`,`root/fence`,`root/strace`), and
decide whether host opens outside scratch should also count (at minimum against the advertisement).

**B4 — verdict-line spoof over stdout; VERDICT-CHANGING (proven).** The harness prints the return value; the
parser accepts `out.startswith("BREACH ")` (:230). A fence that `print("BREACH planted")` then returns `None`
yields stdout `"BREACH planted\nADMIT"` → parsed **BREACH**, reason `'planted-by-print\nADMIT'` (fence-spoof.py,
driver-run). Refusals are forgeable with zero inspection; combined with B2 blind refusals need no truth at all.
(Inverse is safe: `ADMIT`-then-BREACH → `BREACH`, and ERROR counts as admission on the refusal side, :291.)
**Fix:** communicate the verdict on a dedicated channel (exit code, fd slot), not stdout shared with fence
prints — or at least require the LAST line.

**B5 — content/metadata channel with zero opens; VERDICT-CHANGING (proven).** Only `open/openat/openat2/creat`
are traced. `stat/lstat/access/readlink/getxattr/euidaccess` are never traced: the fence resolved
`outside.cfg` (15 B), `mod_refusals45_t9.py` (28 B), its own `fixture_fence.py` (780 B), `/etc/hostname`,
`/proc/self/mountinfo`, `readlink("/proc/self/exe") → /usr/bin/python3.14` — `BREACH opens=0` (fence-stat.py).
`readlink`/`getxattr` return file *content* — "parsed" under the advertised wording — with no open at all;
`inotify_add_watch`, `name_to_handle_at` likewise. Makes every keyed/covert decision open-free.
**Fix:** add `-e trace=%file` classes or audit `newfstatat/access/readlink*/getxattr` similarly; or accept and
document "reads" = opens only (then the advertisement, not the count, is wrong).

**B6 — the "blocked open" accounting is dead code in both directions; VERDICT-CHANGING (proven).** The pending
bucket exists to count opens that never return (:215). But (a) `RESUMED_RE.search` → `pending.pop(pid)` runs
*before* the open check and matches ANY resumed syscall (:200-202): strace 7.2 prints a blocked `openat`
as `<unfinished ...>` then `<... openat resumed>) = ?` on kill — absolute-path blocked open erased
(`kill-abs-strace.txt:36-38`). (b) If the line stays pending (relative path, killed without resume decode:
`kill-rel-strace.txt:37` `openat(AT_FDCWD<…/modX>, "fifo.cfg", …) = ?`), the extraction regex `'"(/[^"]+)"'`
(:216) requires an absolute quoted path — `AT_FDCWD<dir>, "rel"` yields none. So a sacrificial child/thread
blocked on an outside FIFO then killed leaves **no counted open**; conversely f4's real fifo-open (control
`read=4`) survives only because it's an unfinished-absolute line that never resumes. HUNG runs skip parsing
entirely (:189, HUNG+READ conflated). **Fix:** decode resumed lines with their stored pending text instead of
popping; match dirfd-annotated relative paths against the annotated cwd.

**B7 — io_uring opens/reads invisible to strace; verdict-changing CAPABILITY (channel proven, not exploited).**
`io_uring_setup` succeeded inside the sandbox (`setup fd 3 errno 0`); SQE ops (IORING_OP_OPENAT/READ) execute in
kernel context and emit no `open*` syscalls. The `-e trace=` filter never sees them. Overkill while B1 exists,
but the only clean fix for B1 (fd-delivered log) still leaves this channel. Partial fix set: seccomp-filter
`io_uring_*` in the sandbox, or accept as documented residue.

## Not bypasses (tested, closed)

- `openat2` IS decoded/traced by strace 7.2 (`openat2(...) = -1 E2BIG` logged).
- Bind-mount laundering (mount an outside dir over a dir inside `d`): `mount --bind d.parent d` → `rc=32`
  (bubblewrap locked mounts; no `--unshare-user` in `ro_sandbox` → no usable userns caps).
- Subprocesses DO get traced (`-f`); children opening scratch paths count normally — B6's kill is what
  exempts them, not process boundaries.
- `open_by_handle_at`: needs CAP_DAC_READ_SEARCH — absent under `ro_sandbox`.
- `CLONE_UNTRACED`: needs CAP_SYS_ADMIN — absent.
- `O_PATH`/`O_NOFOLLOW` opens still annotate and count.
- A refusal module building zero fixtures → `not rows` → LEAKED (:294): correct fail-safe.
- Extra refusal `.py` → `rtotal != REFUSAL_TOTAL` → fail; extra honest `.py` → `fixtures>104` → fail: glob
  additions can only tighten.

## Direct answers to the assigned questions

1. **Is `contradicted` the right count?** Granularity yes — the advertised count is modules
   (`advertised=10`, `contradicted=7` baseline). Two defects: (i) `contradicted = rtotal - clean +
   build_errors["refusal"]` (:317) double-counts a build-errored module (it's already inside `rtotal -
   clean`), so the printed number can exceed the true module count (fail-safe direction); (ii) it is the right
   count of the *wrong, forgeable* measurement — B1/B2 show `contradicted=0` with a fence that inspects
   nothing. So: right unit, unreliable quantity.
2. **Can a fence reach pass while violating "no file outside d is parsed"?** Yes, five demonstrated ways:
   B1 (erase the evidence), B3 (opens outside the scratch tuple are uncounted — /etc, /proc, root/mods,
   root/strace, include targets outside scratch), B5 (no-open channels: stat/readlink/getxattr), B6 (killed
   blocked opens), B7 (io_uring). The docstring's own threat-model — "everything a hostile module can write"
   (:190 comment, scratch = fx+btmp only) — measures module artifacts, not the fence's actual parsing, and the
   fence itself is the thing under test.
3. **`clean` per-module vs per-fixture:** per-module roll-up matches the advertised count and per-fixture
   `FENCE-RUN` rows keep detail — defensible. Minor: precedence `HUNG` > `READ` (:297-300) hides opens behind a
   hang, and HUNG skips log parsing (:189) losing evidence; fail-safe, not a hole.
4. **Does HONEST allow a fence keyed on fixture-id text?** Yes — proven: module name is baked into `d`'s path
   by the counter itself; honest/refusal names form a disjoint, total split. Even argv suffices for
   absolute-token fixtures (f4, f5).

## Secondary defects (not verdict-changing)

- **D1** `run_fence` env lacks `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL=/dev/null`/`GIT_PINS` (:185-187): the
  fence's own `pin_git` calls inherit host git config; `/etc/gitconfig` `include.path` would parse a host file
  unmeasurably (B3) and nondeterministically. Frozen design pushes env-pinning onto the fence; the counter
  doesn't enforce it.
- **D2** `build_module` dropped r44's `path_ok` argv check (:158-166 vs r44 `build_battery`): docstring promises
  "tokens relative to `d` or absolute inside it" — unenforced; a held-out module can pass absolute outside
  tokens and the fence may dutifully open them.
- **D3** Module build children aren't straced and `--ro-bind / /` reads the whole host: modules can launder
  host data into `d` (copied inside-`d` files count as inside). Threat-model gap, same family as B3.
- **D4** `first` computed but unused (:198,213); `contradicted` double-count (above); `HUNG` skips pending-parse.
- **D5** `K45_KEEP_STRACE` copies the post-tamper log — preserved "evidence" is the forged artifact
  (`keep-trunc-log.txt` IS the truncated log, 1 line survived).

## Smallest safe correction (for the L1; nothing here asks to unfreeze)

(1) Deliver the strace log out-of-band — `--ro-bind-data`/fd slot or a pipe — and treat a missing/empty log as
tamper; (2) bind `d` at a constant sandbox path with rewritten argv; (3) count opens outside `d` under all of
`root`, plus trace stat/readlink/getxattr or amend the advertised "parsed" to "opened under fx|btmp"; (4)
verdict via exit code/fd, not stdout; (5) pin the fence's git env in `run_fence` itself.

## Receipts (in this dir; SHA256SUMS)

`runA-killshot.out` — real counter, `PREDICATE C1 pass` on the forged fence (ENVELOPE unchanged, exit 0).
`runB-nokill.out` — same fence minus `os.unlink`, `read=10 contradicted=10 PREDICATE C1 fail`.
`fence-*.py` — the seven test fences. `mini-driver.py` — calls the real `run_fence`/`HARNESS`. Driver outputs:
`f_hostread → BREACH opens=0 'host-read plazir27 200'`; `f_modsread → BREACH opens=0 'mods-read 28 …'`;
`f_stat → BREACH opens=0 'stat-ok n=5 rl=/usr/bin/python3.14'`; `f_spoof → BREACH opens=0 'planted-by-print\nADMIT'`;
`f_logkill2 → BREACH opens=0 'read-then-erased secret=OUTSIDE-SECRET'`; `f_logtrunc → ADMIT opens=1` (partial).
`kill-abs-strace.txt`/`kill-rel-strace.txt` — strace 7.2 evidence for B6. `keep-trunc-log.txt` — truncated-log
autopsy. Envelope used for runs A/B exactly as specified; no other counter/probe runs on this seat.

VERDICT: c1-predicate-bypasses-7-verdict-changing-6
