# R43CritC1Counter — can a dishonest battery make `round43_c1_verify.py` green?

Seat: `R43CritC1Counter` (critic, round 43 wave 1). Target:
`kengaku-shokunin/plans/round43_c1_verify.py` (frozen digest in `claims/frozen-digests.txt`;
`PINS total=2 mismatched=0` in every run below) plus the two pinned tools
(`anchor_digest_check.py` `11bb2cad…`, `order_check.py` `948d5e1d…`). Lane clone at
`/fast/scratch/hyaku/kengaku-r43/R43CritC1Counter/lane` (tip `d33350fdb01ce27cbff47b04642fd2c1471e5c26`,
rev-parse toplevel asserted = the clone; nothing was committed there). Scratch
`/fast/scratch/hyaku/kengaku-r43/R43CritC1Counter` (sentinel present). Attack modules and receipts:
`.ufo/waves/round-43/build/R43CritC1Counter/`.

Every counter run was executed inside the round-43 envelope
(`claims/envelope.sh`: bwrap, `--ro-bind /home/vgpnk`, scratch overlaid, `~/.cache` scratch-backed,
`date +%T` start/end, `~/.local/bin` CONTENT digest). All receipts carry the `ENVELOPE` line; the
`~/.local/bin` content digest was `328be01808ba022f` before and after **every** run (14 runs), i.e.
no measurement was invalidated.

## 0. Method and positive control

- Dev mode (`--only`, `--battery-dir`, `--work $S/w`) on the lane clone; `PREDICATE C1 n/a` every time.
  A run with the empty battery reproduced the freeze control (`BATTERY fixtures=0 … survived=9`,
  `PREDICATE C1 n/a`, exit 1).
- **Positive control** (`run-B03-honest-na1.txt`): an honest NA1 fixture (a 12-cell SOURCES row)
  kills attributably:
  `MUTANT NA1 anchor silence killed by=a-na1-long-row attributed=L477 value=differs hits=1`;
  `BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0`. So the dev harness itself performs the
  frozen attribution machinery (legs f and g: span executed at L477, site record differs).

## 1. Round-42 substitutes re-tried against legs h/i

### V1 — receipt-is-directory (r42 `b-xo1`): **BLOCKED** (leg i)
`battery/B04_o_dir/o_receipt_dir.py`: `--receipt` names a directory present at HEAD. Counter:
```
SETUP fixture 'o-receipt-dir' of B04_o_dir/o_receipt_dir.py escapes its directory: --receipt corpus/evidence/r43/claimsdir is a tree at HEAD, not a blob
```
exit 2 (`run-B04-o-dir.txt`). The `./`-prefixed spelling is refused the same way
(`run-B05-o-dir-prefixed.txt`: `--receipt ./corpus/evidence/r43/claimsdir is a tree at HEAD, not a blob`),
so git's rev parsing normalises the prefix and the leg is not defeated by it.

### V2 — emptied-directory (r42 `b-xo3`): plain **BLOCKED**, absolute spelling **BYPASSES leg i** but yields no kill
- Plain: `battery/B11_emptied/o_emptied_dir.py` (dir created at freeze, removed, re-created at HEAD)
  → refus: `--receipt corpus/evidence/r43/claimsdir is a tree at HEAD, not a blob`, exit 2
  (`run-B11-emptied.txt`).
- Absolute spelling: `battery/B13_emptied_abs/o_emptied_dir_abs.py` passes `--receipt <abs path inside d>`.
  Leg i's `git cat-file -t "HEAD:<raw token>"` fails on an absolute path (`returncode != 0`), so the
  tree check is skipped; the tool normalises the absolute path back into the repo and proceeds:
  ```
  FIXTURE o-emptied-dir-abs tool=order expect=reject declared=- observed_rc=1 observed=- ok
  ```
  (`run-B13-emptied-abs.txt`; same bypass for the plain receipt-dir: `run-B06-o-dir-abs.txt`).
  **This is a fixable fence gap in leg i**: the blob check inspects the raw argv token while the tool
  resolves paths, so a path spelling the leg cannot parse escapes the check. It has **no green
  consequence for the frozen nine**: the tree-at-HEAD receipt trips order_check's unconditional clause 1
  for reference AND mutant alike (none of NO5/NO7/NO22 mutates clause 1), so `exhibits` stays empty
  (`MUTANT NO5 order rc-silence SURVIVED exhibits=none`).

### V3 — staged-manifest (r42 `b-x13`): **no mapping into the frozen nine** (blocked for green)
`battery/B09_staged/a_staged_index.py`: committed evidence + a staged-only `SHA256SUMS` asserting a made-up
digest, run under `--evidence-ref index`; the reference accepts (`observed_rc=0 ok`). Round 43's nine
mutants contain no index-mode site (the r42 X13 branch is not among them), so no frozen direction can be
exhibited through this shape (`MUTANT NA1 … SURVIVED exhibits=none`).

## 2. New vectors from the ticket

