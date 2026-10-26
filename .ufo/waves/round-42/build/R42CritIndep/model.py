#!/usr/bin/env python3
"""R42CritIndep: independent Python model of the captured tb2 `circuit-fibsqrt` sim.c +
the captured test_outputs.py, written from the captured sources only (no grader import,
no sim.c binary, no reading of the probe's case builders).

Model of sim.c (captured sha256 700645ac..., 353 lines):
  parse : fgets(256) loop, then sscanf(line, "out%d = %[^\\n]", &idx, &op) -- C scanf semantics
          (literal 'out', %d skips leading whitespace, ' = ' is ws / '=' / ws, %[^\\n] needs >=1
          non-newline char).  num_signals grows to idx+1 BEFORE the op is classified.
          op classification in this order: "0", "1", starts-with-"out" AND no ' ' (copy),
          starts-with-"~out" (not), sscanf(op,"out%d %c out%d")==3 (binary), else DROPPED
          (the gate keeps the global-initialised CONST_0 type, deps are not registered).
  main  : values zeroed, parse, input = strtoul(argv[1], 0), values[i] = bit i of input for
          i < min(32, num_signals), 32000 x simulate_step(), then if num_signals >= 32 print
          sum(values[num_signals-32+i] << i) as unsigned 32-bit decimal.
  step  : event-driven min-heap over signal indices; step 0 seeds every signal; a changed
          signal pushes its dependents into the current queue only when dep > sig and not yet
          done, and always into the next queue (once).
"""
from __future__ import annotations

import heapq

MAX_SIGNALS = 32000
MAX_DEPS = 10000
C0, C1, COPY, NOT, AND, OR, XOR = range(7)

WS = " \t\n\v\f\r"


def _skip_ws(s, i):
    while i < len(s) and s[i] in WS:
        i += 1
    return i


def _scan_int(s, i):
    """C %d: skip leading whitespace, optional sign, >=1 digit. Returns (value, next_i)."""
    i = _skip_ws(s, i)
    j = i
    if j < len(s) and s[j] in "+-":
        j += 1
    k = j
    while k < len(s) and s[k].isdigit() and s[k].isascii():
        k += 1
    if k == j:
        return None, i
    return int(s[i:k]), k


def outer_scan(line):
    """sscanf(line, "out%d = %[^\\n]", &idx, &op) == 2 -> (idx, op) else None."""
    if not line.startswith("out"):
        return None
    idx, i = _scan_int(line, 3)
    if idx is None:
        return None
    i = _skip_ws(line, i)
    if i >= len(line) or line[i] != "=":
        return None
    i = _skip_ws(line, i + 1)
    if i >= len(line) or line[i] == "\n":
        return None
    j = line.find("\n", i)
    return idx, (line[i:] if j < 0 else line[i:j])


def scan_binary(op):
    """sscanf(op, "out%d %c out%d") == 3 -> (a, char, b) else None."""
    if not op.startswith("out"):
        return None
    a, i = _scan_int(op, 3)
    if a is None:
        return None
    i = _skip_ws(op, i)
    if i >= len(op):
        return None
    ch = op[i]
    i = _skip_ws(op, i + 1)
    if not op.startswith("out", i):
        return None
    b, _ = _scan_int(op, i + 3)
    if b is None:
        return None
    return a, ch, b


class Program:
    def __init__(self):
        self.gtype = [C0] * MAX_SIGNALS
        self.src1 = [0] * MAX_SIGNALS
        self.src2 = [0] * MAX_SIGNALS
        self.deps = [[] for _ in range(MAX_SIGNALS)]
        self.num_signals = 0
        self.dropped = 0
        self.oob_write = set()
        self.parsed = 0

    def _set(self, idx, typ, a=0, b=0):
        if idx < 0 or idx >= MAX_SIGNALS:
            self.oob_write.add(idx)          # UB in C: gates[idx] is out of bounds
            return
        self.gtype[idx] = typ
        self.src1[idx] = a
        self.src2[idx] = b

    def _dep(self, src, idx):
        if 0 <= src < MAX_SIGNALS and len(self.deps[src]) < MAX_DEPS:
            self.deps[src].append(idx)
        # out-of-range src / full dep table is UB or exit(1) in C; not reached by these cases

    def line(self, line):
        got = outer_scan(line)
        if got is None:
            return
        idx, op = got
        self.parsed += 1
        if idx >= self.num_signals:
            self.num_signals = idx + 1
        if op == "0":
            self._set(idx, C0)
        elif op == "1":
            self._set(idx, C1)
        elif op.startswith("out") and " " not in op:
            src, _ = _scan_int(op, 3)
            self._set(idx, COPY, src)
            self._dep(src, idx)
        elif op.startswith("~out"):
            src, _ = _scan_int(op, 4)
            self._set(idx, NOT, src)
            self._dep(src, idx)
        else:
            b = scan_binary(op)
            if b is not None:
                a, ch, c = b
                typ = {"&": AND, "|": OR, "^": XOR}.get(ch)
                if typ is None:
                    self.dropped += 1          # op_char unknown: type stays as it was
                    self._dep(a, idx)
                    self._dep(c, idx)
                    return
                self._set(idx, typ, a, c)
                self._dep(a, idx)
                self._dep(c, idx)
            else:
                self.dropped += 1              # silently a CONST_0 gate

    def feed(self, data: bytes):
        """fgets(256) semantics: one newline-terminated line, or 255 bytes when longer."""
        text = data.decode("latin-1")
        i = 0
        while i < len(text):
            j = text.find("\n", i)
            end = len(text) if j < 0 else j + 1
            if end - i > 255:
                chunk = text[i:i + 255]
                i += 255
            else:
                chunk = text[i:end]
                i = end
            self.line(chunk)


