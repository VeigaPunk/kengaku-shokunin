# F42C1StrongAttrib — strong attribution for the 8 vacuous-span mutants (wave 2, falsify)

Critic seat, kengaku round 42 wave 2. Lane read-only; nothing in the lane was edited. Scratch:
`/fast/scratch/hyaku/kengaku-r42/F42C1StrongAttrib` (clone `lane` at docs commit
`508434ad55c709337065611691c426f05875492d`, toplevel verified). All runs under the mandated envelope
(`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin …`), receipts in
`.ufo/waves/round-42/falsify/F42C1StrongAttrib/`.

## 0. What was attacked

`R42CritAttribution` §2.1: for **8/14** round-42 C1 mutants the frozen attribution leg f
(`span ∩ t_lines ≠ ∅`) is vacuous — the mutated line executes on *every* fixture of the tool (3 by
construction: XO6, XO7, X13; 5 more on this fixture family: X1, X9, XO1, XO3, XO5), so the leg cannot
distinguish "the fixture exercises the advertised behaviour" from "the line runs unconditionally". The
residual was named as a per-mutant **value probe** at the mutated site (§2.2). This seat implements that
probe: for each of the 8 mutants, on the battery42 **killing fixture** (the `killed by=` id in
`.ufo/waves/round-42/integrate/measure-final.txt`), measure whether the mutated expression evaluates
differently between reference and mutant.

## 1. Method

- **Environment calibration first.** The frozen counter `plans/round42_c1_verify.py` (sha256
  `559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649`; pinned tools
  `11bb2cad…`/`948d5e1d…` verified at the clone) was run end-to-end on the clone inside the envelope:
  `PINS total=2 mismatched=0`; all 29 `FIXTURE` lines `ok`; `MUTANTS total=14 killed=14 survived=0
  invalid=0 null_detected=0 unattributed=0`; `MUTANTS-BY-TOOL anchor=9/9 order=5/5`;
  `PREDICATE C1 pass`, exit 0. All 14 `killed by=` ids are identical to `measure-final.txt`
  (runs/counter.out, sha256 `2d509638f3dc89ba41f44dadb668e97bdddb0861ed064a0eab4a95a3225cd15f`).
  The battery and runner reproduce the landing measurement.
