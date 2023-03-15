import random
import time

# Constants
INITIAL_WOLVES = 8
INITIAL_MOOSE = 20
WOLF_BIRTH_RATE = 0.3
WOLF_DEATH_RATE = 0.1
MOOSE_BIRTH_RATE = 0.5
MOOSE_DEATH_RATE = 0.2
MAP_SIZE = 25

class IsleRoyaleSimulator:
    def __init__(self, num_years):
        self.num_years = num_years
        self.current_year = 0
        self.wolves = INITIAL_WOLVES
        self.moose = INITIAL_MOOSE
        self.map = [[0 for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
        self.place_species_on_map()

    def place_species_on_map(self):
        # Place wolves on map
        for i in range(self.wolves):
            x = random.randint(0, MAP_SIZE-1)
            y = random.randint(0, MAP_SIZE-1)
            self.map[x][y] = 'W'

        # Place moose on map
        for i in range(self.moose):
            x = random.randint(0, MAP_SIZE-1)
            y = random.randint(0, MAP_SIZE-1)
            # Check if there's already a wolf on this spot
            while self.map[x][y] == 'W':
                x = random.randint(0, MAP_SIZE-1)
                y = random.randint(0, MAP_SIZE-1)
            self.map[x][y] = 'M'

    def run(self):
        while self.current_year < self.num_years:
            print(f"Year {self.current_year}:")
            self.print_map()
            print(f"{self.wolves} wolves, {self.moose} moose")
            self.run_year()
            self.current_year += 1
            time.sleep(0.1)


    def run_year(self):
        # Wolves
        num_wolf_births = int(self.wolves * WOLF_BIRTH_RATE)
        num_wolf_deaths = int(self.wolves * WOLF_DEATH_RATE)
        self.wolves += num_wolf_births - num_wolf_deaths
        self.wolves = max(self.wolves, 0)

        # Moose
        num_moose_births = int(self.moose * MOOSE_BIRTH_RATE)
        num_moose_deaths = int(self.moose * MOOSE_DEATH_RATE)
        self.moose += num_moose_births - num_moose_deaths
        self.moose = max(self.moose, 0)

        # Predation
        predation = min(self.wolves, self.moose)
        self.wolves -= predation
        self.moose -= predation

        # Update map
        self.place_species_on_map()

    def print_map(self):
        for row in self.map:
            for col in row:
                print(col, end=' ')
            print()

# Run the simulation for 10 years
sim = IsleRoyaleSimulator(num_years=10)
sim.run()