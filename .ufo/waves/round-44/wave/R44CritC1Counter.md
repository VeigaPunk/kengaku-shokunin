# R44CritC1Counter — dishonest-battery falsification of C1's admission rule

Seat: R44CritC1Counter (critic, leaf). Round 44 (hyaku run 9), ONE v2 wave. Target: falsify C1's admission
rule (`plans/round44_c1_verify.py`, frozen) by building dishonest batteries and checking whether any reaches
the `MUTANTS total=5 killed=5 …` shaped lines without a fixture that genuinely demonstrates the advertised
behaviour. Also: is `claims/control-c1-witness-as-battery.txt` the **only cheap route** to the pass?

## Setup (all absolute)

- Lane clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r44/R44CritC1Counter/lane`; `git -C ... rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r44/R44CritC1Counter/lane`; `rev-parse --short HEAD` = `5e3d3aa`. No battery44 exists in the clone (`plans/battery44` absent; 9 `battery*` plans dirs counted).
- Every counter run inside the round-44 envelope (`claims/envelope.sh`); `--work` under my scratch; battery dirs under my scratch.
- All receipts (this report's raw run outputs) live in `.ufo/waves/round-44/wave/R44CritC1Counter/`; all <1 MiB; sha256 listed below.

## Frozen mutants (from `plans/round44_c1_verify.py` MUTANTS, and `plans/round-44-claims.md`)

| id | tool | class | direction | advertised (span) |
|---|---|---|---|---|
| U5 | anchor | digest-short | silence | `anchor_digest_check.py:88` 'any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`)' |
| U6 | anchor | digest-long | silence | same line 88 |
| U7 | anchor | – | rc-mirror | lines 98-99 'A token that resolves to several of the row's captures is not a defect' |
| U9 | anchor | – | rc-mirror | lines 106-107 'lessons are read from the working tree for paths committed at HEAD' |
| U14c | order | – | error | `order_check.py:26-27` 'Exit: 0 order holds · 1 order broken · 2 setup error (... unparseable round number, bad arguments)' |

Kill rule (docstring): attributed kill = (a) fixture's declared expect/defects exactly match the UNMODIFIED
tool's output on it (`wrong==0`), (b) the mutant exhibits the declared direction on that fixture
(`exhibits`), (c) traced re-run reproduces (rc, classes) AND runs a line of the replaced span (leg f),
(d) site record (next line + locals digest / return) differs from a twice-stable reference record (leg g),
(e) no tamper/null/sidechannel, (f) frozen pins unchanged before and after.

## Baseline (positive control): my own honest battery — different shapes from `claims/witness/w_u.py`

Module `/fast/scratch/hyaku/kengaku-r44/R44CritC1Counter/bats/honest/b_honest.py` written from scratch:
5 fixtures with distinct fids, bodies, row ids (S401/S402), evidence dir `corpus/evidence/q9/`, lesson file
`corpus/lessons/l.md`, order repo with `plans/odd-claims.md` + `corpus/evidence/round7/x-probe.txt`
(witness uses r1/round7 names/bodies — no copying: my row ids, capture paths, contents, and provenance
layout differ). Run (receipt `baseline-honest2.txt`, sha256 `b5415ec9e9372cbd7df2f139d83b34b694868698d1514ec4647e5e6ef5149fd5`):

```
ENVELOPE /usr/bin/bwrap … -- python3 …/plans/round44_c1_verify.py --lane …/lane --battery-dir …/bats/honest --work …/w-honest2
ENVELOPE start 20:33:38 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE h5-short-token … observed_rc=1 observed=digest-short ok
…
MUTANT U5 anchor silence killed by=h5-short-token attributed=L522 value=differs hits=1
MUTANT U6 anchor silence killed by=h6-long-token attributed=L522 value=differs hits=1
MUTANT U7 anchor rc-mirror killed by=h7-twin-gone attributed=L539 value=differs hits=1
MUTANT U9 anchor rc-mirror killed by=h9-dirty-lesson attributed=L384 value=differs hits=1
MUTANT U14c order error killed by=o14c-odd-claims attributed=L161 value=differs hits=1
BATTERY fixtures=5 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/4 order=1/1
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:41 exit=0 … unchanged
```

So the shaped lines are reachable by **original, cheap work** (~5 s, one module, five fixtures), not only by
copying the witness. The witness-as-battery control (freeze file) is the canonical cheap route; it is not the
**only** cheap route — but every cheap route found requires fixtures that literally realize the advertised
behaviour. No dishonest shortcut reached the lines (below).

## Dishonest batteries tried (all under envelope, all `--battery-dir`, dev mode)

