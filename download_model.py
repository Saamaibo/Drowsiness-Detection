"""Download dlib's 68-point facial landmark model into Model/.

Usage:  python download_model.py

The model is trained on the iBUG 300-W dataset, whose license excludes
commercial use, so it is downloaded from the official source instead of being
redistributed in this repository.
"""
import argparse
import bz2
import hashlib
import shutil
import sys
import urllib.request
from pathlib import Path

URL = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
SHA256 = "fbdc2cb80eb9aa7a758672cbfdda32ba6300efe9b6e6c7a299ff7e736b11b92f"
DEST = Path(__file__).resolve().parent / "Model" / "shape_predictor_68_face_landmarks.dat"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--url", default=URL, help="override the download URL")
    p.add_argument("--no-verify", action="store_true", help="skip the SHA-256 check")
    p.add_argument("--force", action="store_true", help="download again even if the file exists")
    args = p.parse_args()

    if DEST.exists() and not args.force:
        print(f"{DEST} already exists. Use --force to download it again.")
        return 0

    DEST.parent.mkdir(parents=True, exist_ok=True)
    archive = DEST.with_suffix(".dat.bz2")
    print(f"Downloading {args.url}")
    try:
        with urllib.request.urlopen(args.url) as r, open(archive, "wb") as out:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                out.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r  {done / 1e6:.1f} / {total / 1e6:.1f} MB", end="", flush=True)
        print()

        print("Decompressing...")
        with bz2.open(archive, "rb") as src, open(DEST, "wb") as dst:
            shutil.copyfileobj(src, dst)
    except Exception as e:
        DEST.unlink(missing_ok=True)
        print(f"Download failed: {e}", file=sys.stderr)
        return 1
    finally:
        archive.unlink(missing_ok=True)

    if not args.no_verify and sha256_of(DEST) != SHA256:
        DEST.unlink()
        print("Checksum mismatch, so the file was deleted. Use --no-verify to skip this check.",
              file=sys.stderr)
        return 1

    print(f"Saved to {DEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
