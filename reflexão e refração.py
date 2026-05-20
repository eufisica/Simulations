import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Índices de refração
n1 = 1.0  # Ar
n2 = 1.5  # Vidro

# Configuração da figura com espaço para o Slider
fig, ax = plt.subplots(figsize=(9, 7))
plt.subplots_adjust(bottom=0.2)

# Criar o gráfico embutido (Inset) para o detalhe das frentes de onda
# [esquerda, baixo, largura, altura] em frações da janela
ax_inset = fig.add_axes([0.62, 0.58, 0.25, 0.25])

def atualizar_simulacao(angulo_inc_graus):
    ax.clear()
    ax_inset.clear()
    
    # 1. Configuração dos eixos principais
    ax.axhline(0, color='blue', lw=2, label='Interface Ar/Vidro')
    ax.axvline(0, color='gray', linestyle='--', alpha=0.7, label='Normal')
    ax.fill_between([-5, 5], 0, -5, color='lightblue', alpha=0.3, label=f'Vidro (n={n2})')
    ax.fill_between([-5, 5], 0, 5, color='white', alpha=0.3, label=f'Ar (n={n1})')
    
    # Graus para radianos
    theta1 = np.radians(angulo_inc_graus)
    
    # Lei de Snell para a refração: n1 * sin(theta1) = n2 * sin(theta2)
    sin_theta2 = (n1 * np.sin(theta1)) / n2
    theta2 = np.arcsin(sin_theta2)
    
    # 2. Desenhar os Raios (Óptica Geométrica)
    # Raio Incidente (Vem de cima para a origem)
    x_inc = np.array([-3 * np.sin(theta1), 0])
    y_inc = np.array([3 * np.cos(theta1), 0])
    ax.plot(x_inc, y_inc, color='red', lw=2.5, label='Raio Incidente')
    
    # Raio Refletido (Sobe a partir da origem com o mesmo ângulo)
    x_refletido = np.array([0, 3 * np.sin(theta1)])
    y_refletido = np.array([0, 3 * np.cos(theta1)])
    ax.plot(x_refletido, y_refletido, color='orange', lw=2, linestyle='--', label='Raio Refletido')
    
    # Raio Refratado (Entra no vidro)
    x_refra = np.array([0, 3 * np.sin(theta2)])
    y_refra = np.array([0, -3 * np.cos(theta2)])
    ax.plot(x_refra, y_refra, color='green', lw=2.5, label='Raio Refratado')
    
    # Estética do gráfico principal
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_title(f"Reflexão e Refração da Luz (Ângulo Incidente: {angulo_inc_graus}°)", fontsize=12)
    ax.legend(loc='upper left', fontsize=8)
    
    # 3. Desenhar o Quadro de Detalhe (Frentes de Onda na Interface)
    ax_inset.axhline(0, color='blue', lw=1.5)
    ax_inset.axvline(0, color='gray', linestyle='--', alpha=0.5)
    
    # Gerar várias frentes de onda paralelas
    # A distância entre frentes (comprimento de onda \lambda) encurta no meio mais denso
    lambda1 = 0.3  # No ar
    lambda2 = lambda1 * (n1 / n2)  # No vidro ( \lambda_2 = \lambda_1 / n_2 )
    
    # Direções perpendiculares aos raios (direção da frente de onda)
    # Frente incidente: perpendicular ao raio incidente
    for i in range(-5, 6):
        d = i * lambda1
        # Equação da reta da frente de onda: x*sin(theta) - y*cos(theta) = d
        x_vals = np.linspace(-1, 1, 100)
        y_vals = (x_vals * np.sin(theta1) - d) / np.cos(theta1)
        # Mostrar apenas acima da interface (Ar)
        mask = y_vals >= 0
        if np.any(mask):
            ax_inset.plot(x_vals[mask], y_vals[mask], color='red', alpha=0.4, lw=1)
            
        # Frentes Refratadas (Vidro)
        d2 = i * lambda2
        y_vals_refra = (x_vals * np.sin(theta2) - d2) / np.cos(theta2)
        mask_refra = y_vals_refra <= 0
        if np.any(mask_refra):
            ax_inset.plot(x_vals[mask_refra], y_vals_refra[mask_refra], color='green', alpha=0.4, lw=1)

    # Estética do Inset
    ax_inset.set_xlim(-0.8, 0.8)
    ax_inset.set_ylim(-0.8, 0.8)
    ax_inset.set_aspect('equal')
    ax_inset.set_title("Frentes de Onda", fontsize=9)
    ax_inset.tick_params(axis='both', which='both', labelsize=7)
    
    fig.canvas.draw_idle()

# Configuração inicial
atualizar_simulacao(45)

# Criar o Slider decorativo abaixo do gráfico
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_angulo = Slider(ax_slider, 'Ângulo de Incidência (°)', 0.0, 85.0, valinit=45.0, valstep=1.0)

# Ligar o evento de mudança ao slider
slider_angulo.on_changed(atualizar_simulacao)

plt.show()