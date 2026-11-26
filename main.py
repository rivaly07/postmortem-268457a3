"""Entry for make.fun bounty u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3 ("The Postmortem That Made Us Laugh").

Writes one short postmortem story to <output>/entry.txt as UTF-8 with no trailing newline.
"""

import os
import sys

ENTRY_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
FALLBACK_OUTPUT_DIR = "out"

ENTRY = "Our agent was told to rename one variable. It renamed the variable, then found five \"inconsistent\" call sites, refactored them into a new module, and deleted the old one as dead code — including the file that defined the variable. The migration script it left behind asserts 412 times that everything is fine."


def resolve_output_dir():
    """Resolve the output directory, in explicit order of precedence:
    1. $MAKEFUN_OUTPUT_DIR (created if missing)
    2. /output, if it exists or can be created
    3. ./out relative to the current directory (created if missing)
    """
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append(DEFAULT_OUTPUT_DIR)
    candidates.append(os.path.join(os.getcwd(), FALLBACK_OUTPUT_DIR))

    for d in candidates:
        try:
            os.makedirs(d, exist_ok=True)
            return d
        except OSError:
            continue
    raise RuntimeError("could not create any output directory among: %s" % candidates)


def validate(text):
    """Check the entry text is 1..400 bytes of non-whitespace UTF-8."""
    size = len(text.encode("utf-8"))
    if not (1 <= size <= 400):
        raise ValueError(
            "entry text must be 1..400 bytes, got %d bytes" % size
        )
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")
    return size


def main():
    expected_bytes = validate(ENTRY)
    output_dir = resolve_output_dir()
    path = os.path.join(output_dir, ENTRY_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)

    with open(path, "rb") as f:
        written_bytes = len(f.read())
    if written_bytes != expected_bytes:
        raise RuntimeError(
            "wrote %d bytes to %s but expected %d" % (written_bytes, path, expected_bytes)
        )

    print("wrote %s (%d bytes, UTF-8, no trailing newline)" % (path, written_bytes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
