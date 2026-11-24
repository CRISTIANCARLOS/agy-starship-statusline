# agy-starship-statusline

Custom statusline for Google Antigravity CLI (`agy`) inspired by Starship prompt pills.

Displays real-time session telemetry directly in the terminal user interface:
- **Agent state:** IDLE (green), BUSY (orange), THINK (violet), TOOL (blue)
- **Active Model:** Display name of the active LLM (e.g. Gemini 3.8 Flash)
- **Context window usage:** Live percentage indicator with warning thresholds
- **VCS indicator:** Active git branch and dirty status

---

## Preview

```text
● IDLE 󰚩 Gemini 3.8 Flash (High) 󰘚 16.4%  main
```

*(Falls back automatically to standard brackets if the terminal font lacks Nerd Fonts)*

---

## Quick Installation

### Windows (PowerShell)

Run the following command in PowerShell:

```powershell
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/CRISTIANCARLOS/agy-starship-statusline/main/install.ps1" | Invoke-Expression
```

### Manual Setup

1. Copy `statusline.py` into `~/.gemini/antigravity-cli/statusline.py`.
2. Add the `statusLine` block to your `~/.gemini/antigravity-cli/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python C:\\Users\\<USER>\\.gemini\\antigravity-cli\\statusline.py"
  }
}
```

3. Or toggle directly inside the `agy` interactive chat:

```text
/statusline python ~/.gemini/antigravity-cli/statusline.py
```

---

## License

MIT
