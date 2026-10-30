#!/usr/bin/env python3
"""Round 53, claim C1: AST classifier for the presence-only definition (.ufo/waves/round-53/p1-spec.md).

    classify_source(src) -> {test key: 'P1' | 'P0'}

A test key is ``name`` for a module-level ``test_*`` function and ``Class.name`` for a ``test_*`` method of
class ``Class``.  ``P1`` is the spec's Y (presence-only); ``P0`` is N or U.

The classifier is an abstract interpreter over the ``ast`` of one file.  Every expression gets a *kind*:

    K  pure: literals, constant paths/strings, no filesystem state            (os.path.join("/a", "b"))
    N  a name/path that came from a directory listing (loop variable)          (for f in os.listdir(d))
    L  a collection of names from a listing (listdir/iterdir/glob/scandir...)  ; W os.walk ; E enumerate
    Q  bools over a constant collection ; V bools over a listing (any() ok, all() is a universal -> violation)
    B  a boolean that depends only on existence/type/listing-name membership   (p.exists(), "x" in os.listdir(d))
    C  a count (len of a listing, loop counter); a count comparison is a value, never existence
    X  anything else (content, command output, size, return value of foreign code, unknown)
    S  the ``self`` object, F  a callable value

Rule order (see ``Run`` below):
  1. Reach: test body + implicit setup (setUp*, setup_*, autouse fixtures) + same-file helpers / ``self.`` methods /
     requested same-file fixtures (the whole fixture function, teardown included) / referenced module- and
     class-level constants, transitively, cycle-guarded.  A lambda bound to a name is a same-file helper.
  2. Any *reachable* operation that is not a plain existence predicate or pure path/name arithmetic is a violation
     (subprocess, open for reading, read_*, json, stat/size/mtime, network, unknown call, foreign import call, ...).
     A filesystem *write* is not a violation: the spec forbids reads, and names touch/mkdir as the way
     presence is created.  An in-test import of a foreign module is a violation only when it is called.
  3. Assertions: ``assert``, ``self.assert*``, ``pytest.fail`` / ``self.fail`` / ``raise`` under an ``if``/``except``
     or under the negation of a path condition (early ``return``, ``for``/``else``).
     Each assertion condition must be of kind B/N/L/C (fs dependent) and not X; a purely constant assertion (other
     than a literal ``True``) is a violation; counts / equality of listings / value comparisons are violations.
  4. P1 iff no violation and at least one fs-dependent assertion.  Otherwise P0.

Standard library only, deterministic, no network, no filesystem access.
"""
from __future__ import annotations

import ast
import builtins
import hashlib
import sys
import warnings

K, N, L, W, E, Q, V, B, C, X, S, F = "K", "N", "L", "W", "E", "Q", "V", "B", "C", "X", "S", "F"
FS = frozenset({N, L, W, E, Q, V, B, C})

IMPLICIT_SETUP = True          # setUp / setUpClass / setup_method / setup_class / setup_module / setup_function / autouse
SETUP_METHODS = ("setUpClass", "setup_class", "setUp", "setup_method")
SETUP_FUNCS = ("setup_module", "setup_function")

# ---- tables ---------------------------------------------------------------------------------------
EXIST_Q = {"os.path.exists", "os.path.isfile", "os.path.isdir", "os.path.islink", "os.path.lexists",
           "os.path.ismount"}
LIST_Q = {"os.listdir": L, "os.scandir": L, "glob.glob": L, "glob.iglob": L, "os.walk": W}
PURE_Q = {"pathlib.Path", "pathlib.PurePath", "pathlib.PosixPath", "pathlib.PurePosixPath",
          "pathlib.Path.cwd", "pathlib.Path.home",
          "os.path.join", "os.path.basename", "os.path.dirname", "os.path.abspath", "os.path.normpath",
          "os.path.realpath", "os.path.expanduser", "os.path.expandvars", "os.path.split", "os.path.splitext",
          "os.path.relpath", "os.path.isabs", "os.path.normcase", "os.path.splitdrive", "os.fspath", "os.getcwd",
          "os.getenv", "os.environ.get", "glob.escape", "fnmatch.fnmatch", "fnmatch.fnmatchcase", "fnmatch.filter",
          "fnmatch.translate", "os.path.commonpath", "os.path.commonprefix", "os.fsdecode", "os.fsencode",
          "os.cpu_count"}
NEUTRAL_Q = {"time.sleep", "pytest.skip", "pytest.xfail", "warnings.warn", "pytest.fixture", "pytest.param",
             "contextlib.suppress", "contextlib.redirect_stdout", "contextlib.redirect_stderr",
             "contextlib.ExitStack"}
NEUTRAL_PREFIX = ("logging.", "typing.", "sys.stdout", "sys.stderr")
CONST_ATTR_Q = {"os.sep", "os.pathsep", "os.linesep", "os.curdir", "os.pardir", "os.name", "os.F_OK", "sys.platform",
                "os.environ", "sys.version_info", "sys.argv", "os.altsep", "os.devnull", "os.extsep"}
EXIST_M = {"exists", "is_file", "is_dir", "is_symlink", "is_mount", "lexists", "is_socket", "is_fifo",
           "is_block_device", "is_char_device"}
LIST_M = {"glob": L, "rglob": L, "scandir": L}
PATH_PURE_M = {"joinpath", "with_name", "with_suffix", "with_stem", "relative_to", "as_posix", "absolute", "expanduser",
               "match", "is_absolute", "is_relative_to", "full_match", "__truediv__", "__str__", "resolve"}
STR_M = {"startswith", "endswith", "lower", "upper", "strip", "lstrip", "rstrip", "replace", "split", "rsplit", "join",
         "format", "removeprefix", "removesuffix", "casefold", "title", "zfill", "partition", "rpartition", "isdigit",
         "isalpha", "isalnum", "splitlines", "encode", "decode", "capitalize", "swapcase", "ljust", "rjust", "center",
         "expandtabs", "format_map", "isupper", "islower", "isspace", "translate", "get", "keys", "values", "items",
         "copy", "find", "rfind", "count_k"}
PURE_ATTR = {"name", "stem", "suffix", "suffixes", "parts", "parent", "parents", "root", "anchor", "drive", "path",
             "real", "imag"}
MUTATORS = {"append", "add", "extend", "update", "insert", "appendleft"}
# Filesystem *writes* are not reads (spec clause 3 forbids reads/parses, not writes; the operational
# definition even names touch/mkdir as the way to create presence).  A write that is followed by a
# content read still ends in P0, because the read itself is a clause-3 violation.
WRITE_M = {"write_text", "write_bytes", "touch", "mkdir", "makedirs", "unlink", "rmdir", "rename",
           "replace", "symlink_to", "hardlink_to", "link_to"}
WRITE_COUNT_M = {"write_text", "write_bytes"}          # these return a byte/char count
WRITE_OPEN_MODES = {"w", "wb", "a", "ab", "x", "xb"}    # write-only modes of open()
FILE_SIDE_EFFECT_M = {"write", "writelines", "flush", "close"}   # file handle side effects
MUTATE_Q = {"os.mkdir", "os.makedirs", "os.remove", "os.unlink", "os.rmdir", "os.rename", "os.replace",
            "os.link", "os.symlink", "os.truncate", "os.chmod", "os.utime"}
TMP_FIXTURES = {"tmp_path", "tmpdir", "tmp_path_factory", "tmpdir_factory"}
KNOWN_K_MODULES = {"os", "sys", "pathlib", "glob", "fnmatch", "stat", "time", "pytest", "unittest", "logging", "typing",
                   "re", "string", "math", "posixpath", "genericpath", "collections", "itertools", "functools",
                   "textwrap", "warnings", "__future__", "dataclasses", "enum", "contextlib", "abc"}
PURE_BUILTIN_VALUE = {"int", "float", "abs", "min", "max", "sum", "round", "ord", "chr", "hex", "oct", "bin", "divmod",
                      "pow", "complex", "hash", "id", "type", "callable", "ascii", "format", "bytes", "bytearray",
                      "slice", "object", "super", "vars", "dir"}
ASSERT_METHODS = {"assertTrue", "assertFalse", "assertIn", "assertNotIn", "assertEqual", "assertNotEqual", "assertIs",
                  "assertIsNot", "assertIsNone", "assertIsNotNone", "assertGreater", "assertGreaterEqual",
                  "assertLess", "assertLessEqual", "assert_", "failUnless", "failIf", "assertEquals",
                  "assertNotEquals"}
CMP_FOR_ASSERT = {"assertIn": ast.In, "assertNotIn": ast.NotIn, "assertEqual": ast.Eq, "assertEquals": ast.Eq,
                  "assertNotEqual": ast.NotEq, "assertNotEquals": ast.NotEq, "assertIs": ast.Is,
                  "assertIsNot": ast.IsNot, "assertGreater": ast.Gt, "assertGreaterEqual": ast.GtE,
                  "assertLess": ast.Lt, "assertLessEqual": ast.LtE}
NEUTRAL_SELF = {"subTest", "skipTest", "addCleanup", "id", "shortDescription", "maxDiff"}
FAIL_SELF = {"fail"}


