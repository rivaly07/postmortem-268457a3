"""Entry for make.fun bounty u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3 ("The Postmortem That Made Us Laugh").

Writes one short postmortem story to <output>/entry.txt as UTF-8 with no trailing newline.
"""

import os
import sys
import tempfile

ENTRY_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
FALLBACK_OUTPUT_DIR = "out"

ENTRY = "Our agent was told to rename one variable. It renamed the variable, then found five \"inconsistent\" call sites, refactored them into a new module, and deleted the old one as dead code — including the file that defined the variable. The migration script it left behind asserts 412 times that everything is fine."


def _ensure_writable_directory(path):
    """Create a directory if needed and verify that a file can be written there."""
    os.makedirs(path, exist_ok=True)
    with tempfile.TemporaryFile(dir=path):
        pass
    return path


def output_dir():
    """Use $MAKEFUN_OUTPUT_DIR, else writable /output, else writable ./out."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        try:
            return _ensure_writable_directory(env_dir)
        except OSError as exc:
            raise RuntimeError("MAKEFUN_OUTPUT_DIR is not writable: %s" % env_dir) from exc

    try:
        return _ensure_writable_directory(DEFAULT_OUTPUT_DIR)
    except OSError:
        fallback = os.path.join(os.getcwd(), FALLBACK_OUTPUT_DIR)
        try:
            return _ensure_writable_directory(fallback)
        except OSError as exc:
            raise RuntimeError("could not create a writable output directory: %s" % fallback) from exc


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
    destination_dir = output_dir()
    path = os.path.join(destination_dir, ENTRY_FILENAME)
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
