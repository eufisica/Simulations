import pygame
import math
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets

# --- Configurações Iniciais ---
pygame.init()
LARGURA, ALTURA = 1000, 750
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Plano Inclinado - José Gonçalves (eufisica)")
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO  = (0, 0, 0)
AZUL_NORMAL = (0, 100, 255)
CIANO_VEL   = (0, 200, 200)
VERMELHO_BLOCO = (220, 20, 60)
VERDE_PESO  = (34, 139, 34)
CINZA_RAMPA = (200, 200, 200)
COR_MOLA    = (80, 80, 80)
FUNDO_INTERFACE = (240, 240, 240)

# --- Variáveis Físicas ---
gravidade = 9.81
distancia = 0  
velocidade = 0
em_movimento = False
k_mola = 70.0  
altura_bloco = 30 

# --- Widgets ---
slider_v0 = Slider(tela, 150, 600, 200, 15, min=0, max=30, step=0.1, initial=20)
label_v0 = TextBox(tela, 370, 590, 120, 35, fontSize=20, colour=FUNDO_INTERFACE)

slider_ang = Slider(tela, 150, 640, 200, 15, min=0, max=90, step=1, initial=20)
label_ang = TextBox(tela, 370, 630, 120, 35, fontSize=20, colour=FUNDO_INTERFACE)

slider_mu = Slider(tela, 150, 680, 200, 15, min=0, max=0.8, step=0.01, initial=0.05)
label_mu = TextBox(tela, 370, 670, 120, 35, fontSize=20, colour=FUNDO_INTERFACE)

for w in [label_v0, label_ang, label_mu]: w.disable()
font_bold = pygame.font.SysFont('Arial', 18, bold=True)

def desenhar_mola_centrada(surface, inicio, fim, angulo_rad, voltas=12):
    offset_x = (altura_bloco / 2) * math.sin(angulo_rad)
    offset_y = -(altura_bloco / 2) * math.cos(angulo_rad)
    p1 = (inicio[0] + offset_x, inicio[1] + offset_y)
    p2 = (fim[0] + offset_x, fim[1] + offset_y)
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist < 2: return
    pontos = []
    for i in range(voltas * 2 + 1):
        frac = i / (voltas * 2)
        perp_dist = 12 if (0 < i < voltas * 2) else 0
        off_x = -dy/dist * perp_dist if i % 2 == 1 else 0
        off_y = dx/dist * perp_dist if i % 2 == 1 else 0
        if i % 4 == 3: off_x, off_y = -off_x, -off_y
        pontos.append((p1[0] + dx * frac + off_x, p1[1] + dy * frac + off_y))
    pygame.draw.lines(surface, COR_MOLA, False, pontos, 3)
    pygame.draw.line(surface, PRETO, (p1[0]-15, p1[1]-15), (p1[0]+15, p1[1]+15), 6)

def desenhar_seta(surface, cor, origem, vetor):
    if math.hypot(*vetor) < 2: return
    fim = (origem[0] + vetor[0], origem[1] + vetor[1])
    pygame.draw.line(surface, cor, origem, fim, 4)
    angulo = math.atan2(vetor[1], vetor[0])
    p1 = (fim[0] - 10 * math.cos(angulo - 0.5), fim[1] - 10 * math.sin(angulo - 0.5))
    p2 = (fim[0] - 10 * math.cos(angulo + 0.5), fim[1] - 10 * math.sin(angulo + 0.5))
    pygame.draw.polygon(surface, cor, [fim, p1, p2])

def reset_simulacao():
    global distancia, velocidade, em_movimento
    distancia, velocidade, em_movimento = 0, slider_v0.getValue(), True

