# R46ExecC2States — independent ground truth for C2 leg B (grader verdict per newline state)

Seat: `R46ExecC2States` (executor, leaf). Round 46 wave 1, lane `kengaku-shokunin`, base
`64ba8385ea10af1b78d367dcb242b92d97062af7`, stage-1 freeze `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`.
Scope: **measure only** — no lane file was edited; the one predictor edit lives in a scratch `--shared` clone.

## 0. What was read before measuring

- `plans/round-46-claims.md` (sha256 `4f22d994…`) in full: C2 is frozen whole, leg B = "the entry's predictor vs the
  CAPTURED grader on 16 frozen newline states (lone CR, LF-CR, CR-CR-LF, VT/FF/NEL/LS non-newlines, CRLF controls)"
  with the predicate "`B predictor` with `disagree=0`, grader_pass>=4 and grader_fail>=4".
- `corpus/lessons/round-45-verifier-spotcheck.md` §2, §5 item 2: "Mark or supersede the entry's `## Predictor` (lone-CR
  divergence; prose at `:150,:194` overclaims universal newline)".
- The frozen graders/tools: `plans/round46_c2_verify.py` (`2042d873…`), `plans/round45_c2_verify.py` (`ab6825e3…`),
  `corpus/evidence/round45/tb2-password-recovery/test_outputs.py` (`2dc14fc1…`) — all three re-hashed inside the run
  (`receipt-States.txt` → `digests`), equal to `.ufo/waves/round-46/claims/frozen-digests.txt`.
- `corpus/knowledge/tb2-password-recovery-grader.md:191-199`: the landed predictor
  `text.replace("\r\n", "\n").strip().split("\n")` while the prose at `:194` claims "`read_text`'s universal-newline read".

## 1. Method (faithful to the counter, not a re-implementation)

Harness = the counter's own: `rules45.GRADE_PY.replace('open(p, "w")', 'open(p, "w", newline="")')` executed by
`round45_c2_verify.sandboxed()` (bubblewrap: `--unshare-net --unshare-pid --unshare-ipc`, `/usr`+`/etc` ro,
`--bind work/app /app`, `--ro-bind work/tests /tests`, `LANG=C.UTF-8 PYTHONUTF8=1`). The 16 frozen states are built by
importing `plans/round46_c2_verify.py` and applying its own `DECOY` + the grader's answer literal exactly as `leg_b`
does (`re.sub(r"[CD]", …)`), so the states are byte-identical to the counter's.
Per-state detail comes from a second run of an identical harness that records both test functions separately.

Fidelity check (independent run vs the frozen before-receipts):

| quantity | mine (`receipt-States.txt`) | frozen receipt |
|---|---|---|
| 16 frozen states | `grader_pass=30 grader_fail=16` over 46; on the 16: `10/6` | `control-c2-nothing.txt: B … states=16 grader_pass=10 grader_fail=6` |
| landed predictor on the 16 | `disagree=6` (F00,F01,F02,F05,F06,F07) | `B … disagree=6 DEFECT` |
| splitlines predictor on the 16 | `disagree=4` (F12–F15) | `control-c2-splitlines.txt: B … disagree=4 DEFECT` |

## 2. Grader verdict per state — the 16 frozen `STATE_SHAPES`

`an = 8XDP5Q2RT9ZK7VB3BV4WW54` (23 chars, the only literal in the grader) — this is the counter's `C` placeholder;
`D` = the counter's `DECOY`. Ids `F00…F15` are row-for-row the ones in `tables.md` §A (`F00_'C\rD'` = `F00_an\rD`).
`exists` = `test_recovery_file_exists`, `match` = `test_password_match`. P1 = landed (CRLF-only), P2 = universal
newlines (`\r\n`→`\n` then `\r`→`\n`) + `.strip()` + `split("\n")`, P3 = `strip().splitlines()`, P4 = strip-per-line.

