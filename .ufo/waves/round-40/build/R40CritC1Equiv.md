# R40CritC1Equiv — Q29 audit: are the 21 frozen C1 directions reachable, or is any mutant equivalent?

Seat: critic, round 40 wave 1. Scope: `plans/round40_c1_verify.py` `MUTANTS` (21 entries: anchor 11, ledger 7, order 3)
against the pinned tool bytes (`anchor_digest_check.py 11bb2cad…`, `ledger_tip.py 853bcb2a…`, `order_check.py 948d5e1d…`).
Nothing frozen was edited. All work ran in `/fast/scratch/hyaku/kengaku-r40/R40CritC1Equiv` (clone `--shared` of the lane,
`rev-parse --show-toplevel` = the clone; HEAD `3077adbc7145726519f60f01426a5d03381ad444`) and was deleted at the end.

Question asked of every mutant: from the tool source, is the declared direction (`silence | rc-silence | rc-mirror |
error | rc-error`, `exhibits()` in `plans/round40_c1_verify.py:393-404`) reachable — i.e. is there a fixture of the same
tool on which `(exit code, class set)` moves in that direction? A mutant with no such fixture would be observationally
equivalent at the counter's granularity and could never be killed by any `plans/battery40` module.

## Verdict shape

**21/21 reachable, 0/21 equivalent.** Every declared direction was *measured*, not just argued, on a fixture built from
the frozen bytes. The witness column is still imperfect: one cell cites a fixture that exhibits a different direction
(F1), one names a fixture id that does not exist (F2), and four carry a broken locator (F3). None is a direction defect;
F1 is the one that can cost a wave-1 executor a kill.

## Method (four independent legs)

1. **Needle/compile leg.** Imported the frozen `MUTANTS` table and, against the pinned tool bytes in my clone:
   every `old` string occurs exactly once (21/21 `needle=1`) and every mutant compiles (`py_compile`, 21/21). Command:
   a python script loading `plans/round40_c1_verify.py` from the clone and printing `f"{mid} … needle={n} {ok}"`.
   This is the precondition for `invalid=0` in the frozen predicate.
2. **Round-39 harness, repointed to round-40 HEAD.** Copied `h_anchor.py` / `h_ledger.py` into scratch, changed only
   `S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/R40CritC1Equiv")`; `TAG=_r40 python3 h_anchor.py` (140 s) and
   `TAG=_r40 python3 h_ledger.py` (593 s). At the round-40 tip the anchor run reproduces `out_anchor_r5.txt` line for
   line except the row count (`rows=111 tokens=19` vs `rows=109 tokens=17` — S119/S120 landed) and
   `MUTANTS n=24 killed_by_all_fixtures=21`; the ledger run reproduces `out_ledger_r5.txt` exactly
   (`n=18 killed_by_tip=2 killed_by_tip+d4=3 killed_by_all=13`, same killers).
3. **Frozen counter, with the committed witness battery plus one critic fixture.** Wrote a scratch battery dir holding
   the three `claims/witness/*.py` modules verbatim plus `eq_a17.py` (below), then ran
   `python3 plans/round40_c1_verify.py --lane <clone> --battery-dir <scratch>/bat --only A17,A27,L01,L11,L21,O04,O12,O14 --work <scratch>/w`
   → `BATTERY fixtures=10 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=8 killed=8 survived=0 invalid=0
   null_detected=0`, `PINS mismatched=0` both ends, `PREDICATE C1 n/a` (development mode), exit 0. So A17 is killable
   *in its declared direction* under the frozen rule itself.
4. **Direct `(ref, mut)` measurement** of every remaining mutant on its killer fixture, printing exit code and the
   counter's own class extraction (`class=` tokens; `NO:<id>` on `agree=NO`; `hit:`/`fail:` lines).

Class-set granularity is the counter's: `classes()` at `plans/round40_c1_verify.py:333-350`.

## Per-mutant result

`ref → mut` is `exit/classes`. Fixtures are the round-39 `h_*` fixtures (X/T numbers) or the committed round-40
witnesses (w-*), both rebuilt at the round-40 tip; `eq-a17` is my scratch fixture.

