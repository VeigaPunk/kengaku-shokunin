# R33IdGuard — scratch id-collision guard, produced and proven (kengaku round 33, hyaku run 7)

**VERDICT: guard-proven**

Seat: leaf, no dispatch. Access date for every source opened this round: 2026-10-25.
Scope honoured: the only lane writes are the six artifacts below plus this report. No `corpus/`
edit, no `plans/` edit, no git command beyond read-only `show`/`status`/`rev-parse`, no pacman,
no tool install (nothing needed; see §9).

## 1. Inputs (all read-only)

| role | path | state |
|---|---|---|
| frozen claims | `kengaku-shokunin/plans/round-33-claims.md` | read; §C1 kill rule binds this guard |
| registry, pre-append | `git show HEAD:corpus/SOURCES.md` | HEAD = `7895588`; **95** rows, ids ≤ `S102` |
| staged package | `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` | 181 lines, **175** ids, `S077`…`S251` |
| lane gate (cross-check only) | `plans/sources_adopt.py` | run with `--registry`/`--package`, no `--out` → writes nothing |

The registry input is the **committed blob**, not the working-tree file: the guard exists to run
*before* an append, so the pre-append registry is its only valid input. §7 shows why that
distinction is load-bearing this round rather than pedantic.

## 2. Artifacts on disk

All under `.ufo/waves/round-33/assimilation/` (wave evidence, committable):

| file | bytes | sha256 |
|---|---|---|
| `reg-ids` | 475 | `397dbe620e6327d483f7ed3a32ae920d2e5efb36abb9ad79d9ce8e4b92aa4131` |
| `staged-ids` | 875 | `2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c` |
| `collisions` | 95 | `662ef9de7f38440db5b317c85c2e6339e47f53c6df82e7a83e78a1b369dea34b` |
| `id-guard-proof.txt` | 7685 | `da2c0934d8063075471f7ec27b7976ba8b717b59bd1db081d9f4d982e76786f5` (final, 153 lines; §8 records the pre-§8 digest) |
| `id-guard-fixture-registry.md` | 390 | `d7f37405ec0c23712cc4fc7b567779853b893ca4d5a850227af934a80725694d` |
| `id-guard-fixture-staged.md` | 98 | `f5319c1e755260a71fb5393edbba51bbcfa569cc883f07fb49496e5a06c98fb4` |

Every number in this report was produced by the commands in §4–§6 and is reproduced verbatim in
`id-guard-proof.txt`; nothing here is transcribed from a summary.

## 3. Production commands (exactly as run)

```sh
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
STG=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
W=$LANE/.ufo/waves/round-33/assimilation
ANCH='^ {0,3}\|[[:space:]]*S[0-9]{3,}'

git -C "$LANE" show HEAD:corpus/SOURCES.md | grep -oE "$ANCH" | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > "$W/reg-ids"
grep -oE "$ANCH" "$STG"                      | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > "$W/staged-ids"
LC_ALL=C comm -12 "$W/reg-ids" "$W/staged-ids" > "$W/collisions"
```

`LC_ALL=C` is required: `comm` refuses/destroys on non-lexicographic order, and the host locale
would otherwise sort `S1xx` differently from the anchor's byte order.

## 4. Outputs

```
$ wc -l reg-ids staged-ids collisions
  95 reg-ids
 175 staged-ids
  19 collisions

$ sed -n '1p;$p' reg-ids          → S001 / S102
$ sed -n '1p;$p' staged-ids       → S077 / S251
$ seq -f 'S%03g' 1 102 | LC_ALL=C comm -23 - reg-ids
S087 S088 S089 S095 S096 S098 S099      # ids unused inside S001..S102
```

`collisions` (19, the deliverable file, verbatim):

```
S077 S078 S079 S080 S081 S082 S083 S084 S085 S086
S090 S091 S092 S093 S094 S097 S100 S101 S102
```

