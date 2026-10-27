# R44BatU7a — battery44 module `u7_twin_a.py` (C1, frozen mutant U7)

Seat: executor R44BatU7a · round 44 (hyaku run 9), ONE v2 wave (build + attack) · 2026-10-26.
Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Frozen claims read in full:
`plans/round-44-claims.md` (freeze commit `5f16ed04b04a80a17a5a1a060c12093d9a152a64`). Nothing frozen was edited.
Scratch: `S=/fast/scratch/hyaku/kengaku-r44/R44BatU7a`; `TMPDIR=$S`; every run under
`claims/envelope.sh "$S/env" …`; clone `$S/lane` verified `rev-parse --show-toplevel` = `$S/lane`; no commit anywhere.

## 1. The frozen mutant, as read from the counter

`plans/round44_c1_verify.py:242-246` (`MUTANTS` table), verbatim:

```
('U7', 'anchor', '-', 'rc-mirror', 'direct',
 "plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures is not a defect' (only the first resolving capture is claimed)",
 f"{WR} (MUTANT U7); round-43 wave-1 R43PlanNext B.1 row 7",
 'hit = sorted(p for p, ent in per.items() if tok in ent["digests"])\n                claimed.update(hit)\n                if verbose:\n                    path, how',
 'hit = sorted(p for p, ent in per.items() if tok in ent["digests"])[:1]\n                claimed.update(hit)\n                if verbose:\n                    path, how'),
```

Tool branch (`plans/anchor_digest_check.py:538-552`, the `else` arm of a 64-hex token that IS in the row's
digest scope): `hit` collects **every** capture whose digest set holds the token; `claimed.update(hit)`; then the
`len(per) > 1` block prints `class=capture-unanchored` for each capture not claimed. The advertised sentence
(`:98-99`): “A token that resolves to several of the row's captures is not a defect — that means those captures
have identical bytes, and the one digest is the true digest of every one of them.” With `[:1]` the sorted-first
capture is claimed and the byte-identical twin is left unclaimed → one `DEFECT … class=capture-unanchored` line
and exit 1, where the unmodified tool prints nothing and exits 0. Declared direction `rc-mirror`
(`round44_c1_verify.py` `exhibits()`: `expect == "accept" and ref[0] == 0 and mut[0] == 1`). Fixtures therefore
declare `expect=accept`, `defects=[]` (anchor classes are the `class=` tokens of `DEFECT ` lines; an accept
fixture has none).

## 2. The module

