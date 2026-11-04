<!-- SourceR84 draft of the round-84 lesson Gate row for S271. Shape copied from
     corpus/lessons/round-83.md §Gate (5 columns: id and decision | URL or own-work location |
     access date | located quote (each under 25 words) | reason / flip).
     The L1 installs this row into corpus/lessons/round-84.md; the lesson file does not exist yet. -->

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S271 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/gcode-to-text/tests/test_outputs.py | 2026-11-04 | :17: `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}", (` (5 words) | The pinned grader itself supplies the acceptance rule for the content leg and :10 supplies the presence leg; it does not prove an agent solved the task. flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is attempted from this source — a separate claim, not made here. |
