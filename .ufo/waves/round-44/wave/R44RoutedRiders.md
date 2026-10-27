# R44RoutedRiders — four routed guard/probe defects reproduced in a clone, fixed as patches

Seat R44RoutedRiders (executor), kengaku round 44 wave, 2026-10-26. Lane cloned at tip `5e3d3aa`
(`git -C <clone> rev-parse --show-toplevel` asserted equal to the clone for every clone used). I wrote no lane
file: everything below is a **patch** under `.ufo/waves/round-44/wave/R44RoutedRiders/`, for the L1 to land.

Rows carried by the routed ledger (`corpus/routed-findings.jsonl`) and reproduced here, in the ledger's own
check strings (run with cwd = clone root):

| row | class | source | patch | red before | green after |
|---|---|---|---|---|---|
| `R39-R2` | `probe-work-dir-traceback` | ledger row 2; `corpus/lessons/round-39-verifier-spotcheck.md:134` | `01` (+`01b`) | `rc=1`, `FileNotFoundError` from `plans/git_leak_probe.py:258` | `rc=2`, `SETUP scratch parent … cannot host scratch: No such file or directory` |
| `R42-R3-26` | `guard-exit-code` | `.ufo/waves/round-42/falsify/F42RevRiders.md:74` (D3) | `02` | `rc=1`, `CHECK red reason=sentinel-unreadable:Permission denied` | `rc=2`, `SETUP root-untrusted … reason=sentinel-unreadable error=Permission denied` |
| `R42-R3-27` | `guard-selftest-gap` | `F42RevRiders.md:85` (D4) | `03` | `reported=36 test_rc=1` (`SELFTEST ok=36/36`) | `reported=37 test_rc=0` (`SELFTEST ok=37/37`) |
| `R42-R6` | `scratch-guard-exit-contract` | `plans/scratch_guard.py:17` | `02`+`03` | `grep_rc=1`, 0 case lines | `grep_rc=0`, `case check-sentinel-unreadable PASS exit=2` |

4 rows, 3 code patches plus 1 companion re-pin (`01b`, §5). `R42-R3-26` and `R42-R6` are one root cause seen
twice: the docstring promises `Exit 1 … exit 2 when the root is not a directory or the sentinel cannot be read
(cannot evaluate)` (`plans/scratch_guard.py:17-18`, 24 words), the code returns 1 for the unreadable leg, and the
36-case selftest had no case for it. `R42-R3-27` needs the same missing case.

## 1. Patch inventory

    .ufo/waves/round-44/wave/R44RoutedRiders/
      01-r39-r2-git-leak-probe-work-dir.patch          sha256 73f2fd73f51f1024f5a5c09afd3db289ee673e32cc9eddab5bee23dcba730f6f
      01b-r39-repin-git-leak-probe.patch               sha256 cc128ed77e10c30548a6f81eea85b9583763a7f4d11aadfc9783d34cd945ecfd
      02-r42-r3-26-check-exit2-unreadable.patch        sha256 857a108f0304be6bddcc47b9988452e72072f024f6b067d7ea333d6fda78f323
      03-r42-r3-27-r42-r6-selftest-unreadable-case.patch sha256 12f6841505ae2da098f4966cd4c9b977509872adb3419cdaaa70ab345a9c1fa5
      red-green-receipt.txt     the red→green→attribution→landing receipt (§3, §4, §5)
      isolation-matrix.txt      patch-order isolation and non-vacuity of the new case (§4)
      regress-check.txt         no-harm legs (§6)

Apply with `git apply -p1` from the lane root, order immaterial (the four patches touch four different files or
disjoint regions). Verified in one go on a pristine clone (`lane10`): all four `applied`, then:

    f28d2db2cbda8e62110ec3f2f707394079cfe3e92cdf1e06cd75748324f19965  plans/git_leak_probe.py
    43bff44cf3c8d14cb1120c75c12897133d06662e4e2898c3ca04d495666f9dcf  plans/pkg-spec-r39.json
    d35a1f7cd13412e1c152248be344e799070f89269aeacf5a5e5154fd6c459968  plans/round39_c2_verify.py
    b232262341b34942985fd7351ed502dbf7bd8377d766083f123e3c1f3e330d8f  plans/scratch_guard.py

Pristine bytes for contrast: `git_leak_probe.py` `4961a50f…`, `scratch_guard.py` `f0360e30…`, `pkg-spec-r39.json`
`f62163ce…`.

## 2. The fixes, and why these shapes

