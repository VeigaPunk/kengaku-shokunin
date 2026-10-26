Registry row for `SKILL.md` §Gate/probe registry (append after the `round42-c2` / `fibsqrt-probe` block;
the table has eight columns: name | kind | entry | verdict map | self-test | pinned values | write scope |
owner). Drafted by wave-1 seat `R43FlipCheck`, not landed: the L1 integrates.

| `gate-flip-check` | gate | `python3 plans/gate_flip_check.py --lesson <path>` (one lesson file; no lane needed, no git) | `0` every conditional Gate refusal is resolved by a later `Flip check (round N): <item> — fired\|not fired — <evidence>` line · `1` `FLIPS total=<n> unresolved=<u>` with `u>0` (one `FLIP line=<n> flip_line=<n> item=… shapes=… resolution=…` line per obligation, plus `FLIP-DETAIL … refused_rows=<n> malformed_resolutions=<n>`) · `2` setup/usage (`SETUP no '## Gate' section`, unreadable lesson, argparse) | `python3 plans/gate_flip_check.py --selftest` (19 built fixtures in a temp dir, each run as a subprocess: 10 red, 8 green, 1 setup; `SELFTEST ok=19/19`) | none in the script; the lesson it reads is the input. Red control: `--lesson corpus/lessons/round-42.md` → `FLIPS total=2 unresolved=2`, exit 1 (the `Dockerfile` and `README.md` rows); green control: a scratch copy with the two resolution lines appended → `FLIPS total=2 unresolved=0`, exit 0 | none — reads the named lesson, writes nothing; `--selftest` writes only its own `mkdtemp` tree | kengaku |

Addendum to add under the table, in the style of the round-36/37/40 entries:

Round-43 registry addendum: `gate-flip-check` is the first row whose input is a **lesson** rather than a
package, a capture or a receipt: it reads one `## Gate` section, keeps the refusals that state a flip
condition (`Flip:`, `flips when`, `if … admit`, or a companion bullet naming a refused candidate), and
requires each to be resolved by a later line of the same file. It is red on the landing tip by
construction — 45 obligations in 18 lessons, none resolved (`.ufo/waves/round-43/build/R43FlipCheck/sweep.txt`)
— so wire it as a forward gate from round 43, never as a claim that the corpus is clean. Its verdict is a
recorded sentence, not an executed consequence: a `fired` line with the wrong evidence passes, which is
the limit the criterion (draft `QUALITY-Q35`) names. First instance closed by the tool: round-42 D3
(`corpus/lessons/round-42.md:44`, `corpus/lessons/round-42-verifier-spotcheck.md:37-42`).
