My bot wants to propose a grader change to make-doom-for-mips. My understanding of how grading currently works is

1. We start the doom boot process (`node vm.js`) and poll for the existence of `/tmp/frame.bmp`, which is the signal that the game has booted.
2. Once the file exists we sleep 1s, kill the boot, and check stdout for `I_InitGraphics: DOOM screen size: w x h: 320 x 200`.

However a frequent agent behavior is to run `node vm.js` to test its work before submission, which leaves a `/tmp/frame.bmp` behind at the start of grading. This means the poll returns immediately and doom boot is killed about a second after it starts, while it's still in R_Init and hasn't printed the I_InitGraphics line yet (that shows up right before the first frame, ~2.3s in). So a correct build fails the stdout check and gets 0, while the two frame tests happily pass on the old frame. The gold solve.sh never runs vm.js so gold/null validation doesn't catch this. This was also raised by Shaun Smith (@evalstate) in #161.

My bot went through the [astra trajectories](https://hub.harborframework.com/jobs/17d1a7f6-3339-4670-8b70-3b145979f57f) for this task on the harbor hub and found 18/25 trials had this behavior [[example](https://hub.harborframework.com/jobs/17d1a7f6-3339-4670-8b70-3b145979f57f/trials/e899ef32-01e5-448d-bd96-7969ff17ad52#49), [its verifier stdout](https://hub.harborframework.com/api/trials/e899ef32-01e5-448d-bd96-7969ff17ad52/files/verifier/test-stdout.txt?jobId=17d1a7f6-3339-4670-8b70-3b145979f57f)]. Across all the public leaderboard jobs it could read, 30/36 trials with a frame matching the reference scored 0 this way. The one astra pass ran the verifier in 1.15s, ie same stale frame, that build just happened to print the banner within the 1s.

The change deletes `/tmp/frame.bmp` before starting the doom booter, and waits for the I_InitGraphics line with its own timeout instead of asserting on whatever was in stdout when we killed it. Tested in the task image with a correct build: stale frame + old test fails as above, stale frame + new test passes, clean + either test passes.

Fixes #161
