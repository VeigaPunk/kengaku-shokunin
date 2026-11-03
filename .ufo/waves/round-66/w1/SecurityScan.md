# SecurityScan — R66 w1 report

Scope: adversarial security review of the R66 C1 tensor probe, its five cases, the proposed
registry counter, and the install channel recorded in `plans/round-66-claims.md`.
Full evidence, line citations and remediation per finding: `SecurityScan/findings.md` (same dir).

Read-only seat: **no lane file was edited**; no frozen fact, predicate, counter, kill rule or case
file was touched. All experiments ran in scratch (`/fast/scratch/hyaku/kengaku-r66/SecurityScan`,
removed on exit) and in throwaway `bwrap` sandboxes. No tool was installed.

## Key lines

1. **M-1 must-fix** — `check_receipt` accepts a hand-written receipt: with only `GRADER`+`PROBE`+five
   frozen `VECTOR` lines and **no `CASE` line and no junit file**, `--check-receipt` printed
   `CHECK ok cases=5 / PREDICATE R66-C1 pass`, exit 0. With a self-authored sibling `junit/` whose
   every testcase carries `<failure message="fabricated"/>` — bytes contradicting the claimed all-P
   vector — it also printed `CHECK ok cases=5 / PREDICATE R66-C1 pass`, exit 0. Cause: probe 240–277
   never requires a `CASE` line (261–273 loops over lines that happen to be present) and never
   re-derives the vector from junit XML; `cases=5` at 281 is a hardcoded literal. **The C1 counter
   has the same fabricated-receipt hole R66-C2 exists to fix in R65**; the claims' line 55 call the
   C1 junit binding "the stronger check" — forge D shows it is only self-consistency.
2. **M-2 should-fix** — `check_receipt` never re-hashes the grader: pointed at a tampered grader
   (sha `3de1539b…` vs pinned `4ae4285e…`) it returned `ok: True problems: []`. Only `cmd_run`
   re-hashes (202).
3. **M-3 should-fix** — malformed receipts crash with no `PREDICATE` line: unknown case id →
   `KeyError: 'S999'`; token without `=` → `ValueError … length 1`; token with two `=` →
   `ValueError … length 3`. A crash is not a named finding and not a verdict.
4. **M-4 should-fix** — the `bwrap` argv (140–162) has **no `--unshare-net`**: from inside the
   sandbox, `connect(('1.1.1.1',443))` succeeded (`OUTBOUND INTERNET OK`), the host's `/proc/net/route`
   and 788 host PIDs were visible, a sandbox listener appeared in the host's `ss -ltn`, and the host
   connected to it. The grader's gloo rendezvous (`MASTER_PORT=12355`, grader 30–34) is therefore a
   **host** socket. Fix is viable: under `--unshare-net` a bind/listen/connect on `127.0.0.1:12355`
   succeeded while outbound gave `Network is unreachable`.
5. **M-5 should-fix** — no `--unshare-pid`: `os.kill(<host pid>, SIGTERM)` from inside the sandbox
   **killed the host process**; `/proc/<pid>/cmdline` of a host `llama-server` was readable.
6. **M-6 note** — `cmd_run` copies junit to `receipt.parent/"junit"` (221–223); for the canonical
   receipt path that **is** the git-tracked `corpus/evidence/round66/tensor/junit/`, so the
   post-freeze run replaced committed bytes (freeze `9a07df6a` vs HEAD hold different blobs for all
   five). Consequence: the named control of record `prefreeze-run2.txt` no longer verifies against
   the working tree (5× `junit_sha does not match committed junit bytes`); it verifies against the
   frozen commit (`git cat-file 9a07df6a:…/junit/k1-ref.xml` → `9c02c97350d88956…` = the control's
   own claim). The claims' line-33 harness-fix note holds only for a receipt outside the committed tree.
7. **M-7/M-8 note** — junit bytes resolved from a caller-controlled dir (270); unvalidated case id → `KeyError`.
8. **M-9 clean** — the five case dirs hold only `parallel_linear.py`; grep for
   `open(|socket|subprocess|os\.|urllib|requests|exec|eval|__import__|Path\(` across all four
   returns **no matches**; K4/K5 differ from K1 by exactly one method body each.
