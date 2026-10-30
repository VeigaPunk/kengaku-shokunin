#!/usr/bin/env python3
"""C1PriceScoutC: fetch public primaries, archive them (SOURCE-URL header + verbatim bytes),
price the four R53-C1 confirmed tasks, emit prior-art-part.json, and validate the result
against the frozen counter's own leg_prior_art()."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1PriceScoutC")
LANE = SCRATCH / "lane"
SEAT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutC")
FETCHED = SEAT / "fetched"
RAW = SCRATCH / "raw"
RUN_DIR = "corpus/evidence/round53"

TASKS = {
    "fix-code-vulnerability": [
        "test_report_file_exists_example", "test_vul_file", "test_cwe_id",
        "test_hkey_basic_cases", "test_hkey_error_cases", "test_hkey_real_world_examples"],
    "modernize-scientific-stack": ["test_modernized_code_runs", "test_dependency_file_exists"],
    "pytorch-model-cli": [
        "test_weights_file_exists", "test_cli_tool_exists", "test_prediction_file_exists",
        "test_prediction_file_content", "test_cli_tool_executable", "test_cli_tool_output"],
    "torch-tensor-parallelism": ["test_parallel_linear_exists", "test_column_parallel_linear",
                                  "test_row_parallel_linear"],
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fetch(url: str, dest: Path) -> bytes:
    """Fetch a public URL. API.github.com via gh api (token never printed); everything else via curl."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if url.startswith("https://api.github.com/"):
        r = subprocess.run(["gh", "api", url], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"gh api failed for {url}: {r.stderr.decode()[:200]}")
        data = r.stdout
    else:
        r = subprocess.run(["curl", "-sSL", "--max-time", "90", "-H", "Accept: text/html,*/*", url],
                           capture_output=True)
        if r.returncode != 0 or not r.stdout:
            raise SystemExit(f"curl failed for {url}: rc={r.returncode}")
        data = r.stdout
    dest.write_bytes(data)
    return data


def archive(url: str, name: str) -> Path:
    """Write <seat>/fetched/<name> = 'SOURCE-URL: <url>' + the fetched bytes verbatim."""
    raw = RAW / ("src_" + name)
    data = fetch(url, raw)
    out = FETCHED / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(("SOURCE-URL: " + url + "\n").encode("utf-8") + data)
    return out


