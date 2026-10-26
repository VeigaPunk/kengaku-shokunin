# F40RevBatMan — non-author honesty review of `plans/battery40/a_man.py` (A21, A22)

kengaku round 40, wave 2 (FALSIFY), 2026-10-26. Lane tip measured: `ec1005a2a28bc5cfdde7723374368ed4cc956eed`
(clean scratch clone, `git rev-parse --show-toplevel` == clone root verified before any write).
Target: battery module `plans/battery40/a_man.py` (81 lines, read in full) against frozen mutant rows A21/A22
(`plans/round40_c1_verify.py:155-164`). No LSP server/device is available in this session for these `.py`
files — all semantic checks are text-level (`read`/`grep`) plus executed runs; that fallback is recorded here
per reviewer protocol. No tools were installed (bwrap/git/python3 already present; nothing to record under the
2026-10-19 tooling authorization).

## What the mutants advertise (frozen rows)

- **A21** `rc-mirror`, old→new `"dig = m.group(1).lower()" → "dig = m.group(1)"` (`round40_c1_verify.py:155-159`).
  adv quotes `plans/anchor_digest_check.py:44-46`: "the digest that entry lists, and the digest of the
  committed file bytes, are both accepted views of that one capture", with the parenthetical "(a manifest
  entry is read case-folded)".
- **A22** `rc-mirror`, old→new removes the manifest view from `capture_digests`
  (`round40_c1_verify.py:160-164`); adv quotes the same sentence.
- Mutated sites verified present in the tool: `anchor_digest_check.py:250` (A21, inside `evidence_index`)
  and `anchor_digest_check.py:308-309` (A22, inside `capture_digests`).

## Per-fixture verdicts

### f000 `a_man-stale-manifest-digest` — **HONEST**

Build (`a_man.py:69-73`, shared `_repo` at `a_man.py:45-59`): fresh `ctx.init` repo (not a lane clone —
`a_man.py:49`), one committed 11-cell row S900 whose source cell names
`corpus/evidence/round41/tb2-man/test_outputs.py` (explicit-lane-path binding, tool route 3,
`anchor_digest_check.py:346-356`), capture bytes `assert True  # a_man capture\n`
(sha256 `faa64ae46ee6fb984697c7d9e269404e697ac259c86000f679dd1ac7bfe5b574`), and a `SHA256SUMS` listing
`7d6ec0a363b17dbe224063b26eef23e9b3f729bd9419eee37b736d11e18936be` (lowercase) — the digest of a different
literal (`a_man.py:42`), **not** the capture bytes. Row anchor = the manifest digest.

- Exhibits the advertised sentence honestly: the anchored digest resolves **only** through the manifest view
  (blob view is `faa64ae4…`), so the reference's rc 0 / no-DEFECT (observed FIXTURE line) is exactly "the
  digest that entry lists … accepted view" with the two views disagreeing. The module states the
  disagreement is deliberate (`a_man.py:20-22`).
- Kills A22 as predicted: mutant deletes `anchor_digest_check.py:308-309` → the token leaves the row's
  capture set but stays a committed capture via `all_digests` (`evidence_index` untouched by A22) →
  `digest-wrong-capture`, rc 1 — matches the module's own prediction (`a_man.py:17-18`) and observed run
  (matrix below).
- Does **not** kill A21: the entry is lowercase, so removing `.lower()` changes nothing (observed rc 0) —
  exactly the docstring's co-location note (`a_man.py:22-25`).

### f001 `a_man-uppercase-manifest-entry` — **HONEST**

Build (`a_man.py:62-66`): identical repo except `SHA256SUMS` lists `7D6EC0A363B17DBE224063B26EEF23E9B3F729BD9419EEE37B736D11E18936BE`
(UPPERCASE); the row anchor stays lowercase. `diff -r --exclude=.git f000 f001` shows **exactly one** differing
file, `SHA256SUMS`, case-only — a true minimal pair.

- Exhibits the sentence including the case-fold parenthetical: the reference lowercases at read
  (`anchor_digest_check.py:250`) → capture set `{faa64ae4…, 7d6ec0a3…}` → rc 0 (observed). Because the blob
  digest differs from the anchored digest, the acceptance is genuinely the manifest view, not a blob-view pass.
- Kills A21 as predicted: mutant keeps the written case → token `7d6ec0a3…` is in no committed evidence →
  `digest-unknown`, rc 1 — matches `a_man.py:12-14` and observed run.
- Also kills A22 (observed rc 1, `digest-wrong-capture`). The module discloses this dual kill
  (`a_man.py:23-25`); the counter prints only the first killer (`by = by or fx["fid"]`,
  `round40_c1_verify.py:533`) and the stale fixture is first in `FIXTURES` order (`a_man.py:76-81`), so the
  single `killed by=` line hides nothing.

## Observed mutant × fixture matrix (direct runs, sandboxed)

Receipt: `.ufo/waves/round-40/falsify/F40RevBatMan/a_man-mutant-matrix.txt` (variants built by applying the
frozen old→new strings to the lane tool; every run inside the HOST-SAFETY bwrap wrapper).

```
f000 ref: rc=0 defects=-
f000 A21: rc=0 defects=-
f000 A22: rc=1 defects=['DEFECT S900 anchor token=7d6ec0a3… class=digest-wrong-capture …']
f001 ref: rc=0 defects=-
f001 A21: rc=1 defects=['DEFECT S900 anchor token=7d6ec0a3… class=digest-unknown …']
f001 A22: rc=1 defects=['DEFECT S900 anchor token=7d6ec0a3… class=digest-wrong-capture …']
```

Every cell matches the module docstring's predictions (`a_man.py:10-25`), including the classes
`digest-unknown` (A21) and `digest-wrong-capture` (A22). No inference remains.

