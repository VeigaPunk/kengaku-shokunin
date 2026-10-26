# R43SentinelCounter — the NEW parent-side git legs of `plans/round43_c1_verify.py`

Seat R43SentinelCounter (sentinel), kengaku round 43 wave 1. Scope: `order_argv_breach`, `repo_breach`,
`symlink_breach` (the three legs that run `git` in the COUNTER's own process, outside bwrap, with
`PIN_CHECK_ENV`), plus the tracer's env (`K43_SPAN`) and the `symlink_breach` TOCTOU. Read-only review of the
frozen counter; every fixture lives in my scratch (`/fast/scratch/hyaku/kengaku-r43/R43SentinelCounter`); no
vector names a real host path as a target. Counter/tool sources unmodified; nothing in the lane touched.
Host guard: every fixture build ran `git -C <fixture>` only, after asserting the fixture was its own toplevel
(`Ctx.git` does this itself); every run below is bracketed by the round-43 envelope.

## Bottom line

* **No program is executed** by the three parent-side calls. 17 command-bearing `.git/config` keys
  (`core.fsmonitor`, `core.hooksPath`, `core.sshCommand`, `core.alternateRefsCommand`, `core.pager`,
  `core.editor`, `core.gitproxy`, `diff.external`, `filter.x.clean`, `credential.helper`,
  `uploadpack.packObjectsHook`, `gpg.program`, `sequence.editor`, `alias.rp`, `alias.config`,
  `alias.cat-file`, `log.showSignature`) with a marker script as the value: `"marker": false` on all 17, and
  `rev-parse --show-toplevel` / `config --get core.worktree` / `cat-file -t HEAD:README` all behaved normally
  (probe1 §A). The four `GIT_CONFIG_KEY_*` pins are belt-and-braces for these three subcommands, not the
  load-bearing control.
* **No write outside `d`** was observed from those calls: a fixture whose git dir sits outside `d` was
  snapshotted before/after `rev-parse`, `config --get` and `cat-file -t` → `"outside_tree_changed": false`,
  `"added": []`, `"removed": []` (probe2 §2).
* **Reads outside `d` ARE possible**, three ways, and two of them defeat R4's stated purpose: a `.git` FILE
  pointing at an outside git dir (F1), a repo deeper than the walk's depth cap (F2), and `include.path` /
  `objects/info/alternates` (F5). The blob leg can also be silenced by argparse abbreviation (F3).

Severity counts at the end: 6 findings, 2 high.

## F1 — HIGH — a fixture's git dir can live outside `d`; all three legs stay silent

**Line:** `plans/round43_c1_verify.py:461-492` (`repo_breach` reads only `rev-parse --show-toplevel` and
`core.worktree`, never `rev-parse --absolute-git-dir`); `:494-502` (`symlink_breach` only follows symlinks — a
`.git` FILE is not one).

**Exploit path.** `git init --separate-git-dir=<dest>/side/gitdir <d>` (or writing `.git` as
`gitdir: <outside>` by hand) makes `<d>/.git` a plain FILE. `rev-parse --show-toplevel` then prints `d`, so the
worktree half of R4 is satisfied; nothing inspects where the objects, refs and config actually live. The
git dir — the data the tool reads — is outside `d`, and the counter prints `wrong=0`.

**Evidence.**

```
$ python3 probe3.py    # inside envelope.sh
{"vector": "separate git dir outside d",
 "dot_git": "gitdir: .../p3/gd/side/gitdir",
 "absolute_git_dir": [0, ".../p3/gd/side/gitdir", ""], "inside_d": false,
 "repo_breach": null, "symlink_breach": null,
 "show_toplevel": [0, ".../p3/gd/f001", ""]}
{"vector": "order_check on esc-gitdir-outside", "rc": 0,
 "out": ["ORDER ok no claims file committed at or before the receipt shows the frozen probe executed",
         "ORDER RESULT PASS"], "err": ""}
```

End to end through the FROZEN counter (module `m_escape.py`, copied beside this report):

```
$ python3 lane/plans/round43_c1_verify.py --lane lane --battery-dir p3/bat --only NA1 --work p3/w
PINS total=2 mismatched=0
FIXTURE esc-gitdir-outside tool=order expect=accept declared=- observed_rc=0 observed=- ok
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
```

A *passing* order fixture whose entire git store is outside `d` is admitted with `wrong=0` and no SETUP
refusal. probe1's earlier shape (`.git` file → outside gitdir, `core.worktree=<d>`) gives the same nulls with
`cat_file [0, "blob"]`.

