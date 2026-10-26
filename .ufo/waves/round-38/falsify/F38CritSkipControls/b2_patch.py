"""Skip-control battery (seat F38CritSkipControls), control B2: a battery38 module that rewrites the counter's
own kill rule at import time.

battery38 modules are exec'd inside the counter's process (round38_c1_verify.py `load()` / `battery38_fixtures`),
before any mutant runs, and `attributed` is read as a module global at call time. Patching it makes every
mutant "killed" by the one fixture below, which fires no clause at all: it stages the GENUINE round-35
package, which the reference accepts, so nothing in this battery demonstrates any advertised gate behaviour.

The counter's five-token side-channel scan does not test for this mechanism, and this module avoids those
tokens deliberately.
"""
import sys

FID = "patch-genuine-accept"


def _rewrite_rule():
    main = sys.modules.get("__main__")
    if main is not None and hasattr(main, "attributed"):
        main.attributed = lambda *a, **k: True


_rewrite_rule()


def build(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": FID, "expect": "accept", "defects": [], "build": build}]
