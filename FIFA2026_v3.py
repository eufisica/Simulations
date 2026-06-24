import json
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

def gerar_estrutura_inicial():
    selecoes_grupos = {
        "Grupo A": ["México", "Coreia do Sul", "Chéquia", "África do Sul"],
        "Grupo B": ["Canadá", "Suíça", "Bósnia & Herzegovina", "Catar"],
        "Grupo C": ["Brasil", "Marrocos", "Escócia", "Haiti"],
        "Grupo D": ["EUA", "Austrália", "Paraguai", "Turquia"],
        "Grupo E": ["Alemanha", "Costa do Marfim", "Equador", "Curaçao"],
        "Grupo F": ["Países Baixos", "Japão", "Suécia", "Tunísia"],
        "Grupo G": ["Egito", "Irão", "Bélgica", "Nova Zelândia"],
        "Grupo H": ["Espanha", "Uruguai", "Cabo Verde", "Arábia Saudita"],
        "Grupo I": ["França", "Noruega", "Senegal", "Iraque"],
        "Grupo J": ["Argentina", "Áustria", "Argélia", "Jordânia"],
        "Grupo K": ["Colômbia", "Portugal", "Congo", "Uzbequistão"],
        "Grupo L": ["Inglaterra", "Gana", "Croácia", "Panamá"],
    }

    estrutura = {}
    for grupo, equipas in selecoes_grupos.items():
        e1, e2, e3, e4 = equipas
        estrutura[grupo] = [
            {"eq1": e1, "g1": "", "eq2": e2, "g2": ""},
            {"eq1": e3, "g1": "", "eq2": e4, "g2": ""},
            {"eq1": e1, "g1": "", "eq2": e3, "g2": ""},
            {"eq1": e4, "g1": "", "eq2": e2, "g2": ""},
            {"eq1": e4, "g1": "", "eq2": e1, "g2": ""},
            {"eq1": e2, "g1": "", "eq2": e3, "g2": ""}
        ]

    # Inicialização dos Dezasseis-avos com os placeholders oficiais do chaveamento
    estrutura["Dezasseis-avos (R32)"] = [
        {"eq1": "2º Grupo A", "g1": "", "eq2": "2º Grupo B", "g2": ""},  # Jogo 73
        {"eq1": "1º Grupo E", "g1": "", "eq2": "3º Grupo A", "g2": ""},  # Jogo 74
        {"eq1": "1º Grupo I", "g1": "", "eq2": "3º Grupo C", "g2": ""},  # Jogo 75
        {"eq1": "1º Grupo C", "g1": "", "eq2": "2º Grupo F", "g2": ""},  # Jogo 76
        {"eq1": "1º Grupo F", "g1": "", "eq2": "2º Grupo C", "g2": ""},  # Jogo 77
        {"eq1": "1º Grupo H", "g1": "", "eq2": "2º Grupo J", "g2": ""},  # Jogo 78
        {"eq1": "1º Grupo J", "g1": "", "eq2": "2º Grupo H", "g2": ""},  # Jogo 79
        {"eq1": "1º Grupo D", "g1": "", "eq2": "3º Grupo B", "g2": ""},  # Jogo 80
        {"eq1": "1º Grupo G", "g1": "", "eq2": "3º Grupo F", "g2": ""},  # Jogo 81
        {"eq1": "1º Grupo B", "g1": "", "eq2": "3º Grupo E", "g2": ""},  # Jogo 82
        {"eq1": "2º Grupo E", "g1": "", "eq2": "2º Grupo I", "g2": ""},  # Jogo 83
        {"eq1": "1º Grupo A", "g1": "", "eq2": "3º Grupo H", "g2": ""},  # Jogo 84
        {"eq1": "1º Grupo L", "g1": "", "eq2": "3º Grupo G", "g2": ""},  # Jogo 85
        {"eq1": "2º Grupo D", "g1": "", "eq2": "2º Grupo G", "g2": ""},  # Jogo 86
        {"eq1": "1º Grupo K", "g1": "", "eq2": "3º Grupo I", "g2": ""},  # Jogo 87
        {"eq1": "2º Grupo K", "g1": "", "eq2": "2º Grupo L", "g2": ""}   # Jogo 88
    ]
    
    estrutura["Oitavos-de-final"] = [{"eq1": f"Venc. Jogo {73+i*2}", "g1": "", "eq2": f"Venc. Jogo {74+i*2}", "g2": ""} for i in range(8)]
    estrutura["Quartos-de-final"] = [{"eq1": f"Venc. Oitavos {i*2+1}", "g1": "", "eq2": f"Venc. Oitavos {i*2+2}", "g2": ""} for i in range(4)]
    estrutura["Meias-finais"] = [{"eq1": "Venc. Quartos 1", "g1": "", "eq2": "Venc. Quartos 2", "g2": ""} for i in range(2)]
    estrutura["Terceiro Lugar"] = [{"eq1": "Derrotado Meias 1", "g1": "", "eq2": "Derrotado Meias 2", "g2": ""}]
    estrutura["FINAL"] = [{"eq1": "Venc. Meias 1", "g1": "", "eq2": "Venc. Meias 2", "g2": ""}]
            
    return estrutura

