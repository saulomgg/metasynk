# ---------------------------------------------------------
# MetaSynk - Ferramenta Oficial HubSynk
# Versão: V.1.0
# Desenvolvido por: saulomgg (https://github.com/saulomgg)
#
# Este software faz parte do ecossistema HubSynk.
# Apoie o projeto, acesse meu portfólio e ajude a manter
# o desenvolvimento e atualizações constantes!
# ---------------------------------------------------------

import sys
from tkinter import Tk
from src.ui.main_window import MetadataEditorApp

def main():
    try:
        root = Tk()
        app = MetadataEditorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro crítico ao iniciar a aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
