# R35IdGuard — round 35 wave 1, build (executor)

Seat: R35IdGuard. Assignment: addendum §10 id-collision check at
`A=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/assimilation` (created),
plus the §10 quarantine-slice derivation. Host `linux 7.2.11-arch1-1`; lane HEAD
`11d64530179b78e33ba6074fc77d63d36ee7ac31` (= the freeze commit). No tools installed/upgraded
(grep/sort/comm/awk/git read-only as coreutils, all preinstalled).

## 1. Real run — id-collision check (freeze registry vs staged package)

Registry input = committed blob at freeze HEAD (`git show HEAD:corpus/SOURCES.md`), so the check is
reproducible even while the worktree moves. Contract anchor `ANCH='^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
(0–3-space pattern):

```bash
$ ANCH='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
$ git show HEAD:corpus/SOURCES.md | grep -oE "$ANCH" | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > $A/reg-ids
$ grep -oE "$ANCH" /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md \
    | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > $A/staged-ids
$ LC_ALL=C comm -12 $A/reg-ids $A/staged-ids > $A/collisions
$ wc -l $A/reg-ids $A/staged-ids $A/collisions
  97 …/reg-ids
 175 …/staged-ids
  21 …/collisions
 293 total
$ sed -n '1p;$p' $A/reg-ids      # S001 … S104
$ sed -n '1p;$p' $A/staged-ids   # S077 … S251
$ cat $A/collisions
S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S093 S094 S097 S100 S101 S102 S103 S104
$ sha256sum $A/reg-ids $A/staged-ids $A/collisions
19fbc1993eddf356ae663f50c2b41ccbfac7b393d1f9b5f4cbda922c9a394d7b  reg-ids
2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c  staged-ids   # identical to round-33 staged-ids digest
25415253cbf9dc02876c6e2dec3be2cf3d788ac0e0630560062cb6cd0d20bfbc  collisions
```

- **reg-ids = 97** (S001–S104), **staged-ids = 175** (S077–S251), **collisions = 21**:
  S077–S086, S090–S094, S097, S100–S104. Every staged id is a collision with the lane's registry
  (the staged package continues the lane's S-space, so this is expected pre-renumber state; the
  adopted rows must be renumbered to unused ids per the §10 contract).
- Cross-check: `staged-ids` sha256 is byte-identical to the round-33 staged-ids receipt
  (`2df53989…`), i.e. the merge package is unchanged since round 33; the collision set grew by
  S103/S104 vs round-33's 19 only because the lane admitted S103/S104 in round 33.

## 2. Guard proof — the 0–3-space pattern is load-bearing

Fixture under `$A/guard-proof/`:
`guard-registry.md` carries an indented `  | S002 |` row plus a column-zero `| S900 |` row;
`guard-staged.md` carries `| S002 |` and `| S901 |`.

```bash
$ grep -oE "$ANCH" guard-registry.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > guard-reg-ids    # S002 S900
$ grep -oE "$ANCH" guard-staged.md  | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > guard-staged-ids # S002 S901
$ LC_ALL=C comm -12 guard-reg-ids guard-staged-ids > guard-collisions
$ cat guard-collisions; wc -l guard-collisions
S002
1
$ BAD='^[|][[:space:]]*S[0-9]{3,}'      # discriminator control: column-zero-only anchor
$ grep -oE "$BAD" guard-registry.md | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > guard-reg-ids-badanchor
$ LC_ALL=C comm -12 guard-reg-ids-badanchor guard-staged-ids | wc -l
0
```

The contract anchor sees the indented `S002` row → nonempty collisions (1). The column-zero-only
control on the **same fixture** sees only `S900` → 0 collisions, proving the 0–3-space allowance is
what makes the guard fire. **guard = ok.**

## 3. Quarantine slice — §10 awk over the absent-defect register

Re-derived from the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
with the §10 awk (lane column is field 2 in that 7-column table; id field 4, class field 5):

```bash
$ awk -F'|' '$2 ~ /kengaku/ && $4 ~ /^[[:space:]]*S[0-9]{3,}[[:space:]]*$/ \
    {gsub(/[[:space:]]/,"",$4); gsub(/[[:space:]]/,"",$5); print " "$4"   "$5" "}' \
    absent-defect-register.md > $A/quarantine-slice
$ cat $A/quarantine-slice
 S091   `payload-absent`
 S105   `payload-absent`
$ wc -l $A/quarantine-slice
2
$ cmp $A/quarantine-slice .ufo/waves/round-34/assimilation/quarantine-slice && echo byte-identical
$ cmp $A/quarantine-slice .ufo/waves/round-31/assimilation/quarantine-slice && echo byte-identical
$ sha256sum $A/quarantine-slice
6db0080e92291a9c686563174ba3ca512976828d36d311a54a77024034ad6a0e
```

**slice = 2** rows — `S091` and `S105`, both `payload-absent` — byte-identical to the round-31 and
round-34 saved slices. Dispositions (same as prior rounds): both stay unadopted; neither is cited by
the C1/C2 admitted entry sets; flip = a round that fetches the payload and locates a quote.

## 4. Worktree divergence disclosure

`corpus/SOURCES.md` carries an uncommitted modification from another seat's in-flight C1 append
(`git status --porcelain` → ` M corpus/SOURCES.md`). Worktree reg-ids = 100 (S001–S107),
worktree collisions = 24 = the HEAD 21 + S105/S106/S107. The freeze-state numbers above (97/175/21)
are the reproducible baseline at the freeze commit; the worktree divergence is recorded, not folded in.

## Evidence inventory (all under `.ufo/waves/round-35/assimilation/`)

- `reg-ids` (97), `staged-ids` (175), `collisions` (21) — §1
- `reg-ids-worktree` (100), `collisions-worktree` (24) — §4
- `guard-proof/guard-registry.md`, `guard-proof/guard-staged.md`, `guard-proof/guard-reg-ids`,
  `guard-proof/guard-staged-ids`, `guard-proof/guard-collisions` (S002), `guard-proof/guard-reg-ids-badanchor`,
  `guard-proof/guard-collisions-badanchor` (empty) — §2
- `quarantine-slice` (2 rows) — §3

VERDICT: collisions-21-guard-ok-slice-2