**Impact.** R4's purpose — "the measured scenario would live outside `d` while the counter printed
`wrong=0`" (`:465`) — is reachable. `d` no longer bounds the state the tool reads: a fixture can serve blobs
and refs from a directory it did not build in `d`, share one git store between fixtures, or point at a
sibling seat's scratch. Not a host write: the tool run is read-only everywhere except `work`/`tmp`, and the
parent-side calls are read-only (measured above).

**Smallest remediation.** One extra call in `repo_breach` (after `:479`): require
`rev-parse --absolute-git-dir` to resolve inside `d`, and refuse any `.git` entry that is a plain file (the
canonical module contract never needs one — every repo is built in `d`). Both measured available:
`absolute_git_dir [0, ".../p3/gd/side/gitdir"]` vs `inside_d false`, and for a normal repo
`gitdir [0, ".../p4/ord/repo/.git"]`.

## F2 — HIGH — `repo_breach` skips any repo deeper than three levels, so R4's rule is not enforced

**Line:** `plans/round43_c1_verify.py:475` (`if depth >= 3: dirs[:] = []`), inside the walk at `:468-476`; the
refusal it feeds is `:477-491`.

**Exploit path.** `path_ok` accepts any argv token inside `d`, so `--lane x/y/z/r` is legal and
`Ctx.init`/`Ctx.git` build that repo. The walk stops descending at depth 3, so `d/x/y/z/r` is never examined
by `repo_breach`, whatever its `core.worktree` says.

**Evidence** (probe1 §D, probe3 end to end; scratch-relative outside target `.../p1/outside/wt-deep`):

```
{"vector": "repo at depth 4, core.worktree outside",
 "repo_breach": null,
 "show_toplevel": [0, ".../p1/outside/wt-deep", ""],
 "config_worktree": [0, ".../p1/outside/wt-deep", ""]}
{"vector": "repo at depth 2 for control",
 "repo_breach": "r/rev-parse --show-toplevel=.../p1/outside/wt-deep"}
FIXTURE esc-deep-worktree tool=order expect=error declared=- observed_rc=2 observed=- ok
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
```

Depth 2 is refused, depth 4 is not; the end-to-end run admits the escaping fixture, and `order_check` really
adopted the outside root (it answered `ORDER ERROR claims file name is not round-NN-claims.md: claims.md`
after resolving paths against `.../outside/wt`).

**Impact.** The literal R4 sentence in the frozen claims ("repo toplevel/`core.worktree` must stay in `d`") is
bypassable by nesting the lane repo one directory deeper — a level of nesting nobody would notice writing a
fixture. `wrong=0` stops implying the scenario lived in `d`.

**Smallest remediation.** Do not enumerate a tree: derive the repos from the argv the fixture returned. For an
order fixture check `git -C <d>/<lane> rev-parse --show-toplevel` **and** `--absolute-git-dir` and require both
under `d` (the contract already fixes `--lane` as `["--lane", <repo>]`); keep the walk only as a secondary
sweep with no depth cap, or with a fixture-size bound (the walk is the counter's own, so a cap on files
visited rather than depth).

## F3 — MEDIUM — leg i parses argv itself and is silenced by argparse abbreviation

**Line:** `plans/round43_c1_verify.py:511-519` (the parser accepts only the exact literals `--lane`,
`--claims`, `--receipt`, in the `--opt value` and `--opt=value` forms).

**Exploit path.** `order_check.py`'s own parser is argparse, which accepts any unambiguous prefix
(`--claim`, `--c`, `--receip`, `--r`) and the `--claim=value` form. `order_argv_breach` sees none of those, so
`--claims` naming a *tree* at HEAD is never tested.

**Evidence** (probe4 §C, and the frozen tool itself accepting the abbreviations):

```
{"vector": "leg i --lane repo --claims claims --receipt README", "result": "--claims claims is a tree at HEAD, not a blob"}
{"vector": "leg i --lane repo --claim claims --receipt README",  "result": null}
{"vector": "leg i --lane repo --claim=claims --receipt README",  "result": null}
{"vector": "leg i --lane repo --c claims --receipt README",      "result": null}
{"vector": "leg i --lane repo --claims README --receip claims",  "result": null}
$ order_check.py --lane . --c .ufo/waves/round-42/claims/round-42-claims.md --receip corpus/evidence/round42/receipt.txt
ORDER RESULT PASS   rc=0
```

(The exact forms do work, including out of order: `--receipt claims --claims README` still refuses.)

**Impact.** Leg i's stated rule ("`--claims`/`--receipt` must each name a BLOB at HEAD", `:505-508`) does not
hold for argv the tool accepts; a fixture can present a tree/gitlink as claims and be admitted. The module
contract already fixes the canonical six-token shape, so this is also a contract-violation signal the counter
ignores.