Reading of that list: every one of the 19 is a staged row whose id the registry already spends —
`S077`–`S086`, `S090`–`S093`, `S100` are mined rows, and `S094`/`S097`/`S101`/`S102` are the
round-32 **refusal** rows, which still occupy their ids (CORPUS rule 2: ids are never reused).
16 of the 19 (`S094`, `S097`, `S101`, `S102` among them) belong to staged content the C1 entry does
not adopt; the remaining three (`S093` mined; `S094`/`S097` the refused twins) are exactly the ids
C1 re-points or refuses. `S093` appearing here is correct and not a defect: the entry gains `S093`
in `used-by` and appends no staged `S093` row, and the guard's job is only to say "do not append a
row whose id is spent".

**The two ids C1 renumbers into are free:**

```
$ grep -cE '^S(103|104)$' reg-ids
0
$ grep -cE '^S(103|104)$' collisions
0
```

`S103` and `S104` are absent from `reg-ids` (verified: 0 occurrences) and therefore necessarily
absent from `collisions` (0 occurrences). This is the acceptance condition, met.

## 5. Proof the guard can fail (fixture, scratch `/tmp/r33-idguard/`)

Fixture registry with an **indented** row, fixture staged list naming the same id:

```
$ cat -A fake-registry.md
# fake registry (id-guard proof fixture, round 33)$
$
| id | source | kind |$
|---|---|---|$
  | S002 | indented fixture row that a column-zero anchor cannot see | docs |$
| S900 | registry-only row | docs |$
$ cat -A fake-staged.md
| S002 | staged fixture row colliding with the indented registry row |$
| S901 | staged-only row |$
```

Same pipeline, same anchor:

```
$ grep -oE "$ANCH" fake-registry.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > fake-reg-ids
$ grep -oE "$ANCH" fake-staged.md   | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > fake-staged-ids
$ LC_ALL=C comm -12 fake-reg-ids fake-staged-ids > fake-collisions
fake-reg-ids:    S002 S900
fake-staged-ids: S002 S901
fake-collisions: S002              → 1 collision line (nonempty ⇒ the guard CAN fail)
```

Discriminator control — the same fixture under a column-zero-only anchor
(`^[|][[:space:]]*S[0-9]{3,}`) must false-green, which is why the contract's 0–3-space anchor is
the one that has to be used:

```
bad-anchor reg-ids: [S900]
bad-anchor collision lines: 0
```

So the anchor is load-bearing, not decoration: an indented registry row is invisible to the
column-zero pattern and the collision silently passes.

Republication: the red run repeats from the **committed** fixture copies in
`.ufo/waves/round-33/assimilation/` (`comm -12` → `S002`, `lines=1`), so the proof does not depend
on surviving scratch.

## 6. Independent cross-check against the lane's own gate

```
$ python3 plans/sources_adopt.py --registry /tmp/r33-idguard/reg-head.md --package "$STG"
exit=3
registry=95 staged=173 collisions=17 malformed=2 duplicates=0 defects=167 prose=167
  collisions: S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S094 S097 S100 S102
  malformed: S093:escaped-pipe S101:escaped-pipe
```

The two parsers agree on 17 ids, and the difference is explained rather than papered over: the
gate's row parser rejects `S093` and `S101` as `escaped-pipe` rows and drops them from the staged id
list (173 instead of 175), so it never tests them for collision. The anchor guard sees the id
anyway and therefore reports the superset (19). For a collision guard the superset is the correct
behaviour — a malformed row that would be refused on schema grounds is still an id that must not be
appended twice — but the two checks are complementary: the gate owns schema/quote/`used-by`, the
guard owns id occupancy. Both refuse (exit 3); neither is a substitute for the other.

## 7. Ordering disclosure — the worktree is already past the append (not this seat's edit)

Recorded at the start of this seat's run, before any artifact was written:

