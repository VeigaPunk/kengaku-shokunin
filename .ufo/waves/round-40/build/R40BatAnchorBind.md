# R40BatAnchorBind — battery40 module `a_bind` (anchor: A15, A17, A27)

Seat: executor, round-40 wave 1, item `R40BatAnchorBind`. Leaf; no subagents, no background jobs.
Wrote exactly one lane-visible artefact plus its receipts, all under `.ufo/waves/round-40/build/R40BatAnchorBind/`:

| file | role |
|---|---|
| `battery/a_bind.py` | battery40 module (3 fixtures, stdlib only, fids prefixed `a_bind-`) |
| `targeted.txt` | `--only A15,A17,A27` receipt (this module only) |
| `loadbearing.txt` | one-fixture-removed table receipt |
| `full.txt` | full default counter receipt (module copied into a scratch clone's `plans/battery40/`) |
| `sha256.txt` | module digest |

`sha256 battery/a_bind.py` = `844e200425226af66941fed0d042ec7bd57b8c1dc90d95ab0c7fc9b40737540e`
(stable across the targeted run, the full run and the three load-bearing runs; identical bytes in the scratch clone).

## Axes

- **Calibration** — three advertised sentences of `plans/anchor_digest_check.py` (`:55` ambiguous slug binds nothing,
  `:74` `--evidence-ref index` reads index blobs, `:96-98` a named capture with no token is `capture-unanchored`) now
  have a committed-fixture kill in their declared direction. +3 mutants reachable.
- **Operability** — each fixture is one small construction on a `--shared` clone of lane HEAD, ~1 s; the full
  21-mutant counter ran in 8.5 s wall. No fixture leaves a process, a hook or a path outside its own directory.
- **Harm** — in the full run no other mutant exhibits anything on these fixtures (`exhibits=none` for all 18
  survivors), so the module adds three kills and disturbs nothing else.

## Fixtures

Reference facts used by the module (measured on a clean clone of lane HEAD `3077adb`):
`python3 plans/anchor_digest_check.py --lane "$S/lane"` → `rows=111 tokens=19 defects=0`, rc=0. So a fixture's
declared defect set is exactly the defects it creates.

| fid | behaviour demonstrated | mutant | construction |
|---|---|---|---|
| `a_bind-a27-token-per-capture` | S111 keeps its own pinned URL and gains a second one (`regex-log/tests/test_outputs.py`) while its anchor token becomes S108's digest — the git-webserver capture is named and unclaimed, so the row is `capture-unanchored` (ref rc=1). The mutant drops the class (rc=0). | A27 `silence` | token substitution `sha256 S111 -> sha256 S108` in the S111 row + second URL appended to the row's source cell (cell index 2) |
| `a_bind-a15-slug-ambiguity` | two committed `task.toml` files claim one task slug (`harbor/amb-bind-task`, dirs `roundX/tb2-amb-a` and `roundX/tb2-amb-b`); the row's token is `roundX/tb2-amb-a`'s digest, so the ambiguity binds nothing and the token is `anchor-unbound` (ref rc=1). The mutant keeps `owners[0]` (the `amb-a` dir) and resolves the token (rc=0). | A15 `rc-silence` | new row S902 + two committed evidence dirs |
| `a_bind-a17-index-bytes` | one capture committed with body A (digest A), then rewritten and **staged** with body B (digest B, `SHA256SUMS` rewritten and staged); row S903 claims digest B and the tool is read in `--evidence-ref index`. Reference reads index blobs and accepts (rc=0); the mode-swapped mutant reads `HEAD:` blobs, finds neither B in the row's scope nor in the committed set, prints `digest-unknown` and exits 1. | A17 `rc-mirror` | committed capture → rewrite + `git add` (no commit) → row anchored to B |

Design notes.

- A17's fixture deliberately keeps **every** indexed path present at HEAD. A staged *new* file would make the
  mode-swapped mutant die in `blobs()` (`cat-file: <spec> is not a blob`, `Usage`) and exit 2 — the `rc-error`
  direction, not A17's declared `rc-mirror`. The staged-rewrite shape is what yields the declared rc 1.
- A15's fixture uses a slug no other row mentions, so the mutant's behaviour change is confined to the new row;
  `owners` is `sorted()`, so the alphabetically first dir is the bound one and carries the row's token.
- A27's fixture restates the round-40 witness shape (`claims/witness/w_anchor.py` `w-a27-second-url`) in this
  module's own code; the witness module is a development battery and is not part of `plans/battery40`, so the kill
  now has a committed home. Rows touched: S111 only.

## Evidence

Targeted run (`python3 plans/round40_c1_verify.py --lane "$S/lane" --battery-dir …/battery --only A15,A17,A27 --work "$S/w"`),
`targeted.txt`, rc=0:

```
PINS total=3 mismatched=0
FIXTURE a_bind-a27-token-per-capture tool=anchor expect=reject declared=capture-unanchored observed_rc=1 observed=capture-unanchored ok
FIXTURE a_bind-a15-slug-ambiguity tool=anchor expect=reject declared=anchor-unbound observed_rc=1 observed=anchor-unbound ok
FIXTURE a_bind-a17-index-bytes tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT A15 anchor rc-silence killed by=a_bind-a15-slug-ambiguity -- plans/anchor_digest_check.py:55 'is matched **exactly** against the `name = "<org>/<task>"
MUTANT A17 anchor rc-mirror killed by=a_bind-a17-index-bytes -- plans/anchor_digest_check.py:74 '`--evidence-ref index` reads the index blobs (`git cat-fi
MUTANT A27 anchor silence killed by=a_bind-a27-token-per-capture -- plans/anchor_digest_check.py:96-98 'A capture none of the row's anchor tokens resolves is
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Load-bearing table (`loadbearing.txt`; each run drops exactly one fixture, order A27, A15, A17):

| fixture dropped | A15 | A17 | A27 | BATTERY / MUTANTS |
|---|---|---|---|---|
| `a_bind-a27-token-per-capture` | killed | killed | **SURVIVED** | `fixtures=2 wrong=0 tampered=0 sidechannel=0` / `killed=2 survived=1` |
| `a_bind-a15-slug-ambiguity` | **SURVIVED** | killed | killed | `fixtures=2 wrong=0 tampered=0 sidechannel=0` / `killed=2 survived=1` |
| `a_bind-a17-index-bytes` | killed | **SURVIVED** | killed | `fixtures=2 wrong=0 tampered=0 sidechannel=0` / `killed=2 survived=1` |

One-to-one: each of the three kills depends on exactly its own fixture, and no fixture's removal costs another
fixture's kill. All three runs kept `wrong=0 tampered=0 sidechannel=0`, `invalid=0 null_detected=0`.

Full default counter (`plans/battery40/` in the scratch clone holds only `a_bind.py`; `--lane "$S/lane" --work "$S/w2"`),
`full.txt`, rc=1 (expected — 18 mutants belong to other wave-1 modules):

```
PINS total=3 mismatched=0
MUTANT A15 anchor rc-silence killed by=a_bind-a15-slug-ambiguity -- plans/anchor_digest_check.py:55 'is matched **exactly** against the `name = "<org>/<task>"
MUTANT A17 anchor rc-mirror killed by=a_bind-a17-index-bytes -- plans/anchor_digest_check.py:74 '`--evidence-ref index` reads the index blobs (`git cat-fi
MUTANT A27 anchor silence killed by=a_bind-a27-token-per-capture -- plans/anchor_digest_check.py:96-98 'A capture none of the row's anchor tokens resolves is
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=3 survived=18 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

The other 18 lines are `SURVIVED exhibits=none` for A01, A02, A03, A06, A08, A09, A21, A22, L01, L05, L06, L11,
L14, L15, L21, O04, O12, O14 — no `exhibits=` other than `none`, i.e. my fixtures exhibit no direction any of them
declares. The predicate can only pass once every wave-1 module lands.

## Risks and limits

- **Tip coupling.** The fixtures clone lane HEAD, so their reference results are declared at the landing tip. The
  two A15/A17 rows (S902, S903) and the two `roundX/` capture dirs are created inside the fixture clone only; if a
  future round adds a real row with SID S902/S903 or a dir `corpus/evidence/roundX/`, the row insert and the slug set
  change and the declared sets must be re-measured. S902/S903 are the only ids assumed free (HEAD holds S001–S111;
  measured `rows=111`).
- **A27 restates the witness.** Same construction as the pre-freeze witness, independently coded. If a later change
  makes `regex-log` a row of its own with the same URL, S111's second locator would still be the same capture, so the
  shape is stable; a change to S111's own digest would need the token rewritten to the *other* capture's digest.
- **A15 depends on sort order.** `owners` is `sorted()`; the row token is `roundX/tb2-amb-a`'s digest. Renaming or
  adding a third dir whose path sorts before `tb2-amb-a` would make the mutant bind a different capture and stop
  exhibiting rc-silence — the fixture names its two dirs, so only an edit to the module can break this.
- **The kill is a result difference in the declared direction, not intent proof** (frozen limit). `null_detected=0`
  shows each fixture's reference result is reproducible; the module carries no side-channel token (`sidechannel=0`)
  and no fixture writes outside its own directory.
- No lane file was written or staged: the module and receipts live only under `.ufo/waves/round-40/build/`. The full
  run used the module copied into the scratch clone at `$S/lane/plans/battery40/a_bind.py` (same sha256).
- Tooling: nothing installed or upgraded (no pacman, no `uv`, no `npx`). Scratch `S=/fast/scratch/hyaku/kengaku-r40/R40BatAnchorBind`
  removed after the receipts were copied out.

VERDICT: battery40-a_bind-killed-3/3-wrong-0
