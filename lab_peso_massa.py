"""
Simulação: Razão entre Força (Peso) e Massa — EUFISICA simulations
Laboratório Virtual de Física | Dinamometria e Análise Gráfica
Desenvolvido em Python com Tkinter e Matplotlib
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- CONSTANTES E DADOS DOS ASTROS ---
ASTROS = {
    'terra': {
        'name': 'Terra',
        'g': 9.81,
        'bg': '#0284c7',
        'ground': '#15803d',
        'detail': 'Superfície Terrestre',
        'color': '#0284c7'
    },
    'lua': {
        'name': 'Lua',
        'g': 1.62,
        'bg': '#0f172a',
        'ground': '#64748b',
        'detail': 'Superfície Lunar',
        'color': '#64748b'
    },
    'marte': {
        'name': 'Marte',
        'g': 3.71,
        'bg': '#9a3412',
        'ground': '#ea580c',
        'detail': 'Superfície Marciana',
        'color': '#ea580c'
    },
    'jupiter': {
        'name': 'Júpiter',
        'g': 24.79,
        'bg': '#7c2d12',
        'ground': '#451a03',
        'detail': 'Atmosfera de Júpiter',
        'color': '#b45309'
    }
}


class EufisicaSimApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Simulação: Razão entre Força e Massa — EUFISICA")
        self.geometry("1200x850")
        self.minsize(1000, 700)

        # Estado da Aplicação
        self.astro_key = 'terra'
        self.mass = 10.0
        self.records = []  # Registo de medições da tabela

        # Configuração dos Estilos
        self.setup_styles()

        # Content Container Principal
        self.main_container = ttk.Frame(self, padding=15)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Construir Interface
        self.create_header()
        self.create_student_bar()
        self.create_simulation_area()
        self.create_worksheet_area()

        # Inicializar Simulação e Gráfico
        self.update_sim()
        self.render_table()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.bg_color = '#f8fafc'
        self.card_bg = '#ffffff'

        self.configure(bg=self.bg_color)
        self.style.configure('.', background=self.bg_color, font=('Segoe UI', 9))
        self.style.configure('TFrame', background=self.bg_color)

        # Títulos e Badges
        self.style.configure('HeaderTitle.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#0f172a', background=self.card_bg)
        self.style.configure('HeaderSub.TLabel', font=('Segoe UI', 9), foreground='#475569', background=self.card_bg)
        self.style.configure('Badge.TLabel', font=('Segoe UI', 8, 'bold'), foreground='#2563eb', background='#eff6ff', padding=(8, 4))

        # Botões
        self.style.configure('Action.TButton', font=('Segoe UI', 9, 'bold'), background='#2563eb', foreground='#ffffff')
        self.style.map('Action.TButton', background=[('active', '#1d4ed8')])

        self.style.configure('Secondary.TButton', font=('Segoe UI', 9, 'bold'), background='#f1f5f9', foreground='#0f172a')
        self.style.map('Secondary.TButton', background=[('active', '#e2e8f0')])

        self.style.configure('Danger.TButton', font=('Segoe UI', 8, 'bold'), background='#fef2f2', foreground='#ef4444')
        self.style.map('Danger.TButton', background=[('active', '#ef4444')], foreground=[('active', '#ffffff')])

        # Separadores / Tabs
        self.style.configure('TNotebook', background=self.bg_color, tabmargins=[2, 5, 2, 0])
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 9, 'bold'), padding=[12, 6], background='#e2e8f0', foreground='#475569')
        self.style.map('TNotebook.Tab', background=[('selected', '#2563eb')], foreground=[('selected', '#ffffff')])

    def create_header(self):
        header_frame = tk.Frame(self.main_container, bg=self.card_bg, highlightbackground='#e2e8f0', highlightthickness=1, padx=15, pady=10)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Logo EUFISICA no Canvas
        logo_canvas = tk.Canvas(header_frame, width=45, height=45, bg=self.card_bg, highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
        logo_canvas.create_oval(3, 3, 42, 42, outline='#2563eb', width=2, fill='#eff6ff')
        logo_canvas.create_line(15, 22, 20, 15, 28, 30, 32, 22, fill='#2563eb', width=3, capstyle=tk.ROUND, joinstyle=tk.ROUND)
        logo_canvas.create_oval(32, 20, 38, 26, fill='#f59e0b', outline='')
        logo_canvas.create_oval(8, 20, 14, 26, fill='#2563eb', outline='')

        title_frame = tk.Frame(header_frame, bg=self.card_bg)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(title_frame, text="Simulação: Razão entre Força (Peso) e Massa", style='HeaderTitle.TLabel').pack(anchor='w')
        ttk.Label(title_frame, text="EUFISICA simulations • Laboratório Virtual de Física | Dinamometria e Análise Gráfica", style='HeaderSub.TLabel').pack(anchor='w')

        badge = ttk.Label(header_frame, text="Mecânica & Gravitação", style='Badge.TLabel')
        badge.pack(side=tk.RIGHT)

    def create_student_bar(self):
        bar_frame = tk.Frame(self.main_container, bg=self.card_bg, highlightbackground='#e2e8f0', highlightthickness=1, padx=15, pady=10)
        bar_frame.pack(fill=tk.X, pady=(0, 15))

        f1 = tk.Frame(bar_frame, bg=self.card_bg)
        f1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(f1, text="NOME DO ALUNO", font=('Segoe UI', 7, 'bold'), fg='#475569', bg=self.card_bg).pack(anchor='w')
        self.entry_name = ttk.Entry(f1)
        self.entry_name.pack(fill=tk.X, pady=(2, 0))

        f2 = tk.Frame(bar_frame, bg=self.card_bg)
        f2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(f2, text="NÚMERO", font=('Segoe UI', 7, 'bold'), fg='#475569', bg=self.card_bg).pack(anchor='w')
        self.entry_num = ttk.Entry(f2)
        self.entry_num.pack(fill=tk.X, pady=(2, 0))

        f3 = tk.Frame(bar_frame, bg=self.card_bg)
        f3.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(f3, text="TURMA", font=('Segoe UI', 7, 'bold'), fg='#475569', bg=self.card_bg).pack(anchor='w')
        self.entry_class = ttk.Entry(f3)
        self.entry_class.pack(fill=tk.X, pady=(2, 0))

    def create_simulation_area(self):
        grid_frame = tk.Frame(self.main_container, bg=self.bg_color)
        grid_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))

        # --- CONTROLO DA EXPERIÊNCIA (ESQUERDA) ---
        ctrl_card = tk.Frame(grid_frame, bg=self.card_bg, highlightbackground='#e2e8f0', highlightthickness=1, padx=15, pady=15, width=320)
        ctrl_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        ctrl_card.pack_propagate(False)

        tk.Label(ctrl_card, text="Controlo da Experiência", font=('Segoe UI', 11, 'bold'), fg='#0f172a', bg=self.card_bg).pack(anchor='w')
        tk.Label(ctrl_card, text="Medição Direta no Dinamómetro", font=('Segoe UI', 8), fg='#475569', bg=self.card_bg).pack(anchor='w', pady=(0, 15))
        ttk.Separator(ctrl_card, orient='horizontal').pack(fill=tk.X, pady=(0, 15))

        # Seleção do Astro
        tk.Label(ctrl_card, text="Astro / Localização", font=('Segoe UI', 9, 'bold'), fg='#0f172a', bg=self.card_bg).pack(anchor='w')
        self.combo_astro = ttk.Combobox(ctrl_card, state='readonly', values=[
            "Terra (g ≈ 9.81 N/kg)",
            "Lua (g ≈ 1.62 N/kg)",
            "Marte (g ≈ 3.71 N/kg)",
            "Júpiter (g ≈ 24.79 N/kg)"
        ])
        self.combo_astro.current(0)
        self.combo_astro.pack(fill=tk.X, pady=(4, 15))
        self.combo_astro.bind("<<ComboboxSelected>>", self.on_astro_change)

        # Controlo de Massa
        mass_hdr = tk.Frame(ctrl_card, bg=self.card_bg)
        mass_hdr.pack(fill=tk.X)
        tk.Label(mass_hdr, text="Massa do Corpo (m)", font=('Segoe UI', 9, 'bold'), fg='#0f172a', bg=self.card_bg).pack(side=tk.LEFT)
        self.lbl_mass_val = tk.Label(mass_hdr, text="10.0 kg", font=('Consolas', 10, 'bold'), fg='#2563eb', bg=self.card_bg)
        self.lbl_mass_val.pack(side=tk.RIGHT)

        self.scale_mass = ttk.Scale(ctrl_card, from_=1.0, to=100.0, value=10.0, command=self.on_mass_change)
        self.scale_mass.pack(fill=tk.X, pady=(6, 20))

        btn_add = ttk.Button(ctrl_card, text="➕ Registar Medição na Tabela", style='Action.TButton', command=self.add_record)
        btn_add.pack(fill=tk.X, pady=(10, 0))

        # --- CANVAS E MÉTRICAS (DIREITA) ---
        sim_card = tk.Frame(grid_frame, bg=self.card_bg, highlightbackground='#e2e8f0', highlightthickness=1, padx=15, pady=15)
        sim_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sim_title_frame = tk.Frame(sim_card, bg=self.card_bg)
        sim_title_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(sim_title_frame, text="Dinamómetro e Medição da Força", font=('Segoe UI', 11, 'bold'), fg='#0f172a', bg=self.card_bg).pack(side=tk.LEFT)
        self.lbl_planet_tag = ttk.Label(sim_title_frame, text="Superfície Terrestre", style='Badge.TLabel')
        self.lbl_planet_tag.pack(side=tk.RIGHT)

        self.sim_canvas = tk.Canvas(sim_card, height=280, bg='#000000', highlightthickness=0)
        self.sim_canvas.pack(fill=tk.BOTH, expand=True)

        # Cartões de Métricas
        metrics_frame = tk.Frame(sim_card, bg=self.card_bg)
        metrics_frame.pack(fill=tk.X, pady=(10, 0))

        m1 = tk.Frame(metrics_frame, bg='#f8fafc', highlightbackground='#e2e8f0', highlightthickness=1, padx=10, pady=8)
        m1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)
        tk.Label(m1, text="VALOR DA FORÇA / PESO (P)", font=('Segoe UI', 7, 'bold'), fg='#475569', bg='#f8fafc').pack()
        self.lbl_m_weight = tk.Label(m1, text="98.1 N", font=('Consolas', 12, 'bold'), fg='#2563eb', bg='#f8fafc')
        self.lbl_m_weight.pack()

        m2 = tk.Frame(metrics_frame, bg='#f8fafc', highlightbackground='#e2e8f0', highlightthickness=1, padx=10, pady=8)
        m2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)
        tk.Label(m2, text="VALOR DA MASSA (m)", font=('Segoe UI', 7, 'bold'), fg='#475569', bg='#f8fafc').pack()
        self.lbl_m_mass = tk.Label(m2, text="10.0 kg", font=('Consolas', 12, 'bold'), fg='#0f172a', bg='#f8fafc')
        self.lbl_m_mass.pack()

        m3 = tk.Frame(metrics_frame, bg='#f8fafc', highlightbackground='#e2e8f0', highlightthickness=1, padx=10, pady=8)
        m3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)
        tk.Label(m3, text="RAZÃO (P / m)", font=('Segoe UI', 7, 'bold'), fg='#475569', bg='#f8fafc').pack()
        self.lbl_m_ratio = tk.Label(m3, text="9.81 N/kg", font=('Consolas', 12, 'bold'), fg='#10b981', bg='#f8fafc')
        self.lbl_m_ratio.pack()

    def create_worksheet_area(self):
        ws_frame = tk.Frame(self.main_container, bg=self.card_bg, highlightbackground='#e2e8f0', highlightthickness=1, padx=10, pady=10)
        ws_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(ws_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Protocolo
        self.tab_protocol = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_protocol, text="📋 Enquadramento Teórico")
        self.build_tab_protocol()

        # Tab 2: Tabela de Dados
        self.tab_data = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_data, text="📊 Tabela de Dados")
        self.build_tab_data()

        # Tab 3: Gráfico
        self.tab_graph = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_graph, text="📈 Gráfico F = f(m)")
        self.build_tab_graph()

        # Tab 4: Questões
        self.tab_questions = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_questions, text="✍️ Questões do Relatório")
        self.build_tab_questions()

        # Rodapé
        footer = tk.Frame(ws_frame, bg=self.card_bg)
        footer.pack(fill=tk.X, pady=(10, 0))
        btn_export = ttk.Button(footer, text="💾 Exportar Relatório de Laboratório (.txt)", style='Secondary.TButton', command=self.export_report)
        btn_export.pack(side=tk.RIGHT)

    def build_tab_protocol(self):
        tk.Label(self.tab_protocol, text="Proporcionalidade Direta entre Força Gravítica (Peso) e Massa", font=('Segoe UI', 11, 'bold'), fg='#2563eb', bg=self.bg_color).pack(anchor='w', pady=(0, 10))

        b1 = tk.Frame(self.tab_protocol, bg='#ffffff', highlightbackground='#2563eb', highlightthickness=1, padx=12, pady=10)
        b1.pack(fill=tk.X, pady=(0, 10))
        tk.Label(b1, text="1. Relação entre Força Peso e Massa", font=('Segoe UI', 9, 'bold'), fg='#2563eb', bg='#ffffff').pack(anchor='w')
        t1 = ("A Força Gravítica (Peso, P ou F) que atua num determinado corpo é diretamente proporcional à sua massa (m).\n"
              "A constante de proporcionalidade representa a intensidade do campo gravítico local (g):\n\n"
              "P = m · g    ⇒    Razão = P / m = g")
        tk.Label(b1, text=t1, font=('Segoe UI', 9), fg='#0f172a', bg='#ffffff', justify=tk.LEFT).pack(anchor='w', pady=(4, 0))

        b2 = tk.Frame(self.tab_protocol, bg='#ffffff', highlightbackground='#2563eb', highlightthickness=1, padx=12, pady=10)
        b2.pack(fill=tk.X)
        tk.Label(b2, text="2. Interpretação Gráfica de F = f(m)", font=('Segoe UI', 9, 'bold'), fg='#2563eb', bg='#ffffff').pack(anchor='w')
        t2 = ("Ao representar graficamente a Força (F ou P) em função da Massa (m), obtém-se uma reta que passa pela origem.\n"
              "O declive dessa reta corresponde ao valor numérico da aceleração da gravidade local (g).")
        tk.Label(b2, text=t2, font=('Segoe UI', 9), fg='#0f172a', bg='#ffffff', justify=tk.LEFT).pack(anchor='w', pady=(4, 0))

    def build_tab_data(self):
        top_bar = tk.Frame(self.tab_data, bg=self.bg_color)
        top_bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(top_bar, text="Tabela de Registo de Medições", font=('Segoe UI', 10, 'bold'), fg='#2563eb', bg=self.bg_color).pack(side=tk.LEFT)

        btn_clear = ttk.Button(top_bar, text="🗑️ Limpar Tudo", style='Danger.TButton', command=self.clear_all_records)
        btn_clear.pack(side=tk.RIGHT, padx=4)

        btn_add = ttk.Button(top_bar, text="+ Adicionar Medição Atual", style='Secondary.TButton', command=self.add_record)
        btn_add.pack(side=tk.RIGHT, padx=4)

        columns = ('ensaio', 'astro', 'peso', 'massa', 'razao')
        self.tree = ttk.Treeview(self.tab_data, columns=columns, show='headings', height=8)

        self.tree.heading('ensaio', text='Ensaio')
        self.tree.heading('astro', text='Astro')
        self.tree.heading('peso', text='Força / Peso P (N)')
        self.tree.heading('massa', text='Massa m (kg)')
        self.tree.heading('razao', text='Razão P/m (N/kg)')

        self.tree.column('ensaio', width=60, anchor='center')
        self.tree.column('astro', width=120, anchor='center')
        self.tree.column('peso', width=150, anchor='center')
        self.tree.column('massa', width=150, anchor='center')
        self.tree.column('razao', width=150, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_del = ttk.Button(self.tab_data, text="❌ Eliminar Registo Selecionado", style='Danger.TButton', command=self.delete_selected_record)
        btn_del.pack(anchor='e', pady=(8, 0))

    def build_tab_graph(self):
        tk.Label(self.tab_graph, text="Gráfico da Força Gravítica (F) em função da Massa (m)", font=('Segoe UI', 10, 'bold'), fg='#2563eb', bg=self.bg_color).pack(anchor='w')
        tk.Label(self.tab_graph, text="Os pontos representam os registos na tabela. As linhas tracejadas representam o comportamento teórico de cada astro.", font=('Segoe UI', 8), fg='#475569', bg=self.bg_color).pack(anchor='w', pady=(0, 10))

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def build_tab_questions(self):
        q_frame = tk.Frame(self.tab_questions, bg=self.bg_color)
        q_frame.pack(fill=tk.BOTH, expand=True)

        q1_title = "1. Observa o gráfico da Força (F) em função da Massa (m). Que tipo de linha descreve a relação entre estas duas grandezas?"
        tk.Label(q_frame, text=q1_title, font=('Segoe UI', 9, 'bold'), fg='#0f172a', bg=self.bg_color, wraplength=900, justify=tk.LEFT).pack(anchor='w', pady=(5, 2))
        self.txt_q1 = tk.Text(q_frame, height=3, font=('Segoe UI', 9), bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=1)
        self.txt_q1.pack(fill=tk.X, pady=(0, 10))

        q2_title = "2. Relaciona a inclinação (declive) das retas no gráfico com a intensidade do campo gravítico (g) dos astros. Qual apresenta maior declive?"
        tk.Label(q_frame, text=q2_title, font=('Segoe UI', 9, 'bold'), fg='#0f172a', bg=self.bg_color, wraplength=900, justify=tk.LEFT).pack(anchor='w', pady=(5, 2))
        self.txt_q2 = tk.Text(q_frame, height=3, font=('Segoe UI', 9), bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=1)
        self.txt_q2.pack(fill=tk.X, pady=(0, 10))

        q3_title = "3. Com base nos dados da tabela, calcula a razão P / m para três massas diferentes no mesmo astro. O valor da razão altera-se?"
        tk.Label(q_frame, text=q3_title, font=('Segoe UI', 9, 'bold'), fg='#0f172a', bg=self.bg_color, wraplength=900, justify=tk.LEFT).pack(anchor='w', pady=(5, 2))
        self.txt_q3 = tk.Text(q_frame, height=3, font=('Segoe UI', 9), bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=1)
        self.txt_q3.pack(fill=tk.X, pady=(0, 5))

    # --- ATUALIZAÇÕES ---

    def on_astro_change(self, event=None):
        idx = self.combo_astro.current()
        keys = ['terra', 'lua', 'marte', 'jupiter']
        self.astro_key = keys[idx]
        self.lbl_planet_tag.config(text=ASTROS[self.astro_key]['detail'])
        self.update_sim()

    def on_mass_change(self, val):
        self.mass = float(val)
        self.lbl_mass_val.config(text=f"{self.mass:.1f} kg")
        self.update_sim()

    def update_sim(self):
        astro = ASTROS[self.astro_key]
        weight = self.mass * astro['g']
        ratio = weight / self.mass

        self.lbl_m_mass.config(text=f"{self.mass:.1f} kg")
        self.lbl_m_weight.config(text=f"{weight:.1f} N")
        self.lbl_m_ratio.config(text=f"{ratio:.2f} N/kg")

        self.render_sim_canvas(astro, weight)

    def render_sim_canvas(self, astro, weight):
        c = self.sim_canvas
        c.delete('all')

        w = c.winfo_width()
        h = c.winfo_height()

        if w <= 1:
            w, h = 750, 280

        c.create_rectangle(0, 0, w, h, fill=astro['bg'], outline='')

        if self.astro_key == 'lua':
            for i in range(25):
                sx = (i * 37) % w
                sy = (i * 19) % (h - 40)
                c.create_rectangle(sx, sy, sx + 2, sy + 2, fill='#ffffff', outline='')

        ground_y = h - 35
        c.create_rectangle(0, ground_y, w, h, fill=astro['ground'], outline='')
        c.create_line(0, ground_y, w, ground_y, fill='#ffffff', width=2)

        cx = w / 2
        c.create_rectangle(cx - 80, 10, cx + 80, 24, fill='#334155', outline='')
        c.create_rectangle(cx - 10, 24, cx + 10, 40, fill='#475569', outline='')

        dyn_top = 40
        spring_len = min(110, 35 + (weight / 2500) * 75)
        dyn_bottom = dyn_top + spring_len

        turns = 10
        seg_h = spring_len / turns
        points = [(cx, dyn_top)]
        for i in range(turns):
            dx = 12 if (i % 2 == 0) else -12
            points.append((cx + dx, dyn_top + (i + 0.5) * seg_h))
        points.append((cx, dyn_bottom))

        for i in range(len(points) - 1):
            c.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill='#cbd5e1', width=3)

        mass_y = dyn_bottom + 25
        c.create_line(cx, dyn_bottom, cx, mass_y - 18, fill='#94a3b8', width=3)

        box_size = min(60, 32 + self.mass * 0.3)
        c.create_rectangle(cx - box_size / 2, mass_y - box_size / 2, cx + box_size / 2, mass_y + box_size / 2, fill='#3b82f6', outline='#1d4ed8', width=2)

        c.create_text(cx, mass_y, text=f"{self.mass:.1f} kg", fill='#ffffff', font=('Consolas', 9, 'bold'))

        arrow_start = mass_y + box_size / 2
        arrow_len = min(65, 20 + (weight / 2500) * 45)
        arrow_end = arrow_start + arrow_len

        c.create_line(cx, arrow_start, cx, arrow_end, fill='#f59e0b', width=4)
        c.create_polygon(cx - 7, arrow_end - 2, cx + 7, arrow_end - 2, cx, arrow_end + 7, fill='#f59e0b', outline='')

        c.create_text(cx + 15, arrow_start + arrow_len / 2, text=f"P = {weight:.1f} N", fill='#ffffff', font=('Segoe UI', 9, 'bold'), anchor='w')

        # Mostrador Digital
        c.create_rectangle(20, 20, 210, 105, fill='#0f172a', outline='#334155', width=1)
        c.create_text(30, 35, text="Mostrador Dinamómetro", fill='#38bdf8', font=('Segoe UI', 9, 'bold'), anchor='w')
        c.create_text(30, 55, text=f"Astro: {astro['name']}", fill='#ffffff', font=('Segoe UI', 8), anchor='w')
        c.create_text(30, 72, text=f"Massa (m): {self.mass:.1f} kg", fill='#ffffff', font=('Segoe UI', 8), anchor='w')
        c.create_text(30, 90, text=f"Força (P): {weight:.1f} N", fill='#f59e0b', font=('Consolas', 9, 'bold'), anchor='w')

    def add_record(self):
        astro = ASTROS[self.astro_key]
        weight = self.mass * astro['g']
        ratio = weight / self.mass

        self.records.append({
            'astro_key': self.astro_key,
            'astro_name': astro['name'],
            'weight': weight,
            'mass': self.mass,
            'ratio': ratio,
            'color': astro['color']
        })

        self.render_table()

    def render_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, rec in enumerate(self.records, 1):
            self.tree.insert('', 'end', values=(
                i,
                rec['astro_name'],
                f"{rec['weight']:.1f}",
                f"{rec['mass']:.1f}",
                f"{rec['ratio']:.2f}"
            ))

        self.render_graph()

    def delete_selected_record(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected[0])
        self.records.pop(idx)
        self.render_table()

    def clear_all_records(self):
        if self.records and messagebox.askyesno("Confirmar", "Desejas limpar todos os registos da tabela?"):
            self.records = []
            self.render_table()

    def render_graph(self):
        self.ax.clear()

        max_m = 100.0
        for k, a in ASTROS.items():
            m_vals = [0, max_m]
            f_vals = [0, max_m * a['g']]
            self.ax.plot(m_vals, f_vals, linestyle='--', color=a['color'], alpha=0.7, label=f"{a['name']} (g≈{a['g']} N/kg)")

        for rec in self.records:
            self.ax.scatter(rec['mass'], rec['weight'], color=rec['color'], edgecolors='black', s=50, zorder=5)

        self.ax.set_title("Força Gravítica P (N) em função da Massa m (kg)", fontsize=10, fontweight='bold', color='#0f172a')
        self.ax.set_xlabel("Massa m (kg)", fontsize=9)
        self.ax.set_ylabel("Força Gravítica P (N)", fontsize=9)
        self.ax.set_xlim(0, 105)
        self.ax.set_ylim(0, 2600)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.legend(loc='upper left', fontsize=8)

        self.fig.tight_layout()
        self.graph_canvas.draw()

    def export_report(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Ficheiro de Texto", "*.txt"), ("Todos os Ficheiros", "*.*")],
            title="Guardar Relatório de Laboratório"
        )
        if not filename:
            return

        name = self.entry_name.get() or "Não especificado"
        num = self.entry_num.get() or "N/A"
        turma = self.entry_class.get() or "N/A"

        q1_ans = self.txt_q1.get("1.0", tk.END).strip()
        q2_ans = self.txt_q2.get("1.0", tk.END).strip()
        q3_ans = self.txt_q3.get("1.0", tk.END).strip()

        report_str = f"""====================================================================