## Wave-1 attack-vector checklist — none present

| Vector (wave-1 counter attacks) | Evidence of absence |
|---|---|
| reads the tool / own program text at run time | `a_man.py` imports only `hashlib` (`a_man.py:30`); no `open`/read of any file anywhere; `manifest_digest()` hashes a literal (`a_man.py:42`) |
| writes outside d (HOME, PATH dirs, other modules' dirs) | all writes are `d`-relative (`a_man.py:50-56`); `Ctx._inside` raises on escape (`round40_c1_verify.py:233-237`); build child env `HOME=/nonexistent` (`round40_c1_verify.py:248`); tree dump shows only `corpus/**` + git internals inside d |
| relative argv tokens / symlinks pointing out of d | argv = `["--lane", str(d), "--evidence-ref", "head"]` (`a_man.py:66,73`) — absolute, inside d (`path_ok`, `round40_c1_verify.py:296-300`); tree dump shows zero symlinks |
| `.lock` / `.git/index` names the fingerprint skips | no `*.lock` anywhere in either tree (dump); `.git/index` present but `git status --porcelain` empty → index == HEAD == worktree, and the tool reads HEAD blobs only (`anchor_digest_check.py:157-160`), so the skipped names carry no run-relevant state; harness fingerprint before/after runs: `tampered=0` |
| phase detection (telling reference from mutant) | fixtures are static data: no reads, no code executed at run time, nothing can inspect argv/env mid-run |
| bare-string `build()` return | both builders return a list (`a_man.py:66,73`); harness rejects non-list argv (`isinstance(argv, list)`, `round40_c1_verify.py:429`) |
| cross-module fixture forgery | fixtures are single-row repos built by `ctx.init` (`a_man.py:49`), sharing nothing with sibling modules' dirs (counter owns `dest/fNNN` per module, `round40_c1_verify.py:419-421`) |
| sidechannel tokens | observed `BATTERY … sidechannel=0` |

## Measurements

Sandboxed invocation (HOST-SAFETY wrapper; battery dir held only `a_man.py`, sha256
`0dfc073362c6919e7e69001035a5a85f38f5d32028f1d63f363b71ea82ebd2ac`, byte-identical to the repo file):

```
$ bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
    --proc /proc --unshare-pid --die-with-parent \
    python3 <fleet>/plans/round40_c1_verify.py --lane "$S/lane" --battery-dir "$S/battery" \
    --only A21,A22 --work "$S/w"
PINS total=3 mismatched=0
FIXTURE a_man-stale-manifest-digest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_man-uppercase-manifest-entry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT A21 anchor rc-mirror killed by=a_man-uppercase-manifest-entry -- plans/anchor_digest_check.py:44-46 'the digest that entry lists, and the digest of the com
MUTANT A22 anchor rc-mirror killed by=a_man-stale-manifest-digest -- plans/anchor_digest_check.py:44-46 (as A21: the manifest entry is an accepted view of the 
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

`PREDICATE C1 n/a` is expected: `--battery-dir`/`--only` are development flags
(`round40_c1_verify.py:460-462,517-519`); the frozen full-battery predicate is the landing measurement's job,
not this dev invocation. Receipt: `a_man-run.txt`.

Fixture-tree inspection (build logic copied into scratch script `inspect_fixture.py`, replicating the
harness's `Ctx` byte-for-byte): both trees dumped in full — lstat mode/size, symlink targets (none),
`git ls-tree -r HEAD` (3 blobs), `git status --porcelain` (empty), `SHA256SUMS` text, computed capture
digest. Receipt: `a_man-fixture-trees.txt` (8269 bytes).

Lane diff: the fixture tracks only 3 paths, all under `corpus/`; `lane lacks corpus/evidence/round41`
(checked with `test -e`); fixture `corpus/SOURCES.md` differs from the lane's (own header + single S900
row) — no lane state imported, copied, or forged.

## Findings

**No dishonest fixture.** Both fixtures build inputs that exhibit the advertised sentence through the
manifest view alone, kill their mutants in the declared `rc-mirror` direction, and use none of the wave-1
attack vectors. Two cosmetic notes, non-blocking:

1. `a_man.py:17-18` predicts `digest-wrong-capture` for A22's mutant — correct only because `evidence_index`
   still populates `all_digests` under A22 (the mutant edits `capture_digests`, not `evidence_index`);
   verified against `anchor_digest_check.py:250-253` vs `:308-309` and observed. Not a defect; the direction
   is rc-only.
2. The counter's `killed by=` shows one fixture per mutant (`round40_c1_verify.py:533`); A22's second killer
   (f001) is visible only in the module docstring and in my matrix receipt. Counter display limitation, not
   a battery honesty issue.

## Residual risk / verification gaps

- The frozen 21-mutant full predicate was not re-measured here (dev subset `--only A21,A22`); out of this
  seat's scope.
- My mutant-matrix runs used variants I built in scratch from the lane tool with the frozen old→new strings
  (uniqueness asserted); they are corroborating observations, not the counter's own variant files.
- Scratch removed after receipts were copied out (`/fast/scratch/hyaku/kengaku-r40/F40RevBatMan` deleted);
  no process left running.

## Receipts

- `.ufo/waves/round-40/falsify/F40RevBatMan/a_man-run.txt` — sandboxed harness invocation, verbatim.
- `.ufo/waves/round-40/falsify/F40RevBatMan/a_man-fixture-trees.txt` — full fixture-tree dumps.
- `.ufo/waves/round-40/falsify/F40RevBatMan/a_man-mutant-matrix.txt` — mutant × fixture matrix.

VERDICT: battery-a_man-honest-2/2
