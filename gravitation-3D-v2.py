import pygame
import math
import sys

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Configurações da Janela
WIDTH, HEIGHT = 1220, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Órbitas 3D - José Gonçalves (eufisica)")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Segoe UI", 13)
FONT_BOLD = pygame.font.SysFont("Segoe UI", 14, bold=True)

# Cores
BG_COLOR = (11, 14, 20)
PANEL_COLOR = (206, 214, 206)
GROUP_COLOR = (189, 199, 189)
TEXT_COLOR = (43, 58, 43)
WHITE = (255, 255, 255)

# Constantes Físicas Calibradas
G = 10.0
DT = 0.002

class Body:
    def __init__(self, x, y, z, vx, vy, vz, mass, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
        self.radius = radius
        self.color = color
        self.history = []  # Armazena tuplos (x, y, z) para a trajetória

class Slider:
    def __init__(self, x, y, w, min_val, max_val, curr_val, label, step=0.1):
        self.rect = pygame.Rect(x, y, w, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.curr_val = curr_val
        self.label = label
        self.step = step
        self.handle_x = x + int((curr_val - min_val) / (max_val - min_val) * w)
        self.active = False

    def draw(self, surf):
        pygame.draw.rect(surf, (150, 160, 150), self.rect, border_radius=4)
        pygame.draw.circle(surf, (80, 90, 80), (self.handle_x, self.rect.centery), 7)
        val_str = f"{self.curr_val:.1f}" if self.step >= 0.1 else f"{self.curr_val:.0f}"
        txt = FONT.render(f"{self.label}: {val_str}", True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x, self.rect.y - 18))

    def update(self, mx, my, click):
        if click and self.rect.inflate(20, 20).collidepoint(mx, my):
            self.active = True
        if not click:
            self.active = False
            
        if self.active:
            self.handle_x = max(self.rect.x, min(mx, self.rect.x + self.rect.w))
            rel = (self.handle_x - self.rect.x) / self.rect.w
            val = self.min_val + rel * (self.max_val - self.min_val)
            self.curr_val = round(val / self.step) * self.step
            return True
        return False

class Checkbox:
    def __init__(self, x, y, label, checked=True):
        self.rect = pygame.Rect(x, y, 14, 14)
        self.label = label
        self.checked = checked

    def draw(self, surf):
        pygame.draw.rect(surf, (240, 240, 240), self.rect, border_radius=3)
        pygame.draw.rect(surf, (100, 110, 100), self.rect, 1, border_radius=3)
        if self.checked:
            pygame.draw.rect(surf, (43, 58, 43), self.rect.inflate(-6, -6), border_radius=1)
        txt = FONT.render(self.label, True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x + 20, self.rect.y - 1))

    def handle_event(self, mx, my, click):
        if click and self.rect.collidepoint(mx, my):
            self.checked = not self.checked
            return True
        return False

# Parâmetros Globais da Câmara 3D
cam_yaw = 0.5   
cam_pitch = 0.6 
cam_zoom = 16.0 

def project_3d(x, y, z):
    """ Projeta coordenadas 3D para o plano 2D da tela com matriz de rotação básica """
    x1 = x * math.cos(cam_yaw) - z * math.sin(cam_yaw)
    z1 = x * math.sin(cam_yaw) + z * math.cos(cam_yaw)
    
    y2 = y * math.cos(cam_pitch) - z1 * math.sin(cam_pitch)
    z2 = y * math.sin(cam_pitch) + z1 * math.cos(cam_pitch)
    
    scale = cam_zoom * 50 / (z2 + 200) 
    screen_x = int(450 + x1 * scale)
    screen_y = int(300 - y2 * scale)
    return screen_x, screen_y, z2

def init_bodies(sliders):
    m1 = sliders['m1'].curr_val * 100
    m2 = sliders['m2'].curr_val * 0.1
    m3 = sliders['m3'].curr_val * 0.1
    m4 = sliders['m4'].curr_val * 0.1
    m5 = sliders['m5'].curr_val * 0.1

    def get_v_obj(r): return math.sqrt((G * m1) / r)

    r2, r3, r4, r5 = 6.5, 10.5, 15.0, 19.5

    raw_configs = [
        # O Sol foi reduzido de raio 18 para 10
        {'x': 0,   'y': 0, 'z': 0,   'vx': 0,                'vy': 0, 'vz': 0,               'mass': m1, 'rad': 10, 'color': (252, 196, 25)},
        # Planetas com raios mais discretos (4, 4, 5, 6)
        {'x': r2,  'y': 0, 'z': 0,   'vx': 0,                'vy': 0, 'vz': get_v_obj(r2),   'mass': m2, 'rad': 4,  'color': (28, 126, 214)},
        # PLANETA RETRÓGRADO: Inversão do vetor de velocidade inicial (-get_v_obj) para orbitar no sentido oposto
        {'x': 0,   'y': 0, 'z': r3,  'vx': -get_v_obj(r3)*0.85,'vy': 0, 'vz': 0,              'mass': m3, 'rad': 4,  'color': (43, 138, 62)},
        {'x': -r4, 'y': 0, 'z': 0,   'vx': 0,                'vy': 0, 'vz': -get_v_obj(r4),  'mass': m4, 'rad': 5,  'color': (230, 126, 34)},
        {'x': 0,   'y': 0, 'z': -r5, 'vx': get_v_obj(r5)*1.1,  'vy': 0, 'vz': 0,               'mass': m5, 'rad': 6,  'color': (155, 89, 182)}
    ]
    
    return [Body(c['x'], c['y'], c['z'], c['vx'], c['vy'], c['vz'], c['mass'], c['rad'], c['color']) for c in raw_configs]

