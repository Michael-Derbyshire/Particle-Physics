import math
import random
import pygame
import PyParticles

# Set up the clock to lock the framerate.
clock = pygame.time.Clock()

# Set up the environment and the screen.
(width, height) = (1200, 700)
screen = pygame.display.set_mode((width, height))


class UniverseScreen:
    # Initialisation Method to set up the Universe Screen.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
    
    # Allows the player to move around the space environment.    
    def scroll(self, dx = 0, dy = 0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
    
    # Allows the player to zoom in their screen in increments.    
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
    
    # Allows the player to reset at the centre of the 'Universe'.    
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0

# Creates an instance of class using the pre-determined width and height.  
universe_screen = UniverseScreen(width, height)
pygame.display.set_caption("Black Hole Simulator")

# Create the environment.
universe = PyParticles.Environment(width, height)
universe.colour = (0,0,0) # Black background.
# Adds functions from the PyParticles.py file - specifically from the universe class.
universe.addFunctions(['move'])

# Make the particles mass related to their appearance.
def calculateRadius(mass):
    return 1.2 * mass ** (0.5)

# Create 200 white particles.
for p in range(200):
    particleMass = random.randint(1,10)
    particleSize = calculateRadius(particleMass)
    universe.addParticles(mass = particleMass, size = particleSize, colour=(255,255,255))


# Game loop.
running = True


while running:
    
    # Update the environment and makes the background black.
    universe.update()
    screen.fill(universe.colour)
    
    # Draw the particles on screen after movement.
    for p in universe.particles:
        
        # Adjust particle position based on view zoom and position
        mag = universe_screen.magnification
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * mag)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * mag)
        size = int(p.size * mag)
        
        if size < 2:
            pygame.draw.rect(screen, p.colour, (int(x), int(y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(x), int(y)), int(size), 0)
    
    # Sets the fps to 60, and updates the screen.
    clock.tick(60)
    pygame.display.flip()
    
    # Event Handlers.
    for event in pygame.event.get():
        # allows the player to quit the game with the 'x' on the window.
        if event.type == pygame.QUIT:
            running = False
        # Player controls for the movement mechanics.
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