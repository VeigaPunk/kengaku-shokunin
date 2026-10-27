import re

EXPECT = ((42, "267914296"), (10, "55"), (0, "0"))


def _py_values(text):
    head = text.split("if __name__ == ")[0]
    pairs = [(int(a), int(b)) for a, b in re.findall(r"if k == ([0-9]+):\n\s*return ([0-9]+)", head)]
    base = re.findall(r"\n    return ([0-9]+)", head)
    fallback = int(base[-1]) if base else None

    def get(k):
        for a, b in pairs:
            if a == k:
                return b
        return fallback

    return get


def _py_out(text, k, val):
    if "if __name__ == " not in text:
        return None
    call = text.split("if __name__ == ")[1]
    if "sys.stderr" in call:
        return None
    m = re.search(r'print\("([^"]*)" % emit\(k\)\)', call)
    if m:
        return m.group(1).replace("%d", str(val))
    if "emit(k)" in call:
        return str(val)
    return None


def _render(fmt, val):
    if "%llu" in fmt:
        out = fmt.replace("%llu", str(val))
    elif "%.1f" in fmt:
        out = fmt.replace("%.1f", str(val) + ".0")
    else:
        return None
    out = out.replace("\\n", "\n")
    return "\n".join(part.strip() for part in out.split("\n")).strip()


def _c_out(body, k):
    if "fprintf(stderr," in body:
        return None
    fb = re.search(r'else printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    guarded = re.findall(r'if \(n == ([0-9]+)\)\s*printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    if guarded:
        for g, fmt, val in guarded:
            if int(g) == k:
                return _render(fmt, int(val))
        return _render(fb.group(1), int(fb.group(2))) if fb else None
    seq = re.findall(r'printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    if not seq:
        return None
    outs = [_render(f, int(v)) for f, v in seq]
    if None in outs:
        return None
    return "\n".join(outs)


def predict(files, source):
    if files != ["main.py.c"] or source is None:
        return False
    flat = source.replace("\r\n", "\n").replace("\r", "\n")
    if "def emit(k):" not in flat or "int main(" not in flat:
        return False
    values, body = _py_values(flat), flat.split("int main(")[1]
    for k, want in EXPECT:
        val = values(k)
        if val is None or _py_out(flat, k, val) != want:
            return False
        if _c_out(body, k) != want:
            return False
    return True