class SimuladorMundial:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Mundial FIFA 2026 - Chaveamento Oficial")
        self.root.geometry("950x750")
        self.root.configure(bg="#f4f4f4")
        
        self.caminho_ficheiro = "resultados_mundial_2026.json"
        self.dados = self.carregar_ficheiro_inicial()
        
        self.entries = {}
        self.tabelas_views = {}
        self.labels_equipas = {}
        
        self.frames_responsivos = {
            "Classificacoes": {}, "Fase de Grupos": {}, "Dezasseis-avos": {},
            "Oitavos": {}, "Quartos": {}, "Meias-Finais": {}, "Finais": {}
        }

        self.root.update_idletasks()
        self.setup_ui()

    def carregar_ficheiro_inicial(self):
        if os.path.exists(self.caminho_ficheiro):
            with open(self.caminho_ficheiro, "r", encoding="utf-8") as f:
                return json.load(f)
        return gerar_estrutura_inicial()

    def recolher_dados_da_interface(self):
        for fase, jogos in self.dados.items():
            if fase in self.entries:
                for i, jogo in enumerate(jogos):
                    g1 = self.entries[fase][i][0].get().strip()
                    g2 = self.entries[fase][i][1].get().strip()
                    jogo["g1"] = int(g1) if g1.isdigit() else ""
                    jogo["g2"] = int(g2) if g2.isdigit() else ""

    def atualizar_interface_com_dados(self):
        for fase, jogos in self.dados.items():
            if fase in self.entries:
                for i, jogo in enumerate(jogos):
                    self.entries[fase][i][0].delete(0, tk.END)
                    self.entries[fase][i][0].insert(0, str(jogo["g1"]))
                    self.entries[fase][i][1].delete(0, tk.END)
                    self.entries[fase][i][1].insert(0, str(jogo["g2"]))
        self.atualizar_fluxo_eliminatorias()

    def calcular_classificacoes(self):
        classificacao = {}
        grupos_lista = [f"Grupo {chr(i)}" for i in range(65, 77)]
        
        for nome_grupo in grupos_lista:
            if nome_grupo not in self.dados: continue
            classificacao[nome_grupo] = {}
            equipas = set()
            for jogo in self.dados[nome_grupo]:
                equipas.add(jogo["eq1"])
                equipas.add(jogo["eq2"])
            for eq in equipas:
                classificacao[nome_grupo][eq] = {"P": 0, "J": 0, "V": 0, "E": 0, "D": 0, "GM": 0, "GS": 0, "DG": 0}

            for jogo in self.dados[nome_grupo]:
                g1, g2 = jogo["g1"], jogo["g2"]
                if g1 != "" and g2 != "":
                    g1, g2 = int(g1), int(g2)
                    eq1, eq2 = jogo["eq1"], jogo["eq2"]
                    
                    classificacao[nome_grupo][eq1]["J"] += 1
                    classificacao[nome_grupo][eq2]["J"] += 1
                    classificacao[nome_grupo][eq1]["GM"] += g1
                    classificacao[nome_grupo][eq1]["GS"] += g2
                    classificacao[nome_grupo][eq2]["GM"] += g2
                    classificacao[nome_grupo][eq2]["GS"] += g1
                    
                    if g1 > g2:
                        classificacao[nome_grupo][eq1]["P"] += 3
                        classificacao[nome_grupo][eq1]["V"] += 1
                        classificacao[nome_grupo][eq2]["D"] += 1
                    elif g2 > g1:
                        classificacao[nome_grupo][eq2]["P"] += 3
                        classificacao[nome_grupo][eq2]["V"] += 1
                        classificacao[nome_grupo][eq1]["D"] += 1
                    else:
                        classificacao[nome_grupo][eq1]["P"] += 1
                        classificacao[nome_grupo][eq2]["P"] += 1
                        classificacao[nome_grupo][eq1]["E"] += 1
                        classificacao[nome_grupo][eq2]["E"] += 1
                    
                    classificacao[nome_grupo][eq1]["DG"] = classificacao[nome_grupo][eq1]["GM"] - classificacao[nome_grupo][eq1]["GS"]
                    classificacao[nome_grupo][eq2]["DG"] = classificacao[nome_grupo][eq2]["GM"] - classificacao[nome_grupo][eq2]["GS"]

        posicoes_grupos = {}
        for grupo, tree in self.tabelas_views.items():
            for item in tree.get_children():
                tree.delete(item)
            
            if grupo in classificacao:
                equipas_ordenadas = sorted(
                    classificacao[grupo].items(),
                    key=lambda x: (x[1]["P"], x[1]["DG"], x[1]["GM"]),
                    reverse=True
                )
                for rank, (equipa, stats) in enumerate(equipas_ordenadas, 1):
                    tree.insert("", "end", values=(rank, equipa, stats["P"], stats["J"], stats["V"], stats["E"], stats["D"], stats["DG"]))
                
                # Guarda as posições ordenadas (1º, 2º e 3º classificado de cada grupo)
                jogos_jogados = sum(1 for j in self.dados[grupo] if j["g1"] != "" and j["g2"] != "")
                if jogos_jogados > 0:
                    posicoes_grupos[grupo] = {
                        1: equipas_ordenadas[0][0],
                        2: equipas_ordenadas[1][0],
                        3: equipas_ordenadas[2][0]
                    }
                else:
                    posicoes_grupos[grupo] = {1: f"1º {grupo}", 2: f"2º {grupo}", 3: f"3º {grupo}"}
                    
        return posicoes_grupos

    def atualizar_fluxo_eliminatorias(self):
        """Passa os classificados dinamicamente através do chaveamento oficial fornecido."""
        posicoes = self.calcular_classificacoes()
        
        # Mapeamento Oficial Fornecido (Chaveamento FIFA 2026 - Jogos 73 a 88)
        # Formato: (Grupo_Equipa1, Posição_Equipa1, Grupo_Equipa2, Posição_Equipa2)
        chaveamento_oficial = [
            ("Grupo A", 2, "Grupo B", 2),  # Jogo 73 (Los Angeles)
            ("Grupo E", 1, "Grupo A", 3),  # Jogo 74 (Boston) -> 3º Buscado do Grp A
            ("Grupo I", 1, "Grupo C", 3),  # Jogo 75 (New York)  -> 3º Buscado do Grp C
            ("Grupo C", 1, "Grupo F", 2),  # Jogo 76 (Houston)
            ("Grupo F", 1, "Grupo C", 2),  # Jogo 77 (Monterrey)
            ("Grupo H", 1, "Grupo J", 2),  # Jogo 78 (Miami)
            ("Grupo J", 1, "Grupo H", 2),  # Jogo 79 (Dallas)
            ("Grupo D", 1, "Grupo B", 3),  # Jogo 80 (San Francisco) -> 3º Buscado do Grp B
            ("Grupo G", 1, "Grupo F", 3),  # Jogo 81 (Seattle) -> 3º Buscado do Grp F
            ("Grupo B", 1, "Grupo E", 3),  # Jogo 82 (Vancouver) -> 3º Buscado do Grp E
            ("Grupo E", 2, "Grupo I", 2),  # Jogo 83 (Toronto)
            ("Grupo A", 1, "Grupo H", 3),  # Jogo 84 (Cidade do México) -> 3º Buscado do Grp H
            ("Grupo L", 1, "Grupo G", 3),  # Jogo 85 (Filadélfia) -> 3º Buscado do Grp G
            ("Grupo D", 2, "Grupo G", 2),  # Jogo 86 (Kansas City)
            ("Grupo K", 1, "Grupo I", 3),  # Jogo 87 (Houston) -> 3º Buscado do Grp I
            ("Grupo K", 2, "Grupo L", 2)   # Jogo 88 (Atlanta)
        ]
        
        # Preenche os Dezasseis-avos buscando diretamente nas classificações
        for idx, (g1, pos1, g2, pos2) in enumerate(chaveamento_oficial):
            self.dados["Dezasseis-avos (R32)"][idx]["eq1"] = posicoes[g1][pos1]
            self.dados["Dezasseis-avos (R32)"][idx]["eq2"] = posicoes[g2][pos2]

        def obter_vencedor_e_derrotado(fase, idx_jogo, label_padrao):
            j = self.dados[fase][idx_jogo]
            if j["g1"] != "" and j["g2"] != "":
                if int(j["g1"]) > int(j["g2"]): return j["eq1"], j["eq2"]
                elif int(j["g2"]) > int(j["g1"]): return j["eq2"], j["eq1"]
                else: return f"{j['eq1']} (Pen)", f"{j['eq2']} (Derrotado)"
            return f"Venc. Jogo {label_padrao}", f"Derr. Jogo {label_padrao}"

        # Atualizar Oitavos baseando-se no chaveamento sequencial da esquerda e direita
        # Oitavos 1: Venc J73 x Venc J74, Oitavos 2: Venc J75 x Venc J76, etc.
        for i in range(8):
            v1, _ = obter_vencedor_e_derrotado("Dezasseis-avos (R32)", i * 2, f"{73 + i * 2}")
            v2, _ = obter_vencedor_e_derrotado("Dezasseis-avos (R32)", i * 2 + 1, f"{74 + i * 2}")
            self.dados["Oitavos-de-final"][i]["eq1"] = v1
            self.dados["Oitavos-de-final"][i]["eq2"] = v2

        # Atualizar Quartos
        for i in range(4):
            v1, _ = obter_vencedor_e_derrotado("Oitavos-de-final", i * 2, f"Oit.{i*2+1}")
            v2, _ = obter_vencedor_e_derrotado("Oitavos-de-final", i * 2 + 1, f"Oit.{i*2+2}")
            self.dados["Quartos-de-final"][i]["eq1"] = v1
            self.dados["Quartos-de-final"][i]["eq2"] = v2

        # Atualizar Meias
        for i in range(2):
            v1, _ = obter_vencedor_e_derrotado("Quartos-de-final", i * 2, f"Q.{i*2+1}")
            v2, _ = obter_vencedor_e_derrotado("Quartos-de-final", i * 2 + 1, f"Q.{i*2+2}")
            self.dados["Meias-finais"][i]["eq1"] = v1
            self.dados["Meias-finais"][i]["eq2"] = v2

        # Final e 3º Lugar
        v1, d1 = obter_vencedor_e_derrotado("Meias-finais", 0, "Meia 1")
        v2, d2 = obter_vencedor_e_derrotado("Meias-finais", 1, "Meia 2")
        self.dados["Terceiro Lugar"][0]["eq1"] = d1
        self.dados["Terceiro Lugar"][0]["eq2"] = d2
        self.dados["FINAL"][0]["eq1"] = v1
        self.dados["FINAL"][0]["eq2"] = v2

        # Atualização visual imediata das Labels de texto nas abas
        for fase, jogos in self.dados.items():
            if fase in self.labels_equipas:
                for i, jogo in enumerate(jogos):
                    self.labels_equipas[fase][i][0].config(text=jogo["eq1"])
                    self.labels_equipas[fase][i][1].config(text=jogo["eq2"])

    def gravar_e_calcular(self):
        self.recolher_dados_da_interface()
        self.atualizar_fluxo_eliminatorias()
        with open(self.caminho_ficheiro, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Sucesso", "Resultados calculados e eliminatórias atualizadas!")

    def guardar_como(self):
        self.recolher_dados_da_interface()
        self.atualizar_fluxo_eliminatorias()
        ficheiro_escolhido = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Ficheiros JSON", "*.json")])
        if ficheiro_escolhido:
            self.caminho_ficheiro = ficheiro_escolhido
            with open(self.caminho_ficheiro, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=4)
            self.lbl_status.config(text=f"Ficheiro Atual: {os.path.basename(self.caminho_ficheiro)}")

    def abrir_ficheiro(self):
        ficheiro_escolhido = filedialog.askopenfilename(filetypes=[("Ficheiros JSON", "*.json")])
        if ficheiro_escolhido:
            self.caminho_ficheiro = ficheiro_escolhido
            with open(self.caminho_ficheiro, "r", encoding="utf-8") as f:
                self.dados = json.load(f)
            self.atualizar_interface_com_dados()
            self.lbl_status.config(text=f"Ficheiro Atual: {os.path.basename(self.caminho_ficheiro)}")

    def ajustar_todos_os_grids(self, event=None):
        largura_janela = self.notebook.winfo_width()
        if largura_janela <= 1: largura_janela = self.root.winfo_width()
        largura_quadro = 425
        num_colunas = max(1, largura_janela // largura_quadro)

        for chave_aba, dicionario_frames in self.frames_responsivos.items():
            for idx, (nome, frame) in enumerate(dicionario_frames.items()):
                frame.grid_forget()
                frame.grid(row=idx // num_colunas, column=idx % num_colunas, padx=8, pady=8, sticky="nsew")

    def criar_aba_scroll(self, notebook, titulo):
        aba = tk.Frame(notebook, bg="#f4f4f4")
        notebook.add(aba, text=titulo)
        canvas = tk.Canvas(aba, bg="#f4f4f4", highlightthickness=0)
        scrollbar = ttk.Scrollbar(aba, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f4f4f4")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        return scroll_frame, scroll_frame

    def setup_ui(self):
        tk.Label(self.root, text="MUNDIAL FIFA 2026 - SIMULADOR TOTAL", font=("Segoe UI", 15, "bold"), bg="#f4f4f4", fg="#1e3d59").pack(pady=2)
        self.lbl_status = tk.Label(self.root, text=f"Ficheiro Atual: {os.path.basename(self.caminho_ficheiro)}", font=("Segoe UI", 9, "italic"), bg="#f4f4f4", fg="#555")
        self.lbl_status.pack()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        self.notebook.bind("<Configure>", self.ajustar_todos_os_grids)

        # Aba Classificações
        aba_class = tk.Frame(self.notebook, bg="#f4f4f4")
        self.notebook.add(aba_class, text="📊 Classificações")
        canvas_class = tk.Canvas(aba_class, bg="#f4f4f4", highlightthickness=0)
        scroll_class = ttk.Scrollbar(aba_class, orient="vertical", command=canvas_class.yview)
        frame_tabelas = tk.Frame(canvas_class, bg="#f4f4f4")
        frame_tabelas.bind("<Configure>", lambda e: canvas_class.configure(scrollregion=canvas_class.bbox("all")))
        canvas_class.create_window((0, 0), window=frame_tabelas, anchor="nw")
        canvas_class.configure(yscrollcommand=scroll_class.set)
        canvas_class.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scroll_class.pack(side="right", fill="y")

        grupos_lista = [f"Grupo {chr(i)}" for i in range(65, 77)]
        colunas = ("#", "Equipa", "P", "J", "V", "E", "D", "DG")
        for grupo in grupos_lista:
            lf = tk.LabelFrame(frame_tabelas, text=grupo, font=("Segoe UI", 10, "bold"), bg="white", fg="#1e3d59")
            self.frames_responsivos["Classificacoes"][grupo] = lf
            tree = ttk.Treeview(lf, columns=colunas, show="headings", height=4)
            tree.pack(fill="x", padx=5, pady=5)
            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=28 if col != "Equipa" else 135, anchor="center" if col != "Equipa" else "w")
            self.tabelas_views[grupo] = tree

        # Identificação dos locais nos títulos dos quadros de mata-mata
        locais_r32 = [
            "Jogo 73 (Los Angeles)", "Jogo 74 (Boston)", "Jogo 75 (Nova Iorque)", "Jogo 76 (Houston)",
            "Jogo 77 (Monterrey)", "Jogo 78 (Miami)", "Jogo 79 (Dallas)", "Jogo 80 (São Francisco)",
            "Jogo 81 (Seattle)", "Jogo 82 (Vancouver)", "Jogo 83 (Toronto)", "Jogo 84 (C. México)",
            "Jogo 85 (Filadélfia)", "Jogo 86 (Kansas City)", "Jogo 87 (Houston)", "Jogo 88 (Atlanta)"
        ]

        fases_mapeamento = [
            ("Fase de Grupos", "Fase de Grupos", grupos_lista, None),
            ("Dezasseis-avos", "Dezasseis-avos", ["Dezasseis-avos (R32)"], locais_r32),
            ("Oitavos", "Oitavos", ["Oitavos-de-final"], [f"Oitavos {i+1}" for i in range(8)]),
            ("Quartos", "Quartos", ["Quartos-de-final"], [f"Quartos {i+1}" for i in range(4)]),
            ("Meias-Finais", "Meias-Finais", ["Meias-finais"], ["Meia-Final 1", "Meia-Final 2"]),
            ("Finais", "Finais", ["Terceiro Lugar", "FINAL"], ["3º Lugar", "Grande Final"])
        ]

        for titulo_aba, chave_responsiva, chaves_fases, labels_custom in fases_mapeamento:
            _, frame_alvo = self.criar_aba_scroll(self.notebook, titulo_aba)
            
            for fase in chaves_fases:
                if fase not in self.dados: continue
                self.entries[fase] = []
                self.labels_equipas[fase] = []
                
                # Se for uma aba com múltiplos blocos (ex: Grupos), cria blocos individuais
                # Se for eliminatória, divide cada jogo no seu próprio LabelFrame Responsivo!
                for i, jogo in enumerate(self.dados[fase]):
                    titulo_quadro = labels_custom[i] if labels_custom else fase
                    
                    lf_fase = tk.LabelFrame(frame_alvo, text=f" {titulo_quadro} ", font=("Segoe UI", 10, "bold"), bg="white", fg="#ff6e40", bd=2)
                    self.frames_responsivos[chave_responsiva][f"{fase}_{i}"] = lf_fase
                    
                    row = tk.Frame(lf_fase, bg="white")
                    row.pack(fill="x", pady=8, padx=8)
                    
                    lbl_e1 = tk.Label(row, text=jogo["eq1"], width=18, anchor="e", bg="white", font=("Segoe UI", 9))
                    lbl_e1.pack(side="left", padx=2)
                    
                    e1 = tk.Entry(row, width=3, justify="center", font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
                    e1.insert(0, str(jogo["g1"]))
                    e1.pack(side="left")
                    
                    tk.Label(row, text="x", bg="white", font=("Segoe UI", 9, "bold"), fg="#777").pack(side="left", padx=5)
                    
                    e2 = tk.Entry(row, width=3, justify="center", font=("Segoe UI", 9, "bold"), bd=1, relief="solid")
                    e2.insert(0, str(jogo["g2"]))
                    e2.pack(side="left")
                    
                    lbl_e2 = tk.Label(row, text=jogo["eq2"], width=18, anchor="w", bg="white", font=("Segoe UI", 9))
                    lbl_e2.pack(side="left", padx=2)
                    
                    self.entries[fase].append((e1, e2))
                    self.labels_equipas[fase].append((lbl_e1, lbl_e2))

        self.atualizar_fluxo_eliminatorias()

        # --- Botões ---
        button_frame = tk.Frame(self.root, bg="#f4f4f4")
        button_frame.pack(side="bottom", fill="x", pady=10)
        center_btns = tk.Frame(button_frame, bg="#f4f4f4")
        center_btns.pack(anchor="center")

        tk.Button(center_btns, text="⚙️ CALCULAR & ATUALIZAR", command=self.gravar_e_calcular, bg="#ff6e40", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6, relief="flat", cursor="hand2").pack(side="left", padx=10)
        tk.Button(center_btns, text="💾 GUARDAR COMO...", command=self.guardar_como, bg="#1e3d59", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6, relief="flat", cursor="hand2").pack(side="left", padx=10)
        tk.Button(center_btns, text="📂 ABRIR...", command=self.abrir_ficheiro, bg="#17b978", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6, relief="flat", cursor="hand2").pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMundial(root)
    root.mainloop()