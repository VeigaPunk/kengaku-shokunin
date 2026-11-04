# ReceiptReview — R69-C1 `check_receipt` clause review + forgery families

Seat: ReceiptReview-2 · round-69 w1 · 2026-11-03 · leaf (no dispatch, no labrat)

Reviewed bytes: `plans/round69_c1_nginx_probe.py` working tree, sha256
`66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea`.
Read-only git: the file does not exist at `a518980e` (pre-freeze base); it was **added by the
freeze commit itself** `b288e8e0`, and `git show b288e8e0:plans/round69_c1_nginx_probe.py | sha256sum`
= `66b5128d…` = working tree, `git status --porcelain` on it clean. So the reviewed checker is
exactly the frozen instrument. Grader file re-hashed now:
`045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` (= SHA256SUMS line 111, = frozen pin). ✔

No `lsp` device is present in this session's tool inventory; this review is by direct source
reading plus execution of the checker (recorded per the reviewer protocol as text-level, not
semantic-LSP, evidence).

## 1. Clause table (frozen sentence → checker)

Frozen sentence: *"Each of the five frozen cases yields its frozen eight-leg vector, every one
of the eight grader legs is observed `P` in at least one case and `F` in at least one case, and
the receipt's PROBE and GRADER sha256 equal the committed bytes; the counter then prints
`PREDICATE R69-C1 pass` and exits 0."*

| # | Clause | Implementing lines | Status |
|---|---|---|---|
| 1 | five cases yield frozen eight-leg vectors | `vector-mismatch` L536, `vector-agree` L537-538, `leg-set` L540-541, `leg-vector` L542-544, `leg-missing` L551, `case-set` L525-526 | **Partly effective** — logic present and correct, but unreachable for battery-written receipts because the VECTOR input contract is broken (**M-A**) |
| 2 | every leg P in ≥1 case and F in ≥1 case | `seen_p`/`seen_f` tally L545-552, `leg-coverage` defect L553-554 | **Implemented but self-contradictory** — unsatisfiable against the frozen case table (**M-B**) |
| 3 | PROBE sha256 equals committed bytes | L493-497 vs `own_sha256()` L238-239 | **Partly** — binds the *working-tree* bytes at `__file__`, not the git commit; equivalent only while the tree is clean (clean today, verified) (**M-J**) |
| 4 | GRADER sha256 equals committed bytes | L498-506 vs frozen constant `GRADER_SHA256` (+pin substring L505-506) | **Partly** — constant comparison only; `check_receipt` never re-hashes the grader file (only `run_battery` SETUP does, L405-408) (**M-K**) |
| 5 | prints `PREDICATE R69-C1 pass`, exits 0 | L563-568 | Implemented faithfully, but unreachable in practice given 1–2 (all 13 executed receipts returned rc 1) |

## 2. Findings (by severity)

**M-A · P0 — writer/parser VECTOR token-count mismatch: the checker refuses every receipt the
battery can write.** `run_battery` L460-461 emits
`VECTOR {id} {vector} expected {expected} agree={agree}` = **6 whitespace tokens**;
`check_receipt` L512-516 requires exactly **5** tokens (`len(parts) != 5 → defect("vector-line")`,
`continue`). No line the writer can produce passes the parser; with every VECTOR line defecting,
`vectors` stays empty → `case-set` defect, the per-case loop `continue`s before any per-case
check, and all 8 `leg-coverage` tallies read p=0 f=0. Evidence: F1 (byte-faithful writer-format
green receipt, sha256 `ad298d169ed190583240e89adfcc991e93cc96f6a31dc96ab4d126a180a1e22b`) →
`DEFECT vector-line` ×5, `DEFECT case-set`, `DEFECT leg-coverage` ×8, `PREDICATE R69-C1 fail`, rc 1.
Consequence: when the C1 battery runs, its own receipt fails `--check-receipt` → kill rule
("a `--check-receipt` defect list that is nonempty") fires on a genuine run.

