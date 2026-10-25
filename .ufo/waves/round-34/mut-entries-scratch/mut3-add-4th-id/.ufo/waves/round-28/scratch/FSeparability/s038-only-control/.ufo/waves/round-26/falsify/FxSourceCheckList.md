# FxSourceCheckList — Q10 source/number re-read

Scope: admission source/number check for proposed `corpus/knowledge/grader-perturbation-audit.md`; re-opened S043 independently and checked S043/S047 against the Gate and source receipt. No production files changed.

## S043 — CheckList

- URL: https://aclanthology.org/2020.acl-main.442.pdf. Direct `curl -sS -L --max-redirs 5 -o /tmp/fxsource-s043.pdf -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\ncontent_type=%{content_type}\nsize_download=%{size_download}\n' 'https://aclanthology.org/2020.acl-main.442.pdf' && sha256sum /tmp/fxsource-s043.pdf` → HTTP 200; effective URL unchanged; `application/pdf`; 400832 bytes; SHA-256 `98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1`; exit 0.
- Independently opened the downloaded PDF with `pdfinfo`/`pdftotext`. It is *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*, ACL 2020 proceedings version (July 5–10, 2020; pages 4902–4912); PDF metadata CreationDate is 2020-06-08 -03, not the publication date. No distinct version number is stated.
- Quote (21 words; exact): “An Invariance test (INV) is when we apply label-preserving perturbations to inputs and expect the model prediction to remain the same.” It appears under §2.2 on PDF p.3 / proceedings p.4904 (extracted p.3 lines 48–50; footer line 63 says 4904). It does **not** appear on PDF p.2 / proceedings p.4903.
- The quote matches word-for-word in `corpus/lessons/round-26.md:47`, `corpus/evidence/round26-sources/gate.md:5`, and `.ufo/waves/round-26/build/SrcCheckList.md:8`; each cited location says PDF p.2 / p.4903, which is wrong. The paper's §2.2 heading begins on p.4904 as well. Correct the location in the Gate and receipt before admission.
- Support: the source defines label-preserving **input** perturbation invariance for model predictions. It supports the draft's contrast at `.ufo/waves/round-26/drafts/grader-perturbation-audit.md:17-20` (“not a new method” for invariance generally; this audit targets grader verdicts under response-format perturbations). It does not define or empirically validate this lane's grader audit. None of the draft's numeric population, result, interval, or count claims relies on S043; those are separate audit evidence, not CheckList figures.

## S047 — local selftest receipt

- Source: `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt`, version/path `attrib-calibration-selftest-v2`, frozen at base `f11bffbf` (no publication date applies; lesson/source-opening date is 2026-10-21).
- Exact final result line, source line 19: “selftest: 18 checks, 0 failed”; line 20 says `exit=0`. The quote is word-for-word with `corpus/lessons/round-26.md:51` and `corpus/evidence/round26-sources/gate.md:9`.
- Local SHA-256: `75db30f95088b9aa859cf80cc48430a13a3d42adb446410920413f9647f05f29`. `git show f11bffbf:corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt | sha256sum` returned the same hash (exit 0); the local source is byte-identical to the cited base source. The `18` checks and `0` failures are supported; S047 does not support other draft numbers and is not cited in the draft.

## Commands/evidence

- `pdfinfo /tmp/fxsource-s043.pdf` reported title/author and `Pages: 11`, `CreationDate: Mon Jun 8 19:01:05 2020 -03` (exit 0).
- `pdftotext -f 2 -l 2 -layout /tmp/fxsource-s043.pdf /tmp/fxsource-s043-p2.txt && pdftotext -f 3 -l 3 -layout /tmp/fxsource-s043.pdf /tmp/fxsource-s043-p3.txt` (exit 0). Reading p2 shows footer 4903 and no quote; p3 shows §2.2 and quote at lines 48–50, footer 4904.
- `sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt` returned the local hash above (exit 0).
- No tools installed.

VERDICT: PARTIAL — S043 substantively supports the draft's limited prior-art distinction, and S047 exactly supports the cited 18-check/0-failed correction; however, the S043 exact location is misstated in both Gate/source receipt (p.4903 rather than p.4904), so this source package is not clean for admission until corrected. This is only the assigned source/number re-read; Q13/other admission criteria are not assessed here.
## Post-correction re-read (2026-10-21)

- Re-read the added S048 registry row (`corpus/SOURCES.md:70`), the pre-admission source-receipt correction (`corpus/evidence/round26-sources/gate.md:32-41`), the lesson correction (`corpus/lessons/round-26.md:57-66`), and updated draft citations (`.ufo/waves/round-26/drafts/grader-perturbation-audit.md:1,17-21`).
- S048 records the same independently reopened URL, HTTP 200 and SHA-256, exact 21-word quote, and corrected §2.2 location PDF p.3 / proceedings p.4904. The lesson and source-receipt addenda explicitly supersede the historical S043 p.2 / p.4903 location without rewriting that immutable row; the draft now cites S048 at the corrected location.
- S047's local hash, base identity, exact result line, and supported numbers remain as checked above. No draft numeric claim is made dependent on S043/S048.
- The original `VERDICT: PARTIAL` above is preserved as the finding before correction. The named S048 correction closes that source-location defect for the current draft. This addendum assesses only the source/number criterion; Q13 and other admission criteria remain unassessed.

VERDICT (updated source/number criterion): PASS — the current draft's S048 citation is accurately located and supports its scoped prior-art distinction; S047's cited 18 checks / 0 failures is exact. This is not a full admission verdict.