import random
import math

# Global Variables
gravity = (math.pi, 0.0002)
massOfAir = 0.1

class Environment:
    def addFunctions(self, functionList):
        for f in functionList:
            # Try and get function, provide defaults in case of failure.
            (n, func) = self.functionDictionary.get(f, (-1, None))
            # Single Particle Function.
            if n == 1:
                self.particleFunctions1.append(func)
            # Two Particle Function.
            elif n == 2:
                self.particleFunctions2.append(func)
            else:
                print("No function founf called %s" %f)    
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.springs = []
        self.colour = (255, 255, 255)
        self.massOfAir = 0.2
        self.particleFunctions1 = []
        self.particleFunctions2 = []
        # Add the possible interaction functions.
        self.functionDictionary = {
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.addDrag()),
            'bounce': (1, lambda p: self.bounce(p)), # Bounce is called in environment.
            'accelerate': (1, lambda p: p.accelerate(self.gravity)),
            'collide': (2, lambda p1, p2: collide(p1,p2)),
            'combine': (2, lambda p1, p2: combine(p1,p2)),
        }
        
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
            
        # Adds a spring between p1 & p2.
    def addSpring(self, p1, p2, length=50, strength=0.5):
        self.springs.append(Spring(self.particles[p1], self.particles[p2], length, strength))
    
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
        
        # Exert Spring forces
        for spring in self.springs:
            spring.update() 
        # Loop through all particles.
        for i, particle in enumerate(self.particles):
            # Call single and double particle functions through Lambda functions.
            for f in self.particleFunctions1:
                f(particle)
              
            # Double Particle function call.    
            if(self.particleFunctions2 != []):
                for particle2 in self.particles[i+1:]:
                    # Call the Two particle Function.
                    for f in self.particleFunctions2:
                        f(particle, particle2)
                
                
    # Used to locate where the mouse has clicked.
    def findParticle(self, coords):
        (x, y) = coords
        for p in self.particles:
            if math.hypot(p.x-x, p.y-y) <= p.size:
                return p     

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
        
# Combines two particles that collide together in the Space.py.
def combine(self, otherParticle):
    # Check if the particles are touching.
    dx = (self.x - otherParticle.x)
    dy = (self.y - otherParticle.y)
    dist = math.hypot(dx, dy)
    if dist < self.size + otherParticle.size:
        # Calculate the mass of the two particles and place a new particle in between them.
        totalMass = self.mass + otherParticle.mass
        self.x = (self.x*self.mass + otherParticle.x*otherParticle.mass)/totalMass
        self.y = (self.y*self.mass + otherParticle.x*otherParticle.mass)/totalMass
        # Combine the vector to a single speed and direction.
        (self.angle, self.speed) = addVectors(self.angle, self.speed*self.mass/totalMass, otherParticle.angle, otherParticle.speed*otherParticle.mass/totalMass)
        # Accounts for collision.
        self.speed *= (self.elasticity * otherParticle.elasticity)
        # Set new mass
        self.mass = totalMass
        # Indicate collision has occured - Dealt with later.
        self.collide_with = otherParticle

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
    
    # Moves the particles on screen.    
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        
    # Adds Drag to the particles.
    def addDrag(self):
        self.speed *= self.drag
        
    # Applies a force to the object - In this instance it will be gravity.
    def accelerate(self, vector):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, vector[0], vector[1])
        
    def mouseMove(self, x, y):
        # Get difference from previous position.
        dx = x - self.x
        dy = y - self.y
        # Work out relative angle and speed.
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1 
        
# Spring Class
class Spring:
    def __init__(self, p1, p2, length=50, strength=0.5):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.strength = strength
    
    # This pulls the strings together.
    def update(self):
        # Calculate distance between particles.
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.hypot(dx, dy)
        # Calculate the angle.
        theta = math.atan2(dy, dx)
        # Attraction force that stops when lenght of spring is reached.
        force = (self.length - dist) * self.strength
        
        # Push the particles closer to eachother.
        self.p1.accelerate((theta + 0.5 * math.pi, force/self.p1.mass))
        self.p2.accelerate((theta + 0.5 * math.pi, force/self.p2.mass))