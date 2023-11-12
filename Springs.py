import random
import math
import pygame
import PyParticles

clock = pygame.time.Clock()

# Spring Creation.
def createSpring(particleOne, particleTwo):
    # Get the ID's of two particles and then connect them
    # with a spring equal to their current length
    index1 = universe.particles.index(particleOne)
    index2 = universe.particles.index(particleTwo)
    universe.addSpring(index1, index2)

# Set up the environment & the screen.
(width, height) = (1200, 700)
screen = pygame.display.set_caption('Springs')
screen = pygame.display.set_mode((width, height))

paused = False
running = True

# Set up the environment.
universe = PyParticles.Environment(width, height)
universe.colour = (255, 255, 255)
universe.addFunctions(['move', 'bounce', 'collide', 'drag'])
universe.accelerate = (math.pi, 0.01)

# Add some particles for testing.
for p in range(4):
    universe.addParticles(mass=100, size=16, speed=2, elasticity=1, colour=(20,40,200))
    
    
universe.addSpring(0,1, length=100, strength=0.01)
universe.addSpring(1,2, length=100, strength=0.01)
universe.addSpring(2,0, length=80, strength=0.01)

# Variables for selecting springs
springSelectOne = None
springSelectTwo = None
selectingSprings = False
    
selectedParticle = None

while running:
    
    # Update if not paused.
    if not paused:
        universe.update()
        
    screen.fill(universe.colour)
    
    # Draw the particles and springs.
    for p in universe.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, 0)
    
    for s in universe.springs:
        pygame.draw.aaline(screen, (0,0,0), (int(s.p1.x), int(s.p1.y)), (int(s.p2.x), int(s.p2.y)))
    
    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change to the paused state when space is pressed. 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
            # Check if they want to select springs.
            elif event.key == pygame.K_LCTRL:
                selectingSprings = True
        # Stops selecting springs.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                selectingSprings = False
                springSelectOne = None
                springSelectTwo = None
        # Deal with mouse selection.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = event.pos
            selectedParticle = universe.findParticle(event.pos)
            # If they are making a spring, initialise varibales.
            if selectedParticle and selectingSprings:
                if springSelectOne:
                    springSelectTwo = selectedParticle
                    # Create Spring.
                    createSpring(springSelectOne, springSelectTwo)
                else:
                    springSelectOne = selectedParticle
                selectedParticle = None
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedParticle = None
        elif selectedParticle and event.type == pygame.MOUSEMOTION:
            (mouseX, mouseY) = event.pos
            selectedParticle.mouseMove(mouseX, mouseY)
    
    # Limits the framerate and Draws.            
    clock.tick(60)
    pygame.display.flip()
    