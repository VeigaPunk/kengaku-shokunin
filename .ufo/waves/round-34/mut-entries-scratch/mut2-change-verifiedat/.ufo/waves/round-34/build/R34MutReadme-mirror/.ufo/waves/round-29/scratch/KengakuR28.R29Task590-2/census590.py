#!/usr/bin/env python3
"""Independent projection census v2, raw task_id 590, round 29.

Seat KengakuR28.R29Task590-2, read-only leaf. Each pinned input is read once,
bytes retained and verified. Six serialized-text replacements are applied in
the manifest-declared order to the raw TEXT; the projected text is parsed and
leaf-walked. plans/config_projection.py is neither read nor imported.

v2 change: every token occurrence is mapped to its exact leaf path by a
one-occurrence sentinel substitution inside the containing element slice,
instead of value-equality matching (which double-counted duplicate values).
"""
import hashlib
import json
import re

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
MAN = LANE + "/plans/fixtures/r29/manifest.json"
EXPECT = {
    RAW: "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
    GEN: "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd",
    PROF: "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
    MAN: "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
}
B = {}
for p, want in EXPECT.items():
    b = open(p, "rb").read()
    got = hashlib.sha256(b).hexdigest()
    assert got == want, ("pin mismatch", p, got, want)
    B[p] = b

text = B[RAW].decode("utf-8")
doc = json.loads(text)
man = json.loads(B[MAN])
profiles = json.loads(B[PROF])
ORDER = man["replacement_order"]


def lit(t):
    return "__%s__" % t


def leaves(o, path="$"):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, path + "['" + k + "']")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, path + "[%d]" % i)
    else:
        yield path, o


def sig(path):
    return re.sub(r"\[\d+\]", "[]", path)


def cls(path):
    s = sig(path)
    if s == "$['start_url']":
        return "url_start"
    if s == "$['eval']['reference_url']":
        return "url_reference"
    if s == "$['eval']['program_html'][]['url']":
        return "url_program_html"
    if s == "$['eval']['program_html'][]['locator']":
        return "selector_expression"
    if "'must_include'][]" in s or "'must_exclude'][]" in s:
        return "content_required_string"
    if s == "$['intent']" or s == "$['intent_template']" \
            or "instantiation_dict" in s or "reference_answer" in s:
        return "natural_language_or_answer"
    return "other_metadata"


print("## PINS")
print("raw sha256=%s bytes=%d codepoints=%d non_ascii=%d"
      % (hashlib.sha256(B[RAW]).hexdigest(), len(B[RAW]), len(text),
         sum(1 for c in text if ord(c) > 127)))
print("generator sha256=%s bytes=%d" % (hashlib.sha256(B[GEN]).hexdigest(), len(B[GEN])))
print("profiles sha256=%s manifest sha256=%s"
      % (hashlib.sha256(B[PROF]).hexdigest(), hashlib.sha256(B[MAN]).hexdigest()))
print("declared_order=%s" % ",".join(ORDER))
print("profile_names=%s" % ",".join(sorted(profiles)))

# ---- element spans in ORIGINAL text (codepoint offsets) -----------------
dec = json.JSONDecoder()
i0 = text.index("[") + 1
spans = []
i = i0
while True:
    while i < len(text) and text[i] in " \t\r\n,":
        i += 1
    if text[i] == "]":
        break
    obj, end = dec.raw_decode(text, i)
    spans.append({"ord": len(spans), "start": i, "end": end, "obj": obj})
    i = end
assert len(spans) == len(doc) == 812
ids = [s["obj"]["task_id"] for s in spans]
print("\n## POPULATION")
print("tasks=%d distinct_ids=%d ids_equal_ordinal_all=%s"
      % (len(spans), len(set(ids)), ids == list(range(len(ids)))))
print("task_id_590_ordinal=%d" % ids.index(590))

# ---- token occurrences --------------------------------------------------
occ = {}
for t in ORDER:
    hits, i = [], text.find(lit(t))
    while i != -1:
        hits.append(i)
        i = text.find(lit(t), i + 1)
    occ[t] = hits
    print("token=%-15s occurrences=%3d task_ordinals=%3d"
          % (t, len(hits), len({next(s["ord"] for s in spans if s["start"] <= h < s["end"]) for h in hits})))
print("total_occurrences=%d" % sum(len(v) for v in occ.values()))
print("tokens_absent=%s WIKIPEDIA_substrings=%d"
      % ([t for t in ORDER if not occ[t]], text.count("WIKIPEDIA")))

ALL_MARKERS = {}
for m in re.findall(r"__[A-Za-z0-9_]+__", text):
    ALL_MARKERS[m] = ALL_MARKERS.get(m, 0) + 1
