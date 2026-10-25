"""Independent reference JSON string-span scanner (spec-based, no json.decoder.scanstring).

Produces (start, end, path_tuple, role, decoded_value) records where:
  start = index of the opening quote
  end   = index AFTER the closing quote
  role  = 'key' for object member names, 'value' otherwise
Path convention matches the production one: object member value path = parent_path + (key,),
array element path = parent_path + (index,); KEY spans record the PARENT path.
"""
WS = " \t\n\r"


def _skip_ws(s, i):
    while i < len(s) and s[i] in WS:
        i += 1
    return i


ESC = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}


def _scan_string(s, i):
    """i points at the opening quote. Return (decoded, end_after_closing_quote)."""
    assert s[i] == '"'
    i += 1
    out = []
    while True:
        if i >= len(s):
            raise ValueError("unterminated string")
        c = s[i]
        if c == '"':
            return "".join(out), i + 1
        if c == "\\":
            i += 1
            if i >= len(s):
                raise ValueError("unterminated escape")
            e = s[i]
            if e in ESC:
                out.append(ESC[e])
                i += 1
            elif e == "u":
                hexpart = s[i + 1:i + 5]
                if len(hexpart) != 4:
                    raise ValueError("bad \\u")
                out.append(chr(int(hexpart, 16)))
                i += 5
            else:
                raise ValueError("bad escape %r" % e)
            continue
        if ord(c) < 0x20:
            raise ValueError("control char in string")
        out.append(c)
        i += 1


def ref_spans(s):
    spans = []
    length = len(s)

    def value(i, path):
        i = _skip_ws(s, i)
        c = s[i]
        if c == '"':
            dec, end = _scan_string(s, i)
            spans.append((i, end, path, "value", dec))
            return end
        if c in "{[":
            close = "}" if c == "{" else "]"
            i = _skip_ws(s, i + 1)
            if s[i] == close:
                return i + 1
            idx = 0
            while True:
                i = _skip_ws(s, i)
                if c == "{":
                    key, end = _scan_string(s, i)
                    spans.append((i, end, path, "key", key))
                    i = _skip_ws(s, end)
                    assert s[i] == ":"
                    i = value(i + 1, path + (key,))
                else:
                    i = value(i, path + (idx,))
                    idx += 1
                i = _skip_ws(s, i)
                if s[i] == ",":
                    i += 1
                    continue
                assert s[i] == close
                return i + 1
        for lit in ("true", "false", "null"):
            if s.startswith(lit, i):
                return i + len(lit)
        j = i
        if j < length and s[j] == "-":
            j += 1
        while j < length and s[j].isdigit():
            j += 1
        if j < length and s[j] == ".":
            j += 1
            while j < length and s[j].isdigit():
                j += 1
        if j < length and s[j] in "eE":
            j += 1
            if j < length and s[j] in "+-":
                j += 1
            while j < length and s[j].isdigit():
                j += 1
        assert j > i, i
        return j

    end = _skip_ws(s, value(0, ()))
    assert end == length, (end, length)
    return spans