**`01` — `git_leak_probe.py` scratch parent (R39-R2).** The probe called
`root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))` (pristine `:258`); an absent `--work`
raised `FileNotFoundError` out of `tempfile` and exited **1**, i.e. a traceback in the exit-code slot the registry
reserves for a case verdict. The ledger allows "create the dir or exit 2 with a setup message"; I chose exit 2 and
never create a caller-supplied tree (a mistyped absolute path must not materialise directories), and I wrapped the
`mkdtemp` call rather than testing `os.path.isdir` first, because the read-only case is the one that bites in this
fleet (the envelope makes `$HOME` read-only):

    parent = a.work if a.work is not None else (os.environ.get("TMPDIR") or "tempfile default")
    try:
        root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
    except OSError as exc:
        print(f"SETUP scratch parent {parent} cannot host scratch: {exc.strerror or exc}", file=sys.stderr)
        return 2

Measured both failure shapes (§6): absent → `No such file or directory`, existing-but-read-only → `Read-only file
system`, both `rc=2`. `--dry` still never touches scratch (`--dry --work /nonexistent` → `rc=0`).

**`02` — `check` unreadable sentinel (R42-R3-26, and half of R42-R6).** New leg in `cmd_check` right after
`sentinel_state()`: a sentinel that exists but cannot be read is *cannot evaluate*, so `return 2` with
`SETUP root-untrusted root=… reason=sentinel-unreadable error=…` (json: `{"ok": false, "reason":
"sentinel-unreadable", "error": …}`), never `CHECK red`. `CHECK red` + exit 2 would reproduce the same
contradiction in the other direction; the `SETUP` line keeps the reason token a consumer greps for, and the
docstring now names that marker.

**`03` — the missing selftest case (R42-R3-27, and half of R42-R6).** One case in `_selftest_in`, after
`check-sentinel-unparseable`: create a sentinel in the bare root, `chmod 000`, drive `check` and `check --json`
through the same dispatch as the CLI, assert `exit=2` and `reason=sentinel-unreadable` on both, then restore the
mode and unlink so the later `refuse-bare-root` case still sees a sentinel-less root. Suite `36/36` → `37/37`.

## 3. Red before, green after (the four ledger checks verbatim)

`/fast/scratch/hyaku/kengaku-r44/R44RoutedRiders/red-green-receipt.txt` = `final-receipt.sh` on a fresh
`--shared` clone `lane10` @ `5e3d3aa`, whole run under the round-44 envelope:

    ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/env15 …/env15 --bind
             …/env15/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent
             -- bash …/final-receipt.sh …/lane10
    ENVELOPE start 20:41:59 cwd=/home/vgpnk/Projects/shokunin
    -- clone: /fast/scratch/hyaku/kengaku-r44/R44RoutedRiders/lane10 @ 5e3d3aa, 0 modified

    == BEFORE any patch ==
      R39-R2: rc=1 | Traceback (most recent call last):
      R42-R3-26: rc=1 | CHECK red reason=sentinel-unreadable:Permission denied round=None want=* seats=0
      R42-R6: grep_rc=1 (0 case line)
      R42-R3-27: reported=36 test_rc=1 | SELFTEST ok=36/36
      round39-c2: checks=7 defects=0 PREDICATE C2 pass

    == + 01b (round-39 re-pin; all four) ==
      R39-R2: rc=2 | SETUP scratch parent …/tmp.02oVdsTKr0/absent cann…
      R42-R3-26: rc=2 | SETUP root-untrusted root=…/tmp.HpFaaMjgF7 reason…
      R42-R6: grep_rc=0 (1 case line)
      R42-R3-27: reported=37 test_rc=0 | SELFTEST ok=37/37
      round39-c2 landed: checks=7 defects=0 PREDICATE C2 pass

    == frozen dry table ==
      cmp_rc=0 (wants 0)
    ENVELOPE end 20:42:07 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

The exact ledger commands, so the L1 can re-run them (each `rc` printed above is `$?` of exactly this):

    # R39-R2
    d=$(mktemp -d -p "${TMPDIR:-/tmp}"); python3 plans/git_leak_probe.py --lane . --work "$d/absent" >/dev/null 2>&1; \
      rc=$?; rm -rf -- "$d"; [ "$rc" -eq 2 ] || [ "$rc" -eq 0 ]
    # R42-R3-26
    d=$(mktemp -d -p "${TMPDIR:-/tmp}"); : > "$d/.ROUND-ROOT-SENTINEL"; chmod 000 "$d/.ROUND-ROOT-SENTINEL"; \
      python3 plans/scratch_guard.py check "$d" >/dev/null 2>&1; rc=$?; chmod 644 "$d/.ROUND-ROOT-SENTINEL"; \
      rm -rf -- "$d"; [ "$rc" -eq 2 ]
    # R42-R6
    o=$(python3 plans/scratch_guard.py --selftest 2>&1) && printf '%s\n' "$o" | grep -qE '^case +check-sentinel-unreadable +PASS exit=2'
    # R42-R3-27
    test "$(python3 plans/scratch_guard.py --selftest 2>/dev/null | sed -n 's/.*SELFTEST ok=\([0-9]*\)\/.*/\1/p' | tail -1)" -ge 37

