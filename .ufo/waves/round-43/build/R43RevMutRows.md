# R43RevMutRows — review of the 9 frozen C1 mutant rows (round 43 wave 1)

Seat: R43RevMutRows (reviewer, leaf) · 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: the `MUTANTS` table of `plans/round43_c1_verify.py` (L214-260) checked against
`plans/anchor_digest_check.py` (591 ln), `plans/order_check.py` (214 ln), the recorded witness run
`.ufo/waves/round-43/claims/witness-run.txt`, and `.ufo/waves/round-42/falsify/F42XMutNear.md` §3-§5.
Nothing frozen was edited; no battery43 module exists yet, so no battery was reviewed.

## Inputs (all read-only; digests measured, not assumed)

Clone per the seat rule: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`
with `S=/fast/scratch/hyaku/kengaku-r43/R43RevMutRows`; `git -C "$S/lane" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r43/R43RevMutRows/lane` (asserted before any write); clone HEAD = lane HEAD =
`d33350fdb01ce27cbff47b04642fd2c1471e5c26` (the lane has moved past the claims' baseline tip `317148c4…`; the
five frozen inputs below are byte-identical lane-vs-clone, and the counter's own `PINS`/`PINS-AFTER` checks
passed in the re-run, so the re-run measures the frozen bytes). `git -C "$S/lane" status --porcelain | wc -l`
= `0` after all work.

| file | sha256 (lane = clone) |
|------|-----------------------|
| `plans/round43_c1_verify.py` | `1a1cd1f886fd4581170f83dc4a5293276fd9b981f9a6f1235d121b0cc97d6cca` |
| `plans/anchor_digest_check.py` | `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` (= claims pin `11bb2cad…`) |
| `plans/order_check.py` | `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc` (= claims pin `948d5e1d…`) |
| `.ufo/waves/round-43/claims/witness/w_near.py` | `9a0440083dfda853ec1fbe1c1e0d2fa3c1978b38a456267b1dddf5d8203454c3` |
| `.ufo/waves/round-43/claims/witness-run.txt` | `057d6cd9332535cb5c810a1bcfdb4b66bfd9cee6632a615a1834932985909a84` |

Command: `for f in …; do a=$(sha256sum lane/$f | cut -d' ' -f1); b=$(sha256sum $S/lane/$f | cut -d' ' -f1); …; done`
→ `SAME` for all five.

## Method

1. **Byte-exact static checks** (Python over the clone's files): for each row — `old` occurs exactly once in
   its tool (`src.count(old) == 1`), the mutated source `src.replace(old,new,1)` compiles, the `adv` cell is
   parsed as `path:lo-hi 'quote' (note)`, and the quote (whitespace-normalized, `#` comment prefixes of
   continuation lines dropped, `…`-style ` ... ` elisions split into fragments that must occur in order) is
   located in the tool file with a per-character line map, giving the quote's true line span. Word counts are
   whitespace tokens of the quote, elision marker excluded.
2. **Direction cross-check**: every `MUTANT` line of `witness-run.txt` parsed and compared with the table's
   `tool`/`direction`, the traced `attributed=L<n>` with the first line of the `old` span, and `value=differs`.
3. **Witness re-run** in the clone, inside the round-43 envelope (below), diffed against the recorded run
   with `ENVELOPE` lines stripped from both sides.
4. **§3 cross-check**: each row's id, site branch and replacement compared against `F42XMutNear.md` §3's
   table and §4's demonstrated killers; §5's NA12-null exclusion re-read.

## Witness re-run (receipt `.ufo/waves/round-43/build/R43RevMutRows/witness-rerun.txt`, 3363 B, sha256 `5c95f89de84d40691484a57cdfd17eca95b48e115ce504478748bd0026d7d8de`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/env /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/env --bind /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/lane/plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/lane --battery-dir /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/lane/.ufo/waves/round-43/claims/witness --work /fast/scratch/hyaku/kengaku-r43/R43RevMutRows/w
ENVELOPE start 19:12:01 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 19:12:06 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(A first identical run, 19:11:40→19:11:45, exit=0, same before/after digest `328be01808ba022f unchanged` —
both envelope-valid; the receipt run is the one quoted.) Command:
`envelope.sh "$S/env" python3 "$S/lane/plans/round43_c1_verify.py" --lane "$S/lane" --battery-dir "$S/lane/.ufo/waves/round-43/claims/witness" --work "$S/w"`.