def main() -> int:
    # ---------- 1. the row archives ----------
    plan = [
        # (url, archive file name)
        ("https://arxiv.org/abs/2507.02825", "arxiv-2507.02825-abs.html"),
        ("https://arxiv.org/abs/2503.15223", "arxiv-2503.15223-abs.html"),
        ("https://arxiv.org/abs/2511.21654", "arxiv-2511.21654-abs.html"),
        ("https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/242", "ghapi-issues-242.json"),
        ("https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53", "ghapi-pulls-53.json"),
    ]
    sweeps = [
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22fix-code-vulnerability%22+%22only+checked+to+exist%22", "sweep-fcv-tb21-onlychecked.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22fix-code-vulnerability%22+existence", "sweep-fcv-tb2-existence.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22fix-code-vulnerability%22+%22only+checked+to+exist%22", "sweep-fcv-tb1-onlychecked.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22test_report_file_exists_example%22", "sweep-fcv-tb21-testname.json"),
        ("https://api.github.com/search/issues?q=%22test_vul_file%22", "sweep-fcv-global-testname.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22pytorch-model-cli%22+%22only+checked+to+exist%22", "sweep-pmc-tb21-onlychecked.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22pytorch-model-cli%22+existence", "sweep-pmc-tb2-existence.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22pytorch-model-cli%22+%22only+checked+to+exist%22", "sweep-pmc-tb1-onlychecked.json"),
        ("https://api.github.com/search/issues?q=%22test_weights_file_exists%22", "sweep-pmc-global-testname.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22torch-tensor-parallelism%22+%22only+checked+to+exist%22", "sweep-ttp-tb21-onlychecked.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22torch-tensor-parallelism%22+existence", "sweep-ttp-tb2-existence.json"),
        ("https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22torch-tensor-parallelism%22+%22only+checked+to+exist%22", "sweep-ttp-tb1-onlychecked.json"),
        ("https://api.github.com/search/issues?q=%22test_parallel_linear_exists%22", "sweep-ttp-global-testname.json"),
    ]
    for url, name in plan + sweeps:
        p = archive(url, name)
        print("archived", name, p.stat().st_size, "bytes  sha256", sha256_file(p)[:16])

    # ---------- 2. quotes, extracted verbatim from the archives ----------
    def arctext(name: str) -> str:
        return (FETCHED / name).read_text(encoding="utf-8", errors="replace")

    def norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    def extract(text: str, pattern: str, group: int = 0) -> str:
        m = re.search(pattern, norm(text), re.S)
        if not m:
            raise SystemExit("quote pattern not found: " + pattern)
        return norm(m.group(group))

    quotes = {
        "fix-code-vulnerability": extract(arctext("ghapi-pulls-53.json"),
            r"Tests were updated when they over-specified or let any solution pass\."),
        "pytorch-model-cli": extract(arctext("arxiv-2503.15223-abs.html"),
            r"These benchmarks leverage testing to validate generated patches\. However, because testing is rarely exhaustive, a patch may pass the tests"),
        "torch-tensor-parallelism": extract(arctext("arxiv-2511.21654-abs.html"),
            r"create an environment in which agents can easily reward hack, such as by hardcoding test cases or editing the testing files"),
        "modernize-scientific-stack": extract(arctext("ghapi-issues-242.json"),
            r"Lines 46.50 \(`test_dependency_file_exists`\) check that `/app/requirements.txt` or `/app/pyproject.toml` exists\. The file is never opened\."),
    }

    # ---------- 3. rows ----------
    def row(task, verdict, url, arch, quote, sweep_files):
        r = {"task": task, "verdict": verdict, "url": url,
             "fetched": f"{RUN_DIR}/fetched/{arch}",
             "fetched_sha256": sha256_file(FETCHED / arch),
             "quote": quote}
        if sweep_files:
            r["sweep"] = [{"file": f"{RUN_DIR}/fetched/{f}", "file_sha256": sha256_file(FETCHED / f)}
                          for f in sweep_files]
        return r

    rows = [
        row("fix-code-vulnerability", "phenomenon-new",
            "https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53",
            "ghapi-pulls-53.json", quotes["fix-code-vulnerability"],
            ["sweep-fcv-tb21-onlychecked.json", "sweep-fcv-tb2-existence.json",
             "sweep-fcv-tb1-onlychecked.json", "sweep-fcv-tb21-testname.json",
             "sweep-fcv-global-testname.json"]),
        row("modernize-scientific-stack", "phenomenon-known",
            "https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/242",
            "ghapi-issues-242.json", quotes["modernize-scientific-stack"], []),
        row("pytorch-model-cli", "phenomenon-new", "https://arxiv.org/abs/2503.15223",
            "arxiv-2503.15223-abs.html", quotes["pytorch-model-cli"],
            ["sweep-pmc-tb21-onlychecked.json", "sweep-pmc-tb2-existence.json",
             "sweep-pmc-tb1-onlychecked.json", "sweep-pmc-global-testname.json"]),
        row("torch-tensor-parallelism", "phenomenon-new", "https://arxiv.org/abs/2511.21654",
            "arxiv-2511.21654-abs.html", quotes["torch-tensor-parallelism"],
            ["sweep-ttp-tb21-onlychecked.json", "sweep-ttp-tb2-existence.json",
             "sweep-ttp-tb1-onlychecked.json", "sweep-ttp-global-testname.json"]),
    ]
    (SEAT / "prior-art-part.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")

    # SHA256SUMS for the fetched/ dir
    lines = []
    for f in sorted(FETCHED.iterdir()):
        if f.name == "SHA256SUMS":
            continue
        lines.append(f"{sha256_file(f)}  {f.name}")
    (FETCHED / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------- 4. validate with the frozen counter's own leg_prior_art ----------
    spec = importlib.util.spec_from_file_location("r53c1", LANE / "plans/round53_c1_triage.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fake = SCRATCH / "fakelane"
    (fake / RUN_DIR / "fetched").mkdir(parents=True, exist_ok=True)
    for f in FETCHED.iterdir():
        if f.name != "SHA256SUMS":
            (fake / RUN_DIR / "fetched" / f.name).write_bytes(f.read_bytes())
    (fake / RUN_DIR / "prior-art.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    idx = json.loads((LANE / "corpus/evidence/round53/tests-index.json").read_text())["tests"]
    idx = [{"task": t["task"], "name": t["name"]} for t in idx]
    ok, L = m.leg_prior_art(fake, m.CFG, list(TASKS), idx)
    print("\n--- counter leg_prior_art on my part ---")
    for line in L:
        print(line)
    print("leg_prior_art ok =", ok)

    # ---------- 5. local checks: quotes, naming, sweep bodies ----------
    print("\n--- per-row local checks ---")
    allok = True
    for r in rows:
        task = r["task"]
        tl = TASKS[task]
        atext = (fake / RUN_DIR / "fetched" / Path(r["fetched"]).name).read_text(errors="replace")
        q = norm(r["quote"])
        inq = 8 <= len(q.split()) <= 25
        intext = q in norm(atext)
        hdr = m.HDR.match(atext)
        hdr_ok = bool(hdr) and m.url_key(hdr.group(1)) == m.url_key(r["url"])
        if r["verdict"] == "phenomenon-known":
            names = m.names_task(q, task, tl)
            body_names = None
        else:
            names = None
            body_names = m.names_task(atext, task, tl)
        sweep_names = []
        for s in r.get("sweep", []):
            st = (fake / RUN_DIR / "fetched" / Path(s["file"]).name).read_text(errors="replace")
            sweep_names.append((Path(s["file"]).name, m.names_task(st, task, tl),
                                bool(m.HDR.match(st))))
        good = inq and intext and hdr_ok and (names is not False) and (body_names is not True) \
            and all(not n for _, n, _ in sweep_names) and all(h for _, _, h in sweep_names)
        allok = allok and good
        print(f"{task}: words={len(q.split())} in_archive={intext} header_ok={hdr_ok} "
              f"known_quote_names_task={names} new_body_names_task={body_names} good={good}")
        for nm, n, h in sweep_names:
            print(f"    sweep {nm}: names_task={n} header={h}")
    print("\nALL LOCAL CHECKS PASS:", allok)
    print("leg_prior_art ok:", ok)
    return 0 if (ok and allok) else 1


if __name__ == "__main__":
    sys.exit(main())
