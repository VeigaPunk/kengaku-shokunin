# F37ProbeOnTip — the gate exactly as V2 runs it, then three adversarial probe environments

Round 37 (hyaku run 8) wave 2 falsify. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Target tip: `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`. Seat wrote only under
`.ufo/waves/round-37/falsify/F37ProbeOnTip/` and `/fast/scratch/hyaku/kengaku-r37/F37ProbeOnTip/` (deleted).
No lane file, no lane git index, no jj state was touched.

## 1. Setup and provenance

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/fx/lane
$ git -C $S/fx/lane checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ git -C $S/fx/lane rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r37/F37ProbeOnTip/fx/lane
$ git -C $S/fx/lane rev-parse HEAD
357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ git -C $S/fx/lane ls-files --others --exclude-standard | wc -l
0
$ sha256sum plans/pkg_gate.py plans/git_webserver_probe.py plans/pkg-spec-r37.json corpus/evidence/round37/git-webserver-probe.txt
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py
63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf  plans/git_webserver_probe.py
4c61d103cff74021fec4dcedb27b6f5d85a3b5d6b11c1b4eda7df0ebe909c9b6  plans/pkg-spec-r37.json
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  corpus/evidence/round37/git-webserver-probe.txt
```

Environment: `kernel=7.2.11-arch1-1`, `python3=/usr/bin/python3 Python 3.14.8`, `uv 0.13.0`,
`bubblewrap 0.13.1`, `unshare util-linux 2.42.4`, `uid=1000`.
`python3 -c 'import Bio'` → `ModuleNotFoundError: No module named 'Bio'` — so the gate's P10 took the
`uv` branch on every run below (proved, not inferred, in §2).

Tip provenance, for the record (`git log -1 --format='%h %s'`):

| commit | subject |
|---|---|
| `5c7d5d7` | round-37: SCORECARD and LOG round-37 sections … measure script |
| `357dece` | round-37: post-hoc C1 kill-attribution audit … |
| `dc90676` | round-37: close lesson (wave 2 dispatched …) (master) |

`git merge-base --is-ancestor` → `5c7d5d7 → 357dece = 0`, `5c7d5d7 → master = 0`, `357dece → master = 0`
(all ancestors). `git diff --stat 5c7d5d7 357dece -- plans/pkg_gate.py plans/git_webserver_probe.py
plans/pkg-spec-r37.json plans/round37_c2_verify.py corpus/evidence/round37/git-webserver-probe.txt
corpus/evidence/round37/tb2-git-webserver/` printed **nothing**, and the same diff
`357dece..dc90676` on the same paths printed nothing: the whole probe package is byte-identical across
the receipt's own recorded TIP (`5c7d5d7`, `integrate/measure-final.txt:1`), the wave-2 target
(`357dece`) and master. See finding F3.

## 2. Primary — the gate exactly as V2 runs it

Spec built the way `round37_c2_verify.py:87-92` builds it (template copy + receipt digest filled):

```
$ python3 - <<'PY'
spec = json.loads((root/"plans/pkg-spec-r37.json").read_text())
spec["receipt_sha256"] = sha256(root/spec["receipt"])
PY
receipt_sha256=835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  template_receipt_sha256= None

$ cd $D && python3 plans/pkg_gate.py package --root . --spec $S/pkg-spec-r37-effective.json \
    --rerun --require-clean-tree
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=32 distinct_quotes=32 distinct_lines=32 out_of_word_range=0
P4 ok checked=32 bad=0 first=0
P5 ok manifest_entries=6 bad=0 first=0
P6 ok rows=3 bad=0 first=0
P7 ok source_lines=4 bad=0 first=0
P8 ok index_rows=44 knowledge_files=44 bad=0 first=0
P9 ok untracked=0 first=0
P10 ok probe_rerun=byte-equal bytes=8443
defects=0
gate_exit=0          real 0m52.828s   stderr: (empty)
```

The effective spec lives outside the clone root (`$S/…`), so P9 is measured on the tree, not on the
instrument (`untracked=0` before and after: `untracked_before=0`, `untracked_after=0`).

**The uv branch was taken** — observed with a logged shim on `PATH` (the shim `exec`s the real
`/home/vgpnk/.local/bin/uv`), on a second clean-tree run:

```
$ UV_SHIM_LOG=$S/out/uv-calls.log PATH=$S/shim:$PATH python3 plans/pkg_gate.py package --root . \
    --spec $S/pkg-spec-r37-effective.json --rerun --require-clean-tree