Body of the re-run (ENVELOPE lines aside) is **byte-identical** to the recorded `witness-run.txt`:
`diff <(grep -v '^ENVELOPE ' witness-run.txt) <(grep -v '^ENVELOPE ' witness-rerun.txt)` → empty, `rc=0`.
Key lines reproduced: `PINS total=2 mismatched=0`; six `FIXTURE … ok` lines; nine `MUTANT … killed by=…
attributed=L… value=differs hits=1`; `BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0`;
`MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`;
`MUTANTS-BY-TOOL anchor=6/6 order=3/3`; `ADVERTISED direct=8 indirect=1 none=0`; `PINS-AFTER mismatched=0`;
`PREDICATE C1 n/a (non-default battery or mutant subset)`; exit 0.

## Per-mutant table — quote, kind, span

"quote span" = the lines the quoted words actually occupy (whitespace-normalized join; elision fragments
spanned). "verbatim" = every quoted fragment found in order, unique first fragment (`frag0uniq=1` for all 9).

| id | adv cited | quote span | verdict | words | adv_kind | `old` span (count=1) | mut. compiles |
|----|-----------|------------|---------|-------|----------|----------------------|---------------|
| NA1 | anchor:34-35 | 34-35 | EXACT | 17 | direct | L477 | yes |
| NA5 | anchor:54-56 | 54-55 | CONTAINS (+1 tail) | 17 | direct | L258 | yes |
| NA7 | anchor:112-113 | 112-113 | EXACT | 21 | direct | L458 | yes |
| NA18 | anchor:53-54 | 53-54 | EXACT (elided) | 7 + elision | indirect | L154-155 | yes |
| NA20 | anchor:108-110 | 108-109 | CONTAINS (+1 tail) | 22 | direct | L468 | yes |
| NA21 | anchor:108-109 | 108-109 | EXACT (elided) | 17 + elision | direct | L456 | yes |
| NO5 | order:14-16 | 14-15 | CONTAINS (+1 tail) | 20 | direct | L120 | yes |
| NO7 | order:56-57 | 56-57 | EXACT | 23 | direct | L60 | yes |
| NO22 | order:15-16 | 15-16 | EXACT | 12 | direct | L105-106 | yes |

**Misquotes: 0.** All nine quotes are verbatim in their tool at the cited neighbourhood. The three CONTAINS
rows cite one line more than the quoted words occupy, and the extra line is the *same sentence's* unquoted
continuation, not a different sentence: NA5 L56 `for an evidence directory; the capture is that directory…`;
NA20 L110 `is 64 lowercase hex and a digest **of the capture that row names**…`; NO5 L16 `than \`receipt
unreadable\`, or a receipt-shaped \`CASE ... observed=\` line;`. Every quoted word lies inside the cited
range. If the L1 wants strict span equality the three ranges would trim to 54-55 / 108-109 / 14-15 — a
counter edit, which is frozen, so this is a note, never an action. The two elided quotes (` ... `) replace,
respectively, `or \`github.com/<owner>/<repo>/blob/<commit>/<subpath>\`` (NA18, L53-54) and `from *every*
anchor class above` (NA21, L109) — both elided spans are verbatim too (NA20 quotes the full sentence NA21
elides, same lines).

## adv_kind

- **NA18 `indirect` — right.** The mutation widens the URL_RAW commit group `{7,40}` → `{4,40}`
  (`anchor_digest_check.py:154-155`); the quoted sentence (L53-54) words the URL route and its shape but
  never the 7-hex floor: `grep -n 'abbreviat|7,40|40 hex|7-40|4-40|seven|shortened|abbreviation'` over the
  tool hits `{7,40}` only at code L155/L157, and the docstring's only "abbreviation" (L84) is about
  ellipsis-suffixed anchor tokens, not commit segments. The floor follows from git's abbreviation rule, as
  the claims file words it. (The same floor sits unworded in URL_BLOB L156-157 — not a row here.)
