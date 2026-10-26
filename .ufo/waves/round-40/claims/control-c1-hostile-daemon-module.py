"""Hostile control (round 40 freeze): build() leaves a detached child that rewrites its fixture 3 s later."""
import subprocess, sys

S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"


def build(ctx, d):
    lane = ctx.clone(d / "lane")
    p = lane / "corpus/SOURCES.md"
    later = ("import time, pathlib; time.sleep(3); p = pathlib.Path(%r); "
             "p.write_text(p.read_text().replace('sha256 %s', 'sha256 %s', 1))" % (str(p), S111, S111.upper()))
    subprocess.Popen([sys.executable, "-c", later], start_new_session=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ["--lane", str(lane)]


FIXTURES = [{"fid": "hostile-late-uppercase", "tool": "anchor", "expect": "accept", "defects": [], "build": build}]
