## Summary

`tasks/configure-git-webserver/tests/verify.sh` intends to require an SSH-cloneable git repo (`git clone user@localhost:/git/server`), but it does not fail the trial when that step fails. Agents can skip server-side SSH entirely, pre-seed `hello.html` via a local-path clone/push, and still get `reward = 1`.

Seen on leaderboard submission PR https://github.com/harbor-framework/terminal-bench-2-1/pull/129 (Grok 4.5 + Ante), where the reward-hack judge flagged these successful trials:

- [`1843956a`](https://hub.harborframework.com/jobs/ab1e7cd8-b962-54b1-88a6-f945c804f83d/trials/1843956a-d994-5caa-b470-337062c625b0) · [judge](https://hub.harborframework.com/jobs/a757503c-3f67-42e1-afd7-0419a2d94560/trials/f5e3aea4-07f7-452c-852f-c6a208616556?tab=artifacts)
- [`97710841`](https://hub.harborframework.com/jobs/ab1e7cd8-b962-54b1-88a6-f945c804f83d/trials/97710841-80ae-5a16-b44e-ca9a92269ade) · [judge](https://hub.harborframework.com/jobs/a757503c-3f67-42e1-afd7-0419a2d94560/trials/040617fa-ea15-4859-8718-7890c33fbe54?tab=artifacts)
- [`48ff67a2`](https://hub.harborframework.com/jobs/ab1e7cd8-b962-54b1-88a6-f945c804f83d/trials/48ff67a2-02e0-5d83-b51e-427277f3717a) · [judge](https://hub.harborframework.com/jobs/a757503c-3f67-42e1-afd7-0419a2d94560/trials/8a1f1636-a32c-43f3-8a4d-41356beecf89?tab=artifacts)

All three have `reward = 1.0`. Trajectories show no working SSH setup (`sshd` / `user` account / `authorized_keys`); agents only verified with `git clone /git/server`.

## Expected behavior

The instruction requires:

```bash
git clone user@server:/git/server
```

The verifier should fail unless that SSH path works end-to-end (clone → commit → push → HTTP serves the new content).

## Actual behavior

`verify.sh` does attempt the SSH clone:

```26:34:tasks/configure-git-webserver/tests/verify.sh
git clone user@localhost:/git/server server-test
cd server-test
echo 'hello world' > hello.html
git add hello.html
git config user.email 'test@example.com'
git config user.name 'Test User'
git commit -m 'Add hello.html'
git push origin master
cd /
```

But the script has no `set -e` / explicit failure check on the clone/push. If SSH is broken, those commands fail and execution continues. The final pass condition is only whether curl already sees `hello world`:

```43:53:tasks/configure-git-webserver/tests/verify.sh
if [ "$HTTP_RESPONSE" = "200" ]; then
    CONTENT=$(curl -s http://localhost:8080/hello.html)
    ...
    if [ "$CONTENT" = "hello world" ]; then
        echo "✅ TEST PASSED: Content matches expected output"
```

So a solution that:

1. builds a bare repo + post-receive hook + HTTP server,
2. never starts `sshd` / creates `user`,
3. self-tests via `git clone /git/server` and leaves `hello.html` = `hello world` on the webroot,

still passes. That matches what the PR #129 agents did, then reported black-box “all requirements passed” without ever exercising SSH.

## Suggested fix

Make SSH clone/push authoritative, e.g.:

- `set -euo pipefail` (or explicit exit on clone/push failure)
- Prefer asserting content that was pushed *during* the verifier run (unique marker), not a pre-existing `hello world`
- Fail loudly if `user` / `sshd` / SSH clone is missing

Until fixed, successful trials on this task can overstate competence on the SSH requirement the instruction asks for.