Path (only file I wrote inside the fleet tree):
`.ufo/waves/round-44/wave/R44BatU7a/battery/u7_twin_a.py`
sha256 `8c322cf38293f34b82669734e793e75f8cb6d82071bdb7ac854e34bf387e66e5`, 6675 bytes, stdlib `hashlib` only.
SIDECHANNEL scan of its own text (case-insensitive, the counter's 29-token list) → `tokens []`:
`python3 - <<'EOF' … [x for x in SID if x in p.read_text().lower()] … EOF` printed `bytes 6675 tokens []`.
Every fid starts `u7_twin_a-`. Repos are built from nothing (`ctx.init`, `ctx.write`, `ctx.git`); no lane clone,
no symlink, `--lane <absolute path inside d>` only (argv shape `--lane V`).

| fid | shape | what it demonstrates (one line, as in the module) |
|---|---|---|
| `u7_twin_a-rowpath-registry` | five-row registry, binding route 3 (explicit lane paths), **two commits** | one digest claimed for two byte-identical filings in one evidence directory named by the row's own lane paths; the mutant leaves one unanchored (`ledger.txt` when the sorted-first is `ledger-mirror.txt`) |
| `u7_twin_a-provenance-table` | binding route 1 (`PROVENANCE.md`), one table line per commit | the same branch reached through a provenance table grown one line per commit (row `S610`, files `record.txt` / `record-copy.txt`) |
| `u7_twin_a-url-two-tasks` | binding route 2 (pinned raw URLs), two `task.toml` directories | the same branch reached through two pinned raw URLs under two task directories holding identical `solve.py` bytes (row `S620`, slugs `u7gamma` / `u7delta`) |

Green plumbing shared by all three (so a `wrong` would be visible): the single-capture rows with their own token
(`S500`, `S502`) and one row making no anchor claim (`S503` — the tool's own stated presence limit), header row
outside the census regex. Each build returns `["--lane", str(repo)]`, an absolute path under the fixture dir.

## 3. Proof run (development mode, U7 only) — inside the envelope

```
S=/fast/scratch/hyaku/kengaku-r44/R44BatU7a; export TMPDIR="$S"
.lane path: "$S/lane" (git clone -q --shared <lane>, toplevel verified)
.ufo/waves/round-44/claims/envelope.sh "$S/env" python3 plans/round44_c1_verify.py \
  --lane "$S/lane" --battery-dir .ufo/waves/round-44/wave/R44BatU7a/battery --only U7 --work "$S/w3"
```

Output (receipt `.ufo/waves/round-44/wave/R44BatU7a/dev-u7-receipt.txt`, sha256
`35116bc84d4ecd65359e0721e2641ee27ce15556e3ebd4d2676fce7c290ff999`; the file holds two identical runs):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU7a/env /fast/scratch/hyaku/kengaku-r44/R44BatU7a/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU7a/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU7a/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU7a/battery --only U7 --work /fast/scratch/hyaku/kengaku-r44/R44BatU7a/w3
ENVELOPE start 20:34:42 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u7_twin_a-rowpath-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-provenance-table tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-url-two-tasks tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U7 anchor rc-mirror killed by=u7_twin_a-rowpath-registry attributed=L539 value=differs hits=3 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:34:44 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Second identical run (`--work "$S/w5"`, same envelope end line, `20:34:49 … 20:34:51 exit=0 … unchanged`
appended to the same receipt). All three fixtures are `ok` (`wrong=0`), no tamper, no sidechannel, `null_detected=0`,
`unattributed=0`; the kill is `attributed=L539 value=differs` — span line 539 is exactly the replaced
`hit = sorted(...)` line (leg f ran it, leg g's site record differs because the mutant's `claimed` holds one path
where the reference's holds two).
`hits=3`: **every** fixture exhibits the declared `rc-mirror` on its own (see §4).

## 4. Load-bearing table

Two directions, each a fresh dev run (same envelope, `--only U7`; all exit 0, all `wrong=0 tampered=0
sidechannel=0 null_detected=0 unattributed=0`, `local_bin_content_before=…=328be01808ba022f … unchanged`):

| battery variant | fixtures | U7 result |
|---|---|---|
| module as written | 3 | killed, `attributed=L539 value=differs`, hits=3 |
| without `u7_twin_a-rowpath-registry` | 2 | killed `by=u7_twin_a-provenance-table` hits=2 |
| without `u7_twin_a-provenance-table` | 2 | killed `by=u7_twin_a-rowpath-registry` hits=2 |
| without `u7_twin_a-url-two-tasks` | 2 | killed `by=u7_twin_a-rowpath-registry` hits=2 |
| **only** `u7_twin_a-rowpath-registry` | 1 | killed `by=u7_twin_a-rowpath-registry` hits=1 |
| **only** `u7_twin_a-provenance-table` | 1 | killed `by=u7_twin_a-provenance-table` hits=1 |
| **only** `u7_twin_a-url-two-tasks` | 1 | killed `by=u7_twin_a-url-two-tasks` hits=1 |

Reading: no single fixture is load-bearing in the sense of being indispensable (removing any one still kills U7 —
the three are independent triggers of the same branch), and each one is load-bearing in the stronger sense that
each kills U7 **alone**, on its own binding route. Envelope lines for the removal rows: starts `20:33:47`,
`20:33:51`, `20:33:54`; solo rows: `20:34:06`, `20:34:10`, `20:34:13`; all end `exit=0 … unchanged`.

## 5. Full default counter on the clone (`plans/battery44` seeded with this module only)

```
test "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" && echo TOPLEVEL-OK   -> TOPLEVEL-OK
cp .ufo/waves/round-44/wave/R44BatU7a/battery/u7_twin_a.py "$S/lane/plans/battery44/"
cd "$S/lane" && .ufo/waves/round-44/claims/envelope.sh "$S/env" python3 plans/round44_c1_verify.py \
  --lane "$S/lane" --work "$S/w4"
```

Receipt `.ufo/waves/round-44/wave/R44BatU7a/full-default-receipt.txt`, sha256
`0e906f5841f1dc3c353a91c75115efa2a1d0adcd5b6c3b753115a35d9b375e32`:

```
ENVELOPE start 20:34:45 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU7a/lane
PINS total=2 mismatched=0
FIXTURE u7_twin_a-rowpath-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-provenance-table tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-url-two-tasks tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror killed by=u7_twin_a-rowpath-registry attributed=L539 value=differs hits=3 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:34:47 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

U7 killed (attributed, value differs); the four other frozen mutants survive because no other seat's battery44
module is present in this clone — expected per the assignment, not a defect of this module. `PREDICATE C1 fail`
and exit 1 are the correct result for a one-module battery.

## 6. Host safety and hygiene

- Every build, tool run and counter run was executed under `claims/envelope.sh` (bwrap: host `/home/vgpnk`
  read-only, `$HOME/.cache` overlaid from scratch, `/home/vgpnk/.local/bin` content digest
  `328be01808ba022f` **unchanged** before/after in all seven envelope brackets; no `INVALID`, no exit 4).
- No writes to any PATH directory, `/usr`, `/etc`, `$HOME` outside scratch, the lane's `corpus/`, `plans/`,
  git index or jj state, the fleet root, or any sibling lane. Only files written outside scratch:
  `.ufo/waves/round-44/wave/R44BatU7a/battery/u7_twin_a.py` (the assigned module), this report and the two
  receipts beside it.
- No tool installs or upgrades (nothing needed; `/usr/bin/python3` 3.14.8, `/usr/bin/bwrap` present). No pacman,
  no `-Sy`/`-Syu`.
- Fixture repos live only inside the counter's sandboxed scratch (`$S/w*`) and were removed by the counter;
  `$S/lane` got the battery44 copy (the mandated proof step) and was never committed.

## 7. Limits hit or named

1. **Kill rule ≠ intent.** The counter records a result difference in the declared direction on a fixture that
   runs the replaced line and changes the site record. `attributed=L539` proves the span ran; it does not prove
   the *twin* semantics are the only cause. My three fixtures were each read for that cause (one token, two
   byte-identical captures, one evidence directory each), but the counter cannot see intent.
2. **Byte-identical is the premise, not a convenience.** A "pair" whose bytes differ cannot be resolved by one
   digest, so it is a different advertisement (`digest-wrong-capture` / two tokens) and would not be green under
   the unmodified tool. My twins share one body string by construction.
3. **Fixture 3 rides on plumbing.** The URL → `task.toml` slug binding route is battery43-covered behaviour used
   here only as a vehicle; if that route changed, the fixture would report `wrong` (or a defect) rather than
   exercise U7. Fixtures 1 and 2 then still kill U7 (§4).
4. **Presence limit carried.** Row `S503` makes no anchor claim and stays green; these fixtures certify the tokens
   present, not that every row carries one (the tool's own stated limit at `:106-107` block).
5. **Independence is by non-consultation.** I did not open, import, copy or read `claims/witness/w_u.py` or any
   sibling U7 module; the three shapes (lane-path registry / provenance table / URL-two-task) were chosen from
   the frozen claims and the three binding routes in the tool. The counter's token scan is a heuristic, so the
   non-author review of "not a re-spelling" stays part of admission.
6. **One mutant only.** The full default run still fails until the other seats' modules for U5, U6, U9, U14c land
   and a clean-clone landing run prints `killed=5 survived=0`; this module moves `anchor` from 0 to 1 of 4.
7. **Environment parity.** The tool ran on host `/usr/bin/python3` 3.14.8 inside bwrap, on a clone of the lane
   HEAD whose frozen tool digests matched (`PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`); the
   counter's `--jobs 8` default was used, and the two dev runs were byte-identical.

VERDICT: battery44-u7_twin_a-U7-killed-yes-fixtures-3
