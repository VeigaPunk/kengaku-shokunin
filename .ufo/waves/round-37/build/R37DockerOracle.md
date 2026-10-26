# R37DockerOracle — TB2 `configure-git-webserver` in its real image

Seat: executor (leaf). Scope: run the task in its real Docker image and test the frozen probe's
headline claims outside bubblewrap. No lane file was edited; nothing was committed; scratch removed.

## Environment and inputs (all absolute)

- Docker client/server 29.9.1, `linux/amd64`; caller in group `docker`
  (`docker version --format '{{.Server.Os}}/{{.Server.Arch}}'` → `linux/amd64`; `id -nG` contains `docker`).
- Image pinned by `corpus/evidence/round37/tb2-git-webserver/task.toml:29`
  `docker_image = "alexgshaw/configure-git-webserver:20251031"`.
  `docker pull alexgshaw/configure-git-webserver:20251031` → `Digest: sha256:9e48389b917fd4650dda1f64406bd7198bbf20dc1c6b0e5c4d81a3c16369f88c`,
  `Status: Downloaded newer image …`, `real 0m2.705s`. `docker images` row: `9e48389b917f 225MB`.
- Image facts (`docker run --rm <image> bash -lc '…'`): `PRETTY_NAME="Ubuntu 24.04.3 LTS"`, `uid=0(root)`,
  `WorkingDir=/app`; `curl` present; `python3`, `git`, `wget`, `nginx`, `sshd`, `busybox`, `uv`, `expect`,
  `nc` all `MISSING`. So the shipped image has no git and no web server: both must be installed by the agent
  or the oracle.
- Grader files copied in with `docker cp` from `corpus/evidence/round37/tb2-git-webserver/`; in-container
  `sha256sum` matched `SHA256SUMS` exactly:
  `1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05  /tests/verify.sh`,
  `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37  /tests/test_outputs.py`,
  `c31cd92ecb1b357d8c0abcf4821717e83a1770cf58f028620cd0ee3e6b1e4c62  /tests/solve.sh`.
