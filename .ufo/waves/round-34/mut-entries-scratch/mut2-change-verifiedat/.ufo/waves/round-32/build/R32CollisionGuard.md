# R32 Collision Guard — 0-3-space id-collision guard proof (round 32 C1 preflight)

Seat: `L1Kengaku32.R32CollisionGuard` (leaf). Access date for all opens: 2026-10-25.
Scope: frontier-step mechanics (frozen claims §Non-claims: "the collision guard [is] frontier-step
mechanics under §10, not claims"). No production edits: scratch lives in
`/tmp/r32-CollisionGuard/`; this report is the only file written under the lane repo.

## Scratch registry (the staged set containing S002)

`/tmp/r32-CollisionGuard/scratch-registry.md` (65 bytes), containing an **indented** row
(2 leading spaces before the pipe) and a **column-zero** row:

```
  | S002 | indented scratch row
| S003 | column-zero scratch row
```

## Commands run

- (a) column-zero-only: `grep -oE '^\|[[:space:]]*S[0-9]{3,}'`
- (b) 0-3-space: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`

## Outputs (verbatim)

### (a) column-zero-only pattern

```
| S003
```

Exit 0. The indented row `  | S002` is **not** matched: 0 hits on indented rows
→ **0 collisions**.

### (b) 0-3-space pattern

```
  | S002
| S003
```

Exit 0. Of the two matches, exactly one hits an indented row → **1 collision, id S002**.

Both patterns were run twice against the same scratch registry, once through the shell's
builtin grep (pi-uu-grep 0.2.0) and once through the canonical `/usr/bin/grep`
(GNU grep 3.12-modified); outputs were identical.

## Interpretation

- A column-zero-only scanner (a) is blind to a row indented by 1–3 spaces: an accidental or
  duplicate indented row would pass invisible, so an ID collision would go undetected.
- The 0-3-space pattern (b) — the form the production counters already use
  (`plans/adoption_check.py` `ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")`;
  `plans/round32_c1_verify.py` `ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|")`) —
  catches the indented row, so a stray row surfaces instead of silently colliding.
- Collision count = matches on indented rows: (a) 0, (b) 1 (S002). Both acceptance conditions hold.

## Verdict

VERDICT: guard-proven

## Notes

- No tool installs or updates were performed (stock grep only; no channel record needed).
- No production bytes were touched; the staged package (`shokuknow/merge/kengaku/`) was read
  read-only; no counters were run (out of this seat's scope).
