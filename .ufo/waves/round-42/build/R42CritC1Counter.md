# R42CritC1Counter — can a dishonest battery make `round42_c1_verify.py` green?

Seat: `R42CritC1Counter` (critic, round 42 wave 1). Target:
`kengaku-shokunin/plans/round42_c1_verify.py` (sha256 `559fca0c…c6649`, the frozen digest in
`.ufo/waves/round-42/claims/frozen-digests.txt`) plus the two tools it pins
(`anchor_digest_check.py` `11bb2cad…`, `order_check.py` `948d5e1d…`). Lane clone at
`/fast/scratch/hyaku/kengaku-r42/R42CritC1Counter/lane` (tip `fda71ae0…`); nothing was committed there,
`git status --short` shows only the untracked attack `plans/battery42/`. Scratch
`/fast/scratch/hyaku/kengaku-r42/R42CritC1Counter` (`.ROUND-ROOT-SENTINEL` present). Attack modules and
receipts: `.ufo/waves/round-42/build/R42CritC1Counter/` (this report's directory). Every counter run below
was executed inside the Q32 envelope

```
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <command>
```

with `date +%T` and `ls -A /home/vgpnk/.local/bin | sha256sum` before/after in each `run-*.txt`
(`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` unchanged in every run,
17:24:22 → 17:30:01).

## 1. Headline: dishonest green REACHED

A battery of 14 new fixtures (`.ufo/…/R42CritC1Counter/battery/{b_anchor,b_order}.py`) reaches the
frozen predicate line on the lane clone with **three of its fourteen kills earned by fixtures that do not
demonstrate the advertised behaviour**. `run-predicate.txt`:

```
BATTERY fixtures=14 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=5/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
PREDICATE-EXIT 0
```

The three substitutes, with the frozen advertised sentence each is supposed to demonstrate:

| id | counter line (from `run-predicate.txt`) | advertised sentence | what the fixture actually does |
|---|---|---|---|
| `b-xo1-receipt-is-directory` | `MUTANT XO1 order rc-silence killed by=b-xo1-receipt-is-directory attributed=L183 hits=1` | “FAIL when the freeze commit (the first commit adding <claims>) already contains <receipt>” (`plans/order_check.py:17,183`) | `--receipt .ufo/waves/round-42/claims` is a **directory** the freeze commit contains because it contains the claims file. No receipt artefact exists anywhere in the history. `git cat-file -e <freeze>:<dir>` returns 0 for a tree (`order_check.py:183`). |
| `b-xo3-emptied-directory` | `MUTANT XO3 order rc-silence killed by=b-xo3-emptied-directory attributed=L188 hits=1` | “FAIL when <receipt> was committed before <claims> (pre-registration inverted …)” (`plans/order_check.py:18,188`) | `--receipt` is a directory created in commit 1, removed in commit 2, re-created after the freeze; `add_commit(git, dir)` returns commit 1 (`order_check.py:95`) and `merge-base --is-ancestor` fires though no receipt was ever committed. |
| `b-x13-staged-manifest` | `MUTANT X13 anchor rc-silence killed by=b-x13-staged-manifest attributed=L570 hits=1` | “`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts” (`plans/anchor_digest_check.py:73`) | Nothing is unpromoted: `file.txt` **and** its `SHA256SUMS` are committed. Only the manifest is staged, rewritten to assert a made-up digest equal to the row's token. HEAD mode prints `digest-unknown`; index mode accepts the staged manifest as a “view” of the committed capture (`anchor_digest_check.py:302-310`) → rc 0. The kill shows index mode trusting a staged digest that contradicts the committed bytes, not a capture promotion. |

A weaker X13 substitute (a staged `PROVENANCE.md` locator table; the capture is promoted) also killed X13 in
the first battery run (`MUTANT X13 … killed by=b-x13-staged-table attributed=L570`,
`run-battery.txt`), showing the gap is not one fixture's accident.

Attribution (leg f) does not discriminate here: the attributed spans are lines that execute on every
invocation — `order_check.py:183` (clause 1 is unconditional in `main`) and
`anchor_digest_check.py:570` (the `--evidence-ref` argument declaration). The freeze names exactly this
limit (“a kill records a result difference in the declared direction on a fixture that executes the mutated
line, not the fixture's intent”), so the three substitutes are **admitted by the frozen kill rule**; the
predicate alone cannot certify the advertised behaviours. The load-bearing gate for C1 is the non-author
review of `plans/battery42` that the freeze also names — my receipt shows why it must be exercised.

## 2. Vectors from the ticket, each tested under the envelope

### V1 — repo-local `.git/config` executes code during a tool run: **BLOCKED**

`probe/p_probe.py` fixture `p-config-external-commands` builds a clean order history and then sets
`diff.external=/bin/false`, a pager, `include.path=/dev/null`, `diff.drv.textconv=/bin/false`,
`sshCommand=/bin/false` in the fixture's own `.git/config` (keys assembled so the module passes the token
scan). `run-probes.txt`:

```
FIXTURE p-config-external-commands tool=order expect=accept declared=- observed_rc=0 observed=- ok
```

A failure of any invoked external program would have made the tool's `git log` raise and the run exit 2
(`Git.run`, `order_check.py:71-76`). The counter pins `core.fsmonitor`/`core.hooksPath`
(`round42_c1_verify.py:385-386`), but the decisive fact is the command set: the two tools issue only
`rev-parse`, `log --format=%H --diff-filter=A`, `rev-list`, `ls-tree`, `cat-file`, `merge-base`,
`ls-files` (`order_check.py:29-30`, `anchor_digest_check.py:187-205,374-398`). None of these runs
`diff.external` (needs `--ext-diff`), textconv (needs patch output), a pager (stdout is a pipe), hooks,
filters or an ssh transport. A fake `gpgsig` commit with `log.showSignature=true` and
`gpg.program=/bin/false` also left `GPG-LOG-RC 0` with empty stderr (`run-extra.txt`).
A definitive control (`run-config-exec.txt`) put an executable marker script in `diff.external`,
`core.pager`, `textconv`, `filter.*.clean/smudge`, `sshCommand` and an included `[alias]`, then ran each
command the two tools issue with the counter's env: `MID-MARKER absent` for all nine, and only the
explicit `git trick` alias invocation produced `MARKER-PRESENT` (so the payload itself works; no tool
command reaches it).
**Result: no configuration-driven program ran; no per-variant difference can be manufactured this way.**
The freeze's claim “these two tools run none (git plumbing only)” holds for code execution.

### V1b — config as a *data redirect* (`core.worktree`): **WORKS** (path_ok defeated)

Not code execution, but the same fixture lever. `run-p5.txt` builds a decoy repo `A` whose claims blob
contains a hit (would be rc 1) and a host repo `H` outside `d` with a clean history, then sets `A`'s
`core.worktree` to `H`:

```
REV-PARSE-TOP /fast/scratch/hyaku/kengaku-r42/R42CritC1Counter/p5/host
ORDER … ORDER ok … ORDER RESULT PASS
ORDER-RC 0
--- same decoy without the redirect ---
ORDER HIT .ufo/waves/round-42/claims/note.txt@59517620…:1 kind=gate-p10 `gate: P10 ok fresh probe output byte-equal`
ORDER-RC 1
```

`order_check.main` trusts `git rev-parse --show-toplevel` (`order_check.py:152`) and resolves the argv
paths against that root (`repo_path`, `:84-92`), while `path_ok` only checks the argv tokens against `d`
(`round42_c1_verify.py:343-355`) — the relative tokens exist inside `d` as decoys. `probe2/p_redirect.py`
turns this into an attributed kill whose scenario lives **outside** `d`. `run-extra.txt`:

```
FIXTURE p-redirect-host-repo tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT XO5 order rc-mirror killed by=p-redirect-host-repo attributed=L117 hits=1
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
```

This breaks the written contract (“No lane clone is offered: build every repo from nothing. Every argv
path (absolute OR relative) must resolve inside d”) and repair d specifically, while printing
`wrong=0 tampered=0`. It is a **fixable defect, not a disclosed tradeoff**: no limit in
`round-42-claims.md` covers a fixture whose measured history is a host repository.

### V2a — a symlinked capture pointing at host files: **BLOCKED as a content read**

`p-link-target-hashed` commits `corpus/evidence/r2/link.txt` as a symlink to `/etc/hostname` and anchors
the row on the digest of the link target string (`sha256(b"/etc/hostname")`). `run-probes.txt`:

```
FIXTURE p-link-target-hashed tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
```

Had the tool hashed the host file's bytes the row would have been `digest-unknown` and the fixture
`WRONG`. The anchor tool digests the git blob (`evidence_index`, `anchor_digest_check.py:217-238`), and a
symlink's blob is its target path. A symlinked capture therefore certifies a pointer, never host content.

### V2b — a symlinked row source pointing at host files: **WORKS** (host read outside `d`)

`p-host-row-file` commits `corpus/SOURCES.md` as a symlink to a file in the seat's scratch, outside `d`,
containing a 10-cell row. `run-probes.txt`:

```
FIXTURE p-host-row-file tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
```

The declared class could only be produced by parsing the host file: the fixture's own sources file is the
symlink and contains no row text. `parse_rows` reads the working-tree path and follows the link
(`anchor_digest_check.py:395-398`); `load_errata` does the same for lessons (`:374-384`). `path_ok` never
sees it, `fingerprint` records the link target but does not reject it
(`round42_c1_verify.py:324-341`). Same class of defect as V1b: the fixture's declared result depends on
state outside `d`, and the contract check says nothing.

### V3 — the direction satisfied through a crash rather than the advertised branch: **BLOCKED**

`probe3/p_crash.py` (no `.git` at all; the anchor tool exits 2 before printing) run with `--only X9`,
`run-extra.txt`:

```
FIXTURE p-crash-only tool=anchor expect=reject declared=- observed_rc=2 observed=- WRONG
MUTANT X9 anchor rc-silence SURVIVED exhibits=none
```

`exhibits` rejects any result outside `(0,1)` for the class direction (`round42_c1_verify.py:442-457`),
`rc-silence`/`rc-mirror` demand exact 0/1, and both tools convert every exception into exit 2
(`anchor_digest_check.py:585-587`, `order_check.py:207-210`). I also enumerated the 14 mutants: every
mutation is a boolean/string relaxation (`if False`, a widened/narrowed regex, a dropped fallback), so
none has an exception path a fixture could reach. No crash-based kill is available.

### V4 — repairs a–c re-tested (variant store hidden, `--unshare-ipc`, `--tmpfs /run`): **HOLD, and are unreachable**

`run-p4-p5.txt`, using the counter's own sandbox flags:

```
IPC-CHILD ipc-hidden
run-listing []
variants-listing []
slots-listing []
store-readable False
proc-cmdline-present True
```

a (`/variants` + `/slots` are empty tmpfs overlays; the variant arrives by `--ro-bind-data`,
`round42_c1_verify.py:412-418`), b (`--unshare-ipc`, a SysV segment seeded in the outer namespace is
invisible in the child) and c (`/run` empty) hold. The round-41 hostile modules (`h_var`, `h_ipc`,
`h_run`) require **fixture code to execute inside the tool run**; for these two tools the only such route
is config-driven git execution, which V1 shows is not reachable. So a–c cannot be exercised positively in
round 42 — they are holding by construction, not by measurement of an attack. (`/proc/self/cmdline` is
readable, i.e. the slot path is discoverable by code that somehow runs; that only matters if V1 ever
opens.)

### V5 — the token scan itself: **WORKS** (heuristic evadable)

The first `probe2/p_redirect.py` contained the literal text `core.worktree` and the counter printed
`SIDECHANNEL probe2/p_redirect.py tokens=core.`. After respelling the key as `"co" + "re.worktree"` the
same fixture ran with `BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0` (`run-p4-p5.txt`). The scan is
performed only on the module source (`round42_c1_verify.py:478-479`), never on the fixture files the module
writes, so `sidechannel=0` certifies nothing about what the build produced. The freeze names the scan a
heuristic, so this is disclosed; it must not be quoted as evidence of cleanliness.

## 3. Impacted axes

- **Calibration** (the claim under test): the count “14/14 killed attributably” is not a count of
  demonstrated behaviours. Three of my fourteen kills are substitutes admitted by the frozen kill rule, and
  a fourth (`p-redirect`) is obtainable without building the scenario at all. Round 42's C1 admission must
  therefore rest on the non-author review of every fixture, not on the `MUTANTS` line; otherwise the axis
  number would be bought by fixture shape.
- **Soundness**: `path_ok` + the “built from nothing” sentence are the counter's written contract with the
  battery, and both are unenforced for (i) `core.worktree` redirects (V1b), (ii) symlinks out of `d`
  (V2b), (iii) fixture text not scanned (V5). None of these three is covered by a limit named at the
  freeze; they are fixable defects.
- Not impacted: pins, null-detection, tamper fingerprints, the rc/class tables and the `invalid` checks all
  behaved as advertised in every run (no `null_detected`, no `TAMPERED`, no `invalid`).

## 4. Smallest safe correction (ranked)

1. **Enforce the fixture contract after build** (`round42_c1_verify.py:499-507`, next to the existing
   shape check): refuse a fixture when (a) any symlink under `d` resolves outside `d` (the fingerprint
   already reads link targets at `:324-341`), or (b) any `.git/config` in `d` carries a redirect/exec key
   (`worktree`, `include.path`, `fsmonitor`, `hooksPath`, `*.external`, `*.textconv`, `sshCommand`,
   `pager.*`, `filter.*`), or (c) an order fixture's `--claims`/`--receipt` path is not a `blob` at HEAD
   (`git cat-file -t`). (a) and (b) close V1b/V2b; (c) closes the XO1/XO3 directory receipts. All three are
   contract checks, not intent judgements, so they do not contradict the frozen kill rule.
2. **Treat every `--evidence-ref` (X13) kill as review-gated**, or require the index-only delta under
   `corpus/evidence/` to be a capture file rather than `PROVENANCE.md`/`SHA256SUMS*`/`task.toml`. This
   judges fixture shape and therefore conflicts with the freeze's “not the fixture's intent” sentence; it
   belongs in the review checklist unless the freeze is amended.
3. **Do not rely on `sidechannel=0`**: scan fixture text too (the build child can hash what it wrote) and
   note that token assembly defeats the string match (V5).
4. Nothing else needs changing: the rc/class/attribution machinery, the pins, the second unmodified run
   and the tamper fingerprint all perform as documented.

## 5. Limits of this review

- My fixtures are new (`b_*.py`, `p_*.py`), not copies of the freeze modules; I read the freeze modules to
  learn reachability only. The battery is 14 fixtures; substituting three of them is enough for the
  counterexample, so I did not search for a dishonest route for the other eleven (X1, X3, X6, X7, X9, X12,
  X14, X15, XO5, XO6, XO7 are ordinary demonstrations).
- The `p-redirect` kill needs a host repository to exist at measurement time; it demonstrates the contract
  breach and the counter's blindness, not a self-contained module.
- V1 covers every config key reachable by the tools' command set and one fake-signature attempt; a key I
  did not consider could still exist.
- Repairs a–c are measured only as sandbox properties (V4); the round-41 hostile modules could not be
  adapted into fixture code that actually runs in round 42's tool runs.

## 6. Receipts (all under `.ufo/waves/round-42/build/R42CritC1Counter/`)

| file | sha256 |
|---|---|
| `battery/b_anchor.py` | `f12a9b1d825ef4a52a3783e620eced59cfa55e03007e87ac577fb3058c3b9e4b` |
| `battery/b_order.py` | `6b1b75dcc3c004097ede313203643e49d698b3ba6106708683224e587ba21213` |
| `probe/p_probe.py` | `131c97c0776ff4f23828b756a552def562b3ce111f8792d1834b009e770ceec6` |
| `probe2/p_redirect.py` | `831af175597e74b1ca5bfbae6f087b6f63ef26b4c761fdddf0da8562f77d1e89` |
| `probe3/p_crash.py` | `ef623ad73f1461f010c2bb6518ea886f08d620fb1435b042bab14b448a95e949` |
| `probe4/p_x13.py` | `9a637412387fd5d1a0fe8dcdd71506032a7eff418768243642ff96666cb2c1b1` |
| `run-predicate.txt` (headline, exit 0) | `4260522c71bd0981e2bc71d7b3249db0a1f67c7d9dcc200989199d8efaceaacf` |
| `run-battery.txt` (first, staged-table X13) | `f6f48f7097a7d4d2c4d3149eb88878277c3f25b341267f7b2db37b81f89e7c73` |
| `run-probes.txt` (V1, V2a, V2b, V3) | `84d50f1bb1e3fed16fb87438e717a6cd2fb743f3fc6ad691665f449a8721484c` |
| `run-p5.txt` (V1b manual) | `d493fb2a6d77852dbacf066999d1f44d9af933d7fc1fb20106d77802ee126ebf` |
| `run-p4-p5.txt` (V4, V1b kill, V5) | `46fa12a281e9ca44d902848bbe0542ecbf632fbfe32f575fd5b7f2b74cbb36ee` |
| `run-extra.txt` (gpg, V3, redirect, default exit) | `65d8b6257b5034b9cffaf7877c0a9a4fada7ca02d97385ae99cf4a9c5e6bd4b8` |
| `run-x13.txt` (staged-manifest probe) | `84d508ee48195444c38c6dc13a52c52e26d02ea52142665169002c251aa2412d` |
| `run-config-exec.txt` (V1 definitive marker control) | `1f5e19311160a5e07c810ec97c52a1db7408a8605a2b23166d7be4f086ebc291` |

Envelope before/after: `17:24:22` … `17:30:01` (counter runs end 17:27:44; the config-exec control is 17:30:01); `/home/vgpnk/.local/bin` listing digest
`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` before and after every run.
No file was written outside the report directory and the scratch directory; the lane clone in scratch is
otherwise untouched (only the untracked `plans/battery42/`).

VERDICT: c1-counter-dishonest-green-reached-vectors-7
