# R44CritEquivU — critic review of the round-44 C1 frozen mutants (U5 U6 U7 U9 U14c)

Seat: `R44CritEquivU` (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (clone `$S/lane`).
Scratch: `$/=/fast/scratch/hyaku/kengaku-r44/R44CritEquivU`. Every run inside the round-44 envelope
(`claims/envelope.sh`); `local_bin_content_before=after=328be01808ba022f unchanged` on every run below.

## 1. Per-mutant findings (equivalent / redundant / misquoted)

| id | tool | class | direction | old → new (code span) | adv quote check | verdict |
|---|---|---|---|---|---|---|
| U5 | anchor | digest-short | silence | `("digest-short" if len(tok) < 64 else "digest-long")` → label `<64` as long (anchor_digest_check.py:522) | verbatim prefix of line 88; cite `:88` exact | not equivalent, not redundant |
| U6 | anchor | digest-long | silence | same line → label `>64` as short (:522) | verbatim prefix of line 88; cite `:88` exact | not equivalent, not redundant |
| U7 | anchor | – | rc-mirror | `hit = sorted(p for p, ent in per.items() if tok in ent["digests"])` → `[:1]` (:539) | verbatim across 98–99; cite `:98-99` exact | not equivalent |
| U9 | anchor | – | rc-mirror | `f.read_text(encoding="utf-8", errors="replace")` → `git(lane,"show","HEAD:"+p).decode(...)` (:384) | verbatim across 106–107; cite `:106-107` exact | not equivalent |
| U14c | order | – | error | `if not m:` → `if False:` (order_check.py:161-162) | verbatim segments across 26–27; cite `:26-27` exact | not equivalent |

**No misquotes.** Each `adv` cell quotes the docstring verbatim at the cited file:line (U5/U6: the sentence
begins at line 88 and the quoted part is fully contained in it; U7/U9/U14c span exactly the two cited lines,
newline replaced by space). Each cited sentence advertises exactly the behaviour the mutant breaks:

- U5/U6 — docs line 88: "any other anchor token must be exactly 64 lowercase hex digits (`digest-short`,
  `digest-long`, `digest-uppercase` otherwise)". Code line 522 splits `<64 → digest-short`, `>64 → digest-long`.
  U5 mislabels short tokens as `digest-long`; U6 mislabels long tokens as `digest-short`. Both leave the defect
  (exit 1) but change the advertised class — the `silence` direction.
- U7 — docs lines 97-100: "A token that resolves to several of the row's captures is not a defect — that means
  those captures have identical bytes…". Mutant claims only the first resolving capture (`[:1]`), so on a row
  that names N>1 captures the second capture stays unclaimed and `check()` (:547-556) emits
  `capture-unanchored`: accept → reject, `rc-mirror`.
- U9 — docs lines 105-108: "lessons are read from the working tree for paths committed at HEAD, so a seat's
  erratum counts before it is committed". Mutant reads the HEAD blob instead, so an erratum present only in the
  working tree no longer exempts the row: accept → reject, `rc-mirror`.
- U14c — docs lines 26-27: "Exit: … 2 setup error (not a git work tree, claims or receipt never committed,
  unparseable round number, bad arguments)". The claims-name guard raises `SetupError` (exit 2) for a claims file
  whose name is not `round-NN-claims.md`; disabled, `m` is None and `m.group(1)` raises AttributeError (traceback,
  exit 1): 2 → 1, the `error` direction.

**No equivalents.** Every mutant has a reachable fixture state where its output differs from the reference in the
declared direction — demonstrated pre-freeze by the witness (`claims/witness/w_u.py`, read for review; shapes
below) through the unmodified round-44 counter: `witness-run.txt` shows `MUTANTS total=5 killed=5 survived=0
invalid=0 null_detected=0 unattributed=0`, every kill `attributed=L522/L539/L384/L161 value=differs`. Witness
shapes match the advertisement:

- `u5-sixty-three-hex`: 63-hex anchor token → reject, `digest-short` (U5 relabels it digest-long).
- `u6-sixty-five-hex`: 65-hex anchor token → reject, `digest-long` (U6 relabels it digest-short).
- `u7-twin-captures`: row names two byte-identical captures (`cap.txt` + `twin.txt`, same BODY), one token → accept
  (U7 leaves the second capture unanchored → defect).
