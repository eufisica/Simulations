import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
DAMPING = 0.98  # Coeficiente de restituição (perda de energia na colisão)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sphere Collision Simulation - José Gonçalves (eufisica)")
clock = pygame.time.Clock()

class Sphere:
    def __init__(self, x, y, radius, color, vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.mass = radius ** 2  # Mass proportional to area
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Wall collisions
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * DAMPING
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * DAMPING
        
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * DAMPING
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * DAMPING
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw a small highlight for 3D effect
        highlight_pos = (int(self.x - self.radius/3), int(self.y - self.radius/3))
        pygame.draw.circle(surface, WHITE, highlight_pos, self.radius//4)

def check_collision(sphere1, sphere2):
    """Check and handle collision between two spheres"""
    dx = sphere2.x - sphere1.x
    dy = sphere2.y - sphere1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < sphere1.radius + sphere2.radius:
        # Collision detected
        # Normalize collision vector
        nx = dx / distance
        ny = dy / distance
        
        # Separate spheres (prevents spheres from getting stuck together)
        overlap = sphere1.radius + sphere2.radius - distance
        sphere1.x -= nx * overlap / 2
        sphere1.y -= ny * overlap / 2
        sphere2.x += nx * overlap / 2
        sphere2.y += ny * overlap / 2
        
        # Relative velocity
        dvx = sphere1.vx - sphere2.vx
        dvy = sphere1.vy - sphere2.vy
        
        # Relative velocity in collision normal direction
        dvn = dvx * nx + dvy * ny
        
        # CORRECÇÃO: Só processa se as esferas se estiverem a aproximar (dvn > 0)
        # Se dvn <= 0, elas já se estão a afastar e não fazemos nada.
        if dvn <= 0:
            return
        
        # Collision impulse corrigido com o DAMPING (Coeficiente de Restituição)
        impulse = (1 + DAMPING) * dvn / (sphere1.mass + sphere2.mass)
        
        # Update velocities
        sphere1.vx -= impulse * sphere2.mass * nx
        sphere1.vy -= impulse * sphere2.mass * ny
        sphere2.vx += impulse * sphere1.mass * nx
        sphere2.vy += impulse * sphere1.mass * ny

# Create two spheres
sphere1 = Sphere(200, 200, 40, RED, vx=5, vy=2)
sphere2 = Sphere(600, 300, 50, BLUE, vx=-3, vy=-1)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reset spheres
                sphere1 = Sphere(200, 200, 40, RED, vx=5, vy=2)
                sphere2 = Sphere(600, 300, 50, BLUE, vx=-3, vy=-1)
    
    # Update spheres
    sphere1.update()
    sphere2.update()
    
    # Check collision between spheres
    check_collision(sphere1, sphere2)
    
    # Draw
    screen.fill(BLACK)
    sphere1.draw(screen)
    sphere2.draw(screen)
    
    # Display instructions
    font = pygame.font.Font(None, 24)
    text = font.render("Press SPACE to reset", True, WHITE)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()