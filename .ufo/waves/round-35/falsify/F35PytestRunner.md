# F35PytestRunner — round 35 wave 2 falsify report

Seat: F35PytestRunner (executor, leaf). Target: falsify C1's landed grader-run claim by executing the
pinned `protein-assembly` grader exactly the way the receipt's `test.sh` does, on the three assigned
probe cases, and comparing pytest exit-derived reward with the receipt's `observed` column.

Lane tip verified: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (`git rev-parse HEAD`, 2026-10-25).
Grader pin verified: `corpus/evidence/round35/tb2-eval/test_outputs.py` sha256
`44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` == receipt `sha256` column.

## Method (reproducible command)

Case bytes generated from the frozen probe builder:

```
python3 .ufo/waves/round-35/falsify/F35PytestRunner/gen_cases.py <tmpdir>
# imports build_cases from plans/tb2_grader_probe.py; writes <tmpdir>/<case>/gblock.txt
```

Per case, replicate the `test.sh` uvx invocation (`uvx -p 3.13 -w pytest==8.4.1
-w biopython==1.85 -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json
/tests/test_outputs.py -rA`) inside a user+mount namespace so the grader's hard-coded
`/app/gblock.txt` is served from a tmp dir — no host `/app`, no sudo (bwrap 0.13.1,
`--unshare-user`; `/` left empty, only needed paths bound rw, including `/run` for
`/etc/resolv.conf -> /run/systemd/resolve/stub-resolv.conf`):

```
bwrap --unshare-user \
  --bind /usr /usr --bind /etc /etc --bind /lib /lib --bind /lib64 /lib64 \
  --bind /bin /bin --bind /var /var --bind /home /home --bind /root /root \
  --bind /run /run --bind /sys /sys --proc /proc --dev /dev --tmpfs /tmp \
  --dir /app --bind $CASE /app \
  --dir /tests --bind <lane>/corpus/evidence/round35/tb2-eval /tests \
  --dir /logs --dir /logs/verifier --chdir /app \
  /home/vgpnk/.local/bin/uvx -p 3.13 -w pytest==8.4.1 \
    -w biopython==1.85 -w pytest-json-ctrf==0.3.5 \
    pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
Reward = 1 iff exit 0 (same rule as test.sh lines 26-29).
```

Fidelity note: host `uv` is 0.13.0 (test.sh installed uv 0.9.5 in-container); same pinned python 3.13 and
package versions, so pytest/grader behavior is what the container would see. No tool was installed by this
seat (uvx and bwrap already present).

## Results

| case | receipt observed | receipt reward | pytest exit | my reward | match |
|---|---|---|---|---|---|
| valid-balanced | pass | 1 | 0 | 1 | yes |
| linker-g-only | pass | 1 | 0 | 1 | yes |
| linker-4aa | fail | 0 | 1 | 0 | yes |

Evidence (excerpts from run logs, all in the now-removed /tmp/k35f-XjwK/<case>/run.log):

- valid-balanced / linker-g-only: exit 0; `============================== 1 passed in 0.03s ===============================`
- linker-4aa: exit 1; assertion matches receipt verbatim:
  `E           AssertionError: Linker must be between 5 and 20 amino acids long.` with
  `E           assert 5 <= 4` at `/tests/test_outputs.py:57`, `FAILED ../tests/test_outputs.py::test_gblock`.

Case content sanity vs receipt: nt lengths 2586/2586/2583 match receipt rows; generator printed grader
sha256 matching the receipt pin.

## Conclusion

No disagreement found. The grader executed in the `test.sh` shape produces exactly the observed column of
the receipt for all three assigned probes (the only difference is the working file, which the receipt
records as pass/pass/fail).

VERDICT: pytest-agree-3/3
