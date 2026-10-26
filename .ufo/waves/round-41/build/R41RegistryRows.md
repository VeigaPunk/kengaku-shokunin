# R41RegistryRows — SKILL.md gate/probe registry rows for round 41 (draft)

Seat: `R41RegistryRows` (scribe, leaf). Lane `kengaku-shokunin`. Round 41 wave 1, item = round-40 closure
R3/D2. Draft only — **no lane file was edited**; SKILL.md rows below are paste-ready for the L1.

Clone measured (clean `--shared` clone of the lane, nothing committed there):
`/fast/scratch/hyaku/kengaku-r41/R41RegistryRows/lane`, tip `fc79f2a49be0221e138b3885fa0d83bc43b31a42`.
Every number below comes from a command run in that clone; the command is printed with it and the output is
kept in this directory (§7). Frozen inputs were checked first:
`sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` → 11/11 `OK` (claims `3b239b50…`, C1 counter
`8835a94b…`, C2 counter `cf1632b5…`, probe `8c471fbd…`, spec `8e96421d…`, dry table `a656ce9b…`, capture
manifest `9aafc9a0…`, `tip_receipts.py` `e4f49714…`, `sources_adopt.py` `38492bf1…`, `pkg_gate.py` `ea638822…`,
`order_check.py` `948d5e1d…`). Every run that can write inside a bwrap sandbox — the C1 counter, the C2 counter, the
probe and `tip_receipts` — was made inside the mandated host-guard envelope
(`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin … --unshare-pid --die-with-parent`); the nested sandboxes
work under it, and the envelope re-runs are byte-identical to the earlier bare runs (`c2-env.txt` = `c2.txt`,
`probe-env.txt` = `probe.txt`, `tipfull-env.txt` = `tipfull.txt`, same sha256). Nothing was written outside this
report dir and the scratch dir (scratch deleted, §8).

## 1. Four rows, exact column shape