RELATÓRIO DE LABORATÓRIO VIRTUAL DE FÍSICA
Simulação: Razão entre Força (Peso) e Massa — EUFISICA simulations
====================================================================

IDENTIFICAÇÃO DO ALUNO:
Nome: {name}
Número: {num}
Turma: {turma}

--------------------------------------------------------------------
TABELA DE REGISTO DE MEDIÇÕES:
--------------------------------------------------------------------
Ensaio | Astro      | Força P (N) | Massa m (kg) | Razão P/m (N/kg)
--------------------------------------------------------------------
"""
        for i, r in enumerate(self.records, 1):
            report_str += f"{i:<7} | {r['astro_name']:<10} | {r['weight']:<11.1f} | {r['mass']:<12.1f} | {r['ratio']:.2f}\n"

        report_str += f"""--------------------------------------------------------------------

RESPOSTAS ÀS QUESTÕES DO RELATÓRIO:

1. Relação entre Força (F) e Massa (m) no gráfico:
{q1_ans if q1_ans else '[Sem resposta]'}

2. Relação entre a inclinação da reta e a gravidade (g) do astro:
{q2_ans if q2_ans else '[Sem resposta]'}

3. Constância da razão P/m e conclusões:
{q3_ans if q3_ans else '[Sem resposta]'}

====================================================================
Gerado por EUFISICA simulations • Laboratório Virtual de Física
====================================================================
"""

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_str)
            messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao guardar o ficheiro: {e}")


if __name__ == "__main__":
    app = EufisicaSimApp()
    app.mainloop()