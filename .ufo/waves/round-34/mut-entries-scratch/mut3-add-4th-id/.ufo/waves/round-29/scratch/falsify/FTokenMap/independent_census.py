#!/usr/bin/env python3
"""Independent __MAP__ census. Reads only pinned inputs + instrument stdout/JSON.
Never reads or imports plans/config_projection.py."""
import hashlib
import json
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
MAN = LANE + "/plans/fixtures/r29/manifest.json"
INSTRUMENT = LANE + "/plans/config_projection.py"

OUT = {}

# ---------- pinned inputs, read once ----------
raw_bytes = open(RAW, "rb").read()
gen_bytes = open(GEN, "rb").read()
prof_bytes = open(PROF, "rb").read()
man_bytes = open(MAN, "rb").read()
raw_text = raw_bytes.decode("utf-8")
gen_text = gen_bytes.decode("utf-8")
profiles = json.loads(prof_bytes.decode("utf-8"))
manifest = json.loads(man_bytes.decode("utf-8"))

OUT["input_sha256"] = {
    "raw": hashlib.sha256(raw_bytes).hexdigest(),
    "generate_test_data_py": hashlib.sha256(gen_bytes).hexdigest(),
    "profiles": hashlib.sha256(prof_bytes).hexdigest(),
    "manifest": hashlib.sha256(man_bytes).hexdigest(),
}

# ---------- derive token order from generator TEXT (own regex, not AST lib) ----------
steps = []
for line in gen_text.splitlines():
    m = re.search(r'raw\s*=\s*raw\.replace\("(__[A-Z_]+__)"\s*,\s*([A-Za-z_]+)\)', line)
    if m:
        steps.append({"token": m.group(1), "name": m.group(2), "line": None})
for i, line in enumerate(gen_text.splitlines(), start=1):
    for s in steps:
        if s["token"] in line and s["line"] is None:
            s["line"] = i
tokens = [s["token"] for s in steps]
OUT["derived_steps"] = steps
OUT["manifest_replacement_order"] = manifest["replacement_order"]
OUT["order_matches_manifest_names"] = [s["name"] for s in steps] == manifest["replacement_order"]

# ---------- literal text census ----------
text_counts = {t: raw_text.count(t) for t in tokens}
OUT["raw_text_occurrences"] = text_counts
OUT["raw_text_occurrences_total"] = sum(text_counts.values())

# non-overlapping vs lookahead-overlapping, per token (self-overlap ambiguity)
def overlap_count(s, pat):
    return len(re.findall("(?=" + re.escape(pat) + ")", s))

OUT["self_overlap_ambiguity"] = {t: {"count": raw_text.count(t), "lookahead": overlap_count(raw_text, t)} for t in tokens}

# substring matrix between tokens
sub = {}
for a in tokens:
    for b in tokens:
        if a != b:
            sub[f"{a} in {b}"] = b.count(a)
OUT["token_substring_matrix_nonzero"] = {k: v for k, v in sub.items() if v}

# profile values: any token in any value, any value in any value, any value containing '__'
val_issues = []
for pname, pv in profiles.items():
    for name, val in pv["values"].items():
        for t in tokens:
            if t in val:
                val_issues.append({"profile": pname, "name": name, "contains_token": t, "value": val})
        if "__" in val:
            val_issues.append({"profile": pname, "name": name, "has_double_underscore": True, "value": val})
OUT["profile_value_token_collisions"] = val_issues
OUT["profile_value_map"] = {pn: pv["values"]["MAP"] for pn, pv in profiles.items()}

# lookalike census
lookalikes = ["__MAP", "MAP__", "__MAPS__", "_MAP_", "__map__", "__Map__", "MAP", "__last_url__", "__page__"]
OUT["lookalike_raw_counts"] = {p: raw_text.count(p) for p in lookalikes}

