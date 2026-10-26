# R36IdGuard — round 36 wave 1, build (executor)

Seat: R36IdGuard. Assignment: addendum §10 id-collision check at
`A=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/assimilation` (created), the
guard proof on an indented `  | S002 |` fixture, the §10 quarantine-slice derivation, and the
S108–S110 / held-package aliasing question. Host `linux 7.2.11-arch1-1`; lane HEAD
`f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd` (freeze `3241b86`, amendment 1 `acbda2f`). No tool
installed or upgraded (POSIX sh, grep, sort, comm, awk as shipped).

## 1. Real run — collision check (lane registry vs held staged package)

Contract anchor, exactly as assigned:

```sh
ANCH='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
grep -oE "$ANCH" corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > $A/reg-ids
grep -oE "$ANCH" /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md \
  | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > $A/staged-ids
LC_ALL=C comm -12 $A/reg-ids $A/staged-ids > $A/collisions
```

Observed output:

```
$ wc -l $A/reg-ids $A/staged-ids $A/collisions
  100 …/reg-ids
  175 …/staged-ids
   24 …/collisions
$ sed -n '1p;$p' $A/reg-ids      # S001 … S107
$ sed -n '1p;$p' $A/staged-ids   # S077 … S251
$ cat $A/collisions
S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S093 S094
S097 S100 S101 S102 S103 S104 S105 S106 S107   (one per line in the file)
```

- **reg-ids = 100** (S001–S107), **staged-ids = 175** (S077–S251, first `S077`, last `S251`),
  **collisions = 24**.
- The registry holds no duplicate id: `… | LC_ALL=C sort | uniq -d` prints nothing.
- Input digests: `corpus/SOURCES.md` `33549258a5ee4d9d68eec040b53f73c10c6e0179ba14c49b8dd5771fbe57e148`;
  staged `a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b` (177 759 B, mtime
  2026-10-24 23:33:20 −0300). `staged-ids` sha256 `2df53989…` is byte-identical to the round-33 and
  round-35 receipts — the merge package has not moved since round 33.
- All 175 staged ids are unique in the package (`sort | uniq -d` → empty); the min staged id is above
  the registry's floor, i.e. the package deliberately continues the lane's S-space, so overlap is
  expected pre-renumber state, not a package defect.

## 2. Guard proof — the 0–3-space allowance is load-bearing

Fixture `$A/guard-proof/` (files `guard-registry.md`, `guard-staged.md`), registry carrying an
**indented** `  | S002 |` row plus column-zero `| S900 |`, staged carrying `| S002 |` and `| S901 |`:

```
$ grep -oE "$ANCH" guard-registry.md | …             # S002 S900
$ grep -oE "$ANCH" guard-staged.md  | …             # S002 S901
$ LC_ALL=C comm -12 guard-reg-ids guard-staged-ids  # S002
$ wc -l < guard-collisions
1
$ BAD='^[|][[:space:]]*S[0-9]{3,}'                  # column-zero-only control, same fixture
$ LC_ALL=C comm -12 guard-reg-ids-badanchor guard-staged-ids | wc -l
0
```

Same fixture, two anchors: the contract anchor sees the indented `S002` and fires (1 collision); the
column-zero-only control sees only `S900` and returns 0. **The collision check is nonempty for an
indented collision ⇒ guard = ok.**

Two further indent controls (`guard-indent-4-vs-3.md`: one 4-space row `S003`, one 3-space row `S004`):

```
$ grep -oE "$ANCH" guard-indent-4-vs-3.md | …       # S004   (3-space parsed, 4-space excluded)
```

Disclosure, so the proof is not overclaimed: **both real inputs are column-zero today**
(`grep -cE '^ +\|[[:space:]]*S[0-9]{3,}'` → `0` for `corpus/SOURCES.md` and `0` for the staged file),
so the column-zero-only anchor returns the same 24 ids on today's data. The allowance's value is
forward-looking — a package or hand-edited row that arrives indented cannot false-green — and the
fixture, not the current tree, is what makes it measurable. The round-35/round-33 fixtures are the
same construction; this round's copy is independent and committed with its own receipts.

