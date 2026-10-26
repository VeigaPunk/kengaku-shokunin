# R41RevWitness — the 23 frozen C1 mutant rows, audited (round 41, wave 1)

Seat: reviewer, leaf. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. All reviewed files verified
byte-identical to the freeze commit `8ef8b4fc7c6302c527db90244d69aa18f53e83bf`
(`git -C $S/lane diff --stat 8ef8b4fc… HEAD -- <files>` → empty, receipt `freeze-diff.txt`, 0 bytes; lane HEAD
at review time `fc79f2a49be0221e138b3885fa0d83bc43b31a42`). Tool pins re-hashed on the lane:
`tip_receipts.py` `e4f49714…`, `sources_adopt.py` `38492bf1…` — both equal the counter's `PINS`.

## 1. Witness re-run — byte-equal

Command (inside the orchestrator envelope, on my own `--shared` clone, `--work` outside the lane):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  python3 $S/lane/plans/round41_c1_verify.py --lane $S/lane --battery-dir $S/wb --work $S/w
```

with `wb/` holding copies of the two frozen witness modules. Output `witness-rerun.txt` vs frozen
`.ufo/waves/round-41/claims/witness-run.txt`: `diff` empty; sha256 both
`0ec8cae786b1e03d045db7e3109a7d63c0c11f9ff68763d65e3c4f3c8b348ed1`. Tail of the re-run:

```
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0
```

stderr empty. All 23 mutants killed in their declared directions; all 22 witness fixtures `ok`
(`wrong=0 tampered=0 sidechannel=0`). **The frozen witness run reproduces byte-for-byte.**

## 2. Per-mutant table

Quote status: `verbatim` = every quoted fragment found word-exact, in order, inside the cited line range
(whitespace-normalized; for S04 the `#` of the comment's second line is the only between-words byte, see F4).
`RANGE-CLIP` = quote verbatim in the file but the cited range clips the span; `tight` is the minimal
containing range. "words" = quoted words (elisions excluded). Kill fixture = the `by=` the frozen run prints.
Mechanism = what `old -> new` does on that fixture (rc/class values not printed by the counter are marked
`[code]` = derived from the tool source, the direction itself is observed).

