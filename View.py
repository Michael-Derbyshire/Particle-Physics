"""
Use Maths to make particles collide and bounce in Pygame.
Created by Michael Derbyshire, Universty South Wales
"""
import math
import pygame
# PyParticles will be the new module.
import PyParticles

# Set up display.
pygame.display.set_caption('Example Setup')
backgroundColour = (255,255,255)
(width, height) = (1200, 700)
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load('Images/usw.jpg')
pygame.display.set_icon(icon)
env = PyParticles.Environment(width, height)

# Generate 10 particles randomly.
env.addParticles(10)
running = True
selectedParticle = None

# Add game Loop.
while running:
    for event in pygame.event.get():
        #quit if user closes window.
        if event.type == pygame.QUIT:
            running = False
            
    # Clear screen.
    env.update()
    screen.fill(env.colour)
    
    # Go through the particles and draw them.
    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)
    
    # Update Display
    pygame.display.flip()
    
    for event in pygame.event.get():
        # Quit if the user closes window.
        if event.type == pygame.QUIT:
            running = False
        # User picks up a particle - find it in the environment.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selectedParticle = env.findParticle(event.pos)
            if selectedParticle:
                selectedParticle.colour = (255,0,0)
        # User relases a particle, deselect.
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedParticle.colour = (0,0,255)
            selectedParticle = None
        # User moves the mouse with the selected particle - move it in the environment.
        elif selectedParticle and event.type == pygame.MOUSEMOTION:
            (mouseX, mouseY) = event.pos
            selectedParticle.mouseMove(mouseX, mouseY)  