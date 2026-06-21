import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulacaoPlanoInclinado:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação: Plano Inclinado - José Gonçalves (eufisica)")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f4f4f9")

        # Constantes Físicas
        self.g = 9.81
        self.scale_time = 0.05

        # Parâmetros fixos do plano geométrico no Canvas
        self.x_base_esquerda = 100
        self.x_base_direita = 500
        self.y_base = 350
        self.comprimento_base = self.x_base_direita - self.x_base_esquerda

        # Estado da simulação (Valores Iniciais)
        self.h = 150.0
        self.m = 5.0
        self.mu = 0.0
        
        self.bloco_pos_plano = 0.0
        self.velocidade = 0.0
        self.tempo = 0.0
        self.em_execucao = False

        # Listas de dados para gráficos
        self.dados_tempo = []
        self.dados_ec = []
        self.dados_ep = []
        self.dados_etotal = []
        self.dados_pos = []
        self.dados_vel = []

        self.atualizar_constantes_geometricas()
        self.configurar_interface()
        self.desenhar_cenario()
        
        # Iniciar o Loop Principal de Animação
        self.loop()

    def atualizar_constantes_geometricas(self):
        self.alpha = np.arctan(self.h / self.comprimento_base)
        self.comprimento_plano = np.sqrt(self.comprimento_base**2 + self.h**2)

    def configurar_interface(self):
        # Frame Principal Organizador
        main_frame = tk.Frame(self.root, bg="#f4f4f9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- LADO ESQUERDO: Canvas + Controlos ---
        left_frame = tk.Frame(main_frame, bg="#f4f4f9")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas de Desenho
        self.canvas = tk.Canvas(left_frame, width=600, height=400, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

        # Painel de Controlo
        control_panel = tk.LabelFrame(left_frame, text="Controlos", font=("Arial", 11, "bold"), bg="white", padx=15, pady=15)
        control_panel.pack(fill=tk.X, padx=5)

        # Sliders e Inputs
        self.val_h_label = tk.Label(control_panel, text=f"Altura (h): {self.h} m", bg="white", anchor="w")
        self.val_h_label.pack(fill=tk.X)
        self.slider_h = ttk.Scale(control_panel, from_=50, to=300, value=self.h, command=self.on_slider_change)
        self.slider_h.pack(fill=tk.X, pady=(0, 10))

        self.val_m_label = tk.Label(control_panel, text=f"Massa (m): {self.m} kg", bg="white", anchor="w")
        self.val_m_label.pack(fill=tk.X)
        self.slider_m = ttk.Scale(control_panel, from_=1, to=20, value=self.m, command=self.on_slider_change)
        self.slider_m.pack(fill=tk.X, pady=(0, 10))

        self.val_mu_label = tk.Label(control_panel, text=f"Coef. Atrito (μ): {self.mu:.2f}", bg="white", anchor="w")
        self.val_mu_label.pack(fill=tk.X)
        self.slider_mu = ttk.Scale(control_panel, from_=0, to=1, value=self.mu, command=self.on_slider_change)
        self.slider_mu.pack(fill=tk.X, pady=(0, 10))

        # Botões
        btn_frame = tk.Frame(control_panel, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)

        btn_start = tk.Button(btn_frame, text="Iniciar", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), command=self.start_sim)
        btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        btn_pause = tk.Button(btn_frame, text="Pausar", bg="#ffc107", fg="#333", font=("Arial", 10, "bold"), command=self.pause_sim)
        btn_pause.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        btn_reset = tk.Button(btn_frame, text="Reiniciar", bg="#dc3545", fg="white", font=("Arial", 10, "bold"), command=self.reset_sim)
        btn_reset.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.label_alpha = tk.Label(control_panel, text=f"Ângulo (α): {np.degrees(self.alpha):.1f}°", bg="white", font=("Arial", 10, "bold"), anchor="w")
        self.label_alpha.pack(fill=tk.X, pady=5)

        # --- LADO DIREITO: Gráficos Matplotlib ---
        right_frame = tk.Frame(main_frame, bg="#f4f4f9")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.fig, (self.ax_eng, self.ax_cin) = plt.subplots(2, 1, figsize=(5, 7))
        self.fig.tight_layout(pad=3.0)

        # Gráfico de Energia Configurações Prévias
        self.ax_eng.set_title("Energia (J) vs Tempo")
        self.ax_eng.set_xlabel("Tempo (s)")
        self.ax_eng.grid(True)
        
        # Gráfico de Cinemática Configurações Prévias
        self.ax_cin.set_title("Cinemática vs Tempo")
        self.ax_cin.set_xlabel("Tempo (s)")
        self.ax_cin_vel = self.ax_cin.twinx() # Eixo Y duplo
        self.ax_cin.grid(True)

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_slider_change(self, event=None):
        self.h = round(self.slider_h.get())
        self.m = round(self.slider_m.get(), 1)
        self.mu = round(self.slider_mu.get(), 2)

        self.val_h_label.config(text=f"Altura (h): {self.h} px")
        self.val_m_label.config(text=f"Massa (m): {self.m} kg")
        self.val_mu_label.config(text=f"Coef. Atrito (μ): {self.mu:.2f}")

        self.atualizar_constantes_geometricas()
        self.label_alpha.config(text=f"Ângulo (α): {np.degrees(self.alpha):.1f}°")

        if not self.em_execucao and self.bloco_pos_plano == 0:
            self.desenhar_cenario()

    def start_sim(self):
        self.em_execucao = True

    def pause_sim(self):
        self.em_execucao = False

    def reset_sim(self):
        self.em_execucao = False
        self.bloco_pos_plano = 0.0
        self.velocidade = 0.0
        self.tempo = 0.0
        self.dados_tempo.clear()
        self.dados_ec.clear()
        self.dados_ep.clear()
        self.dados_etotal.clear()
        self.dados_pos.clear()
        self.dados_vel.clear()
        self.atualizar_graficos()
        self.desenhar_cenario()

    def desenhar_vetor(self, x1, y1, dx, dy, legenda, cor):
        if abs(dx) < 2 and abs(dy) < 2:
            return
        # O Canvas do Tkinter usa coordenadas invertidas no eixo Y global, mas a rotação local já trata isso
        self.canvas.create_line(x1, y1, x1 + dx, y1 + dy, fill=cor, width=2, arrow=tk.LAST)
        self.canvas.create_text(x1 + dx + 10 * np.sign(dx if dx != 0 else 1), y1 + dy + 10 * np.sign(dy if dy != 0 else 1), text=legenda, fill="black", font=("Arial", 9, "bold"))

    def desenhar_cenario(self):
        self.canvas.delete("all")

        x_topo = self.x_base_esquerda
        y_topo = self.y_base - self.h

        # Desenhar Solo
        self.canvas.create_line(50, self.y_base, 550, self.y_base, fill="#333", width=2)

        # Desenhar Plano Inclinado
        self.canvas.create_polygon(self.x_base_esquerda, self.y_base, x_topo, y_topo, self.x_base_direita, self.y_base, fill="#e0e0e0", outline="black")

        # Arco do Ângulo alfa (fictício simplificado por uma linha)
        self.canvas.create_arc(self.x_base_direita - 40, self.y_base - 40, self.x_base_direita + 40, self.y_base + 40, start=180, extent=np.degrees(self.alpha), style=tk.ARC, outline="black")

        # Posição do bloco
        proporcao = self.bloco_pos_plano / self.comprimento_plano
        x_bloco_centro = x_topo + proporcao * (self.x_base_direita - x_topo)
        y_bloco_centro = y_topo + proporcao * (self.y_base - y_topo)

        # Desenhar Bloco com Rotação (Aproximação por polígono rotacionado manualmente)
        tam_bloco = 40
        cos_a = np.cos(self.alpha)
        sin_a = np.sin(self.alpha)

        # Coordenadas locais do quadrado (-w/2, -h) até (w/2, 0)
        pts_locais = [
            (-tam_bloco/2, 0),
            (tam_bloco/2, 0),
            (tam_bloco/2, -tam_bloco),
            (-tam_bloco/2, -tam_bloco)
        ]
        
        # Rotacionar e transladar pontos para o referencial global do Canvas
        pts_globais = []
        for px, py in pts_locais:
            gx = x_bloco_centro + (px * cos_a - py * sin_a)
            gy = y_bloco_centro + (px * sin_a + py * cos_a)
            pts_globais.extend([gx, gy])

        self.canvas.create_polygon(pts_globais, fill="#8B4513", outline="black")

        # Centro de Massa (Origem dos vetores no referencial global)
        cm_local_x = 0
        cm_local_y = -tam_bloco/2
        cm_g_x = x_bloco_centro + (cm_local_x * cos_a - cm_local_y * sin_a)
        cm_g_y = y_bloco_centro + (cm_local_x * sin_a + cm_local_y * cos_a)

        self.canvas.create_oval(cm_g_x - 3, cm_g_y - 3, cm_g_x + 3, cm_g_y + 3, fill="red")

        # --- VETORES DE FORÇA ---
        escala_forca = 5.0 / self.m
        P = self.m * self.g
        
        # Força Peso Real (Vertical pura para baixo)
        self.desenhar_vetor(cm_g_x, cm_g_y, 0, P * escala_forca, "P", "blue")

        # Para desenhar os vetores Px, Py, N, Fa que acompanham a inclinação:
        # Px (Ao longo do plano, sentido descendente)
        px_dx = (P * np.sin(self.alpha) * escala_forca) * cos_a
        px_dy = (P * np.sin(self.alpha) * escala_forca) * sin_a
        self.desenhar_vetor(cm_g_x, cm_g_y, px_dx, px_dy, "Px", "cyan")

        # Py (Perpendicular ao plano, para dentro do plano)
        py_dx = -(P * np.cos(self.alpha) * escala_forca) * sin_a
        py_dy = (P * np.cos(self.alpha) * escala_forca) * cos_a
        self.desenhar_vetor(cm_g_x, cm_g_y, py_dx, py_dy, "Py", "purple")

        # Força Normal (Oposta à Py)
        self.desenhar_vetor(cm_g_x, cm_g_y, -py_dx, -py_dy, "N", "green")

        # Força de Atrito (Oposta à Px)
        Fa = self.mu * (P * np.cos(self.alpha))
        if Fa > 0:
            fa_dx = -(Fa * escala_forca) * cos_a
            fa_dy = -(Fa * escala_forca) * sin_a
            self.desenhar_vetor(cm_g_x, cm_g_y, fa_dx, fa_dy, "Fa", "orange")

    def atualizar_fisica(self):
        if not self.em_execucao:
            return

        Px = self.m * self.g * np.sin(self.alpha)
        Py = self.m * self.g * np.cos(self.alpha)
        N = Py
        Fa = self.mu * N

        forca_resultante = Px - Fa

        if forca_resultante <= 0 and self.velocidade == 0:
            forca_resultante = 0
            self.em_execucao = False

        aceleracao = forca_resultante / self.m

        # Integração Numérica (Euler)
        self.velocidade += aceleracao * self.scale_time * 60
        self.bloco_pos_plano += self.velocidade * self.scale_time
        self.tempo += self.scale_time

        # Métricas Físicas Fictícias (Baseadas em conversão de píxeis para Metros: 100px = 1m)
        altura_real_restante = (1 - (self.bloco_pos_plano / self.comprimento_plano)) * self.h / 100.0
        Ep = self.m * self.g * max(0.0, altura_real_restante)
        Ec = 0.5 * self.m * (self.velocidade / 100.0) ** 2
        Etotal = Ep + Ec

        # Armazenar dados
        self.dados_tempo.append(self.tempo)
        self.dados_ec.append(Ec)
        self.dados_ep.append(Ep)
        self.dados_etotal.append(Etotal)
        self.dados_pos.append(self.bloco_pos_plano)
        self.dados_vel.append(self.velocidade)

        # Limitar dados para manter a fluidez
        if len(self.dados_tempo) > 100:
            self.dados_tempo.pop(0)
            self.dados_ec.pop(0)
            self.dados_ep.pop(0)
            self.dados_etotal.pop(0)
            self.dados_pos.pop(0)
            self.dados_vel.pop(0)

        self.atualizar_graficos()

        # Fim de Curso do Plano
        if self.bloco_pos_plano >= self.comprimento_plano:
            self.bloco_pos_plano = self.comprimento_plano
            self.velocidade = 0.0
            self.em_execucao = False

    def atualizar_graficos(self):
        # Limpar eixos para Redesenho rápido
        self.ax_eng.clear()
        self.ax_cin.clear()
        self.ax_cin_vel.clear()

        # Títulos e Grids de volta
        self.ax_eng.set_title("Energia (J) vs Tempo")
        self.ax_eng.set_xlabel("Tempo (s)")
        self.ax_eng.grid(True)
        
        self.ax_cin.set_title("Cinemática vs Tempo")
        self.ax_cin.set_xlabel("Tempo (s)")
        self.ax_cin.grid(True)

        if self.dados_tempo:
            # Plot Energias
            self.ax_eng.plot(self.dados_tempo, self.dados_ec, color="red", label="E. Cinética (Ec)")
            self.ax_eng.plot(self.dados_tempo, self.dados_ep, color="blue", label="E. Potencial (Ep)")
            self.ax_eng.plot(self.dados_tempo, self.dados_etotal, color="green", linestyle="--", label="E. Total")
            self.ax_eng.legend(loc="upper right")

            # Plot Cinemática (Eixo Duplo)
            self.ax_cin.plot(self.dados_tempo, self.dados_pos, color="purple", label="Posição (m)")
            self.ax_cin_vel.plot(self.dados_tempo, self.dados_vel, color="orange", label="Velocidade (m/s)")
            
            # Legendas combinadas
            self.ax_cin.set_ylabel("Posição", color="purple")
            self.ax_cin_vel.set_ylabel("Velocidade", color="orange")

        self.plot_canvas.draw_idle()

    def loop(self):
        self.atualizar_physics() # Processamento matemático
        self.desenhar_cenario()  # Renderização do Canvas
        # Força o tkinter a repetir o método a cada ~16ms (equivalente a 60 FPS)
        self.root.after(16, self.loop)

    def atualizar_physics(self):
        # Wrapper auxiliar para evitar conflito de nomenclatura com o loop do Tkinter
        self.atualizar_fisica()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacaoPlanoInclinado(root)
    root.mainloop()