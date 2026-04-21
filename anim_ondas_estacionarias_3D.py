import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Configurações estéticas
plt.style.use('dark_background')

# --- Definição da Geometria ---
L_x = 10        # Comprimento da superfície (eixo X)
L_y = 5         # Largura da superfície (eixo Y)
resolution = 50 # Pontos na grade

x = np.linspace(0, L_x, resolution)
y = np.linspace(0, L_y, resolution)
X, Y = np.meshgrid(x, y) # Cria a grade base

# --- Parâmetros Físicos Iniciais ---
omega_ini = 2.0  # Frequência angular temporal
k_ini = 0.628    # Número de onda espacial (k = 2*pi / lambda)
amp_ini = 1.0    # Amplitude

# --- Configuração da Figura e Eixo 3D ---
fig = plt.figure(figsize=(12, 8))
plt.subplots_adjust(bottom=0.25) # Espaço para os sliders
ax = fig.add_subplot(projection='3d')

# Função que define a física da onda estacionária
def calcular_onda(t, amp, k, omega):
    """Calcula o deslocamento Z(x, y, t)"""
    # y(x, t) = 2A * sin(kx) * cos(wt)
    return 2 * amp * np.sin(k * X) * np.cos(omega * t)

# Plota a superfície inicial e guarda a referência
# 'antialiased=True' e 'shade=True' melhoram o visual 3D
Z = calcular_onda(0, amp_ini, k_ini, omega_ini)
surface = [ax.plot_surface(X, Y, Z, cmap='plasma', 
                           linewidth=0, antialiased=True, shade=True)]

# Configurações dos eixos e título
ax.set_xlim(0, L_x)
ax.set_ylim(0, L_y)
ax.set_zlim(-2.5, 2.5) # Limite de deslocamento Z
ax.set_xlabel('Comprimento (X)')
ax.set_ylabel('Largura (Y)')
ax.set_zlabel('Deslocamento (Z)')
ax.set_title("Onda Estacionária 3D")

# Tenta definir uma perspectiva inicial melhor
ax.view_init(elev=30, azim=-60)

# --- Widgets (Controles) ---
# Define a posição [left, bottom, width, height]
ax_amp = plt.axes([0.15, 0.12, 0.3, 0.03])
ax_freq = plt.axes([0.15, 0.08, 0.3, 0.03])
ax_k = plt.axes([0.55, 0.12, 0.3, 0.03])

# Criação dos sliders
s_amp = Slider(ax_amp, 'Amplitude', 0.1, 1.25, valinit=amp_ini)
s_freq = Slider(ax_freq, 'Frequência (ω)', 0.1, 5.0, valinit=omega_ini)
s_k = Slider(ax_k, 'Núm. Onda (k)', 0.1, 2.0, valinit=k_ini)

# --- Função de Atualização da Animação ---
def update(frame):
    # O frame é um contador de tempo
    t = frame * 0.1 
    
    # Lê os valores atuais dos sliders
    amp = s_amp.val
    omega = s_freq.val
    k = s_k.val
    
    # Recalcula a física
    new_Z = calcular_onda(t, amp, k, omega)
    
    # Remove a superfície antiga e desenha a nova (necessário no mplot3d)
    surface[0].remove()
    surface[0] = ax.plot_surface(X, Y, new_Z, cmap='plasma', 
                                 linewidth=0, antialiased=True, shade=True)
    
    return surface[0],

# --- Criação da Animação ---
# interval: tempo entre frames em milissegundos
# blit: deve ser False para mplot3d update
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=False)

plt.show()