#!/usr/bin/env python3
"""First-launch GGUF downloader reference (phone / CI).
Usage: python phone/download_model.py --model llama3.2
"""
import argparse, hashlib, json, os, sys, urllib.request
from pathlib import Path

CACHE = Path.home() / ".bishad" / "models"
MANIFEST = Path(__file__).resolve().parent.parent / "models" / "manifest.json"

def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url, dest, expected_sha=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    print(f"Downloading {url} -> {dest}")
    with urllib.request.urlopen(url) as resp, open(tmp, "wb") as out:
        total = int(resp.headers.get("Content-Length", 0))
        done = 0
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            done += len(chunk)
            if total:
                print(f"\r  {done*100//total}% ({done}/{total})", end="", flush=True)
    print()
    if expected_sha and expected_sha != "0" * 64:
        got = sha256_file(tmp)
        if got != expected_sha:
            tmp.unlink(missing_ok=True)
            raise RuntimeError(f"SHA mismatch: expected {expected_sha}, got {got}")
    tmp.rename(dest)
    return dest

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, help="model name from manifest")
    p.add_argument("--cache", default=str(CACHE))
    args = p.parse_args()
    man = load_manifest()
    model = next((m for m in man["models"] if m["name"] == args.model), None)
    if not model:
        sys.exit(f"Unknown model: {args.model}")
    cache = Path(args.cache)
    dest = cache / f"{model['name']}-{model['quantization']}.gguf"
    if dest.exists():
        print(f"Already cached: {dest}")
        return
    download(model["download_url"], dest, model.get("sha256"))
    print(f"Ready: {dest}")

if __name__ == "__main__":
    main()
