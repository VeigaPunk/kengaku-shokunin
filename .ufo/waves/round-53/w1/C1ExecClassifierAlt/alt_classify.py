"""Alt presence-only classifier (round 53, C1) -- symbolic-execution-light.

Cross-check of the p1-spec, NOT the counted classifier.  Instead of matching call names against
a list of "content readers", every reachable expression is evaluated over a small abstract
domain and a test is P1 iff (a) nothing reachable has an effect other than inert path/name
algebra and (b) every reachable assertion condition evaluates to an existence-only value.

Abstract domain (tag of an abstract value):
  K    inert constant / path / string with no filesystem dependence
  E    boolean that depends only on existence or type of a path
  N    a name/path that came out of a directory listing (membership/name tests on it -> E)
  L    a listing (os.listdir, glob, iterdir, set of names ...): truthiness / membership -> E
  LEN  len() of a listing: only the zero / non-zero tests are existence
  LE   a collection of E booleans (comprehension); only all()/any() make it E
  T    anything else: content, size, command output, return values, counts, unknown code
Effects (subprocess, file reads, network, unknown calls ...) are tracked separately from values
and make the test P0 on their own.  Unknown calls count as effect (spec: U maps to P0).

classify_source(src) -> {key: 'P1'|'P0'}      keys 'name' or 'Class.name'
classify_detail(src) -> {key: {'cls','flags','why'}}   flags list spec holes touched
"""
from __future__ import annotations

import ast
import sys

K, E, N, L, LEN, LE, T = "K", "E", "N", "L", "LEN", "LE", "T"
PRIO = {K: 0, N: 1, L: 2, LEN: 3, E: 4, LE: 5, T: 6}

EXIST_FUNCS = {
    "os.path.exists", "os.path.isfile", "os.path.isdir", "os.path.islink", "os.path.lexists",
    "path.exists", "path.isfile", "path.isdir", "path.islink",
}
EXIST_METHODS = {"exists", "is_file", "is_dir", "is_symlink"}
LIST_FUNCS = {"os.listdir", "glob.glob", "glob.iglob", "os.scandir", "os.walk", "fnmatch.filter",
              "path.listdir"}
LIST_METHODS = {"iterdir", "glob", "rglob", "listdir"}
PURE_FUNCS = {
    "os.path.join", "os.path.dirname", "os.path.basename", "os.path.abspath", "os.path.normpath",
    "os.path.splitext", "os.path.split", "os.path.expanduser", "os.path.realpath",
    "os.path.relpath", "os.path.commonpath", "os.path.isabs", "os.getcwd", "os.fspath",
    "os.getenv", "os.environ.get", "pathlib.Path", "pathlib.PurePath", "pathlib.PosixPath",
    "pathlib.PurePosixPath", "pathlib.Path.cwd", "pathlib.Path.home", "tempfile.gettempdir",
    "shlex.quote", "os.path.sep", "os.sep", "os.cpu_count",
}
BENIGN_FUNCS = {
    "print", "time.sleep", "pytest.skip", "pytest.xfail", "os.makedirs", "os.mkdir", "os.chdir",
    "warnings.warn", "logging.info", "logging.debug", "logging.warning", "logging.error",
    "pytest.importorskip",
}
FAIL_FUNCS = {"pytest.fail", "fail"}
BUILTIN_PURE = {"str", "repr", "int", "float", "bool", "bytes", "format", "abs", "round", "ord",
                "chr", "hash", "id", "type", "dict", "list", "set", "tuple", "frozenset",
                "sorted", "reversed", "enumerate", "zip", "map", "filter", "iter", "len", "any",
                "all", "next", "min", "max", "sum", "range", "isinstance", "issubclass",
                "callable", "getattr", "hasattr", "slice"}
STR_METHODS = {"join", "joinpath", "with_name", "with_suffix", "with_stem", "resolve", "absolute",
               "expanduser", "as_posix", "format", "strip", "lstrip", "rstrip", "lower", "upper",
               "split", "rsplit", "splitlines", "replace", "relative_to", "get", "items", "keys",
               "values", "encode", "decode", "title", "capitalize", "partition", "rpartition",
               "removeprefix", "removesuffix", "__str__", "__fspath__", "is_absolute", "mkdir",
               "touch", "append", "extend", "add", "update", "sort", "reverse", "copy", "pop",
               "write_text", "write_bytes", "unlink", "rmdir", "setdefault", "insert", "remove",
               "discard", "clear"}
BOOL_NAME_METHODS = {"startswith", "endswith", "match", "fnmatch", "is_relative_to", "isdigit",
                     "isalpha", "isalnum", "isupper", "islower", "isspace", "isidentifier",
                     "__contains__"}
