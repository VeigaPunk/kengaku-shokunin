# R33FControlFidelity — C2 frozen before-receipt fidelity vs reconstruction

Seat: leaf executor, round-33 falsify wave, 2026-10-25.
Target: C2 (calibration) frozen control `claims/defects-before.txt`.
Task: compare the frozen control to a reconstruction from the frozen lane commit + the
round-32 wave tree in a /tmp archive; determine whether all six pre-state defects reproduce
without live fleet report bytes; report any delta and why.

**VERDICT: partial catch (2 of 6 items are not lane-reproducible).** N1/N2/N5/N6
reproduce byte-exactly from committed lane bytes + the round-32 wave tree; N3 and N4 do
**not** — their frozen findings are functions of the *fleet repo's* report bytes, which
the lane archive does not contain. The count-6 result still prints in a fleet-less
environment, but with "unreadable" placeholder messages, not the frozen findings. The
control is a faithful record only as a **joint state**: lane@`f0b20ae` + wave-32 tree +
fleet@`3d3ca566^` (pre-erratum report bytes).

## 1. Reconstruction (all git commands on lane repos are read-only; all writes in /tmp)

- Sandbox: `/tmp/r33f-cf/recon2` (plus `recon`, `archive_only` for matrix runs).
- Lane bytes: `git -C <lane> archive f0b20ae -- SCORECARD.md corpus/lessons/round-30.md
  corpus/lessons/round-31.md plans/round33_defects.py .ufo/waves/round-32` extracted, then
  `git init` + `git add -A` + commit → tracked set == `f0b20ae` (5 wave-32 files).
- Wave-32 tree: `git archive c227e48 -- .ufo/waves/round-32` materialised as **untracked**
  files (84 copies, none overwriting the 5 tracked). Fidelity: all 89 files under
  `.ufo/waves/round-32` hash-match `c227e48` blob-for-blob (89/89, 0 mismatches); the 5
  tracked at `f0b20ae` are byte-identical to the same names at `c227e48` (verified per-file);
  live disk == `c227e48` (`git diff --stat c227e48 HEAD -- .ufo/waves/round-32` empty).
  Result: disk=89, tracked=5, untracked=84 — exactly the control's N1 precondition.
- Counter integrity: `f0b20ae:plans/round33_defects.py` sha256 == live
  `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`; selftest on archive
  bytes passes 14/14.

## 2. Run matrix (every run: `python3 <counter> --lane <recon>`)

| run | lane state | fleet bytes | `checks=` | defects | vs control lines 3–9 |
|---|---|---|---|---|---|
| RUN1 | recon, 84 untracked | live repaired | 6 | 4 (N1,N2,N5,N6) | N1/N2/N5/N6 **identical**; N3/N4 absent |
| RUN2 | archive_only (no `.git`) | live repaired | 6 | 4 | N1 **differs** (`git ls-files failed: fatal: not a git repository…`); N2/N5/N6 identical |
| RUN3 | recon | pre-erratum fixture (`3d3ca566^` bytes) | 6 | 6 | all 7 lines **identical** |
| RUN5 | clean recon2 | pre-erratum fixture | 6 | 6 | **byte-identical** (diff empty) |
| RUN4 | recon | fleet-none empty dir | 6 | 6 | N3/N4 differ: "`…/round-31/kengaku.md` is unreadable: the round-31 report cannot be checked" (placeholders) |
| selftest | archive bytes | synthetic fixtures | 14 | 0 | pass |
| adversarial A | recon, wave32 fully tracked | pre-erratum | 6 | 3 (N3,N4,N6) | N1 green as designed |
| adversarial B | recon2 + N2/N5 appends | pre-erratum | 6 | 3 (N3,N4,N6) | N2/N5 green as designed |

RUN5's seven stdout lines (six `DEFECT` lines + `checks=6 defects=6`) are byte-identical to
control lines 3–9; the control file additionally carries two `#` header lines and the
wrapper's `exit=1` line (full control sha256 `0e8cabd7…7af78`).

