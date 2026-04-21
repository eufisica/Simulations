import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons, CheckButtons

# Configurações de Estilo
plt.style.use('dark_background')

# --- Parâmetros Iniciais ---
L = 10.0
x = np.linspace(0, L, 500)
t = 0
dt = 0.05

fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.1, bottom=0.35, top=0.9)

# Linhas da Simulação
line_res, = ax.plot(x, np.zeros_like(x), color='springgreen', lw=3, label='Resultante')
line_fwd, = ax.plot(x, np.zeros_like(x), 'r--', alpha=0.5, label='Progressiva →')
line_bwd, = ax.plot(x, np.zeros_like(x), 'b--', alpha=0.5, label='Regressiva ←')
scatter_nodes = ax.scatter([], [], color='orange', s=100, zorder=5, label='Nós')
scatter_anti = ax.scatter([], [], color='lime', s=100, zorder=5, label='Ventres')

ax.set_ylim(-3, 3)
ax.legend(loc='upper right')

# --- Widgets (Controles) ---
ax_freq = plt.axes([0.15, 0.22, 0.3, 0.03])
ax_amp  = plt.axes([0.15, 0.17, 0.3, 0.03])
ax_n    = plt.axes([0.15, 0.12, 0.3, 0.03])
ax_dens = plt.axes([0.55, 0.22, 0.3, 0.03])
ax_tens = plt.axes([0.55, 0.17, 0.3, 0.03])
ax_damp = plt.axes([0.55, 0.12, 0.3, 0.03])

s_freq = Slider(ax_freq, 'Freq.', 0.1, 5.0, valinit=1.0)
s_amp  = Slider(ax_amp, 'Amp.', 0.1, 1.5, valinit=1.0)
s_n    = Slider(ax_n, 'Harmônico (n)', 1, 10, valinit=1, valstep=1)
s_dens = Slider(ax_dens, 'Densidade (ρ)', 0.1, 5.0, valinit=1.0)
s_tens = Slider(ax_tens, 'Tensão (T)', 1.0, 50.0, valinit=10.0)
s_damp = Slider(ax_damp, 'Amort.', 0.0, 0.5, valinit=0.0)

ax_mode = plt.axes([0.02, 0.4, 0.08, 0.15])
radio = RadioButtons(ax_mode, ('Corda', 'Tubo', 'Harmônicos'))

ax_check = plt.axes([0.02, 0.6, 0.08, 0.1])
check = CheckButtons(ax_check, ['Nós/Ventres'], [False])

# Texto de Métricas
text_metrics = fig.text(0.15, 0.02, '', fontsize=10, color='cyan', family='monospace')

def update(frame):
    global t
    t += dt
    
    # Parâmetros dos Sliders
    A = s_amp.val
    n = s_n.val
    f = s_freq.val
    rho = s_dens.val
    T = s_tens.val
    gamma = s_damp.val
    mode = radio.value_selected
    
    # Física
    v = np.sqrt(T / rho)
    # Para harmônicos em corda presa (L): lambda = 2L/n
    wavelength = (2 * L) / n
    k = 2 * np.pi / wavelength
    omega = 2 * np.pi * f
    
    # Amortecimento (fator exponencial simplificado)
    damp_factor = np.exp(-gamma * t)
    
    # Cálculo das Ondas
    y_fwd = A * damp_factor * np.sin(k * x - omega * t)
    y_bwd = A * damp_factor * np.sin(k * x + omega * t)
    y_res = y_fwd + y_bwd
    
    if mode == 'Tubo':
        # Representação de pressão: deslocada para simular extremidade
        y_res = 2 * A * damp_factor * np.cos(k * x) * np.cos(omega * t)
        line_fwd.set_visible(False)
        line_bwd.set_visible(False)
    else:
        line_fwd.set_visible(True)
        line_bwd.set_visible(True)
        line_fwd.set_ydata(y_fwd)
        line_bwd.set_ydata(y_bwd)

    line_res.set_ydata(y_res)
    
    # Atualizar Nós e Ventres
    show_pts = check.get_status()[0]
    if show_pts:
        nodes_x = np.linspace(0, L, int(n) + 1)
        nodes_y = np.zeros_like(nodes_x)
        anti_x = np.linspace(L/(2*n), L - L/(2*n), int(n))
        anti_y = np.zeros_like(anti_x) # Simplificado para o eixo x
        scatter_nodes.set_offsets(np.c_[nodes_x, nodes_y])
        scatter_anti.set_offsets(np.c_[anti_x, anti_y])
    else:
        scatter_nodes.set_offsets(np.empty((0, 2)))
        scatter_anti.set_offsets(np.empty((0, 2)))

    # Métricas
    text_metrics.set_text(f"Vel. Fase: {v:.2f} m/s | λ: {wavelength:.2f} m | v_transversal max: {omega*A:.2f}")
    
    return line_res, line_fwd, line_bwd, scatter_nodes, scatter_anti

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()