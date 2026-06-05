# ---------------------------------------------------------
# MetaSynk - Ferramenta Oficial HubSynk
# Versão: V.1.0
# Desenvolvido por: saulomgg (https://github.com/saulomgg)
#
# Este software faz parte do ecossistema HubSynk.
# Apoie o projeto, acesse meu portfólio e ajude a manter
# o desenvolvimento e atualizações constantes!
# ---------------------------------------------------------

import os
import webbrowser
from tkinter import filedialog, messagebox, Text, END, Toplevel, Label, Button, Frame
from tkinter import ttk
from src.utils.helpers import resource_path, COLORS, LINKS
from src.utils.video_processor import get_metadata, remove_all_metadata, insert_custom_metadata

class MetadataEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MetaSynk - Editor de Metadados de Vídeo")
        
        # Configurar ícone da janela e barra de tarefas
        self.set_window_icon()
            
        self.master.geometry("800x650")
        master.minsize(600, 450)
        master.configure(bg=COLORS["light_gray"])

        self.video_path = None
        self.setup_styles()
        self.create_widgets()

    def set_window_icon(self):
        """Configura o ícone da janela para aparecer na barra de tarefas e título"""
        try:
            icon_path = resource_path("assets/logo.png")
            
            if os.path.exists(icon_path):
                from tkinter import PhotoImage
                img = PhotoImage(file=icon_path)
                self.master.iconphoto(True, img)
            
            # Tentar ícone .ico para compatibilidade extra no Windows
            ico_path = resource_path("assets/logo.ico")
            if os.path.exists(ico_path):
                self.master.iconbitmap(ico_path)

            # Para Windows, garantir que o ícone apareça na barra de tarefas (AppUserModelID)
            if os.name == 'nt':
                import ctypes
                myappid = 'hubsynk.metasynk.metadata.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("TFrame", background=COLORS["light_gray"])
        self.style.configure("TLabel", background=COLORS["light_gray"], foreground=COLORS["text"])
        self.style.configure("TEntry", fieldbackground="white", foreground=COLORS["text"], borderwidth=1, relief="solid")
        
        self.style.configure("HubSynk.TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             background=COLORS["primary"], 
                             foreground="white", 
                             relief="flat",
                             padding=[10, 5])
        self.style.map("HubSynk.TButton", 
                       background=[("active", "#005ea6")],
                       foreground=[("active", "white")])
        
        self.style.configure("Support.TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             background="#FFC107", 
                             foreground="#1e1e1e", 
                             relief="flat",
                             padding=[10, 5])

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="15", style="TFrame")
        main_frame.pack(expand=True, fill="both")

        # Seção de seleção de arquivo
        file_frame = ttk.Frame(main_frame, style="TFrame")
        file_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(file_frame, text="Arquivo de Vídeo Selecionado:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.label_path = ttk.Label(file_frame, text="Nenhum arquivo selecionado", font=("Segoe UI", 10), wraplength=700, anchor="w")
        self.label_path.pack(fill="x", pady=(2, 5))

        btn_top_frame = ttk.Frame(file_frame, style="TFrame")
        btn_top_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_top_frame, text="ℹ️ Sobre", command=self.open_help, style="HubSynk.TButton").pack(side="right", padx=5)
        ttk.Button(btn_top_frame, text="🎁 Suporte", command=self.open_support, style="Support.TButton").pack(side="right", padx=5)
        ttk.Button(btn_top_frame, text="Selecionar Arquivo", command=self.select_video_file, style="HubSynk.TButton").pack(side="left")

        # Seção de botões de ação
        action_frame = ttk.Frame(main_frame, style="TFrame")
        action_frame.pack(fill="x", pady=10)
        
        for i in range(3): action_frame.columnconfigure(i, weight=1)

        ttk.Button(action_frame, text="Ler Metadados", command=self.read_metadata, style="HubSynk.TButton").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(action_frame, text="Remover Metadados", command=self.remove_metadata, style="HubSynk.TButton").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(action_frame, text="Inserir Metadados", command=self.open_insert_window, style="HubSynk.TButton").grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Seção de exibição
        display_frame = ttk.Frame(main_frame, style="TFrame")
        display_frame.pack(expand=True, fill="both", pady=(0, 10))

        ttk.Label(display_frame, text="Metadados do Arquivo:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Área de texto com scrollbar
        text_container = ttk.Frame(display_frame)
        text_container.pack(expand=True, fill="both", pady=(2, 0))
        
        self.metadata_text = Text(text_container, height=15, font=("Consolas", 9), wrap="word", relief="flat", borderwidth=0)
        self.metadata_text.pack(side="left", expand=True, fill="both")
        
        scrollbar = ttk.Scrollbar(text_container, command=self.metadata_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.metadata_text.config(yscrollcommand=scrollbar.set)

        # Rodapé
        footer_frame = ttk.Frame(self.master, style="TFrame")
        footer_frame.pack(side="bottom", fill="x", pady=(0, 15))
        
        inner_footer = ttk.Frame(footer_frame, style="TFrame")
        inner_footer.pack(expand=True)
        
        # Texto de créditos solicitado
        credits_label = Label(inner_footer, text="Desenvolvido por saulomgg", font=("Segoe UI", 9, "bold"), foreground=COLORS["text"], background=COLORS["light_gray"])
        credits_label.pack(side="left", padx=(0, 5))
        
        ttk.Label(inner_footer, text="|", font=("Segoe UI", 9), foreground=COLORS["dark_gray"], background=COLORS["light_gray"]).pack(side="left", padx=5)
        
        # Link Github
        github_label = Label(inner_footer, text="GitHub", font=("Segoe UI", 9, "bold", "underline"), foreground=COLORS["blue"], cursor="hand2", background=COLORS["light_gray"])
        github_label.pack(side="left", padx=(5, 0))
        github_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/saulomgg"))


    def open_help(self):
        about_win = Toplevel(self.master)
        about_win.title("Sobre MetaSynk - HubSynk")
        about_win.geometry("550x500")
        about_win.resizable(False, False)
        about_win.configure(bg="#1e1e1e")
        about_win.transient(self.master)
        about_win.grab_set()
        
        Label(about_win, text="🔷 HUBSYNK ECOSYSTEM", font=("Consolas", 14, "bold"), bg="#1e1e1e", fg="#2196F3").pack(pady=(20, 10))
        Label(about_win, text="MetaSynk v1.0", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        desc_text = (
            "Esta é uma ferramenta oficial do ecossistema HubSynk.\n\n"
            "O HubSynk foi criado para centralizar e automatizar tarefas "
            "do dia a dia, garantindo segurança e produtividade.\n\n"
            "O desenvolvimento e atualizações constantes dependem da "
            "interação da comunidade. Apoie o projeto!"
        )
        Label(about_win, text=desc_text, font=("Segoe UI", 10), bg="#1e1e1e", fg="#cccccc", wraplength=450, justify="center").pack(pady=15)
        
        links_frame = Frame(about_win, bg="#1e1e1e")
        links_frame.pack(pady=10)
        
        def create_link_btn(text, url, color="#2196F3"):
            btn = Button(links_frame, text=text, font=("Segoe UI", 10, "bold", "underline"), bg="#1e1e1e", fg=color,
                         activebackground="#1e1e1e", activeforeground="white", bd=0, cursor="hand2",
                         command=lambda: webbrowser.open_new(url))
            btn.pack(pady=3)

        create_link_btn("🔗 Link do HubSynk", "https://github.com/saulomgg/HubSynk")
        create_link_btn("🛠️ Link da Official-tools", "https://github.com/saulomgg/HubSynk/tree/main/official-tools")
        create_link_btn("📂 Link do GitHub / Portfólio", "https://github.com/saulomgg")
        
        Label(about_win, text="O desenvolvimento e atualização do programa depende da sua interação e apoio!", 
              font=("Segoe UI", 9, "italic"), bg="#1e1e1e", fg="#FFC107", wraplength=400).pack(pady=10)
        
        Button(about_win, text="Fechar", command=about_win.destroy, bg="#333333", fg="white", 
               relief="flat", padx=20, pady=5, cursor="hand2").pack(pady=15)

    def open_support(self):
        support_win = Toplevel(self.master)
        support_win.title("Suporte e Comunidade - HubSynk")
        support_win.geometry("550x450")
        support_win.resizable(False, False)
        support_win.configure(bg="#1e1e1e")
        support_win.transient(self.master)
        support_win.grab_set()
        
        Label(support_win, text="🚀 APOIE O PROJETO", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="#FFC107").pack(pady=20)
        
        msg = (
            "Você pode encontrar tudo na minha página do GitHub, incluindo outros programas e projetos!\n\n"
            "Para que o projeto continue crescendo, sua participação é fundamental:\n"
            "• Siga no GitHub para atualizações\n"
            "• Dê uma 'Star' nos repositórios que você usa\n"
            "• Considere fazer uma doação para manter o desenvolvimento\n"
            "• Entre nos nossos grupos da comunidade\n\n"
            "Com essa interação e comunidade, vamos desenvolvendo programas cada vez melhores!"
        )
        Label(support_win, text=msg, font=("Segoe UI", 11), bg="#1e1e1e", fg="white", wraplength=480, justify="left").pack(padx=30, pady=10)
        
        btn = Button(support_win, text="Ir para o GitHub / Portfólio", font=("Segoe UI", 12, "bold"), 
                     bg="#2196F3", fg="white", padx=20, pady=10, cursor="hand2",
                     command=lambda: webbrowser.open_new("https://github.com/saulomgg"))
        btn.pack(pady=20)
        
        Button(support_win, text="Voltar", command=support_win.destroy, bg="#333333", fg="white", 
               relief="flat", padx=15, pady=5, cursor="hand2").pack(pady=10)

    def select_video_file(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo de vídeo", 
                                             filetypes=[("Arquivos de Vídeo", "*.mp4;*.mkv;*.avi;*.mov;*.flv;*.webm")])
        if file_path:
            self.video_path = file_path
            self.label_path.config(text=f"Arquivo: {os.path.basename(file_path)}")
            self.read_metadata()

    def read_metadata(self):
        if not self.video_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return

        self.metadata_text.delete(1.0, END)
        try:
            probe = get_metadata(self.video_path)
            self.metadata_text.insert(END, f"Arquivo: {os.path.basename(self.video_path)}\n\n")
            
            if "format" in probe:
                self.metadata_text.insert(END, "--- Formato ---\n")
                for key, value in probe["format"].get("tags", {}).items():
                    self.metadata_text.insert(END, f"{key}: {value}\n")
                self.metadata_text.insert(END, "\n")

            if "streams" in probe:
                for i, stream in enumerate(probe["streams"]):
                    self.metadata_text.insert(END, f"--- Stream {i} ({stream.get('codec_type', 'unknown')}) ---\n")
                    for key, value in stream.get("tags", {}).items():
                        self.metadata_text.insert(END, f"  {key}: {value}\n")
                    self.metadata_text.insert(END, "\n")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remove_metadata(self):
        if not self.video_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", 
                                                 filetypes=[("Arquivos de Vídeo", "*.mp4;*.mkv;*.avi;*.mov;*.flv;*.webm")])
        if not output_path: return

        try:
            remove_all_metadata(self.video_path, output_path)
            messagebox.showinfo("Sucesso", "Metadados removidos com sucesso!")
            self.video_path = output_path
            self.label_path.config(text=f"Arquivo: {os.path.basename(output_path)}")
            self.read_metadata()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def open_insert_window(self):
        if not self.video_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return

        win = Toplevel(self.master)
        win.title("Inserir Metadados")
        win.geometry("500x350")
        win.transient(self.master)
        win.grab_set()
        win.configure(bg=COLORS["light_gray"])

        frame = ttk.Frame(win, padding="15", style="TFrame")
        frame.pack(expand=True, fill="both")

        fields = {"Título": "title", "Autor": "artist", "Ano": "date", "Gênero": "genre", "Comentários": "comment"}
        entries = {}

        for i, (label, tag) in enumerate(fields.items()):
            ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries[tag] = entry
        
        frame.grid_columnconfigure(1, weight=1)

        def apply():
            metadata = {tag: entry.get().strip() for tag, entry in entries.items() if entry.get().strip()}
            if not metadata:
                messagebox.showwarning("Aviso", "Nenhum dado preenchido.")
                return
            
            out = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Arquivos de Vídeo", "*.mp4")])
            if out:
                try:
                    insert_custom_metadata(self.video_path, out, metadata)
                    messagebox.showinfo("Sucesso", "Metadados inseridos!")
                    self.video_path = out
                    self.label_path.config(text=f"Arquivo: {os.path.basename(out)}")
                    self.read_metadata()
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

        ttk.Button(frame, text="Salvar Arquivo com Metadados", command=apply, style="HubSynk.TButton").grid(row=len(fields), columnspan=2, pady=20)
