# F40RevBatBind — non-author honesty review of `plans/battery40/a_bind.py`

kengaku round 40 wave 2 (falsify), 2026-10-26. Target: `plans/battery40/a_bind.py` (105 lines, read in full)
against mutants A15/A17/A27 of `plans/round40_c1_verify.py`. Measured at lane tip
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (scratch clone; `git rev-parse HEAD` → `ec1005a2a28bc5cfdde7723374368ed4cc956eed`,
toplevel `/fast/scratch/hyaku/kengaku-r40/F40RevBatBind/lane`). The shipped `a_bind.py` is byte-identical to the
lane copy (`cmp` → silent). No lane file edited; no commit in any fixture; scratch removed at the end.

## Method

- Scratch per fixture rule: `S=/fast/scratch/hyaku/kengaku-r40/F40RevBatBind`, `TMPDIR=$S`,
  `git clone -q --no-local <lane> "$S/lane"` + checkout of the tip; battery dir `$S/bat` holds only `a_bind.py`.
- Counter run (HOST-SAFETY wrapper, exit 0, 8.85 s wall):
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 "$S/lane/plans/round40_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat" --only A15,A17,A27 --work "$S/w"`
- Fixture trees rebuilt outside the counter (`$S/inspect_fx.py`, verbatim copy of the counter's `Ctx` class +
  `import` of `a_bind.py`), then `diff -r --exclude=.git` against a fresh clone `$S/cmp` at the same tip, plus
  `git status/log/show` per tree. Mutant behaviour probed by applying each mutant's own `old→new` to the pinned
  anchor source (`count(old)==1` asserted) and running the variant under the same wrapper on its fixture tree.

## Counter output (receipt `run-c1-a_bind-only.txt`)

```
PINS total=3 mismatched=0
FIXTURE a_bind-a27-token-per-capture tool=anchor expect=reject declared=capture-unanchored observed_rc=1 observed=capture-unanchored ok
FIXTURE a_bind-a15-slug-ambiguity tool=anchor expect=reject declared=anchor-unbound observed_rc=1 observed=anchor-unbound ok
FIXTURE a_bind-a17-index-bytes tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT A15 anchor rc-silence killed by=a_bind-a15-slug-ambiguity -- plans/anchor_digest_check.py:55 'is matched **exactly** against the `name = "<org>/<task>"
MUTANT A17 anchor rc-mirror killed by=a_bind-a17-index-bytes -- plans/anchor_digest_check.py:74 '`--evidence-ref index` reads the index blobs (`git cat-fi
MUTANT A27 anchor silence killed by=a_bind-a27-token-per-capture -- plans/anchor_digest_check.py:96-98 'A capture none of the row's anchor tokens resolves is
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

## Per-fixture verdicts

