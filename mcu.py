import tkinter as tk
from tkinter import ttk
import math

G = 6.6743e-11
planetas = {
    "Terra": {"M": 5.972e24, "R": 6371000, "color": "#4b9cd3"},
    "Lua": {"M": 7.342e22, "R": 1737400, "color": "#a1a1a1"},
    "Marte": {"M": 6.39e23, "R": 3389500, "color": "#c1440e"},
    "Júpiter": {"M": 1.898e27, "R": 6991100, "color": "#b07f35"}
}

class SimuladorMCU:
    def __init__(self, root):
        self.root = root
        self.root.title("MCU - José Gonçalves (eufisica)")
        self.angle = 0
        
        # Painel Lateral de Controlos
        self.controls = ttk.Frame(root, padding=15)
        self.controls.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(self.controls, text="Seleccione o Corpo Celeste:").pack(anchor=tk.W)
        self.combo_planet = ttk.Combobox(self.controls, values=list(planetas.keys()), state="readonly")
        self.combo_planet.set("Terra")
        self.combo_planet.pack(fill=tk.X, pady=5)
        self.combo_planet.bind("<<ComboboxSelected>>", self.reset_slider)
        
        ttk.Label(self.controls, text="Altura h (km):").pack(anchor=tk.W, pady=(10,0))
        self.slider_h = ttk.Scale(self.controls, from_=100, to=40000, orient=tk.HORIZONTAL, command=self.update_physics)
        self.slider_h.set(2000)
        self.slider_h.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.controls, text="Massa Satélite (m) [kg]:").pack(anchor=tk.W, pady=(10,0))
        self.slider_m = ttk.Scale(self.controls, from_=100, to=10000, orient=tk.HORIZONTAL, command=self.update_physics)
        self.slider_m.set(1000)
        self.slider_m.pack(fill=tk.X, pady=5)
        
        self.lbl_stats = ttk.Label(self.controls, text="", font=("Courier", 10), justify=tk.LEFT)
        self.lbl_stats.pack(anchor=tk.W, pady=20)
        
        # Tela da Simulação
        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.update_physics()
        self.animate()

    def reset_slider(self, event=None):
        p = planetas[self.combo_planet.get()]
        self.slider_h.configure(to=p["R"]*3/1000)
        self.slider_h.set(p["R"]*0.4/1000)
        self.update_physics()

    def update_physics(self, event=None):
        p = planetas[self.combo_planet.get()]
        h = self.slider_h.get() * 1000
        m = self.slider_m.get()
        r = p["R"] + h
        
        v = math.sqrt((G * p["M"]) / r)
        T = (2 * math.pi * r) / v
        Fg = (G * p["M"] * m) / (r**2)
        
        max_h = self.slider_h.cget("to") * 1000
        
        self.physics = {"v": v, "T": T, "Fg": Fg, "r": r, "R_p": p["R"], "h": h, "color": p["color"], "max_h": max_h}
        
        stats = (f"R_planeta: {p['R']/1000:.0f} km\n"
                 f"Altura h:  {h/1000:.0f} km\n"
                 f"Raio r:    {r/1000:.0f} km\n\n"
                 f"Veloc.:    {v/1000:.2f} km/s\n"
                 f"Período T: {T/3600:.2f} h\n"
                 f"Força Fg:  {Fg:.2f} N")
        self.lbl_stats.config(text=stats)

    def animate(self):
        self.canvas.delete("all")
        cx, cy = 300, 300
        
        # Escala baseada na altura máxima para manter consistência ao mover sliders
        max_trajectory_radius = self.physics["R_p"] + self.physics["max_h"]
        scale = 220 / max_trajectory_radius
        
        # Adicionar margem de folga visual fixa de 15 píxeis para o planeta nunca tocar na órbita em h=100km
        r_px = (self.physics["r"] * scale) + 15
        R_px = self.physics["R_p"] * scale
        
        # 1. Desenhar Órbita
        self.canvas.create_oval(cx-r_px, cy-r_px, cx+r_px, cy+r_px, outline="#333333", dash=(4,4))
        
        # 2. Desenhar Planeta (Visualmente reduzido e isolado da linha de órbita)
        self.canvas.create_oval(cx-R_px, cy-R_px, cx+R_px, cy+R_px, fill=self.physics["color"], outline="")
        
        # 3. Posição do Satélite
        sx = cx + r_px * math.cos(self.angle)
        sy = cy + r_px * math.sin(self.angle)
        
        # 4. Desenhar Satélite
        self.canvas.create_oval(sx-5, sy-5, sx+5, sy+5, fill="white", outline="")
        
        # AJUSTE AUTOMÁTICO DO COMPRIMENTO VISUAL DOS VETORES
        v_len = max(25, min(80, (self.physics["v"] / 5000) * 35))
        fg_len = max(25, min(80, (self.physics["Fg"] / 10000) * 40))
        
        # 5. Vetor Velocidade (Verde)
        vx = -v_len * math.sin(self.angle)
        vy = v_len * math.cos(self.angle)
        self.canvas.create_line(sx, sy, sx + vx, sy + vy, fill="#00ff00", width=2, arrow=tk.LAST)
        
        # 6. Vetor Força (Vermelho)
        fx = -fg_len * math.cos(self.angle)
        fy = -fg_len * math.sin(self.angle)
        self.canvas.create_line(sx, sy, sx + fx, sy + fy, fill="#ff3333", width=2, arrow=tk.LAST)
        
        # VELOCIDADE DA ANIMAÇÃO DUPLICADA (Multiplicador de 0.5 passou para 2.0)
        self.angle += (self.physics["v"] / self.physics["r"]) * 2.0
        
        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMCU(root)
    root.mainloop()