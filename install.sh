#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="$HOME/.gemini/antigravity-cli"
mkdir -p "$TARGET_DIR"

DEST_SCRIPT="$TARGET_DIR/statusline.py"
SCRIPT_URL="https://raw.githubusercontent.com/CRISTIANCARLOS/agy-starship-statusline/main/statusline.py"

echo "Downloading statusline.py..."
curl -fsSL "$SCRIPT_URL" -o "$DEST_SCRIPT"

SETTINGS_FILE="$TARGET_DIR/settings.json"
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "{}" > "$SETTINGS_FILE"
fi

if command -v jq >/dev/null 2>&1; then
    TMP_JSON=$(mktemp)
    jq --arg cmd "python3 $DEST_SCRIPT" '.statusLine = {"type": "command", "command": $cmd}' "$SETTINGS_FILE" > "$TMP_JSON"
    mv "$TMP_JSON" "$SETTINGS_FILE"
fi

echo "agy-starship-statusline installed successfully!"