def join(a: str, b: str) -> str:
    if a == b:
        return a
    s = {a, b}
    if s == {K, B}:
        return B
    if s == {K, N}:
        return N
    if s == {K, L} or s == {N, L}:
        return L
    if s == {B, Q}:
        return Q
    return X


def join_all(ks) -> str:
    out = None
    for k in ks:
        out = k if out is None else join(out, k)
    return K if out is None else out


def is_bool_const(n) -> bool:
    return isinstance(n, ast.Constant) and isinstance(n.value, bool)


def is_num_const(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
        return n.value
    return None


def is_empty_literal(n) -> bool:
    return (isinstance(n, (ast.List, ast.Tuple, ast.Set)) and not n.elts) or (
        isinstance(n, ast.Dict) and not n.keys) or (isinstance(n, ast.Constant) and n.value in ("", b""))


class Frame:
    __slots__ = ("vars", "parent", "cls", "ctrl", "rets", "funcs", "imports", "lambdas", "in_assert",
                 "exit_guard")

    def __init__(self, parent=None, cls=None):
        self.vars: dict[str, str] = {}
        self.parent = parent
        self.cls = cls
        self.ctrl: list[tuple[str, str]] = []
        self.rets: list[str] = []
        self.funcs: dict[str, tuple] = {}
        self.imports: dict[str, str] = {}
        self.lambdas: dict[str, ast.Lambda] = {}
        self.in_assert: bool = False
        self.exit_guard: str | None = None

    def find_lambda(self, n):
        f = self
        while f is not None:
            if n in f.lambdas:
                return f.lambdas[n]
            f = f.parent
        return None

    def lookup(self, n):
        f = self
        while f is not None:
            if n in f.vars:
                return f.vars[n]
            f = f.parent
        return None

    def find_func(self, n):
        f = self
        while f is not None:
            if n in f.funcs:
                return f.funcs[n]
            f = f.parent
        return None

    def find_import(self, n):
        f = self
        while f is not None:
            if n in f.imports:
                return f.imports[n]
            f = f.parent
        return None


class Module:
    """Static facts about one file."""

    def __init__(self, tree: ast.Module):
        self.tree = tree
        self.imports: dict[str, str] = {}
        self.funcs: dict[str, ast.AST] = {}
        self.classes: dict[str, ast.ClassDef] = {}
        self.gassign: dict[str, list] = {}           # module-level name -> [(target, value)]
        self.cassign: dict[str, dict[str, list]] = {}
        self.fixtures: dict[str, tuple] = {}         # name -> (funcdef, owner class name | None)
        self.autouse: list[tuple] = []
        self._scan(tree.body, None)

    @staticmethod
    def fixture_info(fd):
        """-> (is_fixture, name, autouse)"""
        for d in fd.decorator_list:
            target = d.func if isinstance(d, ast.Call) else d
            nm = dotted(target)
            if nm and nm.split(".")[-1] == "fixture" and (nm == "fixture" or nm.endswith("pytest.fixture")
                                                            or nm.endswith("pytest_asyncio.fixture")):
                name, auto = fd.name, False
                if isinstance(d, ast.Call):
                    for kw in d.keywords:
                        if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                            name = kw.value.value
                        if kw.arg == "autouse" and isinstance(kw.value, ast.Constant):
                            auto = bool(kw.value.value)
                return True, name, auto
        return False, fd.name, False

    def _scan(self, body, cls):
        for st in body:
            if isinstance(st, ast.Import):
                for a in st.names:
                    if cls is None:
                        if a.asname:
                            self.imports[a.asname] = a.name
                        else:
                            self.imports[a.name.split(".")[0]] = a.name.split(".")[0]
            elif isinstance(st, ast.ImportFrom):
                if st.level == 0 and st.module and cls is None:
                    for a in st.names:
                        if a.name != "*":
                            self.imports[a.asname or a.name] = st.module + "." + a.name
                elif cls is None:
                    for a in st.names:
                        self.imports[a.asname or a.name] = "<local>." + a.name
            elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):
                isf, nm, auto = self.fixture_info(st)
                if cls is None:
                    self.funcs[st.name] = st
                if isf:
                    self.fixtures[nm] = (st, cls)
                    if auto:
                        self.autouse.append((st, cls))
            elif isinstance(st, ast.ClassDef):
                if cls is None:
                    self.classes[st.name] = st
                    self.cassign.setdefault(st.name, {})
                    self._scan(st.body, st.name)
            elif isinstance(st, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                tg = st.targets if isinstance(st, ast.Assign) else [st.target]
                val = getattr(st, "value", None)
                if val is None:
                    continue
                store = self.gassign if cls is None else self.cassign[cls]
                for t in tg:
                    for nm in names_of(t):
                        store.setdefault(nm, []).append((t, val))
            elif isinstance(st, (ast.If, ast.Try, ast.For, ast.While, ast.With)) and cls is None:
                for blk in ("body", "orelse", "finalbody"):
                    self._scan(getattr(st, blk, []) or [], cls)
                for h in getattr(st, "handlers", []) or []:
                    self._scan(h.body, cls)

    def class_chain(self, cname):
        out, seen = [], set()
        todo = [cname]
        while todo:
            c = todo.pop(0)
            if c in seen or c not in self.classes:
                continue
            seen.add(c)
            out.append(c)
            for b in self.classes[c].bases:
                nm = dotted(b)
                if nm and nm.split(".")[-1] in self.classes:
                    todo.append(nm.split(".")[-1])
        return out

    def find_method(self, cname, mname):
        for c in self.class_chain(cname):
            for st in self.classes[c].body:
                if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name == mname:
                    return st, c
        return None


def dotted(n):
    parts = []
    while isinstance(n, ast.Attribute):
        parts.append(n.attr)
        n = n.value
    if isinstance(n, ast.Name):
        parts.append(n.id)
        return ".".join(reversed(parts))
    return None


def names_of(t):
    if isinstance(t, ast.Name):
        return [t.id]
    if isinstance(t, (ast.Tuple, ast.List)):
        return [n for e in t.elts for n in names_of(e)]
    if isinstance(t, ast.Starred):
        return names_of(t.value)
    return []


class Run:
    """Analysis of one test function."""

    def __init__(self, mod: Module):
        self.m = mod
        self.viol: list[str] = []
        self.fs_asserts = 0
        self.fs_touch = 0
        self.stack: list[int] = []
        self.memo: dict = {}
        self.gcache: dict = {}
        self.gprog: set = set()
        self.selfattrs: dict[str, str] = {}
        self.modframe = Frame()
        self.fixcache: dict = {}
        self.cur_cls: str | None = None
        self.break_stack: list = []

    # -- helpers -------------------------------------------------------------------------------
    def v(self, msg: str, node=None) -> str:
        ln = getattr(node, "lineno", None)
        self.viol.append(f"{msg}" + (f"@{ln}" if ln else ""))
        return X

    def ctrl_fs(self, fr) -> bool:
        return any(k in FS or k == X for _, k in fr.ctrl)

    def qname(self, node, fr):
        parts = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if not isinstance(cur, ast.Name):
            return None
        head = cur.id
        if fr.lookup(head) is not None or fr.find_func(head) or head in self.m.funcs and head not in self.m.imports:
            return None
        base = fr.find_import(head) or self.m.imports.get(head)
        if base is None:
            return None
        q = ".".join([base] + parts[::-1])
        for a, b in (("posixpath.", "os.path."), ("genericpath.", "os.path."), ("pathlib.PosixPath", "pathlib.Path"),
                     ("pathlib.PurePosixPath", "pathlib.Path"), ("pathlib.PurePath", "pathlib.Path"),
                     ("pathlib.WindowsPath", "pathlib.Path")):
            if q.startswith(a):
                q = b + q[len(a):]
        return q

    # -- expressions ---------------------------------------------------------------------------
    def eval(self, n, fr) -> str:
        if n is None:
            return K
        m = getattr(self, "e_" + type(n).__name__, None)
        if m is None:
            return self.v(f"unsupported expression {type(n).__name__}", n)
        return m(n, fr)

    def e_Constant(self, n, fr):
        return K

    def e_Name(self, n, fr):
        k = fr.lookup(n.id)
        if k is not None:
            return k
        if fr.find_func(n.id) or n.id in self.m.funcs:
            return F
        if n.id in self.m.gassign:
            return self.global_kind(n.id)
        if n.id in self.m.classes:
            return F
        q = fr.find_import(n.id) or self.m.imports.get(n.id)
        if q is not None:
            return K if q.split(".")[0] in KNOWN_K_MODULES else X
        if n.id == "__file__" or hasattr(builtins, n.id):
            return K
        return X

    def global_kind(self, name):
        if name in self.gcache:
            return self.gcache[name][0]
        if name in self.gprog:
            return X
        self.gprog.add(name)
        saved = self.viol
        self.viol = []
        ks = []
        for t, val in self.m.gassign[name]:
            fr = self.modframe
            k = self.eval(val, fr)
            if isinstance(t, (ast.Tuple, ast.List)) and isinstance(val, (ast.Tuple, ast.List)) \
                    and len(t.elts) == len(val.elts):
                for e, ve in zip(t.elts, val.elts):
                    if isinstance(e, ast.Name) and e.id == name:
                        k = self.eval(ve, fr)
            elif isinstance(t, (ast.Tuple, ast.List)) and k == L:
                k = N
            ks.append(k)
        delta = self.viol
        self.viol = saved
        k = join_all(ks)
        self.gcache[name] = (k, delta)
        self.gprog.discard(name)
        self.viol.extend(delta)
        return k

    def e_Attribute(self, n, fr):
        if n.attr == "param" and isinstance(n.value, ast.Name) and n.value.id == "request":
            # request.param is a fixture parameter value: a name, not filesystem state.
            return K
        q = self.qname(n, fr)
        if q is not None:
            if q in CONST_ATTR_Q:
                return K
            return K if q.split(".")[0] in KNOWN_K_MODULES else X
        rv = n.value
        if isinstance(rv, ast.Name) and fr.lookup(rv.id) == S:
            return self.self_attr(n.attr, fr)
        rk = self.eval(rv, fr)
        if rk in (K, N):
            if n.attr in PATH_PURE_M or n.attr in STR_M or n.attr in PURE_ATTR:
                return rk
            return self.v(f"attribute .{n.attr} of a path/name (value)", n)
        if rk in (L, W, E):
            if n.attr in PURE_ATTR or n.attr in EXIST_M:
                return F
            return self.v(f"attribute .{n.attr} on collection", n)
        return X

    def self_attr(self, attr, fr):
        if attr in self.selfattrs:
            return self.selfattrs[attr]
        cn = self.cur_cls
        if cn:
            for c in self.m.class_chain(cn):
                if attr in self.m.cassign.get(c, {}):
                    ks = []
                    for t, val in self.m.cassign[c][attr]:
                        ks.append(self.eval(val, self.modframe))
                    return join_all(ks)
            if self.m.find_method(cn, attr):
                return F
        return X

    def e_JoinedStr(self, n, fr):
        ks = []
        for v in n.values:
            if isinstance(v, ast.FormattedValue):
                ks.append(self.eval(v.value, fr))
            else:
                ks.append(K)
        if X in ks:
            return X
        return N if any(k in FS or k == N for k in ks) else K

    def e_FormattedValue(self, n, fr):
        return self.eval(n.value, fr)

    def seq_kind(self, elts, fr):
        ks = [self.eval(e.value if isinstance(e, ast.Starred) else e, fr) for e in elts]
        if X in ks:
            return X
        if all(k == K for k in ks):
            return K
        if all(k in (K, N, L) for k in ks):
            return L
        if all(k in (K, B) for k in ks) and any(k == B for k in ks):
            # a tuple/list of existence predicates (all([...]) / any([...]))
            return B
        return X

    def e_List(self, n, fr):
        return self.seq_kind(n.elts, fr)

    e_Tuple = e_List
    e_Set = e_List

    def e_Dict(self, n, fr):
        ks = [self.eval(x, fr) for x in list(n.keys) + list(n.values) if x is not None]
        return K if all(k == K for k in ks) else (X if X in ks else L)

    def e_Starred(self, n, fr):
        return self.eval(n.value, fr)

    def e_Lambda(self, n, fr):
        return F

    def e_BoolOp(self, n, fr):
        ks = [self.eval(v, fr) for v in n.values]
        if X in ks:
            return X
        if all(k == K for k in ks):
            return K
        if any(k in (B, Q, V, C) for k in ks):
            return B
        if any(k in (L, W, E) for k in ks):
            return L
        return N

    def e_UnaryOp(self, n, fr):
        k = self.eval(n.operand, fr)
        if k == X:
            return X
        if isinstance(n.op, ast.Not):
            return K if k == K else B
        return K if k == K else self.v("arithmetic on fs-derived value", n)

    def e_IfExp(self, n, fr):
        tk = self.eval(n.test, fr)
        a, b = self.eval(n.body, fr), self.eval(n.orelse, fr)
        r = join(a, b)
        if r == K and tk in FS:
            return N
        return r

    def e_BinOp(self, n, fr):
        a, b = self.eval(n.left, fr), self.eval(n.right, fr)
        if X in (a, b):
            return X
        if a == K and b == K:
            return K
        op = n.op
        if isinstance(op, (ast.Div, ast.Add, ast.Mod)) and a in (K, N) and b in (K, N):
            return N
        if isinstance(op, ast.Add) and a in (K, L, W, E) and b in (K, L, W, E):
            return L
        if isinstance(op, (ast.BitOr, ast.BitAnd)):
            if a in (K, B) and b in (K, B):
                return B
            if a in (K, L) and b in (K, L):
                return L
        if isinstance(op, ast.Sub) and a in (K, L) and b == L:
            return L          # K - listing: expected names that are missing
        return self.v("arithmetic on fs-derived value", n)

    def e_Subscript(self, n, fr):
        bq = self.qname(n.value, fr) if isinstance(n.value, (ast.Attribute, ast.Name)) else None
        if bq == "os.environ":
            return K
        bk = self.eval(n.value, fr)
        sk = self.eval(n.slice, fr)
        if X in (bk, sk):
            return X
        if bk == K and sk == K:
            return K
        if bk in (K, N) and sk in (K, N):
            return bk
        if bk in (L, W) and sk == K:
            return N if isinstance(n.slice, ast.Constant) else L   # pick a named entry / slice of the listing
        return self.v("index/pick from a count or unknown", n)

    def e_Slice(self, n, fr):
        ks = [self.eval(x, fr) for x in (n.lower, n.upper, n.step) if x is not None]
        return X if X in ks else (K if all(k == K for k in ks) else N)

    def e_Compare(self, n, fr):
        lk, ln = self.eval(n.left, fr), n.left
        res = K
        for op, comp in zip(n.ops, n.comparators):
            rk = self.eval(comp, fr)
            res = join(res, self.cmp1(op, ln, lk, comp, rk, n, fr)) if res != X else X
            lk, ln = rk, comp
        return res

    def cmp1(self, op, ln, lk, rn, rk, at, fr=None):
        if X in (lk, rk):
            return X
        if lk == K and rk == K:
            # Two constants compared: a value comparison.  Inside an assertion's condition the spec
            # allows only path existence/type/membership (clause 2), so this is a violation there;
            # elsewhere it is a neutral constant.
            if fr is not None and getattr(fr, "in_assert", False):
                return self.v("value comparison of computed values", at)
            return K
        if C in (lk, rk):
            # A count is a value, not a path state: the spec's N clause lists "a count" explicitly.
            return self.v("count/size comparison (a count is a value, not a path state)", at)
        if isinstance(op, (ast.In, ast.NotIn)):
            if rk in (L, W, E, Q, K, N) and lk in (K, N):
                return B
            return self.v("membership over non-name values", at)
        if isinstance(op, (ast.LtE, ast.GtE)):
            # K <= L  /  L >= K : the named entries are present (subset)
            if (isinstance(op, ast.LtE) and lk == K and rk == L) or (isinstance(op, ast.GtE) and lk == L and rk == K):
                return B
            return self.v("ordering / superset comparison on listing", at)
        if isinstance(op, (ast.Eq, ast.NotEq, ast.Is, ast.IsNot)):
            if lk in (L, W, E) or rk in (L, W, E):
                return self.v("equality on a listing (exact contents/count/emptiness)", at)
            if lk == B or rk == B:
                return B if (lk in (K, B) and rk in (K, B)) else self.v("bool vs value comparison", at)
            if lk in (K, N) and rk in (K, N):
                return B
        return self.v("value comparison", at)

    def comp(self, n, fr):
        sub = Frame(parent=fr, cls=fr.cls)
        any_fs = False
        iter_fs = False
        for g in n.generators:
            ik = self.eval(g.iter, sub)
            any_fs = any_fs or ik in FS
            iter_fs = iter_fs or ik in (L, W, E)
            self.bind(g.target, self.elem(ik), sub, None)
            for cond in g.ifs:
                ck = self.eval(cond, sub)
                if ck == X:
                    return X
                any_fs = any_fs or ck in FS
        if isinstance(n, ast.DictComp):
            ek = join(self.eval(n.key, sub), self.eval(n.value, sub))
        else:
            ek = self.eval(n.elt, sub)
        if ek == X:
            return X
        if ek == B:
            return V if iter_fs else Q
        if any_fs or ek in (N, L, B, Q, C):
            return L if ek in (K, N, L, W, E) else X
        return K

    e_ListComp = e_SetComp = e_GeneratorExp = e_DictComp = comp

    def e_NamedExpr(self, n, fr):
        k = self.eval(n.value, fr)
        self.assign_name(fr, n.target.id, k, n.value)
        return k

    def e_Await(self, n, fr):
        return self.eval(n.value, fr)

    def e_Yield(self, n, fr):
        fr.rets.append(self.eval(n.value, fr) if n.value is not None else K)
        return K

    # -- element / binding -----------------------------------------------------------------------
    @staticmethod
    def elem(k):
        return {K: K, N: N, L: N, W: "WT", E: "ET", Q: X, V: X, B: X, C: X, X: X}.get(k, X)

    def bind(self, t, k, fr, vnode):
        if isinstance(t, ast.Name):
            self.assign_name(fr, t.id, k, vnode)
            if isinstance(vnode, ast.Lambda):
                fr.lambdas[t.id] = vnode
        elif isinstance(t, (ast.Tuple, ast.List)):
            pos = {"WT": (N, L, L), "ET": (K, N)}.get(k)
            for i, e in enumerate(t.elts):
                if isinstance(e, ast.Starred):
                    self.bind(e.value, L if k not in (K, X) else k, fr, None)
                    continue
                if pos is not None:
                    sk = pos[i] if i < len(pos) else X
                elif k in ("WT", "ET"):
                    sk = X
                elif k == L:
                    sk = N
                else:
                    sk = k
                self.bind(e, sk, fr, None)
        elif isinstance(t, ast.Attribute):
            if isinstance(t.value, ast.Name) and fr.lookup(t.value.id) == S:
                kk = k if k not in ("WT", "ET") else N
                self.selfattrs[t.attr] = join(self.selfattrs[t.attr], kk) if (fr.ctrl and t.attr in self.selfattrs) \
                    else kk
        elif isinstance(t, ast.Subscript):
            if isinstance(t.value, ast.Name) and fr.lookup(t.value.id) is not None:
                cur = fr.lookup(t.value.id)
                kk = k if k not in ("WT", "ET") else N
                self.set_var(fr, t.value.id, join(cur, L if kk in (N, L) else kk) if kk != K or cur != K else K)

    def set_var(self, fr, name, k):
        f = fr
        while f is not None:
            if name in f.vars:
                f.vars[name] = k
                return
            f = f.parent
        fr.vars[name] = k

    def assign_name(self, fr, name, k, vnode):
        if k in ("WT", "ET"):
            k = N
        if self.ctrl_fs(fr):
            if is_bool_const(vnode):
                k = B
            elif is_num_const(vnode) is not None:
                k = C
            elif k == K:
                k = N
        if fr.ctrl and name in fr.vars:
            k = join(fr.vars[name], k)
        fr.vars[name] = k

    # -- calls -----------------------------------------------------------------------------------
    @staticmethod
    def pathish(k):
        return k in (K, N)

    def e_Call(self, n, fr):
        old_ia = fr.in_assert
        if self.is_assert_call(n, fr):
            fr.in_assert = True
        ak = []
        for a in n.args:
            ak.append(self.eval(a.value if isinstance(a, ast.Starred) else a, fr))
        kk = {}
        for kw in n.keywords:
            kk[kw.arg] = self.eval(kw.value, fr)
        fr.in_assert = old_ia
        f = n.func
        if isinstance(f, ast.Name):
            return self.call_name(n, f.id, ak, kk, fr)
        if isinstance(f, ast.Attribute):
            q = self.qname(f, fr)
            if q is not None:
                return self.call_q(n, q, ak, kk, fr)
            rv = f.value
            if isinstance(rv, ast.Name) and fr.lookup(rv.id) == S:
                return self.call_self(n, f.attr, ak, kk, fr)
            if isinstance(rv, ast.Call) and isinstance(rv.func, ast.Name) and rv.func.id == "super":
                return self.v("super() call", n)
            if isinstance(rv, ast.Name) and rv.id in self.m.classes and fr.lookup(rv.id) is None:
                fm = self.m.find_method(rv.id, f.attr)
                if fm:
                    is_static = any(dotted(d) in ("staticmethod",) for d in fm[0].decorator_list)
                    is_cls = any(dotted(d) in ("classmethod",) for d in fm[0].decorator_list)
                    return self.call_func(fm[0], fm[1], ak, kk, bound_self=is_cls and not is_static)
            rk = self.eval(rv, fr)
            return self.call_method(n, rv, rk, f.attr, ak, kk, fr)
        return self.v("call of a computed callee", n)

    def open_is_write(self, n, mode_index=1) -> bool:
        """True when open() is called in a write-only mode (no content is read)."""
        mode_node = n.args[mode_index] if len(n.args) > mode_index else None
        if mode_node is None:
            for kw in n.keywords:
                if kw.arg == "mode":
                    mode_node = kw.value
        mode = mode_node.value if isinstance(mode_node, ast.Constant) and \
            isinstance(mode_node.value, str) else None
        return mode in WRITE_OPEN_MODES

    def is_assert_call(self, n, fr):
        """True for ``assert ...`` style calls whose arguments are assertion conditions."""
        f = n.func
        if isinstance(f, ast.Attribute):
            if f.attr not in ASSERT_METHODS and f.attr not in FAIL_SELF:
                return False
            rv = f.value
            return isinstance(rv, ast.Name) and fr.lookup(rv.id) == S
        if isinstance(f, ast.Name):
            return f.id in ASSERT_METHODS
        return False

    def call_lambda(self, lam, ak, kk, fr):
        """A lambda bound to a name is a same-file helper: inline it (spec: reachable helpers)."""
        sub = Frame(parent=fr, cls=fr.cls)
        params = [a.arg for a in lam.args.args]
        for i, p in enumerate(params):
            sub.vars[p] = ak[i] if i < len(ak) else kk.get(p, X)
        return self.eval(lam.body, sub)

    def call_name(self, n, name, ak, kk, fr):
        lam = fr.find_lambda(name)
        if lam is not None:
            return self.call_lambda(lam, ak, kk, fr)
        loc = fr.find_func(name)
        if loc is not None:
            fd, defr = loc
            return self.call_func(fd, None, ak, kk, parent=defr)
        if fr.lookup(name) is not None:
            return self.v(f"call of a local value {name}", n)
        if name in self.m.funcs:
            return self.call_func(self.m.funcs[name], None, ak, kk)
        if name in self.m.classes:
            return self.v(f"constructs same-file class {name}", n)
        q = fr.find_import(name) or self.m.imports.get(name)
        if q is not None:
            return self.call_q(n, self.norm_q(q), ak, kk, fr)
        return self.builtin(n, name, ak, kk, fr)

    @staticmethod
    def norm_q(q):
        for a, b in (("posixpath.", "os.path."), ("genericpath.", "os.path."), ("pathlib.PosixPath", "pathlib.Path"),
                     ("pathlib.PurePosixPath", "pathlib.Path"), ("pathlib.PurePath", "pathlib.Path"),
                     ("pathlib.WindowsPath", "pathlib.Path")):
            if q.startswith(a):
                q = b + q[len(a):]
        return q

    def builtin(self, n, name, ak, kk, fr):
        allk = ak + list(kk.values())
        if X in allk and name not in ("print",):
            return X if name in ("len", "str", "list", "sorted", "set", "tuple", "any", "all", "bool", "isinstance",
                                 "enumerate", "zip", "reversed", "iter", "frozenset", "repr", "range", "dict") \
                else self.v(f"builtin {name} over unknown value", n)
        if name == "len":
            k = ak[0] if ak else X
            return C if k in (L, W, E, Q, V, N) else (K if k == K else self.v("len of non-collection", n))
        if name in ("any", "all"):
            k = ak[0] if ak else X
            if name == "all" and k in (L, V, W, E):
                return self.v("all(...) over a listing (universal: depends on absence of other entries)", n)
            return K if k == K else B
        if name in ("sorted", "list", "tuple", "set", "frozenset", "reversed", "iter"):
            return ak[0] if ak else K
        if name == "str" or name == "repr":
            return ak[0] if ak and ak[0] in (K, N) else (self.v("str() of non-path", n) if ak else K)
        if name == "bool":
            k = ak[0] if ak else K
            return K if k == K else B
        if name == "enumerate":
            return E if ak and ak[0] in (L, W, E) else (K if all(k == K for k in ak) else X)
        if name == "zip":
            return K if all(k == K for k in ak) else L
        if name == "range":
            return K if all(k == K for k in ak) else self.v("range over a count", n)
        if name == "isinstance" or name == "issubclass":
            return K
        if name == "print":
            return K
        if name == "dict":
            return K if all(k == K for k in allk) else L
        if name == "open":
            # A write-only open does not read content (spec clause 3 forbids *reads*); a read mode
            # (or the default "r") does.
            if self.open_is_write(n, 1):
                return K
            return self.v("open() reads a file", n)
        if name in PURE_BUILTIN_VALUE:
            return K if all(k == K for k in allk) else self.v(f"{name}() computes a value from fs-derived data", n)
        if name in ("exit", "quit"):
            return self.v("exit()", n)
        if name in ("map", "filter", "next", "getattr", "hasattr", "setattr", "eval", "exec", "compile", "input",
                    "__import__", "globals", "locals"):
            return self.v(f"builtin {name}", n)
        if hasattr(builtins, name) and isinstance(getattr(builtins, name), type) and \
                issubclass(getattr(builtins, name), BaseException):
            return K
        return self.v(f"call into undefined name {name}", n)

    def call_q(self, n, q, ak, kk, fr):
        allk = ak + list(kk.values())
        if q in EXIST_Q or q in LIST_Q or q == "os.access":
            self.fs_touch += 1
        if q in EXIST_Q:
            if allk and all(self.pathish(k) for k in allk):
                return B
            return X if X in allk else self.v(f"{q} on a non-path", n)
        if q == "os.access":
            mode = n.args[1] if len(n.args) > 1 else None
            if mode is None:
                for kw in n.keywords:
                    if kw.arg == "mode":
                        mode = kw.value
            ok = mode is not None and (self.qname(mode, fr) == "os.F_OK" or (
                isinstance(mode, ast.Constant) and mode.value == 0))
            if ok and self.pathish(ak[0]):
                return B
            return self.v("os.access with a permission mode", n)
        if q in LIST_Q:
            if allk and all(self.pathish(k) for k in allk):
                return LIST_Q[q]
            if q == "os.listdir" and not allk:
                return L
            return X if X in allk else self.v(f"{q} on a non-path", n)
        if q in ("fnmatch.fnmatch", "fnmatch.fnmatchcase") and allk and all(k == K for k in allk):
            # A name/pattern match over constant strings is a value comparison, not a path state.
            return self.v("value comparison (name pattern match)", n)
        if q in PURE_Q:
            if X in allk:
                return X
            if all(k in (K, N) for k in allk):
                return N if N in allk else K
            return self.v(f"{q} over a listing/count", n)
        if q in NEUTRAL_Q or q.startswith(NEUTRAL_PREFIX):
            return K
        if q in MUTATE_Q:
            return K          # a filesystem mutation is a write, not a read
        if q == "pytest.fail":
            self.fail_site(fr, n)
            return K
        if q in ("pytest.raises", "pytest.warns", "pytest.approx", "pytest.importorskip", "pytest.deprecated_call"):
            return self.v(f"{q} (behaviour/value)", n)
        if q.startswith("re."):
            return K if all(k in (K, N) for k in allk) else self.v("re over fs-derived data", n)
        if q.startswith("os.path.") or q.startswith("os."):
            return self.v(f"{q} (size/stat/exec/mutation/other os call)", n)
        if q.split(".")[0] == "<local>":
            return self.v("U: call into a non-captured local module", n)
        return self.v(f"call into {q} (not a plain existence predicate)", n)

    def call_self(self, n, attr, ak, kk, fr):
        cn = self.cur_cls
        if cn:
            fm = self.m.find_method(cn, attr)
            if fm:
                fd, owner = fm
                return self.call_func(fd, owner, ak, kk, bound_self=True)
        if attr in ASSERT_METHODS:
            return self.unittest_assert(n, attr, ak, fr)
        if attr in FAIL_SELF:
            self.fail_site(fr, n)
            return K
        if attr in NEUTRAL_SELF:
            return K
        return self.v(f"self.{attr}(...) not defined in the file", n)

    def unittest_assert(self, n, attr, ak, fr):
        args = n.args
        if attr in ("assertTrue", "failUnless", "assert_"):
            k = ak[0] if ak else X
            self.record_assert(k, n, fr)
        elif attr in ("assertFalse", "failIf"):
            k = ak[0] if ak else X
            self.record_assert(B if k in FS else k, n, fr)
        elif attr in ("assertIsNone", "assertIsNotNone"):
            k = ak[0] if ak else X
            self.record_assert(B if k in FS else (self.v("assertIsNone on a value", n) if k != K else K), n, fr)
        elif attr in CMP_FOR_ASSERT and len(args) >= 2:
            k = self.cmp1(CMP_FOR_ASSERT[attr](), args[0], ak[0], args[1], ak[1], n, fr)
            self.record_assert(k, n, fr)
        else:
            self.v(f"unittest {attr}", n)
        return K

    def call_method(self, n, rv, rk, attr, ak, kk, fr):
        allk = ak + list(kk.values())
        if rk == X:
            return self.v(f".{attr}() on an unknown/content value", n)
        if rk in (K, N):
            if attr in EXIST_M:
                self.fs_touch += 1
                return B
            if attr in LIST_M:
                self.fs_touch += 1
                return LIST_M[attr]
            if attr in ("issubset", "issuperset", "isdisjoint") and allk and allk[0] in (L, W, K):
                if attr == "issubset" and rk == K and allk[0] == L:
                    return B
                if attr == "isdisjoint":
                    return B if allk[0] in (L, K) else X
                if rk == K and attr == "issubset" and allk[0] == K:
                    return K
                return self.v(f"{attr} orientation (extras/exact set)", n)
            if attr in PATH_PURE_M or attr in STR_M:
                if X in allk:
                    return X
                if all(k in (K, N) for k in allk):
                    return N if (rk == N or N in allk) else K
                return self.v(f".{attr}() over a listing/count", n)
            if attr in MUTATORS and isinstance(rv, ast.Name):
                self.mutate(rv.id, allk, fr, n)
                return K
            if attr in WRITE_M:
                # A filesystem write is not a read (spec clause 3); the operational definition names
                # touch/mkdir as the way presence is created.
                return C if attr in WRITE_COUNT_M else K
            if attr in FILE_SIDE_EFFECT_M:
                return K          # writing to / closing a file handle reads nothing
            if attr == "open":
                if self.open_is_write(n, 0):
                    return K
                return self.v(".open() reads a file", n)
            return self.v(f".{attr}() on a path/name (read/write/stat/command)", n)
        if rk in (L, W, E, Q, V):
            if attr in MUTATORS and isinstance(rv, ast.Name):
                self.mutate(rv.id, allk, fr, n)
                return K
            if attr in ("copy", "sort", "reverse"):
                return rk
            if attr in ("issuperset", "isdisjoint") and allk and allk[0] in (K, L):
                return B
            if attr == "issubset":
                return self.v("listing.issubset(...) (extras/exact set)", n)
            if attr in ("keys", "values", "items"):
                return rk
            return self.v(f".{attr}() on a listing (count/pick)", n)
        if rk == F:
            return self.v(f"call of function value .{attr}", n)
        return self.v(f".{attr}() on {rk}", n)

    def mutate(self, name, allk, fr, n):
        cur = fr.lookup(name)
        if cur is None:
            return
        add = join_all(allk)
        if X in allk:
            self.set_var(fr, name, X)
            return
        if cur == K and add == K:
            return
        self.set_var(fr, name, L)

    # -- function inlining -----------------------------------------------------------------------
    def call_func(self, fd, owner, ak, kk, parent=None, bound_self=False, fixture_params=None):
        key = id(fd)
        if key in self.stack:
            return K          # cycle guard: contributes nothing new
        if len(self.stack) > 40:
            return self.v("call depth limit", fd)
        mkey = (key, tuple(ak), tuple(sorted(kk.items())), bound_self, owner)
        if mkey in self.memo:
            return self.memo[mkey]
        self.stack.append(key)
        saved_cls = self.cur_cls
        if owner:
            self.cur_cls = owner
        fr = Frame(parent=parent, cls=owner)
        a = fd.args
        params = [x.arg for x in a.posonlyargs + a.args]
        defaults = {}
        pos_all = a.posonlyargs + a.args
        for p, d in zip(pos_all[len(pos_all) - len(a.defaults):], a.defaults):
            defaults[p.arg] = d
        for p, d in zip(a.kwonlyargs, a.kw_defaults):
            if d is not None:
                defaults[p.arg] = d
        allp = params + [x.arg for x in a.kwonlyargs]
        pos = list(ak)
        if bound_self and any(dotted(d) == "staticmethod" for d in fd.decorator_list):
            bound_self = False
        if bound_self and params:
            fr.vars[params[0]] = S
            params_rest = params[1:]
        else:
            params_rest = params
        for i, p in enumerate(params_rest):
            if i < len(pos):
                fr.vars[p] = pos[i]
            elif p in kk:
                fr.vars[p] = kk[p]
            elif fixture_params is not None and p in fixture_params:
                fr.vars[p] = fixture_params[p]
            elif p in defaults:
                fr.vars[p] = self.eval(defaults[p], self.modframe)
            else:
                fr.vars[p] = X
        for p in [x.arg for x in a.kwonlyargs]:
            fr.vars[p] = kk.get(p, self.eval(defaults[p], self.modframe) if p in defaults else X)
        stmts = fd.body
        self.exec_stmts(stmts, fr)
        ret = join_all(fr.rets)
        self.cur_cls = saved_cls
        self.stack.pop()
        self.memo[mkey] = ret
        return ret

    # -- assertions ------------------------------------------------------------------------------
    def universal(self, fr, node) -> bool:
        f = fr
        for t, k in fr.ctrl:
            if t == "for" and k in (L, W, E):
                self.v("assertion inside a loop over a listing (universal: depends on absence of other entries)", node)
                return True
        return False

    def record_assert(self, k, node, fr=None):
        if fr is not None and self.universal(fr, node):
            return
        if k == X:
            self.v("assertion depends on content/value/unknown", node)
        elif k == K:
            self.v("assertion depends on no path state (constant/computed value)", node)
        else:
            self.fs_asserts += 1

    def fail_site(self, fr, node):
        ks = [k for t, k in fr.ctrl if t in ("if", "exc")]
        if X in ks:
            self.v("failure guarded by an unknown/content condition", node)
        elif self.universal(fr, node):
            return
        elif any(k in FS for k in ks):
            self.fs_asserts += 1
        else:
            self.v("unconditional or constant-guarded failure", node)

    # -- statements ------------------------------------------------------------------------------
    def exec_stmts(self, stmts, fr):
        guard = None
        pushed = False
        n = len(stmts)
        for i, s in enumerate(stmts):
            if guard is not None and not pushed:
                fr.ctrl.append(("if", guard))
                pushed = True
            self.stmt(s, fr)
            if fr.exit_guard is not None:
                guard = fr.exit_guard
                fr.exit_guard = None
        if pushed:
            fr.ctrl.pop()

    def stmt(self, s, fr):
        t = type(s).__name__
        m = getattr(self, "s_" + t, None)
        if m is not None:
            m(s, fr)
        # Pass, Break, Continue, Global, Nonlocal, Delete, ClassDef: nothing reachable of interest

    def s_FunctionDef(self, s, fr):
        fr.funcs[s.name] = (s, fr)

    s_AsyncFunctionDef = s_FunctionDef

    def s_Import(self, s, fr):
        # The spec forbids *importing and calling* the task's own deliverable.  An import that is
        # never used does not decide the verdict, so it is not a violation by itself; a call into it
        # is caught by call_q ("<local>..." / foreign module).
        for a in s.names:
            if a.asname:
                fr.imports[a.asname] = a.name
            else:
                fr.imports[a.name.split(".")[0]] = a.name.split(".")[0]

    def s_ImportFrom(self, s, fr):
        for a in s.names:
            if a.name == "*":
                continue
            fr.imports[a.asname or a.name] = ("<local>" if s.level else (s.module or "")) + "." + a.name

    def s_Expr(self, s, fr):
        if isinstance(s.value, ast.Constant):
            return
        self.eval(s.value, fr)

    def s_Assign(self, s, fr):
        k = self.eval(s.value, fr)
        for t in s.targets:
            self.bind(t, k, fr, s.value)

    def s_AnnAssign(self, s, fr):
        if s.value is not None:
            self.bind(s.target, self.eval(s.value, fr), fr, s.value)

    def s_AugAssign(self, s, fr):
        k = self.eval(s.value, fr)
        if isinstance(s.target, ast.Name):
            old = fr.lookup(s.target.id)
            old = X if old is None else old
            if X in (old, k):
                new = X
            elif old == K and k == K and not self.ctrl_fs(fr):
                new = K
            elif isinstance(s.op, ast.Add) and old in (K, L, W, E) and k in (K, L, W, E, N) and \
                    (old in (L, W, E) or k in (L, W, E)):
                new = L
            elif isinstance(s.op, ast.Add) and old in (K, N) and k in (K, N) and not self.ctrl_fs(fr):
                new = N if N in (old, k) else K
            else:
                new = C
            self.set_var(fr, s.target.id, new)
        else:
            self.bind(s.target, k, fr, None)

    def s_Assert(self, s, fr):
        t = s.test
        if isinstance(t, ast.Constant):
            if not t.value:
                self.fail_site(fr, s)
            return
        old_ia = fr.in_assert
        fr.in_assert = True
        try:
            k = self.eval(t, fr)
        finally:
            fr.in_assert = old_ia
        self.record_assert(k, s, fr)

    def s_Raise(self, s, fr):
        self.fail_site(fr, s)

    def s_Return(self, s, fr):
        fr.rets.append(self.eval(s.value, fr) if s.value is not None else K)

    def s_If(self, s, fr):
        tk = self.eval(s.test, fr)
        if tk == X:
            self.v("branch on unknown/content value", s)
        fr.ctrl.append(("if", tk))
        self.exec_stmts(s.body, fr)
        self.exec_stmts(s.orelse, fr)
        fr.ctrl.pop()
        if not s.orelse and tk in FS and self.exits(s.body):
            # The rest of the block is reached only when the condition is FALSE, so a failure there
            # is still path-dependent (``if path.exists(): return`` followed by ``pytest.fail``).
            fr.exit_guard = tk

    @staticmethod
    def exits(body) -> bool:
        """True when the block always leaves the enclosing block (return/raise/fail)."""
        if not body:
            return False
        st = body[-1]
        if isinstance(st, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
            return True
        if isinstance(st, ast.If) and not st.orelse:
            return Run.exits(st.body)
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
            nm = dotted(st.value.func)
            if nm and nm.split(".")[-1] == "fail":
                return True
        return False

    def s_For(self, s, fr):
        ik = self.eval(s.iter, fr)
        self.bind(s.target, self.elem(ik), fr, None)
        fr.ctrl.append(("for", ik))
        self.break_stack.append(None)
        self.exec_stmts(s.body, fr)
        bg = self.break_stack.pop()
        if bg is not None:
            # The else-branch of a for-loop runs only when the loop was not broken out of.  When the
            # break is guarded by a path condition, that branch is reached exactly when the
            # condition is false, so a failure there is still path-dependent.
            fr.ctrl.append(("if", bg))
            self.exec_stmts(s.orelse, fr)
            fr.ctrl.pop()
        else:
            self.exec_stmts(s.orelse, fr)
        fr.ctrl.pop()

    def s_Break(self, s, fr):
        if self.break_stack:
            g = None
            for t, k in reversed(fr.ctrl):
                if t == "if":
                    g = k
                    break
                if t in ("for", "while"):
                    break
            if g is not None and g in FS:
                cur = self.break_stack[-1]
                self.break_stack[-1] = g if cur is None else join(cur, g)

    s_AsyncFor = s_For

    def s_While(self, s, fr):
        tk = self.eval(s.test, fr)
        fr.ctrl.append(("while", tk))
        self.exec_stmts(s.body, fr)
        self.exec_stmts(s.orelse, fr)
        fr.ctrl.pop()

    def s_Try(self, s, fr):
        before = self.fs_touch
        self.exec_stmts(s.body, fr)
        hk = B if self.fs_touch > before else K    # an exception can only encode path state if the body touched paths
        for h in s.handlers:
            if h.name:
                fr.vars[h.name] = X
            fr.ctrl.append(("exc", hk))
            self.exec_stmts(h.body, fr)
            fr.ctrl.pop()
        self.exec_stmts(s.orelse, fr)
        self.exec_stmts(s.finalbody, fr)

    s_TryStar = s_Try

    def s_With(self, s, fr):
        for it in s.items:
            k = self.eval(it.context_expr, fr)
            if it.optional_vars is not None:
                self.bind(it.optional_vars, k if k in (K, N) else X, fr, None)
        self.exec_stmts(s.body, fr)

    s_AsyncWith = s_With

    def s_Match(self, s, fr):
        self.eval(s.subject, fr)
        for c in s.cases:
            self.exec_stmts(c.body, fr)


# ---- entry points ---------------------------------------------------------------------------------
def test_units(tree: ast.Module):
    """-> [(key, funcdef, class name | None)]"""
    out = []
    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name.startswith("test_"):
            out.append((st.name, st, None))
        elif isinstance(st, ast.ClassDef):
            for sub in st.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name.startswith("test_"):
                    out.append((f"{st.name}.{sub.name}", sub, st.name))
    return out


def parametrized(fd, run: Run):
    names = {}
    for d in fd.decorator_list:
        if isinstance(d, ast.Call):
            nm = dotted(d.func) or ""
            if nm.endswith("parametrize") and len(d.args) >= 2:
                a0 = d.args[0]
                if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                    ids = [x.strip() for x in a0.value.replace(",", " ").split() if x.strip()]
                else:
                    ids = [e.value for e in getattr(a0, "elts", []) if isinstance(e, ast.Constant)]
                vk = run.eval(d.args[1], run.modframe)
                pk = {K: K, L: N}.get(vk, X)
                for i in ids:
                    names[i] = pk
    return names


def analyze_one(mod: Module, fd, cname):
    r = Run(mod)
    r.cur_cls = cname
    fr = Frame(cls=cname)
    selfk = S if cname else None
    params = [x.arg for x in fd.args.posonlyargs + fd.args.args] + [x.arg for x in fd.args.kwonlyargs]
    pm = parametrized(fd, r)
    if cname and params:
        fr.vars[params[0]] = S
        params = params[1:]
    # implicit setup
    if IMPLICIT_SETUP:
        for sf in SETUP_FUNCS:
            if sf in mod.funcs:
                r.call_func(mod.funcs[sf], None, [], {})
        if cname:
            for sm in SETUP_METHODS:
                fm = mod.find_method(cname, sm)
                if fm:
                    r.call_func(fm[0], fm[1], [], {}, bound_self=True)
        for afd, ac in mod.autouse:
            if ac is None or (cname and ac in mod.class_chain(cname)):
                r.call_func(afd, ac, [], {}, bound_self=bool(ac))
    for p in params:
        if p in pm:
            fr.vars[p] = pm[p]
        elif p in mod.fixtures:
            r_fd, r_cls = mod.fixtures[p]
            if p not in r.fixcache:
                r.fixcache[p] = None
                fpar = {}
                r.fixcache[p] = r.call_func(r_fd, r_cls, [], {}, bound_self=bool(r_cls),
                                            fixture_params=r.fixture_args(r_fd, r_cls, pm))
            fr.vars[p] = r.fixcache[p] if r.fixcache[p] is not None else X
        elif p in TMP_FIXTURES:
            fr.vars[p] = K
        else:
            fr.vars[p] = X
    a = fd.args
    pos_all = a.posonlyargs + a.args
    r.exec_stmts(fd.body, fr)
    reasons = list(r.viol)
    if not reasons and r.fs_asserts == 0:
        reasons.append("no assertion reached that tests path existence")
    return ("P1" if not reasons else "P0"), reasons


def _fixture_args(self, fd, cls, pm):
    out = {}
    for x in fd.args.posonlyargs + fd.args.args + fd.args.kwonlyargs:
        p = x.arg
        if p in ("self", "cls"):
            continue
        if p in self.m.fixtures and p != fd.name:
            if p not in self.fixcache:
                self.fixcache[p] = None
                f2, c2 = self.m.fixtures[p]
                self.fixcache[p] = self.call_func(f2, c2, [], {}, bound_self=bool(c2),
                                                  fixture_params=self.fixture_args(f2, c2, pm))
            out[p] = self.fixcache[p] if self.fixcache[p] is not None else X
        elif p in TMP_FIXTURES:
            out[p] = K
        elif p in pm:
            out[p] = pm[p]
        else:
            out[p] = X
    return out


Run.fixture_args = _fixture_args


def classify_detail(src: str) -> dict[str, tuple[str, list[str]]]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = ast.parse(src)
    except (SyntaxError, ValueError, MemoryError, RecursionError):
        return {}
    mod = Module(tree)
    out = {}
    for key, fd, cname in test_units(tree):
        try:
            out[key] = analyze_one(mod, fd, cname)
        except RecursionError:
            out[key] = ("P0", ["recursion limit"])
        except Exception as e:          # an analyser bug must not lose a test id: U -> P0
            out[key] = ("P0", [f"U: analyser error {type(e).__name__}"])
    return out


def classify_source(src: str) -> dict[str, str]:
    return {k: v[0] for k, v in classify_detail(src).items()}


def sha256_self() -> str:
    return hashlib.sha256(open(__file__, "rb").read()).hexdigest()


# ---- selftest ---------------------------------------------------------------------------------------
HDR = "import os, json, subprocess, shutil\nfrom pathlib import Path\nimport pytest\nOUT = '/app/out.txt'\nD = '/app'\n"

CASES: list[tuple[str, str, dict]] = [
    ("spec1 exists", "def test_f(): assert Path('/app/out.txt').exists()", {"test_f": "P1"}),
    ("spec2 content", "def test_f():\n    p = Path('/app/out.txt'); assert p.exists(); assert p.read_text().strip() == '42'",
     {"test_f": "P0"}),
    ("spec3 isfile and isdir", "def test_f(): assert os.path.isfile(OUT) and os.path.isdir(D)", {"test_f": "P1"}),
    ("spec4 size", "def test_f(): assert os.path.getsize(OUT) > 0", {"test_f": "P0"}),
    ("spec5 subprocess", "def test_f():\n    subprocess.run(['x'], check=True)\n    assert Path(OUT).exists()",
     {"test_f": "P0"}),
    ("spec6 helper Y", "def _ok(): return Path(OUT).exists()\ndef test_f(): assert _ok()", {"test_f": "P1"}),
    ("spec7 helper N", "def _ok(): return json.loads(Path(OUT).read_text())['k'] == 1\ndef test_f(): assert _ok()",
     {"test_f": "P0"}),
    ("spec8 pass", "def test_f(): pass", {"test_f": "P0"}),
    ("helper chain depth 3",
     "def a(): return os.path.exists(OUT)\ndef b(): return a() and os.path.isdir(D)\ndef c(): return b()\n"
     "def test_f(): assert c()", {"test_f": "P1"}),
    ("helper chain depth 3 content at the bottom",
     "def a(): return open(OUT).read() == 'x'\ndef b(): return a()\ndef c(): return b()\n"
     "def test_f(): assert c()", {"test_f": "P0"}),
    ("recursion Y",
     "def up(p):\n    if p == '/': return False\n    return os.path.exists(p) or up(os.path.dirname(p))\n"
     "def test_f(): assert up(OUT)", {"test_f": "P1"}),
    ("recursion N (cycle with content)",
     "def a(n):\n    if n: return b(n - 1)\n    return Path(OUT).read_text() == 'x'\ndef b(n): return a(n)\n"
     "def test_f(): assert a(3)", {"test_f": "P0"}),
    ("class based Y + N",
     "class TestX:\n    def _p(self): return Path(OUT)\n    def test_a(self): assert self._p().exists()\n"
     "    def test_b(self): assert self._p().read_text() == 'x'\n"
     "    def test_c(self): self.assertTrue(os.path.isdir(D))\n",
     {"TestX.test_a": "P1", "TestX.test_b": "P0", "TestX.test_c": "P1"}),
    ("unittest self.assertTrue exists + setUp attr",
     "import unittest\nclass T(unittest.TestCase):\n    def setUp(self): self.p = Path(OUT)\n"
     "    def test_x(self): self.assertTrue(self.p.exists())\n", {"T.test_x": "P1"}),
    ("unittest setUp runs a command",
     "import unittest\nclass T(unittest.TestCase):\n    def setUp(self): subprocess.run(['make'])\n"
     "    def test_x(self): self.assertTrue(os.path.exists(OUT))\n", {"T.test_x": "P0"}),
    ("fixture argument Y",
     "@pytest.fixture\ndef out(): return Path(OUT)\ndef test_f(out): assert out.is_file()", {"test_f": "P1"}),
    ("fixture argument N (fixture runs a command)",
     "@pytest.fixture\ndef built():\n    subprocess.run(['make'], check=True)\n    return Path(OUT)\n"
     "def test_f(built): assert built.is_file()", {"test_f": "P0"}),
    ("fixture chain via second fixture",
     "@pytest.fixture\ndef a(): return D\n@pytest.fixture\ndef b(a): return Path(a) / 'x'\n"
     "def test_f(b): assert b.exists()", {"test_f": "P1"}),
    ("unknown fixture (conftest) -> P0",
     "def test_f(workdir): assert (workdir / 'x').exists()", {"test_f": "P0"}),
    ("pytest.fail branch Y",
     "def test_f():\n    if not os.path.exists(OUT):\n        pytest.fail('missing')\n", {"test_f": "P1"}),
    ("pytest.fail branch N (content condition)",
     "def test_f():\n    if Path(OUT).read_text() != 'x':\n        pytest.fail('bad')\n", {"test_f": "P0"}),
    ("raise AssertionError branch Y",
     "def test_f():\n    if not Path(OUT).is_dir():\n        raise AssertionError('no')\n", {"test_f": "P1"}),
    ("unconditional pytest.fail is not existence",
     "def test_f():\n    pytest.fail('no')\n", {"test_f": "P0"}),
    ("os.listdir membership Y",
     "def test_f(): assert 'a.txt' in os.listdir(D)", {"test_f": "P1"}),
    ("os.listdir membership via variable",
     "def test_f():\n    names = os.listdir(D)\n    assert 'a.txt' in names and 'b.txt' in names", {"test_f": "P1"}),
    ("name set from iterdir Y",
     "def test_f():\n    names = {p.name for p in Path(D).iterdir()}\n    assert 'a.txt' in names", {"test_f": "P1"}),
    ("any over iterdir name Y",
     "def test_f(): assert any(p.name == 'x' for p in Path(D).iterdir())", {"test_f": "P1"}),
    ("any over iterdir suffix Y",
     "def test_f(): assert any(p.suffix == '.py' for p in Path(D).iterdir())", {"test_f": "P1"}),
    ("any over iterdir reading content N",
     "def test_f(): assert any('x' in p.read_text() for p in Path(D).iterdir() if p.is_file())", {"test_f": "P0"}),
    ("glob non-empty Y",
     "import glob\ndef test_f(): assert glob.glob('/app/*.py')", {"test_f": "P1"}),
    ("glob via len > 0 is a count N",
     "import glob\ndef test_f(): assert len(glob.glob('/app/*.py')) > 0", {"test_f": "P0"}),
    ("len(listdir) == 3 count N",
     "def test_f(): assert len(os.listdir(D)) == 3", {"test_f": "P0"}),
    ("len(listdir) >= 3 count N",
     "def test_f(): assert len(os.listdir(D)) >= 3", {"test_f": "P0"}),
    ("listing equality N",
     "def test_f(): assert sorted(os.listdir(D)) == ['a', 'b']", {"test_f": "P0"}),
    ("with open read N",
     "def test_f():\n    assert os.path.exists(OUT)\n    with open(OUT) as f:\n        data = f.read()\n", {"test_f": "P0"}),
    ("with open read and assert on data N",
     "def test_f():\n    with open(OUT) as f:\n        assert f.read().strip() == '42'\n", {"test_f": "P0"}),
    ("no assertion N", "def test_f():\n    x = os.path.exists(OUT)\n", {"test_f": "P0"}),
    ("empty module", "", {}),
    ("module without tests", "def helper(): return 1\nX = 3\n", {}),
    ("call into undefined import N",
     "from solution import run\ndef test_f():\n    run()\n    assert os.path.exists(OUT)\n", {"test_f": "P0"}),
    ("import deliverable then exists N (U)",
     "def test_f():\n    import solution\n    assert solution.ready() and os.path.exists(OUT)\n", {"test_f": "P0"}),
    ("comments and docstrings are not code",
     "def test_f():\n    '''runs subprocess.run and read_text'''\n    # json.load(open(OUT))\n    assert os.path.exists(OUT)\n",
     {"test_f": "P1"}),
    ("string constants are not code",
     "def test_f():\n    msg = 'subprocess.run(x)'\n    assert os.path.exists(OUT), msg\n", {"test_f": "P1"}),
    ("assert message reading content is not reached",
     "def test_f():\n    assert os.path.exists(OUT), open(OUT).read()\n", {"test_f": "P1"}),
    ("loop over constant names Y",
     "def test_f():\n    for n in ['a', 'b']:\n        assert os.path.exists(os.path.join(D, n))\n", {"test_f": "P1"}),
    ("loop flag set under listing",
     "def test_f():\n    found = False\n    for f in os.listdir(D):\n        if f.endswith('.py'):\n            found = True\n"
     "    assert found\n", {"test_f": "P1"}),
    ("loop counter -> count N",
     "def test_f():\n    n = 0\n    for f in os.listdir(D):\n        n += 1\n    assert n == 3\n", {"test_f": "P0"}),
    ("module constant with content N",
     "EXPECTED = json.loads(open('/app/e.json').read())\ndef test_f(): assert os.path.exists(OUT) and EXPECTED\n",
     {"test_f": "P0"}),
    ("os.access F_OK Y / R_OK N",
     "def test_a(): assert os.access(OUT, os.F_OK)\ndef test_b(): assert os.access(OUT, os.X_OK)\n",
     {"test_a": "P1", "test_b": "P0"}),
    ("is_symlink and not Y",
     "def test_f(): assert Path(OUT).is_symlink() or not Path(OUT).exists()", {"test_f": "P1"}),
    ("stat mode N",
     "def test_f(): assert Path(OUT).stat().st_mode & 0o111", {"test_f": "P0"}),
    ("parametrize constants Y",
     "@pytest.mark.parametrize('name', ['a', 'b'])\ndef test_f(name): assert Path(D, name).exists()", {"test_f": "P1"}),
    ("tmp_path fixture is pure",
     "def test_f(tmp_path): assert (tmp_path / 'x').exists()", {"test_f": "P1"}),
    ("monkeypatch fixture unknown N",
     "def test_f(monkeypatch):\n    monkeypatch.setenv('A', '1')\n    assert os.path.exists(OUT)\n", {"test_f": "P0"}),
    ("write then exists Y (a write is not a read)",
     "def test_f():\n    Path(OUT).write_text('x')\n    assert Path(OUT).exists()\n", {"test_f": "P1"}),
    ("try/except pytest.fail Y",
     "def test_f():\n    try:\n        os.listdir(D)\n    except OSError:\n        pytest.fail('x')\n", {"test_f": "P1"}),
    ("constant assertion only N", "def test_f(): assert 1 + 1 == 2", {"test_f": "P0"}),
    ("len == 0 is a count N",
     "def test_f(): assert len([f for f in Path(D).iterdir() if f.is_file()]) == 0", {"test_f": "P0"}),
    ("not glob (negated non-empty) Y",
     "import glob\ndef test_f(): assert not glob.glob('/app/*.tmp')", {"test_f": "P1"}),
    ("in-test import of third party N",
     "def test_f():\n    try:\n        import grpc\n    except ImportError:\n        assert False, 'x'\n",
     {"test_f": "P0"}),
    ("pick first glob match then exists Y",
     "def test_f():\n    src = list(Path(D).glob('pmars-*'))\n    assert src\n    assert (src[0] / 'debian').exists()\n",
     {"test_f": "P1"}),
    ("all() over a listing is universal N",
     "def test_f(): assert all(p.is_file() for p in Path(D).iterdir())", {"test_f": "P0"}),
    ("loop assert over a listing is universal N",
     "def test_f():\n    for f in os.listdir(D):\n        assert f.endswith('.py')\n", {"test_f": "P0"}),
    ("all() over constant names Y",
     "def test_f(): assert all(os.path.exists(p) for p in ['/a', '/b'])", {"test_f": "P1"}),
    ("resolve then exists Y",
     "def test_f(): assert Path(OUT).resolve().exists()", {"test_f": "P1"}),
    ("staticmethod helper and Class.method call",
     "class T:\n    @staticmethod\n    def ok(p): return os.path.exists(p)\n"
     "    def test_a(self): assert self.ok(OUT)\n    def test_b(self): assert T.ok(OUT)\n",
     {"T.test_a": "P1", "T.test_b": "P1"}),
    ("not os.path.exists Y / == True Y",
     "def test_a(): assert not os.path.exists(OUT)\ndef test_b(): assert os.path.exists(OUT) == True\n",
     {"test_a": "P1", "test_b": "P1"}),
    ("syntax error -> empty", "def test_f(:\n", {}),
    # --- fix round (round 53 pre-freeze; adversarial cases from C1ExecAdvCases) ---
    ("os.access keyword mode F_OK Y",
     "def test_f(): assert os.access(OUT, mode=os.F_OK)", {"test_f": "P1"}),
    ("len(listdir) > 0 is a count N",
     "def test_f(): assert len(os.listdir(D)) > 0", {"test_f": "P0"}),
    ("all([...]) over existence predicates Y",
     "def test_f(): assert all([Path('/a').exists(), Path('/b').exists()])", {"test_f": "P1"}),
    ("write-mode open then exists Y",
     "def test_f():\n    with open('/tmp/s.w', 'w') as f:\n        f.write('x')\n    assert Path(OUT).exists()\n",
     {"test_f": "P1"}),
    ("touch/mkdir then exists Y",
     "def test_f():\n    Path('/tmp/s3').touch()\n    Path('/tmp/s4').mkdir(exist_ok=True)\n"
     "    assert Path('/tmp/s3').exists()\n", {"test_f": "P1"}),
    ("for/else pytest.fail on exists Y",
     "def test_f():\n    for _ in range(10):\n        if os.path.exists(OUT):\n            break\n"
     "    else:\n        pytest.fail('never appeared')\n", {"test_f": "P1"}),
    ("import of a deliverable that is never called Y",
     "def test_f():\n    import solution\n    assert Path(OUT).exists()\n", {"test_f": "P1"}),
    ("value arithmetic inside the assertion condition N",
     "def test_f(): assert os.path.exists(OUT) and 2 * 2 == 4", {"test_f": "P0"}),
    ("lambda helper Y / N",
     "def test_a():\n    has = lambda p: os.path.exists(p)\n    assert has(OUT)\n"
     "def test_b():\n    has = lambda p: Path(p).read_text() == '1'\n    assert has(OUT)\n",
     {"test_a": "P1", "test_b": "P0"}),
    ("fixture teardown after the yield is reachable N",
     "@pytest.fixture\ndef staged():\n    yield Path(OUT)\n    print(Path(OUT).read_text())\n"
     "def test_f(staged): assert staged.exists()", {"test_f": "P0"}),
    ("request.param fixture used in a path Y",
     "@pytest.fixture(params=['a.txt'])\ndef fname(request):\n    return request.param\n"
     "def test_f(fname): assert Path(D, fname).exists()", {"test_f": "P1"}),
    ("unittest assertTrue(len(listdir) > 0) is a count N",
     "import unittest\nclass V(unittest.TestCase):\n    def test_true_len(self):\n"
     "        self.assertTrue(len(os.listdir(D)) > 0)\n", {"V.test_true_len": "P0"}),
    ("early return then pytest.fail Y",
     "def test_f():\n    if Path(OUT).exists():\n        return\n    pytest.fail('never created')\n",
     {"test_f": "P1"}),
    ("fnmatch value comparison ANDed with exists N",
     "import fnmatch\ndef test_f(): assert fnmatch.fnmatch('out.txt', '*.txt') and os.path.exists(OUT)\n",
     {"test_f": "P0"}),
    ("contextlib.suppress around an existence assert Y",
     "import contextlib\ndef test_f():\n    with contextlib.suppress(Exception):\n"
     "        assert os.path.exists(OUT)\n", {"test_f": "P1"}),
]


def selftest() -> int:
    fails = []
    for name, src, want in CASES:
        got = classify_source(HDR + src if src else "")
        if got != want:
            fails.append((name, want, got, classify_detail(HDR + src) if src else {}))
    for f in fails:
        print("FAIL", f[0], "want", f[1], "got", f[2], f[3])
    print(f"cases={len(CASES)} failures={len(fails)}")
    return 1 if fails else 0


def histogram(paths: list[str], why: bool) -> int:
    import collections
    tot = collections.Counter()
    for p in paths:
        src = open(p, encoding="utf-8", errors="replace").read()
        det = classify_detail(src)
        c = collections.Counter(v[0] for v in det.values())
        tot.update(c)
        print(f"{p}: " + " ".join(f"{k}={c[k]}" for k in ("P1", "P0")))
        if why:
            for k in sorted(det):
                print(f"  {det[k][0]} {k}: {'; '.join(det[k][1][:3])}")
    print("TOTAL " + " ".join(f"{k}={tot[k]}" for k in ("P1", "P0")))
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    why = "--why" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    return histogram(paths, why)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
