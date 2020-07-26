### COMPSCI 130, Semester 012019
### Project One - Virus
import turtle
import random
import math


#used to infect 
class Virus:
    def __init__(self, colour, duration):
        self.colour = colour
        self.duration = duration
        
## This class represents a person
class Person:
    def __init__(self, world_size):
        """ initializes each person generated. Of which creates a random location and random destination"""
        self.world_size = world_size
        self.radius = 7
        #used to avoid all the people being generated from the middle, which would cause instance collision
        self.location = self._get_random_location()
        self.destination = self._get_random_location()
        self.infected = False
        
    #random locations are used to assign a destination for the person
    #the possible locations should not be closer than 1 radius to the edge of the world 
    def _get_random_location(self):
        """Generates a random x coordinate and a random y coordinate. Returns a tuple consisting of a destination"""
        x_location = random.randint(-self.world_size[0] / 2 + self.radius, self.world_size[0] / 2 - self.radius)
        y_location = random.randint(-self.world_size[1] / 2 + self.radius, self.world_size[1] / 2 - self.radius)
        
        self.destination = (x_location, y_location)
        return self.destination
 
    #draw a person using a dot.  Use colour if implementing Viruses 
    def draw(self, colour):
        """Draws the individual people with a colour"""
        turtle.goto(self.location)
        turtle.dot(self.radius * 2, colour)

    #PART C returns true if the distance between self and other is less than the diameter
    def collides(self, other):
        """Checks if there is collision between a Person and another. If there is, the code will return True"""
        if (turtle.distance(other.location)) <= (self.radius * 2):
            return True

    #PART C given a list of people, return a list containing only
    #those people who are in contact with self
    def collision_list(self, list_of_others):
        """Loops through the list of non-infected and calls the collides method, if the collides method returns true
        the non-infected will be added to a list, at the end, the list of collisions is returned"""
        collisioned = []
        for people in list_of_others:
            if self.collides(people) == True:
                collisioned += [people]
        return collisioned

    #infect a person with the given virus
    def infect(self, virus):
        """Calls the Virus class to store a colour proposed as red and a duration for the virus"""
        self.virus = Virus(virus[0], virus[1])
        self.infected = True

    #returns true if within 1 radius
    def reached_destination(self):
        """Checks the distance between the turtle to the proposed destination, if it's within one self.radius, it will return
        True."""
        if turtle.distance(self.destination) <= self.radius:
            return True
        else:
            return False

    #increase hours of sickness, check if duration of virus is reached.  If the
    #duration is reached then the person is cured
    def progress_illness(self, people, infected):
        """ sets the duration of the virus to one less than the previous by calling the cure_time method in the Virus class
        and sets the virus colour based on how long the individual has had the virus(lighter shades of red). Once the duration
        has reached 0, the individual will called into the cured method"""
        self.virus.duration -= 1
        #updates the colour to a lighter tint based on the duration
        
        if self.virus.duration <= 50:
            self.virus.colour = "tomato"
        elif self.virus.duration <= 30:
            self.virus.colour = "light salmon"
        #when the duration is 0, it executes the cured method
        elif self.virus.duration <= 0:
            self.cured(people, infected)  

    #Updates the person each hour.
    #- moves each person by calling the move method
    #- if the destination is reached then set a new destination
    #- progress any illness
    def update(self, people = None, infected = None):
        """updates the move method and checks if the individual has reached the proposed destination by calling the reached_destination
        method. If returned True the individual will receive a new destination by calling the _get_random_destination method.
        Progresses illnesses if there is an infected"""
        #people and infected are also parameters because we have to manipulate the worlds list of infected and non-infected
        self.move()
        if self.reached_destination() == True:
            self.destination = self._get_random_location()
        if self.infected == True:
            self.progress_illness(people, infected)
        
    #moves person towards the destination
    def move(self):
        """Moves the turtle(individual)half a self.radius closer to the proposed destination and sets its old location as its new one"""
        turtle.goto(self.location)
        angle = turtle.towards(self.destination)
        turtle.setheading(angle)
        turtle.forward(self.radius / 2)
        self.location = turtle.position()

    #cures the person of infection. Edits the worlds people and infections, so those parameters are passed into the method too  
    def cured(self, people, infected):
        """adds the individual back to the list of non-infected people, and removed it from the list of infected"""
        try:
            people += [self]
            infected.remove(self)
            self.infected = False
        except TypeError:
            #this part will remove an error that occurs when you have an infected going through the duration update,
            #after all infected have been cured
            pass
      
