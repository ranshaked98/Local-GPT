#!/bin/bash
# ============================================================
# start.sh — Launches the Local GPT app + ngrok tunnel
# Usage:  bash start.sh
# ============================================================

NGROK="/opt/homebrew/bin/ngrok"
BACKEND_DIR="$(dirname "$0")/backend"

echo ""
echo "🚀 Starting Local GPT..."
echo ""

# 1. Start the FastAPI backend in the background
echo "▶ Starting backend on port 8000..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --reload --port 8000 &
UVICORN_PID=$!

# Wait a moment for the server to start
sleep 2

# 2. Start ngrok tunnel on port 8000
echo "▶ Opening ngrok tunnel..."
echo ""
echo "═══════════════════════════════════════════"
echo "  Your public URL will appear below ↓↓↓"
echo "  (look for 'Forwarding https://...')"
echo "═══════════════════════════════════════════"
echo ""
$NGROK http 8000

# When ngrok exits (Ctrl+C), kill uvicorn too
echo ""
echo "Stopping backend..."
kill $UVICORN_PID 2>/dev/null
echo "✅ All stopped."