**M-B · P0 — the frozen case table cannot satisfy the frozen coverage clause (claim-level
double-bind).** The five frozen vectors carry only **6** F's: K2 leg3, K3 legs7+8, K4 leg6,
K5 legs1+5. Legs **2 `test_nginx_running`** and **4 `test_custom_404_page`** are `P` in all five
cases — no red witness exists for them. The claims doc's "Each of the eight legs has one red
witness and four green witnesses by construction" is arithmetically false (6 reds ≠ 8 legs; its
own parenthetical concedes un-red legs leave legs unpriced). Effects, all empirical:
(a) a perfect, internally-consistent receipt (F2, parser-shape, sha256
`ee36c9328892806b0222dc39ce34e3c67553a83d6fc72de6b753a711afa31ae8`) is refused with exactly
`DEFECT leg-coverage test_nginx_running p=5 f=0` and `DEFECT leg-coverage test_custom_404_page p=5 f=0`;
(b) `run_battery`'s own `ok` (L465) requires `full_f == 8`; a perfectly faithful run yields
`full_f=6` → the battery itself writes `PREDICATE R69-C1 fail` and exits 1 (and a `fail`-suffixed
receipt would *also* defect `stored-predicate` at check time);
(c) the double-bind is provable: F12 (sha256
`7e1db5f945ccb2af69fe91dc2a73af13fd32f5b7bd2ec2a611d43163b2c8f009`) gives K1 an F at legs 2 and 4
with matching TEST lines — `seen_p=8 seen_f=8`, but `DEFECT vector-mismatch K1 PFPFPPPP != PPPPPPPP`.
Clauses 1 and 2 are jointly unsatisfiable: no receipt can pass. Per the freeze paragraph this is
an error found before any after-receipt is scored — it needs an honest miss or a dated amendment
(case table must gain two red witnesses, e.g. a case with service down and one with 404 body
wrong, or the coverage clause must be scoped to the six priced legs). **I did not edit any lane
file.**

**M-C · P1 — the C1 selftest is vacuous as frozen.** `run_selftest`'s `body()` uses the same
6-token VECTOR f-string (L602), so all five red fixtures die in the M-A parse collapse before
their intended defect classes are reached. Defect-kind profiles (from `--check-receipt` on the
fixtures `--selftest` writes):
- r1-all-p: `case-set ×1, leg-coverage ×8 (p=0 f=0), vector-line ×5` — the *intended*
  leg-coverage-content defect never fires;
- r3-leg-vector: same profile — intended `vector-mismatch`/`leg-vector` never fire;
- r4-missing-leg: same profile — intended `leg-set`/`leg-missing` never fire;
- r2-probe-sha, r5-grader-sha: fire their intended defects (those checks precede VECTOR parsing)
  but are buried under 14 unintended defect lines each.
`SELFTEST red_refused=5/5 ok=True` (rc 0) therefore proves only "rc==1", not that the intended
refusal reasons work. Additionally the green arm is broken by M-A+M-B:
`--selftest --green-receipt <best-case receipt>` → `GREEN receipt rc=1 accepted=False → ok=False`,
rc 1 — at close time, "the C1 selftest tally" will fail on the genuine green receipt.

**M-D · P2 — SUMMARY is not re-derived; two substring tests only** (L556). Forgery F7 (sha256
`47e470e750cbde44f26b222a60dc8499d6413d7e647bc5b1f8a3aa4bea336363`): `SUMMARY cases=9 legs=77
mismatches=05 setup=01` — refused **only** by the M-B background (its defect set equals the
baseline): the doctored counts pass (`"mismatches=0" in …`, `"setup=0" in …` are substring
tests; `05`/`01` contain them) and are never cross-checked against the actual TEST/VECTOR lines.

**M-E · P2 — duplicated VECTOR lines accepted** (F5, sha256
`a7108488edef673dbcfa68db270df78386bd853c2bc3cee4c96cd6f5c4f82aab`): K1's VECTOR line appears
twice; L516 dict-overwrites last-wins, no duplicate detection. Defect set = baseline only.

**M-F · P2 — leg order not bound** (F4, sha256
`957e064c29c1fbccfa5b0cb38732d3f6da201bee801a07c27faa2a548879c040`): all per-case TEST lines
emitted in reversed grader file order — accepted (defect set = baseline). The claim ties legs to
the grader's file order; the checker is order-insensitive by construction (L522 dict, L542
derivation in LEGS order). Inherent to text receipts; state, don't fix.

