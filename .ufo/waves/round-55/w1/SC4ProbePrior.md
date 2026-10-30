# SC4ProbePrior — scoped findings: the established TB2-grader probe pattern

**Seat:** SC4ProbePrior (scout, read-only). **Wave:** kengaku round 55 w1.
**Deliverable:** `.ufo/waves/round-55/w1/SC4ProbePrior/pattern.md` — the extracted pattern, with
file:line quotes, so E5's `plans/round55_c3_chess_probe.py` can be checked against it.

**Sources read (all lane-repo, read-only):** `plans/round-55-claims.md` (frozen claims, commit
`80afa613`; I changed nothing in it), `plans/password_recovery_probe.py` (r45 C2),
`plans/polyglot_c_py_probe.py` (r46 C3), `plans/build_pmars_probe.py` (r38 C2), the committed
receipts and dry-table freeze receipts, `SKILL.md:565-632` (the gate/probe registry),
`plans/round52_c2_registry.py`, `plans/round46_c3_verify.py`, `plans/order_check.py`,
`plans/attrib_probe.py`, `corpus/lessons/round-45.md`, `corpus/evidence/round52/graders/`.

**The five requested items, each with file:line quotes** (full text in pattern.md §1-§5):

1. **bwrap flag pattern** — identical shared core in all three: `--unshare-net --unshare-pid
   --unshare-ipc --die-with-parent --new-session` + `--ro-bind /usr /usr` + the
   `/bin /sbin /lib /lib64` symlink loop + `--ro-bind /etc /etc --proc /proc --dev /dev --tmpfs
   /tmp` + grader dir **read-only** at `/tests` + `/app` **writable** via `--bind` + `--chdir
   /app` last. `password_recovery_probe.py:213-226`, `polyglot_c_py_probe.py:349-363`,
   `build_pmars_probe.py:239-252`. Grader runs via a bound pytest-free harness printing
   `TEST <name> P|F` lines (`password_recovery_probe.py:175-205, 233-236`;
   `build_pmars_probe.py:174-187`).
2. **Frozen case table + predictions** — module-level `PINS` (digests), `TAGS` (tag →
   instruction line), `TESTS` (ordered test names), and `CASES` = list of a **frozen dataclass**
   `Case(cid, predicted, violates, requirement, recipe)`; the prediction is a **per-test letter
   string** (`P`/`F`/`-`), collapsed by `overall()` into pass/fail.
   `password_recovery_probe.py:69-92, 102-109, 279-281`; `polyglot_c_py_probe.py:73-107,
   172-180`; `build_pmars_probe.py:55-73, 82-100`. Table is frozen twice: in source and as a
   committed `--dry` receipt (byte-equal on re-run — verified for r45 and r46).
3. **Observed vs predicted / mismatches** — one `CASE <cid> predicted=pass observed=pass
   tests=… predicted_tests=… match=yes|NO [regrade=…] violates=… -- <requirement>` line per case,
   then `regrade cases=<n> differ=<k>` (r45/r46) and
   `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>`.
   `password_recovery_probe.py:352-358`, `polyglot_c_py_probe.py:514-520`,
   `build_pmars_probe.py:340-344`. The summary shape is what lane counters parse
   (`round46_c3_verify.py:134, 307`).
4. **CLI conventions** — `--lane` (default `.`), `--work` (scratch parent), `--dry` (frozen table,
   no sandbox), `--stage-check` (build states, never grade) or `--smoke` (plumbing only);
   `--dry`/`--stage-check` mutually exclusive. `--selftest` is the *counter* convention
   (`round52_c2_registry.py:194`, `registry_check.py:146`); `--receipt` is a *file-writing*
   convention (`attrib_probe.py:1137`, `order_check.py:145`) that the three probes do **not** have
   — their receipt is bare stdout (lane lesson `corpus/lessons/round-45.md:13`).
5. **Exit-code contract** — probes: `0` = ran and printed the summary (**mismatches never change
   the exit code**), `1` = only `--stage-check`/`--smoke` failure, `2` = setup error (bad table,
   capture off its digest, missing tool, uncreatable `--work`, failing recipe). Counters instead
   print `PREDICATE <id> pass|fail` and use `0/1/2` for pass/fail/setup
   (`round52_c2_registry.py:133-135`, `round46_c3_verify.py:906-909`). Registry rows state the
   probe contract verbatim (`SKILL.md:582, 615, 616`).

**Defects found (in the current draft `plans/round55_c3_chess_probe.py`, not in the pattern; the
draft is untracked and absent from the freeze commit `80afa613`):**

