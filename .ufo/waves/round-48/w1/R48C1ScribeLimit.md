# R48C1ScribeLimit — scope limitations for the round-48 C1 result

REV a543d92083557dd9b33ee674e9b99b03411f80af

Axes named: **calibration** (the R48-C1 claim axis) and **evidence-integrity** (this report's own axis).
This seat moves neither axis and claims no R48-C1 admission. Bounds served: read-only clone at the frozen base,
one scratch tree under `/fast/scratch/hyaku/kengaku-r48/R48C1ScribeLimit` (removed before yield), this report.

Measured revision: every quote below is from the tree at `a543d920` (stage-1 freeze commit). Lane `HEAD` at
measurement time was `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; the diff `a543d920..HEAD` is 5 files, all under
`.ufo/waves/round-48/` (dispatch/ready), and `plans/fixture_fence.py` is byte-identical at both revisions:
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

## Gate: freeze present, stage 2 absent, no scored execution

- Stage-1 freeze exists and is an ancestor of `HEAD`:
  `a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 … and C2 …`;
  `git merge-base --is-ancestor a543d920 HEAD` → exit 0. Tree `e91c8156c64031483529035923ee1182dcfff31d`;
  `plans/round-48-claims.md` git blob `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`, sha256
  `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672` (both are the same bytes; the peer's
  `3a9c71f3` is the git object id, not a conflicting digest).
- It predates every wave-1 measurement: the wave dispatch commits are `453ddfdb` (08:29:18 -0300) and
  `bf783c1e` (08:29:33 -0300), i.e. 1h36m after the freeze.
- Stage 2 has not happened. `plans/round48_c1_verify.py` does not exist at `a543d920` or at `HEAD`
  (`git cat-file -e` → `fatal: path … does not exist`), so the literals `<P> <H> <S> <B> <M>`, the v3 counter
  code, the frozen honest population and the before-control receipts are all still unwritten.
- `.ufo/waves/round-48/claims/` contains only `README.txt` and `freshness-r48.txt`; no control receipt exists.
  `.ufo/waves/round-48/w1/` at 08:34 -0300 held C1 connector/static reports and one honest-store report, but no
  scored counter receipt.
- Therefore this seat made **no scored counter or probe execution** — not a refusal to run, but the frozen
  prerequisite is absent. There is no round-48 C1 result at any revision yet; the limits below bind the predicate
  as frozen and any future pass measured on the landing tip.

## Named limits

Ordering: L1–L3 bound what the population can prove; L4–L6 bound what "no outside access" is measured to mean;
L7–L9 bound what the verdict says about admission and sensitivity; L10–L13 bound environment, identification and
comparability. Each line states the licence and the forbidden reading.

### L1 — Population-bounded verdict, not universal filesystem safety

The predicate is a finite sample: `REFUSALS total=20`, `SEALED total=<S>`, `HONEST fixtures=<H>` with
`CALIBRATION advertised=<20+S>` (`plans/round-48-claims.md:59-65`). Nothing quantifies over repositories, argv
shapes, filesystem types or hostile mechanisms outside that sample.
**Licensed:** "on the frozen H/20/S inputs, decisions match the frozen expectation with zero counted outside access."
**Not licensed:** "the fence admits every ordinary git repository", "the fence refuses every hostile fixture",
"fixture discovery is filesystem-safe". Round 46 is the proof of the gap: the predicate passed at `264b7757` while
`w2/R46W2C1HoHonest.md` — an override probe by its own words, not a frozen receipt — measured 9/9 ordinary classes
refused, and `w2/R46W2C1HoArgv.md` measured 2 admitted. The 9/9 number is fence-behaviour evidence, not a Q22
pinned-run measurement.

### L2 — The honest population is re-authored, not the original fixtures

The 9 round-46 classes are "each rebuilt from its `w2` report description" and the wave-1 classes are "authored
against the *base* fence description, not against any repaired fence" (`plans/round-48-claims.md:49-50`).
**Licensed:** the repaired fence admits these reconstructions and these description-derived classes.
**Not licensed:** byte-equivalence to the round-46 fixtures (the originals lived only in scratch, not committed);
independence of the honest classes from the fence author's reading of the same description. A repair tuned to the
description can pass the population while still refusing an ordinary layout the description did not enumerate.

### L3 — The honest leg is acceptance-only; over-admission is bounded by the hostile sample

`HONEST fixtures=<H> admitted=<H> refused=0` plus `REFUSALS clean=20` and `SEALED clean=<S>` is a two-sided check
only to the extent the 20+S hostile modules are representative. A fence that admits everything fails the hostile
legs; a fence that admits a hostile class not represented in them is not seen. `CALIBRATION advertised=<20+S>`
counts only hostile modules — the round-46 counter defines it as "the number of frozen hostile modules on which the
fence's observed behaviour contradicts that advertisement" (`plans/round46_c1_verify.py:7-9`).
**Not licensed:** reading `contradicted=0` as "the advertisement holds"; the line's name overstates its domain.

### L4 — "No outside access" is measured over the scratch root only

The inherited contract counter names the boundary: "host paths outside the scratch root are not counted, so a fence
may still read `/etc`, `/proc` and `/sys` while deciding — the advertisement says 'without reading outside d' and
this counter measures the scratch root only" (`plans/round46_c1_verify.py:83-86`).
**Licensed:** no counted access to paths outside `d` that lie under the scratch root.
**Not licensed:** the advertisement sentence "without reading outside `d`" in its general sense; any claim about
`/etc`, `/proc`, `/sys`, the interpreter's own imports, or host state.

### L5 — Untraced kernel channels remain untraced

The inherited counter's own limits: "io_uring SQE opens/reads emit no traced syscall (B7, not exploited here; the
counter does not block `io_uring_*`)" (`plans/round46_c1_verify.py:83-84`). The trace set is a fixed syscall
allowlist (`TRACE_SET`, `:194-205`), and a missing/empty log counts as READ, never as zero.
**Licensed:** absence of outside access through traced open/stat/access/readlink/xattr/exec/write calls.
**Not licensed:** absence of outside access through io_uring, or through any syscall outside the allowlist. This is
the sharpest gap between "fixture-population performance" and "universal filesystem safety": the counter cannot see
an access mechanism it does not name, and the r48 deltas do not add one.

### L6 — Path containment, not backing-store containment

The trace records path names, not device or inode identity; a directory stat is admitted with `st_nlink` nulled by
padding "not measured" (`plans/round46_c1_verify.py:86`). The round-46 source review records the consequence:
"lexical containment is not backing-store containment" (`w2/R46W2C1Intent.md:9-11`) — at the base fence `_tree`
rejects symlinks/special files but never checks mount identity. The r48 work item narrows the mount question to an
admission rule: an honest fixture on a mount boundary "is admitted iff every byte the decision reads is inside `d`"
(`plans/round-48-claims.md:70-72`).
**Licensed:** every read the decision performs names a path inside `d`; admission of an in-`d` mount boundary under
that byte-path rule.
**Not licensed:** that the bytes behind a mount point live on storage inside `d`. A bind mount is path-inside,
backing-outside, and every leg of the predicate would still print clean.

### L7 — Admitted store files are not content-validated (declared trust boundary)

`plans/fixture_fence.py:36-38`: "`.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*` and pack files are admitted
by name and size without content validation: the tool run behind this fence reads none of them for a path (named
limit)".
**Licensed:** a store whose path *shape* matches plain `git init` output; hostility is decided by names, sizes, link
counts and the strict `config` parser.
**Not licensed:** content safety of those files, or safety of any downstream tool that does resolve a path from a
pack, index, reflog or description. The result is a classify-time shape property, not a data-safety property.

### L8 — `leaked=0` is a behaviour claim, not an admission claim; `BENIGN` is unbounded

Delta (b): a result is `LEAK` "only if traced opens/reads outside `d` are observed"; a `touches=0` admission is
`BENIGN-ADMIT`, "counted separately, never as a leak", and "the kill rule keys on hostile behaviour, not on
admission" (`plans/round-48-claims.md:51-53`). The predicate prints `BENIGN total=<B>` "(informational only)"
(`:63`) with no bound on `<B>`.
**Licensed:** no admitted input produced traced outside access; argv/store exactness is not certified.
**Not licensed:** "no hostile fixture was admitted", or "argv tokens were accepted only in the exact contract
shape". A fence can benign-admit out-of-contract inputs while the predicate passes, provided no HONEST refusal and
no hostile traced access occur.

### L9 — Mutation sensitivity is a floor, not a certificate

The kill rule requires "fewer than half caught" to fail, with `<M>` ≥ 12 (`plans/round-48-claims.md:75-77`); a pass
therefore tolerates up to `floor(<M>/2)` surviving single-edit fence mutants. Round 46 measured "13 valid one-edit
mutants run; 2 killed, 11 survived" (`w2/R46W2C1MutFence.md`). Counter mutants are outside the r48 kill rule; the
round-46 spot-check routed "1/6 counter mutants" caught as still-open evidence
(`corpus/lessons/round-46-verifier-spotcheck.md`, Routed defects 1).
**Licensed:** at least half of the wave-1 authored single-edit fence mutants were detected.
**Not licensed:** the counter detects arbitrary fence regressions, multi-edit rewrites, or its own counter-side
mutants. The instrument's calibration is not established by the claim's predicate.

### L10 — Classifier measured, downstream tool run not measured; Linux-only envelope

The traced object is `breach` inside a read-only sandbox; the harness carries only the decision, `10 BREACH`,
`11 ADMIT`, anything else ERROR, and "stdout is never parsed" (`plans/round46_c1_verify.py:63-64`). `run_fence`
invokes `strace -f -qq -y -s 256` around `harness.py / fence.py / d / tool / argv` (`:361-400`), with a 120 s
timeout and fixed caps (`ENTRY_CAP`, `REPO_CAP`, `CONFIG_CAP`, `TEXT_CAP`, `INDEX_CAP`).
**Licensed:** the fence's decision function has the stated behaviour in this Linux envelope.
**Not licensed:** that the subsequent anchored `git` run stays inside `d`; portability (bwrap, strace, Linux
`lstat` semantics, `/usr/bin/python3` are hard requirements, and a missing tool prints `SETUP` and exits 2);
behaviour on pathological-but-ordinary inputs above the caps (those are policy refusals, not hostility, and the
predicate does not distinguish them from a correct refusal).

### L11 — The subject is not pinned; receipts identify it only by REV and the printed fence digest

The round-46 contract states the fence is "Subject (not pinned, it is the work)"
(`plans/round46_c1_verify.py:13-14`). The counter prints `FENCE source=… sha256=…` but compares it to no literal;
`PINS mismatched=0` pins inputs and the imported counter, not the measured fence. The testing overrides
`--refusals/--sealed/--fence/--seed` are declared to print "the predicate of the inputs they name (never a receipt
for the frozen run)" (`:86-88`), and per-run names use a random token unless `--seed` is fixed.
**Licensed:** a receipt plus its `REV` line and `FENCE … sha256=` line identifies the measured fence and inputs.
**Not licensed:** a score receipt without those lines; bit-identical re-derivation of a token-randomised run; any
override run (single-module probes, `--fence` mutants) as a predicate receipt.

### L12 — No race, concurrency or foreign-filesystem coverage

Fixtures are built, then classified, then returned; the fixture is not mutated between classification and use inside
the measured window, and no concurrent writer is part of any leg. Filesystem families outside the test host
(overlayfs, btrfs subvolumes, NFS, FUSE, case-insensitive or normalising filesystems) and git states outside the
plain-init allowlist (linked worktrees, `commondir`, alternates, commit-graph, shallow, replace refs) are absent from
the frozen population unless stage 2 adds them.
**Not licensed:** TOCTOU safety, safety under an adversarial concurrent writer, or universal portability. In-`d`
linked-worktree and alternates layouts are already named as ordinary over-refusal candidates by static review
(`.ufo/waves/round-48/w1/R48C1HoStore.md`: "an ordinary, wholly in-`d` metadata layout is an over-refusal
candidate"), and no measured leg currently covers them.

### L13 — The r48 verdict is not commensurable with round-46 admission counts

Round 46's kill rule fired on ≥2 held-out admissions; r48 replaces it with traced outside access and classifies
`touches=0` admissions as `BENIGN-ADMIT` (`plans/round-48-claims.md:45-53`). A r48 pass therefore does not mean
"the round-46 admission finding is gone" on the same measure — it means the new measure found no traced outside
access. The 3 round-46 benign admissions remain un-refuted as admissions by construction.
**Not licensed:** cross-round calibration trend claims, or "fixed the 3 held-out admissions".

## Findings for the L1 (not edits, not scores)

1. **SEALED/BENIGN mapping is unpinned in the frozen text.** Delta (b) applies BENIGN-ADMIT to "a fixture result",
   while the predicate still requires `SEALED total=<S> clean=<S> leaked=0` (`plans/round-48-claims.md:52-65`). If
   the v3 counter classifies a `touches=0` admission in the SEALED leg as BENIGN, `clean=<S>` cannot print; if it
   classifies it as LEAKED, the SEALED line still fails. Either way an admitted sealed module fails, but the text
   does not say so in one sentence. The v3 counter must resolve this without changing a frozen predicate line
   (freeze shape, `:20-29`); this is a wording hole, not a licence to re-label.
2. **`CALIBRATION advertised=<20+S>` does not measure the advertisement.** It counts contradictions over hostile
   modules only. Reports should not describe `contradicted=0` as "the advertised property holds".
3. **No r48 C1 result exists yet.** Stage 2 is absent (`plans/round48_c1_verify.py` missing at `a543d920` and
   `HEAD`), so `<P> <H> <S> <B> <M>` are all unfixed and no before-control receipt exists. Any statement of a r48
   C1 score at this revision would be fabricated; the limits above are prospective and bind any future pass on the
   landing tip.
4. **Population-vs-universal gap is structural, not fixable by more fixtures.** Every named limit above is an axis
   along which a finite, author-derived population cannot establish universal filesystem safety: untraced channels,
   untraced host paths, backing-store identity, unvalidated file content, and unlisted ordinary layouts. The honest
   framing for a r48 pass is "fixture-population performance under the frozen v3 counter", never "filesystem-safe
   fixture admission".

## Commands run (exact, with observed output where it is evidence)

All git fixture calls used `git -C <abs path>`; the only clone is inside this seat's scratch.

```
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1ScribeLimit && cd … && export TMPDIR=$PWD
  → df /fast: /dev/nvme1n1p2 804G 401G 403G 50% /fast
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' a543d920…
  → a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 … C2 …
git -C … log --format='%H %ci %s' a543d920..HEAD
  → bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767 2026-10-27 08:29:33 -0300 round-48: w1 ready handoff marker
    453ddfdb4e8f69068aaf25084756188012cfcb10 2026-10-27 08:29:18 -0300 round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)
