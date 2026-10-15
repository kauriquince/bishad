#!/usr/bin/env bash
# Tabitha & Bishad v3 — PC auto-start wrapper (Mac/Linux)
set -euo pipefail
cd "$(dirname "$0")"

OLLAMA_URL="${LOCAL_AI_URL:-http://127.0.0.1:11434}"
SERVER_URL="http://127.0.0.1:8765"

echo "[bishad] checking Ollama..."
if ! curl -sf "$OLLAMA_URL/api/tags" -o /dev/null; then
  echo "[bishad] Ollama not responding - starting it..."
  if command -v ollama &>/dev/null; then
    nohup ollama serve &>/dev/null &amp;
  else
    echo "[bishad] ERROR: ollama not found in PATH"
    exit 1
  fi
  echo "[bishad] waiting for API..."
  for i in $(seq 1 30); do
    sleep 2
    if curl -sf "$OLLAMA_URL/api/tags" -o /dev/null; then
      echo "[bishad] Ollama is up."
      break
    fi
    if [ "$i" -eq 30 ]; then
      echo "[bishad] ERROR: Ollama did not start."
      exit 1
    fi
  done
else
  echo "[bishad] Ollama already running."
fi

echo "[bishad] starting server..."
python3 server.py &amp;
SERVER_PID=$!
sleep 1
echo "[bishad] opening browser..."
if command -v open &>/dev/null; then
  open "$SERVER_URL"
elif command -v xdg-open &>/dev/null; then
  xdg-open "$SERVER_URL"
fi
echo "[bishad] running (pid $SERVER_PID). Ctrl+C to stop."
wait $SERVER_PID