print("double_underscore_markers_raw=%s"
      % json.dumps(dict(sorted(ALL_MARKERS.items()))))

# ---- exact occurrence -> leaf path via one-occurrence sentinel ----------
SENT = "QQSENTQQ"


def span_at(pos):
    for s in spans:
        if s["start"] <= pos < s["end"]:
            return s
    raise AssertionError(pos)


def enclosing_literal_span(pos, s):
    qs = None
    i = pos
    while i > s["start"]:
        i -= 1
        if text[i] == '"':
            nb, j = 0, i - 1
            while j >= s["start"] and text[j] == "\\":
                nb += 1
                j -= 1
            if nb % 2 == 0:
                qs = i
                break
    assert qs is not None
    j, qe = qs + 1, None
    while j < s["end"]:
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == '"':
            qe = j
            break
        j += 1
    assert qe is not None
    return qs, qe


occ_rows = []
leaf_hits = {}
for t in ORDER:
    for p in occ[t]:
        s = span_at(p)
        el = text[s["start"]:s["end"]]
        rel = p - s["start"]
        mutated = el[:rel] + SENT + el[rel + len(lit(t)):]
        obj2 = json.loads(mutated)
        orig = dict(list(leaves(s["obj"])))
        new = dict(list(leaves(obj2)))
        diff = [k for k in orig if orig[k] != new.get(k)]
        assert len(diff) == 1, (t, p, diff)
        path = diff[0]
        assert isinstance(orig[path], str)
        assert SENT in new[path] and new[path].replace(SENT, lit(t)) == orig[path], \
            (t, p, path)
        qs, qe = enclosing_literal_span(p, s)
        raw_lit = text[qs:qe + 1]
        occ_rows.append({"token": t, "pos": p, "ord": s["ord"], "path": path,
                         "sig": sig(path), "cls": cls(path),
                         "escaped": "\\" in raw_lit})
        leaf_hits[(s["ord"], path)] = leaf_hits.get((s["ord"], path), 0) + 1

print("\n## OCCURRENCE -> FIELD CENSUS (exact, all 812 tasks)")
per = {}
for r in occ_rows:
    k = (r["token"], r["sig"], r["cls"])
    per[k] = per.get(k, 0) + 1
for (t, s, c), n in sorted(per.items()):
    print("token=%-15s sig=%-56s cls=%-26s occurrences=%d" % (t, s, c, n))
print("distinct_leaves_holding_a_token=%d" % len(leaf_hits))
multi = {}
for n in leaf_hits.values():
    multi[n] = multi.get(n, 0) + 1
print("occurrences_per_leaf_histogram=%s" % json.dumps(dict(sorted(multi.items()))))
print("occurrences_inside_escaped_literal=%d"
      % sum(1 for r in occ_rows if r["escaped"]))
print("locator_leaves_total=%d locator_occurrences=%d"
      % (sum(1 for o in doc for pa, _ in leaves(o) if sig(pa) == "$['eval']['program_html'][]['locator']"),
         sum(1 for r in occ_rows if r["cls"] == "selector_expression")))

print("\n## LEAF DENOMINATORS BY FIELD SIGNATURE")
den = {}
for o in doc:
    for pa, _ in leaves(o):
        den[sig(pa)] = den.get(sig(pa), 0) + 1
for s, n in sorted(den.items(), key=lambda kv: -kv[1]):
    print("  sig=%-58s leaves=%d" % (s, n))

print("\n## MULTI-OCCURRENCE LEAF EXAMPLES")
shown = 0
for (ordn, path), n in sorted(leaf_hits.items(), key=lambda kv: -kv[1]):
    if n > 1 and shown < 6:
        o = spans[ordn]["obj"]
        val = dict(list(leaves(o)))[path]
        print("task_id=%d sig=%s occurrences=%d value_prefix=%r"
              % (o["task_id"], sig(path), n, val[:70]))
        shown += 1

