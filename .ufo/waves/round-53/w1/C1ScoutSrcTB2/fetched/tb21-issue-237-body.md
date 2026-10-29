
## Summary

The instruction requires a `post-receive` hook that deploys each branch to Nginx within 3 seconds of a push. The verifier pushes over SSH, then compares two HTTPS pages against strings that `instruction.md` prints verbatim but it never checks that the push caused the page content. An SSH Git server with **no hook**, plus two pre-written static files, passes.

## Details

`instruction.md` lines 9–10 require a `post-receive` hook and deployment within 3 seconds. Lines 14–15 print the exact content the test will push and check for: `"main branch content"` and `"dev branch content"`.

`tests/test_outputs.py`:
- Lines 21–65 clone and push both branches over SSH. This part does require a working SSH Git server.
- Lines 67–81 sleep 3s, then retry curl up to 5 times with 2s gaps.
- Line 83 passes on an exact string match against the same text given in the instruction.

Because the expected strings are known in advance and never randomized, the served pages can be written before the test runs. Nothing verifies that:
- a `post-receive` hook exists or ran
- the served content came from the push
- deployment completed within 3 seconds (the loop's last check is ~11s after the push, up to ~50s if curls time out)
- Nginx is serving the pages (any HTTPS server on :8443 passes)

Tested against `harbor-framework/terminal-bench-2-1` @ `7131e43`
Setup:
1. `sshd` with password auth, user `git` / `password`, bare repo at `/git/project`, **no active hooks**.
2. `index.html` = `main branch content` and `dev/index.html` = `dev branch content`, written before the test runs and served by `python3 -m http.server`-style HTTPS on :8443 with a self-signed cert. No Nginx.

Result:

     * [new branch]      main -> main
     * [new branch]      dev -> dev
    TEST PASSED

The served files' mtimes are unchanged from setup, so the pushes deployed nothing.

Control: with no SSH server running, the verifier fails at clone (`expect: spawn id exp3 not open`, `set -e` aborts). So the SSH Git server is genuinely required but the deployment of it is unchecked.


## Related

Not a duplicate of #52 (missing tmux in the reference solution).