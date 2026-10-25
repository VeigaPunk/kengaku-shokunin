"""Final stage: per-occurrence CSV, per-task re-serialization deltas, set overlap."""
import csv
import json
import sys
from collections import Counter

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenShopping-2")
import census_shopping as C

raw = open(C.RAW, "rb").read()
text = raw.decode("utf-8")
parser = C.SpanParser(text).parse()
data = json.loads(text)
prof = json.loads(open(C.PROFILES, "rb").read().decode("utf-8"))
TOKEN = C.TOKEN

leaves = []
for lit in parser.literals:
    if lit["role"] == "value" and TOKEN in lit["decoded"]:
        leaves.append(lit)
print("token_leaves", len(leaves))
print("occ_from_leaves", sum(l["decoded"].count(TOKEN) for l in leaves))

rows = []
for lit in leaves:
    v = lit["decoded"]
    pos = v.find(TOKEN)
    n = 0
    while pos != -1:
        n += 1
        rows.append(dict(path=lit["path"], top=lit["top"], task_id=ids[lit["top"]] if False else None,
                         key=lit["key"], raw_cp=lit["start"] + pos,
                         dec_cp_in_value=pos, occ_in_value=n, value_len=len(v),
                         value_class=("token_only" if v == TOKEN else "token_plus_path"),
                         next_char=v[pos + len(TOKEN):pos + len(TOKEN) + 1],
                         line=text.count("\n", 0, lit["start"] + pos) + 1))
        pos = v.find(TOKEN, pos + 1)
rows.sort(key=lambda r: r["raw_cp"])
for r in rows:
    r["task_id"] = data[r["top"]]["task_id"]

# profile deltas and projected offsets (SHOPPING-only substitution, ordered occurrences)
for pname in prof:
    v = prof[pname]["values"]["SHOPPING"]
    delta = len(v) - len(TOKEN)
    for k, r in enumerate(rows):
        r["delta_" + pname] = delta
        r["proj_cp_" + pname] = r["raw_cp"] + k * delta
        r["proj_cp_plus_window_" + pname] = r["raw_cp"] + k * delta + delta

cols = ["path", "top", "task_id", "key", "value_class", "value_len", "next_char",
        "line", "raw_cp", "dec_cp_in_value", "occ_in_value"]
for pname in prof:
    cols += ["delta_" + pname, "proj_cp_" + pname, "proj_cp_plus_window_" + pname]
out = C.LANE + "/.ufo/waves/round-29/scratch/KengakuR28.R29TokenShopping-2/occurrences_shopping.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print("csv_rows", len(rows), "csv_path", out)

# ordered projected offsets must be monotone and forward formula equal span parser result
for pname in prof:
    v = prof[pname]["values"]["SHOPPING"]
    delta = len(v) - len(TOKEN)
    projected = text.replace(TOKEN, v)
    psp = C.SpanParser(projected).parse()
    pstarts = [s for s, e, i in psp.top]
    occ_per_task = Counter(r["top"] for r in rows)
    base = [s for s, e, i in parser.top]
    shift = 0
    ok = True
    for t in range(812):
        if pstarts[t] != base[t] + shift:
            ok = False
        shift += occ_per_task.get(t, 0) * delta
    print("PROFILE", pname, "occurrence_csv_projected_offsets_monotone",
          all(rows[i]["proj_cp_" + pname] < rows[i + 1]["proj_cp_" + pname]
              for i in range(len(rows) - 1)),
          "task_start_formula_match", ok,
          "occurrence_offsets_in_projected_text_match",
          all(projected[r["proj_cp_" + pname]:r["proj_cp_" + pname] + len(v)] == v
              for r in rows))

# per-task upstream re-serialization (json.dump(item, indent=2)) length deltas
print("\n== upstream per-task re-serialization deltas ==")
for pname in prof:
    v = prof[pname]["values"]["SHOPPING"]
    delta = len(v) - len(TOKEN)
    mism = 0
    total = 0
    per_task = {}
    for t, item in enumerate(data):
        base_s = json.dumps(item, indent=2)
        # apply the governed string replacement to every string leaf of this task
        def rew(x):
            if isinstance(x, str):
                return x.replace(TOKEN, v)
            if isinstance(x, list):
                return [rew(y) for y in x]
            if isinstance(x, dict):
                return {k: rew(y) for k, y in x.items()}
            return x
        proj_s = json.dumps(rew(item), indent=2)
        d = len(proj_s) - len(base_s)
        n = sum(1 for r in rows if r["top"] == t)
        if d != n * delta:
            mism += 1
        total += d
        per_task[t] = d
    print("PROFILE", pname, "per_task_delta_mismatch", mism,
          "sum_delta_chars", total, "expected", len(rows) * delta)

# set overlap: token tasks vs lowercase-word tasks
word_re = __import__("re").compile(r"(?<![A-Za-z_])shopping(?![A-Za-z_])")
low_tasks = set()
for lit in parser.literals:
    if lit["role"] == "value" and word_re.search(lit["decoded"]):
        low_tasks.add(lit["top"])
tok_tasks = {r["top"] for r in rows}
print("\nlowercase_word_tasks", len(low_tasks), "token_tasks", len(tok_tasks))
print("overlap", len(low_tasks & tok_tasks),
      "lower_only", len(low_tasks - tok_tasks), "token_only", len(tok_tasks - low_tasks))
print("lowercase_word_fields", dict(Counter(
    lit["key"] for lit in parser.literals
    if lit["role"] == "value" and word_re.search(lit["decoded"]))))
print("lowercase_word_sample_values", [
    (lit["path"], lit["decoded"][:60])
    for lit in parser.literals
    if lit["role"] == "value" and word_re.search(lit["decoded"])][:4])

# all token occurrences in URL-valued fields? observe value classification by key
print("\nkey_by_class", dict(Counter((r["key"], r["value_class"]) for r in rows)))
print("first_row", {k: rows[0][k] for k in cols[:11]})
print("last_row", {k: rows[-1][k] for k in cols[:11]})
print("max_occ_in_value", max(r["occ_in_value"] for r in rows))
print("rows_with_occ_gt_1", [(r["path"], r["occ_in_value"]) for r in rows if r["occ_in_value"] > 1][:12])
