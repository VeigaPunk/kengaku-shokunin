# R49C1ScribeLimit — R49-C1 scope limitations (named limits only)

Seat: `R49C1ScribeLimit` (scribe). Item: draft the exact scope limitations of the r49 C1 result —
**fixture-population performance vs universal filesystem safety** — named limits only.

Axes named: **calibration** (R49-C1). No other axis claimed; this seat changes no production byte.

Contract read before any work (local files only, no URL opened):

| source | line | located quote (≤25 words) |
|---|---|---|
| `plans/round-49-claims.md` | 88 | “an honest fixture whose store sits on a mount boundary inside `d` is admitted iff every byte the decision reads is inside `d`” (23 words) |
| `plans/round-49-claims.md` | 59 | “`touches=0` is `BENIGN-ADMIT`, counted separately, never a leak” (9 words) |
| `corpus/lessons/round-48-verifier-spotcheck.md` | 73 | “the candidate's ≥12-mutant kill battery was never reported … needs the mutation floor committed with receipts” (16 words) |
| `plans/round46_c1_verify.py` (the inherited counter contract) | 83-85 | “host paths outside the scratch root are not counted, so a fence may still read `/etc`, `/proc` and `/sys` while deciding” (23 words) |
| `plans/round46_c1_verify.py` | 83 | “io_uring SQE opens/reads emit no traced syscall (B7, not exploited here” (11 words) |
| `.ufo/waves/round-46/w2/R46W2C1Intent.md` | 9 | “lexical containment is not backing-store containment” (6 words) |
| `.ufo/waves/round-48/w1/R48C1ExecFenceA.md` | 99 | `HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0` (measured line, base fence) |

No remote source was opened by this seat, so no URL/access-date row applies; every citation above is a
committed lane path read at the revision stated below.

---

## 0. Freeze gate and measurement boundary (verified before drafting)

The stage-1 freeze exists in the committed lane tree and predates the round's measurements. Commands and
observed output, verbatim:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ git -C … cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C … log -1 --format='%H %an %ad %s' 9d2900af…
9d2900af41e4d1fc6022eff99010436fde6dbd93 kengaku-shokunin Tue Oct 27 09:58:06 2026 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git -C … log --oneline 9d2900af..HEAD
af88aab round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)
$ git -C … ls-tree -r 9d2900af --name-only | grep -E 'round-49|fixture_fence|round46_c1'
plans/fixture_fence.py
plans/round-49-claims.md
plans/round46_c1_verify.py
   (plus round-45/round-46 wave-side copies of these files; no other plan-level C1 path)
$ git -C … ls-tree -r HEAD --name-only | grep -E 'round49|honest49|sealed49|mutants49'
   (no output)
$ git -C … diff --stat 9d2900af..HEAD -- plans/round-49-claims.md
   (no output)