## 3. Guard hardening — the bare pipeline false-greens on a missing input

Exercised, not assumed:

```
$ grep -oE "$ANCH" /tmp/does-not-exist-SOURCES.md 2>/dev/null | … | sort -u > /tmp/empty-reg
$ LC_ALL=C comm -12 /tmp/empty-reg staged-ids > /tmp/empty-coll
collisions=0 pipeline_status=0     # reg-ids=0
```

A wrong `--registry` path (or an emptied/anchor-silent package) yields **0 collisions and exit 0** —
the exact false-green class R35-D1/R35-D4 name for the other counters. Receipt wrapper written at
`$A/id-collision-check.sh` (scratch, no lane surface): same anchor, plus `REFUSED: input absent` /
`REFUSED: anchor matched no row` → exit 2, real collisions → exit 3, clean → 0.

```
$ sh $A/id-collision-check.sh --selftest
SELFTEST reg=[S002 S900 ] staged=[S002 S901 ] indent=[S004 ] collisions=[S002 ] bad-anchor-collisions=0
SELFTEST guard-ok
$ sh $A/id-collision-check.sh ; echo exit=$?      # receipt: $A/receipt.txt
reg-ids=100 staged-ids=175 collisions=24
exit=3
```

The wrapper re-derives `reg-ids`/`staged-ids`/`collisions` with the identical digests (§5), so it is a
receipt, not a second rule.

## 4. Quarantine slice — §10 awk over the absent-defect register

Read-only register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(83 621 B, mtime 2026-10-24 08:37 −0300, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
— byte-identical to round 30's pinned copy, so the slice is not a re-derivation of changed input;
`grep -c '`kengaku`'` → 3 = the two data rows at lines 101–102 plus the `## By lane` count row
`| kengaku | 2 |` at line 252, which the id-cell condition excludes):

```sh
awk -F'|' -v l='kengaku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  absent-defect-register.md > $A/quarantine-slice
```

```
$ wc -l < $A/quarantine-slice
2
$ cat $A/quarantine-slice
 S091   `payload-absent` 
 S105   `payload-absent` 
$ sha256sum $A/quarantine-slice
6db0080e92291a9c686563174ba3ca512976828d36d311a54a77024034ad6a0e
$ cmp $A/quarantine-slice .ufo/waves/round-31/assimilation/quarantine-slice && echo byte-identical
byte-identical      # also identical to the round-34 and round-35 slices
```

**slice = 2** rows — `S091` (NEC技報 LLM article, `jpn.nec.com/techrep/journal/g23/n02/230212.html`) and
`S105` (GENIAC phase-1 results via the Internet Archive snapshot), both `payload-absent`. Disposition
unchanged: neither is adoptable and neither is cited by an admitted entry; the flip is a round that
fetches the payload and locates the quote. The **class cell is not a fabrication verdict** — per the
register's own header an ABSENT quote is "a CANDIDATE, not a verdict".

## 5. Does S108–S110 collide? Yes — all three, and with different documents

Current registry stops at S107 (`reg-ids` = 100, C2's rows have not landed yet at the time of this
run), so the honest measurement is against the staged list:

```
$ for id in S108 S109 S110; do grep -qx $id $A/staged-ids && echo "$id YES"; done
S108 YES
S109 YES
S110 YES
```

The staged package's rows at those ids are **not** this round's sources:

| id | staged package row (held, `merge/kengaku/SOURCES.append.md:38-40`) | this round's C2 row |
|---|---|---|
| S108 | Toolathlon per-task evaluation scripts (`add-bibtex`, `imagenet`, `excel-data-transformation`), commit `9be8d8f…` | TB2 `regex-log` `tests/test_outputs.py` |
| S109 | 大语言模型评测研究现状…, 情报学报 2025, 44(8):1058-1074 | TB2 `regex-log` `tests/test.sh` |
| S110 | GENIAC 第2期 性能評価結果詳細 (METI) | TB2 `regex-log` `instruction.md` |