| state | grader | exists | match | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|---|---|
| `F00_an\rD` | **pass** | T | T | F | T | T | T |
| `F01_D\ran` | **pass** | T | T | F | T | T | T |
| `F02_D\n\ran` | **pass** | T | T | F | T | T | T |
| `F03_an\r` | **pass** | T | T | T | T | T | T |
| `F04_\ran` | **pass** | T | T | T | T | T | T |
| `F05_an\r\r\nD` | **pass** | T | T | F | T | T | T |
| `F06_D\r\ran` | **pass** | T | T | F | T | T | T |
| `F07_D\r\nan\rD` | **pass** | T | T | F | T | T | T |
| `F08_an\r\n` | **pass** | T | T | T | T | T | T |
| `F09_D\r\nan\r\n` | **pass** | T | T | T | T | T | T |
| `F10_D\rD` | fail | T | F | F | F | F | F |
| `F11_anx\rD` | fail | T | F | F | F | F | F |
| `F12_an\x0bD` | fail | T | F | F | F | **T** | **T** |
| `F13_an\x0cD` | fail | T | F | F | F | **T** | **T** |
| `F14_an\x85D` | fail | T | F | F | F | **T** | **T** |
| `F15_an\u2028D` | fail | T | F | F | F | **T** | **T** |

Reading: `test_recovery_file_exists` passes in every state (the harness always creates the file), so the whole verdict is
`test_password_match`. The landed predictor's error is narrow but real — **lone CR used as a separator**, 6 of 16.
F03/F04 (lone CR at the file edge) already agree because the grader's `.strip()` removes an edge CR before the split;
that is why the gap is 6, not 8.

## 3. Grader verdict per state — 30 states chosen by this seat

| state | text | grader | exists | match | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|---|---|---|
| X01 | `an\r\n\r\n` | **pass** | T | T | T | T | T | T |
| X02 | `an\r\r` | **pass** | T | T | T | T | T | T |
| X03 | `an\r\n\r` | **pass** | T | T | T | T | T | T |
| X04 | `\ran` | **pass** | T | T | T | T | T | T |
| X05 | `an\n\r` | **pass** | T | T | T | T | T | T |
| X06 | `an\r\r\rD` | **pass** | T | T | F | T | T | T |
| X07 | `D\r\r\nan\rD` | **pass** | T | T | F | T | T | T |
| X08 | `D\n\r\nan` | **pass** | T | T | T | T | T | T |
| X09 | `an\rD` | **pass** | T | T | F | T | T | T |
| X10 | `D\rE` | fail | T | F | F | F | F | F |
| X11 | `an\x1cD` | fail | T | F | F | F | **T** | **T** |
| X12 | `an\x1dD` | fail | T | F | F | F | **T** | **T** |
| X13 | `an\x1eD` | fail | T | F | F | F | **T** | **T** |
| X14 | `an\x1fD` | fail | T | F | F | F | F | F |
| X15 | `\x1can` | **pass** | T | T | T | T | T | T |
| X16 | `an\x1f` | **pass** | T | T | T | T | T | T |
| X17 | `an\u2029D` | fail | T | F | F | F | **T** | **T** |
| X18 | `an\u2028` | **pass** | T | T | T | T | T | T |
| X19 | `D\nan\u2028` | **pass** | T | T | T | T | T | T |
| X20 | `\u2028an` | **pass** | T | T | T | T | T | T |
| X21 | `\x85an` | **pass** | T | T | T | T | T | T |
| X22 | `an\x85` | **pass** | T | T | T | T | T | T |
| X23 | `an\x0b` | **pass** | T | T | T | T | T | T |
| X24 | `an\x0c` | **pass** | T | T | T | T | T | T |
| X25 | `\ufeffan\n` | fail | T | F | F | F | F | F |
| X26 | `\ufeff\nan\n` | **pass** | T | T | T | T | T | T |
| X27 | `D\n\ufeffan` | fail | T | F | F | F | F | F |
| X28 | `an\x00\n` | fail | T | F | F | F | F | F |
| X29 | `\x00an\n` | fail | T | F | F | F | F | F |
| X30 | `an\n\x00D` | **pass** | T | T | T | T | T | T |