READ_METHODS = {"read_text", "read_bytes", "open", "stat", "lstat", "readlink", "owner", "group",
                "samefile", "chmod", "read", "readline", "readlines", "iter_lines", "getsize",
                "is_mount"}
TMP_PARAMS = {"tmp_path", "tmp_path_factory", "tmpdir", "tmpdir_factory"}
MODULE_CONSTS = {"os.sep", "os.F_OK", "os.curdir", "os.pardir", "os.linesep", "os.name",
                 "os.environ", "os.path.sep", "sys.platform", "sys.executable", "os.pathsep",
                 "sys.argv", "sys.version_info", "os.altsep", "os.devnull"}

MAX_DEPTH = 8


def join(*vals):
    """Least upper bound used for merging branches/values."""
    vals = [v for v in vals if v is not None]
    if not vals:
        return (K, None)
    best = max(vals, key=lambda v: PRIO[v[0]])
    return (best[0], best[1] if all(v == best for v in vals) else None)


def tag(v):
    return v[0]


def deco_names(fn):
    out = []
    for d in fn.decorator_list:
        node = d.func if isinstance(d, ast.Call) else d
        out.append(ast.unparse(node))
    return out


def is_fixture(fn):
    return any(n in ("pytest.fixture", "fixture", "pytest.yield_fixture") for n in deco_names(fn))


def is_autouse(fn):
    for d in fn.decorator_list:
        if isinstance(d, ast.Call) and ast.unparse(d.func) in ("pytest.fixture", "fixture"):
            for kw in d.keywords:
                if kw.arg == "autouse" and isinstance(kw.value, ast.Constant) and kw.value.value:
                    return True
    return False


class Ctx:
    def __init__(self):
        self.effects: list[str] = []
        self.asserts: list[tuple[str, int]] = []
        self.flags: set[str] = set()


class Frame:
    def __init__(self, env, cls=None, locals_=None):
        self.env = env
        self.env_ref = env
        self.cls = cls
        self.local_funcs = dict(locals_ or {})
        self.guards: list[tuple] = []
        self.rets: list[tuple] = []
        self.depth = 0