9. **M-10 clean** — bind list and modes enumerated (ro: `/usr`, `/etc`, venv, case dir, grader; rw:
   `/ctl` only). From inside the sandbox: `~/.ssh`, `~/.config`, `~/.omp`, `/root` absent;
   `/etc/shadow` and every host `/proc/*/environ` → `PermissionError`; the lock file is not visible.
   The venv is `--ro-bind` (150) and writes to it raise `OSError` → **not writable by a case**.
10. **M-11 clean** — only `bwrap` is spawned (no `shell=True`); no credential path read; lock is the
    operator-specified `~/.local/share/kengaku-r66/port-12355.lock` (`flock(LOCK_EX)`, 207–208).
11. **M-12 note** — `TORCH version=2.15.0+cpu` in the receipt is the hardcoded constant (58), never measured.
12. **M-13 note** — registry counter path refusal **works**: `corpus/SOURCES.md`, `/etc/passwd`,
    `../../../../etc/hostname`, `corpus/evidence/../../../etc/hosts` and a planted symlink
    `corpus/evidence/link.xml → /etc/passwd` were each refused (`refused capture outside
    corpus/evidence/`, exit 1); selftest 13/13 exit 0. Loose: an id↔capture mismatch
    (`QUOTE S183` pointing at S234's capture) is accepted; the red/ fixture
    `corpus/evidence/round66/red/fabricated-r65.txt` is an eligible capture; the needle is a raw
    byte-substring, not line-anchored (a fragment and a line-spanning needle both pass).
13. **M-14 note** — install channel verified on disk: `uv 0.13.0`, `pyvenv.cfg` `uv = 0.13.0`,
    `torch 2.15.0+cpu`, `pytest 9.2.0`; no `pip.conf`/`.netrc`/token files in the venv;
    `transformers 5.22.1` is installed but the pinned grader imports only
    `pytest/torch/dist/mp/nn` — harmless, but unnecessary venv surface.
14. **M-15 note** — `resume_continuity_v1` does not occur anywhere in the R66 surface (only in
    `corpus/evidence/round13-coverage/r13-planner.md`), so no zero-mutation obligation applies to
    these artifacts. The nearest analogue I verified directly: three `--check-receipt` runs left all
    18 files under `corpus/evidence/round66/` byte-identical (sha256 manifest diff empty) and
    `git status --porcelain corpus/ plans/` is empty — the check path writes nothing.

## Smallest remediations (for the L1; I did not edit anything)

- `check_receipt`: require one `CASE` line per case; re-derive each vector by parsing the
  **committed** junit XML (same rule as `run_case` 168–176) and require it to equal both the
  receipt's `VECTOR` line and the frozen table; resolve junit against `JUNIT_DIR` (55), not
  `receipt.parent`; re-hash `GRADER`; wrap parsing in try/except → `CHECK defect:` findings;
  replace the hardcoded `cases=5` (281) with the observed count; add a refused fixture whose junit
  contradicts its vector.
- `run_case`: add `--unshare-net` and `--unshare-pid` to the `bwrap` argv (140–162) — verified
  `--unshare-net` keeps the grader's loopback rendezvous working while cutting egress.
- `cmd_run`: keep the run's junit output out of the committed `corpus/evidence/round66/tensor/junit/`
  (e.g. receipt-local output dir) so a re-run cannot replace committed evidence; and record the
  venv's observed `torch.__version__` instead of the constant at line 58.
- registry counter: bind the capture to the registry row for the quoted id; exclude `red/` from
  capture eligibility; require the needle to match on a single line.

## Rule observation (not edited)

The round's C2 predicate names "the C1 probe's per-case junit binding" as the stronger gate
(claims line 55). M-1/M-7 show that binding is optional and self-referential, so C2's strict mode
remains the only strict gate in this round. C2 itself behaves as specified: against
`corpus/evidence/round66/red/fabricated-r65.txt` the proposed `--strict` exits 1 with named
findings; against the committed `corpus/evidence/round65/sqlite-gcov-probe.txt` it exits 0; the
default invocation still prints `PREDICATE R65-C1 pass`, exit 0 (unchanged, as required).

## Deliverables

- `kengaku-shokunin/.ufo/waves/round-66/w1/SecurityScan/findings.md` (full findings, 15 items)
- `kengaku-shokunin/.ufo/waves/round-66/w1/SecurityScan.md` (this trailer)

Installs: none (nothing needed installing). Scratch removed on exit.
