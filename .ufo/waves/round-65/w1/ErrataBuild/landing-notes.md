# ErrataBuild landing notes — R65-C2 (round 65)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (paths below lane-root-based).
This seat edited no lane file; the four artifacts are append texts for the L1.

## Append targets (all base files end in 0x0A; plain append keeps the prefix)

| artifact (seat dir) | target file | sha256 | bytes |
|---|---|---|---|
| `erratum-round64-lesson.md` | `corpus/lessons/round-64.md` | `601f241fc8b0656e80c491bead63040e6a18bb97b987a4094b652f7594580f45` | 743 |
| `scorecard-correction.md` | `SCORECARD.md` | `fbd9a1d25ea8d65d90ad1b7bf47d96029ffacbfe10436c501f858d9fa3e5e051` | 685 |
| `quality-q47.md` | `corpus/QUALITY.md` | `7cee976dde9ea79cca32a40fbefb77852a1ded71e7b4435a3f6563d4b4383c2a` | 700 |
| `kvstore-entry-addendum.md` | `corpus/knowledge/tb2-kv-store-grpc-offline.md` | `c3daed6eeae914996460c09a8466686be5d347b692d344f5e21d191966759ded` | 577 |

Recipe (for the L1, not run by this seat):

```
cat <seat>/erratum-round64-lesson.md            >> corpus/lessons/round-64.md
cat <seat>/scorecard-correction.md              >> SCORECARD.md
cat <seat>/quality-q47.md                       >> corpus/QUALITY.md
cat <seat>/kvstore-entry-addendum.md            >> corpus/knowledge/tb2-kv-store-grpc-offline.md
```

Then the four frozen greps (targets 1 / 1 / >=1 / 1) and `cmp -n <base size>` per file.
Dry-run evidence for this exact recipe: `landing-dryrun.txt`.

## Placement finding — SCORECARD.md

The seat spec asks for `scorecard-correction.md` "after the round-64 section, before the
Planned (round 65) block". That is an insertion at byte 343957 (line 2864, the
`### Planned (round 65)` heading) and it breaks the frozen clause "SCORECARD.md keeps its base
bytes as a byte-prefix" — measured in `landing-dryrun.txt` (insertion control, `cmp` rc 1).
EOF append is the only placement that satisfies the frozen byte-prefix clause; the block heading
`### Round-64 correction (round 65, routed defect 2)` keeps it findable. This seat reports the
conflict instead of applying either placement; the L1 decides.

## Freeze finding — corpus/SOURCES.md

At HEAD `b5032ff8` the three new rows S232/S233/S234 are an insertion at byte 181788 (line 248),
before the trailing `## Paths` footer (`git diff --stat 12a62551..HEAD -- corpus/SOURCES.md`:
3 insertions, 0 deletions). No filed byte is rewritten, but under the strict 12a62551 reading the
base bytes are not a prefix. Under the per-landing reading (base = freeze tip) SOURCES.md is
untouched by the C2 repair and trivially prefix-clean. The four counter targets are unaffected
(`supersedes S230` is already 1 at the freeze, 0 at base). S234 itself validates
(`s234-checks.txt`: `PREDICATE S234-ROW pass`).