## 3. The delta and why

**Only 4 of 6 defects reproduce from the lane reconstruction alone.** N1/N2/N5/N6 are
pure lane-content checks and reproduce exactly (RUN1). **N3 and N4 are fleet-coupled by
construction**: `plans/round33_defects.py` hardcodes
`FLEET = Path("/home/vgpnk/Projects/shokunin")` and
`R31_REPORT = FLEET / ".ufo/reports/round-31/kengaku.md"`, `R32_REPORT = …/round-32/…`;
`--lane` redirects only the lane-local checks (N1/N2/N5/N6). N3 reads the round-31 fleet
report for `a44b5a8` ∞ `superseded`/`erratum` + `ae95fe0`; N4 reads the round-32 fleet
report for `112091c`.

Consequences, all measured:
- With the **live repaired fleet** (erratum commit `3d3ca566` appended), N3/N4 go green and
  the reconstruction prints `defects=4` — the count-6 control does not reproduce (RUN1).
- With **no fleet bytes at all**, the count still lands on 6, but N3/N4 fire
  "unreadable" placeholders — the frozen *findings* ("no appended erratum supersedes the
  a44b5a8 citation", "the round-32 report does not name the closure tip 112091c") are not
  reproduced; a count-matched run is not a reproduction (RUN4).
- N3/N4 reproduce only when the **pre-erratum fleet report bytes** are supplied
  (`git -C <fleet> show '3d3ca566^:.ufo/reports/round-31/kengaku.md'` → sha256
  `cf141d2c…60d71`; round-32 → `75ed1719…60cf`): RUN3/RUN5 byte-identical.
- N1 additionally needs a *reconstructed tracked state*: on an index-less `git archive`
  dump, `git ls-files` fails and N1 prints the git error instead of the 84-file finding
  (RUN2) — the archive alone cannot reproduce N1's message; a git-initialised
  reconstruction is required.

The counter's own selftest docstring names the hazard ("N3/N4 read absolute fleet paths by
default, which would couple the selftest to the live repair state") — the mitigation was
applied to the selftest only, not to the `--lane` path.

## 4. Verdict on the task question

"All six pre-state defects reproduce without live fleet report bytes": **false**. Four do;
N3/N4 are not lane-reproducible and require pre-erratum *fleet history* bytes (not live
working-tree bytes — the live files carry the repair). A reviewer re-running the archive
today sees 4 (or 6 with placeholders) and would misread it as a regression or a failed
reproduction unless told the joint-state precondition.

## 5. Evidence retained

- Sandbox: `/tmp/r33f-cf/` (recon, recon2, archive_only, wave32-full, fleetpre, fleetnone,
  variant/). Variants differ from frozen counter by exactly one line (`FLEET`), sha256
  `f4bf0444…` (`pre_fleet.py`), `fe884bdf…` (`none_fleet.py`); `FLEET`-line diff verified.
- Run logs: `/tmp/r33f-cf/run3.txt`, `run5.txt` (byte-identical stdout), `run4.txt`.
- Control: `claims/defects-before.txt` sha256 `0e8cabd7…7af78`.
- Lane commits: frozen `f0b20ae`, wave-32 inherit `c227e48`, repaired tip `7895588`;
  fleet erratum `3d3ca566` (parent = pre-erratum).

## 6. Risks / notes

- No lane/fleet file was modified; all git writes were inside `/tmp` sandboxes; no tools
  installed.
- The 84-count and 89-total are measured (`git ls-files` + `find`, both in sandbox and
  lane); no inference beyond what is labelled in §1.
- This seat's delta (N3/N4 coupling) matches the sibling build-seat finding
  `build/R33ExecDefsBefore.md` (RUN B/G/H), independently derived here via byte-identical
  reconstruction rather than the live lane.
