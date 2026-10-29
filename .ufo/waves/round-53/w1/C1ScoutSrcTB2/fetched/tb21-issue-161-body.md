## Summary

`test_vm_execution` does not remove `/tmp/frame.bmp` before starting `vm.js`. If an agent self-test left the file behind, the verifier skips its 30-second wait, terminates the new process after one second, and inspects the stale frame.

This can reject a correct implementation before it finishes booting, and does not verify that the frame was produced by the verifier's invocation.

## Suggested fix

Delete `/tmp/frame.bmp` before starting `vm.js`, then wait up to 30 seconds for a new frame to appear.

The identical verifier in `make-mips-interpreter` is already discussed in #9.