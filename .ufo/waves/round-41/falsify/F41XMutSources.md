# F41XMutSources — near-variant mutation probe of `plans/sources_adopt.py` (round 41, wave 2, falsify)

Seat: F41XMutSources (mutation-tester, leaf). Date: 2026-10-26.
Target: the `sources_adopt.py` CLI half — `main()`, the exit-code returns of `check()`/`quote_check()`,
`--attest-opened`, `--scope-to-admit`, `--out` writing, and the EXIT_QUOTE_TOO_LONG/ABSENT/URL_MISMATCH
precedence — probed with 20 near-variants, none of which is a frozen `(old,new)` pair of
`plans/round41_c1_verify.py` (frozen sources mutants: S01–S09, S11), run through a counter copy in
scratch against the landed battery `plans/battery41/` (7 modules, 48 fixtures).

## Method

- Scratch `/fast/scratch/hyaku/kengaku-r41/F41XMutSources` (NVMe; `export TMPDIR="$S"`). Lane clone:
  `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
  `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r41/F41XMutSources/lane`
  (verified before any write; no commit ever made there).
- Clone tip `d7c77895752a2a5f317fa22f2362416ada50a04b` = the wave-2 dispatch commit; its only diff vs the
  goal tip `3d0058fbde48…` is `.ufo/waves/round-41/{falsify-dispatch.json,falsify-spec.json}` (+917 lines,
  no C1 surface touched); `git merge-base --is-ancestor 3d0058fbde… HEAD` → true.
- Pinned surfaces byte-verified at clone time and re-hashed after the run — all equal to
  `.ufo/waves/round-41/claims/frozen-digests.txt`: `sources_adopt.py 38492bf1…`,
  `round41_c1_verify.py 8835a94b…`, `tip_receipts.py e4f49714…`. Nothing frozen changed.
- Counter copy `$S/counter_near.py` = the frozen counter with my 20 near-variant tuples appended to
  `MUTANTS` (frozen entries untouched; run in development mode `--only S07,X01…X20`, so the counter prints
  `PREDICATE C1 n/a`), sha256 `34a3649d6a49e62c4e8e30450ae8b76e18f18ca1895320e77b2a3612442b7e8b`. Before the
  run: every `old` string verified `count==1` in the pristine tool and every mutant variant `py_compile`d.
- Envelope (host-safety rule, verbatim) for the counter run and both probe drivers:
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
  --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 "$S/counter_near.py" --lane "$S/lane"
  --work "$S/counter-work" --only S07,X01,…,X20 --jobs 8`
  (the counter adds its own read-only sandboxes inside it; nesting worked). No writes outside scratch and
  the report dir; no tool installs (nothing to record).

## Calibration — is the copy faithful?