(`an` = the answer literal; full reprs and the exact bytes are in `tables.md` §B.)

Totals over the 46 primary states (`receipt-States.txt` → `summary`): grader 30 pass / 16 fail;
disagreements **P1 = 9** (6 frozen + X06,X07,X09), **P2 = 0**, **P3 = 8**, **P4 = 8**.

Behaviour the table pins down:

- `.strip()` is applied to the **whole file**, once: a single-line padded answer passes (`  an  \n` → `an`), an
  interior padded answer line does not (§5 Z09–Z11).
- `\x0b \x0c \x1c-\x1f \x85 \u2028 \u2029` are `str.strip()` whitespace but **not** separators for `read_text`:
  interior → fail, edge → stripped, so pass (X15,X16,X18–X24). `splitlines()` splits on them, hence P3/P4's 8 misses.
  `\x1f` is an exception: `splitlines()` does not split on it (X14), so P3/P4 agree there.
- U+FEFF (BOM) is **not** whitespace: on the answer line it fails (X25,X27); on its own line it passes (X26).
- NUL is not whitespace and not a separator: `an\x00` fails (X28,X29), a NUL on another line is harmless (X30).
- The counter's UTF-8 assumption is exercised: X21/X22 (NEL) and X18–X20 (LS) can only pass if `read_text` decoded
  UTF-8 and `.strip()` removed those chars — a Latin-1/ASCII read would have errored or left `Â`.

## 4. Byte payloads outside the str domain (`receipt-States.txt` → `byte_rows`)

| payload | bytes | exists | match | P6 decode-guard |
|---|---|---|---|---|
| `Y01_utf16le_bom` | UTF-16LE BOM + `an\r\n` | T | **F** | F |
| `Y02_invalid_ff_after` | `an\n` + `0xFF` | T | **F** | F |
| `Y03_bom_utf8_answer` | UTF-8 BOM + `an\n` | T | **F** | F |
| `Y04_utf16le_no_bom` | UTF-16LE `an\r\n` | T | **F** | F |

`Path.read_text()` raises `UnicodeDecodeError` on Y01/Y02/Y04, so `test_password_match` **errors** (counts as fail)
even though the answer is "in the bytes"; Y03 decodes to `\ufeff` and fails on the BOM (§3 X25). A predictor that
decides from raw bytes must therefore start with `try: text = data.decode() except UnicodeDecodeError: return False`.
C2 leg B never reaches this domain: its states are JSON strings written as UTF-8, so a str-domain predictor is exact
where the counter can measure.

## 5. Extra sweeps (same harness, same envelope)

- 8 padded/joined/empty states (`receipt-States2.txt` → `z`): grader 4 pass / 4 fail; **P1–P4 all 0 disagreements**
  (e.g. `Z01` `  an  \n` **passes** — whole-file strip — while `Z05` `PASSWORD=an\n`, `Z06` `anD\n`, `Z07` ``, `Z08`
  `\r\n` fail).
- 6 interior-padding states (`receipt-States3.txt` → `rows`): `Z09` `an  \n\tD\t\n`, `Z10` `D\n  an  `,
  `Z11` `D\nan \nE` all **fail** while **P4 says pass** (3 disagreements; P1–P3 agree). This is the one class where
  strip-per-line is wrong for a reason other than `splitlines`.
- 300 randomised states (seed 46, token pool `\r\n \r \n \t space \x0b \x0c \x1c-\x1f \x85 \u2028 \u2029 \ufeff \x00
  an D 8XDP ans x`, lengths 1–6; `receipt-States2.txt` → `r`): grader 15 pass / 285 fail; **P1 = 1** (R157
  `'\x0c\x1f\x00\t\ran'`, again a lone-CR separator), **P2 = 0**, **P3 = 10**, **P4 = 10** (ids listed in
  `tables.md`; e.g. R049 `'an\u2029\x0b8XDP'`).