Raw `R39-R2` failure at the tip, for the record (pristine clone, envelope `env15`, same receipt):

    File "/…/lane10/plans/git_leak_probe.py", line 258, in main
        root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
    FileNotFoundError: [Errno 2] No such file or directory: '/…/tmp.XHhsWPuauy/absent/k39-glr-0g6576ki'

## 4. Attribution (which patch flips which row) and non-vacuity

`isolation-matrix.txt`, fresh clone `lane11` @ `5e3d3aa`, single envelope
(`start 20:42:16 … end 20:42:18 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`):

| applied | R39-R2 | R42-R3-26 | R42-R6 | R42-R3-27 |
|---|---|---|---|---|
| nothing | `rc=1` traceback | `rc=1` | `grep_rc=1` | `36 / rc=1` |
| `02` only | `rc=1` | **`rc=2`** | `grep_rc=1` | `36 / rc=1` |
| `01` only (`+02`) | **`rc=2`** | `rc=2` | `grep_rc=1` | `36 / rc=1` |
| `01`+`03` (`+02`) | `rc=2` | `rc=2` | **`grep_rc=0`** | **`37 / rc=0`** |

`03` without `02` is **red**, which is the point of the added case:

    case check-sentinel-unreadable          FAIL exit=1 expected=2 reason=sentinel-unreadable:Permission json-exit=1 expected=2
    SELFTEST ok=36/37
    SELFTEST failed=check-sentinel-unreadable
    selftest_rc=1 (wants 1 while 02 is absent)

and with `02`:

    case check-sentinel-unreadable          PASS exit=2 expected=2 reason=sentinel-unreadable json-exit=2 expected=2
    SELFTEST ok=37/37
    selftest_rc=0

## 5. Impact: `01` collides with the frozen round-39 pins, and `01b` is the re-pin

`plans/git_leak_probe.py` is a frozen instrument of the round-39 claim: `plans/pkg-spec-r39.json`
`frozen_instruments["plans/git_leak_probe.py"]` and `plans/round39_c2_verify.py` `PROBE_SHA256`/
`SPEC_SHA256` hold `4961a50f…`/`f62163ce…`, and `plans/round39_c2_verify.py` checks them (V2 via the pkg gate,
V5 directly). So `01` alone turns the registered gate `round39-c2` red — measured inside the same receipt:

    == + 01 (probe scratch parent; 02,01) ==
      round39-c2 now (probe patched, pins untouched):
      checks=7 defects=2 PREDICATE C2 fail        # V2 DEFECT spec=frozen gate=frozen gate_exit=1; V5 DEFECT probe or dry table not at freeze digest

`01b` re-pins exactly three values (`pkg-spec-r39.json` frozen instrument → `f28d2db2…`, `PROBE_SHA256` →
`f28d2db2…`, `SPEC_SHA256` → `43bff44c…` = the digest of the edited spec) and the gate is green again with the
patched probe (`checks=7 defects=0 PREDICATE C2 pass`, V5 `dry_byte_equal=True`). The dry table digest
`e92a5d6d…` is untouched, because `01` changes no output on the normal path.

**This is a claims-level decision, not mine.** The round-39 freeze says the probe is frozen at `4961a50f…`;
landing `01` requires an append-only erratum that says why the instrument moved and re-records V5 green. If the L1
refuses that, `01` must not land and `R39-R2` stays *declared, not fixed* as `corpus/lessons/round-40.md:53`
already records for one earlier round.

## 6. No-harm legs (`regress-check.txt`, clone `lane10` with all four applied)

    == dry table byte-equal ==            dry_rc=0  cmp_rc=0   cases=25 predicted_pass=13 predicted_fail=12
    == check on a readable root ==        green_rc=0  CHECK ok round=44 want=* seats=0
    == check --round mismatch ==          mismatch_rc=1  CHECK red reason=round-mismatch round=44 want=43 seats=0
    == safe-rm refusal ==                 safe_rm_rc=2  REFUSE reason=target-outside-seat …
    == compile ==                         py_compile_rc=0
    == read-only scratch parent ==        readonly_rc=2  SETUP scratch parent /home/vgpnk cannot host scratch: Read-only file system
    == --dry ignores scratch ==           dry_absent_work_rc=0
    ENVELOPE end 20:42:29 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

(The `check` green/mismatch/safe-rm/compile legs are unchanged code paths; they are recorded to show the new
`sentinel-unreadable` leg did not swallow the readable-sentinel cases.)

