# R44BatU6b — battery44 module `u6_long_b`: an attributed kill of frozen mutant U6 (`digest-long`)

Seat R44BatU6b (executor, kengaku round 44, build+attack v2 wave). Lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read only; nothing in it written). All measurements ran
inside the round-44 envelope (`claims/envelope.sh`), i.e. under `bwrap --ro-bind /home/vgpnk /home/vgpnk`,
scratch the only writable tree besides `/tmp`.

Read first, in full: `plans/round-44-claims.md` (C1 surface, directions, kill rule, fences F1–F6), the
counter `plans/round44_c1_verify.py` (docstring contract, `MUTANTS` U6 row, `Ctx`, `Runner`, attribution legs
f/g), the tool `plans/anchor_digest_check.py` (`check()` anchor-token branch at :520-523). Frozen artefacts
were not modified: `PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0` in every run below.

## Deliverable

`.ufo/waves/round-44/wave/R44BatU6b/battery/u6_long_b.py` — 128 lines, stdlib only (`hashlib`), sha256
`52f50a2fecd053eb15346964702900859b4e474b06dfcf5fe5207f6b496d773a`. Three fixtures, every fid prefixed
`u6_long_b-`, each a one-line comment naming what it demonstrates. Receipts: `R44BatU6b/RECEIPTS.md`
(verbatim envelope blocks, 7 KB).

## What mutant U6 is

