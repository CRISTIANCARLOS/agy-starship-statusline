import sys
import json

def main():
    # Garante saída UTF-8 no Windows para suportar Nerd Fonts e símbolos ANSI
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw and raw.strip() else {}
    except Exception:
        data = {}

    # 1. Estado do Agente (IDLE, BUSY, THINK, TOOL)
    state = str(data.get("agent_state", "idle")).lower()
    state_presets = {
        "idle": (0, 77, "IDLE", "●"),         # Verde
        "working": (0, 214, "BUSY", "⚡"),     # Laranja/Amarelo
        "thinking": (15, 99, "THINK", "🧠"),   # Violeta
        "tool_use": (15, 33, "TOOL", "🔧"),   # Azul
    }
    s_fg, s_bg, s_lbl, s_icon = state_presets.get(state, (0, 248, state.upper(), "●"))

    # 2. Modelo LLM Ativo
    model_info = data.get("model", {})
    model_name = model_info.get("display_name", "Gemini")
    if len(model_name) > 25:
        model_name = model_name[:22] + "..."

    # 3. Janela de Contexto / Tokens
    cw = data.get("context_window", {})
    used_pct = cw.get("used_percentage", 0.0)

    if used_pct >= 80.0:
        c_bg, c_fg = 196, 15  # Vermelho (Atenção / Contexto quase cheio)
    elif used_pct >= 50.0:
        c_bg, c_fg = 214, 0   # Amarelo (Médio)
    else:
        c_bg, c_fg = 239, 15  # Cinza escuro elegante

    # 4. Git / VCS
    vcs = data.get("vcs", {})
    branch = vcs.get("branch", "")
    dirty = "*" if vcs.get("dirty") else ""

    # Helper para montar cápsulas no estilo Starship Pills: TEXTO
    def pill(fg, bg, content):
        return f"\033[38;5;{bg}m\ue0b6\033[38;5;{fg}m\033[48;5;{bg}m{content}\033[0m\033[38;5;{bg}m\ue0b4\033[0m"

    # Fallback caso a fonte/terminal não possua suporte a Nerd Fonts
    def simple_pill(fg, bg, content):
        return f"\033[38;5;{fg}m\033[48;5;{bg}m [{content}] \033[0m"

    try:
        segments = [
            pill(s_fg, s_bg, f"{s_icon} {s_lbl}"),
            pill(15, 25, f"󰚩 {model_name}"),
            pill(c_fg, c_bg, f"󰘚 {used_pct:.1f}%"),
        ]
        if branch:
            segments.append(pill(150, 237, f" {branch}{dirty}"))

        line = " ".join(segments)
        line.encode(sys.stdout.encoding or "utf-8")
        print(line, end="")
    except (UnicodeEncodeError, Exception):
        segments = [
            simple_pill(s_fg, s_bg, s_lbl),
            simple_pill(15, 25, model_name),
            simple_pill(c_fg, c_bg, f"ctx: {used_pct:.1f}%"),
        ]
        if branch:
            segments.append(simple_pill(150, 237, f"git:{branch}{dirty}"))
        print(" ".join(segments), end="")

if __name__ == "__main__":
    main()