## 7. What the L1 must update when landing (I wrote none of it)

1. Apply `01`, `01b`, `02`, `03` with `git apply -p1`; then re-run the four ledger checks and `plans/tip_receipts.py`
   (the probe receipt re-runs byte-compared; `01` moves no normal-path output, so it should stay `equal`).
2. `plans/round-39-claims.md:72` names the probe digest `4961a50f…` — append the erratum from §5 (append-only).
3. `SKILL.md:587` (`git-leak-probe` row): `--work DIR` is an *existing* parent; add "a scratch parent tempfile
   cannot create under" to the exit-2 setup list.
4. `SKILL.md:589` (`round39-c2` row): probe `4961a50f…` → `f28d2db2…`, spec `f62163ce…` → `43bff44c…`.
5. `SKILL.md:605` (`scratch-root-guard` row): retire the "**`check` on an unreadable sentinel exits 1 today
   although `plans/scratch_guard.py:17-18` promises 2** (measured 2026-10-26, routed `R42-R6`)" clause and the
   "no unreadable-sentinel `check` case yet" note; `SELFTEST ok=36/36` → `SELFTEST ok=37/37`.
6. `SCORECARD.md:1769`: `SELFTEST ok=36/36` → `37/37`.
7. `corpus/routed-findings.jsonl`: close `R39-R2`, `R42-R3-26`, `R42-R3-27`, `R42-R6` with the patch digest, the
   new file digest (`git_leak_probe.py` `f28d2db2…`, `scratch_guard.py` `b2322623…`) and the check's `rc`.
   `R42-R2.1`'s existing close text quotes `f0360e30…`; that is a historical close record — leave it.
8. `corpus/lessons/round-40.md:53` ("R2 … **declared, not fixed**") and `corpus/lessons/round-42.md:89`
   (`SELFTEST ok=36/36`): append-only notes; do not rewrite.

## 8. Limits, risks, and what I did not do

- **Residual in `01`:** the guard proves `mkdtemp` failed, not *why*; the `SETUP` line carries `exc.strerror`
  (`No such file or directory`, `Permission denied`, `Read-only file system`) but no errno.
- **Output-shape change in `02`:** `check` on an unreadable sentinel now prints one `SETUP root-untrusted …
  reason=sentinel-unreadable …` line instead of a `SENTINEL`/`SEAT`/`CHECK red` block, because the root is not
  evaluable and the seat listing was misleading there. `grep -rn scratch_guard` over the lane found no code that
  parses this output (SKILL.md row text, lessons, seat reports only), so nothing breaks; a shell that grepped
  `CHECK red` for this specific case must grep `reason=sentinel-unreadable` instead.
- **`03` scope:** the case asserts exit codes and the reason token; it does not pin the rest of `check`'s output.
- **`03` portability:** mode-000 read refusal is POSIX DAC; a root run reads through it and the case would red.
  The lane runs unprivileged (this host: `id -u` → `1000`).
- **Not run here:** the full 25-case `git_leak_probe.py` receipt (a lane gate — the parent's post-integration
  gate), the `round44_c1_verify.py`/`round44_c2_verify.py` counters, and any lane-wide gate. I ran only
  `round39_c2_verify.py` as *change impact* of `01`/`01b`, which is the gate that pins the file I patch.
- **Separability:** round-44's C1 pins only `plans/anchor_digest_check.py`/`plans/order_check.py`
  (`plans/round44_c1_verify.py:130-133`) and C2 pins its own spec/probe/captures; none of the four patched files
  is on either claim's surface.

## 9. Host safety, tooling, scratch

- Every measurement ran under `.ufo/waves/round-44/claims/envelope.sh` (18 envelope runs, `env`…`env18`), each
  printing `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`; no run exited 4 /
  `INVALID`, so no re-run was needed. Nothing was ever written to `/home/vgpnk/.local/bin`, `$HOME`, `/usr` or
  `/etc`. No tool installed, upgraded or named to pacman; no host service touched.
- Writes: my scratch `$S=/fast/scratch/hyaku/kengaku-r44/R44RoutedRiders` (clone `lane`, `lane2`…`lane11`,
  `pristine/`, `pristine2/`, `env*`, `w*`) and this report's directory only. The lane's tracked files are
  untouched: `git -C <lane> status --porcelain` shows only the round's pre-existing untracked control files. No
  commit, push, `git add`, checkout, reset or jj command ran anywhere; the clones were never committed to.
- Scratch removed with `python3 …/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44
  R44RoutedRiders "$S"` after both receipts were copied here (the round root and its `.ROUND-ROOT-SENTINEL`
  untouched).

VERDICT: rider-fixes-4-of-4-red-green-4