### V4 — symlink inside d resolving inside d / shared with another fixture: **ACCEPTED, inert** (leg h narrowness)
`battery/B01_symlink_in/a_symlink_in.py`: `corpus/SOURCES.md` is a symlink to a real file inside d;
leg h passes and the green lane runs (`FIXTURE a-in-symlink … observed_rc=0 ok`, `run-B01-symlink-in.txt`).
Cross-fixture sharing in **hard** form is also accepted: `battery/B12_hardlink/a_hardlink_shared.py`
hard-links fixture 0's blob into fixture 1 (leg h only checks symlinks); both fixtures green
(`run-B12-hardlink.txt`). Neither shape changes any measured split — content is static and symmetric, so
nothing here can forge a kill.

### V5 — symlink under d resolving outside d: **BLOCKED** (leg h)
`battery/B02_symlink_out/a_symlink_out.py`: link target = module dir outside d →
`SETUP … escapes its directory: symlink repo/corpus/SOURCES.md -> …`, exit 2 (`run-B02-symlink-out.txt`),
matching control h5.

### V6 — `.git/config` keys (`include.path`, pager, `diff.external`, textconv, aliases for the exact tool commands): **BLOCKED**
`battery/B07_config/o_config_keys.py`: a green order history with `[alias]` entries for exactly the command
names the tools issue (`log`, `rev-list`, `rev-parse`, `cat-file`, `ls-tree`, `merge-base`, `ls-files`),
each `!printf 'MARKER-…'`, plus pager / `diff.external` / textconv / `include.path` (keys assembled; module
source clean). Result: `FIXTURE o-config-keys … observed_rc=0 ok`, `sidechannel=0`
(`run-B07-config.txt`). Independent verification in a scratch repo: git does **not** expand aliases for
built-in commands (`alias.log` configured, `git log` still real; a non-builtin alias `trick` does fire),
and the tools' plumbing-only command set never runs pager/textconv/external/` diff. No per-variant
difference can be manufactured this way.

### V7 — reach a direction through a crash: **BLOCKED**
`battery/B08_crash/a_crash.py` (anchor, no SOURCES.md → exit 2) and `o_crash.py` (order, receipt never
committed → exit 2) both declared `expect=error` and check `observed_rc=2`; for every frozen mutant the
result is `SURVIVED exhibits=none` (`run-B08-crash.txt`). Both tools convert every exception to exit 2,
and every direction requires the mutant rc to be 0/1 (or, for `error`, a mutant that does not exist among
the nine). No crash-based kill exists.

### V8 — symlink-blob claims (explored reachability): **WORKS as an exotic but genuine demonstration**
`battery/B10_symlink_blob/o_symlink_blob.py`: a symlink committed under `.ufo/waves/round-NN/claims/` is
a blob whose content is its target string — which can itself be the forbidden/excused P10 sentence.
Leg i passes (it is a blob at HEAD). Both order kills become attributable:
```
MUTANT NO5 order rc-silence killed by=o-symlink-blob-late attributed=L120 value=differs hits=1
MUTANT NO7 order rc-mirror killed by=o-symlink-blob-excuse attributed=L60 value=differs hits=1
```
(`run-B10-symlink-blob.txt`, `BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0`). These kills *do*
exercise the advertised semantics (a committed claims blob whose content is the gate line / the P2 echo
trips the token heuristic exactly as order_check documents), so they are demonstrations, not substitutes — 
but the blob type is exotic and worth a reviewer's eye.

## 3. Verdict

No dishonest battery reaches the frozen predicate for the nine mutants. Legs h and i close the round-42
substitutes in their plain spellings; the absolute-path spelling of `--receipt`/`--claims` bypasses leg i's
blob check but kills nothing because none of the nine mutants alters order_check's unconditional clauses;
config-driven execution and crash-direction splits are structurally impossible for these two tools; the
nine directions require genuine ref/mutant splits that only the advertised semantics can produce. The
residual fence gaps (leg i raw-token parsing; token scan heuristic; inside-d symlinks/hardlinks permitted;
alternates-style object sharing is also unguarded) are findings for the L1, not green routes.

| vector | result | evidence |
|---|---|---|
| V1 receipt-is-directory (plain, `./`) | blocked (leg i) | run-B04, run-B05 |
| V2 emptied-directory plain | blocked (leg i) | run-B11 |
| V2' emptied-directory / receipt-dir absolute argv | **fence gap** (bypasses leg i), no kill | run-B13, run-B06 |
| V3 staged-manifest | no mapping into the nine | run-B09 |
| V4 symlink inside d (shared file / hardlink) | accepted, inert | run-B01, run-B12 |
| V5 symlink out of d | blocked (leg h) | run-B02 |
| V6 config keys incl. aliases | blocked | run-B07 + manual alias check |
| V7 crash-direction | blocked | run-B08 |
| V8 symlink-blob claims | works (genuine demonstration) | run-B10 |
| Positive control NA1 honest kill | works | run-B03 |

## 4. Receipts

All under `.ufo/waves/round-43/build/R43CritC1Counter/` (sha256 in `receipts.sha256`; none over 1 MiB;
battery module hashes listed there too). `~/.local/bin` content digest `328be01808ba022f` before/after every
run; envelope start/end timestamps are in each run-*.txt.

VERDICT: c1-counter-dishonest-green-blocked-vectors-9