def simulate(prog: Program, argv1: str, steps=32000):
    """Returns (stdout_text, rc, oob_read). rc 1 == fopen failure is handled by the caller."""
    n = prog.num_signals
    values = [0] * MAX_SIGNALS
    v = int(argv1, 0) & 0xFFFFFFFF if argv1.strip() else 0
    for i in range(min(32, n)):
        values[i] = (v >> i) & 1
    gtype, src1, src2, deps = prog.gtype, prog.src1, prog.src2, prog.deps
    cur, nxt = [], []
    for step in range(steps):
        if step > 0:
            cur, nxt = nxt, cur
            del nxt[:]
            if not cur:
                break                        # nothing left to do (sim.c keeps looping, no effect)
        if step == 0:
            cur[:] = list(range(n))
            heapq.heapify(cur)
        did = set()
        inq2 = set()
        pop, push = heapq.heappop, heapq.heappush
        while cur:
            sig = pop(cur)
            if sig < 0 or sig >= MAX_SIGNALS or sig in did:
                continue
            did.add(sig)
            old = values[sig]
            t = gtype[sig]
            if t == C0:
                new = 0
            elif t == C1:
                new = 1
            elif t == COPY:
                new = values[src1[sig]]
            elif t == NOT:
                new = 0 if values[src1[sig]] else 1
            elif t == AND:
                new = values[src1[sig]] & values[src2[sig]]
            elif t == OR:
                new = values[src1[sig]] | values[src2[sig]]
            else:
                new = values[src1[sig]] ^ values[src2[sig]]
            if new != old:
                values[sig] = new
                for dep in deps[sig]:
                    if 0 <= dep < MAX_SIGNALS:
                        if dep not in did and dep > sig:
                            push(cur, dep)
                        if dep not in inq2:
                            push(nxt, dep)
                            inq2.add(dep)
    if n < 32:
        return "", 0, []
    oob_read = []
    result = 0
    for i in range(32):
        k = n - 32 + i
        if k >= MAX_SIGNALS:
            oob_read.append(k)
            continue
        if values[k]:
            result |= 1 << i
    return f"{result}\n", 0, oob_read


# ---------------------------------------------------------------- grader model (test_outputs.py)
GRADED = [1, 4, 8, 12, 41, 42, 107, 220, 209, 366]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x - 1]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x + 1]


def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def isqrt_newton(n):
    if n < 0:
        raise ValueError("Square root of negative number")
    if n == 0:
        return 0
    x = n
    while True:
        x_new = (x + n // x) // 2
        if x_new >= x:
            return x
        x = x_new


def answer(n):
    return fibonacci(isqrt_newton(n)) % (2 ** 32)


def py_lines(data: bytes) -> int:
    """sum(1 for line in open(path,'r')) with universal newlines."""
    text = data.decode("utf-8", "replace")
    if not text:
        return 0
    n = text.count("\n")
    if not text.endswith("\n"):
        n += 1
    return n


def grade(gates, is_dir=False, missing=False):
    """Three letters for test_gates_file_exists / test_gates_file_size / test_sqrt_fib."""
    exists = not missing
    letters = []
    letters.append("P" if exists else "F")
    if not exists:
        letters.append("F")
    elif is_dir:
        letters.append("F")                  # IsADirectoryError
    else:
        letters.append("P" if py_lines(gates) < 32000 else "F")
    if missing:
        letters.append("F")                  # sim: fopen fails -> exit 1 -> returncode != 0
        return "".join(letters), None
    prog = Program()
    if not is_dir:
        prog.feed(gates)
    else:
        prog.feed(b"")                       # fopen(dir) + fgets -> NULL on Linux: no lines
    if prog.num_signals == 0:
        letters.append("F")                  # no print -> int("") ValueError
        return "".join(letters), None
    out, rc, oob = simulate(prog, "1")
    detail = {"num_signals": prog.num_signals, "oob_write": sorted(prog.oob_write),
              "oob_read": oob, "dropped": prog.dropped, "lines": py_lines(gates)}
    ok = True
    for n in GRADED:
        o, _rc, _oob = simulate(prog, str(n))
        try:
            got = int(o.strip())
        except ValueError:
            ok = False
            break
        if got != answer(n):
            ok = False
            break
    letters.append("P" if ok else "F")
    return "".join(letters), detail


# ---------------------------------------------------------------- my own lookup circuit builder
def wire(out, expr):
    return f"out{out} = {expr}"


def lookup(values, flip=None):
    """Gate lines whose final 32 signals are the answer on exactly `values` (0 elsewhere)."""
    lines = []
    for i in range(32):
        lines.append(wire(i, f"out{i}"))                       # keep argv bits alive
    neg = []
    for i in range(32):
        neg.append(len(lines))
        lines.append(wire(len(lines), f"~out{i}"))
    eqs = []
    for v in sorted(set(values)):
        lits = [i if (v >> i) & 1 else neg[i] for i in range(32)]
        acc = lits[0]
        for x in lits[1:]:
            lines.append(wire(len(lines), f"out{acc} & out{x}"))
            acc = len(lines) - 1
        eqs.append((v, acc))
    outs = []
    for j in range(32):
        sel = []
        for v, acc in eqs:
            a = answer(v)
            if flip and flip[0] == v:
                a ^= 1 << flip[1]
            if (a >> j) & 1:
                sel.append(acc)
        if not sel:
            outs.append(len(lines))
            lines.append(wire(len(lines), "0"))
            continue
        acc = sel[0]
        for s in sel[1:]:
            lines.append(wire(len(lines), f"out{acc} | out{s}"))
            acc = len(lines) - 1
        outs.append(acc)
    base = len(lines)
    for j in range(32):
        lines.append(wire(base + j, f"out{outs[j]}"))
    return lines
