# ForgeScan — R68 wave 1: security scan of the two new instruments

Seat: `ForgeScan` (leaf, no dispatch). Date: 2026-11-03. Round: 68, wave 1.
Scope: `plans/round68_c1_pypi_finish.py` (sha256 `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc`)
and `plans/round68_c2_correction_gate.py` (sha256 `acda6c8a1ee3e6a29a01dbf5fa9576f076808e5cd0339a161eb35e22337ef7f9`),
both read in full; the base module `plans/round63_c1_pypi_probe.py` read for every function the
new probe imports. Read-only on L; all probes ran against **fake lane roots under
`/fast/scratch/hyaku/kengaku-r68/ForgeScan/`** (deleted before yielding). No instrument was
edited. No package was installed. **Port 8080 was never bound or contacted**: every probe used
`--check-receipt`, `--render-table`, `--selftest`, or the gate's `--root`/`--selftest`; the
battery (`run_battery`) was never invoked.

Verdict: the C1 checker implements the frozen strictness sentence it was given, and the C2 gate
implements E1–E5 as coded — but **one C1 kill rule is not instrumented (M-1)**, **C2's E1 does
not implement its frozen "exactly one" wording (M-2)**, and both instruments have
identity/refusal-path weaknesses that bound what their greens mean. Nothing found contradicts
the receipt of record's own bytes: the committed receipt, captures, server log and the three
sha bindings are mutually consistent, and `--check-receipt` on it re-derives `PREDICATE R68-C1
pass` (rc 0).

---

## 1. Trust boundary — stated explicitly (brief item 2 / s1)

