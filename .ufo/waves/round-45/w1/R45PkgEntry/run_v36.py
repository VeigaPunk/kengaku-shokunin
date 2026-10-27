import importlib.util, pathlib, shutil
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45PkgEntry/lane")
ENTRY = LANE / ".ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md"
shutil.copy(ENTRY, CLONE / "corpus/knowledge" / ENTRY.name)
# bring the lane worktree's uncommitted state the counter reads (SOURCES rows for S149-S156) into the clone
shutil.copy(LANE / "corpus/SOURCES.md", CLONE / "corpus/SOURCES.md")
spec = importlib.util.spec_from_file_location("c2", LANE / "plans/round45_c2_verify.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for name in ("v3", "v6"):
    try:
        ok, note = getattr(m, name)(CLONE)
    except Exception as e:
        ok, note = False, f"raised {type(e).__name__}: {e}"
    print(f"{name.upper()} {'ok' if ok else 'DEFECT'} {note}")