git -C … merge-base --is-ancestor a543d920… HEAD → exit 0 (IS_ANCESTOR_OF_HEAD)
git -C … status --porcelain → 3 lines: ?? .ufo/waves/round-48/claims/  ?? .ufo/waves/round-48/w1.ready.partial  ?? .ufo/waves/round-48/w1/
git -C … rev-parse HEAD → bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane && git -C lane checkout a543d920…
  → git -C lane rev-parse --show-toplevel → /fast/scratch/hyaku/kengaku-r48/R48C1ScribeLimit/lane
git -C lane rev-parse a543d920^{tree} → e91c8156c64031483529035923ee1182dcfff31d
sha256sum lane/plans/round-48-claims.md → 87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672
sha256sum lane/plans/fixture_fence.py → 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
sha256sum lane/plans/round46_c1_verify.py → ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508
git -C … show HEAD:plans/fixture_fence.py | sha256sum → 05d5fe03… (identical at HEAD)
git -C … cat-file -e a543d920:plans/round48_c1_verify.py → fatal: path … does not exist
git -C … cat-file -e HEAD:plans/round48_c1_verify.py → fatal: path … does not exist
git -C lane remote -v → origin /home/vgpnk/Projects/shokunin/kengaku-shokunin (fetch/push)
ls plans/refusals46 | wc -l → 20;  ls plans/sealed46 | wc -l → 12
ls plans/battery42 → 5; plans/battery43 → 7; plans/battery44 → 10 (22 modules / 104 fixtures per counter)
```

No counter, probe, fixture, or git mutation was run; no file in the lane was written; nothing was committed or
pushed; no tool was installed or updated. Scratch tree removed at close (see VERDICT).

## Sources opened (access date 2026-10-27; quotes ≤25 words; local `file://` URLs — origin is the local lane)

