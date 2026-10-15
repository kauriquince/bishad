# Tabitha & Bishad v4 — Phone App Architecture

## Overview
Phone clients share the same model list as the PC stack. `models/manifest.json` (and the mirrored `phone` section in `models.json`) drives first-launch downloads.

## Platforms
- **iOS**: Core ML or MLX, loading GGUF models served from the Hugging Face CDN. On-device cache after download.
- **Android**: ONNX Runtime or llama.cpp (via JNI), same GGUF files.

## First launch
1. Read manifest.
2. Check local cache (`~/.bishad/models` or app sandbox equivalent).
3. Download missing GGUF with progress bar.
4. Verify SHA-256 (placeholder until pinned).
5. Cache and switch to offline-only mode.

## Reference downloader
`phone/download_model.py` is a standalone Python reference that implements the same flow for testing and CI.

No model binaries are stored in the repo.