- **The eight `direct` rows — right.** Each quoted sentence words the behaviour the mutation removes:
  NA1 "does not have 11 cells is a `row-malformed` defect" (an over-long row is still "not 11 cells");
  NA7 "no 64-hex token on it may be outside A unless …" (a token *in* A must not be flagged);
  NA20/NA21 the erratum-exemption sentence; NO5 "any file committed … at or before the first commit that
  adds <receipt>" (the mutant scans only the oldest commit); NO7 the P2 echo shape named as excused;
  NO22 "a gate `P10` line whose detail is anything other than `receipt unreadable`" (the gate-line branch
  the mutant disables). NA5 carries one nuance, below.
- **NA5 nuance (judgment note, not a defect).** The sentence words the match target as the committed
  task.toml's `name = "<org>/<task>"`; the reference implements the match on the name's task segment
  (`pick.rsplit("/", 1)[-1]`, L258) and the sentence does not word the `<org>/`-prefix strip. Read
  hyper-literally the sentence describes the mutant's behaviour (full-name match), not the reference's;
  the label `direct` stands on the reading that the sentence's `<org>/<task>` shape *is* the acknowledgement
  that the namespace is stripped before the exact match — the only reading under which the sentence and the
  reference's green behaviour are consistent. The demonstrated behaviour (binding through the committed
  task.toml name, exact match) is the sentence's subject matter, so `direct` is defensible; flagged as the
  one `direct` label whose wording support needs that reading.
- Counter cross-check: the `ADVERTISED` line is derived from the rows, not hardcoded — `adv[adv_kind] += 1`
  at `round43_c1_verify.py:781`, printed at :853; the validity rule (:786) also forces `cls != "-"` iff
  `direction == "silence"` (holds: NA1 is the only silence row and the only one with a class).
- **Recount: `ADVERTISED direct=8 indirect=1 none=0`** — 8 direct (NA1 NA5 NA7 NA20 NA21 NO5 NO7 NO22),
  1 indirect (NA18), 0 none; matches the counter's printed line and the claims file's "8 `direct`,
  1 `indirect`: NA18".

## Directions vs witness-run.txt — 9/9 match

| id | table dir | witness dir | killer (wit-*) | attributed | `old`-span first line | value | §4 killer (w2-*) |
|----|-----------|-------------|----------------|------------|----------------------|-------|------------------|
| NA1 | silence | silence | wit-long-row | L477 | L477 | differs | w2-long-row, L477 |
| NA5 | rc-mirror | rc-mirror | wit-slashed-name-url | L258 | L258 | differs | w2-slashed-name-url, L258 |
| NA7 | rc-mirror | rc-mirror | wit-green-erratum | L458 | L458 | differs | w2-green-erratum, L458 |
| NA18 | rc-mirror | rc-mirror | wit-short-commit-url | L154 | L154 | differs | w2-short-commit-url, L154 |
| NA20 | rc-mirror | rc-mirror | wit-green-erratum | L468 | L468 | differs | w2-green-erratum, L468 |
| NA21 | rc-mirror | rc-mirror | wit-green-erratum | L456 | L456 | differs | w2-green-erratum, L456 |
| NO5 | rc-silence | rc-silence | wit-late-claims-edit | L120 | L120 | differs | w2-late-claims-edit, L120 |
| NO7 | rc-mirror | rc-mirror | wit-p2-excuse | L60 | L60 | differs | w2-p2-excuse, L60 |
| NO22 | rc-silence | rc-silence | wit-late-claims-edit | L105 | L105 | differs | w2-late-claims-edit, L105 |

Every declared direction is what the witness run shows; every kill `value=differs hits=1`; every traced
`attributed=L…` equals the first line of that mutant's replaced span (independently located by `old`'s
unique occurrence). Direction tally: silence 1, rc-mirror 6, rc-silence 2, error 0. The witness module's
`FIXTURES` (6 entries, fids `wit-*`) match the run's six `FIXTURE … ok` lines tool-for-tool and
expect-for-expect (`wit-long-row` anchor reject `[row-malformed]`; the two order fixtures `defects: []`).