**Smallest remediation.** Enforce the contract instead of re-deriving it: refuse any order argv that is not
exactly `["--lane", v, "--claims", v, "--receipt", v]` (or, if flexibility is wanted, reject any token starting
with `--` that is not one of the three long options with a separate value). Then no abbreviation can exist.

## F4 — MEDIUM — the parent-side git calls have no timeout: one fixture hangs the whole measurement

**Line:** `plans/round43_c1_verify.py:479-480`, `:485-486`, `:523-524` — three `subprocess.run` calls with no
`timeout=` and inherited stdin (the build child has 1800 s, a tool run 600 s, these have none).

**Exploit path.** `.git/config` with `include.path = <FIFO>` (or a device node, or a pipe that never closes).
`git rev-parse` and `git config` block opening it.

**Evidence** (probe1 §E, then through the frozen counter with `m_fifo.py`):

```
{"vector": "include.path FIFO", "config_get": ["TIMEOUT","",""], "rev_parse": ["TIMEOUT","",""]}
$ timeout 30 python3 lane/plans/round43_c1_verify.py --lane lane --battery-dir p5/bat --only NA1 --work p5/w
PINS total=2 mismatched=0
ENVELOPE end 19:14:14 exit=124 ...
```

The counter prints `PINS` and then stops: no SETUP line, no fixture line, no receipt, and `finally:
shutil.rmtree(root)` never runs. The envelope records only `exit=124`.

**Impact.** A single fixture (accidentally or deliberately) turns a C1 measurement into a hang with a
non-diagnostic artefact; the operator sees a killed envelope, not "fixture X hung the breach check". This is
the only finding whose trigger needs no fiddling with escape semantics.

**Smallest remediation.** `timeout=30, stdin=subprocess.DEVNULL` on the three calls; on
`subprocess.TimeoutExpired` return a breach string (`"<repo>/git hung"`) so it is a SETUP refusal, which is
the honest outcome.

## F5 — MEDIUM — `include.path` and `objects/info/alternates` read files outside `d` in the parent process

**Line:** `plans/round43_c1_verify.py:485-486` (`git config --get core.worktree` follows includes by
default); `:523-524` (`cat-file -t` honours an alternates file); `:479` likewise for `rev-parse`.

**Exploit path / evidence** (probe1 §B/§F, probe4 §D):

```
{"vector": "include.path outside d",
 "repo_breach": "repo/core.worktree=.../p1/outside/wt",
 "config_worktree": [0, ".../p1/outside/wt", ""]}            # value came from a file outside d
{"vector": "include.path host .gitconfig", "config_get": [1,"",""], "rc": 0}   # /home/vgpnk/.gitconfig parsed, no error
{"vector": "alternates outside d",
 "cat_file": [[0,"from-alternate\n",""],[0,"blob",""]], "repo_breach": null}
```

So a fixture can (a) make the parent-side `config --get` parse an arbitrary host config file and echo the
`core.worktree` it finds into the counter's SETUP message (a read channel into the report, with the value
visible), and (b) serve the blob that leg i judges from an object store outside `d`
(`from-alternate` printed through `cat-file -p`). Reads only; nothing was written (probe2 §2).

**Impact.** Two places where the verdict depends on state outside `d`; (b) additionally means `cat-file -t`
can answer `blob` for content the fixture never built in `d`. Lower than F1/F2 because the value must be a
`core.worktree` for the message path, and because the tool run sees the same alternates.

**Smallest remediation.** `git config --local --no-includes --get core.worktree` (measured:
`plain → /tmp/elsewhere`, `no_includes → rc=1, empty`) and refuse a fixture that has
`.git/objects/info/alternates` (measured: file existence is trivially checkable).

## F6 — LOW — `PIN_CHECK_ENV` omits `GIT_CEILING_DIRECTORIES`, which both other envs set

**Line:** `plans/round43_c1_verify.py:156` vs `:282` (build) and `:552` (tool run).

**Evidence** (probe3 §1; `d = .../p3/upgc/plain`, repo at `.../p3/upgc`, scratch-relative):

```
{"vector": "repo above d found by discovery (no ceiling)",
 "no_ceiling": [0, ".../p3/upgc", ""],
 "cat_file_no_ceiling": [0, "blob", ""],
 "with_ceiling": [128, "", "fatal: not a git repository (or any of the parent directories): .git"],
 "repo_breach_d": null, "leg_i": null}
```

**Impact.** `order_argv_breach` resolves `--lane` through git discovery with no ceiling, so its blob verdict
can come from a repo *above* `d` — and if the operator passes `--work` inside any git repo (a lane clone, a
home directory checkout), from a repo outside the scratch entirely. Read-only; the refusal decision, not the
host, is what moves. The asymmetry is what makes it interesting: the tool run is bounded at the scratch root
and the build child at `dest.parent`, so only the counter's own calls can wander out.

