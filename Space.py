import random
import pygame
import PyParticles

clock = pygame.time.Clock()

# Set up the environment and the screen.
(width, height) = (1200, 700)
screen = pygame.display.set_mode((width, height))

class UniverseScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
    def scroll(self, dx = 0, dy = 0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        

universe_screen = UniverseScreen(width, height)

pygame.display.set_caption("Space")

# Create the environment.
universe = PyParticles.Environment(width, height)
universe.colour = (0,0,0)
universe.addFunctions(['move'])

# Make the particles mass related to their appearance.
def calculateRadius(mass):
    return 0.4 * mass ** (0.5)

# Create 100 white particles.
for p in range(300):
    particleMass = random.randint(1,4)
    particleSize = calculateRadius(particleMass)
    universe.addParticles(mass = particleMass, size = particleSize, colour=(255,255,255))
    
# Game loop.
running = True
particlesToRemove = []

while running:
    
    # Update the environment.
    universe.update()
    screen.fill(universe.colour)
    
    # Draw the particles on screen after movement.
    for p in universe.particles:
        # Check if it has collided_with property, update mass, and remove collision flag.
        if 'collide_with' in p.__dict__:
            particlesToRemove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']
        
        # Adjust particle position based on view zoom and position
        mag = universe_screen.magnification
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * mag)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * mag)
        size = int(p.size * mag)
        
        if size < 2:
            pygame.draw.rect(screen, p.colour, (int(x), int(y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(x), int(y)), int(size), 0)
            
    # Remove particles that were collided with.
    for p in particlesToRemove:
        if p in universe.particles:
            universe.particles.remove(p)
            
    clock.tick(60)
    pygame.display.flip()
    
    # Event Handlers.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universe_screen.scroll(dx=1)
            elif event.key == pygame.K_RIGHT:
                universe_screen.scroll(dx=-1)
            elif event.key == pygame.K_UP:
                universe_screen.scroll(dy=1)
            elif event.key == pygame.K_DOWN:
                universe_screen.scroll(dy=-1)
            elif event.key == pygame.K_EQUALS:
                universe_screen.zoom(2)
            elif event.key == pygame.K_MINUS:
                universe_screen.zoom(0.5)
            elif event.key == pygame.K_r:
                universe_screen.reset()