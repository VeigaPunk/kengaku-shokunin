# R44CritGateRows — round-44 C2 Gate reject rows and falsifiable flip definitions

Seat: critic (leaf). Pre-empts the round-43 closure §3 discernment disagreement
(`corpus/lessons/round-43-verifier-spotcheck.md` §3: a recorded `Flip check (round 43): task.toml — not fired`
whose verdict was false — the entry cited `task.toml:22` and `solve.sh:90`). This report defines, for the
round-44 C2 package (`plans/pkg-spec-r44.json` rows S138–S146), the captured-not-row files, the sentence
classes that could rest on them alone, the tier call for S144–S146, and the Gate reject rows with flip
conditions the exact check command decides. All paths relative to the lane root unless absolute.

## 1. Captured files that are NOT rows: `feal.c`, `gitignore`

The capture manifest lists 11 files; the frozen spec has 9 rows. Deciding command and output:

```
$ export LC_ALL=C
$ jq -r '.rows[].capture' plans/pkg-spec-r44.json | LC_ALL=C sort > s
$ ls -1 corpus/evidence/round44/tb2-feal-linear-cryptanalysis | grep -v '^SHA256SUMS$' | LC_ALL=C sort > c
$ comm -23 c s
feal.c
gitignore
```

- `feal.c` and `gitignore` ARE pinned: both sit in `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/SHA256SUMS`
  (digests `bbd38d19…` and `9a8dd8d9…`) and in the counter's `CAPTURES` (`plans/round44_c2_verify.py:64,66`).
  They are captured, manifest-listed, digest-pinned — and are **not** spec rows (S138–S146 omit them).
- `SHA256SUMS` is inventory, not content (not a row by nature).

Critical structural fact: `plans/pkg_gate.py` P5 (`c_captures`) requires every quote capture to be
manifest-pinned, and `feal.c`/`gitignore` **are** pinned — so nothing in the gate stops an entry from
quoting a non-row capture. V10 restricts `## Mechanism` rows to four decisive captures (test_outputs.py,
solve.sh, gen.py, decrypt.c); V7's requirement map is instruction.md-only. The only guard against
non-row-sourced sentences is the Gate reject record itself — exactly the layer that failed (as a *verdict
truth* check) in round 43.

## 2. Entry sentences that could later rest on `feal.c` / `gitignore` alone

Prose sentences whose only source would be the non-row capture (none currently exists; the entry is not yet
landed — `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` absent at review time):

`feal.c` (implementation detail of the task's pair-generator executable; the task's *existence/role* facts
are row-backed, the *internals* are not):
| would-be sentence | only source | row-backed alternative |
|---|---|---|
| "set_keys masks each round key to 20 bits before expand (0xFFFFF)" | `feal.c:31-34` | none (decrypt.c:31-34 shares it, but citing feal.c alone stays unbacked) |
| "encrypt is a 4-round Feistel with pre/post XOR mixing (right^=left; left^=right)" | `feal.c:74-89` | 4 rounds: `README.md:25` (S143); the mixing control flow has none |
| "the standalone mode takes `<plaintext_hex>` + four `<key_hex>` argv and prints Plaintext:/Ciphertext: lines" | `feal.c:93-130` | none |
| "keys above 0xFFFFF are refused with exit 1" | `feal.c:114-117` | none |
| "feal.c is compiled at image build" | role fact | `Dockerfile:9` (S141); `gen.py:31,65` (S140); `instruction.md:1` (S139) |

`gitignore` (repo hygiene; no graded relevance):
| would-be sentence | only source |
|---|---|
| "the task repo ships a .gitignore (ignores `.git/`, `__pycache__/`, `dist.tar.gz`)" | `gitignore:2,8,23` |

Rule to enforce: any sentence whose *only* support is `feal.c:<line>` or `gitignore:<line>` violates
QUALITY Q2 (load-bearing claim must rest on ≥1 registry row for its scope) and reproduces the round-43
planted-class error. The flips in §4 make this checkable.

## 3. Tier call for S144 `solve.sh`, S145 `decrypt.c`, S146 `task.toml`

Constraint first: the gate's `c_sources` (`pkg_gate.py:198-199`) requires `cells[3] == rules["row_tier"]`
and the frozen spec's `entry_rules.row_tier` is `"A"` — every spec row **must** register tier A or V6/gate
fail. Tier B is unreachable for these rows this round without breaking the freeze (round-43's tier-B path
existed only for non-spec rows admitted by executed flips: S135–S137). So the operative question is whether
each row can **honestly bear** A within its scoped authority.

