"""In-memory probe of plans/gate_timing_check.audit_admission; no Git, no production writes."""
import hashlib
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[5]
sys.dont_write_bytecode = True
sys.path.insert(0, str(LANE / "plans"))
import gate_timing_check as g  # noqa: E402

DRAFT = LANE / ".ufo/waves/round-28/drafts/webarena-task-spec-audit.md"
draft = DRAFT.read_text(encoding="utf-8")
draft_sha = hashlib.sha256(DRAFT.read_bytes()).hexdigest()
canon = "corpus/knowledge/webarena-task-spec-audit.md"
rep = ".ufo/waves/round-28/falsify/FFullEntry.md"
members = {("falsify", "FFullEntry"): g.SeatMember("reviewer", "KengakuR28.FFullEntry")}


def run(label, cand_cell, report_text, entry_text=draft, reason=None):
    blobs = {canon: entry_text, rep: report_text}
    tree = {canon: g.TreeFile("100644", len(entry_text)), rep: g.TreeFile("100644", len(report_text))}
    reason = reason or f"Q10 `{rep}` sha256 {draft_sha}"
    adm = g.GateAdmission(1, cand_cell, "admit", reason, "")
    r = g.audit_admission(adm, 28, tree, members, blobs.get)
    print(f"{label}: ok={r.ok} invalid={list(r.invalid_second)} reasons={list(r.reasons)} generic={list(r.generic)}")


good = f"Re-read {canon}\nsha256 {draft_sha}\nVERDICT: PASS\n"
run("A digest-matching PASS", "knowledge/webarena-task-spec-audit.md", good)
run("B VERDICT FAIL accepted?", "knowledge/webarena-task-spec-audit.md",
    f"Re-read {canon}\nVERDICT: FAIL\n")
run("C report digest != admitted bytes", "knowledge/webarena-task-spec-audit.md",
    f"Re-read {canon}\nsha256 {'0'*64}\nVERDICT: PASS\n")
mutated = draft.replace("812 /812", "813 /813", 1)
print("mutant differs:", mutated != draft, hashlib.sha256(mutated.encode()).hexdigest())
run("D admitted bytes changed after re-read", "knowledge/webarena-task-spec-audit.md", good, entry_text=mutated)
run("E report quotes frontmatter line-start", "knowledge/webarena-task-spec-audit.md",
    f"Re-read {canon}\n```\nwriter: KengakuR28\n```\nVERDICT: PASS\n")
run("F Gate candidate cell keeps ' draft' suffix", "knowledge/webarena-task-spec-audit.md draft", good)
run("G report names only draft path", "knowledge/webarena-task-spec-audit.md",
    f"Re-read .ufo/waves/round-28/drafts/webarena-task-spec-audit.md\nVERDICT: PASS\n")
run("H reason with 'second seats' phrase", "knowledge/webarena-task-spec-audit.md", good,
    reason=f"Q10 `{rep}` plus second seats")