def main():
    global cam_yaw, cam_pitch, cam_zoom
    
    sliders = {
        'bodies': Slider(940, 70, 240, 1, 5, 5, "Número de Corpos", 1),
        'speed': Slider(940, 120, 240, 1, 5, 3, "Velocidade", 1),
        'm1': Slider(940, 200, 240, 0.5, 5, 2.0, "m1 (Sol) x10³⁰ kg"),
        'm2': Slider(940, 250, 240, 1, 20, 6.0, "m2 x10²⁴ kg", 0.5),
        'm3': Slider(940, 300, 240, 1, 20, 2.0, "m3 x10²⁴ kg", 0.5),
        'm4': Slider(940, 350, 240, 1, 20, 4.0, "m4 x10²⁴ kg", 0.5),
        'm5': Slider(940, 400, 240, 1, 20, 8.0, "m5 x10²⁴ kg", 0.5),
    }
    
    checkboxes = {
        'grid': Checkbox(940, 460, "Grelha XZ", False),
        'trails': Checkbox(1070, 460, "Trajetórias", True),
        'velocities': Checkbox(940, 490, "Vetores v", False),
        'cm': Checkbox(1070, 490, "Fixar C.M.", True),
    }

    btn_pause = pygame.Rect(940, 15, 115, 30)
    btn_reset = pygame.Rect(1065, 15, 115, 30)

    is_running = True
    sim_time = 0.0
    bodies = init_bodies(sliders)
    
    while True:
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if btn_pause.collidepoint(mx, my):
                        is_running = not is_running
                    elif btn_reset.collidepoint(mx, my):
                        bodies = init_bodies(sliders)
                        sim_time = 0.0
                    for cb in checkboxes.values():
                        if cb.handle_event(mx, my, True):
                            if cb.label == "Trajetórias" and not cb.checked:
                                for b in bodies: b.history.clear()
                
                if event.button == 4: cam_zoom = min(40.0, cam_zoom + 1.0)
                if event.button == 5: cam_zoom = max(5.0, cam_zoom - 1.0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  cam_yaw -= 0.03
        if keys[pygame.K_RIGHT]: cam_yaw += 0.03
        if keys[pygame.K_UP]:    cam_pitch = min(1.4, cam_pitch + 0.03)
        if keys[pygame.K_DOWN]:  cam_pitch = max(-1.4, cam_pitch - 0.03)

        sliders_changed = False
        for name, s in sliders.items():
            if s.update(mx, my, click):
                sliders_changed = True
                
        if sliders_changed:
            bodies = init_bodies(sliders)

        # --- MOTOR DE FÍSICA ---
        num_active = int(sliders['bodies'].curr_val)
        if is_running:
            iterations = int(sliders['speed'].curr_val) * 2
            for _ in range(iterations):
                ax = [0.0] * num_active
                ay = [0.0] * num_active
                az = [0.0] * num_active
                
                for i in range(num_active):
                    for j in range(i + 1, num_active):
                        dx = bodies[j].x - bodies[i].x
                        dy = bodies[j].y - bodies[i].y
                        dz = bodies[j].z - bodies[i].z  
                        
                        dist_sq = dx*dx + dy*dy + dz*dz
                        dist = math.sqrt(dist_sq)
                        if dist < 0.5: dist = 0.5
                        
                        f_i = (G * bodies[j].mass) / dist_sq
                        f_j = (G * bodies[i].mass) / dist_sq
                        
                        ax[i] += f_i * (dx / dist)
                        ay[i] += f_i * (dy / dist)
                        az[i] += f_i * (dz / dist)
                        
                        ax[j] -= f_j * (dx / dist)
                        ay[j] -= f_j * (dy / dist)
                        az[j] -= f_j * (dz / dist)

                for i in range(num_active):
                    bodies[i].vx += ax[i] * DT
                    bodies[i].vy += ay[i] * DT
                    bodies[i].vz += az[i] * DT
                    bodies[i].x += bodies[i].vx * DT
                    bodies[i].y += bodies[i].vy * DT
                    bodies[i].z += bodies[i].vz * DT
                    
                    if checkboxes['trails'].checked:
                        bodies[i].history.append((bodies[i].x, bodies[i].y, bodies[i].z))
                        if len(bodies[i].history) > 1200:
                            bodies[i].history.pop(0)

                if checkboxes['cm'].checked:
                    total_m = sum(bodies[i].mass for i in range(num_active))
                    cx = sum(bodies[i].x * bodies[i].mass for i in range(num_active)) / total_m
                    cy = sum(bodies[i].y * bodies[i].mass for i in range(num_active)) / total_m
                    cz = sum(bodies[i].z * bodies[i].mass for i in range(num_active)) / total_m
                    for i in range(num_active):
                        bodies[i].x -= cx
                        bodies[i].y -= cy
                        bodies[i].z -= cz
            sim_time += 0.002 * iterations

        # --- RENDERING ---
        screen.fill(BG_COLOR)

        if checkboxes['grid'].checked:
            for g_line in range(-30, 31, 5):
                p1 = project_3d(g_line, 0, -30)
                p2 = project_3d(g_line, 0, 30)
                pygame.draw.line(screen, (35, 45, 55), (p1[0], p1[1]), (p2[0], p2[1]), 1)
                p3 = project_3d(-30, 0, g_line)
                p4 = project_3d(30, 0, g_line)
                pygame.draw.line(screen, (35, 45, 55), (p3[0], p3[1]), (p4[0], p4[1]), 1)

        if checkboxes['trails'].checked:
            for i in range(num_active):
                b = bodies[i]
                if len(b.history) > 1:
                    points_2d = []
                    for h_pt in b.history[::2]: 
                        px, py, _ = project_3d(h_pt[0], h_pt[1], h_pt[2])
                        if 0 <= px <= 900 and 0 <= py <= 600:
                            points_2d.append((px, py))
                    if len(points_2d) > 1:
                        pygame.draw.lines(screen, b.color, False, points_2d, 1)

        render_queue = []
        for i in range(num_active):
            b = bodies[i]
            sx, sy, sz = project_3d(b.x, b.y, b.z)
            render_queue.append((sz, sx, sy, b))
            
        render_queue.sort(key=lambda item: item[0], reverse=True)
        
        for sz, sx, sy, b in render_queue:
            if 0 <= sx <= 900 and 0 <= sy <= 600:
                rad_proj = max(2, int(b.radius * cam_zoom * 15 / (sz + 200)))
                pygame.draw.circle(screen, b.color, (sx, sy), rad_proj)
                
                if checkboxes['velocities'].checked:
                    vx_p, vy_p, _ = project_3d(b.x + b.vx*0.2, b.y + b.vy*0.2, b.z + b.vz*0.2)
                    pygame.draw.line(screen, WHITE, (sx, sy), (vx_p, vy_p), 2)

        panel_rect = pygame.Rect(900, 0, 320, 600)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect)
        pygame.draw.line(screen, (173, 181, 173), (900, 0), (900, 600), 2)

        pygame.draw.rect(screen, (226, 232, 226), btn_pause, border_radius=4)
        pygame.draw.rect(screen, (122, 133, 122), btn_pause, 1, border_radius=4)
        txt_p = FONT_BOLD.render("Pausar" if is_running else "Continuar", True, TEXT_COLOR)
        screen.blit(txt_p, (btn_pause.centerx - txt_p.get_width()//2, btn_pause.centery - txt_p.get_height()//2))

        pygame.draw.rect(screen, (226, 232, 226), btn_reset, border_radius=4)
        pygame.draw.rect(screen, (122, 133, 122), btn_reset, 1, border_radius=4)
        txt_r = FONT_BOLD.render("Reiniciar", True, TEXT_COLOR)
        screen.blit(txt_r, (btn_reset.centerx - txt_r.get_width()//2, btn_reset.centery - txt_r.get_height()//2))

        for s in sliders.values(): s.draw(screen)
        for cb in checkboxes.values(): cb.draw(screen)

        txt_time = FONT_BOLD.render(f"Tempo = {sim_time:.1f} anos", True, WHITE)
        screen.blit(txt_time, (20, 20))
        
        txt_cam = FONT.render("Usa as SETAS DO TECLADO para rodar a câmara | Roda do rato faz Zoom", True, (130, 140, 150))
        screen.blit(txt_cam, (20, 565))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()