# --- Loop Principal ---
rodando = True
while rodando:
    tela.fill(BRANCO)
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT: rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE: reset_simulacao()

    v0_val, ang_val, mu_val = slider_v0.getValue(), slider_ang.getValue(), slider_mu.getValue()
    theta = math.radians(ang_val)
    label_v0.setText(f"{v0_val:.1f} m/s"); label_ang.setText(f"{ang_val} °"); label_mu.setText(f"μ = {mu_val:.2f}")

    rampa_m, escala = 25.0, 30 

    if em_movimento:
        dt = 1/60
        sentido = 1 if velocidade > 0 else -1
        a_total = -gravidade * math.sin(theta) - sentido * (mu_val * gravidade * math.cos(theta))
        if distancia > rampa_m:
            a_total += -(k_mola * (distancia - rampa_m))
        velocidade += a_total * dt
        distancia += velocidade * dt
        if distancia < 0: distancia, velocidade, em_movimento = 0, 0, False

    # Desenho Rampa
    origem = (100, 550)
    topo_rampa = (origem[0] + rampa_m * escala * math.cos(theta), origem[1] - rampa_m * escala * math.sin(theta))
    pygame.draw.polygon(tela, CINZA_RAMPA, [origem, (topo_rampa[0], origem[1]), topo_rampa])
    pygame.draw.line(tela, PRETO, origem, topo_rampa, 4)

    # Mola
    extensao_max = 3.5
    p_fixo = (topo_rampa[0] + extensao_max * escala * math.cos(theta), topo_rampa[1] - extensao_max * escala * math.sin(theta))
    p_contacto = (origem[0] + max(distancia, rampa_m) * escala * math.cos(theta), origem[1] - max(distancia, rampa_m) * escala * math.sin(theta))
    desenhar_mola_centrada(tela, p_fixo, p_contacto, theta)

    # Bloco e Vetores
    bx = origem[0] + (distancia * escala) * math.cos(theta)
    by = origem[1] - (distancia * escala) * math.sin(theta)
    
    # Peso (Verde) e Normal (Azul)
    desenhar_seta(tela, VERDE_PESO, (bx, by), (0, gravidade * 5))
    fn_mag = gravidade * math.cos(theta) * 5
    desenhar_seta(tela, AZUL_NORMAL, (bx, by), (-fn_mag * math.sin(theta), -fn_mag * math.cos(theta)))
    
    # Velocidade (Ciano)
    if abs(velocidade) > 0.1:
        desenhar_seta(tela, CIANO_VEL, (bx, by - 40), (velocidade*4*math.cos(theta), -velocidade*4*math.sin(theta)))

    # Desenho do Bloco
    bloco_surf = pygame.Surface((50, altura_bloco), pygame.SRCALPHA)
    bloco_surf.fill(VERMELHO_BLOCO)
    bloco_rot = pygame.transform.rotate(bloco_surf, ang_val)
    rect = bloco_rot.get_rect(center=(bx, by - altura_bloco/2 + 5))
    tela.blit(bloco_rot, rect)

    # --- INTERFACE E LEGENDA (CORRIGIDO) ---
    # Rótulos dos Sliders
    tela.blit(font_bold.render("Velocidade Inicial:", True, PRETO), (20, 570))
    tela.blit(font_bold.render("Ângulo do Plano:", True, PRETO), (20, 620))
    tela.blit(font_bold.render("Atrito:", True, PRETO), (20, 660))

    # Caixa da Legenda
    pygame.draw.rect(tela, FUNDO_INTERFACE, (550, 580, 420, 130))
    pygame.draw.rect(tela, PRETO, (550, 580, 420, 130), 2) # Borda
    
    # Textos da Legenda com Blit explícito
    tela.blit(font_bold.render("LEGENDA DE VETORES:", True, PRETO), (565, 590))
    tela.blit(font_bold.render("VERDE: Força Peso (P)", True, VERDE_PESO), (565, 615))
    tela.blit(font_bold.render("AZUL: Força Normal (N)", True, AZUL_NORMAL), (565, 640))
    tela.blit(font_bold.render("CIANO: Velocidade (v)", True, CIANO_VEL), (565, 665))
    tela.blit(font_bold.render("ESPAÇO: Disparar Bloco", True, PRETO), (565, 690))

    pygame_widgets.update(eventos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()