```
$ git -C "$LANE" status --porcelain corpus/SOURCES.md
 M corpus/SOURCES.md        # another seat's in-flight C1 append; this seat wrote nothing under corpus/
```

That in-flight append already places `S103` (`Toolathlon … evaluation/main.py`) and `S104`
(`LLMs-as-Judges … 2412.05579`) in the **working-tree** registry. Consequences, measured:

```
$ grep -oE "$ANCH" "$LANE/corpus/SOURCES.md" | … | sort -u > reg-ids-worktree   → 97 ids
$ LC_ALL=C comm -12 reg-ids-worktree staged-ids | wc -l                          → 21
$ LC_ALL=C comm -13 collisions collisions-worktree
S103
S104
```

and the reason those two appear is a real double-allocation in the staged package, not a guard bug:

```
worktree  | S103 | Toolathlon task evaluation script (evaluation/main.py) …
worktree  | S104 | LLMs-as-Judges: A Comprehensive Survey …
staged    | S103 | LLMs-as-Judges: A Comprehensive Survey … (full text) …
staged    | S104 | GENIAC事業 第1期 基盤モデル開発 事業説明 …
```

The renumbering `staged S094 → S103` and `staged S097 → S104` picks ids the *staged package itself*
already spends on two other documents. Nothing is wrong with the lane's new rows — they are the
only `S103`/`S104` in the registry — but two facts must be recorded by the integrator:

1. The guard's green result is only meaningful against the **pre-append** registry (`HEAD`,
   `7895588`). Run against the post-append worktree it reds out by construction (21 collisions),
   which is not a regression: it is the guard correctly reporting that the append has happened.
2. The staged rows `S103` (LLMs-as-Judges full text) and `S104` (GENIAC phase-1) must **never** be
   appended, now or in a later round, or the registry acquires two ids for four documents. This is a
   new standing constraint the round-32 lesson's id-collision note does not yet carry.

## 8. Findings, risks, blockers

- **F1 (guard proven, non-vacuous):** the contract pipeline detects a colliding id from an indented
  row (1 collision) and the column-zero variant misses it entirely (0) — the fixture is committed
  and re-runs from lane bytes.
- **F2 (result):** pre-append registry 95 / staged 175 / collisions 19; `S103`, `S104` free in both
  `reg-ids` and `collisions`.
- **F3 (parser divergence, benign, now documented):** anchor guard 175/19 vs gate 173/17, difference
  = `S093`/`S101` escaped-pipe rows. Guard = superset.
- **F4 (ordering hazard):** the append preceded the guard in wall-clock terms; the green verdict is
  valid only against `HEAD:corpus/SOURCES.md`. Recommend the receipt format name its base commit
  (this report does: `7895588`) so a later reader cannot mistake a post-append red for a broken
  guard.
- **F5 (new standing constraint):** staged `S103`/`S104` identify different documents than the
  appended `S103`/`S104`; neither staged row may ever be appended.
- **R1 (residual, out of this seat's scope):** the guard is a shell convention, not enforced by any
  committed tool; `plans/sources_adopt.py` still refuses collisions when asked, so wiring the
  base-commit into that gate would remove the hazard permanently. Filed here, not implemented.
- **Blocker:** none. No check was skipped; every output above was produced on this host today.
  The receipt is time-bound (`id-guard-proof.txt` §9: artifact mtimes `2026-10-25 14:23:32 -0300`,
  recheck at `14:26:18 -03` byte-identical), and because the registry input is the committed blob
  at `7895588` the guard re-runs to the same bytes after the worktree moves further.

## 9. Tooling

No install, no upgrade, no package transaction (pacman is paused host-wide; none was attempted).
Tools used: `git` (read-only), GNU `grep`/`sed`/`seq`/`wc`/`comm`/`sha256sum`/`stat`/`cut`/`tr`,
`cmp`, `python3` (lane's own `plans/sources_adopt.py`, read-only invocation).

---

`VERDICT: guard-proven`