| id | tool | class | declared | cited witness | measured `ref → mut` | direction met |
|---|---|---|---|---|---|---|
| A01 | anchor | digest-uppercase | silence | X01-upper | `1/{digest-uppercase} → 1/{digest-unknown}` | yes (class leaves the set) |
| A02 | anchor | - | rc-silence | X03-abbrev-7hex | `1/{abbrev-unresolved} → 0/{}` | yes |
| A03 | anchor | - | rc-silence | X05-abbrev-64hex-ellipsis | `1/{abbrev-unresolved} → 0/{}` | yes |
| A06 | anchor | - | rc-mirror | X09-indent4-wrong | `0/{} → 1/{digest-wrong-capture}` | yes |
| A08 | anchor | - | rc-silence | X06-token-in-teaches | `1/{token-outside-anchor} → 0/{}` | yes |
| A09 | anchor | - | rc-silence | X07-12-cells | `1/{row-malformed} → 0/{}` | yes |
| A15 | anchor | - | rc-silence | X17-duplicate-task-slug (index) | `1/{anchor-unbound} → 0/{}` | yes |
| A17 | anchor | - | rc-mirror | X15-index-staged-capture (index) | **`0/{} → 2/{}`** (rc-error shape) | **not via the cited witness**; yes via `eq-a17-staged-modified` → `0/{} → 1/{digest-unknown}` |
| A21 | anchor | - | rc-mirror | X21-uppercase-manifest-entry (index) | `0/{} → 1/{digest-unknown}` | yes |
| A22 | anchor | - | rc-mirror | X20-stale-manifest-digest (index) | `0/{} → 1/{digest-wrong-capture}` | yes |
| A27 | anchor | capture-unanchored | silence | w-a27-second-url / X10-second-url | `1/{capture-unanchored} → 0/{}` | yes |
| L01 | ledger | - | error | T08-source-not-a-repo | `2 → 1` | yes |
| L05 | ledger | - | rc-silence | T05-control-row-flipped-open | `1/{NO:R34-D2} → 0/{}` | yes |
| L06 | ledger | - | rc-silence | T06-control-empty-ledgers | `1/{} → 0/{}` | yes |
| L11 | ledger | - | error | T09-source-work-exists (empty `<work>/lane`) | `2 → 0` | yes |
| L14 | ledger | - | rc-silence | T10-control-check-crashes | `1/{NO:R34-D3} → 0/{}` | yes |
| L15 | ledger | - | rc-silence | T07-control-unknown-check | `1/{NO:R34-D5} → 0/{}` | yes |
| L21 | ledger | - | error | control-mode stale `master` (HEAD~6) | `2 → 0` | yes |
| O04 | order | - | rc-silence | w-o04-p10-ok-excuse | `1/{hit:gate-p10} → 0/{}` | yes |
| O12 | order | - | rc-error | w-o12-gitlink | `0/{} → 2/{}` | yes |
| O14 | order | - | error | w-o14-claims-name-suffixed | `2/{} → 0/{}` | yes |

Every direction is also met *inside* the frozen rule, i.e. with a fixture whose declared `expect`/`defects` equal the
reference result: the silence rows need `defects` = the reference class set (A01 `["digest-uppercase"]`, A27
`["capture-unanchored"]`), the ledger rc-silence rows need `expect="reject"` with the exact `NO:` id shown above, the
error rows `expect="error"`, and A06/A17/A21/A22 `expect="accept"`.

## Equivalence work

**No frozen mutant is equivalent.** For each of the 21 there is an input where `(exit, classes)` differs in the declared
direction — table above. A27's mutation deserves a note because it *looks* syntactic: `defects.append(f"…")` becomes a
parenthesised expression `(f"…" f"…")`, which compiles (the closing paren of the last f-string now closes the tuple-free
expression, `py_compile` ok) and silently drops the defect line. Both effects measured: on X10-second-url
`1/{capture-unanchored} → 0/{}`.

