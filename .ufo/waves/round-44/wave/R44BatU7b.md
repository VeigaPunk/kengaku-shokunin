# R44BatU7b — `plans/battery44/u7_twin_b.py`: frozen mutant U7 killed, three fixtures

Seat `R44BatU7b`, kengaku round 44 (hyaku run 9, 2026-10-26), v2 wave (build + attack). Lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`; my clone `/fast/scratch/hyaku/kengaku-r44/R44BatU7b/lane`
(`git rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r44/R44BatU7b/lane`, HEAD
`5e3d3aa06c6b7000929ac3e62563a39159c4501f`). Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44BatU7b`,
`TMPDIR=$S`. Nothing outside my report dir, my subdir and `$S` was written; the lane was never edited, no git
mutation beyond `git clone --shared`, no commit, no push.

Frozen surface read first and unchanged: `plans/round-44-claims.md` (in full), `plans/round44_c1_verify.py`
(docstring, `MUTANTS`, `Ctx`, `build_module_child`, `Runner`, `main`), `plans/anchor_digest_check.py` (in full).
I did **not** open, import or copy `.ufo/waves/round-44/claims/witness/w_u.py` (the pre-freeze direction
module); my fixtures were derived only from the tool's own code and from U7's `old`/`new` text in the counter.

## 1. The mutant and the branch it changes

`MUTANTS` row U7 (`plans/round44_c1_verify.py`): tool `anchor`, class `-`, direction **`rc-mirror`**, adv_kind
`direct`, adv `plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures is
not a defect' (only the first resolving capture is claimed)`.

```
old  hit = sorted(p for p, ent in per.items() if tok in ent["digests"])
new  hit = sorted(p for p, ent in per.items() if tok in ent["digests"])[:1]
```

Replaced span = `plans/anchor_digest_check.py:539-542` (confirmed: L539 is the `hit = sorted(...)` line, L540
`claimed.update(hit)`, L541 `if verbose:`, L542 `path, how, label = row_scope[tok]`).

Trigger, read off the tool: a row whose `bind_row` returns N>1 captures (`per`, `len(per) > 1`) whose anchor
token is a 64-lowercase-hex digest **of more than one of those captures** — i.e. captures with byte-identical
content, so one digest is the true digest of all of them. Reference: `hit` = every such capture,
`claimed.update(hit)`, so no `capture-unanchored` line, exit 0. U7: `hit[:1]`, so all but the
lexicographically-first resolving capture stay unclaimed and the round-39 block emits
`class=capture-unanchored`, exit 1. That is exactly the declared `rc-mirror` (`expect=accept`, ref 0, mutant 1).

