import pathlib, re, hashlib, os
S = pathlib.Path(os.environ["S"])
lane = S / "lane"
t = (lane / "plans/round44_c1_verify.py").read_text()
rc_sha = hashlib.sha256((lane / "plans/round_close.py").read_bytes()).hexdigest()
t = t.replace('    "order": "plans/order_check.py",\n}', '    "order": "plans/order_check.py",\n    "round_close": "plans/round_close.py",\n}', 1)
t = t.replace('PINS = {\n', f'PINS = {{\n    "plans/round_close.py": "{rc_sha}",\n', 1)
# F3 branch for round_close
t = t.replace('''    if tool == "order":
        if len(argv) != 6''', '''    if tool == "round_close":
        opts = {"--lane": True, "--round": True, "--census": True, "--work": True, "--selftest": False}
        seen, k = [], 0
        while k < len(argv):
            tok = argv[k]
            if tok not in opts or tok in seen:
                return f"round_close argv token {tok!r} is not an exact, single option"
            seen.append(tok)
            k += 2 if opts[tok] else 1
        if k != len(argv) or "--lane" not in seen:
            return "round_close argv malformed or no --lane"
        return None
    if tool == "order":
        if len(argv) != 6''', 1)
M = []
def m(mid, cls, direction, adv, old, new, kind="direct"):
    M.append((mid, "round_close", cls, direction, kind, adv, "R44PlanNext scratch", old, new))
D = "plans/round_close.py"
m("L98a", "-", "0>2", f"{D}:2 'exits 0 only when every leg passed' (git_ok == 0 flipped)", "capture_output=True).returncode == 0", "capture_output=True).returncode != 0")
m("L98b", "-", "0>2", f"{D}:57 receipt committed in HEAD counts (git_ok == 0 -> == 1)", "capture_output=True).returncode == 0", "capture_output=True).returncode == 1")
m("L132", "-", "0>2", f"{D}:57 'neither a file in the lane nor committed in HEAD' dropped (or -> and)", "if (lane / rel).is_file() or git_ok(", "if (lane / rel).is_file() and git_ok(")
m("L122a", "-", "0>2", f"{D}:33 '(b) a backticked corpus/evidence/roundN path for this round' (== -> !=)", "if int(m.group(2)) == round_no:", "if int(m.group(2)) != round_no:")
m("L122b", "-", "0>2", f"{D}:33 (b) (if -> False)", "if int(m.group(2)) == round_no:", "if False:                        ")
m("L145a", "-", "2>0", f"{D}:73 census found 'else the lane's parents' (and -> or)", "if env_root and (Path(env_root) / CENSUS_REL).is_file():", "if env_root or  (Path(env_root) / CENSUS_REL).is_file():")
m("L149", "-", "0>2", f"{D}:73 census 'the lane's parents' (if -> False)", "if cand.is_file():", "if False:           ")
m("L175", "-", "2>1", f"{D}:25 'no claims file' is 2 (if -> False)", "if not claims_path.is_file():", "if False:                    ")
m("L178", "-", "2>1", f"{D}:25 'no order tool' is 2 (if -> False)", "if not order_path.is_file():", "if False:                   ")
m("L319", "-", "2>1", f"{D}:25 --selftest census missing is 2 (if -> False)", "if args.selftest:\n        if census is None:", "if args.selftest:\n        if False:          ")
m("L321", "-", "2>0", f"{D}:25 --selftest census missing is 2 (return 2 -> 0)", "            return 2\n        if not (lane / ORDER_TOOL).is_file():", "            return 0\n        if not (lane / ORDER_TOOL).is_file():")
m("L322", "-", "2>1", f"{D}:25 --selftest no order tool is 2 (if -> False)", "if not (lane / ORDER_TOOL).is_file():", "if False:                            ")
m("L324", "-", "2>0", f"{D}:25 --selftest no order tool is 2 (return 2 -> 0)", "            return 2\n        return selftest(", "            return 0\n        return selftest(")
m("L326", "-", "0>2", f"{D}:25 gate run with --round (is -> is not)", "if args.round is None:", "if args.round is not None:")
m("L328a", "-", "0>2", f"{D}:25 census found -> gate runs (is -> is not)", 'unless --selftest")\n    if census is None:', 'unless --selftest")\n    if census is not None:')
m("L328b", "-", "2>1", f"{D}:25 --census missing is 2 (if -> False)", 'unless --selftest")\n    if census is None:', 'unless --selftest")\n    if False:          ')
m("L331", "-", "2>0", f"{D}:25 --census missing is 2 (return 2 -> 0)", '        print("ROUND-CLOSE RESULT ERROR")\n        return 2\n    return gate(', '        print("ROUND-CLOSE RESULT ERROR")\n        return 0\n    return gate(')
# controls
m("C145b", "-", "0>2", "env-gated: SHOKUNIN_ROOT (if env_root -> False)", "if env_root and (Path(env_root) / CENSUS_REL).is_file():", "if False    and (Path(env_root) / CENSUS_REL).is_file():")
m("C243a", "-", "0>1", "counter-gated: reused --work (if -> False)", "if root.is_symlink() or root.is_file():", "if False                              :")
m("C243b", "-", "0>1", "counter-gated: reused --work (or -> and)", "if root.is_symlink() or root.is_file():", "if root.is_symlink() and root.is_file():")
m("C243c", "-", "0>1", "counter-gated: reused --work (elif -> False)", "elif root.is_dir():", "elif False:       ")
s, e = t.index("MUTANTS = ["), t.index("\n]\n", t.index("MUTANTS = [")) + 3
t = t[:s] + "MUTANTS = " + repr(M).replace("), (", "),\n    (") + "\n" + t[e:]
(S / "ctr/c1_rc.py").write_text(t)
print("ok", len(M), rc_sha[:8])