**The withdrawn O13 is equivalent — the counter's argument is sound.** O13 (`.ufo/waves/round-39/build/R39PlanNext/
order-mutants/O13.py`) differs from the pinned tool only at `order_check.py:110`: `CASE_LINE.search(line)` for
`.match(line)`, the pattern unchanged. `CASE_LINE.flags` is `32` (UNICODE only, no `MULTILINE`), so `^` matches at
position 0 only; `blob_hits` (`order_check.py:101-114`, the call at `:110`) applies the pattern to a single line at a
time, so
`bool(match(l)) == bool(search(l))` for every line. Empirical check over the lane's own claims history: 5,529 distinct
`.ufo/waves` blobs, 2,351,137 lines, 1,042 lines where `CASE`-matching succeeds, **0 disagreements** (command in the
reproduction block). The freeze's choice to list O13 as a limit and not freeze it is correct.

## Findings

**F1 (worth a wave-1 action) — A17's cited witness exhibits the wrong direction.** X15 stages a *new* capture whose path
does not exist at HEAD; under the mutant's swapped `spec_for` (`anchor_digest_check.py:194-196`, advertised at `:74`)
`git cat-file --batch` returns
`<spec> missing`, `blobs()` raises `Usage` and the tool exits **2**, so X15 measures `0 → 2` (rc-error), not the declared
`rc-mirror` (`exhibits()` requires `mut[0] == 1`). Measured above; the r5 harness recorded it only as `:rc`, which hides
the distinction. `rc-mirror` *is* reachable, but only from the other index-mode shape: a capture that exists at HEAD and
is **modified in the index**. My scratch fixture does that (append one line to
`corpus/evidence/round37/tb2-git-webserver/test_outputs.py`, update that directory's `SHA256SUMS`, restage, repoint
S111's token to the staged digest) and gives `0/{} → 1/{digest-unknown}`; the frozen counter killed A17 with it
(`MUTANT A17 anchor rc-mirror killed by=eq-a17-staged-modified`). Smallest safe correction: the `plans/battery40` module
that covers A17 must use the modified-staged shape. A fixture ported from X15 leaves A17 surviving with
`exhibits=rc-error` and C1 unadmitted. Nothing frozen needs editing — the counter docstring's rule already says a kill
needs "a fixture of the same tool" in the declared direction; only the witness cell's citation is loose.

**F2 — O14's witness cell names a fixture that does not exist, and half the mutation is inert.** The cell says
`witness/w_order.py w-o14-claims-name-prefixed`; the module defines `w-o14-claims-name-suffixed`
(`.ufo/waves/round-40/claims/witness/w_order.py:37-38`). The mutant removes **both** anchors, but under `CLAIMS_NAME.match`
the `^` is already implicit, so only `$` is reachable — exactly the **suffixed** fixture (`round-50-claims.md.bak`,
ref `2` → mut `0`). The direction is reachable; the cell's name is wrong.

**F3 — four witness cells cite a path inside a directory.** L21, O04, O12, O14 point at
`{P39}/R39PlanNext.md:110-111` / `:126` where `P39 = .ufo/waves/round-39/build/R39PlanNext`, a directory; the report is
`.ufo/waves/round-39/build/R39PlanNext.md` (sibling). Locator defect only; the cited content exists at the corrected path
(§2.4/§2.5).

**F4 — six kills need a shape the lane does not contain.** A01 (uppercase 64-hex), A02/A03 (short/long ellipsis prefixes),
A06 (4-space row), A09 (12-cell row), A15 (two `task.toml` claiming one slug), A21 (uppercase manifest entry) and A22
(stale manifest entry) are all *lane-equivalent*: at the tip every manifest is lowercase and byte-accurate, every row is
11 cells at ≤3 spaces, and every slug is unique. Their kills are legitimate (each is a sentence the tool advertises:
`anchor_digest_check.py:31,44-46,55,84-89`), but a battery that clones "tip shape" alone kills none of them. This is the
same asymmetry round 39 recorded for batteries; executors should build each fixture to the advertised sentence, not to the
current lane.

**F5 — L11 needs an *empty* `<work>/lane`.** With the empty dir the unmodified tool refuses (`2`) and the mutant clones
into it and runs (`0`). With a non-empty dir both refuse (`2`: ref `REFUSE will not reuse …/lane`, mutant
`REFUSE git clone --shared … failed`, measured) and the mutant survives. The
counter's contract token `{WORK:lane}` ("a fresh path already holding an empty `lane/` dir",
`round40_c1_verify.py:34-36`) is exactly this; the battery must use it, not a pre-filled dir.

**F6 — no text-only mutant is in the 21.** Every measured difference is an exit code or a class-set membership, so the
docstring's exclusion of "summary-line counts, labels" from this table is honoured (`round40_c1_verify.py:62-63`). For
contrast the r5 harness's text killers (A18, L08, L09, L16-L18) are all absent from `MUTANTS`, as claimed.

**F7 — L21's mutant also lies in its provenance line.** With the stale `master`, the mutant prints
`REF AUDIT ref=refs/heads/master rev=9d3aff94… tip=3077adbc… state=match` although rev ≠ tip — the same harm shape as
round 38's F1 that the refusal exists to prevent. No direction reads that text; the kill stays the exit code (`2 → 0`),
so the mutant is under-specified rather than mislabelled.

## Limits of this audit

- Reachability is evidenced on fixtures I built at the round-40 tip; each is one input, not a proof of non-equivalence
  for all inputs — the point needed, since a direction needs one fixture.
- The `plans/battery40` modules do not exist yet, so no claim is made that any *committed* fixture kills these; the
  round-40 do-nothing control (`killed=0 survived=21`) still holds by construction.
- I did not judge C2, and I did not edit any lane file: `eq_a17.py` is a critic scratch fixture, copied beside this
  report for the executor, **not** a battery40 module (it carries no side-channel token, but a battery40 author must
  re-derive and own it).

## Reproduction (all from `/fast/scratch/hyaku/kengaku-r40/R40CritC1Equiv`)

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane   # HEAD 3077adbc…
cp .ufo/.../round-39/build/R39PlanNext/{h_anchor,h_ledger}.py r39/        # then S = this scratch dir
TAG=_r40 python3 r39/h_anchor.py     # 24 mutants, killed_by_all=21, same killers as out_anchor_r5.txt
TAG=_r40 python3 r39/h_ledger.py     # 18 mutants, killed_by_tip=2 +d4=3 all=13, identical to out_ledger_r5.txt
python3 lane/plans/round40_c1_verify.py --lane lane --battery-dir bat \
        --only A17,A27,L01,L11,L21,O04,O12,O14 --work w
  # -> MUTANT A17 anchor rc-mirror killed by=eq-a17-staged-modified; 8/8 killed; PINS mismatched=0 both ends
```

Direct measurements (ref and mutant on the same fixture, class extraction identical to the counter's) produced the
`ref → mut` column above; the O13 scan is
`for line in blob.splitlines(): bool(CASE_LINE.match(line)) == bool(CASE_LINE.search(line))` over every distinct
`.ufo/waves` blob of the clone (`git rev-list --all -- .ufo/waves`, `ls-tree -r`, `cat-file blob`).

## Recommendation to the L1 (no frozen edit implied)

1. Wave-1 anchors: build the A17 fixture as *modified-staged-capture* (F1), the L11 fixture with `{WORK:lane}` (F5),
   and the A21/A22/A15/A09/A06/A02/A03 fixtures against their advertised sentences rather than tip shape (F4).
2. In the round-40 report, record F1 as a witness-citation defect (declared `rc-mirror`, cited witness is `rc-error`),
   and F2/F3 as documentation defects in the `MUTANTS` witness column. All three belong in `corpus/lessons/round-40.md`;
   none licenses removing or relabelling a mutant.
3. Keep O13 as a named limit; the equivalence argument is now backed by an exhaustive-ish empirical check as well as the
   analytic one.

VERDICT: c1-directions-reachable-21/21-equivalent-0
