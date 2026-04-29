"""
Animação 3D de Ondas Circulares - José Gonçalves
================================
Dependências: numpy, matplotlib
Instalar:  pip install numpy matplotlib

Controlos durante a animação:
  - Arrastar com o rato: rodar a câmara
  - Scroll: zoom
  - Teclas 1-5: mudar modo de fontes
  - Tecla espaço: pausar/continuar
  - Tecla w: mostrar/ocultar grade
  - Tecla r: reiniciar tempo
  - Fechar a janela: sair
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib import colormaps

# ---------------------------------------------------------------------------
# Parâmetros iniciais
# ---------------------------------------------------------------------------
GRID = 80           # resolução da malha (NxN)
SIZE = 6.0          # tamanho físico da superfície
FPS  = 30           # frames por segundo

# ---------------------------------------------------------------------------
# Modos de fontes
# ---------------------------------------------------------------------------
MODOS = {
    "1 fonte":   [(0.0,  0.0,  0.0)],
    "2 fontes":  [(-1.5, 0.0,  0.0),   (1.5,  0.0,  0.0)],
    "3 fontes":  [(0.0, -1.8,  0.0),   (-1.6, 0.9,  0.0),  (1.6,  0.9,  0.0)],
    "4 fontes":  [(-1.5,-1.5,  0.0),   (1.5, -1.5,  0.0),  (-1.5, 1.5,  0.0), (1.5,  1.5, 0.0)],
    "Anel (8)":  [(2.2*np.cos(i*np.pi/4), 2.2*np.sin(i*np.pi/4), i*np.pi/4)
                  for i in range(8)],
}

# ---------------------------------------------------------------------------
# Estado da simulação
# ---------------------------------------------------------------------------
state = {
    "paused":   False,
    "wire":     False,
    "t":        0.0,
    "sources":  MODOS["1 fonte"],
    "colormap": "ocean",
}

# ---------------------------------------------------------------------------
# Malha espacial
# ---------------------------------------------------------------------------
half = SIZE / 2
x = np.linspace(-half, half, GRID)
z = np.linspace(-half, half, GRID)
X, Z = np.meshgrid(x, z)

# ---------------------------------------------------------------------------
# Função de altura da onda
# ---------------------------------------------------------------------------
def calcular_onda(X, Z, t, freq, amp, lam, damp, spd):
    k     = 2 * np.pi / lam
    omega = 2 * np.pi * freq
    H     = np.zeros_like(X)
    for (sx, sz, fase) in state["sources"]:
        R      = np.sqrt((X - sx)**2 + (Z - sz)**2) + 1e-6
        decay  = np.exp(-damp * R * 0.5)
        spread = 1.0 / (1.0 + R * 0.4)
        H     += amp * spread * decay * np.sin(k * R - omega * t * spd + fase)
    return H

# ---------------------------------------------------------------------------
# Figura principal
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(14, 8), facecolor="#0d1117")
fig.canvas.manager.set_window_title("Ondas Circulares 3D - José Gonçalves")

# Eixo 3D principal — deixa espaço à esquerda para a barra de cor
ax = fig.add_axes([0.08, 0.18, 0.58, 0.80], projection="3d")
ax.set_facecolor("#0d1117")
ax.tick_params(colors="#888888", labelsize=7)
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor("#222222")
ax.xaxis.label.set_color("#888888")
ax.yaxis.label.set_color("#888888")
ax.zaxis.label.set_color("#888888")
ax.set_xlabel("X", labelpad=2)
ax.set_ylabel("Z", labelpad=2)
ax.set_zlabel("Y", labelpad=2)
ax.set_xlim(-half, half)
ax.set_ylim(-half, half)
ax.view_init(elev=30, azim=45)

# Calcular primeiro frame para inicializar o surface
H0 = calcular_onda(X, Z, 0, freq=2.0, amp=0.5, lam=1.5, damp=0.4, spd=1.5)
vmax = np.max(np.abs(H0)) + 0.01

surf = [ax.plot_surface(
    X, Z, H0,
    cmap=colormaps["ocean"],
    linewidth=0, antialiased=True,
    alpha=0.92, vmin=-vmax, vmax=vmax
)]

# ---------------------------------------------------------------------------
# Barra de cor — à ESQUERDA do gráfico 3D
# ---------------------------------------------------------------------------
cbar_ax = fig.add_axes([0.02, 0.25, 0.015, 0.55])
cbar_ax.set_facecolor("#0d1117")
sm = plt.cm.ScalarMappable(cmap="ocean", norm=plt.Normalize(vmin=-1, vmax=1))
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)
cbar.ax.tick_params(colors="#888888", labelsize=7)
cbar.set_label("amplitude", color="#888888", fontsize=8)

# ---------------------------------------------------------------------------
# Painel de controlos (sliders + botões) — lado direito
# ---------------------------------------------------------------------------
slider_color  = "#1e2530"
slider_handle = "#4a9eff"
label_color   = "#aaaaaa"

def make_slider(left, bottom, label, valmin, valmax, valinit, step=None):
    ax_s = fig.add_axes([left, bottom, 0.22, 0.025], facecolor=slider_color)
    s = Slider(ax_s, label, valmin, valmax, valinit=valinit,
               color=slider_handle, track_color="#333344")
    s.label.set_color(label_color)
    s.label.set_fontsize(8)
    s.valtext.set_color(label_color)
    s.valtext.set_fontsize(8)
    if step:
        s.valstep = step
    return s

L = 0.72
sl_freq = make_slider(L, 0.88, "Frequência (Hz)",  0.3, 6.0, 2.0)
sl_amp  = make_slider(L, 0.80, "Amplitude",         0.05, 1.2, 0.5)
sl_lam  = make_slider(L, 0.72, "Compr. onda (m)",   0.5,  4.0, 1.5)
sl_damp = make_slider(L, 0.64, "Amortecimento",      0.0,  1.5, 0.4)
sl_spd  = make_slider(L, 0.56, "Vel. propagação",    0.5,  4.0, 1.5)
sl_arot = make_slider(L, 0.48, "Auto-rotação",       0.0,  3.0, 0.5)

# ---------------------------------------------------------------------------
# Botões — Pausa e Play separados
# ---------------------------------------------------------------------------
def make_button(left, bottom, width, label, bg="#1e2530"):
    ax_b = fig.add_axes([left, bottom, width, 0.04], facecolor=bg)
    b = Button(ax_b, label, color=bg, hovercolor="#2e3540")
    b.label.set_color(label_color)
    b.label.set_fontsize(8)
    return b

# Botões Pausar e Play lado a lado
btn_pause = make_button(L,         0.38, 0.10, "⏸  Pausar",  "#1e2530")
btn_play  = make_button(L + 0.12,  0.38, 0.10, "▶  Play",   "#162a1e")  # tom verde escuro

btn_reset = make_button(L,         0.32, 0.10, "Reiniciar")
btn_wire  = make_button(L + 0.12,  0.32, 0.10, "Grade ON")
btn_color = make_button(L,         0.26, 0.22, "Paleta: ocean")

# Radio buttons para modo
ax_radio = fig.add_axes([L, 0.05, 0.26, 0.18], facecolor="#0d1117")
radio = RadioButtons(
    ax_radio, list(MODOS.keys()), active=0,
    activecolor="#4a9eff"
)
for lbl in radio.labels:
    lbl.set_color(label_color)
    lbl.set_fontsize(8)

# Título
fig.text(0.75, 0.96, "Ondas Circulares 3D - José Gonçalves",
         color="white", fontsize=11, fontweight="bold", ha="center")

# ---------------------------------------------------------------------------
# Paletas disponíveis
# ---------------------------------------------------------------------------
PALETAS = ["ocean", "plasma", "RdBu_r", "viridis", "hot"]
pal_idx = [0]

# ---------------------------------------------------------------------------
# Função auxiliar: atualizar a barra de cor com a paleta atual
# ---------------------------------------------------------------------------
def refresh_colorbar():
    cmap_name = state["colormap"]
    # Redesenhar o mapeamento escalar com a nova paleta
    new_sm = plt.cm.ScalarMappable(
        cmap=cmap_name,
        norm=plt.Normalize(vmin=-1, vmax=1)
    )
    new_sm.set_array([])
    cbar_ax.cla()
    fig.colorbar(new_sm, cax=cbar_ax)
    cbar_ax.tick_params(colors="#888888", labelsize=7)
    cbar_ax.set_ylabel("amplitude", color="#888888", fontsize=8)

# ---------------------------------------------------------------------------
# Callbacks dos botões
# ---------------------------------------------------------------------------
def cb_pause(event):
    state["paused"] = True

def cb_play(event):
    state["paused"] = False

def cb_reset(event):
    state["t"] = 0.0

def cb_wire(event):
    state["wire"] = not state["wire"]
    btn_wire.label.set_text("Grade OFF" if state["wire"] else "Grade ON")

def cb_color(event):
    pal_idx[0] = (pal_idx[0] + 1) % len(PALETAS)
    state["colormap"] = PALETAS[pal_idx[0]]
    btn_color.label.set_text(f"Paleta: {state['colormap']}")
    refresh_colorbar()
    fig.canvas.draw_idle()

def cb_radio(label):
    state["sources"] = MODOS[label]
    state["t"] = 0.0

btn_pause.on_clicked(cb_pause)
btn_play.on_clicked(cb_play)
btn_reset.on_clicked(cb_reset)
btn_wire.on_clicked(cb_wire)
btn_color.on_clicked(cb_color)
radio.on_clicked(cb_radio)

# Teclas de atalho
def on_key(event):
    k = event.key
    if k == " ":
        state["paused"] = not state["paused"]
    elif k == "r":
        cb_reset(None)
    elif k == "w":
        cb_wire(None)
    elif k in "12345":
        idx = int(k) - 1
        keys = list(MODOS.keys())
        if idx < len(keys):
            state["sources"] = MODOS[keys[idx]]
            radio.set_active(idx)
            state["t"] = 0.0

fig.canvas.mpl_connect("key_press_event", on_key)

# ---------------------------------------------------------------------------
# Marcadores visuais das fontes
# ---------------------------------------------------------------------------
source_dots = []
for _ in range(8):  # máximo possível
    dot, = ax.plot([], [], [], "o", color="#ff6644", markersize=6, zorder=10)
    source_dots.append(dot)

def update_source_dots():
    for i, (sx, sz, _) in enumerate(state["sources"]):
        if i < len(source_dots):
            source_dots[i].set_data([sx], [sz])
            source_dots[i].set_3d_properties([0.15])
    for j in range(len(state["sources"]), len(source_dots)):
        source_dots[j].set_data([], [])
        source_dots[j].set_3d_properties([])

# Auto-rotação acumulada
auto_azim = [45.0]

# ---------------------------------------------------------------------------
# Função de animação
# ---------------------------------------------------------------------------
def animate(frame):
    if not state["paused"]:
        state["t"] += 1.0 / FPS

    freq = sl_freq.val
    amp  = sl_amp.val
    lam  = sl_lam.val
    damp = sl_damp.val
    spd  = sl_spd.val
    arot = sl_arot.val

    H = calcular_onda(X, Z, state["t"], freq, amp, lam, damp, spd)

    # Remover surface anterior e redesenhar
    surf[0].remove()
    vmax = max(np.max(np.abs(H)), 0.01)

    lw = 0.3 if state["wire"] else 0
    surf[0] = ax.plot_surface(
        X, Z, H,
        cmap=colormaps[state["colormap"]],
        linewidth=lw, antialiased=True,
        alpha=0.92, vmin=-vmax, vmax=vmax
    )

    # Limites Z dinâmicos
    margin = max(vmax * 1.2, 0.3)
    ax.set_zlim(-margin, margin)

    # Auto-rotação da câmara
    if not state["paused"]:
        auto_azim[0] += arot * 0.5
    ax.view_init(elev=ax.elev, azim=auto_azim[0])

    update_source_dots()

    return surf[0],

# ---------------------------------------------------------------------------
# Iniciar animação
# ---------------------------------------------------------------------------
ani = animation.FuncAnimation(
    fig, animate,
    interval=1000 // FPS,
    blit=False,
    cache_frame_data=False
)

plt.show()