`MUTANTS` U6 = tool `anchor`, class `digest-long`, direction `silence`, `direct`, advertised at
`plans/anchor_digest_check.py:88` ("any other anchor token must be exactly 64 lowercase hex digits
(`digest-short`, `digest-long`)"). Replacement, one line:

    old  cls, why = ("digest-short" if len(tok) < 64 else "digest-long")
    new  cls, why = ("digest-short" if len(tok) < 64 else "digest-short")

So a token LONGER than 64 hex digits stops printing `class=digest-long` and prints `class=digest-short`
instead; the exit code stays 1 (one `DEFECT` line either way). Direction `silence` needs exactly that: the
class is in the reference's output and in the fixture's declaration and absent from the mutant's output.

Reaching the branch requires a row that is (a) 11 cells, (b) bound to a committed capture, (c) carries the
token in anchor cell 5, (d) with no ellipsis (the abbreviation path is a different branch). Length > 64 is what
selects `digest-long`; `detail=<len>-hex` is computed from the token, so no digest constant is baked in.

## Fixtures (three shapes)

| fid | shape | long token | binding route | demonstrates |
|---|---|---|---|---|
| `u6_long_b-registry-80hex` | five-row registry, one SHA256SUMS, one commit | 80 hex = the capture's digest + `0a1b2c3d4e5f6071` | lane path `corpus/evidence/r44b-registry/bravo.md` (`row-path`) | `digest-long` fires inside an otherwise green census of five rows |
| `u6_long_b-provenance-129hex` | two commits; the second adds a `PROVENANCE.md` table line and the row | 129 hex = `(sha(capture)*3)[:129]`, odd length | `PROVENANCE.md` table line naming `S712` and `` `late.md` `` (`provenance-row` only — the source cell names no path) | the class comes from the token, not from a path binding, and survives a multi-commit history |
| `u6_long_b-index-pair-96hex` | one cell with the capture's 64-hex digest AND a 96-hex paste, read through `--evidence-ref index` | 96 hex = `(sha(late)*2)[:96]` | lane path to a capture that is STAGED, not committed (`git add`, no commit) | the branch fires on the second token of a cell whose first token resolves, under the index ref |

All three: `tool="anchor"`, `expect="reject"`, `defects=["digest-long"]` — the exact class set the unmodified
tool prints (one `DEFECT ... class=digest-long` line, exit 1). Argv: `["--lane", "."]` for the first two,
`["--lane", ".", "--evidence-ref", "index"]` for the third — exact option tokens, no `--opt=value`, both
accepted by `argv_shape_breach` and `path_ok` (the token is `.`, resolved against the tool's own cwd = the
fixture dir). Each repo is built from nothing (`ctx.init(d)`, `ctx.write`, `ctx.git add -A`/`commit`); no lane
clone is used, no symlink, no path outside `d`.

## Run 1 — the assignment's command (U6 only, dev battery dir)

    $ envelope.sh "$S/env" python3 .../plans/round44_c1_verify.py --lane "$S/lane" \
        --battery-dir .../wave/R44BatU6b/battery --only U6 --work "$S/w"

    ENVELOPE start 20:33:04 cwd=/home/vgpnk/Projects/shokunin
    PINS total=2 mismatched=0
    FIXTURE u6_long_b-registry-80hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-provenance-129hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-index-pair-96hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=3 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/1 order=0/0
    ADVERTISED direct=1 indirect=0 none=0
    PINS-AFTER mismatched=0
    ENVELOPE end 20:33:06 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

Every FIXTURE line `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and
`U6 killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=3`. `hits=3` means all three
fixtures exhibit the silence direction; the kill is the first one that also passes the traced re-run.

Attribution, leg by leg:
- leg f (span): `L522` is the replaced line, `plans/anchor_digest_check.py:522`
  `cls, why = ("digest-short" if len(tok) < 64 else "digest-long"), f"{len(tok)}-hex"` — `span & t_lines`
  requires it to execute, and the traced re-run reproduces `(exit, class set)`.
- leg g (value): the next event of the `check()` frame is the `defects.append(...)` line, whose locals digest
  includes `cls`/`why` — `digest-long`/`80-hex` vs `digest-short`/`80-hex`. `value=differs`; the reference
  record was stable over two runs, hence `null_detected=0`.

## Run 2 — load-bearing table

Two directions, both under the envelope (receipts §2, §3; `fixtures=1|2 wrong=0 sidechannel=0`,
`killed=1 invalid=0 unattributed=0 null_detected=0` in all six runs, `exit=0`, PATH-dir digest unchanged
`328be01808ba022f` before and after each):

| variant | fixtures left | U6 result |
|---|---|---|
| drop `registry-80hex` | provenance, index-pair | killed by `u6_long_b-provenance-129hex`, hits=2 |
| drop `provenance-129hex` | registry, index-pair | killed by `u6_long_b-registry-80hex`, hits=2 |
| drop `index-pair-96hex` | registry, provenance | killed by `u6_long_b-registry-80hex`, hits=2 |
| keep only `registry-80hex` | 1 | killed by `u6_long_b-registry-80hex`, hits=1 |
| keep only `provenance-129hex` | 1 | killed by `u6_long_b-provenance-129hex`, hits=1 |
| keep only `index-pair-96hex` | 1 | killed by `u6_long_b-index-pair-96hex`, hits=1 |

Reading: no single fixture is necessary (the other two still kill), and each one is individually SUFFICIENT —
every fixture alone runs line 522 and changes the site record. The kill is therefore not concentrated in one
lucky shape; the module is redundant on purpose.

## Run 3 — full default counter on the clone

    $ cp .../u6_long_b.py "$S/lane/plans/battery44/"     # sha256 equal to the wave-dir module
    $ envelope.sh "$S/env" python3 .../round44_c1_verify.py --lane "$S/lane" --work "$S/w2"

    ENVELOPE start 20:33:59 cwd=/home/vgpnk/Projects/shokunin
    PINS total=2 mismatched=0
    FIXTURE u6_long_b-registry-80hex ... observed=digest-long ok
    FIXTURE u6_long_b-provenance-129hex ... observed=digest-long ok
    FIXTURE u6_long_b-index-pair-96hex ... observed=digest-long ok
    MUTANT U5 anchor silence SURVIVED exhibits=none
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=3
    MUTANT U7 anchor rc-mirror SURVIVED exhibits=none
    MUTANT U9 anchor rc-mirror SURVIVED exhibits=none
    MUTANT U14c order error SURVIVED exhibits=none
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/4 order=0/1
    PINS-AFTER mismatched=0
    PREDICATE C1 fail
    ENVELOPE end 20:34:01 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

U6 is killed in default mode too (same attribution line, `L522 value=differs`); U5/U7/U9/U14c survive because
this module targets U6 only — the other seats' modules are not in this clone. `PREDICATE C1 fail` is the
expected whole-round state for one seat's module.

## Contract and fence compliance (observed, not asserted)

- `defects` = `["digest-long"]` and the reference prints exactly that class set; `expect="reject"` = observed
  rc 1 on every fixture (`wrong=0`).
- `sidechannel=0`: the module text carries no SIDECHANNEL token (it is scanned case-insensitively over the
  whole file, comments and strings included).
- F1 `.git` directory + `rev-parse --absolute-git-dir` inside `d`: `ctx.init` produces a normal `.git`
  directory; no fixture writes a `.git` file (`repo_breach` passed for all three).
- F3 exact argv shape: `--lane .` and `--lane . --evidence-ref index`; no other option form.
- F4/F5/F6: no fixture configures git keys, includes, alternates or a worktree; every git call inside a build
  is bounded by the build child's `GIT_CEILING_DIRECTORIES`.
- `tampered=0`: the tool runs read the fixture trees only.
- Host safety: `git clone -q --shared` to `/fast/scratch/hyaku/kengaku-r44/R44BatU6b/lane`, toplevel verified;
  the real lane's `plans/battery44` was not created (`ls` -> no such directory); no write to `~/.local/bin`,
  `/usr`, `/etc`, the fleet root, or the lane. PATH-dir content digest identical in all nine envelope runs.

## Independence of shapes

I did not read `claims/witness/w_u.py` nor `.ufo/waves/round-44/wave/R44BatU6a/` (the second U6 module), and
the battery does not import/copy/read either. Shapes were derived from `anchor_digest_check.py` alone: a
lane-path binding, a provenance-table binding and an index-ref binding, with three different token lengths and
three different registry layouts. A non-author re-spelling check is still worth doing — the counter scans for
tokens, not intent (round-44 claims, "Work" paragraph).

## Limits

1. Direction is `silence`: reference rc and mutant rc are both 1, so these fixtures cannot distinguish "the
   long class is missing" from "the long class was renamed" beyond the class set, and they say nothing about
   exit-code mutations of U6 (none is declared).
2. Token lengths 80/129/96 are arbitrary non-64 values; they exercise `len(tok) > 64`, not a specific length.
   A mutant that only mishandled, say, exactly 65 characters would still be killed, but no boundary case at
   length 65 or at an astronomically long token is pinned here.
3. Fixture 3 depends on `--evidence-ref index` and on a staged-only capture: if a later counter tightens F3 to
   forbid `--evidence-ref`, that fixture would be refused at SETUP rather than fail — a refusal, not a wrong
   result, but it would have to be re-pointed.
4. Measurements ran on a `--shared` clone of lane tip `5e3d3aa`, not on the landing tip; the tools matched both
   pins (`PINS`/`PINS-AFTER mismatched=0`), so the clone's tool bytes are the frozen bytes.
5. The whole-round predicate was not reachable from this seat: `MUTANTS total=5 killed=1` with only this module
   present. U5, U7, U9, U14c remain for their own seats.
6. `null_detected=0` covers determinism of two reference runs on these three fixtures only.
7. No build/lint/test gate was run beyond the counter itself (wave rule: the parent owns post-integration
   gates). The module was not compiled separately; the counter's module load and the build child exercised it.

VERDICT: battery44-u6_long_b-U6-killed-yes-fixtures-3