class Interp:
    def __init__(self, tree: ast.Module, implicit: bool = False):
        self.tree = tree
        self.implicit = implicit
        self.imports: dict[str, str] = {}
        self.funcs: dict[str, ast.FunctionDef] = {}
        self.classes: dict[str, ast.ClassDef] = {}
        self.methods: dict[str, dict[str, ast.FunctionDef]] = {}
        self.genv: dict[str, tuple] = {}
        self.modctx = Ctx()
        self.ctx = self.modctx
        self.stack_depth = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.imports[(a.asname or a.name).split(".")[0]] = (
                        a.name if a.asname else a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    for a in node.names:
                        self.imports[a.asname or a.name] = node.module + "." + a.name
                else:
                    for a in node.names:
                        self.imports[a.asname or a.name] = "<local>." + a.name
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.funcs[node.name] = node
            elif isinstance(node, ast.ClassDef):
                self.classes[node.name] = node
                self.methods[node.name] = {
                    n.name: n for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        # module level: values only; effects recorded in modctx (not reach per spec)
        fr = Frame(self.genv)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                                 ast.Import, ast.ImportFrom)):
                continue
            try:
                self.exec_stmt(node, fr)
            except RecursionError:
                pass

    # ------------------------------------------------------------------ helpers
    def effect(self, why, node=None):
        self.ctx.effects.append(f"{why}@{getattr(node, 'lineno', '?')}")

    def dotted(self, node, fr):
        """Dotted name if node is Name/Attribute chain whose root is a module/import (not a var)."""
        parts = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if not isinstance(cur, ast.Name):
            return None
        root = cur.id
        if root in fr.env or root in fr.local_funcs or root in self.genv:
            return None
        if root in self.imports:
            base = self.imports[root]
            if base.startswith("<local>"):
                base = "<local>." + root
            parts.append(base)
        else:
            parts.append(root)
        return ".".join(reversed(parts))

    def norm(self, dn):
        # canonicalise common aliases
        for a, b in (("os.path.", "os.path."), ("posixpath.", "os.path."), ("pathlib.Path", "pathlib.Path"),
                     ("pathlib.posixpath", "os.path")):
            if dn.startswith(a):
                return b + dn[len(a):]
        if dn == "Path":
            return "pathlib.Path"
        return dn

    # ------------------------------------------------------------------ expressions
    def ev(self, node, fr):
        m = getattr(self, "ev_" + type(node).__name__, None)
        if m is None:
            # unknown node: evaluate children for effects, result T
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, ast.expr):
                    self.ev(ch, fr)
            return (T, None)
        return m(node, fr)

    def ev_Constant(self, n, fr):
        return (K, n.value if isinstance(n.value, (bool, int)) else None)

    def ev_Name(self, n, fr):
        if n.id in fr.env:
            return fr.env[n.id]
        if n.id in self.genv:
            return self.genv[n.id]
        if n.id in ("True", "False", "None"):
            return (K, None)
        if n.id in self.imports:
            dn = self.imports[n.id]
            return (K, None) if dn in MODULE_CONSTS else (T, None)
        if n.id in self.funcs or n.id in self.classes:
            return (K, None)
        return (K, None) if n.id in BUILTIN_PURE else (T, None)

    def ev_JoinedStr(self, n, fr):
        return self.mix([self.ev(v, fr) for v in n.values])

    def ev_FormattedValue(self, n, fr):
        return self.ev(n.value, fr)

    def mix(self, vals):
        vals = [v for v in vals]
        if any(tag(v) == T for v in vals):
            return (T, None)
        if any(tag(v) in (N, L) for v in vals):
            return (N, None)
        if any(tag(v) in (E, LE, LEN) for v in vals):
            return (T, None)
        return (K, None)

    def ev_List(self, n, fr):
        return self.container(n.elts, fr)

    ev_Tuple = ev_Set = ev_List

    def ev_Dict(self, n, fr):
        return self.container([x for x in n.keys if x is not None] + list(n.values), fr)

    def container(self, elts, fr):
        vals = [self.ev(e, fr) for e in elts]
        if any(tag(v) == T for v in vals):
            return (T, None)
        if any(tag(v) in (N, L) for v in vals):
            return (L, None)
        if any(tag(v) in (E, LE, LEN) for v in vals):
            return (LE, None)
        return (K, None)

    def ev_Starred(self, n, fr):
        return self.ev(n.value, fr)

    def ev_IfExp(self, n, fr):
        self.ev(n.test, fr)
        return join(self.ev(n.body, fr), self.ev(n.orelse, fr))

    def ev_Lambda(self, n, fr):
        return (K, None)

    def ev_BoolOp(self, n, fr):
        vals = [self.ev(v, fr) for v in n.values]
        if any(tag(v) == T for v in vals):
            return (T, None)
        if any(tag(v) == LE for v in vals):
            return (T, None)
        if all(tag(v) == K for v in vals):
            return (K, None)
        if all(tag(v) == L for v in vals):
            return (L, None)
        if all(tag(v) in (K, N) for v in vals):
            return (N, None)
        return (E, None)

    def ev_UnaryOp(self, n, fr):
        v = self.ev(n.operand, fr)
        if isinstance(n.op, ast.Not):
            t = tag(v)
            if t in (K,):
                return (K, None)
            if t in (E, N, L, LEN):
                return (E, None)
            return (T, None)
        if tag(v) == K:
            c = v[1]
            if isinstance(n.op, ast.USub) and isinstance(c, int) and not isinstance(c, bool):
                return (K, -c)
            return (K, None)
        return (T, None)

    def ev_BinOp(self, n, fr):
        a = self.ev(n.left, fr)
        b = self.ev(n.right, fr)
        if tag(a) == T or tag(b) == T:
            return (T, None)
        if isinstance(n.op, (ast.BitOr, ast.BitAnd, ast.Sub)) and tag(a) == L and tag(b) in (L, K):
            return (L, None)
        if isinstance(n.op, ast.Add) and tag(a) == L and tag(b) in (L, K):
            return (L, None)
        if tag(a) in (E, LE, LEN) or tag(b) in (E, LE, LEN):
            return (T, None)
        if tag(a) in (N, L) or tag(b) in (N, L):
            return (N, None)
        return (K, None)

    def ev_Attribute(self, n, fr):
        dn = self.dotted(n, fr)
        if dn is not None:
            dn = self.norm(dn)
            if dn in MODULE_CONSTS or dn.startswith("os.environ"):
                return (K, None)
            return (T, None)
        base = self.ev(n.value, fr)
        t = tag(base)
        if n.attr in ("name", "stem", "suffix", "parent", "parents", "parts", "suffixes", "anchor"):
            return (N, None) if t in (N, L) else (K, None) if t == K else (T, None)
        if t == T:
            return (T, None)
        if n.attr in ("st_size", "st_mode", "st_mtime", "returncode", "stdout", "stderr", "text"):
            return (T, None)
        return (K, None) if t == K else (N, None) if t in (N,) else (T, None)

    def ev_Subscript(self, n, fr):
        base = self.ev(n.value, fr)
        self.ev(n.slice, fr)
        dn = self.dotted(n.value, fr)
        if dn is not None and self.norm(dn) in MODULE_CONSTS:
            return (K, None)
        t = tag(base)
        if t == L:
            return (N, None)
        if t in (K, N):
            return (t, None)
        return (T, None)

    def ev_Slice(self, n, fr):
        for x in (n.lower, n.upper, n.step):
            if x is not None:
                self.ev(x, fr)
        return (K, None)

    def comp_gen(self, n, fr):
        fr2 = Frame(dict(fr.env), fr.cls, fr.local_funcs)
        src = K
        for g in n.generators:
            it = self.ev(g.iter, fr)
            src = tag(it) if tag(it) in (L, T) else (src if src == L else tag(it))
            self.bind(g.target, self.elem(it), fr2)
            for c in g.ifs:
                self.ev(c, fr2)
        return fr2, src

    def ev_ListComp(self, n, fr):
        fr2, src = self.comp_gen(n, fr)
        if isinstance(n, ast.DictComp):
            self.ev(n.key, fr2)
            elt = self.ev(n.value, fr2)
        else:
            elt = self.ev(n.elt, fr2)
        t = tag(elt)
        if t == T or src == T:
            return (T, None)
        if t in (E, LE, LEN):
            return (LE, None)
        if src == L or t in (N, L):
            return (L, None)
        return (K, None)

    ev_SetComp = ev_GeneratorExp = ev_DictComp = ev_ListComp

    def ev_Await(self, n, fr):
        return self.ev(n.value, fr)

    def ev_Yield(self, n, fr):
        v = self.ev(n.value, fr) if n.value else (K, None)
        fr.rets.append(v)
        return (K, None)

    def ev_NamedExpr(self, n, fr):
        v = self.ev(n.value, fr)
        self.bind(n.target, v, fr)
        return v

    def ev_Compare(self, n, fr):
        vals = [self.ev(n.left, fr)] + [self.ev(c, fr) for c in n.comparators]
        out = []
        for i, op in enumerate(n.ops):
            out.append(self.compare(op, vals[i], vals[i + 1]))
        if any(tag(o) == T for o in out):
            return (T, None)
        if all(tag(o) == K for o in out):
            return (K, None)
        return (E, None)

    def compare(self, op, a, b):
        ta, tb = tag(a), tag(b)
        if isinstance(op, (ast.In, ast.NotIn)):
            if ta == T or tb == T:
                return (T, None)
            if tb == L and ta in (K, N, E):
                return (E, None)
            if tb == K and ta == N:
                return (E, None)
            if tb == K and ta == K:
                return (K, None)
            return (T, None)
        if ta == T or tb == T or LE in (ta, tb):
            return (T, None)
        if LEN in (ta, tb):
            other, ov = (b, tb) if ta == LEN else (a, ta)
            if ov != K or not isinstance(other[1], int) or isinstance(other[1], bool):
                return (T, None)
            c = other[1]
            # normalise to "len OP c"
            rev = (ta != LEN)
            cls = type(op)
            if rev:
                cls = {ast.Lt: ast.Gt, ast.Gt: ast.Lt, ast.LtE: ast.GtE, ast.GtE: ast.LtE}.get(cls, cls)
            ok = ((cls in (ast.Eq, ast.NotEq, ast.Gt, ast.LtE) and c == 0)
                  or (cls in (ast.GtE, ast.Lt) and c == 1)
                  or (cls is ast.Gt and c == 0))
            return (E, None) if ok else (T, None)
        if L in (ta, tb):
            if isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) and ta in (L, K) and tb in (L, K):
                return (E, None)
            return (T, None)
        if E in (ta, tb):
            other = b if ta == E else a
            if tag(other) == E:
                return (E, None)
            if tag(other) == K and (other[1] in (True, False, 0, 1) and other[1] is not None):
                return (E, None)
            return (T, None)
        if N in (ta, tb):
            return (E, None)
        return (K, None)

    # ------------------------------------------------------------------ calls
    def ev_Call(self, n, fr):
        func = n.func
        argv = [self.ev(a, fr) for a in n.args]
        kwv = [self.ev(k.value, fr) for k in n.keywords]
        allv = argv + kwv
        # --- same-file callables
        callee, bind_self, owner = self.resolve_callee(func, fr)
        if callee is not None:
            return self.call_user(callee, n, argv, kwv, fr, owner, bind_self)
        dn = self.dotted(func, fr) if isinstance(func, ast.Attribute) else None
        if dn is not None:
            dn = self.norm(dn)
            return self.call_module(dn, n, argv, allv, fr)
        if isinstance(func, ast.Attribute):
            base = self.ev(func.value, fr)
            return self.call_method(func.attr, base, n, argv, allv, fr)
        if isinstance(func, ast.Name):
            return self.call_name(func.id, n, argv, allv, fr)
        self.ev(func, fr)
        self.effect("indirect-call", n)
        return (T, None)

    def resolve_callee(self, func, fr):
        if isinstance(func, ast.Name):
            if func.id in fr.local_funcs:
                return fr.local_funcs[func.id], False, None
            if func.id in fr.env or func.id in self.genv:
                return None, False, None
            if func.id in self.funcs:
                return self.funcs[func.id], False, None
            return None, False, None
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            root = func.value.id
            if root in ("self", "cls") and fr.cls in self.methods and func.attr in self.methods[fr.cls]:
                return self.methods[fr.cls][func.attr], True, fr.cls
            if root in self.classes and func.attr in self.methods.get(root, {}):
                return self.methods[root][func.attr], False, root
        return None, False, None

    def call_user(self, fn, call, argv, kwv, fr, owner, bind_self):
        if self.stack_depth >= MAX_DEPTH:
            self.effect("recursion-limit", call)
            return (T, None)
        a = fn.args
        params = [p.arg for p in a.posonlyargs + a.args]
        env = {}
        if bind_self or (owner and params and params[0] in ("self", "cls")):
            if params and params[0] in ("self", "cls"):
                env[params[0]] = (K, None)
                params = params[1:]
        for p, v in zip(params, argv):
            env[p] = v
        kwnames = [k.arg for k in call.keywords]
        for k, v in zip(kwnames, kwv):
            if k:
                env[k] = v
        # defaults
        defaults = a.defaults
        for p, d in zip(params[len(params) - len(defaults):], defaults):
            if p not in env:
                env[p] = self.ev(d, Frame({}, owner or fr.cls))
        for p in params + [x.arg for x in a.kwonlyargs]:
            env.setdefault(p, (T, None))
        for kd, kp in zip(a.kw_defaults, a.kwonlyargs):
            if kd is not None and kp.arg not in kwnames:
                env[kp.arg] = self.ev(kd, Frame({}, fr.cls))
        if a.vararg:
            env[a.vararg.arg] = (T, None)
        if a.kwarg:
            env[a.kwarg.arg] = (T, None)
        fr2 = Frame(env, owner or fr.cls, fr.local_funcs)
        self.stack_depth += 1
        try:
            return self.run_body(fn, fr2)
        finally:
            self.stack_depth -= 1

    def run_body(self, fn, fr2):
        for st in fn.body:
            self.exec_stmt(st, fr2)
        if fr2.rets:
            return join(*fr2.rets)
        return (K, None)

    def call_name(self, name, n, argv, allv, fr):
        if name in self.imports:
            dn = self.imports[name]
            return self.call_module(self.norm(dn) if not dn.startswith("<local>") else dn, n, argv, allv, fr)
        if name in FAIL_FUNCS:
            self.fail(fr, n)
            return (K, None)
        ts = [tag(v) for v in allv]
        if name == "len":
            return (LEN, None) if ts and ts[0] in (L,) else (T, None) if ts and ts[0] != K else (T, None)
        if name in ("sorted", "list", "set", "tuple", "frozenset", "reversed", "iter", "enumerate",
                    "zip", "map", "filter"):
            if T in ts:
                return (T, None)
            if any(t in (L, N) for t in ts):
                return (L, None)
            if any(t in (E, LE, LEN) for t in ts):
                return (LE, None)
            return (K, None)
        if name in ("any", "all"):
            t = ts[0] if ts else K
            if t == LE:
                return (E, None)
            if t in (L, E, N):
                return (E, None)
            return (T, None) if t == T else (K, None)
        if name == "bool":
            t = ts[0] if ts else K
            if t in (E, N, L, LEN):
                return (E, None)
            return (t, None) if t in (K, T) else (T, None)
        if name == "next":
            t = ts[0] if ts else K
            return (N, None) if t in (L, N) else (T, None) if t == T else (K, None)
        if name in ("str", "repr", "format", "bytes", "abs", "round", "ord", "chr", "hash", "id",
                    "type", "dict"):
            return self.mix(allv) if all(t in (K, N, L, T) for t in ts) else (T, None)
        if name in ("int", "float", "min", "max", "sum", "isinstance", "issubclass", "getattr",
                    "hasattr", "callable", "slice", "range"):
            if name == "range" and all(t == K for t in ts):
                return (K, None)
            return (T, None) if any(t != K for t in ts) or name in ("isinstance", "getattr", "hasattr",
                                                                   "min", "max", "sum") else (K, None)
        if name == "open":
            self.effect("open", n)
            return (T, None)
        if name in BENIGN_FUNCS:
            return (K, None)
        # unknown / local-class constructor / exec / eval / __import__ ...
        if name in self.classes:
            return (K, None)
        self.effect(f"unknown-call:{name}", n)
        return (T, None)

    def call_module(self, dn, n, argv, allv, fr):
        ts = [tag(v) for v in allv]
        if dn in EXIST_FUNCS:
            return (E, None)
        if dn == "os.access":
            mode = ast.unparse(n.args[1]) if len(n.args) > 1 else ""
            if mode == "os.F_OK":
                return (E, None)
            self.effect("os.access-mode", n)
            return (T, None)
        if dn in LIST_FUNCS:
            return (L, None)
        if dn in PURE_FUNCS:
            if T in ts:
                return (T, None)
            return (N, None) if any(t in (N, L) for t in ts) else (K, None)
        if dn in BENIGN_FUNCS:
            return (K, None)
        if dn in FAIL_FUNCS:
            self.fail(fr, n)
            return (K, None)
        self.effect(f"call:{dn}", n)
        return (T, None)

    def call_method(self, attr, base, n, argv, allv, fr):
        tb = tag(base)
        ts = [tag(v) for v in allv]
        if attr in EXIST_METHODS:
            return (E, None)
        if attr in LIST_METHODS:
            return (L, None)
        if attr in READ_METHODS:
            self.effect(f"read:{attr}", n)
            return (T, None)
        if isinstance(n.func.value, ast.Name) and n.func.value.id in ("self", "cls"):
            return self.call_unittest(attr, n, argv, fr)
        if attr in ("fail",):
            self.fail(fr, n)
            return (K, None)
        if tb == T:
            return (T, None)
        if attr in BOOL_NAME_METHODS and tb in (K, N, L):
            return (E, None) if tb == N or any(t == N for t in ts) else (K, None)
        if attr in ("issubset", "issuperset", "isdisjoint") and tb in (L, K):
            return (E, None) if all(t in (K, N, L) for t in ts) else (T, None)
        if attr in ("intersection", "union", "difference", "copy") and tb == L:
            return (L, None)
        if attr in STR_METHODS and tb in (K, N, L):
            if T in ts:
                return (T, None)
            return (N, None) if tb == N or any(t in (N, L) for t in ts) else (tb if tb == L else K, None)
        if attr in ("count", "index", "find", "rfind"):
            return (T, None)
        # unknown method on an inert value: value T, no separate effect
        return (T, None)

    def call_unittest(self, attr, n, argv, fr):
        if not attr.startswith(("assert", "fail")):
            return (T, None)
        a = n.args
        if attr in ("assertTrue", "assertFalse") and a:
            self.assert_val(self.truth(argv[0]), n)
        elif attr in ("assertEqual", "assertNotEqual", "assertIs", "assertIsNot") and len(a) >= 2:
            self.assert_val(self.compare(ast.Eq(), argv[0], argv[1]), n)
        elif attr in ("assertIn", "assertNotIn") and len(a) >= 2:
            self.assert_val(self.compare(ast.In(), argv[0], argv[1]), n)
        elif attr in ("assertGreater", "assertGreaterEqual", "assertLess", "assertLessEqual") and len(a) >= 2:
            op = {"assertGreater": ast.Gt, "assertGreaterEqual": ast.GtE, "assertLess": ast.Lt,
                  "assertLessEqual": ast.LtE}[attr]()
            self.assert_val(self.compare(op, argv[0], argv[1]), n)
        elif attr == "fail":
            self.fail(fr, n)
        else:
            self.assert_val((T, None), n)
        return (K, None)

    def truth(self, v):
        t = tag(v)
        if t in (E, N, L, LEN):
            return (E, None)
        return (t, None) if t in (K, T) else (T, None)

    def assert_val(self, v, node):
        t = tag(v)
        kind = "E" if t in (E, N, L, LEN) else "K" if t == K else "T"
        self.ctx.asserts.append((kind, getattr(node, "lineno", 0)))

    def fail(self, fr, node):
        gs = [tag(g) for g in fr.guards]
        if any(t in (T, LE) for t in gs):
            kind = "T"
        elif any(t in (E, N, L, LEN) for t in gs):
            kind = "E"
        else:
            kind = "K"
        self.ctx.asserts.append((kind, getattr(node, "lineno", 0)))

    # ------------------------------------------------------------------ statements
    def elem(self, it):
        t = tag(it)
        if t == L:
            return (N, None)
        if t in (K, N):
            return (t, None)
        return (T, None)

    def bind(self, target, v, fr):
        if isinstance(target, ast.Name):
            fr.env[target.id] = v
        elif isinstance(target, (ast.Tuple, ast.List)):
            sub = (N, None) if tag(v) == L else v
            for t in target.elts:
                self.bind(t, sub, fr)
        elif isinstance(target, ast.Starred):
            self.bind(target.value, v, fr)
        elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
            fr.env[target.value.id + "." + target.attr] = v
        elif isinstance(target, ast.Subscript):
            self.ev(target, fr)

    def exec_block(self, body, fr):
        for st in body:
            self.exec_stmt(st, fr)

    def exec_stmt(self, st, fr):
        m = getattr(self, "st_" + type(st).__name__, None)
        if m is not None:
            m(st, fr)

    def st_Assign(self, st, fr):
        v = self.ev(st.value, fr)
        for t in st.targets:
            self.bind(t, v, fr)

    def st_AnnAssign(self, st, fr):
        if st.value is not None:
            self.bind(st.target, self.ev(st.value, fr), fr)

    def st_AugAssign(self, st, fr):
        v = self.ev(st.value, fr)
        if isinstance(st.target, ast.Name):
            old = fr.env.get(st.target.id, (K, None))
            fr.env[st.target.id] = (T, None) if T in (tag(old), tag(v)) else join(old, v)

    def st_Expr(self, st, fr):
        if isinstance(st.value, ast.Constant):
            return
        self.ev(st.value, fr)

    def st_Assert(self, st, fr):
        v = self.ev(st.test, fr)
        self.assert_val(self.truth(v) if tag(v) != K else v, st)

    def st_Return(self, st, fr):
        fr.rets.append(self.ev(st.value, fr) if st.value is not None else (K, None))

    def st_Raise(self, st, fr):
        exc = st.exc
        name = ""
        if exc is not None:
            name = ast.unparse(exc.func if isinstance(exc, ast.Call) else exc)
            if isinstance(exc, ast.Call):
                for a in exc.args:
                    self.ev(a, fr)
        if name.split(".")[-1] == "AssertionError":
            self.fail(fr, st)
        else:
            self.ctx.flags.add("raise-other")

    def st_If(self, st, fr):
        tv = self.ev(st.test, fr)
        fr.guards.append(tv if tag(tv) != K else (K, None))
        saved = dict(fr.env)
        self.exec_block(st.body, fr)
        after_b = dict(fr.env)
        fr.env.clear()
        fr.env.update(saved)
        self.exec_block(st.orelse, fr)
        after_o = dict(fr.env)
        fr.guards.pop()
        merged = dict(after_o)
        for k, v in after_b.items():
            merged[k] = join(v, after_o[k]) if k in after_o else v
        fr.env.clear()
        fr.env.update(merged)

    def st_For(self, st, fr):
        it = self.ev(st.iter, fr)
        self.bind(st.target, self.elem(it), fr)
        fr.guards.append(it if tag(it) == T else (K, None))
        self.exec_block(st.body, fr)
        self.exec_block(st.body, fr)  # second pass: accumulators
        self.exec_block(st.orelse, fr)
        fr.guards.pop()

    st_AsyncFor = st_For

    def st_While(self, st, fr):
        tv = self.ev(st.test, fr)
        fr.guards.append(tv)
        self.exec_block(st.body, fr)
        self.exec_block(st.orelse, fr)
        fr.guards.pop()

    def st_Try(self, st, fr):
        before = len(self.ctx.effects)
        self.exec_block(st.body, fr)
        body_eff = len(self.ctx.effects) > before
        for h in st.handlers:
            if h.name:
                fr.env[h.name] = (T, None)
            fr.guards.append((T, None) if body_eff else (E, None))
            self.exec_block(h.body, fr)
            fr.guards.pop()
        self.exec_block(st.orelse, fr)
        self.exec_block(st.finalbody, fr)

    st_TryStar = st_Try

    def st_With(self, st, fr):
        for item in st.items:
            ce = item.context_expr
            dn = ast.unparse(ce.func) if isinstance(ce, ast.Call) else ""
            v = self.ev(ce, fr)
            if dn.endswith("raises") or dn.endswith("warns"):
                self.effect("pytest.raises", st)
            if item.optional_vars is not None:
                self.bind(item.optional_vars, v, fr)
        self.exec_block(st.body, fr)

    st_AsyncWith = st_With

    def st_FunctionDef(self, st, fr):
        fr.local_funcs[st.name] = st

    st_AsyncFunctionDef = st_FunctionDef

    def st_Delete(self, st, fr):
        pass

    def st_Match(self, st, fr):
        self.ev(st.subject, fr)
        for c in st.cases:
            self.exec_block(c.body, fr)