## 2. What was written

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU7b/battery/u7_twin_b.py`

- sha256 `6bee837959584e12577647fb280d1ea50228edf03106868ec2c4cb11087f4d89`, 133 lines, 6804 bytes.
- stdlib only: `import hashlib` is the only import; no file read, no subprocess, no `open(` (`grep -nE
  'import|open\(|read_text|subprocess|os\.' u7_twin_b.py` → only `22:import hashlib`).
- Manual SIDECHANNEL scan of the module text (case-insensitive, same 28 tokens as the counter, comments and
  strings included): `manual token scan hits: none`. The counter independently printed `sidechannel=0`.
- Every fid starts `u7_twin_b-`; module-level `FIXTURES` has three entries, `tool=anchor`, `expect=accept`,
  `defects=[]`; every `build(ctx, d)` fills the empty `d`, builds a repo at `d/lane` from nothing and returns
  `["--lane", <repo>]` (exact F3 anchor argv shape, one option pair).

| fid | shape | binding route | captures in the row | tokens |
|---|---|---|---|---|
| `u7_twin_b-url-trio-identical` | multi-row registry over two commits; three task dirs whose `test_outputs.py` bytes are identical, a fourth neighbour capture of its own | pinned URLs, two shapes: two `raw.githubusercontent.com/<owner>/<task>/<40hex>/<task>/tests/…` and one `github.com/<owner>/<task>/blob/<40hex>/<task>/tests/…` (`url-task`) | 3 identical + 1 (other row) | 1 in the trio row, 1 in the neighbour row |
| `u7_twin_b-prov-twin` | twin pair inside one evidence directory, no `task.toml`, three commits (captures → `PROVENANCE.md` → registry) | two `PROVENANCE.md` table lines naming the same sid, one local file each (`provenance-row`) | 2 identical | 1 |
| `u7_twin_b-mixed-trio` | three-capture row: a twin pair plus a distinct third capture, beside a clean single-capture row | pinned URLs (`url-task`) | 3 (2 identical + 1 distinct) | 2 (one per distinct digest) |

One-line comment per fixture, in the module, naming what it demonstrates (lines 55, 80, 102).

Why each is green under the reference and red under U7 (verified, §3–§6): the identical-bytes captures share
one digest, the row's token is that digest, `hit` = all of them → `claimed` = every capture → `defects=0`.
Under U7 the truncation drops all but one, so the round-39 per-capture loop reports the dropped ones.

## 3. Development-mode proof (`--battery-dir` + `--only U7`)

```
$ S=/fast/scratch/hyaku/kengaku-r44/R44BatU7b
$ "$S/../claims/envelope.sh" "$S/env" python3 .../plans/round44_c1_verify.py --lane "$S/lane" \
    --battery-dir .../wave/R44BatU7b/battery --only U7 --work "$S/w"
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU7b/env /fast/scratch/hyaku/kengaku-r44/R44BatU7b/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU7b/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU7b/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU7b/battery --only U7 --work /fast/scratch/hyaku/kengaku-r44/R44BatU7b/w
ENVELOPE start 20:36:48 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u7_twin_b-url-trio-identical tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-prov-twin tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-mixed-trio tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U7 anchor rc-mirror killed by=u7_twin_b-url-trio-identical attributed=L539 value=differs hits=3 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:36:50 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Every FIXTURE line `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`,
`U7 … killed by=u7_twin_b-url-trio-identical attributed=L539 value=differs hits=3` — all three fixtures exhibit
the declared direction (`hits=3`), the kill is attributed to the span line L539 (leg f) and its site record
differs from the reference's (leg g). Receipt: `wave/R44BatU7b/receipts/dev-u7.txt`
(sha256 `7e6c35f1375919d6584fadf88ff5050111ed4094b823df330de45bccd5a232f8`).

## 4. Full default counter on the clone (module in `plans/battery44/`)

```
$ cp .../wave/R44BatU7b/battery/u7_twin_b.py "$S/lane/plans/battery44/u7_twin_b.py"   # sha256 6bee8379…4d89 both sides
$ .../claims/envelope.sh "$S/env" python3 .../plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"
ENVELOPE start 20:36:52 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u7_twin_b-url-trio-identical tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-prov-twin tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-mixed-trio tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror killed by=u7_twin_b-url-trio-identical attributed=L539 value=differs hits=3 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:36:54 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`PREDICATE C1 fail` and `survived=4` are expected and are not this seat's scope: my clone's `plans/battery44/`
holds only my module, so U5, U6, U9 and U14c have no fixture here (other seats own those modules). U7 is the
one mutant this module is for, and it is killed. Receipt: `wave/R44BatU7b/receipts/full-default.txt`
(sha256 `c41b6e1fd03197d26f36bb802b5acd2190a17aeb3d29248fa13fa6d2ff819336`).

## 5. Load-bearing and sufficiency tables

Both tables use regenerated variants of the module in `$S/lb/<fid>/` and `$S/only/<fid>/` (one `FIXTURES`
entry removed / only that entry kept; nothing else changed), each run with `--battery-dir <variant> --only U7`
inside the envelope. Exit 0 in every row.

| module state | fixtures | U7 result | killed by |
|---|---|---|---|
| full module | 3 | killed, `attributed=L539 value=differs hits=3` | `u7_twin_b-url-trio-identical` |
| without `url-trio-identical` | 2 | killed, `hits=2` | `u7_twin_b-prov-twin` |
| without `prov-twin` | 2 | killed, `hits=2` | `u7_twin_b-url-trio-identical` |
| without `mixed-trio` | 2 | killed, `hits=2` | `u7_twin_b-url-trio-identical` |
| only `url-trio-identical` | 1 | killed, `hits=1` | `u7_twin_b-url-trio-identical` |
| only `prov-twin` | 1 | killed, `hits=1` | `u7_twin_b-prov-twin` |
| only `mixed-trio` | 1 | killed, `hits=1` | `u7_twin_b-mixed-trio` |

Reading: **no single fixture is load-bearing** (removing any one leaves the kill, by another fixture), and
**each fixture is independently sufficient** (each alone kills U7 with `wrong=0 tampered=0 sidechannel=0
null_detected=0 unattributed=0`). The three fixtures are three independent routes to the same branch, which is
the intended redundancy: a re-spelling or a single accidental trigger cannot carry the kill.

Receipts (sha256): `lb-without-u7_twin_b-url-trio-identical.txt` `89c6ba4cf7ebe3c15cb0e03385c4f5b5f58b0395674df1571d73d3d6b84e09c7`,
`lb-without-u7_twin_b-prov-twin.txt` `70fa4e8bd57f220aadc8347529ec85765359ee15fe89fb2255a578441da1ed1c`,
`lb-without-u7_twin_b-mixed-trio.txt` `c9fcccf836cc8bba05d568c7c878d2b36fa13064dbe812fd51040238faab6da0`,
`only-u7_twin_b-url-trio-identical.txt` `b26a35fb0b64b42055c53c1cded16540ad245031678beb59d07b330a82c6c20e`,
`only-u7_twin_b-prov-twin.txt` `008ee8d42052f75b2be160c957f6e62ae950712b0cad8793c7146db3bfc31810`,
`only-u7_twin_b-mixed-trio.txt` `4499265a79fdf43d881377d71e7e7b3edf27d77ac2ad4bab35818ca90b0752a8`.

## 6. Direction receipts: the tool's own lines, reference vs U7

Fixtures built with the counter's own builder (`--build-module ... --dest $S/mb`, inside the envelope), U7's
mutant copy produced by the one text replacement above (`$S/mb/u7_mutant.py`), both run inside the envelope on
`$S/mb/f00k/lane` (f000 = url-trio-identical, f001 = prov-twin, f002 = mixed-trio).

```
f000 reference exit=0 0 defect lines       rows=2 tokens=2 defects=0
f000 U7        exit=1 2 defect lines       DEFECT S201 anchor token=- class=capture-unanchored detail=row-names-3-captures-1-anchor-token-none-resolves-capture-corpus/evidence/r44t/tb2-payload-mux/test_outputs.py loc=corpus/SOURCES.md:3
                                           DEFECT S201 anchor token=- class=capture-unanchored detail=row-names-3-captures-1-anchor-token-none-resolves-capture-corpus/evidence/r44t/tb2-tidal-gauge/test_outputs.py loc=corpus/SOURCES.md:3
                                           rows=2 tokens=2 defects=2
f001 reference exit=0 0 defect lines       rows=1 tokens=1 defects=0
f001 U7        exit=1 1 defect line        DEFECT S211 anchor token=- class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/r44p/bundle/ledger.txt loc=corpus/SOURCES.md:3
                                           rows=1 tokens=1 defects=1
f002 reference exit=0 0 defect lines       rows=2 tokens=3 defects=0
f002 U7        exit=1 1 defect line        DEFECT S221 anchor token=- class=capture-unanchored detail=row-names-3-captures-2-anchor-token-none-resolves-capture-corpus/evidence/r44m/tb2-ring-b/transcript.txt loc=corpus/SOURCES.md:3
                                           rows=2 tokens=3 defects=1
```

The `rows=`/`tokens=`/`defects=` lines and the exit codes are the tool's; `ENVELOPE start/end` lines for each
run are in the receipt files. Note f001: the truncation keeps `ledger-copy.txt` (lexicographically first) and
drops `ledger.txt` — the drop is on the sorted order, not on any semantic choice. Note f002: the row has two
tokens, so the mutant's damage is confined to the twin pair (`tb2-ring-b`), leaving the distinct third capture
claimed by its own token.

Receipts: `direction-f000-ref.txt` `ea13e438ac168496a2bc14ddecb03e4dfa18851e314d3d9a889a1307d534d7c2`,
`direction-f000-u7.txt` `0f62d7d7ca0566973099210289b4448509b27ff63197f02475720ce777918f07`,
`direction-f001-ref.txt` `5b5e101449d99d15b81b3c34d7e38c013e0631c358bf814c153a51895d899a62`,
`direction-f001-u7.txt` `97eea75e26911cdc994b2657bc52369936f489bac9afd314a5d96ab9c9816843`,
`direction-f002-ref.txt` `a27a7535b98128db0aa1beded3d35c349d6adbee6169c27a2fd5414fd99c4b6b`,
`direction-f002-u7.txt` `bd78e37d46580dbe683ab2e8f879a18df4f33fdb7c1f2945ea42074e8f922fc0`.

## 7. Host safety and isolation

Every build, tool run, counter run and probe above ran through
`.ufo/waves/round-44/claims/envelope.sh "$S/env" <command>` (home read-only, `~/.cache` overlaid from scratch,
start/end time, content digest of `~/.local/bin` before/after). Every envelope closed with
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, exit 4 never fired: 15 envelope
lines across §3–§6 and the variant runs, all `unchanged`. The counter itself additionally runs each fixture
build and each tool run in its own `bwrap --ro-bind / /` sandbox with the lane hidden, a fixed PATH and no
network. No write to any PATH directory, `/usr`, `/etc`, `$HOME`, the fleet root, a sibling lane or the lane's
git state; no `pacman`, no install, nothing fetched.

## 8. Limits named

1. **Independence from `claims/witness/w_u.py` is by construction, not measured.** I did not open that module,
   so I cannot show a token- or shape-level difference; a non-author review (the counter cannot see intent) is
   the check, and this module's three shapes (URL trio across two URL shapes, `PROVENANCE` twin pair, mixed
   trio with two tokens) were designed from the tool's own code and U7's `old`/`new`.
2. **A kill is a result difference in the declared direction on a fixture that runs the mutated line and
   changes its site record, not a statement about intent.** `hits=3` means all three fixtures exhibit
   `rc-mirror`; the counter attributes the kill to the first one that survives the span/value legs.
3. **My three fixtures are redundant, not load-bearing** (§5): with any one removed the mutant still dies. A
   reviewer who wants a single-fixture battery can take any one of the three.
4. **`PREDICATE C1 fail` on the full run is scoped, not a defect of this module**: `survived=4` are the four
   mutants other seats' modules own; my clone has no `plans/battery44` fixture for them.
5. **The fixtures are constructed end states, not real registries.** They are the tool's advertised
   multi-capture shape (identical bytes, one digest) instantiated minimally; the tool's other binding routes
   (`row-path`, `provenance-url`) are not exercised here.
6. **`defects=[]` for all three** is asserted against the reference tool as it stands (`PINS total=2
   mismatched=0` before and after every run), not against the frozen digest of a future tip.
7. The development-mode runs print `PREDICATE C1 n/a` by design (non-default battery or mutant subset); they
   are evidence of the fixture lines and the U7 kill, not of the C1 predicate.

VERDICT: battery44-u7_twin_b-U7-killed-yes-fixtures-3
