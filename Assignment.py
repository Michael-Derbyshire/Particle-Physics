"""
Use Maths to make particles collide and bounce in Pygame.
Created by Michael Derbyshire, Universty South Wales
"""

import pygame
import random
import math

# Global Variables
gravity = (math.pi, 0.0002)
massOfAir = 0.1

# Define some colors
WHITE = (255, 255, 255)

# Set the height and width of the screen
screen_width = 1200
screen_height = 700

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
icon = pygame.image.load('Images/usw.jpg')
pygame.display.set_caption('Particle Simulation')
pygame.display.set_icon(icon)


# Particles class with an Initialise and Display Function.
class Particle:
    drag = 0.999
    elasticity = 0.85

    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0,0,255)
        self.thickness = 3
        self.mass = mass
        self.drag = (self.mass/(self.mass + massOfAir)) ** self.size
        #give particles random speed and direction.
        self.speed = random.random()
        self.angle = random.uniform(0,math.pi*2)
        
        
    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        
    def move(self):
        self.speed *= self.drag
        (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    # Bounce off a boundary.
    def bounce(self):
        # Check east wall.
        if self.x > screen_width - self.size:
            self.speed *= self.elasticity
            self.x = screen_width- self.size
            self.angle = - self.angle
        # Check west wall.
        elif self.x < self.size:
            self.speed *= self.elasticity
            self.x = self.size
            self.angle = - self.angle
        # Check south wall.
        elif self.y > screen_height - self.size:
            self.speed *= self.elasticity
            self.y = screen_height - self.size
            self.angle = math.pi - self.angle
        # Check north wall.
        elif self.y < self.size:
            self.speed *= self.elasticity
            self.y = self.size
            self.angle = math.pi - self.angle


# Combines two vectors to make a brand new one.
def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x,y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return(angle, length)

# Checks for collisions between two particles.
def collide(p1, p2):
    # Get the relative coordinates
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    # Calculate the hypotenuse of the triangle formed.
    distance = math.hypot(dx, dy)
    # Compare it with the size of the circles.
    if distance < p1.size + p2.size:
        # Calculate the angle of collision.
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        
        # Get the total mass of the particles.
        totalMass = p1.mass + p2.mass
        
        p1SpeedTemp = p1.speed
        # Combines the vectors to recalculate speed after a collision occurs.
        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass - p2.mass)/totalMass, angle, 2*p2.speed*p2.mass/totalMass)
        (p2.angle, p2.spedd) = addVectors(p2.angle, p1.speed*(p2.mass - p1.mass)/totalMass, angle, 2*p1SpeedTemp*p1.mass/totalMass)
        
        # Reduce speed due to collision.
        p1.speed *= particle.elasticity
        p2.speed *= particle.elasticity
        
        # Move the particles away from eachother to prevent constantr collisions.
        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        

# Used to locate where the mouse has clicked.
def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p


# Loop until the user clicks the close button.
done = False
    
# Loop to create random particles.
numberOfParticles = 10
myParticles = []
for n in range(numberOfParticles):
    size = random.randint(10, 20)
    x = random.randint(size, screen_width)
    y = random.randint(size, screen_height)
    
    density = random.randint(1, 20)
    particle = Particle(x, y, size, size * density)
    myParticles.append(Particle(x, y, size))


# -------- Main Program Loop -----------
selectedParticle = None
relativeX, relativeY = (0,0)
particleColour = (0,0,0)
while not done:
    # Update the screen.
    screen.fill(WHITE)
    for i, particle in enumerate(myParticles):
        # Don't move the Particle if it's not selected.
        if particle != selectedParticle:
            particle.move()
            particle.bounce()
            
        # Loop through the particles to compare them.
        for particle2 in myParticles[i+1:]:
            collide(particle, particle2)
            
        particle.display()
    pygame.display.flip()        


    # Continues the game until exit is pressed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Checks for the mouse click.
    if event.type == pygame.MOUSEBUTTONDOWN:
        (mouseX, mouseY) = event.pos
        selectedParticle = findParticle(myParticles, mouseX, mouseY)
        if selectedParticle:
            selectedParticle.colour = (255,0,0)

    # Updates particles if selected.
    if event.type == pygame.MOUSEBUTTONUP:
        if selectedParticle:
            selectedParticle.colour = (0,0,255)
            selectedParticle.angle = math.atan2(relativeY, relativeX) + 0.5*math.pi
            selectedParticle.speed = math.hypot(relativeX, relativeY) * 0.2
            selectedParticle = None 
    
    # Keepsa track of the level of Movement.
    if selectedParticle and event.type == pygame.MOUSEMOTION:
        (relativeX, relativeY) = event.rel
        (mouseX, mouseY) = event.pos
        selectedParticle.x = mouseX
        selectedParticle.y = mouseY


