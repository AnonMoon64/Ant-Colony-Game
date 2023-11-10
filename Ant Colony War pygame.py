import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1080, 720
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the clock
clock = pygame.time.Clock()

class Ant:
    def __init__(self, colony):
        self.colony = colony
        self.health = 100
        # Random initial x position
        self.x = colony.x + random.randint(-30, 30)  # Spawn the ant near its colony
        self.y = colony.y + random.randint(-30, 30)  # Random initial y position

    def attack(self):
        # Choose a target colony, with a bias towards larger colonies
        if random.random() < 0.5:
            target_colony = max([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)], 
                        key=lambda c: (len(c.population), c.resources), default=None)
        else:
            target_colony = random.choice([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)])
        if target_colony is not None and len(target_colony.population) > 0:
            target_ant = random.choice(target_colony.population)
            damage = random.randint(5, 10)  
            target_ant.health -= damage
            if target_ant.health <= 0:
                target_colony.population.remove(target_ant)
                target_colony.attacked_by_this_turn.append(self.colony)
    
    def gather_resources(self):
        gathered_resources = min(10, self.colony.game.total_resources)
        if random.random() < 0.5 and self.colony.game.total_resources >= gathered_resources:  # 50% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources
        """nearest_resource = min(self.colony.game.resources, key=lambda r: distance(self, r))
        if distance(self, nearest_resource) <= 1:
            # Collect the resource and bring it back to the colony
            self.colony.resources += nearest_resource.amount
            self.colony.game.resources.remove(nearest_resource)
        else:
            # Move towards the nearest resource
            self.x += sign(nearest_resource.x - self.x)
            self.y += sign(nearest_resource.y - self.y)"""

class WorkerAnt(Ant):
    def gather_resources(self):
        gathered_resources = 50
        if random.random() < 0.8 and self.colony.game.total_resources >= gathered_resources:  # 70% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources

class SoldierAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 150  # Soldier ants have more health

    def attack(self):
        # Choose a target colony, with a bias towards larger colonies
        if random.random() < 0.7:
            target_colony = max([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)], 
                        key=lambda c: (len(c.population), c.resources), default=None)
        else:
            target_colony = random.choice([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)])
        if target_colony is not None and len(target_colony.population) > 0:
            target_ant = random.choice(target_colony.population)
            damage = random.randint(20, 40)  
            target_ant.health -= damage
            if target_ant.health <= 0:
                target_colony.population.remove(target_ant)
                target_colony.attacked_by_this_turn.append(self.colony)
                if target_colony.resources > 0:
                    max_gain = 10  # Set a maximum limit to the resources gained
                    gained_resources = min(max_gain, min(3, target_colony.resources))
                    if target_colony.resources >= gained_resources:
                        
                        self.colony.resources += gained_resources  # gain resources
                        target_colony.resources -= gained_resources
                    else:
                        gained_resources = target_colony.resources
                        self.colony.resources += gained_resources  # gain resources
                        target_colony.resources -= gained_resources
    
    def gather_resources(self):
        pass

class ScoutAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 100

    def gather_resources(self):
        gathered_resources = 10 # Scout ants gather more resources
        if random.random() < 0.3 and self.colony.game.total_resources >= gathered_resources:  # 30% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources

class CaretakerAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 200  # Caretaker ants have less health
    
    def heal(self):
        for ant in self.colony.population:
            if ant.health < 100:
                ant.health += 20
                break

    def attack(self):
        pass

    def gather_resources(self):
        pass

class Colony:
    MAX_ALLIES = 3  # Maximum number of allies a colony can have
    def __init__(self, name, game):
        self.name = name
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Assign a random color
        self.x = random.randint(0, WIDTH)  # Random initial x position
        self.y = random.randint(0, HEIGHT)  # Random initial y position
        self.subcolonies = []  # List to store subcolonies
        self.population = []
        self.resources = 2000
        self.game = game
        self.alliances = []
        self.attacked_by_this_turn = []  # New attribute to track attacks

    def is_allied_with(self, other_colony):
        return other_colony in self.alliances

    def form_alliance(self, other_colony):
        if len(self.population) < len(other_colony.population) and not self.is_allied_with(other_colony) and len(self.alliances) < self.MAX_ALLIES:
            self.alliances.append(other_colony)
            other_colony.alliances.append(self)

    def break_alliance(self, other_colony):
        if self.is_allied_with(other_colony):
            self.alliances.remove(other_colony)
            other_colony.alliances.remove(self)

    @property
    def capacity(self):
        return len(self.subcolonies) * 4
    
    def create_subcolony(self):
        SUBCOLONY_COST = 500
        if self.resources >= SUBCOLONY_COST:  # Check if the colony has enough resources
            new_subcolony = Colony(f"{self.name} Subcolony {len(self.subcolonies) + 1}", self.game)
            new_subcolony.x = self.x + random.randint(-80, 80)  # Position the subcolony near the main colony
            new_subcolony.y = self.y + random.randint(-80, 80)
            self.subcolonies.append(new_subcolony)
            self.resources -= SUBCOLONY_COST

    def create_ant(self):
        if len(self.population) < self.capacity and random.random() < 0.8:  
            ant_type = random.choice([WorkerAnt, SoldierAnt, ScoutAnt, CaretakerAnt])
            base_cost = {WorkerAnt: 20, SoldierAnt: 50, ScoutAnt: 10, CaretakerAnt: 35}[ant_type]

            soldier_ants = len([ant for ant in self.population if isinstance(ant, SoldierAnt)])
            new_ant_cost = base_cost + soldier_ants * 2

            if self.resources >= new_ant_cost:
                # Create an ant for the main colony
                new_ant = ant_type(self)
                self.population.append(new_ant)
                self.resources -= new_ant_cost

                # Create an ant for each subcolony
                for subcolony in self.subcolonies:
                    new_subcolony_ant = ant_type(subcolony)
                    new_subcolony_ant.x = subcolony.x + random.randint(-10, 10)  # Spawn the ant near its subcolony
                    new_subcolony_ant.y = subcolony.y + random.randint(-10, 10)
                    subcolony.population.append(new_subcolony_ant)