**Smallest remediation.** Add `"GIT_CEILING_DIRECTORIES": <fixture root>` to `PIN_CHECK_ENV` (it is a
constant there; the fixture root is a prefix of every `d`), or refuse a `--lane` whose discovered toplevel is
not under `d` (which is F2's fix anyway).

## Checked and clean (no finding)

| Vector | Measurement |
|---|---|
| 17 command-bearing config keys vs. the three subcommands | marker never written, `"marker": false` ×17 (probe1 §A) |
| `alias.config`, `alias.cat-file` shadowing a builtin | ignored; normal output, `"marker": false` |
| `gpg.program` + `log.showSignature` (the round-42 V1 pair) | not consulted by these three subcommands; pins unaffected |
| `safe.directory` / `safe.*` | no-op, same-uid (probe2 §4) |
| `extensions.objectFormat=sha256` in `.git/config` | git refuses loudly (`repo version is 0, but v1-only extension found`), never silently different |
| real sha256 repo built with `--object-format=sha256` | works, `repo_breach` null (no escape) |
| `core.repositoryFormatVersion=1`, `extensions.worktreeConfig` | harmless; `rev-parse` still reports the real worktree |
| write outside `d` from the parent-side calls | outside git dir snapshot unchanged (`outside_tree_changed: false`) |
| leg h shapes | outside file / dangling-outside / relative `../..` all refused; inside-only, `../f001` → back inside, absolute-inside: `null` (probe2 §5) |
| leg h TOCTOU | empty window: `d` is `--ro-bind` in every tool run, the build child exits before the checks, and a commanded survivor is torn down — `setsid bash -c 'sleep 3; …'` wrote nothing after bwrap exited (`destA_after_5s == ["now.txt"]`), a sibling `dest` write got `Read-only file system` (probe4 §B) |
| `path_ok` against argv symlinks / `..` | resolves before comparing, so a symlinked token is refused (`round43_c1_verify.py:392-403`) |
| `K43_SPAN` | present only in traced runs (`stdout "True 7,8"` traced vs `"False None"` untraced); supplied by the frozen `MUTANTS` span, not by any fixture; git ignores it |
| tracer output path | `open(out,"w")` at `:207` does follow a symlink planted at `<tmp>/k43-trace.txt`, but the write fails `EROFS` at the sandbox edge (`outside_target "UNTOUCHED"`), and the crash makes the traced run non-reproducing → the hit is skipped, so it degrades to `unattributed`, never a false kill (probe4 §A) |

**Leg-g note (not a finding).** `:815-822` requires the mutant's traced run to reproduce its untraced result
but only stability, not reproduction, from the reference's traced runs (`_r_rc`, `_r_cls` are discarded). If a
tool behaved differently under `sys.settrace`, the site records compared would come from different executions;
the direction is fail-safe (harder to kill) but the recorded `value=differs` would then mean less than it says.

**Limits of this review.** The threat model is a `plans/battery43` author, not the pinned tools: the `.git`
FILE and tracer-output vectors need a fixture, not a tool, so they are inside the boundary the counter
claims to police. I did not test cross-`--work` state, a hostile `TMPDIR`, jj state, or anything that needs a
different uid (the fixture repos are all mine, so ownership/safe.directory checks never fire). `SIDECHANNEL`
remains a heuristic: my own module avoided `core.` by writing `"co" + "re.worktree"`, which the scan cannot
see (named as a limit in the freeze).

## Reproduction

Probes and the two escape modules are beside this report (`probe1.py`…`probe4.py`, `m_escape.py`,
`m_fifo.py`); each needs `S=<scratch>` and its `lane` clone. Envelope lines for every run in this report
(the PATH-dir content digest was unchanged in all six — no measurement is invalid):

```
ENVELOPE ... -- env S=/fast/scratch/hyaku/kengaku-r43/R43SentinelCounter /usr/bin/python3 .../probe1.py
ENVELOPE start 19:09:26 cwd=/fast/scratch/hyaku/kengaku-r43/R43SentinelCounter
ENVELOPE end 19:09:38 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:10:24 ... end 19:10:26 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:11:48 ... end 19:11:50 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:12:00 ... end 19:12:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:12:06 ... end 19:12:08 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged   (dev-mode counter run, exit 1 = survived mutant, expected)
ENVELOPE start 19:12:58 ... end 19:13:05 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:13:42 ... end 19:14:14 exit=124 ... unchanged   (F4 hang, killed by `timeout 30`)
```

Tooling: nothing installed or upgraded (`git 2.x`/`python3 3.14`/`bwrap` as shipped).

VERDICT: c1-sandbox-findings-6-high-2