| id | tool | direction | adv_kind | adv cites (words) | quote status | killed by | mechanism |
|----|------|-----------|----------|-------------------|--------------|-----------|-----------|
| T01 | receipts | error | direct | tip_receipts.py:30-32 (19w) | verbatim | w-t02-no-evidence | `die()`'s `raise SystemExit(2)`→`(0)`; no-evidence lane ref rc=2 → mut rc=0 `[code]` |
| T02 | receipts | error | direct | tip_receipts.py:30-31 (7w) | RANGE-CLIP tight 30-32 | w-t02-no-evidence | evidence-dir guard → `if False`; run proceeds, 0 receipts, rc=0 `[code]` |
| T03 | receipts | rc-silence | direct | tip_receipts.py:30 (16w) | verbatim | w-t03-probe-exit-3 | probe-exit guard → `if False`; exit-3 probe compares equal → rc 0 (ref 1) |
| T04 | receipts | rc-mirror | direct | tip_receipts.py:21-23 (20w) | verbatim | w-t04-temp-paths-masked | mask equality flipped; temp-paths receipt becomes `differ` → rc 1 (ref 0) |
| T05 | receipts | error | direct | tip_receipts.py:31-32 (7w) | RANGE-CLIP tight 30-32 | w-t05-tamper-unknown | unknown-`--tamper` guard → `if False`; unmapped control id → `KeyError` → rc 1 `[code]` (ref 2) |
| T06 | receipts | rc-silence | indirect | tip_receipts.py:29-30 (14w) | verbatim | w-t03-probe-exit-3 | exit-0 conjunction `and`→`or`; see §4 — w-t06 kills it too |
| T07 | receipts | error | direct | tip_receipts.py:30-31 (9w) | RANGE-CLIP tight 30-32 | w-t07-lane-is-subdir | toplevel check → `if False`; clone of a subdir fails → rc 1 `[code]` (ref 2) |
| T08 | receipts | rc-mirror | direct | tip_receipts.py:19-21 (18w) | verbatim | w-t08-uv-absent | dependency-missing skip disabled; probe runs, `FileNotFoundError` → `differ` → rc 1 (ref 0) |
| T09 | receipts | silence | direct | tip_receipts.py:13-14 (11w) | verbatim | w-t09-two-scripts-one-stem | `len(hit)==1`→`>=1`; two scripts one stem → `map:…:derived` printed, declared `skip` class gone |
| T10 | receipts | silence | direct | tip_receipts.py:15-16 (19w) | RANGE-CLIP tight 14-16 | w-t10-derived-list | `STEM_RE` keeps `_`; stems stop matching → `skip` printed, declared `map` class gone |
| T11 | receipts | silence | direct | tip_receipts.py:13-14 (28w) | RANGE-CLIP tight 12-14 | w-t11-table-over-derived | table-override `continue` disabled; `derive_map` overwrites the table row → `origin=derived`, declared `…:table` class gone |
| T12 | receipts | silence | direct | tip_receipts.py:12 (6w) | verbatim | w-t12-log-receipt | `CANDIDATE_RE` drops `.log`; the log receipt is not even a candidate → no line, declared `skip` class gone |
| T13 | receipts | rc-mirror | direct | tip_receipts.py:26-27 (12w) | verbatim | w-t13-control-differ | `control_ok … and not same`→`and same`; control answers `equal` → rc 1 (ref 0) |
| S01 | sources | 2>0 | direct | SKILL.md:573 (3w); sources_adopt.py:1020-1021 (12w) | verbatim | w-s01-quote-plus-registry | quote/registry exclusivity guard → `if False`; quote mode proceeds with `--registry` → rc 0 (ref 2) |
| S02 | sources | 2>1 | direct | SKILL.md:573 (3w); sources_adopt.py:1042 (7w) | verbatim | w-s02-no-arguments | required-args guard → `if False`; `check(None, None…)` → `AttributeError` → rc 1 `[code]` (ref 2) |
| S03 | sources | 2>5 | direct | SKILL.md:573 (3w); sources_adopt.py:1053 (7w) | verbatim | w-s03-slash-date | access-date ISO guard → `if False`; `build_block` refuses `not-opened-this-round` → rc 5 (ref 2) |
| S04 | sources | 2>0 | direct | SKILL.md:573 (3w); sources_adopt.py:1035-1036 (17w) | verbatim (F4) | w-s04-url-map-with-registry | `--url-map`-needs-quote guard → `if False`; registry mode proceeds, map ignored → rc 0 (ref 2) |
| S05 | sources | 2>0 | direct | SKILL.md:573 (3w); sources_adopt.py:1051 (11w) | verbatim | w-s05-admit-without-entries | entries guard → `if False`; block built with `used-by —` → rc 0 (ref 2) |
| S06 | sources | 2>0 | direct | SKILL.md:573 (3w); sources_adopt.py:1059 (12w) | verbatim | w-s06-recheck-soon | recheck guard → `if False and …`; prose recheck normalized → rc 0 (ref 2) |
| S07 | sources | 3>0 | direct | SKILL.md:573 (4w) | verbatim | w-s07-collision-with-admit | `code != EXIT_OK or not want`→`and`; collision reported, then block built → rc 0 (ref 3) |
| S08 | sources | 2>1 | direct | SKILL.md:573 (3w); sources_adopt.py:1019 (7w) | verbatim | w-s08-quote-file-alone | together-guard → `if False`; `quote_check(…, artifact=None)` → `AttributeError` → rc 1 `[code]` (ref 2) |
| S09 | sources | 2>9 | direct | SKILL.md:573 (7w); sources_adopt.py:1028 (2w) | verbatim | w-s09-url-map-unreadable | `if problem:`→`if False:` skips print **and** the `return EXIT_QUOTE_UNREADABLE` inside it; `load_url_map` returned `({}, problem)` (sources_adopt.py:382) → bind fails unmapped → rc 9 (ref 2) |
| S11 | sources | 5>0 | indirect | SKILL.md:573 (4w) | verbatim | w-s11-queued-row | main's `if missing:` → `if False:`; queued row's `S900:not-mined` refusal bypassed, empty block printed → rc 0 (ref 5) |