## Rows vs F42XMutNear §3 (id, site, replacement) — 9/9 match

| id | §3 site | §3 mutation | table `old -> new` | match |
|----|---------|-------------|--------------------|-------|
| NA1 | X9 `!= NCELLS` | `!=` → `<` (over-long rows unflagged) | `if len(r["cells"]) != NCELLS:` → `< NCELLS:` @L477 | yes |
| NA5 | X12 `slugs[d] = pick.rsplit…` | slug keeps `org/task` (url-task dead) | `pick.rsplit("/", 1)[-1]` → `pick` @L258 | yes |
| NA7 | X14 unresolved guard | drop `t not in allowed` | `… and t not in allowed and t not in cited_wrong:` → drops `t not in allowed` @L458 | yes |
| NA18 | URL_RAW commit group | `{7,40}` → `{4,40}` | @L154-155 | yes |
| NA20 | erratum exemption | `exempt.setdefault` → `pass` | @L468 | yes |
| NA21 | erratum cited_wrong | `t in anchor_tokens` (keyed) | `.get(sid, ())` → bare dict @L456 | yes |
| NO5 | XO5 scan loop | `commits` → `commits[:1]` | @L120 | yes |
| NO7 | P2 excuse regex | drop `(?:: \S+)?` variant | `r"^receipt unreadable(?:: \S+)?$"` → `r"^receipt unreadable$"` @L60 | yes |
| NO22 | gate-p10 branch | `if m:` → `if False:` | @L105-106 | yes |

§3's site column names the *frozen round-42 mutant branch* each near-variant sits on; every named branch is
the code span the round-43 row replaces (verified by unique-occurrence location, table above). §4's nine
demonstrated killers and attributed lines match the witness run's (fixture ids renamed `w2-*` → `wit-*`,
same shapes — the witness module's fixture docstrings carry the same intent sentences). §5's NA12 null
exclusion re-read: `< 64` → `<= 64` unreachable behind the `len(tok) != 64` guard — NA12 is correctly out,
and `TOTAL = 9` / `FLOORS anchor=6 order=3` in the counter agree with the 9-row table.

## Findings summary

1. **0 misquotes** — all 9 `adv` quotes verbatim; 6 exact-span citations, 3 citations one line longer at the
   tail into the same sentence's continuation (NA5, NA20, NO5 — note only, quote fully inside the range).
2. **adv_kind right 9/9** — NA18 `indirect` confirmed (7-hex floor worded nowhere in the docstring); the
   other 8 `direct` confirmed; NA5 flagged as the one `direct` resting on the tail-match reading of
   `name = "<org>/<task>"` (judgment note, defensible).
3. **Directions 9/9** as witnessed; all kills `value=differs`, `hits=1`, attributed to the replaced span's
   first line.
4. **§3 match 9/9** on id, site branch, replacement, direction; NA12 exclusion per §5 consistent.
5. **Recount `ADVERTISED direct=8 indirect=1 none=0`** — derived from the rows (counter :781/:853), matches
   the printed line and the claims file.
6. **Witness re-run reproduces the recorded run byte-for-byte** (ENVELOPE lines aside), exit 0, envelope
   digest unchanged at both boundaries.

Residual risk / verification gaps: my quote-span mapping normalizes whitespace and drops `#` comment
prefixes on continuation lines (needed to join wrapped comment prose); each quote's first fragment is unique
in its tool (`frag0uniq=1`), so no false-positive location is plausible. The re-run rode the clone's HEAD
`d33350fd…` (lane has moved past the claims' baseline tip); the five frozen inputs are byte-identical to the
lane and `PINS`/`PINS-AFTER` passed, so the measurement is of the frozen bytes. The counter's /run slot names
(`k43-tracer.py` etc.) are shared across seats; no collision was observed in either run (outputs identical
to the recorded run), but a concurrent counter run by another seat remains a theoretical interference the
envelope cannot see.

Scratch `S=/fast/scratch/hyaku/kengaku-r43/R43RevMutRows` removed after the report was written
(`scratch_guard.py safe-rm`).

VERDICT: mutant-rows-ok-9/9-adv-misquoted-0
