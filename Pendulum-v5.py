import sys
from collections import deque
import numpy as np
import pygame
from scipy.integrate import solve_ivp

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Configurações da Janela
WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dashboard Física: Dinâmica do Pêndulo Gravítico")
clock = pygame.time.Clock()

# Tipografia Moderna
FONT_SM = pygame.font.SysFont("Segoe UI", 13)
FONT_MED = pygame.font.SysFont("Segoe UI", 15)
FONT_BOLD = pygame.font.SysFont("Segoe UI", 15, bold=True)
TITLE_FONT = pygame.font.SysFont("Segoe UI", 24, bold=True)

# Palete de Cores (Sci-Fi / Tech Dashboard)
BG_COLOR = (15, 18, 26)         
PANEL_COLOR = (24, 29, 41)      
PANEL_BORDER = (40, 50, 70)     
TEXT_MAIN = (230, 235, 245)     
TEXT_MUTED = (110, 125, 150)    

# Cores dos Elementos Ativos
BLUE_NEON = (0, 191, 255)       
RED_NEON = (255, 46, 99)        
GREEN_ACCENT = (0, 225, 140)    
DARK_GRAY = (50, 55, 65)

# Constantes Físicas
G = 9.81
PIXELS_PER_METER = 130

# Estado Inicial
length = 1.5
theta0_small = np.radians(10)   # Fixo < 10°
theta0_large = np.radians(60)   # Customizável

# Controlo de Simulação
time_elapsed = 0.0
fps = 60
dt = 1.0 / fps
is_paused = False

# Histórico para o Gráfico de x(t)
max_history = 300
history_small = deque(maxlen=max_history)
history_large = deque(maxlen=max_history)

# Elementos de Interface (UI) - Sliders posicionados e dimensionados com precisão
s_len_x, s_len_y, s_len_w, s_len_h = 160, 575, 200, 8
s_ang_x, s_ang_y, s_ang_w, s_ang_h = 160, 625, 200, 8
val_len = 0.5  # Escala (0.5m a 2.5m), 0.5 significa 1.5m
val_ang = 0.625 # Escala (10° a 90°), 0.625 significa 60°

btn_pause_rect = pygame.Rect(450, 570, 110, 38)
btn_reset_rect = pygame.Rect(575, 570, 110, 38)

dragging_len = False
dragging_ang = False

def get_large_angle(t, l, th0):
    """Física Real (Não-linear)"""
    if t <= 0:
        return th0
    def equations(t, y):
        return [y[1], -(G / l) * np.sin(y[0])]
    sol = solve_ivp(equations, [0, t], [th0, 0.0], t_eval=[t], rtol=1e-5, atol=1e-7)
    return sol.y[0][0] if sol.y.shape[1] > 0 else th0

def get_small_angle(t, l, th0):
    """Aproximação Linear"""
    omega_0 = np.sqrt(G / l)
    return th0 * np.cos(omega_0 * t)

def calculate_periods(l, th0):
    """Calcula os períodos teóricos"""
    T_small = 2 * np.pi * np.sqrt(l / G)
    T_large = T_small * (1 + (1 / 16) * th0**2 + (11 / 3072) * th0**4 + (173 / 737280) * th0**6)
    return T_small, T_large

def draw_grid(surface, rect, size=24):
    """Desenha uma grelha técnica de fundo para o gráfico"""
    for x in range(rect.x, rect.x + rect.width, size):
        pygame.draw.line(surface, (30, 38, 54), (x, rect.y), (x, rect.y + rect.height), 1)
    for y in range(rect.y, rect.y + rect.height, size):
        pygame.draw.line(surface, (30, 38, 54), (rect.x, y), (rect.x + rect.width, y), 1)

def reset_graph_buffers():
    """Garante que as filas nunca ficam vazias, prevenindo erros ao desenhar em pausa"""
    history_small.clear()
    history_large.clear()
    history_small.append(length * np.sin(theta0_small))
    history_large.append(length * np.sin(theta0_large))

# Inicialização dos buffers de dados
reset_graph_buffers()

