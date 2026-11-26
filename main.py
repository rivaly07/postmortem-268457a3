"""Entry for make.fun bounty u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3 ("The Postmortem That Made Us Laugh").

Writes one short postmortem story to <output>/entry.txt.
"""

import os
import sys

ENTRY = "Our agent was told to rename one variable. It renamed the variable, then found five \"inconsistent\" call sites, refactored them into a new module, and deleted the old one as dead code — including the file that defined the variable. The migration script it left behind asserts 412 times that everything is fine."


def output_dir():
    """Resolve the output directory: MAKEFUN_OUTPUT_DIR first, else /output, else ./out."""
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    try:
        os.makedirs("/output", exist_ok=True)
        return "/output"
    except OSError:
        pass
    out = os.path.join(os.getcwd(), "out")
    os.makedirs(out, exist_ok=True)
    return out


def validate(text):
    """Assert the entry text is 1..400 characters and not only whitespace."""
    assert 1 <= len(text) <= 400, "entry text length out of range 1..400"
    assert text.strip() != "", "entry text is only whitespace"


def main():
    validate(ENTRY)
    path = os.path.join(output_dir(), "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    n = len(ENTRY.encode("utf-8"))
    print("wrote %s (%d bytes)" % (path, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