class World:
    def __init__(self, width, height, n):
        self.size = (width, height)
        self.hours = 0
        self.infected = []
        self.people = []
        number_of_infected = 0
        for i in range (n):
            self.add_person()
            
    #add a person to the list
    def add_person(self):
        """Generates a person to the list of people"""
        self.people += [Person(self.size)]
        return self.people

    #choose a random person to infect and infect with a Virus
    def infect_person(self):
        """generates a number between 0 and 199 and changes the non-infected to infected based on the random number indexed to non-infected
        the infected person will be passed in the infected method in the Person method, with a colour red and a duration of 300 (as assumed)"""
        random_number = random.randint(0, len(self.people) - 1)
        #len(self.people) - 1 because the list has a length of 200, while the index max of the list is 199
        Person.infect(self.people[random_number], ("red", 300))
        self.infected += [self.people[random_number]]
        self.people.pop(random_number)
        

    #remove all infections from all people
    def cure_all(self):
        "when c is pressed, all the infected will be turned to non-infected"
        for people in self.infected:
            self.people += [people]
            
        for people in self.people:
            if people in self.infected:
                self.infected.remove(people)
        
    #Part C check for collisions and pass infection to other people
    def update_infections_slow(self):
        """loops through the infected and checks if there are any collisions by calling the Collisions_list in the Persons class, the returned
        class of collisions will all be turned into infected by calling the infect method in the Persons class if theyre not already an infected.
        This means that if there is a collision and both are infected, they will retain their current durations. Durations of the virus are set to 300
        implemented ticks with a red colour virus"""
        for people in self.infected:
            collisions = Person.collision_list(people, self.people)
        for people in collisions:
            if people not in self.infected:
                people.infect(("red", 300))
                self.infected += [people]
            
    #Part D make the collision detection faster
    def update_infections_fast(self):
        pass
                    
    #simulate one hour in the world.
    #- increase hours passed.
    #- update all people
    #- update all infection transmissions
    def simulate(self):
        """Every implemented tick, the code will increase the hour by 1, update the list of non-infected, the list of infected and check collisions
        if there is an infected"""
        
        self.hours += 1
        for people in self.people:
            Person.update(people)
            
        for people in self.infected:
            Person.update(people, self.people, self.infected)
            
        #checks collision if there is an infected   
        if len(self.infected) >= 1:
            self.update_infections_slow()

    #Draw the world.  Perform the following tasks:
    #   - clear the current screen
    #   - draw all the people
    #   - draw the box that frames the world
    #   - write the number of hours and number of people infected at the top of the frame
    def draw(self):
        """This method will clear the current screen, draw all the individual people, the frame of the world and finally display the number of hours
        and number of infected by calling the count_infected method"""
        
        turtle.clear()
        
        # draws the people in list of self.people
        for people in self.people:
            Person.draw(people, "black")
            
        # draws all the peopple who have been infected
        for people in self.infected:
            Person.draw(people, people.virus.colour)
            
        #Positions the turtle to the top of the box
        turtle.home()
        turtle.penup()
        turtle.setheading(0)
        turtle.forward(self.size[1]/2)
        turtle.left(90)
        turtle.forward(self.size[0]/2)
        turtle.left(90)
        
        #draws the fram of the world
        turtle.pendown()
        for i in range (4):
            if i % 2 == 0:
                turtle.forward(self.size[1])
            else:
                turtle.forward(self.size[0])
            turtle.left(90)
        turtle.penup()

        #Prints the total hours of simulation
        turtle.goto(-self.size[0]/2, self.size[1]/2)
        turtle.write("Hours: {}".format(self.hours), align = "left", font = ("Verdana", 10, "bold"))
        turtle.goto(self.size[0] / 2, self.size[1]/2)
        turtle.write("Infected: {}".format(self.count_infected()), align = "right", font = ("Verdana", 10, "bold"))
        pass

    #Count the number of infected people
    def count_infected(self):
        """updates the number of infected"""
        number_of_infected = len(self.infected)
        return number_of_infected
    
#---------------------------------------------------------
#Should not need to alter any of the code below this line
#---------------------------------------------------------
class GraphicalWorld:
    """ Handles the user interface for the simulation

    space - starts and stops the simulation
    'z' - resets the application to the initial state
    'x' - infects a random person
    'c' - cures all the people
    """
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.TITLE = 'COMPSCI 130 Project One'
        self.MARGIN = 50 #gap around each side
        self.PEOPLE = 200 #number of people in the simulation
        self.framework = AnimationFramework(self.WIDTH, self.HEIGHT, self.TITLE)
        
        self.framework.add_key_action(self.setup, 'z') 
        self.framework.add_key_action(self.infect, 'x')
        self.framework.add_key_action(self.cure, 'c')
        self.framework.add_key_action(self.toggle_simulation, ' ') 
        self.framework.add_tick_action(self.next_turn)
        
        self.world = None

    def setup(self):
        """ Reset the simulation to the initial state """
        print('resetting the world')        
        self.framework.stop_simulation()
        self.world = World(self.WIDTH - self.MARGIN * 2, self.HEIGHT - self.MARGIN * 2, self.PEOPLE)
        self.world.draw()
        
    def infect(self):
        """ Infect a person, and update the drawing """
        print('infecting a person')
        self.world.infect_person()
        self.world.draw()

    def cure(self):
        """ Remove infections from all the people """
        print('cured all people')
        self.world.cure_all()
        self.world.draw()

    def toggle_simulation(self):
        """ Starts and stops the simulation """
        if self.framework.simulation_is_running():
            self.framework.stop_simulation()
        else:
            self.framework.start_simulation()           

    def next_turn(self):
        """ Perform the tasks needed for the next animation cycle """
        self.world.simulate()
        self.world.draw()
        
## This is the animation framework
## Do not edit this framework
class AnimationFramework:
    """This framework is used to provide support for animation of
       interactive applications using the turtle library.  There is
       no need to edit any of the code in this framework.
    """
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 1 #smallest delay is 1 millisecond      
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(0, 0) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        turtle.setundobuffer(None)
        self.__animation_loop()

    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def simulation_is_running(self):
        return self.simulation_running
    
    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func):
        self.tick = func

    def __animation_loop(self):
        try:
            if self.simulation_running:
                self.tick()
            turtle.ontimer(self.__animation_loop, self.delay)
        except turtle.Terminator:
            pass


gw = GraphicalWorld()
gw.setup()
turtle.mainloop() #Need this at the end to ensure events handled properly
