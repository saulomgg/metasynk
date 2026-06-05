import os
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, compatível com desenvolvimento e PyInstaller."""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # No desenvolvimento, usa o diretório base do projeto (um nível acima de src)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)

# Configurações de Cores e Estilos (HubSynk UI)
COLORS = {
    "primary": "#0078D7",
    "secondary": "#f0f0f0",
    "text": "#333333",
    "light_gray": "#e0e0e0",
    "dark_gray": "#666666",
    "white": "#ffffff",
    "blue": "blue"
}

LINKS = {
    "github": "https://github.com/saulomgg"
}
