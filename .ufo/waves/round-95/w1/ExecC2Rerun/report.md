# ExecC2Rerun: R95-C2 independent re-measurement and held-out forgery extension

Lane tip T: `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`. Clone: `git clone --shared` then detached at T, under
`/fast/scratch/hyaku/kengaku-r95/ExecC2Rerun/lane` (removed before yield). No lane mutation, no subagents, no
commit/push, no fleet-root write. Gate v2 bytes at T hash to `8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de`
(the frozen table value).

## 1. Census re-measurement: reproduces

Command (cwd = clone): `python3 "$S/lane/plans/round95_false_gate_census.py" --lane "$S/lane" --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 --work "$S/w"`
Receipt: `census-rerun.txt`.

- 14 `GATE` lines, each `passes=0 designated_red=1`.
- `HONEST TOOL plans/round94_freeze_integrity.py@afe9c229e37a sha256=8574b4d5...`; `HONEST W1..W5 pass`; `TARGET legs_passed=5 of 5`.
- `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc 0.

The census reproduces the frozen predicate exactly. Under shared CPU load it took about 17 minutes.

## 2. Held-out forgeries: five false gates, each with a demonstrated wrong verdict

Generator: `forgeries/make_forgeries.py` (exact single-occurrence edits, asserted). Each variant has a unified diff against v2 in `forgeries/<id>.diff`. Variants are built from v2 bytes at T.
Input demonstrations: `demo_inputs.py` → `demo-inputs-receipt.txt` (six inputs x seven gates, rc and verdict lines printed).
Counter runs: `counters/<id>.txt`, each `python3 "$S/lane/plans/round95_c2_counter.py" --lane "$S/lane" --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 --work "$S/w/cnt-<id>" --tool-file "$W/forgeries/<id>.py"`.

| id | diff vs v2 | designed input (wrong verdict) | v2 verdict | variant verdict | counter result |
|---|---|---|---|---|---|
| g1-mode-only-invisible | `touched` = count of rev-list commits whose `git show --numstat` has a non-`0 0` line | I1 chmod-only after freeze | rc 1, `broken:touched-after-freeze=1` | rc 0, `intact`, touched=0 | **W1..W5 pass, PREDICATE pass (missed 5/5)** |
| g2-dot-row-dropped | `table = [... if not p.startswith(".")]` before the row loop | I2 `.probe.py` edited next to `probe.py` | rc 1, `broken` on `.probe.py` | rc 0, `instruments=1` (`.probe.py` dropped) | **pass 5/5 (missed)** |
| g3-ancestry-path | `rev-list --full-history --ancestry-path f..t` | I3 side branch forked before the freeze, its probe.py edit merged after the freeze with `-s ours` | rc 1, `touched-after-freeze=2` | rc 0, `intact`, touched=0 | **W1 pass, W2 pass (20/20), W3 FAIL, W5 FAIL (K5 survived), rc 1; caught only by non-designated legs** |
| g4-gitlink-row-skipped | row skipped when `git ls-tree f -- p` starts `160000 commit` | I4 submodule pointer bumped after freeze | rc 1 | rc 0, `instruments=1` | **pass 5/5 (missed)** |
| g5-nonascii-row-skipped | row skipped when `not p.isascii()` | I6 `probé.py` edited after freeze | rc 1 | rc 0, `instruments=1` | **pass 5/5 (missed)** |
| e5-crlf-equivalent (control, not counted) | CR-tolerant `ROW.match(line)` before strip | I1..I6 all identical to v2 | — | identical rc on every input | pass 5/5 (expected: equivalent) |

The first g5 design (CR-tolerant skipping) was discarded before any run as **equivalent**: `parse_table` iterates `text.splitlines()`, which strips `\r`, so the branch is unreachable. It is kept as e5 to show the equivalence, and is not counted as a false gate.

**Held-out discrimination.** Of the five false gates, **four pass the round-95 counter 5/5** (g1, g2, g4, g5). The fifth, g3, fails the counter, but not at the leg its wrong verdict lives on:

- W2 (twenty fixtures) contains no pre-freeze side branch, and g3 passes W2 20/20.
- g3 is failed by W3 probe P1 (`--full-history` removed from the gate). The battery stays green because the ancestry path still counts the post-freeze side branch, so the battery's probe sensitivity is what fails g3.
- g3 is failed by W5 K5: the no-full-history mutant of g3 is still correct on the treesame fixture, so its designated W2 leg does not turn red.

So the counter's catch of g3 is a probe-sensitivity artefact, not coverage of the pre-freeze input. The claim's declared in-sample scope (14 of 14 killed) is confirmed; it does not extend to held-out forgeries. The census is 14 → 0 in-sample only.

Not built (named in the brief, not done): a forged battery that runs only when anchors are elsewhere; a claims table inside an HTML comment or indented code; trailing-slash rows; a symlink-following variant.

## 3. Unmodified gate v2: wrong verdicts without any forgery

These use the frozen v2 bytes at T unchanged (`native_inputs.py` → `native-inputs-receipt.txt`).

- **N1 refs/replace (major, verdict flip).** An edited `probe.py` commit is replaced by a commit whose tree restores the frozen bytes (`git replace <edited> <fake>`). `git show <edited>:probe.py` prints the frozen bytes. Gate v2 returns `rc=0`, `INSTRUMENT probe.py ... touched=0 verdict=intact`, `PREDICATE freeze-integrity pass` on a changed instrument. The counter cannot see this (no replace ref in any fixture). Route to round 96: pass `--no-replace-objects` (or set `GIT_NO_REPLACE_OBJECTS=1`) on every git call. Not repaired in round.
- **N2 symlink (major; policy-dependent).** `alias.py` is a symlink to `probe.py`. The table hashes the link text (`sha256("probe.py")`). After the freeze, only the followed target changes. `ls-tree` shows `120000 blob` at the rev with no touch. Gate v2 returns `rc=0`, `intact`, `PREDICATE pass`. Whether a followed symlink is the instrument is a policy question (this is [INFERENCE] about intent), but the verdict flip is observed. Route to round 96.
- **N3 gitlink (minor, fail-closed).** An unchanged submodule pin is listed. v2 reports `broken:freeze-bytes-differ-from-table+absent-at-rev` (freeze=absent). Gitlinks cannot be represented; no false intact, but every gitlink row is a false broken.
- **Tag object as `--rev` (no defect).** `tag_input.py` → `tag-input-receipt.txt`. T1 (annotated tag on an edited commit) gives rc 1, `broken:touched-after-freeze=1`. T2 (annotated tag on the freeze commit) gives rc 0, `intact`. Verdicts are correct. The `rev_is_tag_object=` diagnostic printed by my driver is mis-computed and ignored; the header line showing tag ≠ commit is correct.
- **Raw tag through `git show <tag>:path`** returns rc 0 (checked ad hoc, not receipted; not needed for any verdict).

## 4. Tool installs and host changes

None. No tool was installed or upgraded. No pacman, no sysctl change, no `~/.local/bin` write. No bwrap used. Passwordless sudo was not used.

## 5. Scope boundary

This item covers C2 re-measurement and held-out forgeries only. The C1 replay re-measurement, legacy/harm gates, sources and overlap belong to peer seats (ExecC1Rerun-3, ExecLegacyHarm and the scribe seats). I did not run them. The open L0 questions in `.ufo/l0-questions.md` were not touched.

## Receipts (all under this directory)

- `census-rerun.txt`: census at T (14/14 designated red, honest pass).
- `forgeries/`: `make_forgeries.py`, `g1..g5` and `e5` sources, `*.diff` against v2.
- `demo-inputs-receipt.txt`: I1..I6 x (v2, g1..g5, e5).
- `counters/*.txt`: counter output per variant (`PREDICATE` and legs).
- `native-inputs-receipt.txt`: N1..N3 under unmodified v2.
- `tag-input-receipt.txt`: T1, T2.
- Drivers: `demo_inputs.py`, `native_inputs.py`, `tag_input.py`, `forgeries/make_forgeries.py`.