**What the C1 checker authenticates:** the *consistency of bytes it can read*, not that a run
happened. Its inputs are the receipt text (any path), `plans/round68_c1_pypi_finish.py`,
`plans/round63_c1_pypi_probe.py`, `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`,
and every file under `<lane>/corpus/evidence/round68/pypi/` (receipt-relative paths are **not**
used: `lane_root()` at `:63` pins the evidence tree to the instrument's own repo). Every sha it
recomputes is recomputed from those files.

**A forger who can write `corpus/evidence/round68/pypi/` controls every hash the checker
checks.** Demonstrated end to end (never ran anything, never touched 8080):

```
# fake lane = byte copies of both instruments + the grader; evidence hand-written
$ python3 <fake>/plans/round68_c1_pypi_finish.py --check-receipt <fake>/corpus/evidence/round68/pypi/receipt.txt
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=ffffffffffff...
CHECK stored-predicate=pass derived=pass
PREDICATE R68-C1 pass
rc=0
```

The hand-written evidence was: four stderr captures (K1 "1 passed", K3 "AssertionError", K4
"Could not find a version", K2 the five pip retry lines with `host='localhost'`, `port=8080`,
`[Errno 111] Connection refused`), and a two-line `server-log.txt` containing
`GET /simple/vectorops/` and `GET /packages/vectorops-0.1.0-py3-none-any.whl`. Every
`stderr_sha256`, the server-log sha and the `PROBE` sha were computed from those bytes. No
wheel was built, no venv, no bwrap, no index, no PID.

**Does the checker's own-file `PROBE` hash limit this? No.** The `PROBE` line names the sha256
of a *public* file (`own_sha256()`, `:59`); it is unkeyed, self-referential and computable by
anyone who can read `plans/`. It buys exactly one thing: **tamper-evidence on the instrument** —
edit the probe after the receipt was written and `probe-sha` fails. It does not authenticate the
run, the receipt, or the evidence. `BASE-PROBE` and `GRADER` are the same kind of binding
(public constants, `:66–75`, `:252–258`).

**Consequence for the claim.** Named limitation (i) already discloses "cannot by itself prove
that the run happened"; the scan sharpens it: *no* file under the evidence dir is unforgeable,
so `battery-run.txt`, `server-log.txt` and the stderr captures are equally forgeable, and the
PIDs (`1323016`, `1367817`, `1369862`) are dead. The only non-forgeable witnesses would be a
signature/MAC with a key outside the tree, or an external record made by a different process
(e.g. the commit + a receipt sha quoted in `LOG.md` by the L1). Recommendation: the round report
should say "the committed bytes are mutually consistent and the instrument is byte-bound", not
"the run is proven", and the L1 should record the receipt's sha256 in the commit message /
`LOG.md` line so the receipt of record is at least pinned outside its own directory.

---

## 2. Findings

Severity: **M** = must fix before the claim is admitted; **S** = should fix (bounds what the
green means, not blocking); **N** = note.

### M-1 — C1 kill rule (c) is not instrumented; a hung K2/K3/K4 is scored `F` and the receipt passes
*Surface:* `plans/round68_c1_pypi_finish.py:37`, `:150`, `:169`; base `plans/round63_c1_pypi_probe.py:101,364–373,381–388`.

Frozen kill rule (c): "a case hangs past the 900 s bound → the probe exits 2 (could-not-evaluate),
the claim is not admitted, and no vector is inferred."

Observed:
* `LEG_TIMEOUT = 900` (`:37`) is **dead**: one occurrence in the file (the definition). The
  operative per-leg bound is the base module's `LEG_TIMEOUT = 180` (base `:101`), consumed by
  `m.run_leg` (base `:371`) and `m.pip_install_stderr` (base `:386`).
* On `subprocess.TimeoutExpired`, base `run_leg` returns `("F", "TimeoutExpired", "")`
  (base `:372–373`); the new probe never inspects `exc` and writes the capture from `out == ""`.
* `m.pip_install_stderr` (base `:381–388`) has **no** `TimeoutExpired` handler: a K2 pip hang is
  an uncaught exception → traceback, rc 1.
* Consequence, demonstrated: the checker **accepts** a receipt whose K3 leg timed out —
  `CASE K3 ... observed=F expected=F exception=TimeoutExpired stderr_sha256=e3b0c442…b855`
  (empty capture) → `CHECK ok cases=4`, `PREDICATE R68-C1 pass`, rc 0. K4 behaves identically;
  K2 too when the pip confirmation leg returns non-zero cleanly. Only K1 (expected `P`) catches
  a hang, and it does so as a vector mismatch (exit 1), not as could-not-evaluate.
  This refines sibling `ReceiptReview` O1 ("fail-closed either way"): for 3 of 4 cases it is
  **not** fail-closed — the timeout is the expected value.

*Impact:* a hung K2/K3/K4 yields a green receipt with an empty stderr capture and no
`SETUP`/exit-2 signal; kill rule (c) cannot fire. The receipt of record is unaffected (its
`exception=` values are `none`/`AssertionError`/`CalledProcessError`; no timeout occurred), so
the *scored verdict* stands — but the instrument as built does not implement the rule the claim
cites.

*Smallest remediation:* the instrument bytes are frozen by the receipt's `PROBE` line, so this
cannot be patched in place without invalidating the receipt. Either (a) re-freeze: give the new
probe its own leg wrapper that passes `timeout=900`, treats `TimeoutExpired` as
could-not-evaluate (exit 2, no receipt), and wraps the pip leg the same way, then re-run the
battery; or (b) declare it: add a dated amendment naming the effective 180 s bound and the
`F`-on-timeout mapping, and have the checker refuse `exception=TimeoutExpired` outright (that
too is a new instrument + new receipt). Until one of these lands, the round report must not say
the 900 s kill rule was in force.

### M-2 — C2 E1 does not implement "exactly one `## Erratum (round 68)` heading"
*Surface:* `plans/round68_c2_correction_gate.py:49–65` (`erratum_section` returns the first match and never counts).

Frozen E1: "`plans/round-67-claims.md` contains **exactly one** `## Erratum (round 68)`
heading, and the section names both …". The code finds the first heading and stops.

Observed (fake root, real claims + the erratum section appended twice):
```
$ python3 plans/round68_c2_correction_gate.py --root <fake-two-sections>
E1 ok section present, correct-sha=True, wrong-sha-named=True
... DEFECTS n=0 / PREDICATE R68-C2 pass / rc=0
```
Corroborated by sibling fixture `gate/clause-fixtures.txt` (`dup-heading` → `E1 ok`).

*Impact:* a duplicated or accidentally re-appended erratum section passes a check whose frozen
text forbids it; "append-only, exactly one" is unenforced.

*Smallest remediation:* count heading lines whose `strip()` equals the heading and require
`== 1` (`len(matches) != 1 → defect`), then re-run `--selftest` (the stripped fake still yields
one E1 defect, so the 5-defect expectation holds). No receipt binds the gate's bytes
(`corpus/evidence/round68/c2-green.txt` does not exist yet), so this can land before the green
run.

### S-1 — C1: a non-UTF-8 receipt crashes; rc 1 masquerades as a predicate miss
*Surface:* `:243` `path.read_text(encoding="utf-8")` with no handler.

```
$ python3 plans/round68_c1_pypi_finish.py --check-receipt <binary file>
rc=1  Traceback ... UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0
```
No `SETUP` line, no `PREDICATE` line, and rc 1 is the code the claims use for "predicate
failed" (the instrument's own map is 0 pass / 1 fail / 2 could-not-evaluate). A crash is
therefore indistinguishable from a miss to any wrapper that reads only the exit code.

*Remediation (next re-freeze):* `try: text = read_text(...) except (OSError, UnicodeDecodeError)
→ print("SETUP receipt-unreadable …"); return 2`. Directory and nonexistent receipt paths are
already typed (`SETUP receipt-missing`, rc 2) — verified.

### S-2 — C1: the `BASE-PROBE` binding's refusal path is a traceback, and `base-probe-bytes` is unreachable
*Surface:* `:78–84` (`mod_SetupError`), `:66–76` (`load_base_probe`), `:264`.

`mod_SetupError` does `_BASE.SetupError(msg)` with `except NameError`. At call time `_BASE` is
`None` (assigned `_BASE = None` after the function), so the guard never fires:

```
$ python3 <fake>/plans/round68_c1_pypi_finish.py --check-receipt <receipt>   # base probe tampered
rc=1  AttributeError: 'NoneType' object has no attribute 'SetupError'
$ ...                                                                        # base probe deleted
rc=1  FileNotFoundError: .../plans/round63_c1_pypi_probe.py
```
Both are the claim's stated binding ("byte-verified at run time — the `BASE-PROBE` binding")
failing as an unhandled crash with rc 1, and `main`'s `except RuntimeError` cannot catch either.
Second effect: because `main` loads the base module **before** `check_receipt`, and
`load_base_probe` refuses any digest ≠ the constant, the checker's `base-probe-bytes` defect
(`:264`) can never fire on the canonical path — a dead clause (see N-5).

*Remediation (next re-freeze):* make `load_base_probe` return a typed failure (`SETUP
base-probe-sha-mismatch`, exit 2) and drop or keep `base-probe-bytes` knowingly.

### S-3 — C1: a duplicate key *inside* one `CASE` line is last-wins
*Surface:* `:286–292` (`fields[key] = value`).

Demonstrated: `CASE K2 leg=test_api observed=P expected=F exception=CalledProcessError
observed=F index_pid=none …` → `CHECK ok`, `PREDICATE R68-C1 pass`, rc 0. The receipt's first,
visible `observed` value contradicts the one that is checked. Duplicate *lines* are refused
(`case-duplicate`), duplicate *keys* are not.

*Impact:* a receipt can be read as reporting `P` and be checked as `F`. Cheap to exploit by
accident (a hand-edited line) and by intent.

*Remediation (next re-freeze):* refuse a repeated key within a CASE line
(`defect("case-duplicate-field", name+":"+key)`).

### S-4 — C1: the `exception=` field is never validated
*Surface:* `:298–311` (only `observed`, `expected`, `leg` are compared).

`CASE K2 … observed=F expected=F exception=none …` → rc 0. The frozen receipt format names
`exception=CalledProcessError` for K2 and `AssertionError` for K3, and the whole point of the
round is that a `CalledProcessError` (install failed) differs from an `AssertionError` (wrong
math); the checker cannot tell them apart. Combined with M-1 it is what lets
`exception=TimeoutExpired` pass.

*Remediation (next re-freeze):* bind the frozen exception per case (allow `TimeoutExpired` only
as a defect).

### S-5 — C1: artifact identity is content-only — symlinked evidence and any receipt path pass
*Surface:* `sha256_file` = `Path.read_bytes()` (`:53–55`); evidence lookups use `lane / STDERR_DIR / f"{name}.txt"` with `is_file()` only (`:358–367`); `check_receipt` never compares `path` to `RECEIPT_PATH`.

Demonstrated: replacing `stderr/K3.txt` with a symlink to a file outside the tree →
`PREDICATE R68-C1 pass` (the checker hashes through the link; no `is_symlink` guard, no
`resolve()`-containment). And `--check-receipt <any path>` returns the same green as the
canonical receipt: nothing binds the checked text to `corpus/evidence/round68/pypi/receipt.txt`
or to a commit.

*Impact:* a committed symlink satisfies the checker locally while the evidence is not
self-contained for anyone else; a green on a scratch copy is indistinguishable from a green on
the receipt of record. (This is also the only place the brief's s2 surface has teeth: the
symlink *itself* gains nothing beyond the write access it requires — the write access is the
real boundary, §1 — but it defeats the "committed bytes" wording.)

Read-side path traversal is therefore limited to the receipt argument: `--check-receipt
/etc/hostname` reads outside the lane and returns typed defects (rc 1, no crash); every
evidence path is a constant joined to `lane_root()`, so `..` cannot redirect the evidence
lookup. The absence of a `resolve()`/containment check is what S-5's remediation adds.

*Remediation (next re-freeze):* refuse `p.is_symlink()` for every bound artifact, and print (or
assert) `path.resolve() == (lane/RECEIPT_PATH).resolve()` for the canonical run.

### S-6 — C1: `--evidence-dir` / `--receipt` are unnormalized and uncontained (write side)
*Surface:* `:103` (`evid = pathlib.Path(evidence_dir) if evidence_dir else lane / EVID_DIR`), `:106`/`:165–166`/`:194` (writes under `evid`), `:222–224` (receipt write). No `resolve()`, no `is_relative_to`, no check that `evid` is the lane's evidence dir.

Static finding (not executed — the battery binds 8080): a relative `--evidence-dir stderr` or
`--receipt out.txt` resolves against the process CWD, which for this fleet is the repo root
`/home/vgpnk/Projects/shokunin`; the run would then create `stderr/` (or `out.txt`) there. And a
*replication* run that omits `--evidence-dir` silently overwrites the committed evidence of
record (`evid` defaults to the lane), while a receipt written elsewhere would then bind
overwritten evidence.

*Remediation:* require absolute paths (or assert `evid` ∈ {`lane/EVID_DIR`, a path under
`--work`}) and refuse to write the lane evidence dir unless `--receipt` is also the canonical
one. Everything else about §7 hygiene is clean: the venv, stub, hosts file, `home`, tests dir
and every per-case dir come from `work` (`tempfile.mkdtemp(dir=str(work))`, `:139`); no `/tmp`
literal exists in either instrument; `--selftest` writes only `<work>/red/` (verified: the only
new paths under the work dir were `red/` and its five fixtures). The C2 gate writes nothing in
default mode and only `<work>/fake-lane` under `--selftest` (see N-9 for its residue and its
unchecked `--work`).

### S-7 — C2: the erratum section is fence/comment-blind (false red *and* false green)
*Surface:* `:49–65` — section = first line whose `strip()` equals the heading, until the next line starting `## `; no markdown awareness.

Demonstrated both directions:
* **False red:** a genuine erratum whose body contains a fenced snippet with a line starting
  `## ` (`## what the probe printed`) is truncated at that line → `E1 defect … correct-sha=False`,
  `E2 defect`, `E5 defect`, `DEFECTS n=3`. A scribe quoting probe output inside the erratum
  turns the gate red on a correct landing.
* **False green:** the same heading and all five required phrases inside a fenced code block →
  `E1..E5 ok`, `DEFECTS n=0`, rc 0.

*Remediation:* strip fenced blocks and `<!-- -->` comments before scanning (and before
section-boundary detection); require the erratum to be the last `## ` section in the file
(append-only), which also makes the "quoted text elsewhere" case impossible.

### S-8 — C2: E3 is substring presence only — a fabricated tally satisfies it
*Surface:* `:120–128`: `f"PROBE sha256={R67_PROBE_SHA}" in t`, `"SELFTEST" in t`, `"rc=" in t`.

Demonstrated: a two-line file (`PROBE sha256=0379…` + `SELFTEST green_rc=0 red_rc=1 rc=0`) →
`E3 ok`, gate green. Sibling fixture `gate/clause-fixtures.txt` (`loose-tally`, `XPROBE …` +
`NOTSELFTEST …`) passes for the same reason — the `in` checks are not line-anchored.

*Impact:* routed defect 3 ("self-test tally not committed") is satisfied by *any* file with the
right substrings, including one never produced by the probe. The correction's whole point is
that a quoted tally is not a committed one; the gate cannot tell a committed run from a pasted
line.

*Remediation:* anchor to the probe's own selftest grammar — require `^PROBE sha256=<sha>$`,
require every red-fixture `RED … rc=1 refused=True`-class line the probe emits, require the
aggregate `SELFTEST … ok=` line to parse and agree with the per-fixture lines, and require the
tally's sha256 to be recorded in the C2 green receipt.

### S-9 — C2: E4 breaks on the first line mentioning the sqlite probe
*Surface:* `:141–146` — `for ln in reg.splitlines(): if "round65-c1-sqlite-probe" in ln: strict_row = "--strict" in ln; break`.

Demonstrated: a registry section whose first mention is a change-note line ("the
`round65-c1-sqlite-probe` row was reworded this round") followed by the real row carrying
`--strict` → `E4 defect pipeline-row=True, sqlite-row-strict=False`. Symmetrically, a prose
line carrying `--strict` would satisfy E4 while the row itself lacked it.

*Remediation:* scan **all** lines mentioning the row name and require at least one that is a
table row (`ln.lstrip().startswith("|")`) and contains both the row name and `--strict`.

### Notes

* **N-1 — the forged-receipt boundary (§1) is a disclosed limitation, not a code bug.** Stated
  so the L1 does not re-derive it: the `PROBE` hash is not an authentication token. Recommend
  pinning the receipt's sha outside its own directory (commit message / `LOG.md`).
* **N-2 — dead write:** `stderr_dir = work / "stderr"` (`:117–118`) is created and never used;
  the per-case captures go to the evidence dir and K2's raw copy to `<work>/k2-pip-stderr.txt`.
* **N-3 — the K1 server log cannot distinguish K1's server from K3's.** In the scored run K1 and
  K3 served the identical request pair (`/simple/vectorops/`, `/packages/vectorops-0.1.0-py3-none-any.whl`;
  see `battery-run.txt` `SERVED` lines). The checker's log clause is a two-substring test, so the
  committed log proves *a* server answered those paths, not that the `P` leg drew from it. The
  "request-side proof" is a property of the run's structure (the same PID held the port), not of
  the committed bytes. The claims' wording ("the request-side proof that the leg's bytes came
  from this PID") should be read as structural, not byte-bound.
* **N-4 — `index_pid` is any non-`none` string** (`:315`): `index_pid=42` (or `abc`) passes. The
  frozen sentence says "not `none`", so this is as-written; it is not a PID proof.
* **N-5 — selftest coverage vs clause count:** the checker carries 25 literal defect names plus
  six per-case templates; the five red fixtures exercise five clauses (all-P vector, stale PROBE
  sha, duplicate CASE line, missing K2 clause, fabricated stderr sha). The clauses behind
  S-1/S-3/S-4 and the unreachable `base-probe-bytes` (S-2) have no fixture, so a vacuous clause
  would not be caught by `--selftest`.
* **N-6 — `red-before` `DEFECTS n=5` is no longer reproducible in-tree.** The tally landed at
  20:00 (`corpus/evidence/round68/r67-probe-selftest.txt`); a fresh
  `python3 plans/round68_c2_correction_gate.py` now reports `DEFECTS n=4` (E3 ok). The stored
  `.ufo/waves/round-68/w1/gate/red-before.txt` (19:54) is the only support for n=5, and the
  sibling `gate/red-after-concurrent-tally.txt` already records the n=4 state. This is a wave
  state change, **not** a kill-rule (a) event; the L1 should cite the stored receipt, not a
  fresh run, for the red-before count.
* **N-7 — the gate never checks the `a1-mutants.txt` landing.** The claims route defects 1, 2, 5
  to a dated `ERRATUM-68` append in `corpus/evidence/round67/pipe/a1-mutants.txt` (counting
  anchor `grep -c 'ERRATUM-68' → 1`), but E1–E5 never open that file (`A1_MUTANTS` is used only
  in `--selftest`'s fake-tree copy). Frozen E1–E5 do not include it, so this is as-written; the
  anchor remains a manual command.
* **N-8 — `--check-receipt` ignores `--lane`** (`lane_root()` at `:63`): the evidence tree is
  pinned to the instrument's own repo. Strength: evidence cannot be redirected by an argument.
  Limitation: a replication run's receipt cannot be checked against its own scratch tree.
* **N-9 — gate scratch residue:** `--selftest` leaves `<work>/fake-lane` behind (verified) and
  `shutil.rmtree(fake)` (`:172`) runs blindly on the next invocation with no containment
  assertion on `--work` (`--work /` would remove `/fake-lane`). Cosmetic under the seat rules;
  worth a guard if the gate ever runs unattended.
* **N-10 — correction to sibling `ReceiptReview` O4:** the claimed "degenerate `CASE` line with
  no name token would crash the parser (IndexError)" does **not** reproduce on Python 3.14.8.
  Lines `CASE`, `CASE \u00a0`, `CASE \u200b`, `CASE \x00`, `CASE\tK1` all behaved typed: the
  first two are stripped to `CASE` (no `"CASE "` prefix → not parsed, ignored); the last three
  either parse to an unknown case name (`case-unknown` defect, rc 1) or are ignored. No
  `IndexError`. The real tolerance is the opposite of the reviewer's claim — a bare `CASE` line
  is silently ignored rather than refused. O1, O2, O3 and O5 reproduce as stated.

---

## 3. Reproduction

All commands below run against scratch only and never bind 8080. `$L` = the lane,
`$S` = `/fast/scratch/hyaku/kengaku-r68/ForgeScan`.

```bash
mkdir -p "$S/forge/plans" "$S/forge/corpus/evidence/round68/pypi/stderr" \
         "$S/forge/corpus/evidence/round52/graders/pypi-server/tests"
cp "$L/plans/round68_c1_pypi_finish.py" "$L/plans/round63_c1_pypi_probe.py" "$S/forge/plans/"
cp "$L/corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py" \
   "$S/forge/corpus/evidence/round52/graders/pypi-server/tests/"
```

then the driver in `Appendix` writes the forged evidence + receipt and runs every variant. The
key one-liners:

| finding | command (after the appendix driver) |
|---|---|
| §1 / N-1 | `python3 $S/forge/plans/round68_c1_pypi_finish.py --check-receipt $S/forge/corpus/evidence/round68/pypi/receipt.txt` → pass, rc 0 |
| M-1 | driver step `hung-k3` → `PREDICATE R68-C1 pass`, rc 0 |
| S-1 | `python3 $L/plans/round68_c1_pypi_finish.py --check-receipt $S/binary.bin` → traceback, rc 1 |
| S-2 | driver step `base-probe-tampered` → `AttributeError`, rc 1; deleting the base probe gives `FileNotFoundError`, rc 1 |
| S-3 | driver step `dup-key` → pass |
| S-4 | driver step `exception-lie` → pass |
| S-5 | driver step `symlink` → pass |
| M-2 | `python3 $L/plans/round68_c2_correction_gate.py --root $S/gate-dup` → `DEFECTS n=0` |
| S-7 | `--root $S/gate-trunc` → `DEFECTS n=3`; `--root $S/gate-fenced` → `DEFECTS n=0` |
| S-8 | `--root` a root whose tally is two lines → `E3 ok` |
| S-9 | `--root $S/gate-e4-firstline` → `E4 defect … sqlite-row-strict=False` |

Baseline on the real lane (read-only): `--check-receipt corpus/evidence/round68/pypi/receipt.txt`
→ `PREDICATE R68-C1 pass`, rc 0; `--render-table` → `FROZEN-VECTOR P/F/F/F`,
`DERIVED-VECTOR P/F/F/F`; `python3 plans/round68_c2_correction_gate.py` → `DEFECTS n=4` (see N-6).

## Appendix — driver (writes only under `$S`)

Verified driver (run end to end before this report was written; printed rcs in the comments):

```python
import hashlib, pathlib, shutil, subprocess
L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r68/ForgeScan"); F = S/"forge"
shutil.rmtree(F, ignore_errors=True)
for d in ("plans", "corpus/evidence/round68/pypi/stderr",
          "corpus/evidence/round52/graders/pypi-server/tests"):
    (F/d).mkdir(parents=True)
for rel in ("plans/round68_c1_pypi_finish.py", "plans/round63_c1_pypi_probe.py",
            "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"):
    shutil.copyfile(L/rel, F/rel)
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
ev = F/"corpus/evidence/round68/pypi"
fake = {"K1": b"1 passed\n", "K3": b"E   AssertionError: assert 15 == 14\n",
        "K4": b"ERROR: Could not find a version that satisfies the requirement vectorops==0.1.0\n",
        "K2": b"WARNING: Retrying after connection broken by 'NewConnectionError(\"HTTPConnection("
              b"host='localhost', port=8080): Failed to establish a new connection: "
              b"[Errno 111] Connection refused\")'\n"}
for n, b in fake.items(): (ev/"stderr"/f"{n}.txt").write_bytes(b)
(ev/"server-log.txt").write_bytes(
    b'127.0.0.1 - - [x] "GET /simple/vectorops/ HTTP/1.1" 200 -\n'
    b'127.0.0.1 - - [x] "GET /packages/vectorops-0.1.0-py3-none-any.whl HTTP/1.1" 200 -\n')
ss = {n: sha(ev/"stderr"/f"{n}.txt") for n in fake}
r = f"""PROBE sha256={sha(F/'plans/round68_c1_pypi_finish.py')}
BASE-PROBE sha256=2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929
GRADER sha256=82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=42 wheel_sha256={ 'f'*64 } stderr_sha256={ss['K1']}
CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=none wheel_sha256=none stderr_sha256={ss['K2']}
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=42 wheel_sha256={ 'f'*64 } stderr_sha256={ss['K3']}
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=42 wheel_sha256={ 'f'*64 } stderr_sha256={ss['K4']}
K1 server-log sha256={sha(ev/'server-log.txt')} served_simple=True served_wheel=True
K2 stderr-names-endpoint=True
CLASS network-service executed=2
PREDICTION-VECTOR P/F/F/F derived=P/F/F/F
PREDICATE R68-C1 pass
CLASS-PROBE-EXIT=0
"""
(ev/"receipt.txt").write_text(r)
cli = str(F/"plans/round68_c1_pypi_finish.py")
run = lambda p: subprocess.run(["python3", cli, "--check-receipt", str(p)],
                               capture_output=True, text=True)
print("forged-green", run(ev/"receipt.txt").returncode)                 # 0
(S/"dup-key.txt").write_text(r.replace("CASE K2 leg=test_api observed=F",
                                       "CASE K2 leg=test_api observed=P", 1)
                              .replace("expected=F exception=CalledProcessError",
                                       "expected=F exception=CalledProcessError observed=F", 1))
print("dup-key", run(S/"dup-key.txt").returncode)                       # 0
(S/"exception-lie.txt").write_text(r.replace(
    "CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError",
    "CASE K2 leg=test_api observed=F expected=F exception=none", 1))
print("exception-lie", run(S/"exception-lie.txt").returncode)           # 0
(S/"extra-field.txt").write_text(r.replace("CASE K1 leg=test_api", "CASE K1 leg=test_api note=x", 1))
print("extra-field", run(S/"extra-field.txt").returncode)               # 0
out = S/"outside-K3.txt"; shutil.copyfile(ev/"stderr/K3.txt", out)
(ev/"stderr/K3.txt").unlink(); (ev/"stderr/K3.txt").symlink_to(out)
print("symlink", run(ev/"receipt.txt").returncode)                      # 0
(ev/"stderr/K3.txt").unlink(); shutil.copyfile(out, ev/"stderr/K3.txt")
empty = hashlib.sha256(b"").hexdigest(); (ev/"stderr/K3.txt").write_bytes(b"")
hung = [f"CASE K3 leg=test_api observed=F expected=F exception=TimeoutExpired index_pid=42 "
        f"wheel_sha256={'f'*64} stderr_sha256={empty}" if ln.startswith("CASE K3 ") else ln
        for ln in r.splitlines()]
(S/"hung-k3.txt").write_text("\n".join(hung) + "\n")
print("hung-k3", run(S/"hung-k3.txt").returncode)                       # 0  (M-1)
(S/"binary.bin").write_bytes(b"\xff\xfe\x00\x80")
print("binary", run(S/"binary.bin").returncode)                         # 1  (traceback, S-1)
F2 = S/"forge-tampered"; shutil.rmtree(F2, ignore_errors=True); shutil.copytree(F, F2)
with open(F2/"plans/round63_c1_pypi_probe.py", "a") as fh: fh.write("\n# tamper\n")
r2 = subprocess.run(["python3", str(F2/"plans/round68_c1_pypi_finish.py"), "--check-receipt",
                     str(F2/"corpus/evidence/round68/pypi/receipt.txt")], capture_output=True, text=True)
print("base-probe-tampered", r2.returncode, r2.stderr.strip().splitlines()[-1])  # 1 AttributeError
```

Gate fixtures (each a minimal lane-shaped root; real `round67_c1_pipeline_probe.py`, a
hand-written SKILL with the `## Gate/probe registry (PROTOCOL §Gate standard)` heading and two
rows, a two-line tally, and the claims doc + one of: an erratum inside a fence, two erratum
sections, an erratum with a fenced `## ` line, or a prose mention before the sqlite row) were
built the same way and run with `--root`; outputs are quoted in S-7/S-8/S-9/M-2.

---

SCAN must-fix=2 should-fix=9
