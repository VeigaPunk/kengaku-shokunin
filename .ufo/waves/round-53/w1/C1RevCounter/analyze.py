#!/usr/bin/env python3
"""Read-only analysis of plans/round53_c1_triage.py vs the frozen predicate (no edits)."""
import json, re, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin").resolve()
sys.path.insert(0, str(LANE / "plans"))
import round53_c1_triage as T  # noqa: E402

out = {}

# --- leg 1 on the real tree -------------------------------------------------
ok, L = T.leg_pins(LANE, T.CFG)
out["leg_pins_real"] = {"ok": ok, "lines": L}

# --- never-read blocklist: literal vs regex ---------------------------------
r52_conf, texts = T.never_read_blocklist(LANE, T.CFG)
out["blocklist_files"] = sorted(texts.keys())
out["r52_confirmed_tasks"] = sorted(r52_conf)

pop = json.loads((LANE / "plans/round52-tasks.json").read_text())
tasks = sorted(pop["tasks"])
lit, rgx = [], []
for t in tasks:
    if any(t in txt for txt in texts.values()):
        lit.append(t)
    if T.seen_before(t, texts):
        rgx.append(t)
out["tasks_never_read_literal"] = len(tasks) - len(lit)
out["tasks_never_read_regex"] = len(tasks) - len(rgx)
out["regex_misses_literal_hits"] = sorted(set(lit) - set(rgx))

# how many of the regex-never-read tasks would be hidden inside a longer token
extra = []
for t in sorted(set(rgx) & set(lit)):
    for f, txt in texts.items():
        for m in re.finditer(re.escape(t), txt):
            a, b = m.start(), m.end()
            before = txt[a - 1] if a else ""
            after = txt[b] if b < len(txt) else ""
            extra.append((t, f, repr(before), repr(after), txt[max(0, a - 30):b + 30].replace("\n", "|")))
out["regex_miss_examples"] = extra[:20]

# --- oracle leg shape (labels absent at this tip -> expected absent) --------
out["labels_file_exists"] = (LANE / "corpus/evidence/round53/oracle-labels.json").is_file()
out["freeze_file_exists"] = (LANE / "plans/round53-c1-freeze.json").is_file()
out["classifier_exists"] = (LANE / "plans/round53_c1_classify.py").is_file()
out["confirmations_exists"] = (LANE / "corpus/evidence/round53/confirmations.json").is_file()
out["prior_art_exists"] = (LANE / "corpus/evidence/round53/prior-art.json").is_file()

# --- url_key collapse behaviour --------------------------------------------
uk = T.url_key
samples = ["https://Ex.com/A", "https://ex.com/a", "https://ex.com/a/", "https://ex.com/a?x=1",
           "https://ex.com/a#frag", "https://ex.com/a?x=1#f", "http://ex.com/a"]
out["url_key"] = [(u, uk(u)) for u in samples]

# --- quote word counting ----------------------------------------------------
out["quote_word_counts"] = {
    "8 words": len("a b c d e f g h".split()),
    "25 words": len(" ".join(str(i) for i in range(25)).split()),
    "26 words": len(" ".join(str(i) for i in range(26)).split()),
    "7 words": len("a b c d e f g".split()),
}

print(json.dumps(out, indent=1, default=str))