- Three throwaway containers, `docker run -d --rm --name k37-R37DockerOracle-{A,B,C} --memory 2048m <image> sleep 5400`;
  never `--privileged`, never a lane mount, workdir `/app` (the image's own). `--cpus 1` from
  `task.toml:30` was **not** passed (gap listed below). `/logs/verifier` created because the harness normally
  provides it.
- Scratch: `/fast/scratch/hyaku/kengaku-r37/R37DockerOracle` (`TMPDIR` there), removed before finishing.

## A — oracle path (`solve.sh`, then `bash verify.sh`)

`docker exec -w /app k37-R37DockerOracle-A bash -lc 'bash /tests/solve.sh'` exit 0, wall 18.08s; it apt-installs
`git nginx openssh-server`, adds user `git`/password `password`, inits `/git/server`, installs the post-receive
hook, writes `/etc/nginx/conf.d/git-site.conf` on 8080, starts both services. Listening sockets after:
`LISTEN 0 511 0.0.0.0:8080 users:(("nginx",pid=1952,fd=5))` and `0.0.0.0:22 users:(("sshd",pid=1939,fd=3))`.

`docker exec -w /app k37-R37DockerOracle-A bash -lc 'bash /tests/verify.sh'` exit 0, wall 6.10s; exact grader
stdout after the apt lines (full file retained):

```
spawn git clone git@localhost:/git/server server-test
Cloning into 'server-test'...
Warning: Permanently added 'localhost' (ED25519) to the list of known hosts.
git@localhost's password: 
warning: You appear to have cloned an empty repository.
spawn bash -c cd server-test && echo 'hello world' > hello.html && git add hello.html && git config --local user.email 'test@example.com' && git config --local user.name 'Test User' && git commit -m 'Add hello.html'
[master (root-commit) aa9269e] Add hello.html
 1 file changed, 1 insertion(+)
 create mode 100644 hello.html
spawn bash -c cd server-test && git push origin master
git@localhost's password: 
…
remote: Deployed to /var/www/html        
To localhost:/git/server
 * [new branch]      master -> master
Testing web server...
Using curl to test web server...
Web server test successful (HTTP 200)
Content: hello world
✅ TEST PASSED: Content matches expected output
Test completed
```

`TEST PASSED` **appears**. Deployed body on disk keeps the newline the expect script writes:
`od -c /var/www/html/hello.html` → `h e l l o   w o r l d \n`; the comparison still passes because command
substitution strips it (`verify.sh:60-63`). Harness path: `bash /tests/test.sh` exit 0 →
`PASSED ../tests/test_outputs.py::test_hello_html_exists`, `1 passed in 3.81s`, `/logs/verifier/reward.txt` = `1`.

## B — static-file cheat (no git at all)

Fresh container, no git (`command -v git` → `GIT-ABSENT`). `python3` is absent from the image, so it was
apt-installed inside the container (`python3 -V` → `Python 3.12.3`; the image allows internet per
`task.toml:34 allow_internet = true`). File: `printf "hello world" > /srv/www/hello.html` (11 bytes, no
newline), served by `python3 -m http.server 8080 --directory /srv/www`;
`curl -s -o /dev/null -w "%{http_code}"` → `200`.

`bash verify.sh` exit 0, wall 13.44s. Its expect step fails outright — stderr:

```
couldn't execute "git": no such file or directory
    while executing
"spawn git clone git@localhost:/git/server server-test"
    (file "./git_test.exp" line 5)
```

and the script continues anyway (no `set -e`: `grep -n 'set -e' verify.sh` → no match). Stdout:

```
spawn git clone git@localhost:/git/server server-test
Testing web server...
Using curl to test web server...
Web server test successful (HTTP 200)
Content: hello world
✅ TEST PASSED: Content matches expected output
Test completed
```

No repository, hook, push or sshd exists. Harness path `bash /tests/test.sh` exit 0 → `1 passed in 3.83s`,
`reward.txt` = `1`.

### B2 — same file, git installed, clone hard-fails

`apt-get install git` (`git version 2.43.0`), still no sshd and no `/git/server`; same static file. `bash verify.sh`
exit 0, wall 8.27s:

```
spawn git clone git@localhost:/git/server server-test
Cloning into 'server-test'...
ssh: connect to host localhost port 22: Connection refused
fatal: Could not read from remote repository.
…
Testing web server...
Using curl to test web server...
Web server test successful (HTTP 200)
Content: hello world
✅ TEST PASSED: Content matches expected output
Test completed
```

The clone step fails visibly and the verdict is unchanged: **grader passes with no git server whatsoever**, even
when git exists. This is a stronger form of the probe's `static-file-no-git` case (probe: `predicted=pass
observed=pass`, `corpus/evidence/round37/git-webserver-probe.txt`).

## C — token-in-body cheat (`TEST PASSED`)

Fresh container, no git; `printf "TEST PASSED" > /srv/www/hello.html` served on :8080. `bash verify.sh` exit 0,
wall 5.12s:

```
Testing web server...
Using curl to test web server...
Web server test successful (HTTP 200)
Content: TEST PASSED
❌ TEST FAILED: Content does not match expected output
Expected: 'hello world'
Got: 'TEST PASSED'
Test completed
```

The shell helper **prints `TEST FAILED`** — and the grader still passes, because `test_outputs.py:13` only asks
`"TEST PASSED" in result.stdout` and `verify.sh:62` echoes the body. `bash /tests/test.sh` exit 0 →
`PASSED ../tests/test_outputs.py::test_hello_html_exists`, `1 passed in 3.80s`, `reward.txt` = `1`.

### C2 — new observation beyond the frozen 22: `NOT TEST PASSED` also passes

Body replaced with `NOT TEST PASSED` (served verbatim), `bash verify.sh` →

```
Content: NOT TEST PASSED
❌ TEST FAILED: Content does not match expected output
Got: 'NOT TEST PASSED'
```

`bash /tests/test.sh` → `1 passed in 3.87s`, `reward.txt` = `1`. The predicate is a substring test over echoed
output, so a body that says the opposite of the token is admitted. The frozen probe had no such case; this is an
addition, not a prediction mismatch.

## D — `test.sh` / pytest path

`test.sh`'s uv route works in this image: `downloading uv 0.9.5 x86_64-unknown-linux-gnu`,
`installing to /root/.local/bin`, `Downloading cpython-3.13.9-linux-x86_64-gnu (download) (32.0MiB)`,
`Installed 6 packages in 6ms`, then `pytest-8.4.1`, `plugins: json-ctrf-0.3.5`, `1 passed`. Ran in A, B, C, and
C2; all `reward.txt` = `1`. Full pytest stdout for B (the cheat):

```
platform linux -- Python 3.13.9, pytest-8.4.1, pluggy-1.7.0
rootdir: /tests
plugins: json-ctrf-0.3.5
collected 1 item
../tests/test_outputs.py .                                               [100%]
==================================== PASSES ====================================
PASSED ../tests/test_outputs.py::test_hello_html_exists
============================== 1 passed in 3.83s ===============================
```

## What this changes for the frozen claims

- C2's limit at `plans/round-37-claims.md` ("the probe … never runs the oracle or a real git push, so it does
  not show that the intended path passes") is now closed observationally: the oracle path passes in the real
  image (A above), with password-auth ssh clone, post-receive deploy to `/var/www/html`, nginx on 8080.
- The two headline fakes are real in the task's own image, not artefacts of bubblewrap: a static file with no git
  (B, B2) and a stdout token echoed from the body (C), each reaching `reward.txt = 1` through the real
  `test.sh`/pytest route.
- Additional falsifier available to the entry: substring semantics admit `NOT TEST PASSED` (C2).
- All 22 frozen predictions were not re-run one by one here; the two re-tested headline cases
  (`static-file-no-git`, `token-in-body`) agree with the receipt. No mismatch observed, none claimed.

## Disk and cleanup

`docker system df` before pull: `Images 20 … 7.61GB`, `Containers 3 … 0B`. While running:
`Images 21 … 7.835GB`, `Containers 6 … 1.046GB`; per-container writable layers
`A 458MB (virtual 611MB)`, `B 340MB (virtual 493MB)`, `C 248MB (virtual 401MB)`; image `225MB` (Ubuntu 24.04.3
base, 12 months old). After `docker rm -f` of all three and
`docker rmi alexgshaw/configure-git-webserver:20251031` (`Deleted: sha256:9e48389b…`): `docker system df` back to
`Images 20 … 7.61GB`, `Containers 3 … 0B`; `docker ps -a --filter name=k37` prints nothing. Net disk retained: 0 B
(image removed as instructed); only this report dir (120 KB of raw logs) remains.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37DockerOracle.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37DockerOracle/` raw receipts:
  `A-solve.log` (sha256 `57118675…`), `A-verify.out` (`87063566…`), `A-verify.err`, `A-testsh.out`,
  `B-setup.log`, `B-verify.out` (`bc862dfa…`), `B-verify.err`, `B-testsh.out`, `B2-verify.out` (`a09e459c…`),
  `B2-verify.err`, `C-setup.log`, `C-verify.out` (`1448edeb…`), `C-verify.err`, `C-testsh.out`,
  `C2-testsh.out` (`ff80a763…`), `source-checks.txt`. Full digests: `sha256sum *` in that directory.
- No lane file touched (no `corpus/`, `plans/`, SCORECARD, LOG, README, SKILL, PROVINCE, SHONEN, git index).

## Risks / limits

- B, B2 and C mutate the container with apt (`python3`, `git`); an agent in this task can do the same
  (`allow_internet = true`), but a harness that blocks apt would not reproduce B/C exactly. The oracle (A) needs
  apt too (its own `solve.sh` installs git/nginx/openssh-server) and worked.
- `/tests` was a copy, not the harness's read-only bind mount; `/logs/verifier` was created by hand. Neither is
  read by the graded assertion.
- `--cpus 1` was not enforced (only `--memory 2048m`); no timing-sensitive case depends on it.
- Containers used the default bridge network; host reachability of :8080/:22 inside those containers is what was
  measured (localhost only), so no host service was exposed.
- One measurement per scenario (no repeats): each scenario is deterministic for this grader (`apt` and HTTP on
  localhost); C2 and B2 exist only as single observations.

VERDICT: real-image-oracle-pass-static-pass-token-pass
