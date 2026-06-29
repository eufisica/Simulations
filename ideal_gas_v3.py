import pygame
import random
import math

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# --- Configurações da Janela e Cores ---
WIDTH, HEIGHT = 1100, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Gás Ideal (Unidades SI) - eufisica")
clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (210, 210, 210)
DARK_GRAY = (70, 70, 70)
RED = (230, 50, 50)
BLUE = (50, 120, 230)
GREEN = (40, 170, 90)

FONT_SMALL = pygame.font.SysFont("Arial", 13)
FONT_MEDIUM = pygame.font.SysFont("Arial", 16, bold=True)
FONT_LARGE = pygame.font.SysFont("Arial", 20, bold=True)

# --- Fatores de Escala Física (SI) ---
PX_PER_METER = 500.0  # 500 píxeis = 1 metro
DT = 0.0001            # Passo de tempo por frame em segundos (10^-4 s)
U_TO_KG = 1.66e-27     # 1 unidade de massa atómica em kg

# Variável global para acumular a força exercida nas paredes (para cálculo da Pressão)
total_wall_impulse = 0.0

# --- Classe Slider Interativo ---
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label, unit="", is_float=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.label = label
        self.unit = unit
        self.is_float = is_float
        self.active = False
        self.button_radius = 8
        self.update_button_pos()

    def update_button_pos(self):
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.button_x = self.rect.x + int(ratio * self.rect.width)
        self.button_y = self.rect.y + self.rect.height // 2

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect, border_radius=4)
        pygame.draw.rect(surface, DARK_GRAY, (self.rect.x, self.rect.y, self.button_x - self.rect.x, self.rect.height), border_radius=4)
        pygame.draw.circle(surface, BLUE if self.active else DARK_GRAY, (self.button_x, self.button_y), self.button_radius)
        
        val_str = f"{self.val:.2f}" if self.is_float else f"{int(self.val)}"
        txt = FONT_SMALL.render(f"{self.label}: {val_str} {self.unit}", True, BLACK)
        surface.blit(txt, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.inflate(10, 20).collidepoint(event.pos):
                self.active = True
                self.update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.active = False
        elif event.type == pygame.MOUSEMOTION and self.active:
            self.update_value(event.pos[0])
            return True
        return False

    def update_value(self, mouse_x):
        mouse_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
        ratio = (mouse_x - self.rect.x) / self.rect.width
        self.val = self.min_val + ratio * (self.max_val - self.min_val)
        self.button_x = mouse_x

# --- Classe Partícula ---
class Particle:
    def __init__(self, x, y, vx_si, vy_si, mass_u):
        self.x = x
        self.y = y
        self.vx_si = vx_si  # Velocidade em m/s
        self.vy_si = vy_si  # Velocidade em m/s
        self.mass_u = mass_u
        self.radius = int(4 * math.sqrt(mass_u))

    def move(self, box_w_m, box_h_m):
        global total_wall_impulse
        
        # Converter m/s para píxeis/frame para atualizar a posição gráfica
        vx_px = self.vx_si * PX_PER_METER * DT
        vy_px = self.vy_si * PX_PER_METER * DT

        self.x += vx_px
        self.y += vy_px

        box_x_min, box_y_min = 50, 80
        box_x_max = box_x_min + box_w_m * PX_PER_METER
        box_y_max = box_y_min + box_h_m * PX_PER_METER

        mass_kg = self.mass_u * U_TO_KG

        # Colisões com Paredes Laterais (acumula Impulso: F*dt = 2*m*v)
        if self.x - self.radius < box_x_min:
            self.x = box_x_min + self.radius
            self.vx_si *= -1
            total_wall_impulse += 2 * mass_kg * abs(self.vx_si)
        elif self.x + self.radius > box_x_max:
            self.x = box_x_max - self.radius
            self.vx_si *= -1
            total_wall_impulse += 2 * mass_kg * abs(self.vx_si)

        # Colisões com Paredes Verticais
        if self.y - self.radius < box_y_min:
            self.y = box_y_min + self.radius
            self.vy_si *= -1
            total_wall_impulse += 2 * mass_kg * abs(self.vy_si)
        elif self.y + self.radius > box_y_max:
            self.y = box_y_max - self.radius
            self.vy_si *= -1
            total_wall_impulse += 2 * mass_kg * abs(self.vy_si)

    def draw(self, surface):
        speed = math.hypot(self.vx_si, self.vy_si)
        factor = min(speed / 300.0, 1.0)  # Normalização visual baseada em 300 m/s
        color = (int(50 + 180 * factor), 100, int(230 - 180 * factor))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)

