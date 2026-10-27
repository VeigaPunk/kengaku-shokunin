# R44BatU6a — battery44 module `u6_long_a` (frozen mutant U6, attribute kill)

Seat: executor `R44BatU6a`, kengaku round 44 v2 wave (build + attack), lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44BatU6a`
(clone at `$S/lane`, `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`, HEAD `5e3d3aa06c6b7000929ac3e62563a39159c4501f`).

Deliverable: `.ufo/waves/round-44/wave/R44BatU6a/battery/u6_long_a.py`
(sha256 `5dceb2b274cdbe753ebfa7d37f02ea0b53ff31652acab020b0d8911c6b3fa778`, 140 lines, stdlib only, every fid
prefixed `u6_long_a-`).

## 1. The frozen behaviour this module attacks

Read from `plans/round44_c1_verify.py` `MUTANTS` (frozen, unedited) — all five literals below are quoted from that table:

| field | value |
|---|---|
| id / tool | `U6` / `anchor` (`plans/anchor_digest_check.py`, pin `11bb2cad…`, matched: `PINS total=2 mismatched=0` in every run) |
| class / direction / adv_kind | `digest-long` / `silence` / `direct` |
| advertised sentence | `plans/anchor_digest_check.py:88` "any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`" |
| `old` | `cls, why = ("digest-short" if len(tok) < 64 else "digest-long")` (single occurrence, at file line **522**, inside `check()`) |
| `new` | `cls, why = ("digest-short" if len(tok) < 64 else "digest-short")` |

The advertised contract is a **two-sided** label: under 64 hex digits → `digest-short`, over 64 → `digest-long`
(`anchor_digest_check.py:520-524`; the sibling `digest-uppercase` arm is a separate `else` at `:524`). U6 collapses the
long side onto `digest-short`, so a fixture is a kill only if it carries an anchor token **longer than 64 hex digits**
on a row the unmodified tool binds to a committed capture: then the reference prints `class=digest-long` and exit 1,
and the mutant prints `class=digest-short` and the same exit 1 — a silent relabelling, which is the declared direction.

## 2. Fixtures (4, each built from nothing by `build(ctx, d)`; no lane clone)

Every fixture returns `["--lane", "<fixture dir>"]` — argv shape F3-legal (`--lane V` only), the value is inside `d`,
and `github` discovery from it resolves to `d` itself (F1/F6: `ctx.init(d)` makes `d` the repo; `rev-parse
--show-toplevel` = `d`, `--absolute-git-dir` = `d/.git`). Declared `defects` = `["digest-long"]`, `expect = reject`
(reference exit 1), per the module contract: anchor defects are every `class=<C>` of a `DEFECT ` line.

| fid | shape | token | binding route | declared | observed (reference) |
|---|---|---|---|---|---|
| `u6_long_a-registry-65` | five-row registry; the long token is a **true digest plus one hex digit**, so length alone decides the label and not capture membership | 65 | row-path (`corpus/evidence/u6a/registry/…`) | `digest-long`, reject | rc=1, `digest-long` |
| `u6_long_a-manifest-96` | capture never committed as a blob; it exists only as a `SHA256SUMS` entry listed at the same directory | 96 | manifest entry (`dir_entries`) | `digest-long`, reject | rc=1, `digest-long` |
| `u6_long_a-provenance-128` | row names no path and no URL; the capture comes from a `PROVENANCE.md` table line that names both rows | 128 | provenance-row | `digest-long`, reject | rc=1, `digest-long` |
| `u6_long_a-history-200` | two-commit history: capture + clean row land first, the long token is appended in a second commit, so the class must fire against HEAD's evidence set | 200 | row-path | `digest-long`, reject | rc=1, `digest-long` |

Each fixture is load-bearing-in-shape, not redundant-in-kind: four different binding routes, four token lengths, one
two-commit history. The module contains none of the `SIDECHANNEL` tokens (`hits []`,
`python3` scan over the lowercased source with the counter's own 26-token tuple; the counter independently printed
`sidechannel=0`). The source carries one comment line per fixture naming what it demonstrates.

## 3. Dev-mode counter run (the required proof) — `--only U6`

Command (run under the round-44 envelope; `$S/w` scratch):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py \
  --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU6a/battery \
  --only U6 --work "$S/w"