So C2's adoption consumes three ids the held package also claims. Nothing breaks *this* round (the
registry has no S108–S110 yet, and C2's counter requires exactly one row each), but the constraint it
creates is concrete: **the held package's renumber floor moves from S108 to S111** — a `S108` row
appended from the package after C2 lands would be the second row with that id and would trip the
census's `uniq -d` duplicate-id check.

The same aliasing already exists for the quarantine slice and is easy to mis-cite: register/staged
`S091` is the NEC LLM article while lane `S091` is the ABC checklist (`arxiv.org/abs/2507.02825`);
register/staged `S105` is GENIAC phase-1 while lane `S105` is the TB2 `protein-assembly` grader. Any
adopted quarantine row must be renumbered, never cited under its staged id.

**Renumber map if the held round-35 package were adopted later** (two files, both under `$A/`):

- `$A/renumber-min` — **27 lines**, only the ids that collide with the post-C2 registry
  (24 decompressed above + S108/S109/S110), mapped in ascending order to `S111 … S137`:
  `S077→S111 S078→S112 … S107→S134 S108→S135 S109→S136 S110→S137`.
- `$A/renumber-full` — **175 lines**, every staged id in ascending order to `S111 … S285`
  (`S077→S111 … S251→S285`). This is the shape CORPUS rule 2 requires ("adopted ids continue the
  lane's registry"): the 148 staged ids that do not collide today (`S087–S089`, `S095`, `S096`,
  `S098`, `S099` among them) would otherwise be inserted *below* the tip, so a whole-package adoption
  renumbers everything, not just the colliding tail.

```
$ sha256sum $A/renumber-min $A/renumber-full
ed962eb0967dba5ed49641d18561296c3166591867ea795d35a9008c4be60042  renumber-min
3f45981e27d8b51e1f64704211cca1ec43f31270b81a5cc3105eec6edb4de432  renumber-full
```

| | staged ids | collisions vs current registry | collisions after C2 | map range |
|---|---|---|---|---|
| minimal | 175 | 24 | 27 | S111–S137 |
| full | 175 | — | — | S111–S285 |

## 6. Disclosures and limits

- Measurement used the **worktree** `corpus/SOURCES.md` as the assignment directs; it equals the HEAD
  blob in id content (100 rows, S001–S107, `git status --porcelain corpus/ plans/` empty), so no
  HEAD/worktree split this round (round 35 had one, from an in-flight C1 append; it is gone).
- C2's S108–S110 are **not yet in the registry** at run time (in-flight seats). §5 therefore reports
  staged collisions (direct) and the post-C2 collision count 27 (computed), not a measured registry.
- The collision set is a *set of ids*, not a verdict on any row; the staged package continuing the
  lane's S-space is expected pre-renumber state.
- The register is read only; no campaign tool was run. Source repo `/home/vgpnk/Projects/shokuknow`
  untouched. No lane file edited (scratch only, per seat bounds).

## Evidence inventory (all under `.ufo/waves/round-36/assimilation/`)

- `reg-ids` (100, `39a3d432…`), `staged-ids` (175, `2df53989…`), `collisions` (24, `0b231deb…`)
- `receipt.txt` (`reg-ids=100 staged-ids=175 collisions=24`, wrapper exit 3), `id-collision-check.sh`
- `guard-proof/`: `guard-registry.md`, `guard-staged.md`, `guard-reg-ids`, `guard-staged-ids`,
  `guard-collisions` (S002), `guard-reg-ids-badanchor`, `guard-collisions-badanchor` (empty),
  `guard-indent-4-vs-3.md`, `guard-indent-ids` (S004 only)
- `quarantine-slice` (2 rows, `6db0080e…`, byte-identical to r31/r34/r35)
- `renumber-min` (27), `renumber-full` (175)

VERDICT: collisions-24-guard-ok-slice-2
