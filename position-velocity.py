import tkinter as tk
from tkinter import ttk
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulacaoMovimento:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Movimento Interativo - José Gonçalves (eufisica)")
        self.root.geometry("1200x800")
        
        # Variáveis de dados
        self.tempos = [0.0]
        self.pos_x = [0.0]
        self.pos_y = [0.0]
        self.vel_x = [0.0]
        self.vel_y = [0.0]
        
        self.ultimo_tempo = time.time()
        self.primeiro_movimento = True
        
        # Configuração da Interface (Layout)
        self.criar_painel_superior()
        
        # Contentor principal para os gráficos e tela de desenho
        paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lado Esquerdo: Área de arrasto (Canvas)
        self.canvas_width = 400
        self.canvas_height = 400
        self.canvas = tk.Canvas(paned_window, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, bd=2)
        paned_window.add(self.canvas)
        
        # Lado Direito: Área dos Gráficos (Matplotlib)
        self.frame_graficos = ttk.Frame(paned_window)
        paned_window.add(self.frame_graficos)
        
        # Desenhar a grelha inicial e a bola
        self.desenhar_grelha()
        self.bola = self.canvas.create_oval(190, 190, 210, 210, fill="red", tags="bola")
        
        # Inicializar os gráficos do Matplotlib
        self.configurar_graficos()
        
        # Bind dos eventos do rato para arrastar
        self.canvas.tag_bind("bola", "<Button-1>", self.ao_clicar)
        self.canvas.tag_bind("bola", "<B1-Motion>", self.ao_arrastar)
        self.canvas.tag_bind("bola", "<ButtonRelease-1>", self.ao_libertar)

    def criar_painel_superior(self):
        """Cria o painel de leitura de dados no topo."""
        self.frame_topo = ttk.Frame(self.root, padding=10)
        self.frame_topo.pack(fill=tk.X)
        
        self.lbl_r = ttk.Label(self.frame_topo, text="Posição r = 0.00 m", font=("Arial", 14, "bold"))
        self.lbl_r.pack(side=tk.LEFT, padx=20)
        
        self.lbl_v = ttk.Label(self.frame_topo, text="Velocidade v = 0.00 m/s", font=("Arial", 14, "bold"))
        self.lbl_v.pack(side=tk.LEFT, padx=20)
        
        lbl_info = ttk.Label(self.frame_topo, text="Arraste a bola vermelha para simular", font=("Arial", 10, "italic"), foreground="gray")
        lbl_info.pack(side=tk.RIGHT, padx=20)

    def desenhar_grelha(self):
        """Desenha a grelha quadriculada de fundo com os eixos centrais."""
        passo = 20
        # Linhas verticais e horizontais finas
        for x in range(0, self.canvas_width, passo):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="#e0e0e0")
        for y in range(0, self.canvas_height, passo):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#e0e0e0")
            
        # Eixos centrais (Referencial 0,0 no centro)
        self.canvas.create_line(self.canvas_width/2, 0, self.canvas_width/2, self.canvas_height, fill="#888888", width=2)
        self.canvas.create_line(0, self.canvas_height/2, self.canvas_width, self.canvas_height/2, fill="#888888", width=2)

    def obter_coordenadas_reais(self, cx, cy):
        """Converte as coordenadas do Canvas (pixels) para metros (sistema físico)."""
        # Centro do canvas é o (0,0). Cada 20 pixels = 1 metro.
        x_m = (cx - (self.canvas_width / 2)) / 20.0
        y_m = ((self.canvas_height / 2) - cy) / 20.0  # Inverter o eixo Y do canvas
        return x_m, y_m

    def configurar_graficos(self):
        """Configura a estrutura de subplots do Matplotlib."""
        # Criar a figura com uma disposição personalizada de subplots
        self.fig = plt.figure(figsize=(10, 8), tight_layout=True)
        
        # Grelha de subplots: 2 linhas, 3 colunas
        # Coluna da direita (y vs x) ocupa as duas linhas de altura
        self.ax_yx = plt.subplot2grid((2, 3), (0, 2), rowspan=2)
        
        # Colunas da esquerda e centro para os gráficos temporais
        self.ax_xt = plt.subplot2grid((2, 3), (0, 0))
        self.ax_yt = plt.subplot2grid((2, 3), (0, 1))
        self.ax_vxt = plt.subplot2grid((2, 3), (1, 0))
        self.ax_vyt = plt.subplot2grid((2, 3), (1, 1))
        
        # Títulos e Labels
        self.ax_yx.set_title("Posição: Y vs X")
        self.ax_yx.set_xlabel("X (m)")
        self.ax_yx.set_ylabel("Y (m)")
        self.ax_yx.grid(True)
        
        self.ax_xt.set_title("X vs Tempo")
        self.ax_xt.set_xlabel("t (s)")
        self.ax_xt.set_ylabel("X (m)")
        self.ax_xt.grid(True)
        
        self.ax_yt.set_title("Y vs Tempo")
        self.ax_yt.set_xlabel("t (s)")
        self.ax_yt.set_ylabel("Y (m)")
        self.ax_yt.grid(True)
        
        self.ax_vxt.set_title("Vx vs Tempo")
        self.ax_vxt.set_xlabel("t (s)")
        self.ax_vxt.set_ylabel("Vx (m/s)")
        self.ax_vxt.grid(True)
        
        self.ax_vyt.set_title("Vy vs Tempo")
        self.ax_vyt.set_xlabel("t (s)")
        self.ax_vyt.set_ylabel("Vy (m/s)")
        self.ax_vyt.grid(True)
        
        # Integrar a figura no Tkinter
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.frame_graficos)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def ao_clicar(self, event):
        """Deteta o início do movimento."""
        self.ultimo_tempo = time.time()
        if self.primeiro_movimento:
            # Definir o ponto inicial com base onde clicou
            cx, cy = event.x, event.y
            x0, y0 = self.obter_coordenadas_reais(cx, cy)
            self.pos_x = [x0]
            self.pos_y = [y0]
            self.primeiro_movimento = False

    def ao_arrastar(self, event):
        """Gere o movimento da bola, calcula a física e atualiza os gráficos."""
        cx, cy = event.x, event.y
        
        # Limitar para a bola não sair da tela de simulação
        cx = max(10, min(self.canvas_width - 10, cx))
        cy = max(10, min(self.canvas_height - 10, cy))
        
        # Atualiza a posição visual da bola (centrada no rato)
        self.canvas.coords(self.bola, cx-10, cy-10, cx+10, cy+10)
        
        # Tempo decorrido
        agora = time.time()
        dt = agora - self.ultimo_tempo
        
        # Evita divisões por zero ou passos demasiado pequenos que quebrem a derivada
        if dt < 0.01:
            return
            
        self.ultimo_tempo = agora
        
        # Obter coordenadas no sistema métrico
        x, y = self.obter_coordenadas_reais(cx, cy)
        tempo_atual = self.tempos[-1] + dt
        
        # Calcular velocidades instantâneas (v = dx/dt)
        vx = (x - self.pos_x[-1]) / dt
        vy = (y - self.pos_y[-1]) / dt
        
        # Guardar dados nos históricos
        self.tempos.append(tempo_atual)
        self.pos_x.append(x)
        self.pos_y.append(y)
        self.vel_x.append(vx)
        self.vel_y.append(vy)
        
        # Limitar histórico para manter a performance fluida (últimos 150 pontos)
        if len(self.tempos) > 150:
            self.tempos.pop(0)
            self.pos_x.pop(0)
            self.pos_y.pop(0)
            self.vel_x.pop(0)
            self.vel_y.pop(0)
            
        # Cálculos de magnitude vetorial pedidas
        r = np.sqrt(x**2 + y**2)
        v = np.sqrt(vx**2 + vy**2)
        
        # Atualizar labels superiores
        self.lbl_r.config(text=f"Posição r = {r:.2f} m")
        self.lbl_v.config(text=f"Velocidade v = {v:.2f} m/s")
        
        # Atualizar os gráficos em tempo real
        self.atualizar_graficos()

    def ao_libertar(self, event):
        """Zera as velocidades quando o utilizador larga o rato."""
        if self.tempos:
            self.tempos.append(self.tempos[-1] + 0.01)
            self.pos_x.append(self.pos_x[-1])
            self.pos_y.append(self.pos_y[-1])
            self.vel_x.append(0.0)
            self.vel_y.append(0.0)
            self.atualizar_graficos()

    def atualizar_graficos(self):
        """Limpa as linhas antigas dos subplots e desenha as trajetórias atualizadas."""
        # Limpar os eixos de dados mas manter as propriedades
        for ax in [self.ax_yx, self.ax_xt, self.ax_yt, self.ax_vxt, self.ax_vyt]:
            ax.cla()
            ax.grid(True)
            
        # Reconfigurar labels após o clear (cla)
        self.ax_yx.set_title("Posição: Y vs X")
        self.ax_yx.set_xlabel("X (m)")
        self.ax_yx.set_ylabel("Y (m)")
        self.ax_yx.set_xlim(-10, 10)
        self.ax_yx.set_ylim(-10, 10)
        
        self.ax_xt.set_title("X vs Tempo")
        self.ax_xt.set_ylabel("X (m)")
        self.ax_yt.set_title("Y vs Tempo")
        self.ax_yt.set_ylabel("Y (m)")
        self.ax_vxt.set_title("Vx vs Tempo")
        self.ax_vxt.set_ylabel("Vx (m/s)")
        self.ax_vyt.set_title("Vy vs Tempo")
        self.ax_vyt.set_ylabel("Vy (m/s)")
        
        # Desenhar as novas linhas de dados
        self.ax_yx.plot(self.pos_x, self.pos_y, 'r-', marker='o', markersize=3)
        self.ax_xt.plot(self.tempos, self.pos_x, 'b-')
        self.ax_yt.plot(self.tempos, self.pos_y, 'g-')
        self.ax_vxt.plot(self.tempos, self.vel_x, 'm-')
        self.ax_vyt.plot(self.tempos, self.vel_y, 'c-')
        
        # Atualizar a imagem na interface gráfica
        self.canvas_plot.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacaoMovimento(root)
    root.mainloop()