**M-G · P2 — receipt payload not closed: unknown lines ignored, auxiliary lines optional**
(F6, sha256 `1e6ddc3bdd4b80f1425a47b19b2ee24392e087dd957882dacb1b8521b81b756d`, with junk lines
`HACK this receipt was forged offline; no bwrap run happened` — accepted; F8, sha256
`910071c7e69f2b259f4441f6b13bc7bac733d5eafeaf8c8fe40a06c2d60202ce`, with **all** PROBE_VERSION,
PORT and CASE lines stripped — accepted). The checker parses only PROBE/GRADER/VECTOR/TEST/
SUMMARY/PREDICATE prefixes. This strengthens frozen named limitation (iii): `case_sha256`/
`server_pid` are not merely unverifiable — they are **unparsed**; a receipt with no CASE lines
at all is accepted.

**M-H · P3 — TEST lines for unknown case ids accepted** (F10, sha256
`6360a526cfd5d4a31de414ec57046f93061c02beb8be2809bf80b9768cdf92fc`): eight `TEST K9 …` lines
silently ignored (legs dict keyed by cid, never inspected for non-frozen ids).

**M-I · P3 — stored predicate line is shape-only** (F9, sha256
`42353acc3954f8ebe36c6b352b31ac13a618f68bb8c437c300c370759547b13d`):
`PREDICATE R69-C1 never-ran pass` accepted — `endswith(" pass")` (L561) is the whole test.
Cosmetic, since the derived verdict is what returns rc.

**M-J · P3 — clause-3 nuance:** the PROBE check compares against `own_sha256()`, i.e. the bytes
on disk at `__file__` — "committed bytes" only while the tree is clean, which the checker cannot
itself verify (verified externally today: clean, blob == tree).

**M-K · P3 — clause-4 nuance:** `check_receipt` compares the GRADER sha against the frozen
constant and never re-hashes the lane's grader file; a receipt binding the right constant is
accepted regardless of the grader file's current bytes (which only battery SETUP re-hashes,
L405-408).

**M-L · P4 — diagnostics:** `CHECK ok cases=5 …` (L564) is a fixed prefix printed even when the
check fails, and reads `seen_p=0 seen_f=0` whenever the parse collapsed — misleading on the
exact path where a reader most needs accurate diagnostics.

### Consistent with frozen named limitation (i) (not a new defect)
F2 — a complete, self-consistent receipt for a run that never happened (zero `case_sha256`s,
`server_pid=4242`) — is refused today *only* by the M-B background clause. Once M-A/M-B are
amended, a forgery of this class is accepted by design (the checker cannot prove a live run).
The freeze already discloses this; F2 quantifies it.

### What the checker does catch (calibration credit, empirical unless noted)
- F3 all-P with matching TEST lines (sha256 `1f77e4e42bf85952e0dba5df24c5e2a91b7b83fa9fb0c35e1e6f5e26ea8fe88a`): refused — `vector-mismatch` ×4 + `leg-coverage` ×8.
- F11 unknown leg name `test_not_a_grader_leg` (sha256 `b4be109716240004f629ee199cea6b33085cb25252cd227e89607b0b321f6bdb`): refused — `leg-set K1`.
- TEST value ∉ {P,F} → `leg-missing` (static, L545-551); duplicate PROBE/GRADER lines → count defects (L490-492, L499-501); wrong probe/grader sha → `probe-sha`/`grader-sha` (selftest r2/r5, empirically); stored `agree≠True` → `vector-agree` (static, L537-538); wrong per-case vector → `vector-mismatch` (F3, F12 empirically).

## 3. Forgery ledger (all built from the probe's own constants; generator inline below)

