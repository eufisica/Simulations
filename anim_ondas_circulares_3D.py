import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Configurações visuais
plt.style.use('dark_background')

# --- Preparação da Grade ---
grid_size = 100
range_val = 10
x = np.linspace(-range_val, range_val, grid_size)
y = np.linspace(-range_val, range_val, grid_size)
X, Y = np.meshgrid(x, y)

# Distância radial de cada ponto à origem (0,0)
R = np.sqrt(X**2 + Y**2)

# --- Parâmetros Iniciais ---
freq_ini = 2.0   # Frequência angular (omega)
k_ini = 1.5      # Número de onda (proximidade das cristas)
amp_ini = 0.5    # Altura da onda

fig = plt.figure(figsize=(10, 7))
plt.subplots_adjust(bottom=0.2)
ax = fig.add_subplot(111, projection='3d')

# Função para calcular a altura da onda com um leve amortecimento radial
def calcular_onda_circular(t, amp, k, omega):
    # O termo (R + 0.1) evita divisão por zero e cria um decaimento natural
    # de energia conforme a onda se afasta do centro
    z = amp * np.cos(k * R - omega * t) * np.exp(-0.1 * R)
    return z

# Plot inicial
Z = calcular_onda_circular(0, amp_ini, k_ini, freq_ini)
surf = [ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0, antialiased=False)]

# Estética do gráfico
ax.set_zlim(-1, 1)
ax.set_axis_off() # Remove eixos para focar na fluidez da água
ax.view_init(elev=45, azim=45)

# --- Controles ---
ax_freq = plt.axes([0.2, 0.1, 0.6, 0.03])
ax_k = plt.axes([0.2, 0.05, 0.6, 0.03])

s_freq = Slider(ax_freq, 'Velocidade', 0.5, 10.0, valinit=freq_ini)
s_k = Slider(ax_k, 'Densidade (k)', 0.5, 5.0, valinit=k_ini)

def update(frame):
    t = frame * 0.1
    omega = s_freq.val
    k = s_k.val
    
    new_Z = calcular_onda_circular(t, amp_ini, k, omega)
    
    surf[0].remove()
    surf[0] = ax.plot_surface(X, Y, new_Z, cmap='coolwarm', 
                               linewidth=0, antialiased=False, shade=True)
    return surf[0],

ani = FuncAnimation(fig, update, frames=100, interval=30, blit=False)

plt.show()