# ---------- mini JSON parser recording raw string spans + paths ----------
class P:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.leaves = []   # string values (not keys)
        self.keys = []     # string keys with span

    def ws(self):
        s, n = self.s, len(self.s)
        while self.i < n and s[self.i] in " \t\r\n":
            self.i += 1

    def val(self, tmpl, ptr, tidx):
        self.ws()
        c = self.s[self.i]
        if c == '"':
            start = self.i
            self.str_span()
            return None
        if c == "{":
            self.i += 1
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return
            while True:
                self.ws()
                kstart = self.i
                key, kend = self.str_span()
                self.keys.append({"key": key, "raw_start": kstart, "raw_end": kend})
                self.ws()
                assert self.s[self.i] == ":", (self.i, self.s[self.i - 30:self.i + 30])
                self.i += 1
                ctmpl = f"{tmpl}.{key}" if tmpl else key
                cptr = f"{ptr}/{key.replace('~', '~0').replace('/', '~1')}"
                self.val(ctmpl, cptr, tidx)
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "}", (self.i, self.s[self.i])
                self.i += 1
                return
        if c == "[":
            self.i += 1
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
                return
            idx = 0
            while True:
                self.val(f"{tmpl}[]", f"{ptr}/{idx}", tidx)
                idx += 1
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "]", (self.i, self.s[self.i])
                self.i += 1
                return
        # number / true / false / null
        m = re.match(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null", self.s[self.i:])
        assert m, (self.i, self.s[self.i:self.i + 30])
        self.i += m.end()

    def str_span(self):
        s = self.s
        start = self.i
        assert s[self.i] == '"'
        self.i += 1
        while True:
            c = s[self.i]
            if c == "\\":
                self.i += 2
                continue
            if c == '"':
                self.i += 1
                break
            self.i += 1
        return json.loads(s[start:self.i]), self.i

    def record_strings(self, tmpl, ptr, tidx):
        """Re-walk is unnecessary: this parser records strings inline; see val()."""


def parse_collect(text):
    """Return (value, leaves), leaves = string VALUES with path template/pointer/raw span."""
    p = P(text)
    leaves = []

    # custom walker duplicating structure but recording leaves
    def walk(tmpl, ptr, tidx):
        p.ws()
        c = p.s[p.i]
        if c == '"':
            start = p.i
            v, end = p.str_span()
            leaves.append({"task_index": tidx, "template": tmpl, "pointer": ptr,
                           "value": v, "raw_start": start, "raw_end": end})
            return v
        if c == "{":
            p.i += 1
            out = {}
            p.ws()
            if p.s[p.i] == "}":
                p.i += 1
                return out
            while True:
                p.ws()
                ks = p.i
                k, ke = p.str_span()
                p.keys.append({"key": k, "raw_start": ks, "raw_end": ke})
                p.ws()
                assert p.s[p.i] == ":"
                p.i += 1
                ctmpl = f"{tmpl}.{k}" if tmpl else k
                cptr = f"{ptr}/{k.replace('~', '~0').replace('/', '~1')}"
                out[k] = walk(ctmpl, cptr, tidx)
                p.ws()
                if p.s[p.i] == ",":
                    p.i += 1
                    continue
                assert p.s[p.i] == "}"
                p.i += 1
                return out
        if c == "[":
            p.i += 1
            out = []
            p.ws()
            if p.s[p.i] == "]":
                p.i += 1
                return out
            idx = 0
            while True:
                out.append(walk(f"{tmpl}[]", f"{ptr}/{idx}", tidx))
                idx += 1
                p.ws()
                if p.s[p.i] == ",":
                    p.i += 1
                    continue
                assert p.s[p.i] == "]"
                p.i += 1
                return out
        m = re.match(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null", p.s[p.i:])
        assert m
        lit = m.group(0)
        p.i += m.end()
        return json.loads(lit)

    p.ws()
    assert p.s[p.i] == "["
    p.i += 1
    p.ws()
    value = []
    if p.s[p.i] == "]":
        p.i += 1
    else:
        idx = 0
        while True:
            value.append(walk("", f"/{idx}", idx))
            idx += 1
            p.ws()
            if p.s[p.i] == ",":
                p.i += 1
                continue
            assert p.s[p.i] == "]"
            p.i += 1
            break
    p.ws()
    assert p.i == len(p.s), (p.i, len(p.s))
    return value, leaves, p.keys


orig_value, orig_leaves, orig_keys = parse_collect(raw_text)
OUT["orig_task_count"] = len(orig_value)
OUT["orig_string_leaf_count"] = len(orig_leaves)
OUT["orig_string_key_count"] = len(orig_keys)

# occurrences outside string values (keys or structural) - token chars never structural
key_hits = {t: sum(k["key"].count(t) for k in orig_keys) for t in tokens}
OUT["occurrences_in_keys"] = key_hits

# ---- occurrence census from decoded leaves + raw spans ----
orig_occ = {t: 0 for t in tokens}
orig_leaves_with = {t: 0 for t in tokens}
orig_leaves_multi = {t: 0 for t in tokens}
orig_tasks_with = {t: set() for t in tokens}
leaf_token_counts = {}  # (task_index,pointer) -> {token:count}
span_mismatch = []
map_orig_positions = []  # (task_index, pointer, template, raw_offset)
for lf in orig_leaves:
    counts = {t: lf["value"].count(t) for t in tokens}
    counts = {t: c for t, c in counts.items() if c}
    if counts:
        leaf_token_counts[(lf["task_index"], lf["pointer"])] = counts
    for t, c in counts.items():
        orig_occ[t] += c
        orig_leaves_with[t] += 1
        if c > 1:
            orig_leaves_multi[t] += 1
        orig_tasks_with[t].add(lf["task_index"])
    # raw span cross-check: raw slice must contain as many literal tokens as decoded value
    span = raw_text[lf["raw_start"]:lf["raw_end"]]
    for t in tokens:
        if span.count(t) != lf["value"].count(t):
            span_mismatch.append({"pointer": lf["pointer"], "token": t,
                                  "raw": span.count(t), "decoded": lf["value"].count(t)})
    for m in re.finditer(re.escape("__MAP__"), span):
        map_orig_positions.append({
            "task_index": lf["task_index"], "pointer": lf["pointer"],
            "template": lf["template"],
            "offset": lf["raw_start"] + m.start(),
        })
OUT["orig_occurrences_by_token_leaves"] = orig_occ
OUT["orig_leaves_with_token"] = orig_leaves_with
OUT["orig_leaves_multi_same_token"] = orig_leaves_multi
OUT["orig_tasks_with_token"] = {t: len(s) for t, s in orig_tasks_with.items()}
OUT["raw_span_vs_decoded_occurrence_mismatches"] = span_mismatch
OUT["orig_tasks_with_any_token"] = len({k[0] for k in leaf_token_counts})
OUT["map_orig_positions_count"] = len(map_orig_positions)
OUT["map_orig_task_count_check"] = len({p["task_index"] for p in map_orig_positions})
OUT["map_orig_template_hist"] = {}
for p in map_orig_positions:
    OUT["map_orig_template_hist"][p["template"]] = OUT["map_orig_template_hist"].get(p["template"], 0) + 1
OUT["map_per_task_occurrence_hist"] = {}
mm = {}
for p in map_orig_positions:
    mm[p["task_index"]] = mm.get(p["task_index"], 0) + 1
for v in mm.values():
    OUT["map_per_task_occurrence_hist"][str(v)] = OUT["map_per_task_occurrence_hist"].get(str(v), 0) + 1
OUT["orig_total_occurrences"] = sum(orig_occ.values())
OUT["orig_total_occurrences_vs_text"] = OUT["orig_total_occurrences"] - OUT["raw_text_occurrences_total"]

# per-leaf total-token multi-occurrence definitions
multi_any_token = sum(1 for c in leaf_token_counts.values() if any(v > 1 for v in c.values()))
multi_total = sum(1 for c in leaf_token_counts.values() if sum(c.values()) > 1)
OUT["leaves_multi_any_token"] = multi_any_token
OUT["leaves_multi_total_occurrences"] = multi_total
OUT["leaves_with_two_distinct_tokens"] = sum(1 for c in leaf_token_counts.values() if len(c) > 1)

# token followed by slash in raw text (junction sites), per token
junctions = {t: 0 for t in tokens}
for t in tokens:
    for m in re.finditer(re.escape(t), raw_text):
        end = m.end()
        if end < len(raw_text) and raw_text[end] == "/":
            junctions[t] += 1
OUT["tokens_followed_by_slash"] = junctions
OUT["tokens_followed_by_slash_total"] = sum(junctions.values())

# ---------- independent sequential projection per profile ----------
def sha(b):
    return hashlib.sha256(b).hexdigest()

prof_out = {}
for pname, pv in profiles.items():
    values = pv["values"]
    text = raw_text
    stage = []
    stage_counts_after = {}
    for s in steps:
        tok, name = s["token"], s["name"]
        cnt = text.count(tok)  # non-overlapping, same as str.replace application count
        stage.append({"token": tok, "name": name, "applied_replacements": cnt,
                      "map_count_at_stage": text.count("__MAP__")})
        text = text.replace(tok, values[name])
        stage_counts_after[name] = {t: text.count(t) for t in tokens}
    proj_value, proj_leaves, proj_keys = parse_collect(text)
    # leaf-by-leaf diff
    omap = {(l["task_index"], l["pointer"]): l for l in orig_leaves}
    pmap = {(l["task_index"], l["pointer"]): l for l in proj_leaves}
    if set(omap) != set(pmap):
        prof_out[pname] = {"leaf_path_set_mismatch": True,
                           "orig_only": len(set(omap) - set(pmap)), "proj_only": len(set(pmap) - set(omap))}
        continue
    changed = []
    changed_by_token = {t: 0 for t in tokens}
    changed_tasks_by_token = {t: set() for t in tokens}
    path_hist = {}
    cat_hist = {"url_field": 0, "non_url_field": 0}
    mult_multi_any = 0
    mult_multi_total = 0
    leaf_oracle_fail = []
    for key, olf in omap.items():
        plf = pmap[key]
        if olf["value"] == plf["value"]:
            continue
        occ = {}
        for t in tokens:
            c = olf["value"].count(t)
            if c:
                occ[t] = c
        toks = [t for t in tokens if t in occ]
        tmpl = olf["template"]
        cat = "url_field" if (tmpl == "start_url" or tmpl.endswith("url")) else "non_url_field"
        ent = {"pointer": key[1], "template": tmpl, "category": cat,
               "original": olf["value"], "projected": plf["value"], "tokens": toks,
               "occurrences": occ}
        changed.append(ent)
        if any(v > 1 for v in occ.values()):
            mult_multi_any += 1
        if sum(occ.values()) > 1:
            mult_multi_total += 1
        for t in toks:
            changed_by_token[t] += 1
            changed_tasks_by_token[t].add(key[0])
        path_hist[tmpl] = path_hist.get(tmpl, 0) + 1
        cat_hist[cat] += 1
        # leaf-rewrite oracle: sequential replace of decoded value
        exp = olf["value"]
        for s in steps:
            exp = exp.replace(s["token"], values[s["name"]])
        if exp != plf["value"]:
            leaf_oracle_fail.append({"pointer": key[1], "expected": exp, "observed": plf["value"]})
    prof_out[pname] = {
        "steps": stage,
        "stage_counts_after": stage_counts_after,
        "projected_text_sha256": sha(text.encode()),
        "parsed_task_count": len(proj_value),
        "string_leaf_count": len(proj_leaves),
        "changed_leaf_count": len(changed),
        "changed_task_count": len({c["pointer"].split("/")[1] for c in changed}),
        "changed_leaves_by_token": changed_by_token,
        "changed_tasks_by_token": {t: len(s) for t, s in changed_tasks_by_token.items()},
        "changed_leaves_by_path_template": path_hist,
        "changed_leaves_by_category": cat_hist,
        "changed_leaves_multi_any_token": mult_multi_any,
        "changed_leaves_multi_total": mult_multi_total,
        "leaf_rewrite_oracle_failures": leaf_oracle_fail,
        "remaining_known_tokens_text": {t: text.count(t) for t in tokens},
        "remaining_known_tokens_decoded": {t: sum(l["value"].count(t) for l in proj_leaves) for t in tokens},
        "map_changed_leaves": [c for c in changed if "__MAP__" in c["tokens"]],
        "changed": changed,
        "parsed": proj_value,
        "projected_text": text,
    }

OUT["profiles_independent"] = {k: {kk: vv for kk, vv in v.items()
                                   if kk not in ("changed", "parsed", "projected_text", "map_changed_leaves")}
                               for k, v in prof_out.items()}
OUT["map_changed_detail"] = {k: len(v.get("map_changed_leaves", [])) for k, v in prof_out.items()}

# ---------- instrument outputs ----------
summary = subprocess.run([sys.executable, INSTRUMENT, "--summary"], capture_output=True, text=True, cwd=LANE)
js = subprocess.run([sys.executable, INSTRUMENT, "--json"], capture_output=True, text=True, cwd=LANE)
OUT["instrument_summary_exit"] = summary.returncode
OUT["instrument_json_exit"] = js.returncode
d = json.loads(js.stdout)
OUT["instrument_json_findings"] = d["findings"]
OUT["instrument_raw_text_sha256"] = d["raw_text_sha256"]
OUT["instrument_manifest_sha256"] = d["manifest_sha256"]

# parse summary lines
sline = {}
for line in summary.stdout.splitlines():
    sline[line.split(" ", 1)[0]] = line
OUT["summary_lines_map"] = {k: v for k, v in sline.items() if "MAP" in v or k in
                            ("ORIGINAL_OCCURRENCES_BY_TOKEN", "TASKS_WITH_TOKEN", "POPULATION", "TOTAL")}
def parse_after(prefix, line):
    return line[len(prefix):].strip()

mismatches = []

def cmp(label, indep, prod, loc):
    if indep != prod:
        mismatches.append({"metric": label, "independent": indep, "instrument": prod, "location": loc})

# original occurrences & tasks
prod_occ = json.loads(parse_after("ORIGINAL_OCCURRENCES_BY_TOKEN ", sline["ORIGINAL_OCCURRENCES_BY_TOKEN"]))
prod_tasks = json.loads(parse_after("TASKS_WITH_TOKEN ", sline["TASKS_WITH_TOKEN"]))
cmp("ORIGINAL_OCCURRENCES_BY_TOKEN", orig_occ, prod_occ, "summary ORIGINAL_OCCURRENCES_BY_TOKEN")
cmp("TASKS_WITH_TOKEN", {t: len(s) for t, s in orig_tasks_with.items()}, prod_tasks, "summary TASKS_WITH_TOKEN")
cmp("occurrences_by_token_json_population", orig_occ,
    d["population"]["original_occurrences_by_token"], "json population.original_occurrences_by_token")
cmp("tasks_with_token_json_population", {t: len(s) for t, s in orig_tasks_with.items()},
    d["population"]["tasks_with_token"], "json population.tasks_with_token")
cmp("tasks_with_any_token", OUT["orig_tasks_with_any_token"], d["population"]["tasks_with_any_token"],
    "json population.tasks_with_any_token")
cmp("raw_text_sha256", OUT["input_sha256"]["raw"], d["raw_text_sha256"], "json raw_text_sha256")
cmp("manifest_sha256", OUT["input_sha256"]["manifest"], d["manifest_sha256"], "json manifest_sha256")
cmp("tokens_followed_by_slash_total", OUT["tokens_followed_by_slash_total"],
    d["population"].get("tokens_followed_by_slash"), "json population.tokens_followed_by_slash")

# per-profile scalar comparisons
for pname, pv in prof_out.items():
    prod = d["profiles"][pname]
    loc = f"json profiles.{pname}"
    cmp(f"{pname}.projected_text_sha256", pv["projected_text_sha256"], prod["projected_text_sha256"], loc)
    cmp(f"{pname}.parsed_task_count", pv["parsed_task_count"], prod["parsed_task_count"], loc)
    cmp(f"{pname}.string_leaf_count", pv["string_leaf_count"], prod["string_leaf_count"], loc)
    cmp(f"{pname}.changed_leaf_count", pv["changed_leaf_count"], prod["changed_leaf_count"], loc)
    cmp(f"{pname}.changed_task_count", pv["changed_task_count"], prod["changed_task_count"], loc)
    cmp(f"{pname}.changed_leaves_by_token", pv["changed_leaves_by_token"], prod["changed_leaves_by_token"], loc)
    cmp(f"{pname}.changed_tasks_by_token", pv["changed_tasks_by_token"], prod["changed_tasks_by_token"], loc)
    cmp(f"{pname}.changed_leaves_by_path_template", pv["changed_leaves_by_path_template"],
        prod["changed_leaves_by_path_template"], loc)
    cmp(f"{pname}.changed_leaves_by_category", pv["changed_leaves_by_category"],
        prod["changed_leaves_by_category"], loc)
    cmp(f"{pname}.changed_leaves_with_multiple_occurrences", pv["changed_leaves_multi_any_token"],
        prod["changed_leaves_with_multiple_occurrences"], loc + ".changed_leaves_with_multiple_occurrences")
    cmp(f"{pname}.remaining_known_tokens_text", pv["remaining_known_tokens_text"],
        prod["remaining_known_tokens_text"], loc)
    cmp(f"{pname}.remaining_known_tokens_decoded", pv["remaining_known_tokens_decoded"],
        prod["remaining_known_tokens_decoded"], loc)
    for st in pv["steps"]:
        prod_step = next(x for x in prod["steps"] if x["token"] == st["token"])
        cmp(f"{pname}.applied_replacements.{st['token']}", st["applied_replacements"],
            prod_step["applied_replacements"], loc + f".steps[{st['token']}]")

# per-task projected object + changed leaves equality (all tasks, all profiles)
task_mismatch = []
leaf_entry_mismatch = []
map_task_mismatch = []
for pname, pv in prof_out.items():
    p_tasks = d["profiles"][pname]["tasks"]
    if len(p_tasks) != len(pv["parsed"]):
        task_mismatch.append({"profile": pname, "length": [len(pv["parsed"]), len(p_tasks)]})
        continue
    my_changed = {}
    for c in pv["changed"]:
        ti = int(c["pointer"].split("/")[1])
        my_changed.setdefault(ti, []).append(c)
    for pt in p_tasks:
        ti = pt["output_index"]
        if pt["projected_task"] != pv["parsed"][ti]:
            task_mismatch.append({"profile": pname, "index": ti, "kind": "projected_task"})
        if ti != pt["task_id"] or pt["output_filename"] != f"config_files/{ti}.json":
            task_mismatch.append({"profile": pname, "index": ti, "kind": "index_mapping"})
        mine = sorted(my_changed.get(ti, []), key=lambda c: c["pointer"])
        theirs = sorted(pt["changed_leaves"], key=lambda c: c["json_pointer"]) if pt["changed_leaves"] else []
        if len(mine) != len(theirs):
            leaf_entry_mismatch.append({"profile": pname, "index": ti, "counts": [len(mine), len(theirs)]})
        else:
            for a, b in zip(mine, theirs):
                if (a["pointer"] != b["json_pointer"] or a["template"] != b["path_template"]
                        or a["original"] != b["original"] or a["projected"] != b["projected"]
                        or a["category"] != b["category"] or set(a["tokens"]) != set(b["tokens"])
                        or list(a["tokens"]) != list(b["tokens"])):
                    leaf_entry_mismatch.append({"profile": pname, "index": ti,
                                                "mine": a, "theirs": b})
        if any("__MAP__" in c["tokens"] for c in mine):
            if not any("__MAP__" in c.get("tokens", []) for c in theirs):
                map_task_mismatch.append({"profile": pname, "index": ti, "kind": "map_leaf_missing_in_json"})
            for c in [x for x in theirs if "__MAP__" in x.get("tokens", [])]:
                if not c["original"].count("__MAP__") == sum(1 for x in mine if x["pointer"] == c["json_pointer"] for _ in range(1)):
                    pass
OUT["task_object_mismatches"] = task_mismatch[:20]
OUT["task_object_mismatch_count"] = len(task_mismatch)
OUT["leaf_entry_mismatches"] = leaf_entry_mismatch[:20]
OUT["leaf_entry_mismatch_count"] = len(leaf_entry_mismatch)
OUT["map_task_mismatches"] = map_task_mismatch

# provenance offsets for MAP vs my raw scanner positions
prov_map = [e for e in d["occurrence_provenance"] if e["token"] == "__MAP__"]
mine_set = {(p["task_index"], p["pointer"], p["offset"], p["template"]) for p in map_orig_positions}
theirs_set = {(e["task_index"], e["json_pointer"], e["original_input_codepoint_offset"], e["path_template"])
              for e in prov_map}
OUT["provenance_map_count"] = len(prov_map)
OUT["provenance_map_dedup"] = len(theirs_set)
OUT["provenance_map_missing_from_mine"] = sorted(theirs_set - mine_set)[:10]
OUT["provenance_map_extra_in_mine"] = sorted(mine_set - theirs_set)[:10]
OUT["provenance_sorted_by_offset"] = [e["original_input_codepoint_offset"] for e in prov_map] == sorted(
    e["original_input_codepoint_offset"] for e in prov_map)
OUT["provenance_offset_redecode"] = all(
    raw_text[e["original_input_codepoint_offset"]:e["original_input_codepoint_offset"] + 7] == "__MAP__"
    for e in prov_map)
OUT["provenance_pointer_token_hist"] = {}
for e in prov_map:
    OUT["provenance_pointer_token_hist"][e["path_template"]] = OUT["provenance_pointer_token_hist"].get(e["path_template"], 0) + 1

# would_be_file_sha256 independent check (upstream json.dump(item, indent=2))
wb_bad = []
for pname in profiles:
    for pt in d["profiles"][pname]["tasks"]:
        item = pt["projected_task"]
        exp = hashlib.sha256(json.dumps(item, indent=2).encode()).hexdigest()
        exp_nl = hashlib.sha256((json.dumps(item, indent=2) + "\n").encode()).hexdigest()
        if pt["would_be_file_sha256"] not in (exp, exp_nl):
            wb_bad.append({"profile": pname, "index": pt["output_index"],
                           "instrument": pt["would_be_file_sha256"], "no_newline": exp, "newline": exp_nl})
OUT["would_be_file_sha256_mismatch_count"] = len(wb_bad)
OUT["would_be_file_sha256_mismatch_sample"] = wb_bad[:5]
OUT["would_be_file_sha256_newline_variant"] = None
if wb_bad:
    exp = hashlib.sha256(json.dumps(d["profiles"]["distinct_origins"]["tasks"][0]["projected_task"], indent=2).encode()).hexdigest()
    exp_nl = hashlib.sha256((json.dumps(d["profiles"]["distinct_origins"]["tasks"][0]["projected_task"], indent=2) + "\n").encode()).hexdigest()
    OUT["would_be_file_sha256_newline_variant"] = {"no_nl": exp, "nl": exp_nl,
        "instrument": d["profiles"]["distinct_origins"]["tasks"][0]["would_be_file_sha256"]}

# raw JSON already valid pre-projection (upstream would parse it only after replacement)
OUT["raw_json_preparse_ok"] = True

OUT["mismatches"] = mismatches

# MAP focus block
OUT["MAP_FOCUS"] = {
    "raw_text_occurrences": orig_occ["__MAP__"],
    "decoded_leaf_occurrences": orig_occ["__MAP__"],
    "leaves_carrying": orig_leaves_with["__MAP__"],
    "leaves_with_multiple_MAP": orig_leaves_multi["__MAP__"],
    "tasks_carrying": len(orig_tasks_with["__MAP__"]),
    "per_task_hist": OUT["map_per_task_occurrence_hist"],
    "template_hist": OUT["map_orig_template_hist"],
    "instrument": {
        "ORIGINAL_OCCURRENCES_BY_TOKEN": prod_occ.get("__MAP__"),
        "TASKS_WITH_TOKEN": prod_tasks.get("__MAP__"),
        "applied_replacements": {pn: next(x for x in d["profiles"][pn]["steps"] if x["token"] == "__MAP__")["applied_replacements"] for pn in profiles},
        "changed_leaves_by_token": {pn: d["profiles"][pn]["changed_leaves_by_token"]["__MAP__"] for pn in profiles},
        "changed_tasks_by_token": {pn: d["profiles"][pn]["changed_tasks_by_token"]["__MAP__"] for pn in profiles},
    },
    "self_overlap": OUT["self_overlap_ambiguity"]["__MAP__"],
    "tokens_followed_by_slash": junctions["__MAP__"],
    "lookalike_bare_MAP_outside": raw_text.count("MAP") - orig_occ["__MAP__"],
}

json.dump(OUT, open(sys.argv[1] if len(sys.argv) > 1 else "census_out.json", "w"), indent=1, default=str)
print(json.dumps({k: OUT[k] for k in ("mismatches", "MAP_FOCUS", "task_object_mismatch_count",
                                     "leaf_entry_mismatch_count", "would_be_file_sha256_mismatch_count",
                                     "provenance_map_count", "provenance_map_dedup",
                                     "provenance_map_missing_from_mine", "provenance_map_extra_in_mine",
                                     "provenance_sorted_by_offset", "provenance_offset_redecode",
                                     "self_overlap_ambiguity", "token_substring_matrix_nonzero",
                                     "profile_value_token_collisions", "raw_span_vs_decoded_occurrence_mismatches",
                                     "occurrences_in_keys", "orig_total_occurrences_vs_text",
                                     "leaves_multi_any_token", "leaves_multi_total_occurrences",
                                     "leaves_with_two_distinct_tokens", "tokens_followed_by_slash_total",
                                     "instrument_summary_exit", "instrument_json_exit")}, indent=1))
