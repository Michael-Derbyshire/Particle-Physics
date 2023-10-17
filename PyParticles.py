import random
import math

# Global Variables
gravity = (math.pi, 0.0002)
massOfAir = 0.1


# Combines two vectors to make a brand new one.
def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x,y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return(angle, length)

# Used to locate where the mouse has clicked.
def findParticle(particles, coords):
    (x, y) = coords
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p 
        
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
        p1.speed *= p1.elasticity
        p2.speed *= p2.elasticity
            
        # Move the particles away from eachother to prevent constantr collisions.
        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

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
        
    def move(self):
        self.speed *= self.drag
        (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        
    def mouseMove(self, x, y):
        # Get difference from previous position.
        dx = x - self.x
        dy = y - self.y
        # Work out relative angle and speed.
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1     


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.colour = (255, 255, 255)
        self.massOfAir = 0.2
        
    def addParticles(self, n=1, **kargs):
        for i in range(n):
            # try and get an argument, if it fails, generate a random number instead.
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width-size))
            y = kargs.get('y', random.uniform(size, self.height-size))
            
            # Create the Particle.
            p = Particle(x, y, size, mass)
            
            # Add Additional attributes.
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            p.colour = kargs.get('colour', (0, 0, 255))
            p.drag = (p.mass/(p.mass + self.massOfAir)) ** p.size
            
            # Add to the collection on particles.
            self.particles.append(p)
    
    # Bounce off a boundary.
    def bounce(self, particle):
        # Check east wall.
        if particle.x > self.width - particle.size:
            particle.speed *= particle.elasticity
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = - particle.angle
        # Check west wall.
        elif particle.x < particle.size:
            particle.speed *= particle.elasticity
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
        # Check south wall.
        elif particle.y > self.height - particle.size:
            particle.speed *= particle.elasticity
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
        # Check north wall.
        elif particle.y < particle.size:
            particle.speed *= particle.elasticity
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle      
            
    def update(self):
        # Loop through all particles.
        for i, particle in enumerate(self.particles):
            # Move them, check for bounces and collisions.
            particle.move()
            self.bounce(particle)
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)  
                
    # Used to locate where the mouse has clicked.
    def findParticle(self, coords):
        for p in self.particles:
            if math.hypot(p.x - coords[0], p.y - coords[1]) <= p.size:
                return p     
            