# ---- per-profile projection --------------------------------------------
print("\n## PER-PROFILE PROJECTION")
res = {}
for pname in sorted(profiles):
    vals = profiles[pname]["values"]
    assert set(vals) == set(ORDER)
    proj, step = text, {}
    for t in ORDER:
        step[t] = proj.count(lit(t))
        proj = proj.replace(lit(t), vals[t])
    data = json.loads(proj)
    changed = []
    for a, b in zip(doc, data):
        for (pa, va), (_, vb) in zip(leaves(a), leaves(b)):
            if va != vb:
                changed.append((a["task_id"], pa, va, vb))
    rem = {m: proj.count(m) for m in ALL_MARKERS}
    bysig, bycls = {}, {}
    value_level_equal = 0
    for tid, pa, va, vb in changed:
        bysig[sig(pa)] = bysig.get(sig(pa), 0) + 1
        bycls[cls(pa)] = bycls.get(cls(pa), 0) + 1
        direct = va
        for t in ORDER:
            direct = direct.replace(lit(t), vals[t])
        if direct == vb:
            value_level_equal += 1
    res[pname] = {"proj": proj, "data": data, "changed": changed, "digest": None}
    dg = hashlib.sha256(proj.encode("utf-8")).hexdigest()
    res[pname]["digest"] = dg
    print("profile=%s" % pname)
    print("  replacement_counts=%s" % json.dumps(step, sort_keys=True))
    print("  projected_bytes=%d non_ascii=%d sha256=%s"
          % (len(proj.encode("utf-8")), sum(1 for c in proj if ord(c) > 127), dg))
    print("  parsed_tasks=%d changed_leaves=%d changed_tasks=%d path_set_equals_leafhits=%s"
          % (len(data), len(changed), len({c[0] for c in changed}),
             {(t, pa) for t, pa, _, _ in changed} ==
             {(spans[o]["obj"]["task_id"], pa) for (o, pa) in leaf_hits}))
    print("  changed_by_sig=%s" % json.dumps(bysig, sort_keys=True))
    print("  changed_by_class=%s" % json.dumps(bycls, sort_keys=True))
    print("  leaf_value_equals_direct_value_replacement=%d/%d"
          % (value_level_equal, len(changed)))
    print("  markers_after_projection=%s"
          % json.dumps({k: v for k, v in sorted(rem.items()) if v}))

print("\n## CROSS-PROFILE CHANGED-PATH SET")
sets = {p: {(t, sig(pa)) for t, pa, _, _ in res[p]["changed"]} for p in res}
for p in sorted(sets):
    print("profile=%s paths_identical_to_distinct_origins=%s symdiff=%d"
          % (p, sets[p] == sets["distinct_origins"],
             len(sets[p] ^ sets["distinct_origins"])))

# ---- non-URL content-field examples (F3-relevant) ------------------------
print("\n## NON-URL FIELD CHANGES (content / answer)")
for target in ("content_required_string", "natural_language_or_answer"):
    seen = 0
    for r in occ_rows:
        if r["cls"] == target and seen < 5:
            o = spans[r["ord"]]["obj"]
            va = dict(list(leaves(o)))[r["path"]]
            print("task_id=%d sig=%s token=%s\n  raw=%r"
                  % (o["task_id"], r["sig"], r["token"], va))
            for pname in sorted(res):
                vb = dict(list(leaves(res[pname]["data"][r["ord"]])))[r["path"]]
                print("  %-26s -> %r" % (pname, vb))
            seen += 1
    print("class=%s shown=%d" % (target, seen))

print("\n## URL FIELD EXAMPLE (token inside program_html url)")
for r in occ_rows:
    if r["cls"] == "url_program_html":
        o = spans[r["ord"]]["obj"]
        print("task_id=%d sig=%s token=%s\n  raw=%r"
              % (o["task_id"], r["sig"], r["token"],
                 dict(list(leaves(o)))[r["path"]]))
        for pname in sorted(res):
            print("  %-26s -> %r"
                  % (pname, dict(list(leaves(res[pname]["data"][r["ord"]])))[r["path"]]))
        break

# ---- task_id 590 detail -------------------------------------------------
print("\n## TASK_ID 590 DETAIL (ordinal=%d)" % ids.index(590))
o590 = doc[ids.index(590)]
for pname in sorted(res):
    ch = [c for c in res[pname]["changed"] if c[0] == 590]
    print("profile=%s changed_leaves=2 (measured=%d)" % (pname, len(ch)))
    for tid, pa, va, vb in ch:
        print("  path=%s\n    old=%r\n    new=%r" % (pa, va, vb))
    print("  projected_590_canonical_sha256=%s"
          % hashlib.sha256(json.dumps(res[pname]["data"][ids.index(590)],
                                      sort_keys=True).encode()).hexdigest())

print("\n## TASK_ID 590 PROVENANCE (original unicode-codepoint offsets)")
for r in occ_rows:
    if r["ord"] == ids.index(590):
        print("token=%-15s codepoint_offset=%d sig=%s" % (r["token"], r["pos"], r["sig"]))

print("\n## TASK_ID 590 UNCHANGED LEAVES BY CLASS")
for pa, va in leaves(o590):
    if not any(r["ord"] == ids.index(590) and r["path"] == pa for r in occ_rows):
        print("  sig=%-56s cls=%-26s value=%r" % (sig(pa), cls(pa), va))