| Fixture | Family | Verdict under frozen bytes | Defects beyond M-B baseline |
|---|---|---|---|
| F1-green-battery-shape `ad298d16…` | canonical writer-format green | REFUSED rc 1 | +vector-line ×5, +case-set, +leg-coverage ×8 (p=0 f=0) — **M-A** |
| F2-green-parser-shape `ee36c932…` | perfect forged green (never ran) | REFUSED rc 1 | none (baseline = M-B's two leg-coverage) — limitation (i) |
| F3-all-p-parser-shape `1f77e4e4…` | all-P vectors, matching TEST lines | REFUSED rc 1 | +vector-mismatch ×4, +leg-coverage ×8 — caught |
| F4-shuffle-parser-shape `957e064c…` | shuffled leg order, vectors agree | REFUSED rc 1 | none — **undetected (M-F)** |
| F5-dup-vector-parser-shape `a7108488…` | duplicated VECTOR line | REFUSED rc 1 | none — **undetected (M-E)** |
| F6-junk-parser-shape `1e6ddc3b…` | extra unknown lines | REFUSED rc 1 | none — **undetected (M-G)** |
| F7-edited-summary-parser-shape `47e470e7…` | edited SUMMARY | REFUSED rc 1 | none — **undetected (M-D)** |
| F8-stripped-aux-parser-shape `910071c7…` | no PROBE_VERSION/PORT/CASE lines | REFUSED rc 1 | none — **undetected (M-G)** |
| F9-predicate-variant-parser-shape `42353acc…` | `never-ran pass` predicate | REFUSED rc 1 | none — **undetected (M-I)** |
| F10-extra-case-tests-parser-shape `6360a526…` | TEST lines for phantom case K9 | REFUSED rc 1 | none — **undetected (M-H)** |
| F11-bogus-leg-parser-shape `b4be1097…` | unknown leg name | REFUSED rc 1 | +leg-set K1 — caught |
| F12-double-bind `7e1db5f9…` | coverage satisfied, frozen vector violated | REFUSED rc 1 | +vector-mismatch K1 — proves **M-B** double-bind |

"REFUSED rc 1" everywhere is itself the finding: under the frozen bytes *nothing* can be
ACCEPTED, so the per-family "undetected" verdicts are read as "defect set equals the
unsatisfiable baseline". Note the two P0s make the ACCEPTED/REFUSED axis degenerate; the
defect-set deltas above are the discriminating evidence.

## 4. Commands run (exact argv, from scratch `/fast/scratch/hyaku/kengaku-r69/ReceiptReview-2`)

- `python3 gen_fixtures.py` (generator below; imports the probe module, builds F1–F12, prints digests)
- `python3 $P --check-receipt $S/F*.txt` (each of F1–F12; `$P` = lane probe path)
- `python3 - ` heredoc building F12 from F2 (digest above)
- `python3 $P --selftest --work $S/selftest` → `SELFTEST red_refused=5/5 green_ok=0 ok=True`, rc 0
- `python3 $P --selftest --work $S/selftest2 --green-receipt $S/F2-green-parser-shape.txt` → `GREEN receipt rc=1 accepted=False`, `ok=False`, rc 1
- `python3 $P --check-receipt $S/selftest/selftest-red/r{1..5}*.txt | grep -o '^DEFECT [a-z-]*' | sort | uniq -c` (defect-kind profiles)
- `python3 $P --check-receipt <L>/corpus/evidence/round69/nginx/receipt.txt` → `SETUP receipt-missing …`, rc 2 (do-nothing control reproduced)
- `sha256sum` probe + grader; `git -C <L> rev-parse HEAD`; `git -C <L> status --porcelain -- plans/round69_c1_nginx_probe.py plans/round-69-claims.md`; `git -C <L> show b288e8e0:plans/round69_c1_nginx_probe.py | sha256sum`; `git -C <L> diff --stat a518980e HEAD -- plans/round69_c1_nginx_probe.py plans/round-69-claims.md`; `git -C <L> log --oneline a518980e..HEAD -- plans/round69_c1_nginx_probe.py`; `grep -n nginx-request-logging <L>/corpus/evidence/round52/graders/SHA256SUMS`; `ss -ltnp '( sport = :8080 )'` (free, empty)

**Commands NOT run (state per protocol):** the battery itself (`--lane … --work … --receipt …`)
— not authorized for this seat; port 8080 never bound, no lock taken. No `--render-table`
byte-compare (outside seat scope; the case table was verified by reading CASES against the
frozen table, which match). No edits to any lane file; no git/jj write commands; no labrat
probe; no installs/upgrades (none needed). Scratch dir deleted before yield; digests above are
the byte record (generator reproduces all fixtures bit-for-bit given the frozen probe).

## 5. For the C1 attacker / close

1. **M-A**: one-line class of fix (writer L460-461 vs parser L513 — align token counts, e.g. make
   the parser accept 6 tokens and read `parts[2]`/`parts[6]`, or drop `expected` from the writer).
   Until fixed, `PREDICATE R69-C1 pass` is unreachable and the selftest's `red_refused=5/5` is
   vacuous.
2. **M-B**: claims-level contradiction (6 F's in the frozen table vs "every leg F in ≥1 case");
   the battery cannot print pass even with a flawless replay (`full_f=6≠8`, L465). Needs the
   dated-amendment path from the freeze paragraph: add two red witnesses to the case table or
   scope the coverage clause to the priced legs.
3. M-D–M-I: hardening list for the checker (re-derive SUMMARY from TEST/VECTOR lines; reject
   duplicate VECTOR/case ids; bind leg order; reject unknown lines and unknown case ids; require
   CASE/PROBE_VERSION/PORT lines present; require predicate line equality).
4. The committed do-nothing control still reproduces (`SETUP receipt-missing`, rc 2) — unaffected
   by the above.

### Generator (verbatim; regenerates every fixture byte-for-byte)

```python
#!/usr/bin/env python3
import hashlib, importlib.util, pathlib
PROBE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py"
OUT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("probe", PROBE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ZERO = "0" * 64; PROBE_SHA = m.own_sha256()
def vec_values(v): return ["P" if c == "P" else "F" for c in v]
def build(name, *, battery_shape=False, all_p=False, shuffle=False, dup_vector=False,
          junk=False, summary_override=None, strip_aux=False, predicate_override=None,
          extra_case_tests=False, extra_bogus_leg=False):
    lines = [f"PROBE plans/round69_c1_nginx_probe.py sha256 {PROBE_SHA}"]
    if not strip_aux: lines.append(f"PROBE_VERSION {m.PROBE_VERSION}")
    lines.append(f"GRADER {m.GRADER_REL} sha256 {m.GRADER_SHA256} pin {m.TB2_PIN}")
    if not strip_aux: lines.append(f"PORT {m.PORT} free-at-start=True lock={m.LOCK_PATH}")
    for case in m.CASES:
        cid = case["id"]
        vec = "P" * len(m.LEGS) if all_p else case["expected"]
        vals = vec_values(vec)
        if not strip_aux: lines.append(f"CASE {cid} case_sha256={ZERO} server_pid=4242 sandbox_rc=0")
        order = list(m.LEGS)
        if shuffle: order = order[::-1]
        for leg in order: lines.append(f"TEST {cid} {leg} {vals[m.LEGS.index(leg)]}")
        if extra_bogus_leg and cid == "K1": lines.append(f"TEST {cid} test_not_a_grader_leg P")
        if battery_shape:
            lines.append(f"VECTOR {cid} {vec} expected {case['expected']} agree=True")
            if dup_vector and cid == "K1":
                lines.append(f"VECTOR {cid} {vec} expected {case['expected']} agree=True")
        else:
            lines.append(f"VECTOR {cid} {vec} x agree=True")
            if dup_vector and cid == "K1": lines.append(f"VECTOR {cid} {vec} x agree=True")
    if extra_case_tests:
        for leg in m.LEGS: lines.append(f"TEST K9 {leg} P")
    lines.append(f"LEG-COVERAGE legs={len(m.LEGS)} seen_p={len(m.LEGS)} seen_f={len(m.LEGS)}")
    lines.append(summary_override or
                 f"SUMMARY cases={len(m.CASES)} legs={len(m.CASES) * len(m.LEGS)} mismatches=0 setup=0")
    lines.append(predicate_override or "PREDICATE R69-C1 pass")
    if junk:
        lines.append("HACK this receipt was forged offline; no bwrap run happened")
        lines.append("SANDBOX no-live-run rc=0")
    text = "\n".join(lines) + "\n"
    p = OUT / f"{name}.txt"; p.write_text(text, encoding="utf-8")
    print(f"{name}.txt sha256={hashlib.sha256(p.read_bytes()).hexdigest()} bytes={len(text)}")
build("F1-green-battery-shape", battery_shape=True)
build("F2-green-parser-shape")
build("F3-all-p-parser-shape", all_p=True)
build("F4-shuffle-parser-shape", shuffle=True)
build("F5-dup-vector-parser-shape", dup_vector=True)
build("F6-junk-parser-shape", junk=True)
build("F7-edited-summary-parser-shape", summary_override="SUMMARY cases=9 legs=77 mismatches=05 setup=01")
build("F8-stripped-aux-parser-shape", strip_aux=True)
build("F9-predicate-variant-parser-shape", predicate_override="PREDICATE R69-C1 never-ran pass")
build("F10-extra-case-tests-parser-shape", extra_case_tests=True)
build("F11-bogus-leg-parser-shape", extra_bogus_leg=True)
# F12 built from F2 by: TEST K1 test_nginx_running P→F, TEST K1 test_custom_404_page P→F,
# VECTOR K1 PPPPPPPP x agree=True → VECTOR K1 PFPFPPPP x agree=True
```

No tool installs were made; no pacman/uv/npx commands were run.
