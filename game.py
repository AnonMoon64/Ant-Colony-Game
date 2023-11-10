import random
import time

class Game:
    MIN_COLONIES_FOR_ALLIANCES = 10  # Minimum number of colonies for alliances to be allowed
    ALLIANCE_BREAK_PROBABILITY = 0.20 # 0.05  # 5% chance to break an alliance each turn
    RESOURCE_THRESHOLD = 200  # Threshold for resource scarcity

    def __init__(self, num_colonies):  # Add num_colonies as an argument
        self.colonies = []
        self.turn = 0
        self.total_resources = 5000 * num_colonies  # new attribute for total resources
        for i in range(num_colonies):
            self.create_colony(generate_colony_name())

    def create_colony(self, name):
        new_colony = Colony(name, self)
        self.colonies.append(new_colony)

    def next_turn(self):
        self.turn += 1
        if self.turn % 10 == 0:
            self.total_resources += 1000
        for colony in self.colonies:
            colony.attacked_by_this_turn.clear()  # Clear the list at the start of each turn
            colony.create_ant()
            for ant in colony.population:
                # Break alliances randomly, if the colony has grown more than 10% larger than its allies, if an ally attacked this turn, or if resources are scarce
                for ally in list(colony.alliances):  # Use list to create a copy because we might modify the alliances during iteration
                    if random.random() < self.ALLIANCE_BREAK_PROBABILITY or len(colony.population) > 1.2 * len(ally.population) or ally in colony.attacked_by_this_turn or colony.resources < self.RESOURCE_THRESHOLD:
                        colony.break_alliance(ally)
                    elif len(self.colonies) == 2:
                        for colony in self.colonies:
                            colony.break_alliances()
                # Form alliances with smaller colonies if there are enough colonies left
                if len(self.colonies) >= self.MIN_COLONIES_FOR_ALLIANCES:
                    for other_colony in self.colonies:
                        if len(colony.population) < len(other_colony.population) and not colony.is_allied_with(other_colony):
                            if random.random() < 0.2: # 20% chane of forming an alliance
                                colony.form_alliance(other_colony)
                            pass

                ant.gather_resources()
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