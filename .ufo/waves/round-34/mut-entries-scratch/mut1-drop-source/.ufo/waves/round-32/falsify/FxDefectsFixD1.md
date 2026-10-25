# FxDefectsFixD1 — D1 repair review (round 32, 2026-10-25)

Scope: planned D1 repair — appended erratum to the round-31 fleet report
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md`, read-only; the lane writes it).
Draft: `.ufo/waves/round-32/build/R32DraftErrata.md` §(a). Counter: `plans/round32_defects.py`
check R1.

## VERDICT: d1-closable

## Findings (by severity)

No actionable defect found in scope. All three acceptance items verified on real bytes:

### (a) Draft names `a44b5a8` and supersedes it with `ae95fe0` — PASS

Extracted the D1 block from R32DraftErrata.md (lines 9–13 of the file, between headers `## (a)`
and `## (b)`). The block names the phantom token three times, labels the citation "bogus", states it
"is superseded", and names the real commit `ae95fe0` with its subject. Ground truth matches the
draft's "Verified grounds":
- `git cat-file -t a44b5a8` → `fatal: Not a valid object name a44b5a8` (rc=128; phantom).
- `git cat-file -t ae95fe0` → `commit` (rc=0); subject `round-31: entry locator corrections
  (verifier_mode.py:18-21, :39-40) and final falsify evidence`; `ae95fe0` is an ancestor of the
  current lane tip.

### (b) Draft is append-only — PASS

Simulated append: byte-copied the live round-31 fleet report (20,998 bytes) to scratch and appended
the extracted erratum block verbatim (487 bytes). Verification:
- `appended[:len(orig)] == orig` → True (prefix-identical).
- sha256(original) = `cf141d2c…60d71` == sha256(prefix of appended) — no existing byte altered.
- Delta is exactly the 487-byte erratum block; the draft contains no edit/delete instruction for the
  target (it says "Append to `.ufo/reports/round-31/kengaku.md`:" and provides only the block).

### (c) Appending turns R1 green — PASS

Ran the real `check_r1` from `plans/round32_defects.py` (imported, not reimplemented) against the
scratch-appended copy:
- Pre-append (live report): `check_r1` → `"no appended erratum supersedes the a44b5a8 citation"`
  (red) — byte-identical to the frozen control `defects-before.txt` line 3, confirming the
  simulation reproduces the counter's live behavior.
- Post-append: `check_r1` → `""` (green).
- Green mechanism verified on the appended text: `text` contains `a44b5a8` (kept, count 5), the
  `a44b5a8`/`superseded` pair co-occurs within 300 chars on one line (`near(...,"superseded")` →
  True), and `ae95fe0` is present (count 1). Re-ran the same check on a variant with the `> `
  blockquote markers stripped: also green — R1 is insensitive to the quote-marker rendering choice.

## Residual risk

- R1 is green via the **same-line "superseded"** pair only. The counter's `near()` uses `.` without
  DOTALL, so it cannot cross newlines; the word "erratum" alone on its own line does not satisfy it.
  If the lane rewraps the appended block so `a44b5a8` and `superseded` land on different lines, R1
  would stay red despite the erratum being appended. The draft as written (one line carries both
  tokens) is safe; append the draft bytes verbatim.
- The `> ` blockquote prefix is orthography only; both prefix and stripped variants pass.
- Append target is the fleet-path report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md`),
  which the counter reads by default (`R31_REPORT`). Appending to a different copy would not green R1.

## Verification gaps

- Did not run the full `round32_defects.py` counter end-to-end (other checks R2–R7 are intentionally
  still red pre-landing; the frozen control `defects-before.txt` confirms the pre-repair state).
- Did not watch the lane's actual append happen (fleet report is read-only for this reviewer; the
  lane writes it). The simulated append uses the exact draft bytes.

Tool installs: none (no `pacman` transaction; nothing was installed or upgraded).
Scratch (under 60 MB): `/tmp/r32f-fxdefectsfixd1/r31-kengaku-appended.md`,
`r31-kengaku-appended-stripped.md`.