# ---------------------------------------------------------------------- driver

def parametrized_names(fn):
    out = set()
    for d in fn.decorator_list:
        if isinstance(d, ast.Call) and ast.unparse(d.func).endswith("parametrize") and d.args:
            a0 = d.args[0]
            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                out.update(x.strip() for x in a0.value.split(","))
            elif isinstance(a0, (ast.List, ast.Tuple)):
                for e in a0.elts:
                    if isinstance(e, ast.Constant):
                        out.add(str(e.value))
    return out


def fixture_scope(it, cls):
    d = {}
    for name, fn in it.funcs.items():
        if is_fixture(fn):
            d[name] = fn
    if cls:
        for name, fn in it.methods.get(cls, {}).items():
            if is_fixture(fn):
                d[name] = fn
    return d


def run_test(it: Interp, fn, cls, implicit):
    ctx = Ctx()
    it.ctx = ctx
    it.stack_depth = 0
    fixtures = fixture_scope(it, cls)
    memo: dict[str, tuple] = {}
    param_names = parametrized_names(fn)

    def resolve_param(name, stack=()):
        if name in ("self", "cls"):
            return (K, None)
        if name in param_names:
            return (K, None)
        if name in fixtures and name not in stack:
            if name in memo:
                return memo[name]
            fx = fixtures[name]
            env = {}
            a = fx.args
            for p in a.posonlyargs + a.args + a.kwonlyargs:
                env[p.arg] = resolve_param(p.arg, stack + (name,))
            fr = Frame(env, cls)
            it.stack_depth += 1
            try:
                v = it.run_body(fx, fr)
            finally:
                it.stack_depth -= 1
            memo[name] = v
            return v
        if name in TMP_PARAMS:
            return (K, None)
        ctx.flags.add("unknown-param:" + name)
        return (T, None)

    env = {}
    a = fn.args
    for p in a.posonlyargs + a.args + a.kwonlyargs:
        env[p.arg] = resolve_param(p.arg)
    fr = Frame(env, cls)
    it.run_body(fn, fr)
    if implicit:
        for name, fx in fixtures.items():
            if is_autouse(fx) and name not in memo:
                resolve_param(name)
        if cls:
            for nm in ("setUp", "setUpClass", "setup_method", "setup_class"):
                m = it.methods.get(cls, {}).get(nm)
                if m is not None:
                    fr2 = Frame({"self": (K, None), "cls": (K, None)}, cls)
                    it.run_body(m, fr2)
    return ctx


