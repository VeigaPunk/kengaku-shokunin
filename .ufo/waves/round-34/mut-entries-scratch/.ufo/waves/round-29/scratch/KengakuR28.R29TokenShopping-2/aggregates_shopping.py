"""Second-stage aggregates for the __SHOPPING__ token census (same scratch scope)."""
import json
import re
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenShopping-2")
import census_shopping as C

raw = open(C.RAW, "rb").read()
text = raw.decode("utf-8")
parser = C.SpanParser(text).parse()
data = json.loads(text)
ids = [d["task_id"] for d in data]
TOKEN = C.TOKEN
occ = []
for lit in parser.literals:
    if lit["role"] != "value":
        continue
    v = lit["decoded"]
    if TOKEN not in v:
        continue
    strings = [l for l in parser.literals if l is lit]
    pos = v.find(TOKEN)
    n = 0
    while pos != -1:
        n += 1
        cls = "url_token_only" if v == TOKEN else ("url_prefix_embedded" if re.match(r"^https?://", v) is None and v.startswith(TOKEN) else "other")
        occ.append(dict(path=lit["path"], top=lit["top"], key=lit["key"], cls=cls,
                        pos=pos, raw=lit["start"] + pos, val=v,
                        nxt=v[pos + len(TOKEN):pos + len(TOKEN) + 1],
                        n_in_value=n))
        pos = v.find(TOKEN, pos + 1)
print("occurrences", len(occ))

# histograms
from collections import Counter, defaultdict
print("class_totals", dict(Counter(o["cls"] for o in occ)))
print("key_totals", dict(Counter(o["key"] for o in occ)))
print("role_totals", dict(Counter(l["role"] for l in parser.literals
                                  if TOKEN in l["decoded"])))
per_task = Counter(o["top"] for o in occ)
print("occ_per_task_histogram", dict(sorted(Counter(per_task.values()).items())))
per_leaf = Counter(o["path"] for o in occ)
print("occ_per_leaf_histogram", dict(sorted(Counter(per_leaf.values()).items())))
print("tasks_total", len(per_task), "leaves_total", len(per_leaf),
      "occ_total", sum(per_task.values()))

# contiguous task ranges
ranges = []
cur = None
for t in sorted(per_task):
    if cur and t == cur[1] + 1:
        cur[1] = t
        cur[2] += per_task[t]
        cur[3] += 1
    else:
        if cur:
            ranges.append(cur)
        cur = [t, t, per_task[t], 1]
ranges.append(cur)
print("task_ranges", [(a, b, occ_, ntask) for a, b, occ_, ntask in ranges])
print("range_count", len(ranges))

# next-char classes
print("next_char_after_token", dict(Counter(
    ("end_of_value" if o["nxt"] == "" else ("slash" if o["nxt"] == "/" else "other:" + o["nxt"]))
    for o in occ)))
print("token_only_with_next", [(o["path"], o["nxt"]) for o in occ if o["cls"] == "url_token_only" and o["nxt"] != ""])
print("embedded_first_chars", dict(Counter(o["nxt"] for o in occ if o["cls"] != "url_token_only")))

# lowercase word metadata census
word_re = re.compile(r"(?<![A-Za-z_])shopping(?![A-Za-z_])")
low = []
for lit in parser.literals:
    if lit["role"] != "value":
        continue
    for m in word_re.finditer(lit["decoded"]):
        low.append((lit["path"], lit["top"], lit["decoded"]))
print("lowercase_word_count", len(low))
print("lowercase_word_paths_distinct", len({p for p, t, v in low}))
print("lowercase_word_tasks", len({t for p, t, v in low}))
print("lowercase_word_value_starts_http",
      sum(1 for p, t, v in low if v.startswith("http")))
print("lowercase_word_example_paths", sorted({p.split(".")[1] for p, t, v in low}))
ex = [x for x in low if TOKEN not in x[2]][:3]
print("lowercase_word_examples", [(p, json.dumps(v[:80])) for p, t, v in ex])