P10 ok probe_rerun=byte-equal bytes=8443 / defects=0 / gate_shim_exit=0
$ cat $S/out/uv-calls.log
2026-10-26T05:20:19Z run --no-project --with biopython==1.85 python3 plans/git_webserver_probe.py --lane .
```

That is `pkg_gate.py:275-276`'s `except ImportError:` arm verbatim. Output of the two gate runs is
byte-identical (`gate-v2.txt` and `gate-v2-shim.txt` share sha256 `4934fd84…`).

### 2.1 The uv P10 path alone, byte-compared to the receipt

```
$ uv run --no-project --with biopython==1.85 python3 plans/git_webserver_probe.py --lane .
exit 0   real 0m52.761s   stderr: (empty)
$ sha256sum $S/out/probe-uv.txt corpus/evidence/round37/git-webserver-probe.txt
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  $S/out/probe-uv.txt
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  corpus/evidence/round37/git-webserver-probe.txt
$ cmp … && echo BYTE-EQUAL
BYTE-EQUAL
$ uv run --no-project --with biopython==1.85 python3 -c "import Bio,sys;print('bio',Bio.__version__,'py',sys.version.split()[0])"
bio 1.85 py 3.13.16
```

Last line of the run: `cases=22 observed_pass=9 observed_fail=13 mismatches=0`.

## 3. Adversarial A — a listener already on 127.0.0.1:8080 outside the sandbox, probe in a scratch-only netns

Fixture: a scratch-netns run (`unshare -rn`, `ip link set lo up`), a leak HTTP server in **two** places —
one in the host netns (this shell, before the unshare) and one *inside* the scratch netns but outside the
bwrap sandbox the probe builds. Bodies: `HOST-NETNS-LEAK hello world` and `SCRATCH-NS-LEAK hello world`.

```
$ ss -ltn          (host netns, while the probe ran)
LISTEN 0 5  127.0.0.1:8080  0.0.0.0:*
$ ss -ltn          (scratch netns, while the probe ran)
LISTEN 0 5  127.0.0.1:8080  0.0.0.0:*
$ python3 get.py 127.0.0.1 8080      (host)      → HTTP/1.0 200 OK … Content-Length: 27
$ python3 get.py 127.0.0.1 8080      (scratch ns) → HTTP/1.0 200 OK … Content-Length: 27
$ bash $S/out/advA.sh $S $D
advA_exit=0   unshare_exit=0   advA.err: (empty)
$ cmp $S/out/advA.txt corpus/evidence/round37/git-webserver-probe.txt && echo ADV_A_BYTE_EQUAL
ADV_A_BYTE_EQUAL     sha256=835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8
CASE no-server tools=curl predicted=fail observed=fail match=yes …
CASE wrong-port-8081 tools=curl predicted=fail observed=fail match=yes …
cases=22 observed_pass=9 observed_fail=13 mismatches=0
```

Both listeners were up and answering when sampled (200, 27-byte bodies) and stayed up until after the
probe exited; the probe's sandbox still saw an empty `:8080` (`no-server` observed `fail`). Result:
**byte-equal, exit 0**.

### 3.1 Positive control — this byte-equality is a live discriminator, not a tautology

Two controls, both in scratch:

```
# (i) isolation plumbing, same bwrap flag set as sandbox_argv(), same listener
$ unshare -rn -- bash -c 'ip link set lo up; leak.py "hello world" & …'
share-net_status=200
unshare-net_status=000
```

```
# (ii) the probe with one token changed in a scratch copy: --unshare-net → --share-net
$ sed 's/"--unshare-net", "--unshare-pid"/"--share-net", "--unshare-pid"/' probe.py > ctl/probe_sharenet.py
$ unshare -rn -- bash -c 'ip link set lo up; leak.py "hello world" & cd $D && python3 ctl/probe_sharenet.py --lane .'
CASE no-server tools=curl predicted=fail observed=pass match=NO -- verify.sh:57-59 …
SETUP case static-file-no-git did not yield one verdict (rc=3)   ctl2_exit=2
CTL2_DIFFERS
```

So a leaking sandbox flips `no-server` to `observed=pass match=NO` and then refuses at case 2 (the leak
holds the port); the receipt comparison fires. The real probe's byte-equality above therefore carries
information.

## 4. Adversarial B — HOME unset

```
$ env -u HOME python3 -c 'import os;print("HOME_in_env=","HOME" in os.environ)'
HOME_in_env= False
$ env -u HOME python3 plans/git_webserver_probe.py --lane .
advB_exit=0   advB.err: (empty)
$ cmp $S/out/advB.txt corpus/evidence/round37/git-webserver-probe.txt && echo ADV_B_BYTE_EQUAL
ADV_B_BYTE_EQUAL    sha256=835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8
```

`TMPDIR=$S` was exported for the run. Supplementary, because P10 depends on uv: `env -u HOME -u
XDG_CACHE_HOME uv run --no-project --with biopython==1.85 python3 -c 'import Bio'` → `uv_bio 1.85`,
`uv_home_unset_exit=0` (uv resolves its cache from the passwd entry, not `HOME`).

## 5. Adversarial C — PATH lacking bwrap

```
$ PATH=/usr/local/bin /usr/bin/python3 -c 'import os,shutil;print("bwrap_on_path=",shutil.which("bwrap"))'
bwrap_on_path= None          bwrap_abs_executable= True
$ PATH=/usr/local/bin /usr/bin/python3 plans/git_webserver_probe.py --lane .
advC_exit=0   advC.err: (empty)
$ cmp $S/out/advC.txt corpus/evidence/round37/git-webserver-probe.txt && echo ADV_C_BYTE_EQUAL
ADV_C_BYTE_EQUAL    sha256=835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8
```

Stronger variant, `PATH=/nonexistent` (nothing at all on `PATH`): `advC2_exit=0`, `ADV_C2_BYTE_EQUAL`,
same sha256. `BWRAP = "/usr/bin/bwrap"` (`git_webserver_probe.py:49`) is absolute and the sandbox gets
`PATH=/work/bin`, so the probe is genuinely PATH-independent. After all runs: `git status --porcelain
--untracked-files=all | wc -l` → `0`.

## 6. Bonus — the refusal arm (`exit 2`) is real, and one arm is not

```
# bwrap hidden in a private mount ns (not removed from the host)
$ unshare -rm -- bash -c 'mount --bind /dev/null /usr/bin/bwrap; cd $D && python3 plans/git_webserver_probe.py --lane .'
crw-rw-rw- 1 nobody nobody 1, 3 … /usr/bin/bwrap
advD_exit=2   stderr: SETUP bubblewrap (/usr/bin/bwrap) is required
```

Correct refusal: exit 2, message on stderr, no stdout. This is one of the two outcomes the acceptance
allows; the three required environments did not need it.

## 7. Findings

**F1 (design fact, no action) — the frozen spec is a template, not a runnable spec.**
`plans/pkg-spec-r37.json` ships `"receipt_sha256": null` (read from the file; digest `4c61d103…`). A bare
`python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r37.json --require-clean-tree` therefore
rejects:

```
P2 DEFECT receipt_sha256=835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8
defects=1   exit=1
```

This is exactly what `round37_c2_verify.py:87-92` documents ("the counter fills `receipt_sha256` … so P2
is a presence check here and authenticity rests on P10"). Recorded so a reader does not mistake the
template run for a defect in the landing.

**F2 (low, gate output accuracy) — P10's `bytes=` is a character count.**
`c_rerun` prints `bytes={len(want)}` over decoded text (`pkg_gate.py:285`). Receipt:
`receipt_bytes=8529 receipt_chars=8443`; the 86-byte gap is 15 `❌` plus the em dashes in the case lines.
The equality test itself compares text, which is exact for this receipt, so nothing is admitted that
should not be; only the label is wrong, and a future failure report would quote a non-byte number.

**F3 (provenance note) — the C2 receipt's recorded TIP is not the wave-2 tip.**
`integrate/measure-final.txt:1` reads `TIP 5c7d5d75c2f36eb3477594432afe186b8b220086`; the wave-2 target
is `357dece`. Both are ancestors of master `dc90676`, and the entire probe package (`pkg_gate.py`,
`git_webserver_probe.py`, `pkg-spec-r37.json`, `round37_c2_verify.py`, the receipt, the six captures) is
byte-identical across `5c7d5d7`, `357dece` and `dc90676` (`git diff --stat` empty on those paths). The
receipt transfers, but it is a pre-integration measurement and should be labelled as one.

**F4 (operability, worth pricing) — a host without Bio *and* without network/cold uv cache turns P10
into a rejection, not a setup refusal.**
Inside a network-less netns with a fresh `UV_CACHE_DIR`:

```
P10 DEFECT fresh probe exit=2 stderr='error: Request failed after 3 retries in 6.8s\n  cause: Failed to fetch: https://'
defects=1   gate_exit=1
```

`c_rerun` catches the subprocess failure and returns a clause defect, so the gate exits 1 ("reject") — the
module docstring's own contract says 2 is for setup. On this host the P10 path has *no* local Bio fallback
(`import Bio` fails), so P10's operability rests on uv being able to resolve `biopython==1.85` (cache or
network). Not triggered in the primary run (network + cache available), but a CI or offline auditor would
read "package rejected".

**F5 (confirmation) — the sandbox isolation claim on the tip is true under a hostile host.**
Two simultaneous `:8080` listeners (host netns + scratch netns) produced no byte drift and no behaviour
change; the shipped probe's own loopback stays private (controls in §3.1 show what a leak would look
like).

## 8. Limits and risks

- One host, one kernel, one bubblewrap build (`0.13.1`, unprivileged userns enabled). A host with user
  namespaces disabled would fail earlier and refuse with exit 2 — acceptable per the acceptance, but it
  means P10 cannot be evaluated there (see F4 for what the gate then prints).
- Three required environments all ended byte-equal; the acceptance's `exit 2` alternative was not needed
  by A/B/C. The refusal arm was then exercised separately (§6).
- The probe executes the grader offline; no real `git push` occurs (its own docstring limit,
  `git_webserver_probe.py:21-23`). Nothing here bears on whether the oracle solution would pass.
- Host port `8080` was free at the start of the wave (`bind(127.0.0.1,8080)` succeeded); had it been busy,
  env A's host leg would have been confined to the scratch netns only.
- Adversarial A ran `unshare -rn` as uid 1000 with `-r` (map-root); this is an operator-level privilege
  the probe itself does not require, and it exposes nothing outside scratch.

## 9. Evidence manifest

All files below are in `.ufo/waves/round-37/falsify/F37ProbeOnTip/`, hashed in `SHA256SUMS`.

| file | what it is |
|---|---|
| `gate-v2.txt`, `gate-v2.err`, `gate-v2.time` | primary V2 run (exit 0, 10/10 clauses, 52.8 s) |
| `gate-v2-shim.txt`, `uv-calls.log` | same run with the uv shim: proves the uv branch |
| `probe-uv.txt`, `probe-uv.err`, `probe-uv.time` | `uv run …` probe alone, 8443-char/8529-byte receipt |
| `advA*` | env A: rc files, stderr, `ss` dumps (host + scratch ns), GET proofs |
| `advB*`, `advC*`, `advC2*` | env B (HOME unset), env C (`PATH=/usr/local/bin`), variant (`PATH=/nonexistent`) |
| `ctl-sharenet*.txt/.err` | positive control: `--share-net` copy of the probe over a live leak |
| `leak-reach-control.txt` | `share-net_status=200` / `unshare-net_status=000` on the same listener |
| `advD-hidden-bwrap.err/.txt` | refusal arm: bwrap hidden → exit 2, `SETUP bubblewrap …` |
| `gate-template-null.txt` | template spec without the digest → `P2 DEFECT`, exit 1 |
| `gate-v2-offline-cold.txt` | F4: no network + cold uv cache → `P10 DEFECT`, gate exit 1 |
| `byte-compares.txt` | per-leg sha256 + `cmp` against the receipt, versions, clean-tree count |

Scratch `/fast/scratch/hyaku/kengaku-r37/F37ProbeOnTip` was removed after these files were copied out.
No lane file was written; the clone was index-clean at the end (`tree_after_all_runs=0`) and never
committed to.

VERDICT: probe-on-tip-byte-equal-adversarial-3/3
