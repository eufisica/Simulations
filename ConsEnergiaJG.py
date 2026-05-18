import pygame
import math

# Configurações de Janela e Cores
WIDTH, HEIGHT = 1100, 750
SIM_HEIGHT = 580  # Limite da área da pista
WHITE = (255, 255, 255)
BLACK = (44, 62, 80)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
ORANGE = (243, 156, 18)
GRAY = (220, 220, 220)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.handle_rect = pygame.Rect(x + (initial_val - min_val) / (max_val - min_val) * w - 10, y - 5, 20, h + 10)
        self.dragging = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.handle_rect, border_radius=5)
        txt = font.render(f"{self.label}: {self.val:.2f}", True, BLACK)
        screen.blit(txt, (self.rect.x, self.rect.y - 25))

    def update_val(self, pos_x):
        rel_x = max(0, min(pos_x - self.rect.x, self.rect.w))
        self.val = self.min_val + (rel_x / self.rect.w) * (self.max_val - self.min_val)
        self.handle_rect.centerx = self.rect.x + rel_x
        return self.val

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulador de Energia - José Gonçalves (eufisica)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        
        # Física
        self.is_playing = True
        self.g = 9.8
        self.mu = 0.05
        self.thermal_energy = 0
        self.px_to_meter = 50

        # Pista: X é fixo, apenas Y muda
        self.points = [[100, 150], [325, 500], [550, 250], [775, 500], [1000, 150]]
        self.ball_x = self.points[0][0]
        self.ball_y = self.points[0][1]
        self.ball_s_vel = 0
        self.ball_radius = 12

        # UI
        self.slider = Slider(450, 680, 250, 12, 0.0, 0.6, self.mu, "Atrito (mu)")
        self.btn_play_rect = pygame.Rect(50, 665, 120, 45)
        self.btn_reset_rect = pygame.Rect(190, 665, 150, 45)
        
        self.dragging_point = None
        self.dragging_ball = False

    def get_y_at(self, x):
        p = self.points
        if x <= p[0][0]: return p[0][1]
        if x >= p[-1][0]: return p[-1][1]
        for i in range(len(p) - 1):
            if p[i][0] <= x <= p[i+1][0]:
                p0, p1, p2, p3 = p[max(0, i-1)], p[i], p[i+1], p[min(len(p)-1, i+2)]
                t = (x - p1[0]) / (p2[0] - p1[0])
                return 0.5 * ((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*(t**2) + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*(t**3))
        return 550

    def get_slope(self, x):
        dx = 0.5
        return (self.get_y_at(x + dx) - self.get_y_at(x - dx)) / (2 * dx)

    def update_physics(self):
        if self.is_playing and not self.dragging_ball and self.dragging_point is None:
            dt = 1/60
            slope = self.get_slope(self.ball_x)
            angle = math.atan(slope)
            cos_theta = abs(math.cos(angle))

            accel_grav = self.g * math.sin(angle) * self.px_to_meter
            accel_fric = self.mu * self.g * cos_theta * self.px_to_meter
            
            # Condição de parada (atrito estático)
            if self.mu > 0 and abs(self.ball_s_vel) < 0.3 and abs(accel_grav) < accel_fric:
                self.ball_s_vel = 0
            else:
                direction = -1 if self.ball_s_vel > 0 else 1
                self.ball_s_vel += (accel_grav + (accel_fric * direction)) * dt

            self.thermal_energy += self.mu * 1.0 * self.g * cos_theta * abs(self.ball_s_vel * dt / self.px_to_meter)
            self.ball_x += self.ball_s_vel * math.cos(angle) * dt
            
            # Colisão Bordas
            if self.ball_x < self.points[0][0]: 
                self.ball_x = self.points[0][0]; self.ball_s_vel *= -0.2
            elif self.ball_x > self.points[-1][0]: 
                self.ball_x = self.points[-1][0]; self.ball_s_vel *= -0.2

        self.ball_y = self.get_y_at(self.ball_x)

    def draw(self):
        self.screen.fill(WHITE)
        
        # Pista
        track_pts = [(x, self.get_y_at(x)) for x in range(self.points[0][0], self.points[-1][0] + 1)]
        pygame.draw.lines(self.screen, BLACK, False, track_pts, 4)
        for p in self.points:
            pygame.draw.circle(self.screen, RED, (int(p[0]), int(p[1])), 8)

        # Bola
        pygame.draw.circle(self.screen, BLUE, (int(self.ball_x), int(self.ball_y - self.ball_radius)), self.ball_radius)
        
        # UI Painel
        pygame.draw.rect(self.screen, (235, 235, 235), (0, SIM_HEIGHT, WIDTH, HEIGHT - SIM_HEIGHT))
        pygame.draw.line(self.screen, (180, 180, 180), (0, SIM_HEIGHT), (WIDTH, SIM_HEIGHT), 2)
        
        # Botões
        pygame.draw.rect(self.screen, ORANGE, self.btn_play_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, self.btn_reset_rect, border_radius=8)
        
        play_txt = "Pausar" if self.is_playing else "Retomar"
        self.screen.blit(self.font.render(play_txt, True, WHITE), (self.btn_play_rect.centerx - 25, self.btn_play_rect.centery - 8))
        self.screen.blit(self.font.render("Reiniciar Esfera", True, WHITE), (self.btn_reset_rect.centerx - 55, self.btn_reset_rect.centery - 8))
        
        self.slider.draw(self.screen, self.font)

        # Gráficos de Energia
        h = max(0, (550 - self.ball_y) / self.px_to_meter)
        ep, ek = 1.0 * self.g * h, 0.5 * 1.0 * ((self.ball_s_vel / self.px_to_meter)**2)
        energies = [("U", ep, RED), ("K", ek, BLUE), ("Calor", self.thermal_energy, ORANGE)]
        
        for i, (label, val, col) in enumerate(energies):
            pygame.draw.rect(self.screen, (200, 200, 200), (900 + i*50, 620, 35, 80))
            h_bar = min(80, val * 1.5)
            pygame.draw.rect(self.screen, col, (900 + i*50, 700 - h_bar, 35, h_bar))
            self.screen.blit(self.font.render(label, True, BLACK), (900 + i*50, 600))

        pygame.display.flip()

    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clique na UI
                    if my > SIM_HEIGHT:
                        if self.slider.handle_rect.collidepoint((mx, my)):
                            self.slider.dragging = True
                        elif self.btn_play_rect.collidepoint((mx, my)):
                            self.is_playing = not self.is_playing
                        elif self.btn_reset_rect.collidepoint((mx, my)):
                            self.ball_x, self.ball_s_vel, self.thermal_energy = self.points[0][0], 0, 0
                    # Clique na Simulação
                    else:
                        if math.hypot(mx - self.ball_x, my - (self.ball_y - self.ball_radius)) < 20:
                            self.dragging_ball = True
                        else:
                            for i, p in enumerate(self.points):
                                if math.hypot(mx - p[0], my - p[1]) < 15:
                                    self.dragging_point = i
                                    break
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.slider.dragging = self.dragging_ball = False
                    self.dragging_point = None
                
                if event.type == pygame.MOUSEMOTION:
                    if self.slider.dragging:
                        self.mu = self.slider.update_val(mx)
                    if self.dragging_ball:
                        self.ball_x = max(self.points[0][0], min(mx, self.points[-1][0]))
                        self.ball_s_vel = 0
                    if self.dragging_point is not None:
                        # APENAS Y muda. X é fixo para evitar confusão no mouse.
                        self.points[self.dragging_point][1] = max(50, min(my, SIM_HEIGHT - 30))

            self.update_physics()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__": Simulation().run()