# --- Inicialização do Gás ---
def init_particles(n, temp, mass_u, box_w_m, box_h_m):
    particles = []
    box_x_min, box_y_min = 50, 80
    box_w_px = box_w_m * PX_PER_METER
    box_h_px = box_h_m * PX_PER_METER
    
    # Relação Cinética Real: v_quadrática_média = sqrt(2 * k_B * T / m)
    # Ajustamos um fator de escala para que as velocidades fiquem na ordem dos ~100-400 m/s
    v_scale = 12.0 * math.sqrt(temp / mass_u) 
    
    for _ in range(int(n)):
        max_r = int(4 * math.sqrt(mass_u))
        x = random.uniform(box_x_min + max_r + 5, box_x_min + box_w_px - max_r - 5)
        y = random.uniform(box_y_min + max_r + 5, box_y_min + box_h_px - max_r - 5)
        
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5 * v_scale, 1.5 * v_scale)
        vx_si = speed * math.cos(angle)
        vy_si = speed * math.sin(angle)
        
        particles.append(Particle(x, y, vx_si, vy_si, mass_u))
    return particles

def resolve_collisions(particles):
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = particles[i], particles[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist = math.hypot(dx, dy)
            min_dist = p1.radius + p2.radius
            
            if dist < min_dist:
                overlap = min_dist - dist
                if dist == 0: dist = 0.1
                nx, ny = dx / dist, dy / dist
                
                m_total = p1.mass_u + p2.mass_u
                p1.x -= nx * overlap * (p2.mass_u / m_total)
                p1.y -= ny * overlap * (p2.mass_u / m_total)
                p2.x += nx * overlap * (p1.mass_u / m_total)
                p2.y += ny * overlap * (p1.mass_u / m_total)
                
                # Colisão em m/s (Unidades SI)
                kx = p1.vx_si - p2.vx_si
                ky = p1.vy_si - p2.vy_si
                p = 2 * (nx * kx + ny * ky) / m_total
                
                p1.vx_si -= p * p2.mass_u * nx
                p1.vy_si -= p * p2.mass_u * ny
                p2.vx_si += p * p1.mass_u * nx
                p2.vy_si += p * p1.mass_u * ny

# --- Configuração dos Sliders (Métricas SI) ---
sliders = [
    Slider(720, 100, 320, 10, 100, 600, 300, "Temperatura", "K"),
    Slider(720, 160, 320, 10, 0.4, 1.0, 0.8, "Largura da Caixa", "m", is_float=True),
    Slider(720, 220, 320, 10, 1, 10, 4, "Massa das Partículas", "u"),
    Slider(720, 280, 320, 10, 10, 250, 100, "Número de Partículas (N)", "")
]

# Estado inicial
temp_val = sliders[0].val
box_w_m = sliders[1].val
box_h_m = box_w_m  # Caixa quadrada bidimensional
mass_val = sliders[2].val
num_part_val = sliders[3].val

particles = init_particles(num_part_val, temp_val, mass_val, box_w_m, box_h_m)

# Variáveis para média móvel da pressão estabilizada
pressure_history = []
running = True

# --- Loop Principal ---
while running:
    screen.fill(WHITE)
    total_wall_impulse = 0.0  # Reset do impulso no início do frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        for slider in sliders:
            if slider.handle_event(event):
                temp_val = sliders[0].val
                box_w_m = sliders[1].val
                box_h_m = box_w_m
                mass_val = sliders[2].val
                num_part_val = sliders[3].val
                particles = init_particles(num_part_val, temp_val, mass_val, box_w_m, box_h_m)
                pressure_history.clear()

    # Atualização física
    for _ in range(2):
        for p in particles:
            p.move(box_w_m, box_h_m)
        resolve_collisions(particles)

    # Cálculo Físico de Pressão Real: P = Força / Perímetro (em 2D) = (Impulso / DT) / Perímetro
    # Convertido para representar uma ordem de magnitude macroscópica em Pascal (Pa)
    perimeter_m = 2 * (box_w_m + box_h_m)
    calculated_force = total_wall_impulse / DT
    instantaneous_pressure = calculated_force / perimeter_m if perimeter_m > 0 else 0
    
    # Amplificação estatística meramente de representação do volume infinito
    real_pressure_pa = instantaneous_pressure * 1e24  
    pressure_history.append(real_pressure_pa)
    if len(pressure_history) > 30: pressure_history.pop(0)
    avg_pressure_pa = sum(pressure_history) / len(pressure_history)

    # Área Real (m²)
    area_m2 = box_w_m * box_h_m
    
    # Velocidade Média Real (m/s)
    avg_speed_si = sum(math.hypot(p.vx_si, p.vy_si) for p in particles) / max(1, len(particles))

    # --- Renderização Gráfica ---
    # Desenhar Caixa de acordo com a métrica de píxeis calculada
    box_w_px = int(box_w_m * PX_PER_METER)
    box_h_px = int(box_h_m * PX_PER_METER)
    pygame.draw.rect(screen, BLACK, (50, 80, box_w_px, box_h_px), 3)
    
    for p in particles:
        p.draw(screen)
        
    for slider in sliders:
        slider.draw(screen)

    # Painel de Dados SI
    title = FONT_LARGE.render("Termodinâmica Estatística no Sistema Internacional (SI)", True, BLACK)
    screen.blit(title, (50, 25))
    
    pygame.draw.rect(screen, GRAY, (720, 330, 320, 115), border_radius=5)
    
    txt_larg = FONT_MEDIUM.render(f"Largura da Caixa: {box_w_m:.2f} m", True, DARK_GRAY)
    txt_area = FONT_MEDIUM.render(f"Área Ocupada (A): {area_m2:.2f} m²", True, DARK_GRAY)
    txt_vel = FONT_MEDIUM.render(f"Velocidade Média (<v>): {avg_speed_si:.1f} m/s", True, DARK_GRAY)
    txt_pres = FONT_MEDIUM.render(f"Pressão Média (P): {avg_pressure_pa:.1f} Pa (N/m²)", True, RED)
    
    screen.blit(txt_larg, (735, 340))
    screen.blit(txt_area, (735, 365))
    screen.blit(txt_vel, (735, 390))
    screen.blit(txt_pres, (735, 415))

    # --- Histograma Real Maxwell-Boltzmann (m/s) ---
    GRAF_X, GRAF_Y = 720, 495
    GRAF_W, GRAF_H = 320, 125
    pygame.draw.rect(screen, BLACK, (GRAF_X, GRAF_Y, GRAF_W, GRAF_H), 2)
    
    lbl_g = FONT_SMALL.render("Distribuição de Velocidades f(v) [m/s]", True, DARK_GRAY)
    screen.blit(lbl_g, (GRAF_X, GRAF_Y - 20))

    num_bins = 16
    bins = [0] * num_bins
    max_v_graf = 500.0  # Limite de renderização de velocidade 500 m/s
    bin_width = max_v_graf / num_bins
    
    for p in particles:
        v = math.hypot(p.vx_si, p.vy_si)
        bin_idx = int(v / bin_width)
        if bin_idx >= num_bins: bin_idx = num_bins - 1
        bins[bin_idx] += 1
        
    max_count = max(bins) if max(bins) > 0 else 1
    bar_w = GRAF_W / num_bins
    
    for i in range(num_bins):
        bar_h = (bins[i] / max_count) * (GRAF_H - 15)
        bx = GRAF_X + i * bar_w
        by = GRAF_Y + GRAF_H - bar_h
        pygame.draw.rect(screen, GREEN, (bx + 1, by, bar_w - 2, bar_h))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()