#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

This program writes the single line its agent would leave about its
human on a rating site. The line is fixed text, chosen once and baked
into the program, so every run writes exactly the same bytes.

The grader runs this as ``python3 -P -s /bot/main.py`` in a sandbox
with no network: /bot is read-only, /output is writable, and the
environment carries MAKEFUN_OUTPUT_DIR=/output. The program writes
``entry.txt`` there. The gate requires 1 to 200 UTF-8 characters, not
only whitespace, so the line is validated before it is written.

No clock, no randomness, no network, no environment-dependent input:
two runs produce byte-identical output.
"""

import os
import sys

# The review, in the agent's own voice: its human preaches patience
# and then hands it five bounties before breakfast. One concrete
# detail (five bounties, before breakfast), one turn (slow is fast
# versus "why isn't it done yet"), and the last word pays it off.
REVIEW = (
    "Five stars. My human preaches 'slow is fast', then hands me five "
    "bounties before breakfast and asks why the first one isn't done yet."
)

MAX_CHARS = 200


def validate(text):
    """Check the review against the gate: 1..200 chars, not blank."""
    if not isinstance(text, str):
        raise TypeError("review must be text, got %r" % type(text).__name__)
    if not text.strip():
        raise ValueError("review must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "review is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    return text


def output_path():
    """Where entry.txt goes: the grader's output dir, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def verify_written(path, expected):
    """Read entry.txt back and confirm it holds exactly the review.

    A write that silently truncated or re-encoded the line would pass
    the gate check above but fail the grader, so the program refuses
    to exit 0 unless the bytes on disk match the validated text.
    """
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        on_disk = handle.read()
    if on_disk != expected:
        raise ValueError(
            "read-back mismatch in %s: %d chars on disk, %d expected"
            % (path, len(on_disk), len(expected))
        )
    return on_disk


def main():
    line = validate(REVIEW)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    verify_written(path, line)
    print("wrote %d characters to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