$ sha256sum plans/fixture_fence.py plans/round-49-claims.md
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  plans/round-49-claims.md
$ git -C … show 9d2900af:plans/fixture_fence.py | sha256sum
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
$ git -C … show 9d2900af:plans/round-49-claims.md | sha256sum
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  -
$ git -C … status --porcelain
?? .ufo/waves/round-49/w1.ready.dispatched
?? .ufo/waves/round-49/w1/
$ uname -r; strace -V | head -1; stat -f -c '%T' /fast/scratch; id -u
7.2.11-arch1-1
strace -- version 7.2
xfs
1000
```

Freeze verdict: **present and prior.** `9d2900af` is a commit dated 2026-10-27T09:58:06-0300; the round-49
wave launch is `2026-10-28T08:59:38-03:00` (`plans/round-49-claims.md:10`). The freeze's claims bytes are
identical to the worktree (sha256 `7292f4e0…`), and the base fence is byte-identical at the freeze and at
HEAD (`05d5fe03…`).

**Stage 2 does not exist at this revision.** HEAD `af88aab1` contains no `plans/round49_c1_verify.py`,
`plans/honest49/`, `plans/sealed49/` or `plans/mutants49/`. Consequently `<P>`, `<H>`, `<S>`, `<B>` and `<M>`
are unresolved, and **there is no C1 number yet to be limited**. This seat made no scored counter run
(none is runnable) and claims no admission; every limit below is **contract-derived** from the frozen text
plus the committed counter/fence sources, and binds whatever stage 2 produces.

REV of the tree inspected (lens, not a receipt): `REV af88aab193e6034cb9b386472064e3c18fa90128`,
tracked tree clean; only the untracked wave paths above. Freeze `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`.

---

## 1. What a C1 pass would establish (one sentence, so the limits have a referent)

On a clean clone of the landing tip, on this host, over the frozen `<H>`-fixture honest population and the
frozen `20+<S>`-module hostile population, the fence module's `breach()` decision process — under the
counter's fixed syscall-trace envelope over scratch-root paths — admitted every honest fixture with zero
counted outside touches, refused every hostile module with zero counted touches, and caught at least
`<M>/2` of `<M>` declared fence mutants.

That is a **fixture-population performance** statement. It is **not** a universal filesystem-safety
statement; limits A1–C20 below name every reason, with the exact mechanism and evidence for each.

---

## 2. Named limits

Group A — the measured object is a frozen, author-built population.
Group B — the measurement channel sees a bounded slice of behaviour.
Group C — what the receipt can and cannot certify.

### A1 — FROZEN-FINITE-POPULATION

- **Bound.** The honest leg is an exact count over an enumerated set: the 104 fixtures of
  `plans/battery42|43|44` (22 modules) + the 16 rebuilt r46/r48 honest classes + the wave-1 novel honest
  classes, all committed and digest-pinned at stage 2 (`plans/round-49-claims.md:54-57`). The predicate is
  equality (`fixtures=<H> admitted=<H> refused=0`), not a floor.
- **Evidence.** claims:54-57, 73-79; inherited `REFUSAL_FLOOR=20`, `SEALED_FLOOR=12`, `HONEST_TOTAL=104`
  (`plans/round46_c1_verify.py:190-192`); r48 measured 120 fixtures on the same machinery
  (`R48C1ExecFenceA.md:99`).
- **Excludes.** Any claim about a fixture outside the frozen set, about real-world repositories at large, or
  about class space the authors did not enumerate. There is no random sample and no confidence interval;
  “admitted `<H>`/`<H>`” is a census of `<H>`, not an estimate over repositories.

### A2 — AUTHOR-OVERLAP, DESPITE PRE-REGISTRATION

- **Bound.** The population is frozen at stage 2, before any claimed work is scored, and the honest novel
  classes are authored against the **base** fence description — this blocks post-hoc population fitting.
  It does not create independence: population, hostile modules and the fence all come from the same lane
  and wave, and their authors know the base fence and the class list.
- **Evidence.** claims:19-25 (stage 2 ordering), 54-57 (novel classes authored against the base fence
  description); r48 provenance `R48C1ExecFenceA.md:1061` (“85 `anchor`, 35 `order`; 0 duplicate `fid`”).
- **Excludes.** Any inference that the population is representative of git shapes the authors did not
  imagine; a class outside the authors' enumeration is untested no matter how many fixtures pass.

### A3 — HOSTILE-SET

- **Bound.** `REFUSALS` is exactly the 20 frozen `plans/refusals46/` modules; `SEALED` is the 12 frozen
  `plans/sealed46/` modules plus `<S>` wave-1 held-out modules authored against the **landed** candidate.
  `CALIBRATION advertised=<20+S> contradicted=0` counts only those modules (`plans/round-49-claims.md:73-79`).
- **Evidence.** claims:62-64; `REFUSAL_FLOOR = 20`, `SEALED_FLOOR = 12`
  (`plans/round46_c1_verify.py:190-191`).
- **Excludes.** Resistance to hostile classes outside the frozen set; “contradicted=0” is a count over
  `20+S` modules, not an attack-surface coverage measure. The sealed modules are held out from
  fence-writing seats but are still authored inside the same round.

### A4 — COUNT-LITERALS, NOT REPRESENTATIVENESS

- **Bound.** Non-vacuity is enforced by exact literals and per-path pins, re-checked after the run
  (`after = [… sha256(lane / rel) != dig]`, then `pins-after` in `fails`,
  `plans/round46_c1_verify.py:607-612`). An empty or shrunken directory fails; a *padded* or *duplicated*
  population is not detected.
- **Evidence.** counter:190-192 and 607-612; `pin_issues` also flags hostile inputs missing from `PINS`
  in default mode (counter:464-471).
- **Excludes.** Any guarantee that the `<H>` honest classes are distinct, hard, or representative, or that
  the `20+S` hostile classes cover distinct techniques. The literals constrain quantity and pin integrity,
  not class quality.

### A5 — BENIGN-ADMIT: VERDICT, NOT JUSTIFICATION

- **Bound.** On the honest leg, `admitted` counts exactly `ADMIT` rows with zero outside touches
  (`h_adm = sum(_v == "ADMIT" and not _o …)`, counter:598). The r49 delta names a touch-free admission
  `BENIGN-ADMIT`, counts it separately, and never calls it a leak (`plans/round-49-claims.md:59`). Nothing
  checks that the admission was *justified* by the advertised facts.
- **Evidence.** counter:598-606; claims:58-59; r48 admit-all control printed
  `HONEST fixtures=120 admitted=120 refused=0` and passed the honest leg, failing only on
  REFUSALS/SEALED (`R48C1ExecFenceA.md:123-129`).
- **Excludes.** Any claim that a passing fence reasons correctly, minimally, or non-accidentally on honest
  fixtures. A blanket-admit policy satisfies the honest leg by construction; only the hostile legs
  discriminate.

### A6 — FENCE CONSERVATISM: CAPS AND HARDLINKS

- **Bound.** The fence refuses by design above `ENTRY_CAP=200000` walked entries, `REPO_CAP=64` repos,
  `CONFIG_CAP=1 MiB`, `INDEX_CAP=16 MiB`, `TEXT_CAP=64 KiB`, and any regular file with `st_nlink>1`
  (`_linked`, `plans/fixture_fence.py:113-115`, called at `:286,:306,:353`; the inline `st_nlink > 1` rejection in `_tree` at `:216`).
- **Evidence.** `plans/fixture_fence.py:45-49,113-115,185-186,216,218-219`.
- **Excludes.** Any statement that `refused=0` means “the fence admits all legitimate fixtures”. It means
  “no frozen honest fixture hits a cap or a hardlinked store”. A legitimate fixture above a cap, or with a
  hardlinked object, is refused by design and is outside the measurement unless the frozen set contains
  that class.

### B7 — OUTSIDE-SCRATCH-ROOT (the central gap)

- **Bound.** `_outside(p, d, root, ctl)` counts a touch only when the normalized path is `root` or under
  `root`, and not under `d` or `ctl` (counter:292-298). Reads of `/etc`, `/proc`, `/sys`, `$HOME`, the lane
  (hidden), or any host path outside the scratch root are **never counted**.
- **Evidence.** counter:292-298 and the inherited limit sentence at counter:83-85; `analyse()` documents
  its hits as “outside `d` under the scratch root” (counter:300-303).
- **Excludes.** The advertised property “deciding without reading outside `d`” is measured only **inside
  the counter's scratch root**. A fence that reads arbitrary host paths while deciding is indistinguishable
  from a clean one. This is the exact boundary between the claim's fixture-population performance and
  universal filesystem safety.

### B8 — PATH-STRING, NOT BACKING STORE

- **Bound.** Paths are assembled and normalized lexically; dirfd-relative names resolve against the
  `fd<dir>` annotation or cwd `d` (counter:269-290). There is no `st_dev`/inode comparison anywhere in the
  analysis. A bind mount or overlay mounted **inside** `d` is read at a path under `d` and is never a hit.
- **Evidence.** counter:269-298 (no device check); `.ufo/waves/round-46/w2/R46W2C1Intent.md:9`: “lexical
  containment is not backing-store containment”, with the fence's `_tree` shown lstat-only
  (`plans/fixture_fence.py:179-220`).
- **Excludes.** Any enforcement of the freeze's mount-boundary sentence (claims:88) by the counter. The
  freeze states the rule for the fence; the counter has no device/inode channel to observe a violation, so
  mount-boundary conformance rests on source inspection of the fence, not on the C1 receipt.

### B9 — TRACE-SET (fixed syscall list)

- **Bound.** Only `TRACE_SET` is traced (counter:196-214): open/openat/openat2/creat; stat/lstat/newfstatat/
  statx/statfs/statfs64; access/faccessat/faccessat2; readlink(at); getxattr/lgetxattr/listxattr/
  llistxattr; inotify_add_watch; name_to_handle_at/open_by_handle_at; execve(at); and the write-side family.
  Not traced and not blocked: `io_uring_*` (the r46 header names this as B7, “not exploited here”);
  `read`/`readv`/`mmap`/`splice`/`sendfile`/`copy_file_range`; network calls (the sandbox also passes
  `--unshare-net`); `fanotify_*`, `pidfd_*`.
- **Evidence.** counter:196-214, 83-85; sandbox `--unshare-net` in `plans/round44_c1_verify.py:341-357`.
- **Excludes.** Any claim that the fence cannot read or exfiltrate by an untraced channel. An `io_uring`
  read of an outside path would succeed under `--ro-bind / /` and produce no hit; the counter cannot
  detect it, by its own header.

### B10 — FD RE-USE IS NOT READ ACCOUNTING

- **Bound.** The harness closes every fd above 2 before calling `breach` (`os.closerange(3, 1024)`,
  counter:220), so no inherited fd exists at entry. But `read` is untraced: an fd counts only at its opening
  call, and nothing counts how many bytes were read, or whether the file was read at all.
- **Evidence.** counter:220, 196-214.
- **Excludes.** Byte-level or content-level reading claims. “Opened” is the measured predicate; “read” is
  inferred, and the frozen contract's word “reads” (claims:58) is realised as traced opens/stat/access.

### B11 — DIRECTORY STAT AND `st_nlink`

- **Bound.** A successful stat-family call on a real non-symlink directory is skipped (rule g,
  counter:306-340, skip at `:328`), and the r46 header states the `st_nlink` channel is “nulled by padding,
  not measured” (counter:83-88).
- **Evidence.** counter:328, 83-88; padding `PAD = 24` (counter:193).
- **Excludes.** Detection of directory-existence probes and entry-count probing. Padding removes the
  *signal* from `st_nlink`; it does not make directory stats observable, so a fence can count entries of an
  outside directory and stay at zero hits.

### B12 — FAILED CALLS AND THE WRITE SIDE

- **Bound.** For non-open calls, a touch counts only on success; `WRITE_FAMILY` errors (e.g. `EROFS` under
  the read-only sandbox) are **not** counted; an open failing `ENOENT` is not counted (“aimed at nothing”),
  while other open/access errnos (including `EACCES`) are (counter:306-340).
- **Evidence.** counter:306-340; read-only root `--ro-bind / /` in `plans/round44_c1_verify.py:341-357`.
- **Excludes.** Any measurement of whether the fence **would write** outside `d` if it could. The read-only
  sandbox, not the fence, prevents outside writes; the counter's write-side family cannot register a blocked
  write, so “zero touches” is not evidence of write restraint.

### B13 — LANE HIDDEN, SO “DOES NOT READ THE LANE” IS UNEVIDENCED

- **Bound.** The fence runs with an empty read-only bind over the lane
  (`hide_list((lane,), existing=True)`, counter:361-375, `plans/round44_c1_verify.py:341-357`). Probes of
  the lane's contents fail `ENOENT`, and the lane path itself is outside the counted scratch root (B7), so
  any touch on it is uncounted either way: the sandbox, not the counter, keeps the fence away from the
  counter source. The Q39 name-hiding argument is therefore enforced by the sandbox, not demonstrated by a
  zero-touch result.
- **Evidence.** counter:361-375; counter:83-88 (B3 scope).
- **Excludes.** Any statement about the fence's disposition to read the lane or the counter if reachable.
  Inside the harness it cannot; outside it, the result says nothing.

### B14 — SUBJECT IS THE MODULE API, NOT THE PRODUCT PATH

- **Bound.** The measured subject is `breach(d, argv, tool)` called by the harness with `cwd=d`,
  `tool` ∈ {`anchor`, `order`}, argv as JSON tokens, `HOME=/nonexistent`, fixed `PATH`, `python3 -I`
  (counter:215-228, 362-380; contract in `plans/fixture_fence.py:1-12`).
- **Evidence.** counter:215-228, 362-380; `breach` docstring “No git child is ever started”
  (`plans/fixture_fence.py:531-543`).
- **Excludes.** The production CLI/driver around `breach`, other `tool` values, other cwd/environments, and
  any post-admission execution of an admitted fixture. “No git child” is measured only for these inputs.

### B15 — SINGLE HOST, SINGLE FILESYSTEM, SINGLE KERNEL

- **Bound.** All results bind this host: kernel `7.2.11-arch1-1`, uid `1000`, scratch filesystem `xfs`,
  `strace 7.2`. `FENCE_TIMEOUT = 120` (counter:195) makes `hung=0` specific to this host's scheduling and
  the counter's job count.
- **Evidence.** observed host facts above; counter:194-195.
- **Excludes.** Other kernels, filesystems (overlayfs, btrfs subvolumes, NFS, case-folding or
  case-sensitive variants), mount namespaces, other uids or thread loads. A pass is one host's measurement.

### B16 — NO RACE, NO TOCTOU

- **Bound.** Each fixture is built once and handed once to the fence; the fence's sandbox is read-only;
  nothing mutates `d` between the decision and any later use.
- **Evidence.** counter:402-447 (build) and 361-400 (one run per fixture); read-only root
  (`plans/round44_c1_verify.py:341-357`).
- **Excludes.** TOCTOU, concurrent writers/adversaries, and fixtures whose shape changes after the walk.
  The mount and hardlink rules are static-shape checks, not race-hardening evidence.

### B17 — MUTANTS: SIGNATURE SENSITIVITY, NOT SAFETY-SPECIFIC SENSITIVITY

- **Bound.** `<M>` author-declared mutants (payload path + digest + description) are applied to a copy of
  the landed fence; a mutant is caught iff the mutated fence no longer prints the clean signature; the
  floor is `<M>/2`, `<M> ≥ 12` (claims:65-72, 73-79).
- **Evidence.** claims:65-72 (the leg is new in r49); r48 defect 4 requires the battery be committed with
  receipts (`round-48-verifier-spotcheck.md:73`).
- **Excludes.** (i) mutants not declared; (ii) mutants of the counter, harness, strace configuration,
  population or adjudication; (iii) safety-specific sensitivity — “caught” is *any* signature deviation, so
  a mutant that merely refuses an honest fixture is caught without being a safety regression, while a
  mutant that stays unsafe only in an unmeasured channel (B7, B8, B9, B12) is not caught; (iv) any coverage
  gain — the mutant leg re-measures the same three legs under the same channel limits. The `<M>/2` floor
  explicitly tolerates survivors.

### B18 — TESTING OVERRIDES ARE NOT RECEIPTS

- **Bound.** `--fence`, `--refusals`, `--sealed`, `--seed` are testing overrides; the predicate they print
  is the predicate of the inputs they name and never a receipt for the frozen run (counter:87-89, 482-486).
- **Evidence.** counter:87-89, 482-486.
- **Excludes.** Promoting any control, dev-harness or override run (including the r48 scratch candidate
  numbers) to the claim's pass line. Only the stage-2-pinned counter on a clean clone of the landing tip
  counts.

### C19 — STAGE-2-ABSENT AT THIS SEAT'S REVISION

- **Bound.** At `af88aab1` no `plans/round49_c1_verify.py`, `plans/honest49/`, `plans/sealed49/` or
  `plans/mutants49/` exists (verified above); `<P>`, `<H>`, `<S>`, `<B>`, `<M>` and every population/counter
  pin are unresolved. There is no C1 output to interpret, and this seat ran no scored counter.
- **Evidence.** the freeze-gate block in §0; claims:19-25 (stage 2 fills literals and pins only).
- **Excludes.** Any statement that C1 passed or failed, and any number-shaped claim about the r49 population.
  The limits above are contract-derived and remain binding after stage 2; if stage 2's counter changes a
  mechanism (e.g. adds a host-path channel or blocks `io_uring`), the corresponding limit must be re-derived
  from the amended source, not from this draft.

### C20 — REV-BOUND, SINGLE-RUN, NOT A CERTIFICATION

- **Bound.** A pass is a single-run statement at the measured `REV` on a clean clone of the landing tip;
  `TREE-BYTES` applies only if the clone is uncommitted (claims:30-32). Any later edit of the fence, counter,
  population, pins or host invalidates the receipt.
- **Evidence.** claims:30-32, 73-79.
- **Excludes.** Certification of `plans/fixture_fence.py` for the lane's discovery path, for other
  consumers, for other populations, or for any safety property beyond the three measured legs. No score
  change follows from this seat; the score decision is the L1's.

---

## 3. The one-line boundary this draft fixes

> **C1, if it passes, is a census of a frozen, author-built fixture population under a bounded syscall-trace
> channel on one host. It is not a proof of universal filesystem safety: the counter cannot see reads outside
> its scratch root (B7), cannot distinguish a bind-mounted backing store from a path inside `d` (B8), does not
> trace or block `io_uring` (B9), cannot see blocked outside writes (B12), and its honest leg accepts a
> touch-free blanket admission (A5).**

---

## 4. What this seat did not do

- No production file edited; no commit, push, jj/git mutation, or mutating git command anywhere.
- No scored counter or probe executed (none exists at `af88aab1`); no C1/C2 admission claimed; no score
  change asserted.
- No model or model alias named in this report or in any command; routing was not touched.
- No tool installed or upgraded; no pacman transaction attempted (host-wide pause respected).
- No subagent dispatched (leaf member).
- Scratch: `/fast/scratch/hyaku/kengaku-r49/R49C1ScribeLimit` was created for this seat; no clone or fixture
  git call was made (all reads were `git -C <lane>` / `read` on the lane). The directory was removed before
  this yield; `test -e` after removal printed nothing. No `/tmp` path is cited as evidence.

## 5. Limits of this seat's evidence

- The limits are derived from the frozen claims text and the **committed** inherited counter/fence sources;
  the stage-2 counter does not exist, so a mechanism could change at stage 2. Where that happens, the limit
  is re-derived from the amended source (C19).
- The r48 numbers cited (`HONEST fixtures=120 admitted=112 refused=8`) are the before-value from a committed
  seat report, not a run by this seat; they are used only to anchor the population's scale, not as an r49
  result.
- No outside verifier reviewed this draft.

**VERDICT: `c1-limits-drafted` — 20 named limits (A1–A6 population, B7–B18 channel, C19–C20 receipt); stage-1
freeze verified at `9d2900af` and prior to the wave; stage-2 counter/population absent at `af88aab1`, so no
scored run and no C1 number exists; no admission or score claimed; scratch removed.**