Insert after the current last row `db-wal-probe` (`SKILL.md:594`, the table's final `|` row; blank line 595).

```
| `round41-c1-mutants` | gate | `python3 plans/round41_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only T01,S02` are development selectors printing `PREDICATE C1 n/a`; `--work DIR` created if absent and **refused inside the lane**; `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` · `1` any survivor (printed `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, `len(MUTANTS)!=23` or a per-tool count other than 13/10, or `PREDICATE C1 fail` · `2` setup/usage: `/usr/bin/bwrap` or `/usr/bin/python3` not executable, `--work` or the scratch root inside the lane, duplicate fixture id, a module that fails to compile or breaches the `build()` contract (argv tail must be a list of str, every absolute path inside its fixture dir), a battery load error; a development selector exits 0 only with no survivor/invalid/null/tamper/sidechannel and no pin drift, and never prints `pass` | itself, plus `.ufo/waves/round-41/claims/`: `control-c1-nothing.txt` (`BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`, exit 1), `control-c1-no-mutants.txt` + `control-c1-no-mutants.patch` (`MUTANTS total=0` with `fixtures=22`, exit 1 — the non-vacuity control), `control-c1-witness-as-battery.txt` (pass reachable by witnessed work), `control-c1-tool-edited.txt` (`PINS mismatched=1 first=plans/tip_receipts.py`, 13 receipts mutants `invalid`), `control-c1-hostile.txt` (`fixtures=1 wrong=0 tampered=0 sidechannel=1`, `n/a`) | the two tool pins in code — `plans/tip_receipts.py` sha256 `e4f49714299ca1f2…`, `plans/sources_adopt.py` sha256 `38492bf175e0c619…` — plus the counter's own digest `8835a94b…` in `claims/frozen-digests.txt`; literals `TOTAL=23`, `FLOORS={receipts:13, sources:10}`; printed `ADVERTISED direct=21 indirect=2 none=0` | fixtures built and every tool run inside `bwrap --ro-bind / /` (lane hidden, fixed system PATH with no `~/.local/bin`, `--unshare-pid --unshare-net`, `HOME=/nonexistent`); scratch only under `--work`/`$TMPDIR`, removed on exit; the lane is read-only; a battery module's source carrying any SIDECHANNEL token is counted in `sidechannel=` | kengaku |
| `round41-c2` | gate | `python3 plans/round41_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **created if absent**) | `0` `checks=8 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>`, including a check that raises (`error <Class>: …` is a defect, never a pass) · `2` argparse usage only | itself; freeze control `.ufo/waves/round-41/claims/control-c2-nothing.txt` (`checks=8 defects=5`: V2, V3, V4, V7, V8; `PREDICATE C2 fail`, `exit=1`) | spec `plans/pkg-spec-r41.json` `8e96421d…`, gate `plans/pkg_gate.py` `ea638822…`, probe `plans/constraints_probe.py` `8c471fbd…`, dry table `corpus/evidence/round41/constraints-dry-cases-freeze.txt` `a656ce9b…`, ten captures under `corpus/evidence/round41/tb2-constraints-scheduling/` (`SHA256SUMS` `9aafc9a0…`), order tool `plans/order_check.py` `948d5e1d…`, claims `plans/round-41-claims.md` `3b239b50…` — all pinned in the counter and in `claims/frozen-digests.txt` | scratch under `--work` only (created if absent, removed on exit); runs `pkg_gate.py package --rerun --require-clean-tree` (which re-runs the probe in a per-case `bwrap` sandbox) and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`; the lane is read-only | kengaku |
| `constraints-probe` | probe | `python3 plans/constraints_probe.py --lane .` (`--dry` prints the 25 frozen cases, their `violates=` tags and predictions with no sandbox; `--stage-check` builds every case's end state and prints only stage exit codes, the grader module is never imported; `--work DIR` scratch parent, created if absent) | `0` every case yielded three test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, measured, exit 0) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=<n> failed=<k>`) · `2` setup: a capture missing or off its pinned digest, `/usr/bin/bwrap` or `/usr/bin/python3`/`/usr/bin/bash` missing, `--work` uncreatable, duplicate case id / unknown tag / malformed prediction, or a case that did not yield three verdicts twice (`SETUP case <id> did not yield …`) | `plans/round41_c2_verify.py` V5 (probe at its freeze digest, `--dry` byte-equal to the dry table); the probe's own second grading of the same end state (`regrade cases=25 differ=0`) | captures `corpus/evidence/round41/tb2-constraints-scheduling/` — `test_outputs.py` `1422b345…`, `solve.sh` `802d81ec…`, `alice_calendar.ics` `5a5d4580…`, `bob_calendar.ics` `c97e85db…`, `carol_calendar.ics` `32a0f868…` — pinned in the probe; dry table `a656ce9b…`; probe digest `8c471fbd…` (`PROBE_SHA256` in `plans/round41_c2_verify.py`, `frozen_instruments` in `plans/pkg-spec-r41.json`) | scratch under `--work`/`$TMPDIR`, removed on exit; one `bwrap` sandbox per case (`--unshare-pid --unshare-net`, `/app` fresh and writable, `/usr` and `/etc` read-only, `/tmp` private); the receipt carries no temp path, timing or host version | kengaku |
| `round-close-check` | gate | `python3 plans/round_close.py --lane . --round N [--census PATH]` (`--lane` must be the git work-tree top; `--selftest` runs five fixture repos; `--work DIR` is `--selftest` scratch only; `--census` else `$SHOKUNIN_ROOT`, else the lane's parents, `plans/round_close.py:138-150`) | `0` every leg passed (`ROUND-CLOSE RESULT PASS exit=0`) · `1` a leg FAILED — `ORDER RESULT FAIL` for the round's receipt(s), or the census leg exiting non-zero (`ROUND-CLOSE RESULT FAIL exit=1`) · `2` setup: `--round` absent (argparse), no census script, no claims file, no order tool, no `corpus/SOURCES.md`, `--lane` not a git work tree or not its top, the claims naming no readable receipt, or a leg exiting outside {0,1} (`ERROR`, `plans/round_close.py:200-213`) | `--selftest` (five two-commit fixture repos differing only in commit order: `A-excused-p10` 0, `B-executed-p10` 1, `C-receipt-first` 1, `D-receipt-uncommitted` 2, `E-no-receipt-named` 2; measured `SELFTEST checks=5 ok=5 failed=0`) | nothing pinned in code: the command prints the digests it evaluated — `claims=… sha256=…`, `order-tool=plans/order_check.py sha256=948d5e1d…`, `census tool=… sha256=3fb72615…`; the order tool is separately pinned by the round's own counter | none — one `git rev-parse`, one `git cat-file -e`, the order tool's own read-only git reads, the census script's read of `corpus/SOURCES.md`; `--selftest` writes only under `--work` or a fresh temp dir; no probe, gate or counter is imported or executed (`plans/round_close.py:42-45`) | kengaku |
```

Row-count effect of the draft: 31 → 35 rows if all four land (`grep -c '^| \`' SKILL.md` over the table
block, `SKILL.md:564-594` (header `:562`), counts 31 today).

## 2. Registry note: `tip_receipts.py`'s derived mapping (R3, second half)

Append as a paragraph after `SKILL.md:643` (end of the round-40 addendum block, before `## Production
checklist` at `:645`). It extends, and must not contradict, `SKILL.md:636-638`.

```
Round-41 registry addendum: `round41-c1-mutants` is the round-41 C1 counter over the two tools round 41 leaves
unedited (`tip_receipts.py`, the `sources_adopt.py` CLI): 23 frozen mutants, 21 `direct` and 2 `indirect`
advertised behaviours, and a predicate that binds both the total and a per-tool floor, so an empty mutant list
fails. At the freeze it was the do-nothing control (`fixtures=0`, `survived=23`); it turns green only with
`plans/battery41/`, built in wave 1 under the counter's sandbox contract — run it with `--lane` on a disposable
clone and only inside the host-guard bwrap envelope. `round41-c2` is the round-40 C2 counter's V1–V7 re-pointed
at the `constraints-scheduling` package plus V8, the order gate on `plans/round-41-claims.md` and its receipt; it
needs the entry (`corpus/knowledge/tb2-constraints-scheduling-grader.md`) and the two index rows as well as the
receipt, and its gate leg re-runs the probe, so a full run costs a probe run (≈16 s measured). `constraints-probe`
is a `probe` row of the round-37 `git-webserver-probe` shape: `mismatches=` is a data line and the exit code never
carries prediction disagreement. `round-close-check` gives `plans/round_close.py` the row round-40 closure D2
asked for: its two legs are the round's order gate and the fleet sources census, the census needs `--census PATH`
when the lane is not inside the fleet (a clone under `/fast/scratch` is not), and warnings (W-codes) do not fail
the leg. The `tip-receipts` derived mapping (round 40) is strict: a receipt the `RECEIPTS` table does not name is
re-run byte-for-byte (`kind=byte`) iff its basename, non-alphanumerics dropped and case folded, equals the stem of
exactly one committed top-level `plans/*.py`; `--list` prints `origin=derived` for it and
`skip reason=no-committed-re-run-command` for zero or two matches, so ambiguity fails closed and the table stays
the override list. Measured 2026-10-26 on tip `fc79f2a4`: 3 derived receipts (`round39/git-leak-probe.txt`,
`round40/db-wal-probe.txt`, `round41/constraints-probe.txt`), `compared=7 declared_bounded=1 no_command=19`,
`byte_equal=7 differ=0`; the round-41 receipt reproduces `equal bytes=5775` in ~54 s, and a fixture lane with
`plans/foo_probe.py` beside `plans/foo-probe.py` leaves `corpus/evidence/round99/foo-probe.txt` unmapped while
`bar-probe.txt` resolves.
```

## 3. Verification: what was executed, and what the row now says

All commands below were run in the clone (`cd …/lane`, `TMPDIR` = scratch); `c1` inside the host-guard envelope.

| entry | command run | observed (verbatim excerpt) | exit | codes exercised / not |
|---|---|---|---|---|
| `round41-c1-mutants` | `bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 plans/round41_c1_verify.py --lane . --work $S/c1w` | `PINS total=2 mismatched=0` · `BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=23 killed=0 survived=23 invalid=0 null_detected=0` · `MUTANTS-BY-TOOL receipts=0/13 sources=0/10` · `ADVERTISED direct=21 indirect=2 none=0` · `PINS-AFTER mismatched=0` · `PREDICATE C1 fail` | 1 | 1, 2 (below); **0 not reachable** — `plans/battery41/` does not exist at tip `fc79f2a4` |
| `round41-c1-mutants` (dev selector) | same, `--only T01` | `MUTANTS total=1 killed=0 survived=1 …` · `PREDICATE C1 n/a (non-default battery or mutant subset)` | 1 | n/a branch measured; the 0 branch of `n/a` needs a killing battery |
| `round41-c1-mutants` (write-scope refusal) | same, `--work $S/lane/xx` | `SETUP --work must not lie inside the lane (the build sandbox hides the lane)` | 2 | 2 |
| `round41-c2` | `python3 plans/round41_c2_verify.py --lane . --work $S/c2w` (dir absent) | `V1 ok listed=10 bad=0 extra=0` · `V5 ok … dry_byte_equal=True` · `V6 ok census_exit=0` · `V8 ok order_exit=0 result=PASS` · `V2 DEFECT spec=frozen gate=frozen gate_exit=1` · `V3 DEFECT rows=2 bad=['S122:row','S123:row']` · `V4 DEFECT receipt or entry absent` · `V7 DEFECT receipt or entry absent` · `checks=8 defects=4` · `PREDICATE C2 fail` | 1 | 1, 2; **0 not reachable yet** — `corpus/knowledge/tb2-constraints-scheduling-grader.md` was absent at measurement (and so were its two index rows) |
| `round41-c2` (`--work` created) | above | `$S/c2w` existed afterwards → `--work` created if absent, as the row now states | 0 | — |
| `round41-c2` (usage) | `… --bogus` | argparse `error: unrecognized arguments: --bogus` | 2 | 2 |
| `constraints-probe` | `python3 plans/constraints_probe.py --lane .` | `regrade cases=25 differ=0` · `cases=25 observed_pass=6 observed_fail=19 mismatches=2` · `cmp` with `corpus/evidence/round41/constraints-probe.txt` → `BYTE_EQUAL` · 13.3 s wall | 0 | 0 (three ways), 2; **1 not exercised** — no stage failure was induced (stage-check was green) |
| `constraints-probe` (`--dry`) | `… --dry` | `CASE`×25, `TAG`×11, `cases=25 predicted_pass=6 predicted_fail=19`; `cmp` with the frozen dry table → `DRY_BYTE_EQUAL` | 0 | 0 |
| `constraints-probe` (`--stage-check`) | `… --stage-check` | `stagecheck cases=25 failed=0` | 0 | 0 |
| `constraints-probe` (setup) | `… --lane $S/emptylane` | `SETUP capture alice_calendar.ics missing or not at its pinned digest` | 2 | 2 |
| `round-close-check` | `python3 plans/round_close.py --lane . --selftest --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --work $S/rcw` | `SELFTEST case=A-excused-p10 … got=0` … `E-no-receipt-named … got=2` · `SELFTEST checks=5 ok=5 failed=0` | 0 | 0 |
| `round-close-check` | same without `--census` (clone outside the fleet) | `ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH` | 2 | 2 |
| `round-close-check` | `… --round 41 --census <fleet script>` | `ORDER RESULT PASS` · `ROUND-CLOSE order receipt=corpus/evidence/round41/constraints-probe.txt exit=0 verdict=PASS` · `ROUND-CLOSE census exit=0 warnings=15 verdict=PASS` · `ROUND-CLOSE RESULT PASS exit=0` | 0 | 0 |
| `round-close-check` | `… --round 40` / `--round 39` | `ROUND-CLOSE RESULT PASS exit=0` (both) | 0 | 0 |
| `round-close-check` | `… --round 38` | `ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10 …` · `ORDER RESULT FAIL` · `ROUND-CLOSE RESULT FAIL exit=1` | 1 | 1 |
| `round-close-check` (census leg) | `… --round 41 --census $S/fake-census.sh` (prints one `E11` line, exits 1) | `ROUND-CLOSE census exit=1 warnings=0 verdict=FAIL` · `ROUND-CLOSE RESULT FAIL exit=1` | 1 | 1 (census half of the map) |
| `round-close-check` | `… --lane .` with no `--round` | `round_close.py: error: --round is required unless --selftest` | 2 | 2 |
| `tip-receipts` note | `python3 plans/tip_receipts.py --lane . --list` | 8 mapped `receipt … origin=table|derived` lines, 19 `skip reason=no-committed-re-run-command`; `round41/constraints-probe.txt kind=byte script=plans/constraints_probe.py origin=derived provenance=plans/constraints_probe.py:4+plans/round-41-claims.md:92` | 0 | 0 |
| `tip-receipts` note | `python3 plans/tip_receipts.py --lane .` (full) | `receipt … round41/constraints-probe.txt equal bytes=5775 exit=0` · `control … verdict=differ` · `note compared=7 declared_bounded=1 no_command=19` · `receipts=27 byte_equal=7 differ=0 skipped=20` · 54 s | 0 | 0 |
| envelope re-runs | the C2 counter, the probe and `tip_receipts` repeated inside `bwrap --ro-bind ~/.local/bin … --unshare-pid` | same output bytes as bare (`V8 ok … checks=8 defects=4`; `cases=25 observed_pass=6 observed_fail=19 mismatches=2`; `receipts=27 byte_equal=7 differ=0 skipped=20`) | 1 / 0 / 0 | same as above — the envelope changes nothing observable |
| derived-mapping limit | `python3 plans/tip_receipts.py --lane $S/fixture --list` on a two-commit fixture lane holding `plans/foo_probe.py` **and** `plans/foo-probe.py` | `bar-probe.txt kind=byte script=plans/bar_probe.py origin=derived provenance=command=plans/bar_probe.py:3,receipt=undocumented` · `foo-probe.txt skip reason=no-committed-re-run-command` | 0 | 0 (fails closed by silence, as the note says) |

## 4. Findings for the L1 (draft-time state, not a judgment on the claims)

1. **Both counters are red at tip `fc79f2a4`, for the reason their rows now name.** C1 has no `plans/battery41/`
   (`fixtures=0`, `survived=23`, exactly the frozen do-nothing control); C2 has no entry and no S122/S123 index
   rows (`defects=4`: V2/V3/V4/V7; the freeze control had `defects=5` with V8 too, because the receipt was not yet
   committed — it now is, `origin=derived`, `equal bytes=5775`).
2. **C2's gate leg is already functional:** the embedded `P10` read the committed receipt and re-ran the probe
   byte-equal (`gate: P10 ok probe_rerun=byte-equal bytes=5775`, `P2 ok receipt_sha256=pinned`). The remaining gate
   defects are entry-shaped (`P3`, `P4`, `P7` entry unreadable; `P6` `S122/S123: rows=0`; `P8` index rows for the
   entry = 0). So C2's red is the admit-and-index work, not the probe.
3. **`round_close.py` needs `--census` outside the fleet.** On a clone under `/fast/scratch` its parent search finds
   nothing and it exits 2 (`plans/round_close.py:138-150`). The existing addendum (`SKILL.md:633-635`) reports the
   rounds 38/39/40 results but not this precondition; the new row states it.
4. **`round_close.py --round 41` is already green**: `ORDER RESULT PASS`, census `warnings=15 verdict=PASS`,
   `RESULT PASS exit=0` — the order gate found the round-41 receipt committed after the freeze
   (`freeze=8ef8b4fc7c6302c527db90244d69aa18f53e83bf`, `receipt_commit=f774a87ad071122acd39ba02a9901b5b56d9910a`).
   The W04 warning count is 15, unchanged from round 40's closure (D3).
5. **The row I drafted for `constraints-probe` says the exit code never carries prediction disagreement**; that is
   load-bearing because the receipt already shows `mismatches=2` with exit 0 (the two carried pilot mismatches
   `later-valid-wed-1105`, `seconds-30` are in it verbatim, and I did not edit them).
6. **`plans/round_close.py` has no `--version`/digest pin of its own**; its self-describing receipt lines
   (`claims=… sha256=…`, `order-tool=… sha256=948d5e1d…`, `census tool=… sha256=3fb72615…`) are the only
   provenance, so anyone re-running it should keep that block. I drafted the row to say "nothing pinned in code"
   rather than invent a pin.
7. **`tip_receipts` now re-runs the round-41 receipt without any table edit** — the derived mapping picked it up
   from the basename, and provenance resolved to the probe docstring line 4 plus the claims file line 92. That is
   the R3 behaviour the note records; the ambiguity fixture (§3 last row) is the fail-closed evidence.
8. Not exercised, stated plainly: `round41-c1-mutants` exit 0 and its `n/a` zero branch; `round41-c2` exit 0;
   `constraints-probe` exit 1. Each needs work that is not mine (a battery, an entry, an induced stage failure), and
   the rows say which output the code must print when it lands. I did not force any of them by editing a frozen
   file.

## 5. Touched surfaces

- Wrote: this report and the receipt files in this directory (§7), plus `/fast/scratch/hyaku/kengaku-r41/R41RegistryRows/`
  (clone, fixture lane, probe/tip scratch — deleted, §8).
- Read only: `SKILL.md` (rows, addenda), `plans/round-41-claims.md`, `plans/frozen-digests` digests,
  `plans/round41_c1_verify.py`, `plans/round41_c2_verify.py`, `plans/constraints_probe.py`, `plans/round_close.py`,
  `plans/tip_receipts.py`, `plans/pkg-spec-r41.json`, `corpus/lessons/round-40-verifier-spotcheck.md`,
  `.ufo/waves/round-41/claims/`.
- No lane file was created, modified or deleted; no git add/commit/stash/checkout/reset/push/pull, no jj command, no
  write to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the fleet root or a sibling lane. No tool installed.

## 6. Out of scope (deliberately not done)

- Editing `SKILL.md` (L1 integrates), `corpus/README.md` index rows for the new entry, the C2 entry itself, and
  `plans/battery41/` (wave-1 executors).
- Pricing `round_close.py`'s 8 surviving mutants and the 6 `F40TipReceipts` defects (R3's second sentence) — that is
  mutation work for a falsify-wave seat, and a mutant list for `round_close.py` does not exist yet.
- Re-running the C1 counter against a battery: none exists, and inventing one would be executor work.

## 7. Artifacts (this directory)

`c1.txt` (C1 run, envelope) · `c2.txt` (C2 run) · `probe.txt` (probe full run, byte-equal to the lane receipt) ·
`dry2.txt` (probe `--dry`, sha256 `a656ce9b…` = the frozen dry table) · `stage.txt` (`--stage-check`) ·
`setup2.txt` (probe setup exit 2) · `rc-selftest.txt` · `rc-41.txt` · `rc-40.txt` · `rc-39.txt` · `rc-38.txt` ·
`rc-efail.txt` (census FAIL leg) · `rc-noround.txt` · `tiplist.txt` (derived rows) · `tipfull.txt` (7 byte-equal) ·
`tipderived-ambiguity.txt` (two-script stem collision) · `c2-env.txt`, `probe-env.txt`, `tipfull-env.txt` (the same
runs repeated inside the host-guard envelope; byte-identical — `c2-env.txt` sha256 `fd5d149c…`, `probe-env.txt`
`c5aa6742…`, `tipfull-env.txt` `7fe38057…`, each equal to its bare twin). Copied at 15:42–15:46 local; the scratch
clone is gone.

## 8. Scratch

`/fast/scratch/hyaku/kengaku-r41/R41RegistryRows/` held the clone `lane`, the fixture lane, and the work dirs
(`pw`, `pw2`, `tw`, `tw2`, `tw3`, `c1w`, `c2w`, `c2w2`, `rcw`, `emptylane`, the fake census). At 15:44 local that
directory was emptied by something outside this seat (the clone, the fixture lane and every receipt disappeared;
the copies in §7 were already made, so no measurement was lost). I re-cloned at tip `fc79f2a4` — unchanged — and
repeated the three sandbox-writing runs inside the envelope; their outputs are byte-identical to the pre-wipe runs
(§3 last row), so the receipts above stand. The directory is removed with `rm -rf` after this report was written.

Verdict line counters, stated so the judge does not read more than was measured: **n = 5** entries drafted (four
table rows + one registry note); **k = 5** entries whose named command was executed in a clean clone at tip
`fc79f2a4` and whose observed exit codes agree with the drafted verdict map for every code that was reachable
(the unreachable codes — C1 `0`, C2 `0`, probe `1` — are named in §3's last column and in §4 item 8, and no row
claims them as observed).

VERDICT: registry-rows-drafted-5-verified-5
