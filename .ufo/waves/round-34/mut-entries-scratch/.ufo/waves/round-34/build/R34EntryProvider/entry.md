---
title: Provider self-reports and evaluation limits
source: S108, S109
verified-at: 2026-10-25
recheck: 180d; re-open NEC at its next journal issue and verify the archived METI capture remains available
---

# Provider self-reports: keep the caveat beside the score

These sources teach how to read evaluation claims, not how to rank the models. Both are reports by the organizations whose programmes or models are being described. Treat their statements as self-reports: an official page is primary evidence of what its publisher says, not independent confirmation that its protocol worked as intended or that its reported scores generalize.

## NEC: RAKUDA measures one facet

NEC's own technical-journal article describes RAKUDA as a Japanese-language benchmark for its model and places a limitation alongside that evaluation: 「対話性能の一側面しか測れていない」 (NEC技報 Vol.75 No.2, 2024-03; S108). NEC's fuller caveat is that the benchmark evaluates one-turn dialogue with few data. The practical lesson is not to detach the score from the publisher's own boundary: a one-turn, small-data result is evidence about one facet of conversational performance, not dialogue ability as a whole.

This remains NEC's self-report about its own system and benchmark framing. It does not independently establish the quality of the benchmark, the accuracy of the score, or performance beyond that stated scope.

## METI: hold-out procedure and named benchmarks

In its phase-1 results page, METI says it collaborated with Weights & Biases to generate and evaluate held-out data, described as private data for final evaluation and completely unknown test data intended to support fairness. The archived page names the Japanese benchmarks Jaster-GENIAC-v0.1 and JMT-Bench-GENIAC-v0.1; it also names MMLU-GENIAC-v0.1 and MT-Bench-GENIAC-v0.1 for English evaluation (S109). The page dates these results “as of August 2024.” The protocol description and benchmark names are the programme's own account, not an independent audit of hold-out construction, access control, or execution.

The METI original page is withdrawn; the pinned source is the Internet Archive snapshot from 2025-11-18, not any current live-page state. The captured Japanese section states: 「完全に未知なテストデータを用いて性能評価を行うことが重要」 and identifies cooperation with Weights and Biases and hold-out data. (S109; archived capture, § 性能評価結果（日本語）, retrieved 2026-10-25.)

## Reading rule

A publisher's score page can disclose its own limitation right beside the score; preserve that caveat when citing the result. A programme's own protocol account can establish what it says it did and which benchmarks it names; do not silently upgrade that to independent verification. Label both explicitly as self-reports.

**Negative space:** This entry makes no claim about either model's actual performance, comparative standing, or score correctness. It asserts no live page state: NEC's page is live, while METI's original is withdrawn and the archive snapshot is the pin. It does not independently verify the underlying data, hold-out separation, or evaluation execution.
