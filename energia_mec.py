import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Configurações da Janela
WIDTH, HEIGHT = 920, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Conservação de Energia Mecânica")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Segoe UI', 14, bold=True)

# Parâmetros Físicos Alteráveis
g = 9.8
mass = 1.0
mu = 0.00
pxToMeter = 50.0
groundY = 350.0
dt = 0.016  # Passo de tempo fixo

# Geometria da Pista
points = [
    [50, 100],   # Extremidade Esquerda
    [250, groundY], # Início do Plano Horizontal
    [550, groundY], # Fim do Plano Horizontal
    [750, 120]   # Extremidade Direita
]

# Estado da Esfera
ball = {"x": 50.0, "y": 100.0, "sVel": 0.0, "radius": 12}
thermalEnergy = 0.0
initialMechanicEnergy = 0.0
isPlaying = True

# Variáveis de Interação
isDraggingBall = False
activePoint = None

def get_track_data(x):
    if x <= points[0][0]: return points[0][1], 0.0
    if x >= points[3][0]: return points[3][1], 0.0
    for i in range(len(points) - 1):
        if points[i][0] <= x <= points[i+1][0]:
            p1, p2 = points[i], points[i+1]
            slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
            y = p1[1] + slope * (x - p1[0])
            return y, slope
    return groundY, 0.0

def x_to_s(x):
    s = 0.0
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        segLen = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        if p1[0] <= x <= p2[0]:
            pct = (x - p1[0]) / (p2[0] - p1[0])
            s += pct * segLen
            break
        else:
            s += segLen
    return s

def s_to_x(s):
    currentS = 0.0
    if s <= 0: return points[0][0]
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        segLen = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        if currentS + segLen >= s:
            rem = s - currentS
            pct = rem / segLen
            return p1[0] + pct * (p2[0] - p1[0])
        currentS += segLen
    return points[3][0]

def reset_energy_reference():
    global initialMechanicEnergy, thermalEnergy
    h = max(0.0, (groundY - ball["y"]) / pxToMeter)
    initialMechanicEnergy = mass * g * h
    thermalEnergy = 0.0

reset_energy_reference()

# Loop Principal do Sistema
while True:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get_events() if hasattr(pygame, 'get_events') else pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clique na bola
            if math.hypot(mx - ball["x"], my - (ball["y"] - ball["radius"])) < 22:
                isDraggingBall = True
                ball["sVel"] = 0.0
            # Clique nos pontos de controle (Apenas extremidades 0 e 3)
            for idx in [0, 3]:
                if math.hypot(mx - points[idx][0], my - points[idx][1]) < 18:
                    activePoint = points[idx]
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            isDraggingBall = False
            activePoint = None
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isPlaying = not isPlaying
            elif event.key == pygame.K_r:
                ball["x"], ball["y"] = points[0][0], points[0][1]
                ball["sVel"] = 0.0
                reset_energy_reference()

    # Atualização da Física de Euler-Cromer
    if isPlaying and not isDraggingBall and not activePoint:
        trackY, slope = get_track_data(ball["x"])
        angle = math.atan(slope)
        cosTheta = abs(math.cos(angle))
        
        accelGrav = g * math.sin(angle) * pxToMeter
        accelFric = mu * g * cosTheta * pxToMeter
        
        frictionForce = 0.0
        if abs(ball["sVel"]) > 0.01:
            frictionForce = -math.sign(ball["sVel"]) * accelFric if hasattr(math, 'sign') else (-accelFric if ball["sVel"] > 0 else accelFric)

        ball["sVel"] += (accelGrav + frictionForce) * dt
        
        currentS = x_to_s(ball["x"])
        nextS = currentS + ball["sVel"] * dt
        ball["x"] = s_to_x(nextS)
        
        # Inversões elásticas nas bordas
        if ball["x"] <= points[0][0]:
            ball["x"] = points[0][0]
            ball["sVel"] = -ball["sVel"]
        elif ball["x"] >= points[3][0]:
            ball["x"] = points[3][0]
            ball["sVel"] = -ball["sVel"]
            
        trackY, _ = get_track_data(ball["x"])
        ball["y"] = trackY
        
        ds = abs(nextS - currentS) / pxToMeter
        thermalEnergy += mu * mass * g * cosTheta * ds
        
        if slope == 0 and abs(ball["sVel"]) < 0.3 and mu > 0:
            ball["sVel"] = 0.0

    elif isDraggingBall:
        ball["x"] = max(points[0][0], min(mx, points[3][0]))
        ball["y"], _ = get_track_data(ball["x"])
        reset_energy_reference()
        
    elif activePoint:
        activePoint[1] = max(50.0, min(my, groundY - 20.0))
        ball["y"], _ = get_track_data(ball["x"])
        reset_energy_reference()

    # --- Desenho da Interface ---
    screen.fill((248, 249, 250))
    
    # Linha de Solo pontilhada
    for x in range(0, WIDTH, 10):
        pygame.draw.line(screen, (226, 232, 240), (x, groundY), (x+5, groundY), 1)

    # Desenho da Calha
    pygame.draw.lines(screen, (44, 62, 80), False, points, 5)
    
    # Pontos de controle vermelhos
    for idx in [0, 3]:
        pygame.draw.circle(screen, (231, 76, 60), points[idx], 8)
        pygame.draw.circle(screen, (192, 57, 43), points[idx], 8, 2)
        
    # Desenho da Esfera Azul
    pygame.draw.circle(screen, (52, 152, 219), (int(ball["x"]), int(ball["y"] - ball["radius"])), ball["radius"])
    pygame.draw.circle(screen, (41, 128, 185), (int(ball["x"]), int(ball["y"] - ball["radius"])), ball["radius"], 2)

    # --- Cálculos Analíticos Estáveis para o Dashboard ---
    h = max(0.0, (groundY - ball["y"]) / pxToMeter)
    ep = mass * g * h
    emec = max(0.0, initialMechanicEnergy - thermalEnergy) if mu > 0 else initialMechanicEnergy
    ek = max(0.0, emec - ep)

    # Renderização de Texto (Dashboard)
    data_labels = [f"U: {ep:.1f} J", f"K: {ek:.1f} J", f"E. Mec: {emec:.1f} J", f"Calor: {thermalEnergy:.1f} J"]
    colors = [(231, 76, 60), (52, 152, 219), (46, 204, 113), (243, 156, 18)]
    
    for i, text in enumerate(data_labels):
        txt_surface = font.render(text, True, colors[i])
        screen.blit(txt_surface, (50 + i*130, 20))

    # --- Renderização Gráfica de Barras Dinâmicas ---
    maxDisplayE = max(10.0, initialMechanicEnergy)
    bar_x_base = 820
    bar_width = 16
    bar_max_height = 120
    
    energies = [ep, ek, emec, thermalEnergy]
    labels = ["U", "K", "E", "Q"]
    
    for i, energy in enumerate(energies):
        bar_height = (energy / maxDisplayE) * bar_max_height
        bx = bar_x_base + i * 24
        by = 160 - bar_height
        
        # Contentor cinzento de fundo
        pygame.draw.rect(screen, (238, 238, 238), (bx, 40, bar_width, bar_max_height))
        # Preenchimento colorido da barra
        pygame.draw.rect(screen, colors[i], (bx, by, bar_width, bar_height))
        # Label da barra
        lbl = font.render(labels[i], True, (44, 62, 80))
        screen.blit(lbl, (bx + 3, 165))

    pygame.display.flip()
    clock.tick(60)