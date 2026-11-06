# ExecC2 — independent re-measurement of R98-C2 (nested-capture provenance binding)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only. Isolated clones under
`/fast/scratch/hyaku/kengaku-r98/ExecC2/` (`git clone --shared`, detached at T `8e37fc65d5649bb37166fdd6b1657445a8cb55b9`
and at BASE `49a1c4f1097db7c923da56d4213cad75772ed1c0`; `TMPDIR` = scratch; no `/tmp` writes >50 MB; no
production edits, commits, or git/jj mutations in the lane). Evidence persisted at
`w1/ExecC2/` (commands, both counter outputs, both verbose gate runs, defect diffs, own check script+output).

Frozen identifiers verified unchanged: gate bytes at BASE and T are both
`11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` (`git show <rev>:plans/anchor_digest_check.py | sha256sum`),
counter sha `77c6ba05…301f03b` at T matches the claims table, and the S326–S333 captures carry the frozen
digests (e.g. `4983c44d…` for `test_outputs.py`). Census (host, read-only):
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok …/corpus/SOURCES.md`, rc 0
(only pre-existing W04 duplicate-URL warnings, e.g. S234/S237/S243 duplicates — the S234/S243 twins are POP members;
the duplication index is untouched by C2). No tool installs were needed (python3 3.14, git, sha256sum all present).

## 1 · Frozen counter: pass at T, fail at BASE (exactly as frozen)

From the clone root (commands in `w1/ExecC2/commands.txt`):

At T:

```
LEGS K1=pass K2=pass K3=pass K4=pass K5=pass K6=pass K7=pass
GATE defects base=86 rev=45
TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0
PREDICATE R98-C2 pass   rc=0
```

At BASE:

```
LEGS K1=pass K2=pass K3=fail K4=fail K5=pass K6=pass K7=pass
GATE defects base=86 rev=86
TARGET pop=39 cleared=0 still=39 unbound=39 rows_changed=0 captures_changed=0 new_old_row_defects=0
PREDICATE R98-C2 fail   rc=1
```

These match the frozen expected lines and the L1 receipts (`c2-tip.txt`, `c2-base.txt`) verbatim.
Gate standalone: `rows=325 tokens=209 defects=45` at T (clone-T), `rows=317 tokens=201 defects=86` at BASE (clone-BASE).
+8 rows and +8 tokens at T: the eight C1 rows S326–S333 (all BIND by=`url-task`, RESOLVED, **zero DEFECTs** — confirms
the claims note that no new row is flagged). K7 (`new_old_row_defects=0`) and K5/K6 (no POP row or capture changed,
`rows_changed=0 captures_changed=0`) both hold.

## 2 · Own check (no round98 counter, no frozen gate): 39/39 on every conjunct

`w1/ExecC2/independent-check.py` (run from scratch, output `independent-check-output.txt`):

- Parsed POP from the frozen counter source (39 rows S181–S323, rounds 52/92–97), each `(token, expected-path)`.
- For each row, computed `sha256(git show T:<expected-path>)` and compared to the 64-hex token on the row's
  SOURCES line at T: **39/39 equal** (0 mismatches) — including the twin cases, S241 = S243 = `045cc716…`,
  and S224 already carrying the same 64-hex. Spot check via shell: `git show T:…/chess-best-move/tests/test_outputs.py | sha256sum`
  → `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` = S201's token.
- Checked the frozen gate's verbose run at T for `BIND <sid> capture=<path> by=provenance-row` per row and
  the absence of any `DEFECT <sid>` for the row: **39/39 BIND by=provenance-row to the expected path,
  0 DEFECTs**.

So the 39-row population binds independently of the counter's own K-legs — the mechanism is genuinely:
`corpus/evidence/PROVENANCE.md` (52 lines, 41 table rows) supplies `prov_sid` entries the frozen gate's
`bind_row` reads first (gate §`evidence_index`/`bind_row`), with no SOURCES row, capture, or gate byte changed.

## 3 · Where the 41 cleared defects come from (86 → 45)

Set difference over full `DEFECT` lines (`comm -13/-23`, files `defects-BASE-sidclass.txt`, `defects-T-sidclass.txt`,
`lines-BASE.txt`, `lines-T.txt`):

- Gate DEFECT (sid+class) sets: BASE 84 unique pairs / 86 raw lines; T 43 unique pairs / 45 raw lines. Rows
  S300/S233/S213 carry two tokens so raw > sid must hold; the only count identity that works is **86 − 45 = 41** lines.
- **New at T (absent at BASE): NONE.** Zero (sid, class) pairs and zero full lines appear at T that were not at BASE.
  This is K7's claim, seen from the gate's own output: no BASE defect class gains a new kind at T, and no new
  row becomes defective (S326–S333 all clean).
- **Gone at T (present at BASE): exactly 41 lines**, which decompose as:
  1. **The 39 POP rows** (`anchor-unbound`, nested-upstream detail), each cleared by its
     `BIND … by=provenance-row` line (39/39, §2). `new_old_row_defects=0` in the counter is consistent: these
     defects vanished without new classes replacing them.
  2. **S230** — was *not* in POP (its single BASE defect was `digest-wrong-capture`, because it was bound
     by row-path to `corpus/evidence/round52/graders/SHA256SUMS`, a manifest, so the token resolved to a
     "capture belonging to another capture"). At T it binds `by=provenance-url` to
     `…/round52/graders/kv-store-grpc/tests/test_outputs.py` with `RESOLVED … bind=provenance-url`, and its
     defect line vanishes. Its token (`115de2e9…`) still exists (shared with S234, a POP row).
  3. **S213's `anchor-unbound` line** — was *(like S230)* outside POP (S213 had already been escorted into
     row scope at BASE via its correction-cell, so its BASE defect pattern was `token-outside-anchor` **plus**
     `anchor-unbound`). At T the `anchor-unbound` line vanishes (BIND by=`provenance-url`,
     `RESOLVED a540714e…`); the independent `token-outside-anchor` defect (`token=be`, cell 5 of 11) is
     byte-identical at BASE and T and remains — it is a *second, separate* token in the row, not the
     64-hex anchor, and the counter's `rows_changed=0` / defect anatomy correctly never claims it cleared.
     (Full-line diff: S213 contributes 1 of the 41, not 2; the `token=be` line survives at both revs.)

**Extra rows beyond the 39 that cleared — the provenance-url spillover.** PROVENANCE.md's 41 lines each carry
both a sid (→ `prov_sid`, the frozen `provenance-row` rule the counter checks) *and* a pinned raw/blob URL
(→ `prov_url`, the gate's fallback rule consulted when no url-task/row-path binding exists). Reading the
gate source (`evidence_index` builds `prov_url`; `bind_row` falls back to it), four rows rebind through it:

| row | BASE binding | T binding | net defect change |
|---|---|---|---|
| S213 | unbound (`anchor-unbound` + separate `token-outside-anchor`) | `provenance-url` → round52 chess-best-move capture | −1 (anchor-unbound), token-outside-anchor persists |
| S230 | `row-path` → `…/graders/SHA256SUMS` (digest-wrong-capture) | `provenance-url` → round52 kv-store-grpc capture | −1 (fully clean) |
| S237 | `row-path` → `round66/sources/kv-store-grpc-test_outputs.py` | `provenance-url` → round52 kv-store-grpc capture | 0 (was clean, still clean — binding repoints, correctly uncounted by K7 since the class set is unchanged) |
| S272 | (no BIND: row observes clean via abbreviations — no anchor token) | `provenance-url` → round52 sqlite-db-truncate capture | 0 (was clean, still clean; now bound) |

That accounts for **39 + 2 = 41** cleared defect lines (S213 and S230), plus S237/S272 whose bindings changed
with zero net defect delta. This is the *"S213-like provenance-url effect"*-only deviation from the
39-row story, and it is benign and unintended-but-harmless: C2's frozen predicate is scoped to the 39
(`rows_changed=0 captures_changed=0 new_old_row_defects=0`), so the spillover is outside the scored
boundary but is real, traceable, and does **not** mask any defect — every (sid, class) pair at T already
existed at BASE. No row becomes *more* broken, and the residual 45 are all byte-identical BASE lines
(e.g. S173 `anchor-unbound row-carries-no-capture-locator`, S233 two-token, S300 three-token defects,
all unchanged between `lines-BASE.txt` and `lines-T.txt`).

## 4 · What was falsified / not observed

- The frozen counter was **not** something the gate could have been tricked by here in the T/BASE direction:
  the counter uses the BASE gate bytes against both trees (gate byte-identical, see above), and the
  standalone gate run at T reproduces the same defect-count delta without the counter.
- S213's residual `token-outside-anchor` was already there at BASE; C2 does not clear it and does not claim
  it (rows_changed=0). This is a pre-existing defect of a different class, unchanged by PROVENANCE.md.
- New rows S326–S333 are absent from DEFECT sets at T (spot: all eight `BIND … by=url-task`, all eight
  `RESOLVED`, rc-consistent), corroborating L10-style orthogonality; C1's claims are not re-verified here.

## Verdict

**R98-C2 claim verified independently: PASS at T, FAIL at BASE, with the 39/39 conjunct proven by an
own check that bypasses both the round98 counter and the frozen gate, and the 41-defect clearance (39 POP +
S213/S230 provenance-url spillover, S237/S272 net-zero rebindings) fully accounted for with zero new
(sid, class) defects and byte-identical surviving defect lines. The one incidental finding to register
for round 99 is the provenance-url spillover (S213/S230/S237/S272): its cause is mechanically explained
(gate `prov_url` fallback on the same PROVENANCE.md lines) and it clears two non-POP defects while
leaving S213's unrelated `token-outside-anchor` untouched. It is not a counter flaw and was not repaired
(features frozen at F are not touched). Files: `.ufo/waves/round-98/w1/ExecC2.md` + `w1/ExecC2/`.