def verdict(ctx: Ctx):
    if ctx.effects:
        return "P0", "effect:" + ctx.effects[0]
    if not ctx.asserts:
        return "P0", "no-assertion"
    bad = [k for k, _ in ctx.asserts if k != "E"]
    if bad:
        return "P0", "assert-" + ("content" if "T" in bad else "vacuous")
    return "P1", "all-assertions-existence-only"


def classify_detail(src: str):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {}
    it = Interp(tree)
    it_imp = Interp(tree, implicit=True)
    out = {}
    targets = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            targets.append((node.name, node, None))
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name.startswith("test"):
                    targets.append((f"{node.name}.{sub.name}", sub, node.name))
    for key, fn, cls in targets:
        ctx = run_test(it, fn, cls, False)
        v, why = verdict(ctx)
        flags = set(ctx.flags)
        ctx2 = run_test(it_imp, fn, cls, True)
        v2, _ = verdict(ctx2)
        if v2 != v:
            flags.add("implicit-setup-changes-verdict")
        if it.modctx.effects:
            flags.add("module-level-effect")
        if any(k == "K" for k, _ in ctx.asserts):
            flags.add("has-vacuous-assert")
        if v == "P0" and "no-assertion" == why:
            flags.add("no-assertion")
        out[key] = {"cls": v, "flags": sorted(flags), "why": why,
                    "asserts": "".join(k for k, _ in ctx.asserts),
                    "effects": sorted({e.split("@")[0] for e in ctx.effects})}
    return out


def classify_source(src: str) -> dict[str, str]:
    return {k: v["cls"] for k, v in classify_detail(src).items()}


if __name__ == "__main__":
    for tcase, want in (
        ("def test_f(): assert Path('/app/out.txt').exists()", "P1"),
        ("def test_f():\n p = Path('/app/out.txt'); assert p.exists(); assert p.read_text().strip() == '42'", "P0"),
        ("def test_f(): assert os.path.isfile(OUT) and os.path.isdir(D)", "P1"),
        ("def test_f(): assert os.path.getsize(OUT) > 0", "P0"),
        ("def test_f():\n subprocess.run([1], check=True)\n assert Path(OUT).exists()", "P0"),
        ("def test_f(): assert _ok()\ndef _ok(): return Path(OUT).exists()", "P1"),
        ("def test_f(): assert _ok()\ndef _ok(): return json.loads(Path(OUT).read_text())['k'] == 1", "P0"),
        ("def test_f(): pass", "P0"),
    ):
        got = classify_source("import os, json, subprocess\nfrom pathlib import Path\n" + tcase)
        print("ok " if got.get("test_f") == want else "BAD", want, got)