Total graded executions of the two test functions: **360 states** (16 frozen + 30 + 8 + 300 + 6) + 4 byte payloads.
P2's disagreement count over all 360: **0**.

## 6. Is the universal-newline predictor exact? — yes on the str domain; here is the exact predictor

Exact by construction too, not just empirically: the grader is
`Path("/app/recovered_passwords.txt").read_text().strip().split("\n")` with `… in guesses`
(`corpus/evidence/round45/tb2-password-recovery/test_outputs.py:15,20`), and `read_text` (newline=None) performs
exactly `\r\n`→`\n`, `\r`→`\n` on the decoded text. P2 repeats those two rules, then the same `.strip()` and
`split("\n")` and the same exact-equality membership.

Entry-ready block (lint-clean; `round45_c2_verify.PRED_LINT_TOKENS` hits: **[]**, 147 bytes ≤ `PRED_MAX_BYTES` 4000):

```python
def predict(text):
    return text is not None and "8XDP5Q2RT9ZK7VB3BV4WW54" in text.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")
```

The single added leg is `.replace("\r", "\n")`. Measured effect on the frozen counter, on two `--shared` clones of the
freeze commit `fd4129e` (identical trees except that one line, `receipt-c2-before.txt` vs `receipt-c2-after.txt`):

```
before  PINS total=3 mismatched=0
        A anchorline live=8 repaired=0 base_rows=149 base_missing=0 base_changed=0 DEFECT
        B predictor states=16 grader_pass=10 grader_fail=6 disagree=6 DEFECT
        C entry source_ranges=9 source_ranges_bad=4 errata_marks=0/5 DEFECT
after   PINS total=3 mismatched=0
        A anchorline live=8 repaired=0 base_rows=149 base_missing=0 base_changed=0 DEFECT
        B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
        C entry source_ranges=9 source_ranges_bad=4 errata_marks=0/5 DEFECT
```

Only leg B moves (defects 3 → 2); A and C stay base-defective, as the C2 work items intend (S157–S165 + errata).

`newline=""` (leg B) vs round-45's default `open(p, "w")`: `receipt-newline-mode.txt` → `{"n": 46, "identical": true,
"diff_idx": [], "pass": 30, "fail": 16}` — a no-op on Linux (`os.linesep == "\n"`); it would only matter on Windows.
`newline=""` is therefore not what closes the gap; the lone-CR leg is.

## 7. Limits and risks (named, for the L1)

1. Exactness of a str predictor is conditional on the grader decoding UTF-8. Leg B's sandbox fixes
   `LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1` (`round45_c2_verify.SANDBOX_ENV`), and X18–X22 confirm UTF-8 decoding;
   under any other locale `read_text` could raise on these states. Do not relax that env.
2. Raw-byte states (invalid UTF-8 / UTF-16) are outside the str domain; the decode-guard form in §4 is exact there
   (4/4) but has no place in a counter that feeds JSON strings.
3. The four frozen "non-newline" shapes are interior-only; the edge cases (X15..X24) show that `.strip()` rescues them.
   A future generator that only adds interior shapes keeps this asymmetry — cheap to carry, but it should be known.
4. Do not "improve" the predictor with `.lstrip("\ufeff")`, `lstrip()`/`rstrip()` per line, or `splitlines()`: each
   moves it off the grader (BOM 2 states, padding 3 states, separators 8+10 states).
5. `test_recovery_file_exists` never discriminates in this harness (the harness writes the file for every non-None
   state); a state intended to fail on existence is unreachable, exactly as in round 45.

## 8. Host safety — envelope lines

`S=/fast/scratch/hyaku/kengaku-r46/R46ExecC2States`; `E=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh`.
Every run used `$E "$S/env-run" <cmd>`; the fence line is byte-identical in all six receipts:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <S>/env-run <S>/env-run --bind <S>/env-run/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <cmd>
```

