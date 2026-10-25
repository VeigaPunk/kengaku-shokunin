#!/usr/bin/env python3
"""In-memory probe of plans/gate_timing_check.audit_admission (no git, no writes).

Each case builds a synthetic round-29 falsify tree in memory and records whether the
unchanged Q13 structural function would count the cited report as returned support.
"""
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
spec = importlib.util.spec_from_file_location("gtc", f"{LANE}/plans/gate_timing_check.py")
gtc = importlib.util.module_from_spec(spec)
sys.modules["gtc"] = gtc
spec.loader.exec_module(gtc)

ROUND = 29
CAND = "knowledge/webarena-config-projection.md"
DRAFT = ".ufo/waves/round-29/drafts/webarena-config-projection.md"
REPORT = ".ufo/waves/round-29/falsify/FEntrySeat.md"
FINAL_ENTRY = "writer: R29DraftEntry\n# final bytes\n"
STALE_ENTRY = "writer: R29DraftEntry\n# earlier draft bytes\n"
FINAL_SHA = hashlib.sha256(FINAL_ENTRY.encode()).hexdigest()
STALE_SHA = hashlib.sha256(STALE_ENTRY.encode()).hexdigest()

MEMBERS = {("falsify", "FEntrySeat"): gtc.SeatMember("reviewer", "KengakuR28.FEntrySeat-3")}

CASES = [
    ("C0 control: plain PASS, canonical path, final digest",
     f"Re-read {CAND} sha256 {FINAL_SHA}\nVERDICT: PASS\n", None),
    ("C1 FAIL-only verdict",
     f"Re-read {CAND} sha256 {FINAL_SHA}\nVERDICT: FAIL\n", None),
    ("C2 PARTIAL-only verdict",
     f"Re-read {CAND} sha256 {FINAL_SHA}\nVERDICT: PARTIAL\n", None),
    ("C3 echoed contract template, no judgment",
     f"Assigned {CAND}.\nVERDICT: PASS/PARTIAL/FAIL\n", None),
    ("C4 PASS bound to stale digest, final bytes differ",
     f"Re-read {CAND} sha256 {STALE_SHA}\nVERDICT: PASS\n", None),
    ("C5 earlier PASS then final FAIL",
     f"Re-read {CAND}\nVERDICT: PASS\n\n## Later pass on final bytes {FINAL_SHA}\nVERDICT: FAIL\n", None),
    ("C6 PASS only inside fenced code (quoted example)",
     f"Re-read {CAND}\n```\nVERDICT: PASS\n```\n", None),
    ("C7 heading-form PASS only (r28 M85 shape)",
     f"Re-read {CAND} sha256 {FINAL_SHA}\n### VERDICT: PASS\n", None),
    ("C8 names draft path only, plain PASS",
     f"Re-read {DRAFT} sha256 {FINAL_SHA}\nVERDICT: PASS\n", None),
    ("C9 control PASS, Gate prose says 'second seat' with a space",
     f"Re-read {CAND} sha256 {FINAL_SHA}\nVERDICT: PASS\n",
     f"Q10 `{REPORT}`; exact bytes re-read by the second seat."),
]


def run(label, report_text, reason):
    reason = reason or f"Q10 `{REPORT}` returned for sha256 `{FINAL_SHA}`."
    blobs = {CAND: FINAL_ENTRY, REPORT: report_text}
    tree = {REPORT: gtc.TreeFile("100644", len(report_text.encode()))}
    admission = gtc.GateAdmission(1, CAND, "admit", reason, "")
    result = gtc.audit_admission(admission, ROUND, tree, MEMBERS, blobs.get)
    return {
        "case": label,
        "q13_structural_ok": result.ok,
        "anchored_verdicts": gtc.VERDICT_RE.findall(report_text),
        "report_has_final_sha": FINAL_SHA in report_text,
        "reasons": list(result.reasons),
        "invalid": [r for _, r in result.invalid_second],
        "generic": list(result.generic),
    }


out = [run(*case) for case in CASES]
print(json.dumps({"final_sha": FINAL_SHA, "stale_sha": STALE_SHA, "cases": out}, indent=1))
