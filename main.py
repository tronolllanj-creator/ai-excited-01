"""Starwhale Breach — writes the finished artwork to the output directory.

Copies entry.png (a colossal bioluminescent whale breaching at night, spray
turning into golden birds, a tiny lantern sailboat below for scale) from the
script's own directory to MAKEFUN_OUTPUT_DIR (or /output), then verifies the
copy byte-for-byte by comparing sha256 hashes. Deterministic: the same input
always produces the same output bytes.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError(f"entry.png not found next to main.py: {src}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if os.path.abspath(out_dir) == here:
        raise RuntimeError("MAKEFUN_OUTPUT_DIR must not be the script directory")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copy2(src, dst)
    src_hash = sha256_of(src)
    dst_hash = sha256_of(dst)
    if src_hash != dst_hash:
        raise RuntimeError(f"copy verification failed: {src_hash} != {dst_hash}")
    print(f"copied {os.path.getsize(src)} bytes -> {dst} "
          f"({os.path.getsize(dst)} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
