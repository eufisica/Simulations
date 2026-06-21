import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class VerticalLaunchSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Lançamento Vertical - José Gonçalves (eufisica)")
        self.root.geometry("1250x750")
        self.root.minimum_size = (900, 600)
        
        # Configuração do Layout Redimensionável da Janela
        self.root.columnconfigure(0, weight=1) 
        self.root.columnconfigure(1, weight=1) 
        self.root.rowconfigure(0, weight=1)    
        
        # --- PAINEL ESQUERDO (Animação + Controlos) ---
        left_panel = ttk.Frame(self.root, padding=10)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.rowconfigure(0, weight=3) 
        left_panel.rowconfigure(1, weight=1) 
        left_panel.columnconfigure(0, weight=1)
        
        self.anim_canvas = tk.Canvas(left_panel, bg="#bae6fd", highlightthickness=2, highlightbackground="#cbd5e1")
        self.anim_canvas.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.anim_canvas.bind("<Configure>", lambda e: self.desenhar_bola_estatica())
        
        ctrl_frame = ttk.LabelFrame(left_panel, text=" Parâmetros de Lançamento ", padding=10)
        ctrl_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(3): ctrl_frame.columnconfigure(i, weight=1)
        
        # Controlos (Sliders)
        ttk.Label(ctrl_frame, text="Astro/Gravidade:").grid(row=0, column=0, sticky="w", padx=5)
        self.grav_opts = {"Terra (9.81 m/s²)": 9.81, "Lua (1.62 m/s²)": 1.62, "Marte (3.71 m/s²)": 3.71, "Júpiter (24.79 m/s²)": 24.79}
        self.grav_var = tk.StringVar(value="Terra (9.81 m/s²)")
        self.grav_combo = ttk.Combobox(ctrl_frame, textvariable=self.grav_var, values=list(self.grav_opts.keys()), state="readonly")
        self.grav_combo.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        
        ttk.Label(ctrl_frame, text="Massa da Esfera:").grid(row=0, column=1, sticky="w", padx=5)
        self.massa_scale = ttk.Scale(ctrl_frame, from_=0.1, to=10.0, value=1.0, command=lambda e: self.lbl_massa.config(text=f"{float(e):.1f} kg"))
        self.massa_scale.grid(row=1, column=1, sticky="ew", padx=5)
        self.lbl_massa = ttk.Label(ctrl_frame, text="1.0 kg")
        self.lbl_massa.grid(row=2, column=1)

        ttk.Label(ctrl_frame, text="Velocidade Inicial:").grid(row=0, column=2, sticky="w", padx=5)
        self.v0_scale = ttk.Scale(ctrl_frame, from_=-30, to=30, value=20, command=lambda e: self.lbl_v0.config(text=f"{float(e):.1f} m/s"))
        self.v0_scale.grid(row=1, column=2, sticky="ew", padx=5)
        self.lbl_v0 = ttk.Label(ctrl_frame, text="20.0 m/s")
        self.lbl_v0.grid(row=2, column=2)

        ttk.Label(ctrl_frame, text="Altura Inicial:").grid(row=3, column=0, sticky="w", padx=5)
        self.y0_scale = ttk.Scale(ctrl_frame, from_=0, to=200, value=0, command=lambda e: self.lbl_y0.config(text=f"{float(e):.1f} m"))
        self.y0_scale.grid(row=4, column=0, sticky="ew", padx=5)
        self.lbl_y0 = ttk.Label(ctrl_frame, text="0.0 m")
        self.lbl_y0.grid(row=5, column=0)

        ttk.Label(ctrl_frame, text="Resistência do Ar (k):").grid(row=3, column=1, sticky="w", padx=5)
        self.k_scale = ttk.Scale(ctrl_frame, from_=0.0, to=2.0, value=0.0, command=lambda e: self.lbl_k.config(text=f"{float(e):.2f}"))
        self.k_scale.grid(row=4, column=1, sticky="ew", padx=5)
        self.lbl_k = ttk.Label(ctrl_frame, text="0.00")
        self.lbl_k.grid(row=5, column=1)
        
        self.btn_launch = ttk.Button(ctrl_frame, text="Lançar / Reiniciar", command=self.start_simulation)
        self.btn_launch.grid(row=4, column=2, rowspan=2, sticky="nsew", padx=5, pady=5)

        # --- PAINEL DIREITO (Gráficos Dinâmicos) ---
        right_panel = ttk.Frame(self.root, padding=10)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1) 
        right_panel.rowconfigure(1, weight=1) 
        
        # Ajustamos o tamanho da figura (figsize) e adicionamos margens automáticas para os eixos não cortarem
        self.fig, (self.ax_pos, self.ax_vel) = plt.subplots(2, 1, figsize=(5, 6))
        self.fig.set_tight_layout(True) # Garante que os números dos eixos aparecem sempre
        
        self.canvas_plots = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas_plots.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.animation_running = False
        self.reset_plots()

    def reset_plots(self):
        # Limpeza e estilização básica inicial dos eixos
        self.ax_pos.clear()
        self.ax_pos.set_title("Posição (y) vs Tempo (t)", fontsize=10, fontweight='bold')
        self.ax_pos.set_ylabel("Altura (m)")
        self.ax_pos.grid(True, linestyle="--", alpha=0.6)
        self.line_pos, = self.ax_pos.plot([], [], color="blue", lw=2)

        self.ax_vel.clear()
        self.ax_vel.set_title("Velocidade (v) vs Tempo (t)", fontsize=10, fontweight='bold')
        self.ax_vel.set_xlabel("Tempo (s)")
        self.ax_vel.set_ylabel("Velocidade (m/s)")
        self.ax_vel.grid(True, linestyle="--", alpha=0.6)
        self.line_vel, = self.ax_vel.plot([], [], color="red", lw=2)
        
        # Ativar o modo de autoescala contínua em ambos os eixos
        self.ax_pos.set_autoscale_on(True)
        self.ax_vel.set_autoscale_on(True)
        
        self.canvas_plots.draw()

    def desenhar_bola_estatica(self):
        if not self.animation_running:
            self.desenhar_esfera(self.y0_scale.get(), max(self.y0_scale.get() + 50, 10))

    def desenhar_esfera(self, y, alt_max):
        self.anim_canvas.delete("all")
        w = self.anim_canvas.winfo_width()
        h = self.anim_canvas.winfo_height()
        
        # Solo
        self.anim_canvas.create_rectangle(0, h-15, w, h, fill="#475569", outline="")
        
        # Mapeamento dinâmico
        espaco_util = h - 45
        bola_y = h - 15 - (y * espaco_util / alt_max)
        
        raio = 14
        self.anim_canvas.create_oval(w/2 - raio, bola_y - raio, w/2 + raio, bola_y + raio, fill="#ea580c", outline="#c2410c", width=2)

    def start_simulation(self):
        self.animation_running = False
        
        self.g = self.grav_opts[self.grav_var.get()]
        self.m = self.massa_scale.get()
        self.v = self.v0_scale.get()
        self.y = self.y0_scale.get()
        self.k = self.k_scale.get()
        
        # Estimação inicial apenas para a proporção visual do Canvas da esquerda
        v_subida = max(self.v, 0)
        self.alt_max_sim = self.y + (v_subida**2 / (2 * self.g))
        self.alt_max_sim = max(self.alt_max_sim * 1.1, 10)
        
        self.reset_plots()
        
        self.t = 0.0
        self.t_data, self.y_data, self.v_data = [], [], []
        
        self.ultimo_tempo = time.perf_counter()
        self.animation_running = True
        self.update_physics()

    def update_physics(self):
        if not self.animation_running: return
        
        agora = time.perf_counter()
        dt = agora - self.ultimo_tempo
        self.ultimo_tempo = agora
        
        if dt > 0.05: dt = 0.05 

        # Física do Movimento
        f_ar = -self.k * self.v * abs(self.v)
        f_grav = -self.m * self.g
        a = (f_grav + f_ar) / self.m
        
        self.v += a * dt
        self.y += self.v * dt
        self.t += dt
        
        if self.y <= 0:
            self.y = 0; self.v = 0
            self.animation_running = False
            
        self.t_data.append(self.t)
        self.y_data.append(self.y)
        self.v_data.append(self.v)
        
        # 1. Desenhar a Esfera no painel esquerdo
        self.desenhar_esfera(self.y, self.alt_max_sim)
        
        # 2. Injetar novos dados nas linhas dos gráficos
        self.line_pos.set_data(self.t_data, self.y_data)
        self.line_vel.set_data(self.t_data, self.v_data)
        
        # --- ATUALIZAÇÃO E AUTO-ESCALA REAL DOS EIXOS ---
        # Força o recálculo dos limites dos eixos com base nos novos dados inseridos
        self.ax_pos.relim()
        self.ax_pos.autoscale_view(True, True, True)
        
        self.ax_vel.relim()
        self.ax_vel.autoscale_view(True, True, True)
        
        # Redesenhar a janela de gráficos de forma económica (em segundo plano)
        self.canvas_plots.draw_idle() 
        
        if self.animation_running:
            self.root.after(10, self.update_physics)

if __name__ == "__main__":
    root = tk.Tk()
    app = VerticalLaunchSim(root)
    root.mainloop()