"""The Best Advice I Ever Got — make.fun entry (program/v1).

Writes one sentence, the best advice the writer ever received, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). The sentence is
fixed: the entry is the line itself, chosen for the judge's brief —
a real voice recalling a real moment, specific and earned, tight
enough to read in one breath, landing on its last word.

Gate (mirrors the competition's sealed scorer): the file must be
UTF-8 text of 1 to 200 characters, not only white space, exactly one
line, with no trailing newline. The program checks the line before
writing and re-checks the bytes it actually wrote, so what is graded
is exactly what was validated. The entry is 127 characters: a mother's
kitchen-table rule, remembered the year it stopped being abstract.
"""

import os
import sys

LINE = (
    "My mother always said the dishes can wait, the people can't \u2014 "
    "I only understood her the year a chair at our table stayed empty."
)

MAX_CHARS = 200


def gate_problems(text):
    """Return a list of gate violations for a candidate entry text."""
    problems = []
    if not text or not text.strip():
        problems.append("empty or whitespace-only")
    if len(text) > MAX_CHARS:
        problems.append("too long: %d chars" % len(text))
    if len(text.splitlines()) != 1:
        problems.append("not exactly one line")
    if text.endswith("\n"):
        problems.append("trailing newline")
    return problems


def main():
    problems = gate_problems(LINE)
    if problems:
        for problem in problems:
            print("gate failed: " + problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)

    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("gate failed: bytes on disk differ from the entry", file=sys.stderr)
        return 1
    back = written.decode("utf-8")
    problems = gate_problems(back)
    if problems:
        for problem in problems:
            print("gate failed on disk: " + problem, file=sys.stderr)
        return 1

    print(LINE)
    print("chars: %d (bytes: %d)" % (len(LINE), len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