# ---- index vs id, in memory --------------------------------------------
print("\n## INDEX-VERSUS-ID, IN MEMORY")
rev = list(reversed(doc))
print("frozen_order_task590_ordinal=%d reversed_order_task590_ordinal=%d"
      % (ids.index(590), [i for i, o in enumerate(rev) if o["task_id"] == 590][0]))
print("reversed_would_write=config_files/%d.json"
      % [i for i, o in enumerate(rev) if o["task_id"] == 590][0])

# ---- order sensitivity in the frozen benign domain ----------------------
print("\n## ORDER SENSITIVITY IN FROZEN DOMAIN")
vals = profiles["distinct_origins"]["values"]
print("token_literal_pairwise_substring=%s"
      % [(a, b) for a in ORDER for b in ORDER if a != b and lit(a) in lit(b)])
print("profile_value_contains_token_literal=%s"
      % [(p, t) for p in profiles for t in ORDER
         if any(lit(t) in v for v in profiles[p]["values"].values())])
fwd, revd = text, text
for t in ORDER:
    fwd = fwd.replace(lit(t), vals[t])
for t in reversed(ORDER):
    revd = revd.replace(lit(t), vals[t])
print("forward_sha256=%s reverse_sha256=%s equal=%s"
      % (hashlib.sha256(fwd.encode()).hexdigest(),
         hashlib.sha256(revd.encode()).hexdigest(), fwd == revd))
print("done")

# ---- addendum: runtime markers, byte path, locality, textual forms ------
print("\n## RUNTIME-MARKER FIELD CENSUS (not among the six environment tokens)")
for marker in ("__last_url__", "__page__"):
    hits, i = [], text.find(marker)
    while i != -1:
        s = span_at(i)
        el = text[s["start"]:s["end"]]
        rel = i - s["start"]
        obj2 = json.loads(el[:rel] + SENT + el[rel + len(marker):])
        o1 = dict(list(leaves(s["obj"])))
        o2 = dict(list(leaves(obj2)))
        diff = [k for k in o1 if o1[k] != o2.get(k)]
        hits.append((s["obj"]["task_id"], sig(diff[0])))
        i = text.find(marker, i + 1)
    sigs = {}
    for _, sg in hits:
        sigs[sg] = sigs.get(sg, 0) + 1
    print("marker=%-13s occurrences=%d by_field=%s example=%s"
          % (marker, len(hits), json.dumps(sigs, sort_keys=True), hits[:3]))

print("\n## BYTE-LEVEL CROSS-CHECK (independent path: bytes.replace in declared order)")
for pname in sorted(profiles):
    bb = B[RAW]
    for t in ORDER:
        bb = bb.replace(lit(t).encode(), profiles[pname]["values"][t].encode())
    print("profile=%-26s bytes_sha256=%s equals_text_path=%s"
          % (pname, hashlib.sha256(bb).hexdigest(),
             bb == res[pname]["proj"].encode("utf-8")))

print("\n## ELEMENT-LOCALITY CHECK (replace inside element == global projection)")
for pname in sorted(profiles):
    vals = profiles[pname]["values"]
    ok = 0
    for s in spans:
        el = text[s["start"]:s["end"]]
        for t in ORDER:
            el = el.replace(lit(t), vals[t])
        if json.loads(el) == res[pname]["data"][s["ord"]]:
            ok += 1
    print("profile=%-26s element_local_equals_global=%d/%d" % (pname, ok, len(spans)))

print("\n## TASK 590 TEXTUAL FORMS (same JSON value, distinct bytes)")
raw_slice = text[spans[590]["start"]:spans[590]["end"]]
flat_proj = res["distinct_origins"]["proj"]
print("raw_source_slice bytes=%d sha256=%s" % (len(raw_slice.encode()),
      hashlib.sha256(raw_slice.encode()).hexdigest()))
print("raw_text_prefix=%r" % text[:100])
for pname in sorted(profiles):
    el = raw_slice
    for t in ORDER:
        el = el.replace(lit(t), profiles[pname]["values"][t])
    obj = json.loads(el)
    art = json.dumps(obj, indent=2)
    print("profile=%-26s test.json_element_bytes=%d indent2_artifact_bytes=%d "
          "parse_equal=%s artifact_sha256=%s"
          % (pname, len(el.encode()), len(art.encode()),
             obj == res[pname]["data"][590],
             hashlib.sha256(art.encode()).hexdigest()))
print("projected_flat_text_contains_raw_slice=%s"
      % (raw_slice in flat_proj))
print("done-addendum")
