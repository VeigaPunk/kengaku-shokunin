# R45MutV11States — result recovered from w1-results.json (reportless-seat class, round-45 recurrence)

<think>
I need to perform mutation probes. Need constraints: write only under w1/<seat> and scratch. Need report. Need scratch guard safe-rm. Need read package? User asks answer() regex against adversarial grader files (two 23-char tokens). This is purely logic, no counter? We can construct adversarial grader snippets in scratch and call answer() on them, likely through Python. Since they say "Run any fixture build, counter run or probe that can write files inside a bwrap sandbox in which ~/.local/bin is read-only (the envelope below does this)." We should wrap the test run in envelope.sh. Envelope itself bwrap home read-only, scratch bind writable