| source | URL | located quote |
|---|---|---|
| frozen claims | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` | "a fixture result is `LEAK` only if traced opens/reads outside `d` are observed" (§C1 b) |
| claims, honest population | same | "each rebuilt from its `w2` report description"; "authored against the *base* fence description" (§C1 a) |
| claims, predicate/kill | same | "`BENIGN total=<B>` (informational only)"; "the kill rule keys on hostile behaviour, not on admission" |
| claims, mount work item | same | "admitted iff every byte the decision reads is inside `d`" (§C1 Work) |
| routed defect source | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` | "repair over-refusal (9/9 novel honest controls refused) and broaden positive controls" |
| spot-check routed defects | same | "mutation evidence is only 2/13 fence mutants and 1/6 counter mutants caught" |
| fence, named limit | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` | "admitted by name and size without content validation" (`:36-38`) |
| fence, allowlist proof | same | "Nothing is admitted until every byte the decision depends on has been classified" (docstring) |
| counter, calibration count | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` | "The calibration count is the number of frozen hostile modules on which the fence's observed behaviour contradicts that advertisement" |
| counter, named limits | same | "host paths outside the scratch root are not counted"; "io_uring SQE opens/reads emit no traced syscall" (`:83-86`) |
| counter, subject | same | "Subject (not pinned, it is the work)" |
| round-46 honest refusals (override probe; predicate fail expected by its own text) | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1HoHonest.md` | "9/9 were refused, with no outside touches" |
| round-46 admission finding | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1HoArgv.md` | "both fixtures as `ADMIT`, `touches=0`" |
| round-46 mutation | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1MutFence.md` | "13 valid one-edit mutants run; 2 killed, 11 survived" |
| round-46 intent | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1Intent.md` | "lexical containment is not backing-store containment" |
| scorecard | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md` | "the repaired fence over-refuses ordinary repositories and its counter leaves most fence checks unwitnessed" |
| wave-1 honest-store (untracked) | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1HoStore.md` | "an ordinary, wholly in-`d` metadata layout is an over-refusal candidate" |

