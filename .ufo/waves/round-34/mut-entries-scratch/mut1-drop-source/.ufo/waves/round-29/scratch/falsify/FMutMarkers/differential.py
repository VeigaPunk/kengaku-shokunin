"""Differential probes and random differential over /tmp mutant copies (FMutMarkers).

Reads only /tmp/fmut-markers/<variant>/plans/config_projection.py copies; never the lane.
Each copy is a single-line mutant of the control copy (see the report for the exact lines).
"""
import importlib.util, json, random

BASE = "/tmp/fmut-markers"
VARIANTS = ["control", "m1-census", "m1b-global", "m2-order", "m2b-project", "m2c-census", "m2d-decoded", "m2e-occ", "m2f-changed"]


def load(v):
    spec = importlib.util.spec_from_file_location("cp_" + v.replace("-", "_"), f"{BASE}/{v}/plans/config_projection.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mods = {v: load(v) for v in VARIANTS}
SIX = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKS6 = ["__%s__" % n for n in SIX]
TOKS = TOKS6 + ["__last_url__", "__page__"]


def run(mod, raw, profiles):
    try:
        res, findings = mod.audit_text(raw, profiles)
        return {"ok": True, "res": res, "findings": findings}
    except Exception as error:
        return {"ok": False, "exc": type(error).__name__ + ": " + str(error)[:120]}


def ids(r):
    return sorted(f["id"] for f in r["findings"]) if r.get("ok") else ["EXC " + r["exc"]]


probes = {
    "P1_escaped_WIKIPEDIA_literal_in_raw": (r'[{"task_id":0,"intent":"\u005f\u005fWIKIPEDIA__"}]', {n: "http://v.invalid" for n in SIX}),
    "P2_literal_WIKIPEDIA_from_MAP_value": ('[{"task_id":0,"start_url":"__MAP__/x"}]', dict({n: "http://v.invalid" for n in SIX}, MAP="http://wiki.invalid/__WIKIPEDIA__")),
    "P3_escaped_WIKIPEDIA_from_MAP_value": ('[{"task_id":0,"start_url":"__MAP__/x"}]', dict({n: "http://v.invalid" for n in SIX}, MAP=r"\u005f\u005fWIKIPEDIA__")),
    "P4_runtime_marker_only": ('[{"task_id":0,"start_url":"__last_url__"}]', {n: "http://v.invalid" for n in SIX}),
    "P5_clean_control": ('[{"task_id":0,"start_url":"__GITLAB__/x"}]', {n: "http://v.invalid" for n in SIX}),
}
probe_table = {}
for pname, (raw, vals) in probes.items():
    profiles = {"p": {"purpose": "probe", "values": vals}}
    probe_table[pname] = {v: ids(run(mods[v], raw, profiles)) for v in VARIANTS}

rng = random.Random(29)
PIECES = TOKS + [r"\u005f\u005fWIKIPEDIA__", r"\u005f\u005fMAP__", r"\u005f\u005fGITLAB__", "a", "x y", "/p", "/", "_", "é", r"\n", r"\"", r"\\", "0", "__"]
VALS = ["http://v.invalid", "__MAP__", "__WIKIPEDIA__", "__GITLAB__", "/q", "", r"\u005f\u005fWIKIPEDIA__", r"\u005f\u005fMAP__", "x__page__", "__last_url__"]


def rstr():
    return "".join(rng.choice(PIECES) for _ in range(rng.randint(0, 4)))


def rdoc():
    tasks = []
    for i in range(rng.randint(1, 3)):
        fields = ['"task_id":%d' % i, '"start_url":"%s"' % rstr(), '"intent":"%s"' % rstr()]
        if rng.random() < 0.2:
            fields.append('"%s":"%s"' % (rng.choice(TOKS), rstr()))
        tasks.append("{" + ",".join(fields) + "}")
    return "[" + ",".join(tasks) + "]"


trials, invalid = 0, 0
prop_viol = {"text_gt_decoded": 0, "text_pos_decoded_zero": 0, "checked": 0}
stats = {v: {"findings_diff": 0, "result_diff": 0, "exception": 0} for v in VARIANTS[1:]}
examples = {v: [] for v in VARIANTS[1:]}
for _ in range(3000):
    raw = rdoc()
    try:
        json.loads(raw)
    except ValueError:
        invalid += 1
        continue
    trials += 1
    profiles = {"p": {"purpose": "fuzz", "values": {n: rng.choice(VALS) for n in SIX}}}
    base = run(mods["control"], raw, profiles)
    if base["ok"]:
        profile = base["res"]["profiles"].get("p", {})
        rt, rd = profile.get("remaining_known_tokens_text"), profile.get("remaining_known_tokens_decoded")
        if rt is not None and rd is not None:
            prop_viol["checked"] += 1
            for tok in TOKS6:
                prop_viol["text_gt_decoded"] += rt[tok] > rd[tok]
                prop_viol["text_pos_decoded_zero"] += (rt[tok] > 0 and rd[tok] == 0)
    for v in VARIANTS[1:]:
        r = run(mods[v], raw, profiles)
        if not r["ok"]:
            stats[v]["exception"] += 1
            continue
        if ids(r) != ids(base):
            stats[v]["findings_diff"] += 1
            if len(examples[v]) < 2:
                examples[v].append({"raw": raw[:160], "control": ids(base), "variant": ids(r)})
        if json.dumps(r["res"], sort_keys=True, default=str) != json.dumps(base["res"], sort_keys=True, default=str):
            stats[v]["result_diff"] += 1

print("random trials valid:", trials, "invalid skipped:", invalid)
print("control property (six tokens): checked", prop_viol["checked"], "text>decoded", prop_viol["text_gt_decoded"], "text>0&decoded==0", prop_viol["text_pos_decoded_zero"])
for v in VARIANTS[1:]:
    print(" ", v, json.dumps(stats[v], sort_keys=True))
for v in VARIANTS[1:]:
    for ex in examples[v][:1]:
        print(" example", v, json.dumps(ex, ensure_ascii=True)[:400])
for pname, row in probe_table.items():
    print(" ", pname, json.dumps(row, sort_keys=True))