### a_bind-a27-token-per-capture (a_bind.py:51-64; FIXTURES a_bind.py:99-100) — HONEST
Advertised sentence verified at `plans/anchor_digest_check.py:97-98` ("A capture none of the row's anchor
tokens resolves is `capture-unanchored`"); adv cell cites :96-98 — in range.
- Build edits only `corpus/SOURCES.md` in its own clone (`git status --porcelain` → ` M corpus/SOURCES.md`,
  nothing else). The diff (receipt `fixture-diffs.txt`) shows S111's source cell gains the regex-log URL and the
  anchor token becomes `sha256 345c3bd0…` — asserted exactly-once at a_bind.py:59.
- Constants are real lane digests: `sha256sum` on `$S/cmp` → `345c3bd0…8f72  round36/tb2-regex-log/test_outputs.py`,
  `526aee3d…6b37  round37/tb2-git-webserver/test_outputs.py` = S108/S111 (a_bind.py:16-17).
- So the row names two captures, the token resolves only regex-log, and the webserver capture is unanchored —
  exactly the additive-route shape the docstring sentence describes. Reference: rc=1, classes exactly
  `{capture-unanchored}` (FIXTURE line `ok`). Mutant probe on the rebuilt tree: rc=0, no DEFECT line — the
  silence kill the module docstring (a_bind.py:3-5) advertises.
- No wave-1 reliance: reads only lane data (SOURCES.md), writes only inside its fixture dir, argv absolute.

### a_bind-a15-slug-ambiguity (a_bind.py:67-78; FIXTURES a_bind.py:101-102) — HONEST
Advertised sentence verified at `plans/anchor_digest_check.py:55` ("`<subpath>` is matched **exactly** against
the `name = \"<org>/<task>\"` a committed `task.toml` gives") plus :66 ("A row whose token cannot be bound this
way is `anchor-unbound`").
- One commit `aa9c2f6 "a_bind: two task dirs claiming one slug"` adds `roundX/tb2-amb-a` and `roundX/tb2-amb-b`;
  both `task.toml` files observed as `name = "harbor/amb-bind-task"`; row S902 (uncommitted SOURCES.md edit —
  rows are read from the working tree, anchor_digest_check.py:398) claims `sha256 080230c3…`.
- `080230c3…` is the digest of `tb2-amb-a/test_outputs.py` (`sha256sum` receipt), i.e. the alphabetically first
  owner — and the tool sorts owners (`anchor_digest_check.py:334` `owners = sorted(...)`), so the mutant
  (`len(owners) != 1` → `< 1`) binds tb2-amb-a and matches. Reference: rc=1, classes exactly `{anchor-unbound}`;
  mutant probe: rc=0, no DEFECT — the rc-silence kill advertised at a_bind.py:6-8.
- Honesty note: the kill depends on the tool's sorted owner order; had the order differed the mutant would have
  bound tb2-amb-b and survived *visibly* (digest-wrong-capture, rc=1), so nothing is hidden.
- No wave-1 reliance: both captures committed via `ctx.git` inside the fixture dir; token is a genuine digest.

### a_bind-a17-index-bytes (a_bind.py:81-95; FIXTURES a_bind.py:103-104) — HONEST
Advertised sentence verified verbatim at `plans/anchor_digest_check.py:74` ("`--evidence-ref index` reads the
index blobs (`git cat-file :<path>`)").
- Tree state observed: commit `fc66682 "a_bind: committed view of the capture"`; then `git status --porcelain`
  → `M  corpus/evidence/roundX/tb2-idx/SHA256SUMS`, `M  corpus/evidence/roundX/tb2-idx/test_outputs.py`
  (staged), ` M corpus/SOURCES.md`. Three views differ exactly as claimed: HEAD blob
  `assert True  # a_bind committed view`, index blob and worktree `assert True  # a_bind staged view`;
  HEAD SHA256SUMS lists `b22ab420…`, index SHA256SUMS lists `10d3d4b6…`.
- Row S903 (SOURCES.md:127) claims `sha256 10d3d4b6…` = the staged digest, and argv carries
  `--evidence-ref index` (a_bind.py:95). Reference: rc=0, no defects (FIXTURE line `ok`) — only a tool that
  reads index blobs accepts it. Mutant probe (mode-swapped, reads HEAD): rc=1 with
  `DEFECT S903 … class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256…` — precisely the
  behaviour the module docstring (a_bind.py:9-11) advertises.
- The `.git/index` writes here are the behaviour under test (an honest `git add` of a staged capture, the
  documented purpose of index mode, anchor_digest_check.py:75-76), not a fingerprint-skip evasion: the
  fingerprint is taken after the build and re-checked after the runs (`tampered=0`), and no `.lock` file is
  created or relied on.

## Wave-1 attack cross-check (per R40CritC1Counter A1/A2/A4/A5, R40SentinelCounter, R40RevCounters F1-F6)

| Attack | a_bind.py evidence | Verdict |
|---|---|---|
| A1 reads tool/own program text | imports only `hashlib`, `pathlib` (a_bind.py:13-14); reads only `corpus/SOURCES.md` and writes capture files; never opens `plans/*` | clean |
| A2 PATH git shim | no `os`/`subprocess`/`environ` use at all (token scan: none of `environ`, `setsid`, `fork`, …); build env is counter-owned (`HOME=/nonexistent`) | clean |
| A4 relative argv / symlink out of d | argv observed absolute: `['--lane', '…/fxout/fNNN/lane']` (+ `--evidence-ref index`); no symlink API; counter `path_ok` enforced | clean |
| A5 `.lock`/`.git/index` fingerprint skips | no `.lock` created; index used only as the tested A17 behaviour via honest `git add`; `tampered=0` | clean |
| whole-host-fs writes | every write goes through `ctx` paths inside `d` (`Ctx._inside` raises otherwise); observed trees differ from the lane only in the documented files | clean |
| cross-module fixture forgery | builds only into its own `dest/fNNN` (`d / "lane"`); no other module's dir touched | clean |
| bare-string `build()` return (F2) | returns `list[str]` in all three builders (a_bind.py:64,78,95) | clean |
| phase detection | static argv, no env/proc reads; runs are indistinguishable by construction | clean |
| SIDECHANNEL token scan (F5) | counter printed `sidechannel=0`; my identical token scan: `none` | clean |
| empty fid (F6) | fids are non-empty descriptive strings (a_bind.py:99,101,103) | clean |

## Contract compliance

`FIXTURES` entries carry exactly the required keys (`fid`, `tool=anchor`, `expect`, `defects`, `build`);
`build(ctx, d)` fills the empty `d` via `ctx.clone(d / "lane")` and returns the argv tail after the tool path;
no `{WORK}` token is used (the anchor tool takes no `--work`). Declared `defects` match the reference's exact
class set in all three fixtures (counter `ok` on each). The `adv` cells' line citations were re-verified
against the pinned tool bytes: :55, :74, :97-98 all exact.

## Receipts (under `.ufo/waves/round-40/falsify/F40RevBatBind/`)

- `run-c1-a_bind-only.txt` — sandboxed counter run (pasted above).
- `fixtures-built.txt` — rebuilt trees + argv per fixture.
- `fixture-diffs.txt` — `diff -r` of each tree vs the lane + a17 `git status`.
- `mut-A15.out`, `mut-A17.out`, `mut-A27.out` — mutant probes on the rebuilt trees.

## Residual risk / gaps

- The counter's MUTANT lines record kill attribution only; the mutant classes above come from my own probes of
  the mutants' exact `old→new` edits on the rebuilt trees (commands in receipts), not from the counter stdout.
- `ctx.clone` uses `git clone --shared`, so each fixture's `.git/objects/info/alternates` points at the
  counter's pristine clone — harness-owned API, fingerprinted, not a battery choice.
- I did not audit the other six battery modules (out of scope for this seat).

VERDICT: battery-a_bind-honest-3/3