# Loop Principal
running = True
while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    # --- Gestão de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Tolerância de clique alargada na vertical (+-10px) para melhorar a experiência do utilizador
            if s_len_x <= mouse_pos[0] <= s_len_x + s_len_w and s_len_y - 10 <= mouse_pos[1] <= s_len_y + 10:
                dragging_len = True
            if s_ang_x <= mouse_pos[0] <= s_ang_x + s_ang_w and s_ang_y - 10 <= mouse_pos[1] <= s_ang_y + 10:
                dragging_ang = True

            if btn_pause_rect.collidepoint(mouse_pos):
                is_paused = not is_paused
            if btn_reset_rect.collidepoint(mouse_pos):
                time_elapsed = 0.0
                reset_graph_buffers()

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_len = False
            dragging_ang = False

    # Ajustes e Arrastamento dos Sliders (Funciona em tempo real, mesmo em PAUSA)
    reset_physics = False
    if dragging_len:
        val_x = max(s_len_x, min(mouse_pos[0], s_len_x + s_len_w))
        val_len = (val_x - s_len_x) / s_len_w
        length = 0.5 + val_len * 2.0  # Mapeia para intervalo de 0.5m a 2.5m
        reset_physics = True

    if dragging_ang:
        val_x = max(s_ang_x, min(mouse_pos[0], s_ang_x + s_ang_w))
        val_ang = (val_x - s_ang_x) / s_ang_w
        theta0_large = np.radians(10 + val_ang * 80)  # Mapeia para intervalo de 10° a 90°
        reset_physics = True

    if reset_physics:
        time_elapsed = 0.0
        reset_graph_buffers()

    # --- Execução da Física ---
    if not is_paused:
        time_elapsed += dt
        theta_small = get_small_angle(time_elapsed, length, theta0_small)
        theta_large = get_large_angle(time_elapsed, length, theta0_large)
        
        # Guardar dados para renderização do gráfico
        history_small.append(length * np.sin(theta_small))
        history_large.append(length * np.sin(theta_large))
    else:
        # Se estiver pausado, calcula a posição estática correspondente ao ponto atual do tempo
        theta_small = get_small_angle(time_elapsed, length, theta0_small)
        theta_large = get_large_angle(time_elapsed, length, theta0_large)

    # --- Renderização Gráfica ---

    # Cabeçalho
    lbl_title = TITLE_FONT.render("Estudo Dinâmico do Pêndulo Gravítico", True, TEXT_MAIN)
    screen.blit(lbl_title, (30, 25))
    pygame.draw.line(screen, PANEL_BORDER, (30, 70), (WIDTH - 30, 70), 1)

    # --- PAINEL 1: Pêndulos Virtuais (Esquerda) ---
    panel_anim = pygame.Rect(30, 95, 520, 360)
    pygame.draw.rect(screen, PANEL_COLOR, panel_anim, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, panel_anim, 1, border_radius=8)
    
    anim_center_x, anim_center_y = panel_anim.centerx, panel_anim.y + 30
    pygame.draw.line(screen, TEXT_MUTED, (anim_center_x - 80, anim_center_y), (anim_center_x + 80, anim_center_y), 2)

    p_len = length * PIXELS_PER_METER
    
    # Pêndulo Linear (Azul)
    pos_x_sm = anim_center_x + p_len * np.sin(theta_small)
    pos_y_sm = anim_center_y + p_len * np.cos(theta_small)
    pygame.draw.line(screen, BLUE_NEON, (anim_center_x, anim_center_y), (pos_x_sm, pos_y_sm), 2)
    pygame.draw.circle(screen, BLUE_NEON, (int(pos_x_sm), int(pos_y_sm)), 11)

    # Pêndulo Real (Vermelho)
    pos_x_lg = anim_center_x + p_len * np.sin(theta_large)
    pos_y_lg = anim_center_y + p_len * np.cos(theta_large)
    pygame.draw.line(screen, RED_NEON, (anim_center_x, anim_center_y), (pos_x_lg, pos_y_lg), 2)
    pygame.draw.circle(screen, RED_NEON, (int(pos_x_lg), int(pos_y_lg)), 11)

    # --- PAINEL 2: Gráfico x(t) em Tempo Real (Direita) ---
    graph_rect = pygame.Rect(580, 95, 590, 360)
    pygame.draw.rect(screen, PANEL_COLOR, graph_rect, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, graph_rect, 1, border_radius=8)
    draw_grid(screen, graph_rect, size=24)

    # Linha média (Equilíbrio x = 0)
    pygame.draw.line(screen, PANEL_BORDER, (graph_rect.x, graph_rect.centery), (graph_rect.x + graph_rect.width, graph_rect.centery), 2)

    screen.blit(FONT_BOLD.render("Gráfico Estatístico: Posição Horizontal x(t)", True, TEXT_MAIN), (graph_rect.x + 15, graph_rect.y + 12))
    screen.blit(FONT_SM.render("+x (Direita)", True, TEXT_MUTED), (graph_rect.x + 15, graph_rect.y + 40))
    screen.blit(FONT_SM.render("-x (Esquerda)", True, TEXT_MUTED), (graph_rect.x + 15, graph_rect.bottom - 55))

    scale_y = graph_rect.height / 5.5  

    # Desenho das curvas temporais (Protegido contra buffers unitários ou vazios)
    if len(history_small) > 1:
        for idx in range(1, len(history_small)):
            x1 = graph_rect.x + (idx - 1) * (graph_rect.width / max_history)
            y1 = graph_rect.centery - (history_small[idx - 1] * scale_y)
            x2 = graph_rect.x + idx * (graph_rect.width / max_history)
            y2 = graph_rect.centery - (history_small[idx] * scale_y)
            pygame.draw.line(screen, BLUE_NEON, (x1, y1), (x2, y2), 2)

    if len(history_large) > 1:
        for idx in range(1, len(history_large)):
            x1 = graph_rect.x + (idx - 1) * (graph_rect.width / max_history)
            y1 = graph_rect.centery - (history_large[idx - 1] * scale_y)
            x2 = graph_rect.x + idx * (graph_rect.width / max_history)
            y2 = graph_rect.centery - (history_large[idx] * scale_y)
            pygame.draw.line(screen, RED_NEON, (x1, y1), (x2, y2), 2)

    # --- PAINEL 3: Displays Digitais de Telemetria ---
    T_sm, T_lg = calculate_periods(length, theta0_large)
    f_sm, f_lg = 1 / T_sm, 1 / T_lg

    # Painel Pequenos Ângulos (MHS)
    box_blue = pygame.Rect(30, 470, 250, 68)
    pygame.draw.rect(screen, PANEL_COLOR, box_blue, border_radius=6)
    pygame.draw.rect(screen, BLUE_NEON, box_blue, 1, border_radius=6)
    screen.blit(FONT_BOLD.render("Modelo Linear (Fixo 10°)", True, BLUE_NEON), (40, 476))
    screen.blit(FONT_SM.render(f"Período (T): {T_sm:.3f} s", True, TEXT_MAIN), (40, 496))
    screen.blit(FONT_SM.render(f"Frequência (f): {f_sm:.2f} Hz", True, TEXT_MAIN), (40, 514))

    # Painel Grandes Ângulos (Real)
    box_red = pygame.Rect(300, 470, 250, 68)
    pygame.draw.rect(screen, PANEL_COLOR, box_red, border_radius=6)
    pygame.draw.rect(screen, RED_NEON, box_red, 1, border_radius=6)
    screen.blit(FONT_BOLD.render("Modelo Real (Não-Linear)", True, RED_NEON), (310, 476))
    screen.blit(FONT_SM.render(f"Período (T): {T_lg:.3f} s", True, TEXT_MAIN), (310, 496))
    screen.blit(FONT_SM.render(f"Frequência (f): {f_lg:.2f} Hz", True, TEXT_MAIN), (310, 514))

    # --- PAINEL 4: Controlos Gerais Interativos ---
    panel_ctrl = pygame.Rect(30, 550, WIDTH - 60, 140)
    pygame.draw.rect(screen, PANEL_COLOR, panel_ctrl, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, panel_ctrl, 1, border_radius=8)

    # Slider 1: Comprimento do Fio
    screen.blit(FONT_MED.render(f"Comprimento (L): {length:.2f} m", True, TEXT_MAIN), (50, 545))
    pygame.draw.rect(screen, DARK_GRAY, (s_len_x, s_len_y, s_len_w, s_len_h), border_radius=2)
    pygame.draw.circle(screen, TEXT_MAIN, (s_len_x + int(val_len * s_len_w), s_len_y + 4), 7)

    # Slider 2: Ângulo Inicial Máximo do Vermelho
    screen.blit(FONT_MED.render(f"Ângulo Inicial: {np.degrees(theta0_large):.1f}°", True, TEXT_MAIN), (50, 595))
    pygame.draw.rect(screen, DARK_GRAY, (s_ang_x, s_ang_y, s_ang_w, s_ang_h), border_radius=2)
    pygame.draw.circle(screen, TEXT_MAIN, (s_ang_x + int(val_ang * s_ang_w), s_ang_y + 4), 7)

    # Botão Play/Pausa
    pause_color = DARK_GRAY if is_paused else GREEN_ACCENT
    pygame.draw.rect(screen, pause_color, btn_pause_rect, border_radius=6)
    txt_pause = "PLAY" if is_paused else "PAUSA"
    lbl_btn_p = FONT_BOLD.render(txt_pause, True, BG_COLOR if not is_paused else TEXT_MAIN)
    screen.blit(lbl_btn_p, (btn_pause_rect.centerx - lbl_btn_p.get_width()//2, btn_pause_rect.centery - lbl_btn_p.get_height()//2))

    # Botão Reiniciar
    pygame.draw.rect(screen, RED_NEON, btn_reset_rect, border_radius=6)
    lbl_btn_r = FONT_BOLD.render("REINICIAR", True, TEXT_MAIN)
    screen.blit(lbl_btn_r, (btn_reset_rect.centerx - lbl_btn_r.get_width()//2, btn_reset_rect.centery - lbl_btn_r.get_height()//2))

    # Textos de Análise Técnica
    screen.blit(FONT_BOLD.render("Observação Teórica:", True, TEXT_MAIN), (620, 610))
    screen.blit(FONT_SM.render("Nota como em amplitudes elevadas a linha vermelha perde frequência em relação à azul.", True, TEXT_MUTED), (620, 630))
    screen.blit(FONT_SM.render("Isto ocorre porque a aproximação linear sin(theta) ~ theta falha e despreza o atraso real.", True, TEXT_MUTED), (620, 650))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()