## Limits of this report

- Source-inspection and committed-receipt review only. No counter, probe, fixture or mutation was executed; every
  behavioural statement above is either quoted from a committed receipt/report or marked as a structural consequence
  of the frozen text.
- The wave-1 file cited (`R48C1HoStore.md`) is untracked and may change after this reading; its quote is recorded as
  observed at 08:34 -0300.
- Round-46 wave-2 measurements cited here (HoHonest 9/9, HoArgv 2 admitted, MutFence 2/13) are override probes by
  their own text, not frozen predicate receipts; they are used as fence-behaviour evidence only. Their receipt
  headers predate the round-48 Q22 `REV` discipline, so they are not cited as `REV`-pinned runs.
- No external network source was opened; all URLs are `file://` locators into the lane or wave tree.
- This report does not measure the fence, does not compare repaired variants, and makes no R48-C1 or R48-C2
  admission judgment.

## Touched surfaces

- Read-only clone at `/fast/scratch/hyaku/kengaku-r48/R48C1ScribeLimit/lane` (removed).
- Wrote only this report: `kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ScribeLimit.md`.
- No production file, plans file, corpus file, SCORECARD, LOG, MANIFEST, `.ufo/state`, or other seat path written.

VERDICT: scope-limits-named (13), no-score (stage-2 freeze absent at `a543d920` and `HEAD`), no-admission; scratch
removed before yield.
