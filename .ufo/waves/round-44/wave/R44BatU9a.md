# R44BatU9a — battery44 for frozen mutant U9 (lessons read from the working tree)

Seat: executor `R44BatU9a` (leaf). Lane repo, read-only: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
clone at `/fast/scratch/hyaku/kengaku-r44/R44BatU9a/lane` (tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f`; both
tool pins `11bb2cad…` / `948d5e1d…` verified by the counter's `PINS total=2 mismatched=0`).

Deliverable (draft for the L1 to land as `plans/battery44/u9_worktree_a.py`):
`.ufo/waves/round-44/wave/R44BatU9a/battery/u9_worktree_a.py`, 110 lines, stdlib only
(`hashlib`), sha256 `20f3d3da28f138c32d9f1cc99240308112567334b3c149f10f3f20c9074e92bd`.

## Target

`plans/anchor_digest_check.py:106-107` advertises “lessons are read from the working tree for paths committed at
HEAD, so a seat's erratum counts before it is committed while the digest it cites still has to be committed”. The
read is `anchor_digest_check.py:384` — `text = f.read_text(encoding="utf-8", errors="replace")` inside
`load_errata` (`:374`); mutant **U9** swaps it for `git(lane, "show", "HEAD:" + p).decode("utf-8", "replace")`
(one line for one line, span line 384). Declared direction **`rc-mirror`**: fixture `expect=accept`, reference
exits 0, mutant exits 1. Classes are none of the counter's concern here (the reference must print no `DEFECT `
line at all), so every fixture declares `defects: []`.

Every fixture is built from nothing (no lane clone): `ctx.init` makes the repo, evidence and `corpus/SOURCES.md`
and `corpus/lessons/*.md` are committed, and then the lesson is edited **in the working tree** so the only erratum
that exempts the row lives outside HEAD. Reference: exemption present → no defect, exit 0. Mutant: reads HEAD, the
erratum is gone, the row's own wrong token raises, exit 1.

## Fixtures (fid prefix `u9_worktree_a-`)

| fid | shape | reference | U9 |
|---|---|---|---|
| `u9_worktree_a-registry-wrong-capture` | 5-row registry (S201–S205) over `corpus/evidence/r44-registry/` with a `SHA256SUMS` manifest and a `task.toml`; two commits (captures+manifest+notes, then rows); worktree erratum exempts S201, whose anchor cell carries the **sibling capture's real digest** (beta) while the row names alpha | rc 0, no defect | rc 1, `digest-wrong-capture` |
| `u9_worktree_a-history-abbrev` | three-commit history, two committed lessons; a **committed** baseline erratum keeps S302 green in both variants, the worktree erratum covers S301's **8-hex abbreviation** (chosen off `alpha[:8]`, so never a resolving prefix) and its full digest | rc 0, no defect | rc 1, `abbrev-unresolved` |

One-line intent comments are on each `build` function. The registry fixture also carries a correctly anchored
sibling (S202), a second correct capture (S203), a resolving abbreviation (S204) and a tokenless row (S205), so the
reference's green state is a registry that exercises the tool's other branches, not a one-row stub. The history
fixture demonstrates the same branch a second way: the erratum cites a token form (an abbreviation) rather than a
64-hex digest, and HEAD still carries an erratum of its own, so the mutant demonstrably *parses* HEAD and the kill
is the missing working-tree line only.

Independence: `claims/witness/w_u.py` was **not read, imported or copied**; the module is stdlib-only, builds no
lane clone, and neither fixture shares a shape with the pre-freeze direction module (registry+manifest vs
three-commit history; wrong-capture digest vs abbreviation).

## Development run (inside the envelope)

`S=/fast/scratch/hyaku/kengaku-r44/R44BatU9a`; `TMPDIR=$S`.

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU9a/env /fast/scratch/hyaku/kengaku-r44/R44BatU9a/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU9a/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU9a/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU9a/battery --only U9 --work /fast/scratch/hyaku/kengaku-r44/R44BatU9a/w
ENVELOPE start 20:33:55 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u9_worktree_a-registry-wrong-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_a-history-abbrev tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=2 -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:57 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`hits=2` — both fixtures exhibit `rc-mirror` on their own; both are `ok` against the reference with the declared
empty class set, `tampered=0` (no fixture tree changed under the tool runs), `sidechannel=0`.

Sidechannel scan (same token list as the counter, lowercased over the module source):
`python3 - <<EOF … [x for x in toks if x in text] EOF` → `[]` (no hits).

## Load-bearing table (each fixture removed in turn, `--only U9`)

Variants were produced in scratch by appending `FIXTURES = [f for f in FIXTURES if f["fid"] != "<dropped>"]` to a
copy of the module (the deliverable itself unchanged); receipts `receipts/u9-loadbearing.txt`.

| module variant | fixtures | U9 result |
|---|---|---|
| both (deliverable) | 2 | `killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=2` |
| drop `registry-wrong-capture` | 1 | `killed by=u9_worktree_a-history-abbrev attributed=L384 value=differs hits=1` |
| drop `history-abbrev` | 1 | `killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=1` |

```
ENVELOPE start 20:34:07 cwd=/home/vgpnk/Projects/shokunin
FIXTURE u9_worktree_a-history-abbrev tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-history-abbrev attributed=L384 value=differs hits=1 -- …
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
ENVELOPE end 20:34:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:34:11 cwd=/home/vgpnk/Projects/shokunin
FIXTURE u9_worktree_a-registry-wrong-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=1 -- …
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
ENVELOPE end 20:34:13 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Both fixtures are independently load-bearing (either one alone kills U9), so neither is decorative. The
attribution is the value leg: at the span line the frame's `text` is the worktree lesson in the reference and the
HEAD blob in the mutant, so the next-event locals digest differs (`value=differs`), and the reference's own two
traces agree (`unattributed=0`, not `site-record-unstable`).

## Full default counter on the clone (module copied to `$S/lane/plans/battery44/`)

`python3 …/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"` (no `--battery-dir`, no `--only`):

```
ENVELOPE start 20:34:19 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u9_worktree_a-registry-wrong-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_a-history-abbrev tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 …
MUTANT U6 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 …
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:98-99 …
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=2 -- plans/anchor_digest_check.py:106-107 …
MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 …
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:34:22 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

U9 is killed in the full run; the other four survive **because only this module is in the clone's `battery44`** —
they are other seats' targets (U5, U6, U7, U14c), and `PREDICATE C1 fail` is expected until the L1's integrated
battery44 lands. Nothing in this module touches another mutant's branch: both fixtures are anchor `accept` cases.

## Receipts

`receipts/` (all under 1 MiB, sha256):

- `u9-dev.txt` — `7f9f0b599c2af454f917656f49bafb083ac959327ae8ee88826854867650752b`
- `u9-loadbearing.txt` — `cd6dae1cebde7f84a0ecf0b3556a64017cb6d98242ba710b124e31ca490cd4c0`
- `u9-full.txt` — `62b036b5b175d11444adb1ed679c4a1bbd8bcff5ed53fab5149b6d6970542470`

Scratch `/fast/scratch/hyaku/kengaku-r44/R44BatU9a` (537 557 444 bytes) was removed with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44BatU9a "$S"`
(`DELETE path=… resolved=…` — the resolved path equalled `$S`). No tool was installed or upgraded; no pacman
call; nothing written to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the lane, or the fleet root. The clone was
`git clone -q --shared` with `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`; no commit, checkout,
stash or jj mutation anywhere.

## Limits named

1. One mutant, one branch: the module demonstrates `anchor_digest_check.py:384` (working-tree lesson read). It
   says nothing about the other four frozen mutants, and its green registry rows only witness the erratum path
   plus the plain resolution/abbreviation branches they happen to hit.
2. The exemption needs a committed capture to cite, so both fixtures must commit `corpus/evidence/` bytes; a
   fixture that only had a worktree erratum and no committed capture would fail the tool's own erratum-incomplete
   check and could not be green for the reference.
3. The kill's value attribution rests on the lesson text differing between worktree and HEAD; the two fixtures
   differ in *why* it differs (appended 64-hex erratum vs appended abbreviation erratum) but a mutant that read
   HEAD and still produced a byte-identical `text` on some other fixture would read `unattributed`, not killed.
4. The counter's token scan is a heuristic and I only re-ran its exact list (empty); non-author review that the
   module is not a re-spelling of `claims/witness/w_u.py` still belongs to the L1, since I did not read that file.
5. The `--only U9` and `--battery-dir` runs print `PREDICATE C1 n/a` by design; the clone's full run prints
   `PREDICATE C1 fail` because the other four mutants have no module in that clone yet. Neither is a C1 verdict.
6. `python3` here is the host interpreter and every run went through the round-44 envelope (`local_bin_content`
   digest identical before/after each run, `unchanged`); nothing here exercises the tools outside bwrap.

VERDICT: battery44-u9_worktree_a-U9-killed-yes-fixtures-2