class Game:
    MIN_COLONIES_FOR_ALLIANCES = 10  # Minimum number of colonies for alliances to be allowed
    ALLIANCE_BREAK_PROBABILITY = 0.05 # 0.05  # 5% chance to break an alliance each turn
    RESOURCE_THRESHOLD = 300  # Threshold for resource scarcity

    def __init__(self, num_colonies):  
        self.colonies = []
        self.turn = 0
        self.total_resources = 1000 * num_colonies  
        for i in range(num_colonies):
            colony = self.create_colony(f"Colony{i+1}")
        for colony in self.colonies:
            colony.create_subcolony()

    class resource:
        def __init__(self, game):
            self.game = game
            self.x = random.randint(0, WIDTH)  # Random initial x position
            self.y = random.randint(0, HEIGHT)  # Random initial y position
            self.amount = random.randint(1, 10)  # Random initial amount

    def create_colony(self, name):
        new_colony = Colony(name, self)
        self.colonies.append(new_colony)

    def next_turn(self):
        self.turn += 1

        # Add resources back to the world every 10 turns
        if self.turn % 10 == 0:
            self.total_resources += 5000
            pass

        for colony in self.colonies:
            colony.attacked_by_this_turn.clear()  # Clear the list at the start of each turn

            # Create a new subcolony if the number of subcolonies is less than a fifth of the population
            if len(colony.subcolonies) < len(colony.population) / 2:
                colony.create_subcolony()

            # Create an ant for each subcolony
            colony.create_ant()

            # Break alliances randomly, if the colony has grown more than 10% larger than its allies, if an ally attacked this turn, or if resources are scarce
            for ally in list(colony.alliances):  # Use list to create a copy because we might modify the alliances during iteration
                if random.random() < self.ALLIANCE_BREAK_PROBABILITY or len(colony.population) > 1.2 * len(ally.population) or ally in colony.attacked_by_this_turn or colony.resources < self.RESOURCE_THRESHOLD:
                    colony.break_alliance(ally)
                elif len(self.colonies) <= 3:
                    for colony in self.colonies:
                        colony.break_alliances()
            
            # Form alliances with smaller colonies if there are enough colonies left
            if len(self.colonies) >= self.MIN_COLONIES_FOR_ALLIANCES:
                for other_colony in self.colonies:
                    if len(colony.population) < len(other_colony.population) and not colony.is_allied_with(other_colony):
                        if random.random() < 0.2: # 20% chance of forming an alliance
                            colony.form_alliance(other_colony)
                        pass
            
            for ant in colony.population:
                ant.gather_resources()
                if len([c for c in self.colonies if c != colony and len(c.population) > 0]) > 0:
                    ant.attack()
                if isinstance(ant, CaretakerAnt):
                    ant.heal()
        
        # Remove colonies with no ants left
        self.colonies = [colony for colony in self.colonies if len(colony.population) > 0]
        # Check for win condition
        if len(self.colonies) == 1:
            print(f"{self.colonies[0].name} is the winner!")
            return False
        return True

# Initialize game with a number of colonies between 2 and 100
num_colonies = random.randint(30, 50)
game = Game(num_colonies)

while True:
    if not game.next_turn():
        break

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Drawing
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Draw your resources here
    for res in game.resource:
        pygame.draw.circle(screen, (255, 255, 255), (res.x, res.y), 3)

    # Draw your colonies and ants here
    for colony in game.colonies:
        # Draw the main colony as a square
        pygame.draw.rect(screen, colony.color, pygame.Rect(colony.x, colony.y, 20, 20))
        
        # Draw the subcolonies as smaller squares
        for subcolony in colony.subcolonies:
            pygame.draw.rect(screen, colony.color, pygame.Rect(subcolony.x, subcolony.y, 10, 10))

        # Draw the ants as circles
        for ant in colony.population:
            pygame.draw.circle(screen, colony.color, (ant.x, ant.y), 5)
    
    # time.sleep(0.5)

    print(f"Turn {game.turn}")
    for colony in game.colonies:
        worker_ants = len([ant for ant in colony.population if isinstance(ant, WorkerAnt)])
        soldier_ants = len([ant for ant in colony.population if isinstance(ant, SoldierAnt)])
        scout_ants = len([ant for ant in colony.population if isinstance(ant, ScoutAnt)])
        caretaker_ants = len([ant for ant in colony.population if isinstance(ant, CaretakerAnt)])
        print(f"{colony.name} has {len(colony.population)} ants ("
            f"Worker: {worker_ants:<1}. "
            f"Soldier: {soldier_ants:<1}. "
            f"Scout: {scout_ants:<1}. "
            f"Caretaker: {caretaker_ants:<1}. "
            f"capacity {colony.capacity:<1}. "
            f"and colony resources {colony.resources:<1}. "
            f"total world resources {colony.game.total_resources:<1} resources.")

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)