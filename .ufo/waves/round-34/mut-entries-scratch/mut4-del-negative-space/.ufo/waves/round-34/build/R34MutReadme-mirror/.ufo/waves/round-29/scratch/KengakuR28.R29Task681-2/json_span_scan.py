"""Codepoint-offset JSON scanner: attribute every raw-text token occurrence to an
exact JSON path with codepoint offset. Stdlib only; no JSON library offset guessing."""
import hashlib, json, re
from collections import Counter, defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
M = lambda n: "__%s__" % n
text = open(RAW, "rb").read().decode("utf-8")
n = len(text)

WS = " \t\r\n"
class Scan:
    def __init__(s, t):
        s.t = t; s.i = 0; s.scalars = []; s.outside_tokens = []
    def ws(s):
        while s.i < s.t.__len__() and s.t[s.i] in WS: s.i += 1
    def value(s, path):
        s.ws()
        c = s.t[s.i]
        if c == "{": s.obj(path)
        elif c == "[": s.arr(path)
        elif c == '"': s.string(path, is_key=False)
        elif c in "-0123456789": s.number(path)
        elif s.t.startswith("true", s.i): s.i += 4; s.scalars.append((path, "bool", s.i-4, s.i))
        elif s.t.startswith("false", s.i): s.i += 5; s.scalars.append((path, "bool", s.i-5, s.i))
        elif s.t.startswith("null", s.i): s.i += 4; s.scalars.append((path, "null", s.i-4, s.i))
        else: raise ValueError("bad value at %d" % s.i)
    def number(s, path):
        st = s.i
        while s.i < n and s.t[s.i] in "+-0123456789.eE": s.i += 1
        s.scalars.append((path, "number", st, s.i))
    def string(s, path, is_key):
        assert s.t[s.i] == '"'
        st = s.i; s.i += 1
        while s.t[s.i] != '"':
            s.i += 2 if s.t[s.i] == "\\" else 1
        s.i += 1
        raw = s.t[st:s.i]
        val = json.loads(raw)
        s.scalars.append((path, "key" if is_key else "string", st, s.i, val))
        return val
    def obj(s, path):
        s.i += 1  # {
        s.ws()
        if s.t[s.i] == "}": s.i += 1; return
        while True:
            s.ws()
            k = s.string(path, is_key=True)
            s.ws(); assert s.t[s.i] == ":"; s.i += 1
            s.value(path + "/" + k)
            s.ws()
            if s.t[s.i] == ",": s.i += 1; continue
            assert s.t[s.i] == "}"; s.i += 1; return
    def arr(s, path):
        s.i += 1
        s.ws()
        if s.t[s.i] == "]": s.i += 1; return
        idx = 0
        while True:
            s.value(path + "/" + str(idx)); idx += 1
            s.ws()
            if s.t[s.i] == ",": s.i += 1; continue
            assert s.t[s.i] == "]"; s.i += 1; return

sc = Scan(text); sc.value("")
print("consumed", sc.i, "of", n, "trailing_ws", repr(text[sc.i:])[:20])

occ = []
for entry in sc.scalars:
    path, kind, a, b = entry[:4]
    raw = text[a:b]
    for t in TOKENS:
        lit = M(t)
        for m in re.finditer(re.escape(lit), raw):
            occ.append({"token": t, "path": path, "kind": kind,
                        "offset_codepoint": a + m.start(), "in_encoded_escape": False})
print("total occurrences scanned", len(occ))
print("by token", dict(Counter(o["token"] for o in occ)))
print("by kind", dict(Counter(o["kind"] for o in occ)))
print("by token x path-pattern:")
pat = Counter((o["token"], re.sub(r"/\d+", "/[i]", o["path"])) for o in occ)
for (t, p), c in sorted(pat.items()): print("  ", t, c, p)

# any token text outside JSON strings?
inside = set()
for entry in sc.scalars:
    a, b = entry[2], entry[3]
    inside.update(range(a, b))
outside = [(m.start(), m.group(0)) for m in re.finditer(r"__[A-Z_]+__", text) if m.start() not in inside]
print("markers outside string tokens", outside[:5], "count", len(outside))

# per-path leaf-level detail for start_url
start = [e for e in sc.scalars if e[0].endswith("/start_url")]
print("start_url leaves", len(start), "distinct values", len({e[4] for e in start}))
print("start_url value histogram", dict(Counter(e[4] for e in start)))
# suffix presence per token occurrence: chars after token inside same string
suffixes = Counter()
for o in occ:
    e = next(e for e in sc.scalars if e[2] <= o["offset_codepoint"] < e[3])
    raw = text[o["offset_codepoint"]:e[3]-1]
    after = raw[len(M(o["token"])):]
    suffixes[(o["token"], "bare" if after == "" else ("slash_suffix" if after.startswith("/") else "other_suffix"))] += 1
print("suffix class per token", dict(suffixes))

# runtime markers
for mk in ["__last_url__", "__page__"]:
    offs = [m.start() for m in re.finditer(re.escape(mk), text)]
    paths = Counter()
    for off in offs:
        e = next(e for e in sc.scalars if e[2] <= off < e[3])
        paths[re.sub(r"/\d+", "/[i]", e[0])] += 1
    print("runtime marker", mk, "count", len(offs), "paths", dict(paths))
