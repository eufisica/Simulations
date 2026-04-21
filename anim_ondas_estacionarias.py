import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Configurações iniciais da figura
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25) # Espaço para os sliders

# Parâmetros iniciais
L = 10            # Comprimento da corda
x = np.linspace(0, L, 1000)
t = 0
frequencia_ini = 1.0
densidade_ini = 1.0
tensao = 10.0      # Tensão constante para simplificar

# Cálculo da onda
def calcular_onda(x, t, f, mu):
    # v = sqrt(T/mu)
    v = np.sqrt(tensao / mu)
    # k = 2 * pi * f / v
    k = (2 * np.pi * f) / v
    omega = 2 * np.pi * f
    return 2 * np.sin(k * x) * np.cos(omega * t)

line, = ax.plot(x, calcular_onda(x, t, frequencia_ini, densidade_ini), lw=2, color='#2c3e50')
ax.set_ylim(-2.5, 2.5)
ax.set_title("Simulação de Onda Estacionária")
ax.grid(True, linestyle='--')

# Criação dos Sliders
ax_freq = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_dens = plt.axes([0.2, 0.05, 0.65, 0.03])

s_freq = Slider(ax_freq, 'Frequência (Hz)', 0.1, 5.0, valinit=frequencia_ini)
s_dens = Slider(ax_dens, 'Densidade (µ)', 0.1, 5.0, valinit=densidade_ini)

def update(frame):
    global t
    t += 0.05 # Incremento de tempo
    f = s_freq.val
    mu = s_dens.val
    y = calcular_onda(x, t, f, mu)
    line.set_ydata(y)
    return line,

# Animação
ani = FuncAnimation(fig, update, frames=None, interval=20, blit=True)

plt.show()