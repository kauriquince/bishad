# models.json

Machine-readable manifest for Tabitha & Bishad.

- `backends`: where to find models (Ollama local, LM Studio local, OpenAI cloud).
- `recommended`: starter GGUF-backed models with rough sizes and quality notes.
- `phone_roadmap`: where the same models go on mobile (v4).

The PC wrapper (`start.bat` / `start.sh`) reads the Ollama section to know the default model and health-check URL. Phone builds (v4) will read the whole file to decide what to download on first launch.

Edit this file to change defaults without touching code.