```

Output (receipt `receipts/devrun-final.txt`, sha256 `843172575a803a5f99c756a3f34b33dfaeed9d429c7373ea6b2167c4022a6e0b`):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU6a/env /fast/scratch/hyaku/kengaku-r44/R44BatU6a/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU6a/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU6a/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU6a/battery --only U6 --work /fast/scratch/hyaku/kengaku-r44/R44BatU6a/w
ENVELOPE start 20:33:43 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u6_long_a-registry-65 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-manifest-96 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-provenance-128 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-history-200 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
MUTANT U6 anchor silence killed by=u6_long_a-registry-65 attributed=L522 value=differs hits=4 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:45 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Every required literal is present: four `FIXTURE … ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0
unattributed=0`, `U6 killed by=u6_long_a-registry-65 attributed=L522 value=differs`, `hits=4` (all four fixtures
independently exhibit the silence). Attribution legs: the traced re-run reproduces `(exit 1, {digest-long})` and
executes line 522 (§leg f), and its site record differs from the reference's over the same span (§leg g,
`value=differs`). `ENVELOPE … unchanged` — `~/.local/bin` content digest `328be01808ba022f` before and after; no
measurement invalidated, no re-run needed.

## 4. What the class flip actually is (direct probe, same fixtures, envelope-bracketed)

`receipts/flip.sh` builds the four fixtures with the counter's own hidden builder (`--build-module`) and runs the
unmodified tool and a U6 copy on each (receipt `receipts/classflip.txt`, sha256
`827f01da0bb2454120746c5b1ddf857ac36a08d43409489112e023192aa27c85`; `ENVELOPE start 20:33:46 … end 20:33:48 …
unchanged … 328be01808ba022f`):

| fixture | reference | mutant U6 |
|---|---|---|
| f000 | rc=1, 1 defect, `class=digest-long`, token_len=65 | rc=1, 1 defect, `class=digest-short`, token_len=65 |
| f001 | rc=1, 1 defect, `class=digest-long`, token_len=96 | rc=1, 1 defect, `class=digest-short`, token_len=96 |
| f002 | rc=1, 1 defect, `class=digest-long`, token_len=128 | rc=1, 1 defect, `class=digest-short`, token_len=128 |
| f003 | rc=1, 1 defect, `class=digest-long`, token_len=200 | rc=1, 1 defect, `class=digest-short`, token_len=200 |

Same exit status, class set differs: exactly the `silence` direction the frozen table declares, observed on four
independent shapes. This probe also caught my own arithmetic error before it reached the report: the first history
token was `(digest*3)[:200]` = 192 digits (comment and fid said 200); fixed to `*4` so the token really is 200, and the
dev run/flip/drop/full receipts below are all from the corrected module (`5dceb2b2…`).

## 5. Load-bearing table — remove one fixture at a time

Each row: a copy of the module with `FIXTURES = [fx for fx in FIXTURES if fx["fid"] != "<dropped>"]` appended, run with
`--only U6` under the envelope (receipt `receipts/drop-table.txt`, sha256
`52c3f04a954b14eb91cebf478ae48be969d818382e225bc5d49e1f6df6fb2cc0`; all four runs `ENVELOPE … unchanged … 328be01808ba022f`).

| dropped fixture | remaining | U6 result |
|---|---|---|
| `registry-65` | manifest-96, provenance-128, history-200 | **killed** by=`u6_long_a-manifest-96` `attributed=L522 value=differs hits=3` |
| `manifest-96` | registry-65, provenance-128, history-200 | **killed** by=`u6_long_a-registry-65` `attributed=L522 value=differs hits=3` |
| `provenance-128` | registry-65, manifest-96, history-200 | **killed** by=`u6_long_a-registry-65` `attributed=L522 value=differs hits=3` |
| `history-200` | registry-65, manifest-96, provenance-128 | **killed** by=`u6_long_a-registry-65` `attributed=L522 value=differs hits=3` |

Honest reading: **no single fixture is load-bearing**; the kill is redundant by construction (every fixture carries a
long token on a bound row, so each of the four exhibits the silence on its own — `hits=4` on the full module). The
module's value is breadth of shape (manifest-only capture, provenance table, two-commit history, appended-digit true
digest), not a single irreplaceable trigger. A future regression that broke one binding route would still leave three
killers; a regression that broke the four routes at once is not what this module is for.

## 6. Full default counter on the clone (`plans/battery44/`)

Module copied to `$S/lane/plans/battery44/u6_long_a.py` (byte-identical, sha256 `5dceb2b2…`; nothing committed —
`git -C "$S/lane" status --porcelain` shows only `?? plans/battery44/`). Command:

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

Output (receipt `receipts/fullrun.txt`, sha256 `b0a60ea0a5d6e3aaa16b5c122abeb150b2caa42f9d2726e4fe8dcb0854062a84`):

```
ENVELOPE start 20:34:13 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u6_long_a-registry-65 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-manifest-96 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-provenance-128 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
FIXTURE u6_long_a-history-200 tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence killed by=u6_long_a-registry-65 attributed=L522 value=differs hits=4 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:34:15 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