`--only S07` (a frozen mutant) → `MUTANT S07 sources 3>0 killed by=s_exit-collision-admit` — byte-identical
to the frozen counter's line in `.ufo/waves/round-41/integrate/measure-final.txt`. The copy's bookkeeping
equals the landing measurement: `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `null_detected=0`,
`PINS-AFTER mismatched=0`. Receipt: `F41XMutSources/near-run.txt`.

## Results — 20 near-variants: 9 killed, 11 survived

Command: the bwrap line above. Full output: `F41XMutSources/near-run.txt`. Summary lines:
`MUTANTS total=21 killed=10 survived=11 invalid=0 null_detected=0` (21 = 20 near-variants + frozen S07
calibration; killed=10 includes S07), `ADVERTISED direct=15 indirect=4 none=2`.

| id | site (plans/sources_adopt.py) | mutation | dir | verdict |
|---|---|---|---|---|
| X01 | `quote_check` overlong return | `if overlong:` → `if False:` | 6>0 | SURVIVED |
| X02 | `quote_check` absent return | `if absent:` → `if False:` | 7>0 | SURVIVED |
| X03 | `quote_check` mismatch return | `if mismatch:` → `if False:` | 8>0 | SURVIVED |
| X04 | `quote_check` unmapped return | `if unmapped:` → `if False:` | 9>0 | SURVIVED |
| X05 | overlong/absent returns swapped | block swap | 6>7 | SURVIVED |
| X06 | mismatch/unmapped returns swapped | block swap | 8>9 | SURVIVED |
| X07 | cap boundary | `if count > cap:` → `>=` | 0>6 | SURVIVED |
| X08 | `build_block` not-mined refusal | `if cells[7] != "mined":` → `if False:` | 5>0 | killed by=s_exit-queued-admit |
| X09 | `--attest-opened` bypass removed | `if not attest_opened:` → `if True:` | 0>5 | killed by=s_exit-attest-opened |
| X10 | `--attest-opened` ignored | `if not attest_opened:` → `if False:` | 5>0 | killed by=s_exit-opened-elsewhere |
| X11 | `--scope-to-admit` ignored | `if want_ids and scope:` → `if False:` | 2>4 | killed by=s_usage-06-recheck-prose-scoped-row |
| X12 | scoped prose not stripped | list-comp → `row_id: found` | 2>4 | killed by=s_usage-06-recheck-prose-scoped-row |
| X13 | `--recheck` default emptied | `default="180d",` → `default="",` | 0>2 | killed by=s_exit-attest-opened |
| X14 | `build_block` duplicate-request | return list → `[]` | 5>0 | SURVIVED |
| X15 | `check()` malformed exit dropped | `else EXIT_MALFORMED` → `else EXIT_OK` | 4>5 | SURVIVED |
| X16 | `check()` missing returns wrong code | `EXIT_REQUEST` → `EXIT_MALFORMED` | 5>4 | killed by=s_exit-absent-id |
| X17 | `check()` missing branch dropped | `if missing:` → `if False:` | 5>0 | SURVIVED (rc-equivalent) |
| X18 | `check()` clash return dropped | `if clash:` → `if False:` | 3>0 | killed by=s_exit-collision-admit |
| X19 | main() map-problem return code | `EXIT_QUOTE_UNREADABLE` → `EXIT_URL_UNMAPPED` | 2>9 | killed by=s_modes-s09-url-map-nested-shape |
| X20 | `--out` write dropped | `if args.out:` → `if False:` | 0>1 | SURVIVED (rc-invisible) |

## Survivors are live, not dead mutations

Hand fixtures per survivor, reference vs mutant run directly (driver `$S/liveness.py` inside the same bwrap
envelope; receipt `F41XMutSources/liveness.txt`):

```
LIVE X01 ref_rc=6 mut_rc=0   LIVE X05 ref_rc=6 mut_rc=7   LIVE X14 ref_rc=5 mut_rc=0
LIVE X02 ref_rc=7 mut_rc=0   LIVE X06 ref_rc=8 mut_rc=9   LIVE X15 ref_rc=4 mut_rc=5
LIVE X03 ref_rc=8 mut_rc=0   LIVE X07 ref_rc=0 mut_rc=6   LIVE X17 ref_rc=5 mut_rc=5
LIVE X04 ref_rc=9 mut_rc=0   LIVE X20 ref_rc=0 mut_rc=0 ref_out=True mut_out=False
```

X20 detail: the reference writes `out.md` (`out_head='| S131 | https://cited.i…'`) and prints no block; the
mutant writes nothing and prints the block to stdout (`ref_printed_block=False mut_printed_block=True`).

## What holds

The landed battery pins the admit-path refusals from both sides, and the counter's exact-pair directions
catch one-byte neighbours at every site it touches: not-mined (X08), `--attest-opened` in both directions
(X09 removed / X10 ignored), `--scope-to-admit` in both directions (X11 flag ignored → 2>4, X12 prose kept
→ 2>4, both killed by the same scoped fixture), the `--recheck` default (X13), `check()`'s own collision
return (X18, S07's neighbour at a different site), `check()`'s missing-id return *code* (X16, 5>4), and the
map-problem return code with the print kept (X19, S09's neighbour). Nine of twenty near-variants killed;
zero invalid, zero null detections, zero tamper, zero sidechannel.

## What breaks — coverage findings, one advertised sentence per survivor

1. **The quote-verdict half of the CLI is demonstrated by no battery fixture (X01–X04, X07).** All 8
   `s_modes` fixtures stop at a mode guard (exit 2) before `quote_check` judges a span; no fixture ever
   reaches exits 6/7/8/9. Advertised: `SKILL.md:573` "`6` quote over the 25-word cap · `7` quote absent
   from artifact bytes · `8` quote bound to a mismatched URL · `9` quote has no url-map entry". The tool's
   own `--selftest` catches these four (selftest-matrix.txt: X01/X02/X03/X04/X07 rc=1), so the protection
   exists — but only in the tool, which the C1 predicate never runs.
2. **The refusal ORDER is protected by nothing executable (X05, X06).** Swapping 6↔7 and 8↔9 passes all 48
   battery fixtures *and* the tool's 17-case selftest (`SELFTEST-CHK X05 rc=0`, `X06 rc=0`). Advertised
   only by prose: `plans/sources_adopt.py:455-456` "The first refusal in the order 2, 4, 6, 7, 8, 9 wins".
   No battery or selftest case carries two refusals of different classes in one run.
3. **`build_block`'s duplicate-request refusal (X14)** — no fixture passes a duplicated `--admit-ids` that
   reaches `build_block` (`s_usage-03-single-digit-month-duplicate-request` exits at the access-date guard
   first); selftest has no duplicate-request case (rc=0). No SKILL sentence names it (adv none); nearest is
   `SKILL.md:573` "`5` requested id absent".
4. **Exit 4 is never triggered by the battery (X15).** Every staged row in battery41 is an 11-cell clean
   row, so the advertised `SKILL.md:573` "`4` malformed staged row (escaped pipe, column count, quote
   spans)" is undemonstrated at battery level; the mutant falls through to the missing-id refusal (ref 4 →
   mut 5). The selftest catches it (rc=1, 3 failed cases).
5. **S10's rc-equivalence independently reproduced (X17).** Dropping `check()`'s missing branch entirely
   leaves all 22 sources fixtures rc-identical (`exhibits=none`); through `main()` the refusal still exits 5
   (liveness ref_rc=5 mut_rc=5) — matching the pre-freeze withdrawal, `plans/round-41-claims.md:39-40`
   "`S10` … withdrawn before freeze as rc-equivalent: `claims/s10_equivalence.txt` `ref_rc=5 mut_rc=5`".
   Not a defect: `SKILL.md:573` "`5` requested id absent" stays enforced at CLI level; the branch itself is
   nonetheless only selftest-demonstrated (selftest rc=1).
6. **`--out` is structurally invisible to the counter (X20).** The counter observes exit codes and (receipts
   tool only) stdout classes; the sources class set is always empty, so the gate's only file-writing surface
   — `SKILL.md:573` write scope "writes only under `--out`", `--out` help `plans/sources_adopt.py:986`
   "write the append block here" — has no battery demonstration. A mutant that silently drops the write and
   prints the block to stdout passes all 48 fixtures and the selftest (rc=0).

## Counter-limit vectors (the goal's key question for battery reviewers)

None of my mutants or drivers uses the known counter limits (A1′/F1 stub-steering, dead-site credit,
F4/A3 relative-argv escape, F2/F3 AF_UNIX/SysV IPC, A8 source-text-only scan): every mutant is a plain byte
edit of the pinned tool run through the counter's own sandboxing, and every survivor was re-confirmed live
by direct reference/mutant runs outside the counter. The survivors above are battery/selftest coverage gaps,
not counter-limit artifacts. No battery41 module attempted any of those vectors against my runs
(`sidechannel=0`, `tampered=0`, `null_detected=0`).

## Bounds

- Writes: only `$S` (scratch) and `.ufo/waves/round-41/falsify/F41XMutSources{.md,/}`. No lane file touched
  (the three pinned digests re-hashed identical after the run; no git/jj mutation anywhere). No writes
  outside the report dir and scratch — the timestamp rule never fired. No installs. No subagents, no
  background jobs, no `task`.
- The fixture rule's per-call `trap 'rm -rf -- "$S"' EXIT` was not set on intermediate calls because the
  clone and counter copy must persist across this seat's calls; the guarded deletion (`case "$T" in "$S"|"$S"/*)`)
  was performed explicitly after the receipts were copied out.
- Receipts filed: `F41XMutSources/near-run.txt` (counter output), `F41XMutSources/liveness.txt`,
  `F41XMutSources/selftest-matrix.txt`.

VERDICT: near-variants-killed-9/20
