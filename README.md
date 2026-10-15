# Tabitha & Bishad v3 — PC-first, auto-start local AI

## Quick start (PC)

1. Install [Ollama](https://ollama.com) (or LM Studio).
2. Double-click `start.bat` (Windows) or run `./start.sh` (Mac/Linux).
3. The script checks whether Ollama is running; if not, it starts it, waits for the API, then launches `server.py`.
4. Open http://127.0.0.1:8765 — choose AI dialogue, click Detect local models, pick one, press Start.

No models are bundled. The first chat downloads whatever you select from Ollama's registry (GGUF under the hood).

## Roadmap

- **v3 (now):** PC auto-start wrapper + model manifest + health checks.
- **v4:** Phone app — iOS (Core ML / MLX) and Android (ONNX Runtime / llama.cpp), downloading the same GGUF models from a CDN on first launch.
- Models live outside the repo; a `models.json` manifest points at Hugging Face / Ollama registry URLs.

This is parody, not quotes or a real-life relationship.
