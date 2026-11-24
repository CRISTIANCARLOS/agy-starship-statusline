import sys
import json

def shorten_model(name: str) -> str:
    """Encurta o nome do modelo para uma etiqueta minimalista."""
    if not name:
        return "gemini"
    low = name.lower()
    if "3.8 flash" in low:
        return "3.8-flash"
    if "3.8 pro" in low:
        return "3.8-pro"
    if "1.5 flash" in low:
        return "1.5-flash"
    if "1.5 pro" in low:
        return "1.5-pro"
    if "flash" in low:
        return "flash"
    if "pro" in low:
        return "pro"
    parts = name.split()
    return parts[0].lower() if parts else "gemini"

def main():
    # Garante saída UTF-8 no Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw and raw.strip() else {}
    except Exception:
        data = {}

    # 1. Estado do Agente (compacto em minúsculas)
    state = str(data.get("agent_state", "idle")).lower()
    state_presets = {
        "idle": (0, 77, "idle", "●"),         # Verde
        "working": (0, 214, "busy", "⚡"),     # Laranja/Amarelo
        "thinking": (15, 99, "think", "🧠"),   # Violeta
        "tool_use": (15, 33, "tool", "🔧"),   # Azul
    }
    s_fg, s_bg, s_lbl, s_icon = state_presets.get(state, (0, 248, state, "●"))

    # 2. Modelo LLM Ativo (enxuto)
    model_info = data.get("model", {})
    model_name = shorten_model(model_info.get("display_name", ""))

    # 3. Cota da Conta (apenas porcentagem limpa)
    quota_info = data.get("quota", {})
    lowest_remaining = None
    if isinstance(quota_info, dict):
        for _, bucket in quota_info.items():
            if isinstance(bucket, dict) and "remaining_fraction" in bucket:
                rem = bucket["remaining_fraction"]
                if lowest_remaining is None or rem < lowest_remaining:
                    lowest_remaining = rem

    if lowest_remaining is not None:
        rem_pct = lowest_remaining * 100.0
        if rem_pct >= 50.0:
            q_bg, q_fg = 28, 15   # Verde
        elif rem_pct >= 20.0:
            q_bg, q_fg = 214, 0   # Amarelo
        else:
            q_bg, q_fg = 196, 15  # Vermelho

    # 4. Contexto da Conversa (apenas porcentagem inteira limpa)
    cw = data.get("context_window", {})
    used_pct = cw.get("used_percentage", 0.0)

    if used_pct >= 80.0:
        c_bg, c_fg = 196, 15  # Vermelho
    elif used_pct >= 50.0:
        c_bg, c_fg = 214, 0   # Amarelo
    else:
        c_bg, c_fg = 239, 15  # Cinza escuro

    # 5. VCS / Git
    vcs = data.get("vcs", {})
    branch = vcs.get("branch", "")
    dirty = "*" if vcs.get("dirty") else ""

    # Helper para montar cápsulas Starship compactas: TEXTO
    def pill(fg, bg, content):
        return f"\033[38;5;{bg}m\ue0b6\033[38;5;{fg}m\033[48;5;{bg}m{content}\033[0m\033[38;5;{bg}m\ue0b4\033[0m"

    # Fallback seguro para fontes sem glifos
    def simple_pill(fg, bg, content):
        return f"\033[38;5;{fg}m\033[48;5;{bg}m[{content}]\033[0m"

    try:
        segments = [
            pill(s_fg, s_bg, f"{s_icon} {s_lbl}"),
            pill(15, 25, f"󰚩 {model_name}"),
        ]
        if lowest_remaining is not None:
            segments.append(pill(q_fg, q_bg, f"󰆏 {rem_pct:.0f}%"))

        segments.append(pill(c_fg, c_bg, f"󰘚 {used_pct:.0f}%"))

        if branch:
            segments.append(pill(150, 237, f" {branch}{dirty}"))

        line = " ".join(segments)
        line.encode(sys.stdout.encoding or "utf-8")
        print(line, end="")
    except (UnicodeEncodeError, Exception):
        segments = [
            simple_pill(s_fg, s_bg, s_lbl),
            simple_pill(15, 25, model_name),
        ]
        if lowest_remaining is not None:
            segments.append(simple_pill(q_fg, q_bg, f"{rem_pct:.0f}%"))

        segments.append(simple_pill(c_fg, c_bg, f"{used_pct:.0f}%"))

        if branch:
            segments.append(simple_pill(150, 237, f"{branch}{dirty}"))
        print(" ".join(segments), end="")

if __name__ == "__main__":
    main()