All 23 `old` strings occur exactly once in their tool (static scan + the run's `invalid=0`); every
`new` compiles (`py_compile` in the counter). Direction/class consistency rule
(`(direction=="silence") == (cls=="-")`) holds on every row.

## 3. `adv_kind` audit — the `ADVERTISED` recount

Independent count over the 23 rows (not read off the run): T01–T05, T07–T13 direct (12) + S01–S09 direct (9)
= **direct 21**; T06, S11 **indirect 2**; **none 0**. Matches the frozen line `ADVERTISED direct=21
indirect=2 none=0` and the re-run's printed line, and plans/round-41-claims.md §C1. Quoted advertisement
total: 297 words across 23 rows.

Per-row judgement:
- All 21 `direct` rows: the quoted sentence states the behaviour the mutant breaks (exit-code lists,
  skip/map printing rules, guard messages, the comparator must answer `differ`). Sound. S01/S04 quote the
  tool's own comments ("Exclusive: before this guard…", "`--url-map` alone reached neither mode…") — those
  comments state the guard's contract, so `direct` is fair.
- **S11 `indirect` — sound.** SKILL.md:573 advertises `5` = "requested id absent"; the w-s11 row is present
  but `queued`, so the refusal actually exercised (`build_block`'s `not-mined` → same `missing` channel →
  `EXIT_REQUEST`, sources_adopt.py:155-157, 168-170, 1068-1070) is not in the quoted sentence — it follows
  from the sentence plus the code. Correct label.
- **T06 `indirect` — defensible but conservative; see §4.**

## 4. T06: attribution and label

The frozen run prints `MUTANT T06 receipts rc-silence killed by=w-t03-probe-exit-3`, while T06's natural
fixture is w-t06-empty-receipt-control. Checked empirically, inside the envelope, one fixture per run
(receipts `t06-vs-w-t06.txt`, `t06-vs-w-t03.txt`):

- battery = w-t06 only, `--only T06` → `MUTANT T06 receipts rc-silence killed by=w-t06-empty-receipt-control`
- battery = w-t03 only, `--only T06` → `MUTANT T06 receipts rc-silence killed by=w-t03-probe-exit-3`

**Both fixtures exhibit rc-silence for T06** (w-t03: d=1, control ok → mutant `d==0 or control_ok` → rc 0;
w-t06: d=0, control unavailable → mutant returns 0 on the `d==0` disjunct). The counter's kill rule is
direction-based and fixture-agnostic, and `by = by or fx["fid"]` records the *first* exhibiting fixture in
list order — w-t03 precedes w-t06. So the attribution is **sound but order-dependent**: the printed `by=`
is not a canonical witness, and the docstring does not claim it is. No defect; worth knowing when reading
`by=` fields.

Label: the adv cell's parenthetical grounds `indirect` on "an unavailable control on an empty receipt is a
failed control" (the w-t06 reading — needs the code to equate unavailable with failed). But the recorded
kill (w-t03) is grounded *directly* in the quoted sentence itself: "0 every mapped receipt reproduces …
and the control reports `differ`" — the mutant exits 0 while a mapped receipt did not reproduce. Under
round-40 closure R4's definition, the same mutant therefore has a direct grounding for the kill the run
records; `indirect` understates it. Under the direct reading the census would be 22/1/0. The `ADVERTISED`
line is informational (not part of the frozen predicate), the freeze text itself documents the indirect
rationale, and the mutant is killed either way — recorded as a labelling nuance, not a defect.

## 5. S10 withdrawal — rc-equivalence confirmed

Frozen record `.ufo/waves/round-41/claims/s10_equivalence.txt`: `S10 requested-id-absent ref_rc=5 mut_rc=5
EQUIVALENT-BY-RC`. Re-run inside the envelope on my clone (receipt `s10-rerun.txt`): identical line. The
script disables `check()`'s requested-id refusal (sources_adopt.py:236-239); `main()` then reaches
`build_block`, which refuses the same absent id and returns `EXIT_REQUEST` (5) at sources_adopt.py:1068-1070.
Withdrawal is sound for this counter: the kill rule scores (rc, class-set) and the sources class set is
always empty, so a mutant that preserves rc is unkillable — freezing it would break the predicate
permanently. Honest caveat, already implied by "rc-equivalent": stdout is *not* identical (the mutant's
`missing:` line is printed by `main()` after an empty report instead of inside `print_report`'s), but stdout
is outside the kill rule, so the rc-equivalence claim is the right and sufficient one.

## 6. Findings by severity

No high or medium findings. Minor / notes:

- **F1 (minor, citation range, 5 rows — T02, T05, T07, T10, T11).** Each quote is word-verbatim in its
  cited file, but the cited line range clips the span; tight ranges: T02 30-32 (cited 30-31; only the
  closing `)` of the docstring parenthesis lies on line 32), T05 30-32 (cited 31-32; leading "2 usage/setup"
  sits on line 30 — T01 cites the same sentence correctly as 30-32), T07 30-32 (cited 30-31; closing `)`
  again), T10 14-16 (cited 15-16; the leading word "with" ends line 14), T11 12-14 (cited 13-14; "A file
  enters the" ends line 12 — T12 cites line 12 correctly). Clipped content: 2 words, 0 words, 0 words,
  1 word, 4 words respectively. All five are frozen; record-only.
- **F2 (note).** T06 `adv_kind=indirect` is conservative for the kill the run records (§4); census would be
  22/1/0 under the direct reading. No predicate impact.
- **F3 (note, frozen-docstring slip).** `plans/round41_c1_verify.py:75-77` says S10's rc-equivalence is
  "recorded in `claims/witness-run.txt`" — witness-run.txt contains no S10 line (grep: none); the record
  lives in `claims/s10_equivalence.txt`, which plans/round-41-claims.md cites correctly. Frozen; record-only.
- **F4 (note, checker artifact).** S04's quote spans two comment lines (sources_adopt.py:1035-1036); a
  byte-strict join sees `# ` at the break. Every quoted word is present in order; classified verbatim.
- **F5 (note).** For T05, S02, S08 the mutant's rc=1 arises from an uncaught exception (`KeyError`,
  `AttributeError` ×2) rather than a graceful path `[code]`; the declared directions (`error`: mut ∈ {0,1};
  `2>1`) only require the rc, so the kills are valid — but a future battery should not *rely* on crash rcs.

## 7. Host-safety compliance

Every counter/battery/equivalence run above executed inside
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc
/proc --unshare-pid --die-with-parent …`; the counter added its own inner sandboxes. Scratch only under
`/fast/scratch/hyaku/kengaku-r41/R41RevWitness` (clone toplevel asserted before use; no commits anywhere).
No writes outside my report dir and scratch (nothing to timestamp). One anomaly, no impact: my scratch dir
was deleted externally between two calls (parent mtime 15:42, only sibling seats' dirs remained); re-created,
no lane touched. Lane read-only throughout; no git/jj mutation in the lane.

Receipts (this dir): `witness-rerun.txt` (byte-equal re-run), `witness-rerun.err` (empty),
`freeze-diff.txt` (empty), `t06-vs-w-t06.txt`, `t06-vs-w-t03.txt`, `s10-rerun.txt`.

VERDICT: mutant-rows-ok-18/23-adv-misquoted-0
