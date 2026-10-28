#!/usr/bin/env python3
"""Scratch adversarial probe (seat R50C1ExecRepair): witness the REFUSAL direction of every path the
round-50 candidate opens. Each case copies a measured honest fixture and changes only the one thing named;
the honest copy must be ADMITTED and every hostile copy must be REFUSED (and never by a crash)."""
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "adv"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel(target, start):
    return os.path.relpath(str(target), str(start))


def main():
    lane = pathlib.Path(sys.argv[1]).resolve()
    cand = sys.argv[2]
    k50 = load(lane / "plans/round50_c1_verify.py", "k50")
    hb = load(lane / "plans/honest50/build_honest_population.py", "hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "k44")
    fence = load(cand, "cand")

    if OUT.exists():
        shutil.rmtree(OUT)
    work = OUT / "_build"
    work.mkdir(parents=True)
    mods = [
        (lane / "plans/honest50/modules/novel49/n17_replace_ref.py", "n17"),
        (lane / "plans/honest50/modules/novel49/n20_linked_worktree.py", "n20"),
        (lane / "plans/honest50/modules/novel50/n21_separate_gitdir.py", "n21"),
        (lane / "plans/honest50/modules/novel50/n22_alternates_in_d.py", "n22"),
    ]
    built, fails = k50.build_all(hb, k44, mods, work)
    if fails:
        print("BUILD-FAIL", fails)
        return 2
    base = {f["fid"]: pathlib.Path(f["dir"]) for f in built}
    argv = {"n17-replace-ref": ("repo",), "n20-linked-worktree": ("repo",),
            "n21-separate-gitdir": ("wt",), "n22-alternates-in-d": ("lane",)}

    case = {"n": 0}

    def run(name, fid, mutate, path=None):
        case["n"] += 1
        root = OUT / f"c{case['n']:02d}-{name}"
        d = root / "d"
        shutil.copytree(base[fid], d)
        outside = root / "outside"
        outside.mkdir()
        mutate(d, outside)
        lane_tok = argv[fid][0]
        try:
            why = fence.breach(d, ["--lane", lane_tok], "anchor")
            verdict = "ADMIT" if why is None else "BREACH"
        except Exception as e:                                        # a crash is never an admission
            verdict, why = "ERROR", f"{type(e).__name__}: {e}"
        print(f"{name:44s} {verdict:6s} {why}" if why else f"{name:44s} {verdict}")
        return verdict, why

    def noop(d, outside):
        return None

    results = []
    # honest copies: the baseline every hostile case is compared against
    results.append(("HONEST n17 copy", run("honest-n17", "n17-replace-ref", noop)))
    results.append(("HONEST n20 copy", run("honest-n20", "n20-linked-worktree", noop)))
    results.append(("HONEST n21 copy", run("honest-n21", "n21-separate-gitdir", noop)))
    results.append(("HONEST n22 copy", run("honest-n22", "n22-alternates-in-d", noop)))

    # (1) gitfile: every out-of-d / dangling / hardlinked / symlinked shape must stay refused
    def gitfile_out_rel(d, outside):
        (outside / "store").mkdir()
        (outside / "store/HEAD").write_text("ref: refs/heads/master\n")
        (d / "wt/.git").write_text(f"gitdir: {rel(outside / 'store', d / 'wt')}\n")

    def gitfile_out_abs(d, outside):
        (outside / "store").mkdir()
        (d / "wt/.git").write_text(f"gitdir: {outside / 'store'}\n")

    def gitfile_missing(d, outside):
        (d / "wt/.git").write_text("gitdir: ../nope\n")

    def gitfile_is_file_target(d, outside):
        (d / "afile").write_text("x\n")
        (d / "wt/.git").write_text("gitdir: ../afile\n")

    def gitfile_symlink_target(d, outside):
        (outside / "store").mkdir()
        os.symlink(outside / "store", d / "linkstore")
        (d / "wt/.git").write_text("gitdir: ../linkstore\n")

    def gitfile_hardlinked(d, outside):
        os.link(d / "wt/.git", d / "wt/copy-of-git")

    def gitfile_two_lines(d, outside):
        (d / "wt/.git").write_text("gitdir: ../store\ngitdir: ../store\n")

    def gitfile_bom(d, outside):
        (d / "wt/.git").write_bytes(b"\xef\xbb\xbfgitdir: ../store\n")

    results.append(("gitfile out-of-d relative", run("gitfile-out-rel", "n21-separate-gitdir", gitfile_out_rel)))
    results.append(("gitfile out-of-d absolute", run("gitfile-out-abs", "n21-separate-gitdir", gitfile_out_abs)))
    results.append(("gitfile dangling", run("gitfile-missing", "n21-separate-gitdir", gitfile_missing)))
    results.append(("gitfile names a file", run("gitfile-file-target", "n21-separate-gitdir", gitfile_is_file_target)))
    results.append(("gitfile names a symlink", run("gitfile-symlink", "n21-separate-gitdir", gitfile_symlink_target)))
    results.append(("gitfile hardlinked", run("gitfile-hardlink", "n21-separate-gitdir", gitfile_hardlinked)))
    results.append(("gitfile two gitdir lines", run("gitfile-two-lines", "n21-separate-gitdir", gitfile_two_lines)))
    results.append(("gitfile with BOM", run("gitfile-bom", "n21-separate-gitdir", gitfile_bom)))

    # (1c) the pointer grammar git itself enforces (measured, git 2.56.0: one space after `gitdir:`,
    # nothing trimmed, a missing final newline accepted)
    def gitfile_trailing_spaces(d, outside):
        (d / "wt/.git").write_text("gitdir: ../store   \n")

    def gitfile_no_space(d, outside):
        (d / "wt/.git").write_text("gitdir:../store\n")

    def gitfile_two_spaces(d, outside):
        (d / "wt/.git").write_text("gitdir:  ../store\n")

    def gitfile_no_newline(d, outside):
        (d / "wt/.git").write_text("gitdir: ../store")

    results.append(("gitfile target trailing spaces", run("gitfile-trailing-spaces", "n21-separate-gitdir", gitfile_trailing_spaces)))
    results.append(("gitfile prefix without space", run("gitfile-no-space", "n21-separate-gitdir", gitfile_no_space)))
    results.append(("gitfile prefix double space", run("gitfile-two-spaces", "n21-separate-gitdir", gitfile_two_spaces)))
    results.append(("HONEST gitfile no trailing newline", run("honest-gitfile-no-newline", "n21-separate-gitdir", gitfile_no_newline)))

    # (1b) worktree metadata: commondir / gitdir outside d must stay refused
    def commondir_out(d, outside):
        store = outside / "store"
        store.mkdir()
        (d / "repo/.git/worktrees/wt/commondir").write_text(rel(store, d / "repo/.git/worktrees/wt") + "\n")

    def worktree_gitdir_out(d, outside):
        (outside / "x.git").write_text("gitdir: elsewhere\n")
        (d / "repo/.git/worktrees/wt/gitdir").write_text(rel(outside / "x.git", d / "repo/.git/worktrees/wt") + "\n")

    def worktree_gitdir_abs_out(d, outside):
        (outside / "x.git").write_text("gitdir: elsewhere\n")
        (d / "repo/.git/worktrees/wt/gitdir").write_text(str(outside / "x.git") + "\n")

    def worktree_unknown_entry(d, outside):
        (d / "repo/.git/worktrees/wt/locked").write_text("")

    results.append(("commondir out-of-d", run("commondir-out", "n20-linked-worktree", commondir_out)))
    results.append(("worktree gitdir out-of-d rel", run("wt-gitdir-out", "n20-linked-worktree", worktree_gitdir_out)))
    results.append(("worktree gitdir out-of-d abs", run("wt-gitdir-out-abs", "n20-linked-worktree", worktree_gitdir_abs_out)))
    results.append(("worktree unknown entry", run("wt-unknown-entry", "n20-linked-worktree", worktree_unknown_entry)))

    def commondir_trailing_spaces(d, outside):
        (d / "repo/.git/worktrees/wt/commondir").write_text("../..   \n")

    def worktree_gitdir_trailing_spaces(d, outside):
        (d / "repo/.git/worktrees/wt/gitdir").write_text("../../../../wt/.git   \n")

    results.append(("commondir trailing spaces", run("commondir-trailing-spaces", "n20-linked-worktree", commondir_trailing_spaces)))
    results.append(("worktree gitdir trailing spaces", run("wt-gitdir-trailing-spaces", "n20-linked-worktree", worktree_gitdir_trailing_spaces)))

    # (2) alternates: out-of-d, absolute, dangling, symlink, comment, empty must stay refused
    def alt_rel_out(d, outside):
        (outside / "objects").mkdir()
        base = d / "lane/.git/objects"
        (base / "info/alternates").write_text(rel(outside / "objects", base) + "\n")

    def alt_abs_out(d, outside):
        (outside / "objects").mkdir()
        (d / "lane/.git/objects/info/alternates").write_text(str(outside / "objects") + "\n")

    def alt_dangling(d, outside):
        (d / "lane/.git/objects/info/alternates").write_text("../../../nope/.git/objects\n")

    def alt_symlink(d, outside):
        (outside / "objects").mkdir()
        os.symlink(outside / "objects", d / "main/linked-objects")
        base = d / "lane/.git/objects"
        (base / "info/alternates").write_text(rel(d / "main/linked-objects", base) + "\n")

    def alt_comment(d, outside):
        (d / "lane/.git/objects/info/alternates").write_text("# borrowed\n../../../main/.git/objects\n")

    def alt_empty(d, outside):
        (d / "lane/.git/objects/info/alternates").write_text("")

    def alt_hardlinked(d, outside):
        os.link(d / "lane/.git/objects/info/alternates", d / "lane/hard")

    def alt_two_lines_one_out(d, outside):
        (outside / "objects").mkdir()
        base = d / "lane/.git/objects"
        (base / "info/alternates").write_text("../../../main/.git/objects\n" + rel(outside / "objects", base) + "\n")

    results.append(("alternates out-of-d relative", run("alt-rel-out", "n22-alternates-in-d", alt_rel_out)))
    results.append(("alternates out-of-d absolute", run("alt-abs-out", "n22-alternates-in-d", alt_abs_out)))
    results.append(("alternates dangling", run("alt-dangling", "n22-alternates-in-d", alt_dangling)))
    results.append(("alternates names a symlink", run("alt-symlink", "n22-alternates-in-d", alt_symlink)))
    results.append(("alternates comment line", run("alt-comment", "n22-alternates-in-d", alt_comment)))
    results.append(("alternates empty", run("alt-empty", "n22-alternates-in-d", alt_empty)))
    results.append(("alternates hardlinked", run("alt-hardlink", "n22-alternates-in-d", alt_hardlinked)))
    results.append(("alternates 2 lines, one out", run("alt-two-lines", "n22-alternates-in-d", alt_two_lines_one_out)))

    # (2b) chained alternates: an entry inside d whose own alternates borrow from outside d is an escape.
    # `complete` makes the hop a FULL plain init store (a copy of `main/.git`) so the only possible refusal
    # is the chain, not a missing HEAD.
    def chain(store_rel, complete):
        def mutate(dd, outside):
            base = dd / "lane/.git/objects"
            store = dd / store_rel
            if complete:
                store.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(dd / "main/.git", store)
            mid = store / "objects"
            (mid / "info").mkdir(parents=True, exist_ok=True)
            (base / "info/alternates").write_text(rel(mid, base) + "\n")
            (mid / "info/alternates").write_text(rel(outside / "c/.git/objects", mid) + "\n")
            (outside / "c/.git/objects").mkdir(parents=True)
        return mutate

    def alt_cycle(d, outside):
        base = d / "lane/.git/objects"
        other = d / "main/.git/objects"
        (base / "info/alternates").write_text(rel(other, base) + "\n")
        (other / "info/alternates").write_text(rel(base, other) + "\n")

    def alt_chain_inside(d, outside):
        base = d / "lane/.git/objects"
        mid = d / "main/.git/objects"
        third = d / "pool/objects"
        (third / "info").mkdir(parents=True)
        (base / "info/alternates").write_text(rel(mid, base) + "\n")
        (mid / "info/alternates").write_text(rel(third, mid) + "\n")

    def alt_trailing_space(d, outside):
        (d / "lane/.git/objects/info/alternates").write_text("../../../main/.git/objects   \n")

    results.append(("alternates chain via repo", run("alt-chain-repo", "n22-alternates-in-d", chain("a/.git", True))))
    results.append(("alternates chain via bare", run("alt-chain-bare", "n22-alternates-in-d", chain("b.git", False))))
    results.append(("alternates chain via plain dir", run("alt-chain-plain", "n22-alternates-in-d", chain("shared", False))))
    results.append(("alternates entry trailing space", run("alt-trailing-space", "n22-alternates-in-d", alt_trailing_space)))
    results.append(("HONEST alternates cycle in-d", run("honest-alt-cycle", "n22-alternates-in-d", alt_cycle)))
    results.append(("HONEST alternates 2-hop in-d", run("honest-alt-chain-inside", "n22-alternates-in-d", alt_chain_inside)))

    # (2c) the depth cap must REFUSE at the cap, and an honest in-d chain of the same length must still admit
    def alt_chain_depth(n, outside_at_end):
        def mutate(dd, outside):
            base = dd / "lane/.git/objects"
            hops = [dd / f"h{i}/objects" for i in range(1, n + 1)]
            for h in hops:
                (h / "info").mkdir(parents=True, exist_ok=True)
            (base / "info/alternates").write_text(rel(hops[0], base) + "\n")
            for prev, nxt in zip(hops, hops[1:]):
                (prev / "info/alternates").write_text(rel(nxt, prev) + "\n")
            if outside_at_end:
                (outside / "store/.git/objects").mkdir(parents=True)
                (hops[-1] / "info/alternates").write_text(rel(outside / "store/.git/objects", hops[-1]) + "\n")
        return mutate

    results.append(("HONEST alternates 4-hop in-d (at cap)", run("honest-alt-chain-4", "n22-alternates-in-d", alt_chain_depth(4, False))))
    results.append(("alternates 5-hop in-d (over cap)", run("alt-chain-cap5", "n22-alternates-in-d", alt_chain_depth(5, False))))
    results.append(("alternates 4 in-d hops then outside", run("alt-chain-cap-escape", "n22-alternates-in-d", alt_chain_depth(4, True))))

    # (4) refs: any other refs/* name stays refused; refs/replace leaves must be 40-hex
    def ref_replace_nonhex(d, outside):
        shutil.rmtree(d / "repo/.git/refs/replace")
        (d / "repo/.git/refs/replace").mkdir()
        (d / "repo/.git/refs/replace/deadbeef").write_text("0" * 40 + "\n")

    def ref_notes(d, outside):
        (d / "repo/.git/refs/notes").mkdir()
        (d / "repo/.git/refs/notes/commits").write_text("0" * 40 + "\n")

    def ref_replace_nested(d, outside):
        (d / "repo/.git/refs/replace/ab").mkdir()
        (d / "repo/.git/refs/replace/ab/cd").write_text("0" * 40 + "\n")

    def ref_replace_badbody(d, outside):
        name = next((d / "repo/.git/refs/replace").iterdir()).name
        (d / "repo/.git/refs/replace" / name).write_text("not-a-sha\n")

    results.append(("refs/replace non-40hex name", run("ref-replace-nonhex", "n17-replace-ref", ref_replace_nonhex)))
    results.append(("refs/notes namespace", run("ref-notes", "n17-replace-ref", ref_notes)))
    results.append(("refs/replace subdirectory", run("ref-replace-nested", "n17-replace-ref", ref_replace_nested)))
    results.append(("refs/replace body not hex", run("ref-replace-badbody", "n17-replace-ref", ref_replace_badbody)))

    # (5) config: [include] and any unlisted extension stay refused; extensions need version 1
    def cfg(d, text):
        return lambda dd, outside: (dd / "store/config").write_text(text)

    plain = (base["n21-separate-gitdir"] / "store/config").read_text()
    results.append(("[include] section", run("cfg-include", "n21-separate-gitdir",
                                            cfg(None, plain + "[include]\n\tpath = ../evil\n"))))
    results.append(("extensions unlisted key", run("cfg-ext-objectformat", "n21-separate-gitdir",
                                                   cfg(None, "[core]\n\trepositoryformatversion = 1\n"
                                                             "[extensions]\n\tobjectFormat = sha256\n"))))
    results.append(("extensions without version 1", run("cfg-ext-v0", "n21-separate-gitdir",
                                                        cfg(None, "[core]\n\trepositoryformatversion = 0\n"
                                                                  "[extensions]\n\trelativeWorktrees = true\n"))))
    results.append(("repositoryformatversion 2", run("cfg-v2", "n21-separate-gitdir",
                                                     cfg(None, "[core]\n\trepositoryformatversion = 2\n"))))
    results.append(("user section", run("cfg-user", "n21-separate-gitdir",
                                        cfg(None, plain + "[user]\n\tname = x\n"))))

    print("\nSUMMARY")
    bad = []
    for label, (verdict, why) in results:
        want = "ADMIT" if label.startswith("HONEST") else "BREACH"
        if verdict != want:
            bad.append(label)
    print(f"cases={len(results)} mismatched={len(bad)}")
    for label in bad:
        print(f"MISMATCH {label}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