| row | verdict | basis | boundary flip (red if it fires) |
|---|---|---|---|
| S144 solve.sh | admit, tier A | source code authoritative for its own scope: the provided oracle (DECISIVE `solve.sh:289,304`); the probe case `oracle-solve-sh` re-observes it | any sentence implying solve.sh participates in grading (it does not: test.sh only runs `pytest … /tests/test_outputs.py`; solve.sh is executed by the probe as a recipe) |
| S145 decrypt.c | admit, tier A | decisive line `decrypt.c:136` (decimal `printf("%lu")`) sets the medium the oracle and the public-key recipe rely on; tool invoked at `solve.sh:289` | any sentence claiming a non-decimal format passes (receipt case `hex-output` = fail) or that decrypt.c is graded |
| S146 task.toml | admit as mined row; tier A only in "official docs" scope | genuine config: `timeout_sec = 1800.0` (`:22`, also `:25`), `allow_internet = true` (`:34`), `cpus = 1`/`memory_mb = 2048` (`:30-31`), `build_timeout_sec = 600.0` (`:28`) | any sentence asserting grader-side timeout enforcement or "the only time bound" exclusivity (round-43 finding-11 error) |

Notes:
- The one honest load-bearing sentence available to S146: "the environment allows network access
  (`allow_internet = true`, task.toml:34), so the public `gen.py`/`test_outputs.py`/`solve.sh` remain
  fetchable although `gen.py` is deleted from the image (`Dockerfile:13-14`)". `README.md:22` corroborates
  the 30-minute figure, so the timeout sentence does not *need* to rest on task.toml alone.
- V9 forces every row id into the entry body — S146 cannot stay silent; it must carry at least one honest
  citation.

## 4. Gate reject rows and the exact deciding commands

Gate rows (round-43 table shape) for the round-44 C2 package:

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `feal.c` @ `2fd12b88` (captured) | **REJECT — captured, not a row** | implementation detail of the pair-generator executable; no graded predicate; flip: an entry sentence outside `## Located quotes` cites `feal.c:<line>` with no S138–S146 co-citation on that line |
| `gitignore` @ `2fd12b88` (captured) | **REJECT — captured, not a row** | repo hygiene file; flip: an entry sentence outside `## Located quotes` cites `gitignore:<line>` with no S138–S146 co-citation |
| `SHA256SUMS` | **REJECT — inventory, not a content row** | pin inventory; flip: an entry sentence cites it (contentless) |

Deciding command (quote-table excluded; a hit line is unbacked when it carries no `S1xx` co-citation):

```
check_flip() { # $1 = file token, $2 = entry path
  body=$(awk '/^## Located quotes/{skip=1;next} /^## /&&skip{skip=0} !skip' "$2")
  if printf '%s\n' "$body" | grep -nE "$1:[0-9]+" | grep -qvE 'S1[0-9]{2}'; then
    echo "Flip check (round 44): $1 — fired"
  else
    echo "Flip check (round 44): $1 — not fired"
  fi
}
check_flip 'feal\.c' corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
check_flip gitignore  corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
```

A recorded `not fired` verdict is **red** unless it matches this command's output (this is the concrete
execution of the claims' wave-item fix — "a `not fired` verdict naming a file is red when the cited entry
carries a `<file>:<line>` citation of it").

Red control built from the round-43 lesson (run now; same command on the round-43 entry):

```
$ E=corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md
$ for f in Dockerfile feal.py solve.sh task.toml; do …
  round43-entry [Dockerfile] body_hits=3 unbacked_lines=3
  round43-entry [feal.py]   body_hits=1 unbacked_lines=1
  round43-entry [solve.sh]   body_hits=3 unbacked_lines=3
  round43-entry [task.toml]  body_hits=7 unbacked_lines=7
```

i.e. the mechanics would have reported **fired** for `task.toml` and `solve.sh`, contradicting the landed
round-43 `not fired` verdict — proving the command decides the disputed class. If a flip fires, the
round-43 admit path is available: admit `feal.c` as a **tier-B mechanism row** (S135–S137 precedent; it
carries no graded predicate), or re-source the sentence to a row. `gitignore` has no such honest use —
re-source or delete the sentence.

## 5. Flip tally (falsifiable, each with its deciding command)

1. **feal.c sentence flip** — `check_flip 'feal\.c' <entry>` → fired iff ≥1 unbacked `feal.c:<line>` in body.
2. **gitignore sentence flip** — `check_flip gitignore <entry>` → fired iff ≥1 unbacked `gitignore:<line>` in body.
3. **solve.sh role flip** — grep body for a sentence naming solve.sh as graded: `grep -nE 'solve\.sh.*(grad|test|pytest)' <entry>` → fired on match.
4. **decrypt.c format flip** — `grep -nE 'decrypt\.c.*(hex|format|pass)' <entry>` → fired on match (receipt `hex-output` = fail).
5. **task.toml timeout-enforcement flip** — `grep -nE 'task\.toml.*(enforce|only|bound|limit)' <entry>` → fired on match.

## 6. Regression watch

- No gate/V-check currently requires quote captures to be spec rows (P5 only requires manifest-pinning) —
  the flips above are the missing guard.
- V10's mechanism table is restricted to four decisive captures; non-row captures can only enter prose/quotes.
- The round-43 Q35 checker (`plans/gate_flip_check.py`) passes on line existence, not verdict truth; §4's
  command is the verdict-truth check the round-44 Gate should record from.

VERDICT: gate-flips-defined-5
