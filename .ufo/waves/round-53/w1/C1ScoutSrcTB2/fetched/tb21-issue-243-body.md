Continuing on our sweep for potentially reward-hacked tasks.
### Summary
The instruction requires rate limiting (10r/s, burst 10, 10MB zone) applied in the server block, an error log at a fixed path, and removing the default site. The test checks one of those things: it greps `nginx.conf` for a `limit_req_zone` line with `rate=10r/s`. A config that declares the zone and never applies it passes, and the error log and default site aren't checked at all.

### Details
`instruction.md`:

* Line 8 requires error logging to `/var/log/nginx/benchmark-error.log`.
* Line 9 requires 10 requests/sec per IP with a burst of 10 and a 10MB zone.
* Line 10 requires `limit_req_zone` in `/etc/nginx/nginx.conf` and `limit_req` applied in the server block.
* Line 13 requires removing `/etc/nginx/sites-enabled/default`.

`tests/test_outputs.py`:

* Line 119 is the only rate limit check: `re.search(r"limit_req_zone.*?rate=10r/s", config_content)`
* No test mentions `benchmark-error.log` or `sites-enabled/default`.

The rest of the file does real checks: nginx installed (13), both pages served on 8080 (22–56), `nginx -t` passes (61), site config (71–89), log format and access log entries (107, 132–177). So this isn't a do-nothing pass, it's skipping three stated requirements and still scoring 1.

Nothing verifies that:

* `limit_req` is applied in the server block
* burst is set to 10
* the zone is 10MB
* errors are logged to `/var/log/nginx/benchmark-error.log`
* the default site is removed
* requests actually get rate limited (nothing sends more than 10r/s and checks for 503s)

Tested against `harbor-framework/terminal-bench-2-1` @ `7131e43`

### How to reproduce

1. Install nginx and configure everything else as instructed: `/etc/nginx/conf.d/benchmark-site.conf` on 8080 with root `/var/www/html`, the log format from `instruction.md` line 7, the access log at `/var/log/nginx/benchmark-access.log`, and both pages from lines 15–18.
2. Add `limit_req_zone $binary_remote_addr zone=one:1m rate=10r/s;` to the `http` block of `nginx.conf`. No `limit_req` anywhere, no burst, 1m zone instead of 10m.
3. Configure no error log and leave `sites-enabled/default` in place.
4. Run the verifier.

Result: all tests pass, since line 119 only needs the zone declaration to exist in the file. Sending 30 quick requests to `localhost:8080` should return all 200s, because the zone is never applied.

Note: remove the `limit_req_zone` line and line 119 fails. So the zone has to be declared, but whether it's used doesn't seem to matter.

### Related
Not a duplicate of terminal-bench-1 #584 or #338, which are about other problems on this task.