# R34ReviewRowsQuarantine — second-seat review

**Axis:** coverage. Reviewed the frozen §10 admission rule in `plans/round-34-claims.md` (lines 125–133), the two named capture files, and the proposed provider entry. The requested `build/R34RowsQuarantine/append-rows.md` is absent; therefore no row payloads exist here to validate exact ID/anchor encoding or registry shape.

## Row-level verdicts

- **S108 (staged S091 / NEC): defect — do not adopt.** The source capture `assimilation/captures/nec-s091.html` lines 1–10 is an Akamai Access Denied page, not the NEC article. `build/R34CaptureNec.md` lines 5–15 records the retrieval command, 418-byte result, and states no article/quote was retrieved. Thus no anchor was located this round, regardless of the draft entry's quoted phrase. The §10 frozen rule explicitly refuses a row whose quote is absent from the captured bytes. Entry claim in `build/R34EntryProvider/entry.md` line 14 is unsupported by the actual capture.
- **S109 (staged S105 / METI): evidence supports admit, but no append row to approve.** Capture `assimilation/captures/geniac-s105.html` line 112, within the heading at line 111, contains both the hold-out procedure and the two Japanese benchmark names; `build/R34CaptureGeniac.md` lines 4–9 records retrieval, digest, target-found check, and located passage. The anchor actually evidenced is the capture's line-112 sentence(s), in section `性能評価結果（日本語）(※2024年８月時点)`. However the designated `append-rows.md` does not exist, so its S109 record cannot be checked for exact quote, URL/revision, anchor, and tier-B caveat.

## Scope honesty

The provider entry appropriately limits both sources as publisher/program self-reports and explicitly disclaims independent verification (`build/R34EntryProvider/entry.md` lines 10, 16, 20, 22, 26–28). Its METI wording attributes the hold-out description and benchmark names to METI and notes the original page is withdrawn (lines 20–22). The available quote supports only what the page says; it does not verify actual hold-out separation or evaluation execution. The NEC scope caveat cannot cure its absent source payload. The required `no-DOI` tier-B qualifier cannot be confirmed from an absent row payload; do not infer that it is present.

## Evidence commands / outputs

- `read .../assimilation/captures/nec-s091.html` → Access Denied HTML, lines 1–10.
- `read .../build/R34CaptureNec.md` → records curl URL, 418-byte output and absent article passage (lines 5–15).
- `read .../assimilation/captures/geniac-s105.html:104-122` → capture line 112 gives hold-out and benchmark statements.
- `read .../build/R34CaptureGeniac.md` → records URL, size/hash, target-found result, located quote (lines 4–9).
- `read .../build/R34EntryProvider/entry.md` → scope and self-report limitations (lines 10, 16, 20–28).
- `read .../build/R34RowsQuarantine/append-rows.md` → `Path ... not found`.

**VERDICT: review-rows-quarantine (2/2 defect)**