- **Probes.** For each mutant, a *copy* of the tool in scratch was instrumented at the mutated site to
  print `K42PROBE <repr(value)>` (no imports added; stdout is inert for both tools — the anchor parses only
  `DEFECT` lines, the order gate decides on exit code). Two variants per mutant: the reference (original
  tool) and the mutant (`src.replace(old, new, 1)`, exactly the counter's mutation), both with the same
  instrumentation. The mutant's `old`/`new` strings were taken verbatim from the frozen `MUTANTS` table.
- **Runs.** Each instrumented variant was run on every fixture of its tool through the frozen counter's own
  sandbox shape (`ro_sandbox`: `--ro-bind / /`, ro-bind-data slot fd, `/run`/`/proc` isolated, lane hidden,
  cwd = fixture dir, counter env with git config pinned) — a faithful copy of `Runner.run` that also returns
  stdout (scratch `harness.py`, sha256 `30d0d18159ec2df5d1b27141f017f515dfae9ffe659a83df85ff3d00a37e18a7`;
  artifact runs/harness3.out, sha256 `c4b964f013215c8c108fd018170040af64c345de7972179c0a25d7f39f6f15ed`).
- A kill is strongly attributable iff, on the killing fixture, the site value differs between ref and mut
  **and** the run reproduces the declared direction (rc flips). Both were checked per fixture.

## 2. Result — site value ref vs mut on the killing fixture

| mutant | killing fixture (measure-final `killed by=`) | site (replaced expression location) | ref value | mut value | rc ref→mut | differs |
|---|---|---|---|---|---|---|---|
| X13 | `a_row-x13-staged-capture` | argparse `--evidence-ref` default, `anchor_digest_check.py:570` | `'head'` | `'index'` | 1→0 | **yes** |
| XO1 | `o_clause-freeze-single` | `if git.rc("cat-file","-e",f"{freeze}:{receipt}")==0:` cond, `order_check.py:183` | `True` | `False` (short-circuit) | 1→0 | **yes** |
| XO3 | `o_clause-receipt-withdrawn` | pre-registration cond, `order_check.py:188` | `True` | `False` (short-circuit) | 1→0 | **yes** |
| XO5 | `o_scan-xo5-post-receipt-verdicts` | `rev-list --reverse upto` commit list, `order_check.py:117` | `['434d91ea…']` | `['434d91ea…','d8716612…']` (post-receipt blob commit added) | 0→1 | **yes** |
| XO6 | `o_scan-xo6-pass-verdict-row` | `GATE_P10.match("P10 PASS probe executed twice")` on claims blob line, `order_check.py:53` | `False` (no match) | `True` (match; `|PASS`) | 0→1 | **yes** |
| XO7 | `o_scan-xo7-timeout-rows` | `CASE_LINE.match("CASE lookup-28 observed=timeout rc=timeout")` on claims blob line, `order_check.py:55` | `True` (match) | `False` (no match; narrowed to pass\|fail) | 1→0 | **yes** |
| X1 | `a_route-x1-provenance-table` | `got` list after provenance-row binding, `anchor_digest_check.py:318` | `[('corpus/evidence/42/route-a/registry.capture','provenance-row')]` | `[]` | 0→1 | **yes** |
| X9 | `a_row-x9-short-no-token` | `len(r["cells"]) != NCELLS` cond (cells=10, NCELLS=11), `anchor_digest_check.py:477` | `True` | `False` (`10 > 11`) | 1→0 | **yes** |

All 8 killing fixtures show a value difference at the mutated site, and every instrumented run reproduces
the declared kill direction (ref rc = `EXPECT_RC[expect]`, mut rc = the flipped direction; e.g. X13
`a_row-x13-staged-capture` ref_rc=1/mut_rc=0, XO6 ref_rc=0/mut_rc=1). The probes are therefore
consistent with the frozen counter's own attribution (`attributed=L…`) — the value of the replaced
expression genuinely changes on the killing fixture, so the kill is attributable to the mutation.

### Discrimination (site value differs on which fixtures of the tool)

- XO6: exactly the 2 exhibit fixtures (`o_scan-xo6-pass-verdict-row`, `o_scan-xo6-echoed-pass-row`); on
  the other 3 order fixtures the `P10 PASS` line is absent → `GATE_P10` result identical.
- XO7: exactly the 2 exhibit fixtures (`o_scan-xo7-timeout-rows`, `o_scan-xo7-skipped-row-r38`); on the
  other 3, no `CASE … observed=` line survives the narrowed regex either way.
- XO1/XO3: exactly their 2 exhibit fixtures each (the two clause fixtures); `o_clause-clean-order` and the
  `o_scan-*` fixtures have cond=False in both variants.
- XO5: the 2 exhibit fixtures + the 2 `o_clause-*` reject fixtures (there the receipt/claims commit graph
  also puts a second commit on HEAD's claims path; the ordering clause still rejects in both variants, so
  no rc flip — the site differs but the kill direction is unchanged). The killing fixture itself is the
  exhibit where the added commit decides.
- X1: exhibit pair + `a_class-x7-provenance-row` (ref binds via provenance, mut does not; the fixture still
  rejects with `digest-unknown` both ways, so no rc flip there).
- X9: exactly the 2 exhibit fixtures.
- X13: **all 19 anchor fixtures** (the argparse default is fixed before any fixture byte is read — the
  structural unconditionality already documented by `R42CritAttribution`). The value flip `head`→`index`
  is nevertheless observed on the killing fixture and is what changes the kill.

## 3. What this does and does not establish

- **Establishes:** for the 8 mutants whose span leg is vacuous, the kill is not an artifact of the loose leg
  — the mutated expression itself evaluates differently on the killing fixture, in the direction that
  produces the observed result flip. The value probe is the check `R42CritAttribution` §2.2 asked for.
- **Does not change:** the frozen counter (nothing edited; the run in §1 reproduces the landing
  `PREDICATE C1 pass` unchanged). The proposed counter patch in `R42CritAttribution` §6 (count line events
  only; span = changed lines) is untouched — it is a next-freeze improvement, not this seat's scope.
- **Residual (unchanged from wave 1):** the *generic* tracer cannot observe these values; a durable fix
  needs a `probe` field on each `MUTANTS` row at the next freeze. For X13 the value differs on every
  fixture (the default is process-global), so even the value probe cannot *discriminate* for it — but the
  task asked for attribution on the killing fixture, which the probe now supplies.

## 4. Host safety / receipt

Envelope for every counter/probe run:
`/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs
/run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>` (nested counter sandboxes inside).

| block | start | end | `ls -A ~/.local/bin \| sha256sum` before/after |
|---|---|---|---|
| counter run (runs/receipt.txt) | 18:05:04 | 18:05:07 | `8cf5b151…d86d52` = `8cf5b151…d86d52` |
| harness run (runs/receipt3.txt) | 18:05:29 | 18:05:40 | `8cf5b151…d86d52` = `8cf5b151…d86d52` |

Nothing was written to `$HOME`, `/usr`, `/etc`, any PATH directory, the lane, or the fleet root; scratch
only. No tools installed or updated by this seat.

VERDICT: strong-attribution-8/8
