"""R41PlanNext: re-run the round-40 wave-2 near-variants (anchor X1-X16, ledger/order XL1-XO7) through the
UNEDITED round-40 counter at the round-41 tip. Only the module-global MUTANTS is overridden."""
import importlib.util, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
def load(name, f):
    sp = importlib.util.spec_from_file_location(name, str(HERE / f)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
tab = load("xmut_table", "xmut_table.py")
led = load("xmut_driver", "xmut_driver.py")
c1 = led.c1
c1.MUTANTS = list(tab.MUTANTS) + list(led.XMUT)
if __name__ == "__main__":
    sys.exit(c1.main())