As expected for one module of five: U6 killed, `wrong=0 tampered=0 sidechannel=0 invalid=0 null_detected=0
unattributed=0`, `PREDICATE C1 fail` because the other four mutants have no fixtures here. Notably **U5 survives on this
module too** — the sibling "short token labelled digest-long" mutant is invisible to long-token fixtures — which is the
independence the wave wants: this module is U6-specific, not a general anchor-battery.

## 7. Development trail (recorded so the L1 can see what was wrong first)

1. First draft (`--only U6`) printed `FIXTURE u6_long_a-provenance-128 … observed=anchor-unbound,digest-long WRONG`
   (`wrong=1`, exit 1). Cause: the second row in that fixture named no path/URL **and** was not named on the
   `PROVENANCE.md` line, so `bind_row` returned `row-carries-no-capture-locator`. Fix: the provenance line names both
   sids (`| S981 S982 | `beta.bin` | fetched once by the seat |`), both rows bind by `provenance-row`.
2. Second draft passed `--only U6` (`wrong=0`), then the class-flip probe showed the history token was 192 digits, not
   200; fixed and all receipts re-measured from scratch (dev, flip, drop table, full run).

## 8. Limits hit / named

- **`PREDICATE C1 n/a`** in every dev run (by design: non-default battery dir + mutant subset). The frozen predicate
  needs the other four seats' modules; this module can only contribute `anchor=1` of the `anchor=4` floor.
- **No fixture is individually load-bearing** (§5). Redundancy is deliberate but means this module cannot detect a
  regression that leaves one binding route alive; it detects the U6 relabelling on any of four routes.
- **Independence from `claims/witness/w_u.py` is asserted by construction, not by diff**: I did not read, import or copy
  that module (the battery contract forbids it), so I cannot prove non-resemblance beyond stating my four shapes
  (manifest-only capture, provenance table, two-commit history, appended-digit true digest) were chosen from the tool's
  binding routes, not from a witness. The L1's non-author review is the intended check.
- **Only the anchor tool is exercised**; `order_check.py` / U14c gets no coverage here (`MUTANTS-BY-TOOL order=0/1`).
- **The counter prints no class set** for a killed mutant; the same-exit/class-flip reading comes from my own
  envelope-bracketed probe (§4), which re-derives the `new` line from the frozen table rather than importing it — a
  transcription risk, bounded by `assert src.count(old) == 1` and the counter's own `killed … value=differs`.
- **Token-scan is the counter's heuristic** (`sidechannel=0` plus my own scan); it does not prove intent.
- **Envelope**: every counter/probe run was inside `claims/envelope.sh`, `/home/vgpnk` read-only, `~/.local/bin` content
  digest `328be01808ba022f` unchanged before/after in all 7 envelope invocations; no run needed re-running for `exit 4`.
- Nothing installed or upgraded (stdlib `hashlib` only); no lane file, index, corpus, plans or SCORECARD touched; no
  commit/push anywhere; the only lane-side write was the untracked `plans/battery44/` copy inside the scratch clone.
- Scratch `$S` deleted at the end with `plans/scratch_guard.py safe-rm` after the receipts were copied here.

## 9. Receipts (in `.ufo/waves/round-44/wave/R44BatU6a/receipts/`)

| file | sha256 |
|---|---|
| `devrun-final.txt` | `843172575a803a5f99c756a3f34b33dfaeed9d429c7373ea6b2167c4022a6e0b` |
| `classflip.txt` | `827f01da0bb2454120746c5b1ddf857ac36a08d43409489112e023192aa27c85` |
| `drop-table.txt` | `52c3f04a954b14eb91cebf478ae48be969d818382e225bc5d49e1f6df6fb2cc0` |
| `fullrun.txt` | `b0a60ea0a5d6e3aaa16b5c122abeb150b2caa42f9d2726e4fe8dcb0854062a84` |
| `flip.sh` (probe driver) | `2ce885914b51dc2b7c2c3d863fd6953a2f905a58a6fb5a67020d8e1fd8aef53b` |

Module: `.ufo/waves/round-44/wave/R44BatU6a/battery/u6_long_a.py` sha256
`5dceb2b274cdbe753ebfa7d37f02ea0b53ff31652acab020b0d8911c6b3fa778` (byte-identical to the clone copy that produced the
full-run receipt).

VERDICT: battery44-u6_long_a-U6-killed-yes-fixtures-4