# placeholder inventory (guard only)
inv = Counter(re.findall(r"__[A-Z][A-Z_]*?__", text))
print("placeholder_inventory_guard", dict(sorted(inv.items())))
print("token_upper_forms", dict(Counter(re.findall(r"__SHOPPING[A-Z_]*", text))))

# escape census restated
esc_lits = [l for l in parser.literals if "\\" in text[l["start"]:l["end"]]]
print("literals_with_backslash_total", len(esc_lits))
print("literal_literals_u005f", text.count("\\u005f"), text.count("\\u005F"))

# profiles: offset implication detail
prof = json.loads(open(C.PROFILES, "rb").read().decode("utf-8"))
order_occ = sorted(occ, key=lambda o: o["raw"])
print("\n== per-profile offset/span implication ==")
for pname, p in prof.items():
    v = p["values"]["SHOPPING"]
    delta = len(v) - len(TOKEN)
    projected = text.replace(TOKEN, v)
    psp = C.SpanParser(projected).parse()
    pstarts = [s for s, e, i in psp.top]
    pends = [e for s, e, i in psp.top]
    base_starts = [s for s, e, i in parser.top]
    base_ends = [e for s, e, i in parser.top]
    shift = 0
    shifts = []
    for t in range(len(base_starts)):
        shifts.append(shift)
        shift += per_task.get(t, 0) * delta
    print("PROFILE", pname, "value", json.dumps(v), "value_cp", len(v),
          "delta_per_occ", delta)
    print("  projected_len", len(projected), "base_len", len(text),
          "delta_total", len(projected) - len(text))
    print("  task_start_shifts_match", pstarts == [base_starts[t] + shifts[t] for t in range(812)])
    print("  task_end_shifts_match",
          pends == [base_ends[t] + shifts[t] + per_task.get(t, 0) * delta for t in range(812)])
    first_occ = order_occ[0]
    last_occ = order_occ[-1]
    # SHOPPING-only local shift for k-th occurrence = k*delta
    k_first = 0
    k_last = len(order_occ) - 1
    print("  first_occ_base_cp", first_occ["raw"],
          "shopping_only_projected_cp", first_occ["raw"] + k_first * delta,
          "path", first_occ["path"])
    print("  last_occ_base_cp", last_occ["raw"],
          "shopping_only_projected_cp", last_occ["raw"] + k_last * delta,
          "path", last_occ["path"])
    print("  max_task_occ", max(per_task.values()),
          "max_task_delta", max(per_task.values()) * delta)
    dist = Counter(per_task.values())
    print("  task_delta_distribution", {k: (v_, k * delta) for k, v_ in sorted(dist.items())})
    # boundary shape after substitution
    dbl = sum(1 for o in order_occ if o["cls"] != "url_token_only" and v.endswith("/") and o["nxt"] == "/")
    print("  double_slash_boundaries", dbl,
          "token_only_trailing_slash", sum(1 for o in order_occ
                                           if o["cls"] == "url_token_only" and v.endswith("/")))

# per-task projected spans for affected tasks (compact, profile A)
v = prof["distinct_origins"]["values"]["SHOPPING"]
delta = len(v) - len(TOKEN)
shift = 0
rows = []
for t in range(812):
    s, e, _ = parser.top[t]
    n = per_task.get(t, 0)
    if n:
        rows.append((t, ids[t], s + shift, e + shift + n * delta, n, n * delta))
    shift += n * delta
print("\naffected_first_rows", rows[:5])
print("affected_last_rows", rows[-5:])
print("affected_task_span_rows_total", len(rows))

# line numbers for sample occurrences + verify raw line contains token
print("\n== sample line verification ==")
for o in [order_occ[0], order_occ[len(order_occ)//2], order_occ[-1]]:
    line = text.count("\n", 0, o["raw"]) + 1
    line_text = text.splitlines()[line - 1]
    print("path", o["path"], "cp", o["raw"], "line", line,
          "line_has_token", line_text.count(TOKEN),
          "line_len", len(line_text))