- `u9-dirty-erratum`: lessons file committed without the erratum, then rewritten in the working tree with the
  erratum line → accept (U9 reads HEAD, misses the erratum → `digest-unknown` defect).
- `u14c-odd-claims-name`: `--claims plans/odd-claims.md` → reference exit 2 (SetupError), mutant exit 1.

Direction sanity is corroborated by the freeze control `claims/control-c1-direction-mislabel.txt`: U7 relabelled
`rc-silence` → `SURVIVED exhibits=0>1,rc-mirror` (the declared direction is the one that kills).

**No redundancy.** U5 and U6 mutate the same line but swap opposite labels and need disjoint states (short vs long
token); the witness kills each with a distinct fixture (`u5-sixty-three-hex` vs `u6-sixty-five-hex`), so neither
kill subsumes the other. U7, U9, U14c touch disjoint code paths and distinct advertised sentences.

## 2. Standing-battery re-check (battery42 + battery43)

Copied `plans/battery42/*.py` → `b42_*.py`, `plans/battery43/*.py` → `b43_*.py` (name-collision pairs `a_row.py`,
`o_scan.py` disambiguated by prefix, as in the L1 control), 71 fixtures declared, run through the round-44 counter
in a clean clone under the envelope:

```
ENVELOPE start 20:33:43 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
BATTERY fixtures=71 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:50 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

This reproduces `claims/control-c1-standing-batteries.txt` exactly (same 71 fixtures, same `killed=0 survived=5`,
same exit 1). **Claim confirmed: battery42+battery43 kill none of the five.**

## 3. Older batteries (battery40, battery41) through the round-44 counter

Both were run in a clean clone with `--battery-dir` under the envelope. Neither loads, so **zero of their
fixtures run** and none can kill a mutant:

- **battery40** — `SETUP` exit 2, module `b40/a_bind.py` fails to build:
  ```
  SETUP module b40/a_bind.py failed to build (rc=1): … File "…/mod_a_bind.py", line 54, in build_a27
      lane = ctx.clone(d / "lane")
  AttributeError: 'Ctx' object has no attribute 'clone'
  ```
  Round-40 battery modules use the round-40 `ctx.clone`/`ctx.lane` API, removed from the round-44 Ctx (which
  offers only `init`/`git`/`write`/`sh`); `l_refuse.py`/`l_rows.py` also target the `ledger` tool (not in the
  round-44 `TOOLS={anchor,order}`). (Receipt `b40.out` sha256 `dd1e7f059d843ec3be39d0c62309015a348c0fc82a894ab3b39415f3b772f9a4`.)
- **battery41** — `SETUP` exit 2, contract breach on the first fixture:
  ```
  SIDECHANNEL b41/r_ctl.py tokens=witness
  SETUP fixture 'r_ctl-t06-empty-equal-receipt' of b41/r_ctl.py breaks the contract
  ```
  All battery41 fixtures declare tools `receipts`/`sources` (round-41 tools), not in the round-44 `TOOLS`;
  `b41/r_ctl.py` also carries the SIDECHANNEL token `witness` (a sidechannel if it could load). (Receipt `b41.out`
  sha256 `e23a2b539d5cda9954f995cce17c56c06d5afa69bf6cecb67a0a1b9b150f406c`.)

(Receipt `b42b43.out` sha256 `84015c5ddfb44e493fd2d9e14c826469e9c884b87e3f530eecfc48b53aa9b182` — all three receipts
kept in `.ufo/waves/round-44/wave/R44CritEquivU/`, each < 1 MiB.)

## 4. Conclusion

All five frozen mutants are genuine, non-equivalent, pairwise non-redundant, correctly quoted advertisements of the
two tools' own docstrings (all `adv_kind=direct`). The standing battery claim re-verifies (0/5). Older batteries
battery40/battery41 cannot reach the round-44 counter at all (removed API / foreign tool set), so no committed battery
kills a mutant by a do-nothing control.

VERDICT: equivalent-0-misquoted-0-older-battery-kills-0
