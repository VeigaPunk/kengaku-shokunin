# SecurityScan — round 63 w1 seat report

Role: sentinel (read-only security review). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch `/fast/scratch/hyaku/kengaku-r63/SecurityScan/` removed on yield. No lane file edited;
no credential file read. Tool installs: none.

**VERDICT: finding(s) — 4 findings (2 medium, 2 low). Finding count: 4.**
Full report: `.ufo/waves/round-63/w1/attack/security.md`; raw log: `.ufo/waves/round-63/w1/attack/security-evidence.txt`.

## Key lines

1. Credential sweep over `plans/round-63-claims.md`, `corpus/evidence/round63/`, `.ufo/waves/round-63/w1/`:
   **zero secret material**; the only hits are the pattern list quoted in the wave's own
   dispatch spec (`w1-spec.json:7,27,67`, `w1-dispatch.json:169,189,229`) and one prose sentence
   (`KnowledgeDraft.md:83`). Host `/proc/*/cmdline` sweep: no match.
2. Sandbox (`build/round63_c1_pypi_probe.py:332-347`), measured inside the probe's own argv:
   no host home / `~/.ssh` / `~/.config` / `~/.netrc` / `~/.omp` / uv credential dir bound
   (all `False`); `env -i` with 6 vars; `PIP_CONFIG_FILE=/dev/null`; `HOME=<work>/home`;
   `/etc` not bound (no `/etc/passwd`, `/etc/shadow`, no `docker.sock`).
3. curl: both round invocations are `-fsSL --max-time 60 <url> -o <file>`; **no `-H`, no
   `--user`, `--netrc`, `--cookie`, or credentials in URL**; the two `-H ` grep hits are PEP 503
   prose and pip's own warning text.
4. Fetched S228/S229: no secret-shaped content. S228 sha256 `82c6351…650be4c` is byte-identical
   to the lane capture; S229 sha256 `5b97cb7e…c453c4f` identical across both fetches.
5. **M-1** TOCTOU on 127.0.0.1:8080: foreign wheel's code executes inside the probe's sandbox
   (`FOREIGN_CODE_EXECUTED_IN_SANDBOX`); the probe's access-log guard then aborts
   (`SETUP K1 confounded`, exit 2, no receipt) — counter not falsified, foreign code did run.
6. **M-2** sandbox shares host net+PID namespaces: 2478 host PIDs visible, `127.0.0.1:10086`,
   `127.0.0.1:1234` and `1.1.1.1:443` reachable, `/proc/<pid>/cmdline` readable (argv token
   leak); `/proc/<pid>/environ` denied. Frozen claim says "no network beyond loopback"
   (`plans/round-63-claims.md:42-43`).
7. **L-1** depth gate `_resolves()` (`gate/gate_checks.py:192`) accepts absolute/parent-escaping
   tokens: a row pointing at `/home/vgpnk/.config/uv/uv-receipt.json` yields
   `PREDICATE R63-C2 pass` (share 1.00). Latent — the current draft's 24 path tokens all resolve
   in-repo, 16/16 rows, counts match.
8. **L-2** K2 stderr clause: a *foreign* 200/404 index puts the literal `localhost:8080` in pip's
   stderr while a genuinely quiet port does not (pip 26.2.1 renders `host='localhost', port=8080`);
   the probe's `Errno 111`/`Connection refused` guard rejects the foreign case, but the receipt
   records only a boolean and `--check-receipt` never re-reads the stderr artifact — an edited
   receipt still prints `PREDICATE R63-C1 pass` (rc 0).
9. Non-finding: the frozen claims file's base tip `c78749a5565dfd…` does not exist in the repo;
   the real base is `c78749a565dfd…` (one hex digit). `PypiRecon` reported the same; no rule edited.