* **D1 — a non-AssertionError grader failure is scored SETUP, not a case verdict.**
  Draft `:126-130` keys the F verdict on the literal `AssertionError` in the output; the pattern
  maps any other exception to `F error=<Class>` (`build_pmars_probe.py:185-186`). Measured: with
  `/app/move.txt` as a directory the grader raises `IsADirectoryError` (no `AssertionError`), which
  the draft would score SETUP (whole run exit 2) where the pattern scores `F error=IsADirectoryError`.
* **D2 — the summary line can print `mismatches=0` while a case went unevaluated.**
  Draft `:161-166` records a SETUP case, `:174-175` prints the summary *before* the SETUP check at
  `:176-178`. Measured: one forced SETUP case ⇒ `cases=12 observed_pass=4 observed_fail=7
  mismatches=0` (4+7 ≠ 12), then `SETUP cases=…`, exit 2. R55-C3's kill rule (a) targets exactly
  "an observed≠predicted case not counted as a mismatch"; the lane's own detector for this shape is
  `round46_c3_verify.py:331-335` (`p + f == n`), which the printed line violates.
* **D3 — `--work` is destroyed wholesale.** Draft `:228` uses `--work` as the work dir and
  `:242-243` `shutil.rmtree(work)` deletes the caller's whole directory. Measured: a `--work` dir
  pre-populated with `precious/data.txt` came back deleted. The pattern deletes only its own
  `mkdtemp` root inside `--work` and leaves the caller's directory intact (verified for r45).
* **D4 — the receipt does not parse under the lane's own receipt parser.**
  Draft `:173` prints `CASE <name> predicted=P observed=P rc=0` (no `match=`, no `violates=`,
  no per-test letters). `round46_c3_verify.py:307` requires
  `^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) .*?\bviolates=(\S*)` and would parse
  **zero** cases from this receipt. The summary line itself *does* match
  `round46_c3_verify.py:134`. The R55-C1 registry row for `round55-c3` must state the *actual*
  verdict map, which differs from every other probe row (they all say mismatches never affect the
  exit code; the draft exits 1 on a mismatch, `:179-183`).
* **D5 — the frozen case table lacks the instruction-requirement mapping the claims require.**
  Claims R55-C3 instrument bullet: "each mapped to one instruction requirement". The draft's
  `:54-79` is a list of plain tuples with no `Case` dataclass, no `TAGS` dict, no `violates=`
  per case and no `--dry` freeze receipt (the pattern's second freeze of the table).
* **D6 — bwrap flags differ in form** (draft `:100, 104-105, 108`: `--unshare-all`, no
  `--new-session`, extra `--tmpfs /home`), and the grader runs via an inline `-c` program
  (`:41-42`) rather than a bound harness file. Measured functional on this host (uid 1000 inside;
  the draft's battery reproduces all 12 predictions). Form-level, not effect-level.

**Verification actually run** (exit codes): the two `--dry` freeze receipts byte-equal to a fresh
`--dry` (0, 0); the draft's `--selftest` ⇒ `SELFTEST cases=2 failures=0`, exit 0; the draft's
battery ⇒ `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`, exit 0;
a flipped prediction ⇒ `mismatches=1`, exit 1 (a mismatch **is** counted); a forced SETUP case ⇒
`observed_pass=4 observed_fail=7 mismatches=0` + `SETUP cases=…`, exit 2; a pre-populated `--work`
⇒ deleted (D3); `--receipt` output byte-identical to stdout; `build_pmars_probe.py` with an
absent `--work` ⇒ `FileNotFoundError` traceback (pmars does not create `--work`); r45 with a
pre-populated `--work` ⇒ directory contents preserved.

**Not run / not checked (honest):** the two R55-C2 laundering fixtures;
`plans/round52_c2_registry.py`; any upstream fetch, benchmark or network call; no mutating git/jj
command anywhere. `plans/round55_c2_entryargv.py` did not exist when I read the tree early in this
seat; a sibling seat created it untracked at 12:38 (mtime) during the wave, so it is out of my
read set. I re-read only its CLI surface afterwards, to confirm the lane's counter CLI convention
(§4): `plans/round55_c2_entryargv.py:410-416` — `--lane` default `.`, `--source`, `--work`,
`--jobs` (default 3), `--timeout` (default 900), `--dry`, `--selftest` — which matches the
`--selftest`/`--work` counter convention described in §4. I did not run it.

**Files written:** `.ufo/waves/round-55/w1/SC4ProbePrior/pattern.md` (deliverable) and this file.
No lane file was edited; no sibling's file was touched. **Installs:** none. **Scratch:**
`/fast/scratch/hyaku/kengaku-r55/SC4ProbePrior/` — deleted before yielding.