| # | vector | battery | result | why blocked |
|---|---|---|---|---|
| 1 | declared direction differs from the one witnessed | `bats/lie/b_lie.py` (same honest builds, expect/defects flipped) | `BATTERY fixtures=5 wrong=5`; `killed=0 survived=5`; exit 1 | `wrong` check ties declarations to actual reference output; a lying fixture can never participate in a kill |
| 2 | kill by side effect (build writes outside the fixture) | `bats/side/b_side.py` (write into `d.parent`) | `wrong=1` (fixture ran, rc=2, declared accept); `killed=0`; exit 1 | write landed inside the module root but outside that fixture's `d`; the fixture itself was defective (no repo), so it never demonstrates anything; a write truly outside the root is refused by `Ctx._inside` → build failure |
| 3 | sidechannel token smuggled into module text | `bats/token/b_token.py` (comment contains "fork") | `SIDECHANNEL token/b_token.py tokens=fork`; `sidechannel=1`; `killed=0`; exit 1 | module-level token scan catches it before any run |
| 4 | timing / tree-pressure (4000-file decoy repo) | `bats/timing/b_big.py` (honest five + `big-4000-files`) | still `killed=5`, all `value=differs`, exit 0 — but the five kills come from the honest fixtures; decoy adds no kill (wall 20:34:15→20:34:24) | purely additive work cannot forge a direction; harness timeout 600 s converts stalls into non-hits |
| 5 | boundary argv `{WORK}` tokens | `bats/boundary/b_boundary.py` (`--lane {WORK}` anchor; `--claims {WORK}` order) | both `ok`, `wrong=0`, `killed=0`, exit 1 | `{WORK}` passes path_ok and fences, but the tools then exit 2 on both ref and mutant (missing repo / path outside lane); the order mutant also exits 2 (outside-lane SetupError), so the `error` direction never exhibits |
| 6 | tampering by a sibling fixture at build time | `bats/sib/b_sib.py` (fixture 2 writes `junk.txt` into fixture 1's `d` before fingerprinting) | build OK; `tampered=0` (fingerprint is taken after all builds); `killed=0`; exit 1 | intra-module sibling writes are possible pre-fingerprint but land before any measurement; fixture `d` is read-only during tool runs (`--ro-bind / /`, writable only work/tmp), so no run-time tamper exists; no kill fabricated |
| 7 | argv resolving outside the fixture | `bats/esc/b_escape.py` (`--lane /etc`) | `SETUP fixture 'escape-argv-etc' … breaks the contract`; exit 2 | `path_ok` refuses tokens that do not resolve inside `d` |

Every one of the seven runs is captured verbatim in the wave subdir (sha256):

```
dishonest-lie.txt       6f977861ce3197b7827d45be003e5e1cf3f5e07fee02cd9bb7b71b708db678c7
dishonest-side.txt      c9a8328a5759c7e05d0468b4a77f06fe551a3b4880101b88f46d2ecd654870ca
dishonest-token.txt     c45d20de887b77c9ba4bfb8dab24bebabae1dd199349ef6cb3df760102022409
dishonest-timing.txt    69d2624835cc5726ac241bb9197d2686f4f47b103dddefa392c73f25ada986f5
dishonest-boundary.txt  0544dc80067af15b22783bc8717a56551d4b198296285926367baedf001356dd
probe-sibling-tamper2.txt 2e74d645646ab19d14a61eb0798656c79affffba9ba794cf49a6213272e8ea8d
probe-argv-escape.txt   2887b2dc064d8afddee98f147fccee36eae8e0331c84546e939be14d363991c0
control-do-nothing-local.txt 5bba455a4eee7456a29b288bc5fd2d41dc70c959049d7efa8b8438e44095e4ab
```

Local do-nothing control (no battery): `BATTERY fixtures=0`, `MUTANTS total=5 killed=0 survived=5`,
`PREDICATE C1 n/a`, exit 1 — matches freeze `control-c1-nothing.txt`.

## Why the admission rule resisted all seven vectors (structure)

For a kill, the exhibit predicate and attribution legs force the genuine demonstration:

- `exhibits` demands a fixture whose **reference output already matches its declaration** (`wrong==0` is
  global), and on which the mutant measurably changes the declared dimension: for U5/U6 the class
  `digest-short`/`digest-long` must disappear (it only exists via `anchor_digest_check.py:88`, so the
  fixture must contain a <64 / >64-hex anchor token); for U7 the mutant claims the first of several
  resolving captures, so a kill requires a row whose token actually resolves to two captures sharing a
  digest (the twin-capture scenario the advertised sentence names); for U9 the mutant reads HEAD while the
  reference reads the working tree, so a kill requires a HEAD-vs-worktree erratum divergence; for U14c the
  mutant deletes the claims-name guard, so a kill requires an unparseable claims name (any other setup
  error exits 2 on both). None of the seven dishonest batteries could produce the rc/class delta without
  first creating the genuine condition — and when they did create it, the fixture was by definition
  demonstrating.
- Leg f (span runs) + leg g (site record differs from a twice-stable reference) tie the kill to the exact
  replaced lines; they cannot be fabricated by decoys, extra files, timing, `{WORK}` argv tokens, or sibling
  writes. The `value=differs` line is only printed after all three legs pass.

## Answer to the question

1. No dishonest battery reached `killed=5`-shaped lines: all seven vectors blocked. The only runners that
   printed `MUTANTS total=5 killed=5 …` are the two batteries whose fixtures genuinely demonstrate all five
   advertised behaviours (my original `bats/honest`, and the freeze's witness copy as battery44).
2. The witness-as-battery control is not the *only* cheap route to the pass — an independent, differently-
   shaped original battery passes equally cheaply — but it is the canonical cheap route, and no *dishonest*
   shortcut exists: the cheapest passing battery is one whose fixtures genuinely realize the advertised
   behaviours (5 fixtures, ~5 s). The freeze's "reachable by witnessed work" wording holds; the admission
   rule itself was not falsified.

Kill/attribution counters per run are none of my own report's lines: the counter prints them (quoted
above); every number above carries the command + output file that produced it.

VERDICT: dishonest-battery-vectors-7/7