| run | command | ENVELOPE end line |
|---|---|---|
| 46-state ground truth | `$E "$S/env-run" /usr/bin/python3 "$S/measure.py" "$S/work"` | `ENVELOPE end 02:06:12 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged` |
| Z + 300 random + byte sweeps | `$E "$S/env-run" /usr/bin/python3 "$S/measure2.py" "$S/work"` | `ENVELOPE end 02:07:38 exit=0 … unchanged` |
| interior padding | `$E "$S/env-run" /usr/bin/python3 "$S/measure3.py" "$S/work"` | `ENVELOPE end 02:08:19 exit=0 … unchanged` |
| counter, pristine clone | `$E "$S/env-run" /usr/bin/python3 "$S/clone2/plans/round46_c2_verify.py" --lane "$S/clone2" --work "$S/c2work-before"` | `ENVELOPE end 02:09:40 exit=1 … unchanged` |
| counter, repaired clone | `$E "$S/env-run" /usr/bin/python3 "$S/clone/plans/round46_c2_verify.py" --lane "$S/clone" --work "$S/c2work-after"` | `ENVELOPE end 02:09:48 exit=1 … unchanged` |
| newline-mode differential | `$E "$S/env-run" /usr/bin/python3 "$S/measure4.py" "$S/work"` | `ENVELOPE end 02:10:11 exit=0 … unchanged` |

`start` lines: 02:06:10, 02:07:35, 02:08:16, 02:09:36, 02:09:43, 02:10:08 (cwd `/home/vgpnk/Projects/shokunin` each).
Every run also nested its own tighter bwrap (`--unshare-net --unshare-pid --unshare-ipc`, `/usr`,`/etc` ro, tmpfs `/tmp`,
`/app` a scratch dir, `/tests` ro) — the grader never saw the host filesystem. `~/.local/bin` content digest unchanged in
all six. No `/tmp` file used; nothing written outside `$S` and `$R`.

## 9. Files changed / artifacts

Lane files changed: **none**. Scoped writes: this report and `…/w1/R46ExecC2States/`. Scratch clone edits: the one
predictor line in `$S/clone/corpus/knowledge/tb2-password-recovery-grader.md` (§6); no commit anywhere.

Receipts in `.ufo/waves/round-46/w1/R46ExecC2States/` (sha256):

```
40f85b5a39bc22b57517bd4445d5df9752dc9327fd067c7f3ce419bad32a8773  receipt-States.txt
10240dcbaf0013c9633b48d1bf13fccd073ea35c109061e26847335ecdcc591a  receipt-States2.txt
fede2575bfa30ccd0b252649370e216b26409ccc6c31dd210114177da2cdf8b8  receipt-States3.txt
f03c0091292ea14c4a817ab781182d21e1b4f5edcc0cf53c8289951c9dcd375f  receipt-c2-before.txt
25575e02e0afdb0bc9676785a3fa65d1fd504e521a57f6c84ff90a6595dac7e2  receipt-c2-after.txt
d76132f3232ce4312b9cd593a9be97ae08b3c51a36700a63c0d2aaf695840b54  receipt-newline-mode.txt
0e2ad483935c8b4bbe0e25ce60d5d029f91d35f8d2bc3a5848f44a7f259b7e5a  tables.md
50e9edf40c56ab1d86935c8124b13f3c9db6d48197cc2853a62ec150543cf807  measure.py
4199f0f9a267cb4b1c86e8c79c18612403ffdfc243730358b4978f7facfb1f4a  measure2.py
331988931ae654356ed770d30bafa209c2f6999f15fcf3f21726bd19b821d289  measure3.py
1887d9e78bc3bbe782937029616a1ac0df30da2dc703ed345f2336cb518d6139  measure4.py
```

Tool installs: none (no pacman, no uv/npx); stock `/usr/bin/python3` and `/usr/bin/bwrap` only.

VERDICT: grader-newline-states-46-universal-predictor-disagree-0
