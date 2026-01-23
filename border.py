import pygame
import random
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1200, 800
FPS = 60
BG_COLOR = (2, 5, 15)  # Deep Midnight Blue
TEXT_STR = "BORDER 2 - 23 JAN"
MOUSE_RADIUS = 70
SCATTER_FORCE = 12
RETURN_SPEED = 0.15

# Colors
SAFFRON = (255, 153, 51)
WHITE = (255, 255, 255)
GREEN = (18, 136, 7)
CHAKRA = (0, 0, 128)
TEXT_GOLD = (255, 220, 110)

class Particle:
    def __init__(self, x, y, color, is_flag=False):
        self.base_target = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        # Start particles scattered across the bottom
        self.pos = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(HEIGHT, HEIGHT+100))
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        
        self.max_speed = 8
        self.max_force = 0.6
        self.friction = 0.92
        
        self.color = color
        self.is_flag = is_flag
        self.size = random.randint(1, 3)
        self.waving_offset = random.uniform(0, 100)

    def apply_force(self, force):
        self.acc += force

    def update_behavior(self, mouse_pos, time_ms):
        # 1. Flag Waving Logic (only if it's a flag particle and not being pushed)
        if self.is_flag:
            wave = math.sin(time_ms * 0.003 + self.base_target.x * 0.02) * 8
            self.target.y = self.base_target.y + wave
        else:
            self.target = self.base_target

        # 2. Arrive at target
        arrival_force = self.arrive(self.target)
        self.apply_force(arrival_force)

        # 3. Flee from Mouse
        m_pos = pygame.Vector2(mouse_pos)
        if self.pos.distance_to(m_pos) < MOUSE_RADIUS:
            flee_force = self.flee(m_pos)
            self.apply_force(flee_force * SCATTER_FORCE)

    def arrive(self, target):
        desired = target - self.pos
        dist = desired.length()
        if dist < 100:
            speed = (dist / 100) * self.max_speed
        else:
            speed = self.max_speed
        
        if dist > 0:
            desired = desired.normalize() * speed
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
        return pygame.Vector2(0, 0)

    def flee(self, target):
        desired = target - self.pos
        dist = desired.length()
        if dist < MOUSE_RADIUS:
            desired = desired.normalize() * self.max_speed
            desired *= -1
            steer = desired - self.vel
            return steer
        return pygame.Vector2(0, 0)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0
        self.vel *= self.friction

    def draw(self, surface):
        # Add a slight shimmer/flicker to particles
        alpha_color = self.color
        if random.random() > 0.98:
            alpha_color = (255, 255, 255)
            
        pygame.draw.circle(surface, alpha_color, (int(self.pos.x), int(self.pos.y)), self.size)

def create_flag_points():
    points = []
    f_w, f_h = 450, 270
    start_x = (WIDTH - f_w) // 2
    start_y = 150
    
    # Step 5 for performance optimization
    for x in range(0, f_w, 5):
        for y in range(0, f_h, 5):
            # Decide color based on vertical position
            if y < f_h // 3:
                color = SAFFRON
            elif y < (f_h // 3) * 2:
                # Check for Chakra area (Center circle)
                cx, cy = f_w//2, f_h//2
                dist_to_center = math.sqrt((x-cx)**2 + (y-cy)**2)
                if 30 < dist_to_center < 35 or (dist_to_center < 35 and x % 10 == 0):
                    color = CHAKRA
                else:
                    color = WHITE
            else:
                color = GREEN
            
            points.append(Particle(x + start_x, y + start_y, color, is_flag=True))
    return points

def create_text_points(font):
    points = []
    text_surf = font.render(TEXT_STR, True, (255, 255, 255))
    w, h = text_surf.get_size()
    offset_x = (WIDTH - w) // 2
    offset_y = 550
    
    mask = pygame.mask.from_surface(text_surf)
    # Step 3 for dense but performant text
    for x in range(0, w, 3):
        for y in range(0, h, 3):
            if mask.get_at((x, y)):
                points.append(Particle(x + offset_x, y + offset_y, TEXT_GOLD, is_flag=False))
    return points

def main():
    pygame.init()
    # Use hardware acceleration if available
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Border 2 - Cinematic Particle Flag")
    clock = pygame.time.Clock()

    try:
        font = pygame.font.SysFont("Impact", 110)
    except:
        font = pygame.font.Font(None, 130)

    # Initialize Particles
    all_particles = create_flag_points() + create_text_points(font)

    running = True
    while running:
        time_ms = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- DRAWING ---
        # Subtle Blue Background Gradient Effect
        screen.fill(BG_COLOR)
        
        # Update and Draw all particles
        for p in all_particles:
            p.update_behavior(mouse_pos, time_ms)
            p.update()
            p.draw(screen)

        # Cinematic Flare on Mouse
        m_flare = pygame.Surface((MOUSE_RADIUS*2, MOUSE_RADIUS*2), pygame.SRCALPHA)
        pygame.draw.circle(m_flare, (100, 150, 255, 15), (MOUSE_RADIUS, MOUSE_RADIUS), MOUSE_RADIUS)
        screen.blit(m_flare, (mouse_pos[0]-MOUSE_RADIUS, mouse_pos[1]-MOUSE_